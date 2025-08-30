#!/usr/bin/env python3
"""
Comprehensive Unit Tests for E2E Enforcement Logic Fixes

Tests the critical bug fixes in E2E enforcement:
1. Bug Fix: Don't block when violations = 0 (regardless of percentage)
2. Enhanced E2E percentage calculation to recognize valid content
3. Deployment-agnostic override functionality
4. Proper violation detection for actual prohibited content
5. Edge cases and robustness scenarios

Ensures the framework ALWAYS generates test plans when appropriate.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from typing import Dict, Any, Tuple

# Add the enforcement directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'enforcement'))

from e2e_focus_enforcer import (
    E2EFocusEnforcer,
    enforce_e2e_focus
)

class TestE2EEnforcementFixes(unittest.TestCase):
    """Test the critical E2E enforcement bug fixes"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.enforcer = E2EFocusEnforcer()
        
        # Sample valid E2E content (should pass)
        self.valid_e2e_content = """
# Test Cases for ACM-22079

## Test Case 1: Validate ClusterCurator Digest Upgrades

**Description**: Verify ClusterCurator digest-based upgrade functionality

**Setup**: 
- Access to ACM Console
- ClusterCurator v1beta1 available

### Test Steps

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Navigate to console URL | oc login <cluster-url> | Successful login |
| 2 | Create ClusterCurator | Click Create → Configure digest | oc apply -f curator.yaml | ClusterCurator created |
| 3 | Verify upgrade workflow | Monitor status in UI | oc get clustercurator | Status shows progress |

## Test Case 2: Verify Error Handling

**Description**: Test error scenarios for digest upgrades

**Setup**: ClusterCurator environment ready

### Test Steps

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Attempt invalid digest | Enter invalid digest in UI | oc edit clustercurator | Validation error shown |
| 2 | Verify error recovery | Check error handling | oc describe clustercurator | Error conditions logged |
"""
        
        # Sample content with violations (should fail)
        self.content_with_violations = """
# Test Cases

## 1. Unit Testing Priority

### Unit Test Cases
- Test individual components in isolation
- Mock external dependencies
- Validate function return values

## 2. Integration Testing Priority

### Integration Test Scenarios
- Test component interactions
- Validate API integrations
- Test database connections

## 3. Performance Testing Priority

### Performance Test Cases
- Load testing scenarios
- Stress testing validation
- Benchmark comparisons
"""
        
        # Sample content with zero violations but low percentage (the bug scenario)
        self.generic_content_zero_violations = """
# Test Plan

## Feature Testing

**Description**: Test the feature functionality

**Steps**:
1. Access the system
2. Configure the feature
3. Execute the workflow
4. Verify the results

This is generic test content that doesn't contain explicit prohibited patterns
but also doesn't match the old E2E percentage calculation patterns.
"""

class TestCriticalBugFixes(TestE2EEnforcementFixes):
    """Test the critical bug fixes that were causing blocking"""
    
    def test_zero_violations_always_pass_regardless_of_percentage(self):
        """CRITICAL: Zero violations should ALWAYS pass, regardless of percentage calculation"""
        
        # This was the core bug - content with 0 violations but low percentage was blocked
        test_cases = [
            self.valid_e2e_content,
            self.generic_content_zero_violations,
            "# Simple test case\n\nTest something basic.",
            "Feature validation test plan with setup and expected results.",
        ]
        
        for content in test_cases:
            with self.subTest(content=content[:50] + "..."):
                is_compliant, validation_details = self.enforcer.validate_e2e_focus_compliance(content)
                
                # If there are no violations, it should ALWAYS be compliant
                if len(validation_details["violations"]) == 0:
                    self.assertTrue(is_compliant, 
                                  f"BUG: Content with 0 violations was blocked!\n"
                                  f"Violations: {validation_details['violations']}\n"
                                  f"E2E %: {validation_details['e2e_focus_percentage']}\n"
                                  f"Content: {content[:100]}...")
                    self.assertEqual(validation_details["compliance_score"], 100,
                                   "Compliance score should be 100 for zero violations")
    
    def test_actual_violations_still_caught(self):
        """Ensure actual violations are still properly detected and blocked"""
        
        passed, result = self.enforcer.enforce_e2e_focus(self.content_with_violations)
        
        self.assertFalse(passed, "Content with actual violations should be blocked")
        self.assertGreater(result["total_violations"], 0, "Should detect actual violations")
        self.assertGreater(result["prohibited_categories_detected"], 0, "Should detect prohibited categories")
        self.assertLess(result["compliance_score"], 100, "Compliance score should be < 100 for violations")
    
    def test_enhanced_e2e_percentage_calculation(self):
        """Test the enhanced E2E percentage calculation recognizes valid content"""
        
        # Valid E2E content should get high percentage
        e2e_percentage = self.enforcer._calculate_e2e_percentage(self.valid_e2e_content)
        self.assertGreaterEqual(e2e_percentage, 85, 
                               f"Valid E2E content should get high percentage, got {e2e_percentage}%")
        
        # Generic content without violations should get reasonable percentage
        generic_percentage = self.enforcer._calculate_e2e_percentage(self.generic_content_zero_violations)
        self.assertGreaterEqual(generic_percentage, 70,
                               f"Generic valid content should get reasonable percentage, got {generic_percentage}%")
        
        # Content with prohibited patterns should get lower percentage
        violation_percentage = self.enforcer._calculate_e2e_percentage(self.content_with_violations)
        self.assertLess(violation_percentage, 70,
                       f"Content with violations should get lower percentage, got {violation_percentage}%")
    
    def test_deployment_agnostic_override_functionality(self):
        """Test the deployment-agnostic override functionality"""
        
        # Without override: should respect normal logic
        passed_normal, result_normal = self.enforcer.enforce_e2e_focus(self.generic_content_zero_violations, False)
        
        # With override: should pass if no violations (even with low percentage)
        passed_override, result_override = self.enforcer.enforce_e2e_focus(self.generic_content_zero_violations, True)
        
        # Both should pass because there are no violations, but override should ensure it
        self.assertTrue(passed_override, "Deployment-agnostic override should pass content with 0 violations")
        self.assertTrue(result_override["deployment_agnostic_override"], "Override flag should be set")
        
        # Override should not bypass actual violations
        passed_violation, result_violation = self.enforcer.enforce_e2e_focus(self.content_with_violations, True)
        self.assertFalse(passed_violation, "Override should not bypass actual violations")

