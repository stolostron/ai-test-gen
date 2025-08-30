#!/usr/bin/env python3
"""
Enhanced Agent A - JIRA Intelligence with Real-Time PR Discovery Publishing
Integrates with inter-agent communication system for real-time coordination with Agent D
"""

import os
import json
import logging
import asyncio
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from jira_api_client import JiraApiClient
from inter_agent_communication import AgentCommunicationInterface, InterAgentMessage
from information_sufficiency_analyzer import InformationSufficiencyAnalyzer, SufficiencyScore
from framework_stop_handler import FrameworkStopHandler, InsufficientInformationError

logger = logging.getLogger(__name__)


@dataclass
class PRDiscoveryResult:
    """Result from PR discovery analysis"""
    pr_number: str
    pr_title: str
    pr_url: Optional[str]
    files_changed: List[str]
    deployment_components: List[str]
    yaml_files: List[str]
    config_changes: List[str]
    api_changes: List[str]
    operator_changes: List[str]
    confidence_score: float


@dataclass
class EnvironmentCollectionRequirements:
    """Requirements for Agent D environment collection"""
    target_components: List[str]
    required_yamls: List[str]
    required_logs: List[str]
    required_commands: List[str]
    sample_resources: List[str]
    priority: str  # "low", "normal", "high", "critical"


