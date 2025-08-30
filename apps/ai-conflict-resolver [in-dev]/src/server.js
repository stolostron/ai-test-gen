require('dotenv').config();
const express = require('express');
const EnhancedGitHubApp = require('./github-app-enhanced');
const winston = require('winston');
const loggingConfig = require('./config/logging-config');

// Configure logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  defaultMeta: { service: 'ai-conflict-resolver' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple(),
    }),
  ],
});

// Validate required environment variables
const requiredEnvVars = [
  'GITHUB_APP_ID',
  'GITHUB_PRIVATE_KEY',
  'GITHUB_WEBHOOK_SECRET',
  'CLAUDE_API_KEY',
];

const missingEnvVars = requiredEnvVars.filter(varName => !process.env[varName]);
if (missingEnvVars.length > 0) {
  logger.error(`Missing required environment variables: ${missingEnvVars.join(', ')}`);
  logger.error('Please check your .env file or environment configuration');
  process.exit(1);
}

// Configuration
const config = {
  github: {
    appId: process.env.GITHUB_APP_ID,
    privateKey: process.env.GITHUB_PRIVATE_KEY.replace(/\\n/g, '\n'),
    webhookSecret: process.env.GITHUB_WEBHOOK_SECRET,
  },
  claudeApiKey: process.env.CLAUDE_API_KEY,
  maxContextTokens: parseInt(process.env.MAX_CONTEXT_TOKENS) || 150000,
  reserveTokens: parseInt(process.env.RESERVE_TOKENS) || 20000,
  jira: {
    baseUrl: process.env.JIRA_BASE_URL,
    email: process.env.JIRA_EMAIL,
    apiToken: process.env.JIRA_API_TOKEN,
  },
  notifications: {
    slack: {
      enabled: process.env.SLACK_ENABLED === 'true',
      token: process.env.SLACK_TOKEN,
      channel: process.env.SLACK_CHANNEL || '#ai-code-review',
    },
    email: {
      enabled: process.env.EMAIL_ENABLED === 'true',
      smtp: {
        host: process.env.SMTP_HOST,
        port: parseInt(process.env.SMTP_PORT) || 587,
        secure: process.env.SMTP_SECURE === 'true',
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS,
      },
      from: process.env.EMAIL_FROM || 'ai-code-review@example.com',
      defaultRecipients: process.env.EMAIL_DEFAULT_RECIPIENTS?.split(',') || [],
    },
    preferences: {
      notifyOnSuccess: process.env.NOTIFY_ON_SUCCESS !== 'false',
      notifyOnFailure: process.env.NOTIFY_ON_FAILURE !== 'false',
      notifyOnReview: process.env.NOTIFY_ON_REVIEW !== 'false',
      includeDetailedReport: process.env.INCLUDE_DETAILED_REPORT !== 'false',
    },
  },
  // Enhanced logging and metrics configuration
  ...loggingConfig,
  port: process.env.PORT || 3000,
};

// Initialize app
const app = express();
const enhancedGitHubApp = new EnhancedGitHubApp(config);

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    const health = await enhancedGitHubApp.healthCheck();
    res.json({
      ...health,
      service: 'ai-code-review-system',
      version: '2.0.0',
    });
  } catch (error) {
    res.status(500).json({
      status: 'unhealthy',
      service: 'ai-code-review-system',
      version: '2.0.0',
      error: error.message,
      timestamp: new Date().toISOString(),
    });
  }
});

// API endpoint for manual reviews
app.post('/api/review', express.json(), async (req, res) => {
  try {
    const { repository, pr_number } = req.body;
    
    if (!repository || !pr_number) {
      return res.status(400).json({
        error: 'Missing required parameters: repository and pr_number'
      });
    }
    
    res.json({
      message: 'Manual review not yet implemented',
      repository,
      pr_number
    });
  } catch (error) {
    logger.error('Manual review API error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Analytics and metrics endpoints
app.get('/api/analytics', async (req, res) => {
  try {
    const timeRange = req.query.range || '24h';
    const analytics = enhancedGitHubApp.getAnalytics(timeRange);
    
    res.json({
      success: true,
      timeRange,
      analytics,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    logger.error('Analytics API error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/metrics', async (req, res) => {
  try {
    const format = req.query.format || 'json';
    const metrics = enhancedGitHubApp.exportMetrics(format);
    
    if (format === 'prometheus') {
      res.set('Content-Type', 'text/plain');
      res.send(metrics);
    } else {
      res.json({
        success: true,
        format,
        metrics: JSON.parse(metrics),
        timestamp: new Date().toISOString()
      });
    }
  } catch (error) {
    logger.error('Metrics API error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/system', async (req, res) => {
  try {
    const systemMetrics = enhancedGitHubApp.getSystemMetrics();
    
    res.json({
      success: true,
      system: systemMetrics,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    logger.error('System metrics API error:', error);
    res.status(500).json({ error: error.message });
  }
});

// GitHub webhook endpoint
app.use('/webhook', enhancedGitHubApp.getExpressApp());

// Error handling middleware
app.use((error, req, res, next) => {
  logger.error('Unhandled error:', error);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? error.message : undefined,
  });
});

// Start server
const server = app.listen(config.port, () => {
  logger.info(`AI Code Review & Conflict Resolution System running on port ${config.port}`);
  logger.info('Webhook endpoint: POST /webhook');
  logger.info('Health check: GET /health');
  logger.info('Manual review API: POST /api/review');
  logger.info('Analytics API: GET /api/analytics?range=24h');
  logger.info('Metrics API: GET /api/metrics?format=json');
  logger.info('System metrics API: GET /api/system');
  logger.info(`GitHub App ID: ${config.github.appId}`);
  logger.info(`Max context tokens: ${config.maxContextTokens}`);
  logger.info(`Slack notifications: ${config.notifications.slack.enabled ? 'enabled' : 'disabled'}`);
  logger.info(`Email notifications: ${config.notifications.email.enabled ? 'enabled' : 'disabled'}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM signal received: closing HTTP server');
  server.close(() => {
    logger.info('HTTP server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  logger.info('SIGINT signal received: closing HTTP server');
  server.close(() => {
    logger.info('HTTP server closed');
    process.exit(0);
  });
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

module.exports = { app, server };
