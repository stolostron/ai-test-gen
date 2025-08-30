#!/usr/bin/env python3
"""
Validation Learning Core - Non-Intrusive Learning Foundation

This module provides intelligent learning capabilities for all validation systems
while maintaining zero impact on existing framework operations.

Key Features:
- Advanced learning enabled by default (full ML capabilities)
- Non-intrusive operation (zero impact if disabled)
- Safe failure handling (learning failures never affect validation)
- Async-first processing (non-blocking operations)
- Configuration-controlled (complete environment variable control)
- Modular architecture (separate learning services)
- Resource-bounded (controlled memory and storage usage)
- Machine learning integration (TF-IDF, similarity matching, predictive analytics)

Author: AI Systems Suite / Claude Test Generator Framework
Version: 1.1.0 - ML-Enabled by Default
"""

import asyncio
import os
import json
import threading
import time
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import traceback
import psutil
import weakref


class LearningMode(Enum):
    """Learning operation modes with different capability levels"""
    DISABLED = "disabled"       # No learning operations
    CONSERVATIVE = "conservative"  # Basic pattern storage only
    STANDARD = "standard"       # Pattern storage + basic analytics
    ADVANCED = "advanced"       # Full learning capabilities (default)


@dataclass
class ValidationEvent:
    """Container for validation events to be learned from"""
    event_id: str
    event_type: str  # 'evidence_validation', 'cross_agent_validation', etc.
    context: Dict[str, Any]
    result: Dict[str, Any] 
    timestamp: datetime
    source_system: str
    success: bool
    confidence: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'context': self.context,
            'result': self.result,
            'timestamp': self.timestamp.isoformat(),
            'source_system': self.source_system,
            'success': self.success,
            'confidence': self.confidence,
            'metadata': self.metadata
        }


@dataclass
class ValidationInsights:
    """Container for learning-generated insights"""
    insight_type: str
    confidence: float
    recommendations: List[Dict[str, Any]]
    predictions: List[Dict[str, Any]]
    patterns_matched: List[str]
    generated_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'insight_type': self.insight_type,
            'confidence': self.confidence,
            'recommendations': self.recommendations,
            'predictions': self.predictions,
            'patterns_matched': self.patterns_matched,
            'generated_at': self.generated_at.isoformat()
        }


class ResourceMonitor:
    """Monitor system resources for safe learning operation"""
    
    def __init__(self):
        self.max_memory_mb = int(os.getenv('CLAUDE_LEARNING_MAX_MEMORY', '100'))
        self.max_cpu_percent = float(os.getenv('CLAUDE_LEARNING_MAX_CPU', '5.0'))
        
    def is_resource_available(self) -> bool:
        """Check if sufficient resources are available for learning"""
        try:
            # Check memory usage
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            if memory_mb > self.max_memory_mb:
                return False
            
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if cpu_percent > 90:  # System too busy
                return False
                
            return True
            
        except Exception:
            # If we can't check resources, assume not available
            return False


class StorageMonitor:
    """Monitor storage usage and availability"""
    
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.max_storage_mb = int(os.getenv('CLAUDE_LEARNING_MAX_STORAGE', '500'))
        
    def is_storage_available(self) -> bool:
        """Check if storage is available for learning data"""
        try:
            # Ensure storage directory exists
            self.storage_path.mkdir(parents=True, exist_ok=True)
            
            # Check storage space
            if self.storage_path.exists():
                storage_usage = self._calculate_storage_usage()
                return storage_usage < self.max_storage_mb
            
            return True
            
        except Exception:
            return False
    
    def _calculate_storage_usage(self) -> float:
        """Calculate current storage usage in MB"""
        try:
            total_size = 0
            for file_path in self.storage_path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            return total_size / 1024 / 1024  # Convert to MB
        except Exception:
            return 0.0


