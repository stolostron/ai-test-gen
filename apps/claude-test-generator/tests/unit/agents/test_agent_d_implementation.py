#!/usr/bin/env python3
"""
Unit Tests for Agent D (Environment Intelligence) Implementation
Tests the actual agent logic for environment assessment and intelligence
"""

import unittest
import os
import sys
import time
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from typing import Dict, Any, Optional

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
    from learning_framework.integrations.agent_d_integration import (
        AgentD, AgentDWithLearning, EnhancedEnvironmentResultV3
    )
except ImportError as e:
    print(f"Failed to import Agent D modules: {e}")
    print(f"AI Services path: {setup_ai_services_path()}")
    sys.exit(1)


class TestEnhancedEnvironmentResultV3(unittest.TestCase):
    """Test the EnhancedEnvironmentResultV3 data structure"""
    
    def test_result_structure_creation(self):
        """Test creating EnhancedEnvironmentResultV3 structure"""
        result = EnhancedEnvironmentResultV3(
            inherited_context={'test': 'context'},
            environment_selection={'env': 'test'},
            health_assessment={'health': 'good'},
            deployment_assessment={'deploy': 'ready'},
            real_data_package={'data': 'real'},
            enhanced_context={'enhanced': 'context'},
            validation_results={'valid': True},
            confidence_level=0.95
        )
        
        # Verify all fields are present
        self.assertEqual(result.inherited_context, {'test': 'context'})
        self.assertEqual(result.environment_selection, {'env': 'test'})
        self.assertEqual(result.health_assessment, {'health': 'good'})
        self.assertEqual(result.deployment_assessment, {'deploy': 'ready'})
        self.assertEqual(result.real_data_package, {'data': 'real'})
        self.assertEqual(result.enhanced_context, {'enhanced': 'context'})
        self.assertEqual(result.validation_results, {'valid': True})
        self.assertEqual(result.confidence_level, 0.95)
        self.assertEqual(result.pr_context_integration, 'complete')  # Default value
    
    def test_result_structure_defaults(self):
        """Test default values in EnhancedEnvironmentResultV3"""
        result = EnhancedEnvironmentResultV3(
            inherited_context={},
            environment_selection={},
            health_assessment={},
            deployment_assessment={},
            real_data_package={},
            enhanced_context={},
            validation_results={},
            confidence_level=0.8,
            pr_context_integration='partial'
        )
        
        self.assertEqual(result.pr_context_integration, 'partial')


