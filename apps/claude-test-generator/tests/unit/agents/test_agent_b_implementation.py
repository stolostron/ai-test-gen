#!/usr/bin/env python3
"""
Unit Tests for Agent B (Documentation Intelligence) Implementation
Tests the actual agent logic for documentation analysis and intelligence
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
    from learning_framework.integrations.agent_b_integration import (
        AgentB, AgentBWithLearning, EnhancedDocumentationResult
    )
except ImportError as e:
    print(f"Failed to import Agent B modules: {e}")
    print(f"AI Services path: {setup_ai_services_path()}")
    sys.exit(1)


class TestEnhancedDocumentationResult(unittest.TestCase):
    """Test the EnhancedDocumentationResult data structure"""
    
    def test_result_structure_creation(self):
        """Test creating EnhancedDocumentationResult structure"""
        result = EnhancedDocumentationResult(
            inherited_context={'test': 'context'},
            documentation_strategy={'strategy': 'test'},
            documentation_analysis={'docs': 'analysis'},
            feature_understanding={'features': 'understood'},
            enhanced_context={'enhanced': 'context'},
            validation_results={'valid': True},
            confidence_level=0.88
        )
        
        # Verify all fields are present
        self.assertEqual(result.inherited_context, {'test': 'context'})
        self.assertEqual(result.documentation_strategy, {'strategy': 'test'})
        self.assertEqual(result.documentation_analysis, {'docs': 'analysis'})
        self.assertEqual(result.feature_understanding, {'features': 'understood'})
        self.assertEqual(result.enhanced_context, {'enhanced': 'context'})
        self.assertEqual(result.validation_results, {'valid': True})
        self.assertEqual(result.confidence_level, 0.88)


class TestAgentBBasic(unittest.TestCase):
    """Test basic Agent B functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = AgentB()
    
    def test_agent_b_initialization(self):
        """Test Agent B initializes correctly"""
        self.assertIsInstance(self.agent, AgentB)
        self.assertTrue(hasattr(self.agent, 'execute_enhanced_workflow'))
        self.assertTrue(hasattr(self.agent, 'analysis_results'))
        self.assertIsInstance(self.agent.analysis_results, dict)
    
    def test_execute_enhanced_workflow_basic(self):
        """Test basic enhanced workflow execution"""
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'technical_scope': {
                            'feature_type': 'cluster_management',
                            'feature_name': 'ClusterCurator Digest Upgrades',
                            'primary_components': ['ClusterCurator']
                        }
                    }
                }
            }
        }
        
        result = self.agent.execute_enhanced_workflow(test_context)
        
        # Verify return type
        self.assertIsInstance(result, EnhancedDocumentationResult)
        
        # Verify required fields are present
        self.assertEqual(result.inherited_context, test_context)
        self.assertIsInstance(result.documentation_strategy, dict)
        self.assertIsInstance(result.documentation_analysis, dict)
        self.assertIsInstance(result.feature_understanding, dict)
        self.assertIsInstance(result.validation_results, dict)
        self.assertIsInstance(result.confidence_level, (int, float))
    
    def test_documentation_analysis_structure(self):
        """Test documentation analysis structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        doc_analysis = result.documentation_analysis
        required_sections = [
            'feature_documentation', 'implementation_patterns', 
            'api_specifications', 'usage_patterns'
        ]
        
        for section in required_sections:
            self.assertIn(section, doc_analysis, f"Missing documentation section: {section}")
        
        # Verify feature documentation structure
        feature_docs = doc_analysis['feature_documentation']
        self.assertIn('feature_description', feature_docs)
        self.assertIn('functionality_overview', feature_docs)
        self.assertIn('implementation_details', feature_docs)
        
        # Verify API specifications
        api_specs = doc_analysis['api_specifications']
        self.assertIn('api_endpoints', api_specs)
        self.assertIn('crd_specifications', api_specs)
        self.assertIn('field_requirements', api_specs)
        self.assertIsInstance(api_specs['api_endpoints'], list)
        self.assertIsInstance(api_specs['crd_specifications'], list)
        self.assertIsInstance(api_specs['field_requirements'], list)
    
    def test_implementation_patterns_structure(self):
        """Test implementation patterns structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        patterns = result.documentation_analysis['implementation_patterns']
        self.assertIsInstance(patterns, list)
        self.assertGreater(len(patterns), 0, "Should have at least one implementation pattern")
        
        # All patterns should be strings
        for pattern in patterns:
            self.assertIsInstance(pattern, str)
            self.assertGreater(len(pattern), 0, "Pattern names should not be empty")
    
    def test_feature_understanding_structure(self):
        """Test feature understanding structure"""
        result = self.agent.execute_enhanced_workflow({})
        
        understanding = result.feature_understanding
        required_sections = ['feature_capabilities', 'testing_implications']
        
        for section in required_sections:
            self.assertIn(section, understanding, f"Missing understanding section: {section}")
        
        # Verify feature capabilities structure
        capabilities = understanding['feature_capabilities']
        self.assertIn('primary_capabilities', capabilities)
        self.assertIn('secondary_capabilities', capabilities)
        self.assertIn('integration_capabilities', capabilities)
        
        # All capabilities should be lists
        for cap_type in ['primary_capabilities', 'secondary_capabilities', 'integration_capabilities']:
            self.assertIsInstance(capabilities[cap_type], list)
            self.assertGreater(len(capabilities[cap_type]), 0)
        
        # Verify testing implications
        testing_implications = understanding['testing_implications']
        self.assertIsInstance(testing_implications, list)
        self.assertGreater(len(testing_implications), 0)
    
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


