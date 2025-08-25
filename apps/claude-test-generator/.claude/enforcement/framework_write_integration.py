#!/usr/bin/env python3
"""
Framework Write Integration - AUTOMATIC ENFORCEMENT DEPLOYMENT
==============================================================

CRITICAL PURPOSE: Seamlessly integrate validation enforcement into framework execution
DEPLOYMENT LEVEL: Framework-wide automatic activation
INTEGRATION TYPE: Transparent replacement of Write tool usage

This ensures ALL framework executions automatically use validated Write operations.
"""

import os
import sys
import importlib
import json
from pathlib import Path
from datetime import datetime

# Import enforcement components
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from write_tool_interceptor import enforced_write, save_write_enforcement_audit, activate_write_enforcement

class FrameworkWriteIntegration:
    """Integrates validation enforcement into framework execution"""
    
    def __init__(self):
        self.integration_active = False
        self.framework_operations = []
        self.integration_log = []
        
    def activate_framework_enforcement(self):
        """Activate enforcement for all framework operations"""
        self.integration_active = True
        
        # Activate the write tool interceptor
        activate_write_enforcement()
        
        print("🚀 FRAMEWORK WRITE ENFORCEMENT ACTIVATED")
        print("📋 All test generation will use validated Write operations")
        print("🛡️  Format violations will be automatically blocked")
        
        self.log_integration_event("FRAMEWORK_ENFORCEMENT_ACTIVATED", {
            "enforcement_level": "AUTOMATIC",
            "coverage": "ALL_WRITE_OPERATIONS",
            "validation_required": True
        })
        
    def log_integration_event(self, event_type: str, details: dict):
        """Log framework integration events"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
            "integration_status": "ACTIVE" if self.integration_active else "INACTIVE"
        }
        self.integration_log.append(entry)
        
    def framework_validated_write(self, file_path: str, content: str) -> bool:
        """
        Framework-specific validated write with enhanced logging
        
        This replaces all Write tool calls in the framework
        """
        if not self.integration_active:
            print("⚠️  WARNING: Framework enforcement not active")
            
        # Log framework operation
        self.framework_operations.append({
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "content_size": len(content),
            "phase": self._detect_execution_phase(file_path)
        })
        
        # Execute enforced write
        success = enforced_write(file_path, content)
        
        if success:
            print(f"✅ FRAMEWORK WRITE COMPLETED: {os.path.basename(file_path)}")
        else:
            print(f"🚫 FRAMEWORK WRITE BLOCKED: {os.path.basename(file_path)}")
            print("🔧 Fix format violations to proceed")
            
        return success
        
    def _detect_execution_phase(self, file_path: str) -> str:
        """Detect which framework phase is executing based on file path"""
        filename = os.path.basename(file_path)
        
        if "Test-Cases" in filename:
            return "PHASE_5_TEST_GENERATION"
        elif "Complete-Analysis" in filename:
            return "PHASE_5_ANALYSIS_GENERATION"
        elif "run-metadata" in filename:
            return "PHASE_5_METADATA_GENERATION"
        else:
            return "UNKNOWN_PHASE"
            
    def save_framework_integration_audit(self, run_directory: str):
        """Save complete framework integration audit"""
        audit_path = os.path.join(run_directory, "framework-enforcement-audit.json")
        
        audit_data = {
            "integration": "FrameworkWriteIntegration",
            "version": "1.0-AUTOMATIC",
            "enforcement_coverage": "FRAMEWORK_WIDE",
            "integration_active": self.integration_active,
            "framework_operations": self.framework_operations,
            "integration_events": self.integration_log,
            "enforcement_guarantee": "ALL_WRITES_VALIDATED"
        }
        
        os.makedirs(os.path.dirname(audit_path), exist_ok=True)
        with open(audit_path, 'w') as f:
            json.dump(audit_data, f, indent=2)
            
        print(f"📋 Framework integration audit: {audit_path}")
        
        # Also save the write enforcement audit
        save_write_enforcement_audit(run_directory)

# GLOBAL FRAMEWORK INTEGRATION
_framework_integration = FrameworkWriteIntegration()

def activate_framework_write_enforcement():
    """Activate framework-wide write enforcement"""
    _framework_integration.activate_framework_enforcement()

def framework_write(file_path: str, content: str) -> bool:
    """
    MAIN FRAMEWORK WRITE FUNCTION
    
    This function MUST replace all Write tool usage in framework execution
    """
    return _framework_integration.framework_validated_write(file_path, content)

def save_framework_enforcement_audit(run_directory: str):
    """Save complete enforcement audit for framework run"""
    _framework_integration.save_framework_integration_audit(run_directory)

def create_enforcement_activation_script():
    """Create script to automatically activate enforcement in framework runs"""
    script_path = Path(__file__).parent / "activate_framework_enforcement.py"
    
    script_content = '''#!/usr/bin/env python3
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
'''
    
    with open(script_path, 'w') as f:
        f.write(script_content)
        
    # Make executable
    os.chmod(script_path, 0o755)
    
    print(f"📋 Created activation script: {script_path}")
    return str(script_path)

# AUTOMATIC ACTIVATION
activate_framework_write_enforcement()

if __name__ == "__main__":
    print("FRAMEWORK WRITE INTEGRATION")
    print("===========================")
    print("Automatic validation enforcement for all framework Write operations")
    print("")
    
    # Create activation script
    script_path = create_enforcement_activation_script()
    print(f"✅ Created activation script: {script_path}")
    print("")
    print("Integration Status: ACTIVE")
    print("Enforcement Level: FRAMEWORK_WIDE")
    print("Validation Required: MANDATORY")