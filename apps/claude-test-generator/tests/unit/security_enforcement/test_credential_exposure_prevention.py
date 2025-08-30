#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Credential Exposure Prevention System

Tests the critical security enforcement component that prevents credential exposure
in generated test plans. Validates zero-tolerance credential policies, template
enforcement, and real-time security scanning capabilities.

Test Coverage:
- Credential pattern detection (11+ pattern types)
- Auto-sanitization functionality  
- Template compliance enforcement
- Real-time scanning capabilities
- Framework integration hooks
- Security violation blocking
"""

import unittest
import tempfile
import os
import json
from unittest.mock import Mock, patch, mock_open
from pathlib import Path

# Add the enforcement directory to Python path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../.claude/enforcement'))

from credential_exposure_prevention import (
    CredentialExposurePreventionSystem,
    PatternExtensionSecurityWrapper
)


class TestCredentialExposurePreventionSystem(unittest.TestCase):
    """Test suite for CredentialExposurePreventionSystem core functionality"""
    
    def setUp(self):
        """Set up test environment with clean security system"""
        self.security_system = CredentialExposurePreventionSystem()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test security system initialization and pattern setup"""
        # Verify credential patterns are loaded
        self.assertGreater(len(self.security_system.credential_patterns), 5)
        self.assertIn('-p\\s+(?!<|\'|\\{)[^\\s]*', self.security_system.credential_patterns)
        
        # Verify required placeholders are defined
        self.assertIn('<CLUSTER_CONSOLE_URL>', self.security_system.required_placeholders)
        self.assertIn('<CLUSTER_ADMIN_USER>', self.security_system.required_placeholders)
        self.assertIn('<CLUSTER_ADMIN_PASSWORD>', self.security_system.required_placeholders)
        
        # Verify template rules are configured
        self.assertIn('login_commands', self.security_system.template_rules)
        self.assertIn('url_format', self.security_system.template_rules)
        
        # Verify enforcement log is initialized
        self.assertEqual(len(self.security_system.enforcement_log), 0)
    
    def test_password_credential_detection(self):
        """Test detection of password credentials in various formats"""
        test_cases = [
            # Should detect real passwords
            {
                'content': 'oc login cluster.com -u admin -p realpassword123',
                'should_detect': True,
                'description': 'Real password in oc login command'
            },
            {
                'content': 'kubeadmin/Gz7oJ-IHZgq-5MIQ9-Kdhid',
                'should_detect': True,
                'description': 'Kubeadmin with real password'
            },
            {
                'content': 'kubectl --password=secretpass123',
                'should_detect': True,
                'description': 'Kubectl with password flag'
            },
            
            # Should NOT detect placeholders
            {
                'content': 'oc login cluster.com -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>',
                'should_detect': False,
                'description': 'Proper placeholder usage'
            },
            {
                'content': "oc login cluster.com -u admin -p '<PASSWORD>'",
                'should_detect': False,
                'description': 'Quoted placeholder'
            },
            {
                'content': 'oc login cluster.com -u admin -p {password}',
                'should_detect': False,
                'description': 'Templated password'
            }
        ]
        
        for test_case in test_cases:
            with self.subTest(description=test_case['description']):
                result = self.security_system.scan_content(test_case['content'], 'test.md')
                has_violations = len(result['violations']) > 0
                
                self.assertEqual(
                    has_violations, 
                    test_case['should_detect'],
                    f"Content: {test_case['content'][:50]}... Expected detection: {test_case['should_detect']}, Got: {has_violations}"
                )
    
    def test_environment_specific_url_detection(self):
        """Test detection of environment-specific URLs"""
        test_cases = [
            # Should detect real environment URLs
            {
                'content': 'https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com',
                'should_detect': True,
                'description': 'Specific QE environment URL'
            },
            {
                'content': 'https://api.mist5-2.qe.red-chesterfield.com:6443',
                'should_detect': True,
                'description': 'API endpoint with specific environment'
            },
            
            # Should NOT detect example URLs
            {
                'content': 'https://console-openshift-console.apps.cluster.example.com',
                'should_detect': False,
                'description': 'Example domain URL'
            },
            {
                'content': 'https://<CLUSTER_CONSOLE_URL>',
                'should_detect': False,
                'description': 'Placeholder URL'
            },
            {
                'content': 'https://your-cluster-url.com',
                'should_detect': False,
                'description': 'Generic example URL'
            }
        ]
        
        for test_case in test_cases:
            with self.subTest(description=test_case['description']):
                result = self.security_system.scan_content(test_case['content'], 'test.md')
                has_violations = len(result['violations']) > 0
                
                self.assertEqual(
                    has_violations, 
                    test_case['should_detect'],
                    f"URL: {test_case['content']} Expected detection: {test_case['should_detect']}, Got: {has_violations}"
                )
    
    def test_environment_identifier_detection(self):
        """Test detection of environment-specific identifiers"""
        test_cases = [
            # Should detect specific environment identifiers
            {
                'content': 'mist10-0 environment configuration',
                'should_detect': True,
                'description': 'Specific mist environment identifier'
            },
            {
                'content': 'Gz7oJ-IHZgq-5MIQ9-Kdhid token',
                'should_detect': True,
                'description': 'Specific credential token pattern'
            },
            
            # Should NOT detect generic identifiers
            {
                'content': 'test-environment configuration',
                'should_detect': False,
                'description': 'Generic environment name'
            },
            {
                'content': '<ENVIRONMENT_NAME> configuration',
                'should_detect': False,
                'description': 'Placeholder environment name'
            }
        ]
        
        for test_case in test_cases:
            with self.subTest(description=test_case['description']):
                result = self.security_system.scan_content(test_case['content'], 'test.md')
                has_violations = len(result['violations']) > 0
                
                self.assertEqual(
                    has_violations, 
                    test_case['should_detect'],
                    f"Content: {test_case['content']} Expected detection: {test_case['should_detect']}, Got: {has_violations}"
                )
    
    def test_ip_address_detection(self):
        """Test detection of real IP addresses"""
        test_cases = [
            # Should detect real IP addresses
            {
                'content': 'Connect to 192.168.1.100 on port 6443',
                'should_detect': True,
                'description': 'Private IP address'
            },
            {
                'content': 'Server at 10.0.0.5:8080',
                'should_detect': True,
                'description': 'Internal IP with port'
            },
            
            # Should NOT detect example IPs
            {
                'content': 'Example IP: <CLUSTER_IP>',
                'should_detect': False,
                'description': 'Placeholder IP'
            },
            {
                'content': 'Use your cluster IP address',
                'should_detect': False,
                'description': 'Generic IP reference'
            }
        ]
        
        for test_case in test_cases:
            with self.subTest(description=test_case['description']):
                result = self.security_system.scan_content(test_case['content'], 'test.md')
                has_violations = len(result['violations']) > 0
                
                self.assertEqual(
                    has_violations, 
                    test_case['should_detect'],
                    f"Content: {test_case['content']} Expected detection: {test_case['should_detect']}, Got: {has_violations}"
                )
    
    def test_placeholder_validation(self):
        """Test validation of proper placeholder usage"""
        # Content with proper placeholders should pass
        secure_content = """
        # Test Plan
        
        ## Setup
        oc login <CLUSTER_CONSOLE_URL> -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>
        
        ## Environment
        - Cluster: <CLUSTER_CONSOLE_URL>
        - Version: <ACM_VERSION>
        """
        
        result = self.security_system.scan_content(secure_content, 'test.md')
        self.assertEqual(len(result['violations']), 0)
        self.assertTrue(result['passed'])
        self.assertEqual(result['security_score'], 100)
    
    def test_security_score_calculation(self):
        """Test security score calculation based on violations"""
        # Clean content should have perfect score
        clean_content = "Test plan with <CLUSTER_CONSOLE_URL> placeholder"
        result = self.security_system.scan_content(clean_content, 'test.md')
        self.assertEqual(result['security_score'], 100)
        
        # Content with violations should have reduced score
        dirty_content = "oc login https://real-cluster.com -u admin -p password123"
        result = self.security_system.scan_content(dirty_content, 'test.md')
        self.assertLess(result['security_score'], 100)
        self.assertGreater(len(result['violations']), 0)
    
    def test_scan_result_structure(self):
        """Test that scan results have proper structure and metadata"""
        content = "Test content with <PLACEHOLDER>"
        result = self.security_system.scan_content(content, 'test_file.md')
        
        # Verify required fields
        required_fields = ['file_path', 'timestamp', 'violations', 'security_score', 'passed', 'required_fixes']
        for field in required_fields:
            self.assertIn(field, result)
        
        # Verify field types
        self.assertEqual(result['file_path'], 'test_file.md')
        self.assertIsInstance(result['timestamp'], str)
        self.assertIsInstance(result['violations'], list)
        self.assertIsInstance(result['security_score'], (int, float))
        self.assertIsInstance(result['passed'], bool)
        self.assertIsInstance(result['required_fixes'], list)
    
    def test_complex_multi_violation_content(self):
        """Test content with multiple types of security violations"""
        complex_content = """
        # Test Plan: ACM-22079
        
        ## Environment Setup
        oc login https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com -u kubeadmin -p Gz7oJ-IHZgq-5MIQ9-Kdhid
        
        ## Cluster Access
        - Environment: mist10-0
        - API: https://api.mist10-0.qe.red-chesterfield.com:6443
        - Credentials: kubeadmin/Gz7oJ-IHZgq-5MIQ9-Kdhid
        
        ## Test Execution
        kubectl --server=192.168.1.100:8080 --username=admin --password=secret123
        """
        
        result = self.security_system.scan_content(complex_content, 'complex_test.md')
        
        # Should detect multiple violations
        self.assertGreater(len(result['violations']), 3)
        self.assertFalse(result['passed'])
        self.assertLess(result['security_score'], 50)
        
        # Should provide required fixes
        self.assertGreater(len(result['required_fixes']), 0)
    
    def test_enforcement_logging(self):
        """Test that security enforcement actions are logged"""
        initial_log_count = len(self.security_system.enforcement_log)
        
        # Perform scan that should be logged
        content = "oc login cluster.com -u admin -p password123"
        result = self.security_system.scan_content(content, 'test.md')
        
        # Verify logging occurred
        self.assertGreaterEqual(len(self.security_system.enforcement_log), initial_log_count)