class TestAgentBWithLearning(unittest.TestCase):
    """Test Agent B with learning capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock the learning framework to avoid external dependencies
        with patch('learning_framework.integrations.agent_b_integration.AgentLearningFramework') as mock_framework:
            self.mock_learning_framework = Mock()
            mock_framework.return_value = self.mock_learning_framework
            
            self.agent = AgentBWithLearning()
    
    def test_agent_b_with_learning_initialization(self):
        """Test Agent B with learning initializes correctly"""
        self.assertIsInstance(self.agent, AgentBWithLearning)
        self.assertTrue(hasattr(self.agent, 'learning_framework'))
        self.assertTrue(hasattr(self.agent, 'learning_enabled'))
        self.assertEqual(self.agent.agent_id, 'agent_b')
        self.assertTrue(self.agent.learning_enabled)
    
    def test_execute_enhanced_workflow_with_learning_disabled(self):
        """Test enhanced workflow when learning is disabled"""
        self.agent.disable_learning()
        
        test_context = {'test': 'context'}
        result = self.agent.execute_enhanced_workflow(test_context)
        
        # Should still work with learning disabled
        self.assertIsInstance(result, EnhancedDocumentationResult)
        self.assertEqual(result.inherited_context, test_context)
        
        # Learning framework should not be called
        self.mock_learning_framework.apply_learnings.assert_not_called()
    
    def test_execute_enhanced_workflow_with_learning_enabled(self):
        """Test enhanced workflow with learning enabled"""
        # Mock learning framework responses
        self.mock_learning_framework.apply_learnings.return_value = {
            'confidence_adjustment': 0.05,
            'patterns': [
                {'type': 'doc_search_strategy', 'pattern_id': 'test_pattern_1'},
                {'type': 'doc_search_strategy', 'pattern_id': 'test_pattern_2'}
            ],
            'optimization_suggestions': ['hint1', 'hint2'],
            'performance_hints': ['performance_tip']
        }
        
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'technical_scope': {
                            'feature_type': 'cluster_management',
                            'feature_name': 'ClusterCurator Test',
                            'primary_components': ['ClusterCurator']
                        },
                        'component_mapping': {
                            'components': ['ClusterCurator']
                        }
                    }
                }
            }
        }
        
        result = self.agent.execute_enhanced_workflow(test_context)
        
        # Verify learning framework was called
        self.mock_learning_framework.apply_learnings.assert_called_once()
        
        # Verify learning insights were added
        self.assertIn('learning_insights', result.documentation_analysis)
        insights = result.documentation_analysis['learning_insights']
        self.assertEqual(insights['patterns_applied'], 2)
        self.assertEqual(len(insights['optimization_hints']), 2)
        self.assertEqual(len(insights['performance_hints']), 1)
    
    def test_execute_enhanced_workflow_confidence_boost(self):
        """Test that learning can boost confidence"""
        # Mock learning framework to boost confidence
        self.mock_learning_framework.apply_learnings.return_value = {
            'confidence_adjustment': 0.10,
            'patterns': ['high_confidence_pattern']
        }
        
        result = self.agent.execute_enhanced_workflow({})
        
        # Confidence should be boosted (original 0.88 + 0.10 = 0.98)
        self.assertGreater(result.confidence_level, 0.90)
        self.assertLessEqual(result.confidence_level, 0.99)  # Capped at 99%
    
    def test_execute_enhanced_workflow_learning_error_handling(self):
        """Test that learning errors don't break main functionality"""
        # Mock learning framework to raise error
        self.mock_learning_framework.apply_learnings.side_effect = Exception("Learning error")
        
        result = self.agent.execute_enhanced_workflow({})
        
        # Should still work despite learning error
        self.assertIsInstance(result, EnhancedDocumentationResult)
        self.assertNotIn('learning_insights', result.documentation_analysis)
    
    def test_extract_keywords(self):
        """Test keyword extraction functionality"""
        context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'technical_scope': {
                            'feature_name': 'ClusterCurator Digest Upgrades',
                            'primary_components': ['ClusterCurator', 'cluster-curator-controller']
                        }
                    }
                }
            }
        }
        
        keywords = self.agent._extract_keywords(context)
        
        self.assertIsInstance(keywords, list)
        self.assertIn('clustercurator', keywords)
        self.assertIn('digest', keywords)
        self.assertIn('upgrades', keywords)
        self.assertIn('clustercuratorcontroller', keywords)
    
    def test_extract_feature_type(self):
        """Test feature type extraction"""
        context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'technical_scope': {
                            'feature_type': 'cluster_management'
                        }
                    }
                }
            }
        }
        
        feature_type = self.agent._extract_feature_type(context)
        self.assertEqual(feature_type, 'cluster_management')
        
        # Test with missing context
        empty_context = {}
        feature_type = self.agent._extract_feature_type(empty_context)
        self.assertEqual(feature_type, 'unknown')
    
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
    
    def test_extract_doc_sources(self):
        """Test documentation source extraction"""
        result = EnhancedDocumentationResult(
            inherited_context={},
            documentation_strategy={},
            documentation_analysis={
                'feature_documentation': {'test': 'docs'},
                'api_specifications': {'test': 'api'},
                'implementation_patterns': ['pattern1']
            },
            feature_understanding={},
            enhanced_context={},
            validation_results={},
            confidence_level=0.8
        )
        
        sources = self.agent._extract_doc_sources(result)
        
        expected_sources = ['feature_docs', 'api_docs', 'implementation_guides']
        for source in expected_sources:
            self.assertIn(source, sources)
    
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
        result = EnhancedDocumentationResult(
            inherited_context={}, documentation_strategy={}, documentation_analysis={},
            feature_understanding={}, enhanced_context={}, 
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
    
    def test_apply_recommendations_pattern_addition(self):
        """Test that learned patterns are added to implementation patterns"""
        result = EnhancedDocumentationResult(
            inherited_context={}, documentation_strategy={}, 
            documentation_analysis={'implementation_patterns': ['existing_pattern']},
            feature_understanding={}, enhanced_context={}, 
            validation_results={}, confidence_level=0.8
        )
        
        recommendations = {
            'patterns': [
                {'type': 'doc_search_strategy', 'pattern_id': 'new_pattern_1'},
                {'type': 'doc_search_strategy', 'pattern_id': 'new_pattern_2'}
            ]
        }
        
        updated_result = self.agent._apply_recommendations(result, recommendations)
        
        patterns = updated_result.documentation_analysis['implementation_patterns']
        self.assertIn('existing_pattern', patterns)
        self.assertIn('learned_pattern_new_pattern_1', patterns)
        self.assertIn('learned_pattern_new_pattern_2', patterns)
    
    def test_inheritance_compatibility(self):
        """Test that AgentBWithLearning is compatible with base AgentB"""
        # Should be instance of both classes
        self.assertIsInstance(self.agent, AgentB)
        self.assertIsInstance(self.agent, AgentBWithLearning)
        
        # Should have all base class methods
        self.assertTrue(hasattr(self.agent, 'execute_enhanced_workflow'))
        
        # Should maintain same interface
        test_context = {'test': 'context'}
        result = self.agent.execute_enhanced_workflow(test_context)
        base_agent = AgentB()
        base_result = base_agent.execute_enhanced_workflow(test_context)
        
        # Core structure should match (excluding learning insights)
        self.assertEqual(result.inherited_context, base_result.inherited_context)
        self.assertEqual(result.documentation_strategy, base_result.documentation_strategy)
        self.assertEqual(result.feature_understanding, base_result.feature_understanding)


class TestAgentBIntegration(unittest.TestCase):
    """Test Agent B integration scenarios"""
    
    def setUp(self):
        """Set up test environment"""
        with patch('learning_framework.integrations.agent_b_integration.AgentLearningFramework'):
            self.agent_basic = AgentB()
            self.agent_enhanced = AgentBWithLearning()
    
    def test_backward_compatibility(self):
        """Test that enhanced agent maintains backward compatibility"""
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'enhancements': {
                        'technical_scope': {
                            'feature_type': 'cluster_management',
                            'feature_name': 'Test Feature',
                            'primary_components': ['TestComponent']
                        }
                    }
                }
            }
        }
        
        # Run both versions
        basic_result = self.agent_basic.execute_enhanced_workflow(test_context)
        enhanced_result = self.agent_enhanced.execute_enhanced_workflow(test_context)
        
        # Remove learning insights for comparison
        enhanced_docs = enhanced_result.documentation_analysis.copy()
        enhanced_docs.pop('learning_insights', None)
        
        # Core results should be identical
        self.assertEqual(basic_result.inherited_context, enhanced_result.inherited_context)
        self.assertEqual(basic_result.documentation_strategy, enhanced_result.documentation_strategy)
        self.assertEqual(basic_result.documentation_analysis, enhanced_docs)
        self.assertEqual(basic_result.feature_understanding, enhanced_result.feature_understanding)
    
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
            {'feature': 'ClusterCurator'},
            {'feature': 'ACM-Operator'},
            {'feature': 'MCE-Controller'}
        ]
        
        for context in contexts:
            with self.subTest(context=context):
                # Both agents should handle all contexts
                basic_result = self.agent_basic.execute_enhanced_workflow(context)
                enhanced_result = self.agent_enhanced.execute_enhanced_workflow(context)
                
                self.assertIsInstance(basic_result, EnhancedDocumentationResult)
                self.assertIsInstance(enhanced_result, EnhancedDocumentationResult)
                self.assertGreater(basic_result.confidence_level, 0)
                self.assertGreater(enhanced_result.confidence_level, 0)


