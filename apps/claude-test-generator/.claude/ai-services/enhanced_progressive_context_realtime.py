#!/usr/bin/env python3
"""
Enhanced Progressive Context Architecture with Real-Time Agent Coordination
Leverages existing PCA infrastructure for Agent A → Agent D real-time data sharing
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from progressive_context_setup import ProgressiveContextArchitecture, ContextInheritanceChain

logger = logging.getLogger(__name__)


@dataclass
class RealtimePRDiscovery:
    """Real-time PR discovery data structure for PCA"""
    pr_number: str
    pr_title: str
    discovery_timestamp: str
    deployment_components: List[str]
    yaml_files: List[str]
    config_changes: List[str]
    environment_collection_required: bool
    priority: str  # "low", "normal", "high", "urgent"


@dataclass
class EnvironmentCollectionRequest:
    """Environment collection request from Agent A to Agent D"""
    request_id: str
    pr_context: RealtimePRDiscovery
    required_yamls: List[str]
    required_logs: List[str]
    required_commands: List[str]
    collection_priority: str
    immediate_action: bool


class EnhancedProgressiveContextArchitecture(ProgressiveContextArchitecture):
    """
    Enhanced PCA with real-time agent coordination capabilities
    Leverages existing infrastructure for Agent A → Agent D communication
    """
    
    def __init__(self, framework_root: str = None):
        super().__init__(framework_root)
        
        # Real-time coordination extensions
        self.realtime_updates_dir = self.context_dir / "realtime_updates"
        self.realtime_updates_dir.mkdir(exist_ok=True)
        
        # Agent coordination state
        self.active_phase_coordination = {}
        
        logger.info("Enhanced Progressive Context Architecture initialized with real-time coordination")
    
    def enable_realtime_coordination(self, chain_id: str, phase_name: str) -> bool:
        """Enable real-time coordination for a specific phase"""
        
        if chain_id not in self.active_chains:
            logger.error(f"Chain {chain_id} not found")
            return False
        
        # Create real-time coordination directory for this chain
        coordination_dir = self.realtime_updates_dir / chain_id
        coordination_dir.mkdir(exist_ok=True)
        
        self.active_phase_coordination[chain_id] = {
            'phase_name': phase_name,
            'coordination_dir': str(coordination_dir),
            'enabled_at': datetime.now().isoformat(),
            'agent_a_updates': [],
            'agent_d_requests': [],
            'last_update': None
        }
        
        logger.info(f"Real-time coordination enabled for chain {chain_id} in phase {phase_name}")
        return True
    
    def publish_pr_discovery_realtime(self, chain_id: str, agent_id: str, pr_discovery: RealtimePRDiscovery) -> bool:
        """
        Agent A publishes PR discovery to PCA in real-time
        Leverages existing context update mechanism
        """
        
        if chain_id not in self.active_chains:
            logger.error(f"Chain {chain_id} not found")
            return False
        
        # Prepare PR discovery data for context update
        pr_update = {
            'realtime_pr_discoveries': {
                pr_discovery.pr_number: {
                    'pr_number': pr_discovery.pr_number,
                    'pr_title': pr_discovery.pr_title,
                    'discovery_timestamp': pr_discovery.discovery_timestamp,
                    'deployment_components': pr_discovery.deployment_components,
                    'yaml_files': pr_discovery.yaml_files,
                    'config_changes': pr_discovery.config_changes,
                    'environment_collection_required': pr_discovery.environment_collection_required,
                    'priority': pr_discovery.priority,
                    'published_by': agent_id
                }
            },
            'last_pr_discovery_update': datetime.now().isoformat()
        }
        
        # Use existing PCA update mechanism
        success = self.update_agent_context(chain_id, agent_id, pr_update)
        
        if success:
            # Also update coordination state
            if chain_id in self.active_phase_coordination:
                self.active_phase_coordination[chain_id]['agent_a_updates'].append({
                    'type': 'pr_discovery',
                    'pr_number': pr_discovery.pr_number,
                    'timestamp': pr_discovery.discovery_timestamp
                })
                self.active_phase_coordination[chain_id]['last_update'] = datetime.now().isoformat()
            
            # Create real-time update file for Agent D monitoring
            self._create_realtime_update_file(chain_id, 'pr_discovery', pr_discovery)
            
            logger.info(f"PR discovery {pr_discovery.pr_number} published to PCA by {agent_id}")
        
        return success
    
    def publish_environment_collection_request(self, chain_id: str, agent_id: str, 
                                             collection_request: EnvironmentCollectionRequest) -> bool:
        """
        Agent A publishes environment collection request to PCA
        """
        
        if chain_id not in self.active_chains:
            logger.error(f"Chain {chain_id} not found")
            return False
        
        # Prepare collection request for context update
        request_update = {
            'realtime_environment_requests': {
                collection_request.request_id: {
                    'request_id': collection_request.request_id,
                    'pr_context': {
                        'pr_number': collection_request.pr_context.pr_number,
                        'deployment_components': collection_request.pr_context.deployment_components
                    },
                    'required_yamls': collection_request.required_yamls,
                    'required_logs': collection_request.required_logs,
                    'required_commands': collection_request.required_commands,
                    'collection_priority': collection_request.collection_priority,
                    'immediate_action': collection_request.immediate_action,
                    'requested_by': agent_id,
                    'request_timestamp': datetime.now().isoformat()
                }
            },
            'last_environment_request_update': datetime.now().isoformat()
        }
        
        # Use existing PCA update mechanism
        success = self.update_agent_context(chain_id, agent_id, request_update)
        
        if success:
            # Update coordination state
            if chain_id in self.active_phase_coordination:
                self.active_phase_coordination[chain_id]['agent_d_requests'].append({
                    'type': 'environment_request',
                    'request_id': collection_request.request_id,
                    'timestamp': datetime.now().isoformat()
                })
            
            # Create real-time update file
            self._create_realtime_update_file(chain_id, 'environment_request', collection_request)
            
            logger.info(f"Environment collection request {collection_request.request_id} published to PCA")
        
        return success
    
    def get_realtime_pr_discoveries(self, chain_id: str, agent_id: str) -> List[Dict[str, Any]]:
        """
        Agent D retrieves real-time PR discoveries from PCA
        """
        
        agent_context = self.get_agent_context(chain_id, agent_id)
        
        if not agent_context:
            return []
        
        # Get PR discoveries from other agents (primarily Agent A)
        pr_discoveries = []
        
        # Check Agent A context for PR discoveries
        agent_a_context = self.get_agent_context(chain_id, "agent_a_jira_intelligence")
        
        if agent_a_context and 'realtime_pr_discoveries' in agent_a_context:
            for pr_number, pr_data in agent_a_context['realtime_pr_discoveries'].items():
                pr_discoveries.append(pr_data)
        
        logger.info(f"Retrieved {len(pr_discoveries)} PR discoveries for {agent_id}")
        
        return pr_discoveries
    
    def get_realtime_environment_requests(self, chain_id: str, agent_id: str) -> List[Dict[str, Any]]:
        """
        Agent D retrieves real-time environment collection requests from PCA
        """
        
        # Get environment requests from Agent A context
        agent_a_context = self.get_agent_context(chain_id, "agent_a_jira_intelligence")
        
        environment_requests = []
        
        if agent_a_context and 'realtime_environment_requests' in agent_a_context:
            for request_id, request_data in agent_a_context['realtime_environment_requests'].items():
                environment_requests.append(request_data)
        
        logger.info(f"Retrieved {len(environment_requests)} environment requests for {agent_id}")
        
        return environment_requests
    
    def update_environment_collection_results(self, chain_id: str, agent_id: str, 
                                            collection_results: Dict[str, Any]) -> bool:
        """
        Agent D publishes environment collection results back to PCA
        """
        
        results_update = {
            'realtime_environment_collections': collection_results,
            'environment_collection_timestamp': datetime.now().isoformat(),
            'collection_agent': agent_id
        }
        
        success = self.update_agent_context(chain_id, agent_id, results_update)
        
        if success:
            logger.info(f"Environment collection results published by {agent_id}")
        
        return success
    
    def _create_realtime_update_file(self, chain_id: str, update_type: str, data: Any):
        """Create real-time update file for cross-agent monitoring"""
        
        if chain_id not in self.active_phase_coordination:
            return
        
        coordination_dir = self.active_phase_coordination[chain_id]['coordination_dir']
        
        update_file = os.path.join(coordination_dir, f"{update_type}_{datetime.now().strftime('%H%M%S')}.json")
        
        update_data = {
            'update_type': update_type,
            'timestamp': datetime.now().isoformat(),
            'chain_id': chain_id,
            'data': data.__dict__ if hasattr(data, '__dict__') else data
        }
        
        with open(update_file, 'w') as f:
            json.dump(update_data, f, indent=2)
        
        logger.debug(f"Real-time update file created: {update_file}")
    
    def monitor_realtime_updates(self, chain_id: str, agent_id: str, 
                                update_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        Monitor real-time updates from coordination directory
        Agent D can use this to poll for Agent A updates
        """
        
        if chain_id not in self.active_phase_coordination:
            return []
        
        coordination_dir = self.active_phase_coordination[chain_id]['coordination_dir']
        
        if not os.path.exists(coordination_dir):
            return []
        
        updates = []
        update_types = update_types or ['pr_discovery', 'environment_request']
        
        # Scan for update files
        for filename in os.listdir(coordination_dir):
            if not filename.endswith('.json'):
                continue
            
            # Check if this update type is requested
            file_update_type = filename.split('_')[0]
            if file_update_type not in update_types:
                continue
            
            try:
                with open(os.path.join(coordination_dir, filename), 'r') as f:
                    update_data = json.load(f)
                    updates.append(update_data)
            except Exception as e:
                logger.warning(f"Failed to read update file {filename}: {e}")
        
        # Sort by timestamp
        updates.sort(key=lambda x: x.get('timestamp', ''))
        
        logger.info(f"Found {len(updates)} real-time updates for {agent_id}")
        
        return updates
    
    def get_coordination_status(self, chain_id: str) -> Dict[str, Any]:
        """Get real-time coordination status"""
        
        if chain_id not in self.active_phase_coordination:
            return {'coordination_active': False}
        
        coordination_state = self.active_phase_coordination[chain_id]
        
        return {
            'coordination_active': True,
            'phase_name': coordination_state['phase_name'],
            'enabled_at': coordination_state['enabled_at'],
            'last_update': coordination_state['last_update'],
            'agent_a_updates_count': len(coordination_state['agent_a_updates']),
            'agent_d_requests_count': len(coordination_state['agent_d_requests']),
            'coordination_directory': coordination_state['coordination_dir']
        }
    
    def cleanup_realtime_coordination(self, chain_id: str):
        """Cleanup real-time coordination for completed phase"""
        
        if chain_id in self.active_phase_coordination:
            coordination_dir = self.active_phase_coordination[chain_id]['coordination_dir']
            
            # Archive coordination files instead of deleting
            archive_dir = os.path.join(coordination_dir, 'archived')
            os.makedirs(archive_dir, exist_ok=True)
            
            # Move active files to archive
            for filename in os.listdir(coordination_dir):
                if filename.endswith('.json'):
                    src = os.path.join(coordination_dir, filename)
                    dst = os.path.join(archive_dir, filename)
                    try:
                        os.rename(src, dst)
                    except Exception as e:
                        logger.warning(f"Failed to archive {filename}: {e}")
            
            # Remove from active coordination
            del self.active_phase_coordination[chain_id]
            
            logger.info(f"Real-time coordination cleaned up for chain {chain_id}")


