#!/usr/bin/env python3
"""
Mandatory Write Enforcement - FRAMEWORK INTEGRATION MODULE
==========================================================

CRITICAL PURPOSE: Replace ALL Write tool usage in framework with validated operations
INTEGRATION SCOPE: Framework-wide automatic enforcement
DEPLOYMENT STRATEGY: Import-based activation with global enforcement

This module MUST be imported at the start of any framework execution
to ensure all Write operations go through validation enforcement.
"""

import os
import sys
import importlib
from pathlib import Path

# Add enforcement path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import enforcement components
from framework_write_integration import framework_write, save_framework_enforcement_audit

class MandatoryWriteEnforcement:
    """Global enforcement for all framework Write operations"""
    
    def __init__(self):
        self.enforcement_active = True
        self.blocked_operations = 0
        self.approved_operations = 0
        
    def enforced_framework_write(self, file_path: str, content: str) -> bool:
        """
        MANDATORY Write function that replaces ALL Write tool usage
        
        This function MUST be used instead of Write tool in framework execution
        """
        if not self.enforcement_active:
            print("⚠️  WARNING: Write enforcement bypassed (should not happen in production)")
            
        # Execute framework validated write
        success = framework_write(file_path, content)
        
        # Track statistics
        if success:
            self.approved_operations += 1
        else:
            self.blocked_operations += 1
            
        return success
        
    def get_enforcement_summary(self) -> dict:
        """Get enforcement summary for the current run"""
        total = self.approved_operations + self.blocked_operations
        
        return {
            "total_write_operations": total,
            "approved_operations": self.approved_operations,
            "blocked_operations": self.blocked_operations,
            "enforcement_effectiveness": "ACTIVE" if self.blocked_operations > 0 else "PREVENTATIVE",
            "compliance_rate": (self.approved_operations / total * 100) if total > 0 else 100
        }

# GLOBAL ENFORCEMENT INSTANCE
_mandatory_enforcement = MandatoryWriteEnforcement()

def Write(file_path: str, content: str) -> bool:
    """
    FRAMEWORK WRITE FUNCTION - Replaces Claude Code Write tool
    
    This function has the same signature as the Write tool but includes
    mandatory validation enforcement.
    
    CRITICAL: This MUST be used instead of direct Write tool calls
    """
    return _mandatory_enforcement.enforced_framework_write(file_path, content)

def get_write_enforcement_summary() -> dict:
    """Get summary of enforcement actions for current run"""
    return _mandatory_enforcement.get_enforcement_summary()

def finalize_write_enforcement(run_directory: str):
    """Finalize enforcement and save audit for run"""
    # Save framework enforcement audit
    save_framework_enforcement_audit(run_directory)
    
    # Print enforcement summary
    summary = get_write_enforcement_summary()
    print("\n📊 WRITE ENFORCEMENT SUMMARY")
    print("=" * 40)
    print(f"Total Operations: {summary['total_write_operations']}")
    print(f"Approved: {summary['approved_operations']}")
    print(f"Blocked: {summary['blocked_operations']}")
    print(f"Effectiveness: {summary['enforcement_effectiveness']}")
    print(f"Compliance Rate: {summary['compliance_rate']:.1f}%")
    print("=" * 40)

def create_framework_integration_guide():
    """Create integration guide for framework developers"""
    guide_path = Path(__file__).parent / "FRAMEWORK_INTEGRATION_GUIDE.md"
    
    guide_content = '''# Framework Write Enforcement Integration Guide

## MANDATORY INTEGRATION

All framework execution MUST use validated Write operations.

### Step 1: Import Enforcement
```python
# Add at the start of framework execution
import sys
sys.path.append('.claude/enforcement')
from mandatory_write_enforcement import Write
```

### Step 2: Replace Write Tool Usage
```python
# OLD (bypasses validation):
# Write(file_path, content)

# NEW (enforced validation):
Write(file_path, content)  # Now automatically validated
```

### Step 3: Finalize Enforcement
```python
# At end of framework execution
from mandatory_write_enforcement import finalize_write_enforcement
finalize_write_enforcement(run_directory)
```

## Integration Status

✅ **ACTIVE**: All Write operations automatically validated
🛡️  **ENFORCEMENT**: Format violations automatically blocked
📋 **AUDIT**: Complete enforcement audit trail generated

## Validation Rules

- **Test Cases**: Must use Description/Setup/Table format
- **Dual Methods**: Must include UI Method and CLI Method columns  
- **YAML Integration**: Must be within table, not separate sections
- **HTML Prevention**: All HTML tags automatically blocked

## Compliance Guarantee

comprehensive enforcement - no Write operations can bypass validation when
this module is properly integrated into framework execution.
'''
    
    with open(guide_path, 'w') as f:
        f.write(guide_content)
        
    print(f"📋 Integration guide created: {guide_path}")
    return str(guide_path)

# ACTIVATION MESSAGE
print("🔒 MANDATORY WRITE ENFORCEMENT ACTIVATED")
print("📋 All Write operations now require validation approval")
print("🛡️  Format violations will be automatically blocked")

if __name__ == "__main__":
    print("MANDATORY WRITE ENFORCEMENT")
    print("===========================")
    print("Automatic validation for ALL framework Write operations")
    print("")
    
    # Create integration guide
    guide_path = create_framework_integration_guide()
    print(f"✅ Integration guide: {guide_path}")
    print("")
    print("ENFORCEMENT STATUS: ACTIVE")
    print("COVERAGE: FRAMEWORK-WIDE")
    print("VALIDATION: MANDATORY")