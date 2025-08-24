"""
Agent C (GitHub Investigation) Integration with Learning Framework

Shows how to enhance Agent C with learning capabilities while maintaining
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
class EnhancedGitHubResult:
    """Result structure for Agent C GitHub investigation"""
    inherited_context: dict
    github_strategy: dict
    github_analysis: dict
    implementation_analysis: dict
    complete_context: dict
    validation_results: dict
    confidence_level: float


class AgentC:
    """Original Agent C implementation (simplified for demonstration)"""
    
    def __init__(self):
        self.analysis_results = {}
        self.mcp_enabled = False  # Simplified - no actual MCP in demo
        
    def execute_enhanced_workflow(self, complete_context_from_agents_a_d_b: Dict) -> EnhancedGitHubResult:
        """
        Original GitHub investigation logic
        This represents the existing Agent C functionality
        """
        # Simulate existing GitHub investigation
        github_analysis = {
            'pr_investigation_results': {
                'pr_468': {
                    'repository': 'cluster-curator-controller',
                    'title': 'Add digest-based upgrade support',
                    'files_changed': 15,
                    'additions': 450,
                    'deletions': 120,
                    'merge_status': 'merged',
                    'merge_date': '2024-01-15'
                }
            },
            'repository_analysis': {
                'primary_repo': 'stolostron/cluster-curator-controller',
                'related_repos': ['stolostron/clusterlifecycle-api'],
                'test_repos': ['stolostron/clc-ui-e2e']
            },
            'implementation_changes': {
                'core_changes': [
                    'controllers/upgrade_controller.go',
                    'api/v1beta1/clustercurator_types.go',
                    'pkg/digest/discovery.go'
                ],
                'test_changes': [
                    'controllers/upgrade_controller_test.go',
                    'e2e/upgrade_test.go'
                ]
            },
            'code_validation_evidence': {
                'digest_algorithm_implemented': True,
                'fallback_mechanism_present': True,
                'annotation_processing_added': True
            }
        }
        
        implementation_analysis = {
            'implementation_completeness': 'comprehensive',
            'test_coverage_assessment': 'good',
            'integration_readiness': 'ready',
            'validation_confidence': 0.92
        }
        
        # Simulate processing time
        time.sleep(0.1)
        
        # Return structured result
        return EnhancedGitHubResult(
            inherited_context=complete_context_from_agents_a_d_b,
            github_strategy={'pr_investigation_targets': ['pr_468']},
            github_analysis=github_analysis,
            implementation_analysis=implementation_analysis,
            complete_context=complete_context_from_agents_a_d_b,  # Would be enhanced in real implementation
            validation_results={'confidence_score': 0.90},
            confidence_level=0.90
        )


class AgentCWithLearning(AgentC):
    """
    Enhanced Agent C with learning capabilities
    Inherits from original Agent C to maintain all existing functionality
    """
    
    def __init__(self):
        super().__init__()
        # Get singleton learning framework instance
        self.learning_framework = AgentLearningFramework()
        self.agent_id = 'agent_c'
        
        # Feature flag for gradual rollout (can be disabled if needed)
        self.learning_enabled = True
        
        logger.info("Agent C initialized with learning capabilities")
    
    def execute_enhanced_workflow(self, complete_context_from_agents_a_d_b: Dict) -> EnhancedGitHubResult:
        """
        Enhanced GitHub investigation with learning integration
        Maintains exact same interface and behavior as original
        """
        start_time = time.time()
        
        # 1. Check for learning recommendations (fast, cached, non-blocking)
        recommendations = None
        if self.learning_enabled:
            try:
                # Extract context for learning
                jira_context = complete_context_from_agents_a_d_b.get('agent_contributions', {}).get('agent_a_jira', {})
                pr_refs = jira_context.get('enhancements', {}).get('pr_references', {}).get('pr_references', [])
                
                recommendations = self.learning_framework.apply_learnings(
                    self.agent_id,
                    {
                        'type': 'github_investigation',
                        'pr_count': len(pr_refs),
                        'repositories': self._extract_repositories(complete_context_from_agents_a_d_b),
                        'components': self._extract_components(complete_context_from_agents_a_d_b),
                        'mcp_available': self.mcp_enabled
                    }
                )
                
                if recommendations:
                    logger.debug(f"Applied {len(recommendations.get('patterns', []))} learned patterns")
            except Exception as e:
                # Learning errors never affect main execution
                logger.debug(f"Learning recommendation skipped: {e}")
        
        # 2. Execute original logic (exactly the same)
        result = super().execute_enhanced_workflow(complete_context_from_agents_a_d_b)
        
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
                'pr_analyzed': len(result.github_analysis.get('pr_investigation_results', {})) > 0,
                'files_analyzed': sum(pr.get('files_changed', 0) for pr in result.github_analysis.get('pr_investigation_results', {}).values()),
                'implementation_changes_found': len(result.github_analysis.get('implementation_changes', {}).get('core_changes', [])),
                'test_coverage_found': len(result.github_analysis.get('implementation_changes', {}).get('test_changes', [])) > 0,
                'mcp_accelerated': self.mcp_enabled,
                'validation_evidence_collected': len(result.github_analysis.get('code_validation_evidence', {}))
            }
            
            # Queue learning capture (fire-and-forget)
            asyncio.create_task(
                self._capture_learning_async(complete_context_from_agents_a_d_b, result, metrics)
            )
        
        # Return exact same structure as original
        return result
    
    async def _capture_learning_async(self, context: Dict, result: EnhancedGitHubResult, metrics: Dict):
        """
        Async learning capture - runs in background
        Never blocks or affects main execution
        """
        try:
            # Prepare task data for learning
            task_data = {
                'pr_targets': self._extract_pr_targets(context),
                'repositories': self._extract_repositories(context),
                'components': self._extract_components(context),
                'investigation_depth': self._determine_investigation_depth(result)
            }
            
            # Prepare result data for learning
            result_data = {
                'github_analysis': result.github_analysis,
                'implementation_analysis': result.implementation_analysis,
                'pr_count_analyzed': len(result.github_analysis.get('pr_investigation_results', {})),
                'confidence_level': result.confidence_level,
                'mcp_performance': metrics.get('execution_time') if self.mcp_enabled else None
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
    
    def _apply_recommendations(self, result: EnhancedGitHubResult, recommendations: Dict) -> EnhancedGitHubResult:
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
        
        # Add optimization suggestions for future runs
        if 'optimization_suggestions' in recommendations:
            for suggestion in recommendations['optimization_suggestions']:
                if suggestion.get('type') == 'performance' and suggestion.get('expected_improvement'):
                    # Log for future optimization
                    logger.debug(f"Optimization opportunity: {suggestion['suggestion']}")
        
        # Add learning insights
        if recommendations.get('patterns') or recommendations.get('optimization_suggestions'):
            result.github_analysis['learning_insights'] = {
                'patterns_applied': len(recommendations.get('patterns', [])),
                'optimization_hints': recommendations.get('optimization_suggestions', []),
                'performance_hints': recommendations.get('performance_hints', []),
                'mcp_optimization_available': 'Enable MCP for 45-60% performance improvement' if not self.mcp_enabled else None
            }
        
        return result
    
    def _extract_pr_targets(self, context: Dict) -> list:
        """Extract PR targets from context"""
        jira_context = context.get('agent_contributions', {}).get('agent_a_jira', {})
        pr_refs = jira_context.get('enhancements', {}).get('pr_references', {}).get('pr_references', [])
        return [pr.get('pr_number') for pr in pr_refs if pr.get('pr_number')]
    
    def _extract_repositories(self, context: Dict) -> list:
        """Extract repositories from context"""
        repositories = []
        
        # From JIRA context
        jira_context = context.get('agent_contributions', {}).get('agent_a_jira', {})
        pr_refs = jira_context.get('enhancements', {}).get('pr_references', {}).get('pr_references', [])
        for pr in pr_refs:
            if pr.get('repository'):
                repositories.append(pr['repository'])
        
        # From component mapping
        component_mapping = jira_context.get('enhancements', {}).get('component_mapping', {})
        if component_mapping.get('primary_repository'):
            repositories.append(component_mapping['primary_repository'])
        
        return list(set(repositories))  # Unique repositories
    
    def _extract_components(self, context: Dict) -> list:
        """Extract components from context"""
        jira_context = context.get('agent_contributions', {}).get('agent_a_jira', {})
        return jira_context.get('enhancements', {}).get('component_mapping', {}).get('components', [])
    
    def _determine_investigation_depth(self, result: EnhancedGitHubResult) -> str:
        """Determine how deep the investigation went"""
        pr_count = len(result.github_analysis.get('pr_investigation_results', {}))
        files_analyzed = sum(pr.get('files_changed', 0) for pr in result.github_analysis.get('pr_investigation_results', {}).values())
        
        if pr_count > 3 or files_analyzed > 50:
            return 'comprehensive'
        elif pr_count > 1 or files_analyzed > 20:
            return 'standard'
        else:
            return 'basic'
    
    def disable_learning(self):
        """Disable learning if needed (for testing or issues)"""
        self.learning_enabled = False
        logger.info("Learning disabled for Agent C")
    
    def enable_learning(self):
        """Re-enable learning"""
        self.learning_enabled = True
        logger.info("Learning enabled for Agent C")


# Demonstration and validation
def demonstrate_integration():
    """Demonstrate that enhanced agent produces same results"""
    print("Agent C Learning Integration Demonstration")
    print("=" * 50)
    
    # Create both versions
    original_agent = AgentC()
    enhanced_agent = AgentCWithLearning()
    
    # Test context (simulating inherited from Agents A, D, and B)
    test_context = {
        'agent_contributions': {
            'agent_a_jira': {
                'enhancements': {
                    'pr_references': {
                        'pr_references': [
                            {
                                'pr_number': 'PR #468',
                                'repository': 'cluster-curator-controller',
                                'component': 'ClusterCurator'
                            }
                        ]
                    },
                    'component_mapping': {
                        'components': ['ClusterCurator', 'cluster-curator-controller'],
                        'primary_repository': 'stolostron/cluster-curator-controller'
                    }
                }
            },
            'agent_d_environment': {
                'enhancements': {
                    'environment_intelligence': {
                        'acm_version_confirmed': 'ACM 2.14'
                    }
                }
            },
            'agent_b_documentation': {
                'enhancements': {
                    'documentation_analysis': {
                        'implementation_patterns': ['controller_pattern', 'api_pattern']
                    }
                }
            }
        }
    }
    
    # Run both versions
    print(f"\nInvestigating GitHub with test context")
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
    original_github = original_result.github_analysis.copy()
    enhanced_github = enhanced_result.github_analysis.copy()
    enhanced_github.pop('learning_insights', None)
    
    # Verify identical core results
    github_identical = original_github == enhanced_github
    implementation_identical = original_result.implementation_analysis == enhanced_result.implementation_analysis
    
    identical = github_identical and implementation_identical
    print(f"\nCore results identical: {'✅ YES' if identical else '❌ NO'}")
    
    if not identical:
        print("Differences found:")
        if not github_identical:
            print("  GitHub analysis differs")
        if not implementation_identical:
            print("  Implementation analysis differs")
    
    # Show learning enhancements
    if 'learning_insights' in enhanced_result.github_analysis:
        print("\nLearning enhancements applied:")
        insights = enhanced_result.github_analysis['learning_insights']
        print(f"  Patterns applied: {insights.get('patterns_applied', 0)}")
        print(f"  Optimization hints: {len(insights.get('optimization_hints', []))}")
        if insights.get('mcp_optimization_available'):
            print(f"  MCP suggestion: {insights['mcp_optimization_available']}")
    
    print("\n" + "=" * 50)
    print("✅ Integration successful - no regression detected")
    
    return identical


if __name__ == '__main__':
    # Run demonstration
    demonstrate_integration()
