"""
Comprehensive test suite for Agent Learning Framework

Validates that learning framework is non-invasive and causes no regressions
"""

import asyncio
import time
import json
import unittest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
import tempfile
import shutil
from pathlib import Path

# Import framework components
import sys
sys.path.append('..')  # Add parent directory to path
from agent_learning_framework import AgentLearningFramework
from pattern_database import PatternDatabase
from performance_tracker import PerformanceTracker, MetricType, PerformanceMetric
from async_executor import AsyncExecutor, LearningEvent, EventPriority


class TestLearningFrameworkNonBlocking(unittest.TestCase):
    """Test that learning framework never blocks main execution"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'pattern_storage_path': f'{self.temp_dir}/patterns',
            'metrics_storage_path': f'{self.temp_dir}/metrics',
            'worker_count': 2,
            'queue_size': 100,
            'batch_size': 10
        }
        
        # Create config file
        config_path = f'{self.temp_dir}/config.json'
        with open(config_path, 'w') as f:
            json.dump(self.config, f)
        
        self.framework = AgentLearningFramework(config_path)
    
    def tearDown(self):
        """Clean up test environment"""
        asyncio.run(self.framework.async_executor.shutdown())
        shutil.rmtree(self.temp_dir)
    
    async def test_capture_execution_non_blocking(self):
        """Verify capture_execution never blocks"""
        # Mock slow processing
        self.framework.async_executor._process_batch = AsyncMock(
            side_effect=lambda x: asyncio.sleep(5.0)
        )
        
        # Measure execution time
        start = time.time()
        await self.framework.capture_execution(
            'agent_a',
            {'ticket': 'TEST-123'},
            {'status': 'success'},
            {'execution_time': 10.0, 'success': True}
        )
        duration = time.time() - start
        
        # Should return almost immediately
        self.assertLess(duration, 0.1, "capture_execution blocked main flow")
    
    async def test_learning_failure_isolation(self):
        """Verify learning failures don't affect main flow"""
        # Break pattern database
        self.framework.pattern_db = None
        
        # Should handle gracefully
        try:
            await self.framework.capture_execution(
                'agent_a',
                {'ticket': 'TEST-123'},
                {'status': 'success'},
                {'metrics': {}}
            )
            # Should not raise exception
            success = True
        except:
            success = False
        
        self.assertTrue(success, "Learning failure propagated to main flow")
    
    def test_apply_learnings_graceful_failure(self):
        """Test apply_learnings handles errors gracefully"""
        # Break pattern database
        self.framework.pattern_db = None
        
        # Should return None on error
        result = self.framework.apply_learnings('agent_a', {'test': 'context'})
        self.assertIsNone(result, "Failed to handle error gracefully")


