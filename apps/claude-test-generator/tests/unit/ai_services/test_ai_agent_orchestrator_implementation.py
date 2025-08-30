#!/usr/bin/env python3
"""
AI Agent Orchestrator Implementation Tests
==========================================

Tests the ACTUAL working functionality of the AI Agent Orchestrator system.
Validates real YAML execution, agent coordination, and output generation.
"""

import unittest
import sys
import os
import json
import asyncio
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ai_services_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services')
sys.path.insert(0, ai_services_path)

try:
    from ai_agent_orchestrator import (
        AIAgentConfigurationLoader, 
        HybridAIAgentExecutor, 
        PhaseBasedOrchestrator,
        AgentExecutionResult,
        PhaseExecutionResult,
        execute_ai_enhanced_framework,
        test_ai_agent_configurations
    )
    AI_ORCHESTRATOR_AVAILABLE = True
except ImportError as e:
    AI_ORCHESTRATOR_AVAILABLE = False
    print(f"❌ AI Orchestrator not available: {e}")


class TestAIAgentConfigurationLoader(unittest.TestCase):
    """Test AI Agent Configuration Loading with real YAML files"""
    
    @classmethod
    def setUpClass(cls):
        if not AI_ORCHESTRATOR_AVAILABLE:
            cls.skipTest(cls, "AI Orchestrator not available")
    
    def setUp(self):
        """Set up test environment with actual agents directory"""
        self.test_dir = tempfile.mkdtemp()
        self.agents_dir = Path(self.test_dir) / "agents"
        self.agents_dir.mkdir(exist_ok=True)
        
        # Copy actual YAML configurations for testing
        actual_agents_dir = Path(os.path.dirname(__file__)) / ".." / ".." / ".." / ".claude" / "ai-services" / "agents"
        if actual_agents_dir.exists():
            for yaml_file in actual_agents_dir.glob("*.yaml"):
                shutil.copy2(yaml_file, self.agents_dir)
        else:
            print(f"❌ Agents directory not found at: {actual_agents_dir.absolute()}")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_yaml_configuration_loading(self):
        """Test that YAML configurations are actually loaded"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # Should load all 4 agent configurations
        self.assertEqual(len(loader.configurations), 4)
        
        # Check required agent IDs are present
        required_agents = [
            "agent_a_jira_intelligence",
            "agent_b_documentation_intelligence", 
            "agent_c_github_investigation",
            "agent_d_environment_intelligence"
        ]
        
        for agent_id in required_agents:
            self.assertIn(agent_id, loader.configurations)
            config = loader.configurations[agent_id]
            
            # Validate configuration structure
            self.assertIn('agent_metadata', config)
            self.assertIn('context_inheritance', config)
            self.assertIn('ai_capabilities', config)
            self.assertIn('execution_workflow', config)
            self.assertIn('output_specification', config)
    
    def test_configuration_validation(self):
        """Test configuration validation works properly"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # All configurations should be valid
        self.assertTrue(loader.validate_configurations())
    
    def test_phase_agent_grouping(self):
        """Test agents are properly grouped by phases"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # Phase 1: Agent A + Agent D
        phase_1_agents = loader.get_phase_agents("Phase 1 - Parallel Foundation Analysis")
        self.assertEqual(len(phase_1_agents), 2)
        
        agent_ids = [agent['agent_metadata']['agent_id'] for agent in phase_1_agents]
        self.assertIn("agent_a_jira_intelligence", agent_ids)
        self.assertIn("agent_d_environment_intelligence", agent_ids)
        
        # Phase 2: Agent B + Agent C
        phase_2_agents = loader.get_phase_agents("Phase 2 - Parallel Deep Investigation")
        self.assertEqual(len(phase_2_agents), 2)
        
        agent_ids = [agent['agent_metadata']['agent_id'] for agent in phase_2_agents]
        self.assertIn("agent_b_documentation_intelligence", agent_ids)
        self.assertIn("agent_c_github_investigation", agent_ids)
    
    def test_get_specific_configuration(self):
        """Test getting specific agent configuration"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # Test Agent A configuration
        agent_a_config = loader.get_configuration("agent_a_jira_intelligence")
        self.assertIsNotNone(agent_a_config)
        
        # Validate Agent A specific fields
        metadata = agent_a_config['agent_metadata']
        self.assertEqual(metadata['agent_name'], "Agent A - JIRA Intelligence")
        self.assertEqual(metadata['agent_type'], "jira_intelligence")
        
        # Test non-existent agent
        invalid_config = loader.get_configuration("agent_invalid")
        self.assertIsNone(invalid_config)


