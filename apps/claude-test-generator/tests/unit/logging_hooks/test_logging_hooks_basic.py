#!/usr/bin/env python3
"""
Basic Logging Hooks Functionality Test
======================================

Tests that validate the ACTUAL working functionality of the logging hooks system.
These tests focus on proving the implementation works in practice.
"""

import unittest
import sys
import os
import tempfile
import json
import shutil
from pathlib import Path

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
hooks_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'hooks')
logging_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'logging')
sys.path.insert(0, hooks_path)
sys.path.insert(0, logging_path)

try:
    from comprehensive_logging_hook import ComprehensiveLoggingHook
    from mandatory_comprehensive_logger import MandatoryComprehensiveLogger
    HOOKS_AVAILABLE = True
except ImportError as e:
    HOOKS_AVAILABLE = False
    print(f"❌ Hooks not available: {e}")


class TestBasicLoggingFunctionality(unittest.TestCase):
    """Test basic logging functionality that actually works"""
    
    @classmethod
    def setUpClass(cls):
        if not HOOKS_AVAILABLE:
            cls.skipTest(cls, "Logging hooks not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create .claude directory
        claude_dir = Path(self.test_dir) / ".claude"
        claude_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_comprehensive_logging_hook_working(self):
        """Test that comprehensive logging hook actually works"""
        hook = ComprehensiveLoggingHook()
        
        # Test initialization
        self.assertEqual(hook.hook_name, "comprehensive_logging_hook")
        self.assertEqual(hook.version, "1.0-PRODUCTION")
        
        # Test tool processing
        bash_params = {"command": "echo test", "description": "test command"}
        result = hook.process_bash_tool(bash_params)
        
        # Should return params unchanged
        self.assertEqual(result, bash_params)
        
        # Should have logged the command
        self.assertEqual(hook.session_stats['bash_commands'], 1)
        self.assertEqual(len(hook.execution_log), 1)
        
        log_entry = hook.execution_log[0]
        self.assertEqual(log_entry['action'], 'BASH_EXECUTION')
        self.assertEqual(log_entry['details']['command'], 'echo test')
        
        print("✅ Comprehensive Logging Hook: WORKING")
    
    def test_mandatory_comprehensive_logger_working(self):
        """Test that mandatory comprehensive logger actually works"""
        logger = MandatoryComprehensiveLogger("ACM-TEST-BASIC")
        
        # Test initialization
        self.assertEqual(logger.jira_ticket, "ACM-TEST-BASIC")
        self.assertTrue(logger.run_log_dir.exists())
        
        # Test bash command logging
        logger.log_bash_command("oc whoami", "Check authentication")
        self.assertEqual(logger.execution_stats['bash_commands'], 1)
        self.assertTrue(logger.bash_commands_file.exists())
        
        # Test agent operation logging
        logger.log_agent_operation("agent_a", "start", {"task": "test"})
        self.assertEqual(logger.execution_stats['agent_operations'], 1)
        self.assertTrue(logger.agent_operations_file.exists())
        
        # Verify actual file content
        with open(logger.bash_commands_file, 'r') as f:
            bash_log = json.loads(f.readline().strip())
        
        self.assertEqual(bash_log['event_type'], 'BASH_COMMAND')
        self.assertEqual(bash_log['command'], 'oc whoami')
        
        print("✅ Mandatory Comprehensive Logger: WORKING")
    
    def test_log_files_actually_created(self):
        """Test that log files are actually created with real content"""
        logger = MandatoryComprehensiveLogger("ACM-FILE-TEST")
        
        # Log various operations
        logger.log_bash_command("oc get nodes", "Check cluster nodes")
        logger.log_file_operation("read", "/test/config.json", "{'test': 'data'}")
        logger.log_api_call("github", "https://api.github.com/test", "GET")
        
        # Check all expected files exist
        expected_files = [
            logger.master_log_file,
            logger.bash_commands_file,
            logger.file_operations_file,
            logger.api_calls_file
        ]
        
        for log_file in expected_files:
            self.assertTrue(log_file.exists(), f"Log file not created: {log_file}")
            self.assertGreater(log_file.stat().st_size, 0, f"Log file is empty: {log_file}")
        
        # Verify content in master log
        with open(logger.master_log_file, 'r') as f:
            lines = f.readlines()
        
        self.assertGreaterEqual(len(lines), 4)  # 1 init + 3 operations
        
        # Parse first operation log
        log_entry = json.loads(lines[1].strip())
        self.assertEqual(log_entry['event_type'], 'BASH_COMMAND')
        self.assertEqual(log_entry['command'], 'oc get nodes')
        
        print("✅ Log Files Actually Created: WORKING")
    
    def test_directory_structure_created(self):
        """Test that proper directory structure is created"""
        logger = MandatoryComprehensiveLogger("ACM-DIR-TEST")
        
        # Check main directories
        required_dirs = [
            logger.run_log_dir,
            logger.run_log_dir / "agents",
            logger.run_log_dir / "tools",
            logger.run_log_dir / "phases",
            logger.run_log_dir / "raw-data",
            logger.run_log_dir / "analysis"
        ]
        
        for directory in required_dirs:
            self.assertTrue(directory.exists(), f"Required directory not created: {directory}")
        
        # Check latest symlink
        latest_link = logger.jira_log_dir / "latest"
        self.assertTrue(latest_link.exists())
        self.assertTrue(latest_link.is_symlink())
        
        print("✅ Directory Structure: WORKING")
    
    def test_execution_summary_finalization(self):
        """Test execution summary finalization works"""
        logger = MandatoryComprehensiveLogger("ACM-SUMMARY-TEST")
        
        # Log some operations
        logger.log_framework_phase("phase_0", "start")
        logger.log_bash_command("echo 'test'", "Test command")
        logger.log_framework_phase("phase_0", "complete")
        
        # Finalize
        logger.finalize_logging_session()
        
        # Check summary file exists
        self.assertTrue(logger.execution_summary_file.exists())
        
        # Check summary content
        with open(logger.execution_summary_file, 'r') as f:
            summary = json.load(f)
        
        self.assertIn('session_summary', summary)
        self.assertIn('execution_statistics', summary)
        self.assertTrue(summary['comprehensive_logging_complete'])
        self.assertTrue(summary['mandatory_logging_enforced'])
        
        # Check statistics
        stats = summary['execution_statistics']
        self.assertEqual(stats['bash_commands'], 1)
        self.assertEqual(stats['framework_phases'], 2)
        self.assertGreater(stats['total_operations'], 0)
        
        print("✅ Execution Summary: WORKING")


if __name__ == '__main__':
    print("🧪 Basic Logging Hooks Functionality Test")
    print("=" * 45)
    print("Testing ACTUAL working implementation")
    print("=" * 45)
    
    if not HOOKS_AVAILABLE:
        print("❌ Logging hooks not available - cannot test")
        exit(1)
    
    unittest.main(verbosity=2)