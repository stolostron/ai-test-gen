#!/usr/bin/env python3
"""
Framework Logging System Validation Tests

Purpose: Comprehensive validation tests for the framework debug logging system.
Tests all components, integration points, and functionality to ensure reliability.

Author: AI Systems Suite
Version: 1.0.0
"""

import os
import sys
import json
import time
import tempfile
import unittest
import argparse
from pathlib import Path
from typing import Dict, Any, List
import shutil

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from framework_debug_logger import FrameworkDebugLogger, LogEntry
from framework_hooks import FrameworkHookIntegration
from log_analyzer import FrameworkLogAnalyzer
from realtime_monitor import RealTimeFrameworkMonitor
from enable_framework_logging import FrameworkLoggingIntegration

class TestFrameworkDebugLogger(unittest.TestCase):
    """Test FrameworkDebugLogger functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.logger = FrameworkDebugLogger("test-run", self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self, 'logger'):
            self.logger.finalize_logging()
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_logger_initialization(self):
        """Test logger initialization"""
        self.assertIsNotNone(self.logger)
        self.assertEqual(self.logger.run_id, "test-run")
        self.assertTrue(self.logger.log_dir.exists())
        
        # Check directory structure
        expected_dirs = ['phases', 'agents', 'tools', 'context', 'validation', 'environment']
        for dir_name in expected_dirs:
            self.assertTrue((self.logger.log_dir / dir_name).exists())
        
        # Check log files
        expected_files = ['framework_debug_master.jsonl', 'framework_debug_readable.log', 
                         'execution_summary.json']
        for file_name in expected_files:
            self.assertTrue((self.logger.log_dir / file_name).exists())
    
    def test_basic_logging(self):
        """Test basic logging functionality"""
        # Test different log levels
        self.logger.log_debug("TEST_DEBUG", "Debug message", {"test": "data"})
        self.logger.log_info("TEST_INFO", "Info message", {"test": "data"})
        self.logger.log_warning("TEST_WARNING", "Warning message", {"test": "data"})
        self.logger.log_error("TEST_ERROR", "Error message", {"test": "data"})
        self.logger.log_critical("TEST_CRITICAL", "Critical message", {"test": "data"})
        
        # Check logs were written
        master_log = self.logger.log_dir / 'framework_debug_master.jsonl'
        self.assertTrue(master_log.exists())
        
        with open(master_log, 'r') as f:
            log_lines = f.readlines()
        
        self.assertEqual(len(log_lines), 6)  # 5 test logs + 1 initialization log
        
        # Parse and validate log entries
        for line in log_lines[1:]:  # Skip initialization log
            log_entry = json.loads(line)
            self.assertIn('timestamp', log_entry)
            self.assertIn('log_level', log_entry)
            self.assertIn('action', log_entry)
            self.assertIn('details', log_entry)
    
    def test_phase_tracking(self):
        """Test phase tracking functionality"""
        with self.logger.track_phase("test_phase", {"test": "phase_data"}):
            self.logger.log_info("PHASE_WORK", "Doing phase work")
            time.sleep(0.1)
        
        # Check phase logs
        phase_log = self.logger.log_dir / 'phases' / 'phase_test_phase.jsonl'
        self.assertTrue(phase_log.exists())
        
        with open(phase_log, 'r') as f:
            phase_entries = [json.loads(line) for line in f]
        
        # Should have start and complete entries
        self.assertGreaterEqual(len(phase_entries), 2)
        
        # Verify phase tracking
        start_entry = next((e for e in phase_entries if 'PHASE_START' in e['action']), None)
        complete_entry = next((e for e in phase_entries if 'PHASE_COMPLETE' in e['action']), None)
        
        self.assertIsNotNone(start_entry)
        self.assertIsNotNone(complete_entry)
        self.assertEqual(start_entry['phase'], 'test_phase')
        self.assertEqual(complete_entry['phase'], 'test_phase')
    
    def test_agent_tracking(self):
        """Test agent tracking functionality"""
        with self.logger.track_agent("test_agent", "Test agent task", {"test": "agent_data"}):
            self.logger.log_info("AGENT_WORK", "Agent doing work")
            time.sleep(0.1)
        
        # Check agent logs
        agent_log = self.logger.log_dir / 'agents' / 'agent_test_agent.jsonl'
        self.assertTrue(agent_log.exists())
        
        with open(agent_log, 'r') as f:
            agent_entries = [json.loads(line) for line in f]
        
        # Should have spawn and complete entries
        self.assertGreaterEqual(len(agent_entries), 2)
        
        # Verify agent tracking
        spawn_entry = next((e for e in agent_entries if 'AGENT_SPAWN' in e['action']), None)
        complete_entry = next((e for e in agent_entries if 'AGENT_COMPLETE' in e['action']), None)
        
        self.assertIsNotNone(spawn_entry)
        self.assertIsNotNone(complete_entry)
        self.assertEqual(spawn_entry['agent'], 'test_agent')
        self.assertEqual(complete_entry['agent'], 'test_agent')
    
    def test_tool_tracking(self):
        """Test tool tracking functionality"""
        with self.logger.track_tool("test_tool", "test_action", {"input": "test"}) as execution_id:
            self.logger.log_info("TOOL_WORK", f"Tool working with ID: {execution_id}")
            time.sleep(0.1)
        
        # Check tool logs
        tool_log = self.logger.log_dir / 'tools' / 'tool_general.jsonl'
        self.assertTrue(tool_log.exists())
        
        with open(tool_log, 'r') as f:
            tool_entries = [json.loads(line) for line in f]
        
        # Should have start and complete entries
        self.assertGreaterEqual(len(tool_entries), 2)
        
        # Verify tool tracking
        start_entry = next((e for e in tool_entries if 'STARTING_test_action' in e['action']), None)
        complete_entry = next((e for e in tool_entries if 'COMPLETED_test_action' in e['action']), None)
        
        self.assertIsNotNone(start_entry)
        self.assertIsNotNone(complete_entry)
    
    def test_context_flow_logging(self):
        """Test context flow logging"""
        test_context = {"agent_a": "data", "inheritance_chain": ["A", "A+D"]}
        
        self.logger.log_context_flow("CONTEXT_INHERITANCE", test_context, ["A", "A+D"])
        
        # Check context logs
        context_log = self.logger.log_dir / 'context' / 'context_general.jsonl'
        self.assertTrue(context_log.exists())
        
        with open(context_log, 'r') as f:
            context_entries = [json.loads(line) for line in f]
        
        self.assertGreater(len(context_entries), 0)
        
        # Verify context logging
        context_entry = context_entries[0]
        self.assertEqual(context_entry['component'], 'CONTEXT')
        self.assertEqual(context_entry['action'], 'CONTEXT_INHERITANCE')
        self.assertIn('inheritance_chain', context_entry['details'])
    
    def test_validation_logging(self):
        """Test validation checkpoint logging"""
        self.logger.log_validation_checkpoint("test_validation", "passed", 0.95, {"test": "data"})
        
        # Check validation logs
        validation_log = self.logger.log_dir / 'validation' / 'validation_general.jsonl'
        self.assertTrue(validation_log.exists())
        
        with open(validation_log, 'r') as f:
            validation_entries = [json.loads(line) for line in f]
        
        self.assertGreater(len(validation_entries), 0)
        
        # Verify validation logging
        validation_entry = validation_entries[0]
        self.assertEqual(validation_entry['component'], 'VALIDATION')
        self.assertEqual(validation_entry['details']['validation_type'], 'test_validation')
        self.assertEqual(validation_entry['details']['result'], 'passed')
        self.assertEqual(validation_entry['details']['confidence'], 0.95)
    
    def test_error_logging(self):
        """Test error logging"""
        self.logger.log_error("TEST_ERROR", "Test error message", {"error_code": 500})
        
        # Check error log
        error_log = self.logger.log_dir / 'error_log.jsonl'
        self.assertTrue(error_log.exists())
        
        with open(error_log, 'r') as f:
            error_entries = [json.loads(line) for line in f]
        
        self.assertGreater(len(error_entries), 0)
        
        # Verify error logging
        error_entry = error_entries[0]
        self.assertEqual(error_entry['log_level'], 'ERROR')
        self.assertEqual(error_entry['action'], 'TEST_ERROR')
    
    def test_performance_logging(self):
        """Test performance metrics logging"""
        performance_metrics = {
            "execution_time": 1.5,
            "memory_usage": 100
        }
        
        self.logger.log_info("PERFORMANCE_TEST", "Performance test", 
                           performance_metrics=performance_metrics)
        
        # Check logs contain performance metrics
        master_log = self.logger.log_dir / 'framework_debug_master.jsonl'
        with open(master_log, 'r') as f:
            log_lines = f.readlines()
        
        # Find performance log entry
        performance_entry = None
        for line in log_lines:
            entry = json.loads(line)
            if entry.get('action') == 'PERFORMANCE_TEST':
                performance_entry = entry
                break
        
        self.assertIsNotNone(performance_entry)
        self.assertIn('performance_metrics', performance_entry)
        self.assertEqual(performance_entry['performance_metrics']['execution_time'], 1.5)
    
    def test_summary_generation(self):
        """Test execution summary generation"""
        # Generate some logs
        self.logger.log_phase_start("test_phase")
        self.logger.log_agent_spawn("test_agent", "Test task")
        self.logger.log_tool_execution("test_tool", "test_action")
        self.logger.log_validation_checkpoint("test_validation", "passed", 0.9)
        self.logger.log_error("TEST_ERROR", "Test error")
        
        # Check summary file
        summary_file = self.logger.log_dir / 'execution_summary.json'
        self.assertTrue(summary_file.exists())
        
        with open(summary_file, 'r') as f:
            summary = json.load(f)
        
        # Verify summary structure
        self.assertIn('run_metadata', summary)
        self.assertIn('execution_timeline', summary)
        self.assertIn('phase_summary', summary)
        self.assertIn('agent_summary', summary)
        self.assertIn('tool_usage', summary)
        self.assertIn('validation_results', summary)
        self.assertIn('error_summary', summary)
        
        # Verify content
        self.assertEqual(summary['run_metadata']['run_id'], 'test-run')
        self.assertIn('test_phase', summary['phase_summary'])
        self.assertIn('test_agent', summary['agent_summary'])

class TestFrameworkHooks(unittest.TestCase):
    """Test FrameworkHookIntegration functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.logger = FrameworkDebugLogger("test-hooks", self.test_dir)
        self.hooks = FrameworkHookIntegration(self.logger, enable_all_hooks=False)
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self, 'hooks'):
            self.hooks.finalize_framework_logging()
        if hasattr(self, 'logger'):
            self.logger.finalize_logging()
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_hooks_initialization(self):
        """Test hooks initialization"""
        self.assertIsNotNone(self.hooks)
        self.assertEqual(self.hooks.logger, self.logger)
        self.assertIsInstance(self.hooks.hook_registry, dict)
        self.assertIsInstance(self.hooks.framework_state, dict)
    
    def test_tool_hooks_installation(self):
        """Test tool hooks installation"""
        self.hooks.install_claude_code_tool_hooks()
        
        # Check that tool hooks are registered
        expected_tools = ['bash_tool', 'read_tool', 'write_tool', 'task_tool', 'glob_tool', 'grep_tool', 'edit_tool']
        for tool in expected_tools:
            self.assertIn(tool, self.hooks.hook_registry)
            self.assertIsNotNone(self.hooks.hook_registry[tool])
    
    def test_bash_tool_hook(self):
        """Test bash tool hook functionality"""
        self.hooks.install_claude_code_tool_hooks()
        bash_hook = self.hooks.hook_registry['bash_tool']
        
        # Execute bash hook
        result = bash_hook("echo 'test command'", "Test bash execution")
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertIn('stdout', result)
        self.assertIn('stderr', result)
        self.assertIn('return_code', result)
    
    def test_read_tool_hook(self):
        """Test read tool hook functionality"""
        # Create a test file
        test_file = Path(self.test_dir) / "test_file.txt"
        test_content = "Test file content\nLine 2\nLine 3"
        test_file.write_text(test_content)
        
        self.hooks.install_claude_code_tool_hooks()
        read_hook = self.hooks.hook_registry['read_tool']
        
        # Execute read hook
        result = read_hook(str(test_file))
        
        # Verify result
        self.assertEqual(result, test_content)
    
    def test_write_tool_hook(self):
        """Test write tool hook functionality"""
        test_file = Path(self.test_dir) / "write_test.txt"
        test_content = "Written by hook test"
        
        self.hooks.install_claude_code_tool_hooks()
        write_hook = self.hooks.hook_registry['write_tool']
        
        # Execute write hook
        write_hook(str(test_file), test_content)
        
        # Verify file was written
        self.assertTrue(test_file.exists())
        self.assertEqual(test_file.read_text(), test_content)
    
    def test_task_tool_hook(self):
        """Test task tool hook (agent spawning)"""
        self.hooks.install_claude_code_tool_hooks()
        task_hook = self.hooks.hook_registry['task_tool']
        
        # Execute task hook
        result = task_hook("Test agent description", "Test agent prompt", "test-agent")
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'completed')
    
    def test_framework_phase_hooks(self):
        """Test framework phase hooks"""
        self.hooks.install_framework_phase_hooks()
        
        # Test manual phase logging
        self.hooks.manual_phase_start("test_phase", {"test": "data"})
        self.hooks.manual_phase_complete("test_phase", {"test": "data"})
        
        # Verify phase was logged
        phase_log = self.logger.log_dir / 'phases' / 'phase_test_phase.jsonl'
        self.assertTrue(phase_log.exists())
    
    def test_context_flow_hooks(self):
        """Test context flow hooks"""
        self.hooks.install_context_flow_hooks()
        
        # Test context tracking
        self.hooks.track_context_flow("test_context_action", {"test": "context_data"})
        
        # Verify context was logged
        context_log = self.logger.log_dir / 'context' / 'context_general.jsonl'
        self.assertTrue(context_log.exists())
    
    def test_validation_hooks(self):
        """Test validation hooks"""
        self.hooks.install_validation_hooks()
        
        # Test validation tracking
        self.hooks.track_validation("test_validation", "passed", 0.85)
        
        # Verify validation was logged
        validation_log = self.logger.log_dir / 'validation' / 'validation_general.jsonl'
        self.assertTrue(validation_log.exists())
        
        # Check framework state was updated
        self.assertIn('test_validation', self.hooks.framework_state['validation_status'])
        self.assertEqual(self.hooks.framework_state['validation_status']['test_validation']['result'], 'passed')
    
    def test_framework_state_tracking(self):
        """Test framework state tracking"""
        # Start framework logging
        self.hooks.start_framework_logging("test-run", "TEST-123")
        
        # Simulate framework activities
        self.hooks.log_framework_phase("1", "start", {"test": "data"})
        self.hooks.log_agent_activity("agent_a", "spawn", {"task": "test"})
        
        # Check framework state
        state = self.hooks.get_framework_state()
        self.assertEqual(state['current_phase'], '1')
        self.assertIn('agent_a', state['active_agents'])
        self.assertEqual(state['jira_ticket'], 'TEST-123')

