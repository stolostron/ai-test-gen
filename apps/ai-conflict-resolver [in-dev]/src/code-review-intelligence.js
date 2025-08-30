const Anthropic = require('@anthropic-ai/sdk');
const { parse } = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const { execSync } = require('child_process');

class CodeReviewIntelligence {
  constructor(config) {
    this.config = config;
    this.claude = new Anthropic({
      apiKey: config.claude.apiKey,
    });
    
    this.model = config.claude.model || 'claude-3-opus-20240229';
    this.maxTokens = config.claude.maxTokens || 8192;
    
    // Review configuration
    this.reviewConfig = {
      testCoverageThreshold: config.review?.testCoverageThreshold || 85,
      complexityThreshold: config.review?.complexityThreshold || 10,
      duplicateCodeThreshold: config.review?.duplicateCodeThreshold || 5,
      securityScanEnabled: config.review?.securityScanEnabled !== false,
    };
  }

  async reviewPullRequest({ pullRequest, context, repository, octokit }) {
    console.log(`Starting comprehensive PR review for #${pullRequest.number}`);

    try {
      // Get PR diff and files
      const files = await this.getPRFiles({ pullRequest, repository, octokit });
      
      // Perform multi-stage analysis
      const [
        implementationReview,
        testAnalysis,
        securityReview,
        performanceReview,
        codeQualityMetrics,
      ] = await Promise.all([
        this.reviewImplementation({ files, context, pullRequest }),
        this.analyzeTestCoverage({ files, context, repository }),
        this.performSecurityScan({ files, context }),
        this.analyzePerformance({ files, context }),
        this.calculateCodeMetrics({ files }),
      ]);

      // Generate improvement suggestions
      const suggestions = await this.generateImprovementSuggestions({
        implementationReview,
        testAnalysis,
        securityReview,
        performanceReview,
        codeQualityMetrics,
        context,
      });

      // Calculate overall health score
      const healthScore = this.calculateHealthScore({
        implementationReview,
        testAnalysis,
        securityReview,
        performanceReview,
        codeQualityMetrics,
      });

      // Generate comprehensive report
      const report = await this.generateReviewReport({
        pullRequest,
        repository,
        healthScore,
        implementationReview,
        testAnalysis,
        securityReview,
        performanceReview,
        codeQualityMetrics,
        suggestions,
        context,
      });

      return {
        success: true,
        healthScore,
        report,
        suggestions,
        metrics: {
          filesReviewed: files.length,
          criticalIssues: suggestions.filter(s => s.priority === 'critical').length,
          testCoverage: testAnalysis.coverage,
          securityIssues: securityReview.vulnerabilities.length,
        },
      };

    } catch (error) {
      console.error('Error during PR review:', error);
      throw error;
    }
  }

  async reviewImplementation({ files, context, pullRequest }) {
    const systemPrompt = this.buildImplementationReviewPrompt();
    const userPrompt = this.buildImplementationAnalysisPrompt({ files, context, pullRequest });

    const response = await this.claude.messages.create({
      model: this.model,
      max_tokens: this.maxTokens,
      system: systemPrompt,
      messages: [{ role: 'user', content: userPrompt }],
    });

    return this.parseImplementationReview(response.content[0].text);
  }

  async analyzeTestCoverage({ files, context, repository }) {
    // Identify test files and source files
    const testFiles = files.filter(f => 
      f.filename.includes('test') || 
      f.filename.includes('spec') ||
      f.filename.includes('cypress')
    );
    
    const sourceFiles = files.filter(f => 
      !testFiles.includes(f) && 
      (f.filename.endsWith('.js') || f.filename.endsWith('.jsx') || 
       f.filename.endsWith('.ts') || f.filename.endsWith('.tsx'))
    );

    // Analyze test coverage
    const coverageAnalysis = await this.analyzeCoverageGaps({
      testFiles,
      sourceFiles,
      context,
    });

    // Suggest missing tests
    const testSuggestions = await this.suggestMissingTests({
      sourceFiles,
      existingTests: testFiles,
      context,
    });

    return {
      coverage: coverageAnalysis.percentage,
      gaps: coverageAnalysis.gaps,
      suggestions: testSuggestions,
      testQuality: await this.assessTestQuality(testFiles),
    };
  }

