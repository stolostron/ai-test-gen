#!/usr/bin/env python3
"""
Unit Tests for Progressive Context Architecture
Tests the context inheritance system across the 4-agent framework
"""

import unittest
import os
import sys
import json
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

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
    from progressive_context_setup import (
        AgentContextRequirements, ContextInheritanceChain, 
        ProgressiveContextArchitecture, setup_progressive_context_for_jira,
        get_agent_context_for_jira
    )
    from foundation_context import (
        FoundationContext, ContextMetadata, JiraTicketInfo, 
        VersionContext, EnvironmentBaseline
    )
except ImportError as e:
    print(f"Failed to import Progressive Context Architecture modules: {e}")
    print(f"AI Services path: {setup_ai_services_path()}")
    sys.exit(1)


class TestAgentContextRequirements(unittest.TestCase):
    """Test AgentContextRequirements dataclass"""
    
    def test_agent_context_requirements_creation(self):
        """Test creating AgentContextRequirements"""
        req = AgentContextRequirements(
            agent_name="Agent A - JIRA Intelligence",
            agent_type="jira_intelligence",
            required_context_fields=["jira_id", "target_version"],
            context_inheritance_level="full"
        )
        
        self.assertEqual(req.agent_name, "Agent A - JIRA Intelligence")
        self.assertEqual(req.agent_type, "jira_intelligence")
        self.assertEqual(req.required_context_fields, ["jira_id", "target_version"])
        self.assertEqual(req.context_inheritance_level, "full")
        self.assertTrue(req.context_validation_required)  # Default value
        self.assertFalse(req.context_enrichment_needed)  # Default value
    
    def test_agent_context_requirements_with_custom_flags(self):
        """Test AgentContextRequirements with custom validation flags"""
        req = AgentContextRequirements(
            agent_name="Agent B - Documentation Intelligence",
            agent_type="documentation_intelligence",
            required_context_fields=["jira_id", "component"],
            context_inheritance_level="partial",
            context_validation_required=False,
            context_enrichment_needed=True
        )
        
        self.assertEqual(req.context_inheritance_level, "partial")
        self.assertFalse(req.context_validation_required)
        self.assertTrue(req.context_enrichment_needed)


class TestContextInheritanceChain(unittest.TestCase):
    """Test ContextInheritanceChain dataclass"""
    
    def setUp(self):
        """Set up test environment"""
        # Create mock foundation context
        self.mock_foundation_context = Mock(spec=FoundationContext)
        self.mock_foundation_context.jira_info = Mock()
        self.mock_foundation_context.jira_info.jira_id = "ACM-12345"
    
    def test_context_inheritance_chain_creation(self):
        """Test creating ContextInheritanceChain"""
        chain = ContextInheritanceChain(
            foundation_context=self.mock_foundation_context,
            agent_contexts={"agent_a": {"field": "value"}},
            inheritance_metadata={"key": "value"},
            validation_results={"agent_a": True}
        )
        
        self.assertEqual(chain.foundation_context, self.mock_foundation_context)
        self.assertEqual(chain.agent_contexts["agent_a"]["field"], "value")
        self.assertEqual(chain.inheritance_metadata["key"], "value")
        self.assertEqual(chain.validation_results["agent_a"], True)
        self.assertFalse(chain.chain_integrity)  # Default value
    
    def test_context_inheritance_chain_post_init(self):
        """Test ContextInheritanceChain __post_init__ method"""
        chain = ContextInheritanceChain(
            foundation_context=self.mock_foundation_context,
            agent_contexts=None,
            inheritance_metadata=None,
            validation_results=None
        )
        
        # Should initialize empty dicts
        self.assertEqual(chain.agent_contexts, {})
        self.assertEqual(chain.inheritance_metadata, {})
        self.assertEqual(chain.validation_results, {})