class TestLogAnalyzer(unittest.TestCase):
    """Test FrameworkLogAnalyzer functionality"""
    
    def setUp(self):
        """Set up test environment with sample logs"""
        self.test_dir = tempfile.mkdtemp()
        self.logger = FrameworkDebugLogger("test-analyzer", self.test_dir)
        
        # Generate sample logs
        self._generate_sample_logs()
        self.logger.finalize_logging()
        
        # Create analyzer
        self.analyzer = FrameworkLogAnalyzer(str(self.logger.log_dir))
    
    def tearDown(self):
        """Clean up test environment"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def _generate_sample_logs(self):
        """Generate sample logs for testing"""
        # Phase logs
        self.logger.log_phase_start("1", {"test": "phase1"})
        time.sleep(0.1)
        self.logger.log_phase_complete("1", {"test": "phase1"})
        
        # Agent logs
        self.logger.log_agent_spawn("agent_a", "Test JIRA analysis")
        time.sleep(0.1)
        self.logger.log_agent_complete("agent_a", "Analysis complete")
        
        # Tool logs
        self.logger.log_tool_execution("bash", "execute_command", {"command": "echo test"})
        self.logger.log_tool_execution("read", "read_file", {"file": "test.txt"})
        
        # Context logs
        self.logger.log_context_flow("CONTEXT_INHERITANCE", {"agent": "a", "data": "test"})
        
        # Validation logs
        self.logger.log_validation_checkpoint("implementation_reality", "passed", 0.95)
        self.logger.log_validation_checkpoint("evidence_validation", "passed", 0.88)
        
        # Error logs
        self.logger.log_error("TEST_ERROR", "Sample error", {"error_code": 500})
        
        # Performance logs
        self.logger.log_info("PERFORMANCE_TEST", "Performance test", 
                           performance_metrics={"duration": 1.5})
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        self.assertIsNotNone(self.analyzer)
        self.assertTrue(self.analyzer.log_dir.exists())
        self.assertGreater(len(self.analyzer.logs), 0)
    
    def test_timeline_analysis(self):
        """Test execution timeline analysis"""
        timeline = self.analyzer.analyze_execution_timeline()
        
        # Verify timeline structure
        self.assertIn('start_time', timeline)
        self.assertIn('end_time', timeline)
        self.assertIn('total_duration_seconds', timeline)
        self.assertIn('component_stats', timeline)
        self.assertIn('phase_stats', timeline)
        self.assertIn('agent_stats', timeline)
        
        # Verify content
        self.assertGreater(timeline['total_events'], 0)
        self.assertGreater(timeline['total_duration_seconds'], 0)
    
    def test_agent_coordination_analysis(self):
        """Test agent coordination analysis"""
        coordination = self.analyzer.analyze_agent_coordination()
        
        # Verify structure
        self.assertIn('agent_count', coordination)
        self.assertIn('completed_cycles', coordination)
        self.assertIn('agent_lifecycle', coordination)
        
        # Verify content
        self.assertGreater(coordination['agent_count'], 0)
        self.assertIn('agent_a', coordination['agent_lifecycle'])
    
    def test_tool_usage_analysis(self):
        """Test tool usage analysis"""
        tools = self.analyzer.analyze_tool_usage()
        
        # Verify structure
        self.assertIn('total_tool_events', tools)
        self.assertIn('unique_tools', tools)
        self.assertIn('tool_statistics', tools)
        
        # Verify content
        self.assertGreater(tools['total_tool_events'], 0)
        self.assertGreater(tools['unique_tools'], 0)
    
    def test_context_flow_analysis(self):
        """Test context flow analysis"""
        context = self.analyzer.analyze_context_flow()
        
        # Verify structure
        self.assertIn('total_context_events', context)
        self.assertIn('inheritance_steps', context)
        
        # Verify content
        self.assertGreater(context['total_context_events'], 0)
    
    def test_validation_analysis(self):
        """Test validation checkpoint analysis"""
        validation = self.analyzer.analyze_validation_checkpoints()
        
        # Verify structure
        self.assertIn('total_validation_events', validation)
        self.assertIn('validation_types', validation)
        self.assertIn('validation_statistics', validation)
        
        # Verify content
        self.assertGreater(validation['total_validation_events'], 0)
        self.assertGreater(validation['validation_types'], 0)
    
    def test_error_analysis(self):
        """Test error analysis"""
        errors = self.analyzer.analyze_errors()
        
        # Verify structure
        self.assertIn('error_count', errors)
        self.assertIn('error_rate', errors)
        
        # Verify content
        self.assertGreater(errors['error_count'], 0)
        self.assertGreater(errors['error_rate'], 0)
    
    def test_performance_analysis(self):
        """Test performance analysis"""
        performance = self.analyzer.analyze_performance()
        
        # Verify structure
        self.assertIn('total_performance_events', performance)
        
        # Verify content
        self.assertGreater(performance['total_performance_events'], 0)
    
    def test_log_query(self):
        """Test log query functionality"""
        # Query by component
        results = self.analyzer.query_logs({'component': 'AGENT'})
        self.assertGreater(len(results), 0)
        
        # Verify all results are agent logs
        for result in results:
            self.assertEqual(result['component'], 'AGENT')
        
        # Query by log level
        error_results = self.analyzer.query_logs({'log_level': 'ERROR'})
        self.assertGreater(len(error_results), 0)
        
        # Verify all results are errors
        for result in error_results:
            self.assertEqual(result['log_level'], 'ERROR')
    
    def test_debug_report_generation(self):
        """Test debug report generation"""
        report = self.analyzer.generate_debug_report()
        
        # Verify report is JSON
        report_data = json.loads(report)
        
        # Verify report structure
        expected_sections = [
            'timeline_analysis', 'agent_analysis', 'tool_analysis',
            'context_analysis', 'validation_analysis', 'error_analysis',
            'performance_analysis'
        ]
        
        for section in expected_sections:
            self.assertIn(section, report_data)

class TestRealTimeMonitor(unittest.TestCase):
    """Test RealTimeFrameworkMonitor functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.logger = FrameworkDebugLogger("test-monitor", self.test_dir)
        
        # Generate some logs
        self._generate_sample_logs()
        
        # Create monitor
        self.monitor = RealTimeFrameworkMonitor(str(self.logger.log_dir), 0.1)
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self, 'monitor') and self.monitor.monitoring_active:
            self.monitor.stop_monitoring()
        if hasattr(self, 'logger'):
            self.logger.finalize_logging()
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def _generate_sample_logs(self):
        """Generate sample logs for monitoring"""
        self.logger.log_phase_start("1")
        self.logger.log_agent_spawn("agent_a", "Test task")
        self.logger.log_tool_execution("bash", "test_command")
        self.logger.log_validation_checkpoint("test_validation", "passed", 0.9)
    
    def test_monitor_initialization(self):
        """Test monitor initialization"""
        self.assertIsNotNone(self.monitor)
        self.assertEqual(self.monitor.log_dir, Path(self.logger.log_dir))
        self.assertFalse(self.monitor.monitoring_active)
    
    def test_monitor_start_stop(self):
        """Test monitor start and stop"""
        # Start monitoring
        self.monitor.start_monitoring()
        self.assertTrue(self.monitor.monitoring_active)
        
        # Let it monitor for a bit
        time.sleep(0.5)
        
        # Stop monitoring
        self.monitor.stop_monitoring()
        self.assertFalse(self.monitor.monitoring_active)
    
    def test_status_collection(self):
        """Test status collection"""
        self.monitor.start_monitoring()
        time.sleep(0.2)  # Let it collect some data
        
        status = self.monitor.get_current_status()
        
        # Verify status structure
        self.assertIn('current_state', status)
        self.assertIn('recent_events', status)
        self.assertIn('monitoring_active', status)
        
        # Verify monitoring is active
        self.assertTrue(status['monitoring_active'])
        
        self.monitor.stop_monitoring()
    
    def test_status_export(self):
        """Test status export"""
        self.monitor.start_monitoring()
        time.sleep(0.2)
        
        export_file = Path(self.test_dir) / "status_export.json"
        self.monitor.export_status(str(export_file))
        
        # Verify export file
        self.assertTrue(export_file.exists())
        
        with open(export_file, 'r') as f:
            exported_status = json.load(f)
        
        self.assertIn('current_state', exported_status)
        self.assertIn('monitoring_active', exported_status)
        
        self.monitor.stop_monitoring()

