#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Cross-Agent Validation Engine

This test suite validates:
1. Backward compatibility with existing Cross-Agent Validation Engine
2. Learning enhancement functionality when enabled
3. Safe failure handling when learning components fail
4. Performance impact assessment
5. Integration safety guarantees
6. Conflict detection and resolution capabilities
7. Agent coordination and framework state management
"""

import asyncio
import json
import os
import tempfile
import time
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# Add the solutions directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_cross_agent_validation_engine import (
    EnhancedCrossAgentValidationEngine,
    AgentOutput,
    ConflictEvent,
    ConflictType,
    ValidationResult,
    validate_cross_agent_consistency,
    get_cross_agent_insights,
    cross_agent_health_check
)

class TestEnhancedCrossAgentValidationEngine(unittest.TestCase):
    """Comprehensive test suite for Enhanced Cross-Agent Validation Engine"""
    
    def setUp(self):
        """Set up test environment"""
        # Ensure learning is disabled for baseline tests
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'disabled'
        
        # Create test engine
        self.engine = EnhancedCrossAgentValidationEngine()
        
        # Test data - consistent agents
        self.consistent_outputs = {
            'agent_a': AgentOutput(
                agent_id='agent_a',
                output_data={'feature_available': True, 'implementation_method': 'UI'},
                confidence=0.9,
                evidence={'jira_analysis': 'feature confirmed'},
                timestamp=time.time(),
                context={'phase': 'jira_analysis'}
            ),
            'agent_c': AgentOutput(
                agent_id='agent_c',
                output_data={'feature_available': True, 'implementation_method': 'UI'},
                confidence=0.8,
                evidence={'github_scan': 'UI implementation found'},
                timestamp=time.time(),
                context={'phase': 'github_investigation'}
            )
        }
        
        # Test data - conflicting agents
        self.conflicting_outputs = {
            'agent_a': AgentOutput(
                agent_id='agent_a',
                output_data={'feature_available': True, 'schema_fields': {'field1': 'string'}},
                confidence=0.9,
                evidence={'jira_analysis': 'feature confirmed'},
                timestamp=time.time(),
                context={'phase': 'jira_analysis'}
            ),
            'agent_c': AgentOutput(
                agent_id='agent_c',
                output_data={'feature_available': False, 'schema_fields': {'field1': 'integer'}},
                confidence=0.8,
                evidence={'github_scan': 'no implementation found'},
                timestamp=time.time(),
                context={'phase': 'github_investigation'}
            )
        }
        
        # Test data - low quality outputs
        self.low_quality_outputs = {
            'agent_a': AgentOutput(
                agent_id='agent_a',
                output_data={'feature_available': True},
                confidence=0.3,  # Low confidence
                evidence={},  # No evidence
                timestamp=time.time(),
                context={'phase': 'jira_analysis'}
            )
        }
        
        self.test_context = {
            "validation_type": "test_validation",
            "feature": "test_feature",
            "environment": "test_env"
        }
    
    def tearDown(self):
        """Clean up test environment"""
        # Reset environment variables
        if 'CLAUDE_VALIDATION_LEARNING' in os.environ:
            del os.environ['CLAUDE_VALIDATION_LEARNING']
    
    # === Backward Compatibility Tests ===
    
    def test_consistent_agents_validation(self):
        """Test validation with consistent agent outputs"""
        success, result = self.engine.validate_agent_consistency(
            self.consistent_outputs,
            self.test_context
        )
        
        self.assertTrue(success)
        self.assertEqual(result['result'], ValidationResult.SUCCESS)
        self.assertTrue(result['framework_consistent'])
        self.assertTrue(result['quality_passed'])
    
    def test_conflicting_agents_detection(self):
        """Test conflict detection with conflicting agent outputs"""
        success, result = self.engine.validate_agent_consistency(
            self.conflicting_outputs,
            self.test_context
        )
        
        self.assertFalse(success)
        self.assertIn(result['result'], [ValidationResult.CONFLICT_RESOLVED, ValidationResult.FRAMEWORK_HALTED])
        
        # Should detect conflicts
        if result['result'] == ValidationResult.FRAMEWORK_HALTED:
            self.assertIn('unresolved_conflicts', result)
        elif result['result'] == ValidationResult.CONFLICT_RESOLVED:
            self.assertIn('conflicts_resolved', result)
    
    def test_quality_gate_enforcement(self):
        """Test quality gate enforcement"""
        success, result = self.engine.validate_agent_consistency(
            self.low_quality_outputs,
            self.test_context
        )
        
        self.assertFalse(success)
        self.assertEqual(result['result'], ValidationResult.QUALITY_FAILURE)
        self.assertIn('quality_issues', result)
        self.assertIn('failed_gates', result)
    
    def test_convenience_functions_work(self):
        """Test that convenience functions work"""
        # Test validation function
        success, result = validate_cross_agent_consistency(
            self.consistent_outputs,
            self.test_context
        )
        self.assertTrue(success)
        
        # Test health check function
        health = cross_agent_health_check()
        self.assertIn('status', health)
        self.assertEqual(health['core_validation'], 'operational')
    
    # === Learning Enhancement Tests ===
    
    def test_learning_disabled_by_default(self):
        """Test that learning is disabled by default"""
        engine = EnhancedCrossAgentValidationEngine()
        self.assertFalse(engine.learning_enabled)
        
        # Validation should work normally
        success, result = engine.validate_agent_consistency(
            self.consistent_outputs,
            self.test_context
        )
        self.assertTrue(success)
    
    def test_learning_enabled_mode(self):
        """Test learning enabled mode with mocked components"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            with patch('enhanced_cross_agent_validation_engine.LEARNING_AVAILABLE', True):
                with patch('enhanced_cross_agent_validation_engine.ValidationLearningCore') as mock_core:
                    with patch('enhanced_cross_agent_validation_engine.ValidationPatternMemory') as mock_memory:
                        with patch('enhanced_cross_agent_validation_engine.ValidationAnalyticsService') as mock_analytics:
                            # Mock successful initialization
                            mock_core.get_instance.return_value = Mock()
                            mock_memory.return_value = Mock()
                            mock_analytics.return_value = Mock()
                            
                            engine = EnhancedCrossAgentValidationEngine()
                            
                            # Verify learning is enabled
                            self.assertTrue(engine.learning_enabled)
                            self.assertIsNotNone(engine.learning_core)
                            self.assertIsNotNone(engine.pattern_memory)
                            self.assertIsNotNone(engine.analytics_service)
    
    def test_enhanced_validation_with_insights(self):
        """Test validation with learning insights"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            with patch('enhanced_cross_agent_validation_engine.LEARNING_AVAILABLE', True):
                # Create mock analytics service
                mock_analytics = Mock()
                mock_analytics.get_conflict_prediction_insights.return_value = {
                    'risk_score': 0.8,
                    'predicted_conflicts': ['feature_availability_conflict']
                }
                mock_analytics.get_evidence_quality_insights.return_value = {
                    'enhanced_reliability': 0.9,
                    'quality_prediction': 0.85
                }
                
                # Create engine with mocked learning
                engine = EnhancedCrossAgentValidationEngine()
                engine.learning_enabled = True
                engine.analytics_service = mock_analytics
                
                success, result = engine.validate_agent_consistency(
                    self.conflicting_outputs,
                    self.test_context
                )
                
                # Check that learning insights might be included
                # (depends on the specific conflict resolution outcome)
                self.assertIsInstance(result, dict)
                self.assertIn('result', result)
    
    # === Safe Failure Handling Tests ===
    
    def test_learning_failure_safe_handling(self):
        """Test that learning failures don't affect core validation"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            # Create engine with broken learning components
            engine = EnhancedCrossAgentValidationEngine()
            engine.learning_enabled = True
            engine.analytics_service = Mock()
            engine.analytics_service.get_conflict_prediction_insights.side_effect = Exception("Learning failed")
            
            # Validation should still work
            success, result = engine.validate_agent_consistency(
                self.consistent_outputs,
                self.test_context
            )
            
            self.assertTrue(success)
            self.assertEqual(result['result'], ValidationResult.SUCCESS)
    
    def test_learning_initialization_failure(self):
        """Test safe handling of learning initialization failure"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            with patch('enhanced_cross_agent_validation_engine.LEARNING_AVAILABLE', True):
                with patch('enhanced_cross_agent_validation_engine.ValidationLearningCore') as mock_core:
                    # Mock initialization failure
                    mock_core.get_instance.side_effect = Exception("Initialization failed")
                    
                    engine = EnhancedCrossAgentValidationEngine()
                    
                    # Learning should be disabled, but validation should work
                    self.assertFalse(engine.learning_enabled)
                    
                    success, result = engine.validate_agent_consistency(
                        self.consistent_outputs,
                        self.test_context
                    )
                    self.assertTrue(success)
    
    def test_learning_unavailable_graceful_handling(self):
        """Test graceful handling when learning components are unavailable"""
        with patch('enhanced_cross_agent_validation_engine.LEARNING_AVAILABLE', False):
            engine = EnhancedCrossAgentValidationEngine()
            
            self.assertFalse(engine.learning_enabled)
            self.assertIsNone(engine.learning_core)
            
            # Validation should work normally
            success, result = engine.validate_agent_consistency(
                self.consistent_outputs,
                self.test_context
            )
            self.assertTrue(success)
    
    # === Performance Impact Tests ===
    
    def test_performance_impact_disabled_mode(self):
        """Test performance impact when learning is disabled"""
        start_time = time.time()
        
        # Run 50 validations
        for _ in range(50):
            self.engine.validate_agent_consistency(
                self.consistent_outputs,
                self.test_context
            )
        
        total_time = time.time() - start_time
        avg_time_per_validation = total_time / 50
        
        # Should be very fast when disabled
        self.assertLess(avg_time_per_validation, 0.02)  # <20ms per validation
    
    def test_performance_impact_enabled_mode(self):
        """Test performance impact when learning is enabled"""
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'standard'}):
            with patch('enhanced_cross_agent_validation_engine.LEARNING_AVAILABLE', True):
                # Create engine with mocked learning (fast operations)
                engine = EnhancedCrossAgentValidationEngine()
                engine.learning_enabled = True
                engine.learning_core = Mock()
                engine.analytics_service = Mock()
                engine.analytics_service.get_conflict_prediction_insights.return_value = None
                engine.analytics_service.get_evidence_quality_insights.return_value = None
                
                start_time = time.time()
                
                # Run 50 validations
                for _ in range(50):
                    engine.validate_agent_consistency(
                        self.consistent_outputs,
                        self.test_context
                    )
                
                total_time = time.time() - start_time
                avg_time_per_validation = total_time / 50
                
                # Should still be fast when enabled with mocked learning
                self.assertLess(avg_time_per_validation, 0.05)  # <50ms per validation
    
    # === Conflict Detection and Resolution Tests ===
    
    def test_conflict_detection_accuracy(self):
        """Test accuracy of conflict detection"""
        # Test feature availability conflict
        feature_conflict_outputs = {
            'agent_a': AgentOutput(
                agent_id='agent_a',
                output_data={'feature_available': True},
                confidence=0.9,
                evidence={'jira': 'feature found'},
                timestamp=time.time(),
                context={}
            ),
            'agent_c': AgentOutput(
                agent_id='agent_c',
                output_data={'feature_available': False},
                confidence=0.8,
                evidence={'github': 'not implemented'},
                timestamp=time.time(),
                context={}
            )
        }
        
        conflicts = self.engine._detect_conflicts_core(feature_conflict_outputs)
        self.assertGreater(len(conflicts), 0)
        self.assertEqual(conflicts[0].conflict_type, ConflictType.FEATURE_AVAILABILITY)
    
    def test_schema_conflict_detection(self):
        """Test schema definition conflict detection"""
        schema_conflict_outputs = {
            'agent_c': AgentOutput(
                agent_id='agent_c',
                output_data={'schema_fields': {'field1': 'string', 'field2': 'integer'}},
                confidence=0.9,
                evidence={'schema_analysis': 'found schema'},
                timestamp=time.time(),
                context={}
            ),
            'agent_d': AgentOutput(
                agent_id='agent_d',
                output_data={'schema_fields': {'field1': 'integer', 'field2': 'string'}},
                confidence=0.8,
                evidence={'env_analysis': 'different schema'},
                timestamp=time.time(),
                context={}
            )
        }
        
        conflicts = self.engine._detect_conflicts_core(schema_conflict_outputs)
        self.assertGreater(len(conflicts), 0)
        self.assertEqual(conflicts[0].conflict_type, ConflictType.SCHEMA_DEFINITION)
    
    def test_authority_hierarchy_resolution(self):
        """Test authority hierarchy conflict resolution"""
        # Create conflict with agents of different authority levels
        test_conflict = ConflictEvent(
            conflict_type=ConflictType.FEATURE_AVAILABILITY,
            agents_involved=['agent_a', 'implementation_reality_agent'],
            conflicting_claims={'agent_a': True, 'implementation_reality_agent': False},
            evidence_quality={'agent_a': 0.7, 'implementation_reality_agent': 0.9},
            context={},
            resolution_strategy=None,
            resolution_time=None,
            resolution_success=False,
            timestamp=time.time()
        )
        
        resolution = self.engine._apply_authority_hierarchy(test_conflict, {})
        self.assertTrue(resolution['success'])
        self.assertEqual(resolution['authoritative_agent'], 'implementation_reality_agent')
    
    # === Framework State Management Tests ===
    
    def test_framework_state_update(self):
        """Test framework state update functionality"""
        initial_state = self.engine.framework_state.consistency_status
        
        # Update with consistent outputs
        self.engine._update_framework_state(self.consistent_outputs, self.test_context)
        
        # Should maintain or improve consistency
        updated_state = self.engine.framework_state.consistency_status
        self.assertIn(updated_state, ['initialized', 'consistent'])
        
        # Agent outputs should be stored
        self.assertIn('agent_a', self.engine.framework_state.agent_outputs)
        self.assertIn('agent_c', self.engine.framework_state.agent_outputs)
    
    def test_framework_state_conflict_tracking(self):
        """Test framework state conflict tracking"""
        # Update with conflicting outputs
        self.engine._update_framework_state(self.conflicting_outputs, self.test_context)
        
        # Should detect conflicts in state
        self.assertEqual(self.engine.framework_state.consistency_status, 'conflicts_detected')
        self.assertGreater(len(self.engine.framework_state.active_conflicts), 0)
    
    # === Integration Safety Tests ===
    
    def test_multiple_engines_independent_operation(self):
        """Test that multiple engine instances operate independently"""
        engine1 = EnhancedCrossAgentValidationEngine()
        engine2 = EnhancedCrossAgentValidationEngine()
        
        # Both should work independently
        success1, _ = engine1.validate_agent_consistency(
            self.consistent_outputs,
            self.test_context
        )
        
        success2, _ = engine2.validate_agent_consistency(
            self.conflicting_outputs,
            self.test_context
        )
        
        self.assertTrue(success1)
        self.assertFalse(success2)
        
        # Statistics should be independent
        stats1 = engine1.get_validation_statistics()
        stats2 = engine2.get_validation_statistics()
        
        self.assertEqual(stats1['total_validations'], 1)
        self.assertEqual(stats2['total_validations'], 1)
    
    def test_configuration_control(self):
        """Test configuration control via environment variables"""
        # Test disabled mode
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'disabled'}):
            engine = EnhancedCrossAgentValidationEngine()
            self.assertFalse(engine.learning_enabled)
        
        # Test conservative mode
        with patch.dict(os.environ, {'CLAUDE_VALIDATION_LEARNING': 'conservative'}):
            with patch('enhanced_cross_agent_validation_engine.LEARNING_AVAILABLE', True):
                with patch('enhanced_cross_agent_validation_engine.ValidationLearningCore'):
                    with patch('enhanced_cross_agent_validation_engine.ValidationPatternMemory'):
                        with patch('enhanced_cross_agent_validation_engine.ValidationAnalyticsService'):
                            engine = EnhancedCrossAgentValidationEngine()
                            # Would be enabled if mocks work correctly
    
    # === Statistics and Monitoring Tests ===
    
    def test_statistics_tracking(self):
        """Test validation statistics tracking"""
        initial_stats = self.engine.get_validation_statistics()
        
        # Perform some validations
        self.engine.validate_agent_consistency(
            self.consistent_outputs,
            self.test_context
        )
        
        self.engine.validate_agent_consistency(
            self.conflicting_outputs,
            self.test_context
        )
        
        final_stats = self.engine.get_validation_statistics()
        
        # Check statistics updated
        self.assertEqual(final_stats['total_validations'], initial_stats['total_validations'] + 2)
        self.assertIn('success_rate', final_stats)
        self.assertIn('framework_state', final_stats)
    
    def test_health_check_functionality(self):
        """Test health check functionality"""
        health = self.engine.health_check()
        
        self.assertIsInstance(health, dict)
        self.assertIn('status', health)
        self.assertIn('core_validation', health)
        self.assertIn('learning_enabled', health)
        self.assertIn('statistics', health)
        self.assertIn('framework_state', health)
        
        self.assertEqual(health['core_validation'], 'operational')
        self.assertFalse(health['learning_enabled'])
    
    # === Edge Cases Tests ===
    
    def test_empty_agent_outputs_handling(self):
        """Test handling of empty agent outputs"""
        success, result = self.engine.validate_agent_consistency(
            {},
            self.test_context
        )
        
        # Should handle gracefully
        self.assertIsInstance(result, dict)
        self.assertIn('result', result)
    
    def test_single_agent_output_handling(self):
        """Test handling of single agent output"""
        single_output = {'agent_a': self.consistent_outputs['agent_a']}
        
        success, result = self.engine.validate_agent_consistency(
            single_output,
            self.test_context
        )
        
        # Should handle gracefully (no conflicts possible with single agent)
        self.assertIsInstance(result, dict)
        self.assertIn('result', result)
    
    def test_malformed_agent_output_handling(self):
        """Test handling of malformed agent output"""
        malformed_output = {
            'agent_broken': AgentOutput(
                agent_id='agent_broken',
                output_data={},  # Empty output data
                confidence=0.0,  # Zero confidence
                evidence={},     # No evidence
                timestamp=time.time(),
                context={}
            )
        }
        
        success, result = self.engine.validate_agent_consistency(
            malformed_output,
            self.test_context
        )
        
        # Should handle gracefully and likely fail quality gates
        self.assertIsInstance(result, dict)
        self.assertIn('result', result)

class TestLearningInsightsIntegration(unittest.TestCase):
    """Test learning insights integration functionality"""
    
    def test_get_cross_agent_insights_without_learning(self):
        """Test cross-agent insights when learning is disabled"""
        insights = get_cross_agent_insights()
        
        self.assertIsInstance(insights, dict)
        self.assertFalse(insights.get('learning_available', True))
    
    def test_get_cross_agent_insights_with_context(self):
        """Test cross-agent insights with context"""
        test_context = {"feature": "test", "validation_type": "conflict_detection"}
        insights = get_cross_agent_insights(test_context)
        
        self.assertIsInstance(insights, dict)

class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmark tests"""
    
    def test_scalability_benchmark(self):
        """Test scalability with high validation volumes"""
        engine = EnhancedCrossAgentValidationEngine()
        
        test_outputs = {
            'agent_a': AgentOutput(
                agent_id='agent_a',
                output_data={'feature_available': True},
                confidence=0.9,
                evidence={'analysis': 'complete'},
                timestamp=time.time(),
                context={}
            )
        }
        test_context = {"validation_type": "benchmark"}
        
        start_time = time.time()
        
        # Run 500 validations
        for i in range(500):
            success, result = engine.validate_agent_consistency(test_outputs, test_context)
            self.assertTrue(success)
        
        total_time = time.time() - start_time
        validations_per_second = 500 / total_time
        
        # Should handle at least 50 validations per second
        self.assertGreater(validations_per_second, 50)
        
        print(f"Performance benchmark: {validations_per_second:.2f} validations/second")

if __name__ == '__main__':
    # Run specific test categories
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'benchmark':
        # Run only benchmark tests
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPerformanceBenchmarks)
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    else:
        # Run all tests
        unittest.main(verbosity=2)