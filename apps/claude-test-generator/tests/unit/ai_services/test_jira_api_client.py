#!/usr/bin/env python3
"""
Unit Tests for JIRA API Client
Tests JIRA integration with mocking to avoid external dependencies
"""

import unittest
import os
import sys
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Systematic Import Path Management for AI Services
def setup_ai_services_path():
    """Add AI services directory to Python path if not already present"""
    import sys
    import os
    
    # Get the AI services path relative to the test file
    ai_services_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services'))
    
    if ai_services_path not in sys.path:
        sys.path.insert(0, ai_services_path)
    
    return ai_services_path

# Setup import path and import modules
setup_ai_services_path()

try:
    from jira_api_client import (
        JiraApiClient, JiraApiError, JiraAuthenticationError, 
        JiraConnectionError, JiraApiConfig, JiraTicketData
    )
except ImportError as e:
    print(f"Failed to import JIRA API client: {e}")
    print(f"AI Services path: {setup_ai_services_path()}")
    sys.exit(1)


class TestJiraApiConfig(unittest.TestCase):
    """Test JIRA API configuration handling"""
    
    def test_config_creation(self):
        """Test creating JIRA API configuration"""
        config = JiraApiConfig(
            base_url="https://issues.redhat.com",
            username="test@redhat.com",
            api_token="test_token",
            verify_ssl=True,
            timeout=30
        )
        
        self.assertEqual(config.base_url, "https://issues.redhat.com")
        self.assertEqual(config.username, "test@redhat.com")
        self.assertEqual(config.api_token, "test_token")
        self.assertTrue(config.verify_ssl)
        self.assertEqual(config.timeout, 30)
    
    def test_config_defaults(self):
        """Test JIRA API configuration defaults"""
        config = JiraApiConfig(
            base_url="https://issues.redhat.com",
            username="test@redhat.com",
            api_token="test_token"
        )
        
        # Should have default values
        self.assertTrue(config.verify_ssl)
        self.assertEqual(config.timeout, 30)
        self.assertEqual(config.cache_duration, 300)


class TestJiraTicketData(unittest.TestCase):
    """Test JIRA ticket data structure"""
    
    def test_ticket_data_creation(self):
        """Test creating JIRA ticket data"""
        ticket = JiraTicketData(
            id="ACM-12345",
            title="Test Issue",
            status="Open",
            fix_version="2.15.0",
            priority="High",
            component="TestComponent",
            description="Test description"
        )
        
        self.assertEqual(ticket.id, "ACM-12345")
        self.assertEqual(ticket.title, "Test Issue")
        self.assertEqual(ticket.status, "Open")
        self.assertEqual(ticket.fix_version, "2.15.0")
        self.assertEqual(ticket.priority, "High")
        self.assertEqual(ticket.component, "TestComponent")
        self.assertEqual(ticket.description, "Test description")
    
    def test_ticket_data_defaults(self):
        """Test JIRA ticket data defaults"""
        ticket = JiraTicketData(
            id="ACM-12345",
            title="Test Issue",
            status="Open",
            fix_version="2.15.0",
            priority="High",
            component="TestComponent",
            description="Test description"
        )
        
        # Should have default empty lists/dicts
        self.assertEqual(ticket.labels, [])
        self.assertEqual(ticket.custom_fields, {})
        self.assertEqual(ticket.raw_data, {})


