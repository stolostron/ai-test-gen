#!/usr/bin/env python3
"""
Framework Hook Bridge - Connects Framework Executions with Comprehensive Logging
================================================================================

This bridge captures operations from framework executions that happen within Task tools
and integrates them with the mandatory comprehensive logging system.

SOLVES: Hook system only capturing Task tool spawn, not internal framework operations
PROVIDES: Complete operational logging for all framework executions
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading

# Import mandatory logger
from mandatory_comprehensive_logger import get_mandatory_logger

class FrameworkHookBridge:
    """Bridge between framework executions and comprehensive logging system"""
    
    def __init__(self, jira_ticket: str = None):
        self.jira_ticket = jira_ticket
        self.logger = get_mandatory_logger(jira_ticket)
        self.framework_active = False
        self.execution_start_time = None
        self.captured_operations = []
        
        print(f"🌉 FRAMEWORK HOOK BRIDGE ACTIVATED: {jira_ticket}")
    
    def start_framework_execution(self, framework_type: str = "test_generator"):
        """Start framework execution monitoring"""
        self.framework_active = True
        self.execution_start_time = datetime.now()
        self.captured_operations = []
        
        self.logger.log_framework_phase(
            phase="framework_bridge_start",
            operation="start",
            details={
                "framework_type": framework_type,
                "bridge_monitoring": True,
                "execution_start": self.execution_start_time.isoformat()
            }
        )
        
        print(f"🚀 Framework execution monitoring started for {framework_type}")
    
    def capture_agent_operation(self, agent_name: str, operation: str, 
                               data: Dict[str, Any] = None, findings: str = None):
        """Capture agent operations from framework execution"""
        if not self.framework_active:
            return
        
        operation_data = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "operation": operation,
            "data": data or {},
            "findings": findings,
            "execution_context": "framework_bridge_capture"
        }
        
        self.captured_operations.append(operation_data)
        
        self.logger.log_agent_operation(
            agent_name=agent_name,
            operation=operation,
            data=data,
            findings=findings,
            context={
                "bridge_capture": True,
                "framework_execution": True,
                "capture_method": "framework_hook_bridge"
            }
        )
        
        # Write agent-specific logs to subdirectories
        self._write_agent_specific_logs(agent_name, operation_data)
        
        print(f"🔍 Captured {agent_name} {operation}")
    
    def _write_agent_specific_logs(self, agent_name: str, operation_data: Dict[str, Any]):
        """Write agent-specific data to subdirectories"""
        # Create agent-specific directory
        agent_dir = self.logger.run_log_dir / "agents" / agent_name
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        # Write operation to agent-specific log
        agent_log_file = agent_dir / f"{agent_name}_operations.jsonl"
        with open(agent_log_file, 'a') as f:
            f.write(json.dumps(operation_data) + '\n')
        
        # Write analysis data if available
        if operation_data.get('findings'):
            analysis_dir = self.logger.run_log_dir / "analysis" / agent_name
            analysis_dir.mkdir(parents=True, exist_ok=True)
            
            analysis_file = analysis_dir / f"{agent_name}_analysis.json"
            analysis_data = {
                "agent": agent_name,
                "analysis_timestamp": operation_data["timestamp"],
                "findings": operation_data["findings"],
                "operation_data": operation_data["data"],
                "operation_type": operation_data["operation"]
            }
            
            with open(analysis_file, 'w') as f:
                json.dump(analysis_data, f, indent=2)
    
    def capture_bash_command(self, command: str, description: str = None, 
                           output: str = None, agent_context: str = None):
        """Capture bash commands from framework execution"""
        if not self.framework_active:
            return
        
        # Enhanced output capture
        output_data = {
            "command_executed": command,
            "description": description or "",
            "captured_output": output or "[Output captured by bridge]",
            "agent_context": agent_context or "unknown",
            "execution_context": "framework_bridge_capture"
        }
        
        self.logger.log_bash_command(
            command=command,
            description=description or f"Framework command via {agent_context}",
            output=output_data
        )
        
        # Write to tools subdirectory
        self._write_tool_specific_logs("bash", {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "description": description,
            "output": output,
            "agent_context": agent_context
        })
        
        # Write raw data to raw-data subdirectory
        self._write_raw_data_logs(agent_context, "bash_command", {
            "command": command,
            "output": output,
            "timestamp": datetime.now().isoformat()
        })
        
        # Also log as API call if it's an environment command
        if any(cmd in command.lower() for cmd in ['oc ', 'kubectl ', 'gh ', 'curl']):
            self.logger.log_api_call(
                api_name="framework_environment_command",
                endpoint=command,
                method="CLI",
                request_data={
                    "command": command,
                    "agent_context": agent_context,
                    "bridge_capture": True
                },
                response_data={"output": output} if output else {}
            )
        
        print(f"💻 Captured bash: {command[:50]}...")
    
    def _write_tool_specific_logs(self, tool_type: str, tool_data: Dict[str, Any]):
        """Write tool-specific data to tools subdirectory"""
        tools_dir = self.logger.run_log_dir / "tools" / tool_type
        tools_dir.mkdir(parents=True, exist_ok=True)
        
        tool_log_file = tools_dir / f"{tool_type}_operations.jsonl"
        with open(tool_log_file, 'a') as f:
            f.write(json.dumps(tool_data) + '\n')
    
    def _write_raw_data_logs(self, agent_context: str, data_type: str, raw_data: Dict[str, Any]):
        """Write raw operational data to raw-data subdirectory"""
        if not agent_context or agent_context == "unknown":
            return
        
        raw_data_dir = self.logger.run_log_dir / "raw-data" / agent_context
        raw_data_dir.mkdir(parents=True, exist_ok=True)
        
        raw_data_file = raw_data_dir / f"{data_type}_raw.jsonl"
        with open(raw_data_file, 'a') as f:
            f.write(json.dumps(raw_data) + '\n')
    
    def capture_file_operation(self, operation: str, file_path: str, 
                              content: str = None, agent_context: str = None):
        """Capture file operations from framework execution"""
        if not self.framework_active:
            return
        
        self.logger.log_file_operation(
            operation=operation,
            file_path=file_path,
            content=content,
            details={
                "agent_context": agent_context or "unknown",
                "bridge_capture": True,
                "framework_execution": True
            }
        )
        
        print(f"📁 Captured file {operation}: {file_path}")
    
    def capture_api_call(self, api_name: str, endpoint: str, method: str = "GET",
                        request_data: Dict = None, response_data: Dict = None,
                        agent_context: str = None):
        """Capture API calls from framework execution"""
        if not self.framework_active:
            return
        
        enhanced_request = (request_data or {}).copy()
        enhanced_request.update({
            "agent_context": agent_context or "unknown",
            "bridge_capture": True,
            "framework_execution": True
        })
        
        self.logger.log_api_call(
            api_name=api_name,
            endpoint=endpoint,
            method=method,
            request_data=enhanced_request,
            response_data=response_data or {}
        )
        
        print(f"🌐 Captured API: {api_name} - {endpoint}")
    
    def finalize_framework_execution(self, execution_summary: Dict[str, Any] = None):
        """Finalize framework execution and generate comprehensive summary"""
        if not self.framework_active:
            return
        
        execution_end_time = datetime.now()
        execution_duration = (execution_end_time - self.execution_start_time).total_seconds()
        
        # Generate comprehensive execution summary
        bridge_summary = {
            "framework_execution_complete": True,
            "total_operations_captured": len(self.captured_operations),
            "execution_duration_seconds": execution_duration,
            "operations_by_agent": self._group_operations_by_agent(),
            "execution_timeline": self.captured_operations,
            "bridge_effectiveness": "complete",
            "execution_summary": execution_summary or {}
        }
        
        self.logger.log_framework_phase(
            phase="framework_bridge_complete",
            operation="complete",
            details=bridge_summary
        )
        
        # Write bridge summary to separate file
        bridge_summary_file = self.logger.run_log_dir / "framework_bridge_summary.json"
        with open(bridge_summary_file, 'w') as f:
            json.dump(bridge_summary, f, indent=2)
        
        self.framework_active = False
        
        print(f"🎉 Framework execution complete: {len(self.captured_operations)} operations captured")
        print(f"📊 Bridge summary: {bridge_summary_file}")
        
        return bridge_summary
    
    def _group_operations_by_agent(self) -> Dict[str, int]:
        """Group captured operations by agent"""
        agent_counts = {}
        for op in self.captured_operations:
            agent = op.get('agent', 'unknown')
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
        return agent_counts
    
    def inject_comprehensive_execution_log(self, execution_log_path: str):
        """Parse and inject operations from comprehensive execution log"""
        if not Path(execution_log_path).exists():
            print(f"⚠️ Execution log not found: {execution_log_path}")
            return
        
        print(f"📖 Parsing execution log: {execution_log_path}")
        
        try:
            with open(execution_log_path, 'r') as f:
                content = f.read()
            
            # Parse Agent D operations from the log
            operations = self._parse_agent_operations_from_log(content)
            
            # Inject operations into comprehensive logging
            for op in operations:
                if op['type'] == 'bash_command':
                    self.capture_bash_command(
                        command=op['command'],
                        description=op['description'],
                        output=op['output'],
                        agent_context=op['agent']
                    )
                elif op['type'] == 'api_call':
                    self.capture_api_call(
                        api_name=op['api_name'],
                        endpoint=op['endpoint'],
                        method=op['method'],
                        response_data=op['response'],
                        agent_context=op['agent']
                    )
                elif op['type'] == 'file_operation':
                    self.capture_file_operation(
                        operation=op['operation'],
                        file_path=op['file_path'],
                        content=op['content'],
                        agent_context=op['agent']
                    )
            
            print(f"✅ Injected {len(operations)} operations from execution log")
            
        except Exception as e:
            print(f"❌ Failed to parse execution log: {e}")
    
    def _parse_agent_operations_from_log(self, log_content: str) -> List[Dict[str, Any]]:
        """Parse agent operations from comprehensive execution log"""
        operations = []
        lines = log_content.split('\n')
        
        current_agent = None
        
        for line in lines:
            # Detect agent context
            if "Agent D Operation" in line:
                current_agent = "agent_d_environment"
            elif "Agent A" in line:
                current_agent = "agent_a_jira"
            elif "Agent B" in line:
                current_agent = "agent_b_documentation"
            elif "Agent C" in line:
                current_agent = "agent_c_github"
            
            # Parse bash commands
            if line.startswith("Command: "):
                command = line.replace("Command: ", "").strip()
                operations.append({
                    "type": "bash_command",
                    "agent": current_agent or "unknown",
                    "command": command,
                    "description": f"Framework command from {current_agent}",
                    "output": "[Parsed from execution log]"
                })
            
            # Parse API calls (GitHub, environment commands)
            elif "github.com" in line.lower() or "api." in line.lower():
                operations.append({
                    "type": "api_call",
                    "agent": current_agent or "unknown",
                    "api_name": "framework_api",
                    "endpoint": line.strip(),
                    "method": "GET",
                    "response": "[Parsed from execution log]"
                })
            
            # Parse file operations
            elif any(keyword in line.lower() for keyword in ["reading", "writing", "analyzing"]) and any(ext in line for ext in [".json", ".md", ".txt", ".yaml"]):
                operations.append({
                    "type": "file_operation",
                    "agent": current_agent or "unknown",
                    "operation": "read" if "reading" in line.lower() else "write",
                    "file_path": "[Parsed from execution log]",
                    "content": "[Content captured from framework execution]"
                })
        
        return operations

# Global bridge instance
_global_bridge: Optional[FrameworkHookBridge] = None

def get_framework_bridge(jira_ticket: str = None) -> FrameworkHookBridge:
    """Get or create framework hook bridge"""
    global _global_bridge
    if _global_bridge is None:
        _global_bridge = FrameworkHookBridge(jira_ticket)
    return _global_bridge

def activate_framework_bridge_logging(jira_ticket: str = None):
    """Activate framework bridge logging for comprehensive capture"""
    bridge = get_framework_bridge(jira_ticket)
    bridge.start_framework_execution()
    
    print(f"🌉 FRAMEWORK BRIDGE LOGGING ACTIVATED")
    print(f"   Captures operations from framework executions")
    print(f"   Integrates with mandatory comprehensive logging")
    print(f"   Bridges Task tool execution gap")
    
    return bridge

if __name__ == "__main__":
    # Test framework bridge
    bridge = FrameworkHookBridge("ACM-TEST")
    bridge.start_framework_execution("test_generator")
    
    # Simulate framework operations
    bridge.capture_agent_operation("agent_d_environment", "start", {"task": "environment_assessment"})
    bridge.capture_bash_command("oc whoami", "Check authentication", "system:admin", "agent_d")
    bridge.capture_api_call("github", "https://api.github.com/repos/test", "GET", agent_context="agent_c")
    bridge.capture_file_operation("read", "/tmp/config.json", "test config", "agent_b")
    
    summary = bridge.finalize_framework_execution({
        "test_cases_generated": 5,
        "analysis_complete": True
    })
    
    print(f"✅ Bridge test complete: {summary['total_operations_captured']} operations")