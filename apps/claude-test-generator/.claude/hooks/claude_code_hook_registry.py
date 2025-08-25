#!/usr/bin/env python3
"""
Claude Code Hook Registry and Activation System
===============================================

MANDATORY ACTIVATION of comprehensive logging hooks for all framework executions.
Ensures every tool execution, agent operation, and framework stage is captured.

This module ensures that hooks are properly registered with Claude Code and 
activated for ALL framework executions - NO EXCEPTIONS.
"""

import os
import sys
import json
import importlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Hook registration constants
HOOK_REGISTRY_FILE = ".claude/hooks/active_hooks.json"
MANDATORY_HOOKS = [
    "comprehensive_logging_hook",
    "pre_write_enforcement_hook", 
    "todo_display_hook"
]

class ClaudeCodeHookRegistry:
    """Registry and activation system for Claude Code hooks"""
    
    def __init__(self):
        self.hooks_dir = Path(__file__).parent
        self.project_root = self.hooks_dir.parent.parent
        self.registry_file = self.project_root / HOOK_REGISTRY_FILE
        self.active_hooks = {}
        self.hook_metadata = {}
        
        # Ensure registry directory exists
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing registry
        self._load_registry()
    
    def _load_registry(self):
        """Load existing hook registry"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    data = json.load(f)
                    self.active_hooks = data.get('active_hooks', {})
                    self.hook_metadata = data.get('hook_metadata', {})
            except Exception as e:
                print(f"⚠️  Failed to load hook registry: {e}")
                self.active_hooks = {}
                self.hook_metadata = {}
    
    def register_hook(self, hook_name: str, force_activate: bool = True) -> bool:
        """Register a hook with Claude Code"""
        hook_file = self.hooks_dir / f"{hook_name}.py"
        
        if not hook_file.exists():
            print(f"❌ Hook file not found: {hook_file}")
            return False
        
        try:
            # Import hook module
            spec = importlib.util.spec_from_file_location(hook_name, hook_file)
            hook_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(hook_module)
            
            # Get hook metadata
            if hasattr(hook_module, 'HOOK_METADATA'):
                metadata = hook_module.HOOK_METADATA
            else:
                metadata = {
                    "name": hook_name,
                    "description": f"Hook {hook_name}",
                    "enabled": True
                }
            
            # Register hook
            self.active_hooks[hook_name] = {
                "enabled": True,
                "file_path": str(hook_file),
                "registered_at": datetime.now().isoformat(),
                "hook_function": f"{hook_name}.claude_code_tool_hook" if hasattr(hook_module, 'claude_code_tool_hook') else None,
                "mandatory": hook_name in MANDATORY_HOOKS
            }
            
            self.hook_metadata[hook_name] = metadata
            
            print(f"✅ Registered hook: {hook_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to register hook {hook_name}: {e}")
            return False
    
    def activate_mandatory_hooks(self) -> List[str]:
        """Activate all mandatory hooks for comprehensive logging"""
        activated_hooks = []
        
        print("🎯 ACTIVATING MANDATORY COMPREHENSIVE LOGGING")
        print("=" * 60)
        print("Ensuring comprehensive logging is MANDATORY for all framework executions")
        print()
        
        for hook_name in MANDATORY_HOOKS:
            if self.register_hook(hook_name, force_activate=True):
                activated_hooks.append(hook_name)
                print(f"   ✅ {hook_name}: MANDATORY ACTIVATION COMPLETE")
            else:
                print(f"   ❌ {hook_name}: ACTIVATION FAILED")
        
        # Save registry
        self._save_registry()
        
        print(f"\n🔒 MANDATORY LOGGING ACTIVATED: {len(activated_hooks)}/{len(MANDATORY_HOOKS)} hooks")
        return activated_hooks
    
    def _save_registry(self):
        """Save hook registry to file"""
        registry_data = {
            "last_updated": datetime.now().isoformat(),
            "active_hooks": self.active_hooks,
            "hook_metadata": self.hook_metadata,
            "mandatory_hooks": MANDATORY_HOOKS
        }
        
        with open(self.registry_file, 'w') as f:
            json.dump(registry_data, f, indent=2)
    
    def create_claude_code_config(self) -> str:
        """Create Claude Code configuration file to activate hooks"""
        config_file = self.project_root / ".claude" / "claude_code_config.json"
        
        # Create Claude Code hook configuration
        claude_config = {
            "hooks": {
                "enabled": True,
                "hook_directory": str(self.hooks_dir),
                "active_hooks": []
            },
            "logging": {
                "comprehensive_logging": True,
                "mandatory_logging": True,
                "log_all_tools": True,
                "log_directory": ".claude/logs/active-runs"
            }
        }
        
        # Add active hooks to configuration
        for hook_name, hook_data in self.active_hooks.items():
            if hook_data["enabled"]:
                claude_config["hooks"]["active_hooks"].append({
                    "name": hook_name,
                    "file": f"{hook_name}.py",
                    "function": hook_data.get("hook_function", f"claude_code_tool_hook"),
                    "mandatory": hook_data.get("mandatory", False)
                })
        
        # Save configuration
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(claude_config, f, indent=2)
        
        print(f"📝 Claude Code config created: {config_file}")
        return str(config_file)
    
    def get_hook_status(self) -> Dict[str, Any]:
        """Get comprehensive hook status"""
        return {
            "total_hooks": len(self.active_hooks),
            "mandatory_hooks": len([h for h in self.active_hooks.values() if h.get("mandatory", False)]),
            "enabled_hooks": len([h for h in self.active_hooks.values() if h.get("enabled", False)]),
            "active_hooks": list(self.active_hooks.keys()),
            "mandatory_hooks_list": MANDATORY_HOOKS,
            "registry_file": str(self.registry_file)
        }

def activate_comprehensive_logging() -> bool:
    """Main function to activate comprehensive logging for framework"""
    print("🚀 CLAUDE CODE COMPREHENSIVE LOGGING ACTIVATION")
    print("=" * 80)
    print("MANDATORY ACTIVATION: Comprehensive logging will be enabled for ALL framework executions")
    print("NO EXCEPTIONS: Every tool execution, agent operation, and framework stage will be captured")
    print()
    
    registry = ClaudeCodeHookRegistry()
    
    try:
        # Activate mandatory hooks
        activated_hooks = registry.activate_mandatory_hooks()
        
        # Create Claude Code configuration
        config_file = registry.create_claude_code_config()
        
        # Get status
        status = registry.get_hook_status()
        
        print("\n📊 ACTIVATION SUMMARY:")
        print("=" * 30)
        print(f"✅ Total Hooks Registered: {status['total_hooks']}")
        print(f"🔒 Mandatory Hooks Active: {status['mandatory_hooks']}")
        print(f"⚡ Enabled Hooks: {status['enabled_hooks']}")
        print(f"📝 Configuration File: {config_file}")
        
        print("\n🎯 ACTIVE HOOKS:")
        for hook in activated_hooks:
            print(f"   ✅ {hook}")
        
        if len(activated_hooks) == len(MANDATORY_HOOKS):
            print("\n🎉 SUCCESS: COMPREHENSIVE LOGGING FULLY ACTIVATED")
            print("All framework executions will now capture complete operational data")
            return True
        else:
            print("\n⚠️  WARNING: PARTIAL ACTIVATION")
            print("Some mandatory hooks failed to activate")
            return False
            
    except Exception as e:
        print(f"\n❌ ACTIVATION FAILED: {e}")
        return False

if __name__ == "__main__":
    success = activate_comprehensive_logging()
    sys.exit(0 if success else 1)