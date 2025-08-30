const Anthropic = require('@anthropic-ai/sdk');
const { diffLines } = require('diff');

class ClaudeConflictResolver {
  constructor(config) {
    this.config = config;
    this.claude = new Anthropic({
      apiKey: config.apiKey,
    });
    
    this.model = config.model || 'claude-3-opus-20240229';
    this.maxTokens = config.maxTokens || 4096;
  }

  async analyzeConflicts({ pullRequest, context, repository }) {
    try {
      // Get the actual conflict markers from files
      const conflictedFiles = await this.getConflictedFiles({
        pullRequest,
        repository,
        context,
      });

      // Prepare comprehensive context for Claude
      const systemPrompt = this.buildSystemPrompt();
      const userPrompt = this.buildAnalysisPrompt({
        pullRequest,
        context,
        conflictedFiles,
        repository,
      });

      // Call Claude for analysis
      const response = await this.claude.messages.create({
        model: this.model,
        max_tokens: this.maxTokens,
        system: systemPrompt,
        messages: [
          {
            role: 'user',
            content: userPrompt,
          },
        ],
      });

      // Parse Claude's response
      const analysis = this.parseAnalysisResponse(response.content[0].text);
      
      // Generate resolutions for each conflicted file
      const resolutions = await this.generateResolutions({
        conflictedFiles,
        analysis,
        context,
      });

      return {
        confidence: analysis.confidence,
        summary: analysis.summary,
        resolutions,
        context,
        conflictTypes: analysis.conflictTypes,
        riskAssessment: analysis.riskAssessment,
        testCoverage: analysis.testCoverage,
        detailedReport: analysis.detailedReport,
        lowConfidenceReasons: analysis.lowConfidenceReasons || [],
        suggestedResolutions: analysis.suggestedResolutions || [],
      };

    } catch (error) {
      console.error('Error in conflict analysis:', error);
      throw error;
    }
  }

  async generateResolutions({ conflictedFiles, analysis, context }) {
    const resolutions = [];

    for (const file of conflictedFiles) {
      const resolution = await this.resolveFileConflicts({
        file,
        analysis,
        context,
      });
      resolutions.push(resolution);
    }

    return resolutions;
  }

  async resolveFileConflicts({ file, analysis, context }) {
    const systemPrompt = this.buildResolutionSystemPrompt();
    const userPrompt = this.buildResolutionPrompt({
      file,
      analysis,
      context,
    });

    const response = await this.claude.messages.create({
      model: this.model,
      max_tokens: this.maxTokens,
      system: systemPrompt,
      messages: [
        {
          role: 'user',
          content: userPrompt,
        },
      ],
    });

    const resolvedContent = this.extractResolvedContent(response.content[0].text);
    const strategy = this.determineResolutionStrategy(response.content[0].text);

    return {
      path: file.path,
      originalContent: file.content,
      resolvedContent,
      conflictType: file.conflictType,
      strategy,
      explanation: this.extractExplanation(response.content[0].text),
    };
  }

  buildSystemPrompt() {
    return `You are an expert AI system specialized in resolving merge conflicts in code repositories.
You have deep understanding of:
- Software development best practices
- Git version control and merge conflict resolution
- Code semantics and intent
- Test-driven development
- The specific codebase context and patterns

Your task is to analyze merge conflicts intelligently by:
1. Understanding the intent of both conflicting changes
2. Analyzing related JIRA tickets and PR descriptions for context
3. Considering test requirements and acceptance criteria
4. Maintaining code quality and consistency
5. Preserving the functionality from both branches where possible

Always provide:
- A confidence score (0-100%) for your analysis
- Clear reasoning for your decisions
- Risk assessment for the proposed resolution
- Specific resolution strategies for each conflict`;
  }

