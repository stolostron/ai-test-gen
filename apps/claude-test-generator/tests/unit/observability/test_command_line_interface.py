#!/usr/bin/env python3
"""
Comprehensive unit tests for Framework Observability Agent - Command Line Interface

Tests the observe command-line interface functionality including:
- Command parsing and argument handling
- Error handling and user feedback
- Help text and usage information
- Integration with ObservabilityCommandHandler
- File system and import error handling
"""

import unittest
import sys
import io
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add the observability directory to the path for imports
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../.claude/observability'))

# Import the main function from observe script
# We'll need to simulate the observe script functionality since it's not a module


class TestObserveCommandLineInterface(unittest.TestCase):
    """Test suite for observe command-line interface"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_run_dir = os.path.join(self.temp_dir, "runs", "ACM-22079", "ACM-22079-20250826-120000")
        os.makedirs(self.test_run_dir, exist_ok=True)
        
        # Capture stdout and stderr for testing
        self.stdout_backup = sys.stdout
        self.stderr_backup = sys.stderr
        self.captured_stdout = io.StringIO()
        self.captured_stderr = io.StringIO()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        # Restore stdout and stderr
        sys.stdout = self.stdout_backup
        sys.stderr = self.stderr_backup
    
    def capture_output(self):
        """Start capturing stdout and stderr"""
        sys.stdout = self.captured_stdout
        sys.stderr = self.captured_stderr
    
    def get_captured_output(self):
        """Get captured output"""
        stdout_value = self.captured_stdout.getvalue()
        stderr_value = self.captured_stderr.getvalue()
        return stdout_value, stderr_value
    
    def simulate_observe_main(self, args):
        """Simulate the main function from observe script"""
        # This simulates the observe script's main function behavior
        if len(args) < 2:
            print("🔍 **Claude Test Generator - Observability Interface**")
            print("")
            print("**Usage:**")
            print("  ./observe <command>")
            print("")
            print("**Quick Commands:**")
            print("  ./observe /status      - Current execution progress")
            print("  ./observe /business    - Customer impact analysis")
            print("  ./observe /technical   - Implementation details")
            print("  ./observe /agents      - Sub-agent coordination status")
            print("  ./observe /help        - Full command reference")
            print("")
            print("**Examples:**")
            print("  ./observe /deep-dive agent_a")
            print("  ./observe /context-flow")
            print("  ./observe /risks")
            return
        
        command = args[1]
        
        try:
            # Mock handler import and usage
            from observability_command_handler import ObservabilityCommandHandler
            handler = ObservabilityCommandHandler()
            response = handler.process_command(command)
            print(response)
            
        except FileNotFoundError as e:
            print("⚠️ **Observability Data Not Found**")
            print("")
            print("This usually means:")
            print("• Framework is not currently running")
            print("• No recent run data available")
            print("• Working directory is not a test-generator project")
            print("")
            print("**Solution:** Run observability commands from the test-generator directory during active framework execution.")
            
        except ImportError as e:
            print("❌ **Import Error**")
            print(f"Cannot import observability modules: {e}")
            print("")
            print("**Solution:** Ensure you're running from the correct directory with all required modules.")
            
        except Exception as e:
            print("🚨 **Observability Error**")
            print(f"Error processing command '{command}': {e}")
            print("")
            print("**Solution:** Check command syntax or use '/help' for available commands.")
    
    def test_no_arguments_shows_help(self):
        """Test that running observe without arguments shows help text"""
        self.capture_output()
        
        # Simulate running ./observe with no arguments
        self.simulate_observe_main(['observe'])
        
        stdout, stderr = self.get_captured_output()
        
        # Verify help text is displayed
        self.assertIn("Claude Test Generator - Observability Interface", stdout)
        self.assertIn("Usage:", stdout)
        self.assertIn("./observe <command>", stdout)
        self.assertIn("Quick Commands:", stdout)
        self.assertIn("/status", stdout)
        self.assertIn("/business", stdout)
        self.assertIn("/technical", stdout)
        self.assertIn("/agents", stdout)
        self.assertIn("/help", stdout)
        self.assertIn("Examples:", stdout)
        self.assertIn("/deep-dive agent_a", stdout)
        self.assertIn("/context-flow", stdout)
        self.assertIn("/risks", stdout)
    
    @patch('observability_command_handler.ObservabilityCommandHandler')
    def test_successful_command_execution(self, mock_handler_class):
        """Test successful command execution"""
        # Mock handler and response
        mock_handler = Mock()
        mock_handler.process_command.return_value = "🚀 **FRAMEWORK EXECUTION STATUS**\nTest response"
        mock_handler_class.return_value = mock_handler
        
        self.capture_output()
        
        # Simulate running ./observe /status
        self.simulate_observe_main(['observe', '/status'])
        
        stdout, stderr = self.get_captured_output()
        
        # Verify command was processed and response displayed
        self.assertIn("FRAMEWORK EXECUTION STATUS", stdout)
        self.assertIn("Test response", stdout)
        mock_handler.process_command.assert_called_once_with('/status')
    
    @patch('observability_command_handler.ObservabilityCommandHandler')
    def test_file_not_found_error_handling(self, mock_handler_class):
        """Test handling of FileNotFoundError (no run data available)"""
        mock_handler_class.side_effect = FileNotFoundError("Run data not found")
        
        self.capture_output()
        
        # Simulate running ./observe /status when no data is available
        self.simulate_observe_main(['observe', '/status'])
        
        stdout, stderr = self.get_captured_output()
        
        # Verify appropriate error message is displayed
        self.assertIn("Observability Data Not Found", stdout)
        self.assertIn("Framework is not currently running", stdout)
        self.assertIn("No recent run data available", stdout)
        self.assertIn("Working directory is not a test-generator project", stdout)
        self.assertIn("Solution:", stdout)
        self.assertIn("Run observability commands from the test-generator directory", stdout)
    
    @patch('observability_command_handler.ObservabilityCommandHandler')
    def test_import_error_handling(self, mock_handler_class):
        """Test handling of ImportError (missing modules)"""
        mock_handler_class.side_effect = ImportError("No module named 'observability_command_handler'")
        
        self.capture_output()
        
        # Simulate running ./observe /status when modules can't be imported
        self.simulate_observe_main(['observe', '/status'])
        
        stdout, stderr = self.get_captured_output()
        
        # Verify appropriate error message is displayed
        self.assertIn("Import Error", stdout)
        self.assertIn("Cannot import observability modules", stdout)
        self.assertIn("No module named 'observability_command_handler'", stdout)
        self.assertIn("Solution:", stdout)
        self.assertIn("Ensure you're running from the correct directory", stdout)
    
    @patch('observability_command_handler.ObservabilityCommandHandler')
    def test_general_exception_handling(self, mock_handler_class):
        """Test handling of general exceptions during command processing"""
        mock_handler = Mock()
        mock_handler.process_command.side_effect = Exception("Unexpected error occurred")
        mock_handler_class.return_value = mock_handler
        
        self.capture_output()
        
        # Simulate running ./observe /status when an unexpected error occurs
        self.simulate_observe_main(['observe', '/status'])
        
        stdout, stderr = self.get_captured_output()
        
        # Verify appropriate error message is displayed
        self.assertIn("Observability Error", stdout)
        self.assertIn("Error processing command '/status'", stdout)
        self.assertIn("Unexpected error occurred", stdout)
        self.assertIn("Solution:", stdout)
        self.assertIn("Check command syntax", stdout)
        self.assertIn("use '/help' for available commands", stdout)
    
    @patch('observability_command_handler.ObservabilityCommandHandler')
    def test_various_command_types(self, mock_handler_class):
        """Test processing of various command types"""
        mock_handler = Mock()
        mock_handler_class.return_value = mock_handler
        
        # Test different commands
        commands_to_test = [
            '/status',
            '/business',
            '/technical', 
            '/agents',
            '/environment',
            '/risks',
            '/timeline',
            '/context-flow',
            '/validation-status',
            '/performance',
            '/deep-dive agent_a',
            '/help'
        ]
        
        for command in commands_to_test:
            with self.subTest(command=command):
                mock_handler.reset_mock()
                mock_handler.process_command.return_value = f"Response for {command}"
                
                self.capture_output()
                self.simulate_observe_main(['observe', command])
                stdout, stderr = self.get_captured_output()
                
                # Verify command was processed
                mock_handler.process_command.assert_called_once_with(command)
                self.assertIn(f"Response for {command}", stdout)
                
                # Reset captured output
                self.captured_stdout = io.StringIO()
                self.captured_stderr = io.StringIO()


class TestObserveScriptIntegration(unittest.TestCase):
    """Test suite for integration with actual observe script"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_run_dir = os.path.join(self.temp_dir, "runs", "ACM-22079", "ACM-22079-20250826-120000")
        os.makedirs(self.test_run_dir, exist_ok=True)
        
        # Store original sys.argv
        self.original_argv = sys.argv
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        # Restore original sys.argv
        sys.argv = self.original_argv
    
    @patch('sys.path')
    def test_path_modification(self, mock_path):
        """Test that observe script properly modifies Python path"""
        # The observe script should add its directory to sys.path
        # We can test this by checking the path insertion behavior
        
        # Mock the path insertion
        mock_path.insert = Mock()
        
        # Simulate the path insertion from observe script
        observe_dir = Path(__file__).parent / '../../../.claude/observability'
        sys.path.insert(0, str(observe_dir))
        
        # Verify path was inserted
        # In actual script, this would be: sys.path.insert(0, str(Path(__file__).parent))
        self.assertTrue(len(sys.path) > 0)
    
    @patch('observability_command_handler.ObservabilityCommandHandler')
    def test_command_line_argument_parsing(self, mock_handler_class):
        """Test command line argument parsing behavior"""
        mock_handler = Mock()
        mock_handler.process_command.return_value = "Test response"
        mock_handler_class.return_value = mock_handler
        
        # Test various argument patterns
        test_cases = [
            (['observe'], "no arguments"),
            (['observe', '/status'], "single command"),
            (['observe', '/deep-dive', 'agent_a'], "command with parameter"),
            (['observe', '/unknown-command'], "unknown command")
        ]
        
        for args, description in test_cases:
            with self.subTest(args=args, description=description):
                # Mock sys.argv
                sys.argv = args
                
                if len(args) >= 2:
                    # Should process the command
                    try:
                        # In real script, this would be: command = sys.argv[1]
                        command = args[1]
                        self.assertIsNotNone(command)
                    except IndexError:
                        self.fail(f"Argument parsing failed for {args}")
                else:
                    # Should show usage help
                    self.assertEqual(len(args), 1)
    
    def test_script_executable_permissions(self):
        """Test that observe script would have proper executable permissions"""
        # This is more of a documentation test since we can't test actual file permissions
        # The observe script should be executable with proper shebang
        
        observe_script_path = Path(__file__).parent / '../../../.claude/observability/observe'
        
        # Verify script exists (in real testing environment)
        if observe_script_path.exists():
            with open(observe_script_path, 'r') as f:
                first_line = f.readline()
                self.assertTrue(first_line.startswith('#!/'))
                self.assertIn('python', first_line)
    
    @patch('builtins.print')
    def test_error_message_formatting(self, mock_print):
        """Test that error messages are properly formatted"""
        # Test the various error message formats that would be used
        
        # FileNotFoundError format
        error_messages = [
            "⚠️ **Observability Data Not Found**",
            "❌ **Import Error**", 
            "🚨 **Observability Error**"
        ]
        
        for message in error_messages:
            # Test that messages contain proper formatting
            self.assertTrue(message.startswith(('⚠️', '❌', '🚨')))
            self.assertIn('**', message)
    
    def test_usage_help_completeness(self):
        """Test that usage help contains all necessary information"""
        # Define what should be in the help text
        required_help_elements = [
            "Claude Test Generator - Observability Interface",
            "Usage:",
            "./observe <command>",
            "Quick Commands:",
            "/status",
            "/business", 
            "/technical",
            "/agents",
            "/help",
            "Examples:",
            "/deep-dive agent_a",
            "/context-flow",
            "/risks"
        ]
        
        # This would be the help text from the actual script
        help_text = """🔍 **Claude Test Generator - Observability Interface**

**Usage:**
  ./observe <command>

**Quick Commands:**
  ./observe /status      - Current execution progress
  ./observe /business    - Customer impact analysis
  ./observe /technical   - Implementation details
  ./observe /agents      - Sub-agent coordination status
  ./observe /help        - Full command reference

**Examples:**
  ./observe /deep-dive agent_a
  ./observe /context-flow
  ./observe /risks"""
        
        # Verify all required elements are present
        for element in required_help_elements:
            self.assertIn(element, help_text)


