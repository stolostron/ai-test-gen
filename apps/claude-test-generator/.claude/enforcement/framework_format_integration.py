#!/usr/bin/env python3
"""
Framework Format Integration
Integrates test case format validation into the main framework workflow
"""

import os
import json
import subprocess
from pathlib import Path
from .test_case_format_enforcer import TestCaseFormatEnforcer

class FrameworkFormatIntegration:
    def __init__(self, framework_root):
        self.framework_root = Path(framework_root)
        self.enforcer = TestCaseFormatEnforcer()
        self.enforcement_log = []
        
    def validate_generated_test_cases(self, ticket_id, run_path):
        """Validate test cases after generation"""
        test_cases_path = run_path / f"{ticket_id}-Test-Cases.md"
        
        if not test_cases_path.exists():
            error = f"❌ Test cases file not found: {test_cases_path}"
            self.enforcement_log.append(error)
            return False, error
            
        # Run validation
        result = self.enforcer.validate_test_cases(str(test_cases_path))
        
        # Log validation results
        log_entry = {
            'timestamp': self._get_timestamp(),
            'ticket_id': ticket_id,
            'file_path': str(test_cases_path),
            'score': result['score'],
            'percentage': result['percentage'],
            'passed': result['passed'],
            'violations': result['violations']
        }
        
        self.enforcement_log.append(log_entry)
        
        # Generate validation report
        report = self.enforcer.generate_enforcement_report(str(test_cases_path))
        report_path = test_cases_path.parent / f"{ticket_id}-Format-Validation-Report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        # If validation fails, provide corrective guidance
        if not result['passed']:
            self._generate_corrective_guidance(test_cases_path, result)
            
        return result['passed'], result
        
    def _generate_corrective_guidance(self, test_cases_path, validation_result):
        """Generate corrective guidance for failed validation"""
        guidance_path = test_cases_path.parent / "FORMAT_CORRECTION_GUIDANCE.md"
        
        guidance = f"""# FORMAT CORRECTION GUIDANCE

**File:** {test_cases_path.name}
**Current Score:** {validation_result['score']}/{validation_result['max_score']} ({validation_result['percentage']}%)
**Required:** 85+ points

## Critical Issues to Fix:

"""
        
        for violation in validation_result['violations']:
            guidance += f"- {violation}\n"
            
        guidance += """
## Step-by-Step Correction Process:

### 1. Fix Login Step Format
**REQUIRED FORMAT:**
```markdown
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Login successful: `Login successful. You have access to 67 projects.` |
```

### 2. Fix Table Formatting
- Keep all table cells single-line
- No multi-line code blocks in table cells
- Use backticks for inline outputs: `namespace/test-ns created`

### 3. Remove HTML Tags
- Replace `<br/>` with ` - `
- Replace `<b>text</b>` with `**text**`
- Replace `<i>text</i>` with `*text*`

### 4. Add Sample Outputs
Each expected result should include realistic output in backticks:
```markdown
| **Step 2: Create namespace** - Run: `oc create namespace test-ns` | Namespace created: `namespace/test-ns created` |
```

### 5. Remove Internal Scripts
- Never mention `setup_clc`, `login_oc`, or `bin/setup_clc`
- Use generic `oc login <CLUSTER_URL>` format

## Template Example:
```markdown
## Test Case 1: Feature Validation

**Description:** Validate the feature functionality with comprehensive testing.

**Setup:**
- Access to ACM hub cluster
- Required permissions
- Test environment ready

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Login successful: `Login successful. You have access to 67 projects.` |
| **Step 2: Create test namespace** - Run: `oc create namespace test-feature` | Namespace created: `namespace/test-feature created` |
| **Step 3: Apply test resource** - Run: `oc apply -f test-resource.yaml` | Resource created: `clustercurator.cluster.open-cluster-management.io/test-curator created` |
```

## Validation Command:
```bash
python .claude/enforcement/test_case_format_enforcer.py {test_cases_path.name}
```

**Target:** 85+ points for framework acceptance
"""
        
        with open(guidance_path, 'w', encoding='utf-8') as f:
            f.write(guidance)
            
        print(f"📋 Corrective guidance generated: {guidance_path}")
        
    def enforce_format_in_workflow(self, ticket_id, run_path):
        """Enforce format validation as part of the main workflow"""
        print(f"🔍 Enforcing test case format validation for {ticket_id}")
        
        passed, result = self.validate_generated_test_cases(ticket_id, run_path)
        
        if passed:
            print(f"✅ Format validation PASSED: {result['percentage']}% (Target: 85%)")
            return True
        else:
            print(f"❌ Format validation FAILED: {result['percentage']}% (Target: 85%)")
            print("📋 Corrective guidance generated - please review and fix formatting issues")
            
            # In strict mode, could block delivery here
            # For now, just log and continue with warning
            return False
            
    def generate_format_enforcement_summary(self):
        """Generate summary of all format enforcement activities"""
        summary_path = self.framework_root / ".claude" / "enforcement" / "format_enforcement_summary.json"
        
        summary = {
            'total_validations': len(self.enforcement_log),
            'passed_validations': len([log for log in self.enforcement_log if isinstance(log, dict) and log.get('passed', False)]),
            'failed_validations': len([log for log in self.enforcement_log if isinstance(log, dict) and not log.get('passed', True)]),
            'enforcement_log': self.enforcement_log,
            'last_updated': self._get_timestamp()
        }
        
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
            
        return summary
        
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

class FrameworkFormatHook:
    """Hook for integrating format validation into framework execution"""
    
    @staticmethod
    def post_test_generation_hook(ticket_id, run_path):
        """Hook called after test case generation"""
        framework_root = Path(__file__).parent.parent.parent
        integration = FrameworkFormatIntegration(framework_root)
        
        # Enforce format validation
        passed = integration.enforce_format_in_workflow(ticket_id, Path(run_path))
        
        # Generate summary
        summary = integration.generate_format_enforcement_summary()
        
        return {
            'format_validation_passed': passed,
            'enforcement_summary': summary
        }
        
    @staticmethod
    def validate_before_delivery(ticket_id, run_path):
        """Final validation before delivery to user"""
        framework_root = Path(__file__).parent.parent.parent
        integration = FrameworkFormatIntegration(framework_root)
        
        passed, result = integration.validate_generated_test_cases(ticket_id, Path(run_path))
        
        if not passed:
            # Could implement blocking logic here
            print(f"⚠️  WARNING: Test cases for {ticket_id} do not meet format requirements")
            print(f"Score: {result['percentage']}% (Required: 85%)")
            
        return passed

def main():
    """Test the format integration"""
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python framework_format_integration.py <ticket_id> <run_path>")
        sys.exit(1)
        
    ticket_id = sys.argv[1]
    run_path = Path(sys.argv[2])
    
    framework_root = Path(__file__).parent.parent.parent
    integration = FrameworkFormatIntegration(framework_root)
    
    passed = integration.enforce_format_in_workflow(ticket_id, run_path)
    summary = integration.generate_format_enforcement_summary()
    
    print(f"\nFormat validation {'PASSED' if passed else 'FAILED'}")
    print(f"Total validations: {summary['total_validations']}")
    print(f"Passed: {summary['passed_validations']}")
    print(f"Failed: {summary['failed_validations']}")

if __name__ == "__main__":
    main()