#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Evidence Validation Engine

This test suite validates:
1. Backward compatibility with existing Evidence Validation Engine
2. Learning enhancement functionality when enabled
3. Safe failure handling when learning components fail
4. Performance impact assessment
5. Integration safety guarantees
"""

import asyncio
import json
import os
import tempfile
import time
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# Add the solutions directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_evidence_validation_engine import (
    EnhancedEvidenceValidationEngine,
    ValidationEventType,
    ValidationResult,
    validate_evidence,
    get_validation_insights,
    health_check
)

class TestEnhancedEvidenceValidationEngine(unittest.TestCase):
    """Comprehensive test suite for Enhanced Evidence Validation Engine"""
    
    def setUp(self):
        """Set up test environment"""
        # Ensure learning is disabled for baseline tests
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'disabled'
        
        # Create test engine
        self.engine = EnhancedEvidenceValidationEngine()
        
        # Test data
        self.test_content_fiction = {"spec.upgrade.imageDigest": "sha256:abc123"}
        self.test_content_valid = {"spec.upgrade.desiredUpdate": "2.15.0"}
        
        self.test_evidence_with_implementation = {
            "agent_c": {
                "schema": {
                    "spec.upgrade.desiredUpdate": "string",
                    "spec.upgrade.channel": "string"
                },
                "implementation_found": True,
                "source": "github_investigation"
            },
            "agent_d": {
                "deployment_status": "not_deployed",
                "environment": "qe6-vmware",
                "available": True
            }
        }
        
        self.test_evidence_without_implementation = {
            "agent_c": {
                "schema": {},
                "implementation_found": False
            },
            "agent_d": {
                "deployment_status": "unknown",
                "environment": "unavailable"
            }
        }
        
        self.test_context = {
            "validation_type": "test_validation",
            "agent_source": "test",
            "content_type": "yaml_field"
        }
    
    def tearDown(self):
        """Clean up test environment"""
        # Reset environment variables
        if 'CLAUDE_VALIDATION_LEARNING' in os.environ:
            del os.environ['CLAUDE_VALIDATION_LEARNING']
    
    # === Backward Compatibility Tests ===
    
    def test_core_validation_fiction_detection(self):
        """Test core fiction detection without learning"""
        success, result = self.engine.validate_evidence(
            self.test_content_fiction,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.FICTION_DETECTED)
        self.assertIn('alternatives', result)
        self.assertTrue(result['evidence_backed'])
    
    def test_core_validation_comprehensive_enablement(self):
        """Test comprehensive test enablement without learning"""
        success, result = self.engine.validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        self.assertTrue(success)
        self.assertEqual(result['result'], ValidationResult.SUCCESS)
        self.assertTrue(result['comprehensive_testing_enabled'])
        self.assertTrue(result['implementation_backed'])
    
    def test_core_validation_recovery_needed(self):
        """Test recovery guidance without learning"""
        success, result = self.engine.validate_evidence(
            self.test_content_valid,
            self.test_evidence_without_implementation,
            self.test_context
        )
        
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.RECOVERY_NEEDED)
        self.assertIn('recovery_guidance', result)
        self.assertFalse(result['comprehensive_testing_possible'])
    
    def test_backward_compatibility_convenience_functions(self):
        """Test backward compatibility of convenience functions"""
        # Test convenience function
        success, result = validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        self.assertTrue(success)
        self.assertIsInstance(result, dict)
        
        # Test health check function
        health = health_check()
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        self.assertIn('core_validation', health)
    
    # === Learning Enhancement Tests ===
    
    def test_learning_disabled_by_default(self):
        """Test that learning is disabled by default"""
        engine = EnhancedEvidenceValidationEngine()
        self.assertFalse(engine.learning_enabled)
        
        # Validation should work normally
        success, result = engine.validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            self.test_context
        )
        self.assertTrue(success)
    
    def test_learning_enabled_mode(self):
        """Test learning enabled mode"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            with patch('enhanced_evidence_validation_engine.LEARNING_AVAILABLE', True):
                with patch('enhanced_evidence_validation_engine.ValidationLearningCore') as mock_core:
                    with patch('enhanced_evidence_validation_engine.ValidationPatternMemory') as mock_memory:
                        with patch('enhanced_evidence_validation_engine.ValidationAnalyticsService') as mock_analytics:
                            # Mock successful initialization
                            mock_core.get_instance.return_value = Mock()
                            mock_memory.return_value = Mock()
                            mock_analytics.return_value = Mock()
                            
                            engine = EnhancedEvidenceValidationEngine()
                            
                            # Verify learning is enabled
                            self.assertTrue(engine.learning_enabled)
                            self.assertIsNotNone(engine.learning_core)
                            self.assertIsNotNone(engine.pattern_memory)
                            self.assertIsNotNone(engine.analytics_service)
    
    def test_learning_enhancement_with_insights(self):
        """Test validation with learning insights"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            with patch('enhanced_evidence_validation_engine.LEARNING_AVAILABLE', True):
                # Create mock analytics service
                mock_analytics = Mock()
                mock_analytics.get_fiction_detection_insights.return_value = {
                    'confidence': 0.95,
                    'patterns': ['non_existent_field_pattern']
                }
                mock_analytics.get_evidence_quality_insights.return_value = {
                    'enhanced_score': 0.9,
                    'reliability_prediction': 0.85
                }
                
                # Create engine with mocked learning
                engine = EnhancedEvidenceValidationEngine()
                engine.learning_enabled = True
                engine.analytics_service = mock_analytics
                
                success, result = engine.validate_evidence(
                    self.test_content_fiction,
                    self.test_evidence_with_implementation,
                    self.test_context
                )
                
                # Check that learning insights are included
                self.assertFalse(success)  # Still detects fiction correctly
                self.assertIn('fiction_confidence', result)
                self.assertIn('evidence_quality', result)
    
    # === Safe Failure Handling Tests ===
    
    def test_learning_failure_safe_handling(self):
        """Test that learning failures don't affect core validation"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            # Create engine with broken learning components
            engine = EnhancedEvidenceValidationEngine()
            engine.learning_enabled = True
            engine.analytics_service = Mock()
            engine.analytics_service.get_fiction_detection_insights.side_effect = Exception("Learning failed")
            
            # Validation should still work
            success, result = engine.validate_evidence(
                self.test_content_valid,
                self.test_evidence_with_implementation,
                self.test_context
            )
            
            self.assertTrue(success)
            self.assertEqual(result['result'], ValidationResult.SUCCESS)
    
    def test_learning_initialization_failure(self):
        """Test safe handling of learning initialization failure"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            with patch('enhanced_evidence_validation_engine.LEARNING_AVAILABLE', True):
                with patch('enhanced_evidence_validation_engine.ValidationLearningCore') as mock_core:
                    # Mock initialization failure
                    mock_core.get_instance.side_effect = Exception("Initialization failed")
                    
                    engine = EnhancedEvidenceValidationEngine()
                    
                    # Learning should be disabled, but validation should work
                    self.assertFalse(engine.learning_enabled)
                    
                    success, result = engine.validate_evidence(
                        self.test_content_valid,
                        self.test_evidence_with_implementation,
                        self.test_context
                    )
                    self.assertTrue(success)
    
    def test_learning_unavailable_graceful_handling(self):
        """Test graceful handling when learning components are unavailable"""
        with patch('enhanced_evidence_validation_engine.LEARNING_AVAILABLE', False):
            engine = EnhancedEvidenceValidationEngine()
            
            self.assertFalse(engine.learning_enabled)
            self.assertIsNone(engine.learning_core)
            
            # Validation should work normally
            success, result = engine.validate_evidence(
                self.test_content_valid,
                self.test_evidence_with_implementation,
                self.test_context
            )
            self.assertTrue(success)
    
    # === Performance Impact Tests ===
    
    def test_performance_impact_disabled_mode(self):
        """Test performance impact when learning is disabled"""
        start_time = time.time()
        
        # Run 100 validations
        for _ in range(100):
            self.engine.validate_evidence(
                self.test_content_valid,
                self.test_evidence_with_implementation,
                self.test_context
            )
        
        total_time = time.time() - start_time
        avg_time_per_validation = total_time / 100
        
        # Should be very fast when disabled
        self.assertLess(avg_time_per_validation, 0.01)  # <10ms per validation
    
    def test_performance_impact_enabled_mode(self):
        """Test performance impact when learning is enabled"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            with patch('enhanced_evidence_validation_engine.LEARNING_AVAILABLE', True):
                # Create engine with mocked learning (fast operations)
                engine = EnhancedEvidenceValidationEngine()
                engine.learning_enabled = True
                engine.learning_core = Mock()
                engine.analytics_service = Mock()
                engine.analytics_service.get_fiction_detection_insights.return_value = None
                engine.analytics_service.get_evidence_quality_insights.return_value = None
                
                start_time = time.time()
                
                # Run 100 validations
                for _ in range(100):
                    engine.validate_evidence(
                        self.test_content_valid,
                        self.test_evidence_with_implementation,
                        self.test_context
                    )
                
                total_time = time.time() - start_time
                avg_time_per_validation = total_time / 100
                
                # Should still be fast when enabled with mocked learning
                self.assertLess(avg_time_per_validation, 0.05)  # <50ms per validation
    
    # === Integration Safety Tests ===
    
    def test_multiple_engines_independent_operation(self):
        """Test that multiple engine instances operate independently"""
        engine1 = EnhancedEvidenceValidationEngine()
        engine2 = EnhancedEvidenceValidationEngine()
        
        # Both should work independently
        success1, _ = engine1.validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        success2, _ = engine2.validate_evidence(
            self.test_content_fiction,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        self.assertTrue(success1)
        self.assertFalse(success2)
        
        # Statistics should be independent
        stats1 = engine1.get_validation_statistics()
        stats2 = engine2.get_validation_statistics()
        
        self.assertEqual(stats1['total_validations'], 1)
        self.assertEqual(stats2['total_validations'], 1)
    
    def test_configuration_control(self):
        """Test configuration control via environment variables"""
        # Test disabled mode
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'disabled'}):
            engine = EnhancedEvidenceValidationEngine()
            self.assertFalse(engine.learning_enabled)
        
        # Test conservative mode
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'conservative'}):
            with patch('enhanced_evidence_validation_engine.LEARNING_AVAILABLE', True):
                with patch('enhanced_evidence_validation_engine.ValidationLearningCore'):
                    with patch('enhanced_evidence_validation_engine.ValidationPatternMemory'):
                        with patch('enhanced_evidence_validation_engine.ValidationAnalyticsService'):
                            engine = EnhancedEvidenceValidationEngine()
                            # Would be enabled if mocks work correctly
    
    # === Functionality Tests ===
    
    def test_fiction_detection_patterns(self):
        """Test fiction detection with various patterns"""
        test_cases = [
            ({"spec.upgrade.imageDigest": "sha256:abc"}, False),  # Fiction
            ({"spec.upgrade.desiredUpdate": "2.15"}, True),      # Valid
            ({"spec.nonExistentField": "value"}, False),         # Fiction
            ({"metadata.name": "test"}, True)                    # Valid (not in fiction patterns)
        ]
        
        for content, expected_success in test_cases:
            with self.subTest(content=content):
                success, result = self.engine.validate_evidence(
                    content,
                    self.test_evidence_with_implementation,
                    self.test_context
                )
                
                if expected_success:
                    self.assertTrue(success or result['result'] == ValidationResult.SUCCESS)
                else:
                    self.assertFalse(success)
                    self.assertEqual(result['result'], ValidationResult.FICTION_DETECTED)
    
    def test_evidence_quality_assessment(self):
        """Test evidence quality assessment functionality"""
        success, result = self.engine.validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        # Quality assessment should be included
        if 'evidence_quality' in result:
            quality = result['evidence_quality']
            self.assertIsInstance(quality, dict)
            
            # Should have assessments for each evidence source
            for source in ['agent_c', 'agent_d']:
                if source in quality:
                    source_quality = quality[source]
                    self.assertIn('reliability', source_quality)
                    self.assertIn('completeness', source_quality)
    
    def test_statistics_tracking(self):
        """Test validation statistics tracking"""
        initial_stats = self.engine.get_validation_statistics()
        
        # Perform some validations
        self.engine.validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        self.engine.validate_evidence(
            self.test_content_fiction,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        final_stats = self.engine.get_validation_statistics()
        
        # Check statistics updated
        self.assertEqual(final_stats['total_validations'], initial_stats['total_validations'] + 2)
        self.assertEqual(final_stats['fiction_detected'], initial_stats['fiction_detected'] + 1)
        self.assertIn('success_rate', final_stats)
    
    def test_health_check_functionality(self):
        """Test health check functionality"""
        health = self.engine.health_check()
        
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        self.assertIn('core_validation', health)
        self.assertIn('learning_enabled', health)
        self.assertIn('statistics', health)
        
        self.assertEqual(health['core_validation'], 'operational')
        self.assertFalse(health['learning_enabled'])
    
    # === Edge Cases Tests ===
    
    def test_empty_content_handling(self):
        """Test handling of empty content"""
        success, result = self.engine.validate_evidence(
            {},
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        # Should handle gracefully
        self.assertIsInstance(result, dict)
        self.assertIn('result', result)
    
    def test_empty_evidence_handling(self):
        """Test handling of empty evidence"""
        success, result = self.engine.validate_evidence(
            self.test_content_valid,
            {},
            self.test_context
        )
        
        # Should handle gracefully
        self.assertIsInstance(result, dict)
        self.assertIn('result', result)
    
    def test_malformed_context_handling(self):
        """Test handling of malformed context"""
        success, result = self.engine.validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            {"invalid": "context", "nested": {"deep": "value"}}
        )
        
        # Should handle gracefully
        self.assertIsInstance(result, dict)

class TestLearningInsightsIntegration(unittest.TestCase):
    """Test learning insights integration functionality"""
    
    def test_get_validation_insights_without_learning(self):
        """Test validation insights when learning is disabled"""
        insights = get_validation_insights()
        
        self.assertIsInstance(insights, dict)
        self.assertFalse(insights.get('learning_available', True))
    
    def test_get_validation_insights_with_context(self):
        """Test validation insights with context"""
        test_context = {"component": "test", "validation_type": "fiction_detection"}
        insights = get_validation_insights(test_context)
        
        self.assertIsInstance(insights, dict)

class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmark tests"""
    
    def test_scalability_benchmark(self):
        """Test scalability with high validation volumes"""
        engine = EnhancedEvidenceValidationEngine()
        
        test_content = {"spec.upgrade.desiredUpdate": "2.15.0"}
        test_evidence = {
            "agent_c": {"schema": {"spec.upgrade.desiredUpdate": "string"}, "implementation_found": True},
            "agent_d": {"deployment_status": "available"}
        }
        test_context = {"validation_type": "benchmark"}
        
        start_time = time.time()
        
        # Run 1000 validations
        for i in range(1000):
            success, result = engine.validate_evidence(test_content, test_evidence, test_context)
            self.assertTrue(success)
        
        total_time = time.time() - start_time
        validations_per_second = 1000 / total_time
        
        # Should handle at least 100 validations per second
        self.assertGreater(validations_per_second, 100)
        
        print(f"Performance benchmark: {validations_per_second:.2f} validations/second")

if __name__ == '__main__':
    # Run specific test categories
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'benchmark':
        # Run only benchmark tests
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPerformanceBenchmarks)
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    else:
        # Run all tests
        unittest.main(verbosity=2)