class SafeFailureManager:
    """Error isolation and recovery system"""
    
    def __init__(self):
        self.error_stats: Dict[str, int] = {}
        self.circuit_breakers: Dict[str, bool] = {}
        self.last_errors: Dict[str, datetime] = {}
        self.max_errors_per_operation = int(os.getenv('CLAUDE_LEARNING_MAX_ERRORS_PER_OP', '10'))
        self.circuit_breaker_timeout = int(os.getenv('CLAUDE_LEARNING_CIRCUIT_TIMEOUT', '300'))  # 5 minutes
        
    def handle_learning_failure(self, operation: str, error: Exception) -> None:
        """Handle learning operation failure safely"""
        try:
            # Track error statistics
            self.error_stats[operation] = self.error_stats.get(operation, 0) + 1
            self.last_errors[operation] = datetime.utcnow()
            
            # Apply circuit breaker if too many errors
            if self.error_stats[operation] > self.max_errors_per_operation:
                self.circuit_breakers[operation] = True
                
        except Exception:
            # Even failure handling should not fail
            pass
    
    def is_operation_safe(self, operation: str) -> bool:
        """Check if operation is safe to perform"""
        try:
            # Check circuit breaker
            if self.circuit_breakers.get(operation, False):
                # Check if circuit breaker timeout has expired
                last_error = self.last_errors.get(operation)
                if last_error:
                    timeout_expired = (datetime.utcnow() - last_error).total_seconds() > self.circuit_breaker_timeout
                    if timeout_expired:
                        # Reset circuit breaker
                        self.circuit_breakers[operation] = False
                        self.error_stats[operation] = 0
                        return True
                return False
            
            return True
            
        except Exception:
            return False  # Safe default
    
    def reset_circuit_breaker(self, operation: str) -> None:
        """Reset circuit breaker for operation"""
        try:
            self.circuit_breakers[operation] = False
            self.error_stats[operation] = 0
        except Exception:
            pass


class ConfigurationController:
    """Environment-based configuration control"""
    
    def __init__(self):
        self.config = self._load_configuration()
        self.config_lock = threading.Lock()
        
    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        return {
            'learning_mode': os.getenv('CLAUDE_VALIDATION_LEARNING', 'advanced'),
            'storage_path': os.getenv('CLAUDE_LEARNING_STORAGE_PATH', './.claude/learning/validation'),
            'max_memory_mb': int(os.getenv('CLAUDE_LEARNING_MAX_MEMORY', '100')),
            'max_storage_mb': int(os.getenv('CLAUDE_LEARNING_MAX_STORAGE', '500')),
            'learning_rate': float(os.getenv('CLAUDE_LEARNING_RATE', '0.1')),
            'pattern_retention_days': int(os.getenv('CLAUDE_PATTERN_RETENTION_DAYS', '30')),
            'analytics_enabled': os.getenv('CLAUDE_LEARNING_ANALYTICS', 'true').lower() == 'true',
            'prediction_enabled': os.getenv('CLAUDE_LEARNING_PREDICTION', 'true').lower() == 'true',
            'safe_failure_mode': os.getenv('CLAUDE_LEARNING_SAFE_FAILURE', 'true').lower() == 'true',
            'async_queue_size': int(os.getenv('CLAUDE_LEARNING_QUEUE_SIZE', '1000')),
            'max_processing_time_ms': int(os.getenv('CLAUDE_LEARNING_MAX_PROCESSING_TIME', '100')),
            'enable_monitoring': os.getenv('CLAUDE_LEARNING_MONITORING', 'true').lower() == 'true'
        }
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value safely"""
        with self.config_lock:
            return self.config.get(key, default)
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if specific learning feature is enabled"""
        with self.config_lock:
            if self.config['learning_mode'] == 'disabled':
                return False
            return self.config.get(f'{feature}_enabled', True)
    
    def reload_configuration(self) -> None:
        """Reload configuration from environment"""
        with self.config_lock:
            self.config = self._load_configuration()


