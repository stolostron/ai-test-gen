const winston = require('winston');
const FeatureUnderstandingAgent = require('../agents/feature-understanding-agent');
const CodebaseLearningAgent = require('../agents/codebase-learning-agent');
const CodeAnalysisAgent = require('../agents/code-analysis-agent');
const ContextManager = require('../utils/context-manager');
const MetricsCollector = require('../utils/metrics-collector');
const EnhancedLogger = require('../utils/enhanced-logger');

class AgentOrchestrator {
  constructor(config, octokit) {
    this.config = config;
    this.octokit = octokit;
    
    // Initialize enhanced logging and metrics
    this.enhancedLogger = new EnhancedLogger(config.logging || {});
    this.metricsCollector = new MetricsCollector(config.metrics || {});
    
    // Initialize context manager
    this.contextManager = new ContextManager(config);
    
    // Initialize agents
    this.featureAgent = new FeatureUnderstandingAgent(config);
    this.codebaseAgent = new CodebaseLearningAgent(config, octokit);
    this.analysisAgent = new CodeAnalysisAgent(config, octokit);
    
    // Setup basic logging (kept for backward compatibility)
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
      ),
      defaultMeta: { component: 'AgentOrchestrator' }
    });

    // Track workflow state
    this.workflowState = new Map();
    
    // Setup cleanup intervals
    setInterval(() => {
      this.metricsCollector.cleanupOldMetrics();
      this.enhancedLogger.cleanupLogs();
    }, 60 * 60 * 1000); // Run every hour
  }

  async orchestratePRReview(pr, options = {}) {
    const workflowId = this.generateWorkflowId(pr);
    
    // Enhanced logging and metrics for workflow start
    this.enhancedLogger.logWorkflowStart(workflowId, pr, options);
    const reviewTimerId = this.metricsCollector.recordPRReviewStart(pr, options);
    
    this.logger.info('Starting PR review orchestration', {
      workflow_id: workflowId,
      pr_number: pr.number,
      repository: pr.base.repo.full_name,
      options
    });

    try {
      // Initialize workflow state
      this.initializeWorkflowState(workflowId, pr);
      
      // Phase 1: Feature Understanding
      const featureResult = await this.executeFeatureUnderstanding(workflowId, pr);
      
      // Phase 2: Codebase Learning
      const codebaseResult = await this.executeCodebaseLearning(workflowId, pr, featureResult);
      
      // Phase 3: Code Analysis
      const analysisResult = await this.executeCodeAnalysis(workflowId, pr, featureResult, codebaseResult);
      
      // Phase 4: Generate Final Report
      const finalReport = await this.generateFinalReport(workflowId, {
        feature: featureResult,
        codebase: codebaseResult,
        analysis: analysisResult
      });

      const totalDuration = Date.now() - this.getWorkflowState(workflowId).startTime;
      
      // Enhanced logging and metrics for completion
      this.enhancedLogger.logWorkflowComplete(workflowId, totalDuration, finalReport);
      this.metricsCollector.recordPRReviewComplete(reviewTimerId, {
        success: true,
        report: finalReport,
        workflowId
      });
      
      this.logger.info('PR review orchestration completed', {
        workflow_id: workflowId,
        total_duration: totalDuration,
        health_score: finalReport.healthScore
      });

      return {
        success: true,
        workflowId,
        report: finalReport,
        phases: {
          featureUnderstanding: featureResult,
          codebaseLearning: codebaseResult,
          codeAnalysis: analysisResult
        }
      };
    } catch (error) {
      // Enhanced logging and metrics for errors
      this.enhancedLogger.logWorkflowError(workflowId, 'orchestration', error, {
        pr_number: pr.number,
        repository: pr.base.repo.full_name
      });
      this.metricsCollector.recordPRReviewError(reviewTimerId, error, {
        pr_number: pr.number,
        repository: pr.base.repo.full_name
      });
      
      this.logger.error('PR review orchestration failed', {
        workflow_id: workflowId,
        pr_number: pr.number,
        error: error.message,
        stack: error.stack
      });

      // Update workflow state with error
      this.updateWorkflowState(workflowId, {
        status: 'failed',
        error: error.message,
        endTime: Date.now()
      });

      throw error;
    }
  }

  async executeFeatureUnderstanding(workflowId, pr) {
    const phaseStart = Date.now();
    
    this.enhancedLogger.logWorkflowPhase(workflowId, 'feature_understanding', 'started');
    this.enhancedLogger.logAgentExecution('feature', workflowId, 'analyze_context', 'started');
    
    this.logger.info('Executing feature understanding phase', {
      workflow_id: workflowId,
      phase: 'feature_understanding'
    });

    try {
      this.updateWorkflowState(workflowId, {
        currentPhase: 'feature_understanding',
        phaseStartTime: phaseStart
      });

      const result = await this.featureAgent.analyzeFeatureContext(pr);
      
      const phaseDuration = Date.now() - phaseStart;
      
      // Enhanced logging and metrics
      this.enhancedLogger.logWorkflowPhase(workflowId, 'feature_understanding', 'completed', phaseDuration, result);
      this.enhancedLogger.logAgentExecution('feature', workflowId, 'analyze_context', 'completed', phaseDuration);
      this.metricsCollector.recordAgentExecution('feature', phaseDuration, true, {
        workflow_id: workflowId,
        complexity: result.analysis?.complexity
      });
      
      this.updateWorkflowState(workflowId, {
        phases: {
          ...this.getWorkflowState(workflowId).phases,
          featureUnderstanding: {
            status: 'completed',
            duration: phaseDuration,
            result
          }
        }
      });

      return result;
    } catch (error) {
      const phaseDuration = Date.now() - phaseStart;
      
      // Enhanced logging and metrics for errors
      this.enhancedLogger.logWorkflowPhase(workflowId, 'feature_understanding', 'failed', phaseDuration);
      this.enhancedLogger.logAgentExecution('feature', workflowId, 'analyze_context', 'failed', phaseDuration, { error: error.message });
      this.metricsCollector.recordAgentExecution('feature', phaseDuration, false, {
        workflow_id: workflowId,
        error: error.message
      });
      
      this.logger.error('Feature understanding phase failed', {
        workflow_id: workflowId,
        error: error.message
      });

      this.updateWorkflowState(workflowId, {
        phases: {
          ...this.getWorkflowState(workflowId).phases,
          featureUnderstanding: {
            status: 'failed',
            error: error.message,
            duration: phaseDuration
          }
        }
      });

      throw error;
    }
  }

  async executeCodebaseLearning(workflowId, pr, featureContext) {
    const phaseStart = Date.now();
    
    this.enhancedLogger.logWorkflowPhase(workflowId, 'codebase_learning', 'started');
    this.enhancedLogger.logAgentExecution('codebase', workflowId, 'learn_codebase', 'started');
    
    this.logger.info('Executing codebase learning phase', {
      workflow_id: workflowId,
      phase: 'codebase_learning'
    });

    try {
      this.updateWorkflowState(workflowId, {
        currentPhase: 'codebase_learning',
        phaseStartTime: phaseStart
      });

      const result = await this.codebaseAgent.learnRelevantCodebase(pr, featureContext);
      
      const phaseDuration = Date.now() - phaseStart;
      
      // Enhanced logging and metrics
      this.enhancedLogger.logWorkflowPhase(workflowId, 'codebase_learning', 'completed', phaseDuration, result);
      this.enhancedLogger.logAgentExecution('codebase', workflowId, 'learn_codebase', 'completed', phaseDuration);
      this.metricsCollector.recordAgentExecution('codebase', phaseDuration, true, {
        workflow_id: workflowId,
        functions_found: result.insights?.reusableFunctions?.length || 0,
        patterns_found: result.insights?.reusablePatterns?.length || 0
      });
      
      this.updateWorkflowState(workflowId, {
        phases: {
          ...this.getWorkflowState(workflowId).phases,
          codebaseLearning: {
            status: 'completed',
            duration: phaseDuration,
            result
          }
        }
      });

      return result;
    } catch (error) {
      const phaseDuration = Date.now() - phaseStart;
      
      // Enhanced logging and metrics for errors
      this.enhancedLogger.logWorkflowPhase(workflowId, 'codebase_learning', 'failed', phaseDuration);
      this.enhancedLogger.logAgentExecution('codebase', workflowId, 'learn_codebase', 'failed', phaseDuration, { error: error.message });
      this.metricsCollector.recordAgentExecution('codebase', phaseDuration, false, {
        workflow_id: workflowId,
        error: error.message,
        fallback_used: true
      });
      
      this.logger.error('Codebase learning phase failed', {
        workflow_id: workflowId,
        error: error.message
      });

      this.updateWorkflowState(workflowId, {
        phases: {
          ...this.getWorkflowState(workflowId).phases,
          codebaseLearning: {
            status: 'failed',
            error: error.message,
            duration: phaseDuration
          }
        }
      });

      // Continue with limited context if codebase learning fails
      return {
        success: false,
        error: error.message,
        fallback: true,
        knowledge: {
          existingFunctions: [],
          patterns: [],
          utilities: []
        },
        insights: {
          reusableFunctions: [],
          reusablePatterns: [],
          architecturalGuidance: {
            followPatterns: [],
            avoidPatterns: [],
            integrationPoints: []
          }
        }
      };
    }
  }

  async executeCodeAnalysis(workflowId, pr, featureContext, codebaseKnowledge) {
    const phaseStart = Date.now();
    
    this.enhancedLogger.logWorkflowPhase(workflowId, 'code_analysis', 'started');
    this.enhancedLogger.logAgentExecution('analysis', workflowId, 'analyze_implementation', 'started');
    
    this.logger.info('Executing code analysis phase', {
      workflow_id: workflowId,
      phase: 'code_analysis'
    });

    try {
      this.updateWorkflowState(workflowId, {
        currentPhase: 'code_analysis',
        phaseStartTime: phaseStart
      });

      // Optimize context for the analysis agent
      const fullContext = {
        feature: featureContext,
        codebase: codebaseKnowledge,
        pr: pr
      };

      const contextOptStart = Date.now();
      const optimizedContext = await this.contextManager.optimizeContext(
        fullContext, 
        'code-analysis'
      );
      
      // Log context optimization metrics
      const originalSize = JSON.stringify(fullContext).length;
      const optimizedSize = JSON.stringify(optimizedContext).length;
      const compressionRatio = optimizedSize / originalSize;
      
      this.enhancedLogger.logContextOptimization(
        originalSize, 
        optimizedSize, 
        compressionRatio, 
        workflowId
      );
      this.metricsCollector.recordContextOptimization(
        originalSize, 
        optimizedSize, 
        compressionRatio
      );

      const result = await this.analysisAgent.analyzeImplementation(
        pr, 
        featureContext, 
        codebaseKnowledge
      );

      const phaseDuration = Date.now() - phaseStart;
      
      // Enhanced logging and metrics
      this.enhancedLogger.logWorkflowPhase(workflowId, 'code_analysis', 'completed', phaseDuration, result);
      this.enhancedLogger.logAgentExecution('analysis', workflowId, 'analyze_implementation', 'completed', phaseDuration);
      this.metricsCollector.recordAgentExecution('analysis', phaseDuration, true, {
        workflow_id: workflowId,
        health_score: result.healthScore,
        suggestions_count: result.feedback?.suggestions?.length || 0
      });
      
      this.updateWorkflowState(workflowId, {
        phases: {
          ...this.getWorkflowState(workflowId).phases,
          codeAnalysis: {
            status: 'completed',
            duration: phaseDuration,
            result,
            contextOptimization: optimizedContext.metadata
          }
        }
      });

      return result;
    } catch (error) {
      const phaseDuration = Date.now() - phaseStart;
      
      // Enhanced logging and metrics for errors
      this.enhancedLogger.logWorkflowPhase(workflowId, 'code_analysis', 'failed', phaseDuration);
      this.enhancedLogger.logAgentExecution('analysis', workflowId, 'analyze_implementation', 'failed', phaseDuration, { error: error.message });
      this.metricsCollector.recordAgentExecution('analysis', phaseDuration, false, {
        workflow_id: workflowId,
        error: error.message
      });
      
      this.logger.error('Code analysis phase failed', {
        workflow_id: workflowId,
        error: error.message
      });

      this.updateWorkflowState(workflowId, {
        phases: {
          ...this.getWorkflowState(workflowId).phases,
          codeAnalysis: {
            status: 'failed',
            error: error.message,
            duration: phaseDuration
          }
        }
      });

      throw error;
    }
  }

  async generateFinalReport(workflowId, phaseResults) {
    this.logger.info('Generating final report', {
      workflow_id: workflowId,
      phase: 'final_report'
    });

    try {
      const report = {
        workflowId,
        timestamp: new Date().toISOString(),
        repository: this.getWorkflowState(workflowId).repository,
        prNumber: this.getWorkflowState(workflowId).prNumber,
        
        // Executive summary
        summary: this.generateExecutiveSummary(phaseResults),
        
        // Overall health score
        healthScore: this.calculateOverallHealthScore(phaseResults),
        
        // Detailed findings
        findings: this.consolidateFindings(phaseResults),
        
        // Recommendations
        recommendations: this.generateRecommendations(phaseResults),
        
        // Workflow metadata
        workflow: {
          totalDuration: Date.now() - this.getWorkflowState(workflowId).startTime,
          phases: this.getWorkflowState(workflowId).phases,
          agentPerformance: this.calculateAgentPerformance(workflowId)
        }
      };

      this.updateWorkflowState(workflowId, {
        status: 'completed',
        endTime: Date.now(),
        finalReport: report
      });

      return report;
    } catch (error) {
      this.logger.error('Final report generation failed', {
        workflow_id: workflowId,
        error: error.message
      });

      // Return a basic report even if generation fails
      return this.generateBasicReport(workflowId, phaseResults, error);
    }
  }

  generateExecutiveSummary(phaseResults) {
    const { feature, codebase, analysis } = phaseResults;

    return {
      purpose: feature.analysis?.businessPurpose || 'Purpose not determined',
      complexity: feature.analysis?.complexity || 'unknown',
      riskLevel: analysis.feedback?.summary?.riskLevel || 'unknown',
      codebaseUtilization: this.assessCodebaseUtilization(codebase),
      keyFindings: analysis.feedback?.summary?.keyFindings || [],
      overallAssessment: this.generateOverallAssessment(phaseResults)
    };
  }

  assessCodebaseUtilization(codebaseResult) {
    if (!codebaseResult.success) return 'limited';
    
    const insights = codebaseResult.insights || {};
    const reusableFunctionsCount = insights.reusableFunctions?.length || 0;
    const patternsCount = insights.reusablePatterns?.length || 0;
    
    if (reusableFunctionsCount + patternsCount >= 5) return 'high';
    if (reusableFunctionsCount + patternsCount >= 2) return 'medium';
    return 'low';
  }

  generateOverallAssessment(phaseResults) {
    const { feature, codebase, analysis } = phaseResults;
    
    let assessment = 'The pull request ';
    
    // Add feature assessment
    if (feature.success) {
      assessment += `implements ${feature.analysis?.businessPurpose || 'a feature'} `;
    }
    
    // Add codebase integration assessment
    if (codebase.success) {
      const reusableCount = codebase.insights?.reusableFunctions?.length || 0;
      if (reusableCount > 0) {
        assessment += `and identifies ${reusableCount} existing functions that could be leveraged. `;
      } else {
        assessment += 'with minimal reuse of existing codebase. ';
      }
    }
    
    // Add quality assessment
    if (analysis.success) {
      const healthScore = analysis.healthScore || 0;
      if (healthScore >= 80) {
        assessment += 'Code quality is high with minimal issues.';
      } else if (healthScore >= 60) {
        assessment += 'Code quality is acceptable with some improvements needed.';
      } else {
        assessment += 'Code quality needs significant improvements.';
      }
    }
    
    return assessment;
  }

  calculateOverallHealthScore(phaseResults) {
    const { feature, codebase, analysis } = phaseResults;
    
    let score = 100;
    let weights = { feature: 0.2, codebase: 0.3, analysis: 0.5 };
    
    // Feature understanding score
    if (!feature.success) {
      score -= weights.feature * 100;
    } else {
      const complexity = feature.analysis?.complexity || 'medium';
      if (complexity === 'high') score -= weights.feature * 20;
      if (complexity === 'medium') score -= weights.feature * 10;
    }
    
    // Codebase utilization score
    if (!codebase.success) {
      score -= weights.codebase * 30; // Partial penalty for codebase failure
    } else {
      const utilization = this.assessCodebaseUtilization(codebase);
      if (utilization === 'low') score -= weights.codebase * 30;
      if (utilization === 'medium') score -= weights.codebase * 15;
    }
    
    // Code analysis score
    if (!analysis.success) {
      score -= weights.analysis * 100;
    } else {
      score = score - (weights.analysis * (100 - (analysis.healthScore || 0)));
    }
    
    return Math.max(0, Math.min(100, Math.round(score)));
  }

  consolidateFindings(phaseResults) {
    const findings = {
      critical: [],
      warnings: [],
      suggestions: [],
      positive: []
    };

    // Consolidate from analysis phase
    if (phaseResults.analysis.success && phaseResults.analysis.feedback?.suggestions) {
      phaseResults.analysis.feedback.suggestions.forEach(suggestion => {
        switch (suggestion.severity) {
          case 'critical':
            findings.critical.push(suggestion);
            break;
          case 'warning':
            findings.warnings.push(suggestion);
            break;
          case 'suggestion':
          case 'info':
            findings.suggestions.push(suggestion);
            break;
        }
      });
    }

    // Add positive findings
    if (phaseResults.analysis.success && phaseResults.analysis.feedback?.positiveFindings) {
      findings.positive = phaseResults.analysis.feedback.positiveFindings;
    }

    // Add codebase learning insights as suggestions
    if (phaseResults.codebase.success && phaseResults.codebase.insights?.reusableFunctions) {
      phaseResults.codebase.insights.reusableFunctions.forEach(func => {
        findings.suggestions.push({
          type: 'reuse_existing',
          severity: 'suggestion',
          title: `Consider using existing function: ${func.name}`,
          message: func.reason,
          relatedFunction: func.name,
          filepath: func.filepath
        });
      });
    }

    return findings;
  }

  generateRecommendations(phaseResults) {
    const recommendations = {
      immediate: [],
      shortTerm: [],
      longTerm: []
    };

    // Generate based on critical and warning findings
    if (phaseResults.analysis.success) {
      const feedback = phaseResults.analysis.feedback || {};
      
      // Immediate actions for critical issues
      if (feedback.suggestions) {
        feedback.suggestions
          .filter(s => s.severity === 'critical')
          .forEach(s => {
            recommendations.immediate.push({
              action: s.title,
              reason: s.message,
              file: s.file
            });
          });
        
        // Short-term actions for warnings
        feedback.suggestions
          .filter(s => s.severity === 'warning')
          .forEach(s => {
            recommendations.shortTerm.push({
              action: s.title,
              reason: s.message,
              file: s.file
            });
          });
      }
      
      // Testing recommendations
      if (feedback.testingRecommendations) {
        recommendations.shortTerm.push(...feedback.testingRecommendations.map(rec => ({
          action: 'Add tests',
          reason: rec,
          category: 'testing'
        })));
      }
    }

    // Architectural recommendations from codebase learning
    if (phaseResults.codebase.success && phaseResults.codebase.insights?.architecturalGuidance) {
      const guidance = phaseResults.codebase.insights.architecturalGuidance;
      
      guidance.followPatterns?.forEach(pattern => {
        recommendations.longTerm.push({
          action: `Adopt ${pattern} pattern`,
          reason: 'Align with existing codebase patterns',
          category: 'architecture'
        });
      });
    }

    return recommendations;
  }

  calculateAgentPerformance(workflowId) {
    const state = this.getWorkflowState(workflowId);
    const performance = {};

    Object.entries(state.phases || {}).forEach(([phase, data]) => {
      performance[phase] = {
        status: data.status,
        duration: data.duration,
        success: data.status === 'completed',
        efficiency: data.duration ? this.calculateEfficiency(phase, data.duration) : 'unknown'
      };
    });

    return performance;
  }

  calculateEfficiency(phase, duration) {
    // Expected durations in milliseconds
    const expectedDurations = {
      featureUnderstanding: 15000, // 15 seconds
      codebaseLearning: 30000,     // 30 seconds
      codeAnalysis: 45000          // 45 seconds
    };

    const expected = expectedDurations[phase] || 30000;
    const ratio = duration / expected;

    if (ratio <= 0.7) return 'excellent';
    if (ratio <= 1.0) return 'good';
    if (ratio <= 1.5) return 'acceptable';
    return 'slow';
  }

  generateBasicReport(workflowId, phaseResults, error) {
    return {
      workflowId,
      timestamp: new Date().toISOString(),
      status: 'partial',
      error: error.message,
      summary: {
        purpose: 'Report generation failed',
        overallAssessment: 'Unable to complete full analysis'
      },
      healthScore: 50, // Default moderate score
      findings: {
        critical: [{ message: 'Report generation failed', error: error.message }],
        warnings: [],
        suggestions: [],
        positive: []
      },
      recommendations: {
        immediate: [{ action: 'Review system logs', reason: 'Analysis partially failed' }],
        shortTerm: [],
        longTerm: []
      }
    };
  }

  // Workflow state management
  generateWorkflowId(pr) {
    return `pr-${pr.number}-${Date.now()}`;
  }

  initializeWorkflowState(workflowId, pr) {
    this.workflowState.set(workflowId, {
      id: workflowId,
      repository: pr.base.repo.full_name,
      prNumber: pr.number,
      status: 'running',
      startTime: Date.now(),
      currentPhase: 'initializing',
      phases: {}
    });
  }

  getWorkflowState(workflowId) {
    return this.workflowState.get(workflowId) || {};
  }

  updateWorkflowState(workflowId, updates) {
    const current = this.getWorkflowState(workflowId);
    this.workflowState.set(workflowId, { ...current, ...updates });
  }

  // Utility methods
  async getWorkflowStatus(workflowId) {
    const state = this.getWorkflowState(workflowId);
    if (!state.id) {
      return { exists: false };
    }

    return {
      exists: true,
      status: state.status,
      currentPhase: state.currentPhase,
      duration: Date.now() - state.startTime,
      phases: state.phases
    };
  }

  async cancelWorkflow(workflowId, reason = 'User cancelled') {
    const state = this.getWorkflowState(workflowId);
    if (state.id && state.status === 'running') {
      this.updateWorkflowState(workflowId, {
        status: 'cancelled',
        cancelReason: reason,
        endTime: Date.now()
      });
      
      this.logger.info('Workflow cancelled', {
        workflow_id: workflowId,
        reason
      });
      
      return true;
    }
    
    return false;
  }

  // Analytics and metrics access
  getAnalytics(timeRange = '24h') {
    return this.metricsCollector.getPerformanceAnalytics(timeRange);
  }

  getSystemMetrics() {
    return {
      workflows: {
        active: Array.from(this.workflowState.values()).filter(w => w.status === 'running').length,
        total: this.workflowState.size
      },
      performance: this.metricsCollector.getPerformanceAnalytics('1h'),
      system: {
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        timestamp: new Date().toISOString()
      }
    };
  }

  exportMetrics(format = 'json') {
    return this.metricsCollector.exportMetrics(format);
  }

  // Cleanup old workflow states
  cleanupOldWorkflows(maxAge = 24 * 60 * 60 * 1000) { // 24 hours
    const now = Date.now();
    const toDelete = [];

    this.workflowState.forEach((state, workflowId) => {
      const age = now - state.startTime;
      if (age > maxAge) {
        toDelete.push(workflowId);
      }
    });

    toDelete.forEach(workflowId => {
      this.workflowState.delete(workflowId);
    });

    if (toDelete.length > 0) {
      this.logger.info('Cleaned up old workflows', {
        count: toDelete.length
      });
      this.enhancedLogger.info('Workflow cleanup completed', {
        cleaned_workflows: toDelete.length,
        remaining_workflows: this.workflowState.size
      }, 'system');
    }
  }
}

module.exports = AgentOrchestrator;