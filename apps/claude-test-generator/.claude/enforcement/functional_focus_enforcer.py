#!/usr/bin/env python3
"""
Functional Focus Enforcer

Prevents performance testing inclusion in e2e functional test plans.
Enforces framework focus on feature functionality validation rather than performance metrics.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Set

class FunctionalFocusEnforcer:
    """Enforces functional focus by preventing performance test inclusion"""
    
    def __init__(self):
        self.performance_patterns = self._load_performance_patterns()
        self.functional_requirements = self._load_functional_requirements()
        self.violation_threshold = 0  # Zero tolerance for performance tests
        
    def _load_performance_patterns(self) -> Set[str]:
        """Load patterns that indicate performance testing"""
        return {
            # Performance measurement keywords
            "performance", "benchmark", "throughput", "latency", "response time",
            "cpu utilization", "memory usage", "resource consumption", "load testing",
            "stress testing", "performance metrics", "baseline metrics", "resource monitoring",
            "performance comparison", "timing measurements", "performance characteristics",
            "resource utilization", "performance validation", "performance optimization",
            
            # Monitoring and metrics tools
            "oc top", "prometheus", "grafana", "performance-monitor", "resource tracking",
            "baseline", "metrics collection", "monitoring infrastructure", "alerting",
            "performance analysis", "resource efficiency", "load simulation",
            
            # Performance-specific test actions
            "establish baseline", "monitor cpu", "track memory", "measure.*time",
            "performance tracking", "resource.*threshold", "utilization.*during",
            "timing.*validation", "efficiency.*verification", "resource.*cleanup.*efficiency",
            
            # Performance test descriptions
            "performance.*validation", "resource.*utilization.*validation", 
            "performance.*characteristics", "minimal.*impact.*cluster.*operations",
            "performance.*comparison.*traditional", "resource.*efficient",
            "time.*efficiency", "performance.*optimization"
        }
    
    def _load_functional_requirements(self) -> Dict:
        """Load functional testing requirements"""
        return {
            "focus": "e2e_functional_scenarios",
            "purpose": "feature_implementation_validation",
            "scope": [
                "feature_functionality",
                "workflow_validation", 
                "integration_testing",
                "error_handling",
                "security_validation",
                "user_scenarios",
                "api_behavior",
                "configuration_validation"
            ],
            "excluded_types": [
                "performance_testing",
                "load_testing", 
                "stress_testing",
                "benchmark_testing",
                "capacity_planning",
                "resource_optimization",
                "scalability_testing"
            ]
        }
    
    def detect_performance_content(self, content: str) -> Tuple[bool, List[str]]:
        """Detect performance testing content in test cases"""
        
        violations = []
        content_lower = content.lower()
        
        # Check for performance patterns
        for pattern in self.performance_patterns:
            if re.search(pattern.lower(), content_lower):
                violations.append(f"Performance pattern detected: '{pattern}'")
        
        # Check for specific performance test case titles
        performance_titles = [
            "performance.*validation",
            "resource.*utilization.*validation",
            "performance.*resource.*utilization",
            "baseline.*performance",
            "performance.*characteristics"
        ]
        
        for title_pattern in performance_titles:
            if re.search(title_pattern, content_lower):
                violations.append(f"Performance test case title detected: matches '{title_pattern}'")
        
        # Check for performance-focused descriptions
        performance_descriptions = [
            "validate.*performance.*characteristics",
            "ensure.*minimal.*impact.*cluster.*operations",
            "performance.*comparison",
            "resource.*utilization.*ensure",
            "baseline.*cluster.*performance"
        ]
        
        for desc_pattern in performance_descriptions:
            if re.search(desc_pattern, content_lower):
                violations.append(f"Performance description detected: matches '{desc_pattern}'")
        
        return len(violations) > 0, violations
    
    def validate_test_case_focus(self, test_case_content: str) -> Tuple[bool, Dict]:
        """Validate test case maintains functional focus"""
        
        validation_result = {
            "valid": True,
            "violations": [],
            "test_case_type": "unknown",
            "recommendations": [],
            "enforcement_action": "none"
        }
        
        # Detect performance content
        has_performance, performance_violations = self.detect_performance_content(test_case_content)
        
        if has_performance:
            validation_result["valid"] = False
            validation_result["violations"].extend(performance_violations)
            validation_result["test_case_type"] = "performance_testing"
            validation_result["enforcement_action"] = "block_generation"
            
            # Provide functional alternatives
            validation_result["recommendations"] = [
                "Focus on feature functionality validation instead of performance metrics",
                "Test the digest-based upgrade workflow rather than resource utilization",
                "Validate error handling and edge cases rather than timing measurements",
                "Test security and RBAC aspects rather than performance characteristics",
                "Include user workflow scenarios rather than resource monitoring"
            ]
        else:
            # Determine if it's functional
            validation_result["test_case_type"] = self._classify_test_case(test_case_content)
            validation_result["recommendations"] = [
                "Maintain focus on feature functionality validation",
                "Include comprehensive error handling scenarios",
                "Validate security and compliance aspects",
                "Test real user workflows and integration points"
            ]
        
        return validation_result["valid"], validation_result
    
    def _classify_test_case(self, content: str) -> str:
        """Classify test case type based on content"""
        
        content_lower = content.lower()
        
        # Functional patterns
        functional_patterns = [
            "workflow", "functionality", "feature", "integration", "e2e",
            "user scenario", "api behavior", "configuration", "validation"
        ]
        
        # Security patterns  
        security_patterns = [
            "rbac", "security", "authentication", "authorization", "credential",
            "audit", "compliance", "permissions"
        ]
        
        # Error handling patterns
        error_patterns = [
            "error handling", "failure", "retry", "fallback", "exception",
            "recovery", "manual override"
        ]
        
        if any(pattern in content_lower for pattern in security_patterns):
            return "security_validation"
        elif any(pattern in content_lower for pattern in error_patterns):
            return "error_handling"
        elif any(pattern in content_lower for pattern in functional_patterns):
            return "functional_validation"
        else:
            return "unknown"
    
    def enforce_functional_focus(self, test_plan_content: str) -> Tuple[bool, Dict]:
        """Enforce functional focus across entire test plan"""
        
        enforcement_result = {
            "enforcement_passed": True,
            "total_violations": 0,
            "test_cases_analyzed": 0,
            "performance_test_cases_detected": 0,
            "violations_by_test_case": {},
            "enforcement_actions": [],
            "compliance_score": 100,
            "recommendations": []
        }
        
        # Split content by test categories (updated pattern)
        test_case_sections = re.split(r'### \d+\.\s*([^(]*(?:Testing|Test))', test_plan_content)
        
        for i, section in enumerate(test_case_sections[1:], 1):  # Skip header section
            enforcement_result["test_cases_analyzed"] += 1
            
            # Validate each test case
            is_valid, validation_details = self.validate_test_case_focus(section)
            
            if not is_valid:
                enforcement_result["enforcement_passed"] = False
                enforcement_result["performance_test_cases_detected"] += 1
                enforcement_result["total_violations"] += len(validation_details["violations"])
                enforcement_result["violations_by_test_case"][f"test_case_{i}"] = validation_details
                
                # Add enforcement action
                enforcement_result["enforcement_actions"].append({
                    "test_case": f"Test Case {i}",
                    "action": "remove_performance_test_case",
                    "reason": "Performance testing detected - violates functional focus requirement",
                    "violations": validation_details["violations"]
                })
        
        # Calculate compliance score
        if enforcement_result["test_cases_analyzed"] > 0:
            compliance_percentage = ((enforcement_result["test_cases_analyzed"] - enforcement_result["performance_test_cases_detected"]) / 
                                   enforcement_result["test_cases_analyzed"]) * 100
            enforcement_result["compliance_score"] = round(compliance_percentage, 1)
        
        # Overall recommendations
        if enforcement_result["performance_test_cases_detected"] > 0:
            enforcement_result["recommendations"] = [
                f"Remove {enforcement_result['performance_test_cases_detected']} performance test case(s)",
                "Focus on feature functionality validation instead of performance metrics",
                "Add more functional scenarios covering user workflows",
                "Include comprehensive error handling and edge case testing",
                "Validate security and RBAC aspects of the feature"
            ]
        
        return enforcement_result["enforcement_passed"], enforcement_result
    
    def generate_enforcement_report(self, enforcement_result: Dict, jira_ticket: str = None) -> str:
        """Generate detailed enforcement report"""
        
        report = f"""# Functional Focus Enforcement Report

