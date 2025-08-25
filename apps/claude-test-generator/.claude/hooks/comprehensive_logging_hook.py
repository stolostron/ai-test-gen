#!/usr/bin/env python3
"""
Claude Code Comprehensive Logging Hook
=====================================

Captures ALL tool executions for complete framework observability.
Logs every Bash, Read, Write, Task, Glob, Grep, Edit operation with full context.

This hook integrates with Claude Code's tool execution system to provide
comprehensive logging of all framework operations organized by JIRA tickets.
"""

import os
import sys
import json
import time
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add logging directory to path
logging_dir = Path(__file__).parent.parent / "logging"
sys.path.insert(0, str(logging_dir))

try:
    from framework_debug_logger import FrameworkDebugLogger, initialize_global_logger
except ImportError:
    # Fallback if logger not available
    print("⚠️  Framework logger not available, using basic logging")
    FrameworkDebugLogger = None

class ComprehensiveLoggingHook:
    """Claude Code tool hook for comprehensive framework logging"""
    
    def __init__(self):
        self.hook_name = "comprehensive_logging_hook"
        self.version = "1.0-PRODUCTION"
        
        # Initialize framework logger
        self.logger = None
        self.current_run_id = None
        self.current_jira_ticket = None
        
        # Framework state tracking
        self.framework_state = {
            'current_phase': None,
            'active_agents': [],
            'tool_execution_count': 0,
            'session_start_time': datetime.now().isoformat(),
            'jira_ticket': None
        }
        
        # Log storage
        self.execution_log = []
        self.session_stats = {
            'bash_commands': 0,
            'file_reads': 0,
            'file_writes': 0,
            'agent_spawns': 0,
            'searches': 0,
            'file_edits': 0
        }
        
        # Ensure log directories exist
        self.setup_log_directories()
        
    def setup_log_directories(self):
        """Setup logging directory structure"""
        base_log_dir = Path.cwd() / ".claude" / "logging"
        base_log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create immediate session log
        session_log_dir = base_log_dir / "current-session"
        session_log_dir.mkdir(exist_ok=True)
        
        self.session_log_file = session_log_dir / f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}.jsonl"
        
    def initialize_run_logging(self, jira_ticket: str = None, run_id: str = None):
        """Initialize logging for a specific run"""
        if not jira_ticket:
            jira_ticket = self.detect_jira_ticket()
        
        if not run_id:
            run_id = f"{jira_ticket}-{datetime.now().strftime('%Y%m%d-%H%M%S')}" if jira_ticket else f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        self.current_jira_ticket = jira_ticket
        self.current_run_id = run_id
        self.framework_state['jira_ticket'] = jira_ticket
        
        # Setup run-specific logging
        if FrameworkDebugLogger:
            try:
                self.logger = initialize_global_logger(run_id)
                self.logger.log_info("COMPREHENSIVE_LOGGING_START", "Starting comprehensive tool logging", {
                    "run_id": run_id,
                    "jira_ticket": jira_ticket,
                    "hook_version": self.version
                })
            except Exception as e:
                print(f"⚠️  Could not initialize framework logger: {e}")
                self.logger = None
        
        # Create run-specific log directory
        run_log_dir = Path.cwd() / ".claude" / "logging" / run_id
        run_log_dir.mkdir(parents=True, exist_ok=True)
        
        self.run_log_file = run_log_dir / "comprehensive_tool_log.jsonl"
        
        # Log initialization
        self.log_entry("LOGGING_INITIALIZED", "comprehensive_logging", {
            "run_id": run_id,
            "jira_ticket": jira_ticket,
            "timestamp": datetime.now().isoformat()
        })
        
    def detect_jira_ticket(self) -> Optional[str]:
        """Detect JIRA ticket from current context"""
        # Look for JIRA patterns in current working directory
        cwd = Path.cwd()
        
        # Check if we're in a run directory
        for part in cwd.parts:
            if 'ACM-' in part or 'OCPBUGS-' in part or 'RHEL-' in part:
                # Extract ticket ID
                import re
                match = re.search(r'([A-Z]+-\d+)', part)
                if match:
                    return match.group(1)
        
        # Check recent runs directory
        runs_dir = cwd / "runs"
        if runs_dir.exists():
            # Get most recent run directory
            run_dirs = [d for d in runs_dir.iterdir() if d.is_dir() and 'ACM-' in d.name]
            if run_dirs:
                latest_run = max(run_dirs, key=lambda d: d.stat().st_mtime)
                import re
                match = re.search(r'([A-Z]+-\d+)', latest_run.name)
                if match:
                    return match.group(1)
        
        return None
        
    def log_entry(self, action: str, tool: str, details: Dict[str, Any]):
        """Log a tool execution entry"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "run_id": self.current_run_id,
            "jira_ticket": self.current_jira_ticket,
            "action": action,
            "tool": tool,
            "details": details,
            "framework_state": self.framework_state.copy()
        }
        
        self.execution_log.append(entry)
        
        # Write to session log file
        with open(self.session_log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        # Write to run-specific log if available
        if hasattr(self, 'run_log_file') and self.run_log_file:
            with open(self.run_log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        
        # Log to framework logger if available
        if self.logger:
            self.logger.log_debug(f"TOOL_{action}", f"{tool} execution", details, component="TOOL")
    
    def process_tool_call(self, tool_name: str, parameters: dict) -> dict:
        """Process any tool call and log it comprehensively"""
        self.framework_state['tool_execution_count'] += 1
        
        # Initialize logging if not done yet
        if not self.current_run_id:
            self.initialize_run_logging()
        
        try:
            # Log based on tool type
            if tool_name.lower() == "bash":
                return self.process_bash_tool(parameters)
            elif tool_name.lower() == "read":
                return self.process_read_tool(parameters)
            elif tool_name.lower() == "write":
                return self.process_write_tool(parameters)
            elif tool_name.lower() == "task":
                return self.process_task_tool(parameters)
            elif tool_name.lower() in ["glob", "grep"]:
                return self.process_search_tool(tool_name, parameters)
            elif tool_name.lower() == "edit":
                return self.process_edit_tool(parameters)
            else:
                return self.process_generic_tool(tool_name, parameters)
                
        except Exception as e:
            self.log_entry("TOOL_ERROR", tool_name, {
                "parameters": parameters,
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            raise
        
        # Return parameters unchanged (hook doesn't modify behavior)
        return parameters
    
    def process_bash_tool(self, parameters: dict) -> dict:
        """Process Bash tool execution"""
        self.session_stats['bash_commands'] += 1
        
        command = parameters.get('command', '')
        description = parameters.get('description', '')
        
        # Analyze command for framework context
        command_context = self.analyze_bash_command(command)
        
        self.log_entry("BASH_EXECUTION", "bash", {
            "command": command,
            "description": description,
            "timeout": parameters.get('timeout'),
            "background": parameters.get('run_in_background', False),
            "command_analysis": command_context,
            "execution_id": f"bash_{int(time.time() * 1000)}"
        })
        
        return parameters
    
    def analyze_bash_command(self, command: str) -> Dict[str, Any]:
        """Analyze bash command for framework context"""
        analysis = {
            "command_type": "general",
            "framework_relevance": False,
            "environment_interaction": False,
            "data_extraction": False
        }
        
        command_lower = command.lower()
        
        # Detect environment commands
        if any(cmd in command_lower for cmd in ['oc ', 'kubectl ', 'gh ', 'curl']):
            analysis["command_type"] = "environment"
            analysis["environment_interaction"] = True
            analysis["framework_relevance"] = True
        
        # Detect version/info commands
        elif any(cmd in command_lower for cmd in ['version', 'status', 'info', 'get']):
            analysis["command_type"] = "information"
            analysis["data_extraction"] = True
            analysis["framework_relevance"] = True
        
        # Detect authentication commands
        elif any(cmd in command_lower for cmd in ['login', 'auth', 'token']):
            analysis["command_type"] = "authentication"
            analysis["environment_interaction"] = True
            analysis["framework_relevance"] = True
        
        # Detect file operations
        elif any(cmd in command_lower for cmd in ['cat', 'ls', 'find', 'grep']):
            analysis["command_type"] = "file_operation"
            analysis["data_extraction"] = True
        
        return analysis
    
    def process_read_tool(self, parameters: dict) -> dict:
        """Process Read tool execution"""
        self.session_stats['file_reads'] += 1
        
        file_path = parameters.get('file_path', '')
        
        # Analyze file for framework context
        file_context = self.analyze_file_path(file_path)
        
        self.log_entry("FILE_READ", "read", {
            "file_path": file_path,
            "limit": parameters.get('limit'),
            "offset": parameters.get('offset'),
            "file_analysis": file_context,
            "execution_id": f"read_{int(time.time() * 1000)}"
        })
        
        return parameters
    
    def process_write_tool(self, parameters: dict) -> dict:
        """Process Write tool execution"""
        self.session_stats['file_writes'] += 1
        
        file_path = parameters.get('file_path', '')
        content = parameters.get('content', '')
        
        # Analyze file and content for framework context
        file_context = self.analyze_file_path(file_path)
        content_context = self.analyze_file_content(file_path, content)
        
        self.log_entry("FILE_WRITE", "write", {
            "file_path": file_path,
            "content_length": len(content),
            "file_analysis": file_context,
            "content_analysis": content_context,
            "execution_id": f"write_{int(time.time() * 1000)}"
        })
        
        return parameters
    
    def process_task_tool(self, parameters: dict) -> dict:
        """Process Task tool execution (Agent spawning)"""
        self.session_stats['agent_spawns'] += 1
        
        description = parameters.get('description', '')
        subagent_type = parameters.get('subagent_type', 'general-purpose')
        prompt = parameters.get('prompt', '')
        
        # Track agent spawning
        agent_id = f"agent_{subagent_type}_{int(time.time() * 1000)}"
        self.framework_state['active_agents'].append({
            "agent_id": agent_id,
            "type": subagent_type,
            "description": description,
            "spawn_time": datetime.now().isoformat()
        })
        
        self.log_entry("AGENT_SPAWN", "task", {
            "agent_id": agent_id,
            "description": description,
            "subagent_type": subagent_type,
            "prompt_length": len(prompt),
            "prompt_preview": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "execution_id": f"task_{int(time.time() * 1000)}"
        })
        
        return parameters
    
    def process_search_tool(self, tool_name: str, parameters: dict) -> dict:
        """Process Glob/Grep tool execution"""
        self.session_stats['searches'] += 1
        
        pattern = parameters.get('pattern', '')
        path = parameters.get('path', '')
        
        self.log_entry("SEARCH_EXECUTION", tool_name, {
            "pattern": pattern,
            "path": path,
            "tool": tool_name,
            "parameters": {k: v for k, v in parameters.items() if k not in ['pattern', 'path']},
            "execution_id": f"{tool_name}_{int(time.time() * 1000)}"
        })
        
        return parameters
    
    def process_edit_tool(self, parameters: dict) -> dict:
        """Process Edit tool execution"""
        self.session_stats['file_edits'] += 1
        
        file_path = parameters.get('file_path', '')
        old_string = parameters.get('old_string', '')
        new_string = parameters.get('new_string', '')
        replace_all = parameters.get('replace_all', False)
        
        # Analyze file for framework context
        file_context = self.analyze_file_path(file_path)
        
        self.log_entry("FILE_EDIT", "edit", {
            "file_path": file_path,
            "old_string_length": len(old_string),
            "new_string_length": len(new_string),
            "replace_all": replace_all,
            "file_analysis": file_context,
            "execution_id": f"edit_{int(time.time() * 1000)}"
        })
        
        return parameters
    
    def process_generic_tool(self, tool_name: str, parameters: dict) -> dict:
        """Process any other tool execution"""
        self.log_entry("GENERIC_TOOL", tool_name, {
            "tool_name": tool_name,
            "parameters": parameters,
            "execution_id": f"{tool_name}_{int(time.time() * 1000)}"
        })
        
        return parameters
    
    def analyze_file_path(self, file_path: str) -> Dict[str, Any]:
        """Analyze file path for framework context"""
        analysis = {
            "file_type": "unknown",
            "framework_relevance": False,
            "component": "unknown"
        }
        
        file_path_lower = file_path.lower()
        
        # Detect framework components
        if '.claude/' in file_path_lower:
            analysis["framework_relevance"] = True
            
            if 'ai-services/' in file_path_lower:
                analysis["component"] = "ai_services"
                analysis["file_type"] = "ai_service"
            elif 'observability/' in file_path_lower:
                analysis["component"] = "observability"
                analysis["file_type"] = "observability"
            elif 'logging/' in file_path_lower:
                analysis["component"] = "logging"
                analysis["file_type"] = "logging"
            elif 'config/' in file_path_lower:
                analysis["component"] = "config"
                analysis["file_type"] = "configuration"
        
        # Detect run outputs
        elif 'runs/' in file_path_lower:
            analysis["framework_relevance"] = True
            analysis["component"] = "outputs"
            
            if 'test-cases' in file_path_lower:
                analysis["file_type"] = "test_cases"
            elif 'analysis' in file_path_lower:
                analysis["file_type"] = "analysis"
            elif 'metadata' in file_path_lower:
                analysis["file_type"] = "metadata"
        
        # Detect temp repos
        elif 'temp_repos/' in file_path_lower:
            analysis["framework_relevance"] = True
            analysis["component"] = "temp_repos"
            analysis["file_type"] = "source_code"
        
        return analysis
    
    def analyze_file_content(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze file content for framework context"""
        analysis = {
            "content_type": "unknown",
            "jira_references": [],
            "github_references": [],
            "test_cases_count": 0,
            "framework_keywords": []
        }
        
        # Extract JIRA references
        import re
        jira_refs = re.findall(r'([A-Z]+-\d+)', content)
        analysis["jira_references"] = list(set(jira_refs))
        
        # Extract GitHub references
        github_refs = re.findall(r'github\.com/[^\s]+|#(\d+)', content)
        analysis["github_references"] = github_refs[:10]  # Limit to first 10
        
        # Count test cases
        analysis["test_cases_count"] = content.count('Test Case')
        
        # Detect framework keywords
        framework_keywords = ['agent', 'phase', 'validation', 'context', 'progressive', 'evidence']
        analysis["framework_keywords"] = [kw for kw in framework_keywords if kw.lower() in content.lower()]
        
        # Determine content type
        if 'test case' in content.lower():
            analysis["content_type"] = "test_plan"
        elif 'analysis' in content.lower() and any(kw in content.lower() for kw in ['feature', 'requirements']):
            analysis["content_type"] = "analysis_report"
        elif 'metadata' in file_path.lower():
            analysis["content_type"] = "run_metadata"
        
        return analysis
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        return {
            "session_info": {
                "hook_version": self.version,
                "run_id": self.current_run_id,
                "jira_ticket": self.current_jira_ticket,
                "start_time": self.framework_state['session_start_time'],
                "current_time": datetime.now().isoformat()
            },
            "execution_stats": self.session_stats,
            "framework_state": self.framework_state,
            "total_logs": len(self.execution_log),
            "log_files": {
                "session_log": str(self.session_log_file),
                "run_log": str(getattr(self, 'run_log_file', 'not_initialized'))
            }
        }
    
    def save_session_summary(self) -> str:
        """Save comprehensive session summary"""
        summary = self.get_session_summary()
        
        # Save to session directory
        summary_file = self.session_log_file.parent / f"session-summary-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return str(summary_file)

