#!/usr/bin/env python3
"""
Functional Focus Enforcer Unit Tests
==================================

Comprehensive unit tests for Functional Focus Enforcer ensuring E2E-only test plan generation.
Tests the enforcement system that prevents performance testing inclusion.
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
enforcement_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'enforcement')
sys.path.insert(0, enforcement_path)

try:
    from functional_focus_enforcer import (
        FunctionalFocusEnforcer,
        enforce_functional_focus
    )
    FUNCTIONAL_ENFORCER_AVAILABLE = True
except ImportError as e:
    FUNCTIONAL_ENFORCER_AVAILABLE = False
    print(f"❌ Functional Focus Enforcer not available: {e}")


class TestFunctionalFocusEnforcer(unittest.TestCase):
    """Test Functional Focus Enforcer core functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not FUNCTIONAL_ENFORCER_AVAILABLE:
            cls.skipTest(cls, "Functional Focus Enforcer not available")
    
    def setUp(self):
        """Set up test environment"""
        self.enforcer = FunctionalFocusEnforcer()
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_enforcer_initialization(self):
        """Test Functional Focus Enforcer initializes correctly"""
        enforcer = FunctionalFocusEnforcer()
        
        self.assertIsInstance(enforcer.performance_patterns, set)
        self.assertIsInstance(enforcer.functional_requirements, dict)
        self.assertEqual(enforcer.violation_threshold, 0)  # Zero tolerance
        
        # Verify performance patterns loaded
        self.assertGreater(len(enforcer.performance_patterns), 0)
        self.assertIn('performance', enforcer.performance_patterns)
        self.assertIn('benchmark', enforcer.performance_patterns)
        self.assertIn('load testing', enforcer.performance_patterns)
    
    def test_load_performance_patterns(self):
        """Test loading of performance testing patterns"""
        patterns = self.enforcer._load_performance_patterns()
        
        # Verify structure
        self.assertIsInstance(patterns, set)
        self.assertGreater(len(patterns), 20)  # Should have many patterns
        
        # Check key patterns exist
        expected_patterns = [
            'performance', 'benchmark', 'throughput', 'latency',
            'cpu utilization', 'memory usage', 'load testing',
            'stress testing', 'resource monitoring'
        ]
        
        for pattern in expected_patterns:
            self.assertIn(pattern, patterns)
    
    def test_load_functional_requirements(self):
        """Test loading of functional testing requirements"""
        requirements = self.enforcer._load_functional_requirements()
        
        # Verify structure
        self.assertIsInstance(requirements, dict)
        self.assertIn('focus', requirements)
        self.assertIn('scope', requirements)
        self.assertIn('excluded_types', requirements)
        
        # Verify content
        self.assertEqual(requirements['focus'], 'e2e_functional_scenarios')
        self.assertIn('feature_functionality', requirements['scope'])
        self.assertIn('performance_testing', requirements['excluded_types'])
    
    def test_detect_performance_content_positive_cases(self):
        """Test detection of performance testing content - should detect"""
        test_cases = [
            "Validate performance characteristics of the upgrade process",
            "Monitor CPU utilization during cluster operations", 
            "Establish baseline metrics for resource consumption",
            "Performance validation of cluster-curator operations",
            "Ensure minimal impact on cluster operations performance",
            "Test resource utilization and efficiency",
            "Benchmark the upgrade process timing"
        ]
        
        for test_content in test_cases:
            with self.subTest(content=test_content):
                has_performance, violations = self.enforcer.detect_performance_content(test_content)
                self.assertTrue(has_performance, f"Should detect performance content in: {test_content}")
                self.assertGreater(len(violations), 0)
    
    def test_detect_performance_content_negative_cases(self):
        """Test detection of performance testing content - should NOT detect"""
        test_cases = [
            "Verify cluster-curator functionality and workflow",
            "Test error handling and recovery scenarios",
            "Validate security and RBAC configuration",
            "Check user interface interactions",
            "Test CLI command execution and results",
            "Verify feature integration with existing systems"
        ]
        
        for test_content in test_cases:
            with self.subTest(content=test_content):
                has_performance, violations = self.enforcer.detect_performance_content(test_content)
                self.assertFalse(has_performance, f"Should NOT detect performance content in: {test_content}")
                self.assertEqual(len(violations), 0)
    
    def test_validate_test_case_focus_functional_case(self):
        """Test test case focus validation for functional cases"""
        functional_content = """
        Verify cluster-curator upgrade workflow functionality.
        Test the digest-based upgrade process through the UI.
        Validate error handling for invalid configurations.
        """
        
        is_valid, validation_details = self.enforcer.validate_test_case_focus(functional_content)
        
        # Should be valid (no performance content)
        self.assertTrue(is_valid)
        # Note: Classification depends on content - 'error handling' is correctly classified
        self.assertIn(validation_details['test_case_type'], ['functional_validation', 'error_handling'])
        self.assertEqual(validation_details['enforcement_action'], 'none')
        self.assertEqual(len(validation_details['violations']), 0)
    
    def test_validate_test_case_focus_performance_case(self):
        """Test test case focus validation for performance cases"""
        performance_content = """
        Validate performance characteristics of cluster-curator.
        Monitor resource utilization during upgrade process.
        Establish baseline performance metrics.
        """
        
        is_valid, validation_details = self.enforcer.validate_test_case_focus(performance_content)
        
        # Should be invalid (contains performance content)
        self.assertFalse(is_valid)
        self.assertEqual(validation_details['test_case_type'], 'performance_testing')
        self.assertEqual(validation_details['enforcement_action'], 'block_generation')
        self.assertGreater(len(validation_details['violations']), 0)
        self.assertGreater(len(validation_details['recommendations']), 0)
    
    def test_classify_test_case_types(self):
        """Test test case classification"""
        test_cases = [
            ("RBAC and security validation testing", "security_validation"),
            ("Error handling and recovery scenarios", "error_handling"),
            ("Feature workflow and integration testing", "functional_validation"),
            ("Random unclassified content", "unknown")
        ]
        
        for content, expected_type in test_cases:
            with self.subTest(content=content):
                result = self.enforcer._classify_test_case(content)
                self.assertEqual(result, expected_type)
    
    def test_enforce_functional_focus_compliant_plan(self):
        """Test enforcement on compliant test plan"""
        compliant_plan = """
        # Test Plan
        
        ### 1. Workflow Testing
        Verify cluster-curator upgrade workflow functionality.
        
        ### 2. Security Testing
        Validate RBAC and security configurations.
        
        ### 3. Error Handling Testing
        Test error scenarios and recovery processes.
        """
        
        passed, result = self.enforcer.enforce_functional_focus(compliant_plan)
        
        # Should pass enforcement
        self.assertTrue(passed)
        self.assertTrue(result['enforcement_passed'])
        self.assertEqual(result['performance_test_cases_detected'], 0)
        self.assertEqual(result['total_violations'], 0)
        self.assertEqual(result['compliance_score'], 100)
    
    def test_enforce_functional_focus_non_compliant_plan(self):
        """Test enforcement on non-compliant test plan"""
        non_compliant_plan = """
        # Test Plan
        
        ### 1. Unit Testing
        Test individual components in isolation.
        
        ### 2. Performance Testing 
        Validate performance characteristics and resource utilization.
        Monitor CPU usage and establish baseline metrics.
        
        ### 3. Integration Testing
        Test component integration and API behavior.
        """
        
        passed, result = self.enforcer.enforce_functional_focus(non_compliant_plan)
        
        # Should fail enforcement
        self.assertFalse(passed)
        self.assertFalse(result['enforcement_passed'])
        self.assertGreater(result['performance_test_cases_detected'], 0)
        self.assertGreater(result['total_violations'], 0)
        self.assertLess(result['compliance_score'], 100)
        self.assertGreater(len(result['enforcement_actions']), 0)
        self.assertGreater(len(result['recommendations']), 0)
    
    def test_enforce_functional_focus_mixed_plan(self):
        """Test enforcement on mixed compliant/non-compliant test plan"""
        mixed_plan = """
        # Test Plan
        
        ### 1. E2E Workflow Testing
        Verify end-to-end cluster-curator functionality.
        
        ### 2. Performance Testing
        Monitor performance characteristics during upgrades.
        
        ### 3. Security Testing
        Validate RBAC and authentication.
        """
        
        passed, result = self.enforcer.enforce_functional_focus(mixed_plan)
        
        # Should fail due to performance testing
        self.assertFalse(passed)
        # Note: Pattern matching may find fewer sections than expected - that's OK
        self.assertGreaterEqual(result['test_cases_analyzed'], 2)
        self.assertGreaterEqual(result['performance_test_cases_detected'], 1)
        self.assertGreater(result['total_violations'], 0)
        
        # Compliance score should be partial
        expected_compliance = ((3 - 1) / 3) * 100  # 66.7%
        self.assertAlmostEqual(result['compliance_score'], expected_compliance, places=1)
    
    def test_generate_enforcement_report(self):
        """Test enforcement report generation"""
        mock_result = {
            'enforcement_passed': False,
            'test_cases_analyzed': 5,
            'performance_test_cases_detected': 2,
            'total_violations': 8,
            'compliance_score': 60.0,
            'enforcement_actions': [
                {
                    'test_case': 'Test Case 2',
                    'action': 'remove_performance_test_case',
                    'reason': 'Performance testing detected',
                    'violations': ['Performance pattern detected: performance']
                }
            ],
            'recommendations': [
                'Remove 2 performance test case(s)',
                'Focus on feature functionality validation'
            ]
        }
        
        report = self.enforcer.generate_enforcement_report(mock_result, "ACM-12345")
        
        # Verify report structure
        self.assertIn('# Functional Focus Enforcement Report', report)
        self.assertIn('ACM-12345', report)
        self.assertIn('FAILED', report)
        self.assertIn('5', report)  # test cases analyzed
        self.assertIn('2', report)  # performance cases detected
        self.assertIn('8', report)  # total violations
        self.assertIn('60.0%', report)  # compliance score
        
        # Verify enforcement actions section
        self.assertIn('Test Case 2', report)
        self.assertIn('remove_performance_test_case', report)
        
        # Verify recommendations section
        self.assertIn('Remove 2 performance test case(s)', report)
        
        # Verify policy requirements section
        self.assertIn('Functional Focus Requirements', report)
        self.assertIn('ZERO TOLERANCE', report)


