const winston = require('winston');
const path = require('path');

class EnhancedLogger {
  constructor(config = {}) {
    this.config = {
      level: config.level || process.env.LOG_LEVEL || 'info',
      enableFileLogging: config.enableFileLogging !== false,
      enableConsoleLogging: config.enableConsoleLogging !== false,
      logDirectory: config.logDirectory || 'logs',
      maxFileSize: config.maxFileSize || '20m',
      maxFiles: config.maxFiles || 14,
      enableStructuredLogging: config.enableStructuredLogging !== false,
      sensitiveFields: config.sensitiveFields || [
        'password', 'token', 'secret', 'key', 'auth', 'credential',
        'private_key', 'api_key', 'webhook_secret'
      ],
      ...config
    };

    this.loggers = new Map();
    this.setupDefaultLogger();
  }

  setupDefaultLogger() {
    const transports = [];

    // Console transport
    if (this.config.enableConsoleLogging) {
      transports.push(new winston.transports.Console({
        format: winston.format.combine(
          winston.format.colorize(),
          winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
          winston.format.errors({ stack: true }),
          winston.format.printf(({ timestamp, level, message, component, ...meta }) => {
            const componentStr = component ? `[${component}] ` : '';
            const metaStr = Object.keys(meta).length > 0 ? ` ${JSON.stringify(meta)}` : '';
            return `${timestamp} ${level}: ${componentStr}${message}${metaStr}`;
          })
        )
      }));
    }

    // File transports
    if (this.config.enableFileLogging) {
      // Error log
      transports.push(new winston.transports.File({
        filename: path.join(this.config.logDirectory, 'error.log'),
        level: 'error',
        maxsize: this.config.maxFileSize,
        maxFiles: this.config.maxFiles,
        format: winston.format.combine(
          winston.format.timestamp(),
          winston.format.errors({ stack: true }),
          winston.format.json()
        )
      }));

      // Combined log
      transports.push(new winston.transports.File({
        filename: path.join(this.config.logDirectory, 'combined.log'),
        maxsize: this.config.maxFileSize,
        maxFiles: this.config.maxFiles,
        format: winston.format.combine(
          winston.format.timestamp(),
          winston.format.errors({ stack: true }),
          winston.format.json()
        )
      }));

      // Workflow-specific logs
      transports.push(new winston.transports.File({
        filename: path.join(this.config.logDirectory, 'workflows.log'),
        level: 'info',
        maxsize: this.config.maxFileSize,
        maxFiles: this.config.maxFiles,
        format: winston.format.combine(
          winston.format.timestamp(),
          winston.format.json(),
          winston.format((info) => {
            return info.workflow_id ? info : false;
          })()
        )
      }));

      // Performance logs
      transports.push(new winston.transports.File({
        filename: path.join(this.config.logDirectory, 'performance.log'),
        level: 'info',
        maxsize: this.config.maxFileSize,
        maxFiles: this.config.maxFiles,
        format: winston.format.combine(
          winston.format.timestamp(),
          winston.format.json(),
          winston.format((info) => {
            return info.performance || info.duration || info.timing ? info : false;
          })()
        )
      }));
    }

    const defaultLogger = winston.createLogger({
      level: this.config.level,
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        this.config.enableStructuredLogging ? winston.format.json() : winston.format.simple()
      ),
      transports,
      exceptionHandlers: this.config.enableFileLogging ? [
        new winston.transports.File({
          filename: path.join(this.config.logDirectory, 'exceptions.log')
        })
      ] : []
    });

