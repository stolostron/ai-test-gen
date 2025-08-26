#!/usr/bin/env python3
"""
Unit Tests for Agent C (GitHub Investigation) Implementation
Tests the actual agent logic for GitHub investigation and intelligence
"""

import unittest
import os
import sys
import time
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from typing import Dict, Any

# Systematic Import Path Management for AI Services
def setup_ai_services_path():
    """Add AI services directory to Python path if not already present"""
    import sys
    import os
    
    # Get the AI services path relative to the test file
    ai_services_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services'))
    
    if ai_services_path not in sys.path:
        sys.path.insert(0, ai_services_path)
    
    # Also add learning framework path
    learning_framework_path = os.path.join(ai_services_path, 'learning-framework')
    if learning_framework_path not in sys.path:
        sys.path.insert(0, learning_framework_path)
    
    return ai_services_path

# Setup import path and import modules
setup_ai_services_path()

try:
    from learning_framework.integrations.agent_c_integration import (
        AgentC, AgentCWithLearning, EnhancedGitHubResult
    )
except ImportError as e:
    print(f"Failed to import Agent C modules: {e}")
    print(f"AI Services path: {setup_ai_services_path()}")
    sys.exit(1)


class TestEnhancedGitHubResult(unittest.TestCase):
    """Test the EnhancedGitHubResult data structure"""
    
    def test_result_structure_creation(self):
        """Test creating EnhancedGitHubResult structure"""
        result = EnhancedGitHubResult(
            inherited_context={'test': 'context'},
            github_strategy={'strategy': 'test'},
            github_analysis={'github': 'analysis'},
            implementation_analysis={'impl': 'analysis'},
            complete_context={'complete': 'context'},
            validation_results={'valid': True},
            confidence_level=0.90
        )
        
        # Verify all fields are present
        self.assertEqual(result.inherited_context, {'test': 'context'})
        self.assertEqual(result.github_strategy, {'strategy': 'test'})
        self.assertEqual(result.github_analysis, {'github': 'analysis'})
        self.assertEqual(result.implementation_analysis, {'impl': 'analysis'})
        self.assertEqual(result.complete_context, {'complete': 'context'})
        self.assertEqual(result.validation_results, {'valid': True})
        self.assertEqual(result.confidence_level, 0.90)


