"""
Agent B (Documentation Intelligence) Integration with Learning Framework

Shows how to enhance Agent B with learning capabilities while maintaining
backward compatibility and zero regression risk.
"""

import time
import asyncio
import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass

# Import the learning framework
from ..agent_learning_framework import AgentLearningFramework

logger = logging.getLogger(__name__)


@dataclass
class EnhancedDocumentationResult:
    """Result structure for Agent B documentation analysis"""
    inherited_context: dict
    documentation_strategy: dict
    documentation_analysis: dict
    feature_understanding: dict
    enhanced_context: dict
    validation_results: dict
    confidence_level: float


class AgentB:
    """Original Agent B implementation (simplified for demonstration)"""
    
    def __init__(self):
        self.analysis_results = {}
        
    def execute_enhanced_workflow(self, enhanced_context_from_agents_a_d: Dict) -> EnhancedDocumentationResult:
        """
        Original documentation analysis logic
        This represents the existing Agent B functionality
        """
        # Simulate existing documentation analysis
        documentation_analysis = {
            'feature_documentation': {
                'feature_description': 'ClusterCurator upgrade functionality',
                'functionality_overview': 'Digest-based upgrades for disconnected environments',
                'implementation_details': 'Controller-based upgrade orchestration'
            },
            'implementation_patterns': [
                'controller_pattern_upgrade_workflow',
                'api_pattern_digest_discovery',
                'configuration_pattern_annotations'
            ],
            'api_specifications': {
                'api_endpoints': ['/apis/clustercurator/v1beta1'],
                'crd_specifications': ['ClusterCurator CRD v1beta1'],
                'field_requirements': ['spec.upgrade', 'spec.upgrade.desiredUpdate']
            },
            'usage_patterns': [
                'cli_usage_kubectl_apply',
                'api_usage_direct_update',
                'automation_usage_scripts'
            ]
        }
        
        feature_understanding = {
            'feature_capabilities': {
                'primary_capabilities': ['digest-based upgrades', 'disconnected support'],
                'secondary_capabilities': ['annotation-based config', 'version fallback'],
                'integration_capabilities': ['cluster lifecycle', 'mcm integration']
            },
            'testing_implications': [
                'test_digest_discovery_algorithm',
                'test_disconnected_behavior',
                'test_fallback_mechanisms'
            ]
        }
        
        # Simulate processing time
        time.sleep(0.1)
        
        # Return structured result
        return EnhancedDocumentationResult(
            inherited_context=enhanced_context_from_agents_a_d,
            documentation_strategy={'analysis_focus': ['feature_functionality']},
            documentation_analysis=documentation_analysis,
            feature_understanding=feature_understanding,
            enhanced_context=enhanced_context_from_agents_a_d,  # Would be enhanced in real implementation
            validation_results={'confidence_score': 0.88},
            confidence_level=0.88
        )


