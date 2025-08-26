#!/usr/bin/env python3
"""
User Prompt Completion Hook for Claude Code
==========================================

Sound notification hook that triggers when Claude completes responding to user prompts.
Integrates with Claude Code's hook system to provide audio feedback when responses are complete.
"""

import os
import sys
import subprocess
import platform
from datetime import datetime
from typing import Dict, Any, Optional

# Hook metadata for Claude Code registration
HOOK_METADATA = {
    "name": "user_prompt_completion_hook",
    "version": "1.0-PRODUCTION", 
    "description": "Sound notification when Claude completes responding to user prompts",
    "author": "AI Systems Suite",
    "hook_function": "claude_code_tool_hook",
    "triggers": ["user_prompt_submit"],
    "enabled": True
}

class UserPromptCompletionNotifier:
    """Sound notification system for prompt completion"""
    
    def __init__(self):
        self.system = platform.system()
        self.notification_enabled = True
        
    def play_completion_sound(self) -> bool:
        """Play system sound to indicate prompt completion"""
        try:
            if self.system == "Darwin":  # macOS
                # Use macOS say command with system sound
                subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], 
                             check=False, capture_output=True, timeout=3)
                return True
            elif self.system == "Linux":
                # Use Linux beep or speaker-test
                subprocess.run(["speaker-test", "-t", "sine", "-f", "1000", "-l", "1"], 
                             check=False, capture_output=True, timeout=2)
                return True
            elif self.system == "Windows":
                # Use Windows system beep
                import winsound
                winsound.Beep(1000, 500)  # 1000 Hz for 500ms
                return True
            else:
                print("🔔 Prompt completion notification (sound not available)")
                return False
                
        except Exception as e:
            print(f"🔔 Prompt completion notification (sound failed: {e})")
            return False
    
    def log_completion(self, context: Dict[str, Any]) -> None:
        """Log prompt completion event"""
        timestamp = datetime.now().isoformat()
        print(f"🎯 [{timestamp}] User prompt response completed")
        
        # Extract any relevant context
        if 'tool_name' in context:
            print(f"   Last tool: {context['tool_name']}")
        if 'execution_time' in context:
            print(f"   Execution time: {context['execution_time']:.3f}s")

# Global state to track if we should play sound after tool sequences
_last_tool_time = None
_tool_sequence_active = False

def claude_code_tool_hook(tool_name: str, args: Dict[str, Any], result: Any, **kwargs) -> Optional[Dict[str, Any]]:
    """
    Claude Code hook function for user prompt completion notifications
    
    Args:
        tool_name: Name of the tool being executed
        args: Tool arguments
        result: Tool execution result
        **kwargs: Additional context
        
    Returns:
        Hook execution metadata
    """
    global _last_tool_time, _tool_sequence_active
    
    current_time = datetime.now()
    
    # Track tool activity - any tool execution means we're working on a prompt
    if tool_name in ['Task', 'Bash', 'Read', 'Write', 'Edit', 'Glob', 'Grep', 'MultiEdit', 'TodoWrite']:
        _tool_sequence_active = True
        _last_tool_time = current_time
        
        # Don't play sound during active tool execution
        return None
    
    # Check for prompt completion indicators
    completion_triggers = [
        'user_prompt_submit',
        'user_prompt_complete', 
        'response_complete',
        'session_ready'
    ]
    
    should_notify = (
        tool_name in completion_triggers or
        kwargs.get('event_type') == 'prompt_completion' or
        kwargs.get('event_type') == 'response_complete' or
        # If no tools have run for 2+ seconds and we were previously active
        (_tool_sequence_active and _last_tool_time and 
         (current_time - _last_tool_time).total_seconds() > 2.0)
    )
    
    if should_notify:
        notifier = UserPromptCompletionNotifier()
        
        # Create completion context
        completion_context = {
            'tool_name': tool_name,
            'timestamp': current_time.isoformat(),
            'event_type': 'user_prompt_completion',
            'notification_enabled': True,
            'was_tool_sequence': _tool_sequence_active
        }
        
        # Add execution time if available
        if 'execution_time' in kwargs:
            completion_context['execution_time'] = kwargs['execution_time']
        
        # Log the completion
        notifier.log_completion(completion_context)
        
        # Play completion sound
        sound_success = notifier.play_completion_sound()
        completion_context['sound_played'] = sound_success
        
        # Reset sequence tracking
        _tool_sequence_active = False
        _last_tool_time = None
        
        return {
            'hook_name': 'user_prompt_completion_hook',
            'status': 'completed',
            'notification_sent': True,
            'sound_notification': sound_success,
            'context': completion_context
        }
    
    # For other tools, just pass through silently
    return None

def register_with_claude_code() -> bool:
    """Register this hook with Claude Code hook system"""
    try:
        # Import the hook registry
        sys.path.insert(0, os.path.dirname(__file__))
        from claude_code_hook_registry import ClaudeCodeHookRegistry
        
        registry = ClaudeCodeHookRegistry()
        
        # Register this hook
        success = registry.register_hook("user_prompt_completion_hook", force_activate=True)
        
        if success:
            print("✅ User Prompt Completion Hook registered with Claude Code")
            
            # Update the hook registry to include this hook
            registry._save_registry()
            
            # Create updated Claude Code configuration
            registry.create_claude_code_config()
            
            print("🔔 Sound notifications enabled for prompt completion")
            return True
        else:
            print("❌ Failed to register User Prompt Completion Hook")
            return False
            
    except Exception as e:
        print(f"❌ Hook registration failed: {e}")
        return False

def test_notification() -> None:
    """Test the notification system"""
    print("🧪 Testing User Prompt Completion Notification...")
    
    notifier = UserPromptCompletionNotifier()
    
    # Test sound notification
    print("Testing sound notification...")
    success = notifier.play_completion_sound()
    
    if success:
        print("✅ Sound notification test successful")
    else:
        print("❌ Sound notification test failed")
    
    # Test completion logging
    test_context = {
        'tool_name': 'test_tool',
        'execution_time': 1.234
    }
    
    notifier.log_completion(test_context)
    print("✅ Completion logging test successful")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_notification()
    elif len(sys.argv) > 1 and sys.argv[1] == "register":
        success = register_with_claude_code()
        sys.exit(0 if success else 1)
    else:
        print("User Prompt Completion Hook for Claude Code")
        print("Usage:")
        print("  python user_prompt_completion_hook.py test      # Test notification")
        print("  python user_prompt_completion_hook.py register  # Register with Claude Code")