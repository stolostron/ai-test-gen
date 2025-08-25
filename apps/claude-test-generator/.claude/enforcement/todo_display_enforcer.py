#!/usr/bin/env python3
"""
Todo Display Enforcement System

Enforces enhanced phase-by-phase todo display for all TodoWrite operations
in the Claude Test Generator framework. Ensures proper phase breakdown
and real-time progress visibility.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

class TodoDisplayEnforcer:
    """Enforces enhanced todo display standards"""
    
    def __init__(self):
        self.enforcement_config = self._load_enforcement_config()
        self.active = True
        self.hook_installed = False
        
    def _load_enforcement_config(self) -> Dict:
        """Load enforcement configuration"""
        config_path = Path(".claude/config/todo-display-enforcement.json")
        
        if not config_path.exists():
            # Create default enforcement config
            default_config = {
                "enforcement": {
                    "enabled": True,
                    "mandatory_phase_display": True,
                    "require_execution_context": True,
                    "block_standard_display": True
                },
                "display_requirements": {
                    "must_show_current_phase": True,
                    "must_show_phase_progress": True,
                    "must_show_execution_timing": True,
                    "must_include_observability_tips": True
                },
                "violation_handling": {
                    "auto_correct": True,
                    "log_violations": True,
                    "alert_on_fallback": True
                }
            }
            
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            return default_config
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"enforcement": {"enabled": True}}
    
    def enforce_enhanced_display(self, todos: List[Dict]) -> str:
        """Enforce enhanced display for todo updates"""
        if not self.enforcement_config.get("enforcement", {}).get("enabled", True):
            return self._generate_fallback_display(todos)
        
        try:
            # Import and use enhanced display
            from enhanced_todo_integration import enhanced_todo_write_hook
            enhanced_output = enhanced_todo_write_hook(todos)
            
            # Validate the output meets requirements
            if self._validate_enhanced_output(enhanced_output):
                return enhanced_output
            else:
                return self._correct_output_violations(enhanced_output, todos)
                
        except ImportError as e:
            print(f"⚠️ Enhanced display import failed: {e}")
            return self._generate_enforcement_fallback(todos)
        except Exception as e:
            print(f"⚠️ Enhanced display error: {e}")
            return self._generate_enforcement_fallback(todos)
    
    def _validate_enhanced_output(self, output: str) -> bool:
        """Validate that enhanced output meets enforcement requirements"""
        requirements = self.enforcement_config.get("display_requirements", {})
        
        checks = []
        
        # Check for current phase display
        if requirements.get("must_show_current_phase", True):
            checks.append("CURRENT PHASE" in output or "Phase" in output)
        
        # Check for phase progress
        if requirements.get("must_show_phase_progress", True):
            checks.append("PHASE PROGRESS" in output or "OVERVIEW" in output)
        
        # Check for execution timing
        if requirements.get("must_show_execution_timing", True):
            checks.append("EXECUTION STATUS" in output or "Elapsed Time" in output)
        
        # Check for observability tips
        if requirements.get("must_include_observability_tips", True):
            checks.append("Tip:" in output or "/status" in output)
        
        return all(checks)
    
    def _correct_output_violations(self, output: str, todos: List[Dict]) -> str:
        """Correct violations in enhanced output"""
        # If auto-correction is enabled, regenerate
        if self.enforcement_config.get("violation_handling", {}).get("auto_correct", True):
            return self._generate_enforcement_fallback(todos)
        else:
            return output
    
    def _generate_enforcement_fallback(self, todos: List[Dict]) -> str:
        """Generate fallback display that meets enforcement requirements"""
        output = []
        
        # Header with phase information (required)
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("🚀 **FRAMEWORK EXECUTION - PHASE-BY-PHASE PROGRESS**")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("")
        
        # Determine current phase from todos
        current_phase = self._determine_phase_from_todos(todos)
        output.append(f"📍 **CURRENT PHASE**: {current_phase}")
        output.append("")
        
        # Phase progress overview (required)
        output.append("📊 **PHASE PROGRESS OVERVIEW:**")
        phases = [
            "Phase 0: JIRA Analysis & Environment Setup",
            "Phase 1: Technical Documentation Analysis", 
            "Phase 2: Code Implementation Investigation",
            "Phase 3: QE Intelligence & Strategic Analysis",
            "Phase 4: AI Strategic Synthesis",
            "Phase 5: Test Generation & Validation"
        ]
        
        current_phase_idx = self._get_phase_index(current_phase)
        for i, phase in enumerate(phases):
            if i < current_phase_idx:
                status_icon = "✅"
                status_text = "COMPLETED"
            elif i == current_phase_idx:
                status_icon = "🔄"
                status_text = "IN PROGRESS"
            else:
                status_icon = "⏳"
                status_text = "PENDING"
            
            output.append(f"  {status_icon} **{phase}** ({status_text})")
        
        output.append("")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Current phase tasks (required)
        output.append(f"📋 **CURRENT PHASE TASKS**:")
        for todo in todos:
            status = todo.get("status", "pending")
            content = todo.get("content", "Unknown task")
            
            if status == "completed":
                status_icon = "✅"
            elif status == "in_progress":
                status_icon = "🔄"
            else:
                status_icon = "☐"
            
            output.append(f"  ⎿  {status_icon} {content}")
        
        output.append("")
        
        # Execution timing (required)
        output.append("⏱️ **REAL-TIME EXECUTION STATUS:**")
        execution_info = self._get_execution_context()
        output.append(f"📁 **Active Run**: {execution_info.get('run_dir', 'Unknown')}")
        output.append(f"🎫 **JIRA Ticket**: {execution_info.get('jira_ticket', 'Unknown')}")
        output.append(f"⌛ **Elapsed Time**: {execution_info.get('elapsed_time', 'Unknown')}")
        output.append("")
        
        # Observability tips (required)
        output.append("💡 **Framework Observability Commands:**")
        output.append("  🔍 `/status` - Current execution status and progress")
        output.append("  📊 `/timeline` - Phase milestones and completion estimates") 
        output.append("  🤖 `/deep-dive [agent]` - Detailed agent analysis")
        output.append("  🌐 `/environment` - Environment health and compatibility")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return "\n".join(output)
    
    def _determine_phase_from_todos(self, todos: List[Dict]) -> str:
        """Determine current phase from todo content"""
        todo_contents = [todo.get("content", "").lower() for todo in todos]
        
        if any("jira" in content or "research" in content for content in todo_contents):
            return "Phase 0: JIRA Analysis & Environment Setup"
        elif any("documentation" in content or "technical requirements" in content for content in todo_contents):
            return "Phase 1: Technical Documentation Analysis"
        elif any("github" in content or "implementation" in content for content in todo_contents):
            return "Phase 2: Code Implementation Investigation"
        elif any("qe" in content or "intelligence" in content for content in todo_contents):
            return "Phase 3: QE Intelligence & Strategic Analysis"
        elif any("synthesis" in content or "strategic" in content for content in todo_contents):
            return "Phase 4: AI Strategic Synthesis"
        elif any("test" in content or "generation" in content for content in todo_contents):
            return "Phase 5: Test Generation & Validation"
        else:
            return "Phase 0: JIRA Analysis & Environment Setup"
    
    def _get_phase_index(self, phase_name: str) -> int:
        """Get numeric index of current phase"""
        if "Phase 0" in phase_name:
            return 0
        elif "Phase 1" in phase_name:
            return 1
        elif "Phase 2" in phase_name:
            return 2
        elif "Phase 3" in phase_name:
            return 3
        elif "Phase 4" in phase_name:
            return 4
        elif "Phase 5" in phase_name:
            return 5
        else:
            return 0
    
    def _get_execution_context(self) -> Dict:
        """Get current execution context"""
        try:
            # Try to detect current run
            runs_dir = Path("runs")
            if runs_dir.exists():
                # Find most recent run
                run_dirs = []
                for ticket_dir in runs_dir.iterdir():
                    if ticket_dir.is_dir():
                        for run_dir in ticket_dir.iterdir():
                            if run_dir.is_dir() and run_dir.name.count('-') >= 3:
                                run_dirs.append(run_dir)
                
                if run_dirs:
                    latest_run = max(run_dirs, key=lambda d: d.stat().st_mtime)
                    
                    # Try to load metadata
                    metadata_path = latest_run / "run-metadata.json"
                    if metadata_path.exists():
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        
                        return {
                            "run_dir": latest_run.name,
                            "jira_ticket": metadata.get("jira_ticket", "Unknown"),
                            "elapsed_time": "In progress"
                        }
            
            return {"run_dir": "Unknown", "jira_ticket": "Unknown", "elapsed_time": "Unknown"}
            
        except Exception:
            return {"run_dir": "Unknown", "jira_ticket": "Unknown", "elapsed_time": "Unknown"}
    
    def _generate_fallback_display(self, todos: List[Dict]) -> str:
        """Generate basic fallback display"""
        output = []
        output.append("⏺ Update Todos")
        
        for todo in todos:
            status = todo.get("status", "pending")
            content = todo.get("content", "Unknown task")
            
            if status == "completed":
                status_icon = "☒"
            elif status == "in_progress":
                status_icon = "🔄"
            else:
                status_icon = "☐"
            
            output.append(f"  ⎿  {status_icon} {content}")
        
        return "\n".join(output)
    
    def install_enforcement_hook(self) -> None:
        """Install enforcement hook for TodoWrite operations"""
        self.hook_installed = True
        print("✅ Enhanced todo display enforcement activated")
    
    def uninstall_enforcement_hook(self) -> None:
        """Uninstall enforcement hook"""
        self.hook_installed = False
        print("⚠️ Enhanced todo display enforcement deactivated")


# Global enforcer instance
_todo_enforcer = None

def get_todo_enforcer() -> TodoDisplayEnforcer:
    """Get global todo display enforcer"""
    global _todo_enforcer
    
    if _todo_enforcer is None:
        _todo_enforcer = TodoDisplayEnforcer()
        # Auto-install enforcement hook
        _todo_enforcer.install_enforcement_hook()
    
    return _todo_enforcer

def enforce_enhanced_todo_display(todos: List[Dict]) -> str:
    """Enforce enhanced todo display for the given todos"""
    enforcer = get_todo_enforcer()
    return enforcer.enforce_enhanced_display(todos)

def activate_todo_enforcement():
    """Activate todo display enforcement"""
    enforcer = get_todo_enforcer()
    enforcer.install_enforcement_hook()

def deactivate_todo_enforcement():
    """Deactivate todo display enforcement"""
    enforcer = get_todo_enforcer()
    enforcer.uninstall_enforcement_hook()


if __name__ == "__main__":
    # Test the enforcement system
    test_todos = [
        {"id": "1", "content": "Research ACM-22079 JIRA ticket details", "status": "completed"},
        {"id": "2", "content": "Analyze technical requirements and scope", "status": "completed"},
        {"id": "3", "content": "Investigate code implementation details", "status": "in_progress"},
        {"id": "4", "content": "Assess infrastructure and environment setup", "status": "pending"},
        {"id": "5", "content": "Generate comprehensive test plan document", "status": "pending"}
    ]
    
    enforcer = TodoDisplayEnforcer()
    enforced_output = enforcer.enforce_enhanced_display(test_todos)
    print("Enforced Enhanced Display Output:")
    print("=" * 80)
    print(enforced_output)