  async performSecurityScan({ files, context }) {
    const securityPrompt = this.buildSecurityScanPrompt();
    const fileContents = files.map(f => ({
      path: f.filename,
      content: f.patch || '',
      additions: f.additions,
    }));

    const response = await this.claude.messages.create({
      model: this.model,
      max_tokens: this.maxTokens,
      system: securityPrompt,
      messages: [{
        role: 'user',
        content: `Perform security analysis on these changes:\n${JSON.stringify(fileContents, null, 2)}`
      }],
    });

    return this.parseSecurityFindings(response.content[0].text);
  }

  async analyzePerformance({ files, context }) {
    const performanceIssues = [];
    
    for (const file of files) {
      if (file.patch) {
        const issues = await this.detectPerformanceIssues(file);
        performanceIssues.push(...issues);
      }
    }

    // Use AI to analyze complex performance patterns
    if (performanceIssues.length > 0 || files.length > 0) {
      const aiPerformanceAnalysis = await this.getAIPerformanceAnalysis({ files, context });
      performanceIssues.push(...aiPerformanceAnalysis);
    }

    return {
      issues: performanceIssues,
      optimizationSuggestions: await this.generateOptimizationSuggestions(performanceIssues),
    };
  }

  async calculateCodeMetrics({ files }) {
    const metrics = {
      totalLines: 0,
      addedLines: 0,
      deletedLines: 0,
      complexity: [],
      duplication: [],
      maintainabilityIndex: 100,
    };

    for (const file of files) {
      metrics.addedLines += file.additions;
      metrics.deletedLines += file.deletions;
      
      if (file.patch && this.isJavaScriptFile(file.filename)) {
        const complexity = this.calculateComplexity(file.patch);
        if (complexity > this.reviewConfig.complexityThreshold) {
          metrics.complexity.push({
            file: file.filename,
            complexity,
            threshold: this.reviewConfig.complexityThreshold,
          });
        }
      }
    }

    metrics.totalLines = metrics.addedLines + metrics.deletedLines;
    metrics.maintainabilityIndex = this.calculateMaintainabilityIndex(metrics);

    return metrics;
  }

  async generateImprovementSuggestions({ 
    implementationReview, 
    testAnalysis, 
    securityReview, 
    performanceReview, 
    codeQualityMetrics,
    context 
  }) {
    const allIssues = [
      ...this.extractImplementationIssues(implementationReview),
      ...this.extractTestIssues(testAnalysis),
      ...this.extractSecurityIssues(securityReview),
      ...this.extractPerformanceIssues(performanceReview),
      ...this.extractQualityIssues(codeQualityMetrics),
    ];

    // Use AI to generate contextual suggestions
    const aiSuggestions = await this.getAISuggestions({
      issues: allIssues,
      context,
    });

    // Combine and prioritize suggestions
    const suggestions = this.prioritizeSuggestions([...allIssues, ...aiSuggestions]);

    return suggestions;
  }

  calculateHealthScore({ 
    implementationReview, 
    testAnalysis, 
    securityReview, 
    performanceReview, 
    codeQualityMetrics 
  }) {
    const weights = {
      implementation: 0.25,
      testing: 0.25,
      security: 0.20,
      performance: 0.15,
      codeQuality: 0.15,
    };

    const scores = {
      implementation: implementationReview.score || 85,
      testing: Math.min(100, (testAnalysis.coverage / this.reviewConfig.testCoverageThreshold) * 100),
      security: securityReview.vulnerabilities.length === 0 ? 100 : Math.max(0, 100 - (securityReview.vulnerabilities.length * 20)),
      performance: performanceReview.issues.length === 0 ? 100 : Math.max(0, 100 - (performanceReview.issues.length * 15)),
      codeQuality: codeQualityMetrics.maintainabilityIndex,
    };

    const overallScore = Object.keys(weights).reduce((total, key) => {
      return total + (scores[key] * weights[key]);
    }, 0);

    return Math.round(overallScore);
  }