class TestAgentCBasic(unittest.TestCase):
    """Test basic Agent C functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = AgentC()
    
    def test_agent_c_initialization(self):
        """Test Agent C initializes correctly"""
        self.assertIsInstance(self.agent, AgentC)
        self.assertTrue(hasattr(self.agent, 'execute_enhanced_workflow'))
        self.assertTrue(hasattr(self.agent, 'analysis_results'))
        self.assertIsInstance(self.agent.analysis_results, dict)
        self.assertFalse(self.agent.mcp_enabled)  # Default disabled
    
    def test_execute_enhanced_workflow_basic(self):
        """Test basic enhanced workflow execution"""
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
                        }
                    }
                }
            }
        }
        
        result = self.agent.execute_enhanced_workflow(test_context)
        
        # Verify return type
        self.assertIsInstance(result, EnhancedGitHubResult)
        
        # Verify required fields are present
        self.assertEqual(result.inherited_context, test_context)
        self.assertIsInstance(result.github_strategy, dict)
        self.assertIsInstance(result.github_analysis, dict)
        self.assertIsInstance(result.implementation_analysis, dict)
        self.assertIsInstance(result.validation_results, dict)
        self.assertIsInstance(result.confidence_level, (int, float))
    
    def test_github_analysis_structure(self):
        """Test GitHub analysis structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        github_analysis = result.github_analysis
        required_sections = [
            'pr_investigation_results', 'repository_analysis', 
            'implementation_changes', 'code_validation_evidence'
        ]
        
        for section in required_sections:
            self.assertIn(section, github_analysis, f"Missing GitHub analysis section: {section}")
        
        # Verify PR investigation results structure
        pr_results = github_analysis['pr_investigation_results']
        self.assertIsInstance(pr_results, dict)
        
        # Check specific PR structure
        if 'pr_468' in pr_results:
            pr_info = pr_results['pr_468']
            expected_fields = ['repository', 'title', 'files_changed', 'additions', 'deletions']
            for field in expected_fields:
                self.assertIn(field, pr_info, f"Missing PR field: {field}")
        
        # Verify repository analysis
        repo_analysis = github_analysis['repository_analysis']
        self.assertIn('primary_repo', repo_analysis)
        self.assertIn('related_repos', repo_analysis)
        self.assertIsInstance(repo_analysis['related_repos'], list)
    
    def test_implementation_changes_structure(self):
        """Test implementation changes structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        impl_changes = result.github_analysis['implementation_changes']
        self.assertIn('core_changes', impl_changes)
        self.assertIn('test_changes', impl_changes)
        
        # Verify change lists are present
        self.assertIsInstance(impl_changes['core_changes'], list)
        self.assertIsInstance(impl_changes['test_changes'], list)
        self.assertGreater(len(impl_changes['core_changes']), 0, "Should have at least one core change")
    
    def test_code_validation_evidence_structure(self):
        """Test code validation evidence structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        validation_evidence = result.github_analysis['code_validation_evidence']
        expected_evidence = [
            'digest_algorithm_implemented',
            'fallback_mechanism_present', 
            'annotation_processing_added'
        ]
        
        for evidence in expected_evidence:
            self.assertIn(evidence, validation_evidence, f"Missing validation evidence: {evidence}")
            self.assertIsInstance(validation_evidence[evidence], bool)
    
    def test_implementation_analysis_structure(self):
        """Test implementation analysis structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        impl_analysis = result.implementation_analysis
        required_fields = [
            'implementation_completeness',
            'test_coverage_assessment',
            'integration_readiness',
            'validation_confidence'
        ]
        
        for field in required_fields:
            self.assertIn(field, impl_analysis, f"Missing implementation analysis field: {field}")
        
        # Verify specific field types and values
        self.assertIn(impl_analysis['implementation_completeness'], 
                     ['basic', 'good', 'comprehensive'])
        self.assertIn(impl_analysis['test_coverage_assessment'], 
                     ['poor', 'fair', 'good', 'excellent'])
        self.assertIn(impl_analysis['integration_readiness'], 
                     ['not_ready', 'partial', 'ready'])
        self.assertIsInstance(impl_analysis['validation_confidence'], (int, float))
        self.assertGreaterEqual(impl_analysis['validation_confidence'], 0)
        self.assertLessEqual(impl_analysis['validation_confidence'], 1)
    
    def test_confidence_level_range(self):
        """Test that confidence level is within valid range"""
        result = self.agent.execute_enhanced_workflow({})
        
        confidence = result.confidence_level
        self.assertGreaterEqual(confidence, 0.0, "Confidence should be >= 0")
        self.assertLessEqual(confidence, 1.0, "Confidence should be <= 1")
    
    def test_execution_time(self):
        """Test that execution completes within reasonable time"""
        start_time = time.time()
        
        self.agent.execute_enhanced_workflow({})
        
        execution_time = time.time() - start_time
        self.assertLess(execution_time, 5.0, "Execution should complete within 5 seconds")


class TestAgentCWithLearning(unittest.TestCase):
    """Test Agent C with learning capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock the learning framework to avoid external dependencies
        with patch('learning_framework.integrations.agent_c_integration.AgentLearningFramework') as mock_framework:
            self.mock_learning_framework = Mock()
            mock_framework.return_value = self.mock_learning_framework
            
            self.agent = AgentCWithLearning()
    
    def test_agent_c_with_learning_initialization(self):
        """Test Agent C with learning initializes correctly"""
        self.assertIsInstance(self.agent, AgentCWithLearning)
        self.assertTrue(hasattr(self.agent, 'learning_framework'))
        self.assertTrue(hasattr(self.agent, 'learning_enabled'))
        self.assertEqual(self.agent.agent_id, 'agent_c')
        self.assertTrue(self.agent.learning_enabled)
    
    def test_execute_enhanced_workflow_with_learning_disabled(self):
        """Test enhanced workflow when learning is disabled"""
        self.agent.disable_learning()
        
        test_context = {'test': 'context'}
        result = self.agent.execute_enhanced_workflow(test_context)
        
        # Should still work with learning disabled
        self.assertIsInstance(result, EnhancedGitHubResult)
        self.assertEqual(result.inherited_context, test_context)
        
        # Learning framework should not be called
        self.mock_learning_framework.apply_learnings.assert_not_called()
    
    def test_execute_enhanced_workflow_with_learning_enabled(self):
        """Test enhanced workflow with learning enabled"""
        # Mock learning framework responses
        self.mock_learning_framework.apply_learnings.return_value = {
            'confidence_adjustment': 0.05,
            'patterns': [
                {'type': 'pr_investigation', 'pattern_id': 'test_pattern_1'},
                {'type': 'pr_investigation', 'pattern_id': 'test_pattern_2'}
            ],
            'optimization_suggestions': [
                {'type': 'performance', 'suggestion': 'Use MCP for acceleration'},
                {'type': 'quality', 'suggestion': 'Focus on core files'}
            ],
            'performance_hints': ['github_api_optimization']
        }
        
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'pr_references': {
                            'pr_references': [
                                {'pr_number': 'PR #468', 'repository': 'test-repo'}
                            ]
                        },
                        'component_mapping': {
                            'components': ['ClusterCurator'],
                            'primary_repository': 'stolostron/cluster-curator-controller'
                        }
                    }
                }
            }
        }
        
        result = self.agent.execute_enhanced_workflow(test_context)
        
        # Verify learning framework was called
        self.mock_learning_framework.apply_learnings.assert_called_once()
        
        # Verify learning insights were added
        self.assertIn('learning_insights', result.github_analysis)
        insights = result.github_analysis['learning_insights']
        self.assertEqual(insights['patterns_applied'], 2)
        self.assertEqual(len(insights['optimization_hints']), 2)
        self.assertEqual(len(insights['performance_hints']), 1)
    
    def test_execute_enhanced_workflow_confidence_boost(self):
        """Test that learning can boost confidence"""
        # Mock learning framework to boost confidence
        self.mock_learning_framework.apply_learnings.return_value = {
            'confidence_adjustment': 0.06,
            'patterns': ['high_confidence_pattern']
        }
        
        result = self.agent.execute_enhanced_workflow({})
        
        # Confidence should be boosted (original 0.90 + 0.06 = 0.96)
        self.assertGreater(result.confidence_level, 0.93)
        self.assertLessEqual(result.confidence_level, 0.99)  # Capped at 99%
    
    def test_execute_enhanced_workflow_learning_error_handling(self):
        """Test that learning errors don't break main functionality"""
        # Mock learning framework to raise error
        self.mock_learning_framework.apply_learnings.side_effect = Exception("Learning error")
        
        result = self.agent.execute_enhanced_workflow({})
        
        # Should still work despite learning error
        self.assertIsInstance(result, EnhancedGitHubResult)
        self.assertNotIn('learning_insights', result.github_analysis)
    
    def test_extract_pr_targets(self):
        """Test PR target extraction functionality"""
        context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'pr_references': {
                            'pr_references': [
                                {'pr_number': 'PR #468'},
                                {'pr_number': 'PR #123'},
                                {'pr_number': None}  # Should be filtered out
                            ]
                        }
                    }
                }
            }
        }
        
        pr_targets = self.agent._extract_pr_targets(context)
        
        self.assertIsInstance(pr_targets, list)
        self.assertIn('PR #468', pr_targets)
        self.assertIn('PR #123', pr_targets)
        self.assertEqual(len(pr_targets), 2)  # None should be filtered out
    
    def test_extract_repositories(self):
        """Test repository extraction from context"""
        context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'pr_references': {
                            'pr_references': [
                                {'repository': 'cluster-curator-controller'},
                                {'repository': 'clusterlifecycle-api'}
                            ]
                        },
                        'component_mapping': {
                            'primary_repository': 'stolostron/cluster-curator-controller'
                        }
                    }
                }
            }
        }
        
        repositories = self.agent._extract_repositories(context)
        
        self.assertIsInstance(repositories, list)
        self.assertIn('cluster-curator-controller', repositories)
        self.assertIn('clusterlifecycle-api', repositories)
        self.assertIn('stolostron/cluster-curator-controller', repositories)
        # Should be unique list
        self.assertEqual(len(repositories), len(set(repositories)))
    
    def test_extract_components(self):
        """Test component extraction from context"""
        context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'component_mapping': {
                            'components': ['ClusterCurator', 'ACM-Operator']
                        }
                    }
                }
            }
        }
        
        components = self.agent._extract_components(context)
        self.assertEqual(components, ['ClusterCurator', 'ACM-Operator'])
        
        # Test with missing context
        empty_context = {}
        components = self.agent._extract_components(empty_context)
        self.assertEqual(components, [])
    
    def test_determine_investigation_depth(self):
        """Test investigation depth determination"""
        # Comprehensive investigation
        comprehensive_result = EnhancedGitHubResult(
            inherited_context={}, github_strategy={}, 
            github_analysis={
                'pr_investigation_results': {
                    'pr_1': {'files_changed': 20},
                    'pr_2': {'files_changed': 25},
                    'pr_3': {'files_changed': 15},
                    'pr_4': {'files_changed': 10}
                }
            },
            implementation_analysis={}, complete_context={}, 
            validation_results={}, confidence_level=0.9
        )
        
        depth = self.agent._determine_investigation_depth(comprehensive_result)
        self.assertEqual(depth, 'comprehensive')
        
        # Standard investigation
        standard_result = EnhancedGitHubResult(
            inherited_context={}, github_strategy={}, 
            github_analysis={
                'pr_investigation_results': {
                    'pr_1': {'files_changed': 15},
                    'pr_2': {'files_changed': 10}
                }
            },
            implementation_analysis={}, complete_context={}, 
            validation_results={}, confidence_level=0.9
        )
        
        depth = self.agent._determine_investigation_depth(standard_result)
        self.assertEqual(depth, 'standard')
        
        # Basic investigation
        basic_result = EnhancedGitHubResult(
            inherited_context={}, github_strategy={}, 
            github_analysis={
                'pr_investigation_results': {
                    'pr_1': {'files_changed': 5}
                }
            },
            implementation_analysis={}, complete_context={}, 
            validation_results={}, confidence_level=0.9
        )
        
        depth = self.agent._determine_investigation_depth(basic_result)
        self.assertEqual(depth, 'basic')
    
    def test_learning_enable_disable(self):
        """Test learning enable/disable functionality"""
        # Initially enabled
        self.assertTrue(self.agent.learning_enabled)
        
        # Disable learning
        self.agent.disable_learning()
        self.assertFalse(self.agent.learning_enabled)
        
        # Re-enable learning
        self.agent.enable_learning()
        self.assertTrue(self.agent.learning_enabled)
    
    @patch('asyncio.create_task')
    def test_async_learning_capture(self, mock_create_task):
        """Test that async learning capture is triggered"""
        self.mock_learning_framework.apply_learnings.return_value = None
        
        self.agent.execute_enhanced_workflow({})
        
        # Verify async task was created for learning capture
        mock_create_task.assert_called_once()
    
    def test_apply_recommendations_confidence_only_boosts(self):
        """Test that recommendations only boost confidence, never reduce"""
        result = EnhancedGitHubResult(
            inherited_context={}, github_strategy={}, github_analysis={},
            implementation_analysis={}, complete_context={}, 
            validation_results={'confidence_score': 0.8}, confidence_level=0.8
        )
        
        # Test positive adjustment
        recommendations = {'confidence_adjustment': 0.1}
        updated_result = self.agent._apply_recommendations(result, recommendations)
        self.assertEqual(updated_result.confidence_level, 0.9)
        self.assertEqual(updated_result.validation_results['confidence_score'], 0.9)
        
        # Test negative adjustment (should not apply)
        result.confidence_level = 0.8
        recommendations = {'confidence_adjustment': -0.2}
        updated_result = self.agent._apply_recommendations(result, recommendations)
        self.assertEqual(updated_result.confidence_level, 0.8)  # Unchanged
    
    def test_apply_recommendations_mcp_optimization_hint(self):
        """Test MCP optimization hint generation"""
        result = EnhancedGitHubResult(
            inherited_context={}, github_strategy={}, github_analysis={},
            implementation_analysis={}, complete_context={}, 
            validation_results={}, confidence_level=0.8
        )
        
        recommendations = {
            'patterns': ['pattern1'],
            'optimization_suggestions': ['suggestion1']
        }
        
        # With MCP disabled (default)
        updated_result = self.agent._apply_recommendations(result, recommendations)
        
        insights = updated_result.github_analysis['learning_insights']
        self.assertIsNotNone(insights['mcp_optimization_available'])
        self.assertIn('45-60% performance improvement', insights['mcp_optimization_available'])
        
        # With MCP enabled
        self.agent.mcp_enabled = True
        updated_result = self.agent._apply_recommendations(result, recommendations)
        
        insights = updated_result.github_analysis['learning_insights']
        self.assertIsNone(insights['mcp_optimization_available'])
    
    def test_inheritance_compatibility(self):
        """Test that AgentCWithLearning is compatible with base AgentC"""
        # Should be instance of both classes
        self.assertIsInstance(self.agent, AgentC)
        self.assertIsInstance(self.agent, AgentCWithLearning)
        
        # Should have all base class methods
        self.assertTrue(hasattr(self.agent, 'execute_enhanced_workflow'))
        
        # Should maintain same interface
        test_context = {'test': 'context'}
        result = self.agent.execute_enhanced_workflow(test_context)
        base_agent = AgentC()
        base_result = base_agent.execute_enhanced_workflow(test_context)
        
        # Core structure should match (excluding learning insights)
        self.assertEqual(result.inherited_context, base_result.inherited_context)
        self.assertEqual(result.github_strategy, base_result.github_strategy)
        self.assertEqual(result.implementation_analysis, base_result.implementation_analysis)


