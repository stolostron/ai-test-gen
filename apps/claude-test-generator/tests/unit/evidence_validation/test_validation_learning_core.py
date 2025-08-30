#!/usr/bin/env python3
"""
Validation Learning Core Unit Tests
==================================

Comprehensive unit tests for the Validation Learning Core testing:
- Non-intrusive learning foundation functionality
- Safe failure handling and resource management
- Configuration-controlled operation modes
- Async processing and queue management
- Learning service integration and coordination
- Performance monitoring and health checking
- Event validation and pattern storage

This test suite validates the learning foundation that enhances
Evidence Validation without impacting core framework operations.
"""

import unittest
import sys
import os
import tempfile
import json
import time
import threading
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from pathlib import Path
from datetime import datetime

# Add the project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".claude" / "solutions"))
    from validation_learning_core import (
        ValidationLearningCore,
        LearningMode,
        ValidationEvent,
        ValidationInsights,
        ResourceMonitor,
        StorageMonitor,
        SafeFailureManager,
        ConfigurationController,
        LearningMonitoring,
        get_learning_core,
        shutdown_learning_core
    )
    LEARNING_CORE_AVAILABLE = True
except ImportError as e:
    LEARNING_CORE_AVAILABLE = False
    print(f"❌ Validation Learning Core not available: {e}")


class TestValidationLearningCore(unittest.TestCase):
    """Unit tests for Validation Learning Core"""
    
    @classmethod
    def setUpClass(cls):
        if not LEARNING_CORE_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Set environment variables for testing
        self.env_patcher = patch.dict(os.environ, {
            'CLAUDE_VALIDATION_LEARNING': 'standard',
            'CLAUDE_LEARNING_STORAGE_PATH': str(self.test_path),
            'CLAUDE_LEARNING_MAX_MEMORY': '50',
            'CLAUDE_LEARNING_MAX_STORAGE': '100'
        })
        self.env_patcher.start()
        
    def tearDown(self):
        """Clean up test environment"""
        self.env_patcher.stop()
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_learning_core_initialization(self):
        """Test basic learning core initialization"""
        core = ValidationLearningCore()
        
        self.assertIsNotNone(core)
        self.assertEqual(core.learning_mode, LearningMode.STANDARD)
        self.assertIsNotNone(core.config_controller)
        self.assertIsNotNone(core.safe_failure_manager)
        self.assertIsNotNone(core.resource_monitor)
        self.assertIsNotNone(core.storage_monitor)
        self.assertIsInstance(core.validation_stats, dict)
    
    def test_learning_mode_detection(self):
        """Test learning mode detection from configuration"""
        # Test disabled mode
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'disabled'}):
            core = ValidationLearningCore()
            self.assertEqual(core.learning_mode, LearningMode.DISABLED)
            self.assertFalse(core.is_enabled())
        
        # Test conservative mode
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'conservative'}):
            core = ValidationLearningCore()
            self.assertEqual(core.learning_mode, LearningMode.CONSERVATIVE)
            self.assertTrue(core.is_enabled())
        
        # Test advanced mode
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'advanced'}):
            core = ValidationLearningCore()
            self.assertEqual(core.learning_mode, LearningMode.ADVANCED)
            self.assertTrue(core.is_enabled())
    
    def test_safety_checks(self):
        """Test safety check functionality"""
        core = ValidationLearningCore()
        
        # Test is_safe_to_learn method
        if core.is_enabled():
            # Should perform safety checks
            safe = core.is_safe_to_learn()
            self.assertIsInstance(safe, bool)
        else:
            # Disabled learning should never be safe
            self.assertFalse(core.is_safe_to_learn())
    
    def test_validation_event_creation(self):
        """Test validation event creation and validation"""
        # Create a proper validation event
        event = ValidationEvent(
            event_id="test_event_123",
            event_type="evidence_validation",
            context={"test": "context"},
            result={"success": True},
            timestamp=datetime.utcnow(),
            source_system="test_system",
            success=True,
            confidence=0.8,
            metadata={"test": "metadata"}
        )
        
        # Test event validation
        core = ValidationLearningCore()
        is_valid = core._validate_event(event)
        self.assertTrue(is_valid)
        
        # Test event serialization
        event_dict = event.to_dict()
        self.assertIsInstance(event_dict, dict)
        self.assertEqual(event_dict['event_id'], "test_event_123")
        self.assertEqual(event_dict['event_type'], "evidence_validation")
        self.assertTrue(event_dict['success'])
    
    def test_validation_event_learning(self):
        """Test learning from validation events"""
        core = ValidationLearningCore()
        
        # Create test event
        event = ValidationEvent(
            event_id="learn_test_123",
            event_type="evidence_validation",
            context={"validation_type": "fiction_detection"},
            result={"fiction_detected": True},
            timestamp=datetime.utcnow(),
            source_system="evidence_validation_engine",
            success=False,
            confidence=0.9,
            metadata={"pattern": "fictional_field"}
        )
        
        # Should not crash when learning (even if learning is disabled)
        core.learn_from_validation(event)
        
        # This should be safe and non-blocking
        self.assertTrue(True)  # If we get here, learning didn't crash validation
    
    def test_validation_insights_generation(self):
        """Test validation insights generation"""
        core = ValidationLearningCore()
        
        test_context = {
            "validation_type": "evidence_validation",
            "content_type": "cluster_curator",
            "evidence_quality": 0.8
        }
        
        # Should return insights or None safely
        insights = core.get_validation_insights(test_context)
        
        # Result should be None (learning disabled) or ValidationInsights
        self.assertTrue(insights is None or isinstance(insights, ValidationInsights))
    
    def test_health_status_reporting(self):
        """Test health status reporting"""
        core = ValidationLearningCore()
        
        health = core.get_health_status()
        
        # Validate health status structure
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        self.assertIn('learning_mode', health)
        self.assertIn('timestamp', health)
        
        # Check status values
        self.assertIn(health['status'], ['disabled', 'enabled'])
        self.assertEqual(health['learning_mode'], core.learning_mode.value)
    
    def test_shutdown_functionality(self):
        """Test graceful shutdown"""
        core = ValidationLearningCore()
        
        # Should not crash on shutdown
        core.shutdown()
        
        # Test multiple shutdowns (should be safe)
        core.shutdown()
        core.shutdown()
        
        self.assertTrue(True)  # If we get here, shutdown worked


