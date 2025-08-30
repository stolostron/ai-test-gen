#!/usr/bin/env python3
"""
E2E Focus Enforcer

MANDATORY ENFORCEMENT: E2E scenarios only - blocks unit/integration/performance testing
Implements CLAUDE.policies.md requirements for UI E2E direct feature testing
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Set

class E2EFocusEnforcer:
    """Enforces E2E-only focus by blocking unit/integration/performance testing"""
    
    def __init__(self):
        self.prohibited_patterns = self._load_prohibited_patterns()
        self.e2e_requirements = self._load_e2e_requirements()
        self.violation_threshold = 0  # Zero tolerance for non-E2E tests
        
    def _load_prohibited_patterns(self) -> Set[str]:
        """Load patterns that indicate prohibited non-E2E testing"""
        return {
            # BLOCKED: Unit testing patterns
            "unit testing", "unit tests", "unit test", "component testing",
            "component tests", "isolated testing", "function testing",
            "method testing", "class testing", "module testing",
            
            # BLOCKED: Integration testing patterns  
            "integration testing", "integration tests", "integration test",
            "api integration", "service integration", "component integration",
            "system integration", "interface testing",
            
            # BLOCKED: Performance testing patterns
            "performance testing", "performance tests", "performance test",
            "benchmark testing", "load testing", "stress testing",
            "scalability testing", "performance validation", "resource utilization",
            "timing measurements", "baseline performance", "performance metrics",
            
            # BLOCKED: Infrastructure/Foundation testing
            "foundation testing", "infrastructure testing", "cluster validation",
            "deployment validation", "setup testing", "configuration testing",
            "connectivity testing", "prerequisite testing",
            
            # BLOCKED: Non-E2E categories
            "smoke testing", "sanity testing", "acceptance testing",
            "compatibility testing", "regression testing", "validation testing"
        }
    
    def _load_e2e_requirements(self) -> Dict:
        """Load E2E testing requirements from CLAUDE.policies.md"""
        return {
            "focus": "UI_E2E_direct_feature_testing",
            "purpose": "Direct testing of actual feature functionality",
            "approach": "Assume infrastructure is ready - focus on feature workflows",
            "scope": [
                "ui_workflows",
                "feature_functionality", 
                "user_scenarios",
                "cli_e2e_support",
                "error_handling_in_workflows",
                "security_within_e2e_flows"
            ],
            "blocked_types": [
                "unit_testing",
                "integration_testing",
                "performance_testing", 
                "foundation_validation",
                "api_analysis_testing",
                "infrastructure_testing",
                "prerequisite_testing"
            ],
            "required_characteristics": [
                "end_to_end_workflow_focus",
                "ui_interaction_primary",
                "cli_support_secondary", 
                "real_user_scenarios",
                "feature_implementation_direct_testing"
            ]
        }
    
    def detect_prohibited_test_types(self, content: str) -> Tuple[bool, List[str]]:
        """Detect prohibited non-E2E test types in content"""
        
        violations = []
        content_lower = content.lower()
        
        # Check for prohibited patterns
        for pattern in self.prohibited_patterns:
            if re.search(pattern.lower(), content_lower):
                violations.append(f"Prohibited test type detected: '{pattern}'")
        
        # Check for specific prohibited section headers
        prohibited_headers = [
            r"unit testing.*priority",
            r"integration testing.*priority",
            r"performance testing.*priority",
            r"component testing.*priority",
            r"smoke testing.*priority",
            r"foundation.*testing.*priority",
            r"infrastructure.*testing.*priority"
        ]
        
        for header_pattern in prohibited_headers:
            if re.search(header_pattern, content_lower):
                violations.append(f"Prohibited test category header: matches '{header_pattern}'")
        
        # Check for test case priorities that suggest non-E2E focus
        priority_violations = []
        if re.search(r"unit.*p0.*priority", content_lower):
            priority_violations.append("Unit testing marked as P0 priority")
        if re.search(r"integration.*p0.*priority", content_lower):
            priority_violations.append("Integration testing marked as P0 priority")
        if re.search(r"end-to-end.*p1.*priority", content_lower):
            priority_violations.append("E2E testing marked as P1 (should be P0)")
            
        violations.extend(priority_violations)
        
        return len(violations) > 0, violations
    
    def validate_e2e_focus_compliance(self, test_plan_content: str) -> Tuple[bool, Dict]:
        """Validate test plan maintains E2E-only focus per CLAUDE.policies.md"""
        
        validation_result = {
            "compliant": True,
            "violations": [],
            "prohibited_test_categories": [],
            "compliance_score": 100,
            "enforcement_actions": [],
            "e2e_focus_percentage": 0
        }
        
        # Detect prohibited test types
        has_prohibited, prohibited_violations = self.detect_prohibited_test_types(test_plan_content)
        
        if has_prohibited:
            validation_result["compliant"] = False
            validation_result["violations"].extend(prohibited_violations)
            
            # Extract prohibited categories
            prohibited_categories = self._extract_prohibited_categories(test_plan_content)
            validation_result["prohibited_test_categories"] = prohibited_categories
            
            # Generate enforcement actions
            for category in prohibited_categories:
                validation_result["enforcement_actions"].append({
                    "action": "remove_test_category",
                    "category": category,
                    "reason": "Violates CLAUDE.policies.md E2E-only requirement",
                    "policy_reference": "MANDATORY E2E DIRECT FEATURE TESTING PROTOCOL"
                })
        
        # Calculate E2E focus percentage
        validation_result["e2e_focus_percentage"] = self._calculate_e2e_percentage(test_plan_content)
        
        # Calculate compliance score - FIXED LOGIC: Only block if there are actual violations
        if validation_result["e2e_focus_percentage"] < 100 and len(validation_result["violations"]) > 0:
            validation_result["compliance_score"] = validation_result["e2e_focus_percentage"]
            validation_result["compliant"] = False
        elif len(validation_result["violations"]) == 0:
            # If no violations found, consider it compliant regardless of percentage calculation
            validation_result["compliance_score"] = 100
            validation_result["compliant"] = True
        
        return validation_result["compliant"], validation_result
    
    def _extract_prohibited_categories(self, content: str) -> List[str]:
        """Extract prohibited test category names from content"""
        prohibited_categories = []
        
        # Look for section headers with prohibited test types
        category_patterns = [
            (r"### \d+\.\s*(Unit Testing.*)", "Unit Testing"),
            (r"### \d+\.\s*(Integration Testing.*)", "Integration Testing"), 
            (r"### \d+\.\s*(Performance Testing.*)", "Performance Testing"),
            (r"### \d+\.\s*(Component Testing.*)", "Component Testing"),
            (r"### \d+\.\s*(Foundation Testing.*)", "Foundation Testing"),
            (r"### \d+\.\s*(Infrastructure Testing.*)", "Infrastructure Testing"),
            (r"### \d+\.\s*(Smoke Testing.*)", "Smoke Testing"),
            (r"### \d+\.\s*(Validation Testing.*)", "Validation Testing")
        ]
        
        for pattern, category_name in category_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                prohibited_categories.append(category_name)
        
        return prohibited_categories
    
    def _calculate_e2e_percentage(self, content: str) -> int:
        """Calculate percentage of content focused on E2E testing - ENHANCED to recognize valid E2E patterns"""
        
        # Enhanced approach: Look for multiple E2E indicators in content
        e2e_indicators = {
            # Test case patterns that indicate E2E testing
            "test_case_patterns": [
                r"test case \d+:",
                r"## test case",
                r"validate.*workflow",
                r"verify.*functionality",
                r"end-to-end",
                r"e2e",
                r"workflow",
                r"scenario",
                r"user.*journey"
            ],
            # Content structure patterns
            "structure_patterns": [
                r"\| step \| action \| ui method \| cli method \| expected result \|",
                r"setup.*:",
                r"description.*:",
                r"test steps",
                r"expected.*result"
            ],
            # E2E specific language
            "e2e_language": [
                r"navigate to",
                r"click.*button",
                r"log into.*console",
                r"verify.*status",
                r"ui method",
                r"cli method"
            ]
        }
        
        total_indicators = 0
        e2e_score = 0
        
        # Check each category of indicators
        for category, patterns in e2e_indicators.items():
            category_found = 0
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    category_found += 1
                    e2e_score += 1
                total_indicators += 1
        
        # If we found very few total patterns, default to high percentage for E2E-style content
        if total_indicators < 5:
            # Look for basic E2E characteristics
            basic_e2e_patterns = [
                r"test case",
                r"setup",
                r"description",
                r"step.*action",
                r"expected"
            ]
            
            basic_found = sum(1 for pattern in basic_e2e_patterns if re.search(pattern, content, re.IGNORECASE))
            if basic_found >= 3:
                return 90  # High confidence this is E2E content
        
        # Calculate percentage based on indicators found
        if total_indicators == 0:
            return 85  # Default to high percentage if no clear anti-patterns found
            
        percentage = int((e2e_score / total_indicators) * 100)
        
        # Boost percentage if no prohibited patterns detected
        prohibited_content = any(pattern in content.lower() for pattern in [
            "unit test", "integration test", "performance test", "component test",
            "mock", "stub", "unit.*testing", "integration.*testing"
        ])
        
        if not prohibited_content and percentage > 50:
            percentage = min(95, percentage + 20)  # Boost for clean E2E content
        
        return percentage
    
    def generate_e2e_enforcement_prompt(self) -> str:
        """Generate enforcement prompt for Pattern Extension Service"""
        return """
