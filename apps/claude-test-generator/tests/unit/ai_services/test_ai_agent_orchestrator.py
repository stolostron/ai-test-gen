#!/usr/bin/env python3
"""
Unit Tests for AI Agent Orchestrator
Tests hybrid AI-traditional agent orchestration system
"""

import unittest
import os
import sys
import json
import tempfile
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
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
    from ai_agent_orchestrator import (
        AIAgentConfigurationLoader, HybridAIAgentExecutor, PhaseBasedOrchestrator,
        AgentExecutionResult, PhaseExecutionResult, execute_ai_enhanced_framework,
        test_ai_agent_configurations
    )
except ImportError as e:
    print(f"Failed to import AI Agent Orchestrator: {e}")
    print(f"AI Services path: {setup_ai_services_path()}")
    sys.exit(1)


class TestAIAgentConfigurationLoader(unittest.TestCase):
    """Test AI Agent Configuration Loader"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.agents_dir = Path(self.temp_dir) / "agents"
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test YAML configurations
        self._create_test_yaml_configs()
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_test_yaml_configs(self):
        """Create test YAML configuration files"""
        # Agent A configuration
        agent_a_config = """
agent_metadata:
  agent_id: "agent_a_jira_intelligence"
  agent_name: "Agent A - JIRA Intelligence"
  agent_type: "jira_intelligence"
  phase: "Phase 1 - Parallel Foundation Analysis"
  version: "2.0.0-ai-enhanced"

context_inheritance:
  foundation_context_required: true
  context_inheritance_level: "full"
  required_context_fields:
    - "jira_id"
    - "jira_title"
    - "target_version"

ai_capabilities:
  intelligent_analysis:
    - "requirement_extraction"
    - "priority_assessment"

execution_workflow:
  phase_1_foundation:
    - "inherit_foundation_context"
    - "validate_context_completeness"

output_specification:
  analysis_report:
    format: "structured_json"
    sections:
      - "requirement_analysis"
      - "priority_assessment"
"""
        
        # Agent B configuration
        agent_b_config = """
agent_metadata:
  agent_id: "agent_b_documentation_intelligence"
  agent_name: "Agent B - Documentation Intelligence"
  agent_type: "documentation_intelligence"
  phase: "Phase 2 - Parallel Deep Investigation"
  version: "2.0.0-ai-enhanced"

context_inheritance:
  foundation_context_required: true
  context_inheritance_level: "full"
  required_context_fields:
    - "jira_id"
    - "target_version"
    - "component"

ai_capabilities:
  intelligent_discovery:
    - "context_aware_search"
    - "semantic_document_matching"

execution_workflow:
  phase_1_foundation:
    - "inherit_progressive_context"
    - "analyze_agent_a_findings"

output_specification:
  documentation_report:
    format: "structured_json"
    sections:
      - "discovered_documentation"
      - "relevance_analysis"
"""
        
        # Write configuration files
        with open(self.agents_dir / "jira_intelligence_ai.yaml", 'w') as f:
            f.write(agent_a_config)
        
        with open(self.agents_dir / "documentation_ai.yaml", 'w') as f:
            f.write(agent_b_config)
    
    def test_configuration_loading(self):
        """Test loading agent configurations"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # Should load both configurations
        self.assertEqual(len(loader.configurations), 2)
        self.assertIn('agent_a_jira_intelligence', loader.configurations)
        self.assertIn('agent_b_documentation_intelligence', loader.configurations)
    
    def test_get_configuration(self):
        """Test getting specific agent configuration"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        agent_a_config = loader.get_configuration('agent_a_jira_intelligence')
        
        self.assertIsNotNone(agent_a_config)
        self.assertEqual(agent_a_config['agent_metadata']['agent_name'], "Agent A - JIRA Intelligence")
        self.assertEqual(agent_a_config['agent_metadata']['agent_type'], "jira_intelligence")
    
    def test_get_phase_agents(self):
        """Test getting agents by phase"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        phase_1_agents = loader.get_phase_agents("Phase 1 - Parallel Foundation Analysis")
        phase_2_agents = loader.get_phase_agents("Phase 2 - Parallel Deep Investigation")
        
        self.assertEqual(len(phase_1_agents), 1)
        self.assertEqual(len(phase_2_agents), 1)
        self.assertEqual(phase_1_agents[0]['agent_metadata']['agent_id'], 'agent_a_jira_intelligence')
        self.assertEqual(phase_2_agents[0]['agent_metadata']['agent_id'], 'agent_b_documentation_intelligence')
    
    def test_configuration_validation(self):
        """Test configuration validation"""
        loader = AIAgentConfigurationLoader(str(self.agents_dir))
        
        # Should validate successfully
        self.assertTrue(loader.validate_configurations())
    
    def test_invalid_configuration_directory(self):
        """Test handling of invalid configuration directory"""
        with self.assertRaises(FileNotFoundError):
            AIAgentConfigurationLoader("/nonexistent/directory")


