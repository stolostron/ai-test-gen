const winston = require('winston');

class MetricsCollector {
  constructor(config = {}) {
    this.config = config;
    this.metrics = new Map();
    this.counters = new Map();
    this.timers = new Map();
    
    // Setup metrics logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
      ),
      defaultMeta: { component: 'MetricsCollector' },
      transports: [
        new winston.transports.File({ 
          filename: 'metrics.log',
          format: winston.format.json()
        })
      ]
    });

    // Initialize default counters
    this.initializeCounters();
  }

  initializeCounters() {
    // PR Review metrics
    this.counters.set('pr_reviews_total', 0);
    this.counters.set('pr_reviews_success', 0);
    this.counters.set('pr_reviews_failed', 0);
    
    // Agent performance metrics
    this.counters.set('feature_agent_executions', 0);
    this.counters.set('codebase_agent_executions', 0);
    this.counters.set('analysis_agent_executions', 0);
    
    // Error metrics
    this.counters.set('github_api_errors', 0);
    this.counters.set('claude_api_errors', 0);
    this.counters.set('jira_api_errors', 0);
    
    // User interaction metrics
    this.counters.set('manual_commands_total', 0);
    this.counters.set('webhook_events_total', 0);
  }

  // Counter operations
  incrementCounter(name, value = 1, labels = {}) {
    const current = this.counters.get(name) || 0;
    this.counters.set(name, current + value);
    
    this.recordMetric('counter', {
      name,
      value: current + value,
      delta: value,
      labels,
      timestamp: Date.now()
    });
  }

  getCounter(name) {
    return this.counters.get(name) || 0;
  }

  // Timer operations
  startTimer(name, labels = {}) {
    const timerId = `${name}_${Date.now()}_${Math.random()}`;
    this.timers.set(timerId, {
      name,
      startTime: Date.now(),
      labels
    });
    return timerId;
  }

  endTimer(timerId) {
    const timer = this.timers.get(timerId);
    if (!timer) {
      this.logger.warn('Timer not found', { timer_id: timerId });
      return null;
    }

    const duration = Date.now() - timer.startTime;
    this.timers.delete(timerId);

    this.recordMetric('timer', {
      name: timer.name,
      duration,
      labels: timer.labels,
      timestamp: Date.now()
    });

    return duration;
  }

  // Gauge operations (current value metrics)
  setGauge(name, value, labels = {}) {
    this.recordMetric('gauge', {
      name,
      value,
      labels,
      timestamp: Date.now()
    });
  }

  // Histogram operations (distribution metrics)
  recordHistogram(name, value, labels = {}) {
    this.recordMetric('histogram', {
      name,
      value,
      labels,
      timestamp: Date.now()
    });
  }

  // Generic metric recording
  recordMetric(type, data) {
    const metricId = `${data.name}_${Date.now()}`;
    const metric = {
      id: metricId,
      type,
      ...data
    };

    this.metrics.set(metricId, metric);
    this.logger.info('Metric recorded', metric);

    // Optional: Send to external monitoring system
    if (this.config.externalMonitoring?.enabled) {
      this.sendToExternalSystem(metric);
    }
  }

  // PR Review specific metrics
  recordPRReviewStart(pr, options = {}) {
    const timerId = this.startTimer('pr_review_duration', {
      repository: pr.base.repo.full_name,
      pr_number: pr.number,
      event_type: options.eventType || 'unknown'
    });

    this.incrementCounter('pr_reviews_total');
    this.incrementCounter('webhook_events_total');

    this.recordMetric('event', {
      name: 'pr_review_started',
      pr_number: pr.number,
      repository: pr.base.repo.full_name,
      author: pr.user.login,
      draft: pr.draft,
      labels: pr.labels?.map(l => l.name) || [],
      files_changed: pr.changed_files,
      additions: pr.additions,
      deletions: pr.deletions,
      event_type: options.eventType,
      timestamp: Date.now()
    });

    return timerId;
  }

  recordPRReviewComplete(timerId, result) {
    const duration = this.endTimer(timerId);
    
    if (result.success) {
      this.incrementCounter('pr_reviews_success');
    } else {
      this.incrementCounter('pr_reviews_failed');
    }

    this.recordMetric('event', {
      name: 'pr_review_completed',
      success: result.success,
      duration,
      health_score: result.report?.healthScore,
      workflow_id: result.workflowId,
      findings_count: {
        critical: result.report?.findings?.critical?.length || 0,
        warnings: result.report?.findings?.warnings?.length || 0,
        suggestions: result.report?.findings?.suggestions?.length || 0
      },
      timestamp: Date.now()
    });
  }

  recordPRReviewError(timerId, error, context = {}) {
    this.endTimer(timerId);
    this.incrementCounter('pr_reviews_failed');

    this.recordMetric('error', {
      name: 'pr_review_error',
      error_message: error.message,
      error_type: error.constructor.name,
      stack_trace: error.stack,
      context,
      timestamp: Date.now()
    });
  }

  // Agent performance metrics
  recordAgentExecution(agentType, duration, success, context = {}) {
    this.incrementCounter(`${agentType}_agent_executions`);
    
    this.recordHistogram(`${agentType}_agent_duration`, duration, {
      success: success.toString(),
      ...context
    });

    this.recordMetric('agent_execution', {
      name: `${agentType}_agent_execution`,
      agent_type: agentType,
      duration,
      success,
      context,
      timestamp: Date.now()
    });
  }

  // API error tracking
  recordAPIError(apiType, error, endpoint = null) {
    this.incrementCounter(`${apiType}_api_errors`);

    this.recordMetric('api_error', {
      name: `${apiType}_api_error`,
      api_type: apiType,
      endpoint,
      error_message: error.message,
      error_code: error.code || error.status,
      timestamp: Date.now()
    });
  }

  // User interaction metrics
  recordManualCommand(command, user, repository, success = true) {
    this.incrementCounter('manual_commands_total');

    this.recordMetric('user_interaction', {
      name: 'manual_command',
      command,
      user,
      repository,
      success,
      timestamp: Date.now()
    });
  }

  // Context optimization metrics
  recordContextOptimization(originalSize, optimizedSize, compressionRatio) {
    this.recordMetric('context_optimization', {
      name: 'context_optimization',
      original_size: originalSize,
      optimized_size: optimizedSize,
      compression_ratio: compressionRatio,
      savings_bytes: originalSize - optimizedSize,
      timestamp: Date.now()
    });
  }

  // Performance analytics
  getPerformanceAnalytics(timeRange = '24h') {
    const now = Date.now();
    const ranges = {
      '1h': 60 * 60 * 1000,
      '24h': 24 * 60 * 60 * 1000,
      '7d': 7 * 24 * 60 * 60 * 1000
    };
    
    const rangeMs = ranges[timeRange] || ranges['24h'];
    const startTime = now - rangeMs;

    const recentMetrics = Array.from(this.metrics.values())
      .filter(metric => metric.timestamp >= startTime);

    return {
      timeRange,
      totalMetrics: recentMetrics.length,
      counters: Object.fromEntries(this.counters),
      
      // PR Review analytics
      prReviews: {
        total: this.getMetricCount(recentMetrics, 'pr_review_started'),
        completed: this.getMetricCount(recentMetrics, 'pr_review_completed'),
        failed: this.getMetricCount(recentMetrics, 'pr_review_error'),
        averageDuration: this.getAverageDuration(recentMetrics, 'pr_review_duration'),
        averageHealthScore: this.getAverageValue(recentMetrics, 'health_score')
      },
      
      // Agent performance
      agentPerformance: {
        feature: this.getAgentStats(recentMetrics, 'feature'),
        codebase: this.getAgentStats(recentMetrics, 'codebase'),
        analysis: this.getAgentStats(recentMetrics, 'analysis')
      },
      
      // Error rates
      errorRates: {
        github: this.getMetricCount(recentMetrics, 'github_api_error'),
        claude: this.getMetricCount(recentMetrics, 'claude_api_error'),
        jira: this.getMetricCount(recentMetrics, 'jira_api_error')
      },
      
      // Context optimization
      contextOptimization: {
        optimizations: this.getMetricCount(recentMetrics, 'context_optimization'),
        averageCompressionRatio: this.getAverageValue(recentMetrics, 'compression_ratio'),
        totalBytesSaved: this.getTotalValue(recentMetrics, 'savings_bytes')
      }
    };
  }

  // Helper methods for analytics
  getMetricCount(metrics, metricName) {
    return metrics.filter(m => m.name === metricName).length;
  }

  getAverageDuration(metrics, metricName) {
    const durations = metrics
      .filter(m => m.name === metricName && m.duration)
      .map(m => m.duration);
    
    return durations.length > 0 
      ? Math.round(durations.reduce((a, b) => a + b, 0) / durations.length)
      : 0;
  }

  getAverageValue(metrics, field) {
    const values = metrics
      .filter(m => m[field] !== undefined)
      .map(m => m[field]);
    
    return values.length > 0 
      ? Math.round(values.reduce((a, b) => a + b, 0) / values.length * 100) / 100
      : 0;
  }

  getTotalValue(metrics, field) {
    return metrics
      .filter(m => m[field] !== undefined)
      .reduce((total, m) => total + m[field], 0);
  }

  getAgentStats(metrics, agentType) {
    const agentMetrics = metrics.filter(m => 
      m.name === `${agentType}_agent_execution`
    );

    const successCount = agentMetrics.filter(m => m.success).length;
    const totalCount = agentMetrics.length;
    const durations = agentMetrics.map(m => m.duration).filter(Boolean);

    return {
      executions: totalCount,
      successRate: totalCount > 0 ? Math.round((successCount / totalCount) * 100) : 0,
      averageDuration: durations.length > 0 
        ? Math.round(durations.reduce((a, b) => a + b, 0) / durations.length)
        : 0
    };
  }

  // Export metrics for external systems
  exportMetrics(format = 'json') {
    const analytics = this.getPerformanceAnalytics('24h');
    
    switch (format) {
      case 'prometheus':
        return this.toPrometheusFormat(analytics);
      case 'json':
      default:
        return JSON.stringify(analytics, null, 2);
    }
  }

  toPrometheusFormat(analytics) {
    let output = '';
    
    // Counter metrics
    Object.entries(analytics.counters).forEach(([name, value]) => {
      output += `ai_code_review_${name} ${value}\n`;
    });
    
    // Performance metrics
    output += `ai_code_review_average_duration_seconds ${analytics.prReviews.averageDuration / 1000}\n`;
    output += `ai_code_review_average_health_score ${analytics.prReviews.averageHealthScore}\n`;
    
    return output;
  }

  // External monitoring integration
  async sendToExternalSystem(metric) {
    if (!this.config.externalMonitoring?.enabled) return;
    
    try {
      // Example: Send to monitoring service
      // await this.sendToDatadog(metric);
      // await this.sendToPrometheus(metric);
      
      this.logger.debug('Metric sent to external system', { metric_id: metric.id });
    } catch (error) {
      this.logger.error('Failed to send metric to external system', {
        metric_id: metric.id,
        error: error.message
      });
    }
  }

  // Cleanup old metrics
  cleanupOldMetrics(maxAge = 7 * 24 * 60 * 60 * 1000) { // 7 days
    const now = Date.now();
    const toDelete = [];

    this.metrics.forEach((metric, id) => {
      if (now - metric.timestamp > maxAge) {
        toDelete.push(id);
      }
    });

    toDelete.forEach(id => this.metrics.delete(id));

    if (toDelete.length > 0) {
      this.logger.info('Cleaned up old metrics', { count: toDelete.length });
    }
  }
}

module.exports = MetricsCollector;