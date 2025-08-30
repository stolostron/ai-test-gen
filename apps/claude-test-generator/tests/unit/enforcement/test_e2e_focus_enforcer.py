#!/usr/bin/env python3
"""
E2E Focus Enforcer Unit Tests
============================

Comprehensive unit tests for E2E Focus Enforcer ensuring mandatory E2E-only test plan generation.
Tests the enforcement system that blocks unit/integration/performance testing per CLAUDE.policies.md.
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
    from e2e_focus_enforcer import (
        E2EFocusEnforcer,
        enforce_e2e_focus
    )
    E2E_ENFORCER_AVAILABLE = True
except ImportError as e:
    E2E_ENFORCER_AVAILABLE = False
    print(f"❌ E2E Focus Enforcer not available: {e}")


class TestE2EFocusEnforcer(unittest.TestCase):
    """Test E2E Focus Enforcer core functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not E2E_ENFORCER_AVAILABLE:
            cls.skipTest(cls, "E2E Focus Enforcer not available")
    
    def setUp(self):
        """Set up test environment"""
        self.enforcer = E2EFocusEnforcer()
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_enforcer_initialization(self):
        """Test E2E Focus Enforcer initializes correctly"""
        enforcer = E2EFocusEnforcer()
        
        self.assertIsInstance(enforcer.prohibited_patterns, set)
        self.assertIsInstance(enforcer.e2e_requirements, dict)
        self.assertEqual(enforcer.violation_threshold, 0)  # Zero tolerance
        
        # Verify prohibited patterns loaded
        self.assertGreater(len(enforcer.prohibited_patterns), 20)
        self.assertIn('unit testing', enforcer.prohibited_patterns)
        self.assertIn('integration testing', enforcer.prohibited_patterns)
        self.assertIn('performance testing', enforcer.prohibited_patterns)
    
    def test_load_prohibited_patterns(self):
        """Test loading of prohibited testing patterns"""
        patterns = self.enforcer._load_prohibited_patterns()
        
        # Verify structure
        self.assertIsInstance(patterns, set)
        self.assertGreater(len(patterns), 30)  # Should have many patterns
        
        # Check key prohibited patterns exist
        expected_patterns = [
            'unit testing', 'unit tests', 'component testing',
            'integration testing', 'integration tests', 'api integration',
            'performance testing', 'performance tests', 'benchmark testing',
            'foundation testing', 'infrastructure testing', 'smoke testing'
        ]
        
        for pattern in expected_patterns:
            self.assertIn(pattern, patterns)
    
    def test_load_e2e_requirements(self):
        """Test loading of E2E testing requirements"""
        requirements = self.enforcer._load_e2e_requirements()
        
        # Verify structure
        self.assertIsInstance(requirements, dict)
        self.assertIn('focus', requirements)
        self.assertIn('scope', requirements)
        self.assertIn('blocked_types', requirements)
        
        # Verify content aligns with CLAUDE.policies.md
        self.assertEqual(requirements['focus'], 'UI_E2E_direct_feature_testing')
        self.assertIn('ui_workflows', requirements['scope'])
        self.assertIn('unit_testing', requirements['blocked_types'])
        self.assertIn('performance_testing', requirements['blocked_types'])
    
    def test_detect_prohibited_test_types_unit_testing(self):
        """Test detection of prohibited unit testing"""
        unit_test_cases = [
            "Unit testing for cluster-curator components",
            "Component tests for validation logic", 
            "Isolated testing of individual functions",
            "Method testing for upgrade algorithms",
            "Class testing for controller objects"
        ]
        
        for test_content in unit_test_cases:
            with self.subTest(content=test_content):
                has_prohibited, violations = self.enforcer.detect_prohibited_test_types(test_content)
                self.assertTrue(has_prohibited, f"Should detect unit testing in: {test_content}")
                self.assertGreater(len(violations), 0)
                # Check that violation mentions unit testing
                violation_text = ' '.join(violations)
                self.assertIn('unit', violation_text.lower())
    
    def test_detect_prohibited_test_types_integration_testing(self):
        """Test detection of prohibited integration testing"""
        integration_test_cases = [
            "Integration testing between cluster-curator and ACM",
            "API integration testing for upgrade endpoints", 
            "Service integration testing for controller communication",
            "System integration testing for multi-cluster scenarios",
            "Interface testing for external service calls"
        ]
        
        for test_content in integration_test_cases:
            with self.subTest(content=test_content):
                has_prohibited, violations = self.enforcer.detect_prohibited_test_types(test_content)
                self.assertTrue(has_prohibited, f"Should detect integration testing in: {test_content}")
                self.assertGreater(len(violations), 0)
                # Check that violation mentions integration testing
                violation_text = ' '.join(violations)
                self.assertIn('integration', violation_text.lower())
    
    def test_detect_prohibited_test_types_performance_testing(self):
        """Test detection of prohibited performance testing"""
        performance_test_cases = [
            "Performance testing of upgrade operations",
            "Benchmark testing for cluster-curator efficiency", 
            "Load testing for high-volume upgrade scenarios",
            "Stress testing for resource-constrained environments",
            "Scalability testing for large cluster deployments"
        ]
        
        for test_content in performance_test_cases:
            with self.subTest(content=test_content):
                has_prohibited, violations = self.enforcer.detect_prohibited_test_types(test_content)
                self.assertTrue(has_prohibited, f"Should detect performance testing in: {test_content}")
                self.assertGreater(len(violations), 0)
                # Check that violation mentions performance testing
                violation_text = ' '.join(violations)
                self.assertTrue(any(word in violation_text.lower() for word in ['performance', 'benchmark', 'load', 'stress', 'scalability']))
    
    def test_detect_prohibited_test_types_allowed_e2e(self):
        """Test detection should NOT flag allowed E2E testing"""
        e2e_test_cases = [
            "End-to-end workflow testing for cluster upgrades",
            "E2E user scenario testing for digest-based upgrades", 
            "Workflow validation for complete upgrade process",
            "User journey testing through ACM Console",
            "Feature functionality testing via UI interactions"
        ]
        
        for test_content in e2e_test_cases:
            with self.subTest(content=test_content):
                has_prohibited, violations = self.enforcer.detect_prohibited_test_types(test_content)
                self.assertFalse(has_prohibited, f"Should NOT detect prohibited content in E2E: {test_content}")
                self.assertEqual(len(violations), 0)
    
    def test_extract_prohibited_categories(self):
        """Test extraction of prohibited test category names"""
        test_plan_with_categories = """
        # Test Plan
        
        ### 1. Unit Testing Priority
        Test individual components.
        
        ### 2. Integration Testing Priority  
        Test component interactions.
        
        ### 3. Performance Testing Priority
        Test system performance.
        
        ### 4. E2E Testing Priority
        Test end-to-end workflows.
        """
        
        categories = self.enforcer._extract_prohibited_categories(test_plan_with_categories)
        
        # Should detect the prohibited categories
        self.assertIn('Unit Testing', categories)
        self.assertIn('Integration Testing', categories)
        self.assertIn('Performance Testing', categories)
        # Should NOT include E2E Testing (not prohibited)
        self.assertNotIn('E2E Testing', categories)
    
    def test_calculate_e2e_percentage(self):
        """Test E2E focus percentage calculation"""
        test_cases = [
            # (content, expected_percentage)
            ("### 1. E2E Testing\n### 2. Workflow Testing", 100),  # 2/2 E2E
            ("### 1. Unit Testing\n### 2. E2E Testing", 50),       # 1/2 E2E  
            ("### 1. Unit Testing\n### 2. Integration Testing", 0), # 0/2 E2E
            ("", 0),  # No categories
        ]
        
        for content, expected_percentage in test_cases:
            with self.subTest(content=content):
                percentage = self.enforcer._calculate_e2e_percentage(content)
                self.assertEqual(percentage, expected_percentage)
    
    def test_validate_e2e_focus_compliance_perfect_score(self):
        """Test E2E focus compliance validation - perfect score"""
        perfect_e2e_plan = """
        # Test Plan
        
        ### 1. E2E Workflow Testing
        Test complete user workflows.
        
        ### 2. User Scenario Testing  
        Test real user scenarios.
        
        ### 3. End-to-End Feature Testing
        Test complete feature functionality.
        """
        
        is_compliant, validation_details = self.enforcer.validate_e2e_focus_compliance(perfect_e2e_plan)
        
        # Should be perfectly compliant
        self.assertTrue(is_compliant)
        self.assertEqual(validation_details['compliance_score'], 100)
        self.assertEqual(validation_details['e2e_focus_percentage'], 100)
        self.assertEqual(len(validation_details['prohibited_test_categories']), 0)
        self.assertEqual(len(validation_details['violations']), 0)
    
    def test_validate_e2e_focus_compliance_violations(self):
        """Test E2E focus compliance validation - with violations"""
        violating_plan = """
        # Test Plan
        
        ### 1. Unit Testing Priority P0
        Test individual components.
        
        ### 2. Integration Testing Priority P0
        Test component integration.
        
        ### 3. E2E Testing Priority P1
        Test end-to-end workflows.
        """
        
        is_compliant, validation_details = self.enforcer.validate_e2e_focus_compliance(violating_plan)
        
        # Should not be compliant
        self.assertFalse(is_compliant)
        self.assertLess(validation_details['compliance_score'], 100)
        self.assertLess(validation_details['e2e_focus_percentage'], 100)
        self.assertGreater(len(validation_details['prohibited_test_categories']), 0)
        self.assertGreater(len(validation_details['violations']), 0)
        
        # Should detect specific violations
        violations_text = ' '.join(validation_details['violations'])
        self.assertIn('unit', violations_text.lower())
        self.assertIn('integration', violations_text.lower())
        
        # Should have enforcement actions
        self.assertGreater(len(validation_details['enforcement_actions']), 0)
        action_types = [action['action'] for action in validation_details['enforcement_actions']]
        self.assertIn('remove_test_category', action_types)
    
    def test_enforce_e2e_focus_success(self):
        """Test E2E focus enforcement - success case"""
        compliant_plan = """
        # Test Plan
        
        ### 1. End-to-End Workflow Testing
        Test complete upgrade workflows through ACM Console.
        
        ### 2. User Scenario Testing
        Test real customer scenarios for digest-based upgrades.
        """
        
        passed, result = self.enforcer.enforce_e2e_focus(compliant_plan)
        
        # Should pass enforcement
        self.assertTrue(passed)
        self.assertTrue(result['enforcement_passed'])
        self.assertEqual(result['prohibited_categories_detected'], 0)
        self.assertEqual(result['total_violations'], 0)
        self.assertEqual(result['compliance_score'], 100)
        self.assertEqual(result['e2e_focus_percentage'], 100)
    
    def test_enforce_e2e_focus_failure(self):
        """Test E2E focus enforcement - failure case"""
        non_compliant_plan = """
        # Test Plan
        
        ### 1. Unit Testing Priority P0
        Test cluster-curator components individually.
        
        ### 2. Integration Testing Priority P0
        Test API integration between services.
        
        ### 3. Performance Testing Priority P0
        Test system performance and resource usage.
        
        ### 4. E2E Testing Priority P1
        Test end-to-end workflows.
        """
        
        passed, result = self.enforcer.enforce_e2e_focus(non_compliant_plan)
        
        # Should fail enforcement
        self.assertFalse(passed)
        self.assertFalse(result['enforcement_passed'])
        self.assertEqual(result['prohibited_categories_detected'], 3)  # Unit, Integration, Performance
        self.assertGreater(result['total_violations'], 0)
        self.assertLess(result['compliance_score'], 100)
        self.assertLess(result['e2e_focus_percentage'], 100)
        
        # Should have corrective recommendations
        self.assertGreater(len(result['corrective_recommendations']), 0)
        recommendations_text = ' '.join(result['corrective_recommendations'])
        self.assertIn('Remove all unit testing', recommendations_text)
        self.assertIn('Remove all integration testing', recommendations_text)
        self.assertIn('Remove all performance testing', recommendations_text)
    
    def test_generate_e2e_enforcement_prompt(self):
        """Test E2E enforcement prompt generation"""
        prompt = self.enforcer.generate_e2e_enforcement_prompt()
        
        # Verify prompt content
        self.assertIn('CRITICAL E2E FOCUS ENFORCEMENT', prompt)
        self.assertIn('CLAUDE.policies.md', prompt)
        self.assertIn('MANDATORY REQUIREMENTS', prompt)
        self.assertIn('STRICTLY BLOCKED', prompt)
        self.assertIn('Unit Testing categories', prompt)
        self.assertIn('Integration Testing categories', prompt)
        self.assertIn('Performance Testing categories', prompt)
        self.assertIn('Zero tolerance', prompt)
        self.assertIn('100% E2E focus', prompt)
    
    def test_generate_enforcement_report(self):
        """Test enforcement report generation"""
        mock_result = {
            'enforcement_passed': False,
            'e2e_focus_percentage': 25,
            'compliance_score': 25,
            'prohibited_categories_detected': 3,
            'total_violations': 15,
            'enforcement_actions': [
                {
                    'category': 'Unit Testing',
                    'action': 'remove_test_category',
                    'reason': 'Violates CLAUDE.policies.md E2E-only requirement',
                    'policy_reference': 'MANDATORY E2E DIRECT FEATURE TESTING PROTOCOL'
                }
            ],
            'violations_detail': [
                'Prohibited test type detected: unit testing',
                'Unit testing marked as P0 priority'
            ],
            'corrective_recommendations': [
                'Remove all unit testing categories',
                'Focus exclusively on end-to-end user workflows'
            ]
        }
        
        report = self.enforcer.generate_enforcement_report(mock_result, "ACM-22079")
        
        # Verify report structure
        self.assertIn('# E2E Focus Enforcement Report', report)
        self.assertIn('ACM-22079', report)
        self.assertIn('FAILED', report)
        self.assertIn('CLAUDE.policies.md', report)
        
        # Verify summary section
        self.assertIn('25%', report)  # E2E focus percentage
        self.assertIn('3', report)    # prohibited categories
        self.assertIn('15', report)   # total violations
        
        # Verify enforcement actions
        self.assertIn('Remove: Unit Testing', report)
        self.assertIn('MANDATORY E2E DIRECT FEATURE TESTING PROTOCOL', report)
        
        # Verify violations detail
        self.assertIn('unit testing', report)
        self.assertIn('P0 priority', report)
        
        # Verify corrective recommendations
        self.assertIn('Remove all unit testing categories', report)
        
        # Verify policy requirements
        self.assertIn('E2E Focus Requirements', report)
        self.assertIn('ZERO TOLERANCE', report)
        self.assertIn('100% E2E focus required', report)