# Agent integration mixins for existing agents
class AgentARealtimeMixin:
    """Mixin for Agent A to integrate with enhanced PCA"""
    
    def __init__(self, enhanced_pca: EnhancedProgressiveContextArchitecture, chain_id: str):
        self.enhanced_pca = enhanced_pca
        self.chain_id = chain_id
        self.agent_id = "agent_a_jira_intelligence"
    
    def publish_pr_discovery(self, pr_number: str, pr_title: str, 
                           deployment_components: List[str], yaml_files: List[str] = None,
                           config_changes: List[str] = None, priority: str = "high"):
        """Publish PR discovery using enhanced PCA"""
        
        pr_discovery = RealtimePRDiscovery(
            pr_number=pr_number,
            pr_title=pr_title,
            discovery_timestamp=datetime.now().isoformat(),
            deployment_components=deployment_components,
            yaml_files=yaml_files or [],
            config_changes=config_changes or [],
            environment_collection_required=True,
            priority=priority
        )
        
        return self.enhanced_pca.publish_pr_discovery_realtime(
            self.chain_id, self.agent_id, pr_discovery
        )
    
    def request_environment_collection(self, pr_context: RealtimePRDiscovery,
                                     required_yamls: List[str] = None,
                                     required_logs: List[str] = None,
                                     required_commands: List[str] = None,
                                     priority: str = "high"):
        """Request environment collection using enhanced PCA"""
        
        import uuid
        
        collection_request = EnvironmentCollectionRequest(
            request_id=uuid.uuid4().hex[:8],
            pr_context=pr_context,
            required_yamls=required_yamls or [],
            required_logs=required_logs or [],
            required_commands=required_commands or [],
            collection_priority=priority,
            immediate_action=True
        )
        
        return self.enhanced_pca.publish_environment_collection_request(
            self.chain_id, self.agent_id, collection_request
        )


