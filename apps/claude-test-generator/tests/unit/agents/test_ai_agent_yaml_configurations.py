#!/usr/bin/env python3
"""
Unit Tests for AI Agent YAML Configurations
Tests validation and structure of agent configuration files
"""

import unittest
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List

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


class TestYAMLConfigurationBase(unittest.TestCase):
    """Base test class for YAML configuration validation"""
    
    def setUp(self):
        """Set up test environment"""
        self.agents_dir = Path(os.path.dirname(__file__)).parent.parent.parent / ".claude" / "ai-services" / "agents"
        
        # Expected agent files
        self.agent_files = {
            'jira_intelligence_ai.yaml': 'agent_a_jira_intelligence',
            'documentation_ai.yaml': 'agent_b_documentation_intelligence', 
            'github_investigation_ai.yaml': 'agent_c_github_investigation',
            'environment_intelligence_ai.yaml': 'agent_d_environment_intelligence'
        }
    
    def load_agent_config(self, filename: str) -> Dict[str, Any]:
        """Load agent configuration from YAML file"""
        file_path = self.agents_dir / filename
        self.assertTrue(file_path.exists(), f"Agent config file not found: {filename}")
        
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    def validate_required_sections(self, config: Dict[str, Any], expected_sections: List[str]):
        """Validate that all required sections are present"""
        for section in expected_sections:
            self.assertIn(section, config, f"Missing required section: {section}")
    
    def validate_agent_metadata(self, metadata: Dict[str, Any], expected_agent_id: str):
        """Validate agent metadata structure"""
        required_fields = [
            'agent_id', 'agent_name', 'agent_type', 'phase', 
            'version', 'ai_enhancement_level'
        ]
        
        for field in required_fields:
            self.assertIn(field, metadata, f"Missing metadata field: {field}")
            self.assertIsNotNone(metadata[field], f"Metadata field {field} is None")
        
        # Validate specific values
        self.assertEqual(metadata['agent_id'], expected_agent_id)
        self.assertIn('Agent', metadata['agent_name'])
        self.assertIn('2.0.0', metadata['version'])
        self.assertEqual(metadata['ai_enhancement_level'], 'strategic')
    
    def validate_context_inheritance(self, context_config: Dict[str, Any]):
        """Validate context inheritance configuration"""
        required_fields = [
            'foundation_context_required', 'context_inheritance_level',
            'required_context_fields', 'context_validation_required',
            'context_enrichment_enabled'
        ]
        
        for field in required_fields:
            self.assertIn(field, context_config, f"Missing context inheritance field: {field}")
        
        # Validate boolean values
        self.assertIsInstance(context_config['foundation_context_required'], bool)
        self.assertIsInstance(context_config['context_validation_required'], bool)
        self.assertIsInstance(context_config['context_enrichment_enabled'], bool)
        
        # Validate inheritance level
        valid_levels = ['full', 'partial', 'minimal']
        self.assertIn(context_config['context_inheritance_level'], valid_levels)
        
        # Validate required context fields
        required_context_fields = context_config['required_context_fields']
        self.assertIsInstance(required_context_fields, list)
        self.assertGreater(len(required_context_fields), 0)
        
        # All agents should require jira_id
        self.assertIn('jira_id', required_context_fields)
    
    def validate_ai_capabilities(self, ai_config: Dict[str, Any]):
        """Validate AI capabilities configuration"""
        # Should have at least one capability category
        self.assertGreater(len(ai_config), 0)
        
        # All capability categories should be lists
        for capability_name, capabilities in ai_config.items():
            self.assertIsInstance(capabilities, list, 
                               f"AI capability {capability_name} should be a list")
            self.assertGreater(len(capabilities), 0,
                             f"AI capability {capability_name} should not be empty")
    
    def validate_ai_enhancement_config(self, enhancement_config: Dict[str, Any]):
        """Validate AI enhancement configuration"""
        required_fields = [
            'enhancement_weight', 'traditional_weight', 
            'enhancement_triggers', 'ai_models'
        ]
        
        for field in required_fields:
            self.assertIn(field, enhancement_config, f"Missing enhancement config field: {field}")
        
        # Validate weights
        enhancement_weight = enhancement_config['enhancement_weight']
        traditional_weight = enhancement_config['traditional_weight']
        
        self.assertIsInstance(enhancement_weight, (int, float))
        self.assertIsInstance(traditional_weight, (int, float))
        self.assertAlmostEqual(enhancement_weight + traditional_weight, 1.0, places=1)
        
        # Validate enhancement triggers
        triggers = enhancement_config['enhancement_triggers']
        self.assertIsInstance(triggers, list)
        self.assertGreater(len(triggers), 0)
        
        # Validate AI models
        ai_models = enhancement_config['ai_models']
        self.assertIsInstance(ai_models, dict)
        self.assertGreater(len(ai_models), 0)
        
        # Validate each AI model configuration
        for model_name, model_config in ai_models.items():
            self.validate_ai_model_config(model_config, model_name)
    
    def validate_ai_model_config(self, model_config: Dict[str, Any], model_name: str):
        """Validate individual AI model configuration"""
        required_fields = [
            'model_type', 'context_window', 'temperature', 
            'max_tokens', 'system_prompt'
        ]
        
        for field in required_fields:
            self.assertIn(field, model_config, 
                         f"Missing AI model field {field} in {model_name}")
        
        # Validate model type
        self.assertEqual(model_config['model_type'], 'llm')
        
        # Validate numeric parameters
        self.assertIsInstance(model_config['context_window'], int)
        self.assertGreater(model_config['context_window'], 0)
        
        self.assertIsInstance(model_config['temperature'], (int, float))
        self.assertGreaterEqual(model_config['temperature'], 0.0)
        self.assertLessEqual(model_config['temperature'], 2.0)
        
        self.assertIsInstance(model_config['max_tokens'], int)
        self.assertGreater(model_config['max_tokens'], 0)
        
        # Validate system prompt
        self.assertIsInstance(model_config['system_prompt'], str)
        self.assertGreater(len(model_config['system_prompt'].strip()), 50)
    
    def validate_execution_workflow(self, workflow: Dict[str, Any]):
        """Validate execution workflow configuration"""
        # Should have multiple phases
        self.assertGreater(len(workflow), 0)
        
        # All phases should be lists of steps
        for phase_name, steps in workflow.items():
            self.assertIsInstance(steps, list, f"Workflow phase {phase_name} should be a list")
            self.assertGreater(len(steps), 0, f"Workflow phase {phase_name} should not be empty")
            
            # All steps should be strings
            for step in steps:
                self.assertIsInstance(step, str, f"Workflow step should be string in {phase_name}")
    
    def validate_output_specification(self, output_spec: Dict[str, Any]):
        """Validate output specification"""
        required_sections = ['context_updates', 'inheritance_data']
        
        for section in required_sections:
            self.assertIn(section, output_spec, f"Missing output spec section: {section}")
        
        # Validate context updates
        context_updates = output_spec['context_updates']
        self.assertIsInstance(context_updates, list)
        self.assertGreater(len(context_updates), 0)
        
        # Validate inheritance data
        inheritance_data = output_spec['inheritance_data']
        self.assertIsInstance(inheritance_data, dict)
        self.assertGreater(len(inheritance_data), 0)
    
    def validate_quality_assurance(self, qa_config: Dict[str, Any]):
        """Validate quality assurance configuration"""
        required_sections = ['validation_checks']
        
        for section in required_sections:
            self.assertIn(section, qa_config, f"Missing QA section: {section}")
        
        # Validate validation checks
        validation_checks = qa_config['validation_checks']
        self.assertIsInstance(validation_checks, list)
        self.assertGreater(len(validation_checks), 0)
    
    def validate_deployment_metadata(self, deployment: Dict[str, Any]):
        """Validate deployment metadata"""
        required_fields = [
            'deployment_mode', 'resource_requirements', 
            'dependencies', 'configuration_files'
        ]
        
        for field in required_fields:
            self.assertIn(field, deployment, f"Missing deployment field: {field}")
        
        # Validate deployment mode
        self.assertEqual(deployment['deployment_mode'], 'hybrid_ai_traditional')
        
        # Validate resource requirements
        resources = deployment['resource_requirements']
        self.assertIn('cpu_cores', resources)
        self.assertIn('memory_gb', resources)
        self.assertIsInstance(resources['cpu_cores'], int)
        self.assertIsInstance(resources['memory_gb'], int)
        
        # Validate dependencies
        dependencies = deployment['dependencies']
        self.assertIsInstance(dependencies, list)
        self.assertGreater(len(dependencies), 0)
        
        # Validate configuration files
        config_files = deployment['configuration_files']
        self.assertIsInstance(config_files, list)
        self.assertGreater(len(config_files), 0)


