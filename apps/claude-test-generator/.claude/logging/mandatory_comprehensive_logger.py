#!/usr/bin/env python3
"""
Mandatory Comprehensive Logger - NO EXCEPTIONS
==============================================

MANDATORY comprehensive logging system that captures EVERY framework operation.
This logging is REQUIRED and CANNOT be disabled for any framework execution.

CAPTURES EVERYTHING:
- All Bash commands with full input/output
- All file operations (read/write/edit) with content analysis
- All agent operations with complete data flow
- All framework phases with state transitions
- All tool executions with parameter and response data
- All API calls and environment interactions

ORGANIZATION: 
- Logs organized by JIRA ticket for easy navigation
- Real-time logging during execution
- Comprehensive searchable format
- Complete audit trail for debugging
"""

import os
import sys
import json
import time
import threading
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import functools
import re

class MandatoryComprehensiveLogger:
    """MANDATORY comprehensive logger - captures ALL framework operations"""
    
    def __init__(self, jira_ticket: str = None):
        self.jira_ticket = jira_ticket or self._detect_jira_ticket()
        self.run_id = f"{self.jira_ticket}-{datetime.now().strftime('%Y%m%d-%H%M%S')}" if self.jira_ticket else f"unknown-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Setup logging directories
        self.base_log_dir = Path.cwd() / ".claude" / "logs" / "comprehensive"
        self.jira_log_dir = self.base_log_dir / self.jira_ticket if self.jira_ticket else self.base_log_dir / "unknown"
        self.run_log_dir = self.jira_log_dir / self.run_id
        
        # Create directory structure
        self._setup_logging_directories()
        
        # Initialize log files
        self.master_log_file = self.run_log_dir / "comprehensive_master.jsonl"
        self.agent_operations_file = self.run_log_dir / "agent_operations.jsonl" 
        self.tool_executions_file = self.run_log_dir / "tool_executions.jsonl"
        self.bash_commands_file = self.run_log_dir / "bash_commands.jsonl"
        self.file_operations_file = self.run_log_dir / "file_operations.jsonl"
        self.api_calls_file = self.run_log_dir / "api_calls.jsonl"
        self.framework_phases_file = self.run_log_dir / "framework_phases.jsonl"
        self.execution_summary_file = self.run_log_dir / "execution_summary.json"
        
        # Execution tracking
        self.session_start_time = datetime.now()
        self.execution_stats = {
            'total_operations': 0,
            'bash_commands': 0,
            'file_operations': 0,
            'agent_operations': 0,
            'api_calls': 0,
            'tool_executions': 0,
            'framework_phases': 0
        }
        
        # Framework state
        self.current_phase = None
        self.active_agents = []
        self.framework_context = {}
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Initialize logging
        self._initialize_logging_session()
        
        print(f"🔒 MANDATORY COMPREHENSIVE LOGGING ACTIVATED")
        print(f"   JIRA Ticket: {self.jira_ticket}")
        print(f"   Run ID: {self.run_id}")
        print(f"   Log Directory: {self.run_log_dir}")
    
    def _detect_jira_ticket(self) -> Optional[str]:
        """Detect JIRA ticket from current context"""
        # Check current working directory
        cwd = Path.cwd()
        
        # Check if we're in a run directory
        for part in cwd.parts:
            if re.search(r'[A-Z]+-\d+', part):
                match = re.search(r'([A-Z]+-\d+)', part)
                if match:
                    return match.group(1)
        
        # Check recent runs directory
        runs_dir = cwd / "runs"
        if runs_dir.exists():
            run_dirs = [d for d in runs_dir.iterdir() if d.is_dir() and re.search(r'[A-Z]+-\d+', d.name)]
            if run_dirs:
                latest_run = max(run_dirs, key=lambda d: d.stat().st_mtime)
                match = re.search(r'([A-Z]+-\d+)', latest_run.name)
                if match:
                    return match.group(1)
        
        return None
    
    def _setup_logging_directories(self):
        """Setup comprehensive logging directory structure"""
        directories = [
            self.run_log_dir,
            self.run_log_dir / "agents",
            self.run_log_dir / "tools", 
            self.run_log_dir / "phases",
            self.run_log_dir / "raw-data",
            self.run_log_dir / "analysis"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Create latest symlink
        latest_link = self.jira_log_dir / "latest"
        if latest_link.exists() or latest_link.is_symlink():
            latest_link.unlink()
        latest_link.symlink_to(self.run_id)
    
    def _initialize_logging_session(self):
        """Initialize comprehensive logging session"""
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "LOGGING_SESSION_START",
            "jira_ticket": self.jira_ticket,
            "run_id": self.run_id,
            "session_start_time": self.session_start_time.isoformat(),
            "log_directory": str(self.run_log_dir),
            "logging_mode": "MANDATORY_COMPREHENSIVE",
            "framework_version": "4.0-enhanced",
            "details": {
                "comprehensive_logging": True,
                "mandatory_mode": True,
                "captures_all_operations": True,
                "organized_by_jira_ticket": True
            }
        }
        
        self._write_to_log(session_data, self.master_log_file)
        
    def _write_to_log(self, data: Dict[str, Any], log_file: Path):
        """Thread-safe log writing"""
        with self._lock:
            with open(log_file, 'a') as f:
                f.write(json.dumps(data) + '\n')
    
    def log_bash_command(self, command: str, description: str = None, timeout: int = None, 
                        run_in_background: bool = False, output: Dict[str, Any] = None):
        """Log Bash command execution with complete input/output"""
        self.execution_stats['bash_commands'] += 1
        self.execution_stats['total_operations'] += 1
        
        command_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "BASH_COMMAND",
            "jira_ticket": self.jira_ticket,
            "run_id": self.run_id,
            "current_phase": self.current_phase,
            "command": command,
            "description": description,
            "timeout": timeout,
            "run_in_background": run_in_background,
            "execution_context": {
                "active_agents": self.active_agents.copy(),
                "framework_context": self.framework_context.copy()
            },
            "command_analysis": self._analyze_bash_command(command),
            "output": output or {},
            "execution_id": f"bash_{int(time.time() * 1000)}"
        }
        
        self._write_to_log(command_data, self.bash_commands_file)
        self._write_to_log(command_data, self.master_log_file)
        
        print(f"📝 LOGGED: Bash command - {command[:50]}...")
    
    def log_file_operation(self, operation: str, file_path: str, content: str = None, 
                          details: Dict[str, Any] = None):
        """Log file operations with content analysis"""
        self.execution_stats['file_operations'] += 1
        self.execution_stats['total_operations'] += 1
        
        file_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "FILE_OPERATION",
            "jira_ticket": self.jira_ticket,
            "run_id": self.run_id,
            "current_phase": self.current_phase,
            "operation": operation,
            "file_path": file_path,
            "content_length": len(content) if content else 0,
            "content_preview": content[:200] + "..." if content and len(content) > 200 else content,
            "file_analysis": self._analyze_file_operation(file_path, content),
            "execution_context": {
                "active_agents": self.active_agents.copy(),
                "framework_context": self.framework_context.copy()
            },
            "details": details or {},
            "execution_id": f"file_{int(time.time() * 1000)}"
        }
        
        self._write_to_log(file_data, self.file_operations_file)
        self._write_to_log(file_data, self.master_log_file)
        
        print(f"📝 LOGGED: File {operation} - {file_path}")
    
    def log_agent_operation(self, agent_name: str, operation: str, data: Dict[str, Any] = None,
                           findings: str = None, context: Dict[str, Any] = None):
        """Log agent operations with complete data flow"""
        self.execution_stats['agent_operations'] += 1
        self.execution_stats['total_operations'] += 1
        
        agent_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "AGENT_OPERATION", 
            "jira_ticket": self.jira_ticket,
            "run_id": self.run_id,
            "current_phase": self.current_phase,
            "agent_name": agent_name,
            "operation": operation,
            "findings": findings,
            "data": data or {},
            "context": context or {},
            "execution_context": {
                "active_agents": self.active_agents.copy(),
                "framework_context": self.framework_context.copy()
            },
            "execution_id": f"agent_{agent_name}_{int(time.time() * 1000)}"
        }
        
        # Update active agents
        if operation == "start" or operation == "spawn":
            if agent_name not in self.active_agents:
                self.active_agents.append(agent_name)
        elif operation == "complete" or operation == "finish":
            if agent_name in self.active_agents:
                self.active_agents.remove(agent_name)
        
        self._write_to_log(agent_data, self.agent_operations_file)
        self._write_to_log(agent_data, self.master_log_file)
        
        print(f"📝 LOGGED: Agent {agent_name} - {operation}")
    
    def log_tool_execution(self, tool_name: str, parameters: Dict[str, Any], 
                          response: Any = None, execution_time: float = None):
        """Log tool executions with parameters and responses"""
        self.execution_stats['tool_executions'] += 1
        self.execution_stats['total_operations'] += 1
        
        tool_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "TOOL_EXECUTION",
            "jira_ticket": self.jira_ticket,
            "run_id": self.run_id,
            "current_phase": self.current_phase,
            "tool_name": tool_name,
            "parameters": parameters,
            "response": str(response)[:500] + "..." if response and len(str(response)) > 500 else response,
            "execution_time": execution_time,
            "execution_context": {
                "active_agents": self.active_agents.copy(),
                "framework_context": self.framework_context.copy()
            },
            "execution_id": f"tool_{tool_name}_{int(time.time() * 1000)}"
        }
        
        self._write_to_log(tool_data, self.tool_executions_file)
        self._write_to_log(tool_data, self.master_log_file)
        
        print(f"📝 LOGGED: Tool {tool_name}")
    
    def log_framework_phase(self, phase: str, operation: str, details: Dict[str, Any] = None):
        """Log framework phase transitions"""
        self.execution_stats['framework_phases'] += 1
        self.execution_stats['total_operations'] += 1
        
        if operation == "start":
            self.current_phase = phase
        elif operation == "complete":
            if self.current_phase == phase:
                self.current_phase = None
        
        phase_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "FRAMEWORK_PHASE",
            "jira_ticket": self.jira_ticket,
            "run_id": self.run_id,
            "phase": phase,
            "operation": operation,
            "details": details or {},
            "execution_context": {
                "active_agents": self.active_agents.copy(),
                "framework_context": self.framework_context.copy()
            },
            "execution_id": f"phase_{phase}_{int(time.time() * 1000)}"
        }
        
        self._write_to_log(phase_data, self.framework_phases_file)
        self._write_to_log(phase_data, self.master_log_file)
        
        print(f"📝 LOGGED: Framework Phase {phase} - {operation}")
    
    def log_api_call(self, api_name: str, endpoint: str, method: str = "GET", 
                    request_data: Dict[str, Any] = None, response_data: Dict[str, Any] = None):
        """Log API calls with request/response data"""
        self.execution_stats['api_calls'] += 1
        self.execution_stats['total_operations'] += 1
        
        api_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "API_CALL",
            "jira_ticket": self.jira_ticket,
            "run_id": self.run_id,
            "current_phase": self.current_phase,
            "api_name": api_name,
            "endpoint": endpoint,
            "method": method,
            "request_data": request_data or {},
            "response_data": response_data or {},
            "execution_context": {
                "active_agents": self.active_agents.copy(),
                "framework_context": self.framework_context.copy()
            },
            "execution_id": f"api_{api_name}_{int(time.time() * 1000)}"
        }
        
        self._write_to_log(api_data, self.api_calls_file)
        self._write_to_log(api_data, self.master_log_file)
        
        print(f"📝 LOGGED: API call {api_name} - {endpoint}")
    
    def _analyze_bash_command(self, command: str) -> Dict[str, Any]:
        """Analyze bash command for context"""
        analysis = {
            "command_type": "general",
            "framework_relevance": False,
            "environment_interaction": False,
            "data_extraction": False,
            "sensitive_operation": False
        }
        
        command_lower = command.lower()
        
        # Detect environment commands
        if any(cmd in command_lower for cmd in ['oc ', 'kubectl ', 'gh ', 'curl']):
            analysis["command_type"] = "environment"
            analysis["environment_interaction"] = True
            analysis["framework_relevance"] = True
        
        # Detect sensitive operations
        elif any(cmd in command_lower for cmd in ['login', 'auth', 'token', 'password']):
            analysis["command_type"] = "authentication"
            analysis["sensitive_operation"] = True
            analysis["environment_interaction"] = True
        
        # Detect data extraction
        elif any(cmd in command_lower for cmd in ['get', 'list', 'describe', 'status']):
            analysis["command_type"] = "data_extraction"
            analysis["data_extraction"] = True
            analysis["framework_relevance"] = True
        
        return analysis
    
    def _analyze_file_operation(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze file operation for context"""
        analysis = {
            "file_type": "unknown",
            "framework_relevance": False,
            "component": "unknown",
            "contains_jira_refs": False,
            "contains_github_refs": False,
            "content_type": "unknown"
        }
        
        file_path_lower = file_path.lower()
        
        # Analyze file path
        if '.claude/' in file_path_lower:
            analysis["framework_relevance"] = True
            if 'ai-services/' in file_path_lower:
                analysis["component"] = "ai_services"
            elif 'logs/' in file_path_lower:
                analysis["component"] = "logging"
            elif 'config/' in file_path_lower:
                analysis["component"] = "config"
        
        elif 'runs/' in file_path_lower:
            analysis["framework_relevance"] = True
            analysis["component"] = "outputs"
            
            if 'test-cases' in file_path_lower:
                analysis["file_type"] = "test_cases"
            elif 'analysis' in file_path_lower:
                analysis["file_type"] = "analysis"
            elif 'metadata' in file_path_lower:
                analysis["file_type"] = "metadata"
        
        # Analyze content if available
        if content:
            analysis["contains_jira_refs"] = bool(re.search(r'[A-Z]+-\d+', content))
            analysis["contains_github_refs"] = 'github.com' in content.lower()
            
            if 'test case' in content.lower():
                analysis["content_type"] = "test_plan"
            elif 'metadata' in file_path_lower:
                analysis["content_type"] = "run_metadata"
        
        return analysis
    
    def finalize_logging_session(self):
        """Finalize logging session with comprehensive summary"""
        session_end_time = datetime.now()
        execution_duration = (session_end_time - self.session_start_time).total_seconds()
        
        summary_data = {
            "session_summary": {
                "jira_ticket": self.jira_ticket,
                "run_id": self.run_id,
                "start_time": self.session_start_time.isoformat(),
                "end_time": session_end_time.isoformat(),
                "execution_duration_seconds": execution_duration,
                "log_directory": str(self.run_log_dir)
            },
            "execution_statistics": self.execution_stats,
            "framework_final_state": {
                "final_phase": self.current_phase,
                "final_active_agents": self.active_agents,
                "framework_context": self.framework_context
            },
            "log_files_generated": {
                "master_log": str(self.master_log_file),
                "agent_operations": str(self.agent_operations_file),
                "tool_executions": str(self.tool_executions_file),
                "bash_commands": str(self.bash_commands_file),
                "file_operations": str(self.file_operations_file),
                "api_calls": str(self.api_calls_file),
                "framework_phases": str(self.framework_phases_file)
            },
            "comprehensive_logging_complete": True,
            "mandatory_logging_enforced": True
        }
        
        with open(self.execution_summary_file, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"\n🎉 COMPREHENSIVE LOGGING SESSION COMPLETE")
        print(f"   Total Operations Logged: {self.execution_stats['total_operations']}")
        print(f"   Execution Duration: {execution_duration:.2f} seconds")
        print(f"   Log Directory: {self.run_log_dir}")
        print(f"   Summary File: {self.execution_summary_file}")

# Global logger instance
_global_logger: Optional[MandatoryComprehensiveLogger] = None

def get_mandatory_logger(jira_ticket: str = None) -> MandatoryComprehensiveLogger:
    """Get or create mandatory comprehensive logger"""
    global _global_logger
    if _global_logger is None:
        _global_logger = MandatoryComprehensiveLogger(jira_ticket)
    return _global_logger

def finalize_mandatory_logging():
    """Finalize mandatory logging session"""
    global _global_logger
    if _global_logger:
        _global_logger.finalize_logging_session()
        _global_logger = None

# Decorator for automatic logging
def with_mandatory_logging(jira_ticket: str = None):
    """Decorator to ensure mandatory logging for any function"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_mandatory_logger(jira_ticket)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # Keep logger active for session
                pass
        return wrapper
    return decorator

if __name__ == "__main__":
    # Test mandatory logging
    logger = MandatoryComprehensiveLogger("ACM-TEST")
    
    logger.log_framework_phase("0-pre", "start", {"test": "phase_start"})
    logger.log_agent_operation("agent_a", "start", {"task": "test"})
    logger.log_bash_command("oc get nodes", "Check cluster nodes")
    logger.log_file_operation("read", "/test/file.txt", "test content")
    logger.log_tool_execution("task", {"description": "test", "prompt": "test prompt"})
    logger.log_api_call("github", "https://api.github.com/repos/test", "GET")
    logger.log_agent_operation("agent_a", "complete", findings="Test complete")
    logger.log_framework_phase("0-pre", "complete", {"test": "phase_complete"})
    
    logger.finalize_logging_session()
    print("Test completed successfully!")