  buildAnalysisPrompt({ pullRequest, context, conflictedFiles, repository }) {
    return `Analyze the following merge conflicts and provide a resolution strategy:

## Repository Information
- Repository: ${repository.full_name}
- PR #${pullRequest.number}: ${pullRequest.title}
- Base Branch: ${pullRequest.base.ref}
- Head Branch: ${pullRequest.head.ref}

## JIRA Context
${context.jiraTickets.map(ticket => `
### ${ticket.key}: ${ticket.summary}
- Status: ${ticket.status}
- Acceptance Criteria: ${ticket.acceptanceCriteria}
- Description: ${ticket.description}
`).join('\n')}

## PR Description
${pullRequest.body}

## Related PRs and Commits
${context.relatedPRs.map(pr => `- PR #${pr.number}: ${pr.title}`).join('\n')}

## Recent Commits
${context.commits.map(commit => `- ${commit.sha.substring(0, 7)}: ${commit.message}`).join('\n')}

## Conflicted Files
${conflictedFiles.map(file => `
### File: ${file.path}
\`\`\`
${file.content}
\`\`\`
`).join('\n')}

## Test Information
- Current Test Coverage: ${context.testCoverage}%
- Test Files: ${context.testFiles.join(', ')}

Please analyze these conflicts and provide:
1. Overall confidence score (0-100%)
2. Summary of the conflicts and their nature
3. Risk assessment
4. Recommended resolution strategy for each file
5. Any concerns or areas requiring human review

Format your response as JSON with the following structure:
{
  "confidence": <number>,
  "summary": "<string>",
  "conflictTypes": ["<type1>", "<type2>"],
  "riskAssessment": {
    "level": "<low|medium|high>",
    "factors": ["<factor1>", "<factor2>"]
  },
  "testCoverage": <number>,
  "detailedReport": "<markdown string>",
  "lowConfidenceReasons": ["<reason1>", "<reason2>"],
  "suggestedResolutions": [
    {
      "description": "<string>",
      "diff": "<string>"
    }
  ]
}`;
  }

  buildResolutionSystemPrompt() {
    return `You are resolving a specific merge conflict in a file.
Your goal is to:
1. Preserve the intent of both changes
2. Maintain code functionality and quality
3. Follow the project's coding standards
4. Ensure tests will pass

Provide the resolved file content without any conflict markers.
Include an explanation of your resolution strategy.`;
  }

  buildResolutionPrompt({ file, analysis, context }) {
    return `Resolve the merge conflict in this file:

## File: ${file.path}
## Conflict Type: ${file.conflictType}
## File Content with Conflicts:
\`\`\`
${file.content}
\`\`\`

## Context from Analysis:
${analysis.summary}

## Related Test Files:
${context.testFiles.filter(tf => tf.includes(file.path.split('/').pop().replace('.js', ''))).join(', ')}

## Resolution Guidelines:
- Preserve functionality from both branches
- Maintain or improve code quality
- Ensure compatibility with existing tests
- Follow the established patterns in the codebase

Please provide:
1. The fully resolved file content (no conflict markers)
2. Explanation of your resolution strategy
3. Any specific concerns or notes

Format your response as:
RESOLVED_CONTENT:
\`\`\`
<resolved file content here>
\`\`\`

STRATEGY: <explanation of resolution strategy>

NOTES: <any concerns or important notes>`;
  }

  async getConflictedFiles({ pullRequest, repository, context }) {
    // This would integrate with GitHub API to get actual file contents
    // For now, returning mock data structure
    return [
      {
        path: 'src/components/ClusterList.js',
        content: `<<<<<<< HEAD
import { useState, useEffect } from 'react';
import { fetchClusters } from '../api/clusters';
=======
import React, { useState, useEffect } from 'react';
import { getClusters } from '../api/clusterService';
>>>>>>> feature-branch

export const ClusterList = () => {
  const [clusters, setClusters] = useState([]);
  
<<<<<<< HEAD
  useEffect(() => {
    fetchClusters().then(setClusters);
  }, []);
=======
  useEffect(() => {
    getClusters({ includeMetrics: true }).then(data => {
      setClusters(data.items);
    });
  }, []);
>>>>>>> feature-branch
  
  return (
    <div className="cluster-list">
      {clusters.map(cluster => (
        <ClusterCard key={cluster.id} cluster={cluster} />
      ))}
    </div>
  );
};`,
        conflictType: 'import-and-logic',
      },
    ];
  }

  parseAnalysisResponse(responseText) {
    try {
      // Extract JSON from response
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      
      // Fallback parsing if not in expected format
      return {
        confidence: 50,
        summary: responseText,
        conflictTypes: ['unknown'],
        riskAssessment: { level: 'medium', factors: ['parse-error'] },
        testCoverage: 0,
        detailedReport: responseText,
        lowConfidenceReasons: ['Failed to parse structured response'],
        suggestedResolutions: [],
      };
    } catch (error) {
      console.error('Error parsing Claude response:', error);
      return {
        confidence: 0,
        summary: 'Failed to parse AI response',
        conflictTypes: ['parse-error'],
        riskAssessment: { level: 'high', factors: ['parse-failure'] },
        testCoverage: 0,
        detailedReport: responseText,
        lowConfidenceReasons: ['Response parsing failed'],
        suggestedResolutions: [],
      };
    }
  }

  extractResolvedContent(responseText) {
    const contentMatch = responseText.match(/RESOLVED_CONTENT:\s*```[\s\S]*?\n([\s\S]*?)```/);
    if (contentMatch) {
      return contentMatch[1].trim();
    }
    
    // Fallback: try to find any code block
    const codeBlockMatch = responseText.match(/```[\s\S]*?\n([\s\S]*?)```/);
    if (codeBlockMatch) {
      return codeBlockMatch[1].trim();
    }
    
    throw new Error('Could not extract resolved content from response');
  }

  extractExplanation(responseText) {
    const strategyMatch = responseText.match(/STRATEGY:\s*([\s\S]*?)(?:NOTES:|$)/);
    if (strategyMatch) {
      return strategyMatch[1].trim();
    }
    return 'Resolution strategy not provided';
  }

  determineResolutionStrategy(responseText) {
    const strategy = responseText.toLowerCase();
    
    if (strategy.includes('semantic merge')) {
      return 'semantic-merge';
    } else if (strategy.includes('test') && strategy.includes('guided')) {
      return 'test-guided';
    } else if (strategy.includes('combine') || strategy.includes('both')) {
      return 'combined-functionality';
    } else if (strategy.includes('prefer') && strategy.includes('head')) {
      return 'prefer-head';
    } else if (strategy.includes('prefer') && strategy.includes('base')) {
      return 'prefer-base';
    }
    
    return 'intelligent-merge';
  }
}

module.exports = { ClaudeConflictResolver };
