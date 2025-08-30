#!/usr/bin/env python3
"""
Unit Tests for Evidence Validation Engine
Tests the core functionality of evidence validation and false positive prevention
"""

import unittest
import json
import time
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List

# Add source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from services.evidence_validation_engine import (
    EvidenceValidationEngine,
    ValidationCheck,
    ValidationSummary,
    EvidenceValidationResult,
    ValidationType,
    ValidationResult
)


class TestEvidenceValidationEngine(unittest.TestCase):
    """
    Test suite for Evidence Validation Engine
    
    CRITICAL TESTING GOALS:
    1. Test file extension validation accuracy
    2. Test dependency claim verification
    3. Test citation validation
    4. Test false positive pattern detection
    5. Test overall validation accuracy and confidence scoring
    """
    
    def setUp(self):
        """Set up test environment"""
        self.engine = EvidenceValidationEngine()
        self.sample_investigation_data = self._create_sample_investigation_data()
        
    def _create_sample_investigation_data(self) -> Dict[str, Any]:
        """Create sample investigation data for testing"""
        return {
            'jenkins_intelligence': {
                'metadata': {
                    'job_name': 'test-pipeline',
                    'build_number': 123,
                    'build_result': 'FAILURE'
                },
                'failure_analysis': {
                    'primary_failure_type': 'timeout_errors'
                }
            },
            'repository_analysis': {
                'repository_cloned': True,
                'branch_analyzed': 'release-2.9',
                'test_files_found': [
                    'tests/e2e/cluster_test.js',
                    'tests/e2e/application_test.js',
                    'cypress/integration/login.js'
                ],
                'dependency_analysis': {
                    'framework': 'cypress',
                    'version': '12.17.0',
                    'dependencies_healthy': True
                }
            },
            'environment_validation': {
                'cluster_connectivity': True,
                'environment_score': 0.85
            }
        }

    # CRITICAL TEST 1: File Extension Validation Accuracy
    def test_file_extension_validation_accuracy(self):
        """
        CRITICAL: Test file extension validation for preventing false positives
        """
        test_cases = [
            {
                "name": "Correct JS Extension Claim",
                "claim": "Found 3 .js files in the test directory",
                "expected_result": ValidationResult.VERIFIED,
                "expected_confidence_min": 0.9
            },
            {
                "name": "False Positive: .cy.js vs .js",
                "claim": "Found .cy.js files when actual files are .js",
                "expected_result": ValidationResult.FAILED,
                "expected_confidence_min": 0.8
            },
            {
                "name": "No File Data Available",
                "claim": "Found .ts files in repository",
                "investigation_data": {
                    'repository_analysis': {
                        'test_files_found': []
                    }
                },
                "expected_result": ValidationResult.UNABLE_TO_VERIFY
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                investigation_data = case.get('investigation_data', self.sample_investigation_data)
                
                # Test the file extension validation specifically
                check = self.engine._validate_file_extensions(
                    case["claim"], 
                    investigation_data, 
                    time.time()
                )
                
                self.assertEqual(check.result, case["expected_result"])
                self.assertEqual(check.check_type, ValidationType.EXTENSION_VERIFICATION)
                
                if "expected_confidence_min" in case:
                    self.assertGreaterEqual(check.confidence, case["expected_confidence_min"])
                
                # Validate evidence structure
                self.assertIsInstance(check.evidence, list)
                self.assertGreater(len(check.evidence), 0)

    # CRITICAL TEST 2: Dependency Claim Verification
    def test_dependency_claim_verification(self):
        """
        CRITICAL: Test dependency validation for preventing false dependency claims
        """
        test_cases = [
            {
                "name": "Valid Cypress Dependency Claim",
                "claim": "Using Cypress framework version 12.17.0",
                "expected_result": ValidationResult.VERIFIED,
                "expected_confidence_min": 0.8
            },
            {
                "name": "False Positive: MobX Claim Without Verification",
                "claim": "MobX dependency version conflict detected",
                "expected_result": ValidationResult.FAILED,
                "expected_confidence_min": 0.8
            },
            {
                "name": "No Dependency Data Available",
                "claim": "React version incompatibility found",
                "investigation_data": {
                    'repository_analysis': {
                        'dependency_analysis': {}
                    }
                },
                "expected_result": ValidationResult.UNABLE_TO_VERIFY
            },
            {
                "name": "General Dependency Claim",
                "claim": "Package dependencies are healthy",
                "expected_result": ValidationResult.PARTIALLY_VERIFIED
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                investigation_data = case.get('investigation_data', self.sample_investigation_data)
                
                check = self.engine._validate_dependency_claims(
                    case["claim"],
                    investigation_data,
                    time.time()
                )
                
                self.assertEqual(check.result, case["expected_result"])
                self.assertEqual(check.check_type, ValidationType.DEPENDENCY_VERIFICATION)
                
                if "expected_confidence_min" in case:
                    self.assertGreaterEqual(check.confidence, case["expected_confidence_min"])

    # CRITICAL TEST 3: Citation Validation
    def test_citation_validation(self):
        """
        CRITICAL: Test citation validation for ensuring evidence backing
        """
        test_cases = [
            {
                "name": "Valid Jenkins Citation",
                "claim": "[Jenkins:test-pipeline:123:FAILURE] shows timeout errors",
                "expected_result": ValidationResult.VERIFIED,
                "expected_confidence_min": 0.8
            },
            {
                "name": "Valid Repository Citation",
                "claim": "[Repo:release-2.9:tests/cluster.js] contains test logic",
                "expected_result": ValidationResult.VERIFIED,
                "expected_confidence_min": 0.8
            },
            {
                "name": "Multiple Citations Mixed Validity",
                "claim": "[Jenkins:test-pipeline:123:FAILURE] and [Repo:branch:file.js] analysis",
                "investigation_data": {
                    'jenkins_intelligence': {'metadata': {'job_name': 'test-pipeline'}},
                    'repository_analysis': {'repository_cloned': False}  # Repo citation will fail
                },
                "expected_result": ValidationResult.PARTIALLY_VERIFIED
            },
            {
                "name": "No Citations to Verify",
                "claim": "Test failure occurred due to timeout",
                "expected_result": ValidationResult.UNABLE_TO_VERIFY
            },
            {
                "name": "Citations Without Supporting Data",
                "claim": "[Jenkins:missing:999:FAILURE] reference",
                "investigation_data": {
                    'jenkins_intelligence': {'metadata': {}},
                    'repository_analysis': {'repository_cloned': False}
                },
                "expected_result": ValidationResult.FAILED
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                investigation_data = case.get('investigation_data', self.sample_investigation_data)
                
                check = self.engine._validate_citation_claims(
                    case["claim"],
                    investigation_data,
                    time.time()
                )
                
                self.assertEqual(check.result, case["expected_result"])
                self.assertEqual(check.check_type, ValidationType.CITATION_VERIFICATION)
                
                if "expected_confidence_min" in case:
                    self.assertGreaterEqual(check.confidence, case["expected_confidence_min"])

    # CRITICAL TEST 4: False Positive Pattern Detection
    def test_false_positive_pattern_detection(self):
        """
        CRITICAL: Test detection of known false positive patterns
        """
        test_cases = [
            {
                "name": "File Extension Mismatch Pattern",
                "claim": "Found .cy.js files when actual files are .js",
                "should_detect": True
            },
            {
                "name": "MobX Without Verification Pattern",
                "claim": "MobX dependency issues without package.json verification",
                "should_detect": True
            },
            {
                "name": "Overconfident Validation Pattern",
                "claim": "All verified without actual verification process",
                "should_detect": True
            },
            {
                "name": "Valid Technical Claim",
                "claim": "Cypress timeout errors detected in console log",
                "should_detect": False
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                result = self.engine._check_false_positive_patterns(case["claim"], time.time())
                
                if case["should_detect"]:
                    self.assertIsNotNone(result, f"Should detect false positive in: {case['claim']}")
                    self.assertEqual(result.result, ValidationResult.FAILED)
                    self.assertGreaterEqual(result.confidence, 0.9)
                else:
                    self.assertIsNone(result, f"Should not detect false positive in: {case['claim']}")

    # CRITICAL TEST 5: Claim Type Detection
    def test_claim_type_detection(self):
        """
        CRITICAL: Test accurate detection of different claim types
        """
        test_cases = [
            {
                "name": "File Extension Claims",
                "claims": [
                    "Found 147 .js files in repository",
                    "Test files use .cy.js extension",
                    "TypeScript files with .tsx extension"
                ],
                "detection_method": "_is_file_extension_claim",
                "expected": True
            },
            {
                "name": "Dependency Claims",
                "claims": [
                    "MobX version conflict detected",
                    "Cypress framework version 12.17.0",
                    "package.json contains dependencies"
                ],
                "detection_method": "_is_dependency_claim",
                "expected": True
            },
            {
                "name": "Citation Claims",
                "claims": [
                    "[Jenkins:test:123:FAILURE] shows errors",
                    "[Repo:main:file.js:45] contains code",
                    "https://jenkins.example.com/job/test/123/"
                ],
                "detection_method": "_is_citation_claim",
                "expected": True
            },
            {
                "name": "Non-matching Claims",
                "claims": [
                    "Test execution completed successfully",
                    "Performance analysis shows improvement"
                ],
                "detection_method": "_is_file_extension_claim",
                "expected": False
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                detection_method = getattr(self.engine, case["detection_method"])
                
                for claim in case["claims"]:
                    result = detection_method(claim)
                    self.assertEqual(result, case["expected"], 
                                   f"Detection failed for: {claim}")

    # CRITICAL TEST 6: Complete Validation Pipeline
    def test_complete_validation_pipeline(self):
        """
        CRITICAL: Test complete technical claims validation pipeline
        """
        test_claims = [
            "Found 147 .js files in the repository analysis",  # Valid extension claim
            "MobX dependency error without package.json verification",  # False positive
            "[Jenkins:test-pipeline:123:FAILURE] shows timeout errors",  # Valid citation
            "Cypress framework version 12.17.0 detected",  # Valid dependency
            "All issues verified without proper validation",  # False positive pattern
            "Test execution performance improved by 25%"  # General claim
        ]
        
        result = self.engine.validate_technical_claims(test_claims, self.sample_investigation_data)
        
        # Validate result structure
        self.assertIsInstance(result, EvidenceValidationResult)
        self.assertIsInstance(result.checks, list)
        self.assertIsInstance(result.summary, ValidationSummary)
        self.assertIsInstance(result.validated_claims, list)
        self.assertIsInstance(result.rejected_claims, list)
        self.assertIsInstance(result.confidence_score, float)
        
        # Validate summary statistics
        self.assertGreater(result.summary.total_checks, 0)
        self.assertEqual(result.summary.total_checks, len(result.checks))
        self.assertGreaterEqual(result.summary.overall_accuracy, 0.0)
        self.assertLessEqual(result.summary.overall_accuracy, 1.0)
        
        # Should detect and reject false positive claims
        self.assertGreater(len(result.rejected_claims), 0, "Should reject some false positive claims")
        
        # Should validate legitimate claims
        self.assertGreater(len(result.validated_claims), 0, "Should validate legitimate claims")
        
        # Overall confidence should be reasonable
        self.assertGreater(result.confidence_score, 0.3)
        self.assertLessEqual(result.confidence_score, 1.0)

    # CRITICAL TEST 7: Validation Summary Generation
    def test_validation_summary_generation(self):
        """
        CRITICAL: Test validation summary statistics accuracy
        """
        # Create sample validation checks
        sample_checks = [
            ValidationCheck(
                check_type=ValidationType.EXTENSION_VERIFICATION,
                claim="test claim 1",
                result=ValidationResult.VERIFIED,
                confidence=0.9,
                evidence=["evidence 1"],
                verification_method="test_method",
                timestamp=time.time()
            ),
            ValidationCheck(
                check_type=ValidationType.DEPENDENCY_VERIFICATION,
                claim="test claim 2",
                result=ValidationResult.FAILED,
                confidence=0.8,
                evidence=["evidence 2"],
                verification_method="test_method",
                timestamp=time.time()
            ),
            ValidationCheck(
                check_type=ValidationType.CITATION_VERIFICATION,
                claim="test claim 3",
                result=ValidationResult.PARTIALLY_VERIFIED,
                confidence=0.7,
                evidence=["evidence 3"],
                verification_method="test_method",
                timestamp=time.time()
            ),
            ValidationCheck(
                check_type=ValidationType.TECHNICAL_CLAIM_VERIFICATION,
                claim="test claim 4",
                result=ValidationResult.UNABLE_TO_VERIFY,
                confidence=0.5,
                evidence=["evidence 4"],
                verification_method="test_method",
                timestamp=time.time()
            )
        ]
        
        summary = self.engine._generate_validation_summary(sample_checks)
        
        # Validate summary counts
        self.assertEqual(summary.total_checks, 4)
        self.assertEqual(summary.verified_count, 1)
        self.assertEqual(summary.failed_count, 1)
        self.assertEqual(summary.partially_verified_count, 1)
        self.assertEqual(summary.unable_to_verify_count, 1)
        
        # Validate accuracy calculation: (1 + 0.5*1) / 4 = 0.375
        expected_accuracy = (1 + 0.5 * 1) / 4
        self.assertAlmostEqual(summary.overall_accuracy, expected_accuracy, places=2)
        
        # Validate false positive risk: 1/4 = 0.25
        expected_fp_risk = 1 / 4
        self.assertAlmostEqual(summary.false_positive_risk, expected_fp_risk, places=2)

    # CRITICAL TEST 8: Claim Categorization Logic
    def test_claim_categorization_logic(self):
        """
        CRITICAL: Test claim categorization into validated vs rejected
        """
        claims = ["claim1", "claim2", "claim3", "claim4"]
        
        checks = [
            # claim1: verified
            ValidationCheck(
                check_type=ValidationType.EXTENSION_VERIFICATION,
                claim="claim1",
                result=ValidationResult.VERIFIED,
                confidence=0.9,
                evidence=[],
                verification_method="test",
                timestamp=time.time()
            ),
            # claim2: failed
            ValidationCheck(
                check_type=ValidationType.DEPENDENCY_VERIFICATION,
                claim="claim2",
                result=ValidationResult.FAILED,
                confidence=0.8,
                evidence=[],
                verification_method="test",
                timestamp=time.time()
            ),
            # claim3: partially verified (should be validated)
            ValidationCheck(
                check_type=ValidationType.CITATION_VERIFICATION,
                claim="claim3",
                result=ValidationResult.PARTIALLY_VERIFIED,
                confidence=0.7,
                evidence=[],
                verification_method="test",
                timestamp=time.time()
            )
            # claim4: no checks (should be validated by default)
        ]
        
        validated, rejected = self.engine._categorize_claims(claims, checks)
        
        # Validate categorization results
        self.assertIn("claim1", validated)  # Verified
        self.assertIn("claim2", rejected)   # Failed
        self.assertIn("claim3", validated)  # Partially verified
        self.assertIn("claim4", validated)  # No checks, default to validated
        
        self.assertEqual(len(validated), 3)
        self.assertEqual(len(rejected), 1)

    # CRITICAL TEST 9: Confidence Score Calculation
    def test_confidence_score_calculation(self):
        """
        CRITICAL: Test validation confidence score calculation accuracy
        """
        test_cases = [
            {
                "name": "High Confidence Scenario",
                "checks": [
                    ValidationCheck(
                        ValidationType.EXTENSION_VERIFICATION, "claim", ValidationResult.VERIFIED,
                        0.9, [], "test", time.time()
                    ),
                    ValidationCheck(
                        ValidationType.DEPENDENCY_VERIFICATION, "claim", ValidationResult.VERIFIED,
                        0.85, [], "test", time.time()
                    )
                ],
                "expected_min": 0.7
            },
            {
                "name": "Low Confidence Scenario",
                "checks": [
                    ValidationCheck(
                        ValidationType.EXTENSION_VERIFICATION, "claim", ValidationResult.FAILED,
                        0.3, [], "test", time.time()
                    ),
                    ValidationCheck(
                        ValidationType.DEPENDENCY_VERIFICATION, "claim", ValidationResult.UNABLE_TO_VERIFY,
                        0.2, [], "test", time.time()
                    )
                ],
                "expected_max": 0.5
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                summary = self.engine._generate_validation_summary(case["checks"])
                confidence = self.engine._calculate_validation_confidence(case["checks"], summary)
                
                self.assertIsInstance(confidence, float)
                self.assertGreaterEqual(confidence, 0.0)
                self.assertLessEqual(confidence, 1.0)
                
                if "expected_min" in case:
                    self.assertGreaterEqual(confidence, case["expected_min"])
                if "expected_max" in case:
                    self.assertLessEqual(confidence, case["expected_max"])

    # CRITICAL TEST 10: Serialization and Data Persistence
    def test_serialization_and_data_persistence(self):
        """
        CRITICAL: Test validation result serialization for persistence
        """
        # Create sample validation result
        sample_checks = [
            ValidationCheck(
                check_type=ValidationType.EXTENSION_VERIFICATION,
                claim="test claim",
                result=ValidationResult.VERIFIED,
                confidence=0.9,
                evidence=["evidence data"],
                verification_method="test_method",
                timestamp=time.time()
            )
        ]
        
        sample_summary = ValidationSummary(
            total_checks=1,
            verified_count=1,
            failed_count=0,
            partially_verified_count=0,
            unable_to_verify_count=0,
            overall_accuracy=1.0,
            false_positive_risk=0.0,
            validation_timestamp=time.time()
        )
        
        validation_result = EvidenceValidationResult(
            checks=sample_checks,
            summary=sample_summary,
            validated_claims=["test claim"],
            rejected_claims=[],
            confidence_score=0.9
        )
        
        # Test serialization
        serialized = self.engine.to_dict(validation_result)
        
        # Validate serialized structure
        required_keys = ['checks', 'summary', 'validated_claims', 'rejected_claims', 'confidence_score']
        for key in required_keys:
            self.assertIn(key, serialized)
        
        # Test JSON serialization
        json_str = json.dumps(serialized)
        self.assertIsInstance(json_str, str)
        
        # Test JSON deserialization
        restored = json.loads(json_str)
        self.assertEqual(len(restored['checks']), 1)
        self.assertEqual(restored['confidence_score'], 0.9)
        self.assertEqual(restored['summary']['total_checks'], 1)

    # CRITICAL TEST 11: Edge Cases and Error Handling
    def test_edge_cases_and_error_handling(self):
        """
        CRITICAL: Test edge cases and error handling robustness
        """
        edge_cases = [
            {
                "name": "Empty Claims List",
                "claims": [],
                "expected_behavior": "empty_result"
            },
            {
                "name": "None Investigation Data",
                "claims": ["test claim"],
                "investigation_data": {},
                "expected_behavior": "graceful_handling"
            },
            {
                "name": "Very Long Claim",
                "claims": ["x" * 10000],  # 10k character claim
                "expected_behavior": "handle_large_input"
            },
            {
                "name": "Special Characters in Claims",
                "claims": ["claim with émojis 🚀 and spëcial chars ñ"],
                "expected_behavior": "handle_unicode"
            }
        ]
        
        for case in edge_cases:
            with self.subTest(case=case["name"]):
                try:
                    investigation_data = case.get('investigation_data', self.sample_investigation_data)
                    result = self.engine.validate_technical_claims(case["claims"], investigation_data)
                    
                    # Should always return a valid result structure
                    self.assertIsInstance(result, EvidenceValidationResult)
                    
                    if case["expected_behavior"] == "empty_result":
                        self.assertEqual(len(result.checks), 0)
                        self.assertEqual(result.summary.total_checks, 0)
                    
                except Exception as e:
                    self.fail(f"Edge case handling failed for {case['name']}: {str(e)}")


if __name__ == '__main__':
    # Set up test discovery and execution
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestEvidenceValidationEngine)
    
    # Run tests with detailed output
    test_runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = test_runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)