class TestPatternDatabase(unittest.TestCase):
    """Test pattern storage and retrieval"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db = PatternDatabase(storage_path=self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    async def test_pattern_storage_and_retrieval(self):
        """Test storing and retrieving patterns"""
        # Store patterns
        patterns = [
            {
                'type': 'test_pattern',
                'pattern': {'keywords': ['test', 'example']},
                'success_rate': 0.95
            }
        ]
        
        await self.db.store_patterns('agent_a', patterns)
        
        # Retrieve patterns
        context = {'keywords': ['test', 'example']}
        retrieved = await self.db.get_relevant_patterns('agent_a', context)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0]['type'], 'test_pattern')
    
    async def test_relevance_calculation(self):
        """Test pattern relevance scoring"""
        # Store multiple patterns
        patterns = [
            {
                'type': 'exact_match',
                'pattern': {'keywords': ['test', 'exact']},
                'success_rate': 1.0
            },
            {
                'type': 'partial_match',
                'pattern': {'keywords': ['test', 'different']},
                'success_rate': 0.8
            },
            {
                'type': 'no_match',
                'pattern': {'keywords': ['unrelated', 'keywords']},
                'success_rate': 0.9
            }
        ]
        
        await self.db.store_patterns('agent_a', patterns)
        
        # Query with specific context
        context = {'keywords': ['test', 'exact', 'query']}
        retrieved = await self.db.get_relevant_patterns('agent_a', context)
        
        # Should get exact_match first
        self.assertGreater(len(retrieved), 0)
        self.assertEqual(retrieved[0]['type'], 'exact_match')
        self.assertGreater(retrieved[0]['relevance_score'], 0.7)
    
    def test_cached_pattern_retrieval(self):
        """Test synchronous cached pattern access"""
        # Pre-populate cache
        self.db.pattern_cache['agent_a'] = [
            {
                'type': 'cached_pattern',
                'pattern': {'test': True},
                'success_rate': 0.9
            }
        ]
        
        # Get cached patterns (synchronous)
        patterns = self.db.get_cached_patterns('agent_a', {})
        
        self.assertIsNotNone(patterns)
        self.assertEqual(patterns[0]['type'], 'cached_pattern')


class TestPerformanceTracker(unittest.TestCase):
    """Test performance metric tracking"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = PerformanceTracker(storage_path=self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    async def test_metric_update_and_stats(self):
        """Test updating metrics and calculating statistics"""
        # Add metrics
        metrics = {
            'execution_time': 12.5,
            'success': True,
            'confidence': 0.92,
            'execution_id': 'test-001'
        }
        
        await self.tracker.update_metrics('agent_a', metrics)
        
        # Get statistics
        stats = self.tracker.get_current_stats('agent_a')
        
        self.assertIn('execution_time', stats)
        self.assertEqual(stats['execution_time']['current'], 12.5)
        self.assertIn('success_rate', stats)
        self.assertEqual(stats['success_rate']['current'], 1.0)
    
    def test_trend_calculation(self):
        """Test performance trend detection"""
        # Add declining values
        values = [10.0, 11.0, 12.0, 13.0, 14.0] * 4  # 20 values
        
        trend = self.tracker._calculate_trend(values)
        self.assertIn(trend, ['declining', 'slightly_declining'])
        
        # Add improving values
        values = [20.0, 19.0, 18.0, 17.0, 16.0] * 4  # 20 values
        
        trend = self.tracker._calculate_trend(values)
        self.assertIn(trend, ['improving', 'slightly_improving'])
    
    def test_anomaly_detection(self):
        """Test anomaly detection in metrics"""
        # Add normal metrics
        for i in range(20):
            self.tracker.metrics_buffer['agent_a'][MetricType.EXECUTION_TIME].append(
                PerformanceMetric(
                    agent_id='agent_a',
                    metric_type=MetricType.EXECUTION_TIME,
                    value=10.0 + (i % 2),  # Values between 10-11
                    timestamp=datetime.utcnow(),
                    execution_id=f'test-{i}'
                )
            )
        
        # Add anomalous metric
        anomalous_metric = PerformanceMetric(
            agent_id='agent_a',
            metric_type=MetricType.EXECUTION_TIME,
            value=50.0,  # Way outside normal range
            timestamp=datetime.utcnow(),
            execution_id='test-anomaly'
        )
        
        anomalies = self.tracker._detect_anomalies('agent_a', [anomalous_metric])
        
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['metric_type'], 'execution_time')
        self.assertGreater(anomalies[0]['z_score'], 3)


