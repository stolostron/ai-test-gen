#!/usr/bin/env python3
"""
Unit Tests for Agent A (JIRA Intelligence) Implementation
Tests the actual agent logic for JIRA analysis and intelligence
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
    from learning_framework.integrations.agent_a_integration import (
        AgentA, AgentAWithLearning
    )
except ImportError as e:
    print(f"Failed to import Agent A modules: {e}")
    print(f"AI Services path: {setup_ai_services_path()}")
    sys.exit(1)


class TestAgentABasic(unittest.TestCase):
    """Test basic Agent A functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = AgentA()
    
    def test_agent_a_initialization(self):
        """Test Agent A initializes correctly"""
        self.assertIsInstance(self.agent, AgentA)
        self.assertTrue(hasattr(self.agent, 'analyze_jira'))
    
    def test_analyze_jira_basic_functionality(self):
        """Test basic JIRA analysis functionality"""
        ticket = "ACM-12345"
        
        result = self.agent.analyze_jira(ticket)
        
        # Verify return structure
        self.assertIsInstance(result, dict)
        
        # Verify required fields
        required_fields = ['ticket', 'status', 'ticket_type', 'components', 'confidence', 'pr_references', 'version']
        for field in required_fields:
            self.assertIn(field, result, f"Missing required field: {field}")
        
        # Verify field types and values
        self.assertEqual(result['ticket'], ticket)
        self.assertEqual(result['status'], 'success')
        self.assertIsInstance(result['ticket_type'], str)
        self.assertIsInstance(result['components'], list)
        self.assertIsInstance(result['confidence'], (int, float))
        self.assertIsInstance(result['pr_references'], list)
        self.assertIsInstance(result['version'], str)
    
    def test_analyze_jira_different_tickets(self):
        """Test JIRA analysis with different ticket formats"""
        test_tickets = [
            "ACM-12345",
            "ACM-22079", 
            "TEST-999",
            "FEATURE-123"
        ]
        
        for ticket in test_tickets:
            with self.subTest(ticket=ticket):
                result = self.agent.analyze_jira(ticket)
                
                # Should handle all ticket formats
                self.assertEqual(result['ticket'], ticket)
                self.assertEqual(result['status'], 'success')
                self.assertGreater(result['confidence'], 0)
    
    def test_analyze_jira_confidence_range(self):
        """Test that confidence values are within valid range"""
        result = self.agent.analyze_jira("ACM-12345")
        
        confidence = result['confidence']
        self.assertGreaterEqual(confidence, 0.0, "Confidence should be >= 0")
        self.assertLessEqual(confidence, 1.0, "Confidence should be <= 1")
    
    def test_analyze_jira_components_structure(self):
        """Test that components are properly structured"""
        result = self.agent.analyze_jira("ACM-12345")
        
        components = result['components']
        self.assertIsInstance(components, list)
        self.assertGreater(len(components), 0, "Should have at least one component")
        
        # All components should be strings
        for component in components:
            self.assertIsInstance(component, str)
            self.assertGreater(len(component), 0, "Component names should not be empty")
    
    def test_analyze_jira_pr_references(self):
        """Test PR references structure"""
        result = self.agent.analyze_jira("ACM-12345")
        
        pr_references = result['pr_references']
        self.assertIsInstance(pr_references, list)
        
        # PR references should be strings if present
        for pr_ref in pr_references:
            self.assertIsInstance(pr_ref, str)
    
    def test_analyze_jira_execution_time(self):
        """Test that analysis completes within reasonable time"""
        start_time = time.time()
        
        self.agent.analyze_jira("ACM-12345")
        
        execution_time = time.time() - start_time
        self.assertLess(execution_time, 5.0, "Analysis should complete within 5 seconds")
    
    def test_feature_first_analysis_approach(self):
        """Test Agent A optimization: Feature-first analysis approach"""
        result = self.agent.analyze_jira("ACM-22079")
        
        # Verify feature understanding is comprehensive
        self.assertIn('ticket_type', result)
        self.assertIn('components', result)
        
        # Feature understanding should be thorough
        self.assertGreater(len(result['components']), 0, "Should identify feature components")
        self.assertGreater(result['confidence'], 0.8, "Should have high confidence in feature analysis")
        
        # Business context should be present
        self.assertIsInstance(result['ticket_type'], str)
        self.assertNotEqual(result['ticket_type'], '', "Should identify ticket/feature type")
    
    def test_deployment_agnostic_analysis(self):
        """Test Agent A optimization: Analysis completeness regardless of deployment status"""
        # Test with different ticket scenarios that might have different deployment states
        test_scenarios = [
            ("ACM-12345", "deployed_feature"),
            ("ACM-22079", "new_feature"), 
            ("ACM-99999", "future_feature")
        ]
        
        for ticket, scenario_type in test_scenarios:
            with self.subTest(ticket=ticket, scenario=scenario_type):
                result = self.agent.analyze_jira(ticket)
                
                # Analysis should be complete regardless of deployment status
                required_analysis_fields = ['ticket', 'ticket_type', 'components', 'confidence', 'version']
                for field in required_analysis_fields:
                    self.assertIn(field, result, f"Missing {field} in {scenario_type} analysis")
                
                # Confidence should not be artificially limited by deployment status
                self.assertGreater(result['confidence'], 0.5, 
                    f"Analysis confidence should not be limited for {scenario_type}")
    
    def test_version_context_enhancement(self):
        """Test Agent A optimization: Version context enhances rather than limits analysis"""
        result = self.agent.analyze_jira("ACM-22079")
        
        # Version information should be present for context
        self.assertIn('version', result)
        self.assertIsInstance(result['version'], str)
        
        # Analysis should not be limited by version information
        # (Should have comprehensive analysis regardless of version status)
        self.assertGreater(len(result['components']), 0, "Version context should not limit component analysis")
        self.assertGreater(result['confidence'], 0.7, "Version context should not artificially reduce confidence")
        
        # PR references should be analyzed comprehensively
        self.assertIn('pr_references', result)
        self.assertIsInstance(result['pr_references'], list)
    
    def test_future_compatibility_analysis(self):
        """Test Agent A optimization: Future-ready intelligence supporting current and future scenarios"""
        result = self.agent.analyze_jira("ACM-12345")
        
        # Analysis structure should support both current and future deployment scenarios
        # Core analysis fields should be deployment-scenario agnostic
        future_ready_fields = ['ticket', 'ticket_type', 'components', 'confidence', 'pr_references', 'version']
        
        for field in future_ready_fields:
            self.assertIn(field, result, f"Missing future-compatible field: {field}")
        
        # Analysis should provide rich context that works for multiple scenarios
        self.assertIsInstance(result['components'], list)
        self.assertTrue(len(result['components']) > 0 or result['confidence'] > 0.8, 
            "Should provide either component analysis or high confidence feature understanding")
    
    def test_business_context_quality(self):
        """Test Agent A optimization: Strong customer and business requirements foundation"""
        result = self.agent.analyze_jira("ACM-22079")
        
        # Should identify business-relevant information
        self.assertIn('ticket_type', result)
        self.assertIn('components', result)
        
        # Business context indicators
        business_indicators = [
            result['ticket_type'] != '',  # Identifies feature type
            len(result['components']) > 0,  # Identifies affected components
            result['confidence'] > 0.0,  # Has confidence in analysis
            isinstance(result['pr_references'], list)  # Tracks implementation details
        ]
        
        business_quality_score = sum(business_indicators) / len(business_indicators)
        self.assertGreater(business_quality_score, 0.75, 
            "Should demonstrate strong business context quality (>75% indicators present)")


