#!/usr/bin/env python3
"""
Claude Test Generator - Framework Integration for Observability

Integration layer that enables real-time observability during framework execution.
Provides seamless integration with existing multi-agent architecture.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from observability_command_handler import ObservabilityCommandHandler

class FrameworkObservabilityIntegration:
    """Integration layer for real-time framework observability"""
    
    def __init__(self, run_directory: str = None):
        self.handler = ObservabilityCommandHandler(run_directory)
        self.is_enabled = self._check_enabled()
        self.integration_hooks = {}
        self._setup_integration_hooks()
        
    def _check_enabled(self) -> bool:
        """Check if observability is enabled in configuration"""
        config = self.handler.config
        return config.get("observability_agent", {}).get("enabled", True)
    
    def _setup_integration_hooks(self) -> None:
        """Setup integration hooks for framework events"""
        self.integration_hooks = {
            "framework_start": self.on_framework_start,
            "phase_transition": self.on_phase_transition,
            "agent_spawn": self.on_agent_spawn,
            "agent_completion": self.on_agent_completion,
            "context_inheritance": self.on_context_inheritance,
            "validation_checkpoint": self.on_validation_checkpoint,
            "framework_completion": self.on_framework_completion,
            "error_event": self.on_error_event
        }
    
    # Framework Event Handlers
    
    def on_framework_start(self, jira_ticket: str, feature: str, **kwargs) -> None:
        """Handle framework initialization"""
        if not self.is_enabled:
            return
            
        start_data = {
            "framework_state": {
                "current_phase": "initializing",
                "start_time": datetime.now(timezone.utc).isoformat(),
                "completion_percentage": 0
            },
            "run_metadata": {
                "jira_ticket": jira_ticket,
                "feature": feature,
                "start_timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
        
        # Add any additional metadata
        for key, value in kwargs.items():
            start_data["run_metadata"][key] = value
            
        self.handler.update_state(start_data)
        
        print(f"🔍 **Observability Agent**: Framework monitoring initialized for {jira_ticket}")
        print("💡 **Tip**: Use commands like `/status`, `/business`, `/technical` for real-time insights")
    
    def on_phase_transition(self, phase: str, status: str = "in_progress", **kwargs) -> None:
        """Handle phase transitions"""
        if not self.is_enabled:
            return
            
        phase_data = {
            "framework_state": {
                "current_phase": phase,
                "last_update": datetime.now(timezone.utc).isoformat()
            }
        }
        
        # Add phase-specific data
        if kwargs:
            phase_data["phase_data"] = {phase: kwargs}
            
        self.handler.update_state(phase_data)
        
        if status == "completed":
            print(f"✅ **Phase {phase}**: Completed - Data available via `/status` command")
        elif status == "in_progress":
            print(f"🔄 **Phase {phase}**: Started - Monitor progress with `/timeline`")
    
    def on_agent_spawn(self, agent_type: str, inherited_context: Dict = None, **kwargs) -> None:
        """Handle agent spawning"""
        if not self.is_enabled:
            return
            
        agent_data = {
            "agent_coordination": {
                "active_agents": [agent_type],
                "last_spawn": {
                    "agent": agent_type,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "inherited_context_size": len(str(inherited_context)) if inherited_context else 0
                }
            }
        }
        
        self.handler.update_state(agent_data)
        
        print(f"🚀 **Agent {agent_type.upper()}**: Spawned - Use `/deep-dive {agent_type}` for detailed analysis")
    
    def on_agent_completion(self, agent_type: str, results: Dict = None, context_contribution: Dict = None, **kwargs) -> None:
        """Handle agent completion"""
        if not self.is_enabled:
            return
            
        completion_data = {
            "agent_coordination": {
                "completed_agents": [agent_type],
                "last_completion": {
                    "agent": agent_type,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "results_size": len(str(results)) if results else 0,
                    "context_contribution_size": len(str(context_contribution)) if context_contribution else 0
                }
            }
        }
        
        # Remove from active agents
        current_active = self.handler.state.get("agent_coordination", {}).get("active_agents", [])
        if agent_type in current_active:
            current_active.remove(agent_type)
            completion_data["agent_coordination"]["active_agents"] = current_active
            
        self.handler.update_state(completion_data)
        
        print(f"✅ **Agent {agent_type.upper()}**: Completed - Results available via `/deep-dive {agent_type}`")
    
    def on_context_inheritance(self, source_agent: str, target_agent: str, context_data: Dict, validation_status: str = "passed", **kwargs) -> None:
        """Handle context inheritance between agents"""
        if not self.is_enabled:
            return
            
        inheritance_data = {
            "context_inheritance": {
                "last_inheritance": {
                    "source": source_agent,
                    "target": target_agent,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "context_size": len(str(context_data)),
                    "validation_status": validation_status
                }
            },
            "agent_coordination": {
                "context_chain_status": f"{source_agent} → {target_agent} (validated)"
            }
        }
        
        self.handler.update_state(inheritance_data)
        
        if validation_status == "passed":
            print(f"📥 **Context Flow**: {source_agent} → {target_agent} validated - View with `/context-flow`")
        else:
            print(f"⚠️ **Context Conflict**: {source_agent} → {target_agent} validation issues - Check `/risks`")
    
    def on_validation_checkpoint(self, checkpoint_type: str, status: str, details: Dict = None, **kwargs) -> None:
        """Handle validation checkpoints"""
        if not self.is_enabled:
            return
            
        validation_data = {
            "validation_status": {
                checkpoint_type: status
            },
            "last_validation": {
                "checkpoint": checkpoint_type,
                "status": status,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "details": details or {}
            }
        }
        
        self.handler.update_state(validation_data)
        
        if status == "passed":
            print(f"✅ **Validation**: {checkpoint_type.replace('_', ' ').title()} passed")
        elif status == "failed":
            print(f"❌ **Validation**: {checkpoint_type.replace('_', ' ').title()} failed - Check `/validation-status`")
    
    def on_framework_completion(self, run_directory: str, deliverables: List[str], quality_metrics: Dict = None, **kwargs) -> None:
        """Handle framework completion"""
        if not self.is_enabled:
            return
            
        completion_data = {
            "framework_state": {
                "current_phase": "completed",
                "completion_time": datetime.now(timezone.utc).isoformat(),
                "completion_percentage": 100
            },
            "completion_summary": {
                "run_directory": run_directory,
                "deliverables": deliverables,
                "quality_metrics": quality_metrics or {},
                "total_execution_time": self._calculate_total_time()
            }
        }
        
        self.handler.update_state(completion_data)
        
        print("🎉 **Framework Complete**: All phases finished successfully")
        print(f"📁 **Deliverables**: {len(deliverables)} files generated in {run_directory}")
        print("📊 **Final Summary**: Use `/performance` for execution metrics")
    
    def on_error_event(self, error_type: str, error_message: str, phase: str = None, agent: str = None, **kwargs) -> None:
        """Handle error events"""
        if not self.is_enabled:
            return
            
        error_data = {
            "error_events": [{
                "type": error_type,
                "message": error_message,
                "phase": phase,
                "agent": agent,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }],
            "risk_alerts": [{
                "level": "error",
                "message": f"{error_type}: {error_message}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }]
        }
        
        self.handler.update_state(error_data)
        
        print(f"🚨 **Error Detected**: {error_type} - Use `/risks` for details and mitigation")
    
    # User Command Interface
    
    def process_user_command(self, command: str) -> str:
        """Process user observability command"""
        if not self.is_enabled:
            return "⚠️ Observability agent is disabled. Enable in .claude/config/observability-config.json"
        
        return self.handler.process_command(command)
    
    # Utility Methods
    
    def _calculate_total_time(self) -> str:
        """Calculate total execution time"""
        start_time = self.handler.state.get("framework_state", {}).get("start_time", "")
        if not start_time:
            return "unknown"
            
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            current_dt = datetime.now(timezone.utc)
            elapsed = current_dt - start_dt
            
            total_seconds = elapsed.total_seconds()
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            
            if minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        except ValueError:
            return "unknown"
    
    def get_current_status(self) -> Dict:
        """Get current framework status for external monitoring"""
        if not self.is_enabled:
            return {"status": "disabled"}
            
        return {
            "status": "enabled",
            "current_phase": self.handler.state.get("framework_state", {}).get("current_phase", "unknown"),
            "completion_percentage": self.handler.state.get("framework_state", {}).get("completion_percentage", 0),
            "active_agents": self.handler.state.get("agent_coordination", {}).get("active_agents", []),
            "last_update": datetime.now(timezone.utc).isoformat()
        }
    
    def update_run_metadata(self, metadata_updates: Dict) -> None:
        """Update run metadata with new information"""
        if not self.is_enabled:
            return
            
        update_data = {"run_metadata": metadata_updates}
        self.handler.update_state(update_data)


# Global instance for framework integration
_observability_integration = None

def get_observability_integration(run_directory: str = None) -> FrameworkObservabilityIntegration:
    """Get global observability integration instance"""
    global _observability_integration
    
    if _observability_integration is None:
        _observability_integration = FrameworkObservabilityIntegration(run_directory)
    
    return _observability_integration

def init_observability(jira_ticket: str, feature: str, **kwargs) -> None:
    """Initialize observability for framework run"""
    integration = get_observability_integration()
    integration.on_framework_start(jira_ticket, feature, **kwargs)

def observe_phase_transition(phase: str, status: str = "in_progress", **kwargs) -> None:
    """Notify observability of phase transition"""
    integration = get_observability_integration()
    integration.on_phase_transition(phase, status, **kwargs)

def observe_agent_spawn(agent_type: str, inherited_context: Dict = None, **kwargs) -> None:
    """Notify observability of agent spawn"""
    integration = get_observability_integration()
    integration.on_agent_spawn(agent_type, inherited_context, **kwargs)

def observe_agent_completion(agent_type: str, results: Dict = None, context_contribution: Dict = None, **kwargs) -> None:
    """Notify observability of agent completion"""
    integration = get_observability_integration()
    integration.on_agent_completion(agent_type, results, context_contribution, **kwargs)

def observe_context_inheritance(source_agent: str, target_agent: str, context_data: Dict, validation_status: str = "passed", **kwargs) -> None:
    """Notify observability of context inheritance"""
    integration = get_observability_integration()
    integration.on_context_inheritance(source_agent, target_agent, context_data, validation_status, **kwargs)

def observe_validation_checkpoint(checkpoint_type: str, status: str, details: Dict = None, **kwargs) -> None:
    """Notify observability of validation checkpoint"""
    integration = get_observability_integration()
    integration.on_validation_checkpoint(checkpoint_type, status, details, **kwargs)

def observe_framework_completion(run_directory: str, deliverables: List[str], quality_metrics: Dict = None, **kwargs) -> None:
    """Notify observability of framework completion"""
    integration = get_observability_integration()
    integration.on_framework_completion(run_directory, deliverables, quality_metrics, **kwargs)

def observe_error(error_type: str, error_message: str, phase: str = None, agent: str = None, **kwargs) -> None:
    """Notify observability of error events"""
    integration = get_observability_integration()
    integration.on_error_event(error_type, error_message, phase, agent, **kwargs)

def process_observability_command(command: str) -> str:
    """Process user observability command"""
    integration = get_observability_integration()
    return integration.process_user_command(command)

def update_observability_metadata(metadata_updates: Dict) -> None:
    """Update observability metadata"""
    integration = get_observability_integration()
    integration.update_run_metadata(metadata_updates)