🚨 CRITICAL E2E FOCUS ENFORCEMENT (CLAUDE.policies.md):

MANDATORY REQUIREMENTS:
✅ ONLY E2E test scenarios allowed
✅ UI workflows with CLI support  
✅ Direct feature testing (assume infrastructure ready)
✅ Real user scenarios and workflows
✅ E2E Priority P0 (highest priority)

STRICTLY BLOCKED:
❌ Unit Testing categories
❌ Integration Testing categories  
❌ Performance Testing categories
❌ Foundation/Infrastructure Testing
❌ Component/API Testing
❌ Any non-E2E test types

REQUIRED FOCUS:
- End-to-end user workflows
- Feature functionality validation
- UI interactions with CLI support
- Real customer scenarios
- Error handling within workflows

ENFORCEMENT: Zero tolerance - any non-E2E test categories will be automatically blocked.
COMPLIANCE TARGET: 100% E2E focus required.
"""
    
    def enforce_e2e_focus(self, test_plan_content: str, deployment_agnostic_override: bool = False) -> Tuple[bool, Dict]:
        """Main enforcement function for E2E-only focus with deployment-agnostic override"""
        
        enforcement_result = {
            "enforcement_passed": True,
            "total_violations": 0,
            "prohibited_categories_detected": 0,
            "e2e_focus_percentage": 0,
            "compliance_score": 100,
            "violations_detail": [],
            "enforcement_actions": [],
            "corrective_recommendations": [],
            "deployment_agnostic_override": deployment_agnostic_override
        }
        
        # Validate E2E compliance
        is_compliant, validation_details = self.validate_e2e_focus_compliance(test_plan_content)
        
        # Apply deployment-agnostic override if enabled
        if deployment_agnostic_override and len(validation_details["violations"]) == 0:
            # Override enforcement if no actual violations and deployment-agnostic mode enabled
            is_compliant = True
            validation_details["compliance_score"] = 100
            validation_details["e2e_focus_percentage"] = 95  # Assume good E2E content
        
        if not is_compliant:
            enforcement_result["enforcement_passed"] = False
            enforcement_result["total_violations"] = len(validation_details["violations"])
            enforcement_result["prohibited_categories_detected"] = len(validation_details["prohibited_test_categories"])
            enforcement_result["violations_detail"] = validation_details["violations"]
            enforcement_result["enforcement_actions"] = validation_details["enforcement_actions"]
            enforcement_result["compliance_score"] = validation_details["compliance_score"]
        
        enforcement_result["e2e_focus_percentage"] = validation_details["e2e_focus_percentage"]
        
        # Generate corrective recommendations
        if not is_compliant:
            enforcement_result["corrective_recommendations"] = [
                "Remove all unit testing categories and test cases",
                "Remove all integration testing categories and test cases", 
                "Remove all performance testing categories and test cases",
                "Focus exclusively on end-to-end user workflows",
                "Convert any valid scenarios to E2E workflow format",
                "Ensure E2E testing is marked as P0 priority",
                "Include UI interactions with CLI support",
                "Test direct feature functionality assuming infrastructure is ready"
            ]
        
        return enforcement_result["enforcement_passed"], enforcement_result
    
    def generate_enforcement_report(self, enforcement_result: Dict, jira_ticket: str = None) -> str:
        """Generate detailed E2E enforcement report"""
        
        report = f"""# E2E Focus Enforcement Report

