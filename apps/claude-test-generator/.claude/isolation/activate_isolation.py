#!/usr/bin/env python3
"""
App Isolation Activation Script for claude-test-generator
Auto-generated isolation enforcement activation
"""

import sys
from pathlib import Path

# Add isolation directory to path
isolation_dir = Path(__file__).parent
sys.path.insert(0, str(isolation_dir))

# Import and activate isolation
try:
    from app_isolation_enforcer import StrictAppIsolationEngine, AppPermissionWrapper
    
    # Initialize isolation for this app
    app_root = "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator"
    isolation_engine = StrictAppIsolationEngine(app_root)
    permission_wrapper = AppPermissionWrapper("claude-test-generator", app_root)
    
    print(f"✅ Strict isolation activated for app: claude-test-generator")
    print(f"🔒 App root: {app_root}")
    print(f"🛡️ External access blocked, internal access preserved")
    
except Exception as e:
    print(f"❌ Failed to activate isolation for claude-test-generator: {e}")
    sys.exit(1)
