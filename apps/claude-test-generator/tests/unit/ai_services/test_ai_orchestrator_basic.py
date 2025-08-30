#!/usr/bin/env python3
"""
Basic AI Orchestrator Functionality Test
========================================

Tests that validate the ACTUAL working functionality of the AI orchestrator system.
These tests focus on proving the implementation works in practice.
"""

import unittest
import sys
import os
import json
import asyncio
import tempfile
import shutil
from pathlib import Path

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ai_services_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services')
sys.path.insert(0, ai_services_path)

try:
    from ai_agent_orchestrator import AIAgentConfigurationLoader, HybridAIAgentExecutor
    ORCHESTRATOR_AVAILABLE = True
except ImportError as e:
    ORCHESTRATOR_AVAILABLE = False
    print(f"❌ AI Orchestrator not available: {e}")


class TestBasicAIOrchestrator(unittest.TestCase):
    """Test basic AI orchestrator functionality that actually works"""
    
    @classmethod
    def setUpClass(cls):
        if not ORCHESTRATOR_AVAILABLE:
            cls.skipTest(cls, "AI Orchestrator not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        
        # Create agents directory and copy actual YAML files
        self.agents_dir = Path(self.test_dir) / "agents"
        self.agents_dir.mkdir(exist_ok=True)
        
        # Copy actual agent YAML files
        actual_agents_dir = Path(os.path.dirname(__file__)) / ".." / ".." / ".." / "agents"
        if actual_agents_dir.exists():
            for yaml_file in actual_agents_dir.glob("*.yaml"):
                shutil.copy2(yaml_file, self.agents_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_yaml_configuration_loading_working(self):
        """Test that YAML configuration loading actually works"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # Test that configurations were loaded
        self.assertGreater(len(loader.configurations), 0)
        self.assertEqual(len(loader.configurations), 4)
        
        # Test specific agent configurations
        self.assertIn("agent_a_jira_intelligence", loader.configurations)
        self.assertIn("agent_d_environment_intelligence", loader.configurations)
        
        agent_a_config = loader.configurations["agent_a_jira_intelligence"]
        self.assertEqual(agent_a_config["agent_metadata"]["agent_name"], "Agent A - JIRA Intelligence")
        
        print("✅ YAML Configuration Loading: WORKING")
    
    def test_configuration_validation_working(self):
        """Test that configuration validation actually works"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # All configurations should be valid
        validation_result = loader.validate_configurations()
        self.assertTrue(validation_result)
        
        print("✅ Configuration Validation: WORKING")
    
    def test_agent_executor_initialization_working(self):
        """Test that agent executor initializes and works"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        executor = HybridAIAgentExecutor(loader)
        
        # Test initialization
        self.assertIsNotNone(executor.config_loader)
        self.assertIsInstance(executor.ai_models_available, bool)
        
        print("✅ Agent Executor Initialization: WORKING")
    
    def test_agent_execution_creates_real_files(self):
        """Test that agent execution creates real output files"""
        async def test_execution():
            loader = AIAgentConfigurationLoader(str(self.agents_dir))
            executor = HybridAIAgentExecutor(loader)
            
            # Create test run directory
            run_dir = Path(self.test_dir) / "test_run"
            run_dir.mkdir(exist_ok=True)
            
            # Create mock inheritance chain
            mock_chain = type('MockChain', (), {
                'agent_contexts': {
                    'agent_a_jira_intelligence': {
                        'jira_id': 'ACM-BASIC-TEST',
                        'component': 'cluster-curator-controller',
                        'target_version': '2.12.0'
                    }
                }
            })()
            
            # Execute Agent A
            result = await executor.execute_agent(
                'agent_a_jira_intelligence',
                mock_chain,
                str(run_dir)
            )
            
            # Check execution result
            self.assertEqual(result.execution_status, "success")
            self.assertIsNotNone(result.output_file)
            self.assertIsNotNone(result.findings)
            
            # Check that actual file was created
            self.assertTrue(os.path.exists(result.output_file))
            self.assertGreater(os.path.getsize(result.output_file), 0)
            
            # Check file content
            with open(result.output_file, 'r') as f:
                content = json.load(f)
            
            self.assertIn('requirement_analysis', content)
            self.assertIn('dependency_mapping', content)
            self.assertTrue(content['traditional_analysis'])
            
            return result
        
        # Run the test
        result = asyncio.run(test_execution())
        self.assertEqual(result.execution_status, "success")
        
        print("✅ Agent Execution File Creation: WORKING")
    
    def test_multiple_agent_execution_working(self):
        """Test that multiple agents can be executed"""
        async def test_multiple_execution():
            loader = AIAgentConfigurationLoader(str(self.agents_dir))
            executor = HybridAIAgentExecutor(loader)
            
            run_dir = Path(self.test_dir) / "multi_run"
            run_dir.mkdir(exist_ok=True)
            
            # Create mock inheritance chain
            mock_chain = type('MockChain', (), {
                'agent_contexts': {
                    'agent_a_jira_intelligence': {
                        'jira_id': 'ACM-MULTI-TEST',
                        'component': 'cluster-curator-controller'
                    },
                    'agent_d_environment_intelligence': {
                        'cluster_name': 'test-cluster'
                    }
                }
            })()
            
            # Execute both Agent A and Agent D
            agents_to_test = [
                'agent_a_jira_intelligence',
                'agent_d_environment_intelligence'
            ]
            
            results = []
            for agent_id in agents_to_test:
                result = await executor.execute_agent(agent_id, mock_chain, str(run_dir))
                results.append(result)
            
            # Check all executions succeeded
            for i, result in enumerate(results):
                self.assertEqual(result.execution_status, "success", 
                               f"Agent {agents_to_test[i]} failed")
                self.assertIsNotNone(result.output_file)
                self.assertTrue(os.path.exists(result.output_file))
            
            # Check different agents created different files
            output_files = [result.output_file for result in results]
            self.assertEqual(len(set(output_files)), len(output_files))  # All unique
            
            return results
        
        # Run the test
        results = asyncio.run(test_multiple_execution())
        self.assertEqual(len(results), 2)
        
        print("✅ Multiple Agent Execution: WORKING")
    
    def test_phase_agent_grouping_working(self):
        """Test that phase-based agent grouping works"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # Test Phase 1 grouping
        phase_1_agents = loader.get_phase_agents("Phase 1 - Parallel Foundation Analysis")
        self.assertEqual(len(phase_1_agents), 2)
        
        phase_1_ids = [agent['agent_metadata']['agent_id'] for agent in phase_1_agents]
        self.assertIn("agent_a_jira_intelligence", phase_1_ids)
        self.assertIn("agent_d_environment_intelligence", phase_1_ids)
        
        # Test Phase 2 grouping
        phase_2_agents = loader.get_phase_agents("Phase 2 - Parallel Deep Investigation")
        self.assertEqual(len(phase_2_agents), 2)
        
        phase_2_ids = [agent['agent_metadata']['agent_id'] for agent in phase_2_agents]
        self.assertIn("agent_b_documentation_intelligence", phase_2_ids)
        self.assertIn("agent_c_github_investigation", phase_2_ids)
        
        print("✅ Phase Agent Grouping: WORKING")


if __name__ == '__main__':
    print("🧪 Basic AI Orchestrator Functionality Test")
    print("=" * 50)
    print("Testing ACTUAL working implementation")
    print("=" * 50)
    
    if not ORCHESTRATOR_AVAILABLE:
        print("❌ AI Orchestrator not available - cannot test")
        exit(1)
    
    unittest.main(verbosity=2)