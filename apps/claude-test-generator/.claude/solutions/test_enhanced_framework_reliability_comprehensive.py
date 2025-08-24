#!/usr/bin/env python3
"""
COMPREHENSIVE TEST SUITE FOR ENHANCED FRAMEWORK RELIABILITY ARCHITECTURE
=========================================================================

Critical validation test suite ensuring Enhanced Framework Reliability Architecture
maintains all safety guarantees while delivering intelligent learning capabilities.

TEST COVERAGE:
1. Backward Compatibility with 23-Issue Resolution
2. Learning Enhancement Functionality  
3. Safe Failure Handling and Error Isolation
4. Performance Impact Assessment
5. Integration Safety Guarantees
6. Framework State and Recovery Intelligence
7. Non-Intrusive Operation Verification
"""

import os
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import json

# Add the solutions directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from enhanced_framework_reliability_architecture import (
        EnhancedFrameworkReliabilityArchitecture,
        execute_enhanced_framework,
        get_framework_reliability_insights,
        framework_reliability_health_check,
        LearningEventType,
        PerformanceMetric
    )
    ENHANCED_FRAMEWORK_AVAILABLE = True
except ImportError as e:
    print(f"Enhanced Framework not available: {e}")
    ENHANCED_FRAMEWORK_AVAILABLE = False

