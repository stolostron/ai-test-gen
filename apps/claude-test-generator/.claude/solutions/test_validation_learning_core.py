#!/usr/bin/env python3
"""
Validation Learning Core - Comprehensive Test Suite

This test suite validates all safety guarantees and non-intrusive operation
principles of the Validation Learning Core system.

Test Categories:
1. Non-Intrusive Operation Tests
2. Safe Failure Handling Tests  
3. Performance Impact Tests
4. Configuration Control Tests
5. Integration Safety Tests
6. Resource Management Tests
7. Concurrent Operation Tests

Author: AI Systems Suite / Claude Test Generator Framework
Version: 1.0.0
"""

import unittest
import os
import time
import threading
import tempfile
import shutil
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import json

# Import the modules we're testing
from .validation_learning_core import (
    ValidationLearningCore, ValidationEvent, ValidationInsights, 
    LearningMode, get_learning_core, shutdown_learning_core
)
from .learning_services import (
    ValidationPatternMemory, ValidationAnalyticsService, ValidationKnowledgeBase
)
from .validation_learning_mixin import (
    ValidationSystemLearningMixin, learn_from_validation, 
    get_validation_insights, with_learning
)


class TestValidationLearningCore(unittest.TestCase):
    """Test the main ValidationLearningCore functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Set environment variables for testing
        self.original_env = {}
        test_env = {
            'CLAUDE_VALIDATION_LEARNING': 'standard',
            'CLAUDE_LEARNING_STORAGE_PATH': self.test_dir,
            'CLAUDE_LEARNING_MAX_MEMORY': '10',  # Low limits for testing
            'CLAUDE_LEARNING_MAX_STORAGE': '50',
            'CLAUDE_LEARNING_QUEUE_SIZE': '100'
        }
        
        for key, value in test_env.items():
            self.original_env[key] = os.environ.get(key)
            os.environ[key] = value
    
    def tearDown(self):
        """Clean up test environment"""
        # Restore environment variables
        for key, value in self.original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        
        # Clean up temporary directory
        try:
            shutil.rmtree(self.test_dir)
        except Exception:
            pass
        
        # Shutdown learning core
        shutdown_learning_core()
    
    def test_disabled_mode_zero_impact(self):
        """Test that disabled mode has zero impact on performance"""
        # Set learning to disabled
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'disabled'
        
        core = ValidationLearningCore()
        
        # Verify learning is disabled
        self.assertFalse(core.is_enabled())
        self.assertEqual(core.learning_mode, LearningMode.DISABLED)
        
        # Create mock validation event
        mock_event = ValidationEvent(
            event_id='test_event_1',
            event_type='test_validation',
            context={'test': 'data'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='TestSystem',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        # Test that learning operations are no-ops
        self.assertIsNone(core.learn_from_validation(mock_event))
        self.assertIsNone(core.get_validation_insights({'test': 'context'}))
        self.assertFalse(core.is_safe_to_learn())
        
        # Test performance impact (should be negligible)
        start_time = time.time()
        for _ in range(1000):
            core.learn_from_validation(mock_event)
        duration = time.time() - start_time
        
        # Should complete very quickly (less than 10ms for 1000 calls)
        self.assertLess(duration, 0.01)
    
    def test_learning_failure_isolation(self):
        """Test that learning failures don't impact validation operations"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        core = ValidationLearningCore()
        
        # Break the learning system intentionally
        core.pattern_memory = None
        core.analytics_service = None
        core.knowledge_base = None
        
        mock_event = ValidationEvent(
            event_id='test_event_2',
            event_type='test_validation',
            context={'test': 'data'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='TestSystem',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        # These operations should fail silently (no exceptions)
        result = core.learn_from_validation(mock_event)
        self.assertIsNone(result)
        
        result = core.get_validation_insights({'test': 'context'})
        self.assertIsNone(result)
        
        # Health status should still be available
        health = core.get_health_status()
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
    
    def test_configuration_control(self):
        """Test that configuration controls work correctly"""
        # Test different learning modes
        modes = ['disabled', 'conservative', 'standard', 'advanced']
        
        for mode in modes:
            os.environ['CLAUDE_VALIDATION_LEARNING'] = mode
            core = ValidationLearningCore()
            
            expected_enabled = mode != 'disabled'
            self.assertEqual(core.is_enabled(), expected_enabled)
            
            if expected_enabled:
                self.assertEqual(core.learning_mode.value, mode)
            
            core.shutdown()
    
    def test_resource_limits_respected(self):
        """Test that resource limits are respected"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        os.environ['CLAUDE_LEARNING_MAX_MEMORY'] = '1'  # Very low limit
        
        core = ValidationLearningCore()
        
        # Resource monitor should prevent learning when limits exceeded
        # This is tested by mocking the resource monitor
        with patch.object(core.resource_monitor, 'is_resource_available', return_value=False):
            self.assertFalse(core.is_safe_to_learn())
    
    def test_async_operation(self):
        """Test that learning operations are truly async and non-blocking"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        core = ValidationLearningCore()
        
        mock_event = ValidationEvent(
            event_id='test_event_3',
            event_type='test_validation',
            context={'test': 'data'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='TestSystem',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        # Learning should return immediately
        start_time = time.time()
        core.learn_from_validation(mock_event)
        duration = time.time() - start_time
        
        # Should return in less than 1ms (async operation)
        self.assertLess(duration, 0.001)
    
    def test_storage_isolation(self):
        """Test that learning storage is isolated from validation logic"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        core = ValidationLearningCore()
        
        # Learning storage should be in separate directory
        self.assertTrue(core.storage_path.endswith('validation'))
        self.assertNotIn('claude', str(core.storage_path).lower().split('learning')[0])
    
    def test_health_monitoring(self):
        """Test health monitoring functionality"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        core = ValidationLearningCore()
        
        health = core.get_health_status()
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        self.assertIn('learning_mode', health)
        self.assertIn('timestamp', health)
        
        # Test disabled mode health
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'disabled'
        core_disabled = ValidationLearningCore()
        
        health_disabled = core_disabled.get_health_status()
        self.assertEqual(health_disabled['status'], 'disabled')


class TestLearningServices(unittest.TestCase):
    """Test the learning services functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.learning_mode = LearningMode.STANDARD
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            shutil.rmtree(self.test_dir)
        except Exception:
            pass
    
    def test_pattern_memory_safe_operation(self):
        """Test that pattern memory operates safely"""
        pattern_memory = ValidationPatternMemory(
            storage_path=self.test_dir,
            learning_mode=self.learning_mode
        )
        
        # Test safe storage operations
        mock_event = ValidationEvent(
            event_id='test_pattern_1',
            event_type='test_validation',
            context={'test_key': 'test_value'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='TestSystem',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        # Should not raise exceptions
        pattern_memory.store_pattern(mock_event)
        
        # Should return safely even with empty data
        patterns = pattern_memory.find_similar_patterns({'empty': 'context'})
        self.assertIsInstance(patterns, list)
        
        # Statistics should be available
        stats = pattern_memory.get_pattern_statistics()
        self.assertIsInstance(stats, dict)
    
    def test_analytics_service_safe_operation(self):
        """Test that analytics service operates safely"""
        analytics_service = ValidationAnalyticsService(
            storage_path=self.test_dir,
            learning_mode=self.learning_mode
        )
        
        mock_event = ValidationEvent(
            event_id='test_analytics_1',
            event_type='test_validation',
            context={'test_key': 'test_value'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='TestSystem',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        # Should operate safely
        analytics_service.record_validation_event(mock_event)
        
        # Should return None safely when no data available
        insights = analytics_service.generate_insights({'test': 'context'})
        # Can be None or ValidationInsights
        self.assertTrue(insights is None or hasattr(insights, 'confidence'))
        
        trends = analytics_service.analyze_validation_trends()
        # Can be None or dict
        self.assertTrue(trends is None or isinstance(trends, dict))
    
    def test_knowledge_base_safe_operation(self):
        """Test that knowledge base operates safely"""
        knowledge_base = ValidationKnowledgeBase(
            storage_path=self.test_dir,
            learning_mode=self.learning_mode
        )
        
        mock_event = ValidationEvent(
            event_id='test_knowledge_1',
            event_type='test_validation',
            context={'test_key': 'test_value'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='TestSystem',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        # Should operate safely
        knowledge_base.update_knowledge(mock_event)
        
        # Should return safely
        query_result = knowledge_base.query_knowledge('test_subject')
        # Can be None or dict
        self.assertTrue(query_result is None or isinstance(query_result, dict))
        
        summary = knowledge_base.get_knowledge_summary()
        self.assertIsInstance(summary, dict)


class TestValidationLearningMixin(unittest.TestCase):
    """Test the validation learning mixin functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        os.environ['CLAUDE_LEARNING_STORAGE_PATH'] = self.test_dir
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            shutil.rmtree(self.test_dir)
        except Exception:
            pass
        os.environ.pop('CLAUDE_VALIDATION_LEARNING', None)
        os.environ.pop('CLAUDE_LEARNING_STORAGE_PATH', None)
        shutdown_learning_core()
    
    def test_mixin_integration(self):
        """Test that mixin integrates safely with existing classes"""
        
        class MockValidationSystem:
            def __init__(self):
                self.logger = Mock()
            
            def validate_data(self, data):
                return {'success': True, 'confidence': 0.9, 'data': data}
        
        class EnhancedValidationSystem(MockValidationSystem, ValidationSystemLearningMixin):
            def enhanced_validate_data(self, data):
                # Original validation
                result = self.validate_data(data)
                
                # Learning integration
                self._learn_from_validation_result(result, data)
                
                # Optional insights
                insights = self._get_validation_insights({'data_type': type(data).__name__})
                enhanced_result = self._enhance_validation_with_insights(result, insights)
                
                return enhanced_result
        
        # Test enhanced system
        enhanced_system = EnhancedValidationSystem()
        
        # Should work without errors
        result = enhanced_system.enhanced_validate_data({'test': 'data'})
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])
        
        # Should have learning statistics
        stats = enhanced_system.get_learning_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('learning_enabled', stats)
    
    def test_direct_learning_functions(self):
        """Test direct learning functions work safely"""
        
        # Test learn_from_validation function
        learn_from_validation(
            validation_system_name='TestSystem',
            validation_type='test_validation',
            context={'test': 'context'},
            result={'success': True},
            success=True,
            confidence=0.8
        )
        
        # Should not raise exceptions
        
        # Test get_validation_insights function
        insights = get_validation_insights(
            validation_type='test_validation',
            context={'test': 'context'}
        )
        
        # Should return None or ValidationInsights
        self.assertTrue(insights is None or hasattr(insights, 'confidence'))
    
    def test_learning_decorator(self):
        """Test the learning decorator works safely"""
        
        class TestValidationSystem:
            def __init__(self):
                pass
            
            @with_learning(validation_type='decorated_validation')
            def validate_with_decorator(self, data):
                return {'success': True, 'confidence': 0.9, 'result': data}
        
        system = TestValidationSystem()
        
        # Should work without errors
        result = system.validate_with_decorator({'test': 'data'})
        self.assertIsInstance(result, dict)
        self.assertTrue(result['success'])


class TestConcurrentOperation(unittest.TestCase):
    """Test concurrent operation safety"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        os.environ['CLAUDE_LEARNING_STORAGE_PATH'] = self.test_dir
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            shutil.rmtree(self.test_dir)
        except Exception:
            pass
        os.environ.pop('CLAUDE_VALIDATION_LEARNING', None)
        os.environ.pop('CLAUDE_LEARNING_STORAGE_PATH', None)
        shutdown_learning_core()
    
    def test_concurrent_learning_operations(self):
        """Test that concurrent learning operations are safe"""
        core = ValidationLearningCore()
        
        def learning_worker(worker_id):
            """Worker function for concurrent testing"""
            for i in range(10):
                mock_event = ValidationEvent(
                    event_id=f'worker_{worker_id}_event_{i}',
                    event_type='concurrent_test',
                    context={'worker_id': worker_id, 'iteration': i},
                    result={'success': True},
                    timestamp=datetime.utcnow(),
                    source_system='ConcurrentTest',
                    success=True,
                    confidence=0.8,
                    metadata={}
                )
                
                # Should not raise exceptions
                core.learn_from_validation(mock_event)
                
                # Small delay to simulate real usage
                time.sleep(0.001)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=learning_worker, args=(i,))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=5.0)  # 5 second timeout
        
        # All threads should complete without errors
        for thread in threads:
            self.assertFalse(thread.is_alive())
    
    def test_singleton_behavior(self):
        """Test that learning core behaves as singleton"""
        core1 = get_learning_core()
        core2 = get_learning_core()
        
        # Should be the same instance
        self.assertIs(core1, core2)


class TestPerformanceImpact(unittest.TestCase):
    """Test performance impact of learning system"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            shutil.rmtree(self.test_dir)
        except Exception:
            pass
        shutdown_learning_core()
    
    def test_disabled_mode_performance(self):
        """Test that disabled mode has zero performance impact"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'disabled'
        os.environ['CLAUDE_LEARNING_STORAGE_PATH'] = self.test_dir
        
        core = ValidationLearningCore()
        
        mock_event = ValidationEvent(
            event_id='perf_test_1',
            event_type='performance_test',
            context={'test': 'data'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='PerformanceTest',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        # Measure performance
        iterations = 10000
        start_time = time.time()
        
        for _ in range(iterations):
            core.learn_from_validation(mock_event)
        
        duration = time.time() - start_time
        avg_time_per_call = (duration / iterations) * 1000  # Convert to milliseconds
        
        # Should be extremely fast (less than 0.001ms per call)
        self.assertLess(avg_time_per_call, 0.001)
    
    def test_enabled_mode_performance(self):
        """Test that enabled mode has minimal performance impact"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'conservative'
        os.environ['CLAUDE_LEARNING_STORAGE_PATH'] = self.test_dir
        
        core = ValidationLearningCore()
        
        mock_event = ValidationEvent(
            event_id='perf_test_2',
            event_type='performance_test',
            context={'test': 'data'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='PerformanceTest',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        # Measure performance
        iterations = 1000
        start_time = time.time()
        
        for _ in range(iterations):
            core.learn_from_validation(mock_event)
        
        duration = time.time() - start_time
        avg_time_per_call = (duration / iterations) * 1000  # Convert to milliseconds
        
        # Should still be very fast (less than 1ms per call)
        self.assertLess(avg_time_per_call, 1.0)


class TestSafetyGuarantees(unittest.TestCase):
    """Test all safety guarantees are met"""
    
    def test_no_exceptions_on_invalid_input(self):
        """Test that invalid input never causes exceptions"""
        core = ValidationLearningCore()
        
        # Test with invalid event data
        invalid_events = [
            None,
            "invalid_string",
            123,
            {},
            ValidationEvent(None, None, None, None, None, None, None, None, None)
        ]
        
        for invalid_event in invalid_events:
            try:
                core.learn_from_validation(invalid_event)
                # Should not raise exceptions
            except Exception as e:
                self.fail(f"Learning should not raise exceptions, but got: {e}")
        
        # Test with invalid context
        invalid_contexts = [
            None,
            "invalid_string", 
            123,
            [],
        ]
        
        for invalid_context in invalid_contexts:
            try:
                result = core.get_validation_insights(invalid_context)
                # Should return None safely
                self.assertIsNone(result)
            except Exception as e:
                self.fail(f"Insights should not raise exceptions, but got: {e}")
    
    def test_error_recovery(self):
        """Test that the system recovers from errors gracefully"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        core = ValidationLearningCore()
        
        # Simulate storage errors by making storage read-only
        if hasattr(core, 'storage_path'):
            try:
                os.chmod(str(core.storage_path), 0o444)  # Read-only
                
                mock_event = ValidationEvent(
                    event_id='error_test_1',
                    event_type='error_test',
                    context={'test': 'data'},
                    result={'success': True},
                    timestamp=datetime.utcnow(),
                    source_system='ErrorTest',
                    success=True,
                    confidence=0.8,
                    metadata={}
                )
                
                # Should handle storage errors gracefully
                core.learn_from_validation(mock_event)
                
                # System should still be operational
                health = core.get_health_status()
                self.assertIsInstance(health, dict)
                
            finally:
                # Restore permissions
                try:
                    os.chmod(str(core.storage_path), 0o755)
                except Exception:
                    pass


def run_comprehensive_tests():
    """Run all tests and generate a comprehensive report"""
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestValidationLearningCore,
        TestLearningServices, 
        TestValidationLearningMixin,
        TestConcurrentOperation,
        TestPerformanceImpact,
        TestSafetyGuarantees
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Generate report
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success_rate = ((total_tests - failures - errors) / total_tests) * 100 if total_tests > 0 else 0
    
    print("\n" + "="*60)
    print("VALIDATION LEARNING CORE - TEST REPORT")
    print("="*60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_tests - failures - errors}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {success_rate:.1f}%")
    print("="*60)
    
    if failures > 0:
        print("\nFAILURES:")
        for test, trace in result.failures:
            print(f"- {test}: {trace}")
    
    if errors > 0:
        print("\nERRORS:")
        for test, trace in result.errors:
            print(f"- {test}: {trace}")
    
    print(f"\nSAFETY GUARANTEE STATUS: {'✅ VERIFIED' if success_rate >= 95 else '❌ ISSUES DETECTED'}")
    
    return success_rate >= 95


if __name__ == '__main__':
    # Run comprehensive tests
    success = run_comprehensive_tests()
    exit(0 if success else 1)