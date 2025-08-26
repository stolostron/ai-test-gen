#!/usr/bin/env python3
"""
Notification Activation Script for Claude Test Generator
========================================================

Ensures sound notifications are active for every session in this project.
Run this automatically when starting Claude Code in this project.
"""

import os
import sys
import json
from pathlib import Path

def ensure_notification_hook_active():
    """Ensure the user prompt completion hook is active for this session"""
    
    # Get project paths
    project_root = Path(__file__).parent.parent
    hooks_dir = project_root / ".claude" / "hooks"
    config_file = project_root / ".claude" / "claude_code_config.json"
    
    print("🔔 Activating Sound Notifications for Claude Test Generator")
    print("=" * 60)
    
    # Check if hook file exists
    hook_file = hooks_dir / "user_prompt_completion_hook.py"
    if not hook_file.exists():
        print("❌ User prompt completion hook not found")
        return False
    
    # Check if configuration exists
    if not config_file.exists():
        print("📝 Creating Claude Code configuration...")
        
        # Create basic configuration with notification hook
        config_data = {
            "hooks": {
                "enabled": True,
                "hook_directory": str(hooks_dir),
                "active_hooks": [
                    {
                        "name": "user_prompt_completion_hook",
                        "file": "user_prompt_completion_hook.py",
                        "function": "user_prompt_completion_hook.claude_code_tool_hook",
                        "mandatory": False
                    }
                ]
            },
            "logging": {
                "comprehensive_logging": True,
                "mandatory_logging": True,
                "log_all_tools": True,
                "log_directory": ".claude/logs/active-runs"
            }
        }
        
        # Save configuration
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print(f"✅ Configuration created: {config_file}")
    
    # Verify configuration includes our hook
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        hooks = config.get("hooks", {}).get("active_hooks", [])
        notification_hook_active = any(
            hook.get("name") == "user_prompt_completion_hook" 
            for hook in hooks
        )
        
        if notification_hook_active:
            print("✅ Sound notification hook is active")
        else:
            print("⚠️  Sound notification hook not found in configuration")
            return False
            
    except Exception as e:
        print(f"❌ Failed to verify configuration: {e}")
        return False
    
    # Test notification system
    print("\n🧪 Testing notification system...")
    try:
        # Import and test the hook
        sys.path.insert(0, str(hooks_dir))
        from user_prompt_completion_hook import UserPromptCompletionNotifier
        
        notifier = UserPromptCompletionNotifier()
        success = notifier.play_completion_sound()
        
        if success:
            print("✅ Sound notification test successful")
        else:
            print("⚠️  Sound notification test failed (but hook is still active)")
            
    except Exception as e:
        print(f"⚠️  Notification test failed: {e}")
        print("   (Hook may still work during actual Claude Code execution)")
    
    print("\n🎯 NOTIFICATION SETUP COMPLETE")
    print("Sound notifications will play after each response completion")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = ensure_notification_hook_active()
    if success:
        print("\n✅ Ready! Sound notifications are active for this session.")
    else:
        print("\n❌ Setup failed. Check the error messages above.")
    
    sys.exit(0 if success else 1)