const winston = require('winston');

class ContextManager {
  constructor(config) {
    this.config = config;
    this.maxTokens = config.maxContextTokens || 150000; // Claude Sonnet 4 context window
    this.reserveTokens = config.reserveTokens || 20000; // Reserve for response
    this.availableTokens = this.maxTokens - this.reserveTokens;
    
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
      ),
      defaultMeta: { component: 'ContextManager' }
    });
  }

  async optimizeContext(fullContext, agentType = 'general') {
    this.logger.info('Starting context optimization', {
      agent_type: agentType,
      full_context_size: this.estimateTokens(JSON.stringify(fullContext))
    });

    try {
      // Get prioritization strategy for agent type
      const strategy = this.getPrioritizationStrategy(agentType);
      
      // Prioritize context elements
      const prioritized = this.prioritizeContext(fullContext, strategy);
      
      // Compress context to fit within token limits
      const optimized = await this.compressContext(prioritized, strategy);
      
      // Validate optimized context
      const finalContext = this.validateContext(optimized);
      
      this.logger.info('Context optimization completed', {
        agent_type: agentType,
        original_tokens: this.estimateTokens(JSON.stringify(fullContext)),
        optimized_tokens: this.estimateTokens(JSON.stringify(finalContext)),
        compression_ratio: this.calculateCompressionRatio(fullContext, finalContext)
      });

      return finalContext;
    } catch (error) {
      this.logger.error('Context optimization failed', {
        agent_type: agentType,
        error: error.message,
        stack: error.stack
      });
      
      // Return a minimal context on failure
      return this.createMinimalContext(fullContext);
    }
  }

  getPrioritizationStrategy(agentType) {
    const strategies = {
      'feature-understanding': {
        critical: ['featureContext', 'jiraContext', 'prDetails'],
        important: ['commitHistory', 'fileChanges'],
        optional: ['codebaseKnowledge', 'existingPatterns'],
        weights: {
          featureContext: 1.0,
          jiraContext: 0.9,
          prDetails: 0.8,
          commitHistory: 0.6,
          fileChanges: 0.7,
          codebaseKnowledge: 0.4,
          existingPatterns: 0.3
        }
      },
      
      'codebase-learning': {
        critical: ['changedFiles', 'relevantFiles', 'codebaseStructure'],
        important: ['existingFunctions', 'patterns', 'architecture'],
        optional: ['fullRepository', 'historicalData'],
        weights: {
          changedFiles: 1.0,
          relevantFiles: 0.9,
          codebaseStructure: 0.8,
          existingFunctions: 0.7,
          patterns: 0.6,
          architecture: 0.5,
          fullRepository: 0.2,
          historicalData: 0.1
        }
      },
      
      'code-analysis': {
        critical: ['codeChanges', 'featureContext', 'codebaseKnowledge'],
        important: ['existingFunctions', 'patterns', 'staticAnalysis'],
        optional: ['fullContext', 'historicalPatterns'],
        weights: {
          codeChanges: 1.0,
          featureContext: 0.9,
          codebaseKnowledge: 0.8,
          existingFunctions: 0.7,
          patterns: 0.6,
          staticAnalysis: 0.5,
          fullContext: 0.3,
          historicalPatterns: 0.2
        }
      },
      
      'conflict-resolution': {
        critical: ['conflictDetails', 'baseChanges', 'headChanges'],
        important: ['recentHistory', 'authorIntent', 'relatedPRs'],
        optional: ['fullRepository', 'distantHistory'],
        weights: {
          conflictDetails: 1.0,
          baseChanges: 0.9,
          headChanges: 0.9,
          recentHistory: 0.7,
          authorIntent: 0.6,
          relatedPRs: 0.5,
          fullRepository: 0.2,
          distantHistory: 0.1
        }
      }
    };

    return strategies[agentType] || strategies['general'] || {
      critical: ['essential'],
      important: ['relevant'],
      optional: ['additional'],
      weights: {}
    };
  }

  prioritizeContext(fullContext, strategy) {
    const prioritized = {
      critical: {},
      important: {},
      optional: {},
      metadata: {
        originalSize: this.estimateTokens(JSON.stringify(fullContext)),
        prioritizationStrategy: strategy,
        timestamp: new Date().toISOString()
      }
    };

    // Categorize context elements by priority
    Object.keys(fullContext).forEach(key => {
      const value = fullContext[key];
      
      if (strategy.critical.includes(key)) {
        prioritized.critical[key] = value;
      } else if (strategy.important.includes(key)) {
        prioritized.important[key] = value;
      } else {
        prioritized.optional[key] = value;
      }
    });

    return prioritized;
  }

  async compressContext(prioritized, strategy) {
    let currentTokens = 0;
    const compressed = {
      critical: {},
      important: {},
      optional: {},
      compressionLog: []
    };

    // Always include critical context
    for (const [key, value] of Object.entries(prioritized.critical)) {
      const tokens = this.estimateTokens(JSON.stringify(value));
      
      if (currentTokens + tokens <= this.availableTokens) {
        compressed.critical[key] = value;
        currentTokens += tokens;
        compressed.compressionLog.push({
          key,
          action: 'included',
          tokens,
          priority: 'critical'
        });
      } else {
        // Compress critical data
        const compressedValue = await this.compressData(value, key, 'critical');
        const compressedTokens = this.estimateTokens(JSON.stringify(compressedValue));
        
        if (currentTokens + compressedTokens <= this.availableTokens) {
          compressed.critical[key] = compressedValue;
          currentTokens += compressedTokens;
          compressed.compressionLog.push({
            key,
            action: 'compressed',
            originalTokens: tokens,
            compressedTokens,
            priority: 'critical'
          });
        } else {
          compressed.compressionLog.push({
            key,
            action: 'skipped',
            tokens,
            priority: 'critical',
            reason: 'insufficient_space'
          });
        }
      }
    }

    // Include important context if space allows
    const importantEntries = Object.entries(prioritized.important)
      .sort(([a], [b]) => (strategy.weights[b] || 0) - (strategy.weights[a] || 0));

    for (const [key, value] of importantEntries) {
      const tokens = this.estimateTokens(JSON.stringify(value));
      
      if (currentTokens + tokens <= this.availableTokens) {
        compressed.important[key] = value;
        currentTokens += tokens;
        compressed.compressionLog.push({
          key,
          action: 'included',
          tokens,
          priority: 'important'
        });
      } else {
        // Try to compress important data
        const compressedValue = await this.compressData(value, key, 'important');
        const compressedTokens = this.estimateTokens(JSON.stringify(compressedValue));
        
        if (currentTokens + compressedTokens <= this.availableTokens) {
          compressed.important[key] = compressedValue;
          currentTokens += compressedTokens;
          compressed.compressionLog.push({
            key,
            action: 'compressed',
            originalTokens: tokens,
            compressedTokens,
            priority: 'important'
          });
        } else {
          compressed.compressionLog.push({
            key,
            action: 'skipped',
            tokens,
            priority: 'important',
            reason: 'insufficient_space'
          });
        }
      }
    }

    // Include optional context if space allows
    const optionalEntries = Object.entries(prioritized.optional)
      .sort(([a], [b]) => (strategy.weights[b] || 0) - (strategy.weights[a] || 0));

    for (const [key, value] of optionalEntries) {
      const tokens = this.estimateTokens(JSON.stringify(value));
      
      if (currentTokens + tokens <= this.availableTokens) {
        compressed.optional[key] = value;
        currentTokens += tokens;
        compressed.compressionLog.push({
          key,
          action: 'included',
          tokens,
          priority: 'optional'
        });
      } else {
        compressed.compressionLog.push({
          key,
          action: 'skipped',
          tokens,
          priority: 'optional',
          reason: 'insufficient_space'
        });
      }
    }

    compressed.metadata = {
      totalTokens: currentTokens,
      availableTokens: this.availableTokens,
      utilizationRatio: currentTokens / this.availableTokens
    };

    return compressed;
  }

  async compressData(data, key, priority) {
    try {
      switch (key) {
        case 'codeChanges':
          return this.compressCodeChanges(data);
        
        case 'existingFunctions':
          return this.compressFunctions(data);
        
        case 'patterns':
          return this.compressPatterns(data);
        
        case 'fileChanges':
          return this.compressFileChanges(data);
        
        case 'historicalData':
          return this.compressHistoricalData(data);
        
        default:
          return this.genericCompress(data, priority);
      }
    } catch (error) {
      this.logger.warn('Data compression failed', {
        key,
        priority,
        error: error.message
      });
      
      return this.genericCompress(data, priority);
    }
  }

  compressCodeChanges(changes) {
    if (!Array.isArray(changes)) return changes;
    
    return changes.map(change => ({
      filename: change.filename,
      status: change.status,
      additions: change.additions,
      deletions: change.deletions,
      language: change.language,
      // Truncate patch if too long
      patch: change.patch ? change.patch.substring(0, 2000) + '...' : null,
      // Summarize content instead of including full content
      contentSummary: change.content ? {
        lines: change.content.split('\n').length,
        size: change.content.length,
        hasTests: /test|spec/i.test(change.content),
        hasComments: /\/\/|\/\*|\*/g.test(change.content)
      } : null
    }));
  }

  compressFunctions(functions) {
    if (!Array.isArray(functions)) return functions;
    
    // Keep only the most relevant functions
    return functions
      .sort((a, b) => (b.relevance || 0) - (a.relevance || 0))
      .slice(0, 20) // Limit to top 20
      .map(func => ({
        name: func.name,
        filepath: func.filepath,
        type: func.type,
        relevance: func.relevance,
        // Remove detailed code content
        summary: `${func.type} in ${func.filepath}`
      }));
  }

  compressPatterns(patterns) {
    if (!Array.isArray(patterns)) return patterns;
    
    return patterns
      .filter(pattern => pattern.confidence > 0.5) // Keep only high-confidence patterns
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, 10) // Limit to top 10
      .map(pattern => ({
        name: pattern.name,
        count: pattern.count,
        confidence: pattern.confidence
      }));
  }

  compressFileChanges(changes) {
    return {
      totalFiles: changes.length || 0,
      languages: [...new Set(changes.map(c => c.language))],
      directories: [...new Set(changes.map(c => c.directory))],
      totalAdditions: changes.reduce((sum, c) => sum + (c.additions || 0), 0),
      totalDeletions: changes.reduce((sum, c) => sum + (c.deletions || 0), 0),
      // Keep only filenames, not full content
      files: changes.map(c => ({
        filename: c.filename,
        status: c.status,
        language: c.language
      }))
    };
  }

  compressHistoricalData(data) {
    if (Array.isArray(data)) {
      return data.slice(0, 5); // Keep only recent 5 items
    }
    
    if (typeof data === 'object') {
      const compressed = {};
      Object.keys(data).slice(0, 10).forEach(key => {
        compressed[key] = typeof data[key] === 'string' 
          ? data[key].substring(0, 500)
          : data[key];
      });
      return compressed;
    }
    
    return data;
  }

  genericCompress(data, priority) {
    if (typeof data === 'string') {
      const maxLength = priority === 'critical' ? 2000 : 
                       priority === 'important' ? 1000 : 500;
      return data.length > maxLength ? data.substring(0, maxLength) + '...' : data;
    }
    
    if (Array.isArray(data)) {
      const maxItems = priority === 'critical' ? 20 : 
                       priority === 'important' ? 10 : 5;
      return data.slice(0, maxItems);
    }
    
    if (typeof data === 'object' && data !== null) {
      const maxKeys = priority === 'critical' ? 15 : 
                      priority === 'important' ? 10 : 5;
      const compressed = {};
      Object.keys(data).slice(0, maxKeys).forEach(key => {
        compressed[key] = this.genericCompress(data[key], priority);
      });
      return compressed;
    }
    
    return data;
  }

  validateContext(context) {
    const validated = {
      ...context,
      validation: {
        isValid: true,
        issues: [],
        tokens: this.estimateTokens(JSON.stringify(context))
      }
    };

    // Check if context is too large
    if (validated.validation.tokens > this.availableTokens) {
      validated.validation.isValid = false;
      validated.validation.issues.push({
        type: 'size_exceeded',
        message: `Context size (${validated.validation.tokens}) exceeds limit (${this.availableTokens})`
      });
    }

    // Check if critical context is present
    if (!context.critical || Object.keys(context.critical).length === 0) {
      validated.validation.issues.push({
        type: 'missing_critical',
        message: 'No critical context available'
      });
    }

    // Log validation results
    this.logger.info('Context validation completed', {
      is_valid: validated.validation.isValid,
      tokens: validated.validation.tokens,
      issues: validated.validation.issues.length
    });

    return validated;
  }

  createMinimalContext(fullContext) {
    this.logger.warn('Creating minimal context due to optimization failure');
    
    return {
      critical: {
        essential: 'Context optimization failed, using minimal context'
      },
      metadata: {
        isMinimal: true,
        originalSize: this.estimateTokens(JSON.stringify(fullContext)),
        fallbackReason: 'optimization_failure'
      }
    };
  }

  estimateTokens(text) {
    if (!text) return 0;
    
    // Rough estimation: 1 token ≈ 4 characters for English text
    // This is approximate, but good enough for planning
    return Math.ceil(text.length / 4);
  }

  calculateCompressionRatio(original, compressed) {
    const originalSize = this.estimateTokens(JSON.stringify(original));
    const compressedSize = this.estimateTokens(JSON.stringify(compressed));
    
    if (originalSize === 0) return 1;
    
    return compressedSize / originalSize;
  }

  // Utility methods for context building
  buildPromptContext(optimizedContext, agentType) {
    let prompt = '';

    // Add critical context first
    if (optimizedContext.critical) {
      prompt += this.formatContextSection('CRITICAL CONTEXT', optimizedContext.critical);
    }

    // Add important context
    if (optimizedContext.important) {
      prompt += this.formatContextSection('IMPORTANT CONTEXT', optimizedContext.important);
    }

    // Add optional context if available
    if (optimizedContext.optional && Object.keys(optimizedContext.optional).length > 0) {
      prompt += this.formatContextSection('ADDITIONAL CONTEXT', optimizedContext.optional);
    }

    return prompt;
  }

  formatContextSection(title, contextData) {
    let section = `\n${title}:\n`;
    section += '='.repeat(title.length + 1) + '\n\n';

    Object.entries(contextData).forEach(([key, value]) => {
      section += `${key.toUpperCase()}:\n`;
      
      if (typeof value === 'object') {
        section += JSON.stringify(value, null, 2);
      } else {
        section += value;
      }
      
      section += '\n\n';
    });

    return section;
  }

  // Context caching for efficiency
  getCacheKey(context, agentType) {
    const simplified = {
      type: agentType,
      keys: Object.keys(context).sort(),
      size: this.estimateTokens(JSON.stringify(context))
    };
    
    return Buffer.from(JSON.stringify(simplified)).toString('base64');
  }
}

module.exports = ContextManager;