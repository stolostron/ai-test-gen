#!/usr/bin/env python3
"""
Learning Services - Modular Learning Components

This module provides the learning services used by the ValidationLearningCore:
- ValidationPatternMemory: Pattern storage and retrieval
- ValidationAnalyticsService: Learning insights and prediction
- ValidationKnowledgeBase: Accumulated learning data management

All services follow the same safety principles:
- Non-intrusive operation
- Safe failure handling
- Resource-bounded operation
- Configuration-controlled

Author: AI Systems Suite / Claude Test Generator Framework
Version: 1.0.0
"""

import asyncio
import json
import sqlite3
import threading
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
import pickle
import os
import logging
from collections import defaultdict, deque
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

from .validation_learning_core import LearningMode, ValidationEvent, ValidationInsights


@dataclass
class ValidationPattern:
    """Container for validation patterns"""
    pattern_id: str
    pattern_type: str
    context_signature: str
    success_rate: float
    usage_count: int
    first_seen: datetime
    last_seen: datetime
    pattern_data: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            'pattern_id': self.pattern_id,
            'pattern_type': self.pattern_type,
            'context_signature': self.context_signature,
            'success_rate': self.success_rate,
            'usage_count': self.usage_count,
            'first_seen': self.first_seen.isoformat(),
            'last_seen': self.last_seen.isoformat(),
            'pattern_data': self.pattern_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationPattern':
        """Create from dictionary"""
        return cls(
            pattern_id=data['pattern_id'],
            pattern_type=data['pattern_type'],
            context_signature=data['context_signature'],
            success_rate=data['success_rate'],
            usage_count=data['usage_count'],
            first_seen=datetime.fromisoformat(data['first_seen']),
            last_seen=datetime.fromisoformat(data['last_seen']),
            pattern_data=data['pattern_data']
        )


