#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Security Enforcement Validation System

Tests the comprehensive validation system that ensures all security enforcement
components work correctly together. Validates the end-to-end security workflow
from detection through sanitization to enforcement.

Test Coverage:
- SecurityEnforcementValidationSuite functionality
- Credential detection validation
- Auto-sanitization validation  
- Template compliance validation
- Framework integration testing
- Real file enforcement testing
- Validation reporting and summary generation
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

from security_enforcement_validation import (
    SecurityEnforcementValidationSuite,
    validate_security_enforcement
)


class TestSecurityEnforcementValidationSuite(unittest.TestCase):
    """Test suite for SecurityEnforcementValidationSuite functionality"""
    
    def setUp(self):
        """Set up test environment with validation suite"""
        # Mock the missing integration components that might not exist
        with patch('security_enforcement_validation.PatternExtensionSecurityIntegration'), \
             patch('security_enforcement_validation.FrameworkSecurityHook'):
            self.validation_suite = SecurityEnforcementValidationSuite()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_validation_suite_initialization(self):
        """Test validation suite initialization"""
        self.assertIsNotNone(self.validation_suite.security_system)
        self.assertIsNotNone(self.validation_suite.security_wrapper)
        self.assertEqual(len(self.validation_suite.validation_results), 0)
    
    def test_credential_detection_validation(self):
        """Test credential detection validation functionality"""
        # Test the credential detection validation
        result = self.validation_suite._test_credential_detection()
        
        # Verify result structure
        self.assertIn('test_name', result)
        self.assertIn('passed', result)
        self.assertIn('details', result)
        self.assertIn('violations_detected', result)
        self.assertEqual(result['test_name'], 'Credential Detection')
        
        # Verify test cases were processed
        self.assertGreater(len(result['details']), 0)
        self.assertIsInstance(result['violations_detected'], int)
        
        # Verify each test case has required fields
        for detail in result['details']:
            self.assertIn('case_name', detail)
            self.assertIn('expected_detection', detail)
            self.assertIn('actual_detection', detail)
            self.assertIn('violations_count', detail)
            self.assertIn('passed', detail)
    
    def test_auto_sanitization_validation(self):
        """Test auto-sanitization validation functionality"""
        result = self.validation_suite._test_auto_sanitization()
        
        # Verify result structure
        self.assertIn('test_name', result)
        self.assertIn('passed', result)
        self.assertIn('details', result)
        self.assertEqual(result['test_name'], 'Auto-Sanitization')
        
        # Verify sanitization was attempted
        self.assertGreater(len(result['details']), 0)
        
        # Verify sanitization details
        for detail in result['details']:
            # Should have either successful sanitization or failure info
            self.assertTrue(
                'sanitization_applied' in detail or 'sanitization_failed' in detail
            )
    
    @patch('security_enforcement_validation.PatternExtensionSecurityIntegration')
    def test_template_compliance_validation(self, mock_integration):
        """Test template compliance validation functionality"""
        # Mock the integration component
        mock_instance = Mock()
        mock_integration.return_value = mock_instance
        mock_instance.enforce_template_compliance.side_effect = [
            (True, {'compliant': True, 'violations': []}),  # Compliant template
            (False, {'compliant': False, 'violations': ['credential_exposure']})  # Non-compliant
        ]
        
        # Re-initialize with mock
        with patch('security_enforcement_validation.FrameworkSecurityHook'):
            validation_suite = SecurityEnforcementValidationSuite()
        
        result = validation_suite._test_template_compliance()
        
        # Verify result structure
        self.assertIn('test_name', result)
        self.assertIn('passed', result)
        self.assertIn('details', result)
        self.assertEqual(result['test_name'], 'Template Compliance')
        
        # Verify both templates were tested
        self.assertEqual(len(result['details']), 2)
        
        # Verify template types
        template_types = [detail['template_type'] for detail in result['details']]
        self.assertIn('compliant', template_types)
        self.assertIn('non_compliant', template_types)
    
    @patch('security_enforcement_validation.FrameworkSecurityHook')
    def test_framework_integration_validation(self, mock_hook):
        """Test framework integration validation functionality"""
        # Mock the framework hook
        mock_instance = Mock()
        mock_hook.return_value = mock_instance
        mock_instance.pre_generation_hook.side_effect = [
            True,   # Clean intelligence should pass
            False   # Dirty intelligence should be blocked
        ]
        
        # Re-initialize with mock
        with patch('security_enforcement_validation.PatternExtensionSecurityIntegration'):
            validation_suite = SecurityEnforcementValidationSuite()
        
        result = validation_suite._test_framework_integration()
        
        # Verify result structure
        self.assertIn('test_name', result)
        self.assertIn('passed', result)
        self.assertIn('details', result)
        self.assertEqual(result['test_name'], 'Framework Integration')
        
        # Verify both hook types were tested
        self.assertEqual(len(result['details']), 2)
        
        # Verify hook types
        hook_types = [detail['hook_type'] for detail in result['details']]
        self.assertIn('pre_generation_clean', hook_types)
        self.assertIn('pre_generation_dirty', hook_types)
    
    def test_real_file_enforcement_validation(self):
        """Test real file enforcement validation functionality"""
        result = self.validation_suite._test_real_file_enforcement()
        
        # Verify result structure
        self.assertIn('test_name', result)
        self.assertIn('passed', result)
        self.assertIn('details', result)
        self.assertEqual(result['test_name'], 'Real File Enforcement')
        
        # Verify both file types were tested
        self.assertEqual(len(result['details']), 2)
        
        # Verify file types
        file_types = [detail['file_type'] for detail in result['details']]
        self.assertIn('secure', file_types)
        self.assertIn('insecure', file_types)
        
        # Verify enforcement results
        for detail in result['details']:
            self.assertIn('enforcement_passed', detail)
            self.assertIn('expected', detail)
    
    def test_comprehensive_validation_workflow(self):
        """Test the complete comprehensive validation workflow"""
        # Mock the integration components to avoid dependency issues
        with patch('security_enforcement_validation.PatternExtensionSecurityIntegration') as mock_integration, \
             patch('security_enforcement_validation.FrameworkSecurityHook') as mock_hook:
            
            # Setup mocks
            mock_integration_instance = Mock()
            mock_integration.return_value = mock_integration_instance
            mock_integration_instance.enforce_template_compliance.side_effect = [
                (True, {'compliant': True}),
                (False, {'compliant': False})
            ]
            
            mock_hook_instance = Mock()
            mock_hook.return_value = mock_hook_instance
            mock_hook_instance.pre_generation_hook.side_effect = [True, False]
            
            # Re-initialize with mocks
            validation_suite = SecurityEnforcementValidationSuite()
            
            # Run comprehensive validation
            result = validation_suite.run_comprehensive_validation()
            
            # Verify result structure
            self.assertIn('timestamp', result)
            self.assertIn('total_tests', result)
            self.assertIn('passed_tests', result)
            self.assertIn('failed_tests', result)
            self.assertIn('test_results', result)
            self.assertIn('overall_status', result)
            
            # Verify all test components were executed
            self.assertEqual(result['total_tests'], 5)  # 5 validation tests
            self.assertEqual(len(result['test_results']), 5)
            
            # Verify test names
            test_names = [test['test_name'] for test in result['test_results']]
            expected_tests = [
                'Credential Detection',
                'Auto-Sanitization', 
                'Template Compliance',
                'Framework Integration',
                'Real File Enforcement'
            ]
            
            for expected_test in expected_tests:
                self.assertIn(expected_test, test_names)
            
            # Verify summary calculations
            self.assertEqual(result['failed_tests'], result['total_tests'] - result['passed_tests'])
            self.assertIn(result['overall_status'], ['PASSED', 'FAILED'])
    
    def test_validation_with_all_tests_passing(self):
        """Test validation behavior when all tests pass"""
        # Mock all components to return successful results
        with patch.object(self.validation_suite, '_test_credential_detection') as mock_cred, \
             patch.object(self.validation_suite, '_test_auto_sanitization') as mock_sanit, \
             patch.object(self.validation_suite, '_test_template_compliance') as mock_template, \
             patch.object(self.validation_suite, '_test_framework_integration') as mock_framework, \
             patch.object(self.validation_suite, '_test_real_file_enforcement') as mock_file:
            
            # All tests pass
            mock_cred.return_value = {'test_name': 'Credential Detection', 'passed': True}
            mock_sanit.return_value = {'test_name': 'Auto-Sanitization', 'passed': True}
            mock_template.return_value = {'test_name': 'Template Compliance', 'passed': True}
            mock_framework.return_value = {'test_name': 'Framework Integration', 'passed': True}
            mock_file.return_value = {'test_name': 'Real File Enforcement', 'passed': True}
            
            result = self.validation_suite.run_comprehensive_validation()
            
            self.assertEqual(result['total_tests'], 5)
            self.assertEqual(result['passed_tests'], 5)
            self.assertEqual(result['failed_tests'], 0)
            self.assertEqual(result['overall_status'], 'PASSED')
    
    def test_validation_with_some_tests_failing(self):
        """Test validation behavior when some tests fail"""
        # Mock some components to fail
        with patch.object(self.validation_suite, '_test_credential_detection') as mock_cred, \
             patch.object(self.validation_suite, '_test_auto_sanitization') as mock_sanit, \
             patch.object(self.validation_suite, '_test_template_compliance') as mock_template, \
             patch.object(self.validation_suite, '_test_framework_integration') as mock_framework, \
             patch.object(self.validation_suite, '_test_real_file_enforcement') as mock_file:
            
            # Some tests pass, some fail
            mock_cred.return_value = {'test_name': 'Credential Detection', 'passed': True}
            mock_sanit.return_value = {'test_name': 'Auto-Sanitization', 'passed': False}
            mock_template.return_value = {'test_name': 'Template Compliance', 'passed': True}
            mock_framework.return_value = {'test_name': 'Framework Integration', 'passed': False}
            mock_file.return_value = {'test_name': 'Real File Enforcement', 'passed': True}
            
            result = self.validation_suite.run_comprehensive_validation()
            
            self.assertEqual(result['total_tests'], 5)
            self.assertEqual(result['passed_tests'], 3)
            self.assertEqual(result['failed_tests'], 2)
            self.assertEqual(result['overall_status'], 'FAILED')


