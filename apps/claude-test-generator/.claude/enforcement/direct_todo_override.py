#!/usr/bin/env python3
"""
Direct TodoWrite Override System

Directly overrides Claude Code's TodoWrite display to show enhanced
phase-by-phase progress in the terminal during framework execution.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

class DirectTodoOverride:
    """Direct override system for TodoWrite display"""
    
    def __init__(self):
        self.override_active = True
        self.phase_mapping = {
            "research": "Phase 0: JIRA Analysis",
            "jira": "Phase 0: JIRA Analysis", 
            "analyze": "Phase 1: Technical Analysis",
            "technical": "Phase 1: Technical Analysis",
            "investigate": "Phase 2: Code Investigation",
            "implementation": "Phase 2: Code Investigation",
            "github": "Phase 2: Code Investigation",
            "assess": "Phase 0: Environment Assessment",
            "infrastructure": "Phase 0: Environment Assessment",
            "environment": "Phase 0: Environment Assessment",
            "generate": "Phase 5: Test Generation",
            "test": "Phase 5: Test Generation",
            "plan": "Phase 5: Test Generation"
        }
    
    def override_todo_display(self, todos):
        """Override TodoWrite display with enhanced format"""
        if not self.override_active:
            return self._standard_display(todos)
        
        # Generate enhanced display
        output = []
        
        # Main header
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("🚀 **CLAUDE TEST GENERATOR - PHASE EXECUTION**")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("")
        
        # Determine current phase
        current_phase = self._detect_phase_from_todos(todos)
        output.append(f"📍 **CURRENT PHASE**: {current_phase}")
        output.append("")
        
        # Phase progress overview
        output.append("📊 **6-PHASE EXECUTION PROGRESS:**")
        phases = [
            ("Phase 0", "JIRA Analysis & Environment Setup"),
            ("Phase 1", "Technical Documentation Analysis"),
            ("Phase 2", "Code Implementation Investigation"),
            ("Phase 3", "QE Intelligence & Strategic Analysis"),
            ("Phase 4", "AI Strategic Synthesis"),
            ("Phase 5", "Test Generation & Validation")
        ]
        
        current_idx = self._get_phase_index(current_phase)
        for i, (phase_id, phase_name) in enumerate(phases):
            if i < current_idx:
                status = "✅ COMPLETED"
            elif i == current_idx:
                status = "🔄 IN PROGRESS"
            else:
                status = "⏳ PENDING"
            
            output.append(f"  {status} **{phase_id}**: {phase_name}")
        
        output.append("")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Active phase details
        phase_details = self._get_phase_details(current_phase)
        if phase_details:
            output.append(f"🎯 **ACTIVE PHASE**: {phase_details['name']}")
            output.append(f"📋 **Mission**: {phase_details['description']}")
            output.append(f"🤖 **Agents**: {', '.join(phase_details['agents'])}")
            output.append("")
        
        # Current tasks
        output.append("📋 **CURRENT TASKS PROGRESS:**")
        for todo in todos:
            status = todo.get("status", "pending")
            content = todo.get("content", "Unknown task")
            
            if status == "completed":
                icon = "✅"
                status_text = "DONE"
            elif status == "in_progress":
                icon = "🔄"
                status_text = "ACTIVE"
            else:
                icon = "☐"
                status_text = "PENDING"
            
            output.append(f"  {icon} {content} ({status_text})")
        
        output.append("")
        
        # Execution context
        context = self._get_execution_context()
        output.append("⏱️ **EXECUTION CONTEXT:**")
        output.append(f"🎫 **JIRA Ticket**: {context.get('jira_ticket', 'ACM-22079')}")
        output.append(f"📁 **Run Directory**: {context.get('run_dir', 'Current execution')}")
        output.append(f"⌛ **Status**: {context.get('status', 'Framework executing')}")
        output.append("")
        
        # Framework observability
        output.append("🔍 **REAL-TIME FRAMEWORK INSIGHTS:**")
        output.append("  📊 `/status` - Complete execution status and agent progress")
        output.append("  🕐 `/timeline` - Phase milestones and completion estimates")
        output.append("  🤖 `/deep-dive [agent]` - Detailed agent analysis and results")
        output.append("  🌐 `/environment` - Environment health and readiness")
        output.append("  🏢 `/business` - Customer impact and business context")
        output.append("  🔧 `/technical` - Implementation details and strategy")
        output.append("")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return "\n".join(output)
    
    def _detect_phase_from_todos(self, todos):
        """Detect current phase from todo content"""
        todo_texts = [todo.get("content", "").lower() for todo in todos]
        
        # Check for phase indicators in todo content
        for todo_text in todo_texts:
            for keyword, phase in self.phase_mapping.items():
                if keyword in todo_text:
                    return phase
        
        # Default phase detection based on todo progression
        completed_count = len([t for t in todos if t.get("status") == "completed"])
        
        if completed_count == 0:
            return "Phase 0: JIRA Analysis"
        elif completed_count <= 2:
            return "Phase 0: Environment Assessment"
        elif completed_count <= 3:
            return "Phase 2: Code Investigation"
        elif completed_count <= 4:
            return "Phase 3: QE Intelligence"
        else:
            return "Phase 5: Test Generation"
    
    def _get_phase_index(self, phase_name):
        """Get numeric index of phase"""
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
        return 0
    
    def _get_phase_details(self, phase_name):
        """Get detailed information about current phase"""
        phase_info = {
            "Phase 0": {
                "name": "JIRA Analysis & Environment Setup",
                "description": "Extract requirements and validate environment readiness",
                "agents": ["Agent A (JIRA Intelligence)", "Agent D (Environment Intelligence)"]
            },
            "Phase 1": {
                "name": "Technical Documentation Analysis",
                "description": "Deep feature understanding through documentation",
                "agents": ["Agent B (Documentation Intelligence)"]
            },
            "Phase 2": {
                "name": "Code Implementation Investigation", 
                "description": "GitHub analysis and implementation validation",
                "agents": ["Agent C (GitHub Investigation)"]
            },
            "Phase 3": {
                "name": "QE Intelligence & Strategic Analysis",
                "description": "Testing pattern analysis and optimization",
                "agents": ["QE Intelligence Service"]
            },
            "Phase 4": {
                "name": "AI Strategic Synthesis",
                "description": "Cross-agent synthesis and strategic planning",
                "agents": ["Strategic Analysis Engine"]
            },
            "Phase 5": {
                "name": "Test Generation & Validation",
                "description": "Comprehensive test case generation",
                "agents": ["Test Generation Engine", "Validation Services"]
            }
        }
        
        for phase_key, details in phase_info.items():
            if phase_key in phase_name:
                return details
        
        return None
    
    def _get_execution_context(self):
        """Get current execution context"""
        try:
            # Try to find current run
            runs_dir = Path("runs")
            if runs_dir.exists():
                # Look for latest ACM ticket run
                for ticket_dir in runs_dir.iterdir():
                    if ticket_dir.is_dir() and "ACM-" in ticket_dir.name:
                        latest_link = ticket_dir / "latest"
                        if latest_link.exists():
                            return {
                                "jira_ticket": ticket_dir.name,
                                "run_dir": "Active run",
                                "status": "Framework executing"
                            }
            
            return {
                "jira_ticket": "ACM-22079",
                "run_dir": "Current execution", 
                "status": "Framework active"
            }
            
        except Exception:
            return {
                "jira_ticket": "Current ticket",
                "run_dir": "Active",
                "status": "In progress"
            }
    
    def _standard_display(self, todos):
        """Fallback standard display"""
        output = ["⏺ Update Todos"]
        for todo in todos:
            status = todo.get("status", "pending")
            content = todo.get("content", "Unknown task")
            
            if status == "completed":
                icon = "☒"
            elif status == "in_progress":
                icon = "🔄"
            else:
                icon = "☐"
            
            output.append(f"  ⎿  {icon} {content}")
        
        return "\n".join(output)


# Global override instance
_override_system = DirectTodoOverride()

def enhanced_todo_display_override(todos):
    """Main override function for TodoWrite display"""
    return _override_system.override_todo_display(todos)

def activate_override():
    """Activate the display override"""
    global _override_system
    _override_system.override_active = True
    print("✅ Enhanced todo display override activated")

def deactivate_override():
    """Deactivate the display override"""
    global _override_system
    _override_system.override_active = False
    print("⚠️ Enhanced todo display override deactivated")


if __name__ == "__main__":
    # Test the override system
    test_todos = [
        {"id": "1", "content": "Investigate current todo display framework", "status": "completed"},
        {"id": "2", "content": "Analyze observability command handler", "status": "completed"},
        {"id": "3", "content": "Enhance phase-based progress display", "status": "completed"},
        {"id": "4", "content": "Implement real-time phase breakdown", "status": "completed"},
        {"id": "5", "content": "Test and validate enhanced framework", "status": "in_progress"}
    ]
    
    override_system = DirectTodoOverride()
    result = override_system.override_todo_display(test_todos)
    print(result)