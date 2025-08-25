#!/usr/bin/env python3
"""
Enhanced Todo Integration System

Automatically integrates with Claude Code's TodoWrite tool to provide
enhanced phase-by-phase progress display during framework execution.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add the observability module to path
sys.path.append(str(Path(__file__).parent.parent / "observability"))

try:
    from enhanced_todo_display import enhanced_todo_display
except ImportError:
    # Fallback if enhanced display isn't available
    def enhanced_todo_display(todos: List[Dict]) -> str:
        return "Enhanced display not available"

class TodoIntegrationService:
    """Service to integrate enhanced display with TodoWrite operations"""
    
    def __init__(self):
        self.config_path = Path(".claude/config/todo-display-config.json")
        self.enabled = self._check_enabled()
        self.display_hook_active = False
        
    def _check_enabled(self) -> bool:
        """Check if enhanced todo display is enabled"""
        if not self.config_path.exists():
            # Create default config
            self._create_default_config()
            return True
            
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get("enhanced_display", {}).get("enabled", True)
        except (json.JSONDecodeError, FileNotFoundError):
            return True
    
    def _create_default_config(self) -> None:
        """Create default configuration for enhanced todo display"""
        config = {
            "enhanced_display": {
                "enabled": True,
                "show_phase_progress": True,
                "show_execution_timing": True,
                "show_agent_status": True,
                "real_time_updates": True
            },
            "terminal_display": {
                "use_enhanced_format": True,
                "show_phase_header": True,
                "include_observability_tips": True
            }
        }
        
        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def process_todo_update(self, todos: List[Dict]) -> str:
        """Process todo update and return enhanced display if enabled"""
        if not self.enabled:
            return self._format_standard_display(todos)
        
        try:
            # Generate enhanced display
            enhanced_output = enhanced_todo_display(todos)
            
            # Also trigger observability update
            self._update_observability_state(todos)
            
            return enhanced_output
            
        except Exception as e:
            # Fallback to standard display on error
            print(f"⚠️ Enhanced display error: {e}")
            return self._format_standard_display(todos)
    
    def _format_standard_display(self, todos: List[Dict]) -> str:
        """Format standard todo display as fallback"""
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
    
    def _update_observability_state(self, todos: List[Dict]) -> None:
        """Update observability state based on todo changes"""
        try:
            # Import observability integration
            from framework_integration import update_observability_metadata
            
            # Determine current phase from todos
            phase_info = self._analyze_phase_from_todos(todos)
            
            # Update observability with current state
            metadata_update = {
                "current_todos": todos,
                "current_phase": phase_info["phase"],
                "phase_status": phase_info["status"],
                "todo_summary": {
                    "total": len(todos),
                    "completed": len([t for t in todos if t.get("status") == "completed"]),
                    "in_progress": len([t for t in todos if t.get("status") == "in_progress"]),
                    "pending": len([t for t in todos if t.get("status") == "pending"])
                }
            }
            
            update_observability_metadata(metadata_update)
            
        except ImportError:
            # Observability not available, continue without it
            pass
        except Exception as e:
            # Don't fail todo updates due to observability issues
            print(f"⚠️ Observability update failed: {e}")
    
    def _analyze_phase_from_todos(self, todos: List[Dict]) -> Dict:
        """Analyze current phase and status from todo content"""
        todo_contents = [todo.get("content", "").lower() for todo in todos]
        
        # Phase detection logic
        phase = "Phase 0"
        if any("jira" in content or "research" in content for content in todo_contents):
            phase = "Phase 0: JIRA Analysis"
        elif any("documentation" in content or "technical requirements" in content for content in todo_contents):
            phase = "Phase 1: Documentation Analysis"
        elif any("github" in content or "implementation" in content for content in todo_contents):
            phase = "Phase 2: Code Investigation"
        elif any("qe" in content or "intelligence" in content for content in todo_contents):
            phase = "Phase 3: QE Intelligence"
        elif any("synthesis" in content or "strategic" in content for content in todo_contents):
            phase = "Phase 4: Strategic Synthesis"
        elif any("test" in content or "generation" in content for content in todo_contents):
            phase = "Phase 5: Test Generation"
        
        # Status detection
        has_in_progress = any(todo.get("status") == "in_progress" for todo in todos)
        all_completed = all(todo.get("status") == "completed" for todo in todos)
        
        if has_in_progress:
            status = "in_progress"
        elif all_completed:
            status = "completed"
        else:
            status = "pending"
        
        return {"phase": phase, "status": status}
    
    def enable_enhanced_display(self) -> None:
        """Enable enhanced todo display"""
        self.enabled = True
        config = self._load_config()
        config["enhanced_display"]["enabled"] = True
        self._save_config(config)
        print("✅ Enhanced todo display enabled")
    
    def disable_enhanced_display(self) -> None:
        """Disable enhanced todo display"""
        self.enabled = False
        config = self._load_config()
        config["enhanced_display"]["enabled"] = False
        self._save_config(config)
        print("⚠️ Enhanced todo display disabled")
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        if not self.config_path.exists():
            self._create_default_config()
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def _save_config(self, config: Dict) -> None:
        """Save configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)


# Global integration service
_integration_service = None

def get_todo_integration_service() -> TodoIntegrationService:
    """Get global todo integration service"""
    global _integration_service
    
    if _integration_service is None:
        _integration_service = TodoIntegrationService()
    
    return _integration_service

def enhanced_todo_write_hook(todos: List[Dict]) -> str:
    """Hook function for enhanced TodoWrite display"""
    service = get_todo_integration_service()
    return service.process_todo_update(todos)

def enable_enhanced_todos():
    """Enable enhanced todo display"""
    service = get_todo_integration_service()
    service.enable_enhanced_display()

def disable_enhanced_todos():
    """Disable enhanced todo display"""
    service = get_todo_integration_service()
    service.disable_enhanced_display()


if __name__ == "__main__":
    # Test the integration system
    test_todos = [
        {"id": "1", "content": "Research ACM-22079 JIRA ticket details", "status": "completed"},
        {"id": "2", "content": "Analyze technical requirements and scope", "status": "in_progress"},
        {"id": "3", "content": "Investigate code implementation details", "status": "pending"},
        {"id": "4", "content": "Assess infrastructure and environment setup", "status": "pending"},
        {"id": "5", "content": "Generate comprehensive test plan document", "status": "pending"}
    ]
    
    service = TodoIntegrationService()
    enhanced_output = service.process_todo_update(test_todos)
    print("Enhanced Todo Display Output:")
    print("=" * 60)
    print(enhanced_output)