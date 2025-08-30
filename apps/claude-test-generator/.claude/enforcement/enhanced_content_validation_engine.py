#!/usr/bin/env python3
"""
Enhanced Content Validation Rules Engine
Implements comprehensive validation patterns derived from ACM-20640 session analysis
Ensures consistent test case and complete analysis formatting
"""

import re
import json
import os
from pathlib import Path
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class DocumentType(Enum):
    TEST_CASES = "test_cases"
    COMPLETE_ANALYSIS = "complete_analysis"

class ViolationSeverity(Enum):
    CRITICAL = "critical"       # Auto-reject
    HIGH = "high"              # Must fix
    MEDIUM = "medium"          # Should fix
    LOW = "low"               # Nice to fix

@dataclass
class ValidationViolation:
    pattern: str
    message: str
    severity: ViolationSeverity
    line_number: int = None
    suggested_fix: str = None

class EnhancedContentValidationEngine:
    """
    Comprehensive validation engine implementing lessons learned from ACM-20640 session
    """
    
    def __init__(self):
        self.violations: List[ValidationViolation] = []
        self.score = 0
        self.max_score = 100
        
        # Define validation patterns based on session analysis
        self._init_forbidden_patterns()
        self._init_required_patterns()
        self._init_auto_fix_patterns()
        self._init_business_context_requirements()
        
    def _init_forbidden_patterns(self):
        """Initialize forbidden patterns that cause auto-rejection"""
        self.FORBIDDEN_PATTERNS = {
            # Vague expectations - Primary issue from session
            r"[Bb]ased on role configuration": ViolationSeverity.CRITICAL,
            r"[Bb]ased on.*configuration": ViolationSeverity.CRITICAL,
            r"[Dd]epending on": ViolationSeverity.HIGH,
            r"[Aa]ccording to.*configuration": ViolationSeverity.HIGH,
            r"[Mm]ay vary": ViolationSeverity.HIGH,
            
            # Performance/scale testing - Framework policy
            r"[Pp]erformance.*test": ViolationSeverity.CRITICAL,
            r"[Ss]tress.*test": ViolationSeverity.CRITICAL,
            r"[Ll]oad.*test": ViolationSeverity.CRITICAL,
            r"[Ss]cale.*test": ViolationSeverity.CRITICAL,
            r"[Cc]oncurrent.*user": ViolationSeverity.CRITICAL,
            r"[Rr]esponse.*time.*requirement": ViolationSeverity.CRITICAL,
            r"[Ss]ystem.*under.*load": ViolationSeverity.CRITICAL,
            
            # Environment specifics in test cases - Framework rule
            r"<CLUSTER_.*>": ViolationSeverity.MEDIUM,  # Only forbidden in Complete Analysis
            r"https://.*\.com": ViolationSeverity.HIGH,  # Only forbidden in Test Cases
            r"cluster\.example": ViolationSeverity.HIGH,  # Only forbidden in Test Cases
            
            # HTML tags - Quality issue
            r"<br\s*/?>": ViolationSeverity.MEDIUM,
            r"<[^>]+>": ViolationSeverity.MEDIUM,
        }
        
    def _init_required_patterns(self):
        """Initialize required patterns that must be present"""
        self.REQUIRED_PATTERNS = {
            # Business context explanations - Key session learning
            r"What We're Doing:.*[Tt]esting": ViolationSeverity.HIGH,
            
            # Concrete expectations - Session learning
            r"Expected.*:.*(?:yes|no|\w+)": ViolationSeverity.HIGH,
            
            # Specific CLI commands - Technical requirement
            r"CLI.*:.*oc.*": ViolationSeverity.MEDIUM,
            
            # Login standardization - Session requirement
            r"oc login.*--insecure-skip-tls-verify.*kubeadmin": ViolationSeverity.MEDIUM,
            
            # UI navigation specificity - Session requirement
            r"UI.*:.*Navigate": ViolationSeverity.MEDIUM,
        }
        
    def _init_auto_fix_patterns(self):
        """Initialize patterns for automatic fixing"""
        self.AUTO_FIX_PATTERNS = {
            "Based on role configuration": "Specific expectation based on assigned role permissions",
            "depending on": "specifically configured for",
            "according to configuration": "as defined in the role assignment",
            "may vary": "should consistently show",
            "performance test": "feature functionality test",
            "stress test": "error handling test",
            "load test": "integration workflow test",
            "<br/>": "",
            "<br>": "",
        }
        
    def _init_business_context_requirements(self):
        """Initialize business context requirements from session"""
        self.BUSINESS_CONTEXT_PATTERNS = {
            "MTV integration": "Testing Migration Toolkit for Virtualization (MTV) integration with VM RBAC to ensure cross-cluster migration permissions work correctly",
            "Console access": "Testing VM console access permissions to ensure VM operator role provides appropriate console access for troubleshooting and management",
            "Multi-cluster": "Validating that VM RBAC assignments create identical permissions across all target clusters",
            "CNV cluster filtering": "Validating that the system correctly filters clusters for VM role assignments, ensuring that only clusters with Container Native Virtualization (CNV) installed receive VM-specific permissions",
            "VM lifecycle": "Testing VM lifecycle operations to ensure granular permission controls work correctly",
            "Cross-cluster deployment": "Verifying that role assignments automatically propagate to all target clusters through the ManifestWork system"
        }
        
    def validate_document(self, file_path: str, document_type: DocumentType) -> Dict[str, Any]:
        """
        Main validation method for documents
        """
        if not os.path.exists(file_path):
            return {
                "valid": False,
                "score": 0,
                "violations": [ValidationViolation(
                    pattern="file_missing",
                    message=f"Document not found: {file_path}",
                    severity=ViolationSeverity.CRITICAL
                )],
                "auto_fixes": {}
            }
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Reset validation state
        self.violations = []
        self.score = 0
        
        # Run validation based on document type
        if document_type == DocumentType.TEST_CASES:
            self._validate_test_cases(content)
        elif document_type == DocumentType.COMPLETE_ANALYSIS:
            self._validate_complete_analysis(content)
            
        # Calculate final score
        self._calculate_score()
        
        # Generate auto-fixes
        auto_fixes = self._generate_auto_fixes(content)
        
        return {
            "valid": len([v for v in self.violations if v.severity == ViolationSeverity.CRITICAL]) == 0,
            "score": self.score,
            "violations": self.violations,
            "auto_fixes": auto_fixes,
            "summary": self._generate_validation_summary()
        }
        
    def _validate_test_cases(self, content: str):
        """Validate test cases content against enhanced rules"""
        
        # Check for forbidden patterns specific to test cases
        self._check_environment_specificity_test_cases(content)
        self._check_performance_testing_references(content)
        self._check_vague_expectations(content)
        self._check_html_tags(content)
        
        # Check for required patterns
        self._check_business_context_explanations(content)
        self._check_concrete_expectations(content)
        self._check_login_standardization(content)
        self._check_step_structure(content)
        
        # Check mandatory sections
        self._check_test_case_structure(content)
        
    def _validate_complete_analysis(self, content: str):
        """Validate complete analysis content against enhanced rules"""
        
        # Check for forbidden patterns specific to complete analysis
        self._check_placeholder_usage_complete_analysis(content)
        self._check_performance_testing_references(content)
        
        # Check for required patterns
        self._check_environment_specificity_complete_analysis(content)
        self._check_conceptual_overview_structure(content)
        self._check_mandatory_sections_complete_analysis(content)
        
        # Check implementation analysis structure
        self._check_implementation_analysis_structure(content)
        
    def _check_environment_specificity_test_cases(self, content: str):
        """Test cases should NEVER have environment-specific details"""
        patterns = [
            (r"https://console-[a-z0-9\-\.]+\.com", "Test cases must use <CLUSTER_CONSOLE_URL> placeholder"),
            (r"[a-z0-9\-]+\.dev\d+\.[a-z\-]+\.com", "Test cases must use cluster placeholders"),
            (r"almng-test\.", "Test cases must use generic cluster references")
        ]
        
        for pattern, message in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                self.violations.append(ValidationViolation(
                    pattern=pattern,
                    message=f"Line {line_num}: {message}",
                    severity=ViolationSeverity.HIGH,
                    line_number=line_num,
                    suggested_fix="Replace with appropriate placeholder"
                ))
                
    def _check_placeholder_usage_complete_analysis(self, content: str):
        """Complete analysis should NEVER have placeholders"""
        patterns = [
            (r"<CLUSTER_CONSOLE_URL>", "Complete analysis must have actual console URL"),
            (r"<TEST_CLUSTER_\d+>", "Complete analysis must have actual cluster names"),
            (r"<.*_DOMAIN>", "Complete analysis must have actual domain information")
        ]
        
        for pattern, message in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                self.violations.append(ValidationViolation(
                    pattern=pattern,
                    message=f"Line {line_num}: {message}",
                    severity=ViolationSeverity.HIGH,
                    line_number=line_num,
                    suggested_fix="Replace with actual environment details"
                ))
                
    def _check_vague_expectations(self, content: str):
        """Check for vague expectations that need to be specific"""
        vague_patterns = [
            (r"[Bb]ased on role configuration", "Replace with specific expected result"),
            (r"[Dd]epending on.*setup", "Specify exact expected behavior"),
            (r"[Mm]ay vary.*environment", "Define specific expected values"),
            (r"[Aa]ccording to.*configuration", "State concrete expectation")
        ]
        
        for pattern, fix in vague_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                self.violations.append(ValidationViolation(
                    pattern=pattern,
                    message=f"Line {line_num}: Vague expectation found - {match.group()}",
                    severity=ViolationSeverity.CRITICAL,
                    line_number=line_num,
                    suggested_fix=fix
                ))
                
    def _check_performance_testing_references(self, content: str):
        """Check for performance/scale testing which is forbidden"""
        performance_patterns = [
            (r"[Pp]erformance.*test", "Framework only supports E2E feature testing"),
            (r"[Ss]tress.*test", "Remove stress testing - not supported"),
            (r"[Ll]oad.*test", "Remove load testing - not supported"),
            (r"[Cc]oncurrent.*user", "Remove concurrent testing - not supported"),
            (r"[Ss]cale.*test", "Remove scale testing - not supported")
        ]
        
        for pattern, message in performance_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                self.violations.append(ValidationViolation(
                    pattern=pattern,
                    message=f"Line {line_num}: {message}",
                    severity=ViolationSeverity.CRITICAL,
                    line_number=line_num,
                    suggested_fix="Replace with E2E feature functionality testing"
                ))
                
    def _check_business_context_explanations(self, content: str):
        """Check that test steps have 'What We're Doing' explanations"""
        # Look for test step table rows
        test_step_pattern = r'\|\s*\d+\s*\|([^|]+)\|([^|]+)\|([^|]+)\|'
        matches = re.finditer(test_step_pattern, content)
        
        for match in matches:
            step_content = match.group(2) + match.group(3)  # Action + Expected Result columns
            if "What We're Doing:" not in step_content:
                line_num = content[:match.start()].count('\n') + 1
                self.violations.append(ValidationViolation(
                    pattern="missing_business_context",
                    message=f"Line {line_num}: Test step missing 'What We're Doing:' business context explanation",
                    severity=ViolationSeverity.HIGH,
                    line_number=line_num,
                    suggested_fix="Add 'What We're Doing: [business context]' at start of action"
                ))
                
    def _check_concrete_expectations(self, content: str):
        """Check that expectations are concrete (yes/no/specific values)"""
        expectation_pattern = r'Expected[:\s]*([^|]+)'
        matches = re.finditer(expectation_pattern, content)
        
        for match in matches:
            expectation = match.group(1).strip()
            # Check if expectation is concrete
            if not re.search(r'\b(yes|no|\d+|specific|successful|failed|created|deleted|available)\b', expectation, re.IGNORECASE):
                line_num = content[:match.start()].count('\n') + 1
                self.violations.append(ValidationViolation(
                    pattern="vague_expectation",
                    message=f"Line {line_num}: Vague expectation '{expectation}' - needs concrete result",
                    severity=ViolationSeverity.HIGH,
                    line_number=line_num,
                    suggested_fix="Replace with specific expected result (yes/no/specific value)"
                ))
                
    def _check_login_standardization(self, content: str):
        """Check for standardized login instructions"""
        if "oc login" in content:
            if not re.search(r"oc login.*--insecure-skip-tls-verify.*kubeadmin", content):
                self.violations.append(ValidationViolation(
                    pattern="non_standard_login",
                    message="Login instructions should use standard format with --insecure-skip-tls-verify and kubeadmin",
                    severity=ViolationSeverity.MEDIUM,
                    suggested_fix="Use: oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>"
                ))
                
    def _check_environment_specificity_complete_analysis(self, content: str):
        """Complete analysis must have specific environment details"""
        required_specifics = [
            (r"Test Environment:\s*[a-z0-9\-]+\.[a-z0-9\-\.]+", "Actual test environment name"),
            (r"Console URL:\s*https://console[a-z0-9\-\.]+", "Actual console URL"),
            (r"ACM Version:\s*\d+\.\d+\.\d+", "Actual ACM version"),
            (r"OpenShift Version:\s*(\d+\.\d+|Not captured)", "Actual OpenShift version or explicit not captured")
        ]
        
        for pattern, description in required_specifics:
            if not re.search(pattern, content):
                self.violations.append(ValidationViolation(
                    pattern=f"missing_{description.lower().replace(' ', '_')}",
                    message=f"Complete Analysis missing required specific detail: {description}",
                    severity=ViolationSeverity.HIGH,
                    suggested_fix=f"Add {description} from environment assessment"
                ))
                
    def _check_conceptual_overview_structure(self, content: str):
        """Check for conceptual overview before technical details in implementation analysis"""
        impl_section = re.search(r"## 🔧 Implementation Analysis.*?(?=##|$)", content, re.DOTALL)
        if impl_section:
            section_content = impl_section.group(0)
            if not re.search(r"Feature Overview.*?implements.*?transitioning", section_content, re.DOTALL):
                self.violations.append(ValidationViolation(
                    pattern="missing_conceptual_overview",
                    message="Implementation Analysis missing conceptual overview before technical details",
                    severity=ViolationSeverity.HIGH,
                    suggested_fix="Add Feature Overview paragraph explaining business purpose before code details"
                ))
                
    def _check_html_tags(self, content: str):
        """Check for HTML tags that should be removed"""
        html_pattern = r'<[^>]+>'
        matches = re.finditer(html_pattern, content)
        
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            self.violations.append(ValidationViolation(
                pattern="html_tag",
                message=f"Line {line_num}: HTML tag found: {match.group()}",
                severity=ViolationSeverity.MEDIUM,
                line_number=line_num,
                suggested_fix="Remove HTML tags"
            ))
            
    def _check_test_case_structure(self, content: str):
        """Check for mandatory test case sections"""
        required_sections = [
            "### Description",
            "### Setup", 
            "### Test Steps"
        ]
        
        for section in required_sections:
            if section not in content:
                self.violations.append(ValidationViolation(
                    pattern=f"missing_section_{section.replace('### ', '').lower()}",
                    message=f"Missing required section: {section}",
                    severity=ViolationSeverity.HIGH,
                    suggested_fix=f"Add {section} section with appropriate content"
                ))
                
    def _check_mandatory_sections_complete_analysis(self, content: str):
        """Check for mandatory complete analysis sections"""
        required_sections = [
            "## 🎯 Executive Summary",
            "## 🔧 Implementation Analysis: What Has Been Implemented",
            "## 📊 JIRA Intelligence Analysis",
            "## 🌍 Environment Intelligence Assessment"
        ]
        
        for section in required_sections:
            if section not in content:
                self.violations.append(ValidationViolation(
                    pattern=f"missing_section_{section.replace('## ', '').replace('🎯', '').replace('🔧', '').replace('📊', '').replace('🌍', '').strip().lower().replace(' ', '_')}",
                    message=f"Missing required section: {section}",
                    severity=ViolationSeverity.HIGH,
                    suggested_fix=f"Add {section} section with appropriate content"
                ))
                
    def _check_implementation_analysis_structure(self, content: str):
        """Check implementation analysis has proper conceptual to technical flow"""
        impl_match = re.search(r"## 🔧 Implementation Analysis.*?(?=##|$)", content, re.DOTALL)
        if impl_match:
            section = impl_match.group(0)
            
            # Should start with conceptual overview
            if not re.search(r"Feature Overview.*?Business Value", section, re.DOTALL):
                self.violations.append(ValidationViolation(
                    pattern="missing_conceptual_flow",
                    message="Implementation Analysis should start with Feature Overview and Business Value before technical details",
                    severity=ViolationSeverity.MEDIUM,
                    suggested_fix="Add conceptual overview paragraph before diving into code implementations"
                ))
                
    def _check_step_structure(self, content: str):
        """Check test step table structure"""
        # Look for table headers
        if "| Step | Action | Expected Result |" in content:
            # Check that there are actual test steps
            step_pattern = r'\|\s*\d+\s*\|'
            if not re.search(step_pattern, content):
                self.violations.append(ValidationViolation(
                    pattern="empty_test_steps",
                    message="Test steps table found but no test steps present",
                    severity=ViolationSeverity.HIGH,
                    suggested_fix="Add test steps to the table"
                ))
                
    def _generate_auto_fixes(self, content: str) -> Dict[str, str]:
        """Generate automatic fixes for common patterns"""
        auto_fixes = {}
        
        for pattern, replacement in self.AUTO_FIX_PATTERNS.items():
            if pattern in content:
                auto_fixes[pattern] = replacement
                
        return auto_fixes
        
    def _calculate_score(self):
        """Calculate validation score based on violations"""
        penalty_weights = {
            ViolationSeverity.CRITICAL: 25,
            ViolationSeverity.HIGH: 15,
            ViolationSeverity.MEDIUM: 8,
            ViolationSeverity.LOW: 3
        }
        
        total_penalty = 0
        for violation in self.violations:
            total_penalty += penalty_weights[violation.severity]
            
        self.score = max(0, 100 - total_penalty)
        
    def _generate_validation_summary(self) -> Dict[str, Any]:
        """Generate validation summary"""
        summary = {
            "total_violations": len(self.violations),
            "critical_violations": len([v for v in self.violations if v.severity == ViolationSeverity.CRITICAL]),
            "high_violations": len([v for v in self.violations if v.severity == ViolationSeverity.HIGH]),
            "medium_violations": len([v for v in self.violations if v.severity == ViolationSeverity.MEDIUM]),
            "low_violations": len([v for v in self.violations if v.severity == ViolationSeverity.LOW]),
            "auto_fixable": len([v for v in self.violations if v.suggested_fix]),
            "manual_review_required": len([v for v in self.violations if not v.suggested_fix])
        }
        
        return summary

