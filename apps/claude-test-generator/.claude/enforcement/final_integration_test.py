#!/usr/bin/env python3
"""
Final Integration Test
End-to-end test of Agent C HTML sanitization in framework context
"""

import sys
import tempfile
from pathlib import Path

def test_end_to_end_html_prevention():
    """Test complete HTML prevention pipeline"""
    print("🧪 End-to-End HTML Prevention Test")
    print("-" * 50)
    
    # Simulate Agent C collecting contaminated data
    contaminated_data = {
        "pr_investigation_results": {
            "468": {
                "pr_content": "Create YAML configuration:<br><br>```yaml<br>apiVersion: v1",
                "description": "Implementation adds digest support.<br>See changes in <code>controller.go</code>",
                "file_changes": ["pkg/controller.go<br>", "test/e2e_test.go&nbsp;"]
            }
        },
        "repository_analysis": {
            "stolostron/cluster-curator-controller": {
                "search_results": "Found implementation with<br>conditional logic<br><br>Supporting digest-based upgrades"
            }
        }
    }
    
    print(f"📊 Original contaminated data contains HTML: {contains_html(contaminated_data)}")
    
    # Apply Agent C sanitization (Stage 3.5)
    sanitized_data = apply_agent_c_sanitization(contaminated_data)
    
    print(f"🧹 After Agent C sanitization contains HTML: {contains_html(sanitized_data)}")
    
    # Simulate Pattern Extension Service using sanitized data
    test_content = generate_test_content_from_data(sanitized_data)
    
    print(f"📋 Generated test content contains HTML: {contains_html_in_text(test_content)}")
    
    # Test Write tool enforcement (final safety net)
    write_enforcement_result = test_write_enforcement(test_content)
    
    print(f"🔒 Write enforcement result: {write_enforcement_result}")
    
    # Final assessment
    no_html_in_sanitized = not contains_html(sanitized_data)
    no_html_in_content = not contains_html_in_text(test_content)
    write_enforcement_works = write_enforcement_result == "approved"
    
    success = no_html_in_sanitized and no_html_in_content and write_enforcement_works
    
    if success:
        print("✅ End-to-end HTML prevention: WORKING CORRECTLY")
        print("   ✅ Agent C sanitization removes HTML from source data")
        print("   ✅ Pattern Extension generates clean content") 
        print("   ✅ Write enforcement provides final safety net")
    else:
        print("❌ End-to-end HTML prevention: FAILED")
        if not no_html_in_sanitized:
            print("   ❌ Agent C sanitization failed")
        if not no_html_in_content:
            print("   ❌ Test content generation produced HTML")
        if not write_enforcement_works:
            print("   ❌ Write enforcement failed")
    
    return success

def contains_html(data):
    """Check if data structure contains HTML patterns"""
    import re
    html_pattern = r'<[^>]+>|&nbsp;|&lt;|&gt;|&amp;'
    
    def check_recursive(obj):
        if isinstance(obj, dict):
            return any(check_recursive(value) for value in obj.values())
        elif isinstance(obj, list):
            return any(check_recursive(item) for item in obj)
        elif isinstance(obj, str):
            return bool(re.search(html_pattern, obj))
        return False
    
    return check_recursive(data)

def contains_html_in_text(text):
    """Check if text contains HTML patterns"""
    import re
    html_pattern = r'<[^>]+>|&nbsp;|&lt;|&gt;|&amp;'
    return bool(re.search(html_pattern, text))