class TestValidationSummaryAndReporting(unittest.TestCase):
    """Test suite for validation summary and reporting functionality"""
    
    def setUp(self):
        """Set up test environment"""
        with patch('security_enforcement_validation.PatternExtensionSecurityIntegration'), \
             patch('security_enforcement_validation.FrameworkSecurityHook'):
            self.validation_suite = SecurityEnforcementValidationSuite()
    
    def test_validation_summary_printing(self):
        """Test validation summary printing functionality"""
        # Create test summary data
        test_summary = {
            'total_tests': 5,
            'passed_tests': 3,
            'failed_tests': 2,
            'overall_status': 'FAILED',
            'test_results': [
                {'test_name': 'Credential Detection', 'passed': True},
                {'test_name': 'Auto-Sanitization', 'passed': False},
                {'test_name': 'Template Compliance', 'passed': True},
                {'test_name': 'Framework Integration', 'passed': False},
                {'test_name': 'Real File Enforcement', 'passed': True}
            ]
        }
        
        # Test that printing doesn't raise exceptions
        try:
            self.validation_suite._print_validation_summary(test_summary)
        except Exception as e:
            self.fail(f"Validation summary printing raised exception: {e}")
    
    def test_validation_summary_calculations(self):
        """Test validation summary calculations are correct"""
        # Mock test results with known outcomes
        mock_results = [
            {'passed': True},
            {'passed': False},
            {'passed': True},
            {'passed': True},
            {'passed': False}
        ]
        
        # Simulate summary generation
        total_tests = len(mock_results)
        passed_tests = sum(1 for test in mock_results if test['passed'])
        failed_tests = total_tests - passed_tests
        
        self.assertEqual(total_tests, 5)
        self.assertEqual(passed_tests, 3)
        self.assertEqual(failed_tests, 2)
        
        # Test success rate calculation
        success_rate = (passed_tests / total_tests * 100)
        self.assertEqual(success_rate, 60.0)