class TestJiraIntelligenceAgent(TestYAMLConfigurationBase):
    """Test Agent A - JIRA Intelligence configuration"""
    
    def setUp(self):
        super().setUp()
        self.config = self.load_agent_config('jira_intelligence_ai.yaml')
    
    def test_jira_agent_file_exists(self):
        """Test that JIRA intelligence agent YAML file exists"""
        file_path = self.agents_dir / 'jira_intelligence_ai.yaml'
        self.assertTrue(file_path.exists())
    
    def test_jira_agent_basic_structure(self):
        """Test basic YAML structure for JIRA agent"""
        expected_sections = [
            'agent_metadata', 'context_inheritance', 'ai_capabilities',
            'traditional_foundation', 'ai_enhancement_config', 'execution_workflow',
            'output_specification', 'quality_assurance', 'integration_points',
            'monitoring_config', 'deployment_metadata'
        ]
        
        self.validate_required_sections(self.config, expected_sections)
    
    def test_jira_agent_metadata(self):
        """Test JIRA agent metadata validation"""
        metadata = self.config['agent_metadata']
        self.validate_agent_metadata(metadata, 'agent_a_jira_intelligence')
        
        # JIRA-specific validations
        self.assertEqual(metadata['agent_type'], 'jira_intelligence')
        self.assertIn('JIRA Intelligence', metadata['agent_name'])
    
    def test_jira_context_inheritance(self):
        """Test JIRA agent context inheritance configuration"""
        context_config = self.config['context_inheritance']
        self.validate_context_inheritance(context_config)
        
        # JIRA-specific context fields
        required_fields = context_config['required_context_fields']
        jira_specific_fields = ['jira_title', 'jira_status', 'priority', 'component']
        
        for field in jira_specific_fields:
            self.assertIn(field, required_fields, f"JIRA agent missing field: {field}")
    
    def test_jira_ai_capabilities(self):
        """Test JIRA agent AI capabilities"""
        ai_capabilities = self.config['ai_capabilities']
        self.validate_ai_capabilities(ai_capabilities)
        
        # Expected JIRA capability categories
        expected_categories = ['intelligent_analysis', 'nlp_processing', 'knowledge_integration']
        
        for category in expected_categories:
            self.assertIn(category, ai_capabilities, f"Missing JIRA capability: {category}")
    
    def test_jira_traditional_foundation(self):
        """Test JIRA agent traditional foundation integration"""
        foundation = self.config['traditional_foundation']
        
        self.assertEqual(foundation['base_service'], 'JiraApiClient')
        self.assertEqual(foundation['foundation_service'], 'VersionIntelligenceService')
        self.assertIn('jira_info', foundation['data_source'])
    
    def test_jira_ai_enhancement_config(self):
        """Test JIRA agent AI enhancement configuration"""
        enhancement_config = self.config['ai_enhancement_config']
        self.validate_ai_enhancement_config(enhancement_config)
        
        # Should have requirement extractor and priority analyzer
        ai_models = enhancement_config['ai_models']
        self.assertIn('requirement_extractor', ai_models)
        self.assertIn('priority_analyzer', ai_models)
    
    def test_jira_execution_workflow(self):
        """Test JIRA agent execution workflow"""
        workflow = self.config['execution_workflow']
        self.validate_execution_workflow(workflow)
        
        # Should have foundation, analysis, synthesis, and output phases
        expected_phases = ['phase_1_foundation', 'phase_2_ai_analysis', 'phase_3_synthesis', 'phase_4_output']
        
        for phase in expected_phases:
            self.assertIn(phase, workflow, f"Missing JIRA workflow phase: {phase}")
    
    def test_jira_output_specification(self):
        """Test JIRA agent output specification"""
        output_spec = self.config['output_specification']
        self.validate_output_specification(output_spec)
        
        # Should have analysis report
        self.assertIn('analysis_report', output_spec)
        
        # Should provide data for other agents
        inheritance_data = output_spec['inheritance_data']
        expected_agents = ['for_agent_b', 'for_agent_c', 'for_agent_d']
        
        for agent in expected_agents:
            self.assertIn(agent, inheritance_data, f"Missing inheritance data for: {agent}")


