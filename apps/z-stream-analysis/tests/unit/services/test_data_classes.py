#!/usr/bin/env python3
"""
Unit Tests for Data Classes and Enums
Tests data class validation, enum behavior, and field integrity
"""

import unittest
import time
import sys
import os
from dataclasses import asdict
from typing import Dict, Any

# Add source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from services.jenkins_intelligence_service import JenkinsMetadata, JenkinsIntelligence
from services.two_agent_intelligence_framework import (
    InvestigationResult, SolutionResult, ComprehensiveAnalysis, AnalysisPhase
)
from services.evidence_validation_engine import (
    ValidationCheck, ValidationSummary, EvidenceValidationResult,
    ValidationType, ValidationResult
)


class TestJenkinsDataClasses(unittest.TestCase):
    """
    Test suite for Jenkins Intelligence data classes
    
    CRITICAL TESTING GOALS:
    1. Validate JenkinsMetadata field integrity and constraints
    2. Test JenkinsIntelligence composition and validation
    3. Ensure proper serialization and deserialization
    4. Test field type validation and edge cases
    """
    
    def test_jenkins_metadata_field_validation(self):
        """
        CRITICAL: Test JenkinsMetadata field validation and constraints
        """
        # Valid metadata creation
        valid_metadata = JenkinsMetadata(
            build_url="https://jenkins.example.com/job/test/123/",
            job_name="test-pipeline",
            build_number=123,
            build_result="FAILURE",
            timestamp="2024-08-17T17:55:40Z",
            parameters={"CLUSTER_NAME": "test-cluster"},
            console_log_snippet="Error in test execution",
            artifacts=["results.xml", "console.log"],
            branch="release-2.9",
            commit_sha="abc123def456"
        )
        
        # Test field access
        self.assertEqual(valid_metadata.build_url, "https://jenkins.example.com/job/test/123/")
        self.assertEqual(valid_metadata.job_name, "test-pipeline")
        self.assertEqual(valid_metadata.build_number, 123)
        self.assertEqual(valid_metadata.build_result, "FAILURE")
        self.assertIsInstance(valid_metadata.parameters, dict)
        self.assertIsInstance(valid_metadata.artifacts, list)
        
        # Test optional fields
        self.assertEqual(valid_metadata.branch, "release-2.9")
        self.assertEqual(valid_metadata.commit_sha, "abc123def456")
        
        # Test with None optional fields
        minimal_metadata = JenkinsMetadata(
            build_url="https://jenkins.example.com/job/test/123/",
            job_name="test-pipeline",
            build_number=123,
            build_result="SUCCESS",
            timestamp="2024-08-17T17:55:40Z",
            parameters={},
            console_log_snippet="",
            artifacts=[]
        )
        
        self.assertIsNone(minimal_metadata.branch)
        self.assertIsNone(minimal_metadata.commit_sha)
        self.assertEqual(minimal_metadata.parameters, {})
        self.assertEqual(minimal_metadata.artifacts, [])
    
    def test_jenkins_metadata_serialization(self):
        """
        CRITICAL: Test JenkinsMetadata serialization integrity
        """
        metadata = JenkinsMetadata(
            build_url="https://jenkins.example.com/job/test/123/",
            job_name="test-pipeline",
            build_number=123,
            build_result="FAILURE",
            timestamp="2024-08-17T17:55:40Z",
            parameters={"CLUSTER_NAME": "test-cluster", "BRANCH": "main"},
            console_log_snippet="Test failure occurred",
            artifacts=["results.xml"],
            branch="main",
            commit_sha="abcdef123456"
        )
        
        # Test asdict conversion
        metadata_dict = asdict(metadata)
        
        # Validate all fields present
        expected_fields = {
            'build_url', 'job_name', 'build_number', 'build_result',
            'timestamp', 'parameters', 'console_log_snippet', 'artifacts',
            'branch', 'commit_sha'
        }
        self.assertEqual(set(metadata_dict.keys()), expected_fields)
        
        # Validate data types preserved
        self.assertIsInstance(metadata_dict['build_number'], int)
        self.assertIsInstance(metadata_dict['parameters'], dict)
        self.assertIsInstance(metadata_dict['artifacts'], list)
    
    def test_jenkins_intelligence_composition(self):
        """
        CRITICAL: Test JenkinsIntelligence composite structure
        """
        metadata = JenkinsMetadata(
            build_url="https://jenkins.example.com/job/test/123/",
            job_name="test-pipeline",
            build_number=123,
            build_result="FAILURE",
            timestamp="2024-08-17T17:55:40Z",
            parameters={},
            console_log_snippet="",
            artifacts=[]
        )
        
        intelligence = JenkinsIntelligence(
            metadata=metadata,
            failure_analysis={'total_failures': 3, 'primary_failure_type': 'timeout'},
            environment_info={'cluster_name': 'test-cluster'},
            evidence_sources=["[Jenkins:test:123:FAILURE]"],
            confidence_score=0.85
        )
        
        # Test composition integrity
        self.assertIsInstance(intelligence.metadata, JenkinsMetadata)
        self.assertEqual(intelligence.metadata.job_name, "test-pipeline")
        self.assertIsInstance(intelligence.failure_analysis, dict)
        self.assertIsInstance(intelligence.environment_info, dict)
        self.assertIsInstance(intelligence.evidence_sources, list)
        self.assertIsInstance(intelligence.confidence_score, float)
        
        # Test confidence score constraints
        self.assertGreaterEqual(intelligence.confidence_score, 0.0)
        self.assertLessEqual(intelligence.confidence_score, 1.0)


