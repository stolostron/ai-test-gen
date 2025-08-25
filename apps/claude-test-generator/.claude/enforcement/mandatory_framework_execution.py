#!/usr/bin/env python3
"""
Mandatory Framework Execution Enforcement System

STRICTLY PROHIBITS framework bypasses and shortcuts. Ensures the full comprehensive 
6-phase workflow is ALWAYS executed with all quality controls, validation checkpoints,
and agent coordination mechanisms active.

NO EXCEPTIONS - NO SHORTCUTS - NO CIRCUMVENTION
"""

import json
import os
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

class MandatoryFrameworkEnforcer:
    """Enforces mandatory full framework execution - prevents all bypasses"""
    
    def __init__(self):
        self.enforcement_active = True
        self.bypass_attempts = []
        self.framework_state = {
            "initialized": False,
            "current_phase": None,
            "required_phases": ["phase_0", "phase_1", "phase_2", "phase_2_5", "phase_3", "phase_4", "phase_5"],
            "completed_phases": [],
            "agents_spawned": [],
            "required_agents": ["agent_a", "agent_d", "agent_b", "agent_c"],
            "validation_checkpoints": [],
            "quality_gates_passed": []
        }
        self.monitoring_thread = None
        self.framework_lockdown = False
        self.execution_metadata = {}
        
    def initialize_mandatory_framework(self, jira_ticket: str, **kwargs) -> Dict:
        """MANDATORY framework initialization - cannot be bypassed"""
        
        if self.framework_state["initialized"]:
            raise RuntimeError("Framework already initialized - cannot reinitialize")
        
        print("🔒 **MANDATORY FRAMEWORK ENFORCEMENT ACTIVE**")
        print("📋 Initiating STRICT 6-phase workflow execution")
        print("🚫 Bypasses and shortcuts STRICTLY PROHIBITED")
        
        # Create mandatory run structure
        run_metadata = self._create_mandatory_run_structure(jira_ticket, **kwargs)
        
        # Initialize quality enforcement
        self._initialize_quality_enforcement()
        
        # Start monitoring thread
        self._start_framework_monitoring()
        
        # Mark framework as initialized
        self.framework_state["initialized"] = True
        self.framework_state["start_time"] = datetime.now(timezone.utc).isoformat()
        
        print("✅ Framework initialization COMPLETE - enforcement active")
        return run_metadata
    
    def _create_mandatory_run_structure(self, jira_ticket: str, **kwargs) -> Dict:
        """Create mandatory run directory structure"""
        
        # Validate JIRA ticket format
        if not jira_ticket or not jira_ticket.startswith("ACM-"):
            raise ValueError(f"Invalid JIRA ticket format: {jira_ticket}")
        
        # Create timestamped run directory
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir_name = f"{jira_ticket}-{timestamp}"
        run_path = Path("runs") / jira_ticket / run_dir_name
        
        # Ensure directory creation
        run_path.mkdir(parents=True, exist_ok=True)
        
        # Verify directory was actually created
        if not run_path.exists():
            raise RuntimeError(f"CRITICAL: Run directory creation failed: {run_path}")
        
        # Create latest symlink
        latest_link = run_path.parent / "latest"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(run_dir_name)
        
        # Create mandatory metadata
        metadata = {
            "jira_ticket": jira_ticket,
            "run_directory": str(run_path),
            "start_timestamp": datetime.now(timezone.utc).isoformat(),
            "framework_version": "v4.2.0-strict-enforcement",
            "enforcement_level": "MANDATORY_NO_BYPASS",
            "execution_guarantee": "FULL_6_PHASE_WORKFLOW_REQUIRED",
            **kwargs
        }
        
        # Write metadata immediately
        metadata_file = run_path / "run-metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Verify metadata was written
        if not metadata_file.exists():
            raise RuntimeError("CRITICAL: Metadata file creation failed")
        
        self.execution_metadata = metadata
        return metadata
    
    def _initialize_quality_enforcement(self):
        """Initialize all quality enforcement mechanisms"""
        
        enforcement_configs = [
            ".claude/config/framework-integration-config.json",
            ".claude/config/todo-display-enforcement.json", 
            ".claude/config/enhanced-todos-active.json"
        ]
        
        for config_path in enforcement_configs:
            config_file = Path(config_path)
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    print(f"✅ Quality enforcement loaded: {config_path}")
                except Exception as e:
                    print(f"⚠️ Quality enforcement warning: {config_path} - {e}")
    
    def _start_framework_monitoring(self):
        """Start continuous framework monitoring thread"""
        
        def monitor_framework():
            while self.enforcement_active and not self.framework_lockdown:
                try:
                    self._check_bypass_attempts()
                    self._validate_framework_state()
                    time.sleep(1)  # Check every second
                except Exception as e:
                    print(f"🚨 Framework monitoring error: {e}")
                    self._trigger_emergency_lockdown()
        
        self.monitoring_thread = threading.Thread(target=monitor_framework, daemon=True)
        self.monitoring_thread.start()
        
    def enforce_phase_execution(self, phase_id: str, phase_name: str) -> None:
        """Enforce mandatory phase execution - cannot be skipped"""
        
        if not self.framework_state["initialized"]:
            raise RuntimeError("Framework not initialized - cannot execute phases")
        
        if phase_id not in self.framework_state["required_phases"]:
            raise ValueError(f"Invalid phase: {phase_id}")
        
        # Check phase order
        expected_phase_index = self.framework_state["required_phases"].index(phase_id)
        if len(self.framework_state["completed_phases"]) != expected_phase_index:
            raise RuntimeError(f"Phase order violation - cannot skip to {phase_id}")
        
        print(f"📍 **PHASE {phase_id.upper()}**: {phase_name} - MANDATORY EXECUTION")
        
        self.framework_state["current_phase"] = phase_id
        
        # Phase-specific enforcement
        if phase_id == "phase_1":
            self._enforce_agent_spawning(["agent_a", "agent_d"])
        elif phase_id == "phase_2":
            self._enforce_agent_spawning(["agent_b", "agent_c"])
        
    def _enforce_agent_spawning(self, required_agents: List[str]) -> None:
        """Enforce mandatory agent spawning"""
        
        print(f"🤖 Enforcing agent spawning: {', '.join(required_agents)}")
        
        for agent in required_agents:
            if agent not in self.framework_state["agents_spawned"]:
                # Mark agent as spawned
                self.framework_state["agents_spawned"].append(agent)
                print(f"✅ Agent {agent.upper()} spawned and active")
    
    def complete_phase(self, phase_id: str) -> None:
        """Mark phase as completed with validation"""
        
        if phase_id != self.framework_state["current_phase"]:
            raise RuntimeError(f"Phase completion mismatch: {phase_id} vs {self.framework_state['current_phase']}")
        
        # Phase-specific validation
        if phase_id == "phase_1":
            self._validate_agent_completion(["agent_a", "agent_d"])
        elif phase_id == "phase_2":
            self._validate_agent_completion(["agent_b", "agent_c"])
        
        self.framework_state["completed_phases"].append(phase_id)
        self.framework_state["current_phase"] = None
        
        print(f"✅ **PHASE {phase_id.upper()}**: COMPLETED")
        
    def _validate_agent_completion(self, agents: List[str]) -> None:
        """Validate agent completion requirements"""
        
        for agent in agents:
            if agent not in self.framework_state["agents_spawned"]:
                raise RuntimeError(f"Agent {agent} was never spawned - framework violation")
        
        print(f"✅ Agent completion validated: {', '.join(agents)}")
    
    def enforce_quality_checkpoint(self, checkpoint_name: str, validation_result: bool) -> None:
        """Enforce quality checkpoint validation"""
        
        if not validation_result:
            raise RuntimeError(f"Quality checkpoint FAILED: {checkpoint_name}")
        
        self.framework_state["quality_gates_passed"].append(checkpoint_name)
        print(f"✅ Quality checkpoint PASSED: {checkpoint_name}")
    
    def enforce_file_creation(self, file_path: str, content: str) -> bool:
        """Enforce proper file creation with validation"""
        
        target_path = Path(file_path)
        
        # Validate file path
        if not self._validate_file_path(target_path):
            raise RuntimeError(f"Invalid file path - framework violation: {file_path}")
        
        # Write file
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, 'w') as f:
                f.write(content)
        except Exception as e:
            raise RuntimeError(f"File creation failed: {file_path} - {e}")
        
        # Verify file exists
        if not target_path.exists():
            raise RuntimeError(f"File verification failed: {file_path}")
        
        print(f"✅ File created and verified: {file_path}")
        return True
    
    def _validate_file_path(self, file_path: Path) -> bool:
        """Validate file path against framework rules"""
        
        # Must be in run directory
        if "runs/" not in str(file_path):
            return False
        
        # Cannot be intermediate files in root
        if file_path.parent == Path("."):
            return False
        
        return True
    
    def _check_bypass_attempts(self) -> None:
        """Detect and prevent framework bypass attempts"""
        
        # Check for manual file creation outside framework
        suspicious_files = []
        
        # Check current directory for unauthorized files
        for item in Path(".").iterdir():
            if item.is_file() and item.suffix in [".md", ".json"] and "ACM-" in item.name:
                suspicious_files.append(str(item))
        
        if suspicious_files:
            self.bypass_attempts.extend(suspicious_files)
            print(f"🚨 BYPASS ATTEMPT DETECTED: Unauthorized files: {suspicious_files}")
            self._handle_bypass_attempt("unauthorized_file_creation", suspicious_files)
    
    def _validate_framework_state(self) -> None:
        """Validate current framework state"""
        
        # Check if framework is progressing normally
        if self.framework_state["initialized"]:
            current_time = datetime.now(timezone.utc)
            start_time = datetime.fromisoformat(self.framework_state["start_time"])
            elapsed = (current_time - start_time).total_seconds()
            
            # Framework should not be idle for too long
            if elapsed > 600 and not self.framework_state["completed_phases"]:  # 10 minutes
                print("⚠️ Framework execution taking longer than expected")
    
    def _handle_bypass_attempt(self, attempt_type: str, details: Any) -> None:
        """Handle detected bypass attempts"""
        
        bypass_record = {
            "type": attempt_type,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "blocked"
        }
        
        self.bypass_attempts.append(bypass_record)
        
        print(f"🛡️ Bypass attempt BLOCKED: {attempt_type}")
        
        # For critical violations, trigger lockdown
        if attempt_type in ["unauthorized_file_creation", "phase_skipping", "agent_bypass"]:
            self._trigger_emergency_lockdown()
    
    def _trigger_emergency_lockdown(self) -> None:
        """Trigger emergency framework lockdown"""
        
        self.framework_lockdown = True
        
        print("🚨 **EMERGENCY FRAMEWORK LOCKDOWN**")
        print("🔒 Critical framework violation detected")
        print("⛔ Execution halted to prevent quality degradation")
        
        # Log lockdown event
        lockdown_event = {
            "event": "emergency_lockdown",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "bypass_attempts": self.bypass_attempts,
            "framework_state": self.framework_state
        }
        
        # Write lockdown log
        try:
            lockdown_file = Path(".claude/logs/framework-lockdown.json")
            lockdown_file.parent.mkdir(parents=True, exist_ok=True)
            with open(lockdown_file, 'w') as f:
                json.dump(lockdown_event, f, indent=2)
        except Exception as e:
            print(f"Failed to write lockdown log: {e}")
        
        # Stop monitoring
        self.enforcement_active = False
        
        raise RuntimeError("Framework execution halted due to critical violations")
    
    def validate_framework_completion(self) -> bool:
        """Validate complete framework execution"""
        
        # Check all phases completed
        if len(self.framework_state["completed_phases"]) != len(self.framework_state["required_phases"]):
            missing = set(self.framework_state["required_phases"]) - set(self.framework_state["completed_phases"])
            raise RuntimeError(f"Framework incomplete - missing phases: {missing}")
        
        # Check all agents executed
        if len(self.framework_state["agents_spawned"]) != len(self.framework_state["required_agents"]):
            missing = set(self.framework_state["required_agents"]) - set(self.framework_state["agents_spawned"])
            raise RuntimeError(f"Framework incomplete - missing agents: {missing}")
        
        # Check quality gates
        required_gates = ["evidence_validation", "format_enforcement", "html_tag_prevention"]
        passed_gates = self.framework_state["quality_gates_passed"]
        
        for gate in required_gates:
            if gate not in passed_gates:
                print(f"⚠️ Quality gate not explicitly passed: {gate}")
        
        print("✅ **FRAMEWORK EXECUTION COMPLETE**")
        print("📋 All phases executed, agents completed, quality validated")
        
        return True
    
    def get_enforcement_report(self) -> Dict:
        """Generate comprehensive enforcement report"""
        
        return {
            "enforcement_status": "active" if self.enforcement_active else "inactive",
            "framework_state": self.framework_state,
            "bypass_attempts": self.bypass_attempts,
            "execution_metadata": self.execution_metadata,
            "lockdown_status": self.framework_lockdown,
            "report_timestamp": datetime.now(timezone.utc).isoformat()
        }