class AgentDRealtimeMixin:
    """Mixin for Agent D to integrate with enhanced PCA"""
    
    def __init__(self, enhanced_pca: EnhancedProgressiveContextArchitecture, chain_id: str):
        self.enhanced_pca = enhanced_pca
        self.chain_id = chain_id
        self.agent_id = "agent_d_environment_intelligence"
    
    def get_pr_discoveries(self) -> List[Dict[str, Any]]:
        """Get PR discoveries from Agent A via enhanced PCA"""
        return self.enhanced_pca.get_realtime_pr_discoveries(self.chain_id, self.agent_id)
    
    def get_environment_requests(self) -> List[Dict[str, Any]]:
        """Get environment collection requests from Agent A via enhanced PCA"""
        return self.enhanced_pca.get_realtime_environment_requests(self.chain_id, self.agent_id)
    
    def monitor_agent_a_updates(self) -> List[Dict[str, Any]]:
        """Monitor real-time updates from Agent A"""
        return self.enhanced_pca.monitor_realtime_updates(
            self.chain_id, self.agent_id, ['pr_discovery', 'environment_request']
        )
    
    def publish_collection_results(self, collection_results: Dict[str, Any]):
        """Publish environment collection results back to PCA"""
        return self.enhanced_pca.update_environment_collection_results(
            self.chain_id, self.agent_id, collection_results
        )