class TestTwoAgentFrameworkDataClasses(unittest.TestCase):
    """
    Test suite for 2-Agent Framework data classes
    
    CRITICAL TESTING GOALS:
    1. Validate InvestigationResult structure and fields
    2. Test SolutionResult composition and validation
    3. Test ComprehensiveAnalysis integration
    4. Ensure proper data flow between structures
    """
    
    def test_investigation_result_structure(self):
        """
        CRITICAL: Test InvestigationResult structure and validation
        """
        # Create sample Jenkins intelligence
        metadata = JenkinsMetadata(
            build_url="https://jenkins.example.com/job/test/123/",
            job_name="test",
            build_number=123,
            build_result="FAILURE",
            timestamp="",
            parameters={},
            console_log_snippet="",
            artifacts=[]
        )
        
        jenkins_intelligence = JenkinsIntelligence(
            metadata=metadata,
            failure_analysis={},
            environment_info={},
            evidence_sources=[],
            confidence_score=0.8
        )
        
        investigation_result = InvestigationResult(
            jenkins_intelligence=jenkins_intelligence,
            environment_validation={'connectivity': True, 'score': 0.9},
            repository_analysis={'cloned': True, 'branch': 'main'},
            evidence_correlation={'consistency': True, 'score': 0.95},
            confidence_score=0.85,
            investigation_time=2.5
        )
        
        # Test structure integrity
        self.assertIsInstance(investigation_result.jenkins_intelligence, JenkinsIntelligence)
        self.assertIsInstance(investigation_result.environment_validation, dict)
        self.assertIsInstance(investigation_result.repository_analysis, dict)
        self.assertIsInstance(investigation_result.evidence_correlation, dict)
        self.assertIsInstance(investigation_result.confidence_score, float)
        self.assertIsInstance(investigation_result.investigation_time, float)
        
        # Test confidence and timing constraints
        self.assertGreaterEqual(investigation_result.confidence_score, 0.0)
        self.assertLessEqual(investigation_result.confidence_score, 1.0)
        self.assertGreater(investigation_result.investigation_time, 0.0)
    
    def test_solution_result_structure(self):
        """
        CRITICAL: Test SolutionResult structure and validation
        """
        solution_result = SolutionResult(
            evidence_analysis={'patterns': ['timeout'], 'confidence': 0.9},
            bug_classification={'type': 'AUTOMATION_BUG', 'confidence': 0.95},
            fix_recommendations=[
                {'type': 'code_fix', 'priority': 'high', 'confidence': 0.8}
            ],
            implementation_guidance={'steps': ['step1', 'step2'], 'effort': '2-4 hours'},
            confidence_score=0.88,
            solution_time=1.8
        )
        
        # Test structure integrity
        self.assertIsInstance(solution_result.evidence_analysis, dict)
        self.assertIsInstance(solution_result.bug_classification, dict)
        self.assertIsInstance(solution_result.fix_recommendations, list)
        self.assertIsInstance(solution_result.implementation_guidance, dict)
        self.assertIsInstance(solution_result.confidence_score, float)
        self.assertIsInstance(solution_result.solution_time, float)
        
        # Test constraints
        self.assertGreaterEqual(solution_result.confidence_score, 0.0)
        self.assertLessEqual(solution_result.confidence_score, 1.0)
        self.assertGreater(solution_result.solution_time, 0.0)
        
        # Test list structure
        self.assertGreater(len(solution_result.fix_recommendations), 0)
        for recommendation in solution_result.fix_recommendations:
            self.assertIsInstance(recommendation, dict)
    
    def test_comprehensive_analysis_integration(self):
        """
        CRITICAL: Test ComprehensiveAnalysis complete integration
        """
        # Create complete data structure
        metadata = JenkinsMetadata(
            build_url="https://jenkins.example.com/job/test/123/",
            job_name="test",
            build_number=123,
            build_result="FAILURE",
            timestamp="",
            parameters={},
            console_log_snippet="",
            artifacts=[]
        )
        
        jenkins_intelligence = JenkinsIntelligence(
            metadata=metadata,
            failure_analysis={},
            environment_info={},
            evidence_sources=["[Jenkins:test:123:FAILURE]"],
            confidence_score=0.8
        )
        
        investigation_result = InvestigationResult(
            jenkins_intelligence=jenkins_intelligence,
            environment_validation={},
            repository_analysis={},
            evidence_correlation={},
            confidence_score=0.8,
            investigation_time=2.0
        )
        
        solution_result = SolutionResult(
            evidence_analysis={},
            bug_classification={'type': 'AUTOMATION_BUG'},
            fix_recommendations=[],
            implementation_guidance={},
            confidence_score=0.75,
            solution_time=1.5
        )
        
        comprehensive_analysis = ComprehensiveAnalysis(
            jenkins_url="https://jenkins.example.com/job/test/123/",
            investigation_result=investigation_result,
            solution_result=solution_result,
            overall_classification="AUTOMATION_BUG",
            overall_confidence=0.78,
            total_analysis_time=3.5,
            evidence_sources=["[Jenkins:test:123:FAILURE]"]
        )
        
        # Test complete structure
        self.assertIsInstance(comprehensive_analysis.jenkins_url, str)
        self.assertIsInstance(comprehensive_analysis.investigation_result, InvestigationResult)
        self.assertIsInstance(comprehensive_analysis.solution_result, SolutionResult)
        self.assertIsInstance(comprehensive_analysis.overall_classification, str)
        self.assertIsInstance(comprehensive_analysis.overall_confidence, float)
        self.assertIsInstance(comprehensive_analysis.total_analysis_time, float)
        self.assertIsInstance(comprehensive_analysis.evidence_sources, list)
        
        # Test data consistency
        self.assertEqual(comprehensive_analysis.overall_classification, "AUTOMATION_BUG")
        self.assertGreaterEqual(comprehensive_analysis.overall_confidence, 0.0)
        self.assertLessEqual(comprehensive_analysis.overall_confidence, 1.0)
        self.assertGreater(comprehensive_analysis.total_analysis_time, 0.0)


