#!/usr/bin/env python3
"""
Technical Enforcement Testing Script
Verifies that the HTML tag prevention and format enforcement works correctly.
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from format_validator import FormatEnforcementValidator
from pre_write_validator import PreWriteValidationService

def test_html_tag_prevention():
    """Test that HTML tags are properly detected and blocked"""
    print("🧪 Testing HTML Tag Prevention...")
    
    validator = FormatEnforcementValidator()
    
    # Test 1: HTML tags in YAML (the original violation)
    content_with_violation = """Create ClusterCurator YAML: `touch clustercurator-digest.yaml` and add:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>"""
    
    result = validator.validate_html_tags(content_with_violation, "test_cases")
    
    if result["status"] == "CRITICAL_BLOCK":
        print("✅ HTML tag detection working correctly")
        print(f"   Violations detected: {result['violations']}")
    else:
        print("❌ HTML tag detection FAILED - violations not caught")
        return False
    
    # Test 2: Clean content (should pass)
    clean_content = """Create ClusterCurator YAML file and apply configuration:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: digest-upgrade-test
```"""
    
    result = validator.validate_html_tags(clean_content, "test_cases")
    
    if result["status"] == "APPROVED":
        print("✅ Clean content validation working correctly")
    else:
        print("❌ Clean content validation FAILED - false positive")
        return False
    
    return True

def test_yaml_block_validation():
    """Test YAML block HTML prevention"""
    print("🧪 Testing YAML Block HTML Prevention...")
    
    validator = FormatEnforcementValidator()
    
    # Test the specific pattern that caused the original violation
    violation_content = "yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind:"
    
    result = validator.validate_yaml_blocks(violation_content)
    
    if result["status"] == "CRITICAL_BLOCK":
        print("✅ YAML block HTML detection working correctly")
        print(f"   Violations detected: {result['violations']}")
    else:
        print("❌ YAML block HTML detection FAILED")
        return False
    
    return True

def test_pre_write_validation():
    """Test the pre-write validation service"""
    print("🧪 Testing Pre-Write Validation Service...")
    
    service = PreWriteValidationService()
    
    # Test content that should be blocked
    blocked_content = """| **Step 3: Create ClusterCurator** | Configure ClusterCurator | Create YAML: `touch file.yaml` and add:<br/>```yaml<br/>apiVersion: v1<br/>kind: ClusterCurator<br/>```"""
    
    result = service.validate_before_write("runs/test/ACM-Test-Cases.md", blocked_content)
    
    if not result:
        print("✅ Pre-write validation blocking working correctly")
    else:
        print("❌ Pre-write validation FAILED - violations not blocked")
        return False
    
    # Test content that should pass
    approved_content = """| **Step 3: Create ClusterCurator** | Configure ClusterCurator | Create YAML file and apply:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: test-curator
```"""
    
    result = service.validate_before_write("runs/test/ACM-Test-Cases.md", approved_content)
    
    if result:
        print("✅ Pre-write validation approval working correctly")
    else:
        print("❌ Pre-write validation FAILED - clean content blocked")
        return False
    
    return True

def main():
    """Run all enforcement tests"""
    print("🚀 Testing Technical Enforcement Mechanisms\n")
    
    tests = [
        test_html_tag_prevention,
        test_yaml_block_validation, 
        test_pre_write_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_func.__name__} FAILED\n")
        except Exception as e:
            print(f"❌ {test_func.__name__} ERROR: {e}\n")
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All enforcement mechanisms working correctly!")
        print("🔒 Technical enforcement successfully implemented")
        return True
    else:
        print("❌ Some enforcement mechanisms failed")
        print("🚨 Technical enforcement needs fixes")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)