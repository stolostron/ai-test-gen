#!/usr/bin/env python3
"""
Schema-Based Structure Enforcement Engine
Implements JSON schema validation for test cases and complete analysis documents
Derived from ACM-20640 session analysis requirements
"""

import json
import jsonschema
from jsonschema import validate, ValidationError
import re
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class SchemaValidationType(Enum):
    TEST_CASES = "test-case-schema.json"
    COMPLETE_ANALYSIS = "complete-analysis-schema.json"

@dataclass
class SchemaViolation:
    path: str
    message: str
    severity: str
    schema_rule: str
    suggested_fix: str = None

class SchemaStructureEnforcer:
    """
    Schema-based structure enforcement using JSON schema validation
    Ensures documents conform to mandatory structure requirements
    """
    
    def __init__(self):
        self.schema_dir = Path(__file__).parent.parent / "templates"
        self.violations: List[SchemaViolation] = []
        self._load_schemas()
        
    def _load_schemas(self):
        """Load JSON schemas for validation"""
        try:
            # Load test case schema
            test_case_schema_path = self.schema_dir / "test-case-schema.json"
            with open(test_case_schema_path, 'r') as f:
                self.test_case_schema = json.load(f)
                
            # Load complete analysis schema
            complete_analysis_schema_path = self.schema_dir / "complete-analysis-schema.json"
            with open(complete_analysis_schema_path, 'r') as f:
                self.complete_analysis_schema = json.load(f)
                
        except Exception as e:
            raise RuntimeError(f"Failed to load validation schemas: {e}")
    
    def enforce_structure(self, file_path: str, schema_type: SchemaValidationType) -> Dict[str, Any]:
        """
        Main entry point for schema-based structure enforcement
        """
        if not os.path.exists(file_path):
            return {
                "valid": False,
                "violations": [SchemaViolation(
                    path="file_system",
                    message=f"Document not found: {file_path}",
                    severity="critical",
                    schema_rule="file_existence"
                )],
                "document_structure": {},
                "compliance_score": 0
            }
        
        # Reset validation state
        self.violations = []
        
        # Read and parse document
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Convert markdown to structured data for schema validation
        document_structure = self._extract_document_structure(content, schema_type)
        
        # Apply schema validation
        schema_violations = self._validate_against_schema(document_structure, schema_type)
        
        # Apply custom business logic validation
        business_violations = self._validate_business_rules(content, document_structure, schema_type)
        
        # Combine all violations
        all_violations = schema_violations + business_violations
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(all_violations)
        
        return {
            "valid": len([v for v in all_violations if v.severity == "critical"]) == 0,
            "violations": all_violations,
            "document_structure": document_structure,
            "compliance_score": compliance_score,
            "schema_enforcement_summary": self._generate_enforcement_summary(all_violations),
            "recommended_fixes": self._generate_fix_recommendations(all_violations)
        }
    
    def _extract_document_structure(self, content: str, schema_type: SchemaValidationType) -> Dict[str, Any]:
        """
        Extract structured data from markdown content for schema validation
        """
        if schema_type == SchemaValidationType.TEST_CASES:
            return self._extract_test_case_structure(content)
        elif schema_type == SchemaValidationType.COMPLETE_ANALYSIS:
            return self._extract_complete_analysis_structure(content)
    
    def _extract_test_case_structure(self, content: str) -> Dict[str, Any]:
        """Extract test case structure from markdown"""
        structure = {
            "test_cases": []
        }
        
        # Find test case sections
        test_case_pattern = r'## Test Case (\d+[A-Z]?): (.+?)(?=## Test Case|\Z)'
        test_cases = re.finditer(test_case_pattern, content, re.DOTALL)
        
        for match in test_cases:
            test_case_content = match.group(0)
            test_case = self._parse_test_case_section(test_case_content)
            structure["test_cases"].append(test_case)
            
        return structure
    
    def _parse_test_case_section(self, content: str) -> Dict[str, Any]:
        """Parse individual test case section"""
        test_case = {}
        
        # Extract title
        title_match = re.search(r'## (Test Case \d+[A-Z]?: .+)', content)
        if title_match:
            test_case["title"] = title_match.group(1)
            
        # Extract description section
        desc_match = re.search(r'### Description\s*\n(.*?)(?=### |$)', content, re.DOTALL)
        if desc_match:
            desc_content = desc_match.group(1).strip()
            test_case["description"] = self._parse_description_section(desc_content)
            
        # Extract setup section
        setup_match = re.search(r'### Setup\s*\n(.*?)(?=### |$)', content, re.DOTALL)
        if setup_match:
            setup_content = setup_match.group(1).strip()
            test_case["setup"] = self._parse_setup_section(setup_content)
            
        # Extract test steps
        steps_match = re.search(r'### Test Steps\s*\n(.*?)(?=### |$)', content, re.DOTALL)
        if steps_match:
            steps_content = steps_match.group(1).strip()
            test_case["test_steps"] = self._parse_test_steps_section(steps_content)
            
        return test_case
    
    def _parse_description_section(self, content: str) -> Dict[str, Any]:
        """Parse description section structure"""
        description = {
            "content": content,
            "primary_coverage": [],
            "secondary_coverage": [],
            "related_jira_tickets": []
        }
        
        # Extract coverage information if present
        primary_match = re.search(r'Primary Coverage:\s*(.+)', content)
        if primary_match:
            description["primary_coverage"] = [item.strip() for item in primary_match.group(1).split(',')]
            
        # Extract JIRA tickets if present
        jira_pattern = r'(ACM-\d+)'
        jira_matches = re.findall(jira_pattern, content)
        for ticket in jira_matches:
            description["related_jira_tickets"].append({
                "ticket": ticket,
                "status": "UNKNOWN",  # Would need additional parsing
                "description": "Referenced in description"
            })
            
        return description
    
    def _parse_setup_section(self, content: str) -> Dict[str, Any]:
        """Parse setup section structure"""
        setup = {
            "prerequisites": {"commands": []},
            "environment_config": {},
            "rbac_setup": {}
        }
        
        # Extract prerequisite commands
        prereq_pattern = r'```bash\s*\n(.*?)\n```'
        prereq_matches = re.finditer(prereq_pattern, content, re.DOTALL)
        for match in prereq_matches:
            commands = match.group(1).strip().split('\n')
            for cmd in commands:
                if cmd.strip():
                    setup["prerequisites"]["commands"].append({
                        "command": cmd.strip(),
                        "expected_output": "Command execution successful"
                    })
                    
        # Extract environment configuration
        if "ACM" in content:
            acm_version_match = re.search(r'ACM (\d+\.\d+\+)', content)
            if acm_version_match:
                setup["environment_config"]["acm_version"] = acm_version_match.group(1)
                
        # Extract RBAC setup references
        script_match = re.search(r'(https://github\.com/[^\s]+\.sh)', content)
        if script_match:
            setup["rbac_setup"]["script_reference"] = script_match.group(1)
            
        return setup
    
    def _parse_test_steps_section(self, content: str) -> Dict[str, Any]:
        """Parse test steps table structure"""
        test_steps = {
            "table_structure": {
                "columns": ["Step", "Action", "Expected Result", "Sample Commands/UI Navigation"]
            },
            "steps": []
        }
        
        # Extract table rows
        row_pattern = r'\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|'
        rows = re.finditer(row_pattern, content)
        
        for row in rows:
            step = {
                "step_number": int(row.group(1)),
                "action": row.group(2).strip(),
                "expected_result": row.group(3).strip(),
                "commands": self._parse_commands_column(row.group(4).strip())
            }
            test_steps["steps"].append(step)
            
        return test_steps
    
    def _parse_commands_column(self, commands_text: str) -> Dict[str, Any]:
        """Parse commands column into CLI and UI sections"""
        commands = {
            "cli_commands": [],
            "ui_navigation": []
        }
        
        # Extract CLI commands
        cli_pattern = r'\*\*CLI\*\*:\s*`([^`]+)`'
        cli_matches = re.finditer(cli_pattern, commands_text)
        for match in cli_matches:
            commands["cli_commands"].append({
                "command": match.group(1),
                "expected_output": "Command successful"
            })
            
        # Extract UI navigation
        ui_pattern = r'\*\*UI\*\*:\s*([^*]+)'
        ui_matches = re.finditer(ui_pattern, commands_text)
        for match in ui_matches:
            nav_text = match.group(1).strip()
            if "Navigate" in nav_text:
                commands["ui_navigation"].append(nav_text)
                
        return commands
    
    def _extract_complete_analysis_structure(self, content: str) -> Dict[str, Any]:
        """Extract complete analysis structure from markdown"""
        structure = {}
        
        # Extract summary (previously executive summary)
        summary_match = re.search(r'## 🎯 Summary\s*\n(.*?)(?=## |$)', content, re.DOTALL)
        if summary_match:
            structure["summary"] = self._parse_summary(summary_match.group(1))
            
        # Extract implementation analysis
        impl_match = re.search(r'## 🔧 Implementation Analysis.*?\n(.*?)(?=## |$)', content, re.DOTALL)
        if impl_match:
            structure["implementation_analysis"] = self._parse_implementation_analysis(impl_match.group(1))
            
        # Extract test scenarios
        test_match = re.search(r'## 🧪 Test Scenarios\s*\n(.*?)(?=## |$)', content, re.DOTALL)
        if test_match:
            structure["test_scenarios"] = self._parse_test_scenarios(test_match.group(1))
            
        # Extract business impact & strategic value
        business_match = re.search(r'## 📈 Business Impact & Strategic Value\s*\n(.*?)(?=## |$)', content, re.DOTALL)
        if business_match:
            structure["business_impact_strategic_value"] = self._parse_business_impact(business_match.group(1))
            
        return structure
    
    def _parse_summary(self, content: str) -> Dict[str, Any]:
        """Parse summary section"""
        summary = {}
        
        # Extract key fields using regex patterns
        patterns = {
            "jira_ticket": r'JIRA Ticket:\s*(ACM-\d+)',
            "priority_status": r'Priority:\s*([^\n]+)',
            "component": r'Component:\s*([^\n]+)',
            "target_release": r'Target Release:\s*(ACM [^\n]+)',
            "test_environment_status": r'Test Environment Status:\s*([^\n]+)',
            "feature_validation": r'Feature Validation:\s*([^\n]+)',
            "console_url": r'Console URL:\s*(https://[^\n]+)',
            "acm_version": r'ACM Version:\s*(\d+\.\d+\.\d+[^\n]*)',
            "ocp_version": r'OCP Version:\s*([^\n]+)',
            "business_impact": r'Business Impact:\s*([^\n]+)'
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                summary[field] = match.group(1).strip()
                
        return summary
    
    def _parse_implementation_analysis(self, content: str) -> Dict[str, Any]:
        """Parse implementation analysis section"""
        analysis = {}
        
        # Extract conceptual overview
        conceptual_match = re.search(r'### Conceptual Overview.*?\n(.*?)(?=### |$)', content, re.DOTALL)
        if conceptual_match:
            analysis["conceptual_overview"] = self._parse_conceptual_overview(conceptual_match.group(1))
            
        # Extract technical details
        technical_matches = re.finditer(r'### ([^#\n]+)\s*\n(.*?)(?=### |$)', content, re.DOTALL)
        technical_details = []
        for match in technical_matches:
            if "technical" in match.group(1).lower() or "implementation" in match.group(1).lower():
                detail = {
                    "component_name": match.group(1).strip(),
                    "code_implementation": self._extract_code_blocks(match.group(2)),
                    "purpose": match.group(2)[:200] + "..." if len(match.group(2)) > 200 else match.group(2),
                    "file_references": self._extract_file_references(match.group(2))
                }
                technical_details.append(detail)
                
        analysis["technical_details"] = technical_details
        return analysis
    
    def _parse_conceptual_overview(self, content: str) -> Dict[str, Any]:
        """Parse conceptual overview subsection"""
        overview = {}
        
        # Extract feature overview
        feature_match = re.search(r'Feature Overview:\s*([^\n]+(?:\n[^#\n][^\n]*)*)', content)
        if feature_match:
            overview["feature_overview"] = feature_match.group(1).strip()
            
        # Extract key architectural components
        components_pattern = r'\*\*([^*]+)\*\*:\s*([^\n]+)'
        components = re.findall(components_pattern, content)
        overview["key_architectural_components"] = [f"**{comp[0]}**: {comp[1]}" for comp in components]
        
        # Extract business value
        business_match = re.search(r'Business Value:\s*([^\n]+(?:\n[^#\n][^\n]*)*)', content)
        if business_match:
            overview["business_value"] = business_match.group(1).strip()
            
        return overview
    
    def _extract_code_blocks(self, content: str) -> str:
        """Extract code blocks from content"""
        code_pattern = r'```(\w+)?\s*\n(.*?)\n```'
        matches = re.findall(code_pattern, content, re.DOTALL)
        if matches:
            return f"```{matches[0][0]}\n{matches[0][1]}\n```"
        return ""
    
    def _extract_file_references(self, content: str) -> List[str]:
        """Extract file references with line numbers"""
        file_pattern = r'([^\s]+\.(ts|js|go|py|yaml|json))[:\s]*(\d+)?'
        matches = re.findall(file_pattern, content)
        return [f"{match[0]}:{match[2]}" if match[2] else match[0] for match in matches]
    
    def _parse_test_scenarios(self, content: str) -> Dict[str, Any]:
        """Parse test scenarios section"""
        scenarios = {
            "test_case_summaries": [],
            "testing_approach": ""
        }
        
        # Extract test case summaries
        test_case_pattern = r'- Test Case (\d+[A-Z]?): (.+)'
        test_cases = re.findall(test_case_pattern, content)
        for tc_num, tc_desc in test_cases:
            scenarios["test_case_summaries"].append({
                "test_case_name": f"Test Case {tc_num}:",
                "summary": tc_desc.strip(),
                "coverage_area": self._extract_coverage_area(tc_desc)
            })
            
        # Extract testing approach
        approach_match = re.search(r'### Testing Approach Summary\s*\n(.*?)(?=## |$)', content, re.DOTALL)
        if approach_match:
            scenarios["testing_approach"] = approach_match.group(1).strip()
            
        return scenarios
    
    def _parse_business_impact(self, content: str) -> Dict[str, Any]:
        """Parse business impact section"""
        impact = {
            "customer_benefits": "",
            "technical_advantages": "",
            "competitive_positioning": ""
        }
        
        # Extract customer benefits
        customer_match = re.search(r'### Customer Benefits\s*\n(.*?)(?=### |$)', content, re.DOTALL)
        if customer_match:
            impact["customer_benefits"] = customer_match.group(1).strip()
            
        # Extract technical advantages
        tech_match = re.search(r'### Technical Advantages\s*\n(.*?)(?=### |$)', content, re.DOTALL)
        if tech_match:
            impact["technical_advantages"] = tech_match.group(1).strip()
            
        # Extract competitive positioning
        competitive_match = re.search(r'### Competitive Positioning\s*\n(.*?)(?=### |$)', content, re.DOTALL)
        if competitive_match:
            impact["competitive_positioning"] = competitive_match.group(1).strip()
            
        return impact
    
    def _extract_coverage_area(self, description: str) -> str:
        """Extract coverage area from test case description"""
        # Look for common patterns in test descriptions
        if "validation" in description.lower():
            return "Feature validation"
        elif "integration" in description.lower():
            return "Integration testing"
        elif "error" in description.lower():
            return "Error handling"
        elif "permission" in description.lower() or "rbac" in description.lower():
            return "Access control"
        else:
            return "General functionality"
    
    def _validate_against_schema(self, document_structure: Dict[str, Any], schema_type: SchemaValidationType) -> List[SchemaViolation]:
        """Validate document structure against JSON schema"""
        violations = []
        
        try:
            if schema_type == SchemaValidationType.TEST_CASES:
                validate(instance=document_structure, schema=self.test_case_schema)
            elif schema_type == SchemaValidationType.COMPLETE_ANALYSIS:
                validate(instance=document_structure, schema=self.complete_analysis_schema)
                
        except ValidationError as e:
            violations.append(SchemaViolation(
                path=".".join(str(p) for p in e.absolute_path) if e.absolute_path else "root",
                message=e.message,
                severity="high" if "required" in e.message.lower() else "medium",
                schema_rule=e.schema_path[-1] if e.schema_path else "unknown",
                suggested_fix=self._generate_schema_fix_suggestion(e)
            ))
            
        return violations
    
    def _validate_business_rules(self, content: str, document_structure: Dict[str, Any], schema_type: SchemaValidationType) -> List[SchemaViolation]:
        """Apply business logic validation rules"""
        violations = []
        
        if schema_type == SchemaValidationType.TEST_CASES:
            violations.extend(self._validate_test_case_business_rules(content, document_structure))
        elif schema_type == SchemaValidationType.COMPLETE_ANALYSIS:
            violations.extend(self._validate_complete_analysis_business_rules(content, document_structure))
            
        return violations
    
    def _validate_test_case_business_rules(self, content: str, structure: Dict[str, Any]) -> List[SchemaViolation]:
        """Validate test case specific business rules"""
        violations = []
        
        # Check for "What We're Doing" explanations
        test_steps = structure.get("test_cases", [])
        for i, test_case in enumerate(test_steps):
            steps = test_case.get("test_steps", {}).get("steps", [])
            for j, step in enumerate(steps):
                action = step.get("action", "")
                if "What We're Doing:" not in action:
                    violations.append(SchemaViolation(
                        path=f"test_cases[{i}].test_steps.steps[{j}].action",
                        message="Test step missing 'What We're Doing:' business context explanation",
                        severity="high",
                        schema_rule="business_context_requirement",
                        suggested_fix="Add 'What We're Doing: [business context]' at start of action"
                    ))
                    
        # Check for environment-specific details (forbidden in test cases)
        env_specific_patterns = [
            (r'https://console-[a-z0-9\-\.]+\.com', "Use <CLUSTER_CONSOLE_URL> placeholder"),
            (r'[a-z0-9\-]+\.dev\d+\.[a-z\-]+\.com', "Use cluster placeholders"),
        ]
        
        for pattern, fix in env_specific_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                violations.append(SchemaViolation(
                    path="content",
                    message=f"Environment-specific detail found in test case: {match.group()}",
                    severity="high",
                    schema_rule="environment_agnostic_requirement",
                    suggested_fix=fix
                ))
                
        return violations
    
    def _validate_complete_analysis_business_rules(self, content: str, structure: Dict[str, Any]) -> List[SchemaViolation]:
        """Validate complete analysis specific business rules"""
        violations = []
        
        # Check for placeholder usage (forbidden in complete analysis)
        placeholder_patterns = [
            (r'<CLUSTER_CONSOLE_URL>', "Replace with actual console URL"),
            (r'<TEST_CLUSTER_\d+>', "Replace with actual cluster name"),
        ]
        
        for pattern, fix in placeholder_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                violations.append(SchemaViolation(
                    path="content",
                    message=f"Placeholder found in complete analysis: {match.group()}",
                    severity="high",
                    schema_rule="environment_specific_requirement",
                    suggested_fix=fix
                ))
                
        # Check for conceptual overview before technical details
        impl_analysis = structure.get("implementation_analysis", {})
        conceptual = impl_analysis.get("conceptual_overview", {})
        if not conceptual.get("feature_overview") or "implements" not in conceptual.get("feature_overview", ""):
            violations.append(SchemaViolation(
                path="implementation_analysis.conceptual_overview",
                message="Implementation analysis missing proper conceptual overview with business purpose",
                severity="medium",
                schema_rule="conceptual_overview_requirement",
                suggested_fix="Add Feature Overview explaining business purpose before technical details"
            ))
            
        return violations
    
    def _generate_schema_fix_suggestion(self, validation_error: ValidationError) -> str:
        """Generate fix suggestion for schema validation error"""
        error_msg = validation_error.message.lower()
        
        if "required" in error_msg:
            return f"Add missing required field: {validation_error.schema_path[-1] if validation_error.schema_path else 'unknown'}"
        elif "pattern" in error_msg:
            return "Ensure content matches required pattern format"
        elif "minimum" in error_msg:
            return "Increase content length to meet minimum requirements"
        else:
            return "Review schema requirements and adjust content accordingly"
    
    def _calculate_compliance_score(self, violations: List[SchemaViolation]) -> int:
        """Calculate overall compliance score"""
        severity_weights = {
            "critical": 25,
            "high": 15,
            "medium": 8,
            "low": 3
        }
        
        total_penalty = sum(severity_weights.get(v.severity, 5) for v in violations)
        return max(0, 100 - total_penalty)
    
    def _generate_enforcement_summary(self, violations: List[SchemaViolation]) -> Dict[str, Any]:
        """Generate enforcement summary"""
        return {
            "total_violations": len(violations),
            "critical_violations": len([v for v in violations if v.severity == "critical"]),
            "high_violations": len([v for v in violations if v.severity == "high"]),
            "medium_violations": len([v for v in violations if v.severity == "medium"]),
            "low_violations": len([v for v in violations if v.severity == "low"]),
            "schema_violations": len([v for v in violations if "schema" in v.schema_rule]),
            "business_rule_violations": len([v for v in violations if "business" in v.schema_rule])
        }
    
    def _generate_fix_recommendations(self, violations: List[SchemaViolation]) -> List[Dict[str, str]]:
        """Generate prioritized fix recommendations"""
        recommendations = []
        
        # Group violations by severity
        critical_violations = [v for v in violations if v.severity == "critical"]
        high_violations = [v for v in violations if v.severity == "high"]
        
        # Add critical fixes first
        for violation in critical_violations:
            recommendations.append({
                "priority": "IMMEDIATE",
                "path": violation.path,
                "issue": violation.message,
                "fix": violation.suggested_fix or "Manual review required"
            })
            
        # Add high priority fixes
        for violation in high_violations:
            recommendations.append({
                "priority": "HIGH",
                "path": violation.path,
                "issue": violation.message,
                "fix": violation.suggested_fix or "Manual review required"
            })
            
        return recommendations

# Integration with enhanced content validation engine
class ComprehensiveValidationOrchestrator:
    """
    Orchestrates both content validation and schema enforcement
    Provides unified validation interface for Phase 4 integration
    """
    
    def __init__(self):
        try:
            from .enhanced_content_validation_engine import EnhancedContentValidationEngine, DocumentType
        except ImportError:
            from enhanced_content_validation_engine import EnhancedContentValidationEngine, DocumentType
        
        self.content_validator = EnhancedContentValidationEngine()
        self.schema_enforcer = SchemaStructureEnforcer()
        
    def comprehensive_validate(self, file_path: str, document_type: str) -> Dict[str, Any]:
        """
        Run both content validation and schema enforcement
        """
        # Determine validation types
        if document_type.lower() == "test_cases":
            content_doc_type = DocumentType.TEST_CASES
            schema_type = SchemaValidationType.TEST_CASES
        elif document_type.lower() == "complete_analysis":
            content_doc_type = DocumentType.COMPLETE_ANALYSIS
            schema_type = SchemaValidationType.COMPLETE_ANALYSIS
        else:
            raise ValueError(f"Unknown document type: {document_type}")
            
        # Run content validation
        content_results = self.content_validator.validate_document(file_path, content_doc_type)
        
        # Run schema enforcement
        schema_results = self.schema_enforcer.enforce_structure(file_path, schema_type)
        
        # Combine results
        combined_violations = content_results["violations"] + schema_results["violations"]
        
        # Calculate overall scores
        overall_score = (content_results["score"] + schema_results["compliance_score"]) / 2
        
        return {
            "overall_valid": content_results["valid"] and schema_results["valid"],
            "overall_score": overall_score,
            "content_validation": content_results,
            "schema_enforcement": schema_results,
            "combined_violations": combined_violations,
            "total_violations": len(combined_violations),
            "ready_for_delivery": (
                len([v for v in combined_violations if getattr(v, 'severity', 'medium') == "critical"]) == 0 and
                overall_score >= 85
            ),
            "comprehensive_summary": self._generate_comprehensive_summary(content_results, schema_results)
        }
        
    def _generate_comprehensive_summary(self, content_results: Dict, schema_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive validation summary"""
        return {
            "validation_methods": ["enhanced_content_validation", "schema_structure_enforcement"],
            "content_score": content_results["score"],
            "schema_score": schema_results["compliance_score"],
            "content_violations": len(content_results["violations"]),
            "schema_violations": len(schema_results["violations"]),
            "auto_fixable_issues": len(content_results.get("auto_fixes", {})),
            "manual_review_required": schema_results["schema_enforcement_summary"]["critical_violations"] + 
                                   schema_results["schema_enforcement_summary"]["high_violations"],
            "quality_gates_passed": {
                "content_validation": content_results["valid"],
                "schema_compliance": schema_results["valid"],
                "delivery_ready": schema_results["compliance_score"] >= 85
            }
        }

if __name__ == "__main__":
    # Example usage for testing
    enforcer = SchemaStructureEnforcer()
    
    # Test with actual files
    test_cases_path = "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs/ACM-20640/ACM-20640-Test-Cases.md"
    complete_analysis_path = "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs/ACM-20640/ACM-20640-Complete-Analysis.md"
    
    # Test comprehensive validation
    orchestrator = ComprehensiveValidationOrchestrator()
    
    if os.path.exists(test_cases_path):
        test_results = orchestrator.comprehensive_validate(test_cases_path, "test_cases")
        print(json.dumps(test_results, indent=2, default=str))
        
    if os.path.exists(complete_analysis_path):
        analysis_results = orchestrator.comprehensive_validate(complete_analysis_path, "complete_analysis")
        print(json.dumps(analysis_results, indent=2, default=str))