class TestAgentExecutionResult(unittest.TestCase):
    """Test Agent Execution Result structure"""
    
    def test_execution_result_creation(self):
        """Test creating agent execution result"""
        result = AgentExecutionResult(
            agent_id="agent_a_jira_intelligence",
            agent_name="Agent A - JIRA Intelligence",
            execution_status="success",
            execution_time=5.5,
            output_file="/path/to/output.json",
            findings={"key": "value"},
            ai_enhancement_used=True,
            confidence_score=0.9
        )
        
        self.assertEqual(result.agent_id, "agent_a_jira_intelligence")
        self.assertEqual(result.agent_name, "Agent A - JIRA Intelligence")
        self.assertEqual(result.execution_status, "success")
        self.assertEqual(result.execution_time, 5.5)
        self.assertEqual(result.output_file, "/path/to/output.json")
        self.assertEqual(result.findings, {"key": "value"})
        self.assertTrue(result.ai_enhancement_used)
        self.assertEqual(result.confidence_score, 0.9)


class TestPhaseExecutionResult(unittest.TestCase):
    """Test Phase Execution Result structure"""
    
    def test_phase_execution_result_creation(self):
        """Test creating phase execution result"""
        agent_results = [
            AgentExecutionResult(
                agent_id="agent_a",
                agent_name="Agent A",
                execution_status="success",
                execution_time=3.0
            ),
            AgentExecutionResult(
                agent_id="agent_b",
                agent_name="Agent B",
                execution_status="success",
                execution_time=4.0
            )
        ]
        
        result = PhaseExecutionResult(
            phase_name="Phase 1",
            agent_results=agent_results,
            phase_success=True,
            total_execution_time=7.0,
            context_updates={"update": "data"}
        )
        
        self.assertEqual(result.phase_name, "Phase 1")
        self.assertEqual(len(result.agent_results), 2)
        self.assertTrue(result.phase_success)
        self.assertEqual(result.total_execution_time, 7.0)
        self.assertEqual(result.context_updates, {"update": "data"})


class TestHybridAIAgentExecutor(unittest.TestCase):
    """Test Hybrid AI Agent Executor"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.agents_dir = Path(self.temp_dir) / "agents"
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test configuration
        self._create_test_config()
        
        # Create mock config loader
        self.config_loader = AIAgentConfigurationLoader(str(self.agents_dir))
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_test_config(self):
        """Create minimal test configuration"""
        test_config = """
agent_metadata:
  agent_id: "test_agent"
  agent_name: "Test Agent"
  agent_type: "test"
  phase: "Test Phase"

context_inheritance:
  foundation_context_required: true

ai_capabilities:
  test_capability:
    - "test_feature"

ai_enhancement_config:
  enhancement_weight: 0.3
  traditional_weight: 0.7
  enhancement_triggers:
    - "complex_requirements"

execution_workflow:
  phase_1_foundation:
    - "test_step"

output_specification:
  test_report:
    format: "json"