class TestEnvironmentIntelligenceAgent(TestYAMLConfigurationBase):
    """Test Agent D - Environment Intelligence configuration"""
    
    def setUp(self):
        super().setUp()
        self.config = self.load_agent_config('environment_intelligence_ai.yaml')
    
    def test_environment_agent_file_exists(self):
        """Test that environment intelligence agent YAML file exists"""
        file_path = self.agents_dir / 'environment_intelligence_ai.yaml'
        self.assertTrue(file_path.exists())
    
    def test_environment_agent_basic_structure(self):
        """Test basic YAML structure for environment agent"""
        expected_sections = [
            'agent_metadata', 'context_inheritance', 'ai_capabilities',
            'traditional_foundation', 'ai_enhancement_config', 'execution_workflow',
            'environment_assessment', 'tooling_intelligence', 'output_specification',
            'quality_assurance', 'integration_points', 'monitoring_config',
            'advanced_features', 'security_considerations', 'deployment_metadata',
            'execution_coordination'
        ]
        
        self.validate_required_sections(self.config, expected_sections)
    
    def test_environment_agent_metadata(self):
        """Test environment agent metadata validation"""
        metadata = self.config['agent_metadata']
        self.validate_agent_metadata(metadata, 'agent_d_environment_intelligence')
        
        # Environment-specific validations
        self.assertEqual(metadata['agent_type'], 'environment_intelligence')
        self.assertIn('Environment Intelligence', metadata['agent_name'])
    
    def test_environment_context_inheritance(self):
        """Test environment agent context inheritance configuration"""
        context_config = self.config['context_inheritance']
        self.validate_context_inheritance(context_config)
        
        # Environment-specific context fields
        required_fields = context_config['required_context_fields']
        env_specific_fields = ['environment_version', 'cluster_name', 'platform', 'health_status']
        
        for field in env_specific_fields:
            self.assertIn(field, required_fields, f"Environment agent missing field: {field}")
        
        # Should have parallel execution defined
        self.assertIn('parallel_execution', context_config)
        self.assertEqual(context_config['parallel_execution'], 'agent_a_jira_intelligence')
    
    def test_environment_ai_capabilities(self):
        """Test environment agent AI capabilities"""
        ai_capabilities = self.config['ai_capabilities']
        self.validate_ai_capabilities(ai_capabilities)
        
        # Expected environment capability categories
        expected_categories = ['intelligent_assessment', 'tooling_intelligence', 'predictive_analysis']
        
        for category in expected_categories:
            self.assertIn(category, ai_capabilities, f"Missing environment capability: {category}")
    
    def test_environment_assessment_section(self):
        """Test environment assessment configuration"""
        env_assessment = self.config['environment_assessment']
        
        # Should have connectivity, platform, and resource assessment
        expected_sections = ['connectivity_checks', 'platform_analysis', 'resource_assessment']
        
        for section in expected_sections:
            self.assertIn(section, env_assessment, f"Missing assessment section: {section}")
    
    def test_tooling_intelligence_section(self):
        """Test tooling intelligence configuration"""
        tooling = self.config['tooling_intelligence']
        
        # Should have tool mapping and framework discovery
        expected_sections = ['cli_tool_mapping', 'test_framework_discovery']
        
        for section in expected_sections:
            self.assertIn(section, tooling, f"Missing tooling section: {section}")
        
        # Should have primary tools defined
        cli_tools = tooling['cli_tool_mapping']['primary_tools']
        expected_tools = ['oc', 'kubectl', 'curl']
        
        for tool in expected_tools:
            self.assertIn(tool, cli_tools, f"Missing CLI tool: {tool}")
    
    def test_environment_execution_coordination(self):
        """Test environment agent execution coordination"""
        coordination = self.config['execution_coordination']
        
        required_fields = ['coordination_strategy', 'timing_optimization']
        
        for field in required_fields:
            self.assertIn(field, coordination, f"Missing coordination field: {field}")
        
        # Validate coordination strategy
        strategy = coordination['coordination_strategy']
        self.assertEqual(strategy['parallel_start'], 'agent_a_jira_intelligence')
        self.assertTrue(strategy['independent_execution'])
    
    def test_environment_security_considerations(self):
        """Test environment agent security configuration"""
        security = self.config['security_considerations']
        
        expected_sections = ['cluster_access', 'environment_safety']
        
        for section in expected_sections:
            self.assertIn(section, security, f"Missing security section: {section}")
        
        # Validate safety settings
        safety = security['environment_safety']
        self.assertTrue(safety['no_destructive_operations'])
        self.assertTrue(safety['read_only_assessment'])