class TestFrameworkLoggingIntegration(unittest.TestCase):
    """Test complete framework logging integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        
        # Create test config
        self.config_file = Path(self.test_dir) / "test_config.json"
        self._create_test_config()
        
        self.integration = FrameworkLoggingIntegration(str(self.config_file))
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self, 'integration'):
            self.integration.disable_framework_logging()
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def _create_test_config(self):
        """Create test configuration"""
        config = {
            "framework_debug_logging": {
                "enabled": True,
                "global_settings": {
                    "default_log_level": "DEBUG",
                    "auto_start_logging": True
                },
                "log_destinations": {
                    "base_directory": str(Path(self.test_dir) / "logs")
                },
                "hook_configuration": {
                    "auto_install_hooks": True,
                    "enabled_hooks": {
                        "claude_code_tools": True,
                        "framework_phases": True,
                        "agent_coordination": True
                    }
                },
                "real_time_monitoring": {
                    "enabled": False
                }
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def test_integration_initialization(self):
        """Test integration initialization"""
        self.assertIsNotNone(self.integration)
        self.assertIsNotNone(self.integration.config)
        self.assertTrue(self.integration.config['enabled'])
    
    def test_complete_logging_enable_disable(self):
        """Test complete logging enable and disable"""
        # Enable logging
        result = self.integration.enable_framework_logging("test-run", "TEST-123", False)
        
        # Verify successful enablement
        self.assertTrue(result['success'])
        self.assertTrue(result['components']['logger'])
        self.assertTrue(result['components']['hooks'])
        self.assertIsNotNone(result['log_directory'])
        
        # Verify components are active
        self.assertIsNotNone(self.integration.logger)
        self.assertIsNotNone(self.integration.hooks)
        
        # Test status
        status = self.integration.get_status()
        self.assertTrue(status['logging_enabled'])
        self.assertTrue(status['hooks_enabled'])
        
        # Disable logging
        self.integration.disable_framework_logging()
        
        # Verify disabled
        status = self.integration.get_status()
        self.assertFalse(status['logging_enabled'])
        self.assertFalse(status['hooks_enabled'])
    
    def test_demo_logs_creation(self):
        """Test demo logs creation"""
        # Enable logging first
        result = self.integration.enable_framework_logging("demo-run", "DEMO-123", False)
        self.assertTrue(result['success'])
        
        # Create demo logs
        self.integration.create_demo_logs()
        
        # Verify logs were created
        log_dir = Path(result['log_directory'])
        master_log = log_dir / 'framework_debug_master.jsonl'
        self.assertTrue(master_log.exists())
        
        # Verify log content
        with open(master_log, 'r') as f:
            log_lines = f.readlines()
        
        self.assertGreater(len(log_lines), 5)  # Should have multiple demo log entries
        
        # Check for demo-specific entries
        demo_entries = []
        for line in log_lines:
            entry = json.loads(line)
            if 'demo' in str(entry.get('details', {})).lower():
                demo_entries.append(entry)
        
        self.assertGreater(len(demo_entries), 0)

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🧪 RUNNING COMPREHENSIVE FRAMEWORK LOGGING TESTS")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestFrameworkDebugLogger,
        TestFrameworkHooks,
        TestLogAnalyzer,
        TestRealTimeMonitor,
        TestFrameworkLoggingIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🧪 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\n❌ ERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if not result.failures and not result.errors:
        print("✅ ALL TESTS PASSED!")
    
    return result.wasSuccessful()

def run_integration_test():
    """Run a comprehensive integration test"""
    print("\n🔗 RUNNING INTEGRATION TEST")
    print("=" * 40)
    
    test_dir = tempfile.mkdtemp()
    
    try:
        # Test complete workflow
        print("1. Creating framework logging integration...")
        integration = FrameworkLoggingIntegration()
        
        print("2. Enabling comprehensive logging...")
        result = integration.enable_framework_logging("integration-test", "INT-123", False)
        
        if not result['success']:
            print(f"❌ Failed to enable logging: {result.get('error')}")
            return False
        
        print("3. Simulating framework execution...")
        hooks = integration.hooks
        
        # Simulate complete framework workflow
        hooks.log_framework_phase("0-pre", "start")
        hooks.log_framework_phase("1", "start")
        hooks.log_agent_activity("agent_a", "spawn")
        hooks.log_agent_activity("agent_d", "spawn")
        
        # Simulate tool usage
        bash_hook = hooks.hook_registry.get('bash_tool')
        if bash_hook:
            bash_hook("oc get nodes", "Check cluster nodes")
        
        read_hook = hooks.hook_registry.get('read_tool')
        if read_hook:
            try:
                # Create a temporary file to read
                temp_file = Path(test_dir) / "test_read.txt"
                temp_file.write_text("Test content for reading")
                read_hook(str(temp_file))
            except:
                pass  # File operations may fail in test environment
        
        # Simulate context flow
        hooks.track_context_flow("context_inheritance", {"test": "context_data"})
        
        # Simulate validation
        hooks.track_validation("implementation_reality", "passed", 0.95)
        hooks.track_validation("evidence_validation", "passed", 0.88)
        
        # Simulate completion
        hooks.log_agent_activity("agent_a", "complete")
        hooks.log_agent_activity("agent_d", "complete")
        hooks.log_framework_phase("1", "complete")
        hooks.log_framework_phase("0-pre", "complete")
        
        print("4. Analyzing generated logs...")
        analyzer = integration.analyze_logs(analysis_type='all')
        
        if not analyzer:
            print("❌ Failed to analyze logs")
            return False
        
        print("5. Testing real-time monitoring...")
        # Brief monitoring test
        monitor = RealTimeFrameworkMonitor(str(integration.logger.log_dir), 0.1)
        monitor.start_monitoring()
        time.sleep(0.5)
        status = monitor.get_current_status()
        monitor.stop_monitoring()
        
        if not status['monitoring_active']:
            print("❌ Real-time monitoring failed")
            return False
        
        print("6. Disabling logging...")
        integration.disable_framework_logging()
        
        print("✅ Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False
        
    finally:
        if Path(test_dir).exists():
            shutil.rmtree(test_dir)

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Framework Logging System Tests")
    parser.add_argument('--unit', action='store_true', help='Run unit tests')
    parser.add_argument('--integration', action='store_true', help='Run integration test')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    success = True
    
    if args.all or args.unit:
        print("Running unit tests...")
        success &= run_comprehensive_tests()
    
    if args.all or args.integration:
        print("\nRunning integration test...")
        success &= run_integration_test()
    
    if not (args.unit or args.integration or args.all):
        print("No test type specified. Running all tests...")
        success &= run_comprehensive_tests()
        success &= run_integration_test()
    
    print(f"\n{'✅ ALL TESTS SUCCESSFUL!' if success else '❌ SOME TESTS FAILED!'}")
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())