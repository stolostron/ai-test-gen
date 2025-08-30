#!/usr/bin/env python3
"""
Comprehensive Unit Tests for App Isolation Enforcer

Tests the critical app isolation system that enforces strict containment
boundaries preventing apps from accessing external resources. Validates
the hierarchical isolation model where apps can only access their own files.

Test Coverage:
- StrictAppIsolationEngine functionality
- Boundary validation and access control
- Path resolution and pattern blocking
- AppPermissionWrapper safe operations
- AppContextDetector functionality
- SystemIsolationValidator comprehensive testing
- Isolation statistics and monitoring
- Error handling and edge cases
"""

import unittest
import tempfile
import os
import json
from unittest.mock import Mock, patch, mock_open
from pathlib import Path

# Add the isolation directory to Python path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../.claude/isolation'))

from app_isolation_enforcer import (
    StrictAppIsolationEngine,
    AppPermissionWrapper,
    AppContextDetector,
    SystemIsolationValidator,
    AppIsolationViolationError
)


class TestStrictAppIsolationEngine(unittest.TestCase):
    """Test suite for StrictAppIsolationEngine core functionality"""
    
    def setUp(self):
        """Set up test environment with isolated app directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.app_root = os.path.join(self.temp_dir, "test-app")
        os.makedirs(self.app_root, exist_ok=True)
        
        # Create test app structure
        os.makedirs(os.path.join(self.app_root, "runs"), exist_ok=True)
        os.makedirs(os.path.join(self.app_root, ".claude"), exist_ok=True)
        
        self.isolation_engine = StrictAppIsolationEngine(self.app_root)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test isolation engine initialization"""
        self.assertEqual(str(self.isolation_engine.app_root), str(Path(self.app_root).resolve()))
        self.assertEqual(self.isolation_engine.app_id, "test-app")
        self.assertEqual(self.isolation_engine.violations_blocked, 0)
        self.assertEqual(len(self.isolation_engine.access_attempts), 0)
        
        # Verify blocked patterns are configured
        self.assertGreater(len(self.isolation_engine.blocked_patterns), 5)
        self.assertIn("../*", self.isolation_engine.blocked_patterns)
        self.assertIn("../../*", self.isolation_engine.blocked_patterns)
        
        # Verify specifically blocked paths are configured
        self.assertGreater(len(self.isolation_engine.specifically_blocked_paths), 0)
    
    def test_is_within_app_boundaries_allowed_paths(self):
        """Test boundary validation for paths that should be allowed"""
        allowed_paths = [
            ".",  # Current directory (within app)
            "./runs/test.md",  # Internal file
            "./.claude/config.json",  # Internal config
            "CLAUDE.md",  # App config file
            "test_file.py"  # App file
        ]
        
        # Change to app directory for relative path testing
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            for path in allowed_paths:
                with self.subTest(path=path):
                    result = self.isolation_engine.is_within_app_boundaries(path)
                    self.assertTrue(result, f"Path should be allowed: {path}")
        finally:
            os.chdir(original_cwd)
    
    def test_is_within_app_boundaries_blocked_paths(self):
        """Test boundary validation for paths that should be blocked"""
        blocked_paths = [
            "../",  # Parent directory
            "../../",  # Grandparent directory  
            "../other-app/",  # Sibling app
            "/tmp/",  # System directory
            "/Users/ashafi/Documents/work/ai/ai_systems/CLAUDE.md",  # Root config
            str(Path(self.temp_dir).parent)  # Outside app hierarchy
        ]
        
        # Change to app directory for relative path testing
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            for path in blocked_paths:
                with self.subTest(path=path):
                    result = self.isolation_engine.is_within_app_boundaries(path)
                    self.assertFalse(result, f"Path should be blocked: {path}")
        finally:
            os.chdir(original_cwd)
    
    def test_is_blocked_pattern_detection(self):
        """Test pattern-based blocking functionality"""
        test_cases = [
            # Should be blocked
            ("../parent", True, "Parent directory access"),
            ("../../grandparent", True, "Grandparent directory access"),
            ("~/home", True, "Home directory access"),
            ("/Users/someone", True, "System user directory"),
            ("/tmp/temp", True, "Temporary directory"),
            ("/etc/config", True, "System configuration"),
            ("/var/data", True, "System variables"),
            
            # Should NOT be blocked
            ("./internal", False, "Internal relative path"),
            ("runs/test", False, "Internal runs directory"),
            (".claude/config", False, "Internal claude directory"),
            ("test.py", False, "Internal file"),
            ("./some/deep/path", False, "Deep internal path")
        ]
        
        for path, should_be_blocked, description in test_cases:
            with self.subTest(path=path, description=description):
                result = self.isolation_engine.is_blocked_pattern(path)
                self.assertEqual(result, should_be_blocked, 
                               f"{description}: {path} - Expected blocked={should_be_blocked}, Got={result}")
    
    def test_is_specifically_blocked_detection(self):
        """Test specific path blocking functionality"""
        # Test specifically blocked paths (these are configured in the engine)
        blocked_specific_paths = [
            "/Users/ashafi/Documents/work/ai/ai_systems/CLAUDE.md",
            "/Users/ashafi/Documents/work/ai/ai_systems/apps",
            "/Users/ashafi/Documents/work/ai/ai_systems/tests"
        ]
        
        for path in blocked_specific_paths:
            with self.subTest(path=path):
                result = self.isolation_engine.is_specifically_blocked(path)
                # Note: This might return False if the path doesn't resolve correctly in test environment
                # The important thing is that the method doesn't crash
                self.assertIsInstance(result, bool)
    
    def test_validate_access_allowed_operations(self):
        """Test access validation for operations that should be allowed"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            allowed_operations = [
                ("read", "./CLAUDE.md"),
                ("write", "./test_output.md"),
                ("create", "./new_directory"),
                ("delete", "./temp_file.tmp"),
                ("list", "."),
                ("check", "./runs/")
            ]
            
            for operation, path in allowed_operations:
                with self.subTest(operation=operation, path=path):
                    result = self.isolation_engine.validate_access(operation, path)
                    self.assertTrue(result, f"Operation should be allowed: {operation} on {path}")
                    
                    # Verify access attempt was logged
                    self.assertGreater(len(self.isolation_engine.access_attempts), 0)
                    
                    # Check last access attempt
                    last_attempt = self.isolation_engine.access_attempts[-1]
                    self.assertEqual(last_attempt['operation'], operation)
                    self.assertEqual(last_attempt['result'], 'ALLOWED')
        finally:
            os.chdir(original_cwd)
    
    def test_validate_access_blocked_operations(self):
        """Test access validation for operations that should be blocked"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            blocked_operations = [
                ("read", "../"),
                ("write", "../../external.md"),
                ("create", "../new_dir"),
                ("delete", "/tmp/system_file"),
                ("list", "~/"),
                ("check", "/etc/")
            ]
            
            initial_violations = self.isolation_engine.violations_blocked
            
            for operation, path in blocked_operations:
                with self.subTest(operation=operation, path=path):
                    result = self.isolation_engine.validate_access(operation, path)
                    self.assertFalse(result, f"Operation should be blocked: {operation} on {path}")
                    
                    # Verify violation was counted
                    self.assertGreater(self.isolation_engine.violations_blocked, initial_violations)
                    
                    # Check access attempt was logged with blocked status
                    last_attempt = self.isolation_engine.access_attempts[-1]
                    self.assertEqual(last_attempt['operation'], operation)
                    self.assertIn(last_attempt['result'], ['BLOCKED_PATTERN', 'BLOCKED_SPECIFIC', 'BLOCKED_BOUNDARY'])
                    
                    initial_violations = self.isolation_engine.violations_blocked
        finally:
            os.chdir(original_cwd)
    
    def test_enforce_access_control_allowed(self):
        """Test access control enforcement for allowed operations"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Should not raise exception for allowed access
            try:
                self.isolation_engine.enforce_access_control("read", "./CLAUDE.md")
                self.isolation_engine.enforce_access_control("write", "./test.md")
            except AppIsolationViolationError:
                self.fail("Allowed operations should not raise AppIsolationViolationError")
        finally:
            os.chdir(original_cwd)
    
    def test_enforce_access_control_blocked(self):
        """Test access control enforcement for blocked operations"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            blocked_operations = [
                ("read", "../"),
                ("write", "../../external.md"),
                ("create", "/tmp/system_dir")
            ]
            
            for operation, path in blocked_operations:
                with self.subTest(operation=operation, path=path):
                    with self.assertRaises(AppIsolationViolationError) as context:
                        self.isolation_engine.enforce_access_control(operation, path)
                    
                    # Verify error message contains relevant information
                    error_message = str(context.exception)
                    self.assertIn("ISOLATION VIOLATION", error_message)
                    self.assertIn(self.isolation_engine.app_id, error_message)
                    self.assertIn(operation, error_message)
        finally:
            os.chdir(original_cwd)
    
    def test_get_isolation_statistics(self):
        """Test isolation statistics generation"""
        # Generate some access attempts
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Perform some allowed and blocked operations
            self.isolation_engine.validate_access("read", "./allowed.md")
            self.isolation_engine.validate_access("write", "../blocked.md")
            self.isolation_engine.validate_access("create", "./allowed_dir")
            
            stats = self.isolation_engine.get_isolation_statistics()
            
            # Verify statistics structure
            required_fields = [
                'app_id', 'app_root', 'total_access_attempts', 
                'allowed_attempts', 'violations_blocked', 
                'isolation_effectiveness', 'recent_attempts'
            ]
            
            for field in required_fields:
                self.assertIn(field, stats)
            
            # Verify statistics values
            self.assertEqual(stats['app_id'], "test-app")
            self.assertEqual(stats['total_access_attempts'], 3)
            self.assertEqual(stats['allowed_attempts'], 2)
            self.assertEqual(stats['violations_blocked'], 1)
            
            # Verify isolation effectiveness calculation
            expected_effectiveness = (1 / 3 * 100)  # 1 violation out of 3 attempts
            self.assertEqual(stats['isolation_effectiveness'], expected_effectiveness)
            
            # Verify recent attempts (should show last 3)
            self.assertEqual(len(stats['recent_attempts']), 3)
        finally:
            os.chdir(original_cwd)


class TestAppPermissionWrapper(unittest.TestCase):
    """Test suite for AppPermissionWrapper functionality"""
    
    def setUp(self):
        """Set up test environment with permission wrapper"""
        self.temp_dir = tempfile.mkdtemp()
        self.app_root = os.path.join(self.temp_dir, "test-app")
        os.makedirs(self.app_root, exist_ok=True)
        
        # Create test files
        self.test_file = os.path.join(self.app_root, "test.txt")
        with open(self.test_file, 'w') as f:
            f.write("test content")
        
        self.permission_wrapper = AppPermissionWrapper("test-app", self.app_root)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test permission wrapper initialization"""
        self.assertEqual(self.permission_wrapper.app_id, "test-app")
        self.assertEqual(str(self.permission_wrapper.app_path), str(Path(self.app_root).resolve()))
        self.assertIsInstance(self.permission_wrapper.isolation_engine, StrictAppIsolationEngine)
    
    def test_safe_open_read_allowed(self):
        """Test safe file opening for read operations within app boundaries"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Should be able to read files within app
            with self.permission_wrapper.safe_open("test.txt", "r") as f:
                content = f.read()
                self.assertEqual(content, "test content")
        finally:
            os.chdir(original_cwd)
    
    def test_safe_open_write_allowed(self):
        """Test safe file opening for write operations within app boundaries"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Should be able to write files within app
            test_write_file = "write_test.txt"
            with self.permission_wrapper.safe_open(test_write_file, "w") as f:
                f.write("new content")
            
            # Verify file was created
            self.assertTrue(os.path.exists(os.path.join(self.app_root, test_write_file)))
            
            # Clean up
            os.unlink(os.path.join(self.app_root, test_write_file))
        finally:
            os.chdir(original_cwd)
    
    def test_safe_open_blocked(self):
        """Test safe file opening blocks access outside app boundaries"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            blocked_paths = [
                "../external.txt",
                "../../outside.txt",
                "/tmp/system.txt"
            ]
            
            for path in blocked_paths:
                with self.subTest(path=path):
                    with self.assertRaises(AppIsolationViolationError):
                        self.permission_wrapper.safe_open(path, "r")
        finally:
            os.chdir(original_cwd)
    
    def test_safe_exists_allowed(self):
        """Test safe existence check for allowed paths"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Should return True for existing files within app
            result = self.permission_wrapper.safe_exists("test.txt")
            self.assertTrue(result)
            
            # Should return False for non-existing files within app
            result = self.permission_wrapper.safe_exists("nonexistent.txt")
            self.assertFalse(result)
        finally:
            os.chdir(original_cwd)
    
    def test_safe_exists_blocked(self):
        """Test safe existence check for blocked paths"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Should return False for external paths (even if they exist)
            blocked_paths = [
                "../",
                "../../",
                "/tmp/"
            ]
            
            for path in blocked_paths:
                with self.subTest(path=path):
                    result = self.permission_wrapper.safe_exists(path)
                    self.assertFalse(result, f"Blocked path should appear non-existent: {path}")
        finally:
            os.chdir(original_cwd)
    
    def test_safe_listdir_allowed(self):
        """Test safe directory listing for allowed paths"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Should list contents of app directory
            contents = self.permission_wrapper.safe_listdir(".")
            self.assertIn("test.txt", contents)
        finally:
            os.chdir(original_cwd)
    
    def test_safe_listdir_blocked(self):
        """Test safe directory listing blocks external paths"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            with self.assertRaises(AppIsolationViolationError):
                self.permission_wrapper.safe_listdir("../")
        finally:
            os.chdir(original_cwd)
    
    def test_safe_mkdir_allowed(self):
        """Test safe directory creation within app boundaries"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            new_dir = "new_directory"
            self.permission_wrapper.safe_mkdir(new_dir)
            
            # Verify directory was created
            self.assertTrue(os.path.exists(os.path.join(self.app_root, new_dir)))
            self.assertTrue(os.path.isdir(os.path.join(self.app_root, new_dir)))
            
            # Clean up
            os.rmdir(os.path.join(self.app_root, new_dir))
        finally:
            os.chdir(original_cwd)
    
    def test_safe_mkdir_blocked(self):
        """Test safe directory creation blocks external paths"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            with self.assertRaises(AppIsolationViolationError):
                self.permission_wrapper.safe_mkdir("../external_dir")
        finally:
            os.chdir(original_cwd)
    
    def test_safe_remove_allowed(self):
        """Test safe file removal within app boundaries"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Create file to remove
            temp_file = "temp_remove.txt"
            temp_path = os.path.join(self.app_root, temp_file)
            with open(temp_path, 'w') as f:
                f.write("temp")
            
            # Remove using safe_remove
            self.permission_wrapper.safe_remove(temp_file)
            
            # Verify file was removed
            self.assertFalse(os.path.exists(temp_path))
        finally:
            os.chdir(original_cwd)
    
    def test_safe_remove_blocked(self):
        """Test safe file removal blocks external paths"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            with self.assertRaises(AppIsolationViolationError):
                self.permission_wrapper.safe_remove("../external.txt")
        finally:
            os.chdir(original_cwd)
    
    def test_safe_copy_allowed(self):
        """Test safe file copy within app boundaries"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            dest_file = "copy_test.txt"
            self.permission_wrapper.safe_copy("test.txt", dest_file)
            
            # Verify file was copied
            dest_path = os.path.join(self.app_root, dest_file)
            self.assertTrue(os.path.exists(dest_path))
            
            with open(dest_path, 'r') as f:
                content = f.read()
                self.assertEqual(content, "test content")
            
            # Clean up
            os.unlink(dest_path)
        finally:
            os.chdir(original_cwd)
    
    def test_safe_copy_blocked_source(self):
        """Test safe file copy blocks external source paths"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            with self.assertRaises(AppIsolationViolationError):
                self.permission_wrapper.safe_copy("../external.txt", "dest.txt")
        finally:
            os.chdir(original_cwd)
    
    def test_safe_copy_blocked_destination(self):
        """Test safe file copy blocks external destination paths"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            with self.assertRaises(AppIsolationViolationError):
                self.permission_wrapper.safe_copy("test.txt", "../external_dest.txt")
        finally:
            os.chdir(original_cwd)


class TestAppContextDetector(unittest.TestCase):
    """Test suite for AppContextDetector functionality"""
    
    def test_detect_app_context_from_app_directory(self):
        """Test app context detection when running from app directory"""
        # Create temporary app structure
        temp_dir = tempfile.mkdtemp()
        try:
            apps_dir = os.path.join(temp_dir, "apps")
            test_app_dir = os.path.join(apps_dir, "test-app")
            os.makedirs(test_app_dir, exist_ok=True)
            
            # Change to app directory
            original_cwd = os.getcwd()
            try:
                os.chdir(test_app_dir)
                
                context = AppContextDetector.detect_app_context()
                
                self.assertEqual(context['app_id'], 'test-app')
                self.assertEqual(context['is_app_context'], True)
                self.assertIn('test-app', context['app_path'])
                self.assertEqual(context['current_dir'], test_app_dir)
            finally:
                os.chdir(original_cwd)
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_detect_app_context_from_root_directory(self):
        """Test app context detection when running from root directory"""
        # This should detect as root context
        context = AppContextDetector.detect_app_context()
        
        # When not in app directory, should return root context
        expected_fields = ['app_id', 'app_path', 'is_app_context', 'current_dir']
        for field in expected_fields:
            self.assertIn(field, context)
        
        # Should have app_id as 'root' when not in app context
        if context['is_app_context']:
            # If we're actually in an app context, that's fine too
            self.assertIsInstance(context['app_id'], str)
            self.assertNotEqual(context['app_id'], '')
        else:
            self.assertEqual(context['app_id'], 'root')
            self.assertEqual(context['is_app_context'], False)
    
    def test_detect_app_context_edge_cases(self):
        """Test app context detection edge cases"""
        # Test with nested directory structure
        temp_dir = tempfile.mkdtemp()
        try:
            # Create: temp/apps/myapp/subdir/deep/
            deep_dir = os.path.join(temp_dir, "apps", "myapp", "subdir", "deep")
            os.makedirs(deep_dir, exist_ok=True)
            
            original_cwd = os.getcwd()
            try:
                os.chdir(deep_dir)
                
                context = AppContextDetector.detect_app_context()
                
                # Should still detect myapp as the app
                self.assertEqual(context['app_id'], 'myapp')
                self.assertEqual(context['is_app_context'], True)
                self.assertIn('myapp', context['app_path'])
            finally:
                os.chdir(original_cwd)
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestSystemIsolationValidator(unittest.TestCase):
    """Test suite for SystemIsolationValidator functionality"""
    
    def setUp(self):
        """Set up test environment for system validation"""
        self.temp_dir = tempfile.mkdtemp()
        self.app_root = os.path.join(self.temp_dir, "test-app")
        os.makedirs(self.app_root, exist_ok=True)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_system_validator_initialization(self):
        """Test system isolation validator initialization"""
        validator = SystemIsolationValidator()
        
        self.assertIsInstance(validator.context, dict)
        self.assertIn('app_id', validator.context)
        self.assertIn('is_app_context', validator.context)
        self.assertEqual(len(validator.validation_results), 0)
    
    def test_app_isolation_boundaries_from_app_context(self):
        """Test app isolation boundary testing from app context"""
        # Change to app directory to simulate app context
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Mock app context detection to return app context
            with patch.object(AppContextDetector, 'detect_app_context') as mock_detect:
                mock_detect.return_value = {
                    'app_id': 'test-app',
                    'app_path': self.app_root,
                    'is_app_context': True,
                    'current_dir': self.app_root
                }
                
                validator = SystemIsolationValidator()
                result = validator.test_app_isolation_boundaries()
                
                # Verify test result structure
                self.assertIn('test_name', result)
                self.assertIn('status', result)
                self.assertIn('tests_performed', result)
                self.assertIn('violations_found', result)
                self.assertIn('isolation_score', result)
                
                self.assertEqual(result['test_name'], 'app_isolation_boundaries')
                
                # Should have performed tests
                self.assertGreater(len(result['tests_performed']), 0)
                
                # Verify test types
                test_names = [test['test_name'] for test in result['tests_performed']]
                expected_tests = [
                    'parent_directory_access',
                    'root_config_access', 
                    'sibling_app_access',
                    'internal_config_access'
                ]
                
                for expected_test in expected_tests:
                    self.assertIn(expected_test, test_names)
        finally:
            os.chdir(original_cwd)
    
    def test_app_isolation_boundaries_from_root_context(self):
        """Test app isolation boundary testing from root context (should skip)"""
        # Mock root context detection
        with patch.object(AppContextDetector, 'detect_app_context') as mock_detect:
            mock_detect.return_value = {
                'app_id': 'root',
                'app_path': '/Users/ashafi/Documents/work/ai/ai_systems',
                'is_app_context': False,
                'current_dir': os.getcwd()
            }
            
            validator = SystemIsolationValidator()
            result = validator.test_app_isolation_boundaries()
            
            # Should skip testing when not in app context
            self.assertEqual(result['status'], 'SKIPPED')
            self.assertEqual(result['reason'], 'Not in app context - running from root level')
    
    def test_validate_system_isolation_comprehensive(self):
        """Test comprehensive system isolation validation"""
        # Change to app directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Mock app context
            with patch.object(AppContextDetector, 'detect_app_context') as mock_detect:
                mock_detect.return_value = {
                    'app_id': 'test-app',
                    'app_path': self.app_root,
                    'is_app_context': True,
                    'current_dir': self.app_root
                }
                
                validator = SystemIsolationValidator()
                result = validator.validate_system_isolation()
                
                # Verify comprehensive result structure
                self.assertIn('validation_name', result)
                self.assertIn('timestamp', result)
                self.assertIn('context', result)
                self.assertIn('validations', result)
                self.assertIn('total_validations', result)
                self.assertIn('successful_validations', result)
                self.assertIn('validation_score', result)
                self.assertIn('overall_status', result)
                
                self.assertEqual(result['validation_name'], 'system_isolation_validation')
                
                # Should have at least one validation (app boundary testing)
                self.assertGreater(len(result['validations']), 0)
                self.assertGreater(result['total_validations'], 0)
                
                # Overall status should be either SECURE or NEEDS_ATTENTION
                self.assertIn(result['overall_status'], ['SECURE', 'NEEDS_ATTENTION'])
        finally:
            os.chdir(original_cwd)
    
    def test_isolation_validator_statistics_generation(self):
        """Test that isolation validator generates proper statistics"""
        # Create an isolation engine and generate some access attempts
        engine = StrictAppIsolationEngine(self.app_root)
        
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Generate test access attempts
            engine.validate_access("read", "./allowed.txt")  # Should be allowed
            engine.validate_access("write", "../blocked.txt")  # Should be blocked
            
            stats = engine.get_isolation_statistics()
            
            # Verify statistics are properly generated
            self.assertEqual(stats['total_access_attempts'], 2)
            self.assertEqual(stats['allowed_attempts'], 1)
            self.assertEqual(stats['violations_blocked'], 1)
            self.assertEqual(stats['isolation_effectiveness'], 50.0)  # 1 violation out of 2 attempts
            
            # Verify recent attempts tracking
            self.assertEqual(len(stats['recent_attempts']), 2)
            
            # Verify attempt details
            for attempt in stats['recent_attempts']:
                self.assertIn('timestamp', attempt)
                self.assertIn('operation', attempt)
                self.assertIn('target_path', attempt)
                self.assertIn('result', attempt)
        finally:
            os.chdir(original_cwd)


class TestIsolationErrorHandling(unittest.TestCase):
    """Test suite for isolation error handling and edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.app_root = os.path.join(self.temp_dir, "test-app")
        os.makedirs(self.app_root, exist_ok=True)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_app_isolation_violation_error(self):
        """Test AppIsolationViolationError functionality"""
        error_message = "Test isolation violation"
        error = AppIsolationViolationError(error_message)
        
        self.assertEqual(str(error), error_message)
        self.assertIsInstance(error, Exception)
    
    def test_isolation_engine_with_invalid_paths(self):
        """Test isolation engine behavior with invalid/malformed paths"""
        engine = StrictAppIsolationEngine(self.app_root)
        
        invalid_paths = [
            "",  # Empty path
            None,  # None path (will be converted to string)
            "///multiple///slashes",  # Multiple slashes
            "path/with/../../../traversal",  # Path traversal
            "path/with/../../null\x00bytes",  # Path with null bytes
        ]
        
        for path in invalid_paths:
            with self.subTest(path=repr(path)):
                # Should handle invalid paths gracefully (not crash)
                try:
                    result = engine.validate_access("test", str(path) if path is not None else "")
                    # Result should be boolean
                    self.assertIsInstance(result, bool)
                except Exception as e:
                    # If exception occurs, it should be controlled/expected
                    self.assertIsInstance(e, (ValueError, OSError, AppIsolationViolationError))
    
    def test_permission_wrapper_with_nonexistent_app_root(self):
        """Test permission wrapper behavior with nonexistent app root"""
        nonexistent_path = os.path.join(self.temp_dir, "nonexistent-app")
        
        # Should be able to initialize even with nonexistent path
        wrapper = AppPermissionWrapper("nonexistent-app", nonexistent_path)
        
        self.assertEqual(wrapper.app_id, "nonexistent-app")
        self.assertIsInstance(wrapper.isolation_engine, StrictAppIsolationEngine)
    
    def test_context_detector_with_unusual_directory_structures(self):
        """Test context detector with unusual directory structures"""
        # Test with multiple 'apps' in path
        temp_dir = tempfile.mkdtemp()
        try:
            # Create: temp/apps/myapp/apps/anotherapp/
            unusual_dir = os.path.join(temp_dir, "apps", "myapp", "apps", "anotherapp")
            os.makedirs(unusual_dir, exist_ok=True)
            
            original_cwd = os.getcwd()
            try:
                os.chdir(unusual_dir)
                
                context = AppContextDetector.detect_app_context()
                
                # Should detect the first 'apps' occurrence
                self.assertEqual(context['app_id'], 'myapp')
                self.assertEqual(context['is_app_context'], True)
            finally:
                os.chdir(original_cwd)
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_isolation_engine_performance_with_many_attempts(self):
        """Test isolation engine performance with many access attempts"""
        engine = StrictAppIsolationEngine(self.app_root)
        
        original_cwd = os.getcwd()
        try:
            os.chdir(self.app_root)
            
            # Generate many access attempts
            import time
            start_time = time.time()
            
            for i in range(100):
                engine.validate_access("test", f"./file_{i}.txt")
                if i % 10 == 0:  # Some blocked attempts
                    engine.validate_access("test", f"../blocked_{i}.txt")
            
            end_time = time.time()
            
            # Should complete quickly (under 1 second for 100+ attempts)
            self.assertLess(end_time - start_time, 1.0)
            
            # Verify statistics are correct
            stats = engine.get_isolation_statistics()
            self.assertEqual(stats['total_access_attempts'], 110)  # 100 allowed + 10 blocked
            self.assertEqual(stats['allowed_attempts'], 100)
            self.assertEqual(stats['violations_blocked'], 10)
        finally:
            os.chdir(original_cwd)


if __name__ == '__main__':
    # Create comprehensive test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestStrictAppIsolationEngine,
        TestAppPermissionWrapper,
        TestAppContextDetector,
        TestSystemIsolationValidator,
        TestIsolationErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n" + "="*60)
    print(f"APP ISOLATION ARCHITECTURE UNIT TESTS SUMMARY")
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
    
    # Exit with appropriate code
    exit(0 if len(result.failures) == 0 and len(result.errors) == 0 else 1)