class TestAgentCIntegration(unittest.TestCase):
    """Test Agent C integration scenarios"""
    
    def setUp(self):
        """Set up test environment"""
        with patch('learning_framework.integrations.agent_c_integration.AgentLearningFramework'):
            self.agent_basic = AgentC()
            self.agent_enhanced = AgentCWithLearning()
    
    def test_backward_compatibility(self):
        """Test that enhanced agent maintains backward compatibility"""
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'pr_references': {
                            'pr_references': [
                                {'pr_number': 'PR #468', 'repository': 'test-repo'}
                            ]
                        },
                        'component_mapping': {
                            'components': ['ClusterCurator']
                        }
                    }
                }
            }
        }
        
        # Run both versions
        basic_result = self.agent_basic.execute_enhanced_workflow(test_context)
        enhanced_result = self.agent_enhanced.execute_enhanced_workflow(test_context)
        
        # Remove learning insights for comparison
        enhanced_github = enhanced_result.github_analysis.copy()
        enhanced_github.pop('learning_insights', None)
        
        # Core results should be identical
        self.assertEqual(basic_result.inherited_context, enhanced_result.inherited_context)
        self.assertEqual(basic_result.github_strategy, enhanced_result.github_strategy)
        self.assertEqual(basic_result.github_analysis, enhanced_github)
        self.assertEqual(basic_result.implementation_analysis, enhanced_result.implementation_analysis)
    
    def test_performance_comparison(self):
        """Test that enhanced agent doesn't significantly impact performance"""
        test_context = {'test': 'context'}
        
        # Time basic agent
        start = time.time()
        self.agent_basic.execute_enhanced_workflow(test_context)
        basic_time = time.time() - start
        
        # Time enhanced agent
        start = time.time()
        self.agent_enhanced.execute_enhanced_workflow(test_context)
        enhanced_time = time.time() - start
        
        # Enhanced agent should not be significantly slower
        # Allow up to 100% overhead for learning features
        self.assertLess(enhanced_time, basic_time * 2.0, 
                       "Enhanced agent should not be more than 2x slower")
    
    def test_multiple_context_analysis(self):
        """Test analyzing multiple contexts in sequence"""
        contexts = [
            {'context_type': 'clustercurator'},
            {'context_type': 'acm_operator'},
            {'context_type': 'mce_controller'}
        ]
        
        for context in contexts:
            with self.subTest(context=context):
                # Both agents should handle all contexts
                basic_result = self.agent_basic.execute_enhanced_workflow(context)
                enhanced_result = self.agent_enhanced.execute_enhanced_workflow(context)
                
                self.assertIsInstance(basic_result, EnhancedGitHubResult)
                self.assertIsInstance(enhanced_result, EnhancedGitHubResult)
                self.assertGreater(basic_result.confidence_level, 0)
                self.assertGreater(enhanced_result.confidence_level, 0)
    
    def test_mcp_feature_flag(self):
        """Test MCP feature flag functionality"""
        # Test with MCP disabled (default)
        self.assertFalse(self.agent_basic.mcp_enabled)
        self.assertFalse(self.agent_enhanced.mcp_enabled)
        
        # Test enabling MCP
        self.agent_enhanced.mcp_enabled = True
        
        test_context = {'test': 'context'}
        result = self.agent_enhanced.execute_enhanced_workflow(test_context)
        
        self.assertIsInstance(result, EnhancedGitHubResult)
        # MCP flag should be captured in learning metrics
        self.assertTrue(self.agent_enhanced.mcp_enabled)