class LearningMonitoring:
    """Learning system health and performance monitoring"""
    
    def __init__(self):
        self.metrics = {
            'events_processed': 0,
            'patterns_stored': 0,
            'insights_generated': 0,
            'predictions_made': 0,
            'errors_encountered': 0,
            'memory_usage_mb': 0.0,
            'storage_usage_mb': 0.0,
            'avg_processing_time_ms': 0.0,
            'last_activity': None
        }
        self.metrics_lock = threading.Lock()
        self.start_time = time.time()
        
    def record_metric(self, metric_name: str, value: Union[int, float]) -> None:
        """Record performance metric"""
        try:
            with self.metrics_lock:
                if metric_name in self.metrics:
                    if metric_name == 'avg_processing_time_ms':
                        # Calculate running average
                        current_avg = self.metrics[metric_name]
                        events_processed = self.metrics['events_processed']
                        if events_processed > 0:
                            self.metrics[metric_name] = (current_avg * events_processed + value) / (events_processed + 1)
                        else:
                            self.metrics[metric_name] = value
                    else:
                        self.metrics[metric_name] = value
                    
                self.metrics['last_activity'] = datetime.utcnow().isoformat()
                
        except Exception:
            pass  # Silent failure
    
    def increment_counter(self, counter_name: str) -> None:
        """Increment a counter metric"""
        try:
            with self.metrics_lock:
                if counter_name in self.metrics:
                    self.metrics[counter_name] += 1
                self.metrics['last_activity'] = datetime.utcnow().isoformat()
        except Exception:
            pass
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current learning system health status"""
        try:
            with self.metrics_lock:
                error_rate = self.metrics['errors_encountered'] / max(self.metrics['events_processed'], 1)
                uptime_seconds = time.time() - self.start_time
                
                status = 'healthy'
                if error_rate > 0.1:  # More than 10% error rate
                    status = 'degraded'
                elif self.metrics['errors_encountered'] > 50:
                    status = 'degraded'
                
                return {
                    'status': status,
                    'metrics': self.metrics.copy(),
                    'error_rate': error_rate,
                    'uptime_seconds': uptime_seconds,
                    'timestamp': datetime.utcnow().isoformat()
                }
        except Exception:
            return {
                'status': 'unknown',
                'metrics': {},
                'error_rate': 0.0,
                'uptime_seconds': 0.0,
                'timestamp': datetime.utcnow().isoformat()
            }


class ValidationLearningCore:
    """
    Non-intrusive learning foundation for all validation systems
    
    Key Features:
    - Zero impact on validation operations when disabled
    - Safe failure handling (learning failures never affect validation)
    - Async-first processing (non-blocking operations)
    - Configuration-controlled operation
    - Modular learning services
    - Resource-bounded operation
    
    Environment Variables:
    - CLAUDE_VALIDATION_LEARNING: disabled|conservative|standard|advanced
    - CLAUDE_LEARNING_STORAGE_PATH: Path for learning data storage
    - CLAUDE_LEARNING_MAX_MEMORY: Max memory usage in MB (default: 100)
    - CLAUDE_LEARNING_MAX_STORAGE: Max storage usage in MB (default: 500)
    - And many more configuration options...
    """
    
    # Class-level registry to prevent multiple instances
    _instances = weakref.WeakSet()
    _instance_lock = threading.Lock()
    
    def __init__(self):
        # Prevent multiple instances in same process
        with self._instance_lock:
            if any(isinstance(instance, ValidationLearningCore) for instance in self._instances):
                # Return existing instance behavior could be added here
                pass
            self._instances.add(self)
        
        # Configuration-based initialization
        self.config_controller = ConfigurationController()
        self.learning_mode = LearningMode(self.config_controller.get_config('learning_mode', 'advanced'))
        self.storage_path = self.config_controller.get_config('storage_path')
        self.async_queue_size = self.config_controller.get_config('async_queue_size', 1000)
        
        # Initialize safety components (always initialized)
        self.safe_failure_manager = SafeFailureManager()
        self.resource_monitor = ResourceMonitor()
        self.storage_monitor = StorageMonitor(self.storage_path)
        
        # Initialize monitoring if enabled
        if self.config_controller.get_config('enable_monitoring', True):
            self.monitoring = LearningMonitoring()
        else:
            self.monitoring = None
        
        # Initialize logger
        self.logger = logging.getLogger('validation_learning_core')
        self.logger.setLevel(logging.WARNING)  # Only warnings and errors by default
        
        # Async processing infrastructure
        self.learning_queue: Optional[asyncio.Queue] = None
        self.processing_task: Optional[asyncio.Task] = None
        self.shutdown_event = threading.Event()
        self.loop = None
        
        # Learning services (initialized only when enabled)
        self.pattern_memory = None
        self.analytics_service = None
        self.knowledge_base = None
        
        # Initialize learning services only if enabled
        if self.is_enabled():
            self._initialize_learning_services()
    
    def is_enabled(self) -> bool:
        """Check if learning is enabled"""
        return self.learning_mode != LearningMode.DISABLED
    
    def is_safe_to_learn(self) -> bool:
        """Check if it's safe to perform learning operations"""
        if not self.is_enabled():
            return False
        
        try:
            # Check safe failure manager
            if not self.safe_failure_manager.is_operation_safe('learning'):
                return False
            
            # Check system resources
            if not self.resource_monitor.is_resource_available():
                return False
            
            # Check storage availability
            if not self.storage_monitor.is_storage_available():
                return False
            
            return True
            
        except Exception:
            # If safety check fails, assume not safe
            return False
    
    def learn_from_validation(self, validation_event: ValidationEvent) -> None:
        """
        Non-blocking learning from validation events
        
        Key guarantees:
        - Never blocks validation operations
        - Silent failure on errors
        - Async processing
        - Resource-bounded
        
        Args:
            validation_event: ValidationEvent containing learning data
        """
        if not self.is_safe_to_learn():
            return
        
        try:
            # Ensure event has required fields
            if not self._validate_event(validation_event):
                return
            
            # Add to async queue (non-blocking)
            self._queue_learning_event_safe(validation_event)
            
            # Update monitoring
            if self.monitoring:
                self.monitoring.increment_counter('events_processed')
                
        except Exception as e:
            # Silent failure - learning never impacts validation
            self._handle_learning_error('learn_from_validation', e)
    
    def get_validation_insights(self, validation_context: Dict[str, Any]) -> Optional[ValidationInsights]:
        """
        Provide learning insights if available and safe
        
        Args:
            validation_context: Context for which to generate insights
            
        Returns:
            ValidationInsights if learning enabled and insights available
            None if learning disabled or insights unavailable
        """
        if not self.is_enabled():
            return None
        
        try:
            start_time = time.time()
            insights = self._generate_insights_safe(validation_context)
            
            # Update monitoring
            if self.monitoring:
                processing_time = (time.time() - start_time) * 1000  # Convert to ms
                self.monitoring.record_metric('avg_processing_time_ms', processing_time)
                if insights:
                    self.monitoring.increment_counter('insights_generated')
            
            return insights
            
        except Exception as e:
            self._handle_learning_error('get_validation_insights', e)
            return None
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get learning system health status"""
        if not self.is_enabled():
            return {
                'status': 'disabled',
                'learning_mode': self.learning_mode.value,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        base_status = {
            'status': 'enabled',
            'learning_mode': self.learning_mode.value,
            'safe_to_learn': self.is_safe_to_learn(),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if self.monitoring:
            monitoring_status = self.monitoring.get_health_status()
            base_status.update(monitoring_status)
        
        return base_status
    
    def shutdown(self) -> None:
        """Gracefully shutdown learning system"""
        try:
            self.shutdown_event.set()
            
            # Cancel processing task
            if self.processing_task and not self.processing_task.done():
                self.processing_task.cancel()
            
            # Close learning services
            if hasattr(self.pattern_memory, 'close'):
                self.pattern_memory.close()
            if hasattr(self.analytics_service, 'close'):
                self.analytics_service.close()
            if hasattr(self.knowledge_base, 'close'):
                self.knowledge_base.close()
                
        except Exception:
            # Silent failure during shutdown
            pass
    
    def _initialize_learning_services(self) -> None:
        """Initialize learning services (only when enabled)"""
        try:
            # Import learning services only when needed
            from learning_services import (
                ValidationPatternMemory,
                ValidationAnalyticsService,
                ValidationKnowledgeBase
            )
            
            self.pattern_memory = ValidationPatternMemory(
                storage_path=self.storage_path,
                learning_mode=self.learning_mode
            )
            
            if self.learning_mode in [LearningMode.STANDARD, LearningMode.ADVANCED]:
                self.analytics_service = ValidationAnalyticsService(
                    storage_path=self.storage_path,
                    learning_mode=self.learning_mode
                )
            
            if self.learning_mode == LearningMode.ADVANCED:
                self.knowledge_base = ValidationKnowledgeBase(
                    storage_path=self.storage_path,
                    learning_mode=self.learning_mode
                )
                
        except Exception as e:
            self._handle_learning_error('initialize_learning_services', e)
            # Disable learning if initialization fails
            self.learning_mode = LearningMode.DISABLED
    
    def _validate_event(self, event: ValidationEvent) -> bool:
        """Validate that event has required fields"""
        try:
            required_fields = ['event_id', 'event_type', 'context', 'result', 'timestamp', 'source_system']
            for field in required_fields:
                if not hasattr(event, field) or getattr(event, field) is None:
                    return False
            return True
        except Exception:
            return False
    
    def _queue_learning_event_safe(self, event: ValidationEvent) -> None:
        """Queue learning event for async processing safely"""
        try:
            # Initialize async infrastructure if needed
            if not self.learning_queue:
                self._initialize_async_processing()
            
            # Queue event if queue is not full
            if self.learning_queue and not self.learning_queue.full():
                # Use thread-safe approach to add to async queue
                if not self.loop or self.loop.is_closed():
                    return
                
                future = asyncio.run_coroutine_threadsafe(
                    self.learning_queue.put(event),
                    self.loop
                )
                # Don't wait for completion - fire and forget
                
        except Exception as e:
            self._handle_learning_error('queue_learning_event', e)
    
    def _initialize_async_processing(self) -> None:
        """Initialize async processing infrastructure"""
        try:
            # Create new event loop in thread
            def run_async_loop():
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                
                # Create queue
                self.learning_queue = asyncio.Queue(maxsize=self.async_queue_size)
                
                # Start processing task
                self.processing_task = self.loop.create_task(self._process_learning_queue())
                
                # Run loop
                self.loop.run_forever()
            
            # Start async thread
            async_thread = threading.Thread(target=run_async_loop, daemon=True)
            async_thread.start()
            
            # Give thread time to initialize
            time.sleep(0.1)
            
        except Exception as e:
            self._handle_learning_error('initialize_async_processing', e)
    
    async def _process_learning_queue(self) -> None:
        """Process learning events from queue"""
        while not self.shutdown_event.is_set():
            try:
                # Get event with timeout
                event = await asyncio.wait_for(
                    self.learning_queue.get(),
                    timeout=1.0
                )
                
                # Process event safely
                await self._process_learning_event_safe(event)
                
            except asyncio.TimeoutError:
                # Normal timeout - continue processing
                continue
            except Exception as e:
                self._handle_learning_error('process_learning_queue', e)
                # Continue processing - don't let one error stop learning
                continue
    
    async def _process_learning_event_safe(self, event: ValidationEvent) -> None:
        """Process single learning event safely"""
        try:
            start_time = time.time()
            
            # Store pattern if pattern memory available
            if self.pattern_memory:
                await self._store_pattern_async(event)
            
            # Update knowledge base if available
            if self.knowledge_base:
                await self._update_knowledge_async(event)
            
            # Update monitoring
            if self.monitoring:
                processing_time = (time.time() - start_time) * 1000
                self.monitoring.record_metric('avg_processing_time_ms', processing_time)
                self.monitoring.increment_counter('patterns_stored')
                
        except Exception as e:
            self._handle_learning_error('process_learning_event', e)
    
    async def _store_pattern_async(self, event: ValidationEvent) -> None:
        """Store validation pattern asynchronously"""
        try:
            if hasattr(self.pattern_memory, 'store_pattern_async'):
                await self.pattern_memory.store_pattern_async(event)
            elif hasattr(self.pattern_memory, 'store_pattern'):
                # Fallback to sync method
                self.pattern_memory.store_pattern(event)
        except Exception as e:
            self._handle_learning_error('store_pattern_async', e)
    
    async def _update_knowledge_async(self, event: ValidationEvent) -> None:
        """Update knowledge base asynchronously"""
        try:
            if hasattr(self.knowledge_base, 'update_knowledge_async'):
                await self.knowledge_base.update_knowledge_async(event)
            elif hasattr(self.knowledge_base, 'update_knowledge'):
                # Fallback to sync method
                self.knowledge_base.update_knowledge(event)
        except Exception as e:
            self._handle_learning_error('update_knowledge_async', e)
    
    def _generate_insights_safe(self, context: Dict[str, Any]) -> Optional[ValidationInsights]:
        """Generate insights safely"""
        try:
            # Use analytics service if available
            if self.analytics_service and hasattr(self.analytics_service, 'generate_insights'):
                return self.analytics_service.generate_insights(context)
            
            # Use pattern memory for basic insights if available
            if self.pattern_memory and hasattr(self.pattern_memory, 'find_similar_patterns'):
                patterns = self.pattern_memory.find_similar_patterns(context)
                if patterns:
                    return ValidationInsights(
                        insight_type='pattern_match',
                        confidence=0.7,
                        recommendations=[],
                        predictions=[],
                        patterns_matched=[p.get('pattern_id', '') for p in patterns],
                        generated_at=datetime.utcnow()
                    )
            
            return None
            
        except Exception as e:
            self._handle_learning_error('generate_insights', e)
            return None
    
    def _handle_learning_error(self, operation: str, error: Exception) -> None:
        """Handle learning errors safely"""
        try:
            # Update failure manager
            self.safe_failure_manager.handle_learning_failure(operation, error)
            
            # Update monitoring
            if self.monitoring:
                self.monitoring.increment_counter('errors_encountered')
            
            # Log error (at debug level to avoid spam)
            self.logger.debug(f"Learning error in {operation}: {str(error)}")
            
        except Exception:
            # Even error handling should not fail
            pass


# Singleton instance management
_learning_core_instance: Optional[ValidationLearningCore] = None
_instance_lock = threading.Lock()


def get_learning_core() -> ValidationLearningCore:
    """Get singleton ValidationLearningCore instance"""
    global _learning_core_instance
    
    with _instance_lock:
        if _learning_core_instance is None:
            _learning_core_instance = ValidationLearningCore()
        return _learning_core_instance


def shutdown_learning_core() -> None:
    """Shutdown singleton ValidationLearningCore instance"""
    global _learning_core_instance
    
    with _instance_lock:
        if _learning_core_instance is not None:
            _learning_core_instance.shutdown()
            _learning_core_instance = None


# Auto-cleanup on module unload
import atexit
atexit.register(shutdown_learning_core)