class TestDocumentationIntelligenceAgent(TestYAMLConfigurationBase):
    """Test Agent B - Documentation Intelligence configuration"""
    
    def setUp(self):
        super().setUp()
        self.config = self.load_agent_config('documentation_ai.yaml')
    
    def test_documentation_agent_file_exists(self):
        """Test that documentation intelligence agent YAML file exists"""
        file_path = self.agents_dir / 'documentation_ai.yaml'
        self.assertTrue(file_path.exists())
    
    def test_documentation_agent_yaml_valid(self):
        """Test that documentation agent YAML is valid"""
        # Should load without errors
        self.assertIsInstance(self.config, dict)
        self.assertGreater(len(self.config), 0)
    
    def test_documentation_agent_metadata(self):
        """Test documentation agent metadata"""
        self.assertIn('agent_metadata', self.config)
        metadata = self.config['agent_metadata']
        
        # Validate basic structure without strict validation
        # since we don't have the full content
        self.assertIn('agent_id', metadata)
        self.assertIn('agent_name', metadata)


class TestGitHubInvestigationAgent(TestYAMLConfigurationBase):
    """Test Agent C - GitHub Investigation configuration"""
    
    def setUp(self):
        super().setUp()
        self.config = self.load_agent_config('github_investigation_ai.yaml')
    
    def test_github_agent_file_exists(self):
        """Test that GitHub investigation agent YAML file exists"""
        file_path = self.agents_dir / 'github_investigation_ai.yaml'
        self.assertTrue(file_path.exists())
    
    def test_github_agent_yaml_valid(self):
        """Test that GitHub agent YAML is valid"""
        # Should load without errors
        self.assertIsInstance(self.config, dict)
        self.assertGreater(len(self.config), 0)
    
    def test_github_agent_metadata(self):
        """Test GitHub agent metadata"""
        self.assertIn('agent_metadata', self.config)
        metadata = self.config['agent_metadata']
        
        # Validate basic structure
        self.assertIn('agent_id', metadata)
        self.assertIn('agent_name', metadata)