class TestAgentCErrorHandling(unittest.TestCase):
    """Test Agent C error handling and edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = AgentC()
    
    def test_empty_context_handling(self):
        """Test handling of empty context"""
        result = self.agent.execute_enhanced_workflow({})
        
        self.assertIsInstance(result, EnhancedGitHubResult)
        self.assertEqual(result.inherited_context, {})
        self.assertGreater(result.confidence_level, 0)
    
    def test_none_context_handling(self):
        """Test handling of None context"""
        result = self.agent.execute_enhanced_workflow(None)
        
        self.assertIsInstance(result, EnhancedGitHubResult)
        self.assertEqual(result.inherited_context, None)
    
    def test_malformed_context_handling(self):
        """Test handling of malformed context structures"""
        malformed_contexts = [
            {'invalid': 'structure'},
            {'agent_contributions': 'not_a_dict'},
            {'agent_contributions': {'agent_a_jira': None}},
            {'agent_contributions': {'agent_a_jira': {'enhancements': 'not_a_dict'}}}
        ]
        
        for context in malformed_contexts:
            with self.subTest(context=context):
                result = self.agent.execute_enhanced_workflow(context)
                
                self.assertIsInstance(result, EnhancedGitHubResult)
                self.assertEqual(result.inherited_context, context)
                self.assertGreater(result.confidence_level, 0)
    
    def test_very_large_context_handling(self):
        """Test handling of very large context objects"""
        large_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'large_data': 'x' * 10000,  # 10KB of data
                    'enhancements': {
                        'pr_references': {
                            'pr_references': [
                                {'pr_number': f'PR #{i}', 'repository': f'repo-{i}'}
                                for i in range(100)  # 100 PRs
                            ]
                        }
                    }
                }
            }
        }
        
        start_time = time.time()
        result = self.agent.execute_enhanced_workflow(large_context)
        execution_time = time.time() - start_time
        
        self.assertIsInstance(result, EnhancedGitHubResult)
        self.assertLess(execution_time, 10.0, "Should handle large contexts within 10 seconds")
    
    def test_concurrent_execution(self):
        """Test concurrent execution of GitHub investigation"""
        import threading
        
        results = {}
        errors = {}
        
        def investigate_github(thread_id, context):
            try:
                result = self.agent.execute_enhanced_workflow(context)
                results[thread_id] = result
            except Exception as e:
                errors[thread_id] = str(e)
        
        # Create threads for concurrent investigation
        threads = []
        contexts = [
            {'context_id': 1, 'component': 'clustercurator'},
            {'context_id': 2, 'component': 'acm_operator'},
            {'context_id': 3, 'component': 'mce_controller'}
        ]
        
        for i, context in enumerate(contexts):
            thread = threading.Thread(target=investigate_github, args=(i, context))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=10)
        
        # Verify no errors occurred
        self.assertEqual(len(errors), 0, f"Errors occurred during concurrent investigation: {errors}")
        
        # Verify all results were generated
        self.assertEqual(len(results), len(contexts), 
                        f"Expected {len(contexts)} results, got {len(results)}")


if __name__ == '__main__':
    print("🧪 Agent C (GitHub Investigation) Implementation Unit Tests")
    print("Testing agent logic for GitHub investigation and intelligence")
    print("=" * 70)
    
    unittest.main(verbosity=2)