class TestAgentAWithLearning(unittest.TestCase):
    """Test Agent A with learning capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock the learning framework to avoid external dependencies
        with patch('learning_framework.integrations.agent_a_integration.AgentLearningFramework') as mock_framework:
            self.mock_learning_framework = Mock()
            mock_framework.return_value = self.mock_learning_framework
            
            self.agent = AgentAWithLearning()
    
    def test_agent_a_with_learning_initialization(self):
        """Test Agent A with learning initializes correctly"""
        self.assertIsInstance(self.agent, AgentAWithLearning)
        self.assertTrue(hasattr(self.agent, 'learning_framework'))
        self.assertTrue(hasattr(self.agent, 'learning_enabled'))
        self.assertEqual(self.agent.agent_id, 'agent_a')
        self.assertTrue(self.agent.learning_enabled)
    
    def test_analyze_jira_with_learning_disabled(self):
        """Test JIRA analysis when learning is disabled"""
        self.agent.disable_learning()
        
        result = self.agent.analyze_jira("ACM-12345")
        
        # Should still work with learning disabled
        self.assertEqual(result['ticket'], "ACM-12345")
        self.assertEqual(result['status'], 'success')
        
        # Learning framework should not be called
        self.mock_learning_framework.apply_learnings.assert_not_called()
    
    def test_analyze_jira_with_learning_enabled(self):
        """Test JIRA analysis with learning enabled"""
        # Mock learning framework responses
        self.mock_learning_framework.apply_learnings.return_value = {
            'confidence_adjustment': 0.05,
            'patterns': ['pattern1', 'pattern2'],
            'optimization_suggestions': ['hint1', 'hint2']
        }
        
        result = self.agent.analyze_jira("ACM-12345")
        
        # Verify learning framework was called
        self.mock_learning_framework.apply_learnings.assert_called_once()
        
        # Verify learning insights were added
        self.assertIn('learning_insights', result)
        insights = result['learning_insights']
        self.assertEqual(insights['patterns_applied'], 2)
        self.assertEqual(len(insights['optimization_hints']), 2)
    
    def test_analyze_jira_confidence_boost(self):
        """Test that learning can boost confidence"""
        # Mock learning framework to boost confidence
        self.mock_learning_framework.apply_learnings.return_value = {
            'confidence_adjustment': 0.08,
            'patterns': ['high_confidence_pattern']
        }
        
        result = self.agent.analyze_jira("ACM-12345")
        
        # Confidence should be boosted (original 0.90 + 0.08 = 0.98)
        self.assertGreater(result['confidence'], 0.95)
        self.assertLessEqual(result['confidence'], 0.99)  # Capped at 99%
    
    def test_analyze_jira_learning_error_handling(self):
        """Test that learning errors don't break main functionality"""
        # Mock learning framework to raise error
        self.mock_learning_framework.apply_learnings.side_effect = Exception("Learning error")
        
        result = self.agent.analyze_jira("ACM-12345")
        
        # Should still work despite learning error
        self.assertEqual(result['ticket'], "ACM-12345")
        self.assertEqual(result['status'], 'success')
        self.assertNotIn('learning_insights', result)
    
    def test_keyword_extraction(self):
        """Test keyword extraction functionality"""
        keywords = self.agent._extract_keywords("ACM-12345")
        
        self.assertIsInstance(keywords, list)
        self.assertIn('acm', keywords)
        
        # Test different ticket formats
        keywords2 = self.agent._extract_keywords("RHACM-999")
        self.assertIn('rhacm', keywords2)
        
        # Test ticket without hyphen
        keywords3 = self.agent._extract_keywords("TEST123")
        self.assertIsInstance(keywords3, list)  # Should not crash
    
    def test_component_keyword_extraction(self):
        """Test component keyword extraction"""
        analysis = {
            'components': ['ClusterCurator', 'test-component', 'acm_operator']
        }
        
        keywords = self.agent._extract_component_keywords(analysis)
        
        self.assertIsInstance(keywords, list)
        self.assertIn('clustercurator', keywords)
        self.assertIn('testcomponent', keywords)
        self.assertIn('acmoperator', keywords)
    
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
        
        self.agent.analyze_jira("ACM-12345")
        
        # Verify async task was created for learning capture
        mock_create_task.assert_called_once()
    
    def test_apply_recommendations_confidence_only_boosts(self):
        """Test that recommendations only boost confidence, never reduce"""
        analysis = {'confidence': 0.8}
        
        # Test positive adjustment
        recommendations = {'confidence_adjustment': 0.1}
        result = self.agent._apply_recommendations(analysis, recommendations)
        self.assertEqual(result['confidence'], 0.9)
        
        # Test negative adjustment (should not apply)
        recommendations = {'confidence_adjustment': -0.2}
        result = self.agent._apply_recommendations(analysis, recommendations)
        self.assertEqual(result['confidence'], 0.8)  # Unchanged
    
    def test_apply_recommendations_confidence_cap(self):
        """Test that confidence is capped at 99%"""
        analysis = {'confidence': 0.95}
        recommendations = {'confidence_adjustment': 0.1}
        
        result = self.agent._apply_recommendations(analysis, recommendations)
        
        self.assertEqual(result['confidence'], 0.99)  # Capped at 99%
    
    def test_inheritance_compatibility(self):
        """Test that AgentAWithLearning is compatible with base AgentA"""
        # Should be instance of both classes
        self.assertIsInstance(self.agent, AgentA)
        self.assertIsInstance(self.agent, AgentAWithLearning)
        
        # Should have all base class methods
        self.assertTrue(hasattr(self.agent, 'analyze_jira'))
        
        # Should maintain same interface
        result = self.agent.analyze_jira("ACM-12345")
        base_agent = AgentA()
        base_result = base_agent.analyze_jira("ACM-12345")
        
        # Core fields should match (excluding learning insights)
        core_fields = ['ticket', 'status', 'ticket_type', 'components', 'version']
        for field in core_fields:
            self.assertEqual(result[field], base_result[field])
    
    def test_optimization_criteria_with_learning(self):
        """Test Agent A optimizations work correctly with learning enabled"""
        # Mock learning framework for optimization validation
        self.mock_learning_framework.apply_learnings.return_value = {
            'confidence_adjustment': 0.05,
            'patterns': ['feature_analysis_pattern', 'business_context_pattern'],
            'optimization_suggestions': ['feature_first_approach', 'deployment_agnostic_analysis']
        }
        
        result = self.agent.analyze_jira("ACM-22079")
        
        # All optimization criteria should still be met with learning enabled
        optimization_validations = [
            # Feature-first analysis approach
            result['ticket_type'] != '' and len(result['components']) > 0,
            
            # Deployment-agnostic analysis completeness
            all(field in result for field in ['ticket', 'ticket_type', 'components', 'confidence', 'version']),
            
            # Version context enhancement (not limitation)
            result['confidence'] > 0.7 and len(result['components']) > 0,
            
            # Future compatibility
            all(field in result for field in ['ticket', 'ticket_type', 'components', 'confidence', 'pr_references', 'version']),
            
            # Business context quality
            result['confidence'] > 0.0 and isinstance(result['pr_references'], list)
        ]
        
        optimization_score = sum(optimization_validations) / len(optimization_validations)
        self.assertGreater(optimization_score, 0.8, 
            "Agent A optimizations should work correctly with learning enabled (>80% criteria met)")
        
        # Learning should enhance, not replace, the optimization features
        self.assertIn('learning_insights', result)
        insights = result['learning_insights']
        self.assertGreater(insights['patterns_applied'], 0, "Learning should apply optimization patterns")