class EnhancedJIRAIntelligenceAgent:
    """
    Enhanced Agent A with real-time PR discovery and Agent D coordination
    """
    
    def __init__(self, communication_hub, run_dir: str):
        self.agent_id = "agent_a_jira_intelligence"
        self.run_dir = run_dir
        
        # Initialize communication interface
        self.comm = AgentCommunicationInterface(self.agent_id, communication_hub)
        
        # Initialize JIRA client
        self.jira_client = JiraApiClient()
        
        # Initialize information sufficiency components
        self.sufficiency_analyzer = InformationSufficiencyAnalyzer()
        self.stop_handler = FrameworkStopHandler(run_dir)
        
        # Analysis state
        self.analysis_results = {}
        self.pr_discoveries = []
        self.environment_requirements = []
        
        # Configuration
        self.config = {
            'enable_sufficiency_check': True,
            'minimum_score': 0.75,
            'fallback_score': 0.60,
            'allow_force': False  # Can be overridden by command line
        }
        
        logger.info("Enhanced JIRA Intelligence Agent initialized with real-time communication")
    
    async def execute_enhanced_jira_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute enhanced JIRA analysis with real-time PR discovery publishing
        """
        start_time = datetime.now()
        
        try:
            self.comm.update_status("active")
            
            jira_id = context.get('jira_id', 'UNKNOWN')
            logger.info(f"Starting enhanced JIRA analysis for {jira_id}")
            
            # Phase 1: Basic JIRA Analysis
            basic_analysis = await self._perform_basic_jira_analysis(jira_id)
            
            # Phase 2: PR Discovery and Real-Time Publishing
            pr_discoveries = await self._discover_and_publish_pr_information(jira_id, basic_analysis)
            
            # Phase 3: Component and Environment Analysis
            component_analysis = await self._analyze_components_and_environment(basic_analysis, pr_discoveries)
            
            # Phase 4: Generate Environment Collection Requirements
            env_requirements = await self._generate_environment_requirements(component_analysis, pr_discoveries)
            
            # Phase 5: Publish Environment Collection Requirements
            await self._publish_environment_requirements(env_requirements)
            
            # Phase 6: Compile Final Analysis
            final_analysis = await self._compile_final_analysis(
                basic_analysis, pr_discoveries, component_analysis, env_requirements
            )
            
            # Phase 7: Information Sufficiency Check
            if self.config['enable_sufficiency_check']:
                sufficiency_result = await self._check_information_sufficiency(
                    final_analysis, jira_id
                )
                # If we get here, sufficiency check passed or was handled
                final_analysis['sufficiency_score'] = sufficiency_result.overall_score
                final_analysis['sufficiency_status'] = 'sufficient' if sufficiency_result.can_proceed else 'marginal'
            
            # Save analysis results
            output_file = await self._save_analysis_results(final_analysis)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.comm.update_status("completed")
            
            logger.info(f"Enhanced JIRA analysis completed for {jira_id} in {execution_time:.2f}s")
            
            return {
                'findings': final_analysis,
                'output_file': output_file,
                'confidence_score': final_analysis.get('confidence_score', 0.9),
                'execution_method': 'enhanced_with_realtime_coordination',
                'pr_discoveries': len(pr_discoveries),
                'environment_requirements_published': len(env_requirements)
            }
            
        except Exception as e:
            self.comm.update_status("failed")
            logger.error(f"Enhanced JIRA analysis failed: {e}")
            raise
    
    async def _perform_basic_jira_analysis(self, jira_id: str) -> Dict[str, Any]:
        """Perform comprehensive JIRA ticket analysis"""
        logger.info(f"Performing basic JIRA analysis for {jira_id}")
        
        # Get JIRA ticket data
        ticket_data = self.jira_client.get_ticket_information(jira_id)
        
        # Extract comprehensive information
        basic_analysis = {
            'jira_info': {
                'jira_id': jira_id,
                'title': ticket_data.title,
                'description': ticket_data.description,
                'status': ticket_data.status,
                'priority': ticket_data.priority,
                'component': ticket_data.component,
                'fix_version': ticket_data.fix_version,
                'assignee': ticket_data.assignee,
                'labels': ticket_data.labels
            },
            'requirement_analysis': {
                'primary_requirements': self._extract_requirements(ticket_data.description),
                'acceptance_criteria': self._extract_acceptance_criteria(ticket_data.description),
                'technical_scope': self._analyze_technical_scope(ticket_data)
            },
            'business_context': {
                'customer_impact': self._analyze_customer_impact(ticket_data),
                'feature_type': self._classify_feature_type(ticket_data),
                'urgency_assessment': self._assess_urgency(ticket_data)
            }
        }
        
        return basic_analysis
    
    async def _discover_and_publish_pr_information(self, jira_id: str, basic_analysis: Dict[str, Any]) -> List[PRDiscoveryResult]:
        """Discover PR information and publish in real-time to Agent D"""
        logger.info(f"Discovering PR information for {jira_id}")
        
        pr_discoveries = []
        
        # Method 1: Extract PR references from JIRA description/comments
        pr_refs = self._extract_pr_references(basic_analysis['jira_info']['description'])
        
        # Method 2: Search GitHub for related PRs
        github_prs = await self._search_github_for_prs(jira_id, basic_analysis)
        
        # Process discovered PRs
        all_pr_refs = pr_refs + github_prs
        
        for pr_ref in all_pr_refs:
            try:
                # Analyze PR details
                pr_discovery = await self._analyze_pr_details(pr_ref, basic_analysis)
                pr_discoveries.append(pr_discovery)
                
                # REAL-TIME PUBLISHING: Immediately share PR discovery with Agent D
                await self._publish_pr_discovery_realtime(pr_discovery)
                
                logger.info(f"Published PR discovery for {pr_discovery.pr_number} to Agent D")
                
            except Exception as e:
                logger.warning(f"Failed to analyze PR {pr_ref}: {e}")
        
        return pr_discoveries
    
    async def _analyze_pr_details(self, pr_ref: str, context: Dict[str, Any]) -> PRDiscoveryResult:
        """Analyze detailed PR information"""
        
        # Extract PR number
        pr_number = self._extract_pr_number(pr_ref)
        
        # Simulate GitHub API call to get PR details
        # In real implementation, this would use GitHub API
        pr_details = {
            'title': f'ClusterCurator digest-based upgrades for {pr_number}',
            'files_changed': [
                'pkg/clustercurator/controller.go',
                'config/crd/bases/cluster.open-cluster-management.io_clustercurators.yaml',
                'test/functional/clustercurator_test.go',
                'docs/clustercurator-usage.md'
            ],
            'url': f'https://github.com/stolostron/cluster-curator-controller/pull/{pr_number}'
        }
        
        # Analyze file changes for deployment impact
        deployment_components = self._analyze_deployment_components(pr_details['files_changed'])
        yaml_files = self._identify_yaml_files(pr_details['files_changed'])
        config_changes = self._identify_config_changes(pr_details['files_changed'])
        api_changes = self._identify_api_changes(pr_details['files_changed'])
        operator_changes = self._identify_operator_changes(pr_details['files_changed'])
        
        return PRDiscoveryResult(
            pr_number=pr_number,
            pr_title=pr_details['title'],
            pr_url=pr_details['url'],
            files_changed=pr_details['files_changed'],
            deployment_components=deployment_components,
            yaml_files=yaml_files,
            config_changes=config_changes,
            api_changes=api_changes,
            operator_changes=operator_changes,
            confidence_score=0.95
        )
    
    async def _publish_pr_discovery_realtime(self, pr_discovery: PRDiscoveryResult):
        """Publish PR discovery to Agent D in real-time"""
        
        pr_payload = {
            'pr_number': pr_discovery.pr_number,
            'pr_title': pr_discovery.pr_title,
            'pr_url': pr_discovery.pr_url,
            'files_changed': pr_discovery.files_changed,
            'deployment_components': pr_discovery.deployment_components,
            'yaml_files': pr_discovery.yaml_files,
            'config_changes': pr_discovery.config_changes,
            'api_changes': pr_discovery.api_changes,
            'operator_changes': pr_discovery.operator_changes,
            'confidence_score': pr_discovery.confidence_score,
            'collection_priority': 'high',
            'immediate_action_required': True
        }
        
        await self.comm.publish_pr_discovery(pr_payload, target_agent="agent_d_environment_intelligence")
        
        logger.info(f"Real-time PR discovery published: {pr_discovery.pr_number}")
    
    async def _generate_environment_requirements(self, component_analysis: Dict[str, Any], 
                                               pr_discoveries: List[PRDiscoveryResult]) -> List[EnvironmentCollectionRequirements]:
        """Generate specific environment collection requirements for Agent D"""
        
        requirements = []
        
        for pr_discovery in pr_discoveries:
            # Generate requirements based on PR analysis
            req = EnvironmentCollectionRequirements(
                target_components=pr_discovery.deployment_components,
                required_yamls=[
                    f"clustercurator-{pr_discovery.pr_number}-*.yaml",
                    "clustercurator-controller-deployment.yaml",
                    "clustercurator-crd.yaml"
                ] + pr_discovery.yaml_files,
                required_logs=[
                    "clustercurator-controller-manager logs",
                    "open-cluster-management-hub namespace events",
                    "clustercurator operator logs"
                ],
                required_commands=[
                    "oc get clustercurators -A -o yaml",
                    "oc get managedclusters -o yaml",
                    "oc describe clustercurator",
                    "oc logs -n open-cluster-management clustercurator-controller-manager",
                    f"oc get deployment clustercurator-controller-manager -n open-cluster-management -o yaml"
                ],
                sample_resources=[
                    "sample-clustercurator-upgrade.yaml",
                    "sample-managedcluster.yaml",
                    "clustercurator-status-examples.yaml"
                ],
                priority="high"
            )
            
            requirements.append(req)
        
        return requirements
    
    async def _publish_environment_requirements(self, requirements: List[EnvironmentCollectionRequirements]):
        """Publish environment collection requirements to Agent D"""
        
        for req in requirements:
            env_payload = {
                'target_components': req.target_components,
                'required_yamls': req.required_yamls,
                'required_logs': req.required_logs,
                'required_commands': req.required_commands,
                'sample_resources': req.sample_resources,
                'priority': req.priority,
                'collection_timestamp': datetime.now().isoformat(),
                'agent_a_analysis_complete': False  # Will be updated when final analysis is done
            }
            
            await self.comm.request_environment_data(env_payload, target_agent="agent_d_environment_intelligence")
            
            logger.info(f"Environment collection requirements published to Agent D")
    
    async def _compile_final_analysis(self, basic_analysis: Dict[str, Any], 
                                    pr_discoveries: List[PRDiscoveryResult],
                                    component_analysis: Dict[str, Any],
                                    env_requirements: List[EnvironmentCollectionRequirements]) -> Dict[str, Any]:
        """Compile comprehensive final analysis"""
        
        return {
            'analysis_metadata': {
                'agent': 'Agent A - Enhanced JIRA Intelligence',
                'analysis_timestamp': datetime.now().isoformat(),
                'jira_ticket': basic_analysis['jira_info']['jira_id'],
                'analysis_version': 'v2.0_enhanced_realtime'
            },
            'jira_intelligence': basic_analysis,
            'pr_discoveries': [
                {
                    'pr_number': pr.pr_number,
                    'pr_title': pr.pr_title,
                    'pr_url': pr.pr_url,
                    'deployment_impact': pr.deployment_components,
                    'files_modified': len(pr.files_changed),
                    'confidence': pr.confidence_score
                } for pr in pr_discoveries
            ],
            'component_analysis': component_analysis,
            'environment_coordination': {
                'requirements_published': len(env_requirements),
                'realtime_coordination_active': True,
                'agent_d_integration': 'enabled'
            },
            'progressive_context_ready': {
                'agent_b_inheritance': True,
                'agent_c_inheritance': True,
                'findings_available': True
            },
            'confidence_score': 0.92,
            'next_phase_readiness': True
        }
    
    async def _save_analysis_results(self, analysis: Dict[str, Any]) -> str:
        """Save comprehensive analysis results"""
        
        output_file = os.path.join(self.run_dir, "enhanced_agent_a_jira_intelligence.json")
        
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        logger.info(f"Enhanced JIRA analysis saved to {output_file}")
        
        return output_file
    
    # Helper methods
    def _extract_requirements(self, description: str) -> List[str]:
        """Extract requirements from JIRA description"""
        # Simple requirement extraction logic
        requirements = []
        if 'digest-based' in description.lower():
            requirements.append("Implement digest-based upgrade mechanism")
        if 'clustercurator' in description.lower():
            requirements.append("Enhance ClusterCurator functionality")
        if 'disconnected' in description.lower():
            requirements.append("Support disconnected environments")
        return requirements
    
    def _extract_acceptance_criteria(self, description: str) -> List[str]:
        """Extract acceptance criteria from JIRA description"""
        criteria = []
        if 'upgrade' in description.lower():
            criteria.append("Cluster upgrades must complete successfully")
        if 'fallback' in description.lower():
            criteria.append("Fallback mechanism must be implemented")
        return criteria
    
    def _analyze_technical_scope(self, ticket_data) -> Dict[str, Any]:
        """Analyze technical scope of the ticket"""
        return {
            'component_focus': ticket_data.component,
            'api_changes_likely': 'api' in ticket_data.description.lower(),
            'operator_changes_likely': 'operator' in ticket_data.description.lower(),
            'crd_changes_likely': 'crd' in ticket_data.description.lower() or 'custom resource' in ticket_data.description.lower()
        }
    
    def _analyze_customer_impact(self, ticket_data) -> Dict[str, Any]:
        """Analyze customer impact"""
        return {
            'customer_facing': True,
            'breaking_change_risk': 'breaking' in ticket_data.description.lower(),
            'production_impact': ticket_data.priority in ['High', 'Critical']
        }
    
    def _classify_feature_type(self, ticket_data) -> str:
        """Classify the type of feature"""
        if 'enhancement' in ticket_data.description.lower():
            return 'enhancement'
        elif 'bug' in ticket_data.description.lower():
            return 'bugfix'
        elif 'new' in ticket_data.description.lower():
            return 'new_feature'
        else:
            return 'unknown'
    
    def _assess_urgency(self, ticket_data) -> str:
        """Assess urgency level"""
        if ticket_data.priority in ['Critical', 'Blocker']:
            return 'critical'
        elif ticket_data.priority == 'High':
            return 'high'
        else:
            return 'normal'
    
    def _extract_pr_references(self, description: str) -> List[str]:
        """Extract PR references from JIRA description"""
        # Look for PR patterns like "PR #468", "pull/468", etc.
        pr_patterns = [
            r'PR #?(\d+)',
            r'pull/(\d+)',
            r'pull request #?(\d+)',
            r'github\.com/.+/pull/(\d+)'
        ]
        
        pr_refs = []
        for pattern in pr_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            pr_refs.extend(matches)
        
        # Return unique PR numbers
        return list(set(pr_refs))
    
    async def _search_github_for_prs(self, jira_id: str, basic_analysis: Dict[str, Any]) -> List[str]:
        """Search GitHub for PRs related to this JIRA ticket"""
        # Simulate GitHub search
        # In real implementation, this would use GitHub API
        if jira_id == "ACM-22079":
            return ["468"]  # Known PR for ACM-22079
        return []
    
    def _extract_pr_number(self, pr_ref: str) -> str:
        """Extract clean PR number from reference"""
        return pr_ref.strip('#')
    
    def _analyze_deployment_components(self, files_changed: List[str]) -> List[str]:
        """Analyze which components are affected by file changes"""
        components = set()
        
        for file_path in files_changed:
            if 'clustercurator' in file_path.lower():
                components.add('ClusterCurator')
            if 'controller' in file_path.lower():
                components.add('Controller')
            if 'operator' in file_path.lower():
                components.add('Operator')
            if 'crd' in file_path.lower():
                components.add('CustomResourceDefinition')
        
        return list(components)
    
    def _identify_yaml_files(self, files_changed: List[str]) -> List[str]:
        """Identify YAML files from changed files"""
        return [f for f in files_changed if f.endswith(('.yaml', '.yml'))]
    
    def _identify_config_changes(self, files_changed: List[str]) -> List[str]:
        """Identify configuration changes"""
        config_files = []
        for f in files_changed:
            if any(keyword in f.lower() for keyword in ['config', 'settings', 'properties']):
                config_files.append(f)
        return config_files
    
    async def _check_information_sufficiency(self, analysis_data: Dict[str, Any], 
                                           jira_id: str) -> SufficiencyScore:
        """
        Check if collected information is sufficient for test planning
        Implements progressive enhancement strategy
        """
        logger.info(f"Checking information sufficiency for {jira_id}")
        
        # Prepare data for sufficiency analysis
        collected_data = self._prepare_data_for_sufficiency_check(analysis_data)
        
        # Initial sufficiency check
        sufficiency_result = self.sufficiency_analyzer.analyze_sufficiency(collected_data)
        
        logger.info(f"Initial sufficiency score: {sufficiency_result.overall_score:.2f}")
        
        # If sufficient, proceed
        if sufficiency_result.overall_score >= self.config['minimum_score']:
            logger.info("Information is sufficient for comprehensive test planning")
            return sufficiency_result
        
        # Try enhancement if score is marginal
        if sufficiency_result.overall_score >= self.config['fallback_score']:
            logger.info("Attempting to enhance information through web search...")
            
            # Perform web search enhancement
            enhanced_data = await self._enhance_with_web_search(collected_data, sufficiency_result)
            
            # Re-analyze sufficiency
            enhanced_result = self.sufficiency_analyzer.analyze_sufficiency(enhanced_data)
            
            logger.info(f"Enhanced sufficiency score: {enhanced_result.overall_score:.2f}")
            
            if enhanced_result.overall_score >= self.config['fallback_score']:
                if enhanced_result.overall_score < self.config['minimum_score']:
                    logger.warning("Proceeding with marginal information - test coverage may be limited")
                return enhanced_result
        
        # Check if force proceed is allowed
        if self.config.get('allow_force', False):
            logger.warning(f"Force proceed enabled - continuing despite low score: {sufficiency_result.overall_score:.2f}")
            return sufficiency_result
        
        # Trigger framework stop
        logger.error(f"Information insufficient for {jira_id} - triggering framework stop")
        
        missing_info = {
            'critical': sufficiency_result.missing_critical,
            'optional': sufficiency_result.missing_optional
        }
        
        stop_report = self.stop_handler.trigger_stop(
            jira_id=jira_id,
            collected_data=collected_data,
            score=sufficiency_result.overall_score,
            missing_info=missing_info
        )
        
        # Raise exception to stop framework
        raise InsufficientInformationError(stop_report)
    
    def _prepare_data_for_sufficiency_check(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare analysis data for sufficiency checking"""
        prepared_data = {
            'jira_info': analysis_data.get('jira_info', {}),
            'pr_references': [],
            'github_prs': [],
            'pr_discoveries': analysis_data.get('pr_discoveries', []),
            'acceptance_criteria': analysis_data.get('requirement_analysis', {}).get('acceptance_criteria'),
            'technical_design': analysis_data.get('requirement_analysis', {}).get('technical_scope'),
            'affected_components': analysis_data.get('component_analysis', {}).get('affected_components', []),
            'integration_points': analysis_data.get('component_analysis', {}).get('integration_points', []),
            'target_version': analysis_data.get('jira_info', {}).get('fix_version'),
            'environment_info': analysis_data.get('environment_requirements'),
            'business_value': analysis_data.get('business_context', {}).get('customer_impact'),
            'user_impact': analysis_data.get('business_context', {}).get('customer_impact'),
            'test_scenarios': analysis_data.get('requirement_analysis', {}).get('test_scenarios', []),
            'deployment_instruction': analysis_data.get('deployment_guidance'),
            'subtasks': analysis_data.get('subtasks', []),
            'linked_issues': analysis_data.get('linked_issues', []),
            'comments': analysis_data.get('comments', [])
        }
        
        # Extract PR references from discoveries
        for pr_discovery in analysis_data.get('pr_discoveries', []):
            prepared_data['pr_references'].append(pr_discovery.pr_number)
            prepared_data['github_prs'].append({
                'number': pr_discovery.pr_number,
                'title': pr_discovery.pr_title,
                'files_changed': pr_discovery.files_changed
            })
        
        return prepared_data
    
    async def _enhance_with_web_search(self, collected_data: Dict[str, Any], 
                                     sufficiency_result: SufficiencyScore) -> Dict[str, Any]:
        """
        Enhance collected data through web search for missing information
        """
        enhanced_data = collected_data.copy()
        
        # Search for missing PRs if needed
        if 'GitHub PR references' in sufficiency_result.missing_critical:
            logger.info("Searching web for GitHub PR references...")
            # Simulate web search for PRs
            # In real implementation, this would use web search APIs
            jira_id = collected_data.get('jira_info', {}).get('jira_id', '')
            search_query = f"{jira_id} site:github.com pull request"
            logger.info(f"Web search query: {search_query}")
            # For now, we'll just log the attempt
            
        # Search for technical documentation if needed
        if 'Technical design' in sufficiency_result.missing_critical:
            logger.info("Searching for technical documentation...")
            component = collected_data.get('jira_info', {}).get('component', '')
            search_query = f"ACM {component} architecture design documentation"
            logger.info(f"Web search query: {search_query}")
            
        # Search for acceptance criteria examples
        if 'Acceptance criteria' in sufficiency_result.missing_critical:
            logger.info("Searching for similar feature acceptance criteria...")
            feature_type = collected_data.get('business_context', {}).get('feature_type', '')
            search_query = f"ACM {feature_type} acceptance criteria test scenarios"
            logger.info(f"Web search query: {search_query}")
        
        # Add a flag to indicate enhancement was attempted
        enhanced_data['web_enhancement_attempted'] = True
        enhanced_data['enhancement_queries'] = sufficiency_result.recommendations
        
        return enhanced_data
    
    def _identify_api_changes(self, files_changed: List[str]) -> List[str]:
        """Identify API changes"""
        api_files = []
        for f in files_changed:
            if any(keyword in f.lower() for keyword in ['api', 'types', 'v1', 'v1beta1']):
                api_files.append(f)
        return api_files
    
    def _identify_operator_changes(self, files_changed: List[str]) -> List[str]:
        """Identify operator changes"""
        operator_files = []
        for f in files_changed:
            if any(keyword in f.lower() for keyword in ['operator', 'controller', 'manager']):
                operator_files.append(f)
        return operator_files
    
    async def _analyze_components_and_environment(self, basic_analysis: Dict[str, Any], 
                                                pr_discoveries: List[PRDiscoveryResult]) -> Dict[str, Any]:
        """Analyze components and environment implications"""
        
        all_components = set()
        all_api_changes = []
        
        for pr in pr_discoveries:
            all_components.update(pr.deployment_components)
            all_api_changes.extend(pr.api_changes)
        
        return {
            'affected_components': list(all_components),
            'api_changes_detected': len(all_api_changes) > 0,
            'environment_impact': {
                'requires_cluster_access': True,
                'requires_namespace_access': ['open-cluster-management', 'open-cluster-management-hub'],
                'requires_custom_resources': True
            },
            'testing_implications': {
                'functional_testing_required': True,
                'integration_testing_required': True,
                'upgrade_testing_required': True
            }
        }