    this.loggers.set('default', defaultLogger);
  }

  getLogger(component = 'default') {
    if (!this.loggers.has(component)) {
      const logger = winston.createLogger({
        level: this.config.level,
        defaultMeta: { component },
        format: winston.format.combine(
          winston.format.timestamp(),
          winston.format.errors({ stack: true }),
          winston.format.json()
        ),
        transports: this.loggers.get('default').transports
      });
      
      this.loggers.set(component, logger);
    }
    
    return this.loggers.get(component);
  }

  // Enhanced logging methods with automatic sanitization
  info(message, meta = {}, component = 'default') {
    const sanitizedMeta = this.sanitizeSensitiveData(meta);
    this.getLogger(component).info(message, sanitizedMeta);
  }

  warn(message, meta = {}, component = 'default') {
    const sanitizedMeta = this.sanitizeSensitiveData(meta);
    this.getLogger(component).warn(message, sanitizedMeta);
  }

  error(message, meta = {}, component = 'default') {
    const sanitizedMeta = this.sanitizeSensitiveData(meta);
    this.getLogger(component).error(message, sanitizedMeta);
  }

  debug(message, meta = {}, component = 'default') {
    const sanitizedMeta = this.sanitizeSensitiveData(meta);
    this.getLogger(component).debug(message, sanitizedMeta);
  }

  // Workflow-specific logging
  logWorkflowStart(workflowId, pr, options = {}) {
    this.info('Workflow started', {
      workflow_id: workflowId,
      workflow_type: 'pr_review',
      pr_number: pr.number,
      repository: pr.base.repo.full_name,
      author: pr.user.login,
      branch: pr.head.ref,
      base_branch: pr.base.ref,
      draft: pr.draft,
      event_type: options.eventType,
      performance: true,
      timing: {
        start_time: Date.now(),
        iso_start: new Date().toISOString()
      }
    }, 'workflow');
  }

  logWorkflowPhase(workflowId, phase, status, duration = null, result = null) {
    this.info(`Workflow phase ${status}`, {
      workflow_id: workflowId,
      phase,
      status,
      duration,
      result_summary: result ? this.summarizeResult(result) : null,
      performance: true,
      timing: {
        phase_timestamp: Date.now(),
        iso_timestamp: new Date().toISOString()
      }
    }, 'workflow');
  }

  logWorkflowComplete(workflowId, totalDuration, report) {
    this.info('Workflow completed', {
      workflow_id: workflowId,
      total_duration: totalDuration,
      health_score: report.healthScore,
      findings_summary: {
        critical: report.findings?.critical?.length || 0,
        warnings: report.findings?.warnings?.length || 0,
        suggestions: report.findings?.suggestions?.length || 0
      },
      performance: true,
      timing: {
        end_time: Date.now(),
        iso_end: new Date().toISOString(),
        total_duration: totalDuration
      }
    }, 'workflow');
  }

  logWorkflowError(workflowId, phase, error, context = {}) {
    this.error('Workflow error', {
      workflow_id: workflowId,
      phase,
      error_message: error.message,
      error_type: error.constructor.name,
      error_stack: error.stack,
      context: this.sanitizeSensitiveData(context),
      timing: {
        error_time: Date.now(),
        iso_error: new Date().toISOString()
      }
    }, 'workflow');
  }

  // Agent-specific logging
  logAgentExecution(agentType, workflowId, operation, status, duration = null, context = {}) {
    this.info(`Agent ${operation} ${status}`, {
      agent_type: agentType,
      workflow_id: workflowId,
      operation,
      status,
      duration,
      context: this.sanitizeSensitiveData(context),
      performance: true,
      timing: {
        timestamp: Date.now(),
        iso_timestamp: new Date().toISOString()
      }
    }, `agent-${agentType}`);
  }

  // API interaction logging
  logAPICall(service, endpoint, method, status, duration, requestSize = null, responseSize = null) {
    this.info(`API call to ${service}`, {
      service,
      endpoint,
      method,
      status,
      duration,
      request_size: requestSize,
      response_size: responseSize,
      performance: true,
      timing: {
        timestamp: Date.now(),
        iso_timestamp: new Date().toISOString()
      }
    }, `api-${service}`);
  }

  logAPIError(service, endpoint, error, context = {}) {
    this.error(`API error for ${service}`, {
      service,
      endpoint,
      error_message: error.message,
      error_code: error.code || error.status,
      error_type: error.constructor.name,
      context: this.sanitizeSensitiveData(context),
      timing: {
        error_time: Date.now(),
        iso_error: new Date().toISOString()
      }
    }, `api-${service}`);
  }

  // Performance logging
  logPerformanceMetric(metricName, value, unit = 'ms', context = {}) {
    this.info(`Performance metric: ${metricName}`, {
      metric_name: metricName,
      value,
      unit,
      context: this.sanitizeSensitiveData(context),
      performance: true,
      timing: {
        timestamp: Date.now(),
        iso_timestamp: new Date().toISOString()
      }
    }, 'performance');
  }

  // Context optimization logging
  logContextOptimization(originalSize, optimizedSize, compressionRatio, workflowId) {
    this.info('Context optimization completed', {
      workflow_id: workflowId,
      original_size: originalSize,
      optimized_size: optimizedSize,
      compression_ratio: compressionRatio,
      bytes_saved: originalSize - optimizedSize,
      savings_percentage: Math.round((1 - optimizedSize / originalSize) * 100),
      performance: true,
      timing: {
        timestamp: Date.now(),
        iso_timestamp: new Date().toISOString()
      }
    }, 'context-manager');
  }

  // User interaction logging
  logUserCommand(command, user, repository, prNumber, success = true, context = {}) {
    this.info(`User command: ${command}`, {
      command,
      user,
      repository,
      pr_number: prNumber,
      success,
      context: this.sanitizeSensitiveData(context),
      timing: {
        timestamp: Date.now(),
        iso_timestamp: new Date().toISOString()
      }
    }, 'user-interaction');
  }

  // Security logging
  logSecurityEvent(eventType, severity, details, context = {}) {
    this.warn(`Security event: ${eventType}`, {
      event_type: eventType,
      severity,
      details,
      context: this.sanitizeSensitiveData(context),
      security: true,
      timing: {
        timestamp: Date.now(),
        iso_timestamp: new Date().toISOString()
      }
    }, 'security');
  }

  // Data sanitization
  sanitizeSensitiveData(data) {
    if (!data || typeof data !== 'object') return data;

    const sanitized = Array.isArray(data) ? [...data] : { ...data };

    for (const [key, value] of Object.entries(sanitized)) {
      if (this.isSensitiveField(key)) {
        sanitized[key] = this.maskSensitiveValue(value);
      } else if (typeof value === 'object' && value !== null) {
        sanitized[key] = this.sanitizeSensitiveData(value);
      }
    }

    return sanitized;
  }

  isSensitiveField(fieldName) {
    const lowerField = fieldName.toLowerCase();
    return this.config.sensitiveFields.some(pattern => 
      lowerField.includes(pattern.toLowerCase())
    );
  }

  maskSensitiveValue(value) {
    if (typeof value !== 'string') return '[REDACTED]';
    
    if (value.length <= 4) return '***';
    
    const start = value.substring(0, 2);
    const end = value.substring(value.length - 2);
    const middle = '*'.repeat(Math.min(value.length - 4, 8));
    
    return `${start}${middle}${end}`;
  }

  // Result summarization for logging
  summarizeResult(result) {
    if (!result || typeof result !== 'object') return result;

    return {
      success: result.success,
      type: result.type || 'unknown',
      duration: result.duration,
      size: this.getObjectSize(result),
      key_fields: this.extractKeyFields(result)
    };
  }

  extractKeyFields(obj) {
    const keyFields = {};
    const importantKeys = ['success', 'error', 'count', 'length', 'status', 'score', 'confidence'];
    
    for (const key of importantKeys) {
      if (obj.hasOwnProperty(key)) {
        keyFields[key] = obj[key];
      }
    }
    
    return keyFields;
  }

  getObjectSize(obj) {
    try {
      return JSON.stringify(obj).length;
    } catch (error) {
      return 'unknown';
    }
  }

  // Log analytics and insights
  generateLogAnalytics(timeRange = '24h') {
    // This would analyze log patterns and generate insights
    // For now, return a basic structure
    return {
      timeRange,
      summary: 'Log analytics not fully implemented',
      recommendations: []
    };
  }

  // Cleanup old logs (handled by winston rotation, but can be extended)
  cleanupLogs() {
    this.info('Log cleanup completed', {
      cleanup: true,
      timing: {
        timestamp: Date.now(),
        iso_timestamp: new Date().toISOString()
      }
    }, 'system');
  }
}

module.exports = EnhancedLogger;