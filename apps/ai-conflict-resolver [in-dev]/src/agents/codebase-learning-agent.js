const winston = require('winston');
const { Anthropic } = require('@anthropic-ai/sdk');
const path = require('path');
const fs = require('fs').promises;

class CodebaseLearningAgent {
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
      defaultMeta: { component: 'CodebaseLearningAgent' }
    });
    
    // Cache for repository knowledge
    this.repoCache = new Map();
  }

  async learnRelevantCodebase(pr, featureContext) {
    this.logger.info('Starting codebase learning process', {
      pr_number: pr.number,
      repository: pr.base.repo.full_name,
      files_changed: pr.changed_files
    });

    try {
      // Get the files changed in the PR
      const changedFiles = await this.getChangedFiles(pr);
      
      // Find relevant files in the codebase
      const relevantFiles = await this.findRelevantFiles(changedFiles, pr);
      
      // Discover existing functions and patterns
      const codebaseKnowledge = await this.analyzeCodebase(relevantFiles, pr);
      
      // Use AI to generate insights
      const insights = await this.generateInsights(codebaseKnowledge, featureContext);
      
      this.logger.info('Codebase learning completed', {
        pr_number: pr.number,
        relevant_files: relevantFiles.length,
        functions_found: codebaseKnowledge.existingFunctions.length,
        patterns_identified: codebaseKnowledge.patterns.length
      });

      return {
        success: true,
        knowledge: codebaseKnowledge,
        insights,
        relevantFiles,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      this.logger.error('Codebase learning failed', {
        pr_number: pr.number,
        error: error.message,
        stack: error.stack
      });
      throw error;
    }
  }

  async getChangedFiles(pr) {
    try {
      const response = await this.octokit.pulls.listFiles({
        owner: pr.base.repo.owner.login,
        repo: pr.base.repo.name,
        pull_number: pr.number
      });

      return response.data.map(file => ({
        filename: file.filename,
        status: file.status, // added, modified, deleted, renamed
        additions: file.additions,
        deletions: file.deletions,
        changes: file.changes,
        patch: file.patch,
        language: this.detectLanguage(file.filename),
        directory: path.dirname(file.filename),
        basename: path.basename(file.filename)
      }));
    } catch (error) {
      this.logger.error('Failed to get changed files', {
        pr_number: pr.number,
        error: error.message
      });
      return [];
    }
  }

  detectLanguage(filename) {
    const ext = path.extname(filename).toLowerCase();
    const languageMap = {
      '.js': 'javascript',
      '.ts': 'typescript',
      '.jsx': 'react',
      '.tsx': 'react-typescript',
      '.py': 'python',
      '.java': 'java',
      '.go': 'go',
      '.rb': 'ruby',
      '.php': 'php',
      '.cs': 'csharp',
      '.cpp': 'cpp',
      '.c': 'c',
      '.rs': 'rust',
      '.sh': 'shell',
      '.yml': 'yaml',
      '.yaml': 'yaml',
      '.json': 'json',
      '.md': 'markdown'
    };
    
    return languageMap[ext] || 'unknown';
  }

  async findRelevantFiles(changedFiles, pr) {
    const directories = [...new Set(changedFiles.map(f => f.directory))];
    const languages = [...new Set(changedFiles.map(f => f.language))].filter(l => l !== 'unknown');
    
    try {
      // Get repository tree to find related files
      const treeResponse = await this.octokit.git.getTree({
        owner: pr.base.repo.owner.login,
        repo: pr.base.repo.name,
        tree_sha: pr.base.sha,
        recursive: true
      });

      const allFiles = treeResponse.data.tree.filter(item => item.type === 'blob');
      
      // Find files in same directories or with same languages
      const relevantFiles = allFiles.filter(file => {
        const fileDir = path.dirname(file.path);
        const fileLang = this.detectLanguage(file.path);
        
        // Include files in same directories
        if (directories.some(dir => fileDir.startsWith(dir) || dir.startsWith(fileDir))) {
          return true;
        }
        
        // Include files with same language in nearby directories
        if (languages.includes(fileLang)) {
          return true;
        }
        
        // Include common utility/helper files
        if (this.isUtilityFile(file.path)) {
          return true;
        }
        
        return false;
      });

      // Limit the number of files to analyze (performance consideration)
      return relevantFiles.slice(0, 50);
    } catch (error) {
      this.logger.error('Failed to find relevant files', {
        pr_number: pr.number,
        error: error.message
      });
      return [];
    }
  }

  isUtilityFile(filepath) {
    const utilityPatterns = [
      /utils?/i,
      /helpers?/i,
      /common/i,
      /shared/i,
      /lib/i,
      /constants?/i,
      /config/i,
      /types/i,
      /interfaces/i
    ];
    
    return utilityPatterns.some(pattern => pattern.test(filepath));
  }

  async analyzeCodebase(relevantFiles, pr) {
    const knowledge = {
      existingFunctions: [],
      patterns: [],
      existingVars: [],
      architecture: {},
      utilities: [],
      constants: [],
      types: []
    };

    // Analyze a subset of files to avoid overwhelming the system
    const filesToAnalyze = relevantFiles.slice(0, 20);
    
    for (const file of filesToAnalyze) {
      try {
        const content = await this.getFileContent(file, pr);
        if (content) {
          const analysis = this.analyzeFileContent(content, file.path);
          this.mergeAnalysis(knowledge, analysis);
        }
      } catch (error) {
        this.logger.warn('Failed to analyze file', {
          file: file.path,
          error: error.message
        });
      }
    }

    return knowledge;
  }

  async getFileContent(file, pr) {
    try {
      const response = await this.octokit.repos.getContent({
        owner: pr.base.repo.owner.login,
        repo: pr.base.repo.name,
        path: file.path,
        ref: pr.base.sha
      });

      if (response.data.content) {
        return Buffer.from(response.data.content, 'base64').toString('utf8');
      }
    } catch (error) {
      this.logger.debug('Could not get file content', {
        file: file.path,
        error: error.message
      });
    }
    return null;
  }

  analyzeFileContent(content, filepath) {
    const language = this.detectLanguage(filepath);
    
    switch (language) {
      case 'javascript':
      case 'typescript':
        return this.analyzeJavaScriptContent(content, filepath);
      case 'python':
        return this.analyzePythonContent(content, filepath);
      default:
        return this.analyzeGenericContent(content, filepath);
    }
  }

  analyzeJavaScriptContent(content, filepath) {
    const analysis = {
      functions: [],
      variables: [],
      constants: [],
      patterns: [],
      imports: [],
      exports: []
    };

    // Extract function declarations
    const functionPatterns = [
      /function\s+(\w+)\s*\([^)]*\)/g,
      /const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>/g,
      /(\w+)\s*:\s*(?:async\s+)?function/g,
      /async\s+(\w+)\s*\([^)]*\)/g
    ];

    functionPatterns.forEach(pattern => {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        analysis.functions.push({
          name: match[1],
          filepath,
          type: 'function',
          line: content.substring(0, match.index).split('\n').length
        });
      }
    });

    // Extract variable declarations
    const variablePatterns = [
      /(?:const|let|var)\s+(\w+)\s*=/g
    ];

    variablePatterns.forEach(pattern => {
      let match;
      while ((match = pattern.exec(content)) !== null) {
        const name = match[1];
        const isConstant = content.substring(match.index - 10, match.index).includes('const');
        
        if (isConstant && name === name.toUpperCase()) {
          analysis.constants.push({
            name,
            filepath,
            type: 'constant',
            line: content.substring(0, match.index).split('\n').length
          });
        } else {
          analysis.variables.push({
            name,
            filepath,
            type: isConstant ? 'const' : 'variable',
            line: content.substring(0, match.index).split('\n').length
          });
        }
      }
    });

    // Extract imports
    const importPattern = /import\s+.*?\s+from\s+['"]([^'"]+)['"]/g;
    let importMatch;
    while ((importMatch = importPattern.exec(content)) !== null) {
      analysis.imports.push(importMatch[1]);
    }

    // Extract common patterns
    analysis.patterns = this.identifyPatterns(content, 'javascript');

    return analysis;
  }

  analyzePythonContent(content, filepath) {
    const analysis = {
      functions: [],
      variables: [],
      constants: [],
      patterns: [],
      imports: [],
      classes: []
    };

    // Extract function definitions
    const functionPattern = /def\s+(\w+)\s*\([^)]*\):/g;
    let match;
    while ((match = functionPattern.exec(content)) !== null) {
      analysis.functions.push({
        name: match[1],
        filepath,
        type: 'function',
        line: content.substring(0, match.index).split('\n').length
      });
    }

    // Extract class definitions
    const classPattern = /class\s+(\w+)(?:\([^)]*\))?:/g;
    while ((match = classPattern.exec(content)) !== null) {
      analysis.classes.push({
        name: match[1],
        filepath,
        type: 'class',
        line: content.substring(0, match.index).split('\n').length
      });
    }

    // Extract variable assignments
    const variablePattern = /^(\w+)\s*=/gm;
    while ((match = variablePattern.exec(content)) !== null) {
      const name = match[1];
      if (name === name.toUpperCase() && name.length > 1) {
        analysis.constants.push({
          name,
          filepath,
          type: 'constant',
          line: content.substring(0, match.index).split('\n').length
        });
      } else {
        analysis.variables.push({
          name,
          filepath,
          type: 'variable',
          line: content.substring(0, match.index).split('\n').length
        });
      }
    }

    analysis.patterns = this.identifyPatterns(content, 'python');

    return analysis;
  }

  analyzeGenericContent(content, filepath) {
    return {
      functions: [],
      variables: [],
      constants: [],
      patterns: this.identifyPatterns(content, 'generic'),
      metadata: {
        lines: content.split('\n').length,
        size: content.length
      }
    };
  }

  identifyPatterns(content, language) {
    const patterns = [];

    // Common patterns across languages
    const commonPatterns = [
      { name: 'error_handling', regex: /(try|catch|except|error|throw)/gi },
      { name: 'async_patterns', regex: /(async|await|promise|callback)/gi },
      { name: 'validation', regex: /(validate|check|verify|assert)/gi },
      { name: 'logging', regex: /(log|debug|info|warn|error)/gi },
      { name: 'testing', regex: /(test|spec|mock|expect|assert)/gi },
      { name: 'database', regex: /(query|select|insert|update|delete|sql)/gi },
      { name: 'api_calls', regex: /(fetch|request|api|endpoint|http)/gi },
      { name: 'authentication', regex: /(auth|login|token|session|jwt)/gi }
    ];

    commonPatterns.forEach(pattern => {
      const matches = content.match(pattern.regex);
      if (matches && matches.length > 2) { // Only include if pattern appears multiple times
        patterns.push({
          name: pattern.name,
          count: matches.length,
          confidence: Math.min(matches.length / 10, 1.0) // Scale confidence
        });
      }
    });

    return patterns;
  }

  mergeAnalysis(knowledge, analysis) {
    knowledge.existingFunctions.push(...(analysis.functions || []));
    knowledge.existingVars.push(...(analysis.variables || []));
    knowledge.constants.push(...(analysis.constants || []));
    
    // Merge patterns
    analysis.patterns?.forEach(pattern => {
      const existing = knowledge.patterns.find(p => p.name === pattern.name);
      if (existing) {
        existing.count += pattern.count;
        existing.confidence = Math.min((existing.confidence + pattern.confidence) / 2, 1.0);
      } else {
        knowledge.patterns.push(pattern);
      }
    });

    // Store utilities
    if (this.isUtilityFile(analysis.functions?.[0]?.filepath || '')) {
      knowledge.utilities.push(...(analysis.functions || []));
    }
  }

  async generateInsights(codebaseKnowledge, featureContext) {
    const prompt = this.buildInsightPrompt(codebaseKnowledge, featureContext);
    
    try {
      const response = await this.anthropic.messages.create({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 4096,
        temperature: 0.2,
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ]
      });

      const insightsText = response.content[0].text;
      return this.parseInsightsResponse(insightsText);
    } catch (error) {
      this.logger.error('AI insight generation failed', {
        error: error.message,
        knowledge_size: JSON.stringify(codebaseKnowledge).length
      });
      
      // Return basic insights without AI
      return this.generateBasicInsights(codebaseKnowledge);
    }
  }

  buildInsightPrompt(knowledge, featureContext) {
    return `You are an expert developer analyzing an existing codebase to provide insights for implementing a new feature. Your goal is to identify reusable code, patterns, and architectural considerations.

EXISTING CODEBASE KNOWLEDGE:
Available Functions (${knowledge.existingFunctions.length}):
${knowledge.existingFunctions.slice(0, 20).map(f => `- ${f.name} (${f.filepath})`).join('\n')}

Available Constants (${knowledge.constants.length}):
${knowledge.constants.slice(0, 10).map(c => `- ${c.name} (${c.filepath})`).join('\n')}

Utility Functions (${knowledge.utilities.length}):
${knowledge.utilities.slice(0, 10).map(u => `- ${u.name} (${u.filepath})`).join('\n')}

Identified Patterns:
${knowledge.patterns.map(p => `- ${p.name}: ${p.count} occurrences (confidence: ${p.confidence})`).join('\n')}

FEATURE BEING IMPLEMENTED:
Purpose: ${featureContext.analysis?.businessPurpose || 'Not specified'}
Technical Requirements: ${JSON.stringify(featureContext.analysis?.technicalRequirements || [])}
System Impact: ${JSON.stringify(featureContext.analysis?.systemImpact || {})}

PROVIDE INSIGHTS IN JSON FORMAT:
{
  "reusableFunctions": [
    {
      "name": "function_name",
      "filepath": "path/to/file",
      "reason": "Why this function could be reused",
      "adaptationNeeded": "What changes might be needed"
    }
  ],
  "reusablePatterns": [
    {
      "pattern": "pattern_name",
      "description": "How this pattern is used in the codebase",
      "recommendation": "How to apply it to the new feature"
    }
  ],
  "architecturalGuidance": {
    "followPatterns": ["Patterns to follow based on codebase"],
    "avoidPatterns": ["Patterns to avoid"],
    "integrationPoints": ["Where the new feature should integrate"]
  },
  "suggestedApproach": "High-level approach based on existing codebase patterns",
  "potentialConflicts": [
    "Areas where new feature might conflict with existing code"
  ],
  "testingStrategy": "Testing approach based on existing test patterns",
  "dependencies": [
    "Existing dependencies that could be leveraged"
  ]
}

Focus on practical, actionable insights that will help implement the feature efficiently while maintaining consistency with the existing codebase.`;
  }

  parseInsightsResponse(responseText) {
    try {
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      
      return this.parseUnstructuredInsights(responseText);
    } catch (error) {
      this.logger.warn('Failed to parse insights response', {
        error: error.message
      });
      
      return {
        reusableFunctions: [],
        reusablePatterns: [],
        architecturalGuidance: {
          followPatterns: [],
          avoidPatterns: [],
          integrationPoints: []
        },
        suggestedApproach: responseText.substring(0, 500),
        potentialConflicts: [],
        testingStrategy: '',
        dependencies: [],
        rawResponse: responseText
      };
    }
  }

  parseUnstructuredInsights(text) {
    // Basic parsing for unstructured responses
    return {
      reusableFunctions: this.extractReusableFunctions(text),
      reusablePatterns: this.extractPatterns(text),
      architecturalGuidance: this.extractArchitecturalGuidance(text),
      suggestedApproach: this.extractApproach(text),
      potentialConflicts: this.extractConflicts(text),
      testingStrategy: this.extractTestingStrategy(text),
      dependencies: this.extractDependencies(text),
      rawResponse: text
    };
  }

  extractReusableFunctions(text) {
    const functions = [];
    const functionMatches = text.match(/(\w+)\s*\([^)]*\)/g) || [];
    
    functionMatches.slice(0, 10).forEach(match => {
      functions.push({
        name: match.split('(')[0].trim(),
        reason: 'Mentioned in analysis',
        adaptationNeeded: 'Review implementation details'
      });
    });
    
    return functions;
  }

  extractPatterns(text) {
    const patterns = [];
    const patternKeywords = ['pattern', 'approach', 'strategy', 'method'];
    
    patternKeywords.forEach(keyword => {
      const regex = new RegExp(`(${keyword}[^.]+)`, 'gi');
      const matches = text.match(regex) || [];
      matches.slice(0, 3).forEach(match => {
        patterns.push({
          pattern: keyword,
          description: match.trim(),
          recommendation: 'Apply to new feature'
        });
      });
    });
    
    return patterns;
  }

  extractArchitecturalGuidance(text) {
    return {
      followPatterns: this.extractListItems(text, 'follow|use|adopt'),
      avoidPatterns: this.extractListItems(text, 'avoid|don\'t|prevent'),
      integrationPoints: this.extractListItems(text, 'integrate|connect|link')
    };
  }

  extractApproach(text) {
    const sentences = text.split(/[.!?]+/);
    const approachSentences = sentences.filter(s => 
      s.toLowerCase().includes('approach') || 
      s.toLowerCase().includes('recommend') ||
      s.toLowerCase().includes('suggest')
    );
    
    return approachSentences.slice(0, 3).join('. ').trim();
  }

  extractConflicts(text) {
    return this.extractListItems(text, 'conflict|issue|problem|risk');
  }

  extractTestingStrategy(text) {
    const testingSentences = text.split(/[.!?]+/).filter(s => 
      s.toLowerCase().includes('test') || 
      s.toLowerCase().includes('spec')
    );
    
    return testingSentences.slice(0, 2).join('. ').trim();
  }

  extractDependencies(text) {
    return this.extractListItems(text, 'depend|require|need|import');
  }

  extractListItems(text, pattern) {
    const regex = new RegExp(`([^.]*(?:${pattern})[^.]*\\.?)`, 'gi');
    const matches = text.match(regex) || [];
    return matches.slice(0, 5).map(match => match.trim());
  }

  generateBasicInsights(knowledge) {
    return {
      reusableFunctions: knowledge.existingFunctions.slice(0, 10).map(f => ({
        name: f.name,
        filepath: f.filepath,
        reason: 'Available in codebase',
        adaptationNeeded: 'Review for compatibility'
      })),
      reusablePatterns: knowledge.patterns.slice(0, 5).map(p => ({
        pattern: p.name,
        description: `${p.name} pattern used ${p.count} times`,
        recommendation: 'Consider applying to new feature'
      })),
      architecturalGuidance: {
        followPatterns: knowledge.patterns.map(p => p.name),
        avoidPatterns: [],
        integrationPoints: ['Review existing integration patterns']
      },
      suggestedApproach: 'Follow existing codebase patterns and reuse available functions',
      potentialConflicts: ['Review for naming conflicts', 'Check dependency compatibility'],
      testingStrategy: 'Follow existing testing patterns',
      dependencies: ['Use existing dependencies where possible'],
      fallback: true
    };
  }
}

module.exports = CodebaseLearningAgent;