class TestJiraApiClient(unittest.TestCase):
    """Test JIRA API client functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test config
        self.temp_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.temp_dir) / ".claude" / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Patch environment variables
        self.env_patcher = patch.dict(os.environ, {
            'JIRA_BASE_URL': 'https://test.jira.com',
            'JIRA_USERNAME': 'test@example.com',
            'JIRA_API_TOKEN': 'test_token'
        })
        self.env_patcher.start()
    
    def tearDown(self):
        """Clean up test environment"""
        self.env_patcher.stop()
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_client_initialization_from_env(self):
        """Test client initialization from environment variables"""
        client = JiraApiClient()
        
        self.assertEqual(client.config.base_url, "https://test.jira.com")
        self.assertEqual(client.config.username, "test@example.com")
        self.assertEqual(client.config.api_token, "test_token")
    
    def test_connection_test_success(self):
        """Test successful connection test"""
        client = JiraApiClient()
        
        # Mock the test_connection method to return success
        with patch.object(client, 'session') as mock_session:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"displayName": "Test User"}
            mock_response.raise_for_status.return_value = None
            mock_session.get.return_value = mock_response
            
            connected, message = client.test_connection()
            
            self.assertTrue(connected)
            self.assertIn("Connected as Test User", message)
    
    def test_connection_test_failure(self):
        """Test failed connection test"""
        client = JiraApiClient()
        
        # Mock the test_connection method to return failure
        with patch.object(client, 'session') as mock_session:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.text = "Unauthorized"
            mock_session.get.return_value = mock_response
            
            connected, message = client.test_connection()
            
            self.assertFalse(connected)
            self.assertIn("Not authenticated", message)
    
    def test_get_ticket_information_success(self):
        """Test successful ticket information retrieval"""
        client = JiraApiClient()
        
        # Mock the session to return proper ticket data
        with patch.object(client, 'session') as mock_session:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {
                "key": "ACM-12345",
                "fields": {
                    "summary": "Test Issue",
                    "status": {"name": "Open"},
                    "fixVersions": [{"name": "2.15.0"}],
                    "priority": {"name": "High"},
                    "components": [{"name": "TestComponent"}],
                    "description": "Test description",
                    "assignee": {"displayName": "Test Assignee"},
                    "reporter": {"displayName": "Test Reporter"},
                    "created": "2024-01-01T00:00:00.000+0000",
                    "updated": "2024-01-02T00:00:00.000+0000",
                    "labels": ["test", "unit-test"]
                }
            }
            mock_session.get.return_value = mock_response
            
            ticket_data = client.get_ticket_information("ACM-12345")
            
            self.assertIsInstance(ticket_data, JiraTicketData)
            self.assertEqual(ticket_data.id, "ACM-12345")
            self.assertEqual(ticket_data.title, "Test Issue")
            self.assertEqual(ticket_data.status, "Open")
            self.assertEqual(ticket_data.fix_version, "2.15.0")
            self.assertEqual(ticket_data.priority, "High")
            self.assertEqual(ticket_data.component, "TestComponent")
            self.assertEqual(ticket_data.description, "Test description")
            self.assertEqual(ticket_data.assignee, "Test Assignee")
            self.assertEqual(ticket_data.reporter, "Test Reporter")
            self.assertEqual(ticket_data.labels, ["test", "unit-test"])
    
    def test_get_ticket_information_not_found(self):
        """Test ticket not found error"""
        client = JiraApiClient()
        
        # Mock the session to return 404
        with patch.object(client, 'session') as mock_session:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.text = "Not Found"
            mock_session.get.return_value = mock_response
            
            with self.assertRaises(JiraApiError) as context:
                client.get_ticket_information("ACM-99999")
            
            # Check for either the direct error or the retry failure message
            error_msg = str(context.exception)
            self.assertTrue(
                "JIRA ticket ACM-99999 not found" in error_msg or
                "Failed to fetch ACM-99999 after" in error_msg,
                f"Expected error message not found: {error_msg}"
            )
    
    def test_fallback_simulation(self):
        """Test fallback to simulation when API fails"""
        # Initialize client without API credentials
        with patch.dict(os.environ, {}, clear=True):
            client = JiraApiClient()
            
            # Should use simulation for known tickets
            ticket_data = client.get_ticket_information("ACM-22079")
            
            self.assertIsInstance(ticket_data, JiraTicketData)
            self.assertEqual(ticket_data.id, "ACM-22079")
            self.assertIn("ClusterCurator", ticket_data.title)
            self.assertEqual(ticket_data.fix_version, "2.15.0")
    
    def test_cache_functionality(self):
        """Test ticket caching functionality"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create cache directory
            cache_dir = Path(temp_dir) / ".claude" / "cache" / "jira"
            cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Mock the cache directory
            with patch.object(JiraApiClient, '_get_cache_dir', return_value=cache_dir):
                client = JiraApiClient()
                
                # Create test cache file
                cache_file = cache_dir / "ACM-12345.json"
                # Use current timestamp for valid cache
                from datetime import datetime
                current_time = datetime.now().isoformat()
                
                cache_data = {
                    "ticket_data": {
                        "id": "ACM-12345",
                        "title": "Cached Test Issue",
                        "status": "Open",
                        "fix_version": "2.15.0",
                        "priority": "High",
                        "component": "TestComponent",
                        "description": "Cached description",
                        "assignee": "Cached Assignee",
                        "reporter": "Cached Reporter",
                        "created": "2024-01-01T00:00:00",
                        "updated": "2024-01-01T12:00:00",
                        "labels": ["cached", "test"],
                        "custom_fields": {"test_field": "test_value"}
                        # Note: raw_data not cached to avoid size issues
                    },
                    "cache_timestamp": current_time
                }
                
                with open(cache_file, 'w') as f:
                    json.dump(cache_data, f)
                
                # Should load from cache
                ticket_data = client.get_ticket_information("ACM-12345")
                
                self.assertEqual(ticket_data.title, "Cached Test Issue")
    
    def test_invalid_jira_id(self):
        """Test handling of invalid JIRA IDs"""
        client = JiraApiClient()
        
        with self.assertRaises(ValueError) as context:
            client.get_ticket_information("")
        
        self.assertIn("Invalid JIRA ID", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            client.get_ticket_information(None)
        
        self.assertIn("Invalid JIRA ID", str(context.exception))


class TestJiraApiClientConfiguration(unittest.TestCase):
    """Test JIRA API client configuration loading"""
    
    def test_config_file_loading(self):
        """Test loading configuration from file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / ".claude" / "config"
            config_dir.mkdir(parents=True, exist_ok=True)
            
            config_file = config_dir / "jira_config.json"
            config_data = {
                "base_url": "https://config.jira.com",
                "username": "config@example.com",
                "api_token": "config_token",
                "verify_ssl": False,
                "timeout": 60
            }
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            # Mock the config directory
            with patch.object(JiraApiClient, '_get_config_dir', return_value=config_dir):
                with patch.dict(os.environ, {}, clear=True):  # Clear env vars
                    client = JiraApiClient()
                    
                    self.assertEqual(client.config.base_url, "https://config.jira.com")
                    self.assertEqual(client.config.username, "config@example.com")
                    self.assertEqual(client.config.api_token, "config_token")
                    self.assertFalse(client.config.verify_ssl)
                    self.assertEqual(client.config.timeout, 60)
    
    def test_environment_variable_priority(self):
        """Test that environment variables take priority over config file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / ".claude" / "config"
            config_dir.mkdir(parents=True, exist_ok=True)
            
            config_file = config_dir / "jira_config.json"
            config_data = {
                "base_url": "https://config.jira.com",
                "username": "config@example.com",
                "api_token": "config_token"
            }
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            # Mock the config directory and set env vars
            with patch.object(JiraApiClient, '_get_config_dir', return_value=config_dir):
                with patch.dict(os.environ, {
                    'JIRA_BASE_URL': 'https://env.jira.com',
                    'JIRA_USERNAME': 'env@example.com',
                    'JIRA_API_TOKEN': 'env_token'
                }):
                    client = JiraApiClient()
                    
                    # Environment variables should take priority
                    self.assertEqual(client.config.base_url, "https://env.jira.com")
                    self.assertEqual(client.config.username, "env@example.com")
                    self.assertEqual(client.config.api_token, "env_token")


if __name__ == '__main__':
    unittest.main()