**Timestamp**: {datetime.now(timezone.utc).isoformat()}
**JIRA Ticket**: {jira_ticket or 'Unknown'}
**Enforcement Status**: {'PASSED' if enforcement_result['enforcement_passed'] else 'FAILED'}
**Policy Reference**: CLAUDE.policies.md - MANDATORY E2E DIRECT FEATURE TESTING PROTOCOL

## Summary

- **E2E Focus Percentage**: {enforcement_result['e2e_focus_percentage']}%
- **Compliance Score**: {enforcement_result['compliance_score']}%
- **Prohibited Categories Detected**: {enforcement_result['prohibited_categories_detected']}
- **Total Violations**: {enforcement_result['total_violations']}

## Enforcement Actions

"""
        
        if enforcement_result["enforcement_actions"]:
            for action in enforcement_result["enforcement_actions"]:
                report += f"""### Remove: {action['category']}
- **Action**: {action['action']}
- **Reason**: {action['reason']}
- **Policy**: {action['policy_reference']}

"""
        else:
            report += "✅ No enforcement actions required - test plan maintains E2E-only focus\n\n"
        
        # Violations detail
        if enforcement_result["violations_detail"]:
            report += "## Violations Detected\n\n"
            for violation in enforcement_result["violations_detail"]:
                report += f"- {violation}\n"
            report += "\n"
        
        # Corrective recommendations
        if enforcement_result["corrective_recommendations"]:
            report += "## Corrective Actions Required\n\n"
            for rec in enforcement_result["corrective_recommendations"]:
                report += f"- {rec}\n"
            report += "\n"
        
        report += f"""## E2E Focus Requirements (CLAUDE.policies.md)

