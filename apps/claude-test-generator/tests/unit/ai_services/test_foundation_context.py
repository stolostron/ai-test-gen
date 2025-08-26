#!/usr/bin/env python3
"""
Unit Tests for Foundation Context
Tests foundation context data structures and validation
"""

import unittest
import os
import sys
import json
import tempfile
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime

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
    from foundation_context import (
        FoundationContext, FoundationContextBuilder, ContextMetadata,
        JiraTicketInfo, VersionContext, EnvironmentBaseline,
        ContextValidationLevel, create_foundation_context
    )
except ImportError as e:
    print(f"Failed to import Foundation Context: {e}")
    print(f"AI Services path: {setup_ai_services_path()}")
    sys.exit(1)


class TestContextMetadata(unittest.TestCase):
    """Test Context Metadata structure"""
    
    def test_context_metadata_creation(self):
        """Test creating context metadata"""
        metadata = ContextMetadata(
            context_version="1.0.0",
            creation_timestamp="2024-01-01T00:00:00",
            last_updated="2024-01-01T00:00:00",
            consistency_score=0.95,
            validation_level=ContextValidationLevel.STANDARD
        )
        
        self.assertEqual(metadata.creation_timestamp, "2024-01-01T00:00:00")
        self.assertEqual(metadata.context_version, "1.0.0")
        self.assertEqual(metadata.last_updated, "2024-01-01T00:00:00")
        self.assertEqual(metadata.consistency_score, 0.95)
        self.assertEqual(metadata.validation_level, ContextValidationLevel.STANDARD)
    
    def test_context_metadata_defaults(self):
        """Test context metadata defaults"""
        metadata = ContextMetadata()
        
        # Should have generated timestamp and default values
        self.assertIsNotNone(metadata.creation_timestamp)
        self.assertEqual(metadata.context_version, "1.0.0")
        self.assertEqual(metadata.consistency_score, 1.0)
        self.assertEqual(metadata.validation_level, ContextValidationLevel.STANDARD)


class TestJiraTicketInfo(unittest.TestCase):
    """Test JIRA Ticket Info structure"""
    
    def test_jira_ticket_info_creation(self):
        """Test creating JIRA ticket info"""
        jira_info = JiraTicketInfo(
            jira_id="ACM-12345",
            title="Test Issue",
            status="Open",
            fix_version="2.15.0",
            priority="High",
            component="TestComponent",
            detection_timestamp="2024-01-01T00:00:00",
            confidence=0.9
        )
        
        self.assertEqual(jira_info.jira_id, "ACM-12345")
        self.assertEqual(jira_info.title, "Test Issue")
        self.assertEqual(jira_info.status, "Open")
        self.assertEqual(jira_info.fix_version, "2.15.0")
        self.assertEqual(jira_info.priority, "High")
        self.assertEqual(jira_info.component, "TestComponent")
        self.assertEqual(jira_info.detection_timestamp, "2024-01-01T00:00:00")
        self.assertEqual(jira_info.confidence, 0.9)


class TestVersionContext(unittest.TestCase):
    """Test Version Context structure"""
    
    def test_version_context_creation(self):
        """Test creating version context"""
        version_context = VersionContext(
            target_version="2.15.0",
            environment_version="2.14.0",
            comparison_result="newer",
            detection_method="api_detection",
            confidence=0.95,
            version_gap_details={"gap_type": "minor_upgrade"}
        )
        
        self.assertEqual(version_context.target_version, "2.15.0")
        self.assertEqual(version_context.environment_version, "2.14.0")
        self.assertEqual(version_context.comparison_result, "newer")
        self.assertEqual(version_context.detection_method, "api_detection")
        self.assertEqual(version_context.confidence, 0.95)
        self.assertEqual(version_context.version_gap_details, {"gap_type": "minor_upgrade"})


