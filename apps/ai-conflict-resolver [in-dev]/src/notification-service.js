const { WebClient } = require('@slack/web-api');
const nodemailer = require('nodemailer');
const { marked } = require('marked');

class NotificationService {
  constructor(config) {
    this.config = config;
    
    // Initialize Slack client
    if (config.slack?.enabled) {
      this.slackClient = new WebClient(config.slack.token);
      this.slackChannel = config.slack.channel;
    }

    // Initialize email transporter
    if (config.email?.enabled) {
      this.emailTransporter = nodemailer.createTransport({
        host: config.email.smtp.host,
        port: config.email.smtp.port,
        secure: config.email.smtp.secure,
        auth: {
          user: config.email.smtp.user,
          pass: config.email.smtp.pass,
        },
      });
    }

    // Notification preferences
    this.preferences = config.preferences || {
      notifyOnSuccess: true,
      notifyOnFailure: true,
      notifyOnLowConfidence: true,
      includeDetailedReport: true,
      includeRollbackInstructions: true,
    };
  }

  async notifyResolution({ repository, pullRequest, analysis, resolution, validation }) {
    console.log('Sending resolution notifications...');

    const notification = this.buildResolutionNotification({
      repository,
      pullRequest,
      analysis,
      resolution,
      validation,
    });

    const notificationPromises = [];

    // Send Slack notification
    if (this.slackClient && this.preferences.notifyOnSuccess) {
      notificationPromises.push(
        this.sendSlackNotification(notification.slack)
      );
    }

    // Send email notification
    if (this.emailTransporter && this.preferences.notifyOnSuccess) {
      notificationPromises.push(
        this.sendEmailNotification(notification.email)
      );
    }

    // Add comment to PR
    notificationPromises.push(
      this.addPRComment({
        repository,
        pullRequest,
        content: notification.prComment,
      })
    );

    await Promise.all(notificationPromises);
  }

  async notifyError({ repository, pullRequest, error }) {
    console.error('Sending error notification...');

    const notification = this.buildErrorNotification({
      repository,
      pullRequest,
      error,
    });

    const notificationPromises = [];

    if (this.slackClient) {
      notificationPromises.push(
        this.sendSlackNotification(notification.slack)
      );
    }

    if (this.emailTransporter) {
      notificationPromises.push(
        this.sendEmailNotification(notification.email)
      );
    }

    await Promise.all(notificationPromises);
  }

  async notifyHumanReviewNeeded({ repository, pullRequest, analysis }) {
    console.log('Sending human review needed notification...');

    const notification = this.buildHumanReviewNotification({
      repository,
      pullRequest,
      analysis,
    });

    const notificationPromises = [];

    if (this.slackClient && this.preferences.notifyOnLowConfidence) {
      notificationPromises.push(
        this.sendSlackNotification(notification.slack)
      );
    }

    if (this.emailTransporter && this.preferences.notifyOnLowConfidence) {
      notificationPromises.push(
        this.sendEmailNotification(notification.email)
      );
    }

    await Promise.all(notificationPromises);
  }

  async notifyReviewComplete({ pr, report, repository, workflowId }) {
    console.log('Sending review complete notifications...');

    const notification = this.buildReviewCompleteNotification({
      pr,
      report,
      repository,
      workflowId
    });

    const notificationPromises = [];

    // Send Slack notification
    if (this.slackClient && this.preferences.notifyOnSuccess) {
      notificationPromises.push(
        this.sendSlackNotification(notification.slack)
      );
    }

    // Send email notification
    if (this.emailTransporter && this.preferences.notifyOnSuccess) {
      notificationPromises.push(
        this.sendEmailNotification(notification.email)
      );
    }

    await Promise.all(notificationPromises);
  }