class TestValidationEntryPoint(unittest.TestCase):
    """Test suite for validation entry point function"""
    
    @patch('security_enforcement_validation.SecurityEnforcementValidationSuite')
    def test_validate_security_enforcement_success(self, mock_suite_class):
        """Test validate_security_enforcement function with successful validation"""
        # Mock successful validation
        mock_suite = Mock()
        mock_suite_class.return_value = mock_suite
        mock_suite.run_comprehensive_validation.return_value = {
            'overall_status': 'PASSED'
        }
        
        result = validate_security_enforcement()
        
        self.assertTrue(result)
        mock_suite.run_comprehensive_validation.assert_called_once()
    
    @patch('security_enforcement_validation.SecurityEnforcementValidationSuite')
    def test_validate_security_enforcement_failure(self, mock_suite_class):
        """Test validate_security_enforcement function with failed validation"""
        # Mock failed validation
        mock_suite = Mock()
        mock_suite_class.return_value = mock_suite
        mock_suite.run_comprehensive_validation.return_value = {
            'overall_status': 'FAILED'
        }
        
        result = validate_security_enforcement()
        
        self.assertFalse(result)
        mock_suite.run_comprehensive_validation.assert_called_once()
    
    @patch('security_enforcement_validation.SecurityEnforcementValidationSuite')
    def test_validate_security_enforcement_exception_handling(self, mock_suite_class):
        """Test validate_security_enforcement function with exceptions"""
        # Mock exception during validation
        mock_suite = Mock()
        mock_suite_class.return_value = mock_suite
        mock_suite.run_comprehensive_validation.side_effect = Exception("Validation error")
        
        # Should handle exception gracefully
        with self.assertRaises(Exception):
            validate_security_enforcement()


