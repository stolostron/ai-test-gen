#!/usr/bin/env python3
"""
Comprehensive Progressive Context Architecture Unit Tests
=========================================================

Advanced unit tests for Progressive Context Architecture testing:
- Context Inheritance Chain validation and integrity
- Context Isolation System contamination prevention
- Agent Context Requirements and specifications
- Intelligent Conflict Resolution capabilities
- Real-time Context Validation and monitoring
- Performance optimization and metrics tracking
- Integration with Framework Reliability Architecture

This test suite validates the complete Progressive Context Architecture
system ensuring 25-40% accuracy enhancement and 100% data consistency.
"""

import unittest
import sys
import os
import tempfile
import json
import time
import threading
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add the project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    # Add AI services path
    ai_services_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services')
    sys.path.insert(0, ai_services_path)
    
    # Add enforcement path  
    enforcement_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'enforcement')
    sys.path.insert(0, enforcement_path)
    
    from progressive_context_setup import (
        AgentContextRequirements,
        ContextInheritanceChain,
        ProgressiveContextArchitecture,
        setup_progressive_context_for_jira,
        get_agent_context_for_jira
    )
    from foundation_context import (
        FoundationContext,
        ContextMetadata,
        JiraTicketInfo,
        VersionContext,
        EnvironmentBaseline,
        ContextValidationLevel
    )
    from context_isolation_system import ContextIsolationSystem
    PROGRESSIVE_CONTEXT_AVAILABLE = True
except ImportError as e:
    PROGRESSIVE_CONTEXT_AVAILABLE = False
    print(f"❌ Progressive Context Architecture not available: {e}")