  buildReviewCompleteNotification({ pr, report, repository, workflowId }) {
    const healthScore = report.healthScore || 0;
    const emoji = healthScore >= 80 ? '✅' : healthScore >= 60 ? '⚠️' : '❌';
    const status = healthScore >= 80 ? 'Excellent' : healthScore >= 60 ? 'Good' : 'Needs Attention';

    const summary = `
${emoji} **Code Review Complete**
Repository: ${repository.full_name}
PR #${pr.number}: ${pr.title}
Health Score: ${healthScore}%
Status: ${status}
    `.trim();

    return {
      slack: {
        blocks: [{
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: summary
          }
        }]
      },
      email: {
        subject: `[${repository.name}] ${emoji} Code Review Complete - PR #${pr.number}`,
        html: summary.replace(/\n/g, '<br>'),
        to: this.getRecipients(pr)
      }
    };
  }

  buildResolutionNotification({ repository, pullRequest, analysis, resolution, validation }) {
    const isSuccess = resolution.success && validation.testsPass;
    const emoji = isSuccess ? '✅' : '⚠️';
    const status = isSuccess ? 'Successfully Resolved' : 'Resolution Needs Review';

    const summary = `
${emoji} **Merge Conflict ${status}**
Repository: ${repository.full_name}
PR #${pullRequest.number}: ${pullRequest.title}
Confidence: ${analysis.confidence}%
Files Resolved: ${analysis.resolutions.length}
    `.trim();

    // Slack notification
    const slackBlocks = [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: `${emoji} Merge Conflict ${status}`,
        },
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: summary,
        },
      },
      {
        type: 'section',
        fields: [
          {
            type: 'mrkdwn',
            text: `*Confidence Score:*\n${analysis.confidence}%`,
          },
          {
            type: 'mrkdwn',
            text: `*Risk Level:*\n${analysis.riskAssessment.level}`,
          },
        ],
      },
    ];

    if (this.preferences.includeDetailedReport) {
      slackBlocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Files Resolved:*\n${analysis.resolutions.map(r => `• \`${r.path}\` - ${r.strategy}`).join('\n')}`,
        },
      });
    }

    slackBlocks.push({
      type: 'actions',
      elements: [
        {
          type: 'button',
          text: {
            type: 'plain_text',
            text: 'View PR',
          },
          url: pullRequest.html_url,
          style: 'primary',
        },
        {
          type: 'button',
          text: {
            type: 'plain_text',
            text: 'View Resolution PR',
          },
          url: resolution.resolutionPR?.html_url,
        },
      ],
    });

    // Email content
    const emailHtml = this.buildEmailHtml({
      title: `${emoji} Merge Conflict ${status}`,
      summary,
      details: this.buildDetailedReport({ analysis, resolution, validation }),
      actions: [
        { text: 'View PR', url: pullRequest.html_url },
        { text: 'View Resolution', url: resolution.resolutionPR?.html_url },
      ],
    });

    // PR comment
    const prComment = this.buildPRComment({ analysis, resolution, validation });

    return {
      slack: { blocks: slackBlocks },
      email: {
        subject: `[${repository.name}] ${emoji} Conflict ${status} - PR #${pullRequest.number}`,
        html: emailHtml,
        to: this.getRecipients(pullRequest),
      },
      prComment,
    };
  }

  buildErrorNotification({ repository, pullRequest, error }) {
    const summary = `
❌ **Conflict Resolution Failed**
Repository: ${repository.full_name}
PR #${pullRequest.number}: ${pullRequest.title}
Error: ${error.message}
    `.trim();

    const slackBlocks = [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: '❌ Conflict Resolution Failed',
        },
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: summary,
        },
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `\`\`\`${error.stack || error.message}\`\`\``,
        },
      },
    ];

    const emailHtml = this.buildEmailHtml({
      title: '❌ Conflict Resolution Failed',
      summary,
      details: `<pre>${error.stack || error.message}</pre>`,
      actions: [
        { text: 'View PR', url: pullRequest.html_url },
      ],
    });

    return {
      slack: { blocks: slackBlocks },
      email: {
        subject: `[${repository.name}] ❌ Conflict Resolution Failed - PR #${pullRequest.number}`,
        html: emailHtml,
        to: this.getRecipients(pullRequest),
      },
    };
  }

  buildHumanReviewNotification({ repository, pullRequest, analysis }) {
    const summary = `
🤔 **Human Review Required**
Repository: ${repository.full_name}
PR #${pullRequest.number}: ${pullRequest.title}
Confidence: ${analysis.confidence}% (below threshold)
Reasons: ${analysis.lowConfidenceReasons.join(', ')}
    `.trim();

    const slackBlocks = [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: '🤔 Human Review Required',
        },
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: summary,
        },
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Low Confidence Reasons:*\n${analysis.lowConfidenceReasons.map(r => `• ${r}`).join('\n')}`,
        },
      },
      {
        type: 'actions',
        elements: [
          {
            type: 'button',
            text: {
              type: 'plain_text',
              text: 'Review PR',
            },
            url: pullRequest.html_url,
            style: 'primary',
          },
        ],
      },
    ];

    const emailHtml = this.buildEmailHtml({
      title: '🤔 Human Review Required',
      summary,
      details: this.buildHumanReviewDetails(analysis),
      actions: [
        { text: 'Review PR', url: pullRequest.html_url },
      ],
    });

    return {
      slack: { blocks: slackBlocks },
      email: {
        subject: `[${repository.name}] 🤔 Human Review Required - PR #${pullRequest.number}`,
        html: emailHtml,
        to: this.getRecipients(pullRequest),
      },
    };
  }

  buildDetailedReport({ analysis, resolution, validation }) {
    return `
<h3>📊 Resolution Summary</h3>
<p><strong>Confidence Score:</strong> ${analysis.confidence}%</p>
<p><strong>Risk Assessment:</strong> ${analysis.riskAssessment.level}</p>
<p><strong>Test Coverage:</strong> ${analysis.testCoverage}%</p>

<h3>📁 Files Resolved</h3>
<ul>
${analysis.resolutions.map(r => `
  <li>
    <code>${r.path}</code>
    <ul>
      <li>Conflict Type: ${r.conflictType}</li>
      <li>Strategy: ${r.strategy}</li>
      <li>Explanation: ${r.explanation}</li>
    </ul>
  </li>
`).join('')}
</ul>

<h3>✅ Validation Results</h3>
<ul>
  <li>Syntax Valid: ${validation.syntaxValid ? '✅' : '❌'}</li>
  <li>Tests Pass: ${validation.testsPass ? '✅' : '❌'}</li>
  <li>Build Succeeds: ${validation.buildSucceeds ? '✅' : '❌'}</li>
  <li>Security Check: ${validation.securityCheck ? '✅' : '❌'}</li>
</ul>

${this.preferences.includeRollbackInstructions ? `
<h3>🔄 Rollback Instructions</h3>
<p>If you need to rollback this resolution:</p>
<pre><code>git revert ${resolution.resolutionPR?.merge_commit_sha || 'COMMIT_SHA'}</code></pre>
` : ''}
    `;
  }

  buildHumanReviewDetails(analysis) {
    return `
<h3>🤔 Why Human Review is Needed</h3>
<ul>
${analysis.lowConfidenceReasons.map(reason => `<li>${reason}</li>`).join('')}
</ul>

<h3>💡 Suggested Resolutions</h3>
${analysis.suggestedResolutions.map((suggestion, i) => `
<h4>Option ${i + 1}: ${suggestion.description}</h4>
<pre><code>${suggestion.diff}</code></pre>
`).join('')}

<h3>📋 Conflict Analysis</h3>
<p>${analysis.conflictSummary || analysis.summary}</p>
    `;
  }

  buildEmailHtml({ title, summary, details, actions }) {
    return `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background-color: #f4f4f4; padding: 20px; text-align: center; }
    .content { padding: 20px; }
    .button { display: inline-block; padding: 10px 20px; margin: 10px 5px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    .button:hover { background-color: #0056b3; }
    pre { background-color: #f4f4f4; padding: 10px; overflow-x: auto; }
    code { background-color: #f4f4f4; padding: 2px 4px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>${title}</h1>
    </div>
    <div class="content">
      <p>${summary.replace(/\n/g, '<br>')}</p>
      ${details}
      <div style="text-align: center; margin-top: 30px;">
        ${actions.map(action => `
          <a href="${action.url}" class="button">${action.text}</a>
        `).join('')}
      </div>
    </div>
  </div>
</body>
</html>
    `;
  }

  buildPRComment({ analysis, resolution, validation }) {
    // This would be posted to the PR
    return `## 🤖 AI Conflict Resolution Report

### 📊 Summary
- **Confidence Score:** ${analysis.confidence}%
- **Files Resolved:** ${analysis.resolutions.length}
- **Resolution Status:** ${resolution.success ? '✅ Success' : '⚠️ Needs Review'}

### 📁 Resolved Files
${analysis.resolutions.map(r => `- \`${r.path}\` - ${r.strategy} strategy`).join('\n')}