class TestEnvironmentBaseline(unittest.TestCase):
    """Test Environment Baseline structure"""
    
    def test_environment_baseline_creation(self):
        """Test creating environment baseline"""
        env_baseline = EnvironmentBaseline(
            cluster_name="test-cluster",
            api_url="https://api.test-cluster.com:6443",
            console_url="https://console.test-cluster.com",
            platform="openshift",
            region="us-east-1",
            health_status="healthy",
            connectivity_confirmed=True,
            assessment_timestamp="2024-01-01T00:00:00",
            confidence=0.9
        )
        
        self.assertEqual(env_baseline.cluster_name, "test-cluster")
        self.assertEqual(env_baseline.api_url, "https://api.test-cluster.com:6443")
        self.assertEqual(env_baseline.console_url, "https://console.test-cluster.com")
        self.assertEqual(env_baseline.platform, "openshift")
        self.assertEqual(env_baseline.region, "us-east-1")
        self.assertEqual(env_baseline.health_status, "healthy")
        self.assertTrue(env_baseline.connectivity_confirmed)
        self.assertEqual(env_baseline.assessment_timestamp, "2024-01-01T00:00:00")
        self.assertEqual(env_baseline.confidence, 0.9)


class TestFoundationContext(unittest.TestCase):
    """Test Foundation Context main structure"""
    
    def setUp(self):
        """Set up test data"""
        self.metadata = ContextMetadata(
            context_version="1.0.0",
            creation_timestamp="2024-01-01T00:00:00",
            last_updated="2024-01-01T00:00:00",
            consistency_score=0.95,
            validation_level=ContextValidationLevel.STANDARD
        )
        
        self.jira_info = JiraTicketInfo(
            jira_id="ACM-12345",
            title="Test Issue",
            status="Open",
            fix_version="2.15.0",
            priority="High",
            component="TestComponent",
            detection_timestamp="2024-01-01T00:00:00",
            confidence=0.9
        )
        
        self.version_context = VersionContext(
            target_version="2.15.0",
            environment_version="2.14.0",
            comparison_result="newer",
            detection_method="api_detection",
            confidence=0.95,
            version_gap_details={"gap_type": "minor_upgrade"}
        )
        
        self.environment_baseline = EnvironmentBaseline(
            cluster_name="test-cluster",
            api_url="https://api.test-cluster.com:6443",
            console_url="https://console.test-cluster.com",
            platform="openshift",
            region="us-east-1",
            health_status="healthy",
            connectivity_confirmed=True,
            assessment_timestamp="2024-01-01T00:00:00",
            confidence=0.9
        )
    
    def test_foundation_context_creation(self):
        """Test creating foundation context"""
        context = FoundationContext(
            metadata=self.metadata,
            jira_info=self.jira_info,
            version_context=self.version_context,
            environment_baseline=self.environment_baseline,
            deployment_instruction="Upgrade from 2.14.0 to 2.15.0"
        )
        
        self.assertEqual(context.metadata.context_version, "1.0.0")
        self.assertEqual(context.jira_info.jira_id, "ACM-12345")
        self.assertEqual(context.version_context.target_version, "2.15.0")
        self.assertEqual(context.environment_baseline.cluster_name, "test-cluster")
        self.assertEqual(context.deployment_instruction, "Upgrade from 2.14.0 to 2.15.0")
        self.assertFalse(context.agent_inheritance_ready)  # Default should be False
    
    def test_foundation_context_validation(self):
        """Test foundation context validation"""
        context = FoundationContext(
            metadata=self.metadata,
            jira_info=self.jira_info,
            version_context=self.version_context,
            environment_baseline=self.environment_baseline,
            deployment_instruction="Upgrade from 2.14.0 to 2.15.0"
        )
        
        # Test validation
        validation_results = context.validate_completeness()
        
        # Check that all required fields are validated (using real API validation keys)
        expected_checks = [
            'jira_id_present', 'target_version_present', 'environment_version_present',
            'version_gap_analyzed', 'environment_assessed', 'deployment_instruction_generated',
            'connectivity_confirmed', 'metadata_complete'
        ]
        
        for check in expected_checks:
            self.assertIn(check, validation_results)
            self.assertTrue(validation_results[check])
    
    def test_foundation_context_serialization(self):
        """Test foundation context serialization to dictionary"""
        context = FoundationContext(
            metadata=self.metadata,
            jira_info=self.jira_info,
            version_context=self.version_context,
            environment_baseline=self.environment_baseline,
            deployment_instruction="Upgrade from 2.14.0 to 2.15.0"
        )
        
        # Test to_dict method
        context_dict = context.to_dict()
        
        self.assertIsInstance(context_dict, dict)
        self.assertIn('metadata', context_dict)
        self.assertIn('jira_info', context_dict)
        self.assertIn('version_context', context_dict)
        self.assertIn('environment_baseline', context_dict)
        self.assertIn('deployment_instruction', context_dict)
        
        # Check nested structures
        self.assertEqual(context_dict['jira_info']['jira_id'], "ACM-12345")
        self.assertEqual(context_dict['version_context']['target_version'], "2.15.0")
    
    def test_foundation_context_deserialization(self):
        """Test foundation context deserialization from dictionary"""
        context_dict = {
            'metadata': {
                'context_version': '1.0.0',
                'creation_timestamp': '2024-01-01T00:00:00',
                'last_updated': '2024-01-01T00:00:00',
                'consistency_score': 0.95,
                'validation_level': 'standard'
            },
            'jira_info': {
                'jira_id': 'ACM-12345',
                'title': 'Test Issue',
                'status': 'Open',
                'fix_version': '2.15.0',
                'priority': 'High',
                'component': 'TestComponent',
                'detection_timestamp': '2024-01-01T00:00:00',
                'confidence': 0.9
            },
            'version_context': {
                'target_version': '2.15.0',
                'environment_version': '2.14.0',
                'comparison_result': 'newer',
                'detection_method': 'api_detection',
                'confidence': 0.9,
                'version_gap_details': {'gap_type': 'minor_upgrade'}
            },
            'environment_baseline': {
                'cluster_name': 'test-cluster',
                'api_url': 'https://api.test-cluster.com:6443',
                'console_url': 'https://console.test-cluster.com',
                'platform': 'openshift',
                'region': 'us-east-1',
                'health_status': 'healthy',
                'connectivity_confirmed': True,
                'assessment_timestamp': '2024-01-01T00:00:00',
                'confidence': 0.9
            },
            'deployment_instruction': 'Upgrade from 2.14.0 to 2.15.0',
            'agent_inheritance_ready': False,
            'validation_results': None
        }
        
        # Test from_dict method
        context = FoundationContext.from_dict(context_dict)
        
        self.assertIsInstance(context, FoundationContext)
        self.assertEqual(context.jira_info.jira_id, "ACM-12345")
        self.assertEqual(context.version_context.target_version, "2.15.0")
        self.assertEqual(context.environment_baseline.cluster_name, "test-cluster")
    
    def test_foundation_context_file_operations(self):
        """Test saving and loading foundation context from file"""
        context = FoundationContext(
            metadata=self.metadata,
            jira_info=self.jira_info,
            version_context=self.version_context,
            environment_baseline=self.environment_baseline,
            deployment_instruction="Upgrade from 2.14.0 to 2.15.0"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Test saving to file
            success = context.save_to_file(temp_filename)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(temp_filename))
            
            # Test loading from file
            loaded_context = FoundationContext.from_json_file(temp_filename)
            
            self.assertIsInstance(loaded_context, FoundationContext)
            self.assertEqual(loaded_context.jira_info.jira_id, "ACM-12345")
            self.assertEqual(loaded_context.version_context.target_version, "2.15.0")
            
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_agent_context_summary(self):
        """Test agent context summary generation"""
        context = FoundationContext(
            metadata=self.metadata,
            jira_info=self.jira_info,
            version_context=self.version_context,
            environment_baseline=self.environment_baseline,
            deployment_instruction="Upgrade from 2.14.0 to 2.15.0"
        )
        
        summary = context.get_agent_context_summary()
        
        self.assertIsInstance(summary, dict)
        
        # Check required fields for agent inheritance
        expected_fields = [
            'jira_id', 'target_version', 'environment_version',
            'version_gap', 'environment', 'deployment_instruction'
        ]
        
        for field in expected_fields:
            self.assertIn(field, summary)
        
        self.assertEqual(summary['jira_id'], "ACM-12345")
        self.assertEqual(summary['target_version'], "2.15.0")
        self.assertEqual(summary['environment_version'], "2.14.0")
    
    def test_readiness_for_agent_inheritance(self):
        """Test agent inheritance readiness check"""
        context = FoundationContext(
            metadata=self.metadata,
            jira_info=self.jira_info,
            version_context=self.version_context,
            environment_baseline=self.environment_baseline,
            deployment_instruction="Upgrade from 2.14.0 to 2.15.0"
        )
        
        # Test agent inheritance readiness
        # The method should return True if context is complete and valid
        is_ready = context.is_ready_for_agent_inheritance()
        
        # Check that the method performed validation and updated readiness status
        self.assertIsInstance(is_ready, bool)
        self.assertEqual(context.agent_inheritance_ready, is_ready)
        
        # If all validation results are True, should be ready
        validation_results = context.validate_completeness()
        if all(validation_results.values()):
            self.assertTrue(is_ready, "Context should be ready when all validations pass")


