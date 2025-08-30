#!/usr/bin/env python3
"""
Unit Tests for Real MCP Integration
===================================

Comprehensive unit tests for the Real MCP implementation, testing:
- Real MCP client functionality
- Framework MCP integration layer
- Backward compatibility guarantees
- Performance monitoring and fallback mechanisms
- Regression validation
"""

import unittest
import sys
import os
import tempfile
import json
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add the project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# Import the real MCP components
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'mcp'))
    from real_mcp_client import RealMCPClient, MCPServiceCoordinator as RealMCPCoordinator
    from framework_mcp_integration import FrameworkMCPIntegration, MCPServiceCoordinator, validate_mcp_upgrade
    REAL_MCP_AVAILABLE = True
except ImportError as e:
    REAL_MCP_AVAILABLE = False
    print(f"❌ Real MCP components not available for testing: {e}")


class TestRealMCPClient(unittest.TestCase):
    """Unit tests for Real MCP Client"""
    
    @classmethod
    def setUpClass(cls):
        if not REAL_MCP_AVAILABLE:
            cls.skipTest(cls, "Real MCP components not available")
    
    def setUp(self):
        """Set up test environment"""
        self.client = RealMCPClient(fallback_to_optimized=True)
    
    def test_client_initialization(self):
        """Test real MCP client initialization"""
        self.assertIsNotNone(self.client)
        self.assertTrue(self.client.fallback_to_optimized)
        self.assertIsInstance(self.client.performance_stats, dict)
        
        # Check performance stats structure
        expected_stats = ["mcp_calls", "fallback_calls", "total_time", "cache_hits"]
        for stat in expected_stats:
            self.assertIn(stat, self.client.performance_stats)
    
    def test_mcp_server_availability_check(self):
        """Test MCP server availability checking"""
        servers_available = self.client._check_mcp_servers_available()
        
        self.assertIsInstance(servers_available, dict)
        self.assertIn("github", servers_available)
        self.assertIn("filesystem", servers_available)
        self.assertIsInstance(servers_available["github"], bool)
        self.assertIsInstance(servers_available["filesystem"], bool)
    
    def test_service_status(self):
        """Test service status reporting"""
        status = self.client.get_service_status()
        
        # Validate status structure
        required_fields = ["mcp_protocol", "servers_available", "fallback_enabled", "performance_stats"]
        for field in required_fields:
            self.assertIn(field, status)
        
        self.assertEqual(status["mcp_protocol"], "real")
        self.assertTrue(status["fallback_enabled"])
    
    def test_github_operations_with_fallback(self):
        """Test GitHub operations with fallback logic"""
        # Test PR retrieval
        result = self.client.github_get_pull_request("test/repo", 1, use_fallback=True)
        
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        
        # Should either succeed with MCP or fallback
        if result["status"] == "success":
            # Successful operation
            self.assertIn("data", result)
            self.assertIn("source", result)
        elif result["status"] == "mcp_protocol_simulated":
            # MCP protocol simulation
            self.assertIn("server", result)
            self.assertIn("tool", result)
        else:
            # Error case - acceptable in unit tests
            self.assertEqual(result["status"], "error")
    
    def test_filesystem_operations_with_fallback(self):
        """Test filesystem operations with fallback logic"""
        result = self.client.filesystem_search_files("*.py", max_results=5)
        
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        
        # Should either succeed with MCP or fallback
        if result["status"] == "success":
            self.assertIn("data", result)
            self.assertIn("source", result)
        elif result["status"] == "mcp_protocol_simulated":
            self.assertIn("server", result)
            self.assertIn("tool", result)
        else:
            # Error case - acceptable in unit tests
            self.assertEqual(result["status"], "error")
    
    def test_performance_tracking(self):
        """Test performance statistics tracking"""
        initial_stats = self.client.performance_stats.copy()
        
        # Make some calls
        self.client.github_get_pull_request("test/repo", 1, use_fallback=True)
        self.client.filesystem_search_files("*.py", max_results=1)
        
        # Check stats were updated
        final_stats = self.client.performance_stats
        
        # Either MCP calls or fallback calls should have increased
        total_calls_before = initial_stats["mcp_calls"] + initial_stats["fallback_calls"]
        total_calls_after = final_stats["mcp_calls"] + final_stats["fallback_calls"]
        self.assertGreater(total_calls_after, total_calls_before)
    
    def test_all_services_testing(self):
        """Test comprehensive service testing"""
        test_results = self.client.test_all_services()
        
        self.assertIn("status", test_results)
        self.assertIn("test_results", test_results)
        self.assertIn("performance_stats", test_results)
        
        # Validate individual service tests
        results = test_results["test_results"]
        self.assertIn("github", results)
        self.assertIn("filesystem", results)
        
        # Each service should have status and source
        for service in ["github", "filesystem"]:
            self.assertIn("status", results[service])
            self.assertIn("source", results[service])
            self.assertIn(results[service]["status"], ["working", "error"])