**MANDATORY REQUIREMENTS**:
✅ UI E2E scenarios only (100% focus required)
✅ Direct feature testing assuming infrastructure ready
✅ Real user workflows and scenarios
✅ CLI support within E2E workflows
✅ Error handling within E2E flows

**STRICTLY BLOCKED**:
❌ Unit Testing categories
❌ Integration Testing categories  
❌ Performance Testing categories
❌ Foundation/Infrastructure validation
❌ Component/API analysis testing

**ENFORCEMENT LEVEL**: ZERO TOLERANCE for non-E2E test types
**COMPLIANCE TARGET**: 100% E2E focus required for framework acceptance
"""
        
        return report


def enforce_e2e_focus(test_plan_content: str, jira_ticket: str = None, deployment_agnostic: bool = False) -> Tuple[bool, Dict, str]:
    """Main E2E enforcement function with deployment-agnostic override"""
    
    enforcer = E2EFocusEnforcer()
    passed, result = enforcer.enforce_e2e_focus(test_plan_content, deployment_agnostic)
    report = enforcer.generate_enforcement_report(result, jira_ticket)
    
    return passed, result, report


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python e2e_focus_enforcer.py <test_plan_file> [jira_ticket]")
        sys.exit(1)
    
    test_plan_file = sys.argv[1]
    jira_ticket = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        with open(test_plan_file, 'r') as f:
            content = f.read()
        
        passed, result, report = enforce_e2e_focus(content, jira_ticket)
        
        print(report)
        
        if not passed:
            print(f"\n❌ E2E FOCUS ENFORCEMENT FAILED")
            print(f"Prohibited categories detected: {result['prohibited_categories_detected']}")
            print(f"E2E focus percentage: {result['e2e_focus_percentage']}%")
            sys.exit(1)
        else:
            print(f"\n✅ E2E FOCUS ENFORCEMENT PASSED")
            print(f"E2E focus: {result['e2e_focus_percentage']}%")
            sys.exit(0)
            
    except FileNotFoundError:
        print(f"Error: Test plan file not found: {test_plan_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)