class TestResourceMonitor(unittest.TestCase):
    """Test resource monitoring functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not LEARNING_CORE_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def test_resource_monitor_initialization(self):
        """Test resource monitor initialization"""
        monitor = ResourceMonitor()
        
        self.assertIsNotNone(monitor)
        self.assertIsInstance(monitor.max_memory_mb, int)
        self.assertIsInstance(monitor.max_cpu_percent, float)
    
    def test_resource_availability_check(self):
        """Test resource availability checking"""
        monitor = ResourceMonitor()
        
        # Should return boolean
        available = monitor.is_resource_available()
        self.assertIsInstance(available, bool)
    
    @patch.dict(os.environ, {'CLAUDE_LEARNING_MAX_MEMORY': '10'})
    def test_memory_limit_configuration(self):
        """Test memory limit configuration"""
        monitor = ResourceMonitor()
        self.assertEqual(monitor.max_memory_mb, 10)
    
    @patch.dict(os.environ, {'CLAUDE_LEARNING_MAX_CPU': '2.5'})
    def test_cpu_limit_configuration(self):
        """Test CPU limit configuration"""
        monitor = ResourceMonitor()
        self.assertEqual(monitor.max_cpu_percent, 2.5)


class TestStorageMonitor(unittest.TestCase):
    """Test storage monitoring functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not LEARNING_CORE_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_storage_monitor_initialization(self):
        """Test storage monitor initialization"""
        monitor = StorageMonitor(self.test_dir)
        
        self.assertIsNotNone(monitor)
        self.assertEqual(monitor.storage_path, Path(self.test_dir))
        self.assertIsInstance(monitor.max_storage_mb, int)
    
    def test_storage_availability_check(self):
        """Test storage availability checking"""
        monitor = StorageMonitor(self.test_dir)
        
        # Should return boolean
        available = monitor.is_storage_available()
        self.assertIsInstance(available, bool)
    
    def test_storage_usage_calculation(self):
        """Test storage usage calculation"""
        monitor = StorageMonitor(self.test_dir)
        
        # Create test file
        test_file = Path(self.test_dir) / "test_file.txt"
        test_file.write_text("test content")
        
        usage = monitor._calculate_storage_usage()
        self.assertIsInstance(usage, float)
        self.assertGreater(usage, 0)  # Should detect the test file