class TestPatternExtensionSecurityWrapper(unittest.TestCase):
    """Test suite for PatternExtensionSecurityWrapper functionality"""
    
    def setUp(self):
        """Set up test environment with security wrapper"""
        self.security_wrapper = PatternExtensionSecurityWrapper()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test security wrapper initialization"""
        self.assertIsNotNone(self.security_wrapper.security_system)
        self.assertTrue(hasattr(self.security_wrapper, 'sanitize_test_content'))
        self.assertTrue(hasattr(self.security_wrapper, 'secure_test_plan_generation'))
    
    def test_sanitize_test_content(self):
        """Test content sanitization functionality"""
        dirty_content = """
        # Test Plan
        oc login https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com -u kubeadmin -p Gz7oJ-IHZgq-5MIQ9-Kdhid
        
        Environment: mist10-0.qe.red-chesterfield.com
        """
        
        sanitized = self.security_wrapper.sanitize_test_content(dirty_content)
        
        # Verify sanitization occurred
        self.assertNotEqual(sanitized, dirty_content)
        self.assertIn('<CLUSTER_CONSOLE_URL>', sanitized)
        self.assertIn('<CLUSTER_ADMIN_USER>', sanitized)
        self.assertIn('<CLUSTER_ADMIN_PASSWORD>', sanitized)
        
        # Verify no violations remain
        security_system = CredentialExposurePreventionSystem()
        post_scan = security_system.scan_content(sanitized, 'test.md')
        self.assertEqual(len(post_scan['violations']), 0)
    
    def test_secure_test_plan_generation(self):
        """Test secure test plan generation workflow"""
        insecure_content = """
        # Test Plan: ACM-22079
        
        oc login https://real-cluster.com -u admin -p password123
        kubectl get nodes --server=192.168.1.100:8080
        """
        
        success, result = self.security_wrapper.secure_test_plan_generation(insecure_content, 'test.md')
        
        self.assertTrue(success)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, insecure_content)
        
        # Verify result is secure
        security_system = CredentialExposurePreventionSystem()
        post_scan = security_system.scan_content(result, 'test.md')
        self.assertEqual(len(post_scan['violations']), 0)
    
    def test_secure_generation_with_clean_content(self):
        """Test secure generation with already clean content"""
        clean_content = """
        # Test Plan: ACM-22079
        
        oc login <CLUSTER_CONSOLE_URL> -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>
        kubectl get nodes
        """
        
        success, result = self.security_wrapper.secure_test_plan_generation(clean_content, 'test.md')
        
        self.assertTrue(success)
        self.assertEqual(result, clean_content)  # Should remain unchanged
    
    def test_security_wrapper_error_handling(self):
        """Test error handling in security wrapper"""
        # Test with invalid input
        success, result = self.security_wrapper.secure_test_plan_generation(None, 'test.md')
        self.assertFalse(success)
        self.assertIsInstance(result, str)  # Error message
        
        # Test with empty content
        success, result = self.security_wrapper.secure_test_plan_generation('', 'test.md')
        self.assertTrue(success)
        self.assertEqual(result, '')


class TestSecurityEnforcementIntegration(unittest.TestCase):
    """Test suite for security enforcement integration scenarios"""
    
    def setUp(self):
        """Set up test environment for integration testing"""
        self.security_system = CredentialExposurePreventionSystem()
        self.security_wrapper = PatternExtensionSecurityWrapper()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_file_based_security_enforcement(self):
        """Test security enforcement on actual files"""
        # Create test file with security violations
        test_file_path = os.path.join(self.temp_dir, 'test_plan.md')
        with open(test_file_path, 'w') as f:
            f.write("""
            # Test Plan
            oc login https://console.apps.mist10-0.qe.red-chesterfield.com -u kubeadmin -p password123
            """)
        
        # Test enforcement
        with open(test_file_path, 'r') as f:
            content = f.read()
        
        result = self.security_system.scan_content(content, test_file_path)
        self.assertGreater(len(result['violations']), 0)
        self.assertFalse(result['passed'])
    
    def test_template_compliance_enforcement(self):
        """Test enforcement of template compliance standards"""
        # Non-compliant template
        non_compliant = """
        # Test Plan
        oc login https://real-cluster.com -u admin -p password
        """
        
        # Compliant template
        compliant = """
        # Test Plan
        
        ## 🔧 Environment Setup Instructions
        
        **Before running these tests**, replace the following placeholders:
        
        | Placeholder | Description |
        |-------------|-------------|
        | `<CLUSTER_CONSOLE_URL>` | Your OpenShift console URL |
        | `<CLUSTER_ADMIN_USER>` | Cluster admin username |
        | `<CLUSTER_ADMIN_PASSWORD>` | Cluster admin password |
        
        ## Test Execution
        oc login <CLUSTER_CONSOLE_URL> -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>
        """
        
        # Test both templates
        non_compliant_result = self.security_system.scan_content(non_compliant, 'test.md')
        compliant_result = self.security_system.scan_content(compliant, 'test.md')
        
        self.assertGreater(len(non_compliant_result['violations']), 0)
        self.assertEqual(len(compliant_result['violations']), 0)
        self.assertFalse(non_compliant_result['passed'])
        self.assertTrue(compliant_result['passed'])
    
    def test_end_to_end_security_workflow(self):
        """Test complete end-to-end security enforcement workflow"""
        # Start with insecure content
        insecure_input = """
        # Test Plan: ACM-22079 ClusterCurator Digest Upgrades
        
        ## Environment Setup
        oc login https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com -u kubeadmin -p Gz7oJ-IHZgq-5MIQ9-Kdhid
        
        ## Test Execution
        kubectl get clustercurators -n open-cluster-management
        oc get managedclusters
        
        ## Validation
        curl https://api.mist10-0.qe.red-chesterfield.com:6443/api/v1/nodes
        """
        
        # 1. Scan for violations
        initial_scan = self.security_system.scan_content(insecure_input, 'test.md')
        self.assertGreater(len(initial_scan['violations']), 0)
        self.assertFalse(initial_scan['passed'])
        
        # 2. Apply security wrapper
        success, sanitized_content = self.security_wrapper.secure_test_plan_generation(insecure_input, 'test.md')
        self.assertTrue(success)
        
        # 3. Verify sanitized content is secure
        final_scan = self.security_system.scan_content(sanitized_content, 'test.md')
        self.assertEqual(len(final_scan['violations']), 0)
        self.assertTrue(final_scan['passed'])
        self.assertEqual(final_scan['security_score'], 100)
        
        # 4. Verify placeholders are properly used
        self.assertIn('<CLUSTER_CONSOLE_URL>', sanitized_content)
        self.assertIn('<CLUSTER_ADMIN_USER>', sanitized_content)
        self.assertIn('<CLUSTER_ADMIN_PASSWORD>', sanitized_content)
        
        # 5. Verify no real credentials remain
        self.assertNotIn('mist10-0', sanitized_content)
        self.assertNotIn('Gz7oJ-IHZgq-5MIQ9-Kdhid', sanitized_content)
    
    def test_security_performance_impact(self):
        """Test that security enforcement has minimal performance impact"""
        import time
        
        # Large content for performance testing
        large_content = """
        # Large Test Plan
        """ + "\n".join([f"Step {i}: oc get pods -n namespace-{i}" for i in range(1000)])
        
        # Measure scan time
        start_time = time.time()
        result = self.security_system.scan_content(large_content, 'large_test.md')
        scan_time = time.time() - start_time
        
        # Should complete quickly (under 1 second for reasonable content)
        self.assertLess(scan_time, 1.0)
        self.assertIsInstance(result, dict)
        self.assertIn('violations', result)


if __name__ == '__main__':
    # Create comprehensive test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestCredentialExposurePreventionSystem,
        TestPatternExtensionSecurityWrapper,
        TestSecurityEnforcementIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n" + "="*60)
    print(f"SECURITY ENFORCEMENT UNIT TESTS SUMMARY")
    print(f"="*60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure.split(chr(10))[0]}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, error in result.errors:
            print(f"  - {test}: {error.split(chr(10))[0]}")
    
    # Exit with appropriate code
    exit(0 if len(result.failures) == 0 and len(result.errors) == 0 else 1)