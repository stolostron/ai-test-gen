#!/usr/bin/env python3
"""
Direct AI Orchestrator Functionality Test
=========================================

Tests the AI orchestrator using the actual agents directory directly.
"""

import unittest
import sys
import os
import json
import asyncio
import tempfile
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


class TestDirectAIOrchestrator(unittest.TestCase):
    """Test AI orchestrator using actual agents directory"""
    
    @classmethod
    def setUpClass(cls):
        if not ORCHESTRATOR_AVAILABLE:
            cls.skipTest(cls, "AI Orchestrator not available")
    
    def setUp(self):
        """Set up test environment with actual agents directory"""
        # Use the actual agents directory from the project
        project_root = Path(os.path.dirname(__file__)) / ".." / ".." / ".."
        self.agents_dir = project_root / "agents"
        
        if not self.agents_dir.exists():
            self.skipTest(f"Agents directory not found: {self.agents_dir}")
    
    def test_actual_yaml_loading(self):
        """Test loading actual YAML configurations from project"""
        print(f"🎯 Using agents directory: {self.agents_dir}")
        
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        print(f"📋 Loaded {len(loader.configurations)} configurations")
        for agent_id in loader.configurations.keys():
            print(f"   - {agent_id}")
        
        # Should load 4 configurations
        self.assertEqual(len(loader.configurations), 4)
        
        # Check specific configurations exist
        required_agents = [
            "agent_a_jira_intelligence",
            "agent_b_documentation_intelligence",
            "agent_c_github_investigation", 
            "agent_d_environment_intelligence"
        ]
        
        for agent_id in required_agents:
            self.assertIn(agent_id, loader.configurations)
            config = loader.configurations[agent_id]
            self.assertIn('agent_metadata', config)
            
        print("✅ Actual YAML Loading: WORKING")
    
    def test_actual_validation(self):
        """Test configuration validation with actual files"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        validation_result = loader.validate_configurations()
        self.assertTrue(validation_result)
        
        print("✅ Actual Configuration Validation: WORKING")
    
    def test_actual_phase_grouping(self):
        """Test phase grouping with actual configurations"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # Test Phase 1
        phase_1_agents = loader.get_phase_agents("Phase 1 - Parallel Foundation Analysis")
        print(f"Phase 1 agents found: {len(phase_1_agents)}")
        for agent in phase_1_agents:
            print(f"   - {agent['agent_metadata']['agent_name']}")
        
        self.assertEqual(len(phase_1_agents), 2)
        
        # Test Phase 2
        phase_2_agents = loader.get_phase_agents("Phase 2 - Parallel Deep Investigation")
        print(f"Phase 2 agents found: {len(phase_2_agents)}")
        for agent in phase_2_agents:
            print(f"   - {agent['agent_metadata']['agent_name']}")
        
        self.assertEqual(len(phase_2_agents), 2)
        
        print("✅ Actual Phase Grouping: WORKING")
    
    def test_actual_agent_execution(self):
        """Test actual agent execution with real configurations"""
        async def test_execution():
            loader = AIAgentConfigurationLoader(str(self.agents_dir))
            executor = HybridAIAgentExecutor(loader)
            
            # Create temporary run directory
            with tempfile.TemporaryDirectory() as temp_dir:
                run_dir = Path(temp_dir) / "test_run"
                run_dir.mkdir(exist_ok=True)
                
                # Create mock inheritance chain
                mock_chain = type('MockChain', (), {
                    'agent_contexts': {
                        'agent_a_jira_intelligence': {
                            'jira_id': 'ACM-DIRECT-TEST',
                            'component': 'cluster-curator-controller',
                            'target_version': '2.12.0'
                        }
                    }
                })()
                
                print("🔄 Executing Agent A with actual configuration...")
                
                # Execute Agent A
                result = await executor.execute_agent(
                    'agent_a_jira_intelligence',
                    mock_chain,
                    str(run_dir)
                )
                
                print(f"   Status: {result.execution_status}")
                print(f"   Agent: {result.agent_name}")
                print(f"   Execution time: {result.execution_time:.3f}s")
                print(f"   Output file: {result.output_file}")
                print(f"   AI enhancement: {result.ai_enhancement_used}")
                
                # Validate result
                self.assertEqual(result.execution_status, "success")
                self.assertIsNotNone(result.output_file)
                
                # Check file was created
                if result.output_file:
                    self.assertTrue(os.path.exists(result.output_file))
                    
                    # Check content
                    with open(result.output_file, 'r') as f:
                        content = json.load(f)
                    
                    print(f"   Content keys: {list(content.keys())}")
                    self.assertIn('requirement_analysis', content)
                    self.assertIn('dependency_mapping', content)
                
                return result
        
        # Run the test
        result = asyncio.run(test_execution())
        self.assertEqual(result.execution_status, "success")
        
        print("✅ Actual Agent Execution: WORKING")


if __name__ == '__main__':
    print("🧪 Direct AI Orchestrator Functionality Test")
    print("=" * 50)
    print("Testing with ACTUAL agents directory")
    print("=" * 50)
    
    if not ORCHESTRATOR_AVAILABLE:
        print("❌ AI Orchestrator not available - cannot test")
        exit(1)
    
    unittest.main(verbosity=2)