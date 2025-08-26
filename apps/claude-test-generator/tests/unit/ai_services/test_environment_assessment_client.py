#!/usr/bin/env python3
"""
Unit Tests for Environment Assessment Client
Tests environment assessment with mocking to avoid external dependencies
"""

import unittest
import os
import sys
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import subprocess

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
    from environment_assessment_client import (
        EnvironmentAssessmentClient, EnvironmentAssessmentError,
        ClusterConnectionError, PlatformDetectionError,
        EnvironmentAssessmentConfig, EnvironmentData
    )
except ImportError as e:
    print(f"Failed to import Environment Assessment client: {e}")
    print(f"AI Services path: {setup_ai_services_path()}")
    sys.exit(1)


class TestEnvironmentAssessmentConfig(unittest.TestCase):
    """Test Environment Assessment configuration"""
    
    def test_config_creation(self):
        """Test creating environment assessment configuration"""
        config = EnvironmentAssessmentConfig(
            cluster_timeout=60,
            health_check_timeout=30,
            max_retries=5,
            cache_duration=600,
            fallback_to_simulation=False
        )
        
        self.assertEqual(config.cluster_timeout, 60)
        self.assertEqual(config.health_check_timeout, 30)
        self.assertEqual(config.max_retries, 5)
        self.assertEqual(config.cache_duration, 600)
        self.assertFalse(config.fallback_to_simulation)
    
    def test_config_defaults(self):
        """Test environment assessment configuration defaults"""
        config = EnvironmentAssessmentConfig()
        
        self.assertEqual(config.cluster_timeout, 30)
        self.assertEqual(config.health_check_timeout, 15)
        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.cache_duration, 180)
        self.assertTrue(config.fallback_to_simulation)
        self.assertEqual(config.preferred_tools, ['oc', 'kubectl'])


class TestEnvironmentData(unittest.TestCase):
    """Test Environment Data structure"""
    
    def test_environment_data_creation(self):
        """Test creating environment data"""
        env_data = EnvironmentData(
            cluster_name="test-cluster",
            version="2.15.0",
            api_url="https://api.test-cluster.com:6443",
            console_url="https://console.test-cluster.com",
            platform="openshift",
            region="us-east-1",
            health_status="healthy",
            connectivity_confirmed=True,
            platform_details={"platform": "openshift"},
            detection_method="oc_assessment",
            assessment_timestamp="2024-01-01T00:00:00",
            tools_available={"oc": True, "kubectl": False}
        )
        
        self.assertEqual(env_data.cluster_name, "test-cluster")
        self.assertEqual(env_data.version, "2.15.0")
        self.assertEqual(env_data.platform, "openshift")
        self.assertTrue(env_data.connectivity_confirmed)
        self.assertEqual(env_data.raw_data, {})  # Should initialize empty