class TestEvidenceValidationDataClasses(unittest.TestCase):
    """
    Test suite for Evidence Validation data classes
    
    CRITICAL TESTING GOALS:
    1. Validate ValidationCheck structure and constraints
    2. Test ValidationSummary calculations and integrity
    3. Test EvidenceValidationResult composition
    4. Ensure proper enum behavior and validation
    """
    
    def test_validation_check_structure(self):
        """
        CRITICAL: Test ValidationCheck structure and field validation
        """
        validation_check = ValidationCheck(
            check_type=ValidationType.FILE_EXISTENCE,
            claim="Found 147 .js files in repository",
            result=ValidationResult.VERIFIED,
            confidence=0.95,
            evidence=["Repository clone successful", "File count verified"],
            verification_method="filesystem_analysis",
            timestamp=time.time()
        )
        
        # Test field types and values
        self.assertIsInstance(validation_check.check_type, ValidationType)
        self.assertEqual(validation_check.check_type, ValidationType.FILE_EXISTENCE)
        self.assertIsInstance(validation_check.claim, str)
        self.assertIsInstance(validation_check.result, ValidationResult)
        self.assertEqual(validation_check.result, ValidationResult.VERIFIED)
        self.assertIsInstance(validation_check.confidence, float)
        self.assertIsInstance(validation_check.evidence, list)
        self.assertIsInstance(validation_check.verification_method, str)
        self.assertIsInstance(validation_check.timestamp, float)
        
        # Test constraints
        self.assertGreaterEqual(validation_check.confidence, 0.0)
        self.assertLessEqual(validation_check.confidence, 1.0)
        self.assertGreater(validation_check.timestamp, 0.0)
        self.assertGreater(len(validation_check.evidence), 0)
    
    def test_validation_summary_calculations(self):
        """
        CRITICAL: Test ValidationSummary calculation accuracy
        """
        validation_summary = ValidationSummary(
            total_checks=10,
            verified_count=7,
            failed_count=2,
            partially_verified_count=1,
            unable_to_verify_count=0,
            overall_accuracy=0.85,
            false_positive_risk=0.2,
            validation_timestamp=time.time()
        )
        
        # Test count consistency
        total_calculated = (validation_summary.verified_count + 
                          validation_summary.failed_count + 
                          validation_summary.partially_verified_count + 
                          validation_summary.unable_to_verify_count)
        self.assertEqual(total_calculated, validation_summary.total_checks)
        
        # Test field types
        self.assertIsInstance(validation_summary.total_checks, int)
        self.assertIsInstance(validation_summary.verified_count, int)
        self.assertIsInstance(validation_summary.overall_accuracy, float)
        self.assertIsInstance(validation_summary.false_positive_risk, float)
        
        # Test value constraints
        self.assertGreaterEqual(validation_summary.overall_accuracy, 0.0)
        self.assertLessEqual(validation_summary.overall_accuracy, 1.0)
        self.assertGreaterEqual(validation_summary.false_positive_risk, 0.0)
        self.assertLessEqual(validation_summary.false_positive_risk, 1.0)
    
    def test_evidence_validation_result_composition(self):
        """
        CRITICAL: Test EvidenceValidationResult complete structure
        """
        # Create sample checks
        checks = [
            ValidationCheck(
                check_type=ValidationType.FILE_EXISTENCE,
                claim="test claim 1",
                result=ValidationResult.VERIFIED,
                confidence=0.9,
                evidence=["evidence 1"],
                verification_method="method1",
                timestamp=time.time()
            ),
            ValidationCheck(
                check_type=ValidationType.DEPENDENCY_VERIFICATION,
                claim="test claim 2",
                result=ValidationResult.FAILED,
                confidence=0.8,
                evidence=["evidence 2"],
                verification_method="method2",
                timestamp=time.time()
            )
        ]
        
        summary = ValidationSummary(
            total_checks=2,
            verified_count=1,
            failed_count=1,
            partially_verified_count=0,
            unable_to_verify_count=0,
            overall_accuracy=0.5,
            false_positive_risk=0.5,
            validation_timestamp=time.time()
        )
        
        result = EvidenceValidationResult(
            checks=checks,
            summary=summary,
            validated_claims=["test claim 1"],
            rejected_claims=["test claim 2"],
            confidence_score=0.75
        )
        
        # Test composition
        self.assertIsInstance(result.checks, list)
        self.assertEqual(len(result.checks), 2)
        self.assertIsInstance(result.summary, ValidationSummary)
        self.assertIsInstance(result.validated_claims, list)
        self.assertIsInstance(result.rejected_claims, list)
        self.assertIsInstance(result.confidence_score, float)
        
        # Test data consistency
        self.assertEqual(len(result.validated_claims), 1)
        self.assertEqual(len(result.rejected_claims), 1)
        self.assertIn("test claim 1", result.validated_claims)
        self.assertIn("test claim 2", result.rejected_claims)


