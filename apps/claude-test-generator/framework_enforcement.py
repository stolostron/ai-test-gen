#!/usr/bin/env python3
"""
Framework Enforcement Integration - AUTOMATIC ACTIVATION
=======================================================

This module automatically activates enforcement when imported.
Place at start of framework execution to ensure validation.
"""

import os
import sys
from pathlib import Path

# Add enforcement directory to path
enforcement_dir = Path(__file__).parent / ".claude" / "enforcement"
sys.path.insert(0, str(enforcement_dir))

# Import and activate enforcement (this happens automatically)
from mandatory_write_enforcement import Write, finalize_write_enforcement

# Export for framework use
__all__ = ['Write', 'finalize_write_enforcement']

print("🔒 FRAMEWORK ENFORCEMENT ACTIVE: All Write operations validated")
