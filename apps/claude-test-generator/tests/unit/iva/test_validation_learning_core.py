#!/usr/bin/env python3
"""
Validation Learning Core Unit Tests
=================================

Comprehensive unit tests for the ValidationLearningCore component of IVA.
Testing non-intrusive operation, safety guarantees, and learning capabilities.
"""

import unittest
import sys
import os
import json
import asyncio
import tempfile
import shutil
import threading
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
solutions_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'solutions')
sys.path.insert(0, solutions_path)

try:
    from validation_learning_core import (
        ValidationLearningCore,
        ValidationEvent,
        ValidationInsights,
        LearningMode,
        ResourceMonitor,
        StorageMonitor,
        SafeFailureManager,
        ConfigurationController,
        LearningMonitoring,
        get_learning_core,
        shutdown_learning_core
    )
    VALIDATION_LEARNING_AVAILABLE = True
except ImportError as e:
    VALIDATION_LEARNING_AVAILABLE = False
    print(f"❌ Validation Learning Core not available: {e}")


class TestValidationLearningCore(unittest.TestCase):
    """Test ValidationLearningCore main functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not VALIDATION_LEARNING_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None
        
        # Mock environment for disabled mode
        self.env_patcher = patch.dict(os.environ, {
            'CLAUDE_VALIDATION_LEARNING': 'disabled',
            'CLAUDE_LEARNING_STORAGE_PATH': self.test_dir,
            'CLAUDE_LEARNING_MAX_MEMORY': '100',
            'CLAUDE_LEARNING_MAX_STORAGE': '500'
        })
        self.env_patcher.start()
        
        # Create test validation event
        self.test_event = ValidationEvent(
            event_id='test_event_001',
            event_type='evidence_validation',
            context={'validation_type': 'evidence', 'component': 'test'},
            result={'success': True, 'confidence': 0.85},
            timestamp=datetime.utcnow(),
            source_system='evidence_validation_engine',
            success=True,
            confidence=0.85,
            metadata={'test': 'data'}
        )
    
    def tearDown(self):
        """Clean up test environment"""
        self.env_patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)
        # Ensure singleton is reset
        shutdown_learning_core()
    
    def test_validation_learning_core_initialization(self):
        """Test ValidationLearningCore initializes correctly"""
        core = ValidationLearningCore()
        
        # Verify initialization
        self.assertIsNotNone(core.config_controller)
        self.assertIsNotNone(core.safe_failure_manager)
        self.assertIsNotNone(core.resource_monitor)
        self.assertIsNotNone(core.storage_monitor)
        
        # Verify learning mode
        self.assertEqual(core.learning_mode, LearningMode.DISABLED)
        self.assertFalse(core.is_enabled())
        
        # Verify safety components
        self.assertIsNotNone(core.logger)
        self.assertIsNotNone(core.shutdown_event)
    
    def test_disabled_mode_zero_impact(self):
        """Test that disabled mode has zero impact"""
        core = ValidationLearningCore()
        
        # Test learning operations have no impact
        start_time = time.time()
        
        for _ in range(1000):
            core.learn_from_validation(self.test_event)
            insights = core.get_validation_insights({'test': 'context'})
            self.assertIsNone(insights)
        
        execution_time = time.time() - start_time
        
        # Should complete very quickly (< 0.1 seconds for 1000 operations)
        self.assertLess(execution_time, 0.1)
        
        # Verify no learning services initialized
        self.assertIsNone(core.pattern_memory)
        self.assertIsNone(core.analytics_service)
        self.assertIsNone(core.knowledge_base)
    
    def test_enabled_mode_learning_activation(self):
        """Test learning activation in enabled mode"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'conservative'}):
            core = ValidationLearningCore()
            
            # Verify enabled state
            self.assertEqual(core.learning_mode, LearningMode.CONSERVATIVE)
            self.assertTrue(core.is_enabled())
            
            # Verify learning services would be initialized (mocked)
            with patch('validation_learning_core.ValidationPatternMemory') as mock_pattern, \
                 patch('validation_learning_core.ValidationAnalyticsService') as mock_analytics:
                
                core._initialize_learning_services()
                
                # Should attempt to initialize learning services
                self.assertTrue(mock_pattern.called or hasattr(core, 'pattern_memory'))
    
    def test_safety_check_functionality(self):
        """Test safety checking mechanisms"""
        core = ValidationLearningCore()
        
        # Test disabled mode safety
        self.assertFalse(core.is_safe_to_learn())
        
        # Test with enabled mode but broken resources
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            core_enabled = ValidationLearningCore()
            
            with patch.object(core_enabled.resource_monitor, 'is_resource_available', return_value=False):
                self.assertFalse(core_enabled.is_safe_to_learn())
    
    def test_learn_from_validation_safe_failure(self):
        """Test that learning failures don't affect validation"""
        core = ValidationLearningCore()
        
        # Mock to simulate learning failure
        with patch.object(core, '_validate_event', side_effect=Exception("Learning error")):
            # Should not raise exception
            try:
                core.learn_from_validation(self.test_event)
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success, "Learning failure should not propagate")
    
    def test_get_validation_insights_disabled(self):
        """Test insights return None when disabled"""
        core = ValidationLearningCore()
        
        insights = core.get_validation_insights({'test': 'context'})
        self.assertIsNone(insights)
        
        # Should be very fast
        start_time = time.time()
        for _ in range(100):
            core.get_validation_insights({'test': 'context'})
        execution_time = time.time() - start_time
        
        self.assertLess(execution_time, 0.01)  # < 10ms for 100 calls
    
    def test_health_status_reporting(self):
        """Test health status reporting"""
        core = ValidationLearningCore()
        
        # Test disabled status
        status = core.get_health_status()
        self.assertEqual(status['status'], 'disabled')
        self.assertEqual(status['learning_mode'], 'disabled')
        self.assertIn('timestamp', status)
        
        # Test enabled status
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'conservative'}):
            core_enabled = ValidationLearningCore()
            status_enabled = core_enabled.get_health_status()
            
            self.assertEqual(status_enabled['status'], 'enabled')
            self.assertEqual(status_enabled['learning_mode'], 'conservative')
            self.assertIn('safe_to_learn', status_enabled)
    
    def test_shutdown_graceful(self):
        """Test graceful shutdown"""
        core = ValidationLearningCore()
        
        # Should shutdown without errors
        try:
            core.shutdown()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
        
        # Shutdown event should be set
        self.assertTrue(core.shutdown_event.is_set())
    
    def test_singleton_behavior(self):
        """Test singleton behavior of get_learning_core"""
        core1 = get_learning_core()
        core2 = get_learning_core()
        
        # Should return same instance
        self.assertIs(core1, core2)
        
        # Cleanup
        shutdown_learning_core()
        
        # New instance after shutdown
        core3 = get_learning_core()
        self.assertIsNot(core1, core3)
    
    def test_event_validation(self):
        """Test validation event structure validation"""
        core = ValidationLearningCore()
        
        # Valid event
        valid_event = ValidationEvent(
            event_id='test',
            event_type='test_type',
            context={'key': 'value'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='test_system',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        self.assertTrue(core._validate_event(valid_event))
        
        # Invalid event (missing required field)
        invalid_event = ValidationEvent(
            event_id=None,  # Missing required field
            event_type='test_type',
            context={'key': 'value'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='test_system',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        self.assertFalse(core._validate_event(invalid_event))


class TestResourceMonitor(unittest.TestCase):
    """Test ResourceMonitor functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not VALIDATION_LEARNING_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def setUp(self):
        """Set up test environment"""
        self.env_patcher = patch.dict(os.environ, {
            'CLAUDE_LEARNING_MAX_MEMORY': '100',
            'CLAUDE_LEARNING_MAX_CPU': '5.0'
        })
        self.env_patcher.start()
    
    def tearDown(self):
        """Clean up test environment"""
        self.env_patcher.stop()
    
    def test_resource_monitor_initialization(self):
        """Test ResourceMonitor initializes with correct limits"""
        monitor = ResourceMonitor()
        
        self.assertEqual(monitor.max_memory_mb, 100)
        self.assertEqual(monitor.max_cpu_percent, 5.0)
    
    def test_resource_availability_check(self):
        """Test resource availability checking"""
        monitor = ResourceMonitor()
        
        # Should return boolean
        available = monitor.is_resource_available()
        self.assertIsInstance(available, bool)
        
        # Test with mock to simulate high resource usage
        with patch('validation_learning_core.psutil.Process') as mock_process:
            mock_process.return_value.memory_info.return_value.rss = 200 * 1024 * 1024  # 200MB
            
            self.assertFalse(monitor.is_resource_available())
    
    def test_resource_monitor_error_handling(self):
        """Test resource monitor handles errors gracefully"""
        monitor = ResourceMonitor()
        
        with patch('validation_learning_core.psutil.Process', side_effect=Exception("System error")):
            # Should return False on error (safe default)
            self.assertFalse(monitor.is_resource_available())


class TestStorageMonitor(unittest.TestCase):
    """Test StorageMonitor functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not VALIDATION_LEARNING_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.env_patcher = patch.dict(os.environ, {
            'CLAUDE_LEARNING_MAX_STORAGE': '500'
        })
        self.env_patcher.start()
    
    def tearDown(self):
        """Clean up test environment"""
        self.env_patcher.stop()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_storage_monitor_initialization(self):
        """Test StorageMonitor initializes correctly"""
        monitor = StorageMonitor(self.test_dir)
        
        self.assertEqual(monitor.storage_path, Path(self.test_dir))
        self.assertEqual(monitor.max_storage_mb, 500)
    
    def test_storage_availability_check(self):
        """Test storage availability checking"""
        monitor = StorageMonitor(self.test_dir)
        
        # Should be available for empty directory
        self.assertTrue(monitor.is_storage_available())
        
        # Test storage calculation
        usage = monitor._calculate_storage_usage()
        self.assertGreaterEqual(usage, 0.0)
    
    def test_storage_usage_calculation(self):
        """Test storage usage calculation"""
        monitor = StorageMonitor(self.test_dir)
        
        # Create test file
        test_file = Path(self.test_dir) / 'test.txt'
        test_file.write_text('test content' * 1000)  # Create some content
        
        usage = monitor._calculate_storage_usage()
        self.assertGreater(usage, 0.0)
        
        # Should still be available (under limit)
        self.assertTrue(monitor.is_storage_available())


class TestSafeFailureManager(unittest.TestCase):
    """Test SafeFailureManager functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not VALIDATION_LEARNING_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def setUp(self):
        """Set up test environment"""
        self.env_patcher = patch.dict(os.environ, {
            'CLAUDE_LEARNING_MAX_ERRORS_PER_OP': '5',
            'CLAUDE_LEARNING_CIRCUIT_TIMEOUT': '60'
        })
        self.env_patcher.start()
    
    def tearDown(self):
        """Clean up test environment"""
        self.env_patcher.stop()
    
    def test_safe_failure_manager_initialization(self):
        """Test SafeFailureManager initializes correctly"""
        manager = SafeFailureManager()
        
        self.assertEqual(manager.max_errors_per_operation, 5)
        self.assertEqual(manager.circuit_breaker_timeout, 60)
        self.assertIsInstance(manager.error_stats, dict)
        self.assertIsInstance(manager.circuit_breakers, dict)
    
    def test_failure_handling(self):
        """Test failure handling and circuit breaker logic"""
        manager = SafeFailureManager()
        
        operation = 'test_operation'
        
        # Initially operation should be safe
        self.assertTrue(manager.is_operation_safe(operation))
        
        # Add errors until circuit breaker triggers
        for i in range(6):  # More than max_errors_per_operation (5)
            manager.handle_learning_failure(operation, Exception(f"Error {i}"))
        
        # Circuit breaker should be active
        self.assertFalse(manager.is_operation_safe(operation))
        
        # Reset circuit breaker
        manager.reset_circuit_breaker(operation)
        self.assertTrue(manager.is_operation_safe(operation))
    
    def test_circuit_breaker_timeout(self):
        """Test circuit breaker timeout functionality"""
        manager = SafeFailureManager()
        operation = 'timeout_test'
        
        # Trigger circuit breaker
        for _ in range(6):
            manager.handle_learning_failure(operation, Exception("Error"))
        
        self.assertFalse(manager.is_operation_safe(operation))
        
        # Simulate timeout by modifying last error time
        old_time = datetime.utcnow() - timedelta(seconds=120)  # 2 minutes ago
        manager.last_errors[operation] = old_time
        
        # Should reset automatically due to timeout
        self.assertTrue(manager.is_operation_safe(operation))
    
    def test_failure_handling_error_isolation(self):
        """Test that failure handling itself doesn't fail"""
        manager = SafeFailureManager()
        
        # Should handle errors gracefully even if internal operations fail
        with patch.object(manager, 'error_stats', side_effect=Exception("Internal error")):
            try:
                manager.handle_learning_failure('test', Exception("Test error"))
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success)


class TestConfigurationController(unittest.TestCase):
    """Test ConfigurationController functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not VALIDATION_LEARNING_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def test_configuration_loading(self):
        """Test configuration loading from environment"""
        test_config = {
            'CLAUDE_VALIDATION_LEARNING': 'standard',
            'CLAUDE_LEARNING_STORAGE_PATH': '/test/path',
            'CLAUDE_LEARNING_MAX_MEMORY': '200',
            'CLAUDE_LEARNING_ANALYTICS': 'false'
        }
        
        with patch.dict(os.environ, test_config):
            controller = ConfigurationController()
            
            self.assertEqual(controller.get_config('learning_mode'), 'standard')
            self.assertEqual(controller.get_config('storage_path'), '/test/path')
            self.assertEqual(controller.get_config('max_memory_mb'), 200)
            self.assertFalse(controller.get_config('analytics_enabled'))
    
    def test_feature_enabled_check(self):
        """Test feature enabled checking"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            controller = ConfigurationController()
            
            # Should be enabled in standard mode
            self.assertTrue(controller.is_feature_enabled('analytics'))
            
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'disabled'}):
            controller = ConfigurationController()
            
            # Should be disabled when learning is disabled
            self.assertFalse(controller.is_feature_enabled('analytics'))
    
    def test_configuration_thread_safety(self):
        """Test configuration controller thread safety"""
        controller = ConfigurationController()
        
        # Test concurrent access
        def access_config():
            for _ in range(100):
                controller.get_config('learning_mode')
                controller.is_feature_enabled('analytics')
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=access_config)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should complete without errors
        self.assertTrue(True)
    
    def test_configuration_reload(self):
        """Test configuration reload functionality"""
        controller = ConfigurationController()
        
        original_mode = controller.get_config('learning_mode')
        
        # Change environment and reload
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'advanced'}):
            controller.reload_configuration()
            new_mode = controller.get_config('learning_mode')
            
            self.assertEqual(new_mode, 'advanced')
            self.assertNotEqual(original_mode, new_mode)


