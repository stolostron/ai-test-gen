#!/usr/bin/env python3
"""
AUTO-INTEGRATION SCRIPT - Automatic Validation Enforcement
=========================================================

This script automatically integrates validation enforcement into any framework.
Place this at the start of your framework execution to enable validation.
"""

import sys
import os

# Add enforcement directory to path
enforcement_dir = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, enforcement_dir)

from framework_integration_enforcer import FrameworkIntegrationEnforcer

def auto_enable_validation():
    """Automatically enable validation for current framework"""
    enforcer = FrameworkIntegrationEnforcer()
    
    # Patch current module
    current_module = sys.modules[__name__]
    enforcer.enforce_framework_validation(current_module)
    
    # Try to patch main module if different
    if '__main__' in sys.modules and sys.modules['__main__'] != current_module:
        enforcer.enforce_framework_validation(sys.modules['__main__'])
    
    print("🛡️  AUTOMATIC VALIDATION ENFORCEMENT ACTIVE")
    return enforcer

# AUTO-ENABLE on import
if __name__ != "__main__":
    auto_enable_validation()

if __name__ == "__main__":
    print("FRAMEWORK INTEGRATION ENFORCER")
    print("This script enables automatic validation enforcement")
    auto_enable_validation()
