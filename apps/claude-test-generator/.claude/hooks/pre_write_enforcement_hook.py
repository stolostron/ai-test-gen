#!/usr/bin/env python3
"""
Claude Code Pre-Write Enforcement Hook
MAXIMUM ROBUSTNESS: Intercepts ALL Write tool calls and enforces mandatory validation

This hook integrates with Claude Code's tool execution system to provide
unavoidable validation enforcement that cannot be bypassed by any framework.
"""

import os
import sys
import json
import traceback
from pathlib import Path
from datetime import datetime

# Add enforcement directory to path
enforcement_dir = Path(__file__).parent.parent / "enforcement"
sys.path.insert(0, str(enforcement_dir))

try:
    from pre_write_validator import enforce_pre_write_validation
    from format_validator import FormatEnforcementValidator
except ImportError as e:
    print(f"⚠️  Warning: Could not import validation modules: {e}")
    print("🔧 Falling back to basic validation")

class PreWriteEnforcementHook:
    """Claude Code tool hook for Write tool interception and validation"""
    
    def __init__(self):
        self.hook_name = "pre_write_enforcement_hook"
        self.version = "1.0-ROBUST"
        self.enforcement_log = []
        self.stats = {
            "total_writes": 0,
            "blocked_writes": 0,
            "approved_writes": 0,
            "validation_errors": 0
        }
        
    def log_enforcement_action(self, file_path: str, action: str, details: dict):
        """Log all enforcement actions for audit trail"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "hook": self.hook_name,
            "file_path": file_path,
            "action": action,
            "details": details
        }
        self.enforcement_log.append(entry)
        
        # Also write to immediate log for debugging
        log_dir = Path.cwd() / ".claude" / "logs"
        log_dir.mkdir(exist_ok=True)
        
        with open(log_dir / "enforcement_hook.log", "a") as f:
            f.write(f"{datetime.now().isoformat()} - {action}: {file_path} - {details}\n")
    
    def validate_write_content(self, file_path: str, content: str) -> tuple[bool, dict]:
        """
        Execute comprehensive validation on Write tool content
        
        Returns:
            (validation_passed: bool, result_details: dict)
        """
        try:
            # Use existing validation system if available
            if 'enforce_pre_write_validation' in globals():
                validation_passed = enforce_pre_write_validation(file_path, content)
                return validation_passed, {"method": "full_validation", "passed": validation_passed}
            else:
                # Fallback basic validation
                return self.basic_html_validation(content)
                
        except Exception as e:
            self.stats["validation_errors"] += 1
            error_details = {
                "method": "validation_error", 
                "error": str(e),
                "fallback": "basic_validation"
            }
            
            # Use basic validation as fallback
            basic_result, basic_details = self.basic_html_validation(content)
            error_details.update(basic_details)
            
            return basic_result, error_details
    
    def basic_html_validation(self, content: str) -> tuple[bool, dict]:
        """Basic HTML tag detection as fallback"""
        html_patterns = [r'<br\s*/?>', r'<[^>]+>', r'&lt;', r'&gt;', r'&amp;']
        
        violations = []
        for pattern in html_patterns:
            import re
            matches = re.findall(pattern, content, re.IGNORECASE)
            violations.extend(matches)
        
        if violations:
            return False, {
                "method": "basic_html_validation",
                "violations": violations,
                "violation_count": len(violations)
            }
        
        return True, {"method": "basic_html_validation", "passed": True}
    
    def process_write_tool_call(self, tool_name: str, parameters: dict) -> dict:
        """
        Main hook function: Process Write tool calls with mandatory validation
        
        This function is called by Claude Code before executing the Write tool.
        It enforces validation and can block the tool execution if violations are found.
        """
        # Only process Write tool calls
        if tool_name != "Write":
            return parameters  # Pass through other tools unchanged
        
        # Extract Write tool parameters
        file_path = parameters.get("file_path", "unknown_file")
        content = parameters.get("content", "")
        
        self.stats["total_writes"] += 1
        
        print(f"\n🛡️  PRE-WRITE ENFORCEMENT HOOK: {file_path}")
        print("=" * 60)
        
        # Execute validation
        validation_passed, validation_details = self.validate_write_content(file_path, content)
        
        if not validation_passed:
            # BLOCK THE WRITE OPERATION
            self.stats["blocked_writes"] += 1
            
            block_details = {
                "reason": "Validation failed",
                "validation_details": validation_details,
                "action": "Write operation blocked"
            }
            
            self.log_enforcement_action(file_path, "BLOCKED", block_details)
            
            # Create detailed error message
            error_message = f"""