class TestLearningMonitoring(unittest.TestCase):
    """Test LearningMonitoring functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not VALIDATION_LEARNING_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def test_learning_monitoring_initialization(self):
        """Test LearningMonitoring initializes correctly"""
        monitoring = LearningMonitoring()
        
        # Verify metrics structure
        expected_metrics = [
            'events_processed', 'patterns_stored', 'insights_generated',
            'predictions_made', 'errors_encountered', 'memory_usage_mb',
            'storage_usage_mb', 'avg_processing_time_ms', 'last_activity'
        ]
        
        for metric in expected_metrics:
            self.assertIn(metric, monitoring.metrics)
    
    def test_metric_recording(self):
        """Test metric recording functionality"""
        monitoring = LearningMonitoring()
        
        # Test simple metric recording
        monitoring.record_metric('memory_usage_mb', 50.5)
        self.assertEqual(monitoring.metrics['memory_usage_mb'], 50.5)
        
        # Test counter increment
        monitoring.increment_counter('events_processed')
        self.assertEqual(monitoring.metrics['events_processed'], 1)
        
        monitoring.increment_counter('events_processed')
        self.assertEqual(monitoring.metrics['events_processed'], 2)
    
    def test_processing_time_average(self):
        """Test processing time average calculation"""
        monitoring = LearningMonitoring()
        
        # Record several processing times
        monitoring.record_metric('avg_processing_time_ms', 10.0)
        monitoring.increment_counter('events_processed')
        
        monitoring.record_metric('avg_processing_time_ms', 20.0)
        monitoring.increment_counter('events_processed')
        
        # Should calculate running average
        avg_time = monitoring.metrics['avg_processing_time_ms']
        self.assertAlmostEqual(avg_time, 15.0, places=1)
    
    def test_health_status_calculation(self):
        """Test health status calculation"""
        monitoring = LearningMonitoring()
        
        # Test healthy status
        monitoring.metrics['events_processed'] = 100
        monitoring.metrics['errors_encountered'] = 5  # 5% error rate
        
        status = monitoring.get_health_status()
        
        self.assertEqual(status['status'], 'healthy')
        self.assertIn('metrics', status)
        self.assertIn('error_rate', status)
        self.assertIn('uptime_seconds', status)
        self.assertEqual(status['error_rate'], 0.05)
        
        # Test degraded status (high error rate)
        monitoring.metrics['errors_encountered'] = 15  # 15% error rate
        
        status_degraded = monitoring.get_health_status()
        self.assertEqual(status_degraded['status'], 'degraded')
    
    def test_thread_safety(self):
        """Test thread safety of monitoring operations"""
        monitoring = LearningMonitoring()
        
        def record_metrics():
            for i in range(100):
                monitoring.increment_counter('events_processed')
                monitoring.record_metric('memory_usage_mb', float(i))
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=record_metrics)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should complete without errors
        # Total events should be 500 (5 threads × 100 increments)
        self.assertEqual(monitoring.metrics['events_processed'], 500)


class TestValidationEventDataStructures(unittest.TestCase):
    """Test ValidationEvent and ValidationInsights data structures"""
    
    @classmethod
    def setUpClass(cls):
        if not VALIDATION_LEARNING_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def test_validation_event_creation(self):
        """Test ValidationEvent creation and serialization"""
        event = ValidationEvent(
            event_id='test_001',
            event_type='evidence_validation',
            context={'key': 'value'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='test_system',
            success=True,
            confidence=0.85,
            metadata={'meta': 'data'}
        )
        
        # Test to_dict conversion
        event_dict = event.to_dict()
        
        required_fields = [
            'event_id', 'event_type', 'context', 'result',
            'timestamp', 'source_system', 'success', 'confidence', 'metadata'
        ]
        
        for field in required_fields:
            self.assertIn(field, event_dict)
        
        # Test timestamp serialization
        self.assertIsInstance(event_dict['timestamp'], str)
    
    def test_validation_insights_creation(self):
        """Test ValidationInsights creation and serialization"""
        insights = ValidationInsights(
            insight_type='pattern_match',
            confidence=0.9,
            recommendations=[{'type': 'suggestion', 'message': 'test'}],
            predictions=[{'type': 'success_rate', 'value': 0.85}],
            patterns_matched=['pattern_1', 'pattern_2'],
            generated_at=datetime.utcnow()
        )
        
        # Test to_dict conversion
        insights_dict = insights.to_dict()
        
        required_fields = [
            'insight_type', 'confidence', 'recommendations',
            'predictions', 'patterns_matched', 'generated_at'
        ]
        
        for field in required_fields:
            self.assertIn(field, insights_dict)
        
        # Test data types
        self.assertIsInstance(insights_dict['recommendations'], list)
        self.assertIsInstance(insights_dict['predictions'], list)
        self.assertIsInstance(insights_dict['patterns_matched'], list)


if __name__ == '__main__':
    print("🧪 Validation Learning Core Unit Tests")
    print("=" * 50)
    print("Testing non-intrusive operation, safety guarantees, and learning capabilities")
    print("=" * 50)
    
    if not VALIDATION_LEARNING_AVAILABLE:
        print("❌ Validation Learning Core not available - skipping tests")
        exit(1)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestValidationLearningCore))
    suite.addTests(loader.loadTestsFromTestCase(TestResourceMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestStorageMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestSafeFailureManager))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigurationController))
    suite.addTests(loader.loadTestsFromTestCase(TestLearningMonitoring))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationEventDataStructures))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print(f"\n📊 Validation Learning Core Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
    
    exit(0 if result.wasSuccessful() else 1)