**Timestamp**: {datetime.now(timezone.utc).isoformat()}
**JIRA Ticket**: {jira_ticket or 'Unknown'}
**Enforcement Status**: {'PASSED' if enforcement_result['enforcement_passed'] else 'FAILED'}

## Summary

- **Test Cases Analyzed**: {enforcement_result['test_cases_analyzed']}
- **Performance Test Cases Detected**: {enforcement_result['performance_test_cases_detected']}
- **Total Violations**: {enforcement_result['total_violations']}
- **Compliance Score**: {enforcement_result['compliance_score']}%

## Enforcement Actions

"""
        
        if enforcement_result["enforcement_actions"]:
            for action in enforcement_result["enforcement_actions"]:
                report += f"""### {action['test_case']}
- **Action**: {action['action']}
- **Reason**: {action['reason']}
- **Violations**:
"""
                for violation in action['violations']:
                    report += f"  - {violation}\n"
                report += "\n"
        else:
            report += "✅ No enforcement actions required - all test cases maintain functional focus\n\n"
        
        # Recommendations
        if enforcement_result["recommendations"]:
            report += "## Recommendations\n\n"
            for rec in enforcement_result["recommendations"]:
                report += f"- {rec}\n"
        
        report += f"""
## Functional Focus Requirements

**Framework Purpose**: E2E scenarios targeting feature implementation
**Allowed Test Types**:
- Feature functionality validation
- Workflow and integration testing
- Error handling and edge cases
- Security and RBAC validation
- User scenario testing