"""
        with open(self.agents_dir / "test_agent.yaml", 'w') as f:
            f.write(test_config)
    
    def test_executor_initialization(self):
        """Test hybrid AI agent executor initialization"""
        executor = HybridAIAgentExecutor(self.config_loader)
        
        self.assertIsNotNone(executor.config_loader)
        self.assertIsInstance(executor.ai_models_available, bool)
    
    def test_ai_model_availability_check(self):
        """Test AI model availability checking"""
        executor = HybridAIAgentExecutor(self.config_loader)
        
        # Should check for AI models configuration
        availability = executor._check_ai_model_availability()
        self.assertIsInstance(availability, bool)
    
    def test_ai_enhancement_trigger_logic(self):
        """Test AI enhancement triggering logic"""
        executor = HybridAIAgentExecutor(self.config_loader)
        
        config = self.config_loader.get_configuration('test_agent')
        
        # Test with low confidence (should trigger AI if available)
        foundation_result_low = {'confidence_score': 0.6}
        should_enhance_low = executor._should_apply_ai_enhancement(config, foundation_result_low)
        
        # Test with high confidence (should not trigger AI)
        foundation_result_high = {'confidence_score': 0.95}
        should_enhance_high = executor._should_apply_ai_enhancement(config, foundation_result_high)
        
        # Logic depends on AI availability
        if executor.ai_models_available:
            self.assertTrue(should_enhance_low)
            self.assertFalse(should_enhance_high)
        else:
            self.assertFalse(should_enhance_low)
            self.assertFalse(should_enhance_high)
    
    @patch('jira_api_client.JiraApiClient')
    def test_agent_a_traditional_execution(self, mock_jira_client):
        """Test Agent A traditional execution"""
        # Mock JIRA client
        mock_client_instance = Mock()
        mock_ticket_data = Mock()
        mock_ticket_data.title = "Test Issue"
        mock_ticket_data.component = "TestComponent"
        mock_ticket_data.priority = "High"
        mock_ticket_data.fix_version = "2.15.0"
        mock_client_instance.get_ticket_information.return_value = mock_ticket_data
        mock_jira_client.return_value = mock_client_instance
        
        executor = HybridAIAgentExecutor(self.config_loader)
        
        context = {'jira_id': 'ACM-12345', 'component': 'TestComponent'}
        result = asyncio.run(executor._execute_agent_a_traditional(context, self.temp_dir))
        
        self.assertIsInstance(result, dict)
        self.assertIn('findings', result)
        self.assertIn('output_file', result)
        self.assertIn('confidence_score', result)
        
        # Verify output file was created
        self.assertTrue(os.path.exists(result['output_file']))
    
    def test_agent_b_traditional_execution(self):
        """Test Agent B traditional execution"""
        executor = HybridAIAgentExecutor(self.config_loader)
        
        context = {'component': 'TestComponent', 'target_version': '2.15.0'}
        result = asyncio.run(executor._execute_agent_b_traditional(context, self.temp_dir))
        
        self.assertIsInstance(result, dict)
        self.assertIn('findings', result)
        self.assertIn('output_file', result)
        self.assertEqual(result['execution_method'], 'traditional')
        
        # Verify output file was created
        self.assertTrue(os.path.exists(result['output_file']))
    
    def test_agent_c_traditional_execution(self):
        """Test Agent C traditional execution"""
        executor = HybridAIAgentExecutor(self.config_loader)
        
        context = {'component': 'TestComponent', 'jira_id': 'ACM-12345'}
        result = asyncio.run(executor._execute_agent_c_traditional(context, self.temp_dir))
        
        self.assertIsInstance(result, dict)
        self.assertIn('findings', result)
        self.assertIn('output_file', result)
        self.assertEqual(result['execution_method'], 'traditional')
        
        # Verify output file was created
        self.assertTrue(os.path.exists(result['output_file']))
    
    @patch('environment_assessment_client.EnvironmentAssessmentClient')
    def test_agent_d_traditional_execution(self, mock_env_client):
        """Test Agent D traditional execution"""
        # Mock environment client
        mock_client_instance = Mock()
        mock_env_data = Mock()
        mock_env_data.cluster_name = "test-cluster"
        mock_env_data.version = "2.15.0"
        mock_env_data.platform = "openshift"
        mock_env_data.health_status = "healthy"
        mock_env_data.connectivity_confirmed = True
        mock_env_data.tools_available = {"oc": True, "kubectl": False}
        mock_env_data.detection_method = "oc_assessment"
        mock_client_instance.assess_environment.return_value = mock_env_data
        mock_env_client.return_value = mock_client_instance
        
        executor = HybridAIAgentExecutor(self.config_loader)
        
        context = {'cluster_name': 'test-cluster'}
        result = asyncio.run(executor._execute_agent_d_traditional(context, self.temp_dir))
        
        self.assertIsInstance(result, dict)
        self.assertIn('findings', result)
        self.assertIn('output_file', result)
        self.assertEqual(result['execution_method'], 'traditional')
        
        # Verify output file was created
        self.assertTrue(os.path.exists(result['output_file']))
    
    def test_ai_enhancement_execution(self):
        """Test AI enhancement execution"""
        executor = HybridAIAgentExecutor(self.config_loader)
        
        config = self.config_loader.get_configuration('test_agent')
        foundation_result = {'findings': {'test': 'data'}, 'confidence_score': 0.7}
        
        # Create mock inheritance chain
        mock_inheritance_chain = Mock()
        
        ai_result = asyncio.run(executor._execute_ai_enhancement(
            'test_agent', config, foundation_result, mock_inheritance_chain, self.temp_dir
        ))
        
        self.assertIsInstance(ai_result, dict)
        self.assertIn('ai_insights', ai_result)
        self.assertTrue(ai_result['enhancement_applied'])
    
    def test_results_synthesis(self):
        """Test synthesis of traditional and AI results"""
        executor = HybridAIAgentExecutor(self.config_loader)
        
        config = self.config_loader.get_configuration('test_agent')
        foundation_result = {
            'findings': {'traditional': 'data'},
            'output_file': '/path/to/output.json',
            'confidence_score': 0.8
        }
        ai_enhancement_result = {
            'ai_insights': {
                'enhanced_analysis': True,
                'confidence_boost': 0.1
            }
        }
        
        final_result = executor._synthesize_results(
            'test_agent', config, foundation_result, ai_enhancement_result, self.temp_dir
        )
        
        self.assertIsInstance(final_result, dict)
        self.assertIn('findings', final_result)
        self.assertIn('ai_enhancement', final_result['findings'])
        self.assertEqual(final_result['confidence_score'], 0.9)  # 0.8 + 0.1 boost


class TestPhaseBasedOrchestrator(unittest.TestCase):
    """Test Phase-Based Orchestrator"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.agents_dir = Path(self.temp_dir) / "agents"
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        
        # Create comprehensive test configuration
        self._create_comprehensive_test_configs()
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_comprehensive_test_configs(self):
        """Create comprehensive test configurations for all agents"""
        configs = {
            "jira_intelligence_ai.yaml": {
                "agent_metadata": {
                    "agent_id": "agent_a_jira_intelligence",
                    "agent_name": "Agent A - JIRA Intelligence",
                    "phase": "Phase 1 - Parallel Foundation Analysis"
                },
                "context_inheritance": {"foundation_context_required": True},
                "ai_capabilities": {"test": True},
                "execution_workflow": {"test": True},
                "output_specification": {"test": True}
            },
            "documentation_ai.yaml": {
                "agent_metadata": {
                    "agent_id": "agent_b_documentation_intelligence",
                    "agent_name": "Agent B - Documentation Intelligence",
                    "phase": "Phase 2 - Parallel Deep Investigation"
                },
                "context_inheritance": {"foundation_context_required": True},
                "ai_capabilities": {"test": True},
                "execution_workflow": {"test": True},
                "output_specification": {"test": True}
            },
            "github_investigation_ai.yaml": {
                "agent_metadata": {
                    "agent_id": "agent_c_github_investigation",
                    "agent_name": "Agent C - GitHub Investigation",
                    "phase": "Phase 2 - Parallel Deep Investigation"
                },
                "context_inheritance": {"foundation_context_required": True},
                "ai_capabilities": {"test": True},
                "execution_workflow": {"test": True},
                "output_specification": {"test": True}
            },
            "environment_intelligence_ai.yaml": {
                "agent_metadata": {
                    "agent_id": "agent_d_environment_intelligence",
                    "agent_name": "Agent D - Environment Intelligence",
                    "phase": "Phase 1 - Parallel Foundation Analysis"
                },
                "context_inheritance": {"foundation_context_required": True},
                "ai_capabilities": {"test": True},
                "execution_workflow": {"test": True},
                "output_specification": {"test": True}
            }
        }
        
        import yaml
        for filename, config in configs.items():
            with open(self.agents_dir / filename, 'w') as f:
                yaml.dump(config, f)
    
    @patch('ai_agent_orchestrator.ProgressiveContextArchitecture')
    def test_orchestrator_initialization(self, mock_pca):
        """Test orchestrator initialization"""
        with patch('ai_agent_orchestrator.AIAgentConfigurationLoader') as mock_loader:
            mock_loader.return_value.validate_configurations.return_value = True
            
            orchestrator = PhaseBasedOrchestrator(self.temp_dir)
            
            self.assertIsNotNone(orchestrator.config_loader)
            self.assertIsNotNone(orchestrator.agent_executor)
            self.assertIsNotNone(orchestrator.pca)
    
    def test_execution_summary_generation(self):
        """Test execution summary generation"""
        orchestrator = PhaseBasedOrchestrator(self.temp_dir)
        
        # Create mock execution results
        execution_results = {
            'phases': {
                'phase_1': PhaseExecutionResult(
                    phase_name="Phase 1",
                    agent_results=[
                        AgentExecutionResult(
                            agent_id="agent_a",
                            agent_name="Agent A",
                            execution_status="success",
                            execution_time=3.0,
                            ai_enhancement_used=True
                        ),
                        AgentExecutionResult(
                            agent_id="agent_d",
                            agent_name="Agent D",
                            execution_status="success",
                            execution_time=2.0,
                            ai_enhancement_used=False
                        )
                    ],
                    phase_success=True,
                    total_execution_time=5.0,
                    context_updates={}
                )
            }
        }
        
        summary = orchestrator._generate_execution_summary(execution_results)
        
        self.assertEqual(summary['total_agents'], 2)
        self.assertEqual(summary['successful_agents'], 2)
        self.assertEqual(summary['success_rate'], 1.0)
        self.assertEqual(summary['ai_enhancement_rate'], 0.5)
        self.assertEqual(summary['total_execution_time'], 5.0)
        self.assertEqual(summary['framework_status'], 'success')


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""
    
    def test_ai_agent_configuration_testing(self):
        """Test AI agent configuration testing function"""
        with patch('ai_agent_orchestrator.AIAgentConfigurationLoader') as mock_loader:
            mock_loader.return_value.validate_configurations.return_value = True
            
            result = test_ai_agent_configurations()
            self.assertTrue(result)
            
            mock_loader.return_value.validate_configurations.return_value = False
            result = test_ai_agent_configurations()
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()