class TestEnvironmentAssessmentClient(unittest.TestCase):
    """Test Environment Assessment Client functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir) / ".claude" / "cache" / "environment"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test config
        self.config = EnvironmentAssessmentConfig(
            cluster_timeout=10,
            health_check_timeout=5,
            max_retries=2,
            fallback_to_simulation=True
        )
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @patch('environment_assessment_client.subprocess.run')
    def test_tool_detection_success(self, mock_subprocess):
        """Test successful tool detection"""
        # Mock successful tool detection
        mock_result = Mock()
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result
        
        # Mock cache_dir by patching the initialization
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            
            # Should detect tools as available
            self.assertTrue(client.available_tools.get('oc', False))
            self.assertTrue(client.available_tools.get('kubectl', False))
            self.assertEqual(client.primary_tool, 'oc')  # First available tool
    
    @patch('environment_assessment_client.subprocess.run')
    def test_tool_detection_failure(self, mock_subprocess):
        """Test tool detection when tools are not available"""
        # Mock failed tool detection
        mock_subprocess.side_effect = FileNotFoundError("Command not found")
        
        # Mock cache_dir by patching the initialization
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            
            # Should detect tools as unavailable
            self.assertFalse(client.available_tools.get('oc', False))
            self.assertFalse(client.available_tools.get('kubectl', False))
            self.assertIsNone(client.primary_tool)
    
    @patch('environment_assessment_client.subprocess.run')
    def test_cluster_info_success(self, mock_subprocess):
        """Test successful cluster info retrieval"""
        # Mock cluster info command success
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = """
        Kubernetes control plane is running at https://api.test-cluster.com:6443
        CoreDNS is running at https://api.test-cluster.com:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
        """
        mock_subprocess.return_value = mock_result
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            client.primary_tool = 'kubectl'  # Set primary tool
            
            cluster_info = client._get_cluster_info()
            
            self.assertIn('kubernetes_master', cluster_info)
            self.assertEqual(cluster_info['kubernetes_master'], 'https://api.test-cluster.com:6443')
    
    @patch('environment_assessment_client.subprocess.run')
    def test_cluster_info_failure(self, mock_subprocess):
        """Test cluster info retrieval failure"""
        # Mock cluster info command failure
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Connection refused"
        mock_subprocess.return_value = mock_result
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            client.primary_tool = 'kubectl'  # Set primary tool
            
            with self.assertRaises(ClusterConnectionError) as context:
                client._get_cluster_info()
            
            self.assertIn("Cluster info command failed", str(context.exception))
    
    @patch('environment_assessment_client.subprocess.run')
    def test_version_info_json_success(self, mock_subprocess):
        """Test successful version info retrieval with JSON"""
        # Mock version command with JSON output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            "clientVersion": {"gitVersion": "v1.28.0"},
            "serverVersion": {"gitVersion": "v1.28.0"},
            "openshiftVersion": "4.15.0"
        })
        mock_subprocess.return_value = mock_result
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            client.primary_tool = 'oc'  # Set primary tool
            
            version_info = client._get_version_info()
            
            self.assertEqual(version_info['client_version'], 'v1.28.0')
            self.assertEqual(version_info['server_version'], 'v1.28.0')
            self.assertEqual(version_info['openshift_version'], '4.15.0')
            self.assertEqual(version_info['version'], '4.15.0')  # OpenShift version takes priority
    
    @patch('environment_assessment_client.subprocess.run')
    def test_version_info_text_fallback(self, mock_subprocess):
        """Test version info with text parsing fallback"""
        # Mock version command with text output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = """
        Client Version: v1.28.0
        Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
        Server Version: v1.28.0
        """
        mock_subprocess.return_value = mock_result
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            client.primary_tool = 'kubectl'  # Set primary tool
            
            version_info = client._get_version_info()
            
            self.assertEqual(version_info['client_version'], 'v1.28.0')
            self.assertEqual(version_info['server_version'], 'v1.28.0')
            self.assertEqual(version_info['version'], 'v1.28.0')
    
    @patch('environment_assessment_client.subprocess.run')
    def test_health_status_healthy(self, mock_subprocess):
        """Test health status detection - healthy cluster"""
        # Mock nodes command with healthy nodes
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = """
        node1   Ready    control-plane   1d   v1.28.0
        node2   Ready    worker          1d   v1.28.0
        node3   Ready    worker          1d   v1.28.0
        """
        mock_subprocess.return_value = mock_result
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            client.primary_tool = 'kubectl'  # Set primary tool
            
            health_status = client._get_health_status()
            
            self.assertEqual(health_status, 'healthy')
    
    @patch('environment_assessment_client.subprocess.run')
    def test_health_status_degraded(self, mock_subprocess):
        """Test health status detection - degraded cluster"""
        # Mock nodes command with some unhealthy nodes
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = """
        node1   Ready      control-plane   1d   v1.28.0
        node2   NotReady   worker          1d   v1.28.0
        node3   Ready      worker          1d   v1.28.0
        """
        mock_subprocess.return_value = mock_result
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            client.primary_tool = 'kubectl'  # Set primary tool
            
            health_status = client._get_health_status()
            
            self.assertEqual(health_status, 'degraded')
    
    @patch('environment_assessment_client.subprocess.run')
    def test_platform_detection_openshift(self, mock_subprocess):
        """Test OpenShift platform detection"""
        # Mock namespace command showing OpenShift namespaces
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = """
        default                   Active   1d
        kube-system              Active   1d
        openshift-apiserver      Active   1d
        openshift-authentication Active   1d
        """
        mock_subprocess.return_value = mock_result
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            client.primary_tool = 'oc'  # Set primary tool
            
            platform_info = client._detect_platform()
            
            self.assertEqual(platform_info['platform'], 'openshift')
            self.assertEqual(platform_info['distribution'], 'openshift')
            self.assertIn('oc_cli', platform_info['features'])
            self.assertIn('openshift_namespaces', platform_info['features'])
    
    @patch('environment_assessment_client.subprocess.run')
    def test_platform_detection_kubernetes(self, mock_subprocess):
        """Test Kubernetes platform detection"""
        # Mock namespace command showing only Kubernetes namespaces
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = """
        default       Active   1d
        kube-system   Active   1d
        kube-public   Active   1d
        """
        mock_subprocess.return_value = mock_result
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            client.primary_tool = 'kubectl'  # Set primary tool
            
            platform_info = client._detect_platform()
            
            self.assertEqual(platform_info['platform'], 'kubernetes')
            self.assertIn('kubernetes_system', platform_info['features'])
    
    def test_fallback_simulation(self):
        """Test fallback to simulation when tools are unavailable"""
        config = EnvironmentAssessmentConfig(fallback_to_simulation=True)
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            with patch.object(EnvironmentAssessmentClient, '_detect_available_tools', return_value={}):
                with patch.object(EnvironmentAssessmentClient, '_select_primary_tool', return_value=None):
                    client = EnvironmentAssessmentClient(config)
                    
                    # Should fall back to simulation
                    env_data = client.assess_environment("test-cluster")
                    
                    self.assertIsInstance(env_data, EnvironmentData)
                    self.assertEqual(env_data.cluster_name, "test-cluster")
                    self.assertEqual(env_data.detection_method, "intelligent_simulation")
    
    def test_cache_functionality(self):
        """Test environment assessment caching"""
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            client = EnvironmentAssessmentClient(self.config)
            
            # Create test cache file
            cache_file = self.cache_dir / "test-cluster.json"
            cache_data = {
                "cache_timestamp": "2024-01-01T00:00:00",
                "environment_data": {
                    "cluster_name": "test-cluster",
                    "version": "2.15.0",
                    "api_url": "https://api.test-cluster.com:6443",
                    "console_url": "https://console.test-cluster.com",
                    "platform": "openshift",
                    "region": "us-east-1",
                    "health_status": "healthy",
                    "connectivity_confirmed": True,
                    "platform_details": {"platform": "openshift"},
                    "detection_method": "cached",
                    "assessment_timestamp": "2024-01-01T00:00:00",
                    "tools_available": {"oc": True}
                }
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
            
            # Should load from cache if within cache duration
            with patch('environment_assessment_client.datetime') as mock_datetime:
                from datetime import datetime
                mock_now = datetime.fromisoformat("2024-01-01T00:02:00")  # 2 minutes later
                mock_datetime.now.return_value = mock_now
                mock_datetime.fromisoformat = datetime.fromisoformat
                
                cached_env_data = client._get_cached_assessment("test-cluster")
                
                self.assertIsInstance(cached_env_data, EnvironmentData)
                self.assertEqual(cached_env_data.cluster_name, "test-cluster")
    
    def test_connectivity_test_success(self):
        """Test successful connectivity test"""
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            with patch('environment_assessment_client.subprocess.run') as mock_subprocess:
                # Mock successful connectivity test
                mock_result = Mock()
                mock_result.returncode = 0
                mock_subprocess.return_value = mock_result
                
                client = EnvironmentAssessmentClient(self.config)
                client.primary_tool = 'kubectl'  # Set primary tool
                
                connected, message = client.test_connectivity()
                
                self.assertTrue(connected)
                self.assertIn("Cluster connectivity confirmed", message)
    
    def test_connectivity_test_failure(self):
        """Test failed connectivity test"""
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            with patch('environment_assessment_client.subprocess.run') as mock_subprocess:
                # Mock failed connectivity test
                mock_result = Mock()
                mock_result.returncode = 1
                mock_result.stderr = "Connection refused"
                mock_subprocess.return_value = mock_result
                
                client = EnvironmentAssessmentClient(self.config)
                client.primary_tool = 'kubectl'  # Set primary tool
                
                connected, message = client.test_connectivity()
                
                self.assertFalse(connected)
                self.assertIn("Cluster connection failed", message)
    
    def test_no_tools_available(self):
        """Test behavior when no tools are available"""
        config = EnvironmentAssessmentConfig(fallback_to_simulation=False)
        
        # Mock cache_dir and create client properly
        with patch('environment_assessment_client.Path') as mock_path:
            mock_path.return_value = self.cache_dir
            with patch.object(EnvironmentAssessmentClient, '_detect_available_tools', return_value={}):
                with patch.object(EnvironmentAssessmentClient, '_select_primary_tool', return_value=None):
                    client = EnvironmentAssessmentClient(config)
                    
                    # Should raise error when no tools and simulation disabled
                    with self.assertRaises(EnvironmentAssessmentError) as context:
                        client.assess_environment("test-cluster")
                    
                    self.assertIn("tools unavailable and simulation disabled", str(context.exception))


if __name__ == '__main__':
    unittest.main()