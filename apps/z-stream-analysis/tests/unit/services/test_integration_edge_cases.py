#!/usr/bin/env python3
"""
Integration Edge Case Tests
Tests edge cases, integration scenarios, and performance boundaries
"""

import unittest
import time
import sys
import os
import threading
import concurrent.futures
from unittest.mock import Mock, patch
from typing import List, Dict, Any

# Add source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from services.jenkins_intelligence_service import JenkinsIntelligenceService, JenkinsMetadata, JenkinsIntelligence
from services.two_agent_intelligence_framework import TwoAgentIntelligenceFramework, InvestigationResult, SolutionResult
from services.evidence_validation_engine import EvidenceValidationEngine, ValidationCheck, ValidationResult, ValidationType


class TestIntegrationEdgeCases(unittest.TestCase):
    """
    Test suite for integration edge cases and boundary conditions
    
    CRITICAL TESTING GOALS:
    1. Test concurrent execution scenarios
    2. Test large data processing capabilities  
    3. Test memory usage with extreme inputs
    4. Test integration between all services
    5. Test real-world edge cases and error conditions
    """
    
    def setUp(self):
        """Set up test environment"""
        self.jenkins_service = JenkinsIntelligenceService()
        self.framework = TwoAgentIntelligenceFramework()
        self.validation_engine = EvidenceValidationEngine()
        
    def test_concurrent_analysis_execution(self):
        """
        CRITICAL: Test concurrent execution of multiple analyses
        """
        jenkins_urls = [
            "https://jenkins1.com/job/test1/123/",
            "https://jenkins2.com/job/test2/456/", 
            "https://jenkins3.com/job/test3/789/"
        ]
        
        # Mock subprocess to avoid real network calls
        with patch('subprocess.run') as mock_subprocess:
            mock_response = Mock()
            mock_response.returncode = 0
            mock_response.stdout = "Mock Jenkins data"
            mock_subprocess.return_value = mock_response
            
            def analyze_url(url):
                """Function to run in concurrent threads"""
                return self.jenkins_service.analyze_jenkins_url(url)
            
            # Execute concurrent analyses
            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(analyze_url, url) for url in jenkins_urls]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            execution_time = time.time() - start_time
            
            # Validate results
            self.assertEqual(len(results), 3)
            for result in results:
                self.assertIsInstance(result, JenkinsIntelligence)
                self.assertGreaterEqual(result.confidence_score, 0.0)
                self.assertLessEqual(result.confidence_score, 1.0)
            
            # Should complete within reasonable time (< 5 seconds for mocked operations)
            self.assertLess(execution_time, 5.0)
    
    def test_large_console_log_processing(self):
        """
        CRITICAL: Test processing of very large console logs
        """
        # Create a large console log (1MB+)
        large_log_lines = ["ERROR: Test failure occurred"] * 50000  # ~1.3MB
        large_console_log = "\n".join(large_log_lines)
        
        with patch('subprocess.run') as mock_subprocess:
            mock_console_response = Mock()
            mock_console_response.returncode = 0
            mock_console_response.stdout = large_console_log
            
            mock_api_response = Mock()
            mock_api_response.returncode = 0
            mock_api_response.stdout = '{"result": "FAILURE", "timestamp": "2024-08-17T17:55:40Z", "parameters": {}}'
            
            def subprocess_side_effect(*args, **kwargs):
                cmd_args = args[0]
                if 'consoleText' in ' '.join(cmd_args):
                    return mock_console_response
                elif 'api/json' in ' '.join(cmd_args):
                    return mock_api_response
                else:
                    return Mock(returncode=1, stdout="", stderr="Unknown URL")
            
            mock_subprocess.side_effect = subprocess_side_effect
            
            # Test large console log processing
            start_time = time.time()
            result = self.jenkins_service.analyze_jenkins_url("https://jenkins.com/job/test/123/")
            processing_time = time.time() - start_time
            
            # Validate result
            self.assertIsInstance(result, JenkinsIntelligence)
            self.assertEqual(len(result.metadata.console_log_snippet), 2000)  # Should be truncated
            self.assertIn("ERROR: Test failure occurred", result.metadata.console_log_snippet)
            
            # Should complete within reasonable time (< 2 seconds)
            self.assertLess(processing_time, 2.0)
    
    def test_extreme_failure_pattern_detection(self):
        """
        CRITICAL: Test failure pattern detection with extreme cases
        """
        # Console log with mixed failure patterns and high complexity
        complex_console_log = """
        [INFO] Starting test execution with 1000 parallel threads
        [ERROR] TimeoutError: Timed out after 30 seconds waiting for element #user-login-button
        [ERROR] ElementNotInteractableException: Element not found for selector .submit-form
        [WARN] cypress timed out waiting for selector '.cluster-list-container'
        [ERROR] NoSuchElementException: Unable to locate element with xpath //div[@class='main-content']
        [ERROR] Connection refused to https://api.cluster.example.com:6443
        [ERROR] DNS resolution failed for cluster endpoint api.test.cluster.com
        [INFO] Retrying connection attempt 1 of 5
        [ERROR] Network error: failed to connect to cluster after 5 attempts
        [ERROR] TimeoutError: timeout waiting for element after 60000ms
        [ERROR] Element not found: button[data-test="create-cluster-button"]
        [FATAL] Test suite failed with 15 errors and 8 timeouts
        """ * 100  # Multiply to create more complex patterns
        
        # Analyze complex failure patterns
        failure_analysis = self.jenkins_service._analyze_failure_patterns(complex_console_log)
        
        # Validate detection accuracy
        self.assertIsInstance(failure_analysis, dict)
        self.assertIn('patterns', failure_analysis)
        self.assertIn('total_failures', failure_analysis)
        self.assertIn('primary_failure_type', failure_analysis)
        
        # Should detect multiple failure types
        patterns = failure_analysis['patterns']
        self.assertGreater(len(patterns['timeout_errors']), 0)
        self.assertGreater(len(patterns['element_not_found']), 0)
        self.assertGreater(len(patterns['network_errors']), 0)
        
        # Total failures should be significant
        self.assertGreater(failure_analysis['total_failures'], 10)
        
        # Should determine primary failure type
        self.assertIn(failure_analysis['primary_failure_type'], 
                     ['timeout_errors', 'element_not_found', 'network_errors'])
    
    def test_evidence_validation_with_complex_claims(self):
        """
        CRITICAL: Test evidence validation with complex and mixed claims
        """
        complex_claims = [
            "Found 147 .js files and 23 .cy.js files in repository analysis",
            "MobX version 6.3.2 conflicts with React 18.0.0 in package.json",
            "[Jenkins:complex-pipeline:9999:FAILURE:2024-08-17T17:55:40Z] shows multiple timeout errors",
            "[Repo:release-2.9:tests/e2e/complex_test.js:45-67:abc123:file_verified] contains problematic selector logic",
            "Environment validation succeeded with 99.9% confidence across 15 endpoints",
            "All tests verified without actual verification process completion",  # False positive pattern
            "Cypress framework version 12.17.0 detected through package.json analysis",
            "Database connection timeout after 30 seconds with proper retry logic",
            "API rate limiting detected: 429 responses from 5 different endpoints"
        ]
        
        # Mock investigation data
        investigation_data = {
            'jenkins_intelligence': {
                'metadata': {'job_name': 'complex-pipeline', 'build_number': 9999}
            },
            'repository_analysis': {
                'repository_cloned': True,
                'test_files_found': [
                    'tests/e2e/complex_test.js',
                    'tests/unit/api_test.js',
                    'tests/integration/db_test.js'
                ],
                'dependency_analysis': {
                    'framework': 'cypress',
                    'version': '12.17.0',
                    'dependencies': {'react': '18.0.0', 'mobx': '6.3.2'}
                }
            },
            'environment_validation': {
                'cluster_connectivity': True,
                'environment_score': 0.999
            }
        }
        
        # Execute complex validation
        start_time = time.time()
        result = self.validation_engine.validate_technical_claims(complex_claims, investigation_data)
        validation_time = time.time() - start_time
        
        # Validate results
        self.assertIsInstance(result.checks, list)
        self.assertGreater(len(result.checks), 0)
        self.assertIsInstance(result.summary.total_checks, int)
        self.assertGreater(result.summary.total_checks, 0)
        
        # Should detect and reject false positive patterns
        self.assertGreater(len(result.rejected_claims), 0)
        false_positive_claim = "All tests verified without actual verification process completion"
        self.assertIn(false_positive_claim, result.rejected_claims)
        
        # Should validate legitimate technical claims
        self.assertGreater(len(result.validated_claims), 0)
        
        # Overall confidence should be reasonable
        self.assertGreater(result.confidence_score, 0.3)
        self.assertLessEqual(result.confidence_score, 1.0)
        
        # Should complete within reasonable time
        self.assertLess(validation_time, 1.0)
    
    def test_two_agent_framework_with_complex_scenario(self):
        """
        CRITICAL: Test complete 2-agent framework with complex real-world scenario
        """
        complex_jenkins_url = "https://jenkins-complex.example.com/job/multi-component-e2e-tests/12345/"
        
        # Mock complex Jenkins responses
        with patch('subprocess.run') as mock_subprocess:
            mock_console_log = """
            [INFO] Starting multi-component E2E test suite
            [INFO] Testing components: UI, API, Database, Message Queue, Cache
            [ERROR] TimeoutError in UI component: element selector '.complex-form' not found after 30s
            [ERROR] API component: 500 Internal Server Error from /api/v1/complex-endpoint
            [INFO] Database component: Connection successful, all queries passed
            [ERROR] Message Queue: Connection timeout to rabbitmq://complex.queue.com:5672
            [INFO] Cache component: Redis connection successful, performance within limits
            [ERROR] UI component: Multiple element interactions failed due to dynamic loading
            [FATAL] Test suite failed: 2 components failed, 3 components passed
            """
            
            mock_build_info = {
                "result": "UNSTABLE",
                "timestamp": "2024-08-17T17:55:40Z",
                "parameters": {
                    "CLUSTER_NAME": "complex-k8s-cluster",
                    "BRANCH": "release-2.9",
                    "TEST_SUITE": "multi-component-e2e",
                    "COMPONENTS": "ui,api,database,messagequeue,cache"
                },
                "artifacts": ["test-results.xml", "component-logs.zip", "performance-metrics.json"]
            }
            
            mock_console_response = Mock()
            mock_console_response.returncode = 0
            mock_console_response.stdout = mock_console_log
            
            mock_api_response = Mock()
            mock_api_response.returncode = 0
            mock_api_response.stdout = '{"result": "UNSTABLE", "timestamp": "2024-08-17T17:55:40Z", "parameters": {"CLUSTER_NAME": "complex-k8s-cluster", "BRANCH": "release-2.9"}}'
            
            def subprocess_side_effect(*args, **kwargs):
                cmd_args = args[0]
                if 'consoleText' in ' '.join(cmd_args):
                    return mock_console_response
                elif 'api/json' in ' '.join(cmd_args):
                    return mock_api_response
                else:
                    return Mock(returncode=1, stdout="", stderr="Unknown URL")
            
            mock_subprocess.side_effect = subprocess_side_effect
            
            # Execute complete 2-agent analysis
            start_time = time.time()
            result = self.framework.analyze_pipeline_failure(complex_jenkins_url)
            analysis_time = time.time() - start_time
            
            # Validate complete analysis structure
            self.assertIsInstance(result.investigation_result, InvestigationResult)
            self.assertIsInstance(result.solution_result, SolutionResult)
            self.assertIsInstance(result.overall_classification, str)
            self.assertIsInstance(result.overall_confidence, float)
            
            # Validate investigation results
            jenkins_intel = result.investigation_result.jenkins_intelligence
            self.assertEqual(jenkins_intel.metadata.build_result, "UNSTABLE")
            self.assertIn("TimeoutError", jenkins_intel.metadata.console_log_snippet)
            self.assertGreater(jenkins_intel.failure_analysis['total_failures'], 0)
            
            # Validate solution results
            classification = result.solution_result.bug_classification['primary_classification']
            self.assertIn(classification, ['AUTOMATION BUG', 'PRODUCT BUG', 'INFRASTRUCTURE BUG'])
            self.assertGreater(len(result.solution_result.fix_recommendations), 0)
            
            # Validate overall results
            self.assertGreater(result.overall_confidence, 0.4)
            self.assertLessEqual(result.overall_confidence, 1.0)
            self.assertGreater(result.total_analysis_time, 0.0)
            
            # Should complete within reasonable time (< 3 seconds for mocked operations)
            self.assertLess(analysis_time, 3.0)
    
    def test_memory_usage_with_large_datasets(self):
        """
        CRITICAL: Test memory usage and performance with large datasets
        """
        # Create large validation dataset
        large_claims = []
        for i in range(1000):
            large_claims.extend([
                f"Found {i} files in repository analysis iteration {i}",
                f"[Jenkins:test-{i}:{i}:FAILURE] shows timeout errors",
                f"Environment validation {i} succeeded with connectivity",
                f"Dependency {i} verified through package.json analysis"
            ])
        
        # Large investigation data
        large_investigation_data = {
            'jenkins_intelligence': {
                'metadata': {'job_name': 'large-test', 'build_number': 9999}
            },
            'repository_analysis': {
                'repository_cloned': True,
                'test_files_found': [f'test_{i}.js' for i in range(500)],
                'dependency_analysis': {
                    'framework': 'cypress',
                    'dependencies': {f'package_{i}': f'1.{i}.0' for i in range(100)}
                }
            },
            'environment_validation': {
                'cluster_connectivity': True,
                'environment_score': 0.95
            }
        }
        
        # Execute large dataset validation
        start_time = time.time()
        result = self.validation_engine.validate_technical_claims(large_claims, large_investigation_data)
        processing_time = time.time() - start_time
        
        # Validate large dataset handling
        self.assertEqual(len(large_claims), 4000)  # 1000 * 4 claims
        self.assertIsInstance(result.summary.total_checks, int)
        self.assertGreater(result.summary.total_checks, 0)
        
        # Should handle large datasets efficiently (< 5 seconds)
        self.assertLess(processing_time, 5.0)
        
        # Memory usage should be reasonable (result should serialize)
        serialized = self.validation_engine.to_dict(result)
        self.assertIsInstance(serialized, dict)
    
    def test_error_cascade_prevention(self):
        """
        CRITICAL: Test error cascade prevention across services
        """
        problematic_jenkins_url = "https://problematic-jenkins.com/job/error-prone/999/"
        
        # Simulate various error conditions
        error_scenarios = [
            {"side_effect": TimeoutError("Network timeout")},
            {"side_effect": ConnectionError("Connection refused")},
            {"side_effect": ValueError("Invalid JSON response")},
            {"return_value": Mock(returncode=1, stdout="", stderr="Command failed")}
        ]
        
        for i, scenario in enumerate(error_scenarios):
            with self.subTest(scenario=i):
                with patch('subprocess.run', **scenario):
                    try:
                        # Should handle errors gracefully without cascading
                        result = self.jenkins_service.analyze_jenkins_url(problematic_jenkins_url)
                        
                        # Should return valid result structure even with errors
                        self.assertIsInstance(result, JenkinsIntelligence)
                        self.assertIsInstance(result.metadata, JenkinsMetadata)
                        self.assertIsInstance(result.confidence_score, float)
                        
                        # Confidence should reflect error conditions
                        self.assertLessEqual(result.confidence_score, 0.7)
                        
                    except Exception as e:
                        self.fail(f"Error cascade occurred in scenario {i}: {str(e)}")
    
    def test_integration_serialization_roundtrip(self):
        """
        CRITICAL: Test complete serialization roundtrip across all services
        """
        jenkins_url = "https://jenkins.example.com/job/integration-test/123/"
        
        with patch('subprocess.run') as mock_subprocess:
            mock_response = Mock()
            mock_response.returncode = 0
            mock_response.stdout = "Integration test console log"
            mock_subprocess.return_value = mock_response
            
            # Execute complete framework analysis
            framework_result = self.framework.analyze_pipeline_failure(jenkins_url)
            
            # Test framework serialization
            framework_serialized = self.framework.to_dict(framework_result)
            self.assertIsInstance(framework_serialized, dict)
            
            # Test Jenkins service serialization
            jenkins_result = framework_result.investigation_result.jenkins_intelligence
            jenkins_serialized = self.jenkins_service.to_dict(jenkins_result)
            self.assertIsInstance(jenkins_serialized, dict)
            
            # Test validation engine with sample claims
            claims = ["Integration test claim", "[Jenkins:integration-test:123:FAILURE] detected"]
            investigation_data = {
                'jenkins_intelligence': {'metadata': {'job_name': 'integration-test'}},
                'repository_analysis': {'repository_cloned': True},
                'environment_validation': {'cluster_connectivity': True}
            }
            
            validation_result = self.validation_engine.validate_technical_claims(claims, investigation_data)
            validation_serialized = self.validation_engine.to_dict(validation_result)
            self.assertIsInstance(validation_serialized, dict)
            
            # Test JSON serialization roundtrip
            import json
            
            # Framework JSON roundtrip
            framework_json = json.dumps(framework_serialized)
            framework_restored = json.loads(framework_json)
            self.assertEqual(framework_restored['jenkins_url'], jenkins_url)
            
            # Jenkins JSON roundtrip
            jenkins_json = json.dumps(jenkins_serialized)
            jenkins_restored = json.loads(jenkins_json)
            self.assertIn('metadata', jenkins_restored)
            
            # Validation JSON roundtrip
            validation_json = json.dumps(validation_serialized)
            validation_restored = json.loads(validation_json)
            self.assertIn('checks', validation_restored)
            self.assertIn('summary', validation_restored)