class TestProgressiveContextArchitecture(unittest.TestCase):
    """Test ProgressiveContextArchitecture main class"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.pca = ProgressiveContextArchitecture(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test ProgressiveContextArchitecture initialization"""
        self.assertEqual(self.pca.framework_root, self.temp_dir)
        self.assertTrue(self.pca.context_dir.exists())
        self.assertIsInstance(self.pca.agent_configurations, dict)
        self.assertEqual(len(self.pca.agent_configurations), 4)  # 4 agents
        self.assertIsInstance(self.pca.active_chains, dict)
    
    def test_load_agent_configurations(self):
        """Test loading agent configurations"""
        configs = self.pca._load_agent_configurations()
        
        # Should have 4 agents
        self.assertEqual(len(configs), 4)
        
        # Check specific agent configurations
        expected_agents = [
            'agent_a_jira_intelligence',
            'agent_b_documentation_intelligence', 
            'agent_c_github_investigation',
            'agent_d_environment_intelligence'
        ]
        
        for agent_key in expected_agents:
            self.assertIn(agent_key, configs)
            config = configs[agent_key]
            self.assertIsInstance(config, AgentContextRequirements)
            self.assertTrue(config.agent_name)
            self.assertTrue(config.agent_type)
            self.assertTrue(config.required_context_fields)
            self.assertEqual(config.context_inheritance_level, "full")
    
    def test_agent_a_configuration_details(self):
        """Test Agent A configuration details"""
        agent_config = self.pca.agent_configurations['agent_a_jira_intelligence']
        
        self.assertEqual(agent_config.agent_name, 'Agent A - JIRA Intelligence')
        self.assertEqual(agent_config.agent_type, 'jira_intelligence')
        self.assertTrue(agent_config.context_validation_required)
        self.assertTrue(agent_config.context_enrichment_needed)
        
        # Check required fields
        expected_fields = [
            'jira_id', 'jira_title', 'jira_status', 'target_version',
            'priority', 'component', 'deployment_instruction'
        ]
        for field in expected_fields:
            self.assertIn(field, agent_config.required_context_fields)
    
    def test_agent_d_configuration_details(self):
        """Test Agent D configuration details"""
        agent_config = self.pca.agent_configurations['agent_d_environment_intelligence']
        
        self.assertEqual(agent_config.agent_name, 'Agent D - Environment Intelligence')
        self.assertEqual(agent_config.agent_type, 'environment_intelligence')
        
        # Check specific required fields for Agent D
        expected_fields = [
            'jira_id', 'target_version', 'environment_version', 'cluster_name',
            'platform', 'health_status', 'deployment_instruction'
        ]
        for field in expected_fields:
            self.assertIn(field, agent_config.required_context_fields)
    
    @patch('progressive_context_setup.VersionIntelligenceService')
    def test_create_foundation_context_for_jira(self, mock_vis_class):
        """Test creating foundation context for JIRA"""
        # Mock VersionIntelligenceService
        mock_vis = Mock()
        mock_vis_class.return_value = mock_vis
        
        # Mock foundation context
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.is_ready_for_agent_inheritance.return_value = True
        mock_foundation_context.metadata = Mock()
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        mock_foundation_context.get_agent_context_summary.return_value = {}
        
        mock_vis.create_foundation_context.return_value = mock_foundation_context
        
        # Test foundation context creation
        result = self.pca.create_foundation_context_for_jira("ACM-12345", "test-env")
        
        # Verify calls
        mock_vis.create_foundation_context.assert_called_once_with("ACM-12345", "test-env")
        mock_foundation_context.is_ready_for_agent_inheritance.assert_called_once()
        
        # Verify enhancement
        self.assertEqual(result.metadata.context_version, "1.1.0-pca")
        self.assertTrue(result.metadata.pca_enabled)
        self.assertTrue(result.metadata.agent_inheritance_ready)
    
    @patch('progressive_context_setup.VersionIntelligenceService')
    def test_create_foundation_context_validation_failure(self, mock_vis_class):
        """Test foundation context creation with validation failure"""
        # Mock VersionIntelligenceService
        mock_vis = Mock()
        mock_vis_class.return_value = mock_vis
        
        # Mock foundation context that fails validation
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.is_ready_for_agent_inheritance.return_value = False
        mock_foundation_context.metadata = Mock()
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        mock_foundation_context.get_agent_context_summary.return_value = {}
        
        mock_vis.create_foundation_context.return_value = mock_foundation_context
        
        # Should raise ValueError on validation failure
        with self.assertRaises(ValueError) as context:
            self.pca.create_foundation_context_for_jira("ACM-12345", "test-env")
        
        self.assertIn("Foundation context validation failed", str(context.exception))
    
    def test_enhance_foundation_for_pca(self):
        """Test enhancing foundation context for PCA"""
        # Create mock foundation context
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.metadata = Mock()
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        mock_foundation_context.get_agent_context_summary.return_value = {}
        
        # Test enhancement
        enhanced = self.pca._enhance_foundation_for_pca(mock_foundation_context)
        
        # Verify PCA enhancements
        self.assertEqual(enhanced.metadata.context_version, "1.1.0-pca")
        self.assertTrue(enhanced.metadata.pca_enabled)
        self.assertTrue(enhanced.metadata.agent_inheritance_ready)
        
        # Verify PCA agent context summary was set
        self.assertTrue(hasattr(enhanced, '_pca_agent_context_summary'))
        pca_summary = enhanced._pca_agent_context_summary
        
        # Check PCA metadata
        self.assertIn('pca_metadata', pca_summary)
        pca_metadata = pca_summary['pca_metadata']
        self.assertTrue(pca_metadata['agent_inheritance_ready'])
        self.assertEqual(pca_metadata['agent_count'], 4)
        self.assertEqual(pca_metadata['expected_agents'], ['agent_a', 'agent_b', 'agent_c', 'agent_d'])
        
        # Check agent contexts
        for agent in ['agent_a', 'agent_b', 'agent_c', 'agent_d']:
            agent_key = f"{agent}_context"
            self.assertIn(agent_key, pca_summary)
            self.assertTrue(pca_summary[agent_key]['context_ready'])
    
    def test_prepare_agent_contexts(self):
        """Test preparing individual agent contexts"""
        # Create mock foundation context
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        mock_foundation_context.version_context = Mock()
        mock_foundation_context.environment_baseline = Mock()
        mock_foundation_context.environment_baseline.platform = "OpenShift"
        mock_foundation_context.environment_baseline.cluster_name = "test-cluster"
        mock_foundation_context.environment_baseline.health_status = "healthy"
        
        # Mock get_agent_context_summary
        base_context = {
            'jira_id': 'ACM-12345',
            'target_version': '2.15.0',
            'component': 'TestComponent'
        }
        mock_foundation_context.get_agent_context_summary.return_value = base_context
        
        # Test agent context preparation
        agent_contexts = self.pca._prepare_agent_contexts(mock_foundation_context)
        
        # Should have contexts for all 4 agents
        self.assertEqual(len(agent_contexts), 4)
        
        # Check agent A context
        agent_a_context = agent_contexts['agent_a_jira_intelligence']
        self.assertIn('jira_id', agent_a_context)
        self.assertIn('target_version', agent_a_context)
        self.assertIn('agent_metadata', agent_a_context)
        self.assertIn('context_validation', agent_a_context)
        
        # Check agent metadata
        metadata = agent_a_context['agent_metadata']
        self.assertEqual(metadata['agent_name'], 'Agent A - JIRA Intelligence')
        self.assertEqual(metadata['agent_type'], 'jira_intelligence')
        self.assertEqual(metadata['foundation_context_id'], 'ACM-12345')
        
        # Check context validation
        validation = agent_a_context['context_validation']
        self.assertIn('required_fields_present', validation)
        self.assertIn('context_completeness_score', validation)
        self.assertTrue(validation['validation_passed'])
    
    def test_get_default_value_for_field(self):
        """Test getting default values for missing fields"""
        # Create mock foundation context
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.environment_baseline = Mock()
        mock_foundation_context.environment_baseline.platform = "OpenShift"
        mock_foundation_context.environment_baseline.cluster_name = "test-cluster"
        mock_foundation_context.environment_baseline.health_status = "healthy"
        
        # Test known defaults
        self.assertEqual(
            self.pca._get_default_value_for_field('agent_a_findings', mock_foundation_context),
            {}
        )
        self.assertEqual(
            self.pca._get_default_value_for_field('environment_platform', mock_foundation_context),
            "OpenShift"
        )
        self.assertEqual(
            self.pca._get_default_value_for_field('cluster_name', mock_foundation_context),
            "test-cluster"
        )
        
        # Test unknown field
        result = self.pca._get_default_value_for_field('unknown_field', mock_foundation_context)
        self.assertEqual(result, "auto_generated_unknown_field")
    
    def test_validate_inheritance_chain(self):
        """Test validating inheritance chain integrity"""
        # Create mock inheritance chain
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.is_ready_for_agent_inheritance.return_value = True
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        
        # Create agent contexts with proper validation structure
        agent_contexts = {}
        for agent_key in self.pca.agent_configurations.keys():
            agent_contexts[agent_key] = {
                'jira_id': 'ACM-12345',
                'target_version': '2.15.0',
                'context_validation': {
                    'context_completeness_score': 0.9,
                    'validation_passed': True
                }
            }
            # Add all required fields for this agent
            for field in self.pca.agent_configurations[agent_key].required_context_fields:
                agent_contexts[agent_key][field] = f"mock_{field}"
        
        inheritance_chain = ContextInheritanceChain(
            foundation_context=mock_foundation_context,
            agent_contexts=agent_contexts,
            inheritance_metadata={},
            validation_results={}
        )
        
        # Test validation
        result = self.pca._validate_inheritance_chain(inheritance_chain)
        
        # Should pass validation
        self.assertTrue(result)
        self.assertTrue(inheritance_chain.validation_results['foundation_context'])
        
        # All agent validations should pass
        for agent_key in self.pca.agent_configurations.keys():
            self.assertTrue(inheritance_chain.validation_results[agent_key])
    
    def test_validate_inheritance_chain_failure(self):
        """Test inheritance chain validation with failures"""
        # Create mock inheritance chain with failing foundation
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.is_ready_for_agent_inheritance.return_value = False
        
        inheritance_chain = ContextInheritanceChain(
            foundation_context=mock_foundation_context,
            agent_contexts={},
            inheritance_metadata={},
            validation_results={}
        )
        
        # Test validation
        result = self.pca._validate_inheritance_chain(inheritance_chain)
        
        # Should fail validation
        self.assertFalse(result)
        self.assertFalse(inheritance_chain.validation_results['foundation_context'])
    
    def test_initialize_context_inheritance_chain(self):
        """Test initializing complete inheritance chain"""
        # Create mock foundation context with PCA summary
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        mock_foundation_context.version_context = Mock()
        mock_foundation_context.environment_baseline = Mock()
        mock_foundation_context.is_ready_for_agent_inheritance.return_value = True
        mock_foundation_context.get_agent_context_summary.return_value = {
            'jira_id': 'ACM-12345',
            'target_version': '2.15.0'
        }
        
        # Mock PCA agent context summary
        pca_summary = {
            'pca_metadata': {
                'context_chain_id': 'pca_ACM-12345_20240101_120000'
            }
        }
        mock_foundation_context._pca_agent_context_summary = pca_summary
        
        # Test chain initialization
        with patch.object(self.pca, '_save_inheritance_chain') as mock_save:
            inheritance_chain = self.pca.initialize_context_inheritance_chain(mock_foundation_context)
        
        # Verify chain creation
        self.assertIsInstance(inheritance_chain, ContextInheritanceChain)
        self.assertEqual(inheritance_chain.foundation_context, mock_foundation_context)
        self.assertEqual(len(inheritance_chain.agent_contexts), 4)
        
        # Verify chain is stored in active chains
        chain_id = pca_summary['pca_metadata']['context_chain_id']
        self.assertIn(chain_id, self.pca.active_chains)
        
        # Verify save was called
        mock_save.assert_called_once_with(inheritance_chain)
    
    def test_save_inheritance_chain(self):
        """Test saving inheritance chain to disk"""
        # Create mock inheritance chain
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        mock_foundation_context.get_agent_context_summary.return_value = {
            'jira_id': 'ACM-12345'
        }
        
        inheritance_chain = ContextInheritanceChain(
            foundation_context=mock_foundation_context,
            agent_contexts={'agent_a': {'field': 'value'}},
            inheritance_metadata={
                'chain_id': 'test_chain_123',
                'created_at': '2024-01-01T12:00:00'
            },
            validation_results={'foundation_context': True},
            chain_integrity=True
        )
        
        # Test saving
        self.pca._save_inheritance_chain(inheritance_chain)
        
        # Verify file was created
        expected_dir = self.pca.context_dir / "ACM-12345"
        expected_file = expected_dir / "test_chain_123.json"
        
        self.assertTrue(expected_dir.exists())
        self.assertTrue(expected_file.exists())
        
        # Verify file content
        with open(expected_file) as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data['inheritance_metadata']['chain_id'], 'test_chain_123')
        self.assertTrue(saved_data['chain_integrity'])
        self.assertIn('agent_a', saved_data['agent_contexts'])
    
    def test_get_agent_context(self):
        """Test getting specific agent context"""
        # Create and store mock inheritance chain
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        
        test_context = {'field': 'value', 'agent_id': 'agent_a'}
        inheritance_chain = ContextInheritanceChain(
            foundation_context=mock_foundation_context,
            agent_contexts={'agent_a': test_context},
            inheritance_metadata={},
            validation_results={}
        )
        
        chain_id = 'test_chain_456'
        self.pca.active_chains[chain_id] = inheritance_chain
        
        # Test getting agent context
        result = self.pca.get_agent_context(chain_id, 'agent_a')
        
        self.assertEqual(result, test_context)
        self.assertEqual(result['field'], 'value')
        self.assertEqual(result['agent_id'], 'agent_a')
    
    def test_get_agent_context_not_found(self):
        """Test getting agent context for non-existent chain/agent"""
        # Test non-existent chain
        result = self.pca.get_agent_context('non_existent_chain', 'agent_a')
        self.assertIsNone(result)
        
        # Test non-existent agent in existing chain
        mock_foundation_context = Mock(spec=FoundationContext)
        inheritance_chain = ContextInheritanceChain(
            foundation_context=mock_foundation_context,
            agent_contexts={},
            inheritance_metadata={},
            validation_results={}
        )
        
        chain_id = 'test_chain_789'
        self.pca.active_chains[chain_id] = inheritance_chain
        
        result = self.pca.get_agent_context(chain_id, 'non_existent_agent')
        self.assertIsNone(result)
    
    def test_update_agent_context(self):
        """Test updating agent context with new data"""
        # Create and store mock inheritance chain
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        
        test_context = {
            'field': 'original_value',
            'agent_metadata': {'key': 'value'}
        }
        inheritance_chain = ContextInheritanceChain(
            foundation_context=mock_foundation_context,
            agent_contexts={'agent_a': test_context},
            inheritance_metadata={},
            validation_results={}
        )
        
        chain_id = 'test_chain_update'
        self.pca.active_chains[chain_id] = inheritance_chain
        
        # Test updating context
        updates = {'field': 'updated_value', 'new_field': 'new_value'}
        
        with patch.object(self.pca, '_save_inheritance_chain') as mock_save:
            result = self.pca.update_agent_context(chain_id, 'agent_a', updates)
        
        # Verify update was successful
        self.assertTrue(result)
        
        # Verify context was updated
        updated_context = self.pca.active_chains[chain_id].agent_contexts['agent_a']
        self.assertEqual(updated_context['field'], 'updated_value')
        self.assertEqual(updated_context['new_field'], 'new_value')
        self.assertIn('last_updated', updated_context['agent_metadata'])
        
        # Verify save was called
        mock_save.assert_called_once()
    
    def test_update_agent_context_failures(self):
        """Test update_agent_context failure scenarios"""
        # Test non-existent chain
        result = self.pca.update_agent_context('non_existent', 'agent_a', {})
        self.assertFalse(result)
        
        # Test non-existent agent
        mock_foundation_context = Mock(spec=FoundationContext)
        inheritance_chain = ContextInheritanceChain(
            foundation_context=mock_foundation_context,
            agent_contexts={},
            inheritance_metadata={},
            validation_results={}
        )
        
        chain_id = 'test_chain_fail'
        self.pca.active_chains[chain_id] = inheritance_chain
        
        result = self.pca.update_agent_context(chain_id, 'non_existent_agent', {})
        self.assertFalse(result)
    
    def test_get_chain_status(self):
        """Test getting comprehensive chain status"""
        # Create mock inheritance chain
        mock_foundation_context = Mock(spec=FoundationContext)
        mock_foundation_context.jira_info = Mock()
        mock_foundation_context.jira_info.jira_id = "ACM-12345"
        
        agent_contexts = {
            'agent_a': {
                'context_validation': {'validation_passed': True}
            },
            'agent_b': {
                'context_validation': {'validation_passed': False}
            }
        }
        
        inheritance_chain = ContextInheritanceChain(
            foundation_context=mock_foundation_context,
            agent_contexts=agent_contexts,
            inheritance_metadata={
                'created_at': '2024-01-01T12:00:00'
            },
            validation_results={'foundation_context': True, 'agent_a': True, 'agent_b': False},
            chain_integrity=False
        )
        
        chain_id = 'status_test_chain'
        self.pca.active_chains[chain_id] = inheritance_chain
        
        # Test getting status
        status = self.pca.get_chain_status(chain_id)
        
        # Verify status information
        self.assertEqual(status['chain_id'], chain_id)
        self.assertEqual(status['foundation_jira_id'], 'ACM-12345')
        self.assertFalse(status['chain_integrity'])
        self.assertEqual(status['agent_count'], 2)
        self.assertEqual(status['agents_ready'], 1)  # Only agent_a is ready
        self.assertEqual(status['creation_time'], '2024-01-01T12:00:00')
        self.assertFalse(status['all_agents_ready'])
    
    def test_get_chain_status_not_found(self):
        """Test getting status for non-existent chain"""
        status = self.pca.get_chain_status('non_existent_chain')
        
        self.assertIn('error', status)
        self.assertIn('not found', status['error'])


