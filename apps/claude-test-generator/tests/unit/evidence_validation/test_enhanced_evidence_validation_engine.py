#!/usr/bin/env python3
"""
Enhanced Evidence Validation Engine Unit Tests
==============================================

Comprehensive unit tests for the Enhanced Evidence Validation Engine testing:
- Core validation logic and evidence-based decision making
- Fiction detection capabilities and pattern recognition
- Alternative provision strategies and success optimization
- Evidence quality assessment and reliability scoring
- Learning integration and non-intrusive enhancement
- Error handling and graceful degradation
- Performance optimization and resource management

This test suite validates the critical Evidence Validation Engine components
that prevent cascade failures and ensure framework reliability.
"""

import unittest
import sys
import os
import tempfile
import json
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add the project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".claude" / "solutions"))
    from enhanced_evidence_validation_engine import (
        EnhancedEvidenceValidationEngine,
        ValidationEventType,
        ValidationResult,
        ValidationEvent,
        FictionDetectionContext,
        AlternativeContext,
        EvidenceQualityContext,
        validate_evidence,
        get_validation_insights,
        health_check
    )
    EVIDENCE_VALIDATION_AVAILABLE = True
except ImportError as e:
    EVIDENCE_VALIDATION_AVAILABLE = False
    print(f"❌ Enhanced Evidence Validation Engine not available: {e}")

try:
    from validation_learning_core import ValidationLearningCore, LearningMode
    LEARNING_CORE_AVAILABLE = True
except ImportError:
    LEARNING_CORE_AVAILABLE = False
    print("⚠️ Validation Learning Core not available for testing")


