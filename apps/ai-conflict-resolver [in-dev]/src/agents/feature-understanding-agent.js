const winston = require('winston');
const { Anthropic } = require('@anthropic-ai/sdk');

class FeatureUnderstandingAgent {
  constructor(config) {
    this.config = config;
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
      defaultMeta: { component: 'FeatureUnderstandingAgent' }
    });
  }

  async analyzeFeatureContext(pr, jiraContext = null) {
    this.logger.info('Starting feature context analysis', {
      pr_number: pr.number,
      repository: pr.base.repo.full_name
    });

    try {
      const context = await this.gatherContext(pr, jiraContext);
      const analysis = await this.performAIAnalysis(context);
      
      this.logger.info('Feature context analysis completed', {
        pr_number: pr.number,
        analysis_keys: Object.keys(analysis)
      });

      return {
        success: true,
        analysis,
        context,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      this.logger.error('Feature context analysis failed', {
        pr_number: pr.number,
        error: error.message,
        stack: error.stack
      });
      throw error;
    }
  }

  async gatherContext(pr, jiraContext) {
    const context = {
      pr: {
        title: pr.title,
        body: pr.body || '',
        number: pr.number,
        author: pr.user.login,
        baseBranch: pr.base.ref,
        headBranch: pr.head.ref,
        repository: pr.base.repo.full_name
      },
      jira: jiraContext || await this.extractJiraContext(pr),
      commits: await this.getCommitMessages(pr),
      fileChanges: await this.getFileChangeSummary(pr)
    };

    return context;
  }

  async extractJiraContext(pr) {
    const jiraPattern = /([A-Z]{2,}-\d+)/g;
    const combinedText = `${pr.title} ${pr.body || ''}`;
    const matches = combinedText.match(jiraPattern) || [];
    
    if (matches.length === 0) {
      return {
        tickets: [],
        hasJiraContext: false,
        extractedFromPR: true
      };
    }

    return {
      tickets: [...new Set(matches)], // Remove duplicates
      hasJiraContext: true,
      extractedFromPR: true,
      requirements: this.extractRequirementsFromText(pr.body || ''),
      acceptanceCriteria: this.extractAcceptanceCriteria(pr.body || '')
    };
  }

  extractRequirementsFromText(text) {
    const requirementPatterns = [
      /(?:requirement|requirements?|need|needs?|should|must)[\s:]+([^\n.]+)/gi,
      /(?:feature|functionality)[\s:]+([^\n.]+)/gi,
      /(?:user story|story)[\s:]+([^\n.]+)/gi
    ];

    const requirements = [];
    requirementPatterns.forEach(pattern => {
      const matches = text.match(pattern) || [];
      requirements.push(...matches);
    });

    return requirements.slice(0, 5); // Limit to prevent noise
  }

  extractAcceptanceCriteria(text) {
    const criteriaPatterns = [
      /(?:acceptance criteria|criteria|given|when|then)[\s:]+([^\n.]+)/gi,
      /(?:scenario|scenarios?)[\s:]+([^\n.]+)/gi,
      /(?:expected|expects?)[\s:]+([^\n.]+)/gi
    ];

    const criteria = [];
    criteriaPatterns.forEach(pattern => {
      const matches = text.match(pattern) || [];
      criteria.push(...matches);
    });

    return criteria.slice(0, 10);
  }

  async getCommitMessages(pr) {
    // In a real implementation, this would use octokit to fetch commits
    // For now, we'll extract from PR title and description
    return {
      count: 1,
      messages: [pr.title],
      summary: pr.title,
      hasDetailedMessages: false
    };
  }

  async getFileChangeSummary(pr) {
    // This would typically come from the GitHub API
    return {
      filesChanged: pr.changed_files || 0,
      additions: pr.additions || 0,
      deletions: pr.deletions || 0,
      languages: [], // Would be detected from file extensions
      areas: [] // Would be determined by file paths
    };
  }

  async performAIAnalysis(context) {
    const prompt = this.buildAnalysisPrompt(context);
    
    try {
      const response = await this.anthropic.messages.create({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 4096,
        temperature: 0.3,
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ]
      });

      const analysisText = response.content[0].text;
      return this.parseAnalysisResponse(analysisText);
    } catch (error) {
      this.logger.error('AI analysis failed', {
        error: error.message,
        context_size: JSON.stringify(context).length
      });
      throw new Error(`AI analysis failed: ${error.message}`);
    }
  }

  buildAnalysisPrompt(context) {
    return `You are an expert software developer analyzing a pull request to understand the feature being implemented. Your goal is to deeply understand the intent, requirements, and potential challenges.

PULL REQUEST CONTEXT:
Title: ${context.pr.title}
Description: ${context.pr.body}
Author: ${context.pr.author}
Base Branch: ${context.pr.baseBranch}
Files Changed: ${context.fileChanges.filesChanged}
Lines Added: ${context.fileChanges.additions}
Lines Deleted: ${context.fileChanges.deletions}

JIRA CONTEXT:
Has JIRA Tickets: ${context.jira.hasJiraContext}
Tickets: ${context.jira.tickets.join(', ')}
Requirements: ${JSON.stringify(context.jira.requirements)}
Acceptance Criteria: ${JSON.stringify(context.jira.acceptanceCriteria)}

COMMIT CONTEXT:
Recent Commits: ${JSON.stringify(context.commits.messages)}

ANALYSIS REQUIRED:
Please analyze this pull request and provide a detailed understanding in the following JSON format:

{
  "businessPurpose": "What business problem is this solving?",
  "technicalRequirements": [
    "List of specific technical requirements"
  ],
  "functionalRequirements": [
    "List of functional requirements"
  ],
  "edgeCases": [
    "Potential edge cases that should be considered"
  ],
  "systemImpact": {
    "areas": ["Which parts of the system will be affected"],
    "integrations": ["What integrations might be impacted"],
    "performance": "Performance considerations",
    "security": "Security considerations"
  },
  "implementationStrategy": "Recommended approach for implementation",
  "testingStrategy": [
    "Key areas that need testing"
  ],
  "riskFactors": [
    "Potential risks or challenges"
  ],
  "dependencies": [
    "Any dependencies or prerequisites"
  ]
}

Focus on understanding the intent behind the change, not just the mechanics. Consider the broader system context and potential implications.`;
  }

  parseAnalysisResponse(responseText) {
    try {
      // Try to extract JSON from the response
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }

      // If no JSON found, parse manually
      return this.parseUnstructuredResponse(responseText);
    } catch (error) {
      this.logger.warn('Failed to parse structured response, falling back to text analysis', {
        error: error.message
      });
      
      return {
        businessPurpose: this.extractSection(responseText, 'business purpose|purpose'),
        technicalRequirements: this.extractListItems(responseText, 'technical requirements|requirements'),
        functionalRequirements: this.extractListItems(responseText, 'functional requirements'),
        edgeCases: this.extractListItems(responseText, 'edge cases|edge case'),
        systemImpact: {
          areas: this.extractListItems(responseText, 'system impact|areas affected'),
          integrations: [],
          performance: this.extractSection(responseText, 'performance'),
          security: this.extractSection(responseText, 'security')
        },
        implementationStrategy: this.extractSection(responseText, 'implementation|strategy'),
        testingStrategy: this.extractListItems(responseText, 'testing|test'),
        riskFactors: this.extractListItems(responseText, 'risks|risk factors'),
        dependencies: this.extractListItems(responseText, 'dependencies|prerequisites'),
        rawResponse: responseText
      };
    }
  }

  parseUnstructuredResponse(text) {
    // Fallback parsing for unstructured responses
    const sections = text.split(/\n\s*\n/);
    
    return {
      businessPurpose: this.extractFromSections(sections, ['purpose', 'business', 'goal']),
      technicalRequirements: this.extractListFromSections(sections, ['technical', 'requirements']),
      functionalRequirements: this.extractListFromSections(sections, ['functional', 'features']),
      edgeCases: this.extractListFromSections(sections, ['edge', 'cases', 'exceptions']),
      systemImpact: {
        areas: this.extractListFromSections(sections, ['impact', 'affected', 'areas']),
        integrations: [],
        performance: this.extractFromSections(sections, ['performance']),
        security: this.extractFromSections(sections, ['security'])
      },
      implementationStrategy: this.extractFromSections(sections, ['implementation', 'approach', 'strategy']),
      testingStrategy: this.extractListFromSections(sections, ['testing', 'test']),
      riskFactors: this.extractListFromSections(sections, ['risk', 'challenges']),
      dependencies: this.extractListFromSections(sections, ['dependencies', 'prerequisites']),
      rawResponse: text
    };
  }

  extractSection(text, pattern) {
    const regex = new RegExp(`(?:${pattern})[:\\s]*([^\\n]+)`, 'i');
    const match = text.match(regex);
    return match ? match[1].trim() : '';
  }

  extractListItems(text, pattern) {
    const regex = new RegExp(`(?:${pattern})[:\\s]*([\\s\\S]*?)(?=\\n\\s*[A-Z]|$)`, 'i');
    const match = text.match(regex);
    
    if (!match) return [];
    
    const listText = match[1];
    const items = listText
      .split(/[\n-•*]/)
      .map(item => item.trim())
      .filter(item => item.length > 0 && !item.match(/^[:\s]*$/))
      .slice(0, 10); // Limit items
    
    return items;
  }

  extractFromSections(sections, keywords) {
    for (const section of sections) {
      const lowerSection = section.toLowerCase();
      if (keywords.some(keyword => lowerSection.includes(keyword))) {
        return section.trim();
      }
    }
    return '';
  }

  extractListFromSections(sections, keywords) {
    const relevantSection = this.extractFromSections(sections, keywords);
    if (!relevantSection) return [];
    
    return relevantSection
      .split(/[\n-•*]/)
      .map(item => item.trim())
      .filter(item => item.length > 0)
      .slice(0, 10);
  }

  // Validation methods
  validateAnalysis(analysis) {
    const requiredFields = ['businessPurpose', 'technicalRequirements', 'systemImpact'];
    const missing = requiredFields.filter(field => !analysis[field]);
    
    if (missing.length > 0) {
      this.logger.warn('Analysis missing required fields', { missing });
      return false;
    }
    
    return true;
  }

  getAnalysisSummary(analysis) {
    return {
      purpose: analysis.businessPurpose,
      complexity: this.assessComplexity(analysis),
      riskLevel: this.assessRisk(analysis),
      testingNeeds: analysis.testingStrategy?.length || 0,
      dependencies: analysis.dependencies?.length || 0
    };
  }

  assessComplexity(analysis) {
    const factors = [
      analysis.technicalRequirements?.length || 0,
      analysis.systemImpact?.areas?.length || 0,
      analysis.dependencies?.length || 0,
      analysis.riskFactors?.length || 0
    ];
    
    const totalComplexity = factors.reduce((sum, factor) => sum + factor, 0);
    
    if (totalComplexity <= 5) return 'low';
    if (totalComplexity <= 15) return 'medium';
    return 'high';
  }

  assessRisk(analysis) {
    const riskCount = analysis.riskFactors?.length || 0;
    const securityMentioned = analysis.systemImpact?.security?.length > 0;
    const performanceMentioned = analysis.systemImpact?.performance?.length > 0;
    
    let riskScore = riskCount;
    if (securityMentioned) riskScore += 2;
    if (performanceMentioned) riskScore += 1;
    
    if (riskScore <= 2) return 'low';
    if (riskScore <= 5) return 'medium';
    return 'high';
  }
}

module.exports = FeatureUnderstandingAgent;