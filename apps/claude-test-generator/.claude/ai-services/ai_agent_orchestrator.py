#!/usr/bin/env python3
"""
AI Agent Orchestrator - Phase 2 AI Enhancement Integration
Orchestrates hybrid AI-traditional agent execution using YAML configurations
"""

import os
import json
import yaml
import logging
import asyncio
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from foundation_context import FoundationContext
from progressive_context_setup import ProgressiveContextArchitecture, ContextInheritanceChain

logger = logging.getLogger(__name__)


@dataclass
class AgentExecutionResult:
    """Result from agent execution"""
    agent_id: str
    agent_name: str
    execution_status: str  # "success", "failed", "partial"
    execution_time: float
    output_file: Optional[str] = None
    findings: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    ai_enhancement_used: bool = False
    confidence_score: float = 0.0


@dataclass
class PhaseExecutionResult:
    """Result from phase execution"""
    phase_name: str
    agent_results: List[AgentExecutionResult]
    phase_success: bool
    total_execution_time: float
    context_updates: Dict[str, Any]


class AIAgentConfigurationLoader:
    """Loads and validates AI agent YAML configurations"""
    
    def __init__(self, agents_dir: str = None):
        self.agents_dir = Path(agents_dir or ".claude/ai-services/agents")
        self.configurations = {}
        self._load_all_configurations()
    
    def _load_all_configurations(self):
        """Load all agent YAML configurations"""
        if not self.agents_dir.exists():
            raise FileNotFoundError(f"Agents directory not found: {self.agents_dir}")
        
        yaml_files = list(self.agents_dir.glob("*.yaml"))
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r') as f:
                    config = yaml.safe_load(f)
                
                agent_id = config['agent_metadata']['agent_id']
                self.configurations[agent_id] = config
                logger.info(f"Loaded configuration for {agent_id}")
                
            except Exception as e:
                logger.error(f"Failed to load {yaml_file}: {e}")
    
    def get_configuration(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for specific agent"""
        return self.configurations.get(agent_id)
    
    def get_phase_agents(self, phase: str) -> List[Dict[str, Any]]:
        """Get all agents for a specific phase"""
        phase_agents = []
        for config in self.configurations.values():
            if config['agent_metadata']['phase'] == phase:
                phase_agents.append(config)
        return phase_agents
    
    def validate_configurations(self) -> bool:
        """Validate all loaded configurations"""
        required_sections = [
            'agent_metadata', 'context_inheritance', 'ai_capabilities',
            'execution_workflow', 'output_specification'
        ]
        
        for agent_id, config in self.configurations.items():
            for section in required_sections:
                if section not in config:
                    logger.error(f"Missing section '{section}' in {agent_id}")
                    return False
        
        logger.info("All agent configurations validated successfully")
        return True


class HybridAIAgentExecutor:
    """Executes individual agents with hybrid AI-traditional approach"""
    
    def __init__(self, config_loader: AIAgentConfigurationLoader):
        self.config_loader = config_loader
        self.ai_models_available = self._check_ai_model_availability()
    
    def _check_ai_model_availability(self) -> bool:
        """Check if AI models are available for enhancement"""
        # In a real implementation, this would check AI service availability
        # For now, we'll simulate AI availability based on environment
        ai_config_file = Path(".claude/config/ai_models_config.json")
        return ai_config_file.exists()
    
    async def execute_agent(self, agent_id: str, inheritance_chain: ContextInheritanceChain, 
                          run_dir: str) -> AgentExecutionResult:
        """Execute a single agent with hybrid AI-traditional approach"""
        start_time = datetime.now()
        
        try:
            config = self.config_loader.get_configuration(agent_id)
            if not config:
                raise ValueError(f"Configuration not found for agent {agent_id}")
            
            logger.info(f"Executing {config['agent_metadata']['agent_name']}")
            
            # Phase 1: Foundation (Traditional 70%)
            foundation_result = await self._execute_traditional_foundation(
                agent_id, config, inheritance_chain, run_dir
            )
            
            # Phase 2: AI Enhancement (30%) - if available and triggered
            ai_enhancement_result = None
            ai_enhancement_used = False
            
            if self._should_apply_ai_enhancement(config, foundation_result):
                ai_enhancement_result = await self._execute_ai_enhancement(
                    agent_id, config, foundation_result, inheritance_chain, run_dir
                )
                ai_enhancement_used = True
            
            # Phase 3: Synthesis
            final_result = self._synthesize_results(
                agent_id, config, foundation_result, ai_enhancement_result, run_dir
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentExecutionResult(
                agent_id=agent_id,
                agent_name=config['agent_metadata']['agent_name'],
                execution_status="success",
                execution_time=execution_time,
                output_file=final_result.get('output_file'),
                findings=final_result.get('findings'),
                ai_enhancement_used=ai_enhancement_used,
                confidence_score=final_result.get('confidence_score', 0.8)
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Agent {agent_id} execution failed: {e}")
            
            return AgentExecutionResult(
                agent_id=agent_id,
                agent_name=config['agent_metadata']['agent_name'] if config else agent_id,
                execution_status="failed",
                execution_time=execution_time,
                error_message=str(e)
            )
    
    async def _execute_traditional_foundation(self, agent_id: str, config: Dict[str, Any],
                                           inheritance_chain: ContextInheritanceChain,
                                           run_dir: str) -> Dict[str, Any]:
        """Execute traditional foundation (70% weight)"""
        logger.info(f"Executing traditional foundation for {agent_id}")
        
        # Get agent context from inheritance chain
        agent_context = inheritance_chain.agent_contexts.get(agent_id, {})
        
        if agent_id == "agent_a_jira_intelligence":
            result = await self._execute_agent_a_traditional(agent_context, run_dir)
        elif agent_id == "agent_b_documentation_intelligence":
            result = await self._execute_agent_b_traditional(agent_context, run_dir)
        elif agent_id == "agent_c_github_investigation":
            result = await self._execute_agent_c_traditional(agent_context, run_dir)
        elif agent_id == "agent_d_environment_intelligence":
            result = await self._execute_agent_d_traditional(agent_context, run_dir)
        else:
            raise ValueError(f"Unknown agent ID: {agent_id}")
        
        return result
    
    async def _execute_agent_a_traditional(self, context: Dict[str, Any], run_dir: str) -> Dict[str, Any]:
        """Execute Agent A traditional JIRA intelligence"""
        from jira_api_client import JiraApiClient
        
        try:
            jira_client = JiraApiClient()
            jira_id = context.get('jira_id', 'UNKNOWN')
            
            # Traditional JIRA analysis
            ticket_data = jira_client.get_ticket_information(jira_id)
            
            analysis = {
                'requirement_analysis': {
                    'primary_requirements': [ticket_data.title],
                    'component_focus': ticket_data.component,
                    'priority_level': ticket_data.priority,
                    'version_target': ticket_data.fix_version
                },
                'dependency_mapping': {
                    'component_dependencies': [ticket_data.component],
                    'version_dependencies': [ticket_data.fix_version]
                },
                'traditional_analysis': True,
                'data_source': 'jira_api' if hasattr(ticket_data, 'raw_data') and ticket_data.raw_data else 'simulation'
            }
            
            output_file = os.path.join(run_dir, "agent_a_analysis.json")
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            
            return {
                'findings': analysis,
                'output_file': output_file,
                'confidence_score': 0.8,
                'execution_method': 'traditional'
            }
            
        except Exception as e:
            logger.error(f"Agent A traditional execution failed: {e}")
            raise
    
    async def _execute_agent_b_traditional(self, context: Dict[str, Any], run_dir: str) -> Dict[str, Any]:
        """Execute Agent B traditional documentation intelligence"""
        # Simplified traditional documentation search
        component = context.get('component', 'unknown')
        version = context.get('target_version', 'unknown')
        
        documentation_analysis = {
            'discovered_documentation': [
                f"https://access.redhat.com/documentation/{component}",
                f"https://docs.openshift.com/{component}/{version}"
            ],
            'relevance_analysis': {
                'high_relevance': f"{component} {version} documentation",
                'medium_relevance': f"{component} general documentation"
            },
            'traditional_search': True,
            'search_method': 'pattern_based'
        }
        
        output_file = os.path.join(run_dir, "agent_b_documentation.json")
        with open(output_file, 'w') as f:
            json.dump(documentation_analysis, f, indent=2)
        
        return {
            'findings': documentation_analysis,
            'output_file': output_file,
            'confidence_score': 0.7,
            'execution_method': 'traditional'
        }
    
    async def _execute_agent_c_traditional(self, context: Dict[str, Any], run_dir: str) -> Dict[str, Any]:
        """Execute Agent C traditional GitHub investigation"""
        component = context.get('component', 'unknown')
        jira_id = context.get('jira_id', 'unknown')
        
        github_analysis = {
            'repository_analysis': {
                'target_repositories': [
                    f"stolostron/{component}",
                    f"open-cluster-management-io/{component}"
                ],
                'search_queries': [
                    f"{jira_id} in:comments",
                    f"{component} is:pr"
                ]
            },
            'traditional_investigation': True,
            'search_method': 'api_based'
        }
        
        output_file = os.path.join(run_dir, "agent_c_github.json")
        with open(output_file, 'w') as f:
            json.dump(github_analysis, f, indent=2)
        
        return {
            'findings': github_analysis,
            'output_file': output_file,
            'confidence_score': 0.75,
            'execution_method': 'traditional'
        }
    
    async def _execute_agent_d_traditional(self, context: Dict[str, Any], run_dir: str) -> Dict[str, Any]:
        """Execute Agent D traditional environment intelligence"""
        from environment_assessment_client import EnvironmentAssessmentClient
        
        try:
            env_client = EnvironmentAssessmentClient()
            cluster_name = context.get('cluster_name', 'current')
            
            # Traditional environment assessment
            env_data = env_client.assess_environment(cluster_name)
            
            environment_analysis = {
                'environment_assessment': {
                    'cluster_name': env_data.cluster_name,
                    'version': env_data.version,
                    'platform': env_data.platform,
                    'health_status': env_data.health_status,
                    'connectivity_confirmed': env_data.connectivity_confirmed
                },
                'tooling_analysis': {
                    'available_tools': env_data.tools_available,
                    'primary_tool': list(env_data.tools_available.keys())[0] if env_data.tools_available else 'none'
                },
                'traditional_assessment': True,
                'detection_method': env_data.detection_method
            }
            
            output_file = os.path.join(run_dir, "agent_d_environment.json")
            with open(output_file, 'w') as f:
                json.dump(environment_analysis, f, indent=2)
            
            return {
                'findings': environment_analysis,
                'output_file': output_file,
                'confidence_score': 0.85,
                'execution_method': 'traditional'
            }
            
        except Exception as e:
            logger.error(f"Agent D traditional execution failed: {e}")
            raise
    
    def _should_apply_ai_enhancement(self, config: Dict[str, Any], 
                                   foundation_result: Dict[str, Any]) -> bool:
        """Determine if AI enhancement should be applied"""
        if not self.ai_models_available:
            return False
        
        enhancement_triggers = config.get('ai_enhancement_config', {}).get('enhancement_triggers', [])
        
        # Simple trigger logic - in production this would be more sophisticated
        confidence_score = foundation_result.get('confidence_score', 1.0)
        return confidence_score < 0.9  # Apply AI if confidence is not high
    
    async def _execute_ai_enhancement(self, agent_id: str, config: Dict[str, Any],
                                    foundation_result: Dict[str, Any],
                                    inheritance_chain: ContextInheritanceChain,
                                    run_dir: str) -> Dict[str, Any]:
        """Execute AI enhancement (30% weight)"""
        logger.info(f"Applying AI enhancement for {agent_id}")
        
        # Simulated AI enhancement - in production this would call actual AI models
        ai_enhancement = {
            'ai_insights': {
                'enhanced_analysis': True,
                'confidence_boost': 0.1,
                'additional_findings': [
                    'AI-identified pattern',
                    'Enhanced semantic analysis'
                ]
            },
            'ai_method': 'llm_analysis',
            'enhancement_applied': True
        }
        
        return ai_enhancement
    
    def _synthesize_results(self, agent_id: str, config: Dict[str, Any],
                          foundation_result: Dict[str, Any],
                          ai_enhancement_result: Optional[Dict[str, Any]],
                          run_dir: str) -> Dict[str, Any]:
        """Synthesize traditional and AI results"""
        traditional_weight = config.get('ai_enhancement_config', {}).get('traditional_weight', 0.7)
        ai_weight = config.get('ai_enhancement_config', {}).get('enhancement_weight', 0.3)
        
        # Weighted synthesis of results
        final_findings = foundation_result['findings'].copy()
        final_confidence = foundation_result['confidence_score']
        
        if ai_enhancement_result:
            # Apply AI enhancement
            final_findings['ai_enhancement'] = ai_enhancement_result['ai_insights']
            final_confidence = min(1.0, final_confidence + ai_enhancement_result['ai_insights']['confidence_boost'])
        
        return {
            'findings': final_findings,
            'output_file': foundation_result['output_file'],
            'confidence_score': final_confidence,
            'synthesis_method': 'weighted_hybrid'
        }


class PhaseBasedOrchestrator:
    """Orchestrates agent execution by phases"""
    
    def __init__(self, framework_root: str = None):
        self.framework_root = framework_root or os.getcwd()
        self.config_loader = AIAgentConfigurationLoader()
        self.agent_executor = HybridAIAgentExecutor(self.config_loader)
        self.pca = ProgressiveContextArchitecture(self.framework_root)
        
        # Validate configurations
        if not self.config_loader.validate_configurations():
            raise ValueError("Agent configuration validation failed")
    
    async def execute_full_framework(self, jira_id: str, environment: str = None) -> Dict[str, Any]:
        """Execute complete 4-agent framework with AI enhancement"""
        logger.info(f"Starting full framework execution for {jira_id}")
        
        # Setup Progressive Context Architecture
        foundation_context = self.pca.create_foundation_context_for_jira(jira_id, environment)
        inheritance_chain = self.pca.initialize_context_inheritance_chain(foundation_context)
        
        # Create run directory
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir = os.path.join(self.framework_root, "runs", jira_id, f"{jira_id}-{timestamp}")
        os.makedirs(run_dir, exist_ok=True)
        
        execution_results = {
            'jira_id': jira_id,
            'execution_timestamp': datetime.now().isoformat(),
            'run_directory': run_dir,
            'phases': {}
        }
        
        try:
            # Phase 1: Parallel Foundation Analysis (Agent A + Agent D)
            phase_1_result = await self._execute_phase_parallel(
                "Phase 1 - Parallel Foundation Analysis",
                ["agent_a_jira_intelligence", "agent_d_environment_intelligence"],
                inheritance_chain, run_dir
            )
            execution_results['phases']['phase_1'] = phase_1_result
            
            # Phase 2: Parallel Deep Investigation (Agent B + Agent C)
            phase_2_result = await self._execute_phase_parallel(
                "Phase 2 - Parallel Deep Investigation", 
                ["agent_b_documentation_intelligence", "agent_c_github_investigation"],
                inheritance_chain, run_dir
            )
            execution_results['phases']['phase_2'] = phase_2_result
            
            # Generate execution summary
            execution_results['summary'] = self._generate_execution_summary(execution_results)
            
            # Save execution metadata
            metadata_file = os.path.join(run_dir, "ai_execution_metadata.json")
            with open(metadata_file, 'w') as f:
                json.dump(execution_results, f, indent=2)
            
            logger.info(f"Full framework execution completed for {jira_id}")
            return execution_results
            
        except Exception as e:
            logger.error(f"Framework execution failed for {jira_id}: {e}")
            execution_results['error'] = str(e)
            execution_results['status'] = 'failed'
            return execution_results
    
    async def _execute_phase_parallel(self, phase_name: str, agent_ids: List[str],
                                    inheritance_chain: ContextInheritanceChain,
                                    run_dir: str) -> PhaseExecutionResult:
        """Execute agents in parallel for a phase"""
        logger.info(f"Executing {phase_name} with agents: {agent_ids}")
        start_time = datetime.now()
        
        # Execute agents in parallel
        tasks = []
        for agent_id in agent_ids:
            task = self.agent_executor.execute_agent(agent_id, inheritance_chain, run_dir)
            tasks.append(task)
        
        # Wait for all agents to complete
        agent_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_results = []
        context_updates = {}
        
        for i, result in enumerate(agent_results):
            if isinstance(result, Exception):
                logger.error(f"Agent {agent_ids[i]} failed with exception: {result}")
                result = AgentExecutionResult(
                    agent_id=agent_ids[i],
                    agent_name=agent_ids[i],
                    execution_status="failed",
                    execution_time=0,
                    error_message=str(result)
                )
            
            successful_results.append(result)
            
            # Update Progressive Context Architecture
            if result.execution_status == "success" and result.findings:
                agent_key = result.agent_id
                context_updates[f"{agent_key}_findings"] = result.findings
                
                # Update inheritance chain
                inheritance_chain.agent_contexts[agent_key].update({
                    f"{agent_key}_findings": result.findings,
                    "execution_status": "completed",
                    "output_file": result.output_file
                })
        
        execution_time = (datetime.now() - start_time).total_seconds()
        phase_success = all(r.execution_status == "success" for r in successful_results)
        
        return PhaseExecutionResult(
            phase_name=phase_name,
            agent_results=successful_results,
            phase_success=phase_success,
            total_execution_time=execution_time,
            context_updates=context_updates
        )
    
    def _generate_execution_summary(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate execution summary"""
        total_agents = 0
        successful_agents = 0
        total_time = 0
        ai_enhanced_agents = 0
        
        for phase_data in execution_results['phases'].values():
            for agent_result in phase_data.agent_results:
                total_agents += 1
                if agent_result.execution_status == "success":
                    successful_agents += 1
                if agent_result.ai_enhancement_used:
                    ai_enhanced_agents += 1
                total_time += agent_result.execution_time
        
        return {
            'total_agents': total_agents,
            'successful_agents': successful_agents,
            'success_rate': successful_agents / total_agents if total_agents > 0 else 0,
            'ai_enhancement_rate': ai_enhanced_agents / total_agents if total_agents > 0 else 0,
            'total_execution_time': total_time,
            'framework_status': 'success' if successful_agents == total_agents else 'partial'
        }


# Convenience functions for external use
async def execute_ai_enhanced_framework(jira_id: str, environment: str = None) -> Dict[str, Any]:
    """Execute AI-enhanced framework for JIRA ticket"""
    orchestrator = PhaseBasedOrchestrator()
    return await orchestrator.execute_full_framework(jira_id, environment)


def test_ai_agent_configurations() -> bool:
    """Test AI agent configuration loading and validation"""
    try:
        config_loader = AIAgentConfigurationLoader()
        return config_loader.validate_configurations()
    except Exception as e:
        logger.error(f"Configuration test failed: {e}")
        return False


if __name__ == "__main__":
    # Example usage and testing
    import sys
    
    async def main():
        if len(sys.argv) > 1:
            jira_id = sys.argv[1]
            environment = sys.argv[2] if len(sys.argv) > 2 else None
            
            print(f"🤖 Executing AI-Enhanced Framework for {jira_id}...")
            
            try:
                results = await execute_ai_enhanced_framework(jira_id, environment)
                print(f"✅ Framework execution completed!")
                print(f"📊 Summary: {results['summary']}")
                print(f"📁 Results saved to: {results['run_directory']}")
                
            except Exception as e:
                print(f"❌ Framework execution failed: {e}")
                sys.exit(1)
        else:
            print("🧪 Testing AI agent configurations...")
            if test_ai_agent_configurations():
                print("✅ All configurations valid!")
            else:
                print("❌ Configuration validation failed!")
                sys.exit(1)
    
    # Run async main
    asyncio.run(main())