class TestAgentDBasic(unittest.TestCase):
    """Test basic Agent D functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = AgentD()
    
    def test_agent_d_initialization(self):
        """Test Agent D initializes correctly"""
        self.assertIsInstance(self.agent, AgentD)
        self.assertTrue(hasattr(self.agent, 'execute_enhanced_workflow'))
        self.assertTrue(hasattr(self.agent, 'analysis_results'))
        self.assertIsInstance(self.agent.analysis_results, dict)
    
    def test_execute_enhanced_workflow_basic(self):
        """Test basic enhanced workflow execution"""
        test_context = {
            'foundation_data': {
                'version_context': {
                    'target_version': 'ACM 2.15',
                    'jira_version': 'ACM 2.15'
                }
            },
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'component_mapping': {
                            'components': ['ClusterCurator']
                        }
                    }
                }
            }
        }
        
        result = self.agent.execute_enhanced_workflow(test_context)
        
        # Verify return type
        self.assertIsInstance(result, EnhancedEnvironmentResultV3)
        
        # Verify required fields are present
        self.assertEqual(result.inherited_context, test_context)
        self.assertIsInstance(result.environment_selection, dict)
        self.assertIsInstance(result.health_assessment, dict)
        self.assertIsInstance(result.deployment_assessment, dict)
        self.assertIsInstance(result.real_data_package, dict)
        self.assertIsInstance(result.validation_results, dict)
        self.assertIsInstance(result.confidence_level, (int, float))
    
    def test_execute_enhanced_workflow_with_user_input(self):
        """Test enhanced workflow with user-specified environment"""
        test_context = {'test': 'context'}
        user_env = "user-specified-cluster"
        
        result = self.agent.execute_enhanced_workflow(test_context, user_env)
        
        self.assertIsInstance(result, EnhancedEnvironmentResultV3)
        self.assertEqual(result.inherited_context, test_context)
    
    def test_environment_selection_structure(self):
        """Test environment selection structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        env_selection = result.environment_selection
        self.assertIn('environment', env_selection)
        self.assertIn('selection_score', env_selection)
        
        environment = env_selection['environment']
        self.assertIn('cluster_name', environment)
        self.assertIn('cluster_type', environment)
        self.assertIn('selected_reason', environment)
        
        # Verify data types
        self.assertIsInstance(env_selection['selection_score'], (int, float))
        self.assertGreater(env_selection['selection_score'], 0)
    
    def test_health_assessment_structure(self):
        """Test health assessment structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        health = result.health_assessment
        required_fields = [
            'connectivity_status', 'health_score', 'acm_version', 'mce_version',
            'openshift_version', 'infrastructure_score', 'api_availability', 'authentication_status'
        ]
        
        for field in required_fields:
            self.assertIn(field, health, f"Missing health assessment field: {field}")
        
        # Verify specific values and types
        self.assertIn(health['connectivity_status'], ['connected', 'disconnected', 'partial'])
        self.assertIsInstance(health['health_score'], (int, float))
        self.assertGreaterEqual(health['health_score'], 0)
        self.assertLessEqual(health['health_score'], 10)
        self.assertIsInstance(health['api_availability'], bool)
    
    def test_deployment_assessment_structure(self):
        """Test deployment assessment structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        deployment = result.deployment_assessment
        required_fields = [
            'deployment_status', 'confidence_score', 'version_gap', 'readiness_assessment'
        ]
        
        for field in required_fields:
            self.assertIn(field, deployment, f"Missing deployment assessment field: {field}")
        
        # Verify version gap structure
        version_gap = deployment['version_gap']
        self.assertIn('target_version', version_gap)
        self.assertIn('current_version', version_gap)
        self.assertIn('gap_exists', version_gap)
        self.assertIsInstance(version_gap['gap_exists'], bool)
    
    def test_real_data_package_structure(self):
        """Test real data package structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        real_data = result.real_data_package
        required_fields = [
            'login_command', 'namespaces', 'operator_status', 'sample_resources'
        ]
        
        for field in required_fields:
            self.assertIn(field, real_data, f"Missing real data field: {field}")
        
        # Verify specific structures
        self.assertIsInstance(real_data['namespaces'], list)
        self.assertIsInstance(real_data['operator_status'], dict)
        self.assertIsInstance(real_data['sample_resources'], dict)
        
        # Verify sample resources structure
        sample_resources = real_data['sample_resources']
        self.assertIn('clustercurators', sample_resources)
        self.assertIn('managedclusters', sample_resources)
        self.assertIsInstance(sample_resources['managedclusters'], list)
    
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


class TestAgentDWithLearning(unittest.TestCase):
    """Test Agent D with learning capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock the learning framework to avoid external dependencies
        with patch('learning_framework.integrations.agent_d_integration.AgentLearningFramework') as mock_framework:
            self.mock_learning_framework = Mock()
            mock_framework.return_value = self.mock_learning_framework
            
            self.agent = AgentDWithLearning()
    
    def test_agent_d_with_learning_initialization(self):
        """Test Agent D with learning initializes correctly"""
        self.assertIsInstance(self.agent, AgentDWithLearning)
        self.assertTrue(hasattr(self.agent, 'learning_framework'))
        self.assertTrue(hasattr(self.agent, 'learning_enabled'))
        self.assertEqual(self.agent.agent_id, 'agent_d')
        self.assertTrue(self.agent.learning_enabled)
    
    def test_execute_enhanced_workflow_with_learning_disabled(self):
        """Test enhanced workflow when learning is disabled"""
        self.agent.disable_learning()
        
        test_context = {'test': 'context'}
        result = self.agent.execute_enhanced_workflow(test_context)
        
        # Should still work with learning disabled
        self.assertIsInstance(result, EnhancedEnvironmentResultV3)
        
        # Learning framework should not be called
        self.mock_learning_framework.apply_learnings.assert_not_called()
    
    def test_execute_enhanced_workflow_with_learning_enabled(self):
        """Test enhanced workflow with learning enabled"""
        # Mock learning framework responses
        self.mock_learning_framework.apply_learnings.return_value = {
            'confidence_adjustment': 0.05,
            'patterns': ['pattern1', 'pattern2'],
            'optimization_suggestions': ['hint1', 'hint2'],
            'performance_hints': ['timeout_optimization']
        }
        
        test_context = {
            'foundation_data': {
                'version_context': {'target_version': 'ACM 2.15'}
            },
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'component_mapping': {'components': ['ClusterCurator']}
                    }
                }
            }
        }
        
        result = self.agent.execute_enhanced_workflow(test_context)
        
        # Verify learning framework was called
        self.mock_learning_framework.apply_learnings.assert_called_once()
        
        # Verify learning insights were added
        self.assertIn('learning_insights', result.health_assessment)
        insights = result.health_assessment['learning_insights']
        self.assertEqual(insights['patterns_applied'], 2)
        self.assertEqual(len(insights['optimization_hints']), 2)
        self.assertEqual(len(insights['performance_hints']), 1)
    
    def test_execute_enhanced_workflow_confidence_boost(self):
        """Test that learning can boost confidence"""
        # Mock learning framework to boost confidence
        self.mock_learning_framework.apply_learnings.return_value = {
            'confidence_adjustment': 0.07,
            'patterns': ['high_confidence_pattern']
        }
        
        result = self.agent.execute_enhanced_workflow({})
        
        # Confidence should be boosted (original 0.92 + 0.07 = 0.99)
        self.assertGreater(result.confidence_level, 0.95)
        self.assertLessEqual(result.confidence_level, 0.99)  # Capped at 99%
    
    def test_execute_enhanced_workflow_learning_error_handling(self):
        """Test that learning errors don't break main functionality"""
        # Mock learning framework to raise error
        self.mock_learning_framework.apply_learnings.side_effect = Exception("Learning error")
        
        result = self.agent.execute_enhanced_workflow({})
        
        # Should still work despite learning error
        self.assertIsInstance(result, EnhancedEnvironmentResultV3)
        self.assertNotIn('learning_insights', result.health_assessment)
    
    def test_extract_target_version(self):
        """Test target version extraction"""
        context = {
            'foundation_data': {
                'version_context': {
                    'target_version': 'ACM 2.15.0'
                }
            }
        }
        
        version = self.agent._extract_target_version(context)
        self.assertEqual(version, 'ACM 2.15.0')
        
        # Test with missing context
        empty_context = {}
        version = self.agent._extract_target_version(empty_context)
        self.assertEqual(version, 'unknown')
    
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
    
    def test_determine_check_types(self):
        """Test check type determination"""
        result = EnhancedEnvironmentResultV3(
            inherited_context={},
            environment_selection={},
            health_assessment={
                'connectivity_status': 'connected',
                'acm_version': '2.14.5'
            },
            deployment_assessment={
                'deployment_status': 'feature_not_deployed'
            },
            real_data_package={'test': 'data'},
            enhanced_context={},
            validation_results={},
            confidence_level=0.9
        )
        
        check_types = self.agent._determine_check_types(result)
        
        expected_types = ['connectivity', 'version_detection', 'deployment_assessment', 'real_data_collection']
        for check_type in expected_types:
            self.assertIn(check_type, check_types)
    
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
        result = EnhancedEnvironmentResultV3(
            inherited_context={}, environment_selection={}, health_assessment={},
            deployment_assessment={}, real_data_package={}, enhanced_context={},
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
    
    def test_generate_env_recommendations(self):
        """Test environment recommendation generation"""
        recommendations = {
            'patterns': [
                {
                    'type': 'env_health_check',
                    'stats': {'success_rate': 0.95}
                },
                {
                    'type': 'other_pattern',
                    'stats': {'success_rate': 0.8}
                }
            ]
        }
        
        env_recs = self.agent._generate_env_recommendations(recommendations)
        
        self.assertIsInstance(env_recs, list)
        # Should generate recommendation for high success rate health check
        self.assertGreater(len(env_recs), 0)
        
        # Verify recommendation structure
        for rec in env_recs:
            self.assertIn('type', rec)
            self.assertIn('suggestion', rec)
    
    def test_inheritance_compatibility(self):
        """Test that AgentDWithLearning is compatible with base AgentD"""
        # Should be instance of both classes
        self.assertIsInstance(self.agent, AgentD)
        self.assertIsInstance(self.agent, AgentDWithLearning)
        
        # Should have all base class methods
        self.assertTrue(hasattr(self.agent, 'execute_enhanced_workflow'))
        
        # Should maintain same interface
        test_context = {'test': 'context'}
        result = self.agent.execute_enhanced_workflow(test_context)
        base_agent = AgentD()
        base_result = base_agent.execute_enhanced_workflow(test_context)
        
        # Core structure should match (excluding learning insights)
        self.assertEqual(result.inherited_context, base_result.inherited_context)
        self.assertEqual(result.environment_selection, base_result.environment_selection)
        self.assertEqual(result.deployment_assessment, base_result.deployment_assessment)
        self.assertEqual(result.real_data_package, base_result.real_data_package)


class TestAgentDIntegration(unittest.TestCase):
    """Test Agent D integration scenarios"""
    
    def setUp(self):
        """Set up test environment"""
        with patch('learning_framework.integrations.agent_d_integration.AgentLearningFramework'):
            self.agent_basic = AgentD()
            self.agent_enhanced = AgentDWithLearning()
    
    def test_backward_compatibility(self):
        """Test that enhanced agent maintains backward compatibility"""
        test_context = {
            'foundation_data': {
                'version_context': {'target_version': 'ACM 2.15'}
            },
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'component_mapping': {'components': ['ClusterCurator']}
                    }
                }
            }
        }
        
        # Run both versions
        basic_result = self.agent_basic.execute_enhanced_workflow(test_context)
        enhanced_result = self.agent_enhanced.execute_enhanced_workflow(test_context)
        
        # Remove learning insights for comparison
        enhanced_health = enhanced_result.health_assessment.copy()
        enhanced_health.pop('learning_insights', None)
        
        # Core results should be identical
        self.assertEqual(basic_result.inherited_context, enhanced_result.inherited_context)
        self.assertEqual(basic_result.environment_selection, enhanced_result.environment_selection)
        self.assertEqual(basic_result.health_assessment, enhanced_health)
        self.assertEqual(basic_result.deployment_assessment, enhanced_result.deployment_assessment)
        self.assertEqual(basic_result.real_data_package, enhanced_result.real_data_package)
    
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
    
    def test_user_specified_environment_handling(self):
        """Test handling of user-specified environments"""
        test_context = {'test': 'context'}
        user_environments = ["prod-cluster", "test-env", "custom-cluster"]
        
        for user_env in user_environments:
            with self.subTest(user_env=user_env):
                # Both agents should handle user-specified environments
                basic_result = self.agent_basic.execute_enhanced_workflow(test_context, user_env)
                enhanced_result = self.agent_enhanced.execute_enhanced_workflow(test_context, user_env)
                
                self.assertIsInstance(basic_result, EnhancedEnvironmentResultV3)
                self.assertIsInstance(enhanced_result, EnhancedEnvironmentResultV3)
                self.assertEqual(basic_result.inherited_context, enhanced_result.inherited_context)
    
    def test_multiple_context_analysis(self):
        """Test analyzing multiple contexts in sequence"""
        contexts = [
            {'component': 'ClusterCurator'},
            {'component': 'ACM-Operator'},
            {'component': 'MCE-Controller'}
        ]
        
        for context in contexts:
            with self.subTest(context=context):
                # Both agents should handle all contexts
                basic_result = self.agent_basic.execute_enhanced_workflow(context)
                enhanced_result = self.agent_enhanced.execute_enhanced_workflow(context)
                
                self.assertIsInstance(basic_result, EnhancedEnvironmentResultV3)
                self.assertIsInstance(enhanced_result, EnhancedEnvironmentResultV3)
                self.assertGreater(basic_result.confidence_level, 0)
                self.assertGreater(enhanced_result.confidence_level, 0)