class TestE2EFocusConvenienceFunctions(unittest.TestCase):
    """Test E2E Focus convenience functions"""
    
    @classmethod
    def setUpClass(cls):
        if not E2E_ENFORCER_AVAILABLE:
            cls.skipTest(cls, "E2E Focus Enforcer not available")
    
    def test_enforce_e2e_focus_convenience_function(self):
        """Test the convenience function for E2E focus enforcement"""
        test_plan = """
        ### 1. Unit Testing Priority P0
        Test individual components.
        
        ### 2. E2E Testing Priority P1
        Test end-to-end workflows.
        """
        
        passed, result, report = enforce_e2e_focus(test_plan, "ACM-12345")
        
        # Verify function works
        self.assertIsInstance(passed, bool)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(report, str)
        
        # Should fail due to unit testing and wrong priority
        self.assertFalse(passed)
        self.assertIn('ACM-12345', report)
        self.assertGreater(result['prohibited_categories_detected'], 0)


class TestE2EFocusEdgeCases(unittest.TestCase):
    """Test E2E Focus edge cases and error conditions"""
    
    @classmethod
    def setUpClass(cls):
        if not E2E_ENFORCER_AVAILABLE:
            cls.skipTest(cls, "E2E Focus Enforcer not available")
    
    def setUp(self):
        """Set up test environment"""
        self.enforcer = E2EFocusEnforcer()
    
    def test_enforce_e2e_focus_empty_content(self):
        """Test enforcement with empty content"""
        empty_content = ""
        
        passed, result = self.enforcer.enforce_e2e_focus(empty_content)
        
        # Should pass (no violations in empty content)
        self.assertTrue(passed)
        self.assertEqual(result['prohibited_categories_detected'], 0)
        self.assertEqual(result['total_violations'], 0)
        self.assertEqual(result['e2e_focus_percentage'], 0)  # No categories = 0%
        self.assertEqual(result['compliance_score'], 100)    # No violations = 100%
    
    def test_detect_prohibited_test_types_edge_patterns(self):
        """Test detection with edge case patterns"""
        edge_cases = [
            ("unittest module import", True),    # Contains 'unit'
            ("integration with third party", True), # Contains 'integration'
            ("high performance computing", True),    # Contains 'performance'
            ("testing framework integration", True), # Contains both 'testing' and 'integration'
            ("end-to-end testing workflow", False), # E2E is allowed
            ("user acceptance testing", True),      # Contains 'acceptance testing' (prohibited)
        ]
        
        for content, should_detect in edge_cases:
            with self.subTest(content=content):
                has_prohibited, violations = self.enforcer.detect_prohibited_test_types(content)
                if should_detect:
                    self.assertTrue(has_prohibited, f"Should detect prohibited content in: {content}")
                else:
                    self.assertFalse(has_prohibited, f"Should NOT detect prohibited content in: {content}")
    
    def test_calculate_e2e_percentage_malformed_content(self):
        """Test E2E percentage calculation with malformed content"""
        malformed_cases = [
            "### Testing without number",  # Malformed header
            "## Wrong header level",      # Wrong markdown level
            "### 1. Testing",             # Missing parenthetical requirement
            "Normal text without headers", # No headers at all
        ]
        
        for content in malformed_cases:
            with self.subTest(content=content):
                percentage = self.enforcer._calculate_e2e_percentage(content)
                # Should handle gracefully (return 0 for no valid categories)
                self.assertIsInstance(percentage, int)
                self.assertGreaterEqual(percentage, 0)
                self.assertLessEqual(percentage, 100)
    
    def test_validate_e2e_focus_compliance_boundary_conditions(self):
        """Test E2E focus compliance at boundary conditions"""
        # Test case with exactly 100% E2E focus
        perfect_case = "### 1. E2E Testing\nComplete workflow testing"
        is_compliant, result = self.enforcer.validate_e2e_focus_compliance(perfect_case)
        self.assertTrue(is_compliant)
        self.assertEqual(result['e2e_focus_percentage'], 100)
        
        # Test case with 0% E2E focus
        zero_case = "### 1. Unit Testing\nComponent testing only"
        is_compliant, result = self.enforcer.validate_e2e_focus_compliance(zero_case)
        self.assertFalse(is_compliant)
        self.assertEqual(result['e2e_focus_percentage'], 0)


if __name__ == '__main__':
    print("🧪 E2E Focus Enforcer Unit Tests")
    print("=" * 35)
    print("Testing E2E Focus Enforcement System")
    print("=" * 35)
    
    if not E2E_ENFORCER_AVAILABLE:
        print("❌ E2E Focus Enforcer not available - skipping tests")
        exit(1)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestE2EFocusEnforcer))
    suite.addTests(loader.loadTestsFromTestCase(TestE2EFocusConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestE2EFocusEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print(f"\n📊 E2E Focus Enforcer Test Summary:")
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