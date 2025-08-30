#!/usr/bin/env python3
"""
Progressive Context Architecture Setup - Phase 1 Final Component
Establishes the framework for context inheritance across the 4-agent system
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

from foundation_context import FoundationContext, ContextMetadata
from version_intelligence_service import VersionIntelligenceService

# Import context manager for token counting
import sys
sys.path.append('../../src')
try:
    from context.context_manager import ContextManager, ContextItemType, create_framework_context_manager, get_importance_score
    CONTEXT_MANAGER_AVAILABLE = True
except ImportError:
    CONTEXT_MANAGER_AVAILABLE = False
    print("Warning: Context Manager not available, using legacy context tracking")

logger = logging.getLogger(__name__)


@dataclass
class AgentContextRequirements:
    """Requirements for agent context inheritance"""
    agent_name: str
    agent_type: str
    required_context_fields: List[str]
    context_inheritance_level: str  # "full", "partial", "minimal"
    context_validation_required: bool = True
    context_enrichment_needed: bool = False


@dataclass
class ContextInheritanceChain:
    """Defines context inheritance chain across framework phases"""
    foundation_context: FoundationContext
    agent_contexts: Dict[str, Dict[str, Any]]
    inheritance_metadata: Dict[str, Any]
    validation_results: Dict[str, bool]
    chain_integrity: bool = False
    
    # Enhanced context management (Factor 3)
    context_manager: Optional[Any] = None  # ContextManager instance
    total_tokens: int = 0
    token_budget_allocation: Dict[str, int] = None
    context_compression_applied: bool = False
    
    def __post_init__(self):
        if not self.agent_contexts:
            self.agent_contexts = {}
        if not self.inheritance_metadata:
            self.inheritance_metadata = {}
        if not self.validation_results:
            self.validation_results = {}
        if not self.token_budget_allocation:
            self.token_budget_allocation = {}
    
    def get_agent_context(self, agent_id: str) -> Dict[str, Any]:
        """Get context for specific agent with token tracking"""
        return self.agent_contexts.get(agent_id, {})
    
    def merge_contexts(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Merge contexts from multiple agents with token management"""
        merged = {}
        for agent_id in agent_ids:
            if agent_id in self.agent_contexts:
                merged.update(self.agent_contexts[agent_id])
        return merged
    
    def add_agent_context(self, agent_id: str, context_data: Dict[str, Any], importance: float = 0.8):
        """Add agent context with intelligent token management"""
        self.agent_contexts[agent_id] = context_data
        
        # Add to context manager if available
        if self.context_manager and CONTEXT_MANAGER_AVAILABLE:
            context_str = json.dumps(context_data, default=str)
            self.context_manager.add_context(
                content=context_str,
                importance=importance,
                item_type=ContextItemType.AGENT_OUTPUT,
                source=agent_id,
                metadata={"agent_id": agent_id, "context_size": len(context_str)}
            )
            
            # Update token tracking
            metrics = self.context_manager.get_context_summary()
            self.total_tokens = metrics.total_tokens
            self.context_compression_applied = metrics.compression_savings > 0


