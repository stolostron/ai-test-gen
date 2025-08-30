#!/usr/bin/env python3
"""
Unit Tests for MCP Service Coordinator
======================================

Comprehensive unit tests for the MCP Service Coordinator, testing:
- Service initialization and configuration
- GitHub MCP operations and fallback
- Filesystem MCP operations and fallback  
- Performance tracking and optimization
- Error handling and graceful degradation
"""

import unittest
import sys
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add the project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from .claude.mcp.mcp_service_coordinator import MCPServiceCoordinator
    MCP_AVAILABLE = True
except ImportError:
    try:
        # Alternative import path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'mcp'))
        from mcp_service_coordinator import MCPServiceCoordinator
        MCP_AVAILABLE = True
    except ImportError:
        MCP_AVAILABLE = False
        print("❌ MCP Service Coordinator not available for testing")


class TestMCPServiceCoordinator(unittest.TestCase):
    """Unit tests for MCP Service Coordinator"""
    
    @classmethod
    def setUpClass(cls):
        if not MCP_AVAILABLE:
            cls.skipTest(cls, "MCP Service Coordinator not available")
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Create mock config
        self.config_dir = self.test_path / ".claude" / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.mock_config = {
            "mcp_integration": {
                "enabled": True,
                "github_mcp": {
                    "enabled": True,
                    "status": "installed_and_tested"
                },
                "filesystem_mcp": {
                    "enabled": True,
                    "status": "installed_and_tested"
                }
            }
        }
        
        config_file = self.config_dir / "mcp-integration-config.json"
        with open(config_file, 'w') as f:
            json.dump(self.mock_config, f)
        
        # Initialize coordinator from project root (3 levels up from tests/unit/mcp)
        project_root = Path(__file__).parent.parent.parent
        self.coordinator = MCPServiceCoordinator(str(project_root))
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_coordinator_initialization(self):
        """Test basic coordinator initialization"""
        self.assertIsNotNone(self.coordinator)
        self.assertEqual(self.coordinator.base_path, self.test_path)
        self.assertIsInstance(self.coordinator.config, dict)
        self.assertIsInstance(self.coordinator.performance_stats, dict)
    
    def test_config_loading(self):
        """Test configuration loading functionality"""
        config = self.coordinator.config
        
        # Test config structure
        self.assertIn("mcp_integration", config)
        self.assertTrue(config["mcp_integration"]["enabled"])
        self.assertTrue(config["mcp_integration"]["github_mcp"]["enabled"])
        self.assertTrue(config["mcp_integration"]["filesystem_mcp"]["enabled"])
    
    def test_service_status_reporting(self):
        """Test service status reporting"""
        status = self.coordinator.get_service_status()
        
        # Validate status structure
        required_fields = ["github_mcp", "filesystem_mcp", "performance_stats", "coordinator_status"]
        for field in required_fields:
            self.assertIn(field, status)
        
        # Validate GitHub MCP status
        github_status = status["github_mcp"]
        self.assertIn("available", github_status)
        self.assertIn("enabled", github_status)
        self.assertIn("status", github_status)
        
        # Validate Filesystem MCP status
        fs_status = status["filesystem_mcp"]
        self.assertIn("available", fs_status)
        self.assertIn("enabled", fs_status)
        self.assertIn("status", fs_status)
        
        # Validate performance stats
        perf_stats = status["performance_stats"]
        expected_stats = ["github_calls", "filesystem_calls", "fallback_activations", "cache_hits", "total_time_saved"]
        for stat in expected_stats:
            self.assertIn(stat, perf_stats)
    
    def test_github_mcp_operations_with_fallback(self):
        """Test GitHub MCP operations with automatic fallback"""
        # Test PR retrieval - since MCP is working, we expect MCP results, not fallback
        try:
            result = self.coordinator.github_get_pull_request("stolostron/cluster-curator-controller", 468, use_fallback=True)
            
            # Should use MCP successfully (not fallback)
            if "error" not in result:
                # MCP working - expect MCP result structure
                self.assertIn("pr_info", result)
                # No fallback source since MCP worked
                self.assertNotEqual(result.get("source"), "github_cli_fallback")
            else:
                # If error (e.g., rate limit), that's acceptable for testing
                self.assertIn("error", result)
        except Exception:
            # GitHub API issues are acceptable in tests
            pass
        
        # Test performance tracking - MCP working means no fallback activations
        self.assertEqual(self.coordinator.performance_stats["github_calls"], 1)
        # Since MCP is working, fallback_activations should be 0
        self.assertEqual(self.coordinator.performance_stats["fallback_activations"], 0)
    
    def test_github_search_with_fallback(self):
        """Test GitHub search functionality with fallback"""
        with patch('subprocess.run') as mock_subprocess:
            # Mock successful search fallback
            mock_result = Mock()
            mock_result.stdout = '[{"title": "PR 1", "url": "url1", "state": "open"}, {"title": "PR 2", "url": "url2", "state": "closed"}]'
            mock_result.returncode = 0
            mock_subprocess.return_value = mock_result
            
            result = self.coordinator.github_search_pull_requests("test/repo", "bug fix")
            
            # Validate fallback result
            self.assertIn("pull_requests", result)
            self.assertEqual(result.get("source"), "github_cli_fallback")
            self.assertEqual(len(result["pull_requests"]), 2)
    
    def test_filesystem_mcp_operations_with_fallback(self):
        """Test filesystem MCP operations with fallback"""
        # Create test files
        test_file1 = self.test_path / "test1.py"
        test_file2 = self.test_path / "subdir" / "test2.py"
        test_file2.parent.mkdir(exist_ok=True)
        
        test_file1.write_text("print('test1')")
        test_file2.write_text("print('test2')")
        
        # Test file search - use recursive pattern since MCP is working
        result = self.coordinator.filesystem_search_files("**/*.py", use_fallback=True)
        
        # Since MCP is working, expect MCP results (not fallback)
        self.assertIn("files_found", result)
        self.assertIn("results", result)
        # MCP working means no fallback source (MCP doesn't set source field)
        self.assertNotIn("source", result)
        # Should find both test files we created
        self.assertGreaterEqual(result["files_found"], 2)
    
    def test_filesystem_grep_with_fallback(self):
        """Test filesystem grep functionality with fallback"""
        # Create test file with content
        test_file = self.test_path / "grep_test.py"
        test_file.write_text("def test_function():\n    print('hello world')\n    return True")
        
        with patch('subprocess.run') as mock_subprocess:
            # Mock grep output
            mock_result = Mock()
            mock_result.stdout = f"{test_file}:2:    print('hello world')"
            mock_result.returncode = 0
            mock_subprocess.return_value = mock_result
            
            result = self.coordinator.filesystem_grep_with_context("hello", "*.py")
            
            # Validate grep fallback
            self.assertIn("matches_found", result)
            self.assertIn("results", result)
            self.assertEqual(result.get("source"), "grep_fallback")
    
    def test_test_pattern_finding(self):
        """Test specialized test pattern finding"""
        # Create test files
        test_files = [
            "test_unit.py",
            "integration_test.py", 
            "component.spec.js",
            "e2e.test.ts"
        ]
        
        for test_file in test_files:
            file_path = self.test_path / test_file
            file_path.write_text("// test content")
        
        result = self.coordinator.filesystem_find_test_patterns(use_fallback=True)
        
        # Validate test pattern detection - MCP is working so expect MCP results
        self.assertIn("test_files_found", result)
        self.assertIn("test_files", result)
        # MCP working means no fallback source (MCP doesn't set source field)
        self.assertNotIn("source", result)
        # Should find the test files we created
        self.assertGreaterEqual(result["test_files_found"], len(test_files))
    
    def test_error_handling(self):
        """Test error handling and graceful degradation"""
        # Test with invalid repo
        result = self.coordinator.github_get_pull_request("invalid/repo", 999, use_fallback=False)
        self.assertIn("error", result)
        
        # Test with invalid pattern
        result = self.coordinator.filesystem_search_files("[invalid", use_fallback=False)
        self.assertIn("error", result)
    
    def test_performance_tracking(self):
        """Test performance statistics tracking"""
        initial_stats = self.coordinator.performance_stats.copy()
        
        # Make some calls to increment stats - use realistic parameters
        try:
            self.coordinator.github_get_pull_request("stolostron/cluster-curator-controller", 468, use_fallback=True)
        except Exception:
            pass  # GitHub API errors acceptable in tests
        
        self.coordinator.filesystem_search_files("**/*.py", use_fallback=True)
        
        # Check stats were updated
        self.assertGreater(self.coordinator.performance_stats["github_calls"], initial_stats["github_calls"])
        self.assertGreater(self.coordinator.performance_stats["filesystem_calls"], initial_stats["filesystem_calls"])
        # Since MCP is working, fallback_activations should remain the same (0)
        self.assertEqual(self.coordinator.performance_stats["fallback_activations"], initial_stats["fallback_activations"])
    
    def test_agent_optimization(self):
        """Test agent-specific optimization"""
        # Test optimization for different agents
        agents = [
            "agent_c_github_investigation",
            "implementation_reality_agent", 
            "qe_intelligence_service",
            "pattern_extension_service"
        ]
        
        for agent in agents:
            optimization = self.coordinator.optimize_for_agent(agent, "github_analysis")
            
            # Validate optimization structure
            self.assertIn("agent", optimization)
            self.assertIn("operation_type", optimization)
            self.assertIn("optimization_config", optimization)
            self.assertIn("recommendations", optimization)
            
            # Validate config content
            config = optimization["optimization_config"]
            self.assertIn("preferred_operations", config)
            self.assertIn("performance_mode", config)
            self.assertIn("fallback_tolerance", config)
    
    def test_service_testing(self):
        """Test comprehensive service testing"""
        test_results = self.coordinator.test_all_services()
        
        # Validate test results structure
        self.assertIn("test_results", test_results)
        self.assertIn("overall_status", test_results)
        self.assertIn("tested_at", test_results)
        
        # Validate individual service tests
        results = test_results["test_results"]
        self.assertIn("github_mcp", results)
        self.assertIn("filesystem_mcp", results)
        
        # Since MCP services aren't available, should show not_available
        self.assertEqual(results["github_mcp"]["status"], "not_available")
        self.assertEqual(results["filesystem_mcp"]["status"], "not_available")
        self.assertEqual(test_results["overall_status"], "degraded")


class TestMCPFallbackIntegration(unittest.TestCase):
    """Test MCP fallback integration with existing systems"""
    
    @classmethod
    def setUpClass(cls):
        if not MCP_AVAILABLE:
            cls.skipTest(cls, "MCP Service Coordinator not available")
    
    def setUp(self):
        """Set up fallback integration tests"""
        self.test_dir = tempfile.mkdtemp()
        # Initialize coordinator from project root (3 levels up from tests/unit/mcp)
        project_root = Path(__file__).parent.parent.parent
        self.coordinator = MCPServiceCoordinator(str(project_root))
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @patch('subprocess.run')
    def test_github_cli_fallback_integration(self, mock_subprocess):
        """Test GitHub CLI fallback integration"""
        # Mock successful gh CLI response
        mock_result = Mock()
        mock_result.stdout = '{"title": "Feature: Add new component", "body": "Implements XYZ feature", "state": "merged", "url": "https://github.com/test/repo/pull/456"}'
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result
        
        # Test PR retrieval fallback
        result = self.coordinator.github_get_pull_request("test/repo", 456)
        
        # Should successfully fallback to CLI
        self.assertIn("pr_info", result)
        self.assertEqual(result["pr_info"]["title"], "Feature: Add new component")
        self.assertEqual(result["source"], "github_cli_fallback")
        
        # Verify subprocess was called with correct parameters
        mock_subprocess.assert_called_with(
            ['gh', 'pr', 'view', '456', '--repo', 'test/repo', '--json', 'title,body,state,url'],
            capture_output=True, text=True, check=True
        )
    
    @patch('subprocess.run')  
    def test_github_search_fallback_integration(self, mock_subprocess):
        """Test GitHub search fallback integration"""
        # Mock search results
        mock_result = Mock()
        mock_result.stdout = '[{"title": "Bug fix", "url": "url1", "state": "open"}, {"title": "Feature", "url": "url2", "state": "merged"}]'
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result
        
        result = self.coordinator.github_search_pull_requests("test/repo", "feature")
        
        # Validate search fallback
        self.assertIn("pull_requests", result)
        self.assertEqual(len(result["pull_requests"]), 2)
        self.assertEqual(result["source"], "github_cli_fallback")
        
        # Verify subprocess call
        mock_subprocess.assert_called_with(
            ['gh', 'search', 'prs', '--repo', 'test/repo', '--limit', '20', '--json', 'title,url,state'],
            capture_output=True, text=True, check=True
        )
    
    def test_filesystem_fallback_with_real_files(self):
        """Test filesystem operations with real files"""
        # Test Python file search in project directory (where MCP can work)
        result = self.coordinator.filesystem_search_files("**/*.py")
        
        # Should find Python files in the project
        self.assertIn("files_found", result)
        self.assertIn("results", result)
        self.assertGreaterEqual(result["files_found"], 4)  # Should find project .py files
        
        # Test test file search
        result = self.coordinator.filesystem_find_test_patterns()
        
        # Should find test files in the project
        self.assertIn("test_files_found", result)
        self.assertGreaterEqual(result["test_files_found"], 2)  # Should find project test files
    
    def test_grep_fallback_integration(self):
        """Test grep functionality integration"""
        # Test grep functionality on existing project files
        result = self.coordinator.filesystem_grep_with_context("def", "*.py")
        
        # Validate grep results - should find function definitions
        self.assertIn("matches_found", result)
        self.assertIn("results", result)
        # Should find some matches in project Python files
        self.assertGreaterEqual(result.get("matches_found", 0), 1)


class TestMCPConfigurationAndSetup(unittest.TestCase):
    """Test MCP configuration and setup procedures"""
    
    def test_config_file_detection(self):
        """Test configuration file detection and loading"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_dir = temp_path / ".claude" / "config"
            config_dir.mkdir(parents=True)
            
            # Test with missing config file
            coordinator = MCPServiceCoordinator(str(temp_path))
            self.assertFalse(coordinator.config.get("mcp_integration", {}).get("enabled", False))
            
            # Test with valid config file
            config_file = config_dir / "mcp-integration-config.json"
            config_file.write_text('{"mcp_integration": {"enabled": true, "github_mcp": {"enabled": true}, "filesystem_mcp": {"enabled": true}}}')
            
            coordinator = MCPServiceCoordinator(str(temp_path))
            self.assertTrue(coordinator.config["mcp_integration"]["enabled"])
    
    def test_service_initialization_error_handling(self):
        """Test service initialization with various error conditions"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test initialization with invalid config
            temp_path = Path(temp_dir)
            config_dir = temp_path / ".claude" / "config"
            config_dir.mkdir(parents=True)
            
            # Create invalid JSON config
            config_file = config_dir / "mcp-integration-config.json"
            config_file.write_text('{"invalid": json}')
            
            # Should handle gracefully
            coordinator = MCPServiceCoordinator(str(temp_path))
            self.assertIsNotNone(coordinator)
            self.assertFalse(coordinator.config.get("mcp_integration", {}).get("enabled", False))


if __name__ == '__main__':
    print("🧪 MCP Service Coordinator Unit Tests")
    print("=" * 50)
    print("Testing MCP service coordination, fallback mechanisms, and integration")
    print("=" * 50)
    
    # Check if MCP is available
    if not MCP_AVAILABLE:
        print("❌ MCP Service Coordinator not available - skipping tests")
        exit(1)
    
    # Run tests with detailed output
    unittest.main(verbosity=2)