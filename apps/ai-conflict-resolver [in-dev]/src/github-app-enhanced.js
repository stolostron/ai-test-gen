const { App } = require('@octokit/app');
const { Octokit } = require('@octokit/rest');
const express = require('express');
const { createNodeMiddleware } = require('@octokit/webhooks');
const { ClaudeConflictResolver } = require('./claude-resolver');
const { CodeReviewIntelligence } = require('./code-review-intelligence');
const { JiraClient } = require('./jira-client');
const { NotificationService } = require('./notification-service');
const { ContextCollector } = require('./context-collector');

class EnhancedGitHubApp {
  constructor(config) {
    this.config = config;
    
    // Initialize GitHub App
    this.app = new App({
      appId: config.github.appId,
      privateKey: config.github.privateKey,
      oauth: {
        clientId: config.github.clientId,
        clientSecret: config.github.clientSecret,
      },
    });

    // Initialize services
    this.conflictResolver = new ClaudeConflictResolver(config.claude);
    this.codeReviewer = new CodeReviewIntelligence(config);
    this.jiraClient = new JiraClient(config.jira);
    this.notificationService = new NotificationService(config.notifications);
    this.contextCollector = new ContextCollector({
      github: this.app,
      jira: this.jiraClient,
    });

    // Set up webhook handlers
    this.setupWebhooks();
  }

  setupWebhooks() {
    const webhooks = this.app.webhooks;

    // Handle PR events
    webhooks.on(['pull_request.opened', 'pull_request.synchronize', 'pull_request.reopened'], 
      async ({ payload, octokit }) => {
        await this.handlePullRequestEvent(payload, octokit);
      }
    );

    // Handle PR ready for review
    webhooks.on('pull_request.ready_for_review', async ({ payload, octokit }) => {
      await this.performCodeReview(payload, octokit);
    });

    // Handle manual triggers via PR comment
    webhooks.on('issue_comment.created', async ({ payload, octokit }) => {
      if (payload.issue.pull_request) {
        await this.handleCommentCommand(payload, octokit);
      }
    });

    // Handle review submission
    webhooks.on('pull_request_review.submitted', async ({ payload, octokit }) => {
      await this.handleReviewFeedback(payload, octokit);
    });
  }

  async handlePullRequestEvent(payload, octokit) {
    const { repository, pull_request } = payload;
    
    console.log(`Processing PR #${pull_request.number} in ${repository.full_name}`);

    try {
      // Get detailed PR information
      const prDetails = await octokit.pulls.get({
        owner: repository.owner.login,
        repo: repository.name,
        pull_number: pull_request.number,
      });

      // Check for conflicts
      const hasConflicts = prDetails.data.mergeable_state === 'dirty';
      
      // Perform both conflict resolution and code review
      const tasks = [];

      if (hasConflicts) {
        console.log('Merge conflicts detected - initiating resolution');
        tasks.push(this.resolveConflicts({
          repository,
          pullRequest: prDetails.data,
          octokit,
        }));
      }

      // Always perform code review on new or updated PRs
      console.log('Initiating AI code review');
      tasks.push(this.performCodeReview(payload, octokit));

      // Execute tasks in parallel
      const results = await Promise.allSettled(tasks);
      
      // Handle results
      results.forEach((result, index) => {
        if (result.status === 'rejected') {
          console.error(`Task ${index} failed:`, result.reason);
        }
      });

    } catch (error) {
      console.error('Error handling PR event:', error);
      await this.notificationService.notifyError({
        repository,
        pullRequest: pull_request,
        error,
      });
    }
  }

  async performCodeReview(payload, octokit) {
    const { repository, pull_request } = payload;
    
    console.log(`Starting AI code review for PR #${pull_request.number}`);

    try {
      // Set PR status to indicate review is in progress
      await this.updatePRStatus({
        repository,
        pullRequest: pull_request,
        state: 'pending',
        description: '🤖 AI Code Review in progress...',
        context: 'ai-code-review',
        octokit,
      });

      // Collect comprehensive context
      const context = await this.contextCollector.gatherContext({
        repository,
        pullRequest: pull_request,
        octokit,
      });

      // Perform AI code review
      const reviewResult = await this.codeReviewer.reviewPullRequest({
        pullRequest: pull_request,
        context,
        repository,
        octokit,
      });

      // Post review results
      await this.postReviewResults({
        repository,
        pullRequest: pull_request,
        reviewResult,
        octokit,
      });

      // Update PR status based on health score
      const state = reviewResult.healthScore >= 75 ? 'success' : 
                    reviewResult.healthScore >= 60 ? 'failure' : 'failure';
      
      await this.updatePRStatus({
        repository,
        pullRequest: pull_request,
        state,
        description: `Health Score: ${reviewResult.healthScore}/100`,
        context: 'ai-code-review',
        targetUrl: reviewResult.reportUrl,
        octokit,
      });

      // Send notifications
      await this.notificationService.notifyReview({
        repository,
        pullRequest: pull_request,
        reviewResult,
      });

      // Update JIRA with review results
      await this.updateJiraWithReview({
        context,
        reviewResult,
        pullRequest: pull_request,
      });

    } catch (error) {
      console.error('Error during code review:', error);
      
      await this.updatePRStatus({
        repository,
        pullRequest: pull_request,
        state: 'error',
        description: 'AI Code Review failed',
        context: 'ai-code-review',
        octokit,
      });

      throw error;
    }
  }

