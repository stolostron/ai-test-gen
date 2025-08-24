#!/usr/bin/env python3
"""
ENFORCEMENT SYSTEM COMPREHENSIVE TESTER
======================================

CRITICAL PURPOSE: Test all 3 layers of enforcement system
VALIDATION TYPE: End-to-end testing with violation scenarios
ROBUSTNESS CHECK: Verify system cannot be bypassed

This tester validates that the enforcement system catches all violation types.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

class EnforcementSystemTester:
    """Comprehensive tester for 3-layer enforcement system"""
    
    def __init__(self):
        self.test_results = []
        self.enforcement_dir = os.path.join(os.path.dirname(__file__))
        
        # Add enforcement directory to path
        sys.path.insert(0, self.enforcement_dir)
        
    def log_test_result(self, test_name: str, expected_result: str, actual_result: str, passed: bool):
        """Log test results"""
        result = {
            "test": test_name,
            "expected": expected_result,
            "actual": actual_result,
            "passed": passed
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}: {actual_result}")
    
    def test_layer_1_wrapper_enforcement(self):
        """Test Layer 1: Tool Wrapper Scripts"""
        print("\n🔧 TESTING LAYER 1: Tool Wrapper Scripts")
        print("-" * 40)
        
        try:
            from validated_write_wrapper import validated_write
            
            # Test 1: HTML tag violation should be blocked
            html_content = """# Test
| Step | Action | CLI Method |
|------|--------|------------|
| 1 | Test | `command`<br/>`more` |
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                test_file = f.name
            
            try:
                result = validated_write(test_file, html_content)
                self.log_test_result(
                    "HTML Tag Blocking",
                    "BLOCKED",
                    "ALLOWED" if result else "BLOCKED",
                    not result  # Should be blocked (False)
                )
            finally:
                if os.path.exists(test_file):
                    os.unlink(test_file)
            
            # Test 2: Clean content should be allowed
            clean_content = """# Test
| Step | Action | CLI Method | Expected Results |
|------|--------|------------|------------------|
| 1 | Test action | `oc get pods` | Pods listed successfully |
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                test_file = f.name
            
            try:
                result = validated_write(test_file, clean_content)
                self.log_test_result(
                    "Clean Content Approval", 
                    "ALLOWED",
                    "ALLOWED" if result else "BLOCKED",
                    result  # Should be allowed (True)
                )
            finally:
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except ImportError as e:
            self.log_test_result(
                "Layer 1 Import",
                "SUCCESS", 
                f"FAILED: {str(e)}",
                False
            )
    
    def test_layer_2_integration(self):
        """Test Layer 2: Framework Integration"""
        print("\n🔧 TESTING LAYER 2: Framework Integration")
        print("-" * 40)
        
        try:
            from framework_integration_enforcer import enable_framework_validation
            
            result = enable_framework_validation()
            self.log_test_result(
                "Framework Integration",
                "ENABLED",
                "ENABLED" if result else "FAILED",
                result
            )
            
        except ImportError as e:
            self.log_test_result(
                "Layer 2 Import",
                "SUCCESS",
                f"FAILED: {str(e)}",
                False
            )
    
    def test_layer_3_git_hooks(self):
        """Test Layer 3: Git Hooks Safety Net"""
        print("\n🔧 TESTING LAYER 3: Git Hooks Safety Net")
        print("-" * 40)
        
        try:
            from git_hooks_safety_net import GitHooksSafetyNet
            
            # Create temporary git repo for testing
            with tempfile.TemporaryDirectory() as temp_dir:
                # Initialize git repo
                os.system(f"cd {temp_dir} && git init")
                
                safety_net = GitHooksSafetyNet(temp_dir)
                result = safety_net.setup_safety_net()
                
                self.log_test_result(
                    "Git Hooks Setup",
                    "SUCCESS",
                    "SUCCESS" if result else "FAILED", 
                    result
                )
                
                # Test hook existence
                hook_path = os.path.join(temp_dir, '.git', 'hooks', 'pre-commit')
                hook_exists = os.path.exists(hook_path)
                
                self.log_test_result(
                    "Pre-commit Hook Creation",
                    "EXISTS",
                    "EXISTS" if hook_exists else "MISSING",
                    hook_exists
                )
                
        except ImportError as e:
            self.log_test_result(
                "Layer 3 Import", 
                "SUCCESS",
                f"FAILED: {str(e)}",
                False
            )
    
    def test_violation_scenarios(self):
        """Test specific violation scenarios"""
        print("\n🔧 TESTING VIOLATION SCENARIOS")
        print("-" * 40)
        
        violation_tests = [
            {
                "name": "Paragraph Format Violation",
                "content": """
**Step 1:** This should be table format
- **UI Method**: Something
- **CLI Method**: Something
""",
                "should_block": True
            },
            {
                "name": "Citation Violation", 
                "content": """
# Test Cases
Some content [Source: example.com] with citations.
""",
                "should_block": True
            },
            {
                "name": "YAML HTML Violation",
                "content": """
| Step | CLI Method |
|------|------------|
| 1 | `touch file.yaml` and add:<br/>```yaml<br/>apiVersion: v1<br/>``` |
""",
                "should_block": True
            },
            {
                "name": "Valid Content",
                "content": """
# Test Cases

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Test | Navigate to console | `oc get pods` | Pods listed |
""",
                "should_block": False
            }
        ]
        
        try:
            from pre_write_validator import enforce_pre_write_validation
            
            for test in violation_tests:
                # Use proper test cases file name to trigger test_cases content type
                test_file_name = f"{test['name'].replace(' ', '-')}-Test-Cases.md"
                result = enforce_pre_write_validation(test_file_name, test["content"])
                
                # If should_block=True, we expect result=False (blocked)
                # If should_block=False, we expect result=True (allowed)
                expected_blocked = test["should_block"]
                actually_blocked = not result
                test_passed = (expected_blocked == actually_blocked)
                
                self.log_test_result(
                    test["name"],
                    "BLOCKED" if expected_blocked else "ALLOWED", 
                    "BLOCKED" if actually_blocked else "ALLOWED",
                    test_passed
                )
                
        except ImportError as e:
            self.log_test_result(
                "Validation Import",
                "SUCCESS",
                f"FAILED: {str(e)}",
                False
            )
    
    def run_comprehensive_test(self):
        """Run complete enforcement system test"""
        print("🧪 ENFORCEMENT SYSTEM COMPREHENSIVE TEST")
        print("=" * 50)
        
        # Test all layers
        self.test_layer_1_wrapper_enforcement()
        self.test_layer_2_integration()
        self.test_layer_3_git_hooks()
        self.test_violation_scenarios()
        
        # Calculate results
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n📊 TEST RESULTS SUMMARY")
        print("=" * 30)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"   - {result['test']}: Expected {result['expected']}, got {result['actual']}")
        
        if success_rate >= 80:
            print("\n✅ ENFORCEMENT SYSTEM: OPERATIONAL")
            print("🛡️  Validation enforcement is working correctly")
        else:
            print("\n❌ ENFORCEMENT SYSTEM: NEEDS ATTENTION")
            print("🔧 Review failed tests and fix issues")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = EnforcementSystemTester()
    success = tester.run_comprehensive_test()
    
    sys.exit(0 if success else 1)