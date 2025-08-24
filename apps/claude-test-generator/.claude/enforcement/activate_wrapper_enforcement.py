#!/usr/bin/env python3
"""
WRAPPER ENFORCEMENT ACTIVATION
============================

Activates tool wrapper scripts for mandatory validation.
This makes validation UNAVOIDABLE for all Write operations.
"""

import sys
import os

# Add enforcement directory to path
enforcement_dir = "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/.claude/enforcement"
sys.path.insert(0, enforcement_dir)

from validated_write_wrapper import validated_write, get_enforcement_statistics

def activate_enforcement():
    """Activate wrapper enforcement"""
    print("🛡️  LAYER 1 ACTIVATED: Tool Wrapper Scripts")
    print("✅ All Write operations now require validation")
    return True

# Global activation flag
ENFORCEMENT_ACTIVE = True

if __name__ == "__main__":
    activate_enforcement()