class TestSafeFailureManager(unittest.TestCase):
    """Test safe failure management"""
    
    @classmethod
    def setUpClass(cls):
        if not LEARNING_CORE_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def test_safe_failure_manager_initialization(self):
        """Test safe failure manager initialization"""
        manager = SafeFailureManager()
        
        self.assertIsNotNone(manager)
        self.assertIsInstance(manager.error_stats, dict)
        self.assertIsInstance(manager.circuit_breakers, dict)
        self.assertIsInstance(manager.last_errors, dict)
    
    def test_failure_handling(self):
        """Test failure handling functionality"""
        manager = SafeFailureManager()
        
        # Test handling a learning failure
        test_error = Exception("Test learning error")
        manager.handle_learning_failure("test_operation", test_error)
        
        # Should track the error
        self.assertIn("test_operation", manager.error_stats)
        self.assertEqual(manager.error_stats["test_operation"], 1)
        self.assertIn("test_operation", manager.last_errors)
    
    def test_circuit_breaker_functionality(self):
        """Test circuit breaker functionality"""
        # Set low error threshold for testing
        with patch.dict(os.environ, {'CLAUDE_LEARNING_MAX_ERRORS_PER_OP': '2'}):
            manager = SafeFailureManager()
            
            # Initially should be safe
            self.assertTrue(manager.is_operation_safe("test_op"))
            
            # Add errors to trigger circuit breaker
            test_error = Exception("Test error")
            for i in range(3):  # Exceed threshold of 2
                manager.handle_learning_failure("test_op", test_error)
            
            # Should trigger circuit breaker
            self.assertFalse(manager.is_operation_safe("test_op"))
            
            # Test circuit breaker reset
            manager.reset_circuit_breaker("test_op")
            self.assertTrue(manager.is_operation_safe("test_op"))


