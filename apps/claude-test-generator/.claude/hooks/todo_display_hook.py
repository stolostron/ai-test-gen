#!/usr/bin/env python3
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