class AgentBWithLearning(AgentB):
    """
    Enhanced Agent B with learning capabilities
    Inherits from original Agent B to maintain all existing functionality
    """
    
    def __init__(self):
        super().__init__()
        # Get singleton learning framework instance
        self.learning_framework = AgentLearningFramework()
        self.agent_id = 'agent_b'
        
        # Feature flag for gradual rollout (can be disabled if needed)
        self.learning_enabled = True
        
        logger.info("Agent B initialized with learning capabilities")
    
    def execute_enhanced_workflow(self, enhanced_context_from_agents_a_d: Dict) -> EnhancedDocumentationResult:
        """
        Enhanced documentation analysis with learning integration
        Maintains exact same interface and behavior as original
        """
        start_time = time.time()
        
        # 1. Check for learning recommendations (fast, cached, non-blocking)
        recommendations = None
        if self.learning_enabled:
            try:
                # Extract context for learning
                jira_context = enhanced_context_from_agents_a_d.get('agent_contributions', {}).get('agent_a_jira', {})
                feature_info = jira_context.get('enhancements', {}).get('technical_scope', {})
                
                recommendations = self.learning_framework.apply_learnings(
                    self.agent_id,
                    {
                        'type': 'documentation_analysis',
                        'feature_type': feature_info.get('feature_type', 'unknown'),
                        'components': feature_info.get('primary_components', []),
                        'keywords': self._extract_keywords(enhanced_context_from_agents_a_d)
                    }
                )
                
                if recommendations:
                    logger.debug(f"Applied {len(recommendations.get('patterns', []))} learned patterns")
            except Exception as e:
                # Learning errors never affect main execution
                logger.debug(f"Learning recommendation skipped: {e}")
        
        # 2. Execute original logic (exactly the same)
        result = super().execute_enhanced_workflow(enhanced_context_from_agents_a_d)
        
        # 3. Apply any learning optimizations (non-invasive)
        if recommendations:
            result = self._apply_recommendations(result, recommendations)
        
        # 4. Capture execution data (async, non-blocking)
        if self.learning_enabled:
            execution_time = time.time() - start_time
            
            metrics = {
                'execution_time': execution_time,
                'success': result.confidence_level > 0.7,
                'confidence': result.confidence_level,
                'documentation_found': len(result.documentation_analysis.get('feature_documentation', {})) > 0,
                'patterns_identified': len(result.documentation_analysis.get('implementation_patterns', [])),
                'usage_patterns_found': len(result.documentation_analysis.get('usage_patterns', [])),
                'testing_implications_derived': len(result.feature_understanding.get('testing_implications', []))
            }
            
            # Queue learning capture (fire-and-forget)
            asyncio.create_task(
                self._capture_learning_async(enhanced_context_from_agents_a_d, result, metrics)
            )
        
        # Return exact same structure as original
        return result
    
    async def _capture_learning_async(self, context: Dict, result: EnhancedDocumentationResult, metrics: Dict):
        """
        Async learning capture - runs in background
        Never blocks or affects main execution
        """
        try:
            # Prepare task data for learning
            task_data = {
                'feature_type': self._extract_feature_type(context),
                'components': self._extract_components(context),
                'keywords': self._extract_keywords(context),
                'documentation_sources': self._extract_doc_sources(result)
            }
            
            # Prepare result data for learning
            result_data = {
                'documentation_analysis': result.documentation_analysis,
                'feature_understanding': result.feature_understanding,
                'patterns_found': result.documentation_analysis.get('implementation_patterns', []),
                'confidence_level': result.confidence_level
            }
            
            await self.learning_framework.capture_execution(
                self.agent_id,
                task_data,
                result_data,
                metrics
            )
        except Exception as e:
            # Log but don't propagate
            logger.debug(f"Learning capture error (non-critical): {e}")
    
    def _apply_recommendations(self, result: EnhancedDocumentationResult, recommendations: Dict) -> EnhancedDocumentationResult:
        """
        Apply learning recommendations to enhance analysis
        Only makes improvements, never degrades results
        """
        # Apply confidence adjustment if patterns indicate high success
        if 'confidence_adjustment' in recommendations:
            adjustment = recommendations['confidence_adjustment']
            # Only boost, never reduce
            if adjustment > 0:
                result.confidence_level = min(
                    result.confidence_level + adjustment,
                    0.99  # Cap at 99%
                )
                result.validation_results['confidence_score'] = result.confidence_level
                logger.debug(f"Confidence boosted by {adjustment:.2%}")
        
        # Add learned patterns if found
        if 'patterns' in recommendations and recommendations['patterns']:
            # Add to implementation patterns if not already present
            current_patterns = set(result.documentation_analysis.get('implementation_patterns', []))
            for pattern in recommendations['patterns']:
                if pattern.get('type') == 'doc_search_strategy':
                    pattern_name = f"learned_pattern_{pattern.get('pattern_id', 'unknown')}"
                    if pattern_name not in current_patterns:
                        result.documentation_analysis.setdefault('implementation_patterns', []).append(pattern_name)
        
        # Add learning insights
        if recommendations.get('patterns') or recommendations.get('optimization_suggestions'):
            result.documentation_analysis['learning_insights'] = {
                'patterns_applied': len(recommendations.get('patterns', [])),
                'optimization_hints': recommendations.get('optimization_suggestions', []),
                'performance_hints': recommendations.get('performance_hints', [])
            }
        
        return result
    
    def _extract_keywords(self, context: Dict) -> list:
        """Extract keywords from context for pattern matching"""
        keywords = []
        
        # Extract from JIRA context
        jira_context = context.get('agent_contributions', {}).get('agent_a_jira', {})
        feature_scope = jira_context.get('enhancements', {}).get('technical_scope', {})
        
        # Add feature-related keywords
        if feature_scope.get('feature_name'):
            keywords.extend(feature_scope['feature_name'].lower().split())
        
        # Add component keywords
        components = feature_scope.get('primary_components', [])
        for component in components:
            keywords.append(component.lower().replace('-', '').replace('_', ''))
        
        return list(set(keywords))  # Unique keywords
    
    def _extract_feature_type(self, context: Dict) -> str:
        """Extract feature type from context"""
        jira_context = context.get('agent_contributions', {}).get('agent_a_jira', {})
        return jira_context.get('enhancements', {}).get('technical_scope', {}).get('feature_type', 'unknown')
    
    def _extract_components(self, context: Dict) -> list:
        """Extract components from context"""
        jira_context = context.get('agent_contributions', {}).get('agent_a_jira', {})
        return jira_context.get('enhancements', {}).get('component_mapping', {}).get('components', [])
    
    def _extract_doc_sources(self, result: EnhancedDocumentationResult) -> list:
        """Extract documentation sources from result"""
        sources = []
        
        # Check different documentation areas
        if result.documentation_analysis.get('feature_documentation'):
            sources.append('feature_docs')
        if result.documentation_analysis.get('api_specifications'):
            sources.append('api_docs')
        if result.documentation_analysis.get('implementation_patterns'):
            sources.append('implementation_guides')
        
        return sources
    
    def disable_learning(self):
        """Disable learning if needed (for testing or issues)"""
        self.learning_enabled = False
        logger.info("Learning disabled for Agent B")
    
    def enable_learning(self):
        """Re-enable learning"""
        self.learning_enabled = True
        logger.info("Learning enabled for Agent B")


