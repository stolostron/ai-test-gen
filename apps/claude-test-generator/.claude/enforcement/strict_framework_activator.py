#!/usr/bin/env python3
"""
Strict Framework Activator

Master activator that ensures the complete mandatory framework workflow is
ALWAYS executed with NO BYPASSES, NO SHORTCUTS, and COMPLETE QUALITY ENFORCEMENT.

This is the MAIN ENTRY POINT for all framework execution.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import all enforcement systems
from mandatory_framework_execution import get_framework_enforcer, initialize_mandatory_framework
from framework_initialization_validator import validate_framework_initialization
from execution_path_monitor import get_execution_monitor, start_execution_monitoring
from quality_checkpoint_enforcer import get_quality_enforcer

class StrictFrameworkActivator:
    """Master framework activator with strict enforcement"""
    
    def __init__(self):
        self.activation_log = []
        self.enforcement_systems = {
            "mandatory_execution": False,
            "initialization_validation": False,
            "execution_monitoring": False,
            "quality_enforcement": False
        }
        self.framework_state = "uninitialized"
        
    def activate_strict_framework(self, jira_ticket: str, **kwargs) -> Dict:
        """Activate the complete mandatory framework with strict enforcement"""
        
        activation_start = datetime.now(timezone.utc)
        
        print("🔒 **STRICT FRAMEWORK ACTIVATION INITIATED**")
        print("🚫 NO BYPASSES • NO SHORTCUTS • COMPLETE WORKFLOW REQUIRED")
        print("=" * 80)
        
        activation_result = {
            "activation_timestamp": activation_start.isoformat(),
            "jira_ticket": jira_ticket,
            "enforcement_level": "MAXIMUM_STRICT",
            "activation_stages": {},
            "framework_state": "activating",
            "enforcement_systems": {},
            "errors": []
        }
        
        try:
            # Stage 1: Pre-activation validation
            stage1_result = self._stage_1_pre_activation_validation(jira_ticket, **kwargs)
            activation_result["activation_stages"]["stage_1"] = stage1_result
            
            if not stage1_result["success"]:
                activation_result["framework_state"] = "activation_failed"
                activation_result["errors"].extend(stage1_result["errors"])
                return activation_result
            
            # Stage 2: Framework initialization validation
            stage2_result = self._stage_2_initialization_validation(jira_ticket, **kwargs)
            activation_result["activation_stages"]["stage_2"] = stage2_result
            
            if not stage2_result["success"]:
                activation_result["framework_state"] = "activation_failed"
                activation_result["errors"].extend(stage2_result["errors"])
                return activation_result
            
            # Stage 3: Enforcement systems activation
            stage3_result = self._stage_3_enforcement_activation(stage2_result["run_metadata"])
            activation_result["activation_stages"]["stage_3"] = stage3_result
            
            if not stage3_result["success"]:
                activation_result["framework_state"] = "activation_failed"
                activation_result["errors"].extend(stage3_result["errors"])
                return activation_result
            
            # Stage 4: Framework execution initialization
            stage4_result = self._stage_4_framework_execution_init(jira_ticket, **kwargs)
            activation_result["activation_stages"]["stage_4"] = stage4_result
            
            if not stage4_result["success"]:
                activation_result["framework_state"] = "activation_failed"
                activation_result["errors"].extend(stage4_result["errors"])
                return activation_result
            
            # Stage 5: Final validation and handoff
            stage5_result = self._stage_5_final_validation()
            activation_result["activation_stages"]["stage_5"] = stage5_result
            
            if not stage5_result["success"]:
                activation_result["framework_state"] = "activation_failed"
                activation_result["errors"].extend(stage5_result["errors"])
                return activation_result
            
            # Activation complete
            activation_result["framework_state"] = "active_enforcing"
            activation_result["enforcement_systems"] = self.enforcement_systems
            activation_result["run_metadata"] = stage2_result["run_metadata"]
            
            activation_end = datetime.now(timezone.utc)
            activation_result["activation_duration"] = (activation_end - activation_start).total_seconds()
            
            print("🎉 **STRICT FRAMEWORK ACTIVATION COMPLETE**")
            print("🔒 All enforcement systems ACTIVE and MONITORING")
            print("🚀 6-phase mandatory workflow READY for execution")
            print("=" * 80)
            
            return activation_result
            
        except Exception as e:
            activation_result["framework_state"] = "activation_error"
            activation_result["errors"].append(f"Critical activation error: {str(e)}")
            print(f"🚨 **FRAMEWORK ACTIVATION FAILED**: {str(e)}")
            return activation_result
    
    def _stage_1_pre_activation_validation(self, jira_ticket: str, **kwargs) -> Dict:
        """Stage 1: Pre-activation validation"""
        
        print("📋 **STAGE 1**: Pre-activation validation")
        
        result = {
            "stage": "pre_activation_validation",
            "success": False,
            "errors": [],
            "validations": {}
        }
        
        # Validate JIRA ticket format
        if not jira_ticket or not jira_ticket.startswith("ACM-"):
            result["errors"].append(f"Invalid JIRA ticket format: {jira_ticket}")
        else:
            result["validations"]["jira_ticket"] = "valid"
            print(f"✅ JIRA ticket validated: {jira_ticket}")
        
        # Check framework prerequisites
        required_files = [
            ".claude/config/framework-integration-config.json",
            ".claude/enforcement/mandatory_framework_execution.py",
            ".claude/enforcement/execution_path_monitor.py",
            ".claude/enforcement/quality_checkpoint_enforcer.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            result["errors"].extend([f"Missing required file: {f}" for f in missing_files])
        else:
            result["validations"]["framework_files"] = "complete"
            print("✅ Framework files validated")
        
        result["success"] = len(result["errors"]) == 0
        return result
    
    def _stage_2_initialization_validation(self, jira_ticket: str, **kwargs) -> Dict:
        """Stage 2: Framework initialization validation"""
        
        print("📋 **STAGE 2**: Framework initialization validation")
        
        result = {
            "stage": "initialization_validation",
            "success": False,
            "errors": [],
            "run_metadata": None
        }
        
        try:
            # Run comprehensive initialization validation
            validation_result = validate_framework_initialization(jira_ticket, **kwargs)
            
            if validation_result["overall_status"] == "passed":
                result["success"] = True
                result["run_metadata"] = validation_result["run_metadata"]
                self.enforcement_systems["initialization_validation"] = True
                print("✅ Framework initialization validation PASSED")
            else:
                result["errors"] = validation_result["errors"]
                print("❌ Framework initialization validation FAILED")
                
        except Exception as e:
            result["errors"].append(f"Initialization validation error: {str(e)}")
        
        return result
    
    def _stage_3_enforcement_activation(self, run_metadata: Dict) -> Dict:
        """Stage 3: Enforcement systems activation"""
        
        print("📋 **STAGE 3**: Enforcement systems activation")
        
        result = {
            "stage": "enforcement_activation", 
            "success": False,
            "errors": [],
            "activated_systems": []
        }
        
        try:
            # Activate mandatory framework execution
            enforcer = get_framework_enforcer()
            self.enforcement_systems["mandatory_execution"] = True
            result["activated_systems"].append("mandatory_execution")
            print("✅ Mandatory execution enforcement ACTIVE")
            
            # Activate execution path monitoring
            monitor = get_execution_monitor()
            execution_context = {
                "jira_ticket": run_metadata["jira_ticket"],
                "run_directory": run_metadata["run_directory"]
            }
            start_execution_monitoring(execution_context)
            self.enforcement_systems["execution_monitoring"] = True
            result["activated_systems"].append("execution_monitoring")
            print("✅ Execution path monitoring ACTIVE")
            
            # Activate quality enforcement
            quality_enforcer = get_quality_enforcer()
            self.enforcement_systems["quality_enforcement"] = True
            result["activated_systems"].append("quality_enforcement")
            print("✅ Quality checkpoint enforcement ACTIVE")
            
            result["success"] = True
            
        except Exception as e:
            result["errors"].append(f"Enforcement activation error: {str(e)}")
        
        return result
    
    def _stage_4_framework_execution_init(self, jira_ticket: str, **kwargs) -> Dict:
        """Stage 4: Framework execution initialization"""
        
        print("📋 **STAGE 4**: Framework execution initialization")
        
        result = {
            "stage": "framework_execution_init",
            "success": False, 
            "errors": [],
            "execution_metadata": None
        }
        
        try:
            # Initialize mandatory framework execution
            execution_metadata = initialize_mandatory_framework(jira_ticket, **kwargs)
            result["execution_metadata"] = execution_metadata
            result["success"] = True
            self.framework_state = "initialized"
            print("✅ Framework execution initialized")
            
        except Exception as e:
            result["errors"].append(f"Framework execution init error: {str(e)}")
        
        return result
    
    def _stage_5_final_validation(self) -> Dict:
        """Stage 5: Final validation and readiness check"""
        
        print("📋 **STAGE 5**: Final validation and readiness check")
        
        result = {
            "stage": "final_validation",
            "success": False,
            "errors": [],
            "readiness_checks": {}
        }
        
        # Check all enforcement systems are active
        inactive_systems = [name for name, active in self.enforcement_systems.items() if not active]
        
        if inactive_systems:
            result["errors"].extend([f"Enforcement system not active: {sys}" for sys in inactive_systems])
        else:
            result["readiness_checks"]["enforcement_systems"] = "all_active"
            print("✅ All enforcement systems verified active")
        
        # Validate framework state
        if self.framework_state in ["uninitialized"]:
            result["errors"].append(f"Framework state not ready: {self.framework_state}")
        else:
            result["readiness_checks"]["framework_state"] = self.framework_state
            print(f"✅ Framework state verified: {self.framework_state}")
        
        result["success"] = len(result["errors"]) == 0
        
        if result["success"]:
            self.framework_state = "ready_for_execution"
        
        return result
    
    def get_activation_status(self) -> Dict:
        """Get current activation status"""
        
        return {
            "framework_state": self.framework_state,
            "enforcement_systems": self.enforcement_systems,
            "activation_log": self.activation_log,
            "status_timestamp": datetime.now(timezone.utc).isoformat()
        }


def activate_mandatory_framework(jira_ticket: str, **kwargs) -> Dict:
    """Main entry point for mandatory framework activation"""
    
    activator = StrictFrameworkActivator()
    return activator.activate_strict_framework(jira_ticket, **kwargs)

def check_framework_readiness() -> bool:
    """Quick check if framework is ready for activation"""
    
    try:
        # Check if all required enforcement files exist
        required_files = [
            ".claude/enforcement/mandatory_framework_execution.py",
            ".claude/enforcement/framework_initialization_validator.py", 
            ".claude/enforcement/execution_path_monitor.py",
            ".claude/enforcement/quality_checkpoint_enforcer.py"
        ]
        
        return all(Path(f).exists() for f in required_files)
        
    except Exception:
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python strict_framework_activator.py ACM-XXXXX [additional_args]")
        sys.exit(1)
    
    jira_ticket = sys.argv[1]
    
    # Parse additional arguments
    kwargs = {}
    for i in range(2, len(sys.argv)):
        if "=" in sys.argv[i]:
            key, value = sys.argv[i].split("=", 1)
            kwargs[key] = value
    
    print("🚀 Testing Strict Framework Activation")
    print(f"🎫 JIRA Ticket: {jira_ticket}")
    
    # Test activation
    result = activate_mandatory_framework(jira_ticket, **kwargs)
    
    print(f"\n📊 Activation Result:")
    print(f"Status: {result['framework_state']}")
    
    if result.get("errors"):
        print(f"Errors: {result['errors']}")
        sys.exit(1)
    
    if result.get("run_metadata"):
        print(f"Run Directory: {result['run_metadata']['run_directory']}")
    
    print("✅ Framework activation test SUCCESSFUL")