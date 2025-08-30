#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Factor 3 Budget Monitor
===================================================

Tests the real-time budget monitoring system including alert handling,
threshold management, and optimization recommendations.
"""

import unittest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import time
import threading

# Add source path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

try:
    from context.budget_monitor import (
        BudgetMonitor, BudgetAlert, BudgetThreshold, BudgetOptimization,
        BudgetAlertLevel, create_budget_monitor, setup_console_alert_handler
    )
    from context.context_manager import ContextManager, ContextItemType
    BUDGET_MONITOR_AVAILABLE = True
except ImportError as e:
    BUDGET_MONITOR_AVAILABLE = False
    print(f"⚠️ Budget Monitor not available: {e}")

class TestBudgetThreshold(unittest.TestCase):
    """Test BudgetThreshold functionality"""
    
    def setUp(self):
        if not BUDGET_MONITOR_AVAILABLE:
            self.skipTest("Budget Monitor not available")
    
    def test_threshold_creation(self):
        """Test budget threshold creation"""
        threshold = BudgetThreshold(
            level=BudgetAlertLevel.WARNING,
            utilization=0.7,
            actions=["compress_low_priority", "monitor_closely"]
        )
        
        self.assertEqual(threshold.level, BudgetAlertLevel.WARNING)
        self.assertEqual(threshold.utilization, 0.7)
        self.assertEqual(len(threshold.actions), 2)
    
    def test_threshold_validation(self):
        """Test threshold validation"""
        # Test invalid utilization
        with self.assertRaises(ValueError):
            BudgetThreshold(
                level=BudgetAlertLevel.CRITICAL,
                utilization=1.5,  # Invalid > 1.0
                actions=["test"]
            )
        
        with self.assertRaises(ValueError):
            BudgetThreshold(
                level=BudgetAlertLevel.CRITICAL,
                utilization=-0.1,  # Invalid < 0.0
                actions=["test"]
            )

class TestBudgetAlert(unittest.TestCase):
    """Test BudgetAlert functionality"""
    
    def setUp(self):
        if not BUDGET_MONITOR_AVAILABLE:
            self.skipTest("Budget Monitor not available")
    
    def test_alert_creation(self):
        """Test budget alert creation"""
        alert = BudgetAlert(
            level=BudgetAlertLevel.CRITICAL,
            message="Budget utilization critical",
            utilization=0.85,
            recommended_actions=["compress_immediately", "block_new_content"],
            context_stats={"total_tokens": 17000, "max_tokens": 20000}
        )
        
        self.assertEqual(alert.level, BudgetAlertLevel.CRITICAL)
        self.assertIn("critical", alert.message)
        self.assertEqual(alert.utilization, 0.85)
        self.assertEqual(len(alert.recommended_actions), 2)
        self.assertIsNotNone(alert.timestamp)
    
    def test_alert_severity_ordering(self):
        """Test alert severity ordering"""
        alerts = [
            BudgetAlert(BudgetAlertLevel.INFO, "Info", 0.3, []),
            BudgetAlert(BudgetAlertLevel.EMERGENCY, "Emergency", 0.95, []),
            BudgetAlert(BudgetAlertLevel.WARNING, "Warning", 0.6, []),
            BudgetAlert(BudgetAlertLevel.CRITICAL, "Critical", 0.8, [])
        ]
        
        # Sort by severity
        sorted_alerts = sorted(alerts, key=lambda x: x.level.value)
        
        expected_order = [
            BudgetAlertLevel.INFO,
            BudgetAlertLevel.WARNING,
            BudgetAlertLevel.CRITICAL,
            BudgetAlertLevel.EMERGENCY
        ]
        
        for i, expected_level in enumerate(expected_order):
            self.assertEqual(sorted_alerts[i].level, expected_level)

class TestBudgetMonitor(unittest.TestCase):
    """Test BudgetMonitor core functionality"""
    
    def setUp(self):
        if not BUDGET_MONITOR_AVAILABLE:
            self.skipTest("Budget Monitor not available")
        
        # Create mock context manager
        self.mock_context_manager = Mock(spec=ContextManager)
        self.mock_context_manager.max_tokens = 20000
        self.mock_context_manager.get_context_summary.return_value = Mock(
            total_tokens=5000,
            budget_utilization=0.25,
            total_items=10,
            tokens_by_type={
                ContextItemType.FOUNDATION.value: 1000,
                ContextItemType.AGENT_OUTPUT.value: 3000,
                ContextItemType.TEMPLATE.value: 1000
            }
        )
        
        self.budget_monitor = BudgetMonitor(self.mock_context_manager)
    
    def test_budget_monitor_initialization(self):
        """Test budget monitor initialization"""
        self.assertEqual(self.budget_monitor.context_manager, self.mock_context_manager)
        self.assertIsNotNone(self.budget_monitor.thresholds)
        self.assertGreater(len(self.budget_monitor.thresholds), 0)
        self.assertEqual(len(self.budget_monitor.alert_history), 0)
    
    def test_default_thresholds(self):
        """Test default threshold configuration"""
        thresholds = self.budget_monitor.thresholds
        
        # Should have thresholds for each alert level
        threshold_levels = [t.level for t in thresholds]
        self.assertIn(BudgetAlertLevel.WARNING, threshold_levels)
        self.assertIn(BudgetAlertLevel.CRITICAL, threshold_levels)
        self.assertIn(BudgetAlertLevel.EMERGENCY, threshold_levels)
        
        # Thresholds should be in ascending order
        utilizations = [t.utilization for t in sorted(thresholds, key=lambda x: x.utilization)]
        self.assertEqual(utilizations, sorted(utilizations))
    
    def test_check_budget_status_normal(self):
        """Test budget status check under normal conditions"""
        # Mock low utilization
        self.mock_context_manager.get_context_summary.return_value.budget_utilization = 0.3
        
        alert_level, alert = self.budget_monitor.check_budget_status()
        
        self.assertEqual(alert_level, BudgetAlertLevel.INFO)
        self.assertIsNone(alert)
    
    def test_check_budget_status_warning(self):
        """Test budget status check with warning threshold"""
        # Mock warning level utilization
        self.mock_context_manager.get_context_summary.return_value.budget_utilization = 0.65
        
        alert_level, alert = self.budget_monitor.check_budget_status()
        
        self.assertEqual(alert_level, BudgetAlertLevel.WARNING)
        self.assertIsNotNone(alert)
        self.assertEqual(alert.level, BudgetAlertLevel.WARNING)
        self.assertGreater(len(alert.recommended_actions), 0)
    
    def test_check_budget_status_critical(self):
        """Test budget status check with critical threshold"""
        # Mock critical level utilization
        self.mock_context_manager.get_context_summary.return_value.budget_utilization = 0.85
        
        alert_level, alert = self.budget_monitor.check_budget_status()
        
        self.assertEqual(alert_level, BudgetAlertLevel.CRITICAL)
        self.assertIsNotNone(alert)
        self.assertEqual(alert.level, BudgetAlertLevel.CRITICAL)
        self.assertIn("compress", " ".join(alert.recommended_actions).lower())
    
    def test_check_budget_status_emergency(self):
        """Test budget status check with emergency threshold"""
        # Mock emergency level utilization
        self.mock_context_manager.get_context_summary.return_value.budget_utilization = 0.96
        
        alert_level, alert = self.budget_monitor.check_budget_status()
        
        self.assertEqual(alert_level, BudgetAlertLevel.EMERGENCY)
        self.assertIsNotNone(alert)
        self.assertEqual(alert.level, BudgetAlertLevel.EMERGENCY)
        self.assertIn("block", " ".join(alert.recommended_actions).lower())
    
    def test_alert_history_tracking(self):
        """Test alert history tracking"""
        # Generate multiple alerts
        utilizations = [0.65, 0.75, 0.85, 0.95]
        
        for util in utilizations:
            self.mock_context_manager.get_context_summary.return_value.budget_utilization = util
            self.budget_monitor.check_budget_status()
        
        # Should have recorded alerts (not INFO level)
        self.assertGreater(len(self.budget_monitor.alert_history), 0)
        self.assertLessEqual(len(self.budget_monitor.alert_history), 4)
    
    def test_monitoring_statistics(self):
        """Test monitoring statistics collection"""
        # Perform several budget checks
        for i in range(5):
            self.mock_context_manager.get_context_summary.return_value.budget_utilization = 0.5 + (i * 0.1)
            self.budget_monitor.check_budget_status()
        
        stats = self.budget_monitor.get_monitoring_statistics()
        
        self.assertIn("monitoring_status", stats)
        self.assertEqual(stats["monitoring_status"], "active")
        self.assertGreaterEqual(stats["total_measurements"], 5)
        self.assertIn("average_utilization", stats)
        self.assertIn("peak_utilization", stats)

class TestBudgetOptimization(unittest.TestCase):
    """Test budget optimization recommendations"""
    
    def setUp(self):
        if not BUDGET_MONITOR_AVAILABLE:
            self.skipTest("Budget Monitor not available")
        
        self.mock_context_manager = Mock(spec=ContextManager)
        self.mock_context_manager.max_tokens = 20000
        self.budget_monitor = BudgetMonitor(self.mock_context_manager)
    
    def test_budget_optimization_recommendations(self):
        """Test budget optimization recommendations"""
        # Mock unbalanced token distribution
        self.mock_context_manager.get_context_summary.return_value = Mock(
            total_tokens=15000,
            budget_utilization=0.75,
            tokens_by_type={
                ContextItemType.FOUNDATION.value: 8000,  # Too much foundation
                ContextItemType.AGENT_OUTPUT.value: 5000,
                ContextItemType.TEMPLATE.value: 1000,
                ContextItemType.METADATA.value: 800,
                ContextItemType.DEBUG.value: 200
            }
        )
        
        optimization = self.budget_monitor.get_budget_optimization_recommendations()
        
        self.assertIsInstance(optimization, BudgetOptimization)
        self.assertIsNotNone(optimization.rationale)
        self.assertGreater(len(optimization.recommendations), 0)
    
    def test_well_balanced_budget_optimization(self):
        """Test optimization recommendations for well-balanced budget"""
        # Mock well-balanced distribution
        self.mock_context_manager.get_context_summary.return_value = Mock(
            total_tokens=10000,
            budget_utilization=0.5,
            tokens_by_type={
                ContextItemType.FOUNDATION.value: 1500,  # 15% - good
                ContextItemType.AGENT_OUTPUT.value: 5000,  # 50% - good
                ContextItemType.TEMPLATE.value: 2000,  # 20% - good
                ContextItemType.METADATA.value: 1000,  # 10% - good
                ContextItemType.DEBUG.value: 500  # 5% - good
            }
        )
        
        optimization = self.budget_monitor.get_budget_optimization_recommendations()
        
        self.assertIn("well-balanced", optimization.rationale.lower())

class TestBudgetMonitoringFeatures(unittest.TestCase):
    """Test advanced budget monitoring features"""
    
    def setUp(self):
        if not BUDGET_MONITOR_AVAILABLE:
            self.skipTest("Budget Monitor not available")
        
        self.mock_context_manager = Mock(spec=ContextManager)
        self.mock_context_manager.max_tokens = 20000
        self.budget_monitor = BudgetMonitor(self.mock_context_manager, enable_monitoring=True)
    
    def test_real_time_monitoring_start_stop(self):
        """Test real-time monitoring start and stop"""
        # Start monitoring
        self.budget_monitor.start_monitoring()
        self.assertTrue(self.budget_monitor.monitoring_active)
        
        # Give it a moment to run
        time.sleep(0.1)
        
        # Stop monitoring
        self.budget_monitor.stop_monitoring()
        self.assertFalse(self.budget_monitor.monitoring_active)
    
    def test_monitoring_interval_configuration(self):
        """Test monitoring interval configuration"""
        # Create monitor with custom interval
        monitor = BudgetMonitor(
            self.mock_context_manager,
            enable_monitoring=True,
            monitoring_interval=0.05  # 50ms
        )
        
        self.assertEqual(monitor.monitoring_interval, 0.05)
        
        # Start monitoring and verify it runs at specified interval
        monitor.start_monitoring()
        time.sleep(0.15)  # Let it run for 3 intervals
        monitor.stop_monitoring()
        
        # Should have taken multiple measurements
        stats = monitor.get_monitoring_statistics()
        self.assertGreaterEqual(stats["total_measurements"], 2)
    
    @patch('context.budget_monitor.logger')
    def test_alert_handler_integration(self, mock_logger):
        """Test alert handler integration"""
        # Add a custom alert handler
        alerts_received = []
        
        def custom_handler(alert):
            alerts_received.append(alert)
        
        self.budget_monitor.add_alert_handler(custom_handler)
        
        # Trigger an alert
        self.mock_context_manager.get_context_summary.return_value.budget_utilization = 0.85
        
        alert_level, alert = self.budget_monitor.check_budget_status()
        
        # Handler should have been called
        self.assertEqual(len(alerts_received), 1)
        self.assertEqual(alerts_received[0].level, BudgetAlertLevel.CRITICAL)
    
    def test_threshold_customization(self):
        """Test custom threshold configuration"""
        custom_thresholds = [
            BudgetThreshold(BudgetAlertLevel.WARNING, 0.5, ["monitor"]),
            BudgetThreshold(BudgetAlertLevel.CRITICAL, 0.7, ["compress"]),
            BudgetThreshold(BudgetAlertLevel.EMERGENCY, 0.9, ["block"])
        ]
        
        monitor = BudgetMonitor(self.mock_context_manager, thresholds=custom_thresholds)
        
        self.assertEqual(len(monitor.thresholds), 3)
        
        # Test custom warning threshold
        self.mock_context_manager.get_context_summary.return_value.budget_utilization = 0.55
        alert_level, alert = monitor.check_budget_status()
        
        self.assertEqual(alert_level, BudgetAlertLevel.WARNING)

class TestBudgetMonitorIntegration(unittest.TestCase):
    """Test budget monitor integration features"""
    
    def setUp(self):
        if not BUDGET_MONITOR_AVAILABLE:
            self.skipTest("Budget Monitor not available")
    
    def test_create_budget_monitor_factory(self):
        """Test budget monitor factory function"""
        mock_cm = Mock(spec=ContextManager)
        mock_cm.max_tokens = 20000
        
        monitor = create_budget_monitor(mock_cm)
        
        self.assertIsInstance(monitor, BudgetMonitor)
        self.assertEqual(monitor.context_manager, mock_cm)
    
    def test_console_alert_handler_setup(self):
        """Test console alert handler setup"""
        mock_cm = Mock(spec=ContextManager)
        monitor = BudgetMonitor(mock_cm)
        
        # Setup console handler
        setup_console_alert_handler(monitor)
        
        # Should have added a handler
        self.assertGreater(len(monitor.alert_handlers), 0)
    
    @patch('builtins.print')
    def test_console_alert_output(self, mock_print):
        """Test console alert output"""
        mock_cm = Mock(spec=ContextManager)
        mock_cm.get_context_summary.return_value.budget_utilization = 0.85
        
        monitor = BudgetMonitor(mock_cm)
        setup_console_alert_handler(monitor)
        
        # Trigger alert
        alert_level, alert = monitor.check_budget_status()
        
        # Console should have been called
        mock_print.assert_called()

class TestBudgetMonitorRobustness(unittest.TestCase):
    """Test budget monitor robustness and edge cases"""
    
    def setUp(self):
        if not BUDGET_MONITOR_AVAILABLE:
            self.skipTest("Budget Monitor not available")
        
        self.mock_context_manager = Mock(spec=ContextManager)
        self.mock_context_manager.max_tokens = 20000
        self.budget_monitor = BudgetMonitor(self.mock_context_manager)
    
    def test_context_manager_exception_handling(self):
        """Test handling of context manager exceptions"""
        # Mock context manager to raise exception
        self.mock_context_manager.get_context_summary.side_effect = Exception("Context error")
        
        # Should not crash on exception
        alert_level, alert = self.budget_monitor.check_budget_status()
        
        # Should return safe defaults
        self.assertEqual(alert_level, BudgetAlertLevel.INFO)
        self.assertIsNone(alert)
    
    def test_concurrent_monitoring(self):
        """Test concurrent monitoring access"""
        def check_status():
            self.mock_context_manager.get_context_summary.return_value.budget_utilization = 0.7
            return self.budget_monitor.check_budget_status()
        
        # Run multiple threads
        threads = []
        results = []
        
        for _ in range(5):
            thread = threading.Thread(target=lambda: results.append(check_status()))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All should complete without error
        self.assertEqual(len(results), 5)
    
    def test_memory_usage_with_long_monitoring(self):
        """Test memory usage during long monitoring sessions"""
        # Simulate long monitoring session
        for i in range(1000):
            self.mock_context_manager.get_context_summary.return_value.budget_utilization = 0.3 + (i % 10) * 0.05
            self.budget_monitor.check_budget_status()
        
        # Alert history should be limited
        self.assertLessEqual(len(self.budget_monitor.alert_history), self.budget_monitor.max_alert_history)
        
        # Measurements should be limited
        stats = self.budget_monitor.get_monitoring_statistics()
        self.assertLessEqual(stats["total_measurements"], 1000)

def run_budget_monitor_tests():
    """Run comprehensive budget monitor tests"""
    print("🔍 FACTOR 3 BUDGET MONITOR - COMPREHENSIVE UNIT TESTS")
    print("=" * 65)
    
    if not BUDGET_MONITOR_AVAILABLE:
        print("⚠️ Budget Monitor not available - skipping tests")
        return False
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestBudgetThreshold,
        TestBudgetAlert,
        TestBudgetMonitor,
        TestBudgetOptimization,
        TestBudgetMonitoringFeatures,
        TestBudgetMonitorIntegration,
        TestBudgetMonitorRobustness
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 65)
    print(f"🧪 Tests Run: {result.testsRun}")
    print(f"✅ Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"🚨 Errors: {len(result.errors)}")
    print("=" * 65)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_budget_monitor_tests()
    exit(0 if success else 1)