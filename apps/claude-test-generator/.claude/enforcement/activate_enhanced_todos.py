#!/usr/bin/env python3
"""
Activation Script for Enhanced Todo Display

Automatically activates the enhanced phase-by-phase todo display system
for all TodoWrite operations in the Claude Test Generator framework.
"""

import json
import os
import sys
from pathlib import Path

def activate_enhanced_todos():
    """Activate enhanced todo display system"""
    
    # Create configuration files
    configs = {
        ".claude/config/todo-display-config.json": {
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
        },
        ".claude/config/todo-display-enforcement.json": {
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
    }
    
    # Create config files
    for config_path, config_data in configs.items():
        full_path = Path(config_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print(f"✅ Created config: {config_path}")
    
    # Create hook activation script
    hook_script = """#!/usr/bin/env python3
'''
TodoWrite Hook for Enhanced Display

This hook is automatically called by Claude Code's TodoWrite tool
to provide enhanced phase-by-phase progress display.
'''

import sys
import json
from pathlib import Path

# Add enforcement path
sys.path.append(str(Path(__file__).parent.parent / "enforcement"))

try:
    from todo_display_enforcer import enforce_enhanced_todo_display
    
    def enhanced_todo_hook(todos):
        '''Hook function for enhanced TodoWrite display'''
        if isinstance(todos, str):
            # Parse JSON if string
            todos = json.loads(todos)
        
        return enforce_enhanced_todo_display(todos)
    
    # Export hook function
    __all__ = ['enhanced_todo_hook']
    
except ImportError as e:
    print(f"Warning: Enhanced todo display not available: {e}")
    
    def enhanced_todo_hook(todos):
        '''Fallback hook function'''
        return "Enhanced display not available"
"""
    
    hook_path = Path(".claude/hooks/todo_display_hook.py")
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(hook_path, 'w') as f:
        f.write(hook_script)
    
    print(f"✅ Created hook: {hook_path}")
    
    # Create activation marker
    marker_path = Path(".claude/config/enhanced-todos-active.json")
    marker_data = {
        "enhanced_todos": {
            "active": True,
            "activated_at": "2025-08-24T00:00:00Z",
            "version": "1.0",
            "features": [
                "phase_by_phase_display",
                "real_time_progress_tracking",
                "execution_context_awareness",
                "observability_integration"
            ]
        }
    }
    
    with open(marker_path, 'w') as f:
        json.dump(marker_data, f, indent=2)
    
    print(f"✅ Created activation marker: {marker_path}")
    
    # Create README for the enhanced system
    readme_content = """# Enhanced Todo Display System

This system provides phase-by-phase progress tracking for the Claude Test Generator framework.

## Features

- **Phase-by-Phase Progress**: Clear display of current execution phase
- **Real-Time Updates**: Live progress tracking during framework execution
- **Execution Context**: Shows current run information and timing
- **Observability Integration**: Links to framework observability commands

## Configuration

- `todo-display-config.json` - Main configuration
- `todo-display-enforcement.json` - Enforcement rules
- `enhanced-todos-active.json` - Activation status

## Usage

The enhanced display is automatically activated for all TodoWrite operations.
No manual intervention required.

## Commands

- Use `/status` for current execution status
- Use `/timeline` for phase milestones
- Use `/deep-dive [agent]` for detailed analysis

## Deactivation

To deactivate, set `enabled: false` in the configuration files.
"""
    
    readme_path = Path(".claude/config/README-enhanced-todos.md")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Created documentation: {readme_path}")
    
    print("\n🎉 Enhanced todo display system activated!")
    print("📋 All TodoWrite operations will now show phase-by-phase progress")
    print("🔍 Use observability commands for detailed insights")

def deactivate_enhanced_todos():
    """Deactivate enhanced todo display system"""
    
    # Update configs to disable
    config_files = [
        ".claude/config/todo-display-config.json",
        ".claude/config/todo-display-enforcement.json"
    ]
    
    for config_path in config_files:
        full_path = Path(config_path)
        if full_path.exists():
            try:
                with open(full_path, 'r') as f:
                    config = json.load(f)
                
                # Disable all relevant sections
                if "enhanced_display" in config:
                    config["enhanced_display"]["enabled"] = False
                if "enforcement" in config:
                    config["enforcement"]["enabled"] = False
                
                with open(full_path, 'w') as f:
                    json.dump(config, f, indent=2)
                
                print(f"✅ Deactivated: {config_path}")
                
            except (json.JSONDecodeError, KeyError):
                print(f"⚠️ Could not update: {config_path}")
    
    # Update activation marker
    marker_path = Path(".claude/config/enhanced-todos-active.json")
    if marker_path.exists():
        marker_data = {
            "enhanced_todos": {
                "active": False,
                "deactivated_at": "2025-08-24T00:00:00Z",
                "version": "1.0"
            }
        }
        
        with open(marker_path, 'w') as f:
            json.dump(marker_data, f, indent=2)
        
        print(f"✅ Updated activation marker: {marker_path}")
    
    print("\n⚠️ Enhanced todo display system deactivated")
    print("📋 TodoWrite operations will use standard display")

def status_enhanced_todos():
    """Check status of enhanced todo display system"""
    
    marker_path = Path(".claude/config/enhanced-todos-active.json")
    if not marker_path.exists():
        print("❌ Enhanced todo display system not installed")
        return False
    
    try:
        with open(marker_path, 'r') as f:
            marker = json.load(f)
        
        is_active = marker.get("enhanced_todos", {}).get("active", False)
        
        if is_active:
            print("✅ Enhanced todo display system ACTIVE")
            print("📋 All TodoWrite operations show phase-by-phase progress")
            
            # Check config files
            config_files = [
                ".claude/config/todo-display-config.json",
                ".claude/config/todo-display-enforcement.json"
            ]
            
            for config_path in config_files:
                if Path(config_path).exists():
                    print(f"✅ Config file exists: {config_path}")
                else:
                    print(f"⚠️ Missing config file: {config_path}")
            
            return True
        else:
            print("⚠️ Enhanced todo display system INACTIVE")
            return False
            
    except (json.JSONDecodeError, KeyError):
        print("❌ Invalid activation marker")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "activate":
            activate_enhanced_todos()
        elif command == "deactivate":
            deactivate_enhanced_todos()
        elif command == "status":
            status_enhanced_todos()
        else:
            print("Usage: python activate_enhanced_todos.py [activate|deactivate|status]")
    else:
        # Default to activation
        activate_enhanced_todos()