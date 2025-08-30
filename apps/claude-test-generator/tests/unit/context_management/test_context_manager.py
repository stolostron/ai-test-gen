#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Factor 3 Context Manager
====================================================

Tests the core context management system including token counting,
budget allocation, and Claude 4 Sonnet integration.
"""

import unittest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add source path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

try:
    from context.context_manager import (
        ContextManager, TokenCounter, ContextItem, ContextBudget,
        ContextItemType, BudgetAlertLevel, create_framework_context_manager
    )
    CONTEXT_MANAGER_AVAILABLE = True
except ImportError as e:
    CONTEXT_MANAGER_AVAILABLE = False
    print(f"⚠️ Context Manager not available: {e}")

class TestTokenCounter(unittest.TestCase):
    """Test TokenCounter functionality"""
    
    def setUp(self):
        if not CONTEXT_MANAGER_AVAILABLE:
            self.skipTest("Context Manager not available")
        self.token_counter = TokenCounter(model="claude-4-sonnet-20241022")
    
    def test_token_counting_accuracy(self):
        """Test token counting accuracy for various content types"""
        test_cases = [
            ("Hello world", 2),  # Simple text
            ("", 0),             # Empty string
            ("A" * 100, 25),     # Repetitive text (approximately 100/4)
            (json.dumps({"key": "value", "number": 123}), 7),  # JSON content
        ]
        
        for content, expected_min in test_cases:
            with self.subTest(content=content[:20]):
                tokens = self.token_counter.count_tokens(content)
                self.assertGreaterEqual(tokens, expected_min, 
                    f"Token count {tokens} should be >= {expected_min} for content: {content[:20]}")
                self.assertIsInstance(tokens, int)
    
    def test_model_support(self):
        """Test different model support"""
        models = ["claude-4-sonnet-20241022", "claude-3-sonnet", "gpt-4"]
        
        for model in models:
            with self.subTest(model=model):
                counter = TokenCounter(model=model)
                tokens = counter.count_tokens("Test content for token counting")
                self.assertGreater(tokens, 0)
                self.assertIsInstance(tokens, int)

class TestContextBudget(unittest.TestCase):
    """Test ContextBudget allocation and management"""
    
    def setUp(self):
        if not CONTEXT_MANAGER_AVAILABLE:
            self.skipTest("Context Manager not available")
        self.budget = ContextBudget(max_tokens=10000)
    
    def test_budget_allocation(self):
        """Test budget allocation percentages"""
        allocations = self.budget.get_allocation_summary()
        
        # Test allocation percentages sum to ~100%
        total_percentage = sum(allocations.values())
        self.assertAlmostEqual(total_percentage, 1.0, places=2)
        
        # Test individual allocations
        self.assertEqual(allocations[ContextItemType.FOUNDATION], 0.15)
        self.assertEqual(allocations[ContextItemType.AGENT_OUTPUT], 0.50)
        self.assertEqual(allocations[ContextItemType.TEMPLATE], 0.20)
    
    def test_budget_limits(self):
        """Test budget limit enforcement"""
        # Test foundation budget
        foundation_limit = self.budget.get_type_limit(ContextItemType.FOUNDATION)
        self.assertEqual(foundation_limit, 1500)  # 15% of 10000
        
        # Test agent output budget
        agent_limit = self.budget.get_type_limit(ContextItemType.AGENT_OUTPUT)
        self.assertEqual(agent_limit, 5000)  # 50% of 10000
    
    def test_budget_utilization(self):
        """Test budget utilization tracking"""
        # Add some usage
        self.budget.allocate_tokens(ContextItemType.FOUNDATION, 500)
        self.budget.allocate_tokens(ContextItemType.AGENT_OUTPUT, 1000)
        
        utilization = self.budget.get_utilization()
        expected_utilization = 1500 / 10000  # 15%
        self.assertAlmostEqual(utilization, expected_utilization, places=3)

class TestContextManager(unittest.TestCase):
    """Test ContextManager core functionality"""
    
    def setUp(self):
        if not CONTEXT_MANAGER_AVAILABLE:
            self.skipTest("Context Manager not available")
        self.context_manager = ContextManager(max_tokens=20000)
    
    def test_context_manager_initialization(self):
        """Test context manager initialization"""
        self.assertEqual(self.context_manager.max_tokens, 20000)
        self.assertIsNotNone(self.context_manager.token_counter)
        self.assertIsNotNone(self.context_manager.budget)
        self.assertEqual(len(self.context_manager.context_items), 0)
    
    def test_add_context_success(self):
        """Test successful context addition"""
        content = "Test context for Factor 3 implementation"
        
        result = self.context_manager.add_context(
            content=content,
            importance=0.8,
            item_type=ContextItemType.FOUNDATION,
            source="unit_test",
            metadata={"test": True}
        )
        
        self.assertTrue(result)
        self.assertEqual(len(self.context_manager.context_items), 1)
        
        # Check the added item
        item = self.context_manager.context_items[0]
        self.assertEqual(item.content, content)
        self.assertEqual(item.importance, 0.8)
        self.assertEqual(item.item_type, ContextItemType.FOUNDATION)
        self.assertEqual(item.source, "unit_test")
    
    def test_add_context_budget_overflow(self):
        """Test context addition when budget would overflow"""
        # Fill the budget almost to capacity
        large_content = "x" * 19000  # Should be close to 20000 token limit
        
        self.context_manager.add_context(
            content=large_content,
            importance=0.9,
            item_type=ContextItemType.FOUNDATION,
            source="large_test"
        )
        
        # Try to add more content that would overflow
        overflow_content = "This should be rejected due to budget overflow"
        result = self.context_manager.add_context(
            content=overflow_content,
            importance=0.7,
            item_type=ContextItemType.METADATA,
            source="overflow_test"
        )
        
        # Should be rejected
        self.assertFalse(result)
    
    def test_context_summary(self):
        """Test context summary generation"""
        # Add various types of content
        self.context_manager.add_context("Foundation data", 0.9, ContextItemType.FOUNDATION, "test1")
        self.context_manager.add_context("Agent findings", 0.8, ContextItemType.AGENT_OUTPUT, "test2")
        self.context_manager.add_context("Template data", 0.7, ContextItemType.TEMPLATE, "test3")
        
        summary = self.context_manager.get_context_summary()
        
        self.assertGreater(summary.total_tokens, 0)
        self.assertEqual(summary.total_items, 3)
        self.assertGreater(summary.budget_utilization, 0)
        self.assertLessEqual(summary.budget_utilization, 1.0)
        self.assertIsInstance(summary.tokens_by_type, dict)
    
    def test_importance_based_filtering(self):
        """Test importance-based content filtering"""
        # Add items with different importance scores
        items = [
            ("Critical data", 0.95, ContextItemType.FOUNDATION),
            ("Important data", 0.8, ContextItemType.AGENT_OUTPUT),
            ("Moderate data", 0.6, ContextItemType.METADATA),
            ("Low priority data", 0.3, ContextItemType.DEBUG)
        ]
        
        for content, importance, item_type in items:
            self.context_manager.add_context(content, importance, item_type, "test")
        
        # Test filtering by importance
        high_importance = self.context_manager.get_items_by_importance(min_importance=0.7)
        self.assertEqual(len(high_importance), 2)  # Only first two items
        
        medium_importance = self.context_manager.get_items_by_importance(min_importance=0.5)
        self.assertEqual(len(medium_importance), 3)  # First three items

class TestContextIntegration(unittest.TestCase):
    """Test context management integration features"""
    
    def setUp(self):
        if not CONTEXT_MANAGER_AVAILABLE:
            self.skipTest("Context Manager not available")
    
    def test_framework_context_manager_creation(self):
        """Test framework context manager factory function"""
        cm = create_framework_context_manager()
        
        self.assertIsInstance(cm, ContextManager)
        self.assertEqual(cm.max_tokens, 200000)  # Claude 4 Sonnet default
        self.assertIsNotNone(cm.token_counter)
        self.assertIsNotNone(cm.budget)
    
    def test_framework_context_manager_with_custom_tokens(self):
        """Test framework context manager with custom token limit"""
        cm = create_framework_context_manager(max_tokens=100000)
        
        self.assertEqual(cm.max_tokens, 100000)
    
    @patch('context.context_manager.logger')
    def test_logging_integration(self, mock_logger):
        """Test logging integration"""
        cm = ContextManager(max_tokens=10000)
        
        # Add content and verify logging
        cm.add_context("Test logging", 0.8, ContextItemType.FOUNDATION, "test")
        
        # Verify logger was called
        mock_logger.debug.assert_called()

class TestContextManagerRobustness(unittest.TestCase):
    """Test context manager robustness and edge cases"""
    
    def setUp(self):
        if not CONTEXT_MANAGER_AVAILABLE:
            self.skipTest("Context Manager not available")
        self.context_manager = ContextManager(max_tokens=1000)  # Small budget for testing
    
    def test_empty_content_handling(self):
        """Test handling of empty content"""
        result = self.context_manager.add_context("", 0.8, ContextItemType.FOUNDATION, "test")
        self.assertTrue(result)  # Should accept empty content
        
        summary = self.context_manager.get_context_summary()
        self.assertEqual(summary.total_items, 1)
    
    def test_invalid_importance_scores(self):
        """Test handling of invalid importance scores"""
        # Test values outside 0-1 range
        result1 = self.context_manager.add_context("Test", -0.5, ContextItemType.FOUNDATION, "test")
        result2 = self.context_manager.add_context("Test", 1.5, ContextItemType.FOUNDATION, "test")
        
        # Should clamp to valid range
        self.assertTrue(result1)
        self.assertTrue(result2)
        
        # Check clamped values
        items = self.context_manager.context_items
        self.assertGreaterEqual(items[0].importance, 0.0)
        self.assertLessEqual(items[0].importance, 1.0)
        self.assertGreaterEqual(items[1].importance, 0.0)
        self.assertLessEqual(items[1].importance, 1.0)
    
    def test_large_content_handling(self):
        """Test handling of very large content"""
        large_content = "x" * 10000  # Very large content
        
        result = self.context_manager.add_context(
            large_content, 0.8, ContextItemType.FOUNDATION, "large_test"
        )
        
        # Should be rejected due to budget constraints
        self.assertFalse(result)
    
    def test_concurrent_access_simulation(self):
        """Test simulation of concurrent access"""
        import threading
        
        results = []
        
        def add_content(i):
            result = self.context_manager.add_context(
                f"Content {i}", 0.5, ContextItemType.METADATA, f"thread_{i}"
            )
            results.append(result)
        
        # Simulate concurrent additions
        threads = []
        for i in range(10):
            thread = threading.Thread(target=add_content, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Some should succeed, some might fail due to budget
        self.assertTrue(any(results))

def run_context_manager_tests():
    """Run comprehensive context manager tests"""
    print("🧪 FACTOR 3 CONTEXT MANAGER - COMPREHENSIVE UNIT TESTS")
    print("=" * 65)
    
    if not CONTEXT_MANAGER_AVAILABLE:
        print("⚠️ Context Manager not available - skipping tests")
        return False
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestTokenCounter,
        TestContextBudget,
        TestContextManager,
        TestContextIntegration,
        TestContextManagerRobustness
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
    success = run_context_manager_tests()
    exit(0 if success else 1)