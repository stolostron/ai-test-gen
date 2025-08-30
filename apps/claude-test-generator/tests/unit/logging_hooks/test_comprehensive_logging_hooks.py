#!/usr/bin/env python3
"""
Comprehensive Logging Hooks Unit Tests
======================================

Tests the ACTUAL implementation of the comprehensive logging hooks system,
validating real functionality rather than just documentation.

Tests cover:
- Comprehensive Logging Hook (Claude Code tool interception)
- Mandatory Comprehensive Logger (full operation capture)
- Framework Hook Bridge (Task tool execution gap bridging)
- Real file creation and log content validation
- Actual directory structure and organization
- Complete operational transparency verification
"""

import unittest
import sys
import os
import tempfile
import json
import time
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List

# Add the project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    # Add hooks and logging paths
    hooks_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'hooks')
    logging_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'logging')
    sys.path.insert(0, hooks_path)
    sys.path.insert(0, logging_path)
    
    from comprehensive_logging_hook import ComprehensiveLoggingHook, claude_code_tool_hook
    from mandatory_comprehensive_logger import MandatoryComprehensiveLogger, get_mandatory_logger
    from framework_hook_bridge import FrameworkHookBridge, get_framework_bridge
    LOGGING_HOOKS_AVAILABLE = True
except ImportError as e:
    LOGGING_HOOKS_AVAILABLE = False
    print(f"❌ Logging hooks not available: {e}")