class TestProgressiveContextConvenienceFunctions(unittest.TestCase):
    """Test convenience functions for PCA"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    @patch('progressive_context_setup.ProgressiveContextArchitecture')
    def test_setup_progressive_context_for_jira(self, mock_pca_class):
        """Test setup_progressive_context_for_jira convenience function"""
        # Mock PCA instance
        mock_pca = Mock()
        mock_pca_class.return_value = mock_pca
        
        # Mock foundation context and inheritance chain
        mock_foundation = Mock(spec=FoundationContext)
        mock_chain = Mock(spec=ContextInheritanceChain)
        
        mock_pca.create_foundation_context_for_jira.return_value = mock_foundation
        mock_pca.initialize_context_inheritance_chain.return_value = mock_chain
        
        # Test convenience function
        result = setup_progressive_context_for_jira("ACM-12345", "test-env")
        
        # Verify calls
        mock_pca.create_foundation_context_for_jira.assert_called_once_with("ACM-12345", "test-env")
        mock_pca.initialize_context_inheritance_chain.assert_called_once_with(mock_foundation)
        self.assertEqual(result, mock_chain)
    
    @patch('progressive_context_setup.ProgressiveContextArchitecture')
    def test_get_agent_context_for_jira(self, mock_pca_class):
        """Test get_agent_context_for_jira convenience function"""
        # Mock PCA instance
        mock_pca = Mock()
        mock_pca_class.return_value = mock_pca
        
        # Mock active chains
        mock_foundation = Mock(spec=FoundationContext)
        mock_foundation.jira_info = Mock()
        mock_foundation.jira_info.jira_id = "ACM-12345"
        
        mock_chain = Mock(spec=ContextInheritanceChain)
        mock_chain.foundation_context = mock_foundation
        
        mock_pca.active_chains = {
            'chain_123': mock_chain
        }
        
        test_context = {'agent': 'context_data'}
        mock_pca.get_agent_context.return_value = test_context
        
        # Test convenience function
        result = get_agent_context_for_jira("ACM-12345", "agent_a")
        
        # Verify call
        mock_pca.get_agent_context.assert_called_once_with('chain_123', 'agent_a')
        self.assertEqual(result, test_context)
    
    @patch('progressive_context_setup.ProgressiveContextArchitecture')
    def test_get_agent_context_for_jira_not_found(self, mock_pca_class):
        """Test get_agent_context_for_jira when JIRA ID not found"""
        # Mock PCA instance with no matching chains
        mock_pca = Mock()
        mock_pca_class.return_value = mock_pca
        mock_pca.active_chains = {}
        
        # Test convenience function
        result = get_agent_context_for_jira("ACM-99999", "agent_a")
        
        # Should return None when no matching chain found
        self.assertIsNone(result)


if __name__ == '__main__':
    print("🧪 Progressive Context Architecture Unit Tests")
    print("Testing context inheritance system across 4-agent framework")
    print("=" * 70)
    
    unittest.main(verbosity=2)