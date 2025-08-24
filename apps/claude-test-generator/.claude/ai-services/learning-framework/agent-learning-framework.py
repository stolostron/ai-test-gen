"""
Agent Learning Framework - Core Implementation

Comprehensive learning infrastructure that enables all agents to learn from execution outcomes,
share patterns, and continuously improve accuracy through async processing.
"""

import asyncio
import json
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

# Import framework components
try:
    from .pattern_database import PatternDatabase
    from .performance_tracker import PerformanceTracker, MetricType
    from .async_executor import AsyncExecutor, LearningEvent, EventPriority
except ImportError:
    # Fallback for direct script execution
    from pattern_database import PatternDatabase
    from performance_tracker import PerformanceTracker, MetricType
    from async_executor import AsyncExecutor, LearningEvent, EventPriority

logger = logging.getLogger(__name__)


class AgentLearningFramework:
    """
    Core learning infrastructure for all agents
    Designed to be completely non-blocking and zero-impact
    """
    
    def __init__(self, config_path: str = ".claude/ai-services/learning-framework/config.json"):
        self.enabled = True  # Safe to enable by default
        self.validation_mode = True  # Extra validation during initial rollout
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.pattern_db = PatternDatabase(
            storage_path=self.config.get('pattern_storage_path', '.claude/learning-data/patterns')
        )
        self.performance_tracker = PerformanceTracker(
            storage_path=self.config.get('metrics_storage_path', '.claude/learning-data/metrics')
        )
        self.async_executor = AsyncExecutor(
            worker_count=self.config.get('worker_count', 3),
            queue_size=self.config.get('queue_size', 10000),
            batch_size=self.config.get('batch_size', 50)
        )
        
        # Knowledge base for cross-agent insights
        self.knowledge_base = KnowledgeBase()
        
        # ML models manager (simplified for now)
        self.ml_models = ModelManager()
        
        # Register event processors
        self._register_processors()
        
        # Start background tasks
        self._start_background_tasks()
        
        logger.info("Agent Learning Framework initialized and enabled")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file or use defaults"""
        config_file = Path(config_path)
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load config: {e}, using defaults")
        
        # Default configuration
        return {
            'enabled': True,
            'validation_mode': True,
            'pattern_storage_path': '.claude/learning-data/patterns',
            'metrics_storage_path': '.claude/learning-data/metrics',
            'worker_count': 3,
            'queue_size': 10000,
            'batch_size': 50,
            'cache_ttl': 3600,
            'pattern_relevance_threshold': 0.7,
            'anomaly_detection_enabled': True,
            'cross_agent_learning_enabled': True
        }
    
    def _register_processors(self):
        """Register event processors with async executor"""
        self.async_executor.register_processor(
            'agent_execution',
            self._process_agent_execution_event
        )
        self.async_executor.register_processor(
            'pattern_extraction',
            self._process_pattern_extraction_event
        )
        self.async_executor.register_processor(
            'cross_agent_insight',
            self._process_cross_agent_insight_event
        )
    
    def _start_background_tasks(self):
        """Start background maintenance tasks"""
        # Pattern cleanup task
        asyncio.create_task(self._periodic_pattern_cleanup())
        
        # Model update task
        asyncio.create_task(self._periodic_model_update())
        
        # Cross-agent analysis task
        asyncio.create_task(self._periodic_cross_agent_analysis())
    
    async def capture_execution(self, agent_id: str, task: Dict, result: Dict, metrics: Dict):
        """
        Async capture of execution data - never blocks main flow
        
        Args:
            agent_id: 'agent_a', 'agent_b', 'agent_c', or 'agent_d'
            task: Input task/request data
            result: Agent execution output
            metrics: Performance metrics (time, confidence, quality)
        """
        if not self.enabled:
            return
        
        try:
            # Create learning event
            event = LearningEvent(
                event_id=str(uuid.uuid4()),
                agent_id=agent_id,
                event_type='agent_execution',
                data={
                    'task': task,
                    'result': result,
                    'metrics': metrics,
                    'timestamp': datetime.utcnow().isoformat()
                },
                priority=EventPriority.NORMAL
            )
            
            # Queue for async processing
            queued = await self.async_executor.queue_event(event)
            
            if queued and self.validation_mode:
                logger.debug(f"Learning event queued for {agent_id}")
            
        except Exception as e:
            # Learning failures never affect main execution
            if self.validation_mode:
                logger.warning(f"Learning capture failed (non-critical): {e}")
    
    async def _process_agent_execution_event(self, event: LearningEvent):
        """Process agent execution event"""
        try:
            agent_id = event.agent_id
            data = event.data
            
            # Update performance metrics
            await self.performance_tracker.update_metrics(
                agent_id,
                data['metrics']
            )
            
            # Extract patterns
            patterns = await self._extract_patterns(agent_id, data)
            
            if patterns:
                # Store patterns
                await self.pattern_db.store_patterns(agent_id, patterns)
                
                # Check for cross-agent insights
                if self.config.get('cross_agent_learning_enabled', True):
                    await self._check_cross_agent_insights(agent_id, patterns)
            
            # Update ML models (queue for batch update)
            if data['metrics'].get('success'):
                await self.ml_models.queue_for_update(agent_id, data)
            
        except Exception as e:
            logger.error(f"Error processing execution event: {e}")
    
    async def _extract_patterns(self, agent_id: str, data: Dict) -> List[Dict]:
        """Extract reusable patterns from execution data"""
        patterns = []
        
        try:
            if agent_id == 'agent_a':
                patterns.extend(await self._extract_jira_patterns(data))
            elif agent_id == 'agent_b':
                patterns.extend(await self._extract_documentation_patterns(data))
            elif agent_id == 'agent_c':
                patterns.extend(await self._extract_github_patterns(data))
            elif agent_id == 'agent_d':
                patterns.extend(await self._extract_environment_patterns(data))
            
            # Extract common patterns
            patterns.extend(await self._extract_common_patterns(agent_id, data))
            
        except Exception as e:
            logger.error(f"Pattern extraction error: {e}")
        
        return patterns
    
    async def _extract_jira_patterns(self, data: Dict) -> List[Dict]:
        """Extract patterns specific to JIRA analysis"""
        patterns = []
        task = data.get('task', {})
        result = data.get('result', {})
        metrics = data.get('metrics', {})
        
        # Pattern: Successful ticket type identification
        if result.get('ticket_type') and metrics.get('success'):
            patterns.append({
                'type': 'jira_ticket_classification',
                'pattern': {
                    'keywords': task.get('keywords_found', []),
                    'ticket_type': result['ticket_type'],
                    'components': result.get('components', []),
                    'confidence': metrics.get('confidence', 0)
                },
                'success_rate': 1.0,
                'context': {
                    'ticket_id': task.get('ticket'),
                    'execution_time': metrics.get('execution_time', 0)
                }
            })
        
        # Pattern: Component detection success
        if result.get('components_identified') and len(result['components_identified']) > 0:
            patterns.append({
                'type': 'jira_component_detection',
                'pattern': {
                    'detection_method': result.get('detection_method', 'unknown'),
                    'components': result['components_identified'],
                    'keywords_used': task.get('component_keywords', [])
                },
                'success_rate': metrics.get('component_accuracy', 0.8),
                'context': {
                    'ticket_type': result.get('ticket_type'),
                    'field_sources': result.get('field_sources', [])
                }
            })
        
        return patterns
    
    async def _extract_documentation_patterns(self, data: Dict) -> List[Dict]:
        """Extract patterns from documentation analysis"""
        patterns = []
        result = data.get('result', {})
        metrics = data.get('metrics', {})
        
        # Pattern: Successful documentation search
        if result.get('docs_found') and metrics.get('relevance_score', 0) > 0.7:
            patterns.append({
                'type': 'doc_search_strategy',
                'pattern': {
                    'search_terms': result.get('search_terms', []),
                    'doc_sources': result.get('sources', []),
                    'relevance_score': metrics['relevance_score']
                },
                'success_rate': 1.0 if metrics.get('success') else 0.5
            })
        
        return patterns
    
    async def _extract_github_patterns(self, data: Dict) -> List[Dict]:
        """Extract patterns from GitHub investigation"""
        patterns = []
        result = data.get('result', {})
        metrics = data.get('metrics', {})
        
        # Pattern: PR analysis efficiency
        if result.get('pr_analyzed') and metrics.get('mcp_accelerated'):
            patterns.append({
                'type': 'github_pr_analysis',
                'pattern': {
                    'pr_size': result.get('pr_size', 'unknown'),
                    'files_changed': result.get('files_changed', 0),
                    'analysis_depth': result.get('analysis_depth', 'standard'),
                    'mcp_used': True
                },
                'success_rate': 1.0,
                'context': {
                    'execution_time': metrics.get('execution_time', 0),
                    'mcp_speedup': metrics.get('mcp_speedup', 1.0)
                }
            })
        
        return patterns
    
    async def _extract_environment_patterns(self, data: Dict) -> List[Dict]:
        """Extract patterns from environment analysis"""
        patterns = []
        result = data.get('result', {})
        metrics = data.get('metrics', {})
        
        # Pattern: Environment health check
        if result.get('health_score') and metrics.get('success'):
            patterns.append({
                'type': 'env_health_check',
                'pattern': {
                    'check_methods': result.get('check_methods', []),
                    'health_indicators': result.get('health_indicators', {}),
                    'cluster_type': result.get('cluster_type')
                },
                'success_rate': 1.0,
                'context': {
                    'health_score': result['health_score'],
                    'check_duration': metrics.get('execution_time', 0)
                }
            })
        
        return patterns
    
    async def _extract_common_patterns(self, agent_id: str, data: Dict) -> List[Dict]:
        """Extract patterns common to all agents"""
        patterns = []
        metrics = data.get('metrics', {})
        
        # Pattern: Execution efficiency
        if metrics.get('execution_time') and metrics.get('success'):
            baseline_time = self.performance_tracker.baselines.get(
                agent_id, {}
            ).get(MetricType.EXECUTION_TIME, 30.0)
            
            if metrics['execution_time'] < baseline_time * 0.8:  # 20% faster
                patterns.append({
                    'type': 'execution_optimization',
                    'pattern': {
                        'agent_id': agent_id,
                        'optimization_type': 'performance',
                        'time_saved': baseline_time - metrics['execution_time']
                    },
                    'success_rate': 1.0
                })
        
        return patterns
    
    def apply_learnings(self, agent_id: str, context: Dict) -> Optional[Dict]:
        """
        Apply learned patterns to improve agent execution
        This is called by enhanced agents during execution
        """
        if not self.enabled:
            return None
        
        try:
            # Get relevant patterns (cached, fast)
            patterns = self.pattern_db.get_cached_patterns(agent_id, context)
            
            if not patterns:
                return None
            
            # Get current performance stats
            stats = self.performance_tracker.get_current_stats(agent_id)
            
            # Generate recommendations
            recommendations = {
                'patterns': patterns[:3],  # Top 3 most relevant
                'performance_hints': self._generate_performance_hints(stats),
                'optimization_suggestions': self._generate_optimizations(agent_id, context, patterns),
                'confidence_adjustment': self._calculate_confidence_adjustment(patterns)
            }
            
            return recommendations
            
        except Exception as e:
            if self.validation_mode:
                logger.debug(f"Learning application skipped: {e}")
            return None
    
    def _generate_performance_hints(self, stats: Dict) -> List[str]:
        """Generate performance hints based on statistics"""
        hints = []
        
        # Check execution time trend
        exec_time_stats = stats.get(MetricType.EXECUTION_TIME.value, {})
        if exec_time_stats.get('trend') == 'declining':
            hints.append("Consider increasing timeout - execution times trending up")
        
        # Check success rate
        success_stats = stats.get(MetricType.SUCCESS_RATE.value, {})
        if success_stats.get('recent_mean', 1.0) < 0.9:
            hints.append("Success rate below 90% - consider retry logic")
        
        return hints
    
    def _generate_optimizations(self, agent_id: str, context: Dict, 
                               patterns: List[Dict]) -> List[Dict]:
        """Generate optimization suggestions based on patterns"""
        optimizations = []
        
        # Analyze patterns for optimization opportunities
        for pattern in patterns:
            if pattern['type'] == 'execution_optimization':
                optimizations.append({
                    'type': 'performance',
                    'suggestion': f"Use optimization from pattern {pattern.get('pattern_id', 'unknown')}",
                    'expected_improvement': pattern['pattern'].get('time_saved', 0)
                })
        
        return optimizations
    
    def _calculate_confidence_adjustment(self, patterns: List[Dict]) -> float:
        """Calculate confidence adjustment based on pattern success rates"""
        if not patterns:
            return 0.0
        
        # Weighted average of pattern success rates
        total_weight = 0.0
        weighted_sum = 0.0
        
        for pattern in patterns:
            relevance = pattern.get('relevance_score', 0.5)
            success_rate = pattern.get('stats', {}).get('success_rate', 0.5)
            
            weight = relevance
            weighted_sum += success_rate * weight
            total_weight += weight
        
        if total_weight > 0:
            adjustment = (weighted_sum / total_weight) - 0.5  # Center around 0
            return max(-0.1, min(0.1, adjustment))  # Cap at ±10%
        
        return 0.0
    
    async def _check_cross_agent_insights(self, agent_id: str, patterns: List[Dict]):
        """Check for insights that could benefit other agents"""
        for pattern in patterns:
            # Check if pattern might be useful for other agents
            if pattern.get('success_rate', 0) > 0.9:
                insight_event = LearningEvent(
                    event_id=str(uuid.uuid4()),
                    agent_id='cross_agent',
                    event_type='cross_agent_insight',
                    data={
                        'source_agent': agent_id,
                        'pattern': pattern,
                        'timestamp': datetime.utcnow().isoformat()
                    },
                    priority=EventPriority.LOW
                )
                await self.async_executor.queue_event(insight_event)
    
    async def _periodic_pattern_cleanup(self):
        """Periodically clean up old patterns"""
        while True:
            try:
                await asyncio.sleep(86400)  # Daily
                await self.pattern_db.cleanup_old_patterns(days=30)
                logger.info("Completed pattern cleanup")
            except Exception as e:
                logger.error(f"Pattern cleanup error: {e}")
    
    async def _periodic_model_update(self):
        """Periodically update ML models"""
        while True:
            try:
                await asyncio.sleep(3600)  # Hourly
                await self.ml_models.batch_update()
                logger.info("Completed model update")
            except Exception as e:
                logger.error(f"Model update error: {e}")
    
    async def _periodic_cross_agent_analysis(self):
        """Analyze patterns across agents for insights"""
        while True:
            try:
                await asyncio.sleep(7200)  # Every 2 hours
                insights = await self.knowledge_base.analyze_cross_agent_patterns(
                    self.pattern_db
                )
                logger.info(f"Found {len(insights)} cross-agent insights")
            except Exception as e:
                logger.error(f"Cross-agent analysis error: {e}")


class KnowledgeBase:
    """Manages cross-agent insights and shared knowledge"""
    
    def __init__(self):
        self.insights = []
        self.best_practices = {}
    
    async def analyze_cross_agent_patterns(self, pattern_db: PatternDatabase) -> List[Dict]:
        """Analyze patterns across all agents for insights"""
        insights = []
        
        # This is a simplified implementation
        # In production, this would use more sophisticated analysis
        
        return insights


class ModelManager:
    """Manages ML models for pattern recognition and optimization"""
    
    def __init__(self):
        self.update_queue = []
        self.models = {}
    
    async def queue_for_update(self, agent_id: str, data: Dict):
        """Queue data for model update"""
        self.update_queue.append({
            'agent_id': agent_id,
            'data': data,
            'timestamp': time.time()
        })
    
    async def batch_update(self):
        """Perform batch update of models"""
        if not self.update_queue:
            return
        
        # Process updates
        updates_by_agent = {}
        for update in self.update_queue:
            agent_id = update['agent_id']
            if agent_id not in updates_by_agent:
                updates_by_agent[agent_id] = []
            updates_by_agent[agent_id].append(update['data'])
        
        # Clear queue
        self.update_queue = []
        
        # Update models (simplified)
        for agent_id, updates in updates_by_agent.items():
            logger.debug(f"Updated model for {agent_id} with {len(updates)} samples")
