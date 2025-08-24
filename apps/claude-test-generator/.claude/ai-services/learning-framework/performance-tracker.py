"""
Performance Tracker for Agent Learning Framework

Tracks execution metrics, success rates, and performance trends for continuous improvement.
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Dict, List, Optional, Tuple
import statistics
import aiofiles
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics we track"""
    EXECUTION_TIME = "execution_time"
    SUCCESS_RATE = "success_rate"
    CONFIDENCE_SCORE = "confidence_score"
    ERROR_RATE = "error_rate"
    RESOURCE_USAGE = "resource_usage"
    QUALITY_SCORE = "quality_score"


@dataclass
class PerformanceMetric:
    """Single performance metric data point"""
    agent_id: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    execution_id: str
    metadata: Dict = None

    def to_dict(self):
        data = asdict(self)
        data['metric_type'] = self.metric_type.value
        data['timestamp'] = self.timestamp.isoformat()
        return data


class PerformanceTracker:
    """
    Tracks and analyzes agent performance metrics over time
    """
    
    def __init__(self, storage_path: str = ".claude/learning-data/metrics"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory metrics storage (agent_id -> metric_type -> deque of metrics)
        self.metrics_buffer = defaultdict(lambda: defaultdict(lambda: deque(maxlen=1000)))
        
        # Aggregated statistics cache
        self.stats_cache = defaultdict(dict)
        self.cache_validity = 300  # 5 minutes
        self.last_cache_update = defaultdict(float)
        
        # Performance baselines for comparison
        self.baselines = self._load_baselines()
        
        # Load historical metrics
        self._load_metrics()
    
    def _load_baselines(self) -> Dict:
        """Load performance baselines"""
        return {
            'agent_a': {
                MetricType.EXECUTION_TIME: 15.0,  # seconds
                MetricType.SUCCESS_RATE: 0.95,
                MetricType.CONFIDENCE_SCORE: 0.90
            },
            'agent_b': {
                MetricType.EXECUTION_TIME: 20.0,
                MetricType.SUCCESS_RATE: 0.93,
                MetricType.CONFIDENCE_SCORE: 0.88
            },
            'agent_c': {
                MetricType.EXECUTION_TIME: 25.0,
                MetricType.SUCCESS_RATE: 0.92,
                MetricType.CONFIDENCE_SCORE: 0.87
            },
            'agent_d': {
                MetricType.EXECUTION_TIME: 10.0,
                MetricType.SUCCESS_RATE: 0.96,
                MetricType.CONFIDENCE_SCORE: 0.92
            }
        }
    
    def _load_metrics(self):
        """Load recent metrics from disk"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(days=7)  # Last 7 days
            
            for metric_file in self.storage_path.glob("*_metrics.json"):
                with open(metric_file, 'r') as f:
                    data = json.load(f)
                    
                    for metric_data in data.get('metrics', []):
                        metric = PerformanceMetric(
                            agent_id=metric_data['agent_id'],
                            metric_type=MetricType(metric_data['metric_type']),
                            value=metric_data['value'],
                            timestamp=datetime.fromisoformat(metric_data['timestamp']),
                            execution_id=metric_data['execution_id'],
                            metadata=metric_data.get('metadata', {})
                        )
                        
                        # Only load recent metrics
                        if metric.timestamp > cutoff_time:
                            self.metrics_buffer[metric.agent_id][metric.metric_type].append(metric)
            
            logger.info(f"Loaded metrics for {len(self.metrics_buffer)} agents")
            
        except Exception as e:
            logger.warning(f"Could not load historical metrics: {e}")
    
    async def update_metrics(self, agent_id: str, metrics: Dict):
        """
        Update performance metrics for an agent
        
        Args:
            agent_id: Agent identifier
            metrics: Dictionary of metric values
        """
        try:
            timestamp = datetime.utcnow()
            execution_id = metrics.get('execution_id', str(time.time()))
            
            # Process each metric
            metric_objects = []
            
            # Execution time
            if 'execution_time' in metrics:
                metric_objects.append(PerformanceMetric(
                    agent_id=agent_id,
                    metric_type=MetricType.EXECUTION_TIME,
                    value=metrics['execution_time'],
                    timestamp=timestamp,
                    execution_id=execution_id
                ))
            
            # Success/failure
            if 'success' in metrics:
                metric_objects.append(PerformanceMetric(
                    agent_id=agent_id,
                    metric_type=MetricType.SUCCESS_RATE,
                    value=1.0 if metrics['success'] else 0.0,
                    timestamp=timestamp,
                    execution_id=execution_id
                ))
            
            # Confidence score
            if 'confidence' in metrics:
                metric_objects.append(PerformanceMetric(
                    agent_id=agent_id,
                    metric_type=MetricType.CONFIDENCE_SCORE,
                    value=metrics['confidence'],
                    timestamp=timestamp,
                    execution_id=execution_id
                ))
            
            # Quality score (if provided)
            if 'quality_score' in metrics:
                metric_objects.append(PerformanceMetric(
                    agent_id=agent_id,
                    metric_type=MetricType.QUALITY_SCORE,
                    value=metrics['quality_score'],
                    timestamp=timestamp,
                    execution_id=execution_id
                ))
            
            # Add to buffer
            for metric in metric_objects:
                self.metrics_buffer[agent_id][metric.metric_type].append(metric)
            
            # Invalidate cache for this agent
            self.last_cache_update[agent_id] = 0
            
            # Persist asynchronously
            await self._persist_metrics(agent_id, metric_objects)
            
            # Check for anomalies
            anomalies = self._detect_anomalies(agent_id, metric_objects)
            if anomalies:
                logger.warning(f"Performance anomalies detected for {agent_id}: {anomalies}")
            
        except Exception as e:
            logger.error(f"Failed to update metrics: {e}")
    
    def get_current_stats(self, agent_id: str) -> Dict:
        """
        Get current performance statistics for an agent
        
        Returns cached stats if available, otherwise calculates fresh
        """
        # Check cache validity
        if (time.time() - self.last_cache_update[agent_id]) < self.cache_validity:
            if agent_id in self.stats_cache:
                return self.stats_cache[agent_id]
        
        # Calculate fresh statistics
        stats = self._calculate_statistics(agent_id)
        
        # Update cache
        self.stats_cache[agent_id] = stats
        self.last_cache_update[agent_id] = time.time()
        
        return stats
    
    def _calculate_statistics(self, agent_id: str) -> Dict:
        """Calculate current statistics for an agent"""
        stats = {
            'agent_id': agent_id,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Calculate for each metric type
        for metric_type in MetricType:
            metrics = list(self.metrics_buffer[agent_id][metric_type])
            
            if not metrics:
                continue
            
            values = [m.value for m in metrics]
            recent_values = [m.value for m in metrics[-100:]]  # Last 100
            
            metric_stats = {
                'current': values[-1] if values else None,
                'mean': statistics.mean(values),
                'median': statistics.median(values),
                'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
                'trend': self._calculate_trend(values),
                'recent_mean': statistics.mean(recent_values),
                'improvement': self._calculate_improvement(agent_id, metric_type, recent_values)
            }
            
            stats[metric_type.value] = metric_stats
        
        # Overall health score
        stats['health_score'] = self._calculate_health_score(agent_id, stats)
        
        return stats
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 10:
            return "insufficient_data"
        
        # Simple linear regression on last 20 values
        recent = values[-20:]
        x = list(range(len(recent)))
        
        # Calculate slope
        n = len(recent)
        if n == 0:
            return "no_data"
        
        sum_x = sum(x)
        sum_y = sum(recent)
        sum_xy = sum(x[i] * recent[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        denominator = (n * sum_x2 - sum_x ** 2)
        if denominator == 0:
            return "stable"
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        
        # Determine trend
        if abs(slope) < 0.01:
            return "stable"
        elif slope > 0:
            return "improving" if slope > 0.05 else "slightly_improving"
        else:
            return "declining" if slope < -0.05 else "slightly_declining"
    
    def _calculate_improvement(self, agent_id: str, metric_type: MetricType, 
                              recent_values: List[float]) -> float:
        """Calculate improvement percentage compared to baseline"""
        if not recent_values:
            return 0.0
        
        baseline = self.baselines.get(agent_id, {}).get(metric_type)
        if not baseline:
            return 0.0
        
        current = statistics.mean(recent_values)
        
        # For execution time, lower is better
        if metric_type == MetricType.EXECUTION_TIME:
            improvement = (baseline - current) / baseline * 100
        else:
            # For other metrics, higher is better
            improvement = (current - baseline) / baseline * 100
        
        return round(improvement, 2)
    
    def _calculate_health_score(self, agent_id: str, stats: Dict) -> float:
        """Calculate overall health score for agent"""
        score = 0.0
        weights = {
            MetricType.SUCCESS_RATE.value: 0.4,
            MetricType.EXECUTION_TIME.value: 0.3,
            MetricType.CONFIDENCE_SCORE.value: 0.2,
            MetricType.QUALITY_SCORE.value: 0.1
        }
        
        total_weight = 0.0
        
        for metric_type, weight in weights.items():
            if metric_type in stats:
                metric_data = stats[metric_type]
                improvement = metric_data.get('improvement', 0)
                
                # Convert improvement to 0-1 scale
                metric_score = min(max((improvement + 100) / 200, 0), 1)
                
                score += metric_score * weight
                total_weight += weight
        
        if total_weight > 0:
            score = score / total_weight
        
        return round(score, 3)
    
    def _detect_anomalies(self, agent_id: str, new_metrics: List[PerformanceMetric]) -> List[Dict]:
        """Detect performance anomalies"""
        anomalies = []
        
        for metric in new_metrics:
            buffer = self.metrics_buffer[agent_id][metric.metric_type]
            
            if len(buffer) < 20:  # Need sufficient history
                continue
            
            # Calculate statistics for anomaly detection
            values = [m.value for m in list(buffer)[-50:-1]]  # Exclude current
            mean = statistics.mean(values)
            std_dev = statistics.stdev(values) if len(values) > 1 else 0
            
            # Check if current value is anomalous (3 sigma rule)
            if std_dev > 0:
                z_score = abs(metric.value - mean) / std_dev
                
                if z_score > 3:
                    anomalies.append({
                        'metric_type': metric.metric_type.value,
                        'value': metric.value,
                        'expected_range': (mean - 3*std_dev, mean + 3*std_dev),
                        'z_score': z_score,
                        'severity': 'high' if z_score > 4 else 'medium'
                    })
        
        return anomalies
    
    async def _persist_metrics(self, agent_id: str, metrics: List[PerformanceMetric]):
        """Persist metrics to disk"""
        try:
            # Prepare daily file
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            file_path = self.storage_path / f"{agent_id}_{date_str}_metrics.json"
            
            # Load existing data or create new
            existing_data = {'metrics': []}
            if file_path.exists():
                async with aiofiles.open(file_path, 'r') as f:
                    content = await f.read()
                    existing_data = json.loads(content)
            
            # Append new metrics
            for metric in metrics:
                existing_data['metrics'].append(metric.to_dict())
            
            # Write back
            async with aiofiles.open(file_path, 'w') as f:
                await f.write(json.dumps(existing_data, indent=2))
                
        except Exception as e:
            logger.error(f"Failed to persist metrics: {e}")
    
    def get_performance_report(self, agent_id: str, days: int = 7) -> Dict:
        """Generate comprehensive performance report"""
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        
        report = {
            'agent_id': agent_id,
            'period': f"Last {days} days",
            'generated_at': datetime.utcnow().isoformat(),
            'summary': self.get_current_stats(agent_id),
            'metrics': {}
        }
        
        # Detailed metrics analysis
        for metric_type in MetricType:
            metrics = [
                m for m in self.metrics_buffer[agent_id][metric_type]
                if m.timestamp > cutoff_time
            ]
            
            if not metrics:
                continue
            
            values = [m.value for m in metrics]
            
            report['metrics'][metric_type.value] = {
                'total_measurements': len(metrics),
                'min': min(values),
                'max': max(values),
                'mean': statistics.mean(values),
                'median': statistics.median(values),
                'percentiles': {
                    '25th': statistics.quantiles(values, n=4)[0] if len(values) > 3 else None,
                    '75th': statistics.quantiles(values, n=4)[2] if len(values) > 3 else None,
                    '95th': statistics.quantiles(values, n=20)[18] if len(values) > 19 else None
                }
            }
        
        return report