class TestEnumBehavior(unittest.TestCase):
    """
    Test suite for Enum behavior and validation
    
    CRITICAL TESTING GOALS:
    1. Test ValidationType enum values and behavior
    2. Test ValidationResult state transitions
    3. Test AnalysisPhase workflow validation
    4. Ensure enum serialization integrity
    """
    
    def test_validation_type_enum(self):
        """
        CRITICAL: Test ValidationType enum values and behavior
        """
        # Test all enum values exist
        expected_types = {
            'FILE_EXISTENCE', 'DEPENDENCY_VERIFICATION', 'EXTENSION_VERIFICATION',
            'CITATION_VERIFICATION', 'TECHNICAL_CLAIM_VERIFICATION', 'CROSS_SOURCE_CONSISTENCY'
        }
        
        actual_types = {member.name for member in ValidationType}
        self.assertEqual(actual_types, expected_types)
        
        # Test enum value access
        self.assertEqual(ValidationType.FILE_EXISTENCE.value, "file_existence")
        self.assertEqual(ValidationType.DEPENDENCY_VERIFICATION.value, "dependency_verification")
        self.assertEqual(ValidationType.EXTENSION_VERIFICATION.value, "extension_verification")
        
        # Test enum comparison
        self.assertNotEqual(ValidationType.FILE_EXISTENCE, ValidationType.DEPENDENCY_VERIFICATION)
        self.assertEqual(ValidationType.FILE_EXISTENCE, ValidationType.FILE_EXISTENCE)
    
    def test_validation_result_enum(self):
        """
        CRITICAL: Test ValidationResult enum values and states
        """
        # Test all enum values exist
        expected_results = {'VERIFIED', 'FAILED', 'PARTIALLY_VERIFIED', 'UNABLE_TO_VERIFY'}
        actual_results = {member.name for member in ValidationResult}
        self.assertEqual(actual_results, expected_results)
        
        # Test enum value access
        self.assertEqual(ValidationResult.VERIFIED.value, "verified")
        self.assertEqual(ValidationResult.FAILED.value, "failed")
        self.assertEqual(ValidationResult.PARTIALLY_VERIFIED.value, "partially_verified")
        self.assertEqual(ValidationResult.UNABLE_TO_VERIFY.value, "unable_to_verify")
        
        # Test enum ordering concepts (logical progression)
        # VERIFIED > PARTIALLY_VERIFIED > UNABLE_TO_VERIFY > FAILED
        verification_levels = [
            ValidationResult.VERIFIED,
            ValidationResult.PARTIALLY_VERIFIED, 
            ValidationResult.UNABLE_TO_VERIFY,
            ValidationResult.FAILED
        ]
        
        for i, result in enumerate(verification_levels):
            self.assertIsInstance(result, ValidationResult)
    
    def test_analysis_phase_enum(self):
        """
        CRITICAL: Test AnalysisPhase enum workflow validation
        """
        # Test all enum values exist
        expected_phases = {'INVESTIGATION', 'SOLUTION', 'COMPLETE'}
        actual_phases = {member.name for member in AnalysisPhase}
        self.assertEqual(actual_phases, expected_phases)
        
        # Test enum value access
        self.assertEqual(AnalysisPhase.INVESTIGATION.value, "investigation")
        self.assertEqual(AnalysisPhase.SOLUTION.value, "solution")
        self.assertEqual(AnalysisPhase.COMPLETE.value, "complete")
        
        # Test workflow progression logic
        workflow_order = [
            AnalysisPhase.INVESTIGATION,
            AnalysisPhase.SOLUTION,
            AnalysisPhase.COMPLETE
        ]
        
        for i, phase in enumerate(workflow_order):
            self.assertIsInstance(phase, AnalysisPhase)
            
        # Test phase transitions
        self.assertNotEqual(AnalysisPhase.INVESTIGATION, AnalysisPhase.SOLUTION)
        self.assertNotEqual(AnalysisPhase.SOLUTION, AnalysisPhase.COMPLETE)
    
    def test_enum_serialization(self):
        """
        CRITICAL: Test enum serialization and string representation
        """
        # Test ValidationType serialization
        file_check = ValidationType.FILE_EXISTENCE
        self.assertEqual(str(file_check), "ValidationType.FILE_EXISTENCE")
        self.assertEqual(file_check.value, "file_existence")
        
        # Test ValidationResult serialization  
        verified = ValidationResult.VERIFIED
        self.assertEqual(str(verified), "ValidationResult.VERIFIED")
        self.assertEqual(verified.value, "verified")
        
        # Test AnalysisPhase serialization
        investigation = AnalysisPhase.INVESTIGATION
        self.assertEqual(str(investigation), "AnalysisPhase.INVESTIGATION")
        self.assertEqual(investigation.value, "investigation")
        
        # Test enum reconstruction from string values
        self.assertEqual(ValidationType("file_existence"), ValidationType.FILE_EXISTENCE)
        self.assertEqual(ValidationResult("verified"), ValidationResult.VERIFIED)
        self.assertEqual(AnalysisPhase("investigation"), AnalysisPhase.INVESTIGATION)