### ✅ Validation
- Tests: ${validation.testsPass ? '✅ Passing' : '❌ Failed'}
- Build: ${validation.buildSucceeds ? '✅ Success' : '❌ Failed'}
- Security: ${validation.securityCheck ? '✅ Clean' : '⚠️ Issues Found'}

${resolution.resolutionPR ? `
### 🔗 Resolution PR
A separate PR has been created with the resolved conflicts: #${resolution.resolutionPR.number}

You can:
1. Review the resolution PR
2. Merge it into this PR if satisfied
3. Make manual adjustments if needed
` : ''}

---
*Generated by AI Conflict Resolver v1.0.0*`;
  }

  async sendSlackNotification(message) {
    try {
      await this.slackClient.chat.postMessage({
        channel: this.slackChannel,
        ...message,
      });
      console.log('Slack notification sent successfully');
    } catch (error) {
      console.error('Error sending Slack notification:', error);
    }
  }

  async sendEmailNotification({ to, subject, html }) {
    try {
      await this.emailTransporter.sendMail({
        from: this.config.email.from,
        to: Array.isArray(to) ? to.join(', ') : to,
        subject,
        html,
      });
      console.log('Email notification sent successfully');
    } catch (error) {
      console.error('Error sending email notification:', error);
    }
  }

  async addPRComment({ repository, pullRequest, content }) {
    // This would use the GitHub API to add a comment
    // Implementation depends on how the GitHub client is passed
    console.log('Would add PR comment:', content);
  }

  getRecipients(pullRequest) {
    const recipients = [];
    
    // PR author
    if (pullRequest.user?.email) {
      recipients.push(pullRequest.user.email);
    }

    // Reviewers
    if (pullRequest.requested_reviewers) {
      recipients.push(...pullRequest.requested_reviewers
        .map(reviewer => reviewer.email)
        .filter(Boolean)
      );
    }

    // Default recipients from config
    if (this.config.email?.defaultRecipients) {
      recipients.push(...this.config.email.defaultRecipients);
    }

    return [...new Set(recipients)];
  }
}

module.exports = { NotificationService };