class TestAgentBErrorHandling(unittest.TestCase):
    """Test Agent B error handling and edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = AgentB()
    
    def test_empty_context_handling(self):
        """Test handling of empty context"""
        result = self.agent.execute_enhanced_workflow({})
        
        self.assertIsInstance(result, EnhancedDocumentationResult)
        self.assertEqual(result.inherited_context, {})
        self.assertGreater(result.confidence_level, 0)
    
    def test_none_context_handling(self):
        """Test handling of None context"""
        result = self.agent.execute_enhanced_workflow(None)
        
        self.assertIsInstance(result, EnhancedDocumentationResult)
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
                
                self.assertIsInstance(result, EnhancedDocumentationResult)
                self.assertEqual(result.inherited_context, context)
                self.assertGreater(result.confidence_level, 0)
    
    def test_very_large_context_handling(self):
        """Test handling of very large context objects"""
        large_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'large_data': 'x' * 10000,  # 10KB of data
                    'enhancements': {
                        'technical_scope': {
                            'feature_name': 'Large Feature Name',
                            'components': list(range(100))
                        }
                    }
                }
            }
        }
        
        start_time = time.time()
        result = self.agent.execute_enhanced_workflow(large_context)
        execution_time = time.time() - start_time
        
        self.assertIsInstance(result, EnhancedDocumentationResult)
        self.assertLess(execution_time, 10.0, "Should handle large contexts within 10 seconds")
    
    def test_concurrent_execution(self):
        """Test concurrent execution of documentation analysis"""
        import threading
        
        results = {}
        errors = {}
        
        def analyze_documentation(thread_id, context):
            try:
                result = self.agent.execute_enhanced_workflow(context)
                results[thread_id] = result
            except Exception as e:
                errors[thread_id] = str(e)
        
        # Create threads for concurrent analysis
        threads = []
        contexts = [
            {'context_id': 1, 'feature': 'feature1'},
            {'context_id': 2, 'feature': 'feature2'},
            {'context_id': 3, 'feature': 'feature3'}
        ]
        
        for i, context in enumerate(contexts):
            thread = threading.Thread(target=analyze_documentation, args=(i, context))
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
    print("🧪 Agent B (Documentation Intelligence) Implementation Unit Tests")
    print("Testing agent logic for documentation analysis and intelligence")
    print("=" * 70)
    
    unittest.main(verbosity=2)