class TestAgentAIntegration(unittest.TestCase):
    """Test Agent A integration scenarios"""
    
    def setUp(self):
        """Set up test environment"""
        with patch('learning_framework.integrations.agent_a_integration.AgentLearningFramework'):
            self.agent_basic = AgentA()
            self.agent_enhanced = AgentAWithLearning()
    
    def test_backward_compatibility(self):
        """Test that enhanced agent maintains backward compatibility"""
        ticket = "ACM-22079"
        
        # Run both versions
        basic_result = self.agent_basic.analyze_jira(ticket)
        enhanced_result = self.agent_enhanced.analyze_jira(ticket)
        
        # Remove learning insights for comparison
        enhanced_compare = enhanced_result.copy()
        enhanced_compare.pop('learning_insights', None)
        
        # Core results should be identical
        core_fields = ['ticket', 'status', 'ticket_type', 'components', 'version', 'pr_references']
        for field in core_fields:
            self.assertEqual(basic_result[field], enhanced_compare[field], 
                           f"Field {field} differs between basic and enhanced agents")
    
    def test_performance_comparison(self):
        """Test that enhanced agent doesn't significantly impact performance"""
        ticket = "ACM-12345"
        
        # Time basic agent
        start = time.time()
        self.agent_basic.analyze_jira(ticket)
        basic_time = time.time() - start
        
        # Time enhanced agent
        start = time.time()
        self.agent_enhanced.analyze_jira(ticket)
        enhanced_time = time.time() - start
        
        # Enhanced agent should not be significantly slower
        # Allow up to 100% overhead for learning features
        self.assertLess(enhanced_time, basic_time * 2.0, 
                       "Enhanced agent should not be more than 2x slower")
    
    def test_multiple_ticket_analysis(self):
        """Test analyzing multiple tickets in sequence"""
        tickets = ["ACM-12345", "ACM-22079", "ACM-99999"]
        
        for ticket in tickets:
            with self.subTest(ticket=ticket):
                # Both agents should handle all tickets
                basic_result = self.agent_basic.analyze_jira(ticket)
                enhanced_result = self.agent_enhanced.analyze_jira(ticket)
                
                self.assertEqual(basic_result['status'], 'success')
                self.assertEqual(enhanced_result['status'], 'success')
                self.assertEqual(basic_result['ticket'], ticket)
                self.assertEqual(enhanced_result['ticket'], ticket)
    
    def test_concurrent_analysis(self):
        """Test that agents can handle concurrent analysis requests"""
        import threading
        
        results = {}
        errors = {}
        
        def analyze_ticket(agent_name, agent, ticket):
            try:
                result = agent.analyze_jira(ticket)
                results[f"{agent_name}_{ticket}"] = result
            except Exception as e:
                errors[f"{agent_name}_{ticket}"] = str(e)
        
        # Create threads for concurrent analysis
        threads = []
        tickets = ["ACM-1", "ACM-2", "ACM-3"]
        
        for ticket in tickets:
            # Basic agent thread
            thread1 = threading.Thread(target=analyze_ticket, 
                                      args=("basic", self.agent_basic, ticket))
            # Enhanced agent thread
            thread2 = threading.Thread(target=analyze_ticket, 
                                      args=("enhanced", self.agent_enhanced, ticket))
            
            threads.extend([thread1, thread2])
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=10)
        
        # Verify no errors occurred
        self.assertEqual(len(errors), 0, f"Errors occurred during concurrent analysis: {errors}")
        
        # Verify all results were generated
        expected_results = len(tickets) * 2  # 2 agents per ticket
        self.assertEqual(len(results), expected_results, 
                        f"Expected {expected_results} results, got {len(results)}")