class TestHybridAIAgentExecutor(unittest.TestCase):
    """Test Hybrid AI Agent Executor with real execution"""
    
    @classmethod 
    def setUpClass(cls):
        if not AI_ORCHESTRATOR_AVAILABLE:
            cls.skipTest(cls, "AI Orchestrator not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.agents_dir = Path(self.test_dir) / "agents"
        self.agents_dir.mkdir(exist_ok=True)
        self.run_dir = Path(self.test_dir) / "run"
        self.run_dir.mkdir(exist_ok=True)
        
        # Copy actual YAML configurations
        actual_agents_dir = Path(os.path.dirname(__file__)) / ".." / ".." / ".." / ".claude" / "ai-services" / "agents"
        if actual_agents_dir.exists():
            for yaml_file in actual_agents_dir.glob("*.yaml"):
                shutil.copy2(yaml_file, self.agents_dir)
        
        self.config_loader = AIAgentConfigurationLoader(str(self.agents_dir))
        self.agent_executor = HybridAIAgentExecutor(self.config_loader)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_agent_executor_initialization(self):
        """Test agent executor initializes properly"""
        self.assertIsNotNone(self.agent_executor.config_loader)
        self.assertIsInstance(self.agent_executor.ai_models_available, bool)
    
    def test_ai_model_availability_check(self):
        """Test AI model availability detection"""
        # Should return False since no AI config exists in test environment
        self.assertFalse(self.agent_executor.ai_models_available)
    
    def test_agent_a_execution(self):
        """Test Agent A (JIRA Intelligence) execution"""
        async def test_execution():
            # Create mock inheritance chain
            mock_chain = Mock()
            mock_chain.agent_contexts = {
                'agent_a_jira_intelligence': {
                    'jira_id': 'ACM-TEST-EXEC',
                    'component': 'cluster-curator-controller',
                    'target_version': '2.12.0'
                }
            }
            
            result = await self.agent_executor.execute_agent(
                'agent_a_jira_intelligence',
                mock_chain,
                str(self.run_dir)
            )
            
            # Validate execution result
            self.assertEqual(result.execution_status, "success")
            self.assertEqual(result.agent_id, "agent_a_jira_intelligence")
            self.assertGreater(result.execution_time, 0)
            self.assertIsNotNone(result.output_file)
            self.assertIsNotNone(result.findings)
            
            # Check output file was actually created
            self.assertTrue(os.path.exists(result.output_file))
            
            # Validate output file content
            with open(result.output_file, 'r') as f:
                analysis_data = json.load(f)
            
            self.assertIn('requirement_analysis', analysis_data)
            self.assertIn('dependency_mapping', analysis_data)
            self.assertTrue(analysis_data['traditional_analysis'])
            
            return result
        
        # Run async test
        result = asyncio.run(test_execution())
        self.assertEqual(result.execution_status, "success")
    
    def test_agent_d_execution(self):
        """Test Agent D (Environment Intelligence) execution"""
        async def test_execution():
            # Create mock inheritance chain
            mock_chain = Mock()
            mock_chain.agent_contexts = {
                'agent_d_environment_intelligence': {
                    'cluster_name': 'test-cluster'
                }
            }
            
            result = await self.agent_executor.execute_agent(
                'agent_d_environment_intelligence',
                mock_chain,
                str(self.run_dir)
            )
            
            # Validate execution result
            self.assertEqual(result.execution_status, "success")
            self.assertEqual(result.agent_id, "agent_d_environment_intelligence")
            self.assertIsNotNone(result.output_file)
            
            # Check output file content
            with open(result.output_file, 'r') as f:
                env_data = json.load(f)
            
            self.assertIn('environment_assessment', env_data)
            self.assertIn('tooling_analysis', env_data)
            self.assertTrue(env_data['traditional_assessment'])
            
            return result
        
        # Run async test
        result = asyncio.run(test_execution())
        self.assertEqual(result.execution_status, "success")
    
    def test_ai_enhancement_trigger_logic(self):
        """Test AI enhancement trigger logic"""
        # Create test config and foundation result
        config = {
            'ai_enhancement_config': {
                'enhancement_triggers': ['complex_requirements', 'high_priority_tickets']
            }
        }
        
        # Low confidence should trigger AI enhancement (if models available)
        foundation_result = {'confidence_score': 0.7}
        should_enhance = self.agent_executor._should_apply_ai_enhancement(config, foundation_result)
        
        # Should be False since AI models not available in test environment
        self.assertFalse(should_enhance)
        
        # High confidence should not trigger AI enhancement
        foundation_result_high = {'confidence_score': 0.95}
        should_enhance_high = self.agent_executor._should_apply_ai_enhancement(config, foundation_result_high)
        self.assertFalse(should_enhance_high)
    
    def test_results_synthesis(self):
        """Test traditional and AI results synthesis"""
        config = {
            'ai_enhancement_config': {
                'traditional_weight': 0.7,
                'enhancement_weight': 0.3
            }
        }
        
        foundation_result = {
            'findings': {'analysis': 'traditional_analysis', 'confidence': 0.8},
            'confidence_score': 0.8,
            'output_file': '/test/output.json'
        }
        
        ai_enhancement_result = {
            'ai_insights': {
                'enhanced_analysis': True,
                'confidence_boost': 0.1,
                'additional_findings': ['AI insight 1', 'AI insight 2']
            }
        }
        
        synthesized = self.agent_executor._synthesize_results(
            'agent_a_jira_intelligence',
            config,
            foundation_result,
            ai_enhancement_result,
            str(self.run_dir)
        )
        
        # Check synthesis result
        self.assertIn('ai_enhancement', synthesized['findings'])
        self.assertEqual(synthesized['confidence_score'], 0.9)  # 0.8 + 0.1
        self.assertEqual(synthesized['synthesis_method'], 'weighted_hybrid')


class TestPhaseBasedOrchestrator(unittest.TestCase):
    """Test Phase-Based Orchestrator with real coordination"""
    
    @classmethod
    def setUpClass(cls):
        if not AI_ORCHESTRATOR_AVAILABLE:
            cls.skipTest(cls, "AI Orchestrator not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.agents_dir = Path(self.test_dir) / "agents"
        self.agents_dir.mkdir(exist_ok=True)
        
        # Copy actual YAML configurations
        actual_agents_dir = Path(os.path.dirname(__file__)) / ".." / ".." / ".." / ".claude" / "ai-services" / "agents"
        if actual_agents_dir.exists():
            for yaml_file in actual_agents_dir.glob("*.yaml"):
                shutil.copy2(yaml_file, self.agents_dir)
        
        # Mock the orchestrator to use our test directory
        with patch('ai_agent_orchestrator.AIAgentConfigurationLoader') as mock_loader_class:
            mock_loader = AIAgentConfigurationLoader(str(self.agents_dir))
            mock_loader_class.return_value = mock_loader
            
            # Mock ProgressiveContextArchitecture to avoid complex setup
            with patch('ai_agent_orchestrator.ProgressiveContextArchitecture') as mock_pca:
                mock_pca_instance = Mock()
                mock_pca_instance.create_foundation_context_for_jira.return_value = Mock()
                mock_pca_instance.initialize_context_inheritance_chain.return_value = Mock()
                mock_pca_instance.initialize_context_inheritance_chain.return_value.agent_contexts = {}
                mock_pca.return_value = mock_pca_instance
                
                self.orchestrator = PhaseBasedOrchestrator(str(self.test_dir))
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initializes with all components"""
        self.assertIsNotNone(self.orchestrator.config_loader)
        self.assertIsNotNone(self.orchestrator.agent_executor)
        self.assertIsNotNone(self.orchestrator.pca)
    
    def test_phase_parallel_execution(self):
        """Test parallel execution of agents in a phase"""
        async def test_execution():
            # Mock inheritance chain
            mock_chain = Mock()
            mock_chain.agent_contexts = {
                'agent_a_jira_intelligence': {'jira_id': 'ACM-TEST'},
                'agent_d_environment_intelligence': {'cluster_name': 'test'}
            }
            
            run_dir = os.path.join(self.test_dir, "test_run")
            os.makedirs(run_dir, exist_ok=True)
            
            # Execute Phase 1 (Agent A + Agent D in parallel)
            phase_result = await self.orchestrator._execute_phase_parallel(
                "Phase 1 - Test Parallel Execution",
                ["agent_a_jira_intelligence", "agent_d_environment_intelligence"],
                mock_chain,
                run_dir
            )
            
            # Validate phase execution result
            self.assertIsInstance(phase_result, PhaseExecutionResult)
            self.assertEqual(phase_result.phase_name, "Phase 1 - Test Parallel Execution")
            self.assertEqual(len(phase_result.agent_results), 2)
            self.assertTrue(phase_result.phase_success)
            self.assertGreater(phase_result.total_execution_time, 0)
            
            # Check all agents executed successfully
            for agent_result in phase_result.agent_results:
                self.assertEqual(agent_result.execution_status, "success")
                self.assertIsNotNone(agent_result.output_file)
                self.assertTrue(os.path.exists(agent_result.output_file))
            
            return phase_result
        
        # Run async test
        result = asyncio.run(test_execution())
        self.assertTrue(result.phase_success)
    
    def test_execution_summary_generation(self):
        """Test execution summary generation"""
        # Create mock execution results
        mock_agent_result_1 = AgentExecutionResult(
            agent_id="agent_a_jira_intelligence",
            agent_name="Agent A - JIRA Intelligence",
            execution_status="success",
            execution_time=1.5,
            ai_enhancement_used=False,
            confidence_score=0.8
        )
        
        mock_agent_result_2 = AgentExecutionResult(
            agent_id="agent_d_environment_intelligence",
            agent_name="Agent D - Environment Intelligence", 
            execution_status="success",
            execution_time=2.1,
            ai_enhancement_used=True,
            confidence_score=0.9
        )
        
        mock_phase_result = PhaseExecutionResult(
            phase_name="Test Phase",
            agent_results=[mock_agent_result_1, mock_agent_result_2],
            phase_success=True,
            total_execution_time=3.6,
            context_updates={}
        )
        
        execution_results = {
            'phases': {
                'phase_1': mock_phase_result
            }
        }
        
        summary = self.orchestrator._generate_execution_summary(execution_results)
        
        # Validate summary
        self.assertEqual(summary['total_agents'], 2)
        self.assertEqual(summary['successful_agents'], 2)
        self.assertEqual(summary['success_rate'], 1.0)
        self.assertEqual(summary['ai_enhancement_rate'], 0.5)  # 1 of 2 agents used AI
        self.assertEqual(summary['framework_status'], 'success')


class TestAIOrchestrationIntegration(unittest.TestCase):
    """Test complete AI orchestration integration"""
    
    @classmethod
    def setUpClass(cls):
        if not AI_ORCHESTRATOR_AVAILABLE:
            cls.skipTest(cls, "AI Orchestrator not available")
    
    def setUp(self):
        """Set up integration test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.agents_dir = Path(self.test_dir) / "agents"
        self.agents_dir.mkdir(exist_ok=True)
        
        # Copy actual YAML configurations
        actual_agents_dir = Path(os.path.dirname(__file__)) / ".." / ".." / ".." / ".claude" / "ai-services" / "agents"
        if actual_agents_dir.exists():
            for yaml_file in actual_agents_dir.glob("*.yaml"):
                shutil.copy2(yaml_file, self.agents_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_convenience_function_execution(self):
        """Test convenience function for external use"""
        async def test_execution():
            # Mock the dependencies to avoid full setup
            with patch('ai_agent_orchestrator.PhaseBasedOrchestrator') as mock_orchestrator_class:
                mock_orchestrator = Mock()
                mock_result = {
                    'jira_id': 'ACM-INTEGRATION-TEST',
                    'status': 'success',
                    'summary': {
                        'total_agents': 4,
                        'successful_agents': 4,
                        'success_rate': 1.0,
                        'framework_status': 'success'
                    }
                }
                # Create async mock for the coroutine
                async def mock_async_result(*args, **kwargs):
                    return mock_result
                mock_orchestrator.execute_full_framework = mock_async_result
                mock_orchestrator_class.return_value = mock_orchestrator
                
                # Test the convenience function
                result = await execute_ai_enhanced_framework('ACM-INTEGRATION-TEST', 'test-env')
                
                # Validate result
                self.assertEqual(result['jira_id'], 'ACM-INTEGRATION-TEST')
                self.assertEqual(result['status'], 'success')
                self.assertEqual(result['summary']['framework_status'], 'success')
                
                # Verify orchestrator was called correctly
                # Note: Since we're using an async function instead of Mock.return_value,
                # we validate the result matches expectations instead of call verification
                self.assertIsNotNone(result)
                
                return result
        
        # Run async test
        result = asyncio.run(test_execution())
        self.assertEqual(result['status'], 'success')
    
    def test_configuration_test_function(self):
        """Test configuration testing function"""
        with patch('ai_agent_orchestrator.AIAgentConfigurationLoader') as mock_loader_class:
            mock_loader = Mock()
            mock_loader.validate_configurations.return_value = True
            mock_loader_class.return_value = mock_loader
            
            # Test configuration validation
            result = test_ai_agent_configurations()
            self.assertTrue(result)
            
            # Test with failed validation
            mock_loader.validate_configurations.return_value = False
            result_failed = test_ai_agent_configurations()
            self.assertFalse(result_failed)


if __name__ == '__main__':
    print("🧪 AI Agent Orchestrator Implementation Tests")
    print("=" * 55)
    print("Testing ACTUAL AI orchestration functionality")
    print("=" * 55)
    
    if not AI_ORCHESTRATOR_AVAILABLE:
        print("❌ AI Orchestrator not available - skipping tests")
        exit(1)
    
    unittest.main(verbosity=2)