  async handleCommentCommand(payload, octokit) {
    const { repository, issue, comment } = payload;
    const command = comment.body.toLowerCase().trim();

    // Command handlers
    const commands = {
      '/review': () => this.performCodeReview({ 
        repository, 
        pull_request: issue 
      }, octokit),
      
      '/review security': () => this.performSecurityReview({ 
        repository, 
        pull_request: issue 
      }, octokit),
      
      '/review performance': () => this.performPerformanceReview({ 
        repository, 
        pull_request: issue 
      }, octokit),
      
      '/suggest improvements': () => this.suggestImprovements({ 
        repository, 
        pull_request: issue 
      }, octokit),
      
      '/resolve-conflicts': () => this.handleManualConflictResolution({ 
        repository, 
        pull_request: issue 
      }, octokit),
      
      '/review help': () => this.postHelpComment({ 
        repository, 
        issue 
      }, octokit),
    };

    // Find and execute matching command
    for (const [cmd, handler] of Object.entries(commands)) {
      if (command.startsWith(cmd)) {
        await this.acknowledgeCommand({ repository, issue, command: cmd }, octokit);
        await handler();
        return;
      }
    }
  }

  async postReviewResults({ repository, pullRequest, reviewResult, octokit }) {
    // Create main review comment
    const mainComment = this.formatMainReviewComment(reviewResult);
    
    await octokit.issues.createComment({
      owner: repository.owner.login,
      repo: repository.name,
      issue_number: pullRequest.number,
      body: mainComment,
    });

    // Add inline comments for specific suggestions
    if (reviewResult.suggestions && reviewResult.suggestions.length > 0) {
      await this.postInlineComments({
        repository,
        pullRequest,
        suggestions: reviewResult.suggestions,
        octokit,
      });
    }

    // Add labels based on review results
    await this.updatePRLabels({
      repository,
      pullRequest,
      reviewResult,
      octokit,
    });
  }