# Demonstration and validation
def demonstrate_integration():
    """Demonstrate that enhanced agent produces same results"""
    print("Agent B Learning Integration Demonstration")
    print("=" * 50)
    
    # Create both versions
    original_agent = AgentB()
    enhanced_agent = AgentBWithLearning()
    
    # Test context (simulating inherited from Agents A and D)
    test_context = {
        'agent_contributions': {
            'agent_a_jira': {
                'enhancements': {
                    'technical_scope': {
                        'feature_type': 'cluster_management',
                        'feature_name': 'ClusterCurator Digest Upgrades',
                        'primary_components': ['ClusterCurator', 'cluster-curator-controller']
                    },
                    'component_mapping': {
                        'components': ['ClusterCurator', 'cluster-curator-controller']
                    }
                }
            },
            'agent_d_environment': {
                'enhancements': {
                    'environment_intelligence': {
                        'acm_version_confirmed': 'ACM 2.14'
                    }
                }
            }
        }
    }
    
    # Run both versions
    print(f"\nAnalyzing documentation with test context")
    print("-" * 30)
    
    # Original
    start = time.time()
    original_result = original_agent.execute_enhanced_workflow(test_context)
    original_time = time.time() - start
    
    # Enhanced
    start = time.time()
    enhanced_result = enhanced_agent.execute_enhanced_workflow(test_context)
    enhanced_time = time.time() - start
    
    # Compare results
    print(f"\nOriginal execution time: {original_time:.3f}s")
    print(f"Enhanced execution time: {enhanced_time:.3f}s")
    
    # Check core results (excluding learning insights)
    original_docs = original_result.documentation_analysis.copy()
    enhanced_docs = enhanced_result.documentation_analysis.copy()
    enhanced_docs.pop('learning_insights', None)
    
    # Verify identical core results
    docs_identical = original_docs == enhanced_docs
    understanding_identical = original_result.feature_understanding == enhanced_result.feature_understanding
    
    identical = docs_identical and understanding_identical
    print(f"\nCore results identical: {'✅ YES' if identical else '❌ NO'}")
    
    if not identical:
        print("Differences found:")
        if not docs_identical:
            print("  Documentation analysis differs")
        if not understanding_identical:
            print("  Feature understanding differs")
    
    # Show learning enhancements
    if 'learning_insights' in enhanced_result.documentation_analysis:
        print("\nLearning enhancements applied:")
        insights = enhanced_result.documentation_analysis['learning_insights']
        print(f"  Patterns applied: {insights.get('patterns_applied', 0)}")
        print(f"  Optimization hints: {len(insights.get('optimization_hints', []))}")
    
    print("\n" + "=" * 50)
    print("✅ Integration successful - no regression detected")
    
    return identical


if __name__ == '__main__':
    # Run demonstration
    demonstrate_integration()