class TestContentRecognitionPatterns(TestE2EEnforcementFixes):
    """Test recognition of various E2E content patterns"""
    
    def test_table_format_recognition(self):
        """Test recognition of table-format test cases"""
        
        table_content = """
| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Login to console | Navigate to URL | oc login | Success |
| 2 | Create resource | Click Create | oc apply | Resource created |
"""
        
        percentage = self.enforcer._calculate_e2e_percentage(table_content)
        self.assertGreaterEqual(percentage, 90, "Table format should get high E2E percentage")
    
    def test_workflow_description_recognition(self):
        """Test recognition of workflow descriptions"""
        
        workflow_content = """
## End-to-End Workflow Test

**Description**: Verify complete user workflow

**Setup**: Environment ready

**Steps**:
1. Navigate to the application
2. Configure settings
3. Execute workflow
4. Verify results

**Expected Results**: Workflow completes successfully
"""
        
        percentage = self.enforcer._calculate_e2e_percentage(workflow_content)
        self.assertGreaterEqual(percentage, 85, "Workflow content should get high E2E percentage")
    
    def test_scenario_based_recognition(self):
        """Test recognition of scenario-based test content"""
        
        scenario_content = """
## User Scenario Testing

### Scenario 1: Administrator performs cluster upgrade
- User logs into ACM console
- User navigates to cluster management
- User initiates upgrade workflow
- System processes upgrade request
- User verifies upgrade completion

### Scenario 2: Error handling validation
- User attempts invalid operation
- System displays appropriate error
- User follows recovery steps
"""
        
        percentage = self.enforcer._calculate_e2e_percentage(scenario_content)
        self.assertGreaterEqual(percentage, 80, "Scenario content should get good E2E percentage")
    
    def test_mixed_content_recognition(self):
        """Test recognition of mixed valid E2E content"""
        
        mixed_content = """
# Feature Validation Tests

## Test Case: Complete Feature Workflow

**Description**: Test the feature end-to-end

Setup requirements:
- Console access
- Feature enabled

Test execution:
1. Access the feature
2. Configure parameters  
3. Execute operation
4. Validate outcome

Expected results: Feature works as designed
"""
        
        percentage = self.enforcer._calculate_e2e_percentage(mixed_content)
        self.assertGreaterEqual(percentage, 75, "Mixed valid content should get reasonable E2E percentage")