**Prohibited Test Types**:
- Performance and benchmark testing
- Load and stress testing
- Resource utilization monitoring
- Timing and metrics validation
- Capacity planning scenarios

**Enforcement Level**: ZERO TOLERANCE for performance testing inclusion
"""
        
        return report


def enforce_functional_focus(test_plan_content: str, jira_ticket: str = None) -> Tuple[bool, Dict, str]:
    """Main enforcement function"""
    
    enforcer = FunctionalFocusEnforcer()
    passed, result = enforcer.enforce_functional_focus(test_plan_content)
    report = enforcer.generate_enforcement_report(result, jira_ticket)
    
    return passed, result, report


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python functional_focus_enforcer.py <test_plan_file> [jira_ticket]")
        sys.exit(1)
    
    test_plan_file = sys.argv[1]
    jira_ticket = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        with open(test_plan_file, 'r') as f:
            content = f.read()
        
        passed, result, report = enforce_functional_focus(content, jira_ticket)
        
        print(report)
        
        if not passed:
            print(f"\n❌ FUNCTIONAL FOCUS ENFORCEMENT FAILED")
            print(f"Performance test cases detected: {result['performance_test_cases_detected']}")
            sys.exit(1)
        else:
            print(f"\n✅ FUNCTIONAL FOCUS ENFORCEMENT PASSED")
            print(f"Compliance score: {result['compliance_score']}%")
            sys.exit(0)
            
    except FileNotFoundError:
        print(f"Error: Test plan file not found: {test_plan_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)