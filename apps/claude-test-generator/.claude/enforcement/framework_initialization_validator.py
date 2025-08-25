#!/usr/bin/env python3
"""
Framework Initialization Validator

Validates and enforces proper framework initialization before ANY operations.
Prevents execution without proper framework setup and run directory creation.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class FrameworkInitializationValidator:
    """Validates framework initialization requirements"""
    
    def __init__(self):
        self.validation_cache = {}
        self.strict_mode = True
        self.initialization_required = [
            "run_directory_creation",
            "metadata_generation", 
            "quality_enforcement_activation",
            "agent_architecture_preparation",
            "phase_workflow_setup"
        ]
        
    def validate_initialization_prerequisites(self) -> Tuple[bool, List[str]]:
        """Validate all initialization prerequisites"""
        
        failures = []
        
        # Check framework configuration
        config_valid, config_errors = self._validate_framework_config()
        if not config_valid:
            failures.extend(config_errors)
        
        # Check enforcement systems
        enforcement_valid, enforcement_errors = self._validate_enforcement_systems()
        if not enforcement_valid:
            failures.extend(enforcement_errors)
        
        # Check directory structure
        structure_valid, structure_errors = self._validate_directory_structure()
        if not structure_valid:
            failures.extend(structure_errors)
        
        return len(failures) == 0, failures
    
    def _validate_framework_config(self) -> Tuple[bool, List[str]]:
        """Validate framework configuration files"""
        
        errors = []
        required_configs = [
            ".claude/config/framework-integration-config.json",
            ".claude/enforcement/mandatory_framework_execution.py",
            ".claude/observability/framework_integration.py"
        ]
        
        for config_path in required_configs:
            config_file = Path(config_path)
            if not config_file.exists():
                errors.append(f"Missing critical framework config: {config_path}")
            else:
                # Validate config content for JSON files
                if config_path.endswith(".json"):
                    try:
                        with open(config_file, 'r') as f:
                            config_data = json.load(f)
                        
                        # Validate key sections exist
                        if "framework_integration_configuration" not in config_data:
                            errors.append(f"Invalid framework config structure: {config_path}")
                            
                    except json.JSONDecodeError as e:
                        errors.append(f"Invalid JSON in framework config: {config_path} - {e}")
        
        return len(errors) == 0, errors
    
    def _validate_enforcement_systems(self) -> Tuple[bool, List[str]]:
        """Validate enforcement system availability"""
        
        errors = []
        enforcement_files = [
            ".claude/enforcement/mandatory_framework_execution.py",
            ".claude/enforcement/todo_display_enforcer.py",
            ".claude/enforcement/enhanced_todo_integration.py"
        ]
        
        for enforcement_file in enforcement_files:
            if not Path(enforcement_file).exists():
                errors.append(f"Missing enforcement system: {enforcement_file}")
        
        return len(errors) == 0, errors
    
    def _validate_directory_structure(self) -> Tuple[bool, List[str]]:
        """Validate directory structure readiness"""
        
        errors = []
        required_dirs = [
            "runs",
            ".claude/config",
            ".claude/enforcement", 
            ".claude/observability",
            ".claude/logs"
        ]
        
        for dir_path in required_dirs:
            directory = Path(dir_path)
            if not directory.exists():
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    errors.append(f"Cannot create required directory: {dir_path} - {e}")
        
        return len(errors) == 0, errors
    
    def validate_jira_ticket_format(self, jira_ticket: str) -> Tuple[bool, str]:
        """Validate JIRA ticket format"""
        
        if not jira_ticket:
            return False, "JIRA ticket cannot be empty"
        
        if not jira_ticket.startswith("ACM-"):
            return False, f"JIRA ticket must start with 'ACM-': {jira_ticket}"
        
        # Extract ticket number
        try:
            ticket_parts = jira_ticket.split("-")
            if len(ticket_parts) != 2:
                return False, f"Invalid JIRA ticket format: {jira_ticket}"
            
            ticket_number = int(ticket_parts[1])
            if ticket_number <= 0:
                return False, f"Invalid JIRA ticket number: {jira_ticket}"
                
        except ValueError:
            return False, f"JIRA ticket number must be numeric: {jira_ticket}"
        
        return True, "Valid JIRA ticket format"
    
    def validate_run_directory_creation(self, jira_ticket: str) -> Tuple[bool, str, Path]:
        """Validate run directory creation"""
        
        # Validate JIRA ticket first
        ticket_valid, ticket_error = self.validate_jira_ticket_format(jira_ticket)
        if not ticket_valid:
            return False, ticket_error, None
        
        # Create timestamped run directory
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir_name = f"{jira_ticket}-{timestamp}"
        run_path = Path("runs") / jira_ticket / run_dir_name
        
        try:
            # Create directory
            run_path.mkdir(parents=True, exist_ok=True)
            
            # Validate directory exists
            if not run_path.exists():
                return False, f"Run directory creation failed: {run_path}", None
            
            # Create latest symlink
            latest_link = run_path.parent / "latest"
            if latest_link.exists():
                latest_link.unlink()
            latest_link.symlink_to(run_dir_name)
            
            return True, f"Run directory created successfully: {run_path}", run_path
            
        except Exception as e:
            return False, f"Run directory creation error: {e}", None
    
    def validate_metadata_generation(self, run_path: Path, jira_ticket: str, **kwargs) -> Tuple[bool, str]:
        """Validate metadata file generation"""
        
        metadata = {
            "run_metadata": {
                "ticket_id": jira_ticket,
                "execution_timestamp": datetime.now(timezone.utc).isoformat(),
                "framework_version": "v4.2.0-strict-enforcement",
                "enforcement_level": "MANDATORY_NO_BYPASS",
                "execution_guarantee": "FULL_6_PHASE_WORKFLOW_REQUIRED",
                "initialization_validation": "COMPLETE",
                **kwargs
            },
            "framework_state": {
                "initialized": True,
                "current_phase": None,
                "required_phases": ["phase_0", "phase_1", "phase_2", "phase_2_5", "phase_3", "phase_4", "phase_5"],
                "completed_phases": [],
                "agents_spawned": [],
                "required_agents": ["agent_a", "agent_d", "agent_b", "agent_c"]
            },
            "quality_enforcement": {
                "html_tag_prevention": "ACTIVE",
                "format_enforcement": "ACTIVE", 
                "citation_compliance": "ACTIVE",
                "pattern_validation": "ACTIVE"
            }
        }
        
        metadata_file = run_path / "run-metadata.json"
        
        try:
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Validate file was written
            if not metadata_file.exists():
                return False, "Metadata file creation failed"
            
            # Validate file content
            with open(metadata_file, 'r') as f:
                written_metadata = json.load(f)
            
            if "run_metadata" not in written_metadata:
                return False, "Invalid metadata structure"
            
            return True, f"Metadata generated successfully: {metadata_file}"
            
        except Exception as e:
            return False, f"Metadata generation error: {e}"
    
    def validate_framework_activation(self) -> Tuple[bool, List[str]]:
        """Validate framework systems are properly activated"""
        
        errors = []
        
        # Check if enforcement systems can be imported
        try:
            sys.path.append(str(Path(".claude/enforcement")))
            import mandatory_framework_execution
            print("✅ Mandatory framework execution system available")
        except ImportError as e:
            errors.append(f"Cannot import mandatory framework execution: {e}")
        
        # Check observability system
        try:
            sys.path.append(str(Path(".claude/observability")))
            import framework_integration
            print("✅ Framework integration system available")
        except ImportError as e:
            errors.append(f"Cannot import framework integration: {e}")
        
        return len(errors) == 0, errors
    
    def perform_complete_initialization_validation(self, jira_ticket: str, **kwargs) -> Dict:
        """Perform complete initialization validation"""
        
        validation_results = {
            "validation_timestamp": datetime.now(timezone.utc).isoformat(),
            "jira_ticket": jira_ticket,
            "overall_status": "unknown",
            "validation_steps": {},
            "errors": [],
            "run_metadata": None
        }
        
        print("🔍 **FRAMEWORK INITIALIZATION VALIDATION**")
        print("📋 Performing comprehensive pre-execution validation")
        
        # Step 1: Prerequisites validation
        prereq_valid, prereq_errors = self.validate_initialization_prerequisites()
        validation_results["validation_steps"]["prerequisites"] = {
            "status": "passed" if prereq_valid else "failed",
            "errors": prereq_errors
        }
        
        if not prereq_valid:
            validation_results["errors"].extend(prereq_errors)
            validation_results["overall_status"] = "failed"
            return validation_results
        
        print("✅ Prerequisites validation passed")
        
        # Step 2: JIRA ticket validation
        ticket_valid, ticket_error = self.validate_jira_ticket_format(jira_ticket)
        validation_results["validation_steps"]["jira_ticket"] = {
            "status": "passed" if ticket_valid else "failed",
            "error": ticket_error if not ticket_valid else None
        }
        
        if not ticket_valid:
            validation_results["errors"].append(ticket_error)
            validation_results["overall_status"] = "failed"
            return validation_results
        
        print(f"✅ JIRA ticket format validated: {jira_ticket}")
        
        # Step 3: Run directory creation
        dir_valid, dir_message, run_path = self.validate_run_directory_creation(jira_ticket)
        validation_results["validation_steps"]["run_directory"] = {
            "status": "passed" if dir_valid else "failed",
            "message": dir_message,
            "path": str(run_path) if run_path else None
        }
        
        if not dir_valid:
            validation_results["errors"].append(dir_message)
            validation_results["overall_status"] = "failed"
            return validation_results
        
        print(f"✅ Run directory created: {run_path}")
        
        # Step 4: Metadata generation
        metadata_valid, metadata_message = self.validate_metadata_generation(run_path, jira_ticket, **kwargs)
        validation_results["validation_steps"]["metadata"] = {
            "status": "passed" if metadata_valid else "failed",
            "message": metadata_message
        }
        
        if not metadata_valid:
            validation_results["errors"].append(metadata_message)
            validation_results["overall_status"] = "failed"
            return validation_results
        
        print("✅ Metadata generation completed")
        
        # Step 5: Framework activation validation
        activation_valid, activation_errors = self.validate_framework_activation()
        validation_results["validation_steps"]["framework_activation"] = {
            "status": "passed" if activation_valid else "failed",
            "errors": activation_errors
        }
        
        if not activation_valid:
            validation_results["errors"].extend(activation_errors)
            validation_results["overall_status"] = "failed"
            return validation_results
        
        print("✅ Framework activation validated")
        
        # All validations passed
        validation_results["overall_status"] = "passed"
        validation_results["run_metadata"] = {
            "run_directory": str(run_path),
            "jira_ticket": jira_ticket,
            "initialization_complete": True
        }
        
        print("🎉 **FRAMEWORK INITIALIZATION VALIDATION COMPLETE**")
        print("🚀 Framework ready for mandatory 6-phase execution")
        
        return validation_results


# Standalone validation functions
def validate_framework_initialization(jira_ticket: str, **kwargs) -> Dict:
    """Validate complete framework initialization"""
    validator = FrameworkInitializationValidator()
    return validator.perform_complete_initialization_validation(jira_ticket, **kwargs)

def quick_validation_check() -> bool:
    """Quick validation check for framework readiness"""
    validator = FrameworkInitializationValidator()
    prereq_valid, _ = validator.validate_initialization_prerequisites()
    return prereq_valid


if __name__ == "__main__":
    # Test validation system
    if len(sys.argv) > 1:
        jira_ticket = sys.argv[1]
        
        validator = FrameworkInitializationValidator()
        results = validator.perform_complete_initialization_validation(jira_ticket)
        
        print(f"\n📊 Validation Results:")
        print(f"Status: {results['overall_status']}")
        
        if results["errors"]:
            print(f"Errors: {results['errors']}")
        
        if results["run_metadata"]:
            print(f"Run Directory: {results['run_metadata']['run_directory']}")
        
        sys.exit(0 if results["overall_status"] == "passed" else 1)
    else:
        print("Usage: python framework_initialization_validator.py ACM-XXXXX")
        sys.exit(1)