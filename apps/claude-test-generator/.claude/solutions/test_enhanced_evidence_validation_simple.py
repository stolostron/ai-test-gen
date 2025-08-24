#!/usr/bin/env python3
"""
Simplified Test Suite for Enhanced Evidence Validation Engine

This test suite focuses on core functionality and backward compatibility.
"""

import os
import sys
import unittest
from pathlib import Path

# Add the solutions directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_evidence_validation_engine import (
    EnhancedEvidenceValidationEngine,
    ValidationResult,
    validate_evidence,
    health_check
)

class TestEnhancedEvidenceValidationEngineSimple(unittest.TestCase):
    """Simplified test suite focusing on core functionality"""
    
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
        if 'CLAUDE_VALIDATION_LEARNING' in os.environ:
            del os.environ['CLAUDE_VALIDATION_LEARNING']
    
    # === Core Functionality Tests ===
    
    def test_fiction_detection_works(self):
        """Test that fiction detection works correctly"""
        success, result = self.engine.validate_evidence(
            self.test_content_fiction,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.FICTION_DETECTED)
        self.assertIn('alternatives', result)
    
    def test_valid_content_passes(self):
        """Test that valid content passes validation"""
        success, result = self.engine.validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        self.assertTrue(success)
        self.assertEqual(result['result'], ValidationResult.SUCCESS)
        self.assertTrue(result['comprehensive_testing_enabled'])
    
    def test_recovery_needed_when_no_implementation(self):
        """Test recovery needed when no implementation evidence"""
        success, result = self.engine.validate_evidence(
            self.test_content_valid,
            self.test_evidence_without_implementation,
            self.test_context
        )
        
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.RECOVERY_NEEDED)
        self.assertIn('recovery_guidance', result)
    
    def test_convenience_functions_work(self):
        """Test that convenience functions work"""
        # Test validation function
        success, result = validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            self.test_context
        )
        self.assertTrue(success)
        
        # Test health check function
        health = health_check()
        self.assertIn('status', health)
        self.assertEqual(health['core_validation'], 'operational')
    
    def test_learning_disabled_by_default(self):
        """Test that learning is disabled by default"""
        engine = EnhancedEvidenceValidationEngine()
        self.assertFalse(engine.learning_enabled)
    
    def test_statistics_tracking(self):
        """Test that statistics are tracked correctly"""
        initial_stats = self.engine.get_validation_statistics()
        
        # Perform validation
        self.engine.validate_evidence(
            self.test_content_valid,
            self.test_evidence_with_implementation,
            self.test_context
        )
        
        final_stats = self.engine.get_validation_statistics()
        self.assertEqual(final_stats['total_validations'], initial_stats['total_validations'] + 1)
    
    def test_health_check_works(self):
        """Test health check functionality"""
        health = self.engine.health_check()
        
        self.assertIn('status', health)
        self.assertIn('core_validation', health)
        self.assertIn('learning_enabled', health)
        self.assertEqual(health['core_validation'], 'operational')
        self.assertFalse(health['learning_enabled'])
    
    def test_empty_input_handling(self):
        """Test handling of empty inputs"""
        # Empty content
        success, result = self.engine.validate_evidence(
            {},
            self.test_evidence_with_implementation,
            self.test_context
        )
        self.assertIsInstance(result, dict)
        
        # Empty evidence
        success, result = self.engine.validate_evidence(
            self.test_content_valid,
            {},
            self.test_context
        )
        self.assertIsInstance(result, dict)
    
    def test_engine_independence(self):
        """Test that multiple engines work independently"""
        engine1 = EnhancedEvidenceValidationEngine()
        engine2 = EnhancedEvidenceValidationEngine()
        
        # Different validations on different engines
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
        
        # Check independent statistics
        stats1 = engine1.get_validation_statistics()
        stats2 = engine2.get_validation_statistics()
        
        self.assertEqual(stats1['total_validations'], 1)
        self.assertEqual(stats2['total_validations'], 1)

class TestPerformanceBasic(unittest.TestCase):
    """Basic performance tests"""
    
    def test_performance_is_acceptable(self):
        """Test that performance is acceptable"""
        import time
        
        engine = EnhancedEvidenceValidationEngine()
        
        test_content = {"spec.upgrade.desiredUpdate": "2.15.0"}
        test_evidence = {
            "agent_c": {"schema": {"spec.upgrade.desiredUpdate": "string"}, "implementation_found": True}
        }
        test_context = {"validation_type": "performance_test"}
        
        start_time = time.time()
        
        # Run 100 validations
        for _ in range(100):
            success, result = engine.validate_evidence(test_content, test_evidence, test_context)
            self.assertTrue(success)
        
        total_time = time.time() - start_time
        avg_time = total_time / 100
        
        # Should be fast (less than 10ms per validation)
        self.assertLess(avg_time, 0.01)
        print(f"Average validation time: {avg_time*1000:.2f}ms")

if __name__ == '__main__':
    unittest.main(verbosity=2)