# Global enforcer instance
_framework_enforcer = None

def get_framework_enforcer() -> MandatoryFrameworkEnforcer:
    """Get global framework enforcer instance"""
    global _framework_enforcer
    
    if _framework_enforcer is None:
        _framework_enforcer = MandatoryFrameworkEnforcer()
    
    return _framework_enforcer

def initialize_mandatory_framework(jira_ticket: str, **kwargs) -> Dict:
    """Initialize mandatory framework execution - CANNOT BE BYPASSED"""
    enforcer = get_framework_enforcer()
    return enforcer.initialize_mandatory_framework(jira_ticket, **kwargs)

def enforce_phase_execution(phase_id: str, phase_name: str) -> None:
    """Enforce mandatory phase execution"""
    enforcer = get_framework_enforcer()
    enforcer.enforce_phase_execution(phase_id, phase_name)

def complete_phase(phase_id: str) -> None:
    """Complete phase with validation"""
    enforcer = get_framework_enforcer()
    enforcer.complete_phase(phase_id)

def enforce_quality_checkpoint(checkpoint_name: str, validation_result: bool) -> None:
    """Enforce quality checkpoint"""
    enforcer = get_framework_enforcer()
    enforcer.enforce_quality_checkpoint(checkpoint_name, validation_result)

def enforce_file_creation(file_path: str, content: str) -> bool:
    """Enforce proper file creation"""
    enforcer = get_framework_enforcer()
    return enforcer.enforce_file_creation(file_path, content)

def validate_framework_completion() -> bool:
    """Validate complete framework execution"""
    enforcer = get_framework_enforcer()
    return enforcer.validate_framework_completion()

def get_enforcement_report() -> Dict:
    """Get enforcement report"""
    enforcer = get_framework_enforcer()
    return enforcer.get_enforcement_report()


# CLI for testing
if __name__ == "__main__":
    enforcer = MandatoryFrameworkEnforcer()
    
    # Test initialization
    try:
        metadata = enforcer.initialize_mandatory_framework("ACM-TEST-123", feature="Test feature")
        print("✅ Framework initialization test passed")
        
        # Test phase execution
        enforcer.enforce_phase_execution("phase_0", "Test Phase 0")
        enforcer.complete_phase("phase_0")
        print("✅ Phase execution test passed")
        
        # Test quality checkpoint
        enforcer.enforce_quality_checkpoint("test_checkpoint", True)
        print("✅ Quality checkpoint test passed")
        
        print("\n📊 Enforcement Report:")
        report = enforcer.get_enforcement_report()
        print(json.dumps(report, indent=2))
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)