# GLOBAL HOOK INSTANCE
_hook_instance = ComprehensiveLoggingHook()

def claude_code_tool_hook(tool_name: str, parameters: dict) -> dict:
    """
    Main Claude Code hook function
    
    This function is called by Claude Code before executing any tool.
    It logs comprehensive information about every tool execution.
    """
    try:
        return _hook_instance.process_tool_call(tool_name, parameters)
    except Exception as e:
        # Log the error but don't let hook errors break the framework
        _hook_instance.log_entry("HOOK_ERROR", tool_name, {
            "parameters": parameters,
            "error": str(e),
            "traceback": traceback.format_exc()
        })
        
        # For logging hooks, we don't want to block operations
        print(f"⚠️  Logging hook error (non-blocking): {e}")
        return parameters

def get_session_summary() -> dict:
    """Get current session summary"""
    return _hook_instance.get_session_summary()

def save_session_summary() -> str:
    """Save session summary"""
    return _hook_instance.save_session_summary()

def initialize_run_logging(jira_ticket: str = None, run_id: str = None):
    """Initialize logging for a specific run"""
    return _hook_instance.initialize_run_logging(jira_ticket, run_id)

# Claude Code Hook Registration
HOOK_METADATA = {
    "name": "comprehensive_logging_hook",
    "version": "1.0-PRODUCTION",
    "description": "Comprehensive logging of all Claude Code tool executions for framework observability",
    "author": "AI Systems Suite",
    "hook_function": claude_code_tool_hook,
    "hook_types": ["tool_execution"],
    "enabled": True
}

if __name__ == "__main__":
    # Test the hook
    print("🎯 Testing Comprehensive Logging Hook")
    
    # Test various tool calls
    claude_code_tool_hook("bash", {"command": "echo 'test'", "description": "test command"})
    claude_code_tool_hook("read", {"file_path": "/test/file.txt"})
    claude_code_tool_hook("task", {"description": "Test agent", "subagent_type": "general-purpose", "prompt": "Test prompt"})
    
    # Get summary
    summary = get_session_summary()
    print("Session Summary:", json.dumps(summary, indent=2))
    
    # Save summary
    summary_file = save_session_summary()
    print(f"Summary saved to: {summary_file}")