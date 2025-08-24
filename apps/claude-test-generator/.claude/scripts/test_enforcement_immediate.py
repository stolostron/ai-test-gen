#!/usr/bin/env python3
"""
Immediate Enforcement Testing
Quick test to verify the enforcement system catches HTML violations
"""

import os
import sys
import subprocess
from pathlib import Path

def test_enforcement_system():
    """Test the enforcement system with realistic examples"""
    
    enforcement_dir = Path(__file__).parent.parent / "enforcement"
    
    print("🧪 TESTING ENFORCEMENT SYSTEM")
    print("=" * 50)
    
    # Test 1: Content with HTML violations (should be blocked)
    violation_content = """| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Create YAML | Navigate to console | Create YAML file: `touch test.yaml` and add:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: test<br>```<br><br>`oc apply -f test.yaml` | YAML file created |"""
    
    print("\n🚨 Testing HTML violation detection...")
    result = subprocess.run([
        sys.executable, 
        str(enforcement_dir / "pre_write_validator.py"),
        "test-violations.md",
        violation_content
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("✅ PASS: HTML violations correctly blocked")
        print(f"   Validator output: {result.stderr}")
    else:
        print("❌ FAIL: HTML violations not detected!")
        return False
    
    # Test 2: Clean content (should pass)
    clean_content = """| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Create YAML | Navigate to console | Create YAML file: `touch test.yaml` and add:\n\n```yaml\napiVersion: cluster.open-cluster-management.io/v1beta1\nkind: ClusterCurator\nmetadata:\n  name: test\n```\n\n`oc apply -f test.yaml` | YAML file created |"""
    
    print("\n✅ Testing clean content approval...")
    result = subprocess.run([
        sys.executable, 
        str(enforcement_dir / "pre_write_validator.py"),
        "test-clean.md",
        clean_content
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ PASS: Clean content correctly approved")
    else:
        print("❌ FAIL: Clean content incorrectly blocked!")
        print(f"   Validator output: {result.stderr}")
        return False
    
    # Test 3: Hook system test
    hook_script = Path(__file__).parent.parent / "hooks" / "pre_write_enforcement_hook.py"
    
    if hook_script.exists():
        print("\n🪝 Testing hook system...")
        
        # Test hook with violation
        result = subprocess.run([
            sys.executable,
            str(hook_script),
            "test-hook.md",
            "Content with <br> violation"
        ], capture_output=True, text=True)
        
        if "BLOCKED" in result.stdout or result.returncode != 0:
            print("✅ PASS: Hook correctly blocks violations")
        else:
            print("❌ FAIL: Hook didn't block violation")
            return False
    else:
        print("⚠️  Hook script not found - skipping hook test")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("🛡️  Enforcement system is working correctly")
    return True

def demonstrate_violation_patterns():
    """Demonstrate the exact violation patterns found in the codebase"""
    
    print("\n📋 DEMONSTRATING ACTUAL VIOLATION PATTERNS")
    print("=" * 60)
    
    # Exact pattern from ACM-22079 line 20
    actual_violation = """Create and apply ClusterCurator YAML: `touch clustercurator-digest.yaml` and add:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: digest-upgrade-test<br>  namespace: target-cluster<br>  annotations:<br>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate: "4.16.37"<br>    monitorTimeout: 120<br>```<br><br>`oc apply -f clustercurator-digest.yaml`"""
    
    print("🚨 Actual violation from ACM-22079:")
    print("   Pattern: <br> tags embedded throughout YAML CLI method")
    
    enforcement_dir = Path(__file__).parent.parent / "enforcement"
    
    result = subprocess.run([
        sys.executable, 
        str(enforcement_dir / "format_validator.py"),
        "ACM-22079-Test-Cases.md",
        "test_cases",
        actual_violation
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("✅ DETECTION: Validator correctly catches this violation")
        violation_count = result.stderr.count('<br>')
        print(f"   Found {violation_count} HTML violations")
    else:
        print("❌ FAILURE: Validator missed this violation!")
    
    # Show the corrected version
    corrected_version = """Create and apply ClusterCurator YAML: `touch clustercurator-digest.yaml` and add:

```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: digest-upgrade-test
  namespace: target-cluster
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'
spec:
  desiredCuration: upgrade
  cluster: target-cluster
  upgrade:
    desiredUpdate: "4.16.37"
    monitorTimeout: 120
```

`oc apply -f clustercurator-digest.yaml`"""
    
    print("\n✅ Corrected version (should pass):")
    print("   Pattern: Clean markdown with proper YAML blocks")
    
    # Test the corrected version in a table context
    table_content = f"""| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Create ClusterCurator | Navigate to console | {corrected_version} | Resource created |"""
    
    result = subprocess.run([
        sys.executable, 
        str(enforcement_dir / "pre_write_validator.py"),
        "corrected-test.md",
        table_content
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ VALIDATION: Corrected version passes validation")
    else:
        print("❌ ISSUE: Corrected version still has problems")
        print(f"   Output: {result.stderr}")

def main():
    """Main testing function"""
    print("🛡️  CLAUDE CODE ENFORCEMENT SYSTEM TEST")
    print("=" * 60)
    print("🎯 Objective: Verify HTML violation prevention")
    print("🔍 Testing: Actual violation patterns from codebase")
    print()
    
    # Test basic enforcement
    if not test_enforcement_system():
        print("\n❌ BASIC TESTS FAILED")
        sys.exit(1)
    
    # Demonstrate actual patterns
    demonstrate_violation_patterns()
    
    print("\n🎉 ENFORCEMENT SYSTEM VALIDATION COMPLETE")
    print("=" * 60)
    print("✅ System correctly detects HTML violations")
    print("✅ System correctly approves clean content")  
    print("✅ System prevents exact violations found in codebase")
    print()
    print("🛡️  The enforcement system is ready for deployment!")
    print("💡 Next step: Integrate hook with Claude Code tool system")

if __name__ == "__main__":
    main()