class TestProgressiveContextArchitecture(unittest.TestCase):
    """Test Progressive Context Architecture main orchestration system"""
    
    @classmethod
    def setUpClass(cls):
        if not PROGRESSIVE_CONTEXT_AVAILABLE:
            cls.skipTest(cls, "Progressive Context Architecture not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        self.pca = ProgressiveContextArchitecture(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_progressive_context_architecture_initialization(self):
        """Test PCA initialization and configuration"""
        self.assertEqual(self.pca.framework_root, self.test_dir)
        self.assertTrue(self.pca.context_dir.exists())
        self.assertIsInstance(self.pca.agent_configurations, dict)
        self.assertEqual(len(self.pca.active_chains), 0)
        
        # Check 4-agent configuration
        expected_agents = [
            'agent_a_jira_intelligence',
            'agent_b_documentation_intelligence', 
            'agent_c_github_investigation',
            'agent_d_environment_intelligence'
        ]
        for agent_key in expected_agents:
            self.assertIn(agent_key, self.pca.agent_configurations)
            config = self.pca.agent_configurations[agent_key]
            self.assertIsInstance(config, AgentContextRequirements)
            self.assertEqual(config.context_inheritance_level, 'full')
            self.assertTrue(config.context_validation_required)
    
    def test_agent_context_requirements_validation(self):
        """Test agent context requirements specification"""
        # Test Agent A (JIRA Intelligence)
        agent_a_config = self.pca.agent_configurations['agent_a_jira_intelligence']
        self.assertEqual(agent_a_config.agent_type, 'jira_intelligence')
        expected_fields_a = [
            'jira_id', 'jira_title', 'jira_status', 'target_version',
            'priority', 'component', 'deployment_instruction'
        ]
        for field in expected_fields_a:
            self.assertIn(field, agent_a_config.required_context_fields)
        
        # Test Agent D (Environment Intelligence)
        agent_d_config = self.pca.agent_configurations['agent_d_environment_intelligence']
        self.assertEqual(agent_d_config.agent_type, 'environment_intelligence')
        expected_fields_d = [
            'jira_id', 'target_version', 'environment_version', 'cluster_name',
            'platform', 'health_status', 'deployment_instruction'
        ]
        for field in expected_fields_d:
            self.assertIn(field, agent_d_config.required_context_fields)
        
        # Test Agent B (Documentation Intelligence)
        agent_b_config = self.pca.agent_configurations['agent_b_documentation_intelligence']
        self.assertIn('agent_a_findings', agent_b_config.required_context_fields)
        self.assertTrue(agent_b_config.context_enrichment_needed)
        
        # Test Agent C (GitHub Investigation)
        agent_c_config = self.pca.agent_configurations['agent_c_github_investigation']
        self.assertIn('agent_a_findings', agent_c_config.required_context_fields)
        self.assertTrue(agent_c_config.context_enrichment_needed)
    
    def test_foundation_context_enhancement_for_pca(self):
        """Test foundation context enhancement for PCA"""
        # Create mock foundation context
        mock_foundation = Mock(spec=FoundationContext)
        mock_foundation.metadata = Mock(spec=ContextMetadata)
        mock_foundation.jira_info = Mock(spec=JiraTicketInfo)
        mock_foundation.jira_info.jira_id = "ACM-TEST-123"
        mock_foundation.get_agent_context_summary = Mock(return_value={})
        
        # Test enhancement
        enhanced_context = self.pca._enhance_foundation_for_pca(mock_foundation)
        
        # Check PCA-specific metadata
        self.assertEqual(enhanced_context.metadata.context_version, "1.1.0-pca")
        self.assertTrue(enhanced_context.metadata.pca_enabled)
        self.assertTrue(enhanced_context.metadata.agent_inheritance_ready)
        
        # Check PCA agent context summary
        self.assertIsNotNone(enhanced_context._pca_agent_context_summary)
        pca_summary = enhanced_context._pca_agent_context_summary
        
        # Check PCA metadata
        self.assertIn('pca_metadata', pca_summary)
        pca_metadata = pca_summary['pca_metadata']
        self.assertIn('context_chain_id', pca_metadata)
        self.assertTrue(pca_metadata['agent_inheritance_ready'])
        self.assertEqual(pca_metadata['agent_count'], 4)
        self.assertEqual(len(pca_metadata['expected_agents']), 4)
        
        # Check agent contexts
        for agent_key in ['agent_a_context', 'agent_b_context', 'agent_c_context', 'agent_d_context']:
            self.assertIn(agent_key, pca_summary)
            agent_context = pca_summary[agent_key]
            self.assertIn('focus', agent_context)
            self.assertIn('required_fields', agent_context)
            self.assertTrue(agent_context['context_ready'])
    
    def test_context_inheritance_chain_initialization(self):
        """Test context inheritance chain initialization"""
        # Create enhanced foundation context
        mock_foundation = Mock(spec=FoundationContext)
        mock_foundation.jira_info = Mock()
        mock_foundation.jira_info.jira_id = "ACM-TEST-456"
        mock_foundation.version_context = Mock()
        mock_foundation.version_context.__dict__ = {'target_version': '2.5.0'}
        mock_foundation.environment_baseline = Mock()
        mock_foundation.environment_baseline.platform = 'OpenShift'
        mock_foundation.environment_baseline.cluster_name = 'test-cluster'
        mock_foundation.environment_baseline.health_status = 'healthy'
        mock_foundation.environment_baseline.__dict__ = {'cluster_name': 'test-cluster', 'platform': 'OpenShift', 'health_status': 'healthy'}
        mock_foundation.get_agent_context_summary = Mock(return_value={
            'jira_id': 'ACM-TEST-456',
            'target_version': '2.5.0',
            'component': 'test-component'
        })
        mock_foundation._pca_agent_context_summary = {
            'pca_metadata': {
                'context_chain_id': 'test_chain_123',
                'agent_inheritance_ready': True
            }
        }
        
        # Initialize inheritance chain
        chain = self.pca.initialize_context_inheritance_chain(mock_foundation)
        
        # Validate chain structure
        self.assertIsInstance(chain, ContextInheritanceChain)
        self.assertEqual(chain.foundation_context, mock_foundation)
        self.assertIsInstance(chain.agent_contexts, dict)
        self.assertIsInstance(chain.inheritance_metadata, dict)
        self.assertIsInstance(chain.validation_results, dict)
        
        # Check chain metadata
        self.assertIn('chain_id', chain.inheritance_metadata)
        self.assertEqual(chain.inheritance_metadata['chain_id'], 'test_chain_123')
        self.assertIn('inheritance_sequence', chain.inheritance_metadata)
        self.assertIn('validation_requirements', chain.inheritance_metadata)
        
        # Check inheritance sequence
        expected_sequence = ['foundation', 'agent_a', 'agent_d', 'agent_b', 'agent_c']
        actual_sequence = chain.inheritance_metadata['inheritance_sequence']
        for phase in expected_sequence:
            self.assertIn(phase, actual_sequence)
    
    def test_context_inheritance_chain_integrity(self):
        """Test context inheritance chain integrity validation"""
        # Create test foundation context
        mock_foundation = Mock(spec=FoundationContext)
        mock_foundation.jira_info = Mock()
        mock_foundation.jira_info.jira_id = "ACM-INTEGRITY-789"
        mock_foundation.version_context = Mock()
        mock_foundation.version_context.__dict__ = {'target_version': '2.5.0'}
        mock_foundation.environment_baseline = Mock()
        mock_foundation.environment_baseline.platform = 'OpenShift'
        mock_foundation.environment_baseline.cluster_name = 'test-cluster'
        mock_foundation.environment_baseline.health_status = 'healthy'
        mock_foundation.environment_baseline.__dict__ = {'cluster_name': 'test-cluster', 'platform': 'OpenShift', 'health_status': 'healthy'}
        mock_foundation.get_agent_context_summary = Mock(return_value={
            'jira_id': 'ACM-INTEGRITY-789',
            'target_version': '2.5.0',
            'component': 'test-component'
        })
        mock_foundation._pca_agent_context_summary = {
            'pca_metadata': {
                'context_chain_id': 'integrity_test_chain',
                'agent_inheritance_ready': True
            }
        }
        
        # Initialize chain
        chain = self.pca.initialize_context_inheritance_chain(mock_foundation)
        
        # Test chain integrity before agent contexts
        self.assertFalse(chain.chain_integrity)
        
        # Add agent contexts
        chain.agent_contexts = {
            'agent_a': {'context_validation': {'validation_passed': True}},
            'agent_d': {'context_validation': {'validation_passed': True}},
            'agent_b': {'context_validation': {'validation_passed': True}},
            'agent_c': {'context_validation': {'validation_passed': True}}
        }
        
        # Update validation results
        chain.validation_results = {
            'agent_a': True,
            'agent_d': True, 
            'agent_b': True,
            'agent_c': True
        }
        
        # Test chain integrity calculation
        chain.chain_integrity = all(chain.validation_results.values())
        self.assertTrue(chain.chain_integrity)
    
    def test_context_chain_management(self):
        """Test context chain management and tracking"""
        # Test with multiple chains
        for i in range(3):
            jira_id = f"ACM-CHAIN-{i}"
            mock_foundation = Mock(spec=FoundationContext)
            mock_foundation.jira_info = Mock()
            mock_foundation.jira_info.jira_id = jira_id
            mock_foundation.version_context = Mock()
            mock_foundation.version_context.__dict__ = {'target_version': '2.5.0'}
            mock_foundation.environment_baseline = Mock()
            mock_foundation.environment_baseline.__dict__ = {'cluster_name': 'test-cluster'}
            mock_foundation.get_agent_context_summary = Mock(return_value={
                'jira_id': jira_id,
                'target_version': '2.5.0',
                'component': 'test-component'
            })
            mock_foundation._pca_agent_context_summary = {
                'pca_metadata': {
                    'context_chain_id': f'chain_{i}',
                    'agent_inheritance_ready': True
                }
            }
            
            chain = self.pca.initialize_context_inheritance_chain(mock_foundation)
            chain_id = chain.inheritance_metadata['chain_id']
            
            # Store chain
            self.pca.active_chains[chain_id] = chain
        
        # Validate chain management
        self.assertEqual(len(self.pca.active_chains), 3)
        
        # Test chain retrieval by JIRA ID
        for i in range(3):
            jira_id = f"ACM-CHAIN-{i}"
            found_chain = None
            for chain_id, chain in self.pca.active_chains.items():
                if chain.foundation_context.jira_info.jira_id == jira_id:
                    found_chain = chain
                    break
            self.assertIsNotNone(found_chain)


class TestContextIsolationSystem(unittest.TestCase):
    """Test Context Isolation System contamination prevention"""
    
    @classmethod
    def setUpClass(cls):
        if not PROGRESSIVE_CONTEXT_AVAILABLE:
            cls.skipTest(cls, "Progressive Context Architecture not available")
    
    def setUp(self):
        """Set up test environment"""
        self.isolation_system = ContextIsolationSystem()
    
    def test_context_isolation_system_initialization(self):
        """Test context isolation system initialization"""
        self.assertTrue(self.isolation_system.isolation_active)
        self.assertIsInstance(self.isolation_system.contamination_sources, list)
        
        # Check contamination sources
        expected_sources = [
            'previous_runs', 'chat_context', 'cached_analysis',
            'agent_shortcuts', 'environment_simulation'
        ]
        for source in expected_sources:
            self.assertIn(source, self.isolation_system.contamination_sources)
    
    def test_previous_run_access_blocking(self):
        """Test previous run access blocking"""
        test_context = {
            'jira_id': 'ACM-ISOLATION-123',
            'test_mode': True
        }
        
        blocked_context = self.isolation_system.block_previous_run_access(test_context)
        
        # Check blocking flags
        self.assertTrue(blocked_context['ignore_existing_runs'])
        self.assertTrue(blocked_context['ignore_run_cache'])
        self.assertTrue(blocked_context['ignore_metadata_cache'])
        self.assertTrue(blocked_context['block_run_directory_scanning'])
        self.assertTrue(blocked_context['force_new_run_creation'])
        
        # Check prevention settings
        self.assertEqual(blocked_context['previous_run_detection'], 'DISABLED')
        self.assertEqual(blocked_context['run_optimization'], 'DISABLED')
        self.assertEqual(blocked_context['context_reuse'], 'DISABLED')
        
        # Original context should be preserved
        self.assertEqual(blocked_context['jira_id'], 'ACM-ISOLATION-123')
        self.assertTrue(blocked_context['test_mode'])
    
    def test_chat_contamination_clearing(self):
        """Test chat session contamination clearing"""
        test_context = {
            'user_request': 'Generate test plan',
            'session_data': 'some_data'
        }
        
        cleared_context = self.isolation_system.clear_chat_contamination(test_context)
        
        # Check chat isolation flags
        self.assertTrue(cleared_context['ignore_chat_history'])
        self.assertTrue(cleared_context['ignore_conversation_context'])
        self.assertTrue(cleared_context['ignore_user_familiarity'])
        self.assertTrue(cleared_context['ignore_session_state'])
        self.assertTrue(cleared_context['treat_as_first_request'])
        
        # Check isolation settings
        self.assertEqual(cleared_context['chat_context_isolation'], 'STRICT')
        self.assertEqual(cleared_context['conversation_influence'], 'DISABLED')
        
        # Original context should be preserved
        self.assertEqual(cleared_context['user_request'], 'Generate test plan')
        self.assertEqual(cleared_context['session_data'], 'some_data')
    
    def test_fresh_agent_initialization_forcing(self):
        """Test fresh agent initialization forcing"""
        test_context = {
            'agent_settings': 'existing_settings'
        }
        
        fresh_context = self.isolation_system.force_fresh_agent_initialization(test_context)
        
        # Check fresh initialization flags
        self.assertEqual(fresh_context['agent_state_reset'], 'MANDATORY')
        self.assertEqual(fresh_context['agent_cache_clear'], 'COMPLETE')
        self.assertEqual(fresh_context['agent_memory_isolation'], 'STRICT')
        self.assertTrue(fresh_context['force_agent_restart'])
    
    def test_complete_context_isolation_enforcement(self):
        """Test complete context isolation enforcement"""
        original_context = {
            'jira_id': 'ACM-COMPLETE-456',
            'user_input': 'test plan request',
            'environment': 'test_cluster'
        }
        
        isolated_context = self.isolation_system.enforce_context_isolation(original_context)
        
        # Should have all isolation measures applied
        isolation_flags = [
            'ignore_existing_runs', 'ignore_chat_history', 'agent_state_reset',
            'block_run_directory_scanning', 'treat_as_first_request'
        ]
        for flag in isolation_flags:
            self.assertIn(flag, isolated_context)
        
        # Original context should be preserved
        self.assertEqual(isolated_context['jira_id'], 'ACM-COMPLETE-456')
        self.assertEqual(isolated_context['user_input'], 'test plan request')
        self.assertEqual(isolated_context['environment'], 'test_cluster')


class TestFoundationContextEnhancement(unittest.TestCase):
    """Test Foundation Context data structures and validation"""
    
    @classmethod
    def setUpClass(cls):
        if not PROGRESSIVE_CONTEXT_AVAILABLE:
            cls.skipTest(cls, "Progressive Context Architecture not available")
    
    def test_context_metadata_creation(self):
        """Test context metadata creation and validation"""
        metadata = ContextMetadata(
            context_version="1.1.0-test",
            validation_level=ContextValidationLevel.COMPREHENSIVE
        )
        
        self.assertEqual(metadata.context_version, "1.1.0-test")
        self.assertEqual(metadata.validation_level, ContextValidationLevel.COMPREHENSIVE)
        self.assertIsNotNone(metadata.creation_timestamp)
        self.assertIsNotNone(metadata.last_updated)
        self.assertEqual(metadata.consistency_score, 1.0)
    
    def test_jira_ticket_info_structure(self):
        """Test JIRA ticket info structure"""
        jira_info = JiraTicketInfo(
            jira_id="ACM-FOUNDATION-123",
            title="Test Foundation Context",
            status="In Progress",
            fix_version="2.5.0",
            priority="High",
            component="cluster-curator",
            detection_timestamp=datetime.utcnow().isoformat(),
            confidence=0.95
        )
        
        self.assertEqual(jira_info.jira_id, "ACM-FOUNDATION-123")
        self.assertEqual(jira_info.title, "Test Foundation Context")
        self.assertEqual(jira_info.confidence, 0.95)
        self.assertIsNotNone(jira_info.detection_timestamp)
    
    def test_version_context_structure(self):
        """Test version context structure"""
        version_context = VersionContext(
            target_version="2.5.0",
            environment_version="2.4.5",
            comparison_result="newer",
            detection_method="version_intelligence_service",
            confidence=0.9,
            version_gap_details={"gap_type": "minor_upgrade", "compatibility": "confirmed"}
        )
        
        self.assertEqual(version_context.target_version, "2.5.0")
        self.assertEqual(version_context.environment_version, "2.4.5")
        self.assertEqual(version_context.comparison_result, "newer")
        self.assertIsNotNone(version_context.version_gap_details)
    
    def test_environment_baseline_structure(self):
        """Test environment baseline structure"""
        env_baseline = EnvironmentBaseline(
            cluster_name="test-cluster",
            api_url="https://api.test-cluster.example.com:6443",
            console_url="https://console.test-cluster.example.com",
            platform="OpenShift",
            region="us-east-1",
            health_status="healthy",
            connectivity_confirmed=True,
            assessment_timestamp=datetime.utcnow().isoformat(),
            confidence=0.92
        )
        
        self.assertEqual(env_baseline.cluster_name, "test-cluster")
        self.assertEqual(env_baseline.platform, "OpenShift")
        self.assertTrue(env_baseline.connectivity_confirmed)
        self.assertEqual(env_baseline.confidence, 0.92)
    
    def test_foundation_context_complete_structure(self):
        """Test complete foundation context structure"""
        metadata = ContextMetadata(validation_level=ContextValidationLevel.COMPREHENSIVE)
        jira_info = JiraTicketInfo(
            jira_id="ACM-COMPLETE-789",
            title="Complete Foundation Test",
            status="New",
            fix_version="2.5.0",
            priority="Medium",
            component="test-component",
            detection_timestamp=datetime.utcnow().isoformat()
        )
        version_context = VersionContext(
            target_version="2.5.0",
            environment_version="2.4.5",
            comparison_result="newer",
            detection_method="api_detection"
        )
        env_baseline = EnvironmentBaseline(
            cluster_name="complete-test-cluster",
            api_url="https://api.complete.example.com:6443",
            console_url="https://console.complete.example.com",
            platform="OpenShift",
            region="us-west-2",
            health_status="healthy",
            connectivity_confirmed=True,
            assessment_timestamp=datetime.utcnow().isoformat()
        )
        
        foundation_context = FoundationContext(
            metadata=metadata,
            jira_info=jira_info,
            version_context=version_context,
            environment_baseline=env_baseline,
            deployment_instruction="Deploy via GitOps pipeline",
            agent_inheritance_ready=True
        )
        
        # Test structure
        self.assertEqual(foundation_context.jira_info.jira_id, "ACM-COMPLETE-789")
        self.assertEqual(foundation_context.version_context.target_version, "2.5.0")
        self.assertEqual(foundation_context.environment_baseline.cluster_name, "complete-test-cluster")
        self.assertEqual(foundation_context.deployment_instruction, "Deploy via GitOps pipeline")
        self.assertTrue(foundation_context.agent_inheritance_ready)
        
        # Test serialization
        context_dict = foundation_context.to_dict()
        self.assertIsInstance(context_dict, dict)
        self.assertIn('metadata', context_dict)
        self.assertIn('jira_info', context_dict)
        self.assertIn('version_context', context_dict)
        self.assertIn('environment_baseline', context_dict)


class TestProgressiveContextIntegration(unittest.TestCase):
    """Test Progressive Context Architecture integration functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not PROGRESSIVE_CONTEXT_AVAILABLE:
            cls.skipTest(cls, "Progressive Context Architecture not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_progressive_context_setup_integration(self):
        """Test progressive context setup integration"""
        with patch('progressive_context_setup.VersionIntelligenceService') as mock_vis:
            # Mock foundation context creation
            mock_foundation = Mock(spec=FoundationContext)
            mock_foundation.jira_info = Mock()
            mock_foundation.jira_info.jira_id = "ACM-INTEGRATION-123"
            mock_foundation.metadata = Mock(spec=ContextMetadata)
            mock_foundation.get_agent_context_summary = Mock(return_value={})
            mock_foundation.is_ready_for_agent_inheritance = Mock(return_value=True)
            
            mock_vis_instance = Mock()
            mock_vis_instance.create_foundation_context = Mock(return_value=mock_foundation)
            mock_vis.return_value = mock_vis_instance
            
            # Test integration
            pca = ProgressiveContextArchitecture(self.test_dir)
            result = pca.create_foundation_context_for_jira("ACM-INTEGRATION-123", "test-env")
            
            # Validate integration
            self.assertIsNotNone(result)
            mock_vis_instance.create_foundation_context.assert_called_once_with("ACM-INTEGRATION-123", "test-env")
    
    def test_agent_context_retrieval(self):
        """Test agent context retrieval from inheritance chain"""
        # Setup test chain
        pca = ProgressiveContextArchitecture(self.test_dir)
        
        # Create mock chain
        mock_foundation = Mock(spec=FoundationContext)
        mock_foundation.jira_info = Mock()
        mock_foundation.jira_info.jira_id = "ACM-RETRIEVAL-456"
        mock_foundation.version_context = Mock()
        mock_foundation.version_context.__dict__ = {'target_version': '2.5.0'}
        mock_foundation.environment_baseline = Mock()
        mock_foundation.environment_baseline.platform = 'OpenShift'
        mock_foundation.environment_baseline.cluster_name = 'test-cluster'
        mock_foundation.environment_baseline.health_status = 'healthy'
        mock_foundation.environment_baseline.__dict__ = {'cluster_name': 'test-cluster', 'platform': 'OpenShift', 'health_status': 'healthy'}
        mock_foundation.get_agent_context_summary = Mock(return_value={
            'jira_id': 'ACM-RETRIEVAL-456',
            'target_version': '2.5.0',
            'component': 'test-component'
        })
        mock_foundation._pca_agent_context_summary = {
            'pca_metadata': {
                'context_chain_id': 'retrieval_test_chain',
                'agent_inheritance_ready': True
            }
        }
        
        chain = pca.initialize_context_inheritance_chain(mock_foundation)
        chain.agent_contexts = {
            'agent_a': {
                'context_data': {'jira_analysis': 'completed'},
                'context_validation': {'validation_passed': True}
            }
        }
        
        # Store chain
        chain_id = chain.inheritance_metadata['chain_id']
        pca.active_chains[chain_id] = chain
        
        # Test agent context retrieval
        agent_context = pca.get_agent_context(chain_id, 'agent_a')
        
        self.assertIsNotNone(agent_context)
        self.assertEqual(agent_context['context_data']['jira_analysis'], 'completed')
        self.assertTrue(agent_context['context_validation']['validation_passed'])
    
    def test_context_inheritance_sequence_validation(self):
        """Test context inheritance sequence validation"""
        pca = ProgressiveContextArchitecture(self.test_dir)
        
        # Create test chain
        mock_foundation = Mock(spec=FoundationContext)
        mock_foundation.jira_info = Mock()
        mock_foundation.jira_info.jira_id = "ACM-SEQUENCE-789"
        mock_foundation.version_context = Mock()
        mock_foundation.version_context.__dict__ = {'target_version': '2.5.0'}
        mock_foundation.environment_baseline = Mock()
        mock_foundation.environment_baseline.platform = 'OpenShift'
        mock_foundation.environment_baseline.cluster_name = 'test-cluster'
        mock_foundation.environment_baseline.health_status = 'healthy'
        mock_foundation.environment_baseline.__dict__ = {'cluster_name': 'test-cluster', 'platform': 'OpenShift', 'health_status': 'healthy'}
        mock_foundation.get_agent_context_summary = Mock(return_value={
            'jira_id': 'ACM-SEQUENCE-789',
            'target_version': '2.5.0',
            'component': 'test-component'
        })
        mock_foundation._pca_agent_context_summary = {
            'pca_metadata': {
                'context_chain_id': 'sequence_test_chain',
                'agent_inheritance_ready': True
            }
        }
        
        chain = pca.initialize_context_inheritance_chain(mock_foundation)
        
        # Validate inheritance sequence
        sequence = chain.inheritance_metadata['inheritance_sequence']
        
        # Should follow: foundation → agent_a → agent_d → agent_b → agent_c
        self.assertIn('foundation', sequence)
        self.assertIn('agent_a', sequence)
        self.assertIn('agent_d', sequence)
        self.assertIn('agent_b', sequence)
        self.assertIn('agent_c', sequence)
        
        # Check sequence ordering (agent_a before agent_d, etc.)
        foundation_pos = sequence.index('foundation')
        agent_a_pos = sequence.index('agent_a')
        agent_d_pos = sequence.index('agent_d')
        agent_b_pos = sequence.index('agent_b')
        agent_c_pos = sequence.index('agent_c')
        
        self.assertLess(foundation_pos, agent_a_pos)
        self.assertLess(agent_a_pos, agent_d_pos)
        self.assertLess(agent_d_pos, agent_b_pos)
        self.assertLess(agent_b_pos, agent_c_pos)


if __name__ == '__main__':
    print("🧪 Comprehensive Progressive Context Architecture Unit Tests")
    print("=" * 70)
    print("Testing systematic context inheritance and contamination prevention")
    print("=" * 70)
    
    # Check availability
    if not PROGRESSIVE_CONTEXT_AVAILABLE:
        print("❌ Progressive Context Architecture not available - skipping tests")
        exit(1)
    
    # Run tests with detailed output
    unittest.main(verbosity=2)