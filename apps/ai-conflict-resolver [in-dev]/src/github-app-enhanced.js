const winston = require('winston');
const { App } = require('@octokit/app');
const AgentOrchestrator = require('./orchestrator/agent-orchestrator');
const NotificationService = require('./notification-service');

class EnhancedGitHubApp {
  constructor(config) {
    this.config = config;
    this.app = new App({
      appId: config.github.appId,
      privateKey: config.github.privateKey,
      webhooks: { secret: config.github.webhookSecret }
    });
    
    // Initialize services with octokit factory
    this.orchestrator = new AgentOrchestrator(config, this.createOctokit.bind(this));
    this.notificationService = new NotificationService(config.notifications);
    
    this.setupWebhooks();
    
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
      ),
      defaultMeta: { service: 'enhanced-github-app' }
    });

    // Setup cleanup interval for old workflows
    setInterval(() => {
      this.orchestrator.cleanupOldWorkflows();
    }, 60 * 60 * 1000); // Run every hour
  }

  createOctokit(installationId) {
    return this.app.getInstallationOctokit(installationId);
  }
  
  setupWebhooks() {
    // PR opened - trigger full analysis
    this.app.webhooks.on('pull_request.opened', async ({ payload, octokit }) => {
      await this.handlePullRequestEvent(payload, octokit, 'opened');
    });
    
    // PR updated - trigger incremental analysis
    this.app.webhooks.on('pull_request.synchronize', async ({ payload, octokit }) => {
      await this.handlePullRequestEvent(payload, octokit, 'updated');
    });

    // PR reopened - trigger full analysis
    this.app.webhooks.on('pull_request.reopened', async ({ payload, octokit }) => {
      await this.handlePullRequestEvent(payload, octokit, 'reopened');
    });

    // PR ready for review - trigger analysis if not done
    this.app.webhooks.on('pull_request.ready_for_review', async ({ payload, octokit }) => {
      await this.handlePullRequestEvent(payload, octokit, 'ready_for_review');
    });
    
    // Comment commands
    this.app.webhooks.on('issue_comment.created', async ({ payload, octokit }) => {
      if (payload.issue.pull_request) {
        await this.handleCommentCommand(payload, octokit);
      }
    });

    // Installation events
    this.app.webhooks.on('installation.created', async ({ payload, octokit }) => {
      this.logger.info('New installation created', {
        installation_id: payload.installation.id,
        account: payload.installation.account.login
      });
    });
  }
  
  async handlePullRequestEvent(payload, octokit, eventType) {
    const pr = payload.pull_request;
    const repository = payload.repository;
    
    try {
      this.logger.info('Processing PR event', {
        event_type: eventType,
        action: payload.action,
        pr_number: pr.number,
        repository: repository.full_name,
        author: pr.user.login,
        draft: pr.draft
      });

      // Skip draft PRs unless explicitly ready for review
      if (pr.draft && eventType !== 'ready_for_review') {
        this.logger.info('Skipping draft PR', {
          pr_number: pr.number,
          repository: repository.full_name
        });
        return;
      }

      // Add a reaction to show we're processing
      try {
        await octokit.reactions.createForIssue({
          owner: repository.owner.login,
          repo: repository.name,
          issue_number: pr.number,
          content: 'eyes'
        });
      } catch (reactionError) {
        this.logger.debug('Could not add reaction', { error: reactionError.message });
      }
      
      // Orchestrate the full PR review workflow
      const result = await this.orchestrator.orchestratePRReview(pr, {
        eventType,
        repository,
        incremental: eventType === 'updated'
      });
      
      // Post the comprehensive review results
      await this.postComprehensiveReview(pr, result.report, repository, octokit);
      
      // Send notifications
      await this.notificationService.notifyReviewComplete({
        pr,
        report: result.report,
        repository,
        workflowId: result.workflowId
      });

      // Add success reaction
      try {
        await octokit.reactions.createForIssue({
          owner: repository.owner.login,
          repo: repository.name,
          issue_number: pr.number,
          content: 'rocket'
        });
      } catch (reactionError) {
        this.logger.debug('Could not add success reaction', { error: reactionError.message });
      }
      
    } catch (error) {
      this.logger.error('Failed to handle PR event', {
        pr_number: pr.number,
        repository: repository.full_name,
        event_type: eventType,
        error: error.message,
        stack: error.stack
      });
      
      await this.postErrorComment(pr, error, repository, octokit);

      // Add error reaction
      try {
        await octokit.reactions.createForIssue({
          owner: repository.owner.login,
          repo: repository.name,
          issue_number: pr.number,
          content: 'confused'
        });
      } catch (reactionError) {
        this.logger.debug('Could not add error reaction', { error: reactionError.message });
      }
    }
  }
  
  async handleCommentCommand(payload, octokit) {
    const comment = payload.comment;
    const issue = payload.issue;
    const repository = payload.repository;
    
    if (!this.isCommand(comment.body)) {
      return;
    }
    
    try {
      this.logger.info('Processing comment command', {
        comment_id: comment.id,
        pr_number: issue.number,
        repository: repository.full_name,
        author: comment.user.login,
        command: comment.body.split('\n')[0]
      });

      const command = this.parseCommand(comment.body);
      
      // Add eyes reaction to acknowledge command
      await octokit.reactions.createForComment({
        owner: repository.owner.login,
        repo: repository.name,
        comment_id: comment.id,
        content: 'eyes'
      });

      await this.executeCommand(command, {
        issue,
        comment,
        repository,
        octokit
      });
      
    } catch (error) {
      this.logger.error('Failed to handle comment command', {
        comment_id: comment.id,
        pr_number: issue.number,
        repository: repository.full_name,
        error: error.message
      });

      await this.postComment(issue, repository, octokit, 
        `❌ Command failed: ${error.message}`);
    }
  }
  
  isCommand(text) {
    return text.trim().startsWith('/ai-');
  }
  
  parseCommand(text) {
    const trimmed = text.trim();
    const parts = trimmed.split(/\s+/);
    const command = parts[0];
    const args = parts.slice(1);
    
    return { command, args, original: trimmed };
  }
  
  async executeCommand(command, context) {
    const { issue, repository, octokit, comment } = context;
    
    switch (command.command) {
      case '/ai-review':
        await this.executeReviewCommand(command.args, context);
        break;
      case '/ai-status':
        await this.executeStatusCommand(command.args, context);
        break;
      case '/ai-help':
        await this.executeHelpCommand(context);
        break;
      default:
        await this.postComment(issue, repository, octokit, 
          `❓ Unknown command: \`${command.command}\`. Use \`/ai-help\` for available commands.`);
        
        await octokit.reactions.createForComment({
          owner: repository.owner.login,
          repo: repository.name,
          comment_id: comment.id,
          content: 'confused'
        });
        return;
    }

    // Add success reaction
    await octokit.reactions.createForComment({
      owner: repository.owner.login,
      repo: repository.name,
      comment_id: comment.id,
      content: 'rocket'
    });
  }
  
  async executeReviewCommand(args, context) {
    const { issue, repository, octokit } = context;
    
    try {
      // Get PR details
      const prResponse = await octokit.pulls.get({
        owner: repository.owner.login,
        repo: repository.name,
        pull_number: issue.number
      });

      const pr = prResponse.data;
      
      // Trigger new review
      const result = await this.orchestrator.orchestratePRReview(pr, {
        eventType: 'manual_command',
        repository,
        requestedBy: context.comment.user.login,
        reviewType: args[0] || 'full'
      });
      
      await this.postComprehensiveReview(pr, result.report, repository, octokit);
      
    } catch (error) {
      await this.postComment(issue, repository, octokit, 
        `❌ Failed to perform review: ${error.message}`);
    }
  }

  async executeStatusCommand(args, context) {
    const { issue, repository, octokit } = context;
    
    try {
      // This would check for ongoing workflows for this PR
      const statusMessage = `## 🔍 AI Review Status

**PR #${issue.number}** - Current Status: **Ready**

### Available Commands:
- \`/ai-review\` - Trigger a new comprehensive review
- \`/ai-review security\` - Focus on security analysis
- \`/ai-review performance\` - Focus on performance analysis
- \`/ai-help\` - Show all available commands

### Last Analysis:
Use \`/ai-review\` to get a fresh analysis of this PR.`;

      await this.postComment(issue, repository, octokit, statusMessage);
      
    } catch (error) {
      await this.postComment(issue, repository, octokit, 
        `❌ Failed to get status: ${error.message}`);
    }
  }

  async executeHelpCommand(context) {
    const { issue, repository, octokit } = context;
    
    const helpMessage = `## 🤖 AI Code Review Assistant - Help

### Available Commands:

#### \`/ai-review [type]\`
Trigger a comprehensive code review analysis.
- \`/ai-review\` - Full analysis (feature understanding + codebase learning + code analysis)
- \`/ai-review security\` - Focus on security considerations
- \`/ai-review performance\` - Focus on performance optimization
- \`/ai-review patterns\` - Focus on code patterns and reusability

#### \`/ai-status\`
Check the current status of AI review processes for this PR.

#### \`/ai-help\`
Show this help message.

### What I Analyze:

🎯 **Feature Understanding**
- Extract requirements from JIRA tickets and PR description
- Understand business purpose and technical requirements
- Identify edge cases and system impact

🧠 **Codebase Learning**
- Discover existing functions and utilities you can reuse
- Identify established patterns in your codebase
- Find architectural constraints and guidelines

🔍 **Code Analysis**
- Suggest more efficient implementations using existing code
- Identify potential logic flaws and edge case gaps
- Provide security and performance recommendations
- Generate actionable feedback with code examples

### My Goal:
Help you build better code by leveraging your existing codebase patterns and catching potential issues early!

---
*Powered by Claude Sonnet 4 and designed to follow developer workflows*`;

    await this.postComment(issue, repository, octokit, helpMessage);
  }
  
  async postComprehensiveReview(pr, report, repository, octokit) {
    const comment = this.formatComprehensiveReview(report);
    
    try {
      await octokit.issues.createComment({
        owner: repository.owner.login,
        repo: repository.name,
        issue_number: pr.number,
        body: comment
      });

      // Also post inline comments for specific suggestions
      await this.postInlineComments(pr, report, repository, octokit);
      
    } catch (error) {
      this.logger.error('Failed to post comprehensive review', {
        pr_number: pr.number,
        repository: repository.full_name,
        error: error.message
      });
    }
  }

  async postInlineComments(pr, report, repository, octokit) {
    if (!report.findings?.suggestions) return;

    const inlineComments = report.findings.suggestions
      .filter(suggestion => suggestion.file && suggestion.line)
      .slice(0, 10); // Limit inline comments

    for (const suggestion of inlineComments) {
      try {
        const body = `💡 **${suggestion.title}**

${suggestion.message}

${suggestion.suggestedCode ? `\`\`\`suggestion\n${suggestion.suggestedCode}\n\`\`\`` : ''}

${suggestion.reasoning ? `**Reasoning:** ${suggestion.reasoning}` : ''}`;

        await octokit.pulls.createReviewComment({
          owner: repository.owner.login,
          repo: repository.name,
          pull_number: pr.number,
          body,
          path: suggestion.file,
          line: suggestion.line,
          side: 'RIGHT'
        });
      } catch (error) {
        this.logger.debug('Failed to post inline comment', {
          file: suggestion.file,
          line: suggestion.line,
          error: error.message
        });
      }
    }
  }
  
  formatComprehensiveReview(report) {
    const healthScore = report.healthScore || 0;
    const healthEmoji = healthScore >= 80 ? '🟢' : healthScore >= 60 ? '🟡' : '🔴';
    
    return `## 🤖 Comprehensive AI Code Review

${healthEmoji} **Health Score:** ${healthScore}/100 | **Risk Level:** ${report.summary?.riskLevel || 'unknown'}

### 📋 Executive Summary
**Purpose:** ${report.summary?.purpose || 'Not determined'}
**Assessment:** ${report.summary?.overallAssessment || 'Analysis completed'}
**Codebase Utilization:** ${report.summary?.codebaseUtilization || 'unknown'}

${report.summary?.keyFindings?.length > 0 ? `
**Key Findings:**
${report.summary.keyFindings.map(finding => `- ${finding}`).join('\n')}
` : ''}

### 🔍 Detailed Findings

${this.formatDetailedFindings(report.findings)}

### 📝 Recommendations

${this.formatDetailedRecommendations(report.recommendations)}

### ⚡ Workflow Performance
${this.formatWorkflowPerformance(report.workflow)}

---
<details>
<summary>🤖 About this review</summary>

This comprehensive review was generated using a multi-agent AI system that:

1. **🎯 Understood your feature** by analyzing JIRA tickets and PR context
2. **🧠 Learned your codebase** to find reusable functions and patterns  
3. **🔍 Analyzed your implementation** for efficiency and potential issues

**Model:** Claude Sonnet 4 | **Workflow ID:** \`${report.workflowId}\`
**Analysis Time:** ${Math.round(report.workflow?.totalDuration / 1000)}s

Use \`/ai-help\` for available commands.
</details>`;
  }

  formatDetailedFindings(findings) {
    if (!findings) return 'No specific findings to report.';
    
    let output = '';
    
    if (findings.critical && findings.critical.length > 0) {
      output += '#### 🚨 Critical Issues\n';
      findings.critical.forEach(finding => {
        output += `- **${finding.title || 'Critical Issue'}**`;
        if (finding.file) output += ` (${finding.file}${finding.line ? `:${finding.line}` : ''})`;
        output += `\n  ${finding.message}\n`;
      });
      output += '\n';
    }
    
    if (findings.warnings && findings.warnings.length > 0) {
      output += '#### ⚠️ Warnings\n';
      findings.warnings.forEach(warning => {
        output += `- **${warning.title || 'Warning'}**`;
        if (warning.file) output += ` (${warning.file}${warning.line ? `:${warning.line}` : ''})`;
        output += `\n  ${warning.message}\n`;
      });
      output += '\n';
    }
    
    if (findings.suggestions && findings.suggestions.length > 0) {
      const topSuggestions = findings.suggestions.slice(0, 8);
      output += '#### 💡 Suggestions\n';
      topSuggestions.forEach(suggestion => {
        output += `- **${suggestion.title || 'Suggestion'}**`;
        if (suggestion.file) output += ` (${suggestion.file})`;
        output += `\n  ${suggestion.message}\n`;
      });
      
      if (findings.suggestions.length > 8) {
        output += `\n*... and ${findings.suggestions.length - 8} more suggestions (see inline comments)*\n`;
      }
      output += '\n';
    }
    
    if (findings.positive && findings.positive.length > 0) {
      output += '#### ✅ Positive Findings\n';
      findings.positive.slice(0, 3).forEach(positive => {
        output += `- ${positive}\n`;
      });
      output += '\n';
    }
    
    return output || 'No specific issues identified. Great work! 🎉';
  }

  formatDetailedRecommendations(recommendations) {
    if (!recommendations) return 'No specific recommendations.';
    
    let output = '';
    
    if (recommendations.immediate && recommendations.immediate.length > 0) {
      output += '#### 🔥 Immediate Actions\n';
      recommendations.immediate.forEach(rec => {
        output += `- **${rec.action}**`;
        if (rec.file) output += ` (${rec.file})`;
        output += `\n  ${rec.reason}\n`;
      });
      output += '\n';
    }
    
    if (recommendations.shortTerm && recommendations.shortTerm.length > 0) {
      output += '#### 📈 Short-term Improvements\n';
      recommendations.shortTerm.slice(0, 5).forEach(rec => {
        output += `- **${rec.action}**`;
        if (rec.category) output += ` (${rec.category})`;
        output += `\n  ${rec.reason}\n`;
      });
      output += '\n';
    }
    
    if (recommendations.longTerm && recommendations.longTerm.length > 0) {
      output += '#### 🏗️ Long-term Considerations\n';
      recommendations.longTerm.slice(0, 3).forEach(rec => {
        output += `- **${rec.action}**`;
        if (rec.category) output += ` (${rec.category})`;
        output += `\n  ${rec.reason}\n`;
      });
      output += '\n';
    }
    
    return output || 'No specific recommendations at this time.';
  }

  formatWorkflowPerformance(workflow) {
    if (!workflow) return 'Workflow data not available.';
    
    const duration = Math.round(workflow.totalDuration / 1000);
    let output = `**Total Analysis Time:** ${duration}s\n\n`;
    
    if (workflow.agentPerformance) {
      output += '**Agent Performance:**\n';
      Object.entries(workflow.agentPerformance).forEach(([agent, perf]) => {
        const status = perf.success ? '✅' : '❌';
        const time = Math.round((perf.duration || 0) / 1000);
        output += `- ${status} ${agent.replace(/([A-Z])/g, ' $1').trim()}: ${time}s (${perf.efficiency || 'unknown'})\n`;
      });
    }
    
    return output;
  }
  
  async postComment(issue, repository, octokit, message) {
    await octokit.issues.createComment({
      owner: repository.owner.login,
      repo: repository.name,
      issue_number: issue.number,
      body: message
    });
  }
  
  async postErrorComment(pr, error, repository, octokit) {
    const message = `## ❌ AI Review Error

I encountered an error while analyzing this PR:

\`\`\`
${error.message}
\`\`\`

**What you can do:**
- Try running \`/ai-review\` to retry the analysis
- Check if the PR has any unusual file changes that might be causing issues
- Contact the development team if the issue persists

**Error Details:**
- Workflow: PR Review Analysis
- Timestamp: ${new Date().toISOString()}
- Repository: ${repository.full_name}

The development team has been automatically notified of this issue.`;

    await octokit.issues.createComment({
      owner: repository.owner.login,
      repo: repository.name,
      issue_number: pr.number,
      body: message
    });
  }
  
  getExpressApp() {
    return this.app.webhooks.middleware;
  }

  // Analytics and metrics access
  getAnalytics(timeRange = '24h') {
    return this.orchestrator.getAnalytics(timeRange);
  }

  getSystemMetrics() {
    return this.orchestrator.getSystemMetrics();
  }

  exportMetrics(format = 'json') {
    return this.orchestrator.exportMetrics(format);
  }

  // Health check method for monitoring
  async healthCheck() {
    try {
      // Basic health checks
      const health = {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        components: {
          orchestrator: this.orchestrator ? 'healthy' : 'unhealthy',
          notifications: this.notificationService ? 'healthy' : 'unhealthy',
          github_app: this.app ? 'healthy' : 'unhealthy'
        }
      };

      return health;
    } catch (error) {
      return {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: error.message
      };
    }
  }
}

module.exports = EnhancedGitHubApp;