class TestViolationDetection(TestE2EEnforcementFixes):
    """Test proper detection of prohibited content"""
    
    def test_unit_testing_detection(self):
        """Test detection of unit testing violations"""
        
        unit_content = """
## Unit Testing Priority

### Component Unit Tests
- Test individual functions
- Mock dependencies
- Validate return values
"""
        
        has_violations, violations = self.enforcer.detect_prohibited_test_types(unit_content)
        self.assertTrue(has_violations, "Should detect unit testing violations")
        self.assertGreater(len(violations), 0, "Should list specific violations")
    
    def test_integration_testing_detection(self):
        """Test detection of integration testing violations"""
        
        integration_content = """
## Integration Testing Categories

### Service Integration Tests
- Test API integrations
- Validate component interactions
- Test database connections
"""
        
        has_violations, violations = self.enforcer.detect_prohibited_test_types(integration_content)
        self.assertTrue(has_violations, "Should detect integration testing violations")
    
    def test_performance_testing_detection(self):
        """Test detection of performance testing violations"""
        
        performance_content = """
## Performance Testing Priority

### Load Testing Scenarios
- Benchmark performance metrics
- Stress testing validation
- Resource utilization testing
"""
        
        has_violations, violations = self.enforcer.detect_prohibited_test_types(performance_content)
        self.assertTrue(has_violations, "Should detect performance testing violations")
    
    def test_multiple_violation_detection(self):
        """Test detection of multiple violation types"""
        
        multiple_violations_content = """
## 1. Unit Testing Priority
- Component testing

## 2. Integration Testing Priority  
- API testing

## 3. Performance Testing Priority
- Load testing
"""
        
        has_violations, violations = self.enforcer.detect_prohibited_test_types(multiple_violations_content)
        self.assertTrue(has_violations, "Should detect multiple violations")
        self.assertGreaterEqual(len(violations), 3, "Should detect all violation types")

class TestEdgeCasesAndRobustness(TestE2EEnforcementFixes):
    """Test edge cases and robustness scenarios"""
    
    def test_empty_content(self):
        """Test handling of empty content"""
        
        empty_cases = ["", "   ", "\n\n", "# Empty\n"]
        
        for content in empty_cases:
            with self.subTest(content=repr(content)):
                passed, result = self.enforcer.enforce_e2e_focus(content)
                
                # Empty content should not crash and should have reasonable defaults
                self.assertIsInstance(result["e2e_focus_percentage"], int)
                self.assertIsInstance(result["total_violations"], int)
                self.assertGreaterEqual(result["e2e_focus_percentage"], 0)
    
    def test_very_long_content(self):
        """Test handling of very long content"""
        
        long_content = "# Test Case\n\n" + "This is a test step. " * 1000 + "\n\nExpected result: Success."
        
        try:
            passed, result = self.enforcer.enforce_e2e_focus(long_content)
            
            # Should handle long content without issues
            self.assertIsInstance(result["e2e_focus_percentage"], int)
            self.assertLessEqual(len(result["violations_detail"]), 100)  # Reasonable limit
            
        except Exception as e:
            self.fail(f"Should handle long content gracefully: {e}")
    
    def test_unicode_content(self):
        """Test handling of unicode content"""
        
        unicode_content = """
# Test Plan 测试计划

## Test Case: Functionality Validation 功能验证

**Description**: Test the feature 测试功能

**Steps**:
1. Access system 访问系统
2. Execute workflow 执行工作流
3. Verify results 验证结果

**Expected**: Success 成功
"""
        
        try:
            passed, result = self.enforcer.enforce_e2e_focus(unicode_content)
            
            # Should handle unicode without crashing
            self.assertIsInstance(result["e2e_focus_percentage"], int)
            self.assertGreaterEqual(result["e2e_focus_percentage"], 0)
            
        except Exception as e:
            self.fail(f"Should handle unicode content gracefully: {e}")
    
    def test_malformed_markdown(self):
        """Test handling of malformed markdown"""
        
        malformed_cases = [
            "# Unclosed header\n## Another header\n### Yet another",
            "| Broken | Table\n| Missing | Separators",
            "**Bold without closing\n*Italic without closing",
            "```\nUnclosed code block\nSome code here",
        ]
        
        for content in malformed_cases:
            with self.subTest(content=content[:30] + "..."):
                try:
                    passed, result = self.enforcer.enforce_e2e_focus(content)
                    
                    # Should not crash on malformed markdown
                    self.assertIsInstance(result["e2e_focus_percentage"], int)
                    
                except Exception as e:
                    self.fail(f"Should handle malformed markdown gracefully: {e}")

class TestConvenienceFunctionIntegration(TestE2EEnforcementFixes):
    """Test the convenience function integration"""
    
    def test_enforce_e2e_focus_convenience_function(self):
        """Test the main enforce_e2e_focus convenience function"""
        
        # Test normal usage
        passed, result, report = enforce_e2e_focus(self.valid_e2e_content, "ACM-22079")
        
        self.assertTrue(passed, "Valid E2E content should pass")
        self.assertIn("ACM-22079", report, "Report should include JIRA ticket")
        self.assertGreater(len(report), 100, "Report should be comprehensive")
        
        # Test with deployment-agnostic override
        passed_override, result_override, report_override = enforce_e2e_focus(
            self.generic_content_zero_violations, "ACM-22079", deployment_agnostic=True
        )
        
        self.assertTrue(passed_override, "Should pass with deployment-agnostic override")
        self.assertTrue(result_override["deployment_agnostic_override"], "Override flag should be set")
    
    def test_report_generation_quality(self):
        """Test quality of generated enforcement reports"""
        
        # Test report for passed content
        passed, result, report = enforce_e2e_focus(self.valid_e2e_content, "ACM-22079")
        
        self.assertIn("PASSED", report, "Report should indicate success")
        self.assertIn("E2E Focus Percentage", report, "Report should include percentage")
        self.assertIn("CLAUDE.policies.md", report, "Report should reference policy")
        
        # Test report for failed content
        failed, result_fail, report_fail = enforce_e2e_focus(self.content_with_violations, "ACM-22079")
        
        self.assertIn("FAILED", report_fail, "Report should indicate failure")
        self.assertIn("Violations Detected", report_fail, "Report should list violations")
        self.assertIn("Corrective Actions", report_fail, "Report should provide guidance")