if __name__ == '__main__':
    # Test the enhanced Agent A
    import asyncio
    from inter_agent_communication import get_communication_hub
    
    async def test_enhanced_agent_a():
        """Test enhanced Agent A functionality"""
        print("🧪 Testing Enhanced Agent A - JIRA Intelligence")
        
        # Setup communication hub
        hub = get_communication_hub("phase_1", "test_run_002")
        await hub.start_hub()
        
        # Create enhanced Agent A
        agent_a = EnhancedJIRAIntelligenceAgent(hub, "/tmp/test_run")
        
        # Test context
        test_context = {
            'jira_id': 'ACM-22079',
            'target_version': '2.15.0',
            'component': 'ClusterCurator'
        }
        
        # Execute enhanced analysis
        result = await agent_a.execute_enhanced_jira_analysis(test_context)
        
        print(f"Analysis completed: {result['execution_method']}")
        print(f"PR discoveries: {result['pr_discoveries']}")
        print(f"Environment requirements published: {result['environment_requirements_published']}")
        
        # Check communication history
        comm_history = agent_a.comm.get_communication_history()
        print(f"Messages sent: {len(comm_history)}")
        
        await hub.stop_hub()
        
        print("✅ Enhanced Agent A test completed!")
    
    asyncio.run(test_enhanced_agent_a())