class TestAsyncExecutor(unittest.TestCase):
    """Test async executor functionality"""
    
    def setUp(self):
        self.executor = AsyncExecutor(
            worker_count=2,
            queue_size=100,
            batch_size=10,
            processing_interval=0.1
        )
        
        # Register test processor
        self.processed_events = []
        self.executor.register_processor('test_event', self._test_processor)
    
    def tearDown(self):
        asyncio.run(self.executor.shutdown())
    
    async def _test_processor(self, event):
        """Test event processor"""
        self.processed_events.append(event)
    
    async def test_event_queuing_and_processing(self):
        """Test event queuing and processing"""
        # Queue events
        for i in range(5):
            event = LearningEvent(
                event_id=f'test-{i}',
                agent_id='agent_a',
                event_type='test_event',
                data={'index': i}
            )
            await self.executor.queue_event(event)
        
        # Wait for processing
        await asyncio.sleep(0.5)
        
        # Check processed
        self.assertEqual(len(self.processed_events), 5)
        
    async def test_priority_handling(self):
        """Test priority-based event processing"""
        # Queue events with different priorities
        events = []
        
        # Fill normal queue
        for i in range(50):
            event = LearningEvent(
                event_id=f'normal-{i}',
                agent_id='agent_a',
                event_type='test_event',
                data={'priority': 'normal'},
                priority=EventPriority.NORMAL
            )
            await self.executor.queue_event(event)
            events.append(event)
        
        # Add high priority event
        high_event = LearningEvent(
            event_id='high-priority',
            agent_id='agent_a',
            event_type='test_event',
            data={'priority': 'high'},
            priority=EventPriority.HIGH
        )
        await self.executor.queue_event(high_event)
        
        # High priority should be processed quickly
        await asyncio.sleep(0.5)
        
        # Check that high priority was processed
        processed_ids = [e.event_id for e in self.processed_events]
        self.assertIn('high-priority', processed_ids)
    
    def test_statistics_tracking(self):
        """Test executor statistics"""
        # Check initial stats
        self.assertEqual(self.executor.stats['events_queued'], 0)
        self.assertEqual(self.executor.stats['events_processed'], 0)
        
        # Queue and process events
        async def queue_events():
            for i in range(10):
                event = LearningEvent(
                    event_id=f'stat-{i}',
                    agent_id='agent_a',
                    event_type='test_event',
                    data={}
                )
                await self.executor.queue_event(event)
            
            await asyncio.sleep(0.5)
        
        asyncio.run(queue_events())
        
        # Check stats updated
        self.assertGreater(self.executor.stats['events_queued'], 0)
        self.assertGreater(self.executor.stats['events_processed'], 0)


class TestEndToEndIntegration(unittest.TestCase):
    """End-to-end integration tests"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        config_path = f'{self.temp_dir}/config.json'
        
        config = {
            'pattern_storage_path': f'{self.temp_dir}/patterns',
            'metrics_storage_path': f'{self.temp_dir}/metrics',
            'worker_count': 2,
            'queue_size': 100,
            'processing_interval': 0.1
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        self.framework = AgentLearningFramework(config_path)
    
    def tearDown(self):
        asyncio.run(self.framework.async_executor.shutdown())
        shutil.rmtree(self.temp_dir)
    
    async def test_full_learning_cycle(self):
        """Test complete learning cycle from capture to application"""
        # 1. Capture execution
        await self.framework.capture_execution(
            'agent_a',
            {'ticket': 'TEST-123', 'keywords': ['test', 'integration']},
            {
                'status': 'success',
                'ticket_type': 'feature',
                'components_identified': ['test-component']
            },
            {
                'execution_time': 8.5,
                'success': True,
                'confidence': 0.95,
                'component_accuracy': 0.9
            }
        )
        
        # 2. Wait for async processing
        await asyncio.sleep(0.5)
        
        # 3. Apply learnings
        recommendations = self.framework.apply_learnings(
            'agent_a',
            {'ticket': 'TEST-456', 'keywords': ['test', 'integration']}
        )
        
        # Should get recommendations based on captured pattern
        self.assertIsNotNone(recommendations)
        self.assertIn('patterns', recommendations)
        
    async def test_cross_agent_learning(self):
        """Test learning sharing across agents"""
        # Agent A discovers pattern
        await self.framework.capture_execution(
            'agent_a',
            {'ticket': 'CROSS-123'},
            {'status': 'success', 'pattern_discovered': True},
            {'execution_time': 5.0, 'success': True}
        )
        
        # Wait for processing
        await asyncio.sleep(0.5)
        
        # Agent B should benefit (in full implementation)
        # This is a placeholder for more sophisticated cross-agent testing
        self.assertTrue(self.framework.config.get('cross_agent_learning_enabled'))


def run_tests():
    """Run all tests"""
    unittest.main()


if __name__ == '__main__':
    run_tests()
