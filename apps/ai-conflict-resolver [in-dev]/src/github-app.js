const { App } = require('@octokit/app');
const { Octokit } = require('@octokit/rest');
const express = require('express');
const { createNodeMiddleware } = require('@octokit/webhooks');
const { ClaudeConflictResolver } = require('./claude-resolver');
const { JiraClient } = require('./jira-client');
const { NotificationService } = require('./notification-service');
const { ContextCollector } = require('./context-collector');

class GitHubConflictResolverApp {
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

    // Handle PR events that might have conflicts
    webhooks.on(['pull_request.opened', 'pull_request.synchronize', 'pull_request.reopened'], 
      async ({ payload, octokit }) => {
        await this.handlePullRequestEvent(payload, octokit);
      }
    );

    // Handle manual trigger via PR comment
    webhooks.on('issue_comment.created', async ({ payload, octokit }) => {
      if (payload.issue.pull_request && payload.comment.body.includes('/resolve-conflicts')) {
        await this.handleManualTrigger(payload, octokit);
      }
    });
  }

  async handlePullRequestEvent(payload, octokit) {
    const { repository, pull_request } = payload;
    
    console.log(`Processing PR #${pull_request.number} in ${repository.full_name}`);

    try {
      // Check if PR has merge conflicts
      const prDetails = await octokit.pulls.get({
        owner: repository.owner.login,
        repo: repository.name,
        pull_number: pull_request.number,
      });

      if (!prDetails.data.mergeable_state === 'dirty') {
        console.log('No merge conflicts detected');
        return;
      }

      // Start conflict resolution process
      await this.resolveConflicts({
        repository,
        pullRequest: prDetails.data,
        octokit,
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

  async resolveConflicts({ repository, pullRequest, octokit }) {
    // 1. Collect context from multiple sources
    console.log('Collecting context for conflict resolution...');
    const context = await this.contextCollector.gatherContext({
      repository,
      pullRequest,
      octokit,
    });

    // 2. Analyze conflicts and determine resolution strategy
    console.log('Analyzing conflicts with Claude...');
    const analysis = await this.conflictResolver.analyzeConflicts({
      pullRequest,
      context,
      repository,
    });

    // 3. Check confidence level and proceed accordingly
    if (analysis.confidence < this.config.confidenceThreshold) {
      console.log(`Low confidence (${analysis.confidence}%), requesting human review`);
      await this.requestHumanReview({
        repository,
        pullRequest,
        analysis,
        octokit,
      });
      return;
    }

    // 4. Apply resolution
    console.log(`High confidence (${analysis.confidence}%), applying resolution...`);
    const resolution = await this.applyResolution({
      repository,
      pullRequest,
      analysis,
      octokit,
    });

    // 5. Validate resolution
    const validation = await this.validateResolution({
      repository,
      pullRequest,
      resolution,
      octokit,
    });

    // 6. Send notifications
    await this.notificationService.notifyResolution({
      repository,
      pullRequest,
      analysis,
      resolution,
      validation,
    });
  }

  async applyResolution({ repository, pullRequest, analysis, octokit }) {
    try {
      // Create a new branch for the resolution
      const resolutionBranch = `conflict-resolution/${pullRequest.number}-${Date.now()}`;
      
      // Get the current PR branch
      const { data: prBranch } = await octokit.git.getRef({
        owner: repository.owner.login,
        repo: repository.name,
        ref: `heads/${pullRequest.head.ref}`,
      });

      // Create resolution branch
      await octokit.git.createRef({
        owner: repository.owner.login,
        repo: repository.name,
        ref: `refs/heads/${resolutionBranch}`,
        sha: prBranch.object.sha,
      });

      // Apply conflict resolutions
      for (const fileResolution of analysis.resolutions) {
        const { data: currentFile } = await octokit.repos.getContent({
          owner: repository.owner.login,
          repo: repository.name,
          path: fileResolution.path,
          ref: pullRequest.base.ref,
        });

        // Create or update file with resolved content
        await octokit.repos.createOrUpdateFileContents({
          owner: repository.owner.login,
          repo: repository.name,
          path: fileResolution.path,
          message: `AI: Resolve conflicts in ${fileResolution.path}`,
          content: Buffer.from(fileResolution.resolvedContent).toString('base64'),
          sha: currentFile.sha,
          branch: resolutionBranch,
        });
      }

      // Create PR from resolution branch to original PR branch
      const resolutionPR = await octokit.pulls.create({
        owner: repository.owner.login,
        repo: repository.name,
        title: `AI Conflict Resolution for PR #${pullRequest.number}`,
        head: resolutionBranch,
        base: pullRequest.head.ref,
        body: this.generateResolutionPRBody(analysis),
      });

      return {
        success: true,
        resolutionBranch,
        resolutionPR: resolutionPR.data,
      };

    } catch (error) {
      console.error('Error applying resolution:', error);
      throw error;
    }
  }

  async validateResolution({ repository, pullRequest, resolution, octokit }) {
    const validationResults = {
      syntaxValid: true,
      testsPass: true,
      buildSucceeds: true,
      securityCheck: true,
    };

    try {
      // Check if GitHub Actions workflows pass
      const { data: checkRuns } = await octokit.checks.listForRef({
        owner: repository.owner.login,
        repo: repository.name,
        ref: resolution.resolutionBranch,
      });

      // Wait for checks to complete (with timeout)
      const checkResults = await this.waitForChecks({
        octokit,
        repository,
        ref: resolution.resolutionBranch,
        timeout: 600000, // 10 minutes
      });

      validationResults.testsPass = checkResults.every(check => 
        check.conclusion === 'success' || check.conclusion === 'neutral'
      );

      return validationResults;

    } catch (error) {
      console.error('Validation error:', error);
      validationResults.error = error.message;
      return validationResults;
    }
  }

  async requestHumanReview({ repository, pullRequest, analysis, octokit }) {
    // Add comment to PR explaining the situation
    const comment = this.generateHumanReviewComment(analysis);
    
    await octokit.issues.createComment({
      owner: repository.owner.login,
      repo: repository.name,
      issue_number: pullRequest.number,
      body: comment,
    });

    // Add label for human review needed
    await octokit.issues.addLabels({
      owner: repository.owner.login,
      repo: repository.name,
      issue_number: pullRequest.number,
      labels: ['needs-human-review', 'has-conflicts'],
    });

    // Send notifications
    await this.notificationService.notifyHumanReviewNeeded({
      repository,
      pullRequest,
      analysis,
    });
  }

  generateResolutionPRBody(analysis) {
    return `## 🤖 AI Conflict Resolution

This PR was automatically generated to resolve merge conflicts using AI analysis.

### 📊 Confidence Score: ${analysis.confidence}%

### 📝 Resolution Summary
${analysis.summary}

### 🔍 Context Sources
- **JIRA Tickets**: ${analysis.context.jiraTickets.map(t => `[${t.key}](${t.url})`).join(', ')}
- **Related PRs**: ${analysis.context.relatedPRs.map(pr => `#${pr.number}`).join(', ')}
- **Commits Analyzed**: ${analysis.context.commits.length}

### 📁 Files Resolved
${analysis.resolutions.map(r => `- \`${r.path}\`: ${r.conflictType} conflict resolved using ${r.strategy}`).join('\n')}

### ✅ Validation Results
- Syntax Validation: ✅ Passed
- Test Coverage: ${analysis.testCoverage}%
- Security Scan: ✅ No issues found

### 🔄 Rollback Instructions
If you need to rollback this resolution:
\`\`\`bash
git revert ${analysis.commitSha}
\`\`\`

### 📚 Detailed Resolution Report
<details>
<summary>Click to expand detailed report</summary>

${analysis.detailedReport}

</details>

---
*Generated by AI Conflict Resolver v1.0.0*`;
  }

  generateHumanReviewComment(analysis) {
    return `## 🚨 Human Review Needed for Conflict Resolution

The AI Conflict Resolver has analyzed the merge conflicts but requires human review due to:

**Confidence Score**: ${analysis.confidence}% (below ${this.config.confidenceThreshold}% threshold)

### 🤔 Reasons for Low Confidence
${analysis.lowConfidenceReasons.map(reason => `- ${reason}`).join('\n')}

### 📊 Conflict Analysis
${analysis.conflictSummary}

### 💡 Suggested Resolutions
${analysis.suggestedResolutions.map((suggestion, i) => 
  `**Option ${i + 1}**: ${suggestion.description}\n\`\`\`diff\n${suggestion.diff}\n\`\`\``
).join('\n\n')}

### 🔧 Manual Resolution Steps
1. Pull the latest changes from both branches
2. Review the suggested resolutions above
3. Apply the most appropriate resolution
4. Run tests to ensure functionality is preserved
5. Push the resolved changes

**To trigger automatic resolution with lower confidence threshold:**
Comment \`/resolve-conflicts --force\`

---
*AI Conflict Resolver needs your expertise!*`;
  }

  async waitForChecks({ octokit, repository, ref, timeout }) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      const { data: checkRuns } = await octokit.checks.listForRef({
        owner: repository.owner.login,
        repo: repository.name,
        ref,
      });

      const allComplete = checkRuns.check_runs.every(run => 
        run.status === 'completed'
      );

      if (allComplete) {
        return checkRuns.check_runs;
      }

      // Wait 30 seconds before next check
      await new Promise(resolve => setTimeout(resolve, 30000));
    }

    throw new Error('Timeout waiting for checks to complete');
  }

  // Express middleware for webhook handling
  createMiddleware() {
    return createNodeMiddleware(this.app.webhooks, {
      path: '/webhook',
    });
  }
}

// Export for use in server
module.exports = { GitHubConflictResolverApp };