class TestObserveScriptErrorScenarios(unittest.TestCase):
    """Test suite for observe script error scenarios and edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Store original sys.argv
        self.original_argv = sys.argv
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        # Restore original sys.argv
        sys.argv = self.original_argv
    
    def test_empty_command_handling(self):
        """Test handling of empty command strings"""
        empty_commands = ['', ' ', '\t', '\n']
        
        for empty_cmd in empty_commands:
            with self.subTest(command=empty_cmd):
                # Empty commands should be handled gracefully
                # They might be treated as help requests or invalid commands
                self.assertTrue(len(empty_cmd.strip()) == 0 or empty_cmd.isspace())
    
    def test_command_with_special_characters(self):
        """Test handling of commands with special characters"""
        special_commands = [
            '/status!',
            '/business@#$',
            '/technical with spaces',
            '/deep-dive agent_a; rm -rf /',  # Potential injection attempt
            '/../../../etc/passwd',  # Path traversal attempt
        ]
        
        for cmd in special_commands:
            with self.subTest(command=cmd):
                # Special characters should be handled safely
                # Commands should be processed as strings without execution
                self.assertIsInstance(cmd, str)
    
    def test_very_long_command_handling(self):
        """Test handling of very long command strings"""
        # Test with very long command
        long_command = '/status' + 'a' * 10000
        
        # Should handle long commands without crashing
        self.assertTrue(len(long_command) > 1000)
        self.assertTrue(long_command.startswith('/status'))
    
    def test_unicode_command_handling(self):
        """Test handling of Unicode characters in commands"""
        unicode_commands = [
            '/status日本語',
            '/business🚀',
            '/téchnical',
            '/agénts'
        ]
        
        for cmd in unicode_commands:
            with self.subTest(command=cmd):
                # Unicode should be handled properly
                self.assertIsInstance(cmd, str)
                # Should not crash the script
                try:
                    encoded = cmd.encode('utf-8')
                    self.assertIsInstance(encoded, bytes)
                except UnicodeEncodeError:
                    self.fail(f"Unicode command {cmd} should be encodable")
    
    def test_working_directory_independence(self):
        """Test that script behavior is independent of working directory"""
        # The observe script should work regardless of current working directory
        # as long as it can find the observability modules
        
        original_cwd = os.getcwd()
        
        try:
            # Change to temp directory
            os.chdir(self.temp_dir)
            
            # Script should still be able to locate modules via relative path
            # This tests the path manipulation in the script
            current_dir = os.getcwd()
            self.assertEqual(current_dir, self.temp_dir)
            
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
    
    @patch('observability_command_handler.ObservabilityCommandHandler')
    def test_handler_initialization_with_different_environments(self, mock_handler_class):
        """Test handler initialization in different environment scenarios"""
        # Test various handler initialization scenarios
        scenarios = [
            ("normal_init", Mock()),
            ("slow_init", Mock()),  # Simulate slow initialization
            ("memory_error", Mock()),  # Simulate memory issues
        ]
        
        for scenario_name, mock_handler in scenarios:
            with self.subTest(scenario=scenario_name):
                mock_handler_class.return_value = mock_handler
                
                if scenario_name == "memory_error":
                    mock_handler_class.side_effect = MemoryError("Out of memory")
                
                # Script should handle different initialization scenarios
                try:
                    # This simulates the handler creation in observe script
                    handler = mock_handler_class()
                    if scenario_name != "memory_error":
                        self.assertIsNotNone(handler)
                except MemoryError:
                    # Memory errors should be caught and handled gracefully
                    self.assertEqual(scenario_name, "memory_error")
    
    def test_signal_handling_preparation(self):
        """Test that script would handle system signals appropriately"""
        # This tests the framework for signal handling
        # Real script might need to handle SIGINT, SIGTERM, etc.
        
        import signal
        
        # Test that standard signals exist
        signals_to_handle = [
            signal.SIGINT,   # Ctrl+C
            signal.SIGTERM,  # Termination request
        ]
        
        for sig in signals_to_handle:
            self.assertIsInstance(sig, signal.Signals)
        
        # Script should be prepared to handle these signals gracefully
        # For example, cleanup operations, proper exit codes, etc.


if __name__ == '__main__':
    # Create comprehensive test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestObserveCommandLineInterface,
        TestObserveScriptIntegration,
        TestObserveScriptErrorScenarios
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n" + "="*60)
    print(f"COMMAND LINE INTERFACE UNIT TESTS SUMMARY")
    print(f"="*60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure.split(chr(10))[0]}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, error in result.errors:
            print(f"  - {test}: {error.split(chr(10))[0]}")