if __name__ == '__main__':
    # Test enhanced PCA with real-time coordination
    import asyncio
    
    async def test_enhanced_pca_realtime():
        """Test enhanced PCA real-time coordination"""
        print("🧪 Testing Enhanced PCA Real-Time Coordination")
        
        # Create enhanced PCA
        enhanced_pca = EnhancedProgressiveContextArchitecture()
        
        # Create mock inheritance chain
        from progressive_context_setup import ContextInheritanceChain
        
        # Mock foundation context
        mock_foundation = type('MockFoundation', (), {
            'jira_info': type('JiraInfo', (), {'jira_id': 'ACM-22079'})()
        })()
        
        inheritance_chain = ContextInheritanceChain(
            foundation_context=mock_foundation,
            agent_contexts={
                'agent_a_jira_intelligence': {'jira_id': 'ACM-22079'},
                'agent_d_environment_intelligence': {'jira_id': 'ACM-22079'}
            },
            inheritance_metadata={'chain_id': 'test_chain_001'},
            validation_results={'all_valid': True}
        )
        
        # Add to active chains
        chain_id = 'test_chain_001'
        enhanced_pca.active_chains[chain_id] = inheritance_chain
        
        # Enable real-time coordination
        enhanced_pca.enable_realtime_coordination(chain_id, "Phase 1 Test")
        
        # Create agent mixins
        agent_a_mixin = AgentARealtimeMixin(enhanced_pca, chain_id)
        agent_d_mixin = AgentDRealtimeMixin(enhanced_pca, chain_id)
        
        # Test Agent A publishing PR discovery
        print("Agent A publishing PR discovery...")
        agent_a_mixin.publish_pr_discovery(
            pr_number="468",
            pr_title="ClusterCurator digest-based upgrades",
            deployment_components=["ClusterCurator", "Controller"],
            yaml_files=["clustercurator.yaml"],
            priority="high"
        )
        
        # Test Agent D retrieving PR discoveries
        print("Agent D retrieving PR discoveries...")
        pr_discoveries = agent_d_mixin.get_pr_discoveries()
        print(f"Agent D found {len(pr_discoveries)} PR discoveries")
        
        if pr_discoveries:
            print(f"PR {pr_discoveries[0]['pr_number']}: {pr_discoveries[0]['pr_title']}")
        
        # Test real-time monitoring
        print("Testing real-time update monitoring...")
        updates = agent_d_mixin.monitor_agent_a_updates()
        print(f"Agent D found {len(updates)} real-time updates")
        
        # Get coordination status
        status = enhanced_pca.get_coordination_status(chain_id)
        print(f"Coordination status: {status}")
        
        # Cleanup
        enhanced_pca.cleanup_realtime_coordination(chain_id)
        
        print("✅ Enhanced PCA real-time coordination test completed!")
    
    asyncio.run(test_enhanced_pca_realtime())