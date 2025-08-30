require('dotenv').config();
const express = require('express');
const { GitHubConflictResolverApp } = require('./github-app');
const winston = require('winston');

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
  'GITHUB_CLIENT_ID',
  'GITHUB_CLIENT_SECRET',
  'CLAUDE_API_KEY',
  'JIRA_BASE_URL',
  'JIRA_EMAIL',
  'JIRA_API_TOKEN',
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
    clientId: process.env.GITHUB_CLIENT_ID,
    clientSecret: process.env.GITHUB_CLIENT_SECRET,
  },
  claude: {
    apiKey: process.env.CLAUDE_API_KEY,
    model: process.env.CLAUDE_MODEL || 'claude-3-opus-20240229',
    maxTokens: parseInt(process.env.CLAUDE_MAX_TOKENS) || 4096,
  },
  jira: {
    baseUrl: process.env.JIRA_BASE_URL,
    email: process.env.JIRA_EMAIL,
    apiToken: process.env.JIRA_API_TOKEN,
  },
  notifications: {
    slack: {
      enabled: process.env.SLACK_ENABLED === 'true',
      token: process.env.SLACK_TOKEN,
      channel: process.env.SLACK_CHANNEL || '#conflict-resolutions',
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
      from: process.env.EMAIL_FROM || 'ai-conflict-resolver@example.com',
      defaultRecipients: process.env.EMAIL_DEFAULT_RECIPIENTS?.split(',') || [],
    },
    preferences: {
      notifyOnSuccess: process.env.NOTIFY_ON_SUCCESS !== 'false',
      notifyOnFailure: process.env.NOTIFY_ON_FAILURE !== 'false',
      notifyOnLowConfidence: process.env.NOTIFY_ON_LOW_CONFIDENCE !== 'false',
      includeDetailedReport: process.env.INCLUDE_DETAILED_REPORT !== 'false',
      includeRollbackInstructions: process.env.INCLUDE_ROLLBACK !== 'false',
    },
  },
  confidenceThreshold: parseInt(process.env.CONFIDENCE_THRESHOLD) || 85,
  port: process.env.PORT || 3000,
};

// Initialize app
const app = express();
const conflictResolver = new GitHubConflictResolverApp(config);

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'ai-conflict-resolver',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
  });
});

// GitHub webhook endpoint
app.use(conflictResolver.createMiddleware());

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
  logger.info(`AI Conflict Resolver server running on port ${config.port}`);
  logger.info('Webhook endpoint: POST /webhook');
  logger.info('Health check: GET /health');
  logger.info(`Confidence threshold: ${config.confidenceThreshold}%`);
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