class TestAIAgentYAMLConfigurationIntegration(TestYAMLConfigurationBase):
    """Test integration and consistency across all agent configurations"""
    
    def setUp(self):
        super().setUp()
        self.all_configs = {}
        
        # Load all agent configurations
        for filename, agent_id in self.agent_files.items():
            try:
                self.all_configs[agent_id] = self.load_agent_config(filename)
            except Exception as e:
                # Store error for individual test validation
                self.all_configs[agent_id] = {'error': str(e)}
    
    def test_all_agent_files_exist(self):
        """Test that all expected agent YAML files exist"""
        for filename in self.agent_files.keys():
            file_path = self.agents_dir / filename
            self.assertTrue(file_path.exists(), f"Missing agent file: {filename}")
    
    def test_all_agent_configs_loadable(self):
        """Test that all agent configurations are valid YAML"""
        for agent_id, config in self.all_configs.items():
            self.assertNotIn('error', config, f"Failed to load {agent_id}: {config.get('error', 'Unknown error')}")
            self.assertIsInstance(config, dict, f"Config for {agent_id} is not a dictionary")
    
    def test_consistent_agent_metadata_structure(self):
        """Test that all agents have consistent metadata structure"""
        required_metadata_fields = [
            'agent_id', 'agent_name', 'agent_type', 'phase', 'version', 'ai_enhancement_level'
        ]
        
        for agent_id, config in self.all_configs.items():
            if 'error' in config:
                continue  # Skip failed configs
                
            self.assertIn('agent_metadata', config, f"Missing agent_metadata in {agent_id}")
            metadata = config['agent_metadata']
            
            for field in required_metadata_fields:
                self.assertIn(field, metadata, f"Missing metadata field {field} in {agent_id}")
    
    def test_consistent_ai_enhancement_levels(self):
        """Test that all agents have consistent AI enhancement levels"""
        for agent_id, config in self.all_configs.items():
            if 'error' in config:
                continue
                
            metadata = config.get('agent_metadata', {})
            if 'ai_enhancement_level' in metadata:
                self.assertEqual(metadata['ai_enhancement_level'], 'strategic',
                               f"Inconsistent AI enhancement level in {agent_id}")
    
    def test_consistent_deployment_modes(self):
        """Test that all agents have consistent deployment modes"""
        for agent_id, config in self.all_configs.items():
            if 'error' in config:
                continue
                
            deployment = config.get('deployment_metadata', {})
            if 'deployment_mode' in deployment:
                self.assertEqual(deployment['deployment_mode'], 'hybrid_ai_traditional',
                               f"Inconsistent deployment mode in {agent_id}")
    
    def test_context_inheritance_consistency(self):
        """Test that context inheritance configurations are consistent"""
        for agent_id, config in self.all_configs.items():
            if 'error' in config:
                continue
                
            context_config = config.get('context_inheritance', {})
            
            if 'foundation_context_required' in context_config:
                self.assertTrue(context_config['foundation_context_required'],
                              f"Foundation context should be required for {agent_id}")
            
            if 'context_inheritance_level' in context_config:
                self.assertEqual(context_config['context_inheritance_level'], 'full',
                               f"All agents should have full context inheritance: {agent_id}")
    
    def test_ai_enhancement_weight_consistency(self):
        """Test that AI enhancement weights are consistent across agents"""
        expected_ai_weight = 0.3
        expected_traditional_weight = 0.7
        
        for agent_id, config in self.all_configs.items():
            if 'error' in config:
                continue
                
            enhancement_config = config.get('ai_enhancement_config', {})
            
            if 'enhancement_weight' in enhancement_config:
                self.assertAlmostEqual(enhancement_config['enhancement_weight'], expected_ai_weight, places=1,
                                     msg=f"Inconsistent AI enhancement weight in {agent_id}")
            
            if 'traditional_weight' in enhancement_config:
                self.assertAlmostEqual(enhancement_config['traditional_weight'], expected_traditional_weight, places=1,
                                     msg=f"Inconsistent traditional weight in {agent_id}")
    
    def test_progressive_context_architecture_integration(self):
        """Test that all agents properly integrate with Progressive Context Architecture"""
        for agent_id, config in self.all_configs.items():
            if 'error' in config:
                continue
                
            # Should have context inheritance configuration
            self.assertIn('context_inheritance', config, f"Missing context inheritance in {agent_id}")
            
            # Should have integration points
            integration_points = config.get('integration_points', {})
            if 'progressive_context' in integration_points:
                pca_config = integration_points['progressive_context']
                self.assertIn('update_method', pca_config, f"Missing PCA update method in {agent_id}")
    
    def test_quality_assurance_presence(self):
        """Test that all agents have quality assurance configurations"""
        for agent_id, config in self.all_configs.items():
            if 'error' in config:
                continue
                
            self.assertIn('quality_assurance', config, f"Missing quality assurance in {agent_id}")
            qa_config = config['quality_assurance']
            self.assertIn('validation_checks', qa_config, f"Missing validation checks in {agent_id}")
    
    def test_monitoring_configuration_presence(self):
        """Test that all agents have monitoring configurations"""
        for agent_id, config in self.all_configs.items():
            if 'error' in config:
                continue
                
            self.assertIn('monitoring_config', config, f"Missing monitoring config in {agent_id}")
            monitoring = config['monitoring_config']
            self.assertIn('performance_metrics', monitoring, f"Missing performance metrics in {agent_id}")


if __name__ == '__main__':
    print("🧪 AI Agent YAML Configuration Unit Tests")
    print("Testing agent configuration files and structure validation")
    print("=" * 70)
    
    unittest.main(verbosity=2)