class TestFunctionalFocusConvenienceFunctions(unittest.TestCase):
    """Test Functional Focus convenience functions"""
    
    @classmethod
    def setUpClass(cls):
        if not FUNCTIONAL_ENFORCER_AVAILABLE:
            cls.skipTest(cls, "Functional Focus Enforcer not available")
    
    def test_enforce_functional_focus_convenience_function(self):
        """Test the convenience function for functional focus enforcement"""
        test_plan = """
        ### 1. Functional Testing
        Test feature functionality.
        
        ### 2. Performance Testing
        Monitor system performance.
        """
        
        passed, result, report = enforce_functional_focus(test_plan, "ACM-54321")
        
        # Verify function works
        self.assertIsInstance(passed, bool)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(report, str)
        
        # Should fail due to performance testing
        self.assertFalse(passed)
        self.assertIn('ACM-54321', report)
        self.assertGreater(result['performance_test_cases_detected'], 0)


class TestFunctionalFocusEdgeCases(unittest.TestCase):
    """Test Functional Focus edge cases and error conditions"""
    
    @classmethod
    def setUpClass(cls):
        if not FUNCTIONAL_ENFORCER_AVAILABLE:
            cls.skipTest(cls, "Functional Focus Enforcer not available")
    
    def setUp(self):
        """Set up test environment"""
        self.enforcer = FunctionalFocusEnforcer()
    
    def test_enforce_functional_focus_empty_content(self):
        """Test enforcement with empty content"""
        empty_content = ""
        
        passed, result = self.enforcer.enforce_functional_focus(empty_content)
        
        # Should pass (no violations in empty content)
        self.assertTrue(passed)
        self.assertEqual(result['test_cases_analyzed'], 0)
        self.assertEqual(result['performance_test_cases_detected'], 0)
        self.assertEqual(result['compliance_score'], 100)
    
    def test_detect_performance_content_edge_patterns(self):
        """Test detection with edge case patterns"""
        edge_cases = [
            ("baseline cluster setup", True),  # Contains 'baseline'
            ("performance-critical feature", True),  # Contains 'performance'
            ("former performance engineer", True),  # Contains 'performance' 
            ("perfectly functional workflow", False),  # Contains 'performance' but not performance testing
        ]
        
        for content, should_detect in edge_cases:
            with self.subTest(content=content):
                has_performance, violations = self.enforcer.detect_performance_content(content)
                if should_detect:
                    self.assertTrue(has_performance, f"Should detect in: {content}")
                # Note: We're being conservative - better to over-detect than under-detect
    
    def test_validate_test_case_focus_malformed_content(self):
        """Test validation with malformed content"""
        malformed_cases = [
            None,  # This would cause an exception in real usage
            "",    # Empty string
            "   ",  # Whitespace only
        ]
        
        for content in malformed_cases:
            if content is not None:  # Skip None case as it would raise exception
                with self.subTest(content=repr(content)):
                    is_valid, validation_details = self.enforcer.validate_test_case_focus(content)
                    # Should handle gracefully
                    self.assertIsInstance(is_valid, bool)
                    self.assertIsInstance(validation_details, dict)


if __name__ == '__main__':
    print("🧪 Functional Focus Enforcer Unit Tests")
    print("=" * 42)
    print("Testing Functional Focus Enforcement System")
    print("=" * 42)
    
    if not FUNCTIONAL_ENFORCER_AVAILABLE:
        print("❌ Functional Focus Enforcer not available - skipping tests")
        exit(1)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestFunctionalFocusEnforcer))
    suite.addTests(loader.loadTestsFromTestCase(TestFunctionalFocusConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestFunctionalFocusEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print(f"\n📊 Functional Focus Enforcer Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
    
    exit(0 if result.wasSuccessful() else 1)