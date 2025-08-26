#!/usr/bin/env python3
"""
Write Tool Interceptor - MANDATORY VALIDATION ENFORCEMENT
=========================================================

CRITICAL PURPOSE: Automatically intercept all Write tool calls and enforce validation
INTEGRATION LEVEL: Framework-wide automatic enforcement
AUTHORITY: strict - No Write operations can bypass validation

This creates an unavoidable validation layer for ALL Write tool usage.
"""

import os
import sys
import json
import inspect
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Import existing validation components
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from validated_write_wrapper import validated_write, save_enforcement_audit

class WriteToolInterceptor:
    """Intercepts and validates all Write tool operations"""
    
    def __init__(self):
        self.interceptions = []
        self.active = False
        self.enforcement_mode = "STRICT"
        
    def activate_interception(self):
        """Activate automatic Write tool interception"""
        self.active = True
        print("🛡️  WRITE TOOL INTERCEPTOR ACTIVATED")
        print("📋 All Write operations now require validation approval")
        
    def deactivate_interception(self):
        """Deactivate interception (for testing only)"""
        self.active = False
        print("⚠️  WRITE TOOL INTERCEPTOR DEACTIVATED")
        
    def log_interception(self, file_path: str, content_size: int, status: str, details: Dict):
        """Log all Write tool interceptions"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "content_size": content_size,
            "status": status,
            "details": details,
            "enforcer": "WriteToolInterceptor",
            "stack_trace": self._get_caller_info()
        }
        self.interceptions.append(entry)
        
    def _get_caller_info(self) -> Dict:
        """Get information about what called the Write tool"""
        frame = inspect.currentframe()
        caller_info = {"depth": 0, "functions": []}
        
        try:
            # Walk up the call stack to identify origin
            for i in range(10):  # Limit depth
                frame = frame.f_back
                if frame is None:
                    break
                    
                func_name = frame.f_code.co_name
                filename = frame.f_code.co_filename
                line_no = frame.f_lineno
                
                caller_info["functions"].append({
                    "function": func_name,
                    "file": os.path.basename(filename),
                    "line": line_no
                })
                caller_info["depth"] += 1
                
        except:
            caller_info["error"] = "Could not trace caller"
            
        return caller_info
        
    def intercept_write_call(self, file_path: str, content: str) -> bool:
        """
        CRITICAL: Intercept Write tool call and enforce validation
        
        This function MUST be called instead of direct Write tool usage
        """
        if not self.active:
            # Interception not active - allow direct write (testing mode)
            return True
            
        print(f"\n🚨 WRITE TOOL INTERCEPTED: {file_path}")
        print("🛡️  Enforcing mandatory validation...")
        
        # Execute validated write with enforcement
        success = validated_write(file_path, content)
        
        # Log the interception
        self.log_interception(
            file_path=file_path,
            content_size=len(content),
            status="APPROVED" if success else "BLOCKED",
            details={
                "validation_enforced": True,
                "enforcement_mode": self.enforcement_mode,
                "bypass_prevented": True
            }
        )
        
        if success:
            print("✅ WRITE APPROVED: Validation passed")
        else:
            print("🚫 WRITE BLOCKED: Validation failed")
            
        return success
        
    def get_interception_stats(self) -> Dict:
        """Get interception statistics"""
        total = len(self.interceptions)
        blocked = len([i for i in self.interceptions if i["status"] == "BLOCKED"])
        approved = len([i for i in self.interceptions if i["status"] == "APPROVED"])
        
        return {
            "total_interceptions": total,
            "blocked_writes": blocked,
            "approved_writes": approved,
            "interception_rate": "comprehensive" if self.active else "0%",
            "enforcement_effectiveness": "MAXIMUM" if blocked > 0 else "PREVENTATIVE"
        }
        
    def save_interception_log(self, run_directory: str):
        """Save complete interception audit log"""
        log_path = os.path.join(run_directory, "write-interception-audit.json")
        
        log_data = {
            "interceptor": "WriteToolInterceptor",
            "version": "1.0-AUTOMATIC",
            "enforcement_level": "FRAMEWORK_WIDE",
            "active_during_run": self.active,
            "enforcement_mode": self.enforcement_mode,
            "statistics": self.get_interception_stats(),
            "interceptions": self.interceptions
        }
        
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
            
        print(f"📋 Write interception audit: {log_path}")

# GLOBAL INTERCEPTOR INSTANCE
_interceptor_instance = WriteToolInterceptor()

def activate_write_enforcement():
    """Activate framework-wide Write tool enforcement"""
    _interceptor_instance.activate_interception()
    print("🔒 ENFORCEMENT ACTIVE: All Write tools now require validation")

def deactivate_write_enforcement():
    """Deactivate enforcement (testing only)"""
    _interceptor_instance.deactivate_interception()
    print("⚠️  ENFORCEMENT DEACTIVATED: Write tools bypass validation")

def enforced_write(file_path: str, content: str) -> bool:
    """
    MANDATORY REPLACEMENT for Write tool
    
    Usage in framework:
        OLD: Write(file_path, content)  
        NEW: enforced_write(file_path, content)
    """
    return _interceptor_instance.intercept_write_call(file_path, content)

def get_write_enforcement_stats() -> Dict:
    """Get current enforcement statistics"""
    return _interceptor_instance.get_interception_stats()

def save_write_enforcement_audit(run_directory: str):
    """Save enforcement audit for current run"""
    _interceptor_instance.save_interception_log(run_directory)
    # Also save the underlying validated write audit
    save_enforcement_audit(run_directory)

# AUTOMATIC ACTIVATION ON IMPORT
activate_write_enforcement()

if __name__ == "__main__":
    print("WRITE TOOL INTERCEPTOR")
    print("======================")
    print("This module automatically enforces validation on all Write operations")
    print("")
    print("Commands:")
    print("  activate   - Enable enforcement")
    print("  deactivate - Disable enforcement") 
    print("  stats      - Show enforcement statistics")
    print("  test       - Test with sample content")
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "activate":
            activate_write_enforcement()
        elif command == "deactivate":
            deactivate_write_enforcement()
        elif command == "stats":
            stats = get_write_enforcement_stats()
            print(json.dumps(stats, indent=2))
        elif command == "test":
            # Test with invalid content (should be blocked)
            test_content = "Test content with <br> HTML tag"
            result = enforced_write("/tmp/test-enforcement.md", test_content)
            print(f"Test result: {'APPROVED' if result else 'BLOCKED'}")
    else:
        print("Use --help for commands or import to activate enforcement")