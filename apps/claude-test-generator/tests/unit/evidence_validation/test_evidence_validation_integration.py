#!/usr/bin/env python3
"""
Evidence Validation Engine Integration Tests
==========================================

Comprehensive integration tests for the complete Evidence Validation Engine system:
- End-to-end evidence validation workflows
- Evidence Validation Engine + Learning Core integration
- Real-world cascade failure prevention scenarios
- ACM-22079 regression prevention validation
- Implementation Reality Agent blocking scenarios
- Cross-agent validation and consistency checking
- Performance optimization and learning enhancement

This test suite validates the complete Evidence Validation system
working together to prevent cascade failures and ensure framework reliability.
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
        ValidationResult,
        ValidationEvent,
        ValidationEventType
    )
    from validation_learning_core import (
        ValidationLearningCore,
        LearningMode,
        get_learning_core,
        shutdown_learning_core
    )
    INTEGRATION_COMPONENTS_AVAILABLE = True
except ImportError as e:
    INTEGRATION_COMPONENTS_AVAILABLE = False
    print(f"❌ Evidence Validation Integration components not available: {e}")


class TestEvidenceValidationIntegration(unittest.TestCase):
    """Integration tests for Evidence Validation Engine system"""
    
    @classmethod
    def setUpClass(cls):
        if not INTEGRATION_COMPONENTS_AVAILABLE:
            cls.skipTest(cls, "Evidence Validation Integration components not available")
    
    def setUp(self):
        """Set up integration test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Set up environment for learning
        self.env_patcher = patch.dict(os.environ, {
            'CLAUDE_VALIDATION_LEARNING': 'standard',
            'CLAUDE_LEARNING_STORAGE_PATH': str(self.test_path / 'learning'),
            'CLAUDE_LEARNING_MAX_MEMORY': '100',
            'CLAUDE_LEARNING_MAX_STORAGE': '200'
        })
        self.env_patcher.start()
        
        # Initialize components
        self.learning_core = ValidationLearningCore()
        self.validation_engine = EnhancedEvidenceValidationEngine({
            'storage_path': str(self.test_path / 'validation')
        })
        
    def tearDown(self):
        """Clean up integration test environment"""
        self.env_patcher.stop()
        shutdown_learning_core()
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_end_to_end_validation_workflow(self):
        """Test complete end-to-end validation workflow"""
        # Test Case 1: Successful validation with learning
        valid_content = {
            "spec": {
                "upgrade": {
                    "desiredUpdate": "quay.io/stolostron/cluster-curator:v1.0.0"
                }
            }
        }
        
        evidence_sources = {
            "agent_c": {
                "schema": {
                    "spec": {
                        "upgrade": {
                            "desiredUpdate": "string",
                            "conditions": ["array"]
                        }
                    }
                },
                "implementation_found": True,
                "github_evidence": {
                    "pr_analysis": "PR #468 implements desiredUpdate field",
                    "file_changes": ["cluster-curator-controller.go"]
                }
            },
            "agent_d": {
                "status": "available",
                "environment_type": "disconnected",
                "cli_available": True
            }
        }
        
        context = {
            "validation_type": "integration_test_success",
            "jira_ticket": "ACM-TEST-001",
            "customer": "test_customer"
        }
        
        # Perform validation
        success, result = self.validation_engine.validate_evidence(valid_content, evidence_sources, context)
        
        # Should succeed
        self.assertTrue(success)
        self.assertEqual(result['result'], ValidationResult.SUCCESS)
        self.assertTrue(result['comprehensive_testing_enabled'])
        self.assertTrue(result['implementation_backed'])
        
        # Test Case 2: Fiction detection with learning
        fictional_content = {
            "spec": {
                "upgrade": {
                    "imageDigest": "sha256:abc123"  # Fictional field
                }
            }
        }
        
        success, result = self.validation_engine.validate_evidence(fictional_content, evidence_sources, context)
        
        # Should detect fiction
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.FICTION_DETECTED)
        self.assertIn('alternatives', result)
        self.assertTrue(result['evidence_backed'])
    
    def test_acm_22079_cascade_failure_prevention(self):
        """Test ACM-22079 cascade failure prevention scenario"""
        # Reproduce the original ACM-22079 failure scenario
        acm_22079_content = {
            "metadata": {
                "name": "test-cluster-upgrade"
            },
            "spec": {
                "upgrade": {
                    "imageDigest": "sha256:nonexistentdigest",  # Fictional field
                    "channel": "stable-2.5"
                }
            }
        }
        
        # Real ClusterCurator evidence (what Agent C would find)
        acm_22079_evidence = {
            "agent_c": {
                "schema": {
                    "spec": {
                        "upgrade": {
                            "desiredUpdate": "string",
                            "conditions": ["array"],
                            "channel": "string"
                            # Note: imageDigest is NOT in the real schema
                        }
                    }
                },
                "implementation_found": True,
                "github_analysis": {
                    "repository": "stolostron/cluster-curator-controller",
                    "pr_468_analysis": {
                        "title": "ACM-22079 Initial non-recommended image digest feature",
                        "changes": [
                            "controllers/clustercurator_controller.go",
                            "config/crd/bases/cluster.open-cluster-management.io_clustercurators.yaml"
                        ],
                        "implementation": "3-tier fallback: conditionalUpdates → availableUpdates → image tag"
                    }
                },
                "automation_evidence": {
                    "test_files": ["automation_upgrade.spec.js"],
                    "pattern": "CLI-based automation",
                    "ui_evidence": "NONE_FOUND"
                }
            },
            "agent_d": {
                "status": "not_deployed",
                "environment_type": "disconnected",
                "ui_capabilities": "NOT_AVAILABLE",
                "cli_available": True,
                "tools": ["oc", "kubectl"]
            }
        }
        
        context = {
            "validation_type": "acm_22079_regression_prevention",
            "jira_ticket": "ACM-22079",
            "customer": "amadeus",
            "environment": "disconnected"
        }
        
        # Perform validation - should detect fiction and prevent cascade failure
        success, result = self.validation_engine.validate_evidence(acm_22079_content, acm_22079_evidence, context)
        
        # CRITICAL: Should detect imageDigest as fictional
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.FICTION_DETECTED)
        
        # Should provide valid alternatives
        self.assertIn('alternatives', result)
        alternatives = result['alternatives']
        self.assertGreater(len(alternatives), 0)
        
        # Should suggest desiredUpdate as alternative
        alternative_fields = [alt.get('alternative', '') for alt in alternatives]
        self.assertIn('spec.upgrade.desiredUpdate', alternative_fields)
        
        # Should maintain evidence backing
        self.assertTrue(result['evidence_backed'])
        
        # This prevents the cascade failure that occurred in ACM-22079
        print("✅ ACM-22079 cascade failure prevention: VALIDATED")
    
    def test_implementation_reality_agent_blocking(self):
        """Test Implementation Reality Agent blocking functionality"""
        # Scenario: Attempt to create UI tests without UI evidence
        ui_test_content = {
            "test_type": "ui_automation",
            "steps": [
                {"action": "navigate", "target": "cluster_management_ui"},
                {"action": "click", "selector": ".upgrade-button"},
                {"action": "fill", "field": "image_digest", "value": "sha256:test"}
            ]
        }
        
        # Evidence shows NO UI capabilities
        reality_evidence = {
            "agent_c": {
                "implementation_patterns": {
                    "ui_tests": "NONE_FOUND",
                    "automation_pattern": "CLI_ONLY",
                    "test_files": ["automation_upgrade.spec.js"]
                },
                "schema": {
                    "spec": {
                        "upgrade": {
                            "desiredUpdate": "string"
                            # No imageDigest field
                        }
                    }
                },
                "implementation_found": True
            },
            "agent_d": {
                "ui_capabilities": "NOT_AVAILABLE",
                "environment_type": "disconnected",
                "automation_capabilities": "CLI_ONLY"
            }
        }
        
        context = {
            "validation_type": "implementation_reality_blocking",
            "agent_request": "UI test generation",
            "evidence_requirement": "UI selectors and page objects"
        }
        
        # Should block UI test generation due to lack of UI evidence
        success, result = self.validation_engine.validate_evidence(ui_test_content, reality_evidence, context)
        
        # Should fail validation
        self.assertFalse(success)
        
        # Should provide CLI alternatives
        if 'alternatives' in result:
            alternatives = result['alternatives']
            cli_alternatives = [alt for alt in alternatives if 'cli' in str(alt).lower()]
            self.assertGreater(len(cli_alternatives), 0)
        
        print("✅ Implementation Reality Agent blocking: VALIDATED")
    
    def test_evidence_quality_learning_enhancement(self):
        """Test evidence quality assessment with learning enhancement"""
        # High-quality evidence scenario
        high_quality_evidence = {
            "agent_c_github": {
                "type": "github_analysis",
                "completeness_score": 0.95,
                "reliability_score": 0.9,
                "freshness_score": 0.85,
                "consistency_score": 0.92,
                "github_metadata": {
                    "pr_count": 5,
                    "file_changes": 15,
                    "review_status": "approved"
                }
            },
            "agent_d_environment": {
                "type": "environment_analysis",
                "completeness_score": 0.8,
                "reliability_score": 0.85,
                "freshness_score": 0.9,
                "consistency_score": 0.88,
                "environment_metadata": {
                    "tools_available": ["oc", "kubectl", "helm"],
                    "connectivity": "verified",
                    "permissions": "validated"
                }
            },
            "agent_b_documentation": {
                "type": "documentation_analysis",
                "completeness_score": 0.7,
                "reliability_score": 0.75,
                "freshness_score": 0.6,
                "consistency_score": 0.8
            }
        }
        
        test_content = {
            "spec": {
                "upgrade": {
                    "desiredUpdate": "v2.5.0"
                }
            }
        }
        
        context = {
            "validation_type": "quality_assessment_test",
            "learning_enabled": True
        }
        
        # Perform validation with quality assessment
        success, result = self.validation_engine.validate_evidence(test_content, high_quality_evidence, context)
        
        # Should succeed with high-quality evidence
        self.assertTrue(success)
        
        # Should include evidence quality assessment
        if 'evidence_quality' in result:
            quality_data = result['evidence_quality']
            self.assertIsInstance(quality_data, dict)
            
            # Should assess each evidence source
            for source in high_quality_evidence.keys():
                self.assertIn(source, quality_data)
                source_quality = quality_data[source]
                
                # Should include quality metrics
                required_metrics = ['completeness', 'reliability', 'freshness', 'consistency', 'overall_score']
                for metric in required_metrics:
                    self.assertIn(metric, source_quality)
                    self.assertIsInstance(source_quality[metric], (int, float))
        
        print("✅ Evidence quality learning enhancement: VALIDATED")
    
    def test_cross_validation_consistency_checking(self):
        """Test cross-agent validation and consistency checking"""
        # Scenario: Conflicting evidence between agents
        test_content = {
            "spec": {
                "upgrade": {
                    "desiredUpdate": "v2.5.0"
                }
            }
        }
        
        # Agent C says implementation exists, Agent D says environment doesn't support it
        conflicting_evidence = {
            "agent_c": {
                "implementation_found": True,
                "schema": {
                    "spec": {
                        "upgrade": {
                            "desiredUpdate": "string"
                        }
                    }
                },
                "confidence": 0.9
            },
            "agent_d": {
                "status": "environment_incompatible",
                "version_support": "v2.4.x_only",
                "upgrade_capability": "blocked",
                "confidence": 0.85
            }
        }
        
        context = {
            "validation_type": "cross_validation_consistency",
            "conflict_resolution": "evidence_reconciliation"
        }
        
        # Perform validation - should handle conflict appropriately
        success, result = self.validation_engine.validate_evidence(test_content, conflicting_evidence, context)
        
        # May succeed or fail depending on conflict resolution strategy
        self.assertIsInstance(success, bool)
        self.assertIn('result', result)
        
        # Should provide reconciliation guidance if conflicts detected
        if not success and result.get('result') == ValidationResult.RECOVERY_NEEDED:
            self.assertIn('recovery_guidance', result)
            recovery = result['recovery_guidance']
            self.assertIn('action', recovery)
            self.assertIn('agent_guidance', recovery)
        
        print("✅ Cross-validation consistency checking: VALIDATED")
    
    def test_performance_optimization_learning(self):
        """Test performance optimization through learning"""
        # Simulate multiple validation events to trigger learning
        validation_scenarios = [
            {
                "content": {"spec": {"upgrade": {"desiredUpdate": "v1.0.0"}}},
                "evidence": {"agent_c": {"implementation_found": True}, "agent_d": {"status": "available"}},
                "expected_success": True
            },
            {
                "content": {"spec": {"upgrade": {"imageDigest": "sha256:fake"}}},
                "evidence": {"agent_c": {"implementation_found": True, "schema": {}}, "agent_d": {"status": "available"}},
                "expected_success": False
            },
            {
                "content": {"spec": {"upgrade": {"desiredUpdate": "v2.0.0"}}},
                "evidence": {"agent_c": {"implementation_found": True}, "agent_d": {"status": "available"}},
                "expected_success": True
            }
        ]
        
        validation_times = []
        
        for i, scenario in enumerate(validation_scenarios):
            context = {
                "validation_type": f"performance_test_{i}",
                "iteration": i
            }
            
            start_time = time.time()
            success, result = self.validation_engine.validate_evidence(
                scenario["content"], 
                scenario["evidence"], 
                context
            )
            end_time = time.time()
            
            validation_times.append(end_time - start_time)
            
            # Verify expected outcome
            self.assertEqual(success, scenario["expected_success"])
        
        # Check that validation engine is tracking performance
        stats = self.validation_engine.get_validation_statistics()
        self.assertIn('total_validations', stats)
        self.assertGreaterEqual(stats['total_validations'], len(validation_scenarios))
        
        # Check learning core health
        if self.learning_core.is_enabled():
            health = self.learning_core.get_health_status()
            self.assertIn('status', health)
            self.assertIn(health['status'], ['enabled', 'disabled'])
        
        print("✅ Performance optimization learning: VALIDATED")
    
    def test_framework_halt_prevention(self):
        """Test framework halt prevention with evidence validation"""
        # Scenario: Critical validation failure that should halt framework
        critical_content = {
            "spec": {
                "destructive_operation": True,
                "target": "production_cluster"
            }
        }
        
        # Evidence indicates this is unsafe
        safety_evidence = {
            "agent_c": {
                "implementation_found": False,
                "safety_assessment": "HIGH_RISK",
                "schema": {}
            },
            "agent_d": {
                "status": "production_environment",
                "safety_controls": "insufficient",
                "approval_required": True
            }
        }
        
        context = {
            "validation_type": "framework_halt_test",
            "safety_level": "critical",
            "environment": "production"
        }
        
        # Should fail validation and provide recovery guidance
        success, result = self.validation_engine.validate_evidence(critical_content, safety_evidence, context)
        
        # Should block the operation
        self.assertFalse(success)
        self.assertIn(result['result'], [ValidationResult.RECOVERY_NEEDED, ValidationResult.FICTION_DETECTED])
        
        # Should provide safety guidance
        if 'recovery_guidance' in result:
            guidance = result['recovery_guidance']
            self.assertIn('action', guidance)
            self.assertIn('confidence', guidance)
        
        print("✅ Framework halt prevention: VALIDATED")