class TestEnhancedEvidenceValidationEngine(unittest.TestCase):
    """Unit tests for Enhanced Evidence Validation Engine"""
    
    @classmethod
    def setUpClass(cls):
        if not EVIDENCE_VALIDATION_AVAILABLE:
            cls.skipTest(cls, "Enhanced Evidence Validation Engine not available")
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Initialize validation engine
        self.config = {
            'learning_enabled': False,  # Disable learning for basic tests
            'storage_path': str(self.test_path)
        }
        self.engine = EnhancedEvidenceValidationEngine(self.config)
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_engine_initialization(self):
        """Test basic engine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertIsInstance(self.engine.config, dict)
        self.assertIsInstance(self.engine.validation_stats, dict)
        self.assertIsInstance(self.engine.fiction_patterns, dict)
        self.assertIsInstance(self.engine.alternative_strategies, dict)
        self.assertIsInstance(self.engine.quality_criteria, dict)
    
    def test_core_validation_fiction_detection(self):
        """Test core fiction detection functionality"""
        # Test with fictional field that should be detected
        fictional_content = {
            "spec": {
                "upgrade": {
                    "imageDigest": "sha256:abc123"  # Non-existent field
                }
            }
        }
        
        implementation_evidence = {
            "schema": {
                "spec": {
                    "upgrade": {
                        "desiredUpdate": "string"  # Real field
                    }
                }
            },
            "implementation_found": True
        }
        
        evidence_sources = {
            "agent_c": implementation_evidence,
            "agent_d": {"status": "available"}
        }
        
        context = {"validation_type": "test_fiction_detection"}
        
        success, result = self.engine.validate_evidence(fictional_content, evidence_sources, context)
        
        # Should detect fiction and return false
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.FICTION_DETECTED)
        self.assertIn('alternatives', result)
        self.assertTrue(result['evidence_backed'])
    
    def test_core_validation_success_case(self):
        """Test successful validation case"""
        # Test with valid content
        valid_content = {
            "spec": {
                "upgrade": {
                    "desiredUpdate": "v1.0.0"  # Valid field
                }
            }
        }
        
        implementation_evidence = {
            "schema": {
                "spec": {
                    "upgrade": {
                        "desiredUpdate": "string"
                    }
                }
            },
            "implementation_found": True
        }
        
        evidence_sources = {
            "agent_c": implementation_evidence,
            "agent_d": {"status": "available"}
        }
        
        context = {"validation_type": "test_success"}
        
        success, result = self.engine.validate_evidence(valid_content, evidence_sources, context)
        
        # Should succeed
        self.assertTrue(success)
        self.assertEqual(result['result'], ValidationResult.SUCCESS)
        self.assertTrue(result['comprehensive_testing_enabled'])
        self.assertTrue(result['implementation_backed'])
    
    def test_evidence_insufficient_recovery(self):
        """Test recovery guidance when evidence is insufficient"""
        content = {"test": "data"}
        
        # No implementation evidence
        evidence_sources = {
            "agent_c": {"implementation_found": False},
            "agent_d": {"status": "unknown"}
        }
        
        context = {"validation_type": "test_recovery"}
        
        success, result = self.engine.validate_evidence(content, evidence_sources, context)
        
        # Should require recovery
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.RECOVERY_NEEDED)
        self.assertIn('recovery_guidance', result)
        self.assertFalse(result['comprehensive_testing_possible'])
    
    def test_fiction_detection_patterns(self):
        """Test fiction detection with various patterns"""
        test_cases = [
            # Known fictional fields
            {"spec.upgrade.imageDigest": "test"},
            {"spec.nonExistentField": "test"},
            {"metadata.impossibleField": "test"}
        ]
        
        for fictional_content in test_cases:
            with self.subTest(content=fictional_content):
                evidence_sources = {
                    "agent_c": {"implementation_found": True, "schema": {}},
                    "agent_d": {"status": "available"}
                }
                context = {"validation_type": f"test_fiction_{list(fictional_content.keys())[0]}"}
                
                success, result = self.engine.validate_evidence(fictional_content, evidence_sources, context)
                
                self.assertFalse(success)
                self.assertEqual(result['result'], ValidationResult.FICTION_DETECTED)
    
    def test_alternative_provision(self):
        """Test alternative provision for fictional content"""
        fictional_content = {"spec.upgrade.imageDigest": "sha256:test"}
        
        evidence_sources = {
            "agent_c": {"implementation_found": True, "schema": {}},
            "agent_d": {"status": "available"}
        }
        context = {"validation_type": "test_alternatives"}
        
        success, result = self.engine.validate_evidence(fictional_content, evidence_sources, context)
        
        # Should provide alternatives
        self.assertFalse(success)
        self.assertIn('alternatives', result)
        alternatives = result['alternatives']
        self.assertIsInstance(alternatives, list)
        
        # Check alternative structure
        if alternatives:
            alt = alternatives[0]
            self.assertIn('type', alt)
            self.assertIn('original', alt)
            self.assertIn('alternative', alt)
            self.assertTrue(alt['evidence_backed'])
    
    def test_evidence_quality_assessment(self):
        """Test evidence quality assessment functionality"""
        evidence_sources = {
            "agent_c_github": {
                "type": "github_analysis",
                "completeness_score": 0.9,
                "reliability_score": 0.85,
                "freshness_score": 0.8,
                "consistency_score": 0.95
            },
            "agent_d_environment": {
                "type": "environment_analysis",
                "completeness_score": 0.7,
                "reliability_score": 0.8,
                "freshness_score": 0.9,
                "consistency_score": 0.85
            }
        }
        
        context = {"validation_type": "test_quality"}
        
        quality_assessment = self.engine._assess_evidence_quality_enhanced(evidence_sources, context)
        
        # Validate quality assessment structure
        self.assertIsInstance(quality_assessment, dict)
        for source_name in evidence_sources.keys():
            self.assertIn(source_name, quality_assessment)
            source_quality = quality_assessment[source_name]
            
            # Check required quality metrics
            required_metrics = ['completeness', 'reliability', 'freshness', 'consistency', 'weight', 'overall_score']
            for metric in required_metrics:
                self.assertIn(metric, source_quality)
                self.assertIsInstance(source_quality[metric], (int, float))
    
    def test_field_existence_in_schema(self):
        """Test schema field existence validation"""
        schema = {
            "spec": {
                "upgrade": {
                    "desiredUpdate": "string",
                    "conditions": ["array"]
                }
            },
            "metadata": {
                "name": "string"
            }
        }
        
        # Test existing fields
        self.assertTrue(self.engine._field_exists_in_schema("spec.upgrade.desiredUpdate", schema))
        self.assertTrue(self.engine._field_exists_in_schema("metadata.name", schema))
        
        # Test non-existing fields
        self.assertFalse(self.engine._field_exists_in_schema("spec.upgrade.imageDigest", schema))
        self.assertFalse(self.engine._field_exists_in_schema("metadata.impossibleField", schema))
    
    def test_comprehensive_testing_enablement(self):
        """Test comprehensive testing enablement logic"""
        # Case 1: Implementation evidence available
        impl_evidence_available = {"implementation_found": True, "schema": {}}
        deployment_evidence = {"status": "available"}
        
        can_enable = self.engine._can_enable_comprehensive_testing(impl_evidence_available, deployment_evidence)
        self.assertTrue(can_enable)
        
        # Case 2: Implementation evidence not available
        impl_evidence_missing = {"implementation_found": False}
        
        can_enable = self.engine._can_enable_comprehensive_testing(impl_evidence_missing, deployment_evidence)
        self.assertFalse(can_enable)
        
        # Case 3: No implementation evidence
        can_enable = self.engine._can_enable_comprehensive_testing({}, deployment_evidence)
        self.assertFalse(can_enable)
    
    def test_validation_statistics_tracking(self):
        """Test validation statistics tracking"""
        initial_stats = self.engine.get_validation_statistics()
        initial_total = initial_stats['total_validations']
        
        # Perform some validations
        test_content = {"test": "data"}
        test_evidence = {
            "agent_c": {"implementation_found": True},
            "agent_d": {"status": "available"}
        }
        test_context = {"validation_type": "stats_test"}
        
        # Successful validation
        self.engine.validate_evidence(test_content, test_evidence, test_context)
        
        # Fiction detection validation
        fictional_content = {"spec.upgrade.imageDigest": "test"}
        self.engine.validate_evidence(fictional_content, test_evidence, test_context)
        
        # Check updated statistics
        updated_stats = self.engine.get_validation_statistics()
        self.assertEqual(updated_stats['total_validations'], initial_total + 2)
        self.assertGreaterEqual(updated_stats['fiction_detected'], 1)
        self.assertIn('success_rate', updated_stats)
        self.assertIsInstance(updated_stats['success_rate'], float)
    
    def test_error_handling_and_graceful_degradation(self):
        """Test error handling and graceful degradation"""
        # Test with malformed content
        malformed_content = None
        evidence_sources = {"agent_c": {"implementation_found": True}}
        context = {"validation_type": "error_test"}
        
        # Should not crash and return safe result
        success, result = self.engine.validate_evidence(malformed_content, evidence_sources, context)
        self.assertIsInstance(success, bool)
        self.assertIsInstance(result, dict)
        
        # Test with malformed evidence
        test_content = {"test": "data"}
        malformed_evidence = None
        
        success, result = self.engine.validate_evidence(test_content, malformed_evidence, context)
        self.assertIsInstance(success, bool)
        self.assertIsInstance(result, dict)
    
    def test_health_check_functionality(self):
        """Test health check functionality"""
        health = self.engine.health_check()
        
        # Validate health check structure
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        self.assertIn('core_validation', health)
        self.assertIn('learning_enabled', health)
        self.assertIn('statistics', health)
        
        # Check health status values
        self.assertIn(health['status'], ['healthy', 'degraded', 'error'])
        self.assertEqual(health['core_validation'], 'operational')
        self.assertIsInstance(health['learning_enabled'], bool)
        self.assertIsInstance(health['statistics'], dict)


class TestEvidenceValidationWithLearning(unittest.TestCase):
    """Test Evidence Validation Engine with learning capabilities"""
    
    @classmethod
    def setUpClass(cls):
        if not EVIDENCE_VALIDATION_AVAILABLE:
            cls.skipTest(cls, "Enhanced Evidence Validation Engine not available")
    
    def setUp(self):
        """Set up test environment with learning enabled"""
        self.test_dir = tempfile.mkdtemp()
        
        # Mock learning components
        self.mock_learning_core = Mock()
        self.mock_pattern_memory = Mock()
        self.mock_analytics_service = Mock()
        
        # Configure learning-enabled engine
        self.config = {
            'learning_enabled': True,
            'storage_path': str(self.test_dir)
        }
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'})
    def test_learning_initialization(self):
        """Test learning component initialization"""
        try:
            import psutil
            psutil_available = True
        except ImportError:
            psutil_available = False
        
        if not psutil_available:
            self.skipTest("psutil not available - required for learning components")
        
        with patch('validation_learning_core.ValidationLearningCore') as mock_core:
            with patch('learning_services.ValidationPatternMemory') as mock_memory:
                with patch('learning_services.ValidationAnalyticsService') as mock_analytics:
                    engine = EnhancedEvidenceValidationEngine(self.config)
                    
                    # Learning should be enabled
                    self.assertTrue(engine.learning_enabled)
    
    @patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'disabled'})
    def test_learning_disabled(self):
        """Test that learning can be disabled"""
        engine = EnhancedEvidenceValidationEngine(self.config)
        
        # Learning should be disabled
        self.assertFalse(engine.learning_enabled)
        self.assertIsNone(engine.learning_core)
    
    def test_validation_event_creation(self):
        """Test validation event creation for learning"""
        engine = EnhancedEvidenceValidationEngine(self.config)
        
        # Test event type determination
        result_data = {'result': ValidationResult.FICTION_DETECTED}
        event_type = engine._determine_event_type(result_data)
        self.assertEqual(event_type, ValidationEventType.FICTION_DETECTION)
        
        result_data = {'result': ValidationResult.ALTERNATIVE_PROVIDED}
        event_type = engine._determine_event_type(result_data)
        self.assertEqual(event_type, ValidationEventType.ALTERNATIVE_PROVISION)
        
        result_data = {'result': ValidationResult.RECOVERY_NEEDED}
        event_type = engine._determine_event_type(result_data)
        self.assertEqual(event_type, ValidationEventType.RECOVERY_STRATEGY)


class TestEvidenceValidationIntegration(unittest.TestCase):
    """Test Evidence Validation Engine integration points"""
    
    @classmethod
    def setUpClass(cls):
        if not EVIDENCE_VALIDATION_AVAILABLE:
            cls.skipTest(cls, "Enhanced Evidence Validation Engine not available")
    
    def test_convenience_functions(self):
        """Test convenience functions for backward compatibility"""
        # Test validate_evidence function
        test_content = {"test": "data"}
        test_evidence = {
            "agent_c": {"implementation_found": True},
            "agent_d": {"status": "available"}
        }
        test_context = {"validation_type": "integration_test"}
        
        success, result = validate_evidence(test_content, test_evidence, test_context)
        
        self.assertIsInstance(success, bool)
        self.assertIsInstance(result, dict)
        self.assertIn('result', result)
    
    def test_health_check_function(self):
        """Test health check convenience function"""
        health = health_check()
        
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        self.assertIn('core_validation', health)
    
    def test_validation_insights_function(self):
        """Test validation insights convenience function"""
        context = {"test": "context"}
        insights = get_validation_insights(context)
        
        # Should return insights dict or None
        self.assertTrue(insights is None or isinstance(insights, dict))


class TestEvidenceValidationRealWorldScenarios(unittest.TestCase):
    """Test Evidence Validation Engine with real-world scenarios"""
    
    @classmethod
    def setUpClass(cls):
        if not EVIDENCE_VALIDATION_AVAILABLE:
            cls.skipTest(cls, "Enhanced Evidence Validation Engine not available")
    
    def setUp(self):
        """Set up for real-world scenario testing"""
        self.engine = EnhancedEvidenceValidationEngine()
    
    def test_acm_22079_scenario_fiction_detection(self):
        """Test ACM-22079 scenario - should detect fictional UI elements"""
        # ClusterCurator imageDigest field that doesn't exist
        acm_content = {
            "spec": {
                "upgrade": {
                    "imageDigest": "sha256:abc123"  # Fictional field
                }
            }
        }
        
        # Real ClusterCurator schema without imageDigest
        acm_evidence = {
            "agent_c": {
                "schema": {
                    "spec": {
                        "upgrade": {
                            "desiredUpdate": "string",
                            "conditions": ["array"]
                        }
                    }
                },
                "implementation_found": True
            },
            "agent_d": {
                "status": "not_deployed",
                "ui_capabilities": "not_found"
            }
        }
        
        context = {
            "validation_type": "acm_22079_regression_test",
            "jira_ticket": "ACM-22079"
        }
        
        success, result = self.engine.validate_evidence(acm_content, acm_evidence, context)
        
        # Should detect fiction and provide alternatives
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.FICTION_DETECTED)
        self.assertIn('alternatives', result)
        
        # Should suggest desiredUpdate as alternative
        alternatives = result['alternatives']
        if alternatives:
            alt_fields = [alt.get('alternative', '') for alt in alternatives]
            self.assertIn('spec.upgrade.desiredUpdate', alt_fields)
    
    def test_successful_validation_scenario(self):
        """Test successful validation with proper evidence"""
        # Valid ClusterCurator upgrade configuration
        valid_content = {
            "spec": {
                "upgrade": {
                    "desiredUpdate": "quay.io/stolostron/cluster-curator:v1.0.0"
                }
            }
        }
        
        # Evidence supporting this configuration
        valid_evidence = {
            "agent_c": {
                "schema": {
                    "spec": {
                        "upgrade": {
                            "desiredUpdate": "string"
                        }
                    }
                },
                "implementation_found": True,
                "github_evidence": {
                    "pr_analysis": "PR #468 implements desiredUpdate field",
                    "file_changes": "cluster-curator-controller updates"
                }
            },
            "agent_d": {
                "status": "available",
                "environment_type": "disconnected",
                "cli_available": True
            }
        }
        
        context = {
            "validation_type": "successful_scenario",
            "customer": "amadeus",
            "environment": "disconnected"
        }
        
        success, result = self.engine.validate_evidence(valid_content, valid_evidence, context)
        
        # Should succeed and enable comprehensive testing
        self.assertTrue(success)
        self.assertEqual(result['result'], ValidationResult.SUCCESS)
        self.assertTrue(result['comprehensive_testing_enabled'])
        self.assertTrue(result['implementation_backed'])
    
    def test_multiple_field_validation(self):
        """Test validation with multiple fields"""
        complex_content = {
            "spec": {
                "upgrade": {
                    "desiredUpdate": "v1.0.0",        # Valid
                    "imageDigest": "sha256:abc123",   # Invalid
                    "conditions": ["Ready"]           # Valid
                }
            }
        }
        
        evidence = {
            "agent_c": {
                "schema": {
                    "spec": {
                        "upgrade": {
                            "desiredUpdate": "string",
                            "conditions": ["array"]
                            # imageDigest not in schema
                        }
                    }
                },
                "implementation_found": True
            },
            "agent_d": {"status": "available"}
        }
        
        context = {"validation_type": "multiple_field_test"}
        
        success, result = self.engine.validate_evidence(complex_content, evidence, context)
        
        # Should detect fiction due to imageDigest field
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.FICTION_DETECTED)


if __name__ == '__main__':
    print("🧪 Enhanced Evidence Validation Engine Unit Tests")
    print("=" * 60)
    print("Testing evidence validation, fiction detection, and learning capabilities")
    print("=" * 60)
    
    # Check availability
    if not EVIDENCE_VALIDATION_AVAILABLE:
        print("❌ Enhanced Evidence Validation Engine not available - skipping tests")
        exit(1)
    
    # Run tests with detailed output
    unittest.main(verbosity=2)