class TestAgentAErrorHandling(unittest.TestCase):
    """Test Agent A error handling and edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.agent = AgentA()
    
    def test_empty_ticket_handling(self):
        """Test handling of empty or invalid ticket IDs"""
        # Empty string
        result = self.agent.analyze_jira("")
        self.assertIsInstance(result, dict)
        self.assertEqual(result['ticket'], "")
        
        # None input (should handle gracefully)
        result = self.agent.analyze_jira(None)
        self.assertIsInstance(result, dict)
    
    def test_very_long_ticket_id(self):
        """Test handling of unusually long ticket IDs"""
        long_ticket = "ACM-" + "1" * 1000
        
        result = self.agent.analyze_jira(long_ticket)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['ticket'], long_ticket)
        self.assertEqual(result['status'], 'success')
    
    def test_special_characters_in_ticket(self):
        """Test handling of special characters in ticket IDs"""
        special_tickets = [
            "ACM-12345@test",
            "ACM-12345#hash", 
            "ACM-12345$dollar",
            "ACM-12345%percent"
        ]
        
        for ticket in special_tickets:
            with self.subTest(ticket=ticket):
                result = self.agent.analyze_jira(ticket)
                
                self.assertIsInstance(result, dict)
                self.assertEqual(result['ticket'], ticket)
                self.assertEqual(result['status'], 'success')
    
    def test_unicode_ticket_handling(self):
        """Test handling of unicode characters in ticket IDs"""
        unicode_tickets = [
            "ACM-12345-测试",
            "ACM-12345-тест",
            "ACM-12345-テスト"
        ]
        
        for ticket in unicode_tickets:
            with self.subTest(ticket=ticket):
                result = self.agent.analyze_jira(ticket)
                
                self.assertIsInstance(result, dict)
                self.assertEqual(result['ticket'], ticket)


if __name__ == '__main__':
    print("🧪 Agent A (JIRA Intelligence) Implementation Unit Tests")
    print("Testing agent logic for JIRA analysis and intelligence")
    print("=" * 70)
    
    unittest.main(verbosity=2)