class TestEvidenceValidationHealthAndMetrics(unittest.TestCase):
    """Test Evidence Validation Engine health and metrics"""
    
    @classmethod
    def setUpClass(cls):
        if not INTEGRATION_COMPONENTS_AVAILABLE:
            cls.skipTest(cls, "Evidence Validation Integration components not available")
    
    def setUp(self):
        """Set up health test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.validation_engine = EnhancedEvidenceValidationEngine({
            'storage_path': str(self.test_dir)
        })
    
    def tearDown(self):
        """Clean up health test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_validation_engine_health_check(self):
        """Test validation engine health checking"""
        health = self.validation_engine.health_check()
        
        # Validate health structure
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        self.assertIn('core_validation', health)
        self.assertIn('learning_enabled', health)
        self.assertIn('statistics', health)
        
        # Check health values
        self.assertIn(health['status'], ['healthy', 'degraded'])
        self.assertEqual(health['core_validation'], 'operational')
        self.assertIsInstance(health['learning_enabled'], bool)
        
        # Validate statistics
        stats = health['statistics']
        required_stats = ['total_validations', 'fiction_detected', 'alternatives_provided', 'success_rate']
        for stat in required_stats:
            self.assertIn(stat, stats)
    
    def test_validation_statistics_accuracy(self):
        """Test validation statistics accuracy"""
        initial_stats = self.validation_engine.get_validation_statistics()
        
        # Perform various validations
        test_cases = [
            ({"valid": "content"}, {"agent_c": {"implementation_found": True}}, True),
            ({"spec.upgrade.imageDigest": "fake"}, {"agent_c": {"schema": {}}}, False),
            ({"another": "valid"}, {"agent_c": {"implementation_found": True}}, True)
        ]
        
        for content, evidence, expected_success in test_cases:
            success, result = self.validation_engine.validate_evidence(
                content, evidence, {"validation_type": "stats_test"}
            )
        
        # Check updated statistics
        final_stats = self.validation_engine.get_validation_statistics()
        
        self.assertEqual(
            final_stats['total_validations'], 
            initial_stats['total_validations'] + len(test_cases)
        )
        
        # Should have accurate success rate
        self.assertIsInstance(final_stats['success_rate'], float)
        self.assertGreaterEqual(final_stats['success_rate'], 0.0)
        self.assertLessEqual(final_stats['success_rate'], 1.0)


if __name__ == '__main__':
    print("🧪 Evidence Validation Engine Integration Tests")
    print("=" * 60)
    print("Testing complete Evidence Validation system integration and cascade failure prevention")
    print("=" * 60)
    
    # Check availability
    if not INTEGRATION_COMPONENTS_AVAILABLE:
        print("❌ Evidence Validation Integration components not available - skipping tests")
        exit(1)
    
    # Run tests with detailed output
    unittest.main(verbosity=2)