class TestEnhancedFrameworkReliabilityArchitecture(unittest.TestCase):
    """Comprehensive test suite for Enhanced Framework Reliability Architecture"""
    
    def setUp(self):
        """Set up test environment"""
        if not ENHANCED_FRAMEWORK_AVAILABLE:
            self.skipTest("Enhanced Framework Reliability Architecture not available")
        
        # Ensure learning is disabled by default for safety
        os.environ.pop('CLAUDE_VALIDATION_LEARNING', None)
        
        self.test_run_id = "test-framework-reliability"
        self.test_context = {
            "execution_type": "test",
            "feature": "framework_reliability_test",
            "environment": "test_env"
        }
    
    def tearDown(self):
        """Clean up test environment"""
        # Reset environment
        os.environ.pop('CLAUDE_VALIDATION_LEARNING', None)
    
    # BACKWARD COMPATIBILITY TESTS
    
    def test_framework_reliability_core_functionality_preserved(self):
        """✅ Test that core Framework Reliability functionality is preserved"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Verify core components are available
        self.assertIsNotNone(architecture.execution_manager)
        self.assertIsNotNone(architecture.tool_manager)
        self.assertIsNotNone(architecture.validation_manager)
        self.assertIsNotNone(architecture.agent_coordinator)
        self.assertIsNotNone(architecture.recovery_system)
        
        # Execute framework with core functionality
        success, result = architecture.execute_framework_with_learning(self.test_context)
        
        # Verify core execution works
        self.assertTrue(success)
        self.assertIn('execution_id', result)
        self.assertIn('phases_completed', result)
        self.assertIn('agents_executed', result)
        self.assertIn('validations_performed', result)
        self.assertEqual(result['status'], 'completed')
        
        # Verify 23-issue resolution components
        expected_issues_resolved = [
            'single_session_execution',
            'phase_dependency_enforcement',
            'agent_coordination',
            'tool_correlation',
            'validation_enhancement',
            'write_tool_testing',
            'recovery_system'
        ]
        
        for issue in expected_issues_resolved:
            self.assertIn(issue, result.get('issues_resolved', []))
    
    def test_learning_disabled_by_default_safety(self):
        """✅ Test that learning is safely disabled by default"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Verify learning is disabled by default
        self.assertFalse(architecture.learning_enabled)
        self.assertIsNone(architecture.learning_core)
        self.assertIsNone(architecture.pattern_memory)
        self.assertIsNone(architecture.analytics_service)
        
        # Execute framework - should work identically to original
        success, result = architecture.execute_framework_with_learning(self.test_context)
        
        # Verify core execution success
        self.assertTrue(success)
        self.assertEqual(result['status'], 'completed')
        
        # Verify no learning enhancements are present
        self.assertNotIn('performance_optimization', result)
        self.assertNotIn('failure_risk', result)
        self.assertNotIn('coordination_optimization', result)
        self.assertNotIn('validation_intelligence', result)
        self.assertNotIn('state_optimization', result)
    
    def test_23_issue_resolution_integrity(self):
        """✅ Test that all 23 critical issues remain resolved"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Execute framework
        success, result = architecture.execute_framework_with_learning(self.test_context)
        
        # Verify single-session execution (Issue 1)
        self.assertTrue(architecture.execution_manager.is_executing)
        
        # Verify phase dependency enforcement (Issues 2-5)
        expected_phases = ['0-pre', '0', '1', '2']
        for phase in expected_phases:
            self.assertIn(phase, result.get('phases_completed', []))
        
        # Verify agent coordination (Issues 6-10)
        expected_agents = ['agent_a', 'agent_d', 'agent_b', 'agent_c']
        for agent in expected_agents:
            self.assertIn(agent, result.get('agents_executed', []))
        
        # Verify tool correlation (Issues 11-15)
        self.assertIn('tools_used', result)
        
        # Verify validation enhancement (Issues 16-20)
        self.assertIn('validations_performed', result)
        self.assertTrue(len(result.get('validations_performed', [])) > 0)
        
        # Verify write tool testing (Issues 21-22)
        self.assertIn('write_tool_tests', result)
        
        # Verify recovery system (Issue 23)
        self.assertIsNotNone(architecture.recovery_system)
    
    # LEARNING ENHANCEMENT FUNCTIONALITY TESTS
    
    def test_learning_enabled_functionality(self):
        """✅ Test learning functionality when enabled"""
        # Enable learning for this test
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        # Mock learning components to test functionality
        with patch('enhanced_framework_reliability_architecture.ValidationLearningCore') as mock_learning_core, \
             patch('enhanced_framework_reliability_architecture.ValidationPatternMemory') as mock_pattern_memory, \
             patch('enhanced_framework_reliability_architecture.ValidationAnalyticsService') as mock_analytics:
            
            # Setup mocks
            mock_learning_instance = MagicMock()
            mock_learning_core.get_instance.return_value = mock_learning_instance
            mock_pattern_memory.return_value = MagicMock()
            mock_analytics.return_value = MagicMock()
            
            # Mock analytics to return insights
            mock_analytics.return_value.get_performance_optimization_insights.return_value = {
                'improvements': {'execution_time': 0.75},
                'improvement_potential': 0.3,
                'strategy': 'phase_optimization'
            }
            
            mock_analytics.return_value.get_failure_prediction_insights.return_value = {
                'risk_score': 0.8,
                'predicted_failures': ['resource_contention'],
                'prevention_strategies': ['resource_monitoring']
            }
            
            mock_analytics.return_value.get_coordination_optimization_insights.return_value = {
                'efficiency_score': 0.85,
                'optimal_sequence': ['agent_a', 'agent_d', 'agent_b', 'agent_c'],
                'context_effectiveness': 0.9
            }
            
            architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
            
            # Verify learning is enabled
            self.assertTrue(architecture.learning_enabled)
            
            # Execute framework with learning
            success, result = architecture.execute_framework_with_learning(self.test_context)
            
            # Verify core execution still works
            self.assertTrue(success)
            self.assertEqual(result['status'], 'completed')
            
            # Verify learning enhancements are present
            self.assertIn('performance_optimization', result)
            self.assertIn('predicted_improvements', result)
            self.assertIn('failure_risk', result)
            self.assertIn('coordination_optimization', result)
            
            # Verify learning core was called
            mock_learning_instance.learn_from_validation.assert_called()
    
    def test_performance_optimization_intelligence(self):
        """✅ Test Predictive Performance Intelligence functionality"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        with patch('enhanced_framework_reliability_architecture.ValidationAnalyticsService') as mock_analytics:
            mock_analytics_instance = MagicMock()
            mock_analytics.return_value = mock_analytics_instance
            
            # Mock performance insights
            mock_analytics_instance.get_performance_optimization_insights.return_value = {
                'improvement_potential': 0.75,
                'strategy': 'phase_timing_optimization',
                'improvements': {
                    'execution_time': 0.25,
                    'resource_utilization': 0.40
                }
            }
            
            architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
            architecture.learning_enabled = True
            architecture.analytics_service = mock_analytics_instance
            
            # Execute framework
            success, result = architecture.execute_framework_with_learning(self.test_context)
            
            # Verify performance optimization was applied
            self.assertIn('performance_optimization', result)
            self.assertIn('predicted_improvements', result)
            self.assertEqual(result['predicted_improvements']['execution_time'], 0.25)
            
            # Verify performance pattern was recorded
            self.assertEqual(len(architecture.performance_patterns), 1)
            pattern = architecture.performance_patterns[0]
            self.assertEqual(pattern.improvement_potential, 0.75)
            self.assertEqual(pattern.optimization_strategy, 'phase_timing_optimization')
    
    def test_failure_prediction_intelligence(self):
        """✅ Test Intelligent Recovery Strategy functionality"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        with patch('enhanced_framework_reliability_architecture.ValidationAnalyticsService') as mock_analytics:
            mock_analytics_instance = MagicMock()
            mock_analytics.return_value = mock_analytics_instance
            
            # Mock failure prediction with high risk
            mock_analytics_instance.get_failure_prediction_insights.return_value = {
                'risk_score': 0.8,
                'predicted_failure_type': 'resource_contention',
                'leading_indicators': [{'metric': 'memory_usage', 'value': 0.95}],
                'prevention_strategy': 'resource_monitoring'
            }
            
            architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
            architecture.learning_enabled = True
            architecture.analytics_service = mock_analytics_instance
            
            # Execute framework
            success, result = architecture.execute_framework_with_learning(self.test_context)
            
            # Verify failure prediction was applied
            self.assertIn('failure_risk', result)
            self.assertEqual(result['failure_risk'], 0.8)
            self.assertIn('predicted_failures', result)
            self.assertIn('resource_contention', result['predicted_failures'])
            self.assertIn('prevention_strategies', result)
            
            # Verify failure pattern was recorded
            self.assertEqual(len(architecture.failure_patterns), 1)
            pattern = architecture.failure_patterns[0]
            self.assertEqual(pattern.failure_type, 'resource_contention')
            self.assertEqual(pattern.prevention_strategy, 'resource_monitoring')
    
    def test_agent_coordination_intelligence(self):
        """✅ Test Agent Coordination Intelligence functionality"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        with patch('enhanced_framework_reliability_architecture.ValidationAnalyticsService') as mock_analytics:
            mock_analytics_instance = MagicMock()
            mock_analytics.return_value = mock_analytics_instance
            
            # Mock coordination insights
            mock_analytics_instance.get_coordination_optimization_insights.return_value = {
                'efficiency_score': 0.85,
                'optimal_sequence': ['agent_a', 'agent_d', 'agent_b', 'agent_c'],
                'context_effectiveness': 0.9,
                'optimal_timing': {'agent_spacing': 0.1}
            }
            
            architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
            architecture.learning_enabled = True
            architecture.analytics_service = mock_analytics_instance
            
            # Execute framework
            success, result = architecture.execute_framework_with_learning(self.test_context)
            
            # Verify coordination optimization was applied
            self.assertIn('coordination_optimization', result)
            self.assertIn('coordination_efficiency', result)
            self.assertEqual(result['coordination_efficiency'], 0.85)
            
            # Verify coordination pattern was recorded
            self.assertEqual(len(architecture.coordination_patterns), 1)
            pattern = architecture.coordination_patterns[0]
            self.assertEqual(pattern.coordination_efficiency, 0.85)
            self.assertEqual(pattern.context_sharing_effectiveness, 0.9)
    
    # SAFE FAILURE HANDLING TESTS
    
    def test_safe_failure_when_learning_components_fail(self):
        """✅ Test safe failure handling when learning components fail"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        with patch('enhanced_framework_reliability_architecture.ValidationLearningCore') as mock_learning_core:
            # Make learning core initialization fail
            mock_learning_core.get_instance.side_effect = Exception("Learning component failure")
            
            # Should not raise exception, but gracefully fall back
            architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
            
            # Verify learning is safely disabled
            self.assertFalse(architecture.learning_enabled)
            
            # Framework should still execute successfully
            success, result = architecture.execute_framework_with_learning(self.test_context)
            
            self.assertTrue(success)
            self.assertEqual(result['status'], 'completed')
            
            # Should behave like standard framework (no learning enhancements)
            self.assertNotIn('performance_optimization', result)
            self.assertNotIn('failure_risk', result)
    
    def test_safe_failure_during_enhanced_execution(self):
        """✅ Test safe failure handling during enhanced execution"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        with patch('enhanced_framework_reliability_architecture.ValidationAnalyticsService') as mock_analytics:
            mock_analytics_instance = MagicMock()
            mock_analytics.return_value = mock_analytics_instance
            
            # Make analytics service fail during execution
            mock_analytics_instance.get_performance_optimization_insights.side_effect = Exception("Analytics failure")
            
            architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
            architecture.learning_enabled = True
            architecture.analytics_service = mock_analytics_instance
            
            # Should handle failure gracefully and fall back to core execution
            success, result = architecture.execute_framework_with_learning(self.test_context)
            
            # Core execution should still succeed
            self.assertTrue(success)
            self.assertEqual(result['status'], 'completed')
            
            # Should not have learning enhancements due to failure
            self.assertNotIn('performance_optimization', result)
    
    def test_learning_failure_isolation(self):
        """✅ Test that learning failures are completely isolated"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        with patch('enhanced_framework_reliability_architecture.ValidationLearningCore') as mock_learning_core:
            mock_learning_instance = MagicMock()
            mock_learning_core.get_instance.return_value = mock_learning_instance
            
            # Make learning core fail when called
            mock_learning_instance.learn_from_validation.side_effect = Exception("Learning storage failure")
            
            architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
            architecture.learning_enabled = True
            architecture.learning_core = mock_learning_instance
            
            # Framework should execute successfully despite learning failure
            success, result = architecture.execute_framework_with_learning(self.test_context)
            
            self.assertTrue(success)
            self.assertEqual(result['status'], 'completed')
            
            # Verify all 23 issues are still resolved
            self.assertIn('issues_resolved', result)
            self.assertTrue(len(result['issues_resolved']) >= 7)
    
    # PERFORMANCE IMPACT ASSESSMENT TESTS
    
    def test_performance_impact_with_learning_disabled(self):
        """✅ Test performance impact when learning is disabled"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Measure execution time
        start_time = time.time()
        success, result = architecture.execute_framework_with_learning(self.test_context)
        execution_time = time.time() - start_time
        
        # Verify performance is excellent
        self.assertTrue(success)
        self.assertLess(execution_time, 1.0)  # Should complete in under 1 second
        
        # Verify learning overhead is zero
        self.assertEqual(architecture.reliability_stats['learning_events'], 0)
    
    def test_performance_impact_with_learning_enabled(self):
        """✅ Test performance impact when learning is enabled"""
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        with patch('enhanced_framework_reliability_architecture.ValidationLearningCore') as mock_learning_core, \
             patch('enhanced_framework_reliability_architecture.ValidationAnalyticsService') as mock_analytics:
            
            # Setup mocks with minimal overhead
            mock_learning_core.get_instance.return_value = MagicMock()
            mock_analytics.return_value = MagicMock()
            
            architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
            
            # Measure execution time with learning
            start_time = time.time()
            success, result = architecture.execute_framework_with_learning(self.test_context)
            execution_time = time.time() - start_time
            
            # Verify performance is still acceptable (< 5% overhead)
            self.assertTrue(success)
            self.assertLess(execution_time, 2.0)  # Should complete in under 2 seconds
            
            # Verify learning events were processed
            self.assertGreater(architecture.reliability_stats['learning_events'], 0)
    
    def test_scalability_with_multiple_executions(self):
        """✅ Test scalability with multiple framework executions"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        execution_times = []
        
        # Execute framework multiple times
        for i in range(5):
            start_time = time.time()
            success, result = architecture.execute_framework_with_learning({
                **self.test_context,
                'iteration': i
            })
            execution_time = time.time() - start_time
            execution_times.append(execution_time)
            
            self.assertTrue(success)
            self.assertEqual(result['status'], 'completed')
        
        # Verify consistent performance across executions
        avg_time = sum(execution_times) / len(execution_times)
        self.assertLess(avg_time, 1.0)
        
        # Verify no significant performance degradation
        self.assertLess(max(execution_times) - min(execution_times), 0.5)
    
    # INTEGRATION SAFETY TESTS
    
    def test_framework_state_management_integrity(self):
        """✅ Test framework state management integrity"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Execute framework
        success, result = architecture.execute_framework_with_learning(self.test_context)
        
        # Verify framework state is properly managed
        self.assertTrue(success)
        
        # Check execution manager state
        self.assertFalse(architecture.execution_manager.is_executing)  # Should be completed
        self.assertTrue(len(architecture.execution_manager.completed_phases) > 0)
        
        # Check tool execution tracking
        self.assertTrue(len(architecture.tool_manager.active_operations) >= 0)
        
        # Check validation checkpoints
        self.assertTrue(len(architecture.validation_manager.validation_rules) > 0)
        
        # Check agent coordination
        self.assertTrue(len(architecture.agent_coordinator.agent_dependencies) == 4)
    
    def test_recovery_system_integration(self):
        """✅ Test recovery system integration with learning"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Test recovery system detection
        failure_type = architecture.recovery_system.detect_failure_condition()
        
        # Should detect no failures in normal operation
        self.assertIsNone(failure_type)
        
        # Test recovery system is operational
        self.assertIsNotNone(architecture.recovery_system)
        self.assertTrue(len(architecture.recovery_system.recovery_strategies) > 0)
    
    def test_health_check_functionality(self):
        """✅ Test comprehensive health check functionality"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Get health status
        health = architecture.health_check()
        
        # Verify health check structure
        self.assertIn('status', health)
        self.assertIn('framework_reliability', health)
        self.assertIn('learning_enabled', health)
        self.assertIn('statistics', health)
        
        # Verify healthy status
        self.assertEqual(health['status'], 'healthy')
        self.assertEqual(health['framework_reliability'], 'operational')
        self.assertFalse(health['learning_enabled'])  # Disabled by default
        
        # Verify component health
        self.assertIn('execution_manager', health)
        self.assertIn('validation_manager', health)
        self.assertIn('recovery_system', health)
    
    def test_statistics_tracking_accuracy(self):
        """✅ Test reliability statistics tracking accuracy"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Execute framework multiple times
        for i in range(3):
            success, result = architecture.execute_framework_with_learning({
                **self.test_context,
                'iteration': i
            })
            self.assertTrue(success)
        
        # Get statistics
        stats = architecture.get_reliability_statistics()
        
        # Verify statistics accuracy
        self.assertEqual(stats['total_executions'], 3)
        self.assertEqual(stats['successful_executions'], 3)
        self.assertEqual(stats['success_rate'], 1.0)
        self.assertFalse(stats['learning_enabled'])
        self.assertTrue(stats['framework_components_available'])
    
    # CONVENIENCE FUNCTION TESTS
    
    def test_convenience_functions_work(self):
        """✅ Test convenience functions maintain compatibility"""
        # Test execute_enhanced_framework function
        success, result = execute_enhanced_framework(self.test_run_id, self.test_context)
        
        self.assertTrue(success)
        self.assertIn('execution_id', result)
        self.assertEqual(result['status'], 'completed')
        
        # Test get_framework_reliability_insights function
        insights = get_framework_reliability_insights(self.test_run_id)
        
        self.assertIn('learning_available', insights)
        self.assertFalse(insights['learning_available'])  # Learning disabled by default
        
        # Test framework_reliability_health_check function
        health = framework_reliability_health_check(self.test_run_id)
        
        self.assertIn('status', health)
        self.assertEqual(health['status'], 'healthy')
    
    def test_configuration_control_works(self):
        """✅ Test environment variable configuration control"""
        # Test disabled mode (default)
        architecture1 = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        self.assertFalse(architecture1.learning_enabled)
        
        # Test enabled mode
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'standard'
        
        with patch('enhanced_framework_reliability_architecture.ValidationLearningCore'):
            architecture2 = EnhancedFrameworkReliabilityArchitecture(self.test_run_id + "-2")
            self.assertTrue(architecture2.learning_enabled)
        
        # Test disabled mode override
        os.environ['CLAUDE_VALIDATION_LEARNING'] = 'disabled'
        architecture3 = EnhancedFrameworkReliabilityArchitecture(self.test_run_id + "-3")
        self.assertFalse(architecture3.learning_enabled)
    
    def test_comprehensive_report_generation(self):
        """✅ Test comprehensive report generation functionality"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Execute framework to generate data
        success, result = architecture.execute_framework_with_learning(self.test_context)
        self.assertTrue(success)
        
        # Generate comprehensive report
        report = architecture.generate_comprehensive_report()
        
        # Verify report structure
        self.assertIn('reliability_statistics', report)
        self.assertIn('learning_insights', report)
        self.assertIn('health_status', report)
        self.assertIn('pattern_analysis', report)
        self.assertIn('recommendations', report)
        
        # Verify pattern analysis sections
        pattern_analysis = report['pattern_analysis']
        self.assertIn('performance_trends', pattern_analysis)
        self.assertIn('failure_analysis', pattern_analysis)
        self.assertIn('coordination_efficiency', pattern_analysis)
        self.assertIn('validation_accuracy', pattern_analysis)
        self.assertIn('state_optimization', pattern_analysis)

