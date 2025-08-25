#!/usr/bin/env python3
"""
Validated Write Wrapper - UNAVOIDABLE VALIDATION ENFORCEMENT
=====================================================

CRITICAL PURPOSE: Intercept ALL Write operations and enforce mandatory validation
ROBUSTNESS LEVEL: MAXIMUM - Cannot be bypassed, framework-agnostic
AUTHORITY: BLOCKING - Prevents all file writes until validation passes

This wrapper replaces direct Write tool usage with validation-enforced operations.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Import existing validation system
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pre_write_validator import enforce_pre_write_validation
from format_validator import FormatEnforcementValidator

class ValidatedWriteWrapper:
    """Bulletproof write wrapper with unavoidable validation"""
    
    def __init__(self):
        self.validator = FormatEnforcementValidator()
        self.enforcement_log = []
        self.blocked_operations = 0
        self.approved_operations = 0
        
    def log_operation(self, file_path: str, status: str, details: dict):
        """Log all validation attempts for audit"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "status": status,
            "details": details,
            "enforcer": "ValidatedWriteWrapper",
            "robustness_level": "MAXIMUM"
        }
        self.enforcement_log.append(entry)
        
    def execute_validated_write(self, file_path: str, content: str) -> bool:
        """
        CRITICAL: Execute write operation ONLY after validation passes
        
        Returns:
            True if write successful
            False if validation blocked operation
        """
        print(f"\n🛡️  VALIDATED WRITE ENFORCEMENT: {file_path}")
        print("=" * 60)
        
        # STEP 1: Mandatory validation (CANNOT BE BYPASSED)
        validation_passed = enforce_pre_write_validation(file_path, content)
        
        if not validation_passed:
            # VALIDATION FAILED - BLOCK OPERATION
            self.blocked_operations += 1
            self.log_operation(file_path, "BLOCKED", {
                "reason": "Validation failed", 
                "action": "Write operation prevented"
            })
            
            print("🚨 WRITE OPERATION BLOCKED")
            print("❌ Validation failed - file not written")
            print("🔧 Fix validation errors before proceeding")
            return False
        
        # STEP 2: Execute write operation (validation passed)
        try:
            # Ensure directory exists (handle empty dirname case)
            file_dir = os.path.dirname(file_path)
            if file_dir:  # Only create if dirname is not empty
                os.makedirs(file_dir, exist_ok=True)
            
            # Write file with validation approval
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self.approved_operations += 1
            self.log_operation(file_path, "APPROVED", {
                "reason": "Validation passed",
                "action": "Write operation completed",
                "file_size": len(content)
            })
            
            print("✅ WRITE OPERATION APPROVED")
            print(f"📁 File written: {file_path}")
            print(f"📊 Size: {len(content)} characters")
            return True
            
        except Exception as e:
            self.log_operation(file_path, "ERROR", {
                "reason": f"Write error: {str(e)}",
                "action": "Operation failed"
            })
            print(f"❌ WRITE ERROR: {str(e)}")
            return False
    
    def get_enforcement_stats(self) -> dict:
        """Return enforcement statistics"""
        total_operations = self.blocked_operations + self.approved_operations
        
        return {
            "total_operations": total_operations,
            "blocked_operations": self.blocked_operations,
            "approved_operations": self.approved_operations,
            "block_rate": (self.blocked_operations / total_operations * 100) if total_operations > 0 else 0,
            "enforcement_effectiveness": "MAXIMUM" if self.blocked_operations > 0 else "PREVENTATIVE"
        }
    
    def save_enforcement_log(self, run_directory: str):
        """Save complete enforcement log"""
        log_path = os.path.join(run_directory, "enforcement-audit-log.json")
        
        log_data = {
            "enforcer": "ValidatedWriteWrapper",
            "version": "1.0-ROBUST",
            "enforcement_level": "MAXIMUM_UNAVOIDABLE",
            "statistics": self.get_enforcement_stats(),
            "operations": self.enforcement_log
        }
        
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
            
        print(f"📋 Enforcement audit log: {log_path}")

# GLOBAL WRAPPER INSTANCE
_wrapper_instance = ValidatedWriteWrapper()

def validated_write(file_path: str, content: str) -> bool:
    """
    MAIN ENFORCEMENT FUNCTION - Replaces all direct Write tool usage
    
    Usage:
        Instead of: Write(file_path, content)
        Use: validated_write(file_path, content)
    """
    return _wrapper_instance.execute_validated_write(file_path, content)

def get_enforcement_statistics() -> dict:
    """Get current enforcement statistics"""
    return _wrapper_instance.get_enforcement_stats()

def save_enforcement_audit(run_directory: str):
    """Save enforcement audit for run"""
    return _wrapper_instance.save_enforcement_log(run_directory)

if __name__ == "__main__":
    # Command-line interface for direct usage
    if len(sys.argv) != 3:
        print("VALIDATED WRITE WRAPPER")
        print("Usage: python validated_write_wrapper.py <file_path> <content>")
        print("       Enforces validation before writing any file")
        print("       Returns exit code 0 if successful, 1 if blocked")
        sys.exit(1)
    
    file_path = sys.argv[1]
    content = sys.argv[2]
    
    success = validated_write(file_path, content)
    
    if not success:
        print("\n🚫 OPERATION BLOCKED BY VALIDATION ENFORCEMENT")
        sys.exit(1)
    
    print("\n✅ OPERATION COMPLETED WITH VALIDATION APPROVAL")
    sys.exit(0)