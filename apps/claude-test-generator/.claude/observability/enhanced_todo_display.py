#!/usr/bin/env python3
"""
Enhanced Todo Display System with Phase-by-Phase Progress

Provides real-time phase breakdown display that shows current execution phase
prominently and tracks progress through the 6-phase workflow system.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

class EnhancedTodoDisplay:
    """Enhanced todo display with phase-by-phase progress tracking"""
    
    def __init__(self):
        self.current_run_dir = self._detect_current_run()
        self.phases = self._define_phases()
        self.current_phase = "Phase 0: JIRA Analysis"
        self.phase_progress = {}
        
    def _detect_current_run(self) -> Optional[str]:
        """Detect the currently active run directory"""
        runs_dir = Path("runs")
        if not runs_dir.exists():
            return None
            
        # Find most recent run directory by checking latest symlinks
        for ticket_dir in runs_dir.iterdir():
            if ticket_dir.is_dir():
                latest_link = ticket_dir / "latest"
                if latest_link.exists() and latest_link.is_symlink():
                    return str(latest_link.resolve())
        
        # Fallback to most recent timestamp
        run_dirs = []
        for ticket_dir in runs_dir.iterdir():
            if ticket_dir.is_dir():
                for run_dir in ticket_dir.iterdir():
                    if run_dir.is_dir() and run_dir.name.count('-') >= 3:
                        run_dirs.append(run_dir)
        
        if run_dirs:
            latest_run = max(run_dirs, key=lambda d: d.stat().st_mtime)
            return str(latest_run)
        
        return None
    
    def _define_phases(self) -> Dict:
        """Define the 6-phase framework workflow"""
        return {
            "Phase 0": {
                "name": "JIRA Analysis & Environment Setup",
                "description": "Requirements gathering and environment validation",
                "agents": ["Agent A (JIRA Intelligence)", "Agent D (Environment Intelligence)"],
                "key_outputs": ["Business context", "Environment health", "Version compatibility"]
            },
            "Phase 1": {
                "name": "Technical Documentation Analysis", 
                "description": "Feature understanding through documentation",
                "agents": ["Agent B (Documentation Intelligence)"],
                "key_outputs": ["Technical workflows", "API specifications", "UI patterns"]
            },
            "Phase 2": {
                "name": "Code Implementation Investigation",
                "description": "GitHub code analysis and implementation details",
                "agents": ["Agent C (GitHub Investigation)"],
                "key_outputs": ["Implementation changes", "Testing requirements", "Integration points"]
            },
            "Phase 3": {
                "name": "QE Intelligence & Strategic Analysis",
                "description": "Testing pattern analysis and strategy optimization",
                "agents": ["QE Intelligence Service"],
                "key_outputs": ["Testing patterns", "Coverage analysis", "Strategy recommendations"]
            },
            "Phase 4": {
                "name": "AI Strategic Synthesis",
                "description": "Cross-agent synthesis and test planning",
                "agents": ["Strategic Analysis Engine"],
                "key_outputs": ["Comprehensive understanding", "Test strategy", "Risk assessment"]
            },
            "Phase 5": {
                "name": "Test Generation & Validation",
                "description": "Test case generation with technical validation",
                "agents": ["Test Generation Engine", "Validation Services"],
                "key_outputs": ["Test cases", "Technical validation", "Quality metrics"]
            }
        }
    
    def update_phase_progress(self, phase_id: str, status: str, details: Dict = None):
        """Update progress for a specific phase"""
        self.phase_progress[phase_id] = {
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details or {}
        }
        
        # Update current phase based on what's in progress
        for phase_key in self.phases.keys():
            if self.phase_progress.get(phase_key, {}).get("status") == "in_progress":
                self.current_phase = phase_key
                break
    
    def format_phase_display(self, todos: List[Dict]) -> str:
        """Format enhanced phase-by-phase display"""
        output = []
        
        # Header with current phase prominently displayed
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append(f"🚀 **CURRENT PHASE**: {self.current_phase}")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("")
        
        # Show phase progress overview
        output.append("📊 **PHASE PROGRESS OVERVIEW:**")
        for phase_id, phase_info in self.phases.items():
            phase_status = self.phase_progress.get(phase_id, {}).get("status", "pending")
            
            if phase_status == "completed":
                status_icon = "✅"
                status_text = "COMPLETED"
            elif phase_status == "in_progress":
                status_icon = "🔄"
                status_text = "IN PROGRESS"
            elif phase_status == "failed":
                status_icon = "❌"
                status_text = "FAILED"
            else:
                status_icon = "⏳"
                status_text = "PENDING"
            
            output.append(f"  {status_icon} **{phase_id}**: {phase_info['name']} ({status_text})")
        
        output.append("")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Current phase details
        current_phase_info = self.phases.get(self.current_phase.split(':')[0], {})
        if current_phase_info:
            output.append(f"🎯 **ACTIVE PHASE DETAILS**: {current_phase_info['name']}")
            output.append(f"📋 **Description**: {current_phase_info['description']}")
            output.append(f"🤖 **Active Agents**: {', '.join(current_phase_info['agents'])}")
            output.append(f"📊 **Expected Outputs**: {', '.join(current_phase_info['key_outputs'])}")
            output.append("")
        
        # Task breakdown for current phase
        if todos:
            output.append("📋 **CURRENT PHASE TASKS:**")
            for todo in todos:
                status = todo.get("status", "pending")
                content = todo.get("content", "Unknown task")
                
                if status == "completed":
                    status_icon = "✅"
                elif status == "in_progress":
                    status_icon = "🔄"
                else:
                    status_icon = "☐"
                
                output.append(f"  {status_icon} {content}")
            
            output.append("")
        
        # Real-time execution info
        output.append("⏱️ **REAL-TIME EXECUTION STATUS:**")
        
        # Load current run metadata if available
        execution_info = self._get_execution_info()
        if execution_info:
            output.append(f"📁 **Run Directory**: {execution_info.get('run_directory', 'Unknown')}")
            output.append(f"🎫 **JIRA Ticket**: {execution_info.get('jira_ticket', 'Unknown')}")
            output.append(f"⏰ **Started**: {execution_info.get('start_time', 'Unknown')}")
            
            # Calculate elapsed time
            elapsed = self._calculate_elapsed_time(execution_info.get('start_time'))
            if elapsed:
                output.append(f"⌛ **Elapsed Time**: {elapsed}")
        
        output.append("")
        output.append("💡 **Tip**: Use `/status`, `/timeline`, `/deep-dive [agent]` for detailed insights")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return "\n".join(output)
    
    def _get_execution_info(self) -> Dict:
        """Get current execution information from run metadata"""
        if not self.current_run_dir:
            return {}
        
        metadata_path = Path(self.current_run_dir) / "run-metadata.json"
        if not metadata_path.exists():
            return {}
        
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                
            return {
                "run_directory": str(Path(self.current_run_dir).name),
                "jira_ticket": metadata.get("jira_ticket", "Unknown"),
                "start_time": metadata.get("start_timestamp", "Unknown"),
                "feature": metadata.get("feature", "Unknown")
            }
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            return {}
    
    def _calculate_elapsed_time(self, start_time_str: str) -> Optional[str]:
        """Calculate elapsed time from start"""
        if not start_time_str or start_time_str == "Unknown":
            return None
        
        try:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            elapsed = datetime.now(timezone.utc) - start_time
            
            total_seconds = int(elapsed.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            
            if minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        except (ValueError, TypeError):
            return None
    
    def detect_current_phase_from_todos(self, todos: List[Dict]) -> str:
        """Detect current phase based on todo content"""
        # Analyze todo content to determine phase
        todo_contents = [todo.get("content", "").lower() for todo in todos]
        
        # Phase detection logic based on todo patterns
        if any("jira" in content or "research" in content for content in todo_contents):
            return "Phase 0"
        elif any("documentation" in content or "technical" in content for content in todo_contents):
            return "Phase 1"
        elif any("github" in content or "implementation" in content for content in todo_contents):
            return "Phase 2"
        elif any("qe" in content or "intelligence" in content for content in todo_contents):
            return "Phase 3"
        elif any("synthesis" in content or "strategic" in content for content in todo_contents):
            return "Phase 4"
        elif any("test" in content or "generation" in content for content in todo_contents):
            return "Phase 5"
        else:
            return "Phase 0"  # Default to initial phase


# Integration function for TodoWrite enhancement
def enhanced_todo_display(todos: List[Dict]) -> str:
    """Create enhanced todo display with phase information"""
    display = EnhancedTodoDisplay()
    
    # Detect current phase from todos
    current_phase = display.detect_current_phase_from_todos(todos)
    display.current_phase = current_phase
    
    # Update phase progress based on todo status
    in_progress_todos = [t for t in todos if t.get("status") == "in_progress"]
    completed_todos = [t for t in todos if t.get("status") == "completed"]
    
    if in_progress_todos:
        display.update_phase_progress(current_phase, "in_progress")
    elif completed_todos and not in_progress_todos:
        # All todos completed, phase is done
        display.update_phase_progress(current_phase, "completed")
    
    return display.format_phase_display(todos)


if __name__ == "__main__":
    # Test the enhanced display
    test_todos = [
        {"id": "1", "content": "Research ACM-22079 JIRA ticket details", "status": "completed"},
        {"id": "2", "content": "Analyze technical requirements and scope", "status": "completed"},
        {"id": "3", "content": "Investigate code implementation details", "status": "in_progress"},
        {"id": "4", "content": "Assess infrastructure and environment setup", "status": "pending"},
        {"id": "5", "content": "Generate comprehensive test plan document", "status": "pending"}
    ]
    
    display = enhanced_todo_display(test_todos)
    print(display)