class TestAgentDErrorHandling(unittest.TestCase):
    """Test Agent D error handling and edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = AgentD()
    
    def test_empty_context_handling(self):
        """Test handling of empty context"""
        result = self.agent.execute_enhanced_workflow({})
        
        self.assertIsInstance(result, EnhancedEnvironmentResultV3)
        self.assertEqual(result.inherited_context, {})
        self.assertGreater(result.confidence_level, 0)
    
    def test_none_context_handling(self):
        """Test handling of None context"""
        result = self.agent.execute_enhanced_workflow(None)
        
        self.assertIsInstance(result, EnhancedEnvironmentResultV3)
        self.assertEqual(result.inherited_context, None)
    
    def test_malformed_context_handling(self):
        """Test handling of malformed context structures"""
        malformed_contexts = [
            {'invalid': 'structure'},
            {'foundation_data': 'not_a_dict'},
            {'agent_contributions': None},
            {'foundation_data': {'version_context': None}}
        ]
        
        for context in malformed_contexts:
            with self.subTest(context=context):
                result = self.agent.execute_enhanced_workflow(context)
                
                self.assertIsInstance(result, EnhancedEnvironmentResultV3)
                self.assertEqual(result.inherited_context, context)
                self.assertGreater(result.confidence_level, 0)
    
    def test_very_large_context_handling(self):
        """Test handling of very large context objects"""
        large_context = {
            'foundation_data': {
                'large_data': 'x' * 10000  # 10KB of data
            },
            'agent_contributions': {
                'agent_a_jira': {
                    'large_list': list(range(1000))
                }
            }
        }
        
        start_time = time.time()
        result = self.agent.execute_enhanced_workflow(large_context)
        execution_time = time.time() - start_time
        
        self.assertIsInstance(result, EnhancedEnvironmentResultV3)
        self.assertLess(execution_time, 10.0, "Should handle large contexts within 10 seconds")
    
    def test_concurrent_execution(self):
        """Test concurrent execution of environment analysis"""
        import threading
        
        results = {}
        errors = {}
        
        def analyze_environment(thread_id, context):
            try:
                result = self.agent.execute_enhanced_workflow(context)
                results[thread_id] = result
            except Exception as e:
                errors[thread_id] = str(e)
        
        # Create threads for concurrent analysis
        threads = []
        contexts = [
            {'context_id': 1},
            {'context_id': 2},
            {'context_id': 3}
        ]
        
        for i, context in enumerate(contexts):
            thread = threading.Thread(target=analyze_environment, args=(i, context))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=10)
        
        # Verify no errors occurred
        self.assertEqual(len(errors), 0, f"Errors occurred during concurrent analysis: {errors}")
        
        # Verify all results were generated
        self.assertEqual(len(results), len(contexts), 
                        f"Expected {len(contexts)} results, got {len(results)}")


if __name__ == '__main__':
    print("🧪 Agent D (Environment Intelligence) Implementation Unit Tests")
    print("Testing agent logic for environment assessment and intelligence")
    print("=" * 70)
    
    unittest.main(verbosity=2)