class TestRealWorldEdgeCases(unittest.TestCase):
    """
    Test suite for real-world edge cases and production scenarios
    
    CRITICAL TESTING GOALS:
    1. Test scenarios based on actual Jenkins pipeline failures
    2. Test edge cases found in production environments
    3. Test recovery from partial failures
    4. Test boundary conditions and limits
    """
    
    def setUp(self):
        """Set up test environment"""
        self.jenkins_service = JenkinsIntelligenceService()
        self.validation_engine = EvidenceValidationEngine()
    
    def test_jenkins_url_edge_cases(self):
        """
        CRITICAL: Test Jenkins URL parsing edge cases
        """
        edge_case_urls = [
            "https://jenkins.example.com/job/test-with-spaces%20and%20chars/123/",
            "https://jenkins.example.com/job/nested/job/very/job/deep/job/structure/456/",
            "https://jenkins.example.com/job/unicode-测试-émojis-🚀/789/",
            "https://jenkins.example.com/job/test/999999999/",  # Very large build number
            "https://jenkins.example.com:8080/job/custom-port/123/",
            "http://jenkins-insecure.com/job/http-only/456/",  # HTTP instead of HTTPS
        ]
        
        for url in edge_case_urls:
            with self.subTest(url=url):
                with patch('subprocess.run') as mock_subprocess:
                    mock_response = Mock()
                    mock_response.returncode = 0
                    mock_response.stdout = f"Console log for {url}"
                    mock_subprocess.return_value = mock_response
                    
                    # Should handle all URL variants
                    result = self.jenkins_service.analyze_jenkins_url(url)
                    
                    self.assertIsInstance(result, JenkinsIntelligence)
                    self.assertEqual(result.metadata.build_url, url)
                    self.assertIsInstance(result.metadata.build_number, int)
                    self.assertGreater(result.metadata.build_number, 0)
    
    def test_console_log_edge_cases(self):
        """
        CRITICAL: Test console log parsing edge cases
        """
        edge_case_logs = [
            "",  # Empty log
            "No errors found - all tests passed successfully",  # No failures
            "ERROR" * 10000,  # Repeated error text
            "Mixed\nline\r\nendings\rand\ttabs\there",  # Mixed line endings
            "Special chars: ~!@#$%^&*()_+{}|:<>?[]\\;',./\"",  # Special characters
            "\x00\x01\x02 Binary data in log \xFF\xFE",  # Binary data
            "🚀 Unicode émojis in log 测试 🔥",  # Unicode content
        ]
        
        for i, log in enumerate(edge_case_logs):
            with self.subTest(log_case=i):
                analysis = self.jenkins_service._analyze_failure_patterns(log)
                
                # Should handle all log variants without crashing
                self.assertIsInstance(analysis, dict)
                self.assertIn('patterns', analysis)
                self.assertIn('total_failures', analysis)
                self.assertIn('primary_failure_type', analysis)
                self.assertIsInstance(analysis['total_failures'], int)
                self.assertGreaterEqual(analysis['total_failures'], 0)
    
    def test_parameter_extraction_edge_cases(self):
        """
        CRITICAL: Test parameter extraction with unusual parameter formats
        """
        edge_case_parameters = [
            {},  # Empty parameters
            {"CLUSTER_NAME": ""},  # Empty values
            {"CLUSTER_NAME": None},  # None values  
            {"cluster": "test", "CLUSTER": "different"},  # Case conflicts
            {"VERY_LONG_PARAMETER_NAME_THAT_EXCEEDS_NORMAL_LIMITS": "value"},  # Long names
            {"unicode_测试": "émojis_🚀"},  # Unicode parameters
            {"special_chars": "~!@#$%^&*()_+{}|:<>?"},  # Special character values
            {f"param_{i}": f"value_{i}" for i in range(100)},  # Many parameters
        ]
        
        for i, params in enumerate(edge_case_parameters):
            with self.subTest(params_case=i):
                env_info = self.jenkins_service._extract_environment_info(params)
                
                # Should handle all parameter variants
                self.assertIsInstance(env_info, dict)
                self.assertIn('cluster_name', env_info)
                self.assertIn('target_branch', env_info)
                self.assertIn('test_suite', env_info)
                
                # Values should be None or string
                for value in env_info.values():
                    self.assertTrue(value is None or isinstance(value, str))
    
    def test_validation_engine_boundary_conditions(self):
        """
        CRITICAL: Test validation engine boundary conditions
        """
        boundary_test_cases = [
            {
                "name": "Empty Claims",
                "claims": [],
                "investigation_data": {"jenkins_intelligence": {"metadata": {}}},
                "expected_checks": 0
            },
            {
                "name": "Single Character Claims",
                "claims": ["a", "b", "c"],
                "investigation_data": {"jenkins_intelligence": {"metadata": {}}},
                "expected_checks": 3
            },
            {
                "name": "Very Long Claims",
                "claims": ["x" * 10000],  # 10KB claim
                "investigation_data": {"jenkins_intelligence": {"metadata": {}}},
                "expected_checks": 1
            },
            {
                "name": "Claims with All False Positive Patterns",
                "claims": [
                    "Found .cy.js files when actual files are .js",
                    "MobX dependency issues without package.json verification",
                    "All verified without actual verification process"
                ],
                "investigation_data": {"jenkins_intelligence": {"metadata": {}}},
                "expected_rejected": 3
            }
        ]
        
        for case in boundary_test_cases:
            with self.subTest(case=case["name"]):
                result = self.validation_engine.validate_technical_claims(
                    case["claims"], 
                    case["investigation_data"]
                )
                
                self.assertIsInstance(result.checks, list)
                self.assertIsInstance(result.validated_claims, list)
                self.assertIsInstance(result.rejected_claims, list)
                
                if "expected_checks" in case:
                    self.assertGreaterEqual(len(result.checks), case["expected_checks"])
                
                if "expected_rejected" in case:
                    self.assertEqual(len(result.rejected_claims), case["expected_rejected"])
    
    def test_confidence_score_boundary_validation(self):
        """
        CRITICAL: Test confidence score calculations at boundaries
        """
        # Test minimum confidence scenario
        minimal_metadata = JenkinsMetadata(
            build_url="https://jenkins.com/job/test/123/",
            job_name="unknown",
            build_number=0,
            build_result="UNKNOWN",
            timestamp="",
            parameters={},
            console_log_snippet="",
            artifacts=[]
        )
        
        minimal_failure_analysis = {'total_failures': 0}
        
        minimal_confidence = self.jenkins_service._calculate_confidence_score(
            minimal_metadata, minimal_failure_analysis
        )
        
        # Should be valid confidence score
        self.assertIsInstance(minimal_confidence, float)
        self.assertGreaterEqual(minimal_confidence, 0.0)
        self.assertLessEqual(minimal_confidence, 1.0)
        
        # Test maximum confidence scenario
        maximal_metadata = JenkinsMetadata(
            build_url="https://jenkins.com/job/test/123/",
            job_name="test-pipeline",
            build_number=123,
            build_result="FAILURE",
            timestamp="2024-08-17T17:55:40Z",
            parameters={"CLUSTER_NAME": "test", "BRANCH": "main"},
            console_log_snippet="Detailed error information available",
            artifacts=["results.xml", "logs.zip"],
            branch="main",
            commit_sha="abc123"
        )
        
        maximal_failure_analysis = {'total_failures': 5}
        
        maximal_confidence = self.jenkins_service._calculate_confidence_score(
            maximal_metadata, maximal_failure_analysis
        )
        
        # Should be higher confidence and within bounds
        self.assertIsInstance(maximal_confidence, float)
        self.assertGreaterEqual(maximal_confidence, 0.0)
        self.assertLessEqual(maximal_confidence, 1.0)
        self.assertGreater(maximal_confidence, minimal_confidence)


if __name__ == '__main__':
    # Set up test discovery and execution
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestIntegrationEdgeCases))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestRealWorldEdgeCases))
    
    # Run tests with detailed output
    test_runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = test_runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)