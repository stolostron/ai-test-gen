#!/usr/bin/env python3
"""
Framework Enforcement Activation Script
======================================

This script is automatically executed at the start of framework runs
to ensure validation enforcement is active for all Write operations.
"""

import os
import sys

# Add enforcement path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and activate enforcement
from framework_write_integration import activate_framework_write_enforcement

def main():
    """Activate framework enforcement"""
    print("🔒 ACTIVATING FRAMEWORK WRITE ENFORCEMENT...")
    activate_framework_write_enforcement()
    print("✅ ENFORCEMENT ACTIVE: All Write operations validated")

if __name__ == "__main__":
    main()
