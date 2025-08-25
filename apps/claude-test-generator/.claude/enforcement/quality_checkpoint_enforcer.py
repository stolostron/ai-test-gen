#!/usr/bin/env python3
"""
Quality Checkpoint Enforcer

Enforces mandatory quality checkpoints throughout framework execution.
Prevents delivery of substandard outputs and ensures all quality gates
are passed before progression to next phases.
"""

import json
import re
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

class QualityCheckpointEnforcer:
    """Enforces quality checkpoints throughout execution"""
    
    def __init__(self):
        self.quality_gates = {
            "initialization": {
                "required": True,
                "checkpoints": ["framework_config_validation", "directory_structure_validation"]
            },
            "phase_0": {
                "required": True,
                "checkpoints": ["jira_analysis_quality", "environment_validation"]
            },
            "phase_1": {
                "required": True,
                "checkpoints": ["agent_coordination_validation", "context_inheritance_validation"]
            },
            "phase_2": {
                "required": True,
                "checkpoints": ["documentation_analysis_quality", "implementation_analysis_quality"]
            },
            "phase_3": {
                "required": True,
                "checkpoints": ["ai_analysis_quality", "strategic_intelligence_validation"]
            },
            "phase_4": {
                "required": True,
                "checkpoints": ["pattern_validation", "format_enforcement", "html_tag_prevention"]
            },
            "finalization": {
                "required": True,
                "checkpoints": ["deliverable_quality_validation", "citation_compliance", "structure_validation"]
            }
        }
        
        self.passed_checkpoints = {}
        self.failed_checkpoints = {}
        self.quality_violations = []
        self.enforcement_active = True
        
    def enforce_initialization_quality(self, initialization_data: Dict) -> Tuple[bool, List[str]]:
        """Enforce initialization quality requirements"""
        
        errors = []
        
        # Check framework configuration
        config_valid, config_errors = self._validate_framework_configuration()
        if not config_valid:
            errors.extend(config_errors)
        else:
            self._mark_checkpoint_passed("initialization", "framework_config_validation")
        
        # Check directory structure
        structure_valid, structure_errors = self._validate_directory_structure()
        if not structure_valid:
            errors.extend(structure_errors)
        else:
            self._mark_checkpoint_passed("initialization", "directory_structure_validation")
        
        overall_valid = len(errors) == 0
        
        if not overall_valid:
            self._mark_checkpoint_failed("initialization", "overall", errors)
            
        return overall_valid, errors
    
    def _validate_framework_configuration(self) -> Tuple[bool, List[str]]:
        """Validate framework configuration files"""
        
        errors = []
        required_configs = [
            ".claude/config/framework-integration-config.json",
            ".claude/enforcement/mandatory_framework_execution.py",
            ".claude/enforcement/execution_path_monitor.py"
        ]
        
        for config_path in required_configs:
            if not Path(config_path).exists():
                errors.append(f"Missing critical configuration: {config_path}")
        
        return len(errors) == 0, errors
    
    def _validate_directory_structure(self) -> Tuple[bool, List[str]]:
        """Validate directory structure"""
        
        errors = []
        required_dirs = ["runs", ".claude/config", ".claude/enforcement", ".claude/observability"]
        
        for dir_path in required_dirs:
            if not Path(dir_path).exists():
                errors.append(f"Missing required directory: {dir_path}")
        
        return len(errors) == 0, errors
    
    def enforce_jira_analysis_quality(self, jira_data: Dict) -> Tuple[bool, List[str]]:
        """Enforce JIRA analysis quality requirements"""
        
        errors = []
        
        # Check required JIRA fields
        required_fields = ["jira_ticket", "feature", "priority"]
        for field in required_fields:
            if field not in jira_data or not jira_data[field]:
                errors.append(f"Missing required JIRA field: {field}")
        
        # Validate JIRA ticket format
        jira_ticket = jira_data.get("jira_ticket", "")
        if not jira_ticket.startswith("ACM-"):
            errors.append(f"Invalid JIRA ticket format: {jira_ticket}")
        
        # Check feature description quality
        feature = jira_data.get("feature", "")
        if len(feature) < 10:
            errors.append("Feature description too short - insufficient detail")
        
        if len(errors) == 0:
            self._mark_checkpoint_passed("phase_0", "jira_analysis_quality")
        else:
            self._mark_checkpoint_failed("phase_0", "jira_analysis_quality", errors)
        
        return len(errors) == 0, errors
    
    def enforce_environment_validation_quality(self, env_data: Dict) -> Tuple[bool, List[str]]:
        """Enforce environment validation quality requirements"""
        
        errors = []
        
        # Check environment access data
        if "console_url" not in env_data:
            errors.append("Missing console URL for environment validation")
        
        if "credentials" not in env_data:
            errors.append("Missing credentials for environment access")
        
        # Validate URL format
        console_url = env_data.get("console_url", "")
        if console_url and not console_url.startswith("https://"):
            errors.append("Console URL must use HTTPS")
        
        if len(errors) == 0:
            self._mark_checkpoint_passed("phase_0", "environment_validation")
        else:
            self._mark_checkpoint_failed("phase_0", "environment_validation", errors)
        
        return len(errors) == 0, errors
    
    def enforce_agent_coordination_quality(self, coordination_data: Dict) -> Tuple[bool, List[str]]:
        """Enforce agent coordination quality requirements"""
        
        errors = []
        
        # Check agent spawning data
        required_agents = ["agent_a", "agent_d", "agent_b", "agent_c"]
        spawned_agents = coordination_data.get("agents_spawned", [])
        
        for agent in required_agents:
            if agent not in spawned_agents:
                errors.append(f"Agent {agent} not properly spawned")
        
        # Check context inheritance
        context_inheritance = coordination_data.get("context_inheritance", {})
        if not context_inheritance:
            errors.append("Missing context inheritance data")
        
        if len(errors) == 0:
            self._mark_checkpoint_passed("phase_1", "agent_coordination_validation")
        else:
            self._mark_checkpoint_failed("phase_1", "agent_coordination_validation", errors)
        
        return len(errors) == 0, errors
    
    def enforce_content_quality(self, content: str, content_type: str) -> Tuple[bool, List[str]]:
        """Enforce content quality requirements"""
        
        errors = []
        
        # HTML tag prevention
        html_violations = self._check_html_tag_violations(content)
        if html_violations:
            errors.extend(html_violations)
        
        # Structure validation for test cases
        if content_type == "test_cases":
            structure_violations = self._check_test_case_structure(content)
            if structure_violations:
                errors.extend(structure_violations)
        
        # Citation compliance
        citation_violations = self._check_citation_compliance(content)
        if citation_violations:
            errors.extend(citation_violations)
        
        # Format enforcement
        format_violations = self._check_format_compliance(content)
        if format_violations:
            errors.extend(format_violations)
        
        checkpoint_name = f"{content_type}_quality_validation"
        
        if len(errors) == 0:
            self._mark_checkpoint_passed("phase_4", checkpoint_name)
        else:
            self._mark_checkpoint_failed("phase_4", checkpoint_name, errors)
        
        return len(errors) == 0, errors
    
    def _check_html_tag_violations(self, content: str) -> List[str]:
        """Check for HTML tag violations"""
        
        violations = []
        
        # Common HTML tags that should be blocked
        html_patterns = [
            r'<br\s*/?>', 
            r'<p\s*/?>', 
            r'</p>', 
            r'<div[^>]*>', 
            r'</div>',
            r'<span[^>]*>',
            r'</span>'
        ]
        
        for pattern in html_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                violations.append(f"HTML tag violation detected: {matches[0]}")
        
        return violations
    
    def _check_test_case_structure(self, content: str) -> List[str]:
        """Check test case structure requirements"""
        
        violations = []
        
        # Required structure elements
        required_patterns = [
            r'## Test Case \d+:',
            r'### Description',
            r'### Setup', 
            r'### Test Table'
        ]
        
        for pattern in required_patterns:
            if not re.search(pattern, content):
                violations.append(f"Missing required structure: {pattern}")
        
        # Check for proper table structure
        if "| Step | Action | UI Method | CLI Method | Expected Results |" not in content:
            violations.append("Missing proper test table headers")
        
        return violations
    
    def _check_citation_compliance(self, content: str) -> List[str]:
        """Check citation compliance requirements"""
        
        violations = []
        
        # Test cases should not have citations
        if re.search(r'\[JIRA:[^]]+\]', content) or re.search(r'\[GitHub:[^]]+\]', content):
            violations.append("Test cases should not contain citations")
        
        return violations
    
    def _check_format_compliance(self, content: str) -> List[str]:
        """Check format compliance requirements"""
        
        violations = []
        
        # Check for proper YAML formatting in CLI commands
        yaml_patterns = re.findall(r'```yaml(.*?)```', content, re.DOTALL)
        for yaml_block in yaml_patterns:
            if '\\n' in yaml_block or '\\t' in yaml_block:
                violations.append("YAML block contains escape sequences - should use proper block formatting")
        
        # Check for proper markdown formatting
        if re.search(r'\*\*\*[^*]+\*\*\*', content):
            violations.append("Triple asterisk formatting detected - use proper markdown")
        
        return violations
    
    def enforce_deliverable_quality(self, file_path: str) -> Tuple[bool, List[str]]:
        """Enforce deliverable quality requirements"""
        
        errors = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except Exception as e:
            errors.append(f"Cannot read deliverable file: {e}")
            return False, errors
        
        # Determine content type from filename
        if "Test-Cases" in file_path:
            content_type = "test_cases"
        elif "Analysis" in file_path:
            content_type = "analysis"
        else:
            content_type = "general"
        
        # Run content quality checks
        content_valid, content_errors = self.enforce_content_quality(content, content_type)
        if not content_valid:
            errors.extend(content_errors)
        
        # Check file size (shouldn't be too small)
        if len(content) < 1000:
            errors.append("Deliverable content too short - insufficient detail")
        
        # Check for minimum content requirements
        if content_type == "test_cases":
            if "Test Case" not in content:
                errors.append("No test cases found in test cases file")
        
        checkpoint_name = f"deliverable_quality_{content_type}"
        
        if len(errors) == 0:
            self._mark_checkpoint_passed("finalization", checkpoint_name)
        else:
            self._mark_checkpoint_failed("finalization", checkpoint_name, errors)
        
        return len(errors) == 0, errors
    
    def _mark_checkpoint_passed(self, phase: str, checkpoint: str) -> None:
        """Mark checkpoint as passed"""
        
        if phase not in self.passed_checkpoints:
            self.passed_checkpoints[phase] = []
        
        self.passed_checkpoints[phase].append({
            "checkpoint": checkpoint,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "passed"
        })
        
        print(f"✅ Quality checkpoint PASSED: {phase}.{checkpoint}")
    
    def _mark_checkpoint_failed(self, phase: str, checkpoint: str, errors: List[str]) -> None:
        """Mark checkpoint as failed"""
        
        if phase not in self.failed_checkpoints:
            self.failed_checkpoints[phase] = []
        
        failure_record = {
            "checkpoint": checkpoint,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "failed",
            "errors": errors
        }
        
        self.failed_checkpoints[phase].append(failure_record)
        self.quality_violations.extend(errors)
        
        print(f"❌ Quality checkpoint FAILED: {phase}.{checkpoint}")
        for error in errors:
            print(f"   ⚠️ {error}")
    
    def validate_all_required_checkpoints(self, phase: str) -> Tuple[bool, List[str]]:
        """Validate all required checkpoints for a phase"""
        
        if phase not in self.quality_gates:
            return True, []  # No requirements for this phase
        
        phase_config = self.quality_gates[phase]
        if not phase_config["required"]:
            return True, []  # Phase not required
        
        required_checkpoints = phase_config["checkpoints"]
        passed_checkpoints = [cp["checkpoint"] for cp in self.passed_checkpoints.get(phase, [])]
        
        missing_checkpoints = [cp for cp in required_checkpoints if cp not in passed_checkpoints]
        
        if missing_checkpoints:
            return False, [f"Missing required checkpoint: {cp}" for cp in missing_checkpoints]
        
        return True, []
    
    def get_quality_report(self) -> Dict:
        """Generate comprehensive quality report"""
        
        total_checkpoints = sum(len(phase["checkpoints"]) for phase in self.quality_gates.values() if phase["required"])
        passed_count = sum(len(checkpoints) for checkpoints in self.passed_checkpoints.values())
        failed_count = sum(len(checkpoints) for checkpoints in self.failed_checkpoints.values())
        
        return {
            "quality_summary": {
                "total_required_checkpoints": total_checkpoints,
                "passed_checkpoints": passed_count,
                "failed_checkpoints": failed_count,
                "success_rate": (passed_count / max(total_checkpoints, 1)) * 100,
                "enforcement_status": "active" if self.enforcement_active else "inactive"
            },
            "passed_checkpoints": self.passed_checkpoints,
            "failed_checkpoints": self.failed_checkpoints,
            "quality_violations": self.quality_violations,
            "report_timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def enforce_final_quality_validation(self, run_directory: str) -> Tuple[bool, List[str]]:
        """Enforce final quality validation before completion"""
        
        errors = []
        run_path = Path(run_directory)
        
        # Check for required deliverable files
        required_files = ["Test-Cases.md", "Complete-Analysis.md", "run-metadata.json"]
        
        for required_file in required_files:
            file_path = run_path / f"*{required_file}"
            matching_files = list(run_path.glob(f"*{required_file}"))
            
            if not matching_files:
                errors.append(f"Missing required deliverable: {required_file}")
            else:
                # Validate file quality
                for file_path in matching_files:
                    file_valid, file_errors = self.enforce_deliverable_quality(str(file_path))
                    if not file_valid:
                        errors.extend([f"{file_path.name}: {err}" for err in file_errors])
        
        # Check for unauthorized files
        all_files = list(run_path.glob("*"))
        allowed_patterns = ["Test-Cases.md", "Analysis.md", "metadata.json", "Complete-Analysis.md"]
        
        for file_path in all_files:
            if file_path.is_file():
                if not any(pattern in file_path.name for pattern in allowed_patterns):
                    errors.append(f"Unauthorized file in deliverables: {file_path.name}")
        
        if len(errors) == 0:
            self._mark_checkpoint_passed("finalization", "final_quality_validation")
        else:
            self._mark_checkpoint_failed("finalization", "final_quality_validation", errors)
        
        return len(errors) == 0, errors


# Global quality enforcer
_quality_enforcer = None

def get_quality_enforcer() -> QualityCheckpointEnforcer:
    """Get global quality enforcer"""
    global _quality_enforcer
    
    if _quality_enforcer is None:
        _quality_enforcer = QualityCheckpointEnforcer()
    
    return _quality_enforcer

def enforce_initialization_quality(initialization_data: Dict) -> Tuple[bool, List[str]]:
    """Enforce initialization quality"""
    enforcer = get_quality_enforcer()
    return enforcer.enforce_initialization_quality(initialization_data)

def enforce_jira_analysis_quality(jira_data: Dict) -> Tuple[bool, List[str]]:
    """Enforce JIRA analysis quality"""
    enforcer = get_quality_enforcer()
    return enforcer.enforce_jira_analysis_quality(jira_data)

def enforce_content_quality(content: str, content_type: str) -> Tuple[bool, List[str]]:
    """Enforce content quality"""
    enforcer = get_quality_enforcer()
    return enforcer.enforce_content_quality(content, content_type)

def enforce_final_quality_validation(run_directory: str) -> Tuple[bool, List[str]]:
    """Enforce final quality validation"""
    enforcer = get_quality_enforcer()
    return enforcer.enforce_final_quality_validation(run_directory)

def get_quality_report() -> Dict:
    """Get quality enforcement report"""
    enforcer = get_quality_enforcer()
    return enforcer.get_quality_report()


if __name__ == "__main__":
    # Test quality enforcement
    enforcer = QualityCheckpointEnforcer()
    
    # Test initialization quality
    init_data = {
        "framework_config": "valid",
        "directory_structure": "valid"
    }
    
    init_valid, init_errors = enforcer.enforce_initialization_quality(init_data)
    print(f"Initialization quality: {'PASSED' if init_valid else 'FAILED'}")
    if init_errors:
        print(f"Errors: {init_errors}")
    
    # Test content quality
    test_content = """
    ## Test Case 1: Sample test case
    
    ### Description
    This is a test description.
    
    ### Setup
    - Test setup requirements
    
    ### Test Table
    | Step | Action | UI Method | CLI Method | Expected Results |
    """
    
    content_valid, content_errors = enforcer.enforce_content_quality(test_content, "test_cases")
    print(f"Content quality: {'PASSED' if content_valid else 'FAILED'}")
    if content_errors:
        print(f"Errors: {content_errors}")
    
    # Generate report
    report = enforcer.get_quality_report()
    print(f"Quality report: {json.dumps(report, indent=2)}")