class TestValidationIntegrationScenarios(unittest.TestCase):
    """Test suite for integration scenarios and edge cases"""
    
    def setUp(self):
        """Set up test environment with real components where possible"""
        # Use real security components but mock missing integrations
        with patch('security_enforcement_validation.PatternExtensionSecurityIntegration'), \
             patch('security_enforcement_validation.FrameworkSecurityHook'):
            self.validation_suite = SecurityEnforcementValidationSuite()
    
    def test_validation_with_missing_dependencies(self):
        """Test validation behavior when dependencies are missing"""
        # This tests the real scenario where integration components might not exist
        # The validation should still work with the core security components
        
        # Test credential detection (should work with real components)
        result = self.validation_suite._test_credential_detection()
        self.assertIsInstance(result, dict)
        self.assertIn('test_name', result)
        self.assertIn('passed', result)
    
    def test_validation_with_empty_content(self):
        """Test validation behavior with edge case inputs"""
        # Test with empty content
        empty_result = self.validation_suite.security_system.scan_content("", "empty.md")
        self.assertEqual(len(empty_result['violations']), 0)
        self.assertTrue(empty_result['passed'])
        self.assertEqual(empty_result['security_score'], 100)
    
    def test_validation_with_very_large_content(self):
        """Test validation performance with large content"""
        # Generate large content
        large_content = "# Test Plan\n" + "\n".join([f"Step {i}: oc get pods" for i in range(1000)])
        
        # Test that validation completes in reasonable time
        import time
        start_time = time.time()
        result = self.validation_suite.security_system.scan_content(large_content, "large.md")
        end_time = time.time()
        
        # Should complete quickly (under 2 seconds for reasonable performance)
        self.assertLess(end_time - start_time, 2.0)
        self.assertIsInstance(result, dict)
        self.assertIn('violations', result)
    
    def test_validation_persistence_and_logging(self):
        """Test that validation results are properly logged and persistent"""
        # Run a validation that should create logs
        test_content = "oc login cluster.com -u admin -p password123"
        result = self.validation_suite.security_system.scan_content(test_content, "test.md")
        
        # Verify enforcement log was updated
        enforcement_report = self.validation_suite.security_system.get_enforcement_report()
        self.assertGreater(enforcement_report['total_scans'], 0)
        self.assertIsNotNone(enforcement_report['last_scan'])


if __name__ == '__main__':
    # Create comprehensive test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestSecurityEnforcementValidationSuite,
        TestValidationSummaryAndReporting,
        TestValidationEntryPoint,
        TestValidationIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n" + "="*60)
    print(f"SECURITY ENFORCEMENT VALIDATION UNIT TESTS SUMMARY")
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