class ValidationPatternMemory:
    """
    Pattern storage and retrieval service
    
    Responsibilities:
    - Store validation patterns and outcomes
    - Retrieve similar patterns for prediction
    - Maintain pattern success rates
    - Pattern categorization and indexing
    """
    
    def __init__(self, storage_path: str, learning_mode: LearningMode):
        self.storage_path = Path(storage_path)
        self.learning_mode = learning_mode
        self.logger = logging.getLogger('validation_pattern_memory')
        
        # Thread safety
        self.lock = threading.Lock()
        
        # In-memory cache for recent patterns
        self.pattern_cache: Dict[str, ValidationPattern] = {}
        self.cache_size = 1000
        self.cache_access_order = deque()
        
        # Pattern similarity computation
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.pattern_vectors = {}
        
        # Initialize storage
        self._initialize_storage()
        
        # Load existing patterns
        self._load_patterns_from_storage()
    
    def _initialize_storage(self) -> None:
        """Initialize pattern storage"""
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            
            # Initialize SQLite database for patterns
            self.db_path = self.storage_path / 'patterns.db'
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS patterns (
                        pattern_id TEXT PRIMARY KEY,
                        pattern_type TEXT,
                        context_signature TEXT,
                        success_rate REAL,
                        usage_count INTEGER,
                        first_seen TEXT,
                        last_seen TEXT,
                        pattern_data TEXT
                    )
                ''')
                
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_pattern_type ON patterns(pattern_type)
                ''')
                
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_context_signature ON patterns(context_signature)
                ''')
                
        except Exception as e:
            self.logger.warning(f"Failed to initialize pattern storage: {e}")
    
    def _load_patterns_from_storage(self) -> None:
        """Load existing patterns from storage into cache"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.execute('''
                    SELECT * FROM patterns 
                    ORDER BY last_seen DESC 
                    LIMIT ?
                ''', (self.cache_size,))
                
                for row in cursor.fetchall():
                    pattern_data = json.loads(row[7])  # pattern_data column
                    pattern = ValidationPattern(
                        pattern_id=row[0],
                        pattern_type=row[1],
                        context_signature=row[2],
                        success_rate=row[3],
                        usage_count=row[4],
                        first_seen=datetime.fromisoformat(row[5]),
                        last_seen=datetime.fromisoformat(row[6]),
                        pattern_data=pattern_data
                    )
                    
                    self.pattern_cache[pattern.pattern_id] = pattern
                    self.cache_access_order.append(pattern.pattern_id)
                    
        except Exception as e:
            self.logger.warning(f"Failed to load patterns from storage: {e}")
    
    def store_pattern(self, validation_event: ValidationEvent) -> None:
        """Store validation pattern for future reference"""
        if not self._is_storage_safe():
            return
        
        try:
            # Create pattern from validation event
            pattern = self._create_pattern_from_event(validation_event)
            
            # Store pattern
            asyncio.create_task(self.store_pattern_async(pattern))
            
        except Exception as e:
            self.logger.warning(f"Pattern storage failed: {e}")
    
    async def store_pattern_async(self, pattern: ValidationPattern) -> None:
        """Store pattern asynchronously"""
        try:
            with self.lock:
                # Update or create pattern
                existing_pattern = self.pattern_cache.get(pattern.pattern_id)
                
                if existing_pattern:
                    # Update existing pattern
                    existing_pattern.usage_count += 1
                    existing_pattern.last_seen = pattern.last_seen
                    
                    # Update success rate (running average)
                    total_events = existing_pattern.usage_count
                    existing_pattern.success_rate = (
                        (existing_pattern.success_rate * (total_events - 1) + 
                         (1.0 if pattern.pattern_data.get('success', False) else 0.0)) / total_events
                    )
                    
                    updated_pattern = existing_pattern
                else:
                    # Add new pattern
                    updated_pattern = pattern
                    self._add_to_cache(updated_pattern)
                
                # Store to database
                await self._store_to_database(updated_pattern)
                
        except Exception as e:
            self.logger.warning(f"Async pattern storage failed: {e}")
    
    def find_similar_patterns(self, context: Dict[str, Any], limit: int = 5) -> List[ValidationPattern]:
        """Find similar patterns for prediction"""
        if not self._is_retrieval_safe():
            return []
        
        try:
            context_signature = self._create_context_signature(context)
            similar_patterns = []
            
            with self.lock:
                # First, look for exact matches
                for pattern in self.pattern_cache.values():
                    if pattern.context_signature == context_signature:
                        similar_patterns.append(pattern)
                
                # If no exact matches, look for similar patterns
                if not similar_patterns:
                    similar_patterns = self._find_similar_by_content(context, limit)
            
            # Sort by success rate and usage count
            similar_patterns.sort(
                key=lambda p: (p.success_rate, p.usage_count),
                reverse=True
            )
            
            return similar_patterns[:limit]
            
        except Exception as e:
            self.logger.warning(f"Pattern retrieval failed: {e}")
            return []
    
    def get_pattern_success_rate(self, pattern_id: str) -> float:
        """Get success rate for specific pattern"""
        try:
            with self.lock:
                pattern = self.pattern_cache.get(pattern_id)
                if pattern:
                    return pattern.success_rate
                
                # Check database if not in cache
                return self._get_success_rate_from_db(pattern_id)
                
        except Exception:
            return 0.0
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get pattern memory statistics"""
        try:
            with self.lock:
                total_patterns = len(self.pattern_cache)
                successful_patterns = sum(1 for p in self.pattern_cache.values() if p.success_rate > 0.5)
                
                pattern_types = defaultdict(int)
                for pattern in self.pattern_cache.values():
                    pattern_types[pattern.pattern_type] += 1
                
                return {
                    'total_patterns': total_patterns,
                    'successful_patterns': successful_patterns,
                    'success_rate_distribution': {
                        'high_success': sum(1 for p in self.pattern_cache.values() if p.success_rate > 0.8),
                        'medium_success': sum(1 for p in self.pattern_cache.values() if 0.5 < p.success_rate <= 0.8),
                        'low_success': sum(1 for p in self.pattern_cache.values() if p.success_rate <= 0.5),
                    },
                    'pattern_types': dict(pattern_types),
                    'cache_utilization': len(self.pattern_cache) / self.cache_size
                }
                
        except Exception:
            return {}
    
    def _create_pattern_from_event(self, event: ValidationEvent) -> ValidationPattern:
        """Create validation pattern from event"""
        context_signature = self._create_context_signature(event.context)
        pattern_id = self._generate_pattern_id(event.event_type, context_signature)
        
        return ValidationPattern(
            pattern_id=pattern_id,
            pattern_type=event.event_type,
            context_signature=context_signature,
            success_rate=1.0 if event.success else 0.0,
            usage_count=1,
            first_seen=event.timestamp,
            last_seen=event.timestamp,
            pattern_data={
                'success': event.success,
                'confidence': event.confidence,
                'context_keys': list(event.context.keys()),
                'result_keys': list(event.result.keys()) if isinstance(event.result, dict) else [],
                'source_system': event.source_system
            }
        )
    
    def _create_context_signature(self, context: Dict[str, Any]) -> str:
        """Create signature for context to enable pattern matching"""
        try:
            # Extract key features from context
            features = []
            
            # Add context keys (sorted for consistency)
            features.extend(sorted(context.keys()))
            
            # Add some value signatures for important keys
            for key in ['validation_type', 'operation_type', 'component_type']:
                if key in context:
                    features.append(f"{key}:{context[key]}")
            
            # Create hash of features
            signature_text = '|'.join(features)
            return hashlib.md5(signature_text.encode()).hexdigest()[:16]
            
        except Exception:
            return "unknown"
    
    def _generate_pattern_id(self, event_type: str, context_signature: str) -> str:
        """Generate unique pattern ID"""
        id_text = f"{event_type}:{context_signature}"
        return hashlib.sha256(id_text.encode()).hexdigest()[:32]
    
    def _find_similar_by_content(self, context: Dict[str, Any], limit: int) -> List[ValidationPattern]:
        """Find similar patterns using content similarity"""
        try:
            # Convert context to text for similarity comparison
            context_text = json.dumps(context, sort_keys=True)
            
            similarities = []
            for pattern in self.pattern_cache.values():
                pattern_text = json.dumps(pattern.pattern_data, sort_keys=True)
                
                # Simple text similarity (could be enhanced with ML)
                similarity = self._calculate_text_similarity(context_text, pattern_text)
                if similarity > 0.3:  # Minimum similarity threshold
                    similarities.append((similarity, pattern))
            
            # Sort by similarity and return top matches
            similarities.sort(key=lambda x: x[0], reverse=True)
            return [pattern for _, pattern in similarities[:limit]]
            
        except Exception:
            return []
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        try:
            # Simple token-based similarity
            tokens1 = set(text1.lower().split())
            tokens2 = set(text2.lower().split())
            
            if not tokens1 or not tokens2:
                return 0.0
            
            intersection = len(tokens1.intersection(tokens2))
            union = len(tokens1.union(tokens2))
            
            return intersection / union if union > 0 else 0.0
            
        except Exception:
            return 0.0
    
    def _add_to_cache(self, pattern: ValidationPattern) -> None:
        """Add pattern to cache with LRU eviction"""
        try:
            # Add to cache
            self.pattern_cache[pattern.pattern_id] = pattern
            self.cache_access_order.append(pattern.pattern_id)
            
            # Evict if cache is full
            while len(self.pattern_cache) > self.cache_size:
                oldest_id = self.cache_access_order.popleft()
                if oldest_id in self.pattern_cache:
                    del self.pattern_cache[oldest_id]
                    
        except Exception:
            pass
    
    async def _store_to_database(self, pattern: ValidationPattern) -> None:
        """Store pattern to database"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO patterns 
                    (pattern_id, pattern_type, context_signature, success_rate, 
                     usage_count, first_seen, last_seen, pattern_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    pattern.pattern_id,
                    pattern.pattern_type,
                    pattern.context_signature,
                    pattern.success_rate,
                    pattern.usage_count,
                    pattern.first_seen.isoformat(),
                    pattern.last_seen.isoformat(),
                    json.dumps(pattern.pattern_data)
                ))
                
        except Exception as e:
            self.logger.warning(f"Database storage failed: {e}")
    
    def _get_success_rate_from_db(self, pattern_id: str) -> float:
        """Get success rate from database"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.execute(
                    'SELECT success_rate FROM patterns WHERE pattern_id = ?',
                    (pattern_id,)
                )
                row = cursor.fetchone()
                return row[0] if row else 0.0
                
        except Exception:
            return 0.0
    
    def _is_storage_safe(self) -> bool:
        """Check if storage operations are safe"""
        try:
            return self.storage_path.exists() and os.access(str(self.storage_path), os.W_OK)
        except Exception:
            return False
    
    def _is_retrieval_safe(self) -> bool:
        """Check if retrieval operations are safe"""
        try:
            return len(self.pattern_cache) > 0 or self.db_path.exists()
        except Exception:
            return False
    
    def close(self) -> None:
        """Close pattern memory and cleanup resources"""
        try:
            # Clear cache
            with self.lock:
                self.pattern_cache.clear()
                self.cache_access_order.clear()
        except Exception:
            pass


class ValidationAnalyticsService:
    """
    Learning insights and prediction service
    
    Responsibilities:
    - Generate predictive insights
    - Analyze validation trends
    - Provide recommendations
    - Performance analytics
    """
    
    def __init__(self, storage_path: str, learning_mode: LearningMode):
        self.storage_path = Path(storage_path)
        self.learning_mode = learning_mode
        self.logger = logging.getLogger('validation_analytics_service')
        
        # Analytics data
        self.validation_history = deque(maxlen=10000)  # Keep last 10k events
        self.trend_data = defaultdict(list)
        self.lock = threading.Lock()
        
        # Prediction models (simple statistical models)
        self.success_rate_predictor = None
        self.confidence_predictor = None
        
        # Initialize analytics storage
        self._initialize_analytics_storage()
    
    def _initialize_analytics_storage(self) -> None:
        """Initialize analytics storage"""
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self.analytics_db = self.storage_path / 'analytics.db'
            
            with sqlite3.connect(str(self.analytics_db)) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS validation_events (
                        event_id TEXT PRIMARY KEY,
                        event_type TEXT,
                        timestamp TEXT,
                        success INTEGER,
                        confidence REAL,
                        source_system TEXT,
                        processing_time_ms REAL
                    )
                ''')
                
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS trend_data (
                        date TEXT,
                        metric_name TEXT,
                        metric_value REAL,
                        PRIMARY KEY (date, metric_name)
                    )
                ''')
                
        except Exception as e:
            self.logger.warning(f"Failed to initialize analytics storage: {e}")
    
    def record_validation_event(self, event: ValidationEvent, processing_time_ms: float = 0.0) -> None:
        """Record validation event for analytics"""
        try:
            with self.lock:
                # Add to in-memory history
                event_record = {
                    'event_id': event.event_id,
                    'event_type': event.event_type,
                    'timestamp': event.timestamp,
                    'success': event.success,
                    'confidence': event.confidence,
                    'source_system': event.source_system,
                    'processing_time_ms': processing_time_ms
                }
                
                self.validation_history.append(event_record)
                
                # Update trend data
                date_key = event.timestamp.strftime('%Y-%m-%d')
                self.trend_data[date_key].append(event_record)
                
                # Store to database (async)
                asyncio.create_task(self._store_event_to_db(event_record))
                
        except Exception as e:
            self.logger.warning(f"Failed to record validation event: {e}")
    
    def generate_insights(self, context: Dict[str, Any]) -> Optional[ValidationInsights]:
        """Generate insights based on historical patterns"""
        if not self._is_analytics_safe():
            return None
        
        try:
            with self.lock:
                # Analyze similar contexts
                similar_events = self._find_similar_events(context)
                
                if not similar_events:
                    return None
                
                # Generate recommendations
                recommendations = self._generate_recommendations(similar_events)
                
                # Generate predictions
                predictions = self._generate_predictions(similar_events, context)
                
                # Calculate confidence
                confidence = min(0.9, len(similar_events) / 10.0)  # More events = higher confidence
                
                return ValidationInsights(
                    insight_type='analytics_insights',
                    confidence=confidence,
                    recommendations=recommendations,
                    predictions=predictions,
                    patterns_matched=[e['event_id'] for e in similar_events[:5]],
                    generated_at=datetime.utcnow()
                )
                
        except Exception as e:
            self.logger.warning(f"Failed to generate insights: {e}")
            return None
    
    def analyze_validation_trends(self) -> Optional[Dict[str, Any]]:
        """Analyze validation trends over time"""
        try:
            with self.lock:
                if len(self.validation_history) < 10:
                    return None
                
                # Calculate trends over different time periods
                trends = {}
                
                # Last 24 hours
                recent_events = [
                    e for e in self.validation_history 
                    if (datetime.utcnow() - e['timestamp']).total_seconds() < 86400
                ]
                
                if recent_events:
                    trends['last_24h'] = self._calculate_trend_metrics(recent_events)
                
                # Last 7 days
                week_events = [
                    e for e in self.validation_history 
                    if (datetime.utcnow() - e['timestamp']).total_seconds() < 604800
                ]
                
                if week_events:
                    trends['last_7d'] = self._calculate_trend_metrics(week_events)
                
                # Overall trends
                trends['overall'] = self._calculate_trend_metrics(list(self.validation_history))
                
                return trends
                
        except Exception as e:
            self.logger.warning(f"Failed to analyze trends: {e}")
            return None
    
    def predict_validation_outcome(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Predict likely validation outcome"""
        try:
            with self.lock:
                similar_events = self._find_similar_events(context)
                
                if len(similar_events) < 3:
                    return None
                
                # Calculate success probability
                success_count = sum(1 for e in similar_events if e['success'])
                success_probability = success_count / len(similar_events)
                
                # Calculate expected confidence
                avg_confidence = sum(e['confidence'] for e in similar_events) / len(similar_events)
                
                return {
                    'success_probability': success_probability,
                    'expected_confidence': avg_confidence,
                    'sample_size': len(similar_events),
                    'prediction_confidence': min(0.9, len(similar_events) / 20.0)
                }
                
        except Exception as e:
            self.logger.warning(f"Failed to predict outcome: {e}")
            return None
    
    def _find_similar_events(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find similar validation events"""
        try:
            context_type = context.get('validation_type', 'unknown')
            similar_events = []
            
            for event in self.validation_history:
                # Simple similarity based on event type and source system
                if (event.get('event_type') == context_type or 
                    event.get('source_system') == context.get('source_system')):
                    similar_events.append(event)
            
            return similar_events[-50:]  # Return last 50 similar events
            
        except Exception:
            return []
    
    def _generate_recommendations(self, similar_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate recommendations based on similar events"""
        try:
            recommendations = []
            
            # Analyze success patterns
            successful_events = [e for e in similar_events if e['success']]
            failed_events = [e for e in similar_events if not e['success']]
            
            success_rate = len(successful_events) / len(similar_events) if similar_events else 0.0
            
            if success_rate < 0.5:
                recommendations.append({
                    'type': 'caution',
                    'message': 'Similar validations have low success rate',
                    'confidence': 0.8,
                    'details': {
                        'success_rate': success_rate,
                        'sample_size': len(similar_events)
                    }
                })
            
            if successful_events:
                avg_processing_time = sum(e.get('processing_time_ms', 0) for e in successful_events) / len(successful_events)
                recommendations.append({
                    'type': 'performance',
                    'message': f'Expected processing time: {avg_processing_time:.1f}ms',
                    'confidence': 0.7,
                    'details': {
                        'avg_processing_time_ms': avg_processing_time
                    }
                })
            
            return recommendations
            
        except Exception:
            return []
    
    def _generate_predictions(self, similar_events: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate predictions based on similar events"""
        try:
            predictions = []
            
            if len(similar_events) >= 5:
                # Predict success probability
                success_count = sum(1 for e in similar_events if e['success'])
                success_prob = success_count / len(similar_events)
                
                predictions.append({
                    'type': 'success_probability',
                    'value': success_prob,
                    'confidence': min(0.9, len(similar_events) / 20.0),
                    'sample_size': len(similar_events)
                })
                
                # Predict confidence level
                avg_confidence = sum(e['confidence'] for e in similar_events) / len(similar_events)
                predictions.append({
                    'type': 'expected_confidence',
                    'value': avg_confidence,
                    'confidence': 0.7,
                    'sample_size': len(similar_events)
                })
            
            return predictions
            
        except Exception:
            return []
    
    def _calculate_trend_metrics(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate trend metrics for events"""
        try:
            if not events:
                return {}
            
            total_events = len(events)
            successful_events = sum(1 for e in events if e['success'])
            success_rate = successful_events / total_events
            
            avg_confidence = sum(e['confidence'] for e in events) / total_events
            avg_processing_time = sum(e.get('processing_time_ms', 0) for e in events) / total_events
            
            # Group by source system
            by_system = defaultdict(list)
            for event in events:
                by_system[event['source_system']].append(event)
            
            system_stats = {}
            for system, system_events in by_system.items():
                system_success_rate = sum(1 for e in system_events if e['success']) / len(system_events)
                system_stats[system] = {
                    'event_count': len(system_events),
                    'success_rate': system_success_rate
                }
            
            return {
                'total_events': total_events,
                'success_rate': success_rate,
                'avg_confidence': avg_confidence,
                'avg_processing_time_ms': avg_processing_time,
                'by_system': system_stats
            }
            
        except Exception:
            return {}
    
    async def _store_event_to_db(self, event_record: Dict[str, Any]) -> None:
        """Store event to analytics database"""
        try:
            with sqlite3.connect(str(self.analytics_db)) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO validation_events 
                    (event_id, event_type, timestamp, success, confidence, source_system, processing_time_ms)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event_record['event_id'],
                    event_record['event_type'],
                    event_record['timestamp'].isoformat(),
                    1 if event_record['success'] else 0,
                    event_record['confidence'],
                    event_record['source_system'],
                    event_record['processing_time_ms']
                ))
                
        except Exception as e:
            self.logger.warning(f"Failed to store event to database: {e}")
    
    def _is_analytics_safe(self) -> bool:
        """Check if analytics operations are safe"""
        try:
            return len(self.validation_history) > 0
        except Exception:
            return False
    
    def close(self) -> None:
        """Close analytics service and cleanup resources"""
        try:
            with self.lock:
                self.validation_history.clear()
                self.trend_data.clear()
        except Exception:
            pass


class ValidationKnowledgeBase:
    """
    Accumulated learning data management
    
    Responsibilities:
    - Maintain learning knowledge base
    - Knowledge base optimization
    - Knowledge base queries
    - Knowledge base maintenance
    """
    
    def __init__(self, storage_path: str, learning_mode: LearningMode):
        self.storage_path = Path(storage_path)
        self.learning_mode = learning_mode
        self.logger = logging.getLogger('validation_knowledge_base')
        
        # Knowledge storage
        self.knowledge_db_path = self.storage_path / 'knowledge.db'
        self.lock = threading.Lock()
        
        # Initialize knowledge base
        self._initialize_knowledge_storage()
    
    def _initialize_knowledge_storage(self) -> None:
        """Initialize knowledge base storage"""
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            
            with sqlite3.connect(str(self.knowledge_db_path)) as conn:
                # Knowledge entries table
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS knowledge_entries (
                        entry_id TEXT PRIMARY KEY,
                        knowledge_type TEXT,
                        subject TEXT,
                        content TEXT,
                        confidence REAL,
                        evidence_count INTEGER,
                        created_at TEXT,
                        updated_at TEXT
                    )
                ''')
                
                # Knowledge relationships table
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS knowledge_relationships (
                        relationship_id TEXT PRIMARY KEY,
                        from_entry_id TEXT,
                        to_entry_id TEXT,
                        relationship_type TEXT,
                        strength REAL,
                        created_at TEXT
                    )
                ''')
                
                # Indexes
                conn.execute('CREATE INDEX IF NOT EXISTS idx_knowledge_type ON knowledge_entries(knowledge_type)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_subject ON knowledge_entries(subject)')
                
        except Exception as e:
            self.logger.warning(f"Failed to initialize knowledge storage: {e}")
    
    def update_knowledge(self, validation_event: ValidationEvent) -> None:
        """Update knowledge base with new learning data"""
        if not self._is_update_safe():
            return
        
        try:
            # Extract knowledge from validation event
            knowledge_entries = self._extract_knowledge_from_event(validation_event)
            
            for entry in knowledge_entries:
                asyncio.create_task(self._update_knowledge_entry(entry))
                
        except Exception as e:
            self.logger.warning(f"Knowledge update failed: {e}")
    
    async def update_knowledge_async(self, validation_event: ValidationEvent) -> None:
        """Update knowledge base asynchronously"""
        try:
            knowledge_entries = self._extract_knowledge_from_event(validation_event)
            
            for entry in knowledge_entries:
                await self._update_knowledge_entry(entry)
                
        except Exception as e:
            self.logger.warning(f"Async knowledge update failed: {e}")
    
    def query_knowledge(self, subject: str, knowledge_type: str = None) -> Optional[Dict[str, Any]]:
        """Query knowledge base for specific information"""
        try:
            with self.lock:
                with sqlite3.connect(str(self.knowledge_db_path)) as conn:
                    if knowledge_type:
                        cursor = conn.execute('''
                            SELECT * FROM knowledge_entries 
                            WHERE subject = ? AND knowledge_type = ?
                            ORDER BY confidence DESC, updated_at DESC
                            LIMIT 10
                        ''', (subject, knowledge_type))
                    else:
                        cursor = conn.execute('''
                            SELECT * FROM knowledge_entries 
                            WHERE subject = ?
                            ORDER BY confidence DESC, updated_at DESC
                            LIMIT 10
                        ''', (subject,))
                    
                    entries = []
                    for row in cursor.fetchall():
                        entries.append({
                            'entry_id': row[0],
                            'knowledge_type': row[1],
                            'subject': row[2],
                            'content': json.loads(row[3]),
                            'confidence': row[4],
                            'evidence_count': row[5],
                            'created_at': row[6],
                            'updated_at': row[7]
                        })
                    
                    return {
                        'subject': subject,
                        'entries': entries,
                        'total_entries': len(entries)
                    }
                    
        except Exception as e:
            self.logger.warning(f"Knowledge query failed: {e}")
            return None
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get summary of knowledge base"""
        try:
            with self.lock:
                with sqlite3.connect(str(self.knowledge_db_path)) as conn:
                    # Count entries by type
                    cursor = conn.execute('''
                        SELECT knowledge_type, COUNT(*) 
                        FROM knowledge_entries 
                        GROUP BY knowledge_type
                    ''')
                    
                    type_counts = dict(cursor.fetchall())
                    
                    # Get total entries
                    cursor = conn.execute('SELECT COUNT(*) FROM knowledge_entries')
                    total_entries = cursor.fetchone()[0]
                    
                    # Get average confidence
                    cursor = conn.execute('SELECT AVG(confidence) FROM knowledge_entries')
                    avg_confidence = cursor.fetchone()[0] or 0.0
                    
                    return {
                        'total_entries': total_entries,
                        'average_confidence': avg_confidence,
                        'entries_by_type': type_counts,
                        'last_updated': datetime.utcnow().isoformat()
                    }
                    
        except Exception:
            return {}
    
    def _extract_knowledge_from_event(self, event: ValidationEvent) -> List[Dict[str, Any]]:
        """Extract knowledge entries from validation event"""
        try:
            knowledge_entries = []
            
            # Extract pattern knowledge
            if event.success and event.confidence > 0.7:
                knowledge_entries.append({
                    'knowledge_type': 'successful_pattern',
                    'subject': f"{event.event_type}:{event.source_system}",
                    'content': {
                        'context_keys': list(event.context.keys()),
                        'success_factors': event.metadata,
                        'confidence': event.confidence
                    },
                    'confidence': event.confidence,
                    'evidence_count': 1
                })
            
            # Extract failure knowledge
            if not event.success:
                knowledge_entries.append({
                    'knowledge_type': 'failure_pattern',
                    'subject': f"{event.event_type}:{event.source_system}",
                    'content': {
                        'context': event.context,
                        'result': event.result,
                        'failure_indicators': event.metadata
                    },
                    'confidence': 1.0 - event.confidence,
                    'evidence_count': 1
                })
            
            # Extract system-specific knowledge
            knowledge_entries.append({
                'knowledge_type': 'system_behavior',
                'subject': event.source_system,
                'content': {
                    'event_type': event.event_type,
                    'typical_confidence': event.confidence,
                    'success_rate': 1.0 if event.success else 0.0
                },
                'confidence': 0.5,  # Medium confidence for system behavior
                'evidence_count': 1
            })
            
            return knowledge_entries
            
        except Exception:
            return []
    
    async def _update_knowledge_entry(self, entry_data: Dict[str, Any]) -> None:
        """Update or create knowledge entry"""
        try:
            with self.lock:
                entry_id = self._generate_entry_id(entry_data['knowledge_type'], entry_data['subject'])
                
                with sqlite3.connect(str(self.knowledge_db_path)) as conn:
                    # Check if entry exists
                    cursor = conn.execute(
                        'SELECT evidence_count, confidence FROM knowledge_entries WHERE entry_id = ?',
                        (entry_id,)
                    )
                    existing = cursor.fetchone()
                    
                    if existing:
                        # Update existing entry
                        old_evidence_count, old_confidence = existing
                        new_evidence_count = old_evidence_count + entry_data['evidence_count']
                        
                        # Update confidence (weighted average)
                        new_confidence = (
                            (old_confidence * old_evidence_count + 
                             entry_data['confidence'] * entry_data['evidence_count']) / 
                            new_evidence_count
                        )
                        
                        conn.execute('''
                            UPDATE knowledge_entries 
                            SET content = ?, confidence = ?, evidence_count = ?, updated_at = ?
                            WHERE entry_id = ?
                        ''', (
                            json.dumps(entry_data['content']),
                            new_confidence,
                            new_evidence_count,
                            datetime.utcnow().isoformat(),
                            entry_id
                        ))
                    else:
                        # Create new entry
                        conn.execute('''
                            INSERT INTO knowledge_entries 
                            (entry_id, knowledge_type, subject, content, confidence, evidence_count, created_at, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            entry_id,
                            entry_data['knowledge_type'],
                            entry_data['subject'],
                            json.dumps(entry_data['content']),
                            entry_data['confidence'],
                            entry_data['evidence_count'],
                            datetime.utcnow().isoformat(),
                            datetime.utcnow().isoformat()
                        ))
                        
        except Exception as e:
            self.logger.warning(f"Failed to update knowledge entry: {e}")
    
    def _generate_entry_id(self, knowledge_type: str, subject: str) -> str:
        """Generate unique entry ID"""
        id_text = f"{knowledge_type}:{subject}"
        return hashlib.sha256(id_text.encode()).hexdigest()[:32]
    
    def _is_update_safe(self) -> bool:
        """Check if knowledge updates are safe"""
        try:
            return self.storage_path.exists() and os.access(str(self.storage_path), os.W_OK)
        except Exception:
            return False
    
    def close(self) -> None:
        """Close knowledge base and cleanup resources"""
        try:
            # No specific cleanup needed for SQLite
            pass
        except Exception:
            pass