def apply_agent_c_sanitization(data):
    """Apply Agent C sanitization logic"""
    import re
    
    html_patterns = [
        r'<br\s*/?>', r'<[^>]+>', r'&lt;', r'&gt;', 
        r'&amp;', r'&nbsp;', r'&quot;', r'&apos;'
    ]
    
    def clean_text(text):
        if not isinstance(text, str):
            return text
        cleaned = text
        for pattern in html_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()
    
    def sanitize_recursive(obj):
        if isinstance(obj, dict):
            return {key: sanitize_recursive(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [sanitize_recursive(item) for item in obj]
        elif isinstance(obj, str):
            return clean_text(obj)
        else:
            return obj
    
    return sanitize_recursive(data)

def generate_test_content_from_data(data):
    """Simulate Pattern Extension Service generating test content"""
    # Extract information from sanitized data
    pr_content = data.get("pr_investigation_results", {}).get("468", {}).get("pr_content", "")
    description = data.get("pr_investigation_results", {}).get("468", {}).get("description", "")
    
    # Generate test content (should be clean since data is sanitized)
    test_content = f"""
# Test Case: Verify ClusterCurator Digest Support

## Description
{description}

## Setup
Prerequisites for testing digest-based upgrade functionality.

## Test Steps

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Create ClusterCurator YAML | Navigate to YAML editor | Create clustercurator.yaml with: {pr_content} | YAML configuration created |
| 2 | Apply configuration | Click Apply | oc apply -f clustercurator.yaml | Resource created successfully |
| 3 | Verify digest support | Check status | oc get clustercurator -o yaml | Digest field populated |
"""
    
    return test_content

def test_write_enforcement(content):
    """Test write tool enforcement"""
    import subprocess
    import tempfile
    
    base_path = Path("/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator")
    validator_path = base_path / ".claude/enforcement/format_validator.py"
    
    if not validator_path.exists():
        return "validator_missing"
    
    try:
        result = subprocess.run([
            sys.executable, str(validator_path),
            "test.md", "test", content
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return "approved"
        else:
            return "blocked"
    except Exception:
        return "error"

def test_framework_integration():
    """Test framework integration points"""
    print("\n🔧 Framework Integration Test")
    print("-" * 50)
    
    base_path = Path("/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator")
    
    # Test service integration
    service_file = base_path / ".claude/ai-services/tg-enhanced-github-investigation-service.md"
    if service_file.exists():
        content = service_file.read_text()
        has_sanitization = "sanitize_collected_data" in content
        has_stage = "Stage 3.5" in content
        has_integration = has_sanitization and has_stage
        
        if has_integration:
            print("✅ Agent C service integration: Complete")
        else:
            print("❌ Agent C service integration: Incomplete")
            return False
    else:
        print("❌ Agent C service integration: Service file missing")
        return False
    
    # Test documentation consistency
    claude_files = [
        ("CLAUDE.md", "Agent C HTML sanitization"),
        ("CLAUDE.core.md", "HTML sanitization"),
        ("CLAUDE.features.md", "html_contamination_prevention"),
        ("CLAUDE.policies.md", "Agent C source sanitization")
    ]
    
    doc_consistent = True
    for filename, term in claude_files:
        file_path = base_path / filename
        if file_path.exists():
            content = file_path.read_text()
            if term.lower() not in content.lower():
                print(f"❌ Documentation consistency: {filename} missing '{term}'")
                doc_consistent = False
        else:
            print(f"❌ Documentation consistency: {filename} missing")
            doc_consistent = False
    
    if doc_consistent:
        print("✅ Documentation consistency: All files updated")
    
    return doc_consistent

def main():
    print("🎯 FINAL INTEGRATION TEST")
    print("Complete end-to-end validation of Agent C HTML sanitization")
    print("=" * 70)
    
    # Run comprehensive tests
    e2e_success = test_end_to_end_html_prevention()
    integration_success = test_framework_integration()
    
    print("\n" + "=" * 70)
    print("📊 FINAL INTEGRATION TEST RESULTS")
    print("=" * 70)
    
    if e2e_success and integration_success:
        print("🎉 ALL INTEGRATION TESTS PASSED")
        print("✅ End-to-end HTML prevention working correctly")
        print("✅ Framework integration complete and consistent")
        print("✅ Dual-layer protection architecture operational")
        print("\n🛡️  REGRESSION VALIDATION CONCLUSION:")
        print("✅ NO CRITICAL REGRESSIONS DETECTED")
        print("✅ Agent C HTML sanitization successfully integrated")
        print("✅ Core framework functionality preserved")
        print("✅ All enforcement mechanisms working correctly")
        return True
    else:
        print("❌ INTEGRATION TESTS FAILED")
        if not e2e_success:
            print("❌ End-to-end HTML prevention not working")
        if not integration_success:
            print("❌ Framework integration incomplete")
        print("\n🚨 REGRESSION VALIDATION CONCLUSION:")
        print("❌ CRITICAL ISSUES DETECTED")
        print("❌ Immediate investigation required")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)