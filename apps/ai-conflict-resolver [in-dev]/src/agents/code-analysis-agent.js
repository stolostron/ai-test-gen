const winston = require('winston');
const { Anthropic } = require('@anthropic-ai/sdk');

class CodeAnalysisAgent {
  constructor(config, octokit) {
    this.config = config;
    this.octokit = octokit;
    this.anthropic = new Anthropic({
      apiKey: config.claudeApiKey
    });
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
      ),
      defaultMeta: { component: 'CodeAnalysisAgent' }
    });
  }

  async analyzeImplementation(pr, featureContext, codebaseKnowledge) {
    this.logger.info('Starting code analysis', {
      pr_number: pr.number,
      repository: pr.base.repo.full_name,
      feature_complexity: featureContext.analysis?.complexity || 'unknown'
    });

    try {
      // Get the actual code changes
      const codeChanges = await this.getCodeChanges(pr);
      
      // Analyze each changed file
      const fileAnalyses = await this.analyzeChangedFiles(codeChanges, codebaseKnowledge, featureContext);
      
      // Generate comprehensive feedback using AI
      const feedback = await this.generateFeedback(fileAnalyses, codebaseKnowledge, featureContext);
      
      // Calculate overall health score
      const healthScore = this.calculateHealthScore(feedback);
      
      this.logger.info('Code analysis completed', {
        pr_number: pr.number,
        files_analyzed: fileAnalyses.length,
        feedback_items: feedback.suggestions?.length || 0,
        health_score: healthScore
      });

      return {
        success: true,
        feedback,
        healthScore,
        fileAnalyses,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      this.logger.error('Code analysis failed', {
        pr_number: pr.number,
        error: error.message,
        stack: error.stack
      });
      throw error;
    }
  }

  async getCodeChanges(pr) {
    try {
      const filesResponse = await this.octokit.pulls.listFiles({
        owner: pr.base.repo.owner.login,
        repo: pr.base.repo.name,
        pull_number: pr.number
      });

      const changes = [];
      for (const file of filesResponse.data) {
        if (file.status !== 'removed' && file.patch) {
          changes.push({
            filename: file.filename,
            status: file.status,
            additions: file.additions,
            deletions: file.deletions,
            changes: file.changes,
            patch: file.patch,
            content: await this.getFileContent(pr, file.filename),
            language: this.detectLanguage(file.filename)
          });
        }
      }

      return changes;
    } catch (error) {
      this.logger.error('Failed to get code changes', {
        pr_number: pr.number,
        error: error.message
      });
      return [];
    }
  }

  async getFileContent(pr, filename) {
    try {
      const response = await this.octokit.repos.getContent({
        owner: pr.base.repo.owner.login,
        repo: pr.base.repo.name,
        path: filename,
        ref: pr.head.sha
      });

      if (response.data.content) {
        return Buffer.from(response.data.content, 'base64').toString('utf8');
      }
    } catch (error) {
      this.logger.debug('Could not get file content', {
        filename,
        error: error.message
      });
    }
    return null;
  }

  detectLanguage(filename) {
    const ext = filename.split('.').pop()?.toLowerCase();
    const languageMap = {
      'js': 'javascript',
      'ts': 'typescript',
      'jsx': 'react',
      'tsx': 'react-typescript',
      'py': 'python',
      'java': 'java',
      'go': 'go',
      'rb': 'ruby',
      'php': 'php',
      'cs': 'csharp',
      'cpp': 'cpp',
      'c': 'c',
      'rs': 'rust'
    };
    
    return languageMap[ext] || 'unknown';
  }

  async analyzeChangedFiles(codeChanges, codebaseKnowledge, featureContext) {
    const analyses = [];

    for (const change of codeChanges) {
      try {
        const analysis = await this.analyzeFile(change, codebaseKnowledge, featureContext);
        analyses.push(analysis);
      } catch (error) {
        this.logger.warn('Failed to analyze file', {
          filename: change.filename,
          error: error.message
        });
        
        // Add basic analysis even if detailed analysis fails
        analyses.push({
          filename: change.filename,
          status: 'error',
          error: error.message,
          basicInfo: {
            additions: change.additions,
            deletions: change.deletions,
            language: change.language
          }
        });
      }
    }

    return analyses;
  }

  async analyzeFile(change, codebaseKnowledge, featureContext) {
    // Perform static analysis first
    const staticAnalysis = this.performStaticAnalysis(change);
    
    // Find relevant existing functions
    const relevantFunctions = this.findRelevantFunctions(change, codebaseKnowledge);
    
    // Identify potential improvements
    const improvements = this.identifyImprovements(change, codebaseKnowledge);
    
    return {
      filename: change.filename,
      language: change.language,
      staticAnalysis,
      relevantFunctions,
      improvements,
      metrics: {
        complexity: this.calculateComplexity(change.content),
        maintainability: this.assessMaintainability(change.content),
        testability: this.assessTestability(change.content)
      }
    };
  }

  performStaticAnalysis(change) {
    const analysis = {
      issues: [],
      patterns: [],
      dependencies: []
    };

    if (!change.content) {
      return analysis;
    }

    // Check for common issues
    const issues = [
      this.checkForHardcodedValues(change.content),
      this.checkForErrorHandling(change.content),
      this.checkForLogging(change.content),
      this.checkForSecurityIssues(change.content),
      this.checkForPerformanceIssues(change.content)
    ].flat().filter(Boolean);

    analysis.issues = issues;

    // Identify patterns
    analysis.patterns = this.identifyCodePatterns(change.content, change.language);

    // Extract dependencies
    analysis.dependencies = this.extractDependencies(change.content, change.language);

    return analysis;
  }

  checkForHardcodedValues(content) {
    const issues = [];
    
    // Check for hardcoded strings that might be configuration
    const hardcodedPatterns = [
      { pattern: /'(http[s]?:\/\/[^']+)'/g, type: 'hardcoded_url' },
      { pattern: /"(http[s]?:\/\/[^"]+)"/g, type: 'hardcoded_url' },
      { pattern: /['"]([A-Z0-9]{20,})['"]/, type: 'potential_key' },
      { pattern: /(?:password|pwd|secret|key)\s*[:=]\s*['"]([^'"]+)['"]/gi, type: 'hardcoded_secret' }
    ];

    hardcodedPatterns.forEach(({ pattern, type }) => {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        issues.push({
          type,
          message: `Potential ${type.replace('_', ' ')} found`,
          line: content.substring(0, match.index).split('\n').length,
          severity: type.includes('secret') ? 'critical' : 'warning'
        });
      }
    });

    return issues;
  }

  checkForErrorHandling(content) {
    const issues = [];
    
    // Check for try-catch blocks
    const tryBlocks = content.match(/try\s*\{/g)?.length || 0;
    const catchBlocks = content.match(/catch\s*\(/g)?.length || 0;
    
    if (tryBlocks > 0 && catchBlocks === 0) {
      issues.push({
        type: 'missing_error_handling',
        message: 'Try block found without corresponding catch block',
        severity: 'warning'
      });
    }

    // Check for unhandled promises
    const promisePattern = /\.then\(/g;
    const catchPattern = /\.catch\(/g;
    const promiseCount = content.match(promisePattern)?.length || 0;
    const catchCount = content.match(catchPattern)?.length || 0;
    
    if (promiseCount > catchCount) {
      issues.push({
        type: 'unhandled_promise',
        message: 'Promise chains should include error handling',
        severity: 'warning'
      });
    }

    return issues;
  }

  checkForLogging(content) {
    const issues = [];
    
    // Check if there's appropriate logging
    const loggingPatterns = [
      /console\.(log|error|warn|info)/g,
      /logger\.(log|error|warn|info|debug)/g,
      /log\.(error|warn|info|debug)/g
    ];

    const hasLogging = loggingPatterns.some(pattern => pattern.test(content));
    const hasErrorHandling = /catch|error/gi.test(content);
    
    if (hasErrorHandling && !hasLogging) {
      issues.push({
        type: 'missing_logging',
        message: 'Error handling detected but no logging found',
        severity: 'suggestion'
      });
    }

    return issues;
  }

  checkForSecurityIssues(content) {
    const issues = [];
    
    const securityPatterns = [
      { pattern: /eval\s*\(/g, type: 'eval_usage', severity: 'critical' },
      { pattern: /innerHTML\s*=/g, type: 'innerHTML_usage', severity: 'warning' },
      { pattern: /document\.write\(/g, type: 'document_write', severity: 'warning' },
      { pattern: /\$\{[^}]*\}/g, type: 'template_literal', severity: 'info' }
    ];

    securityPatterns.forEach(({ pattern, type, severity }) => {
      const matches = content.match(pattern);
      if (matches) {
        issues.push({
          type,
          message: `Potential security concern: ${type.replace('_', ' ')}`,
          count: matches.length,
          severity
        });
      }
    });

    return issues;
  }

  checkForPerformanceIssues(content) {
    const issues = [];
    
    const performancePatterns = [
      { pattern: /for\s*\([^)]*\)\s*\{[^}]*for\s*\(/g, type: 'nested_loops', severity: 'warning' },
      { pattern: /\.find\([^)]*\)[^;]*\.find\(/g, type: 'chained_finds', severity: 'suggestion' },
      { pattern: /new\s+Date\(\)/g, type: 'date_creation', severity: 'info' }
    ];

    performancePatterns.forEach(({ pattern, type, severity }) => {
      const matches = content.match(pattern);
      if (matches && matches.length > 2) {
        issues.push({
          type,
          message: `Performance consideration: ${type.replace('_', ' ')}`,
          count: matches.length,
          severity
        });
      }
    });

    return issues;
  }

  identifyCodePatterns(content, language) {
    const patterns = [];
    
    const commonPatterns = [
      { name: 'singleton', pattern: /class\s+\w+\s*\{[^}]*static\s+instance/gi },
      { name: 'factory', pattern: /create\w*\s*\(/gi },
      { name: 'observer', pattern: /(addEventListener|on\w+|subscribe)/gi },
      { name: 'async_await', pattern: /async\s+\w+|await\s+/gi },
      { name: 'promise_chain', pattern: /\.then\(|\.catch\(/gi },
      { name: 'destructuring', pattern: /const\s*\{[^}]+\}\s*=/gi }
    ];

    commonPatterns.forEach(({ name, pattern }) => {
      const matches = content.match(pattern);
      if (matches && matches.length > 0) {
        patterns.push({
          name,
          count: matches.length,
          confidence: Math.min(matches.length / 3, 1.0)
        });
      }
    });

    return patterns;
  }

  extractDependencies(content, language) {
    const dependencies = [];
    
    if (language === 'javascript' || language === 'typescript') {
      // Extract ES6 imports
      const importPattern = /import\s+.*?\s+from\s+['"]([^'"]+)['"]/g;
      let match;
      while ((match = importPattern.exec(content)) !== null) {
        dependencies.push({
          name: match[1],
          type: 'import'
        });
      }

      // Extract require statements
      const requirePattern = /require\s*\(\s*['"]([^'"]+)['"]\s*\)/g;
      while ((match = requirePattern.exec(content)) !== null) {
        dependencies.push({
          name: match[1],
          type: 'require'
        });
      }
    }

    return dependencies;
  }

  findRelevantFunctions(change, codebaseKnowledge) {
    const relevant = [];
    
    // Simple keyword matching for now
    const changeText = change.content?.toLowerCase() || '';
    
    codebaseKnowledge.knowledge?.existingFunctions?.forEach(func => {
      const funcName = func.name.toLowerCase();
      
      // Check if function name appears in the change
      if (changeText.includes(funcName)) {
        relevant.push({
          ...func,
          relevance: 'name_match',
          suggestion: 'Consider using this existing function'
        });
      }
      
      // Check for similar functionality (basic heuristic)
      const funcWords = funcName.split(/[_-]/);
      const matchingWords = funcWords.filter(word => 
        word.length > 3 && changeText.includes(word)
      );
      
      if (matchingWords.length > 0) {
        relevant.push({
          ...func,
          relevance: 'keyword_match',
          matchingWords,
          suggestion: 'Review if this function provides similar functionality'
        });
      }
    });

    return relevant.slice(0, 10); // Limit results
  }

  identifyImprovements(change, codebaseKnowledge) {
    const improvements = [];
    
    // Check for reusable constants
    if (codebaseKnowledge.knowledge?.constants) {
      const constants = this.findReusableConstants(change, codebaseKnowledge.knowledge.constants);
      improvements.push(...constants);
    }

    // Check for pattern consistency
    const patternSuggestions = this.suggestPatternImprovements(change, codebaseKnowledge);
    improvements.push(...patternSuggestions);

    // Check for utility function opportunities
    const utilityOpportunities = this.identifyUtilityOpportunities(change, codebaseKnowledge);
    improvements.push(...utilityOpportunities);

    return improvements;
  }

  findReusableConstants(change, constants) {
    const suggestions = [];
    
    if (!change.content) return suggestions;
    
    // Look for hardcoded values that match existing constants
    constants.forEach(constant => {
      const pattern = new RegExp(`['"]([^'"]*${constant.name.toLowerCase()}[^'"]*)['"]`, 'gi');
      const matches = change.content.match(pattern);
      
      if (matches) {
        suggestions.push({
          type: 'reuse_constant',
          message: `Consider using existing constant: ${constant.name}`,
          constant: constant.name,
          filepath: constant.filepath,
          severity: 'suggestion'
        });
      }
    });

    return suggestions;
  }

  suggestPatternImprovements(change, codebaseKnowledge) {
    const suggestions = [];
    
    const patterns = codebaseKnowledge.knowledge?.patterns || [];
    
    // Suggest following established patterns
    patterns.forEach(pattern => {
      if (pattern.confidence > 0.7) {
        suggestions.push({
          type: 'follow_pattern',
          message: `Consider following the established ${pattern.name} pattern`,
          pattern: pattern.name,
          usage: pattern.count,
          severity: 'info'
        });
      }
    });

    return suggestions;
  }

  identifyUtilityOpportunities(change, codebaseKnowledge) {
    const opportunities = [];
    
    const utilities = codebaseKnowledge.knowledge?.utilities || [];
    
    // Check if change could benefit from existing utilities
    utilities.forEach(utility => {
      const utilityKeywords = utility.name.toLowerCase().split(/[_-]/);
      
      utilityKeywords.forEach(keyword => {
        if (keyword.length > 3 && change.content?.toLowerCase().includes(keyword)) {
          opportunities.push({
            type: 'use_utility',
            message: `Consider using utility function: ${utility.name}`,
            utility: utility.name,
            filepath: utility.filepath,
            severity: 'suggestion'
          });
        }
      });
    });

    return opportunities.slice(0, 5); // Limit suggestions
  }

  calculateComplexity(content) {
    if (!content) return 0;
    
    // Simple complexity calculation based on control structures
    const complexityPatterns = [
      /if\s*\(/g,
      /for\s*\(/g,
      /while\s*\(/g,
      /switch\s*\(/g,
      /catch\s*\(/g,
      /function\s*\(/g,
      /=>\s*{/g
    ];

    let complexity = 1; // Base complexity
    
    complexityPatterns.forEach(pattern => {
      const matches = content.match(pattern);
      if (matches) {
        complexity += matches.length;
      }
    });

    return Math.min(complexity, 50); // Cap at 50
  }

  assessMaintainability(content) {
    if (!content) return 50;
    
    const lines = content.split('\n').length;
    const commentLines = (content.match(/\/\/|\/\*|\*|#/g) || []).length;
    const commentRatio = commentLines / lines;
    
    let score = 70; // Base score
    
    // Adjust based on comment ratio
    if (commentRatio > 0.1) score += 10;
    if (commentRatio > 0.2) score += 10;
    
    // Adjust based on function length (assuming average function length)
    const avgFunctionLength = lines / ((content.match(/function|=>/g) || []).length || 1);
    if (avgFunctionLength < 20) score += 10;
    if (avgFunctionLength > 50) score -= 10;
    
    return Math.max(0, Math.min(100, score));
  }

  assessTestability(content) {
    if (!content) return 50;
    
    let score = 50; // Base score
    
    // Check for testable patterns
    const testablePatterns = [
      /export\s+(function|const|class)/g, // Exported functions
      /return\s+/g, // Functions that return values
      /async\s+function|async\s+\w+/g // Async functions
    ];

    testablePatterns.forEach(pattern => {
      const matches = content.match(pattern);
      if (matches) {
        score += Math.min(matches.length * 5, 20);
      }
    });

    // Reduce score for hard-to-test patterns
    const difficultPatterns = [
      /document\./g, // DOM manipulation
      /window\./g, // Global window access
      /console\./g // Console usage
    ];

    difficultPatterns.forEach(pattern => {
      const matches = content.match(pattern);
      if (matches) {
        score -= Math.min(matches.length * 3, 15);
      }
    });

    return Math.max(0, Math.min(100, score));
  }

  async generateFeedback(fileAnalyses, codebaseKnowledge, featureContext) {
    const prompt = this.buildFeedbackPrompt(fileAnalyses, codebaseKnowledge, featureContext);
    
    try {
      const response = await this.anthropic.messages.create({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 6144,
        temperature: 0.1, // More deterministic for consistent feedback
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ]
      });

      const feedbackText = response.content[0].text;
      return this.parseFeedbackResponse(feedbackText, fileAnalyses);
    } catch (error) {
      this.logger.error('AI feedback generation failed', {
        error: error.message
      });
      
      // Return basic feedback without AI
      return this.generateBasicFeedback(fileAnalyses);
    }
  }

  buildFeedbackPrompt(fileAnalyses, codebaseKnowledge, featureContext) {
    return `You are an expert code reviewer analyzing a pull request. Your goal is to provide actionable, specific feedback that helps improve code quality and leverages existing codebase patterns.

FEATURE CONTEXT:
Purpose: ${featureContext.analysis?.businessPurpose || 'Not specified'}
Requirements: ${JSON.stringify(featureContext.analysis?.technicalRequirements || [])}

AVAILABLE CODEBASE RESOURCES:
Existing Functions: ${codebaseKnowledge.knowledge?.existingFunctions?.length || 0}
Available Utilities: ${codebaseKnowledge.knowledge?.utilities?.length || 0}
Established Patterns: ${codebaseKnowledge.knowledge?.patterns?.map(p => p.name).join(', ') || 'None identified'}

CODEBASE INSIGHTS:
${JSON.stringify(codebaseKnowledge.insights || {}, null, 2)}

CODE ANALYSIS RESULTS:
${fileAnalyses.map(analysis => `
File: ${analysis.filename}
Language: ${analysis.language}
Complexity: ${analysis.metrics?.complexity || 'Unknown'}
Issues Found: ${analysis.staticAnalysis?.issues?.length || 0}
Relevant Functions Available: ${analysis.relevantFunctions?.length || 0}
Improvement Opportunities: ${analysis.improvements?.length || 0}
`).join('\n')}

DETAILED STATIC ANALYSIS:
${fileAnalyses.map(analysis => `
${analysis.filename}:
- Issues: ${JSON.stringify(analysis.staticAnalysis?.issues || [])}
- Relevant Functions: ${JSON.stringify(analysis.relevantFunctions || [])}
- Improvements: ${JSON.stringify(analysis.improvements || [])}
`).join('\n')}

PROVIDE COMPREHENSIVE FEEDBACK IN JSON FORMAT:
{
  "summary": {
    "overallAssessment": "High-level assessment of the PR",
    "keyFindings": ["Most important findings"],
    "riskLevel": "low|medium|high"
  },
  "suggestions": [
    {
      "type": "reuse_existing|efficiency|logic_flaw|best_practice|security|performance",
      "severity": "critical|warning|suggestion|info",
      "file": "filename",
      "line": 0,
      "title": "Brief title",
      "message": "Detailed explanation",
      "currentCode": "Current implementation",
      "suggestedCode": "Improved implementation",
      "reasoning": "Why this change is beneficial",
      "relatedFunction": "existing_function_name (if applicable)"
    }
  ],
  "positiveFindings": [
    "Things that are well implemented"
  ],
  "testingRecommendations": [
    "Specific testing suggestions based on the implementation"
  ],
  "architecturalNotes": [
    "Comments on how the implementation fits with existing architecture"
  ]
}

FOCUS ON:
1. Opportunities to reuse existing functions/utilities
2. More efficient implementations using existing patterns
3. Potential logic flaws or edge case gaps
4. Security considerations
5. Performance improvements
6. Code maintainability

Be specific and actionable. Include code examples when suggesting improvements.`;
  }

  parseFeedbackResponse(responseText, fileAnalyses) {
    try {
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        
        // Validate and enhance the feedback
        return this.enhanceFeedback(parsed, fileAnalyses);
      }
      
      return this.parseUnstructuredFeedback(responseText, fileAnalyses);
    } catch (error) {
      this.logger.warn('Failed to parse feedback response', {
        error: error.message
      });
      
      return this.generateBasicFeedback(fileAnalyses);
    }
  }

  enhanceFeedback(feedback, fileAnalyses) {
    // Add static analysis issues to suggestions
    fileAnalyses.forEach(analysis => {
      if (analysis.staticAnalysis?.issues) {
        analysis.staticAnalysis.issues.forEach(issue => {
          feedback.suggestions.push({
            type: 'static_analysis',
            severity: issue.severity,
            file: analysis.filename,
            line: issue.line || 0,
            title: issue.type.replace('_', ' '),
            message: issue.message,
            reasoning: 'Detected by static analysis'
          });
        });
      }
    });

    // Sort suggestions by severity
    const severityOrder = { critical: 0, warning: 1, suggestion: 2, info: 3 };
    feedback.suggestions.sort((a, b) => 
      severityOrder[a.severity] - severityOrder[b.severity]
    );

    return feedback;
  }

  parseUnstructuredFeedback(text, fileAnalyses) {
    return {
      summary: {
        overallAssessment: text.substring(0, 200),
        keyFindings: this.extractKeyFindings(text),
        riskLevel: this.determineRiskLevel(text)
      },
      suggestions: this.extractSuggestions(text, fileAnalyses),
      positiveFindings: this.extractPositiveFindings(text),
      testingRecommendations: this.extractTestingRecommendations(text),
      architecturalNotes: this.extractArchitecturalNotes(text),
      rawResponse: text
    };
  }

  extractKeyFindings(text) {
    const findings = [];
    const sentences = text.split(/[.!?]+/);
    
    const importantKeywords = ['critical', 'important', 'issue', 'problem', 'improve', 'recommend'];
    
    sentences.forEach(sentence => {
      if (importantKeywords.some(keyword => sentence.toLowerCase().includes(keyword))) {
        findings.push(sentence.trim());
      }
    });

    return findings.slice(0, 5);
  }

  determineRiskLevel(text) {
    const highRiskWords = ['critical', 'security', 'vulnerability', 'dangerous'];
    const mediumRiskWords = ['warning', 'caution', 'concern', 'issue'];
    
    const lowerText = text.toLowerCase();
    
    if (highRiskWords.some(word => lowerText.includes(word))) return 'high';
    if (mediumRiskWords.some(word => lowerText.includes(word))) return 'medium';
    return 'low';
  }

  extractSuggestions(text, fileAnalyses) {
    const suggestions = [];
    
    // Extract basic suggestions from static analysis
    fileAnalyses.forEach(analysis => {
      if (analysis.staticAnalysis?.issues) {
        analysis.staticAnalysis.issues.forEach(issue => {
          suggestions.push({
            type: 'static_analysis',
            severity: issue.severity,
            file: analysis.filename,
            title: issue.type,
            message: issue.message,
            reasoning: 'Static analysis finding'
          });
        });
      }
    });

    return suggestions;
  }

  extractPositiveFindings(text) {
    const findings = [];
    const sentences = text.split(/[.!?]+/);
    
    const positiveKeywords = ['good', 'well', 'excellent', 'proper', 'correct', 'appropriate'];
    
    sentences.forEach(sentence => {
      if (positiveKeywords.some(keyword => sentence.toLowerCase().includes(keyword))) {
        findings.push(sentence.trim());
      }
    });

    return findings.slice(0, 3);
  }

  extractTestingRecommendations(text) {
    const recommendations = [];
    const sentences = text.split(/[.!?]+/);
    
    sentences.forEach(sentence => {
      if (sentence.toLowerCase().includes('test')) {
        recommendations.push(sentence.trim());
      }
    });

    return recommendations.slice(0, 3);
  }

  extractArchitecturalNotes(text) {
    const notes = [];
    const sentences = text.split(/[.!?]+/);
    
    const architecturalKeywords = ['architecture', 'pattern', 'design', 'structure'];
    
    sentences.forEach(sentence => {
      if (architecturalKeywords.some(keyword => sentence.toLowerCase().includes(keyword))) {
        notes.push(sentence.trim());
      }
    });

    return notes.slice(0, 3);
  }

  generateBasicFeedback(fileAnalyses) {
    const suggestions = [];
    let criticalCount = 0;
    let warningCount = 0;

    fileAnalyses.forEach(analysis => {
      if (analysis.staticAnalysis?.issues) {
        analysis.staticAnalysis.issues.forEach(issue => {
          suggestions.push({
            type: 'static_analysis',
            severity: issue.severity,
            file: analysis.filename,
            line: issue.line || 0,
            title: issue.type.replace('_', ' '),
            message: issue.message,
            reasoning: 'Detected by static analysis'
          });

          if (issue.severity === 'critical') criticalCount++;
          if (issue.severity === 'warning') warningCount++;
        });
      }
    });

    return {
      summary: {
        overallAssessment: `Analyzed ${fileAnalyses.length} files with ${suggestions.length} findings`,
        keyFindings: [`${criticalCount} critical issues`, `${warningCount} warnings`],
        riskLevel: criticalCount > 0 ? 'high' : warningCount > 2 ? 'medium' : 'low'
      },
      suggestions,
      positiveFindings: ['Static analysis completed'],
      testingRecommendations: ['Add tests for new functionality'],
      architecturalNotes: ['Review follows existing patterns'],
      fallback: true
    };
  }

  calculateHealthScore(feedback) {
    let score = 100;

    // Deduct points based on issues
    if (feedback.suggestions) {
      feedback.suggestions.forEach(suggestion => {
        switch (suggestion.severity) {
          case 'critical':
            score -= 20;
            break;
          case 'warning':
            score -= 10;
            break;
          case 'suggestion':
            score -= 3;
            break;
          case 'info':
            score -= 1;
            break;
        }
      });
    }

    // Adjust based on risk level
    switch (feedback.summary?.riskLevel) {
      case 'high':
        score -= 15;
        break;
      case 'medium':
        score -= 5;
        break;
    }

    // Ensure score is between 0 and 100
    return Math.max(0, Math.min(100, score));
  }
}

module.exports = CodeAnalysisAgent;