class TestDataClassEdgeCases(unittest.TestCase):
    """
    Test suite for data class edge cases and validation
    
    CRITICAL TESTING GOALS:
    1. Test data class behavior with extreme values
    2. Test Unicode and special character handling
    3. Test large data structure performance
    4. Test serialization with complex nested data
    """
    
    def test_unicode_handling(self):
        """
        CRITICAL: Test Unicode and special character handling
        """
        # Test Unicode in Jenkins metadata
        unicode_metadata = JenkinsMetadata(
            build_url="https://jenkins.example.com/job/测试/123/",
            job_name="test-pipeline-émojis-🚀",
            build_number=123,
            build_result="FAILURE",
            timestamp="2024-08-17T17:55:40Z",
            parameters={"CLUSTER_NAME": "test-émojis-🔥"},
            console_log_snippet="Error: 测试失败 with émojis 🚨",
            artifacts=["results-测试.xml"]
        )
        
        # Test field access with Unicode
        self.assertIn("测试", unicode_metadata.build_url)
        self.assertIn("émojis", unicode_metadata.job_name)
        self.assertIn("🚀", unicode_metadata.job_name)
        self.assertIn("测试失败", unicode_metadata.console_log_snippet)
        
        # Test serialization with Unicode
        serialized = asdict(unicode_metadata)
        self.assertIsInstance(serialized, dict)
    
    def test_large_data_structures(self):
        """
        CRITICAL: Test behavior with large data structures
        """
        # Test large console log
        large_console_log = "Error line\n" * 10000  # ~100KB
        
        large_metadata = JenkinsMetadata(
            build_url="https://jenkins.example.com/job/test/123/",
            job_name="test-pipeline",
            build_number=123,
            build_result="FAILURE",
            timestamp="2024-08-17T17:55:40Z",
            parameters={"CLUSTER_NAME": "test"},
            console_log_snippet=large_console_log,
            artifacts=[f"artifact_{i}.xml" for i in range(100)]  # 100 artifacts
        )
        
        # Test large data handling
        self.assertEqual(len(large_metadata.console_log_snippet), len(large_console_log))
        self.assertEqual(len(large_metadata.artifacts), 100)
        
        # Test serialization performance
        start_time = time.time()
        serialized = asdict(large_metadata)
        serialization_time = time.time() - start_time
        
        # Should complete within reasonable time (< 1 second)
        self.assertLess(serialization_time, 1.0)
        self.assertIsInstance(serialized, dict)
    
    def test_extreme_values(self):
        """
        CRITICAL: Test data classes with extreme values
        """
        # Test extreme confidence values
        extreme_confidence_check = ValidationCheck(
            check_type=ValidationType.FILE_EXISTENCE,
            claim="test claim",
            result=ValidationResult.VERIFIED,
            confidence=1.0,  # Maximum confidence
            evidence=["evidence"],
            verification_method="test",
            timestamp=time.time()
        )
        
        self.assertEqual(extreme_confidence_check.confidence, 1.0)
        
        # Test zero confidence
        zero_confidence_check = ValidationCheck(
            check_type=ValidationType.FILE_EXISTENCE,
            claim="test claim",
            result=ValidationResult.FAILED,
            confidence=0.0,  # Minimum confidence
            evidence=["evidence"],
            verification_method="test",
            timestamp=time.time()
        )
        
        self.assertEqual(zero_confidence_check.confidence, 0.0)
        
        # Test extreme build numbers
        extreme_metadata = JenkinsMetadata(
            build_url="https://jenkins.example.com/job/test/999999999/",
            job_name="test",
            build_number=999999999,  # Very large build number
            build_result="SUCCESS",
            timestamp="2024-08-17T17:55:40Z",
            parameters={},
            console_log_snippet="",
            artifacts=[]
        )
        
        self.assertEqual(extreme_metadata.build_number, 999999999)
        self.assertIsInstance(extreme_metadata.build_number, int)


if __name__ == '__main__':
    # Set up test discovery and execution
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestJenkinsDataClasses))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestTwoAgentFrameworkDataClasses))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestEvidenceValidationDataClasses))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestEnumBehavior))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestDataClassEdgeCases))
    
    # Run tests with detailed output
    test_runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = test_runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)