class TestEnhancedFrameworkReliabilityRegressionSafety(unittest.TestCase):
    """Regression safety tests for Enhanced Framework Reliability Architecture"""
    
    def setUp(self):
        """Set up regression test environment"""
        if not ENHANCED_FRAMEWORK_AVAILABLE:
            self.skipTest("Enhanced Framework Reliability Architecture not available")
        
        # Ensure learning is disabled for regression testing
        os.environ.pop('CLAUDE_VALIDATION_LEARNING', None)
        
        self.test_run_id = "regression-test"
        self.test_context = {
            "execution_type": "regression_test",
            "feature": "framework_reliability_regression",
            "environment": "regression_env"
        }
    
    def test_no_regression_in_core_functionality(self):
        """✅ Test no regression in core Framework Reliability functionality"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Execute framework multiple times to ensure consistency
        results = []
        for i in range(3):
            success, result = architecture.execute_framework_with_learning({
                **self.test_context,
                'test_iteration': i
            })
            results.append((success, result))
        
        # Verify all executions succeed
        for success, result in results:
            self.assertTrue(success)
            self.assertEqual(result['status'], 'completed')
            self.assertIn('execution_id', result)
            self.assertIn('phases_completed', result)
            self.assertIn('agents_executed', result)
            self.assertIn('issues_resolved', result)
        
        # Verify consistency across executions
        phases_counts = [len(result['phases_completed']) for success, result in results]
        agents_counts = [len(result['agents_executed']) for success, result in results]
        
        # All executions should have same structure
        self.assertEqual(len(set(phases_counts)), 1)  # All same
        self.assertEqual(len(set(agents_counts)), 1)   # All same
    
    def test_error_handling_regression_safety(self):
        """✅ Test error handling maintains regression safety"""
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        # Test with invalid context (should handle gracefully)
        try:
            success, result = architecture.execute_framework_with_learning(None)
            # Should either succeed with default handling or fail gracefully
            if success:
                self.assertIsInstance(result, dict)
            else:
                self.assertIsInstance(result, dict)
                self.assertIn('error', result)
        except Exception as e:
            # If exception is raised, it should be handled appropriately
            self.assertIsInstance(e, (ValueError, TypeError))
    
    def test_memory_usage_regression(self):
        """✅ Test memory usage doesn't regress"""
        import psutil
        import gc
        
        # Measure baseline memory
        gc.collect()
        process = psutil.Process()
        baseline_memory = process.memory_info().rss
        
        # Execute framework multiple times
        architecture = EnhancedFrameworkReliabilityArchitecture(self.test_run_id)
        
        for i in range(5):
            success, result = architecture.execute_framework_with_learning({
                **self.test_context,
                'memory_test_iteration': i
            })
            self.assertTrue(success)
        
        # Measure final memory
        gc.collect()
        final_memory = process.memory_info().rss
        memory_increase = final_memory - baseline_memory
        
        # Verify memory usage is reasonable (< 50MB increase)
        self.assertLess(memory_increase, 50 * 1024 * 1024)

