#!/usr/bin/env python3
"""
Simplified Test Suite for Enhanced Cross-Agent Validation Engine

This test suite focuses on core functionality and backward compatibility.
"""

import os
import sys
import time
import unittest
from pathlib import Path

# Add the solutions directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_cross_agent_validation_engine import (
    EnhancedCrossAgentValidationEngine,
    AgentOutput,
    ValidationResult,
    validate_cross_agent_consistency,
    cross_agent_health_check
)

class TestEnhancedCrossAgentValidationEngineSimple(unittest.TestCase):
    """Simplified test suite focusing on core functionality"""
    
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
                output_data={'feature_available': True},
                confidence=0.9,
                evidence={'jira_analysis': 'feature confirmed'},
                timestamp=time.time(),
                context={'phase': 'jira_analysis'}
            ),
            'agent_c': AgentOutput(
                agent_id='agent_c',
                output_data={'feature_available': False},
                confidence=0.8,
                evidence={'github_scan': 'no implementation found'},
                timestamp=time.time(),
                context={'phase': 'github_investigation'}
            )
        }
        
        # Test data - low quality
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
            "feature": "test_feature"
        }
    
    def tearDown(self):
        """Clean up test environment"""
        if 'CLAUDE_VALIDATION_LEARNING' in os.environ:
            del os.environ['CLAUDE_VALIDATION_LEARNING']
    
    # === Core Functionality Tests ===
    
    def test_consistent_agents_pass_validation(self):
        """Test that consistent agents pass validation"""
        success, result = self.engine.validate_agent_consistency(
            self.consistent_outputs,
            self.test_context
        )
        
        self.assertTrue(success)
        self.assertEqual(result['result'], ValidationResult.SUCCESS)
        self.assertTrue(result['framework_consistent'])
        self.assertTrue(result['quality_passed'])
    
    def test_conflicting_agents_detected(self):
        """Test that conflicting agents are detected"""
        success, result = self.engine.validate_agent_consistency(
            self.conflicting_outputs,
            self.test_context
        )
        
        # Should detect conflict and either resolve or halt
        self.assertFalse(success)
        self.assertIn(result['result'], [
            ValidationResult.CONFLICT_RESOLVED, 
            ValidationResult.FRAMEWORK_HALTED
        ])
    
    def test_quality_gates_enforce_standards(self):
        """Test that quality gates enforce minimum standards"""
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
    
    def test_learning_disabled_by_default(self):
        """Test that learning is disabled by default"""
        engine = EnhancedCrossAgentValidationEngine()
        self.assertFalse(engine.learning_enabled)
    
    def test_statistics_tracking(self):
        """Test that statistics are tracked correctly"""
        initial_stats = self.engine.get_validation_statistics()
        
        # Perform validation
        self.engine.validate_agent_consistency(
            self.consistent_outputs,
            self.test_context
        )
        
        final_stats = self.engine.get_validation_statistics()
        self.assertEqual(final_stats['total_validations'], initial_stats['total_validations'] + 1)
    
    def test_health_check_works(self):
        """Test health check functionality"""
        health = self.engine.health_check()
        
        self.assertIn('status', health)
        self.assertIn('core_validation', health)
        self.assertIn('learning_enabled', health)
        self.assertIn('framework_state', health)
        self.assertEqual(health['core_validation'], 'operational')
        self.assertFalse(health['learning_enabled'])
    
    def test_empty_input_handling(self):
        """Test handling of empty inputs"""
        # Empty outputs
        success, result = self.engine.validate_agent_consistency(
            {},
            self.test_context
        )
        self.assertIsInstance(result, dict)
    
    def test_single_agent_handling(self):
        """Test handling of single agent"""
        single_output = {'agent_a': self.consistent_outputs['agent_a']}
        
        success, result = self.engine.validate_agent_consistency(
            single_output,
            self.test_context
        )
        self.assertIsInstance(result, dict)
    
    def test_framework_state_management(self):
        """Test framework state management"""
        initial_state = self.engine.framework_state.consistency_status
        
        # Perform validation
        self.engine.validate_agent_consistency(
            self.consistent_outputs,
            self.test_context
        )
        
        # Framework state should be updated
        self.assertIn('agent_a', self.engine.framework_state.agent_outputs)
        self.assertIn('agent_c', self.engine.framework_state.agent_outputs)
    
    def test_conflict_detection_accuracy(self):
        """Test conflict detection accuracy"""
        # Create conflicting outputs
        feature_conflict = {
            'agent_a': AgentOutput(
                agent_id='agent_a',
                output_data={'feature_available': True},
                confidence=0.9,
                evidence={'jira': 'found'},
                timestamp=time.time(),
                context={}
            ),
            'agent_c': AgentOutput(
                agent_id='agent_c',
                output_data={'feature_available': False},
                confidence=0.8,
                evidence={'github': 'not found'},
                timestamp=time.time(),
                context={}
            )
        }
        
        conflicts = self.engine._detect_conflicts_core(feature_conflict)
        self.assertGreater(len(conflicts), 0)
    
    def test_engine_independence(self):
        """Test that multiple engines work independently"""
        engine1 = EnhancedCrossAgentValidationEngine()
        engine2 = EnhancedCrossAgentValidationEngine()
        
        # Different validations on different engines
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
        
        # Check independent statistics
        stats1 = engine1.get_validation_statistics()
        stats2 = engine2.get_validation_statistics()
        
        self.assertEqual(stats1['total_validations'], 1)
        self.assertEqual(stats2['total_validations'], 1)

class TestPerformanceBasic(unittest.TestCase):
    """Basic performance tests"""
    
    def test_performance_is_acceptable(self):
        """Test that performance is acceptable"""
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
        test_context = {"validation_type": "performance_test"}
        
        start_time = time.time()
        
        # Run 100 validations
        for _ in range(100):
            success, result = engine.validate_agent_consistency(test_outputs, test_context)
            self.assertTrue(success)
        
        total_time = time.time() - start_time
        avg_time = total_time / 100
        
        # Should be fast (less than 20ms per validation)
        self.assertLess(avg_time, 0.02)
        print(f"Average validation time: {avg_time*1000:.2f}ms")

if __name__ == '__main__':
    unittest.main(verbosity=2)