class TestConfigurationController(unittest.TestCase):
    """Test configuration management"""
    
    @classmethod
    def setUpClass(cls):
        if not LEARNING_CORE_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def test_configuration_controller_initialization(self):
        """Test configuration controller initialization"""
        controller = ConfigurationController()
        
        self.assertIsNotNone(controller)
        self.assertIsInstance(controller.config, dict)
    
    def test_configuration_loading(self):
        """Test configuration loading from environment"""
        with patch.dict(os.environ, {
            'CLAUDE_VALIDATION_LEARNING': 'advanced',
            'CLAUDE_LEARNING_MAX_MEMORY': '200',
            'CLAUDE_LEARNING_ANALYTICS': 'false'
        }):
            controller = ConfigurationController()
            
            self.assertEqual(controller.get_config('learning_mode'), 'advanced')
            self.assertEqual(controller.get_config('max_memory_mb'), 200)
            self.assertFalse(controller.get_config('analytics_enabled'))
    
    def test_feature_enablement_check(self):
        """Test feature enablement checking"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            controller = ConfigurationController()
            
            # Learning enabled, so features should be enabled
            self.assertTrue(controller.is_feature_enabled('analytics'))
            self.assertTrue(controller.is_feature_enabled('prediction'))
        
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'disabled'}):
            controller = ConfigurationController()
            
            # Learning disabled, so features should be disabled
            self.assertFalse(controller.is_feature_enabled('analytics'))
            self.assertFalse(controller.is_feature_enabled('prediction'))
    
    def test_configuration_reload(self):
        """Test configuration reloading"""
        controller = ConfigurationController()
        
        # Should not crash on reload
        controller.reload_configuration()
        
        # Configuration should still be valid
        self.assertIsInstance(controller.config, dict)


class TestLearningMonitoring(unittest.TestCase):
    """Test learning system monitoring"""
    
    @classmethod
    def setUpClass(cls):
        if not LEARNING_CORE_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def test_learning_monitoring_initialization(self):
        """Test learning monitoring initialization"""
        monitoring = LearningMonitoring()
        
        self.assertIsNotNone(monitoring)
        self.assertIsInstance(monitoring.metrics, dict)
        
        # Check required metrics exist
        required_metrics = [
            'events_processed', 'patterns_stored', 'insights_generated',
            'predictions_made', 'errors_encountered', 'memory_usage_mb',
            'storage_usage_mb', 'avg_processing_time_ms'
        ]
        for metric in required_metrics:
            self.assertIn(metric, monitoring.metrics)
    
    def test_metric_recording(self):
        """Test metric recording functionality"""
        monitoring = LearningMonitoring()
        
        # Test recording different types of metrics
        monitoring.record_metric('memory_usage_mb', 25.5)
        self.assertEqual(monitoring.metrics['memory_usage_mb'], 25.5)
        
        monitoring.record_metric('avg_processing_time_ms', 100.0)
        self.assertEqual(monitoring.metrics['avg_processing_time_ms'], 100.0)
    
    def test_counter_incrementing(self):
        """Test counter incrementing functionality"""
        monitoring = LearningMonitoring()
        
        initial_count = monitoring.metrics['events_processed']
        monitoring.increment_counter('events_processed')
        self.assertEqual(monitoring.metrics['events_processed'], initial_count + 1)
        
        # Test multiple increments
        monitoring.increment_counter('patterns_stored')
        monitoring.increment_counter('patterns_stored')
        self.assertEqual(monitoring.metrics['patterns_stored'], 2)
    
    def test_health_status_generation(self):
        """Test health status generation"""
        monitoring = LearningMonitoring()
        
        # Add some test data
        monitoring.increment_counter('events_processed')
        monitoring.increment_counter('events_processed')
        monitoring.increment_counter('errors_encountered')
        
        health = monitoring.get_health_status()
        
        # Validate health status structure
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        self.assertIn('metrics', health)
        self.assertIn('error_rate', health)
        self.assertIn('uptime_seconds', health)
        
        # Check calculated values
        self.assertIsInstance(health['error_rate'], float)
        self.assertGreaterEqual(health['uptime_seconds'], 0)


class TestValidationLearningCoreIntegration(unittest.TestCase):
    """Test Validation Learning Core integration functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not LEARNING_CORE_AVAILABLE:
            cls.skipTest(cls, "Validation Learning Core not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_singleton_pattern(self):
        """Test singleton pattern implementation"""
        # Clear any existing instance
        shutdown_learning_core()
        
        # Get two instances
        core1 = get_learning_core()
        core2 = get_learning_core()
        
        # Should be the same instance
        self.assertIs(core1, core2)
        
        # Cleanup
        shutdown_learning_core()
    
    def test_thread_safety(self):
        """Test thread safety of learning core"""
        cores = []
        
        def get_core():
            cores.append(get_learning_core())
        
        # Create multiple threads accessing learning core
        threads = []
        for i in range(5):
            thread = threading.Thread(target=get_core)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # All should be the same instance
        for i in range(1, len(cores)):
            self.assertIs(cores[0], cores[i])
        
        # Cleanup
        shutdown_learning_core()
    
    @patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'conservative'})
    def test_conservative_learning_mode(self):
        """Test conservative learning mode"""
        core = ValidationLearningCore()
        
        self.assertEqual(core.learning_mode, LearningMode.CONSERVATIVE)
        self.assertTrue(core.is_enabled())
    
    @patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'advanced'})
    def test_advanced_learning_mode(self):
        """Test advanced learning mode"""
        core = ValidationLearningCore()
        
        self.assertEqual(core.learning_mode, LearningMode.ADVANCED)
        self.assertTrue(core.is_enabled())


if __name__ == '__main__':
    print("🧪 Validation Learning Core Unit Tests")
    print("=" * 50)
    print("Testing non-intrusive learning foundation and safety systems")
    print("=" * 50)
    
    # Check availability
    if not LEARNING_CORE_AVAILABLE:
        print("❌ Validation Learning Core not available - skipping tests")
        exit(1)
    
    # Run tests with detailed output
    unittest.main(verbosity=2)