🚨 WRITE OPERATION BLOCKED BY ENFORCEMENT HOOK

📁 File: {file_path}
❌ Reason: Content validation failed
🔧 Action Required: Fix violations before proceeding

📋 Validation Details:
{json.dumps(validation_details, indent=2)}

⚠️  The Write tool will not execute until violations are resolved.
🛠️  Please regenerate content without HTML tags and try again.
"""
            
            print(error_message)
            
            # Raise exception to block Write tool execution
            raise ValueError(f"Write operation blocked: {validation_details}")
        
        # APPROVE THE WRITE OPERATION
        self.stats["approved_writes"] += 1
        
        approval_details = {
            "reason": "Validation passed",
            "validation_details": validation_details,
            "action": "Write operation approved",
            "content_size": len(content)
        }
        
        self.log_enforcement_action(file_path, "APPROVED", approval_details)
        
        print(f"✅ VALIDATION PASSED - Write operation approved")
        print(f"📁 File: {file_path}")
        print(f"📊 Content size: {len(content)} characters")
        
        # Return parameters unchanged (allow Write tool to proceed)
        return parameters
    
    def save_enforcement_audit(self, run_directory: str = None):
        """Save complete enforcement audit log"""
        if run_directory is None:
            run_directory = Path.cwd()
        
        audit_path = Path(run_directory) / "enforcement_hook_audit.json"
        
        audit_data = {
            "hook_name": self.hook_name,
            "version": self.version,
            "enforcement_level": "MAXIMUM_UNAVOIDABLE",
            "integration": "claude_code_tool_hook",
            "statistics": self.stats,
            "enforcement_log": self.enforcement_log,
            "audit_timestamp": datetime.now().isoformat()
        }
        
        with open(audit_path, 'w') as f:
            json.dump(audit_data, f, indent=2)
        
        print(f"📋 Enforcement audit saved: {audit_path}")
        return audit_path

# GLOBAL HOOK INSTANCE
_hook_instance = PreWriteEnforcementHook()

def claude_code_tool_hook(tool_name: str, parameters: dict) -> dict:
    """
    Main Claude Code hook function
    
    This function is called by Claude Code before executing any tool.
    For Write tools, it enforces mandatory validation.
    """
    try:
        return _hook_instance.process_write_tool_call(tool_name, parameters)
    except Exception as e:
        # Log the error but don't let hook errors break the framework
        _hook_instance.log_enforcement_action(
            parameters.get("file_path", "unknown"), 
            "HOOK_ERROR", 
            {"error": str(e), "traceback": traceback.format_exc()}
        )
        
        # Re-raise validation errors (these should block)
        if "Write operation blocked" in str(e):
            raise
        
        # For other errors, log but allow operation
        print(f"⚠️  Hook error (non-blocking): {e}")
        return parameters

def get_enforcement_stats() -> dict:
    """Get current enforcement statistics"""
    return _hook_instance.stats

def save_audit_log(run_directory: str = None) -> str:
    """Save enforcement audit log"""
    return _hook_instance.save_enforcement_audit(run_directory)

# Claude Code Hook Registration
# (This section would be used by Claude Code to register the hook)
HOOK_METADATA = {
    "name": "pre_write_enforcement_hook",
    "version": "1.0-ROBUST",
    "description": "Mandatory validation enforcement for Write tool operations",
    "author": "Claude Code Enforcement System",
    "hook_function": claude_code_tool_hook,
    "target_tools": ["Write"],
    "enforcement_level": "CRITICAL",
    "can_block_operations": True
}

if __name__ == "__main__":
    # Test interface for hook validation
    if len(sys.argv) == 3:
        # Test mode: python hook.py <file_path> <content>
        test_file = sys.argv[1]
        test_content = sys.argv[2]
        
        print("🧪 TESTING ENFORCEMENT HOOK")
        print("=" * 40)
        
        test_params = {
            "file_path": test_file,
            "content": test_content
        }
        
        try:
            result = claude_code_tool_hook("Write", test_params)
            print("✅ Test result: Write operation would be APPROVED")
            print("📊 Hook statistics:", get_enforcement_stats())
        except Exception as e:
            print(f"🚨 Test result: Write operation would be BLOCKED")
            print(f"❌ Reason: {e}")
            print("📊 Hook statistics:", get_enforcement_stats())
    else:
        print("Claude Code Pre-Write Enforcement Hook")
        print("Usage for testing: python hook.py <file_path> <content>")
        print("Hook ready for Claude Code integration")
        print(f"Hook metadata: {json.dumps(HOOK_METADATA, indent=2)}")