class ProgressiveContextArchitecture:
    """
    Progressive Context Architecture implementation for the 4-agent framework
    Provides systematic context inheritance with intelligent conflict resolution
    """
    
    def __init__(self, framework_root: str = None, enable_context_management: bool = True):
        self.framework_root = framework_root or os.getcwd()
        self.context_dir = Path(self.framework_root) / ".claude" / "context"
        self.context_dir.mkdir(parents=True, exist_ok=True)
        
        # Agent configuration
        self.agent_configurations = self._load_agent_configurations()
        
        # Context inheritance chains
        self.active_chains: Dict[str, ContextInheritanceChain] = {}
        
        # Initialize context manager (Factor 3)
        self.context_management_enabled = enable_context_management and CONTEXT_MANAGER_AVAILABLE
        if self.context_management_enabled:
            self.context_manager = create_framework_context_manager()
            logger.info("Progressive Context Architecture initialized with intelligent context management")
        else:
            self.context_manager = None
            logger.info("Progressive Context Architecture initialized (legacy mode)")
    
    def _load_agent_configurations(self) -> Dict[str, AgentContextRequirements]:
        """Load agent context requirements for the 4-agent system"""
        
        return {
            'agent_a_jira_intelligence': AgentContextRequirements(
                agent_name='Agent A - JIRA Intelligence',
                agent_type='jira_intelligence',
                required_context_fields=[
                    'jira_id', 'jira_title', 'jira_status', 'target_version', 
                    'priority', 'component', 'deployment_instruction'
                ],
                context_inheritance_level='full',
                context_validation_required=True,
                context_enrichment_needed=True
            ),
            'agent_b_documentation_intelligence': AgentContextRequirements(
                agent_name='Agent B - Documentation Intelligence',
                agent_type='documentation_intelligence',
                required_context_fields=[
                    'jira_id', 'target_version', 'component', 'environment_platform',
                    'deployment_instruction', 'agent_a_findings'
                ],
                context_inheritance_level='full',
                context_validation_required=True,
                context_enrichment_needed=True
            ),
            'agent_c_github_investigation': AgentContextRequirements(
                agent_name='Agent C - GitHub Investigation',
                agent_type='github_investigation',
                required_context_fields=[
                    'jira_id', 'target_version', 'component', 'environment_platform',
                    'deployment_instruction', 'agent_a_findings'
                ],
                context_inheritance_level='full',
                context_validation_required=True,
                context_enrichment_needed=True
            ),
            'agent_d_environment_intelligence': AgentContextRequirements(
                agent_name='Agent D - Environment Intelligence',
                agent_type='environment_intelligence',
                required_context_fields=[
                    'jira_id', 'target_version', 'environment_version', 'cluster_name',
                    'platform', 'health_status', 'deployment_instruction'
                ],
                context_inheritance_level='full',
                context_validation_required=True,
                context_enrichment_needed=True
            )
        }
    
    def create_foundation_context_for_jira(self, jira_id: str, environment: str = None) -> FoundationContext:
        """Create foundation context optimized for Progressive Context Architecture"""
        
        logger.info(f"Creating Progressive Context Architecture foundation for {jira_id}")
        
        # Use Version Intelligence Service to create foundation
        vis = VersionIntelligenceService()
        foundation_context = vis.create_foundation_context(jira_id, environment)
        
        # Enhance foundation context for Progressive Context Architecture
        enhanced_context = self._enhance_foundation_for_pca(foundation_context)
        
        # Validate context readiness for agent inheritance
        if enhanced_context.is_ready_for_agent_inheritance():
            logger.info(f"✅ Foundation context ready for Progressive Context Architecture")
            return enhanced_context
        else:
            logger.error(f"❌ Foundation context not ready for agent inheritance")
            raise ValueError(f"Foundation context validation failed for {jira_id}")
    
    def _enhance_foundation_for_pca(self, foundation_context: FoundationContext) -> FoundationContext:
        """Enhance foundation context with Progressive Context Architecture metadata"""
        
        # Add PCA-specific metadata
        foundation_context.metadata.context_version = "1.1.0-pca"
        foundation_context.metadata.pca_enabled = True
        foundation_context.metadata.agent_inheritance_ready = True
        
        # Add context management metadata (Factor 3)
        if self.context_management_enabled:
            foundation_context.metadata.context_management_enabled = True
            foundation_context.metadata.max_tokens = self.context_manager.max_tokens
            foundation_context.metadata.compression_threshold = self.context_manager.compression_threshold
            
            # Add foundation context to context manager
            foundation_str = json.dumps(foundation_context.get_agent_context_summary(), default=str)
            importance_score = get_importance_score("foundation_context", "progressive_context_architecture")
            
            self.context_manager.add_context(
                content=foundation_str,
                importance=importance_score,
                item_type=ContextItemType.FOUNDATION,
                source="progressive_context_architecture",
                metadata={
                    "jira_id": foundation_context.jira_info.jira_id,
                    "context_type": "foundation",
                    "enhancement_timestamp": datetime.now().isoformat()
                }
            )
            
            # Get initial metrics
            metrics = self.context_manager.get_context_summary()
            foundation_context.metadata.initial_token_count = metrics.total_tokens
            foundation_context.metadata.initial_budget_utilization = metrics.budget_utilization
            
            logger.info(f"Foundation context added to context manager: {metrics.total_tokens:,} tokens ({metrics.budget_utilization:.1%} utilization)")
        else:
            foundation_context.metadata.context_management_enabled = False
        
        # Add agent-specific context summaries
        agent_context_summary = foundation_context.get_agent_context_summary()
        
        # Enhance with agent-specific data preparation
        agent_context_summary.update({
            'pca_metadata': {
                'context_chain_id': f"pca_{foundation_context.jira_info.jira_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'agent_inheritance_ready': True,
                'context_inheritance_level': 'full',
                'context_validation_passed': True,
                'agent_count': 4,
                'expected_agents': ['agent_a', 'agent_b', 'agent_c', 'agent_d']
            },
            'agent_a_context': {
                'focus': 'JIRA ticket analysis and requirements extraction',
                'required_fields': self.agent_configurations['agent_a_jira_intelligence'].required_context_fields,
                'context_ready': True
            },
            'agent_b_context': {
                'focus': 'Documentation discovery and analysis',
                'required_fields': self.agent_configurations['agent_b_documentation_intelligence'].required_context_fields,
                'context_ready': True
            },
            'agent_c_context': {
                'focus': 'GitHub code investigation and PR analysis',
                'required_fields': self.agent_configurations['agent_c_github_investigation'].required_context_fields,
                'context_ready': True
            },
            'agent_d_context': {
                'focus': 'Environment assessment and tooling analysis',
                'required_fields': self.agent_configurations['agent_d_environment_intelligence'].required_context_fields,
                'context_ready': True
            }
        })
        
        # Store enhanced context summary
        foundation_context._pca_agent_context_summary = agent_context_summary
        
        return foundation_context
    
    def initialize_context_inheritance_chain(self, foundation_context: FoundationContext) -> ContextInheritanceChain:
        """Initialize context inheritance chain for the 4-agent framework"""
        
        chain_id = foundation_context._pca_agent_context_summary['pca_metadata']['context_chain_id']
        
        logger.info(f"Initializing context inheritance chain: {chain_id}")
        
        # Create inheritance chain
        inheritance_chain = ContextInheritanceChain(
            foundation_context=foundation_context,
            agent_contexts={},
            inheritance_metadata={
                'chain_id': chain_id,
                'created_at': datetime.now().isoformat(),
                'foundation_jira_id': foundation_context.jira_info.jira_id,
                'agent_count': 4,
                'inheritance_level': 'full',
                'validation_required': True,
                'context_management_enabled': self.context_management_enabled
            },
            validation_results={},
            context_manager=self.context_manager if self.context_management_enabled else None
        )
        
        # Prepare agent contexts
        inheritance_chain.agent_contexts = self._prepare_agent_contexts(foundation_context)
        
        # Validate inheritance chain integrity
        inheritance_chain.chain_integrity = self._validate_inheritance_chain(inheritance_chain)
        
        # Store active chain
        self.active_chains[chain_id] = inheritance_chain
        
        # Save chain to disk for persistence
        self._save_inheritance_chain(inheritance_chain)
        
        logger.info(f"✅ Context inheritance chain initialized successfully")
        
        return inheritance_chain
    
    def _prepare_agent_contexts(self, foundation_context: FoundationContext) -> Dict[str, Dict[str, Any]]:
        """Prepare individual agent contexts from foundation context"""
        
        base_context = foundation_context.get_agent_context_summary()
        agent_contexts = {}
        
        for agent_key, agent_config in self.agent_configurations.items():
            logger.info(f"Preparing context for {agent_config.agent_name}")
            
            # Extract relevant fields for this agent
            agent_context = {}
            for field in agent_config.required_context_fields:
                if field in base_context:
                    agent_context[field] = base_context[field]
                elif field in foundation_context.jira_info.__dict__:
                    agent_context[field] = getattr(foundation_context.jira_info, field)
                elif field in foundation_context.version_context.__dict__:
                    agent_context[field] = getattr(foundation_context.version_context, field)
                elif field in foundation_context.environment_baseline.__dict__:
                    agent_context[field] = getattr(foundation_context.environment_baseline, field)
                else:
                    # Provide sensible defaults for missing fields
                    agent_context[field] = self._get_default_value_for_field(field, foundation_context)
            
            # Add agent-specific metadata
            agent_context['agent_metadata'] = {
                'agent_name': agent_config.agent_name,
                'agent_type': agent_config.agent_type,
                'inheritance_level': agent_config.context_inheritance_level,
                'context_validation_required': agent_config.context_validation_required,
                'context_enrichment_needed': agent_config.context_enrichment_needed,
                'context_inherited_at': datetime.now().isoformat(),
                'foundation_context_id': foundation_context.jira_info.jira_id
            }
            
            # Add context validation
            agent_context['context_validation'] = {
                'required_fields_present': all(field in agent_context for field in agent_config.required_context_fields),
                'context_completeness_score': len(agent_context) / len(agent_config.required_context_fields),
                'validation_passed': True,  # Will be updated during validation
                'validation_timestamp': datetime.now().isoformat()
            }
            
            agent_contexts[agent_key] = agent_context
        
        return agent_contexts
    
    def _get_default_value_for_field(self, field: str, foundation_context: FoundationContext) -> Any:
        """Get sensible default values for missing context fields"""
        
        defaults = {
            'agent_a_findings': {},
            'agent_b_findings': {},
            'agent_c_findings': {},
            'agent_d_findings': {},
            'environment_platform': foundation_context.environment_baseline.platform,
            'cluster_name': foundation_context.environment_baseline.cluster_name,
            'health_status': foundation_context.environment_baseline.health_status
        }
        
        return defaults.get(field, f"auto_generated_{field}")
    
    def _validate_inheritance_chain(self, inheritance_chain: ContextInheritanceChain) -> bool:
        """Validate context inheritance chain integrity"""
        
        logger.info("Validating context inheritance chain integrity")
        
        validation_results = {}
        
        # Validate foundation context
        foundation_valid = inheritance_chain.foundation_context.is_ready_for_agent_inheritance()
        validation_results['foundation_context'] = foundation_valid
        
        # Validate each agent context
        for agent_key, agent_context in inheritance_chain.agent_contexts.items():
            agent_config = self.agent_configurations[agent_key]
            
            # Check required fields
            required_fields_present = all(
                field in agent_context for field in agent_config.required_context_fields
            )
            
            # Check context completeness
            completeness_score = agent_context['context_validation']['context_completeness_score']
            context_complete = completeness_score >= 0.8  # 80% completeness threshold
            
            agent_valid = required_fields_present and context_complete
            validation_results[agent_key] = agent_valid
            
            # Update agent context validation
            agent_context['context_validation']['validation_passed'] = agent_valid
            
            logger.info(f"Agent {agent_key} validation: {'✅' if agent_valid else '❌'}")
        
        # Overall chain integrity
        chain_integrity = all(validation_results.values())
        
        # Store validation results
        inheritance_chain.validation_results = validation_results
        
        logger.info(f"Context inheritance chain integrity: {'✅' if chain_integrity else '❌'}")
        
        return chain_integrity
    
    def _save_inheritance_chain(self, inheritance_chain: ContextInheritanceChain):
        """Save inheritance chain to disk for persistence"""
        
        chain_id = inheritance_chain.inheritance_metadata['chain_id']
        jira_id = inheritance_chain.foundation_context.jira_info.jira_id
        
        # Create JIRA-specific context directory
        jira_context_dir = self.context_dir / jira_id
        jira_context_dir.mkdir(exist_ok=True)
        
        # Save inheritance chain
        chain_file = jira_context_dir / f"{chain_id}.json"
        
        try:
            chain_data = {
                'inheritance_metadata': inheritance_chain.inheritance_metadata,
                'validation_results': inheritance_chain.validation_results,
                'chain_integrity': inheritance_chain.chain_integrity,
                'agent_contexts': inheritance_chain.agent_contexts,
                'foundation_context_summary': inheritance_chain.foundation_context.get_agent_context_summary(),
                'saved_at': datetime.now().isoformat()
            }
            
            with open(chain_file, 'w') as f:
                json.dump(chain_data, f, indent=2)
            
            logger.info(f"Context inheritance chain saved: {chain_file}")
            
        except Exception as e:
            logger.error(f"Failed to save inheritance chain: {e}")
    
    def get_agent_context(self, chain_id: str, agent_key: str) -> Optional[Dict[str, Any]]:
        """Get specific agent context from inheritance chain"""
        
        if chain_id not in self.active_chains:
            logger.error(f"Chain {chain_id} not found in active chains")
            return None
        
        inheritance_chain = self.active_chains[chain_id]
        
        if agent_key not in inheritance_chain.agent_contexts:
            logger.error(f"Agent {agent_key} not found in chain {chain_id}")
            return None
        
        agent_context = inheritance_chain.agent_contexts[agent_key]
        
        logger.info(f"Retrieved context for {agent_key} from chain {chain_id}")
        
        return agent_context
    
    def update_agent_context(self, chain_id: str, agent_key: str, updates: Dict[str, Any]) -> bool:
        """Update agent context with new findings/data"""
        
        if chain_id not in self.active_chains:
            logger.error(f"Chain {chain_id} not found")
            return False
        
        inheritance_chain = self.active_chains[chain_id]
        
        if agent_key not in inheritance_chain.agent_contexts:
            logger.error(f"Agent {agent_key} not found in chain")
            return False
        
        # Update agent context
        agent_context = inheritance_chain.agent_contexts[agent_key]
        agent_context.update(updates)
        
        # Update metadata
        agent_context['agent_metadata']['last_updated'] = datetime.now().isoformat()
        
        # Re-save inheritance chain
        self._save_inheritance_chain(inheritance_chain)
        
        logger.info(f"Updated context for {agent_key} in chain {chain_id}")
        
        return True
    
    def get_chain_status(self, chain_id: str) -> Dict[str, Any]:
        """Get comprehensive status of inheritance chain"""
        
        if chain_id not in self.active_chains:
            return {'error': f'Chain {chain_id} not found'}
        
        inheritance_chain = self.active_chains[chain_id]
        
        return {
            'chain_id': chain_id,
            'foundation_jira_id': inheritance_chain.foundation_context.jira_info.jira_id,
            'chain_integrity': inheritance_chain.chain_integrity,
            'validation_results': inheritance_chain.validation_results,
            'agent_count': len(inheritance_chain.agent_contexts),
            'agents_ready': sum(1 for ctx in inheritance_chain.agent_contexts.values() 
                              if ctx['context_validation']['validation_passed']),
            'creation_time': inheritance_chain.inheritance_metadata['created_at'],
            'all_agents_ready': inheritance_chain.chain_integrity
        }


