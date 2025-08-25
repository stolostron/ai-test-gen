#!/usr/bin/env python3
"""
Pre-Write Validation Service
Technical enforcement mechanism that validates content before Write tool usage.
Implements the missing technical layer for semantic enforcement.
"""
import os
import sys
import re
import json
from pathlib import Path
from format_validator import FormatEnforcementValidator

class PreWriteValidationService:
    """Technical enforcement service that validates content before Write tool usage"""
    
    def __init__(self):
        self.validator = FormatEnforcementValidator()
        self.validation_log = []
        
    def determine_content_type(self, file_path: str) -> str:
        """Determine content type based on file path"""
        if ("Test-Cases" in file_path or "test-cases" in file_path or 
            "test-" in file_path or "Test" in file_path or 
            file_path.endswith(".md")):
            return "test_cases"
        elif "Complete-Analysis" in file_path or "analysis" in file_path:
            return "complete_report"
        else:
            return "general"
    
    def validate_before_write(self, file_path: str, content: str) -> bool:
        """
        MANDATORY validation before any Write tool usage
        Returns True if content passes validation, False if blocked
        """
        print(f"🔍 PRE-WRITE VALIDATION: {file_path}")
        
        content_type = self.determine_content_type(file_path)
        
        # Run comprehensive validation
        result = self.validator.comprehensive_validation(content, content_type)
        
        # Log validation attempt
        self.validation_log.append({
            "file_path": file_path,
            "content_type": content_type,
            "result": result,
            "timestamp": "2025-08-21T18:45:00Z"
        })
        
        if result["status"] in ["CRITICAL_BLOCK", "BLOCKED"]:
            print(f"🚨 WRITE BLOCKED: {file_path}")
            print(f"📋 Reason: {result['message']}")
            print(f"🔧 Required Action: {result.get('action', 'Fix violations')}")
            
            if 'violations' in result:
                print(f"⚠️  Specific Violations:")
                for violation in result['violations']:
                    print(f"   - {violation}")
            
            if 'required_fix' in result:
                print(f"✅ Required Fix: {result['required_fix']}")
            
            print(f"\n❌ CONTENT GENERATION BLOCKED - Fix violations before proceeding")
            return False
        
        print(f"✅ VALIDATION PASSED: {file_path} - Content approved for writing")
        return True
    
    def save_validation_log(self, run_directory: str):
        """Save validation log for audit purposes"""
        log_path = os.path.join(run_directory, "validation-log.json")
        with open(log_path, 'w') as f:
            json.dump(self.validation_log, f, indent=2)
        print(f"📋 Validation log saved: {log_path}")

def enforce_pre_write_validation(file_path: str, content: str) -> bool:
    """
    Main enforcement function - MUST be called before any Write tool usage
    """
    service = PreWriteValidationService()
    return service.validate_before_write(file_path, content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pre_write_validator.py <file_path> <content>")
        print("Returns exit code 0 if validation passes, 1 if blocked")
        sys.exit(1)
    
    file_path = sys.argv[1]
    content = sys.argv[2]
    
    if not enforce_pre_write_validation(file_path, content):
        sys.exit(1)
    
    sys.exit(0)