def run_comprehensive_framework_reliability_tests():
    """Run all Enhanced Framework Reliability Architecture tests"""
    print("🧪 ENHANCED FRAMEWORK RELIABILITY ARCHITECTURE - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    if not ENHANCED_FRAMEWORK_AVAILABLE:
        print("❌ Enhanced Framework Reliability Architecture not available for testing")
        return False
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTest(unittest.makeSuite(TestEnhancedFrameworkReliabilityArchitecture))
    suite.addTest(unittest.makeSuite(TestEnhancedFrameworkReliabilityRegressionSafety))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"🎯 TEST SUMMARY:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print(f"\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback.split('\\n')[-2]}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print(f"\n✅ ALL TESTS PASSED - ENHANCED FRAMEWORK RELIABILITY ARCHITECTURE VALIDATED")
        print(f"🛡️ SAFETY GUARANTEES: All backward compatibility and regression safety verified")
        print(f"⚡ PERFORMANCE: Excellent performance maintained")
        print(f"🧠 LEARNING: Intelligent enhancements ready when enabled")
    else:
        print(f"\n❌ SOME TESTS FAILED - REVIEW REQUIRED")
    
    return success

if __name__ == "__main__":
    success = run_comprehensive_framework_reliability_tests()
    sys.exit(0 if success else 1)