class TestFoundationContextBuilder(unittest.TestCase):
    """Test Foundation Context Builder"""
    
    def test_builder_pattern(self):
        """Test foundation context builder pattern"""
        builder = FoundationContextBuilder()
        
        context = (builder
                  .with_jira_info(
                      jira_id="ACM-12345",
                      title="Test Issue",
                      status="Open",
                      fix_version="2.15.0",
                      priority="High",
                      component="TestComponent"
                  )
                  .with_version_context(
                      target_version="2.15.0",
                      environment_version="2.14.0",
                      comparison_result="newer",
                      detection_method="api_detection"
                  )
                  .with_environment_baseline(
                      cluster_name="test-cluster",
                      api_url="https://api.test-cluster.com:6443",
                      console_url="https://console.test-cluster.com",
                      platform="openshift",
                      region="us-east-1",
                      health_status="healthy",
                      connectivity_confirmed=True
                  )
                  .with_deployment_instruction("Upgrade from 2.14.0 to 2.15.0")
                  .build())
        
        self.assertIsInstance(context, FoundationContext)
        self.assertEqual(context.jira_info.jira_id, "ACM-12345")
        self.assertEqual(context.version_context.target_version, "2.15.0")
        self.assertEqual(context.environment_baseline.cluster_name, "test-cluster")
        self.assertEqual(context.deployment_instruction, "Upgrade from 2.14.0 to 2.15.0")
    
    def test_builder_validation(self):
        """Test builder validation requirements"""
        builder = FoundationContextBuilder()
        
        # Should raise error if required fields are missing
        with self.assertRaises(ValueError) as context:
            builder.build()
        
        self.assertIn("Missing required components", str(context.exception))


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""
    
    def test_create_foundation_context_function(self):
        """Test create_foundation_context convenience function"""
        context = create_foundation_context(
            jira_id="ACM-12345",
            jira_title="Test Issue",
            jira_status="Open",
            target_version="2.15.0",
            environment_version="2.14.0",
            cluster_name="test-cluster",
            environment_health="healthy",
            deployment_instruction="Upgrade from 2.14.0 to 2.15.0"
        )
        
        self.assertIsInstance(context, FoundationContext)
        self.assertEqual(context.jira_info.jira_id, "ACM-12345")
        self.assertEqual(context.version_context.target_version, "2.15.0")
        self.assertEqual(context.environment_baseline.cluster_name, "test-cluster")


if __name__ == '__main__':
    unittest.main()