module.exports = {
  // Enhanced logging configuration
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    enableFileLogging: process.env.ENABLE_FILE_LOGGING !== 'false',
    enableConsoleLogging: process.env.ENABLE_CONSOLE_LOGGING !== 'false',
    logDirectory: process.env.LOG_DIRECTORY || 'logs',
    maxFileSize: process.env.LOG_MAX_FILE_SIZE || '20m',
    maxFiles: parseInt(process.env.LOG_MAX_FILES) || 14,
    enableStructuredLogging: process.env.ENABLE_STRUCTURED_LOGGING !== 'false',
    
    // Sensitive fields to mask in logs
    sensitiveFields: [
      'password', 'token', 'secret', 'key', 'auth', 'credential',
      'private_key', 'api_key', 'webhook_secret', 'bearer',
      'authorization', 'x-api-key', 'client_secret'
    ]
  },

  // Metrics collection configuration
  metrics: {
    enabled: process.env.METRICS_ENABLED !== 'false',
    
    // External monitoring integration
    externalMonitoring: {
      enabled: process.env.EXTERNAL_MONITORING_ENABLED === 'true',
      prometheus: {
        enabled: process.env.PROMETHEUS_ENABLED === 'true',
        endpoint: process.env.PROMETHEUS_ENDPOINT || 'http://localhost:9090',
        pushGateway: process.env.PROMETHEUS_PUSH_GATEWAY
      },
      datadog: {
        enabled: process.env.DATADOG_ENABLED === 'true',
        apiKey: process.env.DATADOG_API_KEY,
        appKey: process.env.DATADOG_APP_KEY,
        site: process.env.DATADOG_SITE || 'datadoghq.com'
      },
      newrelic: {
        enabled: process.env.NEWRELIC_ENABLED === 'true',
        licenseKey: process.env.NEWRELIC_LICENSE_KEY,
        appName: process.env.NEWRELIC_APP_NAME || 'ai-code-review-system'
      }
    },
    
    // Retention policies
    retention: {
      metrics: parseInt(process.env.METRICS_RETENTION_DAYS) || 7, // days
      logs: parseInt(process.env.LOGS_RETENTION_DAYS) || 14 // days
    },
    
    // Performance thresholds for alerting
    thresholds: {
      prReviewDuration: parseInt(process.env.PR_REVIEW_DURATION_THRESHOLD) || 120000, // 2 minutes
      agentExecutionDuration: parseInt(process.env.AGENT_EXECUTION_DURATION_THRESHOLD) || 45000, // 45 seconds
      healthScoreThreshold: parseInt(process.env.HEALTH_SCORE_THRESHOLD) || 60,
      errorRateThreshold: parseInt(process.env.ERROR_RATE_THRESHOLD) || 5 // percent
    }
  },

  // Alerting configuration
  alerting: {
    enabled: process.env.ALERTING_ENABLED === 'true',
    
    channels: {
      slack: {
        enabled: process.env.SLACK_ALERTS_ENABLED === 'true',
        webhookUrl: process.env.SLACK_ALERT_WEBHOOK_URL,
        channel: process.env.SLACK_ALERT_CHANNEL || '#alerts'
      },
      email: {
        enabled: process.env.EMAIL_ALERTS_ENABLED === 'true',
        recipients: process.env.ALERT_EMAIL_RECIPIENTS?.split(',') || [],
        smtp: {
          host: process.env.ALERT_SMTP_HOST,
          port: parseInt(process.env.ALERT_SMTP_PORT) || 587,
          secure: process.env.ALERT_SMTP_SECURE === 'true',
          auth: {
            user: process.env.ALERT_SMTP_USER,
            pass: process.env.ALERT_SMTP_PASS
          }
        }
      },
      pagerduty: {
        enabled: process.env.PAGERDUTY_ENABLED === 'true',
        integrationKey: process.env.PAGERDUTY_INTEGRATION_KEY,
        severity: process.env.PAGERDUTY_DEFAULT_SEVERITY || 'warning'
      }
    },
    
    rules: [
      {
        name: 'high_error_rate',
        condition: 'error_rate > 5%',
        severity: 'warning',
        description: 'Error rate is above threshold'
      },
      {
        name: 'slow_pr_reviews',
        condition: 'average_pr_review_duration > 120s',
        severity: 'warning',
        description: 'PR reviews are taking longer than expected'
      },
      {
        name: 'low_health_scores',
        condition: 'average_health_score < 60',
        severity: 'info',
        description: 'Recent PR health scores are below threshold'
      },
      {
        name: 'agent_failures',
        condition: 'agent_failure_rate > 10%',
        severity: 'critical',
        description: 'High agent failure rate detected'
      },
      {
        name: 'api_errors',
        condition: 'api_error_count > 10/hour',
        severity: 'warning',
        description: 'High API error rate detected'
      }
    ]
  },

  // Dashboard configuration
  dashboard: {
    enabled: process.env.DASHBOARD_ENABLED === 'true',
    refreshInterval: parseInt(process.env.DASHBOARD_REFRESH_INTERVAL) || 30000, // 30 seconds
    
    widgets: [
      {
        type: 'metric',
        title: 'PR Reviews Today',
        metric: 'pr_reviews_total',
        timeRange: '24h'
      },
      {
        type: 'metric',
        title: 'Success Rate',
        metric: 'pr_reviews_success_rate',
        timeRange: '24h',
        format: 'percentage'
      },
      {
        type: 'metric',
        title: 'Average Health Score',
        metric: 'average_health_score',
        timeRange: '24h'
      },
      {
        type: 'chart',
        title: 'Review Duration Trend',
        metric: 'pr_review_duration',
        timeRange: '7d',
        chartType: 'line'
      },
      {
        type: 'chart',
        title: 'Error Rate Trend',
        metric: 'error_rate',
        timeRange: '24h',
        chartType: 'area'
      },
      {
        type: 'table',
        title: 'Recent Workflows',
        data: 'recent_workflows',
        limit: 10
      }
    ]
  },

  // Security logging
  security: {
    enabled: process.env.SECURITY_LOGGING_ENABLED !== 'false',
    
    events: [
      'authentication_failure',
      'authorization_failure',
      'suspicious_activity',
      'rate_limit_exceeded',
      'sensitive_data_access',
      'configuration_change'
    ],
    
    retention: parseInt(process.env.SECURITY_LOG_RETENTION_DAYS) || 90, // days
    
    // SIEM integration
    siem: {
      enabled: process.env.SIEM_ENABLED === 'true',
      endpoint: process.env.SIEM_ENDPOINT,
      format: process.env.SIEM_FORMAT || 'syslog'
    }
  },

  // Audit trail configuration
  audit: {
    enabled: process.env.AUDIT_ENABLED !== 'false',
    
    events: [
      'workflow_started',
      'workflow_completed',
      'workflow_failed',
      'manual_command_executed',
      'configuration_changed',
      'user_action'
    ],
    
    retention: parseInt(process.env.AUDIT_RETENTION_DAYS) || 365, // days
    
    // Compliance requirements
    compliance: {
      sox: process.env.SOX_COMPLIANCE === 'true',
      gdpr: process.env.GDPR_COMPLIANCE === 'true',
      hipaa: process.env.HIPAA_COMPLIANCE === 'true'
    }
  }
};