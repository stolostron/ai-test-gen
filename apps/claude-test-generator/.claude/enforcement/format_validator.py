#!/usr/bin/env python3
"""
Technical Format Enforcement Validator
Implements the documented semantic requirements as executable validation code.
"""
import re
import sys
import json
from typing import Dict, List, Tuple, Any

class FormatEnforcementValidator:
    """Real-time format validation with blocking authority"""
    
    def __init__(self):
        self.html_patterns = [
            r'<br\s*/?>', 
            r'<[^>]+>',
            r'&lt;',
            r'&gt;',
            r'&amp;'
        ]
        
        self.citation_patterns = [
            r'\[Source:.*?\]',
            r'\*\[Source:.*?\]\*',
            r'\(Source:.*?\)',
            r'\[.*?:.*?:.*?\]',
            r'\[Code:.*?\]',
            r'\[GitHub:.*?\]',
            r'\[JIRA:.*?\]',
            r'\[Docs:.*?\]'
        ]
        
        self.violations = []
        
    def validate_html_tags(self, content: str, content_type: str) -> Dict[str, Any]:
        """CRITICAL: HTML tag detection and blocking"""
        violations = []
        
        for pattern in self.html_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                violations.extend(matches)
        
        if violations:
            return {
                "status": "CRITICAL_BLOCK",
                "violations": violations,
                "action": "BLOCK_HTML_CONTENT",
                "message": "HTML tags detected - must use markdown-only formatting",
                "required_fix": "Convert all HTML to proper markdown formatting",
                "blocking_priority": "ABSOLUTE"
            }
        
        return {"status": "APPROVED", "content": content}
    
    def validate_yaml_blocks(self, content: str) -> Dict[str, Any]:
        """CRITICAL: Detect HTML tags within YAML blocks"""
        yaml_html_patterns = [
            r'yaml<br>',
            r'yaml.*<br>.*apiVersion',
            r'<br>\s*apiVersion',
            r'<br>\s*kind:',
            r'<br>\s*metadata:',
            r'<br>\s*spec:'
        ]
        
        violations = []
        for pattern in yaml_html_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            if matches:
                violations.extend(matches)
        
        if violations:
            return {
                "status": "CRITICAL_BLOCK",
                "violations": violations,
                "action": "CONVERT_TO_PROPER_YAML_BLOCKS",
                "message": "HTML tags detected in YAML content - must use proper ```yaml blocks",
                "required_format": "```yaml\napiVersion: cluster.open-cluster-management.io/v1beta1\nkind: ClusterCurator\n```",
                "blocking_priority": "ABSOLUTE"
            }
        
        return {"status": "APPROVED", "yaml_format": "valid"}
    
    def validate_citations_in_test_cases(self, content: str, content_type: str) -> Dict[str, Any]:
        """Enforce citation-free test cases"""
        if content_type != "test_cases":
            return {"status": "APPROVED", "citations": "not_applicable"}
            
        violations = []
        for pattern in self.citation_patterns:
            matches = re.findall(pattern, content)
            if matches:
                violations.extend(matches)
        
        if violations:
            return {
                "status": "BLOCKED",
                "violations": violations,
                "action": "REMOVE_ALL_CITATIONS",
                "message": "Test cases file must be citation-free"
            }
        
        return {"status": "APPROVED", "citations": "none"}
    
    def validate_dual_method_coverage(self, content: str) -> Dict[str, Any]:
        """Validate dual UI+CLI method coverage"""
        # Check for table structure with required columns
        if "| Step |" not in content or "| UI Method |" not in content or "| CLI Method |" not in content:
            return {
                "status": "BLOCKED",
                "missing": ["Required table structure with Step, UI Method, CLI Method columns"],
                "action": "FIX_TABLE_STRUCTURE",
                "message": "Test cases must include dual method coverage table"
            }
        
        # Check for console login CLI method requirement
        if "Log into" in content and "Console" in content:
            if "oc login" not in content:
                return {
                    "status": "BLOCKED",
                    "missing": ["oc login CLI command for console login step"],
                    "action": "ADD_CLI_LOGIN",
                    "message": "Console login steps must include oc login CLI command"
                }
        
        return {"status": "APPROVED", "methods": "dual_coverage_validated"}
    
    def comprehensive_validation(self, content: str, content_type: str) -> Dict[str, Any]:
        """Comprehensive validation pipeline with blocking authority"""
        validation_results = []
        
        # 1. CRITICAL: HTML Tag Prevention
        html_validation = self.validate_html_tags(content, content_type)
        if html_validation["status"] == "CRITICAL_BLOCK":
            return html_validation
        
        # 2. CRITICAL: YAML HTML Prevention  
        if "yaml" in content.lower() or "oc apply" in content:
            yaml_validation = self.validate_yaml_blocks(content)
            if yaml_validation["status"] == "CRITICAL_BLOCK":
                return yaml_validation
        
        # 3. Content-specific validations
        if content_type == "test_cases":
            # Citation-free enforcement
            citation_validation = self.validate_citations_in_test_cases(content, content_type)
            if citation_validation["status"] == "BLOCKED":
                return citation_validation
            
            # Dual-method coverage
            dual_method_validation = self.validate_dual_method_coverage(content)
            if dual_method_validation["status"] == "BLOCKED":
                return dual_method_validation
        
        return {"status": "APPROVED", "content_validated": True}

def validate_file_content(file_path: str, content: str, content_type: str) -> bool:
    """Main validation function with blocking authority"""
    validator = FormatEnforcementValidator()
    result = validator.comprehensive_validation(content, content_type)
    
    if result["status"] in ["CRITICAL_BLOCK", "BLOCKED"]:
        print(f"🚨 VALIDATION FAILED: {file_path}")
        print(f"📋 Issue: {result['message']}")
        print(f"🔧 Required Action: {result.get('action', 'Fix violations')}")
        if 'violations' in result:
            print(f"⚠️  Violations Found: {result['violations']}")
        if 'required_fix' in result:
            print(f"✅ Required Fix: {result['required_fix']}")
        return False
    
    print(f"✅ VALIDATION PASSED: {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python format_validator.py <file_path> <content_type> <content>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    content_type = sys.argv[2]
    content = sys.argv[3]
    
    if not validate_file_content(file_path, content, content_type):
        sys.exit(1)
    
    sys.exit(0)