# Convenience functions for external use
def setup_progressive_context_for_jira(jira_id: str, environment: str = None) -> ContextInheritanceChain:
    """Setup complete Progressive Context Architecture for JIRA ticket"""
    
    pca = ProgressiveContextArchitecture()
    
    # Create foundation context
    foundation_context = pca.create_foundation_context_for_jira(jira_id, environment)
    
    # Initialize inheritance chain
    inheritance_chain = pca.initialize_context_inheritance_chain(foundation_context)
    
    return inheritance_chain


def get_agent_context_for_jira(jira_id: str, agent_key: str) -> Optional[Dict[str, Any]]:
    """Get agent context for specific JIRA ticket"""
    
    pca = ProgressiveContextArchitecture()
    
    # Find active chain for this JIRA ID
    for chain_id, chain in pca.active_chains.items():
        if chain.foundation_context.jira_info.jira_id == jira_id:
            return pca.get_agent_context(chain_id, agent_key)
    
    logger.warning(f"No active context chain found for JIRA {jira_id}")
    return None


if __name__ == "__main__":
    # Example usage and testing
    import sys
    
    if len(sys.argv) > 1:
        jira_id = sys.argv[1]
        environment = sys.argv[2] if len(sys.argv) > 2 else None
        
        print(f"🏗️  Setting up Progressive Context Architecture for {jira_id}...")
        
        try:
            # Setup complete PCA
            inheritance_chain = setup_progressive_context_for_jira(jira_id, environment)
            
            chain_id = inheritance_chain.inheritance_metadata['chain_id']
            
            print(f"✅ Progressive Context Architecture setup complete!")
            print(f"🔗 Chain ID: {chain_id}")
            print(f"🧠 Chain Integrity: {'✅' if inheritance_chain.chain_integrity else '❌'}")
            print(f"👥 Agent Contexts: {len(inheritance_chain.agent_contexts)}")
            
            # Show agent readiness
            for agent_key, agent_context in inheritance_chain.agent_contexts.items():
                ready = agent_context['context_validation']['validation_passed']
                print(f"   🤖 {agent_key}: {'✅' if ready else '❌'}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        print("Usage: python progressive_context_setup.py <JIRA_ID> [environment]")
        print("Example: python progressive_context_setup.py ACM-22079 test-cluster")
        sys.exit(1)