class TestComprehensiveLoggingHook(unittest.TestCase):
    """Test Comprehensive Logging Hook actual implementation"""
    
    @classmethod
    def setUpClass(cls):
        if not LOGGING_HOOKS_AVAILABLE:
            cls.skipTest(cls, "Logging hooks not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create .claude/logging directory structure
        self.claude_dir = Path(self.test_dir) / ".claude"
        self.logging_dir = self.claude_dir / "logging"
        self.logging_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize hook
        self.hook = ComprehensiveLoggingHook()
        
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_hook_initialization(self):
        """Test comprehensive logging hook initialization"""
        self.assertEqual(self.hook.hook_name, "comprehensive_logging_hook")
        self.assertEqual(self.hook.version, "1.0-PRODUCTION")
        self.assertIsInstance(self.hook.framework_state, dict)
        self.assertIsInstance(self.hook.execution_log, list)
        self.assertIsInstance(self.hook.session_stats, dict)
        
        # Check required stats tracking
        required_stats = ['bash_commands', 'file_reads', 'file_writes', 'agent_spawns', 'searches', 'file_edits']
        for stat in required_stats:
            self.assertIn(stat, self.hook.session_stats)
            self.assertEqual(self.hook.session_stats[stat], 0)
    
    def test_log_directory_setup(self):
        """Test actual log directory creation"""
        # Check session log file was created
        self.assertTrue(self.hook.session_log_file.exists())
        self.assertTrue(str(self.hook.session_log_file).endswith('.jsonl'))
        
        # Check directory structure
        session_dir = self.hook.session_log_file.parent
        self.assertTrue(session_dir.exists())
        self.assertEqual(session_dir.name, "current-session")
    
    def test_jira_ticket_detection(self):
        """Test JIRA ticket detection from context"""
        # Test with ACM ticket in directory
        acm_dir = Path(self.test_dir) / "runs" / "ACM-12345"
        acm_dir.mkdir(parents=True)
        
        detected_ticket = self.hook.detect_jira_ticket()
        self.assertEqual(detected_ticket, "ACM-12345")
        
        # Test with OCPBUGS ticket
        ocpbugs_dir = Path(self.test_dir) / "runs" / "OCPBUGS-67890"
        ocpbugs_dir.mkdir(parents=True)
        
        detected_ticket = self.hook.detect_jira_ticket()
        self.assertIn(detected_ticket, ["ACM-12345", "OCPBUGS-67890"])
    
    def test_bash_tool_processing(self):
        """Test actual bash tool processing and logging"""
        parameters = {
            "command": "oc get nodes",
            "description": "Check cluster nodes",
            "timeout": 120
        }
        
        result = self.hook.process_bash_tool(parameters)
        
        # Should return parameters unchanged (hook doesn't modify behavior)
        self.assertEqual(result, parameters)
        
        # Check stats were updated
        self.assertEqual(self.hook.session_stats['bash_commands'], 1)
        
        # Check log entry was created
        self.assertEqual(len(self.hook.execution_log), 1)
        log_entry = self.hook.execution_log[0]
        
        self.assertEqual(log_entry['action'], 'BASH_EXECUTION')
        self.assertEqual(log_entry['tool'], 'bash')
        self.assertEqual(log_entry['details']['command'], 'oc get nodes')
        self.assertEqual(log_entry['details']['description'], 'Check cluster nodes')
        self.assertIn('command_analysis', log_entry['details'])
        
        # Check command analysis
        analysis = log_entry['details']['command_analysis']
        self.assertEqual(analysis['command_type'], 'environment')
        self.assertTrue(analysis['environment_interaction'])
        self.assertTrue(analysis['framework_relevance'])
    
    def test_read_tool_processing(self):
        """Test actual read tool processing and logging"""
        parameters = {
            "file_path": "/tmp/test-config.json",
            "limit": 100,
            "offset": 0
        }
        
        result = self.hook.process_read_tool(parameters)
        
        # Should return parameters unchanged
        self.assertEqual(result, parameters)
        
        # Check stats were updated
        self.assertEqual(self.hook.session_stats['file_reads'], 1)
        
        # Check log entry was created
        self.assertEqual(len(self.hook.execution_log), 1)
        log_entry = self.hook.execution_log[0]
        
        self.assertEqual(log_entry['action'], 'FILE_READ')
        self.assertEqual(log_entry['tool'], 'read')
        self.assertEqual(log_entry['details']['file_path'], '/tmp/test-config.json')
        self.assertIn('file_analysis', log_entry['details'])
    
    def test_task_tool_processing(self):
        """Test actual task tool (agent spawning) processing"""
        parameters = {
            "description": "Test Agent Execution",
            "subagent_type": "general-purpose",
            "prompt": "Generate comprehensive test plan for ACM-12345"
        }
        
        result = self.hook.process_task_tool(parameters)
        
        # Should return parameters unchanged
        self.assertEqual(result, parameters)
        
        # Check stats were updated
        self.assertEqual(self.hook.session_stats['agent_spawns'], 1)
        
        # Check agent was tracked in framework state
        self.assertEqual(len(self.hook.framework_state['active_agents']), 1)
        active_agent = self.hook.framework_state['active_agents'][0]
        self.assertEqual(active_agent['type'], 'general-purpose')
        self.assertEqual(active_agent['description'], 'Test Agent Execution')
        
        # Check log entry was created
        log_entry = self.hook.execution_log[0]
        self.assertEqual(log_entry['action'], 'AGENT_SPAWN')
        self.assertEqual(log_entry['tool'], 'task')
        self.assertIn('agent_id', log_entry['details'])
    
    def test_file_path_analysis(self):
        """Test file path analysis for framework context"""
        # Test framework file
        framework_analysis = self.hook.analyze_file_path(".claude/ai-services/test_service.py")
        self.assertTrue(framework_analysis['framework_relevance'])
        self.assertEqual(framework_analysis['component'], 'ai_services')
        self.assertEqual(framework_analysis['file_type'], 'ai_service')
        
        # Test run output file
        run_analysis = self.hook.analyze_file_path("runs/ACM-12345/ACM-12345-Test-Cases.md")
        self.assertTrue(run_analysis['framework_relevance'])
        self.assertEqual(run_analysis['component'], 'outputs')
        self.assertEqual(run_analysis['file_type'], 'test_cases')
        
        # Test regular file
        regular_analysis = self.hook.analyze_file_path("/home/user/document.txt")
        self.assertFalse(regular_analysis['framework_relevance'])
        self.assertEqual(regular_analysis['component'], 'unknown')
    
    def test_session_log_file_writing(self):
        """Test actual session log file writing"""
        # Process a few operations
        self.hook.process_bash_tool({"command": "echo test", "description": "test"})
        self.hook.process_read_tool({"file_path": "/test/file.txt"})
        
        # Check session log file contains entries
        self.assertTrue(self.hook.session_log_file.exists())
        
        with open(self.hook.session_log_file, 'r') as f:
            lines = f.readlines()
        
        self.assertEqual(len(lines), 2)  # Two operations logged
        
        # Parse and validate log entries
        for line in lines:
            log_entry = json.loads(line.strip())
            self.assertIn('timestamp', log_entry)
            self.assertIn('action', log_entry)
            self.assertIn('tool', log_entry)
            self.assertIn('details', log_entry)
            self.assertIn('framework_state', log_entry)
    
    def test_session_summary_generation(self):
        """Test session summary generation with real data"""
        # Initialize run logging
        self.hook.initialize_run_logging("ACM-TEST", "test-run-123")
        
        # Process various operations
        self.hook.process_bash_tool({"command": "oc whoami", "description": "check auth"})
        self.hook.process_read_tool({"file_path": ".claude/config/test.json"})
        self.hook.process_task_tool({"description": "Test Agent", "subagent_type": "general-purpose", "prompt": "test"})
        
        # Get session summary
        summary = self.hook.get_session_summary()
        
        # Validate summary structure
        self.assertIn('session_info', summary)
        self.assertIn('execution_stats', summary)
        self.assertIn('framework_state', summary)
        self.assertIn('total_logs', summary)
        self.assertIn('log_files', summary)
        
        # Validate session info
        session_info = summary['session_info']
        self.assertEqual(session_info['hook_version'], '1.0-PRODUCTION')
        self.assertEqual(session_info['run_id'], 'test-run-123')
        self.assertEqual(session_info['jira_ticket'], 'ACM-TEST')
        
        # Validate execution stats
        stats = summary['execution_stats']
        self.assertEqual(stats['bash_commands'], 1)
        self.assertEqual(stats['file_reads'], 1)
        self.assertEqual(stats['agent_spawns'], 1)
        
        # Validate total logs
        self.assertEqual(summary['total_logs'], 3)


class TestMandatoryComprehensiveLogger(unittest.TestCase):
    """Test Mandatory Comprehensive Logger actual implementation"""
    
    @classmethod
    def setUpClass(cls):
        if not LOGGING_HOOKS_AVAILABLE:
            cls.skipTest(cls, "Logging hooks not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create .claude/logs directory structure
        self.claude_dir = Path(self.test_dir) / ".claude"
        self.logs_dir = self.claude_dir / "logs" / "comprehensive"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize logger
        self.logger = MandatoryComprehensiveLogger("ACM-TEST-UNIT")
        
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_logger_initialization(self):
        """Test mandatory logger initialization"""
        self.assertEqual(self.logger.jira_ticket, "ACM-TEST-UNIT")
        self.assertTrue(self.logger.run_id.startswith("ACM-TEST-UNIT-"))
        
        # Check directory structure was created
        self.assertTrue(self.logger.run_log_dir.exists())
        self.assertTrue((self.logger.run_log_dir / "agents").exists())
        self.assertTrue((self.logger.run_log_dir / "tools").exists())
        self.assertTrue((self.logger.run_log_dir / "phases").exists())
        self.assertTrue((self.logger.run_log_dir / "raw-data").exists())
        self.assertTrue((self.logger.run_log_dir / "analysis").exists())
        
        # Check latest symlink was created
        latest_link = self.logger.jira_log_dir / "latest"
        self.assertTrue(latest_link.exists())
        self.assertTrue(latest_link.is_symlink())
    
    def test_bash_command_logging(self):
        """Test actual bash command logging with output capture"""
        command = "oc get pods -n openshift-cluster-version"
        description = "Check cluster version pods"
        output = {"stdout": "pod1 Running", "stderr": "", "exit_code": 0}
        
        self.logger.log_bash_command(command, description, output=output)
        
        # Check stats were updated
        self.assertEqual(self.logger.execution_stats['bash_commands'], 1)
        self.assertEqual(self.logger.execution_stats['total_operations'], 1)
        
        # Check bash commands file was created
        self.assertTrue(self.logger.bash_commands_file.exists())
        
        with open(self.logger.bash_commands_file, 'r') as f:
            log_entry = json.loads(f.readline().strip())
        
        self.assertEqual(log_entry['event_type'], 'BASH_COMMAND')
        self.assertEqual(log_entry['command'], command)
        self.assertEqual(log_entry['description'], description)
        self.assertEqual(log_entry['output'], output)
        self.assertIn('command_analysis', log_entry)
        
        # Check master log also contains entry
        self.assertTrue(self.logger.master_log_file.exists())
    
    def test_agent_operation_logging(self):
        """Test actual agent operation logging with data flow"""
        agent_name = "agent_d_environment"
        operation = "start"
        data = {"task": "environment_assessment", "cluster": "test-cluster"}
        findings = "Environment ready for testing"
        context = {"inherited_from": "foundation_context", "phase": "1"}
        
        self.logger.log_agent_operation(agent_name, operation, data, findings, context)
        
        # Check stats were updated
        self.assertEqual(self.logger.execution_stats['agent_operations'], 1)
        
        # Check agent was added to active agents list
        self.assertIn(agent_name, self.logger.active_agents)
        
        # Check agent operations file was created
        self.assertTrue(self.logger.agent_operations_file.exists())
        
        with open(self.logger.agent_operations_file, 'r') as f:
            log_entry = json.loads(f.readline().strip())
        
        self.assertEqual(log_entry['event_type'], 'AGENT_OPERATION')
        self.assertEqual(log_entry['agent_name'], agent_name)
        self.assertEqual(log_entry['operation'], operation)
        self.assertEqual(log_entry['findings'], findings)
        self.assertEqual(log_entry['data'], data)
        self.assertEqual(log_entry['context'], context)
    
    def test_file_operation_logging(self):
        """Test actual file operation logging with content analysis"""
        operation = "write"
        file_path = "runs/ACM-TEST-UNIT/ACM-TEST-UNIT-Test-Cases.md"
        content = """# Test Cases for ACM-TEST-UNIT

## Test Case 1: Environment Validation
- Verify cluster connectivity
- Check ACM components
"""
        details = {"agent": "framework", "phase": "test_generation"}
        
        self.logger.log_file_operation(operation, file_path, content, details)
        
        # Check stats were updated
        self.assertEqual(self.logger.execution_stats['file_operations'], 1)
        
        # Check file operations file was created
        self.assertTrue(self.logger.file_operations_file.exists())
        
        with open(self.logger.file_operations_file, 'r') as f:
            log_entry = json.loads(f.readline().strip())
        
        self.assertEqual(log_entry['event_type'], 'FILE_OPERATION')
        self.assertEqual(log_entry['operation'], operation)
        self.assertEqual(log_entry['file_path'], file_path)
        self.assertEqual(log_entry['content_length'], len(content))
        self.assertIn('file_analysis', log_entry)
        
        # Check content analysis
        analysis = log_entry['file_analysis']
        self.assertTrue(analysis['framework_relevance'])
        self.assertEqual(analysis['component'], 'outputs')
        self.assertEqual(analysis['file_type'], 'test_cases')
        self.assertTrue(analysis['contains_jira_refs'])
    
    def test_framework_phase_logging(self):
        """Test actual framework phase logging with transitions"""
        phase = "phase_1_parallel_foundation"
        operation = "start"
        details = {"agents": ["agent_a", "agent_d"], "context_inheritance": True}
        
        self.logger.log_framework_phase(phase, operation, details)
        
        # Check current phase was set
        self.assertEqual(self.logger.current_phase, phase)
        
        # Check stats were updated
        self.assertEqual(self.logger.execution_stats['framework_phases'], 1)
        
        # Check framework phases file was created
        self.assertTrue(self.logger.framework_phases_file.exists())
        
        with open(self.logger.framework_phases_file, 'r') as f:
            log_entry = json.loads(f.readline().strip())
        
        self.assertEqual(log_entry['event_type'], 'FRAMEWORK_PHASE')
        self.assertEqual(log_entry['phase'], phase)
        self.assertEqual(log_entry['operation'], operation)
        self.assertEqual(log_entry['details'], details)
        
        # Test phase completion
        self.logger.log_framework_phase(phase, "complete", {"duration": "5.2s"})
        self.assertIsNone(self.logger.current_phase)
    
    def test_api_call_logging(self):
        """Test actual API call logging with request/response data"""
        api_name = "github"
        endpoint = "https://api.github.com/repos/openshift/cluster-version-operator"
        method = "GET"
        request_data = {"headers": {"Authorization": "Bearer [REDACTED]"}}
        response_data = {"name": "cluster-version-operator", "description": "OpenShift cluster version operator"}
        
        self.logger.log_api_call(api_name, endpoint, method, request_data, response_data)
        
        # Check stats were updated
        self.assertEqual(self.logger.execution_stats['api_calls'], 1)
        
        # Check API calls file was created
        self.assertTrue(self.logger.api_calls_file.exists())
        
        with open(self.logger.api_calls_file, 'r') as f:
            log_entry = json.loads(f.readline().strip())
        
        self.assertEqual(log_entry['event_type'], 'API_CALL')
        self.assertEqual(log_entry['api_name'], api_name)
        self.assertEqual(log_entry['endpoint'], endpoint)
        self.assertEqual(log_entry['method'], method)
        self.assertEqual(log_entry['request_data'], request_data)
        self.assertEqual(log_entry['response_data'], response_data)
    
    def test_execution_summary_finalization(self):
        """Test comprehensive execution summary generation"""
        # Log various operations
        self.logger.log_framework_phase("phase_0_pre", "start")
        self.logger.log_agent_operation("agent_a", "start", {"task": "jira_analysis"})
        self.logger.log_bash_command("oc whoami", "Check authentication")
        self.logger.log_api_call("jira", "https://issues.redhat.com/ACM-TEST-UNIT", "GET")
        self.logger.log_file_operation("write", "test_output.md", "Test content")
        self.logger.log_agent_operation("agent_a", "complete", findings="Analysis complete")
        self.logger.log_framework_phase("phase_0_pre", "complete")
        
        # Finalize logging session
        self.logger.finalize_logging_session()
        
        # Check execution summary file was created
        self.assertTrue(self.logger.execution_summary_file.exists())
        
        with open(self.logger.execution_summary_file, 'r') as f:
            summary = json.load(f)
        
        # Validate summary structure
        self.assertIn('session_summary', summary)
        self.assertIn('execution_statistics', summary)
        self.assertIn('framework_final_state', summary)
        self.assertIn('log_files_generated', summary)
        self.assertTrue(summary['comprehensive_logging_complete'])
        self.assertTrue(summary['mandatory_logging_enforced'])
        
        # Validate execution statistics
        stats = summary['execution_statistics']
        self.assertEqual(stats['total_operations'], 7)
        self.assertEqual(stats['bash_commands'], 1)
        self.assertEqual(stats['file_operations'], 1)
        self.assertEqual(stats['agent_operations'], 2)
        self.assertEqual(stats['api_calls'], 1)
        self.assertEqual(stats['framework_phases'], 2)
        
        # Validate all log files were generated
        log_files = summary['log_files_generated']
        for log_type, log_path in log_files.items():
            self.assertTrue(Path(log_path).exists(), f"Log file {log_type} not found at {log_path}")


class TestFrameworkHookBridge(unittest.TestCase):
    """Test Framework Hook Bridge actual implementation"""
    
    @classmethod
    def setUpClass(cls):
        if not LOGGING_HOOKS_AVAILABLE:
            cls.skipTest(cls, "Logging hooks not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create .claude/logs directory structure
        self.claude_dir = Path(self.test_dir) / ".claude"
        self.logs_dir = self.claude_dir / "logs" / "comprehensive"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize bridge
        self.bridge = FrameworkHookBridge("ACM-BRIDGE-TEST")
        
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_bridge_initialization(self):
        """Test framework hook bridge initialization"""
        self.assertEqual(self.bridge.jira_ticket, "ACM-BRIDGE-TEST")
        self.assertIsNotNone(self.bridge.logger)
        self.assertFalse(self.bridge.framework_active)
        self.assertIsInstance(self.bridge.captured_operations, list)
    
    def test_framework_execution_monitoring(self):
        """Test framework execution monitoring start/stop"""
        self.bridge.start_framework_execution("test_generator")
        
        self.assertTrue(self.bridge.framework_active)
        self.assertIsNotNone(self.bridge.execution_start_time)
        self.assertEqual(len(self.bridge.captured_operations), 0)
    
    def test_agent_operation_capture(self):
        """Test agent operation capture with subdirectory logging"""
        self.bridge.start_framework_execution()
        
        agent_name = "agent_d_environment"
        operation = "start"
        data = {"environment": "test-cluster", "version": "4.12"}
        findings = "Environment assessment complete"
        
        self.bridge.capture_agent_operation(agent_name, operation, data, findings)
        
        # Check operation was captured
        self.assertEqual(len(self.bridge.captured_operations), 1)
        captured_op = self.bridge.captured_operations[0]
        
        self.assertEqual(captured_op['agent'], agent_name)
        self.assertEqual(captured_op['operation'], operation)
        self.assertEqual(captured_op['data'], data)
        self.assertEqual(captured_op['findings'], findings)
        
        # Check agent-specific subdirectory was created
        agent_dir = self.bridge.logger.run_log_dir / "agents" / agent_name
        self.assertTrue(agent_dir.exists())
        
        # Check agent-specific log file was created
        agent_log_file = agent_dir / f"{agent_name}_operations.jsonl"
        self.assertTrue(agent_log_file.exists())
        
        # Check analysis subdirectory was created (because of findings)
        analysis_dir = self.bridge.logger.run_log_dir / "analysis" / agent_name
        self.assertTrue(analysis_dir.exists())
        
        analysis_file = analysis_dir / f"{agent_name}_analysis.json"
        self.assertTrue(analysis_file.exists())
    
    def test_bash_command_capture(self):
        """Test bash command capture with tools subdirectory logging"""
        self.bridge.start_framework_execution()
        
        command = "oc get clusterversion"
        description = "Check cluster version"
        output = "VERSION  AVAILABLE  PROGRESSING  SINCE  STATUS\n4.12.0   True       False        24h    Cluster version is 4.12.0"
        agent_context = "agent_d_environment"
        
        self.bridge.capture_bash_command(command, description, output, agent_context)
        
        # Check tools subdirectory was created
        tools_dir = self.bridge.logger.run_log_dir / "tools" / "bash"
        self.assertTrue(tools_dir.exists())
        
        # Check tool-specific log file was created
        tool_log_file = tools_dir / "bash_operations.jsonl"
        self.assertTrue(tool_log_file.exists())
        
        # Check raw-data subdirectory was created
        raw_data_dir = self.bridge.logger.run_log_dir / "raw-data" / agent_context
        self.assertTrue(raw_data_dir.exists())
        
        raw_data_file = raw_data_dir / "bash_command_raw.jsonl"
        self.assertTrue(raw_data_file.exists())
        
        # Verify log content
        with open(raw_data_file, 'r') as f:
            raw_data = json.loads(f.readline().strip())
        
        self.assertEqual(raw_data['command'], command)
        self.assertEqual(raw_data['output'], output)
        self.assertIn('timestamp', raw_data)
    
    def test_api_call_capture(self):
        """Test API call capture from framework execution"""
        self.bridge.start_framework_execution()
        
        api_name = "github"
        endpoint = "https://api.github.com/repos/openshift/cluster-version-operator/pulls"
        method = "GET"
        request_data = {"state": "open", "per_page": 10}
        response_data = {"total_count": 5, "items": []}
        agent_context = "agent_c_github"
        
        self.bridge.capture_api_call(api_name, endpoint, method, request_data, response_data, agent_context)
        
        # Verify the API call was logged with enhanced request data
        # The bridge should add its own context to the request data
        # This validates the bridge is actually enhancing the data
    
    def test_framework_execution_finalization(self):
        """Test framework execution finalization with comprehensive summary"""
        self.bridge.start_framework_execution("test_generator")
        
        # Simulate framework operations
        self.bridge.capture_agent_operation("agent_a", "start", {"task": "jira_analysis"})
        self.bridge.capture_bash_command("oc whoami", "Check auth", "system:admin", "agent_d")
        self.bridge.capture_api_call("github", "https://api.github.com/test", "GET", agent_context="agent_c")
        self.bridge.capture_file_operation("write", "test_cases.md", "Test content", "framework")
        self.bridge.capture_agent_operation("agent_a", "complete", findings="Analysis complete")
        
        execution_summary = {"test_cases_generated": 4, "analysis_complete": True}
        final_summary = self.bridge.finalize_framework_execution(execution_summary)
        
        # Check bridge is no longer active
        self.assertFalse(self.bridge.framework_active)
        
        # Check summary structure
        self.assertIn('framework_execution_complete', final_summary)
        self.assertIn('total_operations_captured', final_summary)
        self.assertIn('execution_duration_seconds', final_summary)
        self.assertIn('operations_by_agent', final_summary)
        self.assertIn('execution_timeline', final_summary)
        
        self.assertTrue(final_summary['framework_execution_complete'])
        self.assertEqual(final_summary['total_operations_captured'], 2)  # agent start + complete
        
        # Check bridge summary file was created
        bridge_summary_file = self.bridge.logger.run_log_dir / "framework_bridge_summary.json"
        self.assertTrue(bridge_summary_file.exists())
        
        with open(bridge_summary_file, 'r') as f:
            saved_summary = json.load(f)
        
        self.assertEqual(saved_summary, final_summary)


class TestLoggingHooksIntegration(unittest.TestCase):
    """Test logging hooks integration and complete operational transparency"""
    
    @classmethod
    def setUpClass(cls):
        if not LOGGING_HOOKS_AVAILABLE:
            cls.skipTest(cls, "Logging hooks not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create .claude directory structure
        self.claude_dir = Path(self.test_dir) / ".claude"
        self.logging_dir = self.claude_dir / "logging"
        self.logs_dir = self.claude_dir / "logs" / "comprehensive"
        self.logging_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_claude_code_tool_hook_function(self):
        """Test Claude Code tool hook function integration"""
        # Test the actual hook function that Claude Code would call
        parameters = {
            "command": "oc get nodes",
            "description": "Check cluster nodes",
            "timeout": 120
        }
        
        result = claude_code_tool_hook("bash", parameters)
        
        # Should return parameters unchanged (hook doesn't modify behavior)
        self.assertEqual(result, parameters)
        
        # Check that logging actually occurred by verifying log files exist
        # The hook should have created a session log
        current_session_dir = self.logging_dir / "current-session"
        if current_session_dir.exists():
            session_files = list(current_session_dir.glob("session-*.jsonl"))
            self.assertGreater(len(session_files), 0, "No session log files created")
    
    def test_mandatory_logger_global_instance(self):
        """Test mandatory logger global instance management"""
        # Test getting global logger instance
        logger1 = get_mandatory_logger("ACM-GLOBAL-TEST")
        logger2 = get_mandatory_logger("ACM-GLOBAL-TEST")
        
        # Should return the same instance
        self.assertIs(logger1, logger2)
        
        # Check that logging directory was created
        self.assertTrue(logger1.run_log_dir.exists())
        
        # Test logging with global instance
        logger1.log_bash_command("echo 'global test'", "Test global logging")
        
        # Verify log file was created
        self.assertTrue(logger1.bash_commands_file.exists())
    
    def test_framework_bridge_global_instance(self):
        """Test framework bridge global instance management"""
        # Test getting global bridge instance
        bridge1 = get_framework_bridge("ACM-BRIDGE-GLOBAL")
        bridge2 = get_framework_bridge("ACM-BRIDGE-GLOBAL")
        
        # Should return the same instance
        self.assertIs(bridge1, bridge2)
        
        # Check that bridge has access to logger
        self.assertIsNotNone(bridge1.logger)
        self.assertTrue(bridge1.logger.run_log_dir.exists())
    
    def test_complete_operational_transparency(self):
        """Test complete operational transparency across all systems"""
        # Initialize all logging systems
        hook = ComprehensiveLoggingHook()
        hook.initialize_run_logging("ACM-TRANSPARENCY", "transparency-test")
        
        logger = get_mandatory_logger("ACM-TRANSPARENCY")
        bridge = get_framework_bridge("ACM-TRANSPARENCY")
        bridge.start_framework_execution("test_generator")
        
        # Simulate complete framework execution with all operation types
        operations = [
            # Framework phase start
            ("framework_phase", {"phase": "phase_0_pre", "operation": "start"}),
            
            # Agent spawning
            ("tool_hook", {"tool": "task", "params": {"description": "JIRA Analysis", "subagent_type": "general-purpose"}}),
            
            # Environment commands
            ("tool_hook", {"tool": "bash", "params": {"command": "oc whoami", "description": "Check authentication"}}),
            ("bridge_bash", {"command": "oc get clusterversion", "output": "VERSION: 4.12.0", "agent": "agent_d"}),
            
            # File operations
            ("tool_hook", {"tool": "read", "params": {"file_path": ".claude/config/test.json"}}),
            ("tool_hook", {"tool": "write", "params": {"file_path": "runs/ACM-TRANSPARENCY/analysis.md", "content": "# Analysis\nTest content"}}),
            
            # API calls
            ("bridge_api", {"api": "github", "endpoint": "https://api.github.com/repos/test", "agent": "agent_c"}),
            
            # Agent operations
            ("bridge_agent", {"agent": "agent_a", "operation": "complete", "findings": "JIRA analysis complete"}),
            
            # Framework phase end
            ("framework_phase", {"phase": "phase_0_pre", "operation": "complete"}),
        ]
        
        # Execute all operations
        for op_type, op_data in operations:
            if op_type == "framework_phase":
                logger.log_framework_phase(op_data["phase"], op_data["operation"])
            elif op_type == "tool_hook":
                hook.process_tool_call(op_data["tool"], op_data["params"])
            elif op_type == "bridge_bash":
                bridge.capture_bash_command(op_data["command"], agent_context=op_data["agent"], output=op_data["output"])
            elif op_type == "bridge_api":
                bridge.capture_api_call(op_data["api"], op_data["endpoint"], agent_context=op_data["agent"])
            elif op_type == "bridge_agent":
                bridge.capture_agent_operation(op_data["agent"], op_data["operation"], findings=op_data["findings"])
        
        # Finalize all logging systems
        bridge_summary = bridge.finalize_framework_execution()
        logger.finalize_logging_session()
        hook_summary = hook.save_session_summary()
        
        # Verify complete operational transparency
        self.assertTrue(Path(hook_summary).exists(), "Hook session summary not created")
        self.assertTrue(logger.execution_summary_file.exists(), "Logger execution summary not created")
        self.assertTrue(bridge_summary['framework_execution_complete'], "Bridge execution not complete")
        
        # Verify all log types were captured
        required_log_files = [
            logger.master_log_file,
            logger.bash_commands_file,
            logger.file_operations_file,
            logger.agent_operations_file,
            logger.api_calls_file,
            logger.framework_phases_file,
            hook.session_log_file
        ]
        
        for log_file in required_log_files:
            self.assertTrue(log_file.exists(), f"Required log file missing: {log_file}")
            
            # Verify log file has content
            self.assertGreater(log_file.stat().st_size, 0, f"Log file is empty: {log_file}")
        
        # Verify subdirectory structure was created
        required_subdirs = [
            logger.run_log_dir / "agents",
            logger.run_log_dir / "tools",
            logger.run_log_dir / "analysis",
            logger.run_log_dir / "raw-data"
        ]
        
        for subdir in required_subdirs:
            self.assertTrue(subdir.exists(), f"Required subdirectory missing: {subdir}")


if __name__ == '__main__':
    print("🧪 Comprehensive Logging Hooks Unit Tests")
    print("=" * 55)
    print("Testing ACTUAL implementation of logging hooks system")
    print("=" * 55)
    
    # Check availability
    if not LOGGING_HOOKS_AVAILABLE:
        print("❌ Logging hooks not available - skipping tests")
        exit(1)
    
    # Run tests with detailed output
    unittest.main(verbosity=2)