# Integration point with existing framework
class EnhancedValidationIntegrator:
    """
    Integration class for connecting enhanced validation with existing Phase 4 processing
    """
    
    def __init__(self):
        self.validator = EnhancedContentValidationEngine()
        
    def validate_phase_4_output(self, test_cases_path: str, complete_analysis_path: str) -> Dict[str, Any]:
        """
        Validate both test cases and complete analysis outputs from Phase 4
        """
        results = {}
        
        # Validate test cases
        if os.path.exists(test_cases_path):
            results['test_cases'] = self.validator.validate_document(
                test_cases_path, 
                DocumentType.TEST_CASES
            )
        
        # Validate complete analysis
        if os.path.exists(complete_analysis_path):
            results['complete_analysis'] = self.validator.validate_document(
                complete_analysis_path,
                DocumentType.COMPLETE_ANALYSIS
            )
            
        # Calculate overall validation result
        results['overall'] = self._calculate_overall_result(results)
        
        return results
        
    def _calculate_overall_result(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall validation result"""
        total_critical = 0
        total_high = 0
        average_score = 0
        total_docs = 0
        
        for doc_type, result in results.items():
            if doc_type != 'overall' and result:
                total_critical += result['summary']['critical_violations']
                total_high += result['summary']['high_violations']
                average_score += result['score']
                total_docs += 1
                
        if total_docs > 0:
            average_score = average_score / total_docs
            
        return {
            "validation_passed": total_critical == 0,
            "overall_score": average_score,
            "total_critical_violations": total_critical,
            "total_high_violations": total_high,
            "documents_validated": total_docs,
            "ready_for_delivery": total_critical == 0 and total_high < 3
        }

if __name__ == "__main__":
    # Example usage for testing
    validator = EnhancedContentValidationEngine()
    
    # Test with actual files
    test_cases_path = "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs/ACM-20640/ACM-20640-Test-Cases.md"
    complete_analysis_path = "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs/ACM-20640/ACM-20640-Complete-Analysis.md"
    
    integrator = EnhancedValidationIntegrator()
    results = integrator.validate_phase_4_output(test_cases_path, complete_analysis_path)
    
    print(json.dumps(results, indent=2, default=str))