  formatMainReviewComment(reviewResult) {
    const { report, healthScore, suggestions } = reviewResult;
    
    return `## 🤖 AI Code Review Results

${report.summary}

### 📊 Health Score: ${healthScore}/100 ${this.getHealthEmoji(healthScore)}

<details>
<summary><strong>📋 Detailed Analysis</strong> (click to expand)</summary>

${report.markdown}

</details>

### 💡 Top Suggestions

${suggestions.slice(0, 5).map((s, i) => `
${i + 1}. **[${s.priority.toUpperCase()}]** ${s.title}
   - **File**: \`${s.file}\`
   - **Issue**: ${s.description}
   - **Suggestion**: ${s.suggestion}
   ${s.codeExample ? `\n   \`\`\`${s.language || 'javascript'}\n   ${s.codeExample}\n   \`\`\`` : ''}
`).join('\n')}

${suggestions.length > 5 ? `\n<details>\n<summary>View ${suggestions.length - 5} more suggestions</summary>\n\n${
  suggestions.slice(5).map((s, i) => `
${i + 6}. **[${s.priority.toUpperCase()}]** ${s.title}
   - **File**: \`${s.file}\`
   - **Issue**: ${s.description}
   - **Suggestion**: ${s.suggestion}
`).join('\n')
}\n</details>` : ''}

### 🔗 Actions

- Reply with \`/review\` to trigger a fresh review
- Reply with \`/review security\` for focused security analysis
- Reply with \`/review performance\` for performance deep-dive
- Reply with \`/suggest improvements\` for additional suggestions

---
*Generated by AI Code Review & Conflict Resolution Assistant v2.0.0*
*Health Score Threshold: ${this.config.review?.healthScoreThreshold || 75}/100*`;
  }

  getHealthEmoji(score) {
    if (score >= 90) return '🌟 Excellent';
    if (score >= 75) return '✅ Good';
    if (score >= 60) return '⚠️ Needs Improvement';
    return '❌ Poor';
  }

  async postInlineComments({ repository, pullRequest, suggestions, octokit }) {
    // Get the latest commit SHA
    const { data: commits } = await octokit.pulls.listCommits({
      owner: repository.owner.login,
      repo: repository.name,
      pull_number: pullRequest.number,
    });
    
    const latestCommitSha = commits[commits.length - 1].sha;

    // Group suggestions by file
    const suggestionsByFile = suggestions.reduce((acc, suggestion) => {
      if (suggestion.line && suggestion.file) {
        if (!acc[suggestion.file]) acc[suggestion.file] = [];
        acc[suggestion.file].push(suggestion);
      }
      return acc;
    }, {});

    // Create review with inline comments
    const comments = [];
    
    for (const [file, fileSuggestions] of Object.entries(suggestionsByFile)) {
      for (const suggestion of fileSuggestions.slice(0, 3)) { // Limit inline comments per file
        comments.push({
          path: file,
          line: suggestion.line,
          body: `**${suggestion.priority.toUpperCase()}: ${suggestion.title}**\n\n${suggestion.description}\n\n💡 **Suggestion:**\n${suggestion.suggestion}${
            suggestion.codeExample ? `\n\n\`\`\`${suggestion.language || 'javascript'}\n${suggestion.codeExample}\n\`\`\`` : ''
          }`,
        });
      }
    }

    if (comments.length > 0) {
      try {
        await octokit.pulls.createReview({
          owner: repository.owner.login,
          repo: repository.name,
          pull_number: pullRequest.number,
          commit_id: latestCommitSha,
          event: 'COMMENT',
          comments,
        });
      } catch (error) {
        console.error('Error posting inline comments:', error);
      }
    }
  }

  async updatePRLabels({ repository, pullRequest, reviewResult, octokit }) {
    const labels = [];
    
    // Add health score label
    if (reviewResult.healthScore >= 90) {
      labels.push('ai-review: excellent');
    } else if (reviewResult.healthScore >= 75) {
      labels.push('ai-review: good');
    } else if (reviewResult.healthScore >= 60) {
      labels.push('ai-review: needs-improvement');
    } else {
      labels.push('ai-review: poor');
    }

    // Add issue type labels
    if (reviewResult.metrics.criticalIssues > 0) {
      labels.push('has: critical-issues');
    }
    
    if (reviewResult.metrics.testCoverage < this.config.review?.testCoverageThreshold) {
      labels.push('needs: test-coverage');
    }

    if (reviewResult.report.detailedAnalysis.security.vulnerabilities?.length > 0) {
      labels.push('security: review-needed');
    }

    // Apply labels
    try {
      await octokit.issues.addLabels({
        owner: repository.owner.login,
        repo: repository.name,
        issue_number: pullRequest.number,
        labels,
      });
    } catch (error) {
      console.error('Error applying labels:', error);
    }
  }

  async updatePRStatus({ repository, pullRequest, state, description, context, targetUrl, octokit }) {
    try {
      await octokit.repos.createCommitStatus({
        owner: repository.owner.login,
        repo: repository.name,
        sha: pullRequest.head.sha,
        state,
        description,
        context,
        target_url: targetUrl,
      });
    } catch (error) {
      console.error('Error updating PR status:', error);
    }
  }

  async updateJiraWithReview({ context, reviewResult, pullRequest }) {
    for (const ticket of context.jiraTickets) {
      try {
        const comment = `
AI Code Review completed for PR #${pullRequest.number}

Health Score: ${reviewResult.healthScore}/100
Test Coverage: ${reviewResult.metrics.testCoverage}%
Critical Issues: ${reviewResult.metrics.criticalIssues}
Total Suggestions: ${reviewResult.metrics.totalSuggestions}

View full review: ${pullRequest.html_url}
        `.trim();

        await this.jiraClient.addComment(ticket.key, comment);
      } catch (error) {
        console.error(`Error updating JIRA ticket ${ticket.key}:`, error);
      }
    }
  }

  async postHelpComment({ repository, issue }, octokit) {
    const helpText = `
## 🤖 AI Code Review & Conflict Resolution Commands

### Review Commands
- \`/review\` - Perform comprehensive code review
- \`/review security\` - Focus on security vulnerabilities
- \`/review performance\` - Analyze performance issues
- \`/suggest improvements\` - Get additional improvement suggestions

### Conflict Resolution
- \`/resolve-conflicts\` - Attempt automatic conflict resolution
- \`/resolve-conflicts --force\` - Force resolution with lower confidence

### Options
- \`/review --strict\` - Use stricter review criteria
- \`/review --fast\` - Quick review focusing on critical issues

### Examples
\`\`\`
/review
/review security
/suggest improvements
/resolve-conflicts
\`\`\`

---
*Need help? Contact the team in #ai-code-review*
    `.trim();

    await octokit.issues.createComment({
      owner: repository.owner.login,
      repo: repository.name,
      issue_number: issue.number,
      body: helpText,
    });
  }

  async acknowledgeCommand({ repository, issue, command }, octokit) {
    const emoji = '👀';
    await octokit.reactions.createForIssueComment({
      owner: repository.owner.login,
      repo: repository.name,
      comment_id: issue.id,
      content: emoji,
    });
  }

  // Specialized review methods
  async performSecurityReview({ repository, pull_request }, octokit) {
    // Security-focused review implementation
    console.log('Performing security-focused review...');
    // Implementation would focus on security aspects
  }

  async performPerformanceReview({ repository, pull_request }, octokit) {
    // Performance-focused review implementation
    console.log('Performing performance-focused review...');
    // Implementation would focus on performance aspects
  }

  async suggestImprovements({ repository, pull_request }, octokit) {
    // Generate additional improvement suggestions
    console.log('Generating improvement suggestions...');
    // Implementation would provide more detailed suggestions
  }

  // ... (include the original conflict resolution methods from github-app.js)

  // Express middleware for webhook handling
  createMiddleware() {
    return createNodeMiddleware(this.app.webhooks, {
      path: '/webhook',
    });
  }
}

module.exports = { EnhancedGitHubApp };

