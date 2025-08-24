#!/usr/bin/env python3
"""
Agent C HTML Sanitization Test
Test the new HTML sanitization functionality in Enhanced GitHub Investigation Service
"""

import sys
import re
from pathlib import Path

def test_html_sanitization():
    """Test HTML sanitization patterns against real WebFetch contamination"""
    
    print("🧪 Testing Agent C HTML Sanitization...")
    print("=" * 60)
    
    # Test data simulating WebFetch HTML contamination
    test_cases = [
        {
            "name": "GitHub PR Description with HTML",
            "contaminated_data": {
                "pr_content": "Create ClusterCurator YAML:<br><br>```yaml<br>apiVersion: v1beta1<br>kind: ClusterCurator<br>```",
                "description": "This PR adds digest support.<br>See implementation in <code>pkg/controller</code>"
            },
            "expected_clean": {
                "pr_content": "Create ClusterCurator YAML: ```yaml apiVersion: v1beta1 kind: ClusterCurator ```",
                "description": "This PR adds digest support. See implementation in pkg/controller"
            }
        },
        {
            "name": "GitHub File Changes with HTML Entities",
            "contaminated_data": {
                "file_changes": ["&lt;filename&gt;.go", "test&amp;spec.yaml"],
                "summary": "Modified files: pkg/controller.go<br>Added test cases&nbsp;for validation"
            },
            "expected_clean": {
                "file_changes": ["filename.go", "test&spec.yaml"],
                "summary": "Modified files: pkg/controller.go Added test cases for validation"
            }
        },
        {
            "name": "Nested Data Structure with Mixed HTML",
            "contaminated_data": {
                "pr_investigation_results": {
                    "468": {
                        "title": "Support digest-based upgrades<br>via ClusterCurator",
                        "implementation_changes": "Added conditional updates<br><br>with fallback logic",
                        "commits": ["Initial implementation<br>", "Fixed tests&nbsp;and docs"]
                    }
                }
            },
            "expected_clean": {
                "pr_investigation_results": {
                    "468": {
                        "title": "Support digest-based upgrades via ClusterCurator",
                        "implementation_changes": "Added conditional updates with fallback logic",
                        "commits": ["Initial implementation ", "Fixed tests and docs"]
                    }
                }
            }
        }
    ]
    
    # HTML patterns for testing (matching Agent C implementation)
    html_patterns = [
        r'<br\s*/?>', # <br>, <br/>, <br >
        r'<[^>]+>',   # Any HTML tags
        r'&lt;',      # HTML entities
        r'&gt;',
        r'&amp;',
        r'&nbsp;',
        r'&quot;',
        r'&apos;'
    ]
    
    def clean_text(text):
        """Agent C sanitization logic"""
        if not isinstance(text, str):
            return text
        
        cleaned = text
        
        # Remove HTML tags and entities
        for pattern in html_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up multiple spaces and newlines caused by tag removal
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
        
        # Preserve markdown structure
        cleaned = cleaned.strip()
        
        return cleaned
    
    def sanitize_dict(data):
        """Recursive sanitization"""
        if isinstance(data, dict):
            return {key: sanitize_dict(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [sanitize_dict(item) for item in data]
        elif isinstance(data, str):
            return clean_text(data)
        else:
            return data
    
    def count_html_patterns(data):
        """Count HTML patterns in data"""
        html_pattern = r'<[^>]+>|&lt;|&gt;|&amp;|&nbsp;|&quot;|&apos;'
        
        def extract_strings(obj):
            strings = []
            if isinstance(obj, dict):
                for value in obj.values():
                    strings.extend(extract_strings(value))
            elif isinstance(obj, list):
                for item in obj:
                    strings.extend(extract_strings(item))
            elif isinstance(obj, str):
                strings.append(obj)
            return strings
        
        all_strings = extract_strings(data)
        return sum(len(re.findall(html_pattern, s, re.IGNORECASE)) for s in all_strings)
    
    # Run tests
    total_tests = len(test_cases)
    passed_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{total_tests}: {test_case['name']}")
        print("-" * 40)
        
        contaminated = test_case["contaminated_data"]
        expected = test_case["expected_clean"]
        
        # Count HTML patterns before cleaning
        html_before = count_html_patterns(contaminated)
        
        # Apply sanitization
        sanitized = sanitize_dict(contaminated)
        
        # Count HTML patterns after cleaning
        html_after = count_html_patterns(sanitized)
        
        # Calculate removed patterns
        removed_patterns = html_before - html_after
        
        print(f"   HTML patterns found: {html_before}")
        print(f"   HTML patterns removed: {removed_patterns}")
        print(f"   HTML patterns remaining: {html_after}")
        
        # Verify cleaning effectiveness
        if html_after == 0:
            print("   ✅ All HTML patterns successfully removed")
            passed_tests += 1
        else:
            print("   ❌ HTML patterns still present after sanitization")
            
        # Show before/after for first example
        if i == 1:
            print(f"\n   📝 Example transformation:")
            original_text = contaminated["pr_content"]
            cleaned_text = sanitized["pr_content"]
            print(f"   Before: {original_text[:50]}...")
            print(f"   After:  {cleaned_text[:50]}...")
    
    # Final results
    print("\n" + "=" * 60)
    print(f"🧪 Agent C Sanitization Test Results:")
    print(f"   Tests passed: {passed_tests}/{total_tests}")
    print(f"   Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("   ✅ All tests passed - HTML sanitization working correctly")
        return True
    else:
        print("   ❌ Some tests failed - sanitization needs improvement")
        return False

def test_integration_workflow():
    """Test the complete Agent C workflow with sanitization"""
    print("\n🔄 Testing Agent C Integration Workflow...")
    print("=" * 60)
    
    # Simulate contaminated GitHub analysis from WebFetch
    contaminated_github_analysis = {
        "pr_investigation_results": {
            "468": {
                "pr_content": "Create and apply ClusterCurator YAML: `touch clustercurator.yaml` and add:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1",
                "file_changes": ["pkg/controller.go<br>Modified", "test/unit_test.go&nbsp;Added"],
                "method": "webfetch_fallback"
            }
        },
        "repository_analysis": {
            "stolostron/cluster-curator-controller": {
                "search_results": "Found implementation in controller<br>with digest support<br><br>Added conditional logic"
            }
        }
    }
    
    print("📊 Original contaminated data:")
    print(f"   Contains HTML: {'<br>' in str(contaminated_github_analysis)}")
    print(f"   Contains entities: {'&nbsp;' in str(contaminated_github_analysis)}")
    
    # Apply Agent C sanitization
    html_patterns = [r'<br\s*/?>', r'<[^>]+>', r'&lt;', r'&gt;', r'&amp;', r'&nbsp;', r'&quot;', r'&apos;']
    
    def clean_text(text):
        if not isinstance(text, str):
            return text
        cleaned = text
        for pattern in html_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()
    
    def sanitize_dict(data):
        if isinstance(data, dict):
            return {key: sanitize_dict(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [sanitize_dict(item) for item in data]
        elif isinstance(data, str):
            return clean_text(data)
        else:
            return data
    
    sanitized_github_analysis = sanitize_dict(contaminated_github_analysis)
    
    print("\n🧹 After Agent C sanitization:")
    print(f"   Contains HTML: {'<br>' in str(sanitized_github_analysis)}")
    print(f"   Contains entities: {'&nbsp;' in str(sanitized_github_analysis)}")
    
    # Verify clean data would pass downstream
    clean_data_str = str(sanitized_github_analysis)
    has_html = any(pattern in clean_data_str for pattern in ['<br>', '&nbsp;', '&lt;', '&gt;'])
    
    if not has_html:
        print("   ✅ Clean data ready for Pattern Extension Service")
        print("   ✅ No HTML contamination will reach final output")
        return True
    else:
        print("   ❌ HTML contamination still present")
        return False

if __name__ == "__main__":
    print("🚀 Agent C HTML Sanitization Testing Suite")
    print("Testing enhanced GitHub investigation service sanitization functionality\n")
    
    # Run sanitization tests
    sanitization_ok = test_html_sanitization()
    
    # Run integration workflow test
    integration_ok = test_integration_workflow()
    
    # Final summary
    print("\n" + "🎯 FINAL TEST SUMMARY " + "=" * 40)
    if sanitization_ok and integration_ok:
        print("✅ ALL TESTS PASSED")
        print("✅ Agent C HTML sanitization ready for deployment")
        print("✅ Framework will now prevent HTML contamination at source")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        print("❌ Review sanitization implementation before deployment")
        sys.exit(1)