  async generateReviewReport({ 
    pullRequest, 
    repository, 
    healthScore, 
    implementationReview,
    testAnalysis,
    securityReview,
    performanceReview,
    codeQualityMetrics,
    suggestions,
    context 
  }) {
    const report = {
      summary: this.generateExecutiveSummary({
        pullRequest,
        healthScore,
        suggestions,
        testAnalysis,
        securityReview,
      }),
      detailedAnalysis: {
        implementation: this.formatImplementationReview(implementationReview),
        testing: this.formatTestAnalysis(testAnalysis),
        security: this.formatSecurityReview(securityReview),
        performance: this.formatPerformanceReview(performanceReview),
        codeQuality: this.formatCodeQualityMetrics(codeQualityMetrics),
      },
      suggestions: this.formatSuggestions(suggestions),
      metrics: {
        healthScore,
        testCoverage: testAnalysis.coverage,
        criticalIssues: suggestions.filter(s => s.priority === 'critical').length,
        totalSuggestions: suggestions.length,
      },
    };

    // Generate markdown report
    const markdownReport = await this.generateMarkdownReport(report);

    return {
      ...report,
      markdown: markdownReport,
    };
  }

  // Helper methods

  buildImplementationReviewPrompt() {
    return `You are an expert code reviewer specializing in QE automation. 
Your task is to review code implementations for:
1. Correctness and alignment with requirements
2. Best practices and design patterns
3. Error handling and edge cases
4. Code organization and structure
5. Integration with existing codebase

Provide specific, actionable feedback with code examples where appropriate.`;
  }

  buildImplementationAnalysisPrompt({ files, context, pullRequest }) {
    return `Review this pull request implementation:

PR Title: ${pullRequest.title}
PR Description: ${pullRequest.body || 'No description provided'}

JIRA Context:
${context.jiraTickets.map(t => `- ${t.key}: ${t.summary}\n  Requirements: ${t.acceptanceCriteria}`).join('\n')}

Files Changed:
${files.map(f => `- ${f.filename} (+${f.additions} -${f.deletions})`).join('\n')}

Code Changes:
${files.map(f => `
File: ${f.filename}
\`\`\`diff
${f.patch || 'Binary file or no patch available'}
\`\`\`
`).join('\n')}

Please analyze:
1. Does the implementation meet the requirements?
2. Are there any logic errors or bugs?
3. Is error handling comprehensive?
4. Does it follow team patterns and best practices?
5. Are there any architectural concerns?

Provide your analysis in JSON format:
{
  "score": <0-100>,
  "requirementAlignment": {
    "meets": <boolean>,
    "gaps": ["gap1", "gap2"],
    "suggestions": ["suggestion1", "suggestion2"]
  },
  "codeQuality": {
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "improvements": ["improvement1", "improvement2"]
  },
  "bugs": [
    {
      "severity": "high|medium|low",
      "description": "...",
      "location": "file:line",
      "suggestion": "..."
    }
  ],
  "architecturalConcerns": ["concern1", "concern2"]
}`;
  }

  async getPRFiles({ pullRequest, repository, octokit }) {
    const { data: files } = await octokit.pulls.listFiles({
      owner: repository.owner.login,
      repo: repository.name,
      pull_number: pullRequest.number,
      per_page: 100,
    });

    // For large files, get the full content
    for (const file of files) {
      if (file.patch === undefined && file.status !== 'removed') {
        try {
          const { data: content } = await octokit.repos.getContent({
            owner: repository.owner.login,
            repo: repository.name,
            path: file.filename,
            ref: pullRequest.head.sha,
          });
          
          if (content.content) {
            file.content = Buffer.from(content.content, 'base64').toString();
          }
        } catch (error) {
          console.warn(`Could not fetch content for ${file.filename}:`, error.message);
        }
      }
    }

    return files;
  }

  calculateComplexity(code) {
    try {
      const ast = parse(code, {
        sourceType: 'module',
        plugins: ['jsx', 'typescript'],
        errorRecovery: true,
      });

      let complexity = 1;
      
      traverse(ast, {
        IfStatement() { complexity++; },
        ConditionalExpression() { complexity++; },
        LogicalExpression({ node }) {
          if (node.operator === '&&' || node.operator === '||') {
            complexity++;
          }
        },
        ForStatement() { complexity++; },
        WhileStatement() { complexity++; },
        DoWhileStatement() { complexity++; },
        CatchClause() { complexity++; },
        SwitchCase() { complexity++; },
      });

      return complexity;
    } catch (error) {
      console.warn('Error calculating complexity:', error.message);
      return 0;
    }
  }

  isJavaScriptFile(filename) {
    return /\.(js|jsx|ts|tsx)$/.test(filename);
  }

  async detectPerformanceIssues(file) {
    const issues = [];
    const patch = file.patch || '';

    // Common performance antipatterns
    const patterns = [
      {
        pattern: /\.forEach\([^)]+\)[\s\S]*?\.forEach/,
        issue: 'Nested forEach loops can cause O(n²) complexity',
        severity: 'medium',
      },
      {
        pattern: /await[\s\S]+?for[\s\S]+?await/,
        issue: 'Await inside loops causes sequential execution',
        severity: 'high',
      },
      {
        pattern: /document\.querySelector[\s\S]+?forEach/,
        issue: 'DOM queries inside loops are expensive',
        severity: 'high',
      },
      {
        pattern: /setState[\s\S]{0,50}setState/,
        issue: 'Multiple setState calls should be batched',
        severity: 'medium',
      },
    ];

    patterns.forEach(({ pattern, issue, severity }) => {
      if (pattern.test(patch)) {
        issues.push({
          file: file.filename,
          issue,
          severity,
          type: 'performance',
        });
      }
    });

    return issues;
  }

  prioritizeSuggestions(suggestions) {
    const priorityOrder = {
      'critical': 0,
      'high': 1,
      'medium': 2,
      'low': 3,
    };

    return suggestions
      .sort((a, b) => {
        return (priorityOrder[a.priority] || 3) - (priorityOrder[b.priority] || 3);
      })
      .slice(0, 20); // Limit to top 20 suggestions
  }

  generateExecutiveSummary({ pullRequest, healthScore, suggestions, testAnalysis, securityReview }) {
    const criticalCount = suggestions.filter(s => s.priority === 'critical').length;
    const status = healthScore >= 90 ? '✅ Excellent' : 
                   healthScore >= 75 ? '🟢 Good' :
                   healthScore >= 60 ? '🟡 Needs Improvement' : '🔴 Poor';

    return `
## 📊 PR Review Summary

**PR**: #${pullRequest.number} - ${pullRequest.title}
**Overall Health Score**: ${healthScore}/100 ${status}
**Test Coverage**: ${testAnalysis.coverage}%
**Critical Issues**: ${criticalCount}
**Total Suggestions**: ${suggestions.length}

### 🎯 Key Findings
${criticalCount > 0 ? `- ⚠️ ${criticalCount} critical issues require immediate attention` : '- ✅ No critical issues found'}
${testAnalysis.coverage < this.reviewConfig.testCoverageThreshold ? `- ⚠️ Test coverage (${testAnalysis.coverage}%) is below threshold (${this.reviewConfig.testCoverageThreshold}%)` : '- ✅ Test coverage meets requirements'}
${securityReview.vulnerabilities.length > 0 ? `- ⚠️ ${securityReview.vulnerabilities.length} security vulnerabilities detected` : '- ✅ No security vulnerabilities found'}
    `.trim();
  }

  async generateMarkdownReport(report) {
    const sections = [
      report.summary,
      '\n## 📋 Detailed Analysis\n',
      report.detailedAnalysis.implementation,
      report.detailedAnalysis.testing,
      report.detailedAnalysis.security,
      report.detailedAnalysis.performance,
      report.detailedAnalysis.codeQuality,
      '\n## 💡 Improvement Suggestions\n',
      report.suggestions,
      '\n## 📊 Metrics\n',
      `- **Health Score**: ${report.metrics.healthScore}/100`,
      `- **Test Coverage**: ${report.metrics.testCoverage}%`,
      `- **Critical Issues**: ${report.metrics.criticalIssues}`,
      `- **Total Suggestions**: ${report.metrics.totalSuggestions}`,
    ];

    return sections.join('\n');
  }

  // Parse helper methods
  parseImplementationReview(response) {
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
    } catch (error) {
      console.error('Error parsing implementation review:', error);
    }
    
    return {
      score: 75,
      requirementAlignment: { meets: true, gaps: [], suggestions: [] },
      codeQuality: { strengths: [], weaknesses: [], improvements: [] },
      bugs: [],
      architecturalConcerns: [],
    };
  }

  parseSecurityFindings(response) {
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        return {
          vulnerabilities: parsed.vulnerabilities || [],
          recommendations: parsed.recommendations || [],
        };
      }
    } catch (error) {
      console.error('Error parsing security findings:', error);
    }
    
    return { vulnerabilities: [], recommendations: [] };
  }

  // Additional helper methods would go here...
}

module.exports = { CodeReviewIntelligence };