class TestRegressionPrevention(TestE2EEnforcementFixes):
    """Test prevention of the specific bugs that were fixed"""
    
    def test_bug_scenario_zero_violations_low_percentage(self):
        """Test the specific bug scenario that was causing blocking"""
        
        # This exact scenario was causing the bug:
        # - Content has zero violations (no prohibited patterns)
        # - Percentage calculation returns low value (due to calculation issues)
        # - Old logic: percentage < 100 → BLOCK (BUG!)
        # - New logic: violations = 0 → PASS (FIXED!)
        
        bug_content = """
# Test Cases

## Feature Validation

Test the feature functionality with basic steps and verification.

Setup: Environment ready
Steps: Execute workflow
Expected: Success
"""
        
        # Test with the enforcer directly
        is_compliant, validation_details = self.enforcer.validate_e2e_focus_compliance(bug_content)
        
        # Critical: If violations are 0, should ALWAYS be compliant
        violations_count = len(validation_details["violations"])
        if violations_count == 0:
            self.assertTrue(is_compliant, 
                          f"BUG REGRESSION: Content with 0 violations was blocked!\n"
                          f"Violations: {violations_count}\n"
                          f"E2E %: {validation_details['e2e_focus_percentage']}\n"
                          f"Compliance: {validation_details['compliance_score']}")
            self.assertEqual(validation_details["compliance_score"], 100,
                           "Compliance score should be 100 for zero violations")
    
    def test_percentage_calculation_improvement(self):
        """Test that percentage calculation improvements work"""
        
        # Content that old calculation might miss but new one should catch
        improved_recognition_content = """
Test Case 1: Workflow Validation

Description: Verify user workflow functionality

Setup requirements:
- Access to system
- User credentials available

Test execution steps:
1. User logs into application
2. User navigates to feature area
3. User configures feature settings
4. User executes workflow
5. User verifies expected results

Expected outcome: Workflow completes successfully
"""
        
        percentage = self.enforcer._calculate_e2e_percentage(improved_recognition_content)
        
        # New calculation should recognize this as valid E2E content
        self.assertGreaterEqual(percentage, 80, 
                               f"Improved calculation should recognize valid E2E patterns, got {percentage}%")
    
    def test_deployment_agnostic_always_works(self):
        """Test that deployment-agnostic mode always works as intended"""
        
        # Even content that might have edge cases should pass with deployment-agnostic
        edge_case_content = """
Basic test validation for feature.
Simple verification steps.
Expected results documented.
"""
        
        # Should pass with deployment-agnostic override
        passed, result = self.enforcer.enforce_e2e_focus(edge_case_content, deployment_agnostic_override=True)
        
        # If no actual violations, deployment-agnostic should ensure it passes
        if result["total_violations"] == 0:
            self.assertTrue(passed, "Deployment-agnostic override should ensure passage for 0 violations")
            self.assertTrue(result["deployment_agnostic_override"], "Override flag should be recorded")

def run_e2e_enforcement_tests():
    """Run all E2E enforcement tests and provide detailed results"""
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestCriticalBugFixes,
        TestContentRecognitionPatterns,
        TestViolationDetection,
        TestEdgeCasesAndRobustness,
        TestConvenienceFunctionIntegration,
        TestRegressionPrevention,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"E2E ENFORCEMENT FIXES TEST RESULTS")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split(chr(10))[-2]}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split(chr(10))[-2]}")
    
    # Critical check: Ensure no regression bugs
    critical_failures = [f for f in result.failures if "BUG" in f[1] or "REGRESSION" in f[1]]
    if critical_failures:
        print(f"\n🚨 CRITICAL BUG REGRESSIONS DETECTED:")
        for test, traceback in critical_failures:
            print(f"❌ {test}")
    else:
        print(f"\n✅ NO CRITICAL BUG REGRESSIONS DETECTED")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_e2e_enforcement_tests()
    sys.exit(0 if success else 1)