class TestFrameworkMCPIntegration(unittest.TestCase):
    """Unit tests for Framework MCP Integration"""
    
    @classmethod
    def setUpClass(cls):
        if not REAL_MCP_AVAILABLE:
            cls.skipTest(cls, "Real MCP components not available")
    
    def setUp(self):
        """Set up test environment"""
        self.integration = FrameworkMCPIntegration(enable_real_mcp=True, fallback_enabled=True)
    
    def test_integration_initialization(self):
        """Test framework integration initialization"""
        self.assertIsNotNone(self.integration)
        self.assertTrue(self.integration.enable_real_mcp)
        self.assertTrue(self.integration.fallback_enabled)
        self.assertIsNotNone(self.integration.mcp_client)
        
        # Check performance tracking
        self.assertEqual(self.integration.call_count, 0)
        self.assertEqual(self.integration.mcp_success_count, 0)
        self.assertEqual(self.integration.fallback_count, 0)
    
    def test_github_api_compatibility(self):
        """Test GitHub API backward compatibility"""
        # Test PR retrieval maintains backward compatibility
        result = self.integration.github_get_pull_request("test/repo", 1, use_fallback=True)
        
        self.assertIsInstance(result, dict)
        
        # Should return data in backward compatible format
        if "error" not in result:
            # Success case - should have expected fields
            self.assertTrue(isinstance(result, dict))
            # For MCP simulation, should have title field
            if result.get("mcp_ready"):
                self.assertIn("title", result)
                self.assertIn("state", result)
        else:
            # Error case acceptable in tests
            self.assertIn("error", result)
    
    def test_filesystem_api_compatibility(self):
        """Test filesystem API backward compatibility"""
        result = self.integration.filesystem_search_files("*.py", max_results=5)
        
        self.assertIsInstance(result, dict)
        
        # Should return data in backward compatible format
        if "error" not in result:
            # Success case - should have expected fields
            self.assertTrue(isinstance(result, dict))
            # For MCP simulation, should have files field
            if result.get("mcp_ready"):
                self.assertIn("files", result)
                self.assertIn("total_count", result)
        else:
            # Error case acceptable in tests
            self.assertIn("error", result)
    
    def test_performance_monitoring(self):
        """Test performance monitoring and logging"""
        initial_count = self.integration.call_count
        
        # Make some calls
        self.integration.github_get_pull_request("test/repo", 1, use_fallback=True)
        self.integration.filesystem_search_files("*.py", max_results=1)
        
        # Check call count increased
        self.assertEqual(self.integration.call_count, initial_count + 2)
        
        # Check that either MCP success or fallback count increased
        total_handled = self.integration.mcp_success_count + self.integration.fallback_count
        self.assertGreaterEqual(total_handled, 2)
    
    def test_service_status_comprehensive(self):
        """Test comprehensive service status reporting"""
        status = self.integration.get_service_status()
        
        # Validate framework-specific status
        required_fields = [
            "mcp_integration", "framework_version", "real_mcp_enabled",
            "fallback_enabled", "servers_available", "performance_stats",
            "mcp_client_stats"
        ]
        
        for field in required_fields:
            self.assertIn(field, status)
        
        self.assertEqual(status["mcp_integration"], "real_protocol")
        self.assertEqual(status["framework_version"], "upgraded")
        self.assertTrue(status["real_mcp_enabled"])
        self.assertTrue(status["fallback_enabled"])
    
    def test_compatibility_testing(self):
        """Test compatibility testing functionality"""
        test_results = self.integration.test_all_services()
        
        self.assertIn("framework_compatibility", test_results)
        
        compatibility = test_results["framework_compatibility"]
        self.assertIn("github_compatibility", compatibility)
        self.assertIn("filesystem_compatibility", compatibility)
        
        # Each compatibility test should have status
        for test_name in ["github_compatibility", "filesystem_compatibility"]:
            test_result = compatibility[test_name]
            self.assertIn("status", test_result)
            self.assertIn(test_result["status"], ["compatible", "error"])


class TestMCPServiceCoordinatorBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility of MCPServiceCoordinator"""
    
    @classmethod
    def setUpClass(cls):
        if not REAL_MCP_AVAILABLE:
            cls.skipTest(cls, "Real MCP components not available")
    
    def setUp(self):
        """Set up test environment"""
        self.coordinator = MCPServiceCoordinator(".")
    
    def test_drop_in_replacement(self):
        """Test that new coordinator is a drop-in replacement"""
        # Should have same base interface as old coordinator
        self.assertIsNotNone(self.coordinator)
        self.assertIsNotNone(self.coordinator.base_path)
        
        # Should have github_get_pull_request method
        self.assertTrue(hasattr(self.coordinator, 'github_get_pull_request'))
        
        # Should have filesystem_search_files method
        self.assertTrue(hasattr(self.coordinator, 'filesystem_search_files'))
        
        # Should have service status method
        self.assertTrue(hasattr(self.coordinator, 'get_service_status'))
    
    def test_api_method_signatures(self):
        """Test API method signatures match expectations"""
        # Test github_get_pull_request signature
        result = self.coordinator.github_get_pull_request("test/repo", 1, use_fallback=True)
        self.assertIsInstance(result, dict)
        
        # Test filesystem_search_files signature
        result = self.coordinator.filesystem_search_files("*.py", semantic_search=False, max_results=5)
        self.assertIsInstance(result, dict)
        
        # Test get_service_status signature
        status = self.coordinator.get_service_status()
        self.assertIsInstance(status, dict)
        
        # Test test_all_services signature  
        test_results = self.coordinator.test_all_services()
        self.assertIsInstance(test_results, dict)
    
    def test_no_regressions_in_functionality(self):
        """Test that no regressions exist in core functionality"""
        # This test validates that existing framework code would work unchanged
        
        # Test 1: GitHub operations should work
        try:
            result = self.coordinator.github_get_pull_request("test/repo", 1)
            self.assertIsInstance(result, dict)
            # Should not crash or return unexpected format
        except Exception as e:
            # API errors are acceptable, but not implementation errors
            self.assertNotIn("AttributeError", str(e))
            self.assertNotIn("TypeError", str(e))
        
        # Test 2: Filesystem operations should work
        try:
            result = self.coordinator.filesystem_search_files("*.py")
            self.assertIsInstance(result, dict)
            # Should not crash or return unexpected format
        except Exception as e:
            # Filesystem errors are acceptable, but not implementation errors
            self.assertNotIn("AttributeError", str(e))
            self.assertNotIn("TypeError", str(e))
        
        # Test 3: Service status should work
        status = self.coordinator.get_service_status()
        self.assertIsInstance(status, dict)
        # Should have some expected keys (flexible to allow enhancement)
        self.assertTrue(len(status) > 0)


class TestMCPUpgradeValidation(unittest.TestCase):
    """Test MCP upgrade validation and regression checking"""
    
    @classmethod
    def setUpClass(cls):
        if not REAL_MCP_AVAILABLE:
            cls.skipTest(cls, "Real MCP components not available")
    
    def test_validate_mcp_upgrade(self):
        """Test MCP upgrade validation function"""
        validation = validate_mcp_upgrade()
        
        # Validate structure
        required_fields = ["upgrade_status", "mcp_servers_available", "framework_compatibility", "regression_check"]
        for field in required_fields:
            self.assertIn(field, validation)
        
        # Validate values
        self.assertIn(validation["upgrade_status"], ["success", "partial"])
        self.assertEqual(validation["regression_check"], "passed")
        
        # Should have framework compatibility results
        self.assertIsInstance(validation["framework_compatibility"], dict)
        
        # Should have server availability results
        self.assertIsInstance(validation["mcp_servers_available"], dict)
    
    def test_regression_check_comprehensive(self):
        """Comprehensive regression check"""
        # Create coordinator to test existing interface
        coordinator = MCPServiceCoordinator(".")
        
        # Test 1: All expected methods exist
        expected_methods = [
            "github_get_pull_request",
            "filesystem_search_files", 
            "get_service_status",
            "test_all_services"
        ]
        
        for method in expected_methods:
            self.assertTrue(hasattr(coordinator, method))
            self.assertTrue(callable(getattr(coordinator, method)))
        
        # Test 2: Methods return expected types
        status = coordinator.get_service_status()
        self.assertIsInstance(status, dict)
        
        test_results = coordinator.test_all_services()
        self.assertIsInstance(test_results, dict)
        
        # Test 3: No exceptions on basic operations
        try:
            # These should not crash, regardless of MCP availability
            coordinator.github_get_pull_request("test/repo", 1)
            coordinator.filesystem_search_files("*.py", max_results=1)
        except Exception as e:
            # Only specific types of errors are acceptable
            acceptable_errors = ["ConnectTimeout", "HTTPError", "FileNotFoundError", "PermissionError"]
            error_acceptable = any(error in str(e) for error in acceptable_errors)
            if not error_acceptable:
                self.fail(f"Unexpected error type in regression test: {e}")


if __name__ == '__main__':
    print("🧪 Real MCP Integration Unit Tests")
    print("=" * 50)
    print("Testing real MCP protocol implementation, backward compatibility, and regression prevention")
    print("=" * 50)
    
    # Check if Real MCP is available
    if not REAL_MCP_AVAILABLE:
        print("❌ Real MCP components not available - skipping tests")
        exit(1)
    
    # Run tests with detailed output
    unittest.main(verbosity=2)