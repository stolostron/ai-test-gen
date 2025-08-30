#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Factor 3 Context Compressor
=======================================================

Tests the advanced compression engine including importance-based compression,
semantic summarization, and compression strategies.
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
    from context.context_compressor import (
        AdvancedContextCompressor, CompressionStrategy, CompressionResult,
        CompressionProfile, create_compressor_for_framework
    )
    from context.context_manager import ContextItem, ContextItemType
    CONTEXT_COMPRESSOR_AVAILABLE = True
except ImportError as e:
    CONTEXT_COMPRESSOR_AVAILABLE = False
    print(f"⚠️ Context Compressor not available: {e}")

class TestCompressionProfile(unittest.TestCase):
    """Test CompressionProfile functionality"""
    
    def setUp(self):
        if not CONTEXT_COMPRESSOR_AVAILABLE:
            self.skipTest("Context Compressor not available")
    
    def test_compression_profile_creation(self):
        """Test compression profile creation and properties"""
        profile = CompressionProfile(
            item_type=ContextItemType.AGENT_OUTPUT,
            target_ratio=0.6,
            strategy=CompressionStrategy.IMPORTANCE_BASED,
            preserve_structure=True
        )
        
        self.assertEqual(profile.item_type, ContextItemType.AGENT_OUTPUT)
        self.assertEqual(profile.target_ratio, 0.6)
        self.assertEqual(profile.strategy, CompressionStrategy.IMPORTANCE_BASED)
        self.assertTrue(profile.preserve_structure)
    
    def test_compression_profile_validation(self):
        """Test compression profile validation"""
        # Test invalid ratio
        with self.assertRaises(ValueError):
            CompressionProfile(
                item_type=ContextItemType.FOUNDATION,
                target_ratio=1.5,  # Invalid ratio > 1.0
                strategy=CompressionStrategy.TEMPORAL
            )
        
        with self.assertRaises(ValueError):
            CompressionProfile(
                item_type=ContextItemType.FOUNDATION,
                target_ratio=-0.1,  # Invalid ratio < 0.0
                strategy=CompressionStrategy.TEMPORAL
            )

class TestAdvancedContextCompressor(unittest.TestCase):
    """Test AdvancedContextCompressor functionality"""
    
    def setUp(self):
        if not CONTEXT_COMPRESSOR_AVAILABLE:
            self.skipTest("Context Compressor not available")
        self.compressor = AdvancedContextCompressor()
    
    def test_compressor_initialization(self):
        """Test compressor initialization"""
        self.assertIsNotNone(self.compressor.compression_profiles)
        self.assertIsInstance(self.compressor.compression_profiles, dict)
        
        # Check default profiles exist for all item types
        for item_type in ContextItemType:
            self.assertIn(item_type, self.compressor.compression_profiles)
    
    def test_importance_based_compression(self):
        """Test importance-based compression strategy"""
        # Create test context item
        content = "This is a test content for importance-based compression. " * 10
        item = ContextItem(
            content=content,
            importance=0.7,
            item_type=ContextItemType.AGENT_OUTPUT,
            source="test_agent",
            timestamp=1234567890.0,
            token_count=len(content.split())
        )
        
        result = self.compressor.compress_context_item(
            item, 
            target_ratio=0.6,
            strategy=CompressionStrategy.IMPORTANCE_BASED
        )
        
        self.assertIsInstance(result, CompressionResult)
        self.assertLess(len(result.compressed_content), len(content))
        self.assertGreater(result.compression_ratio, 0)
        self.assertLessEqual(result.compression_ratio, 1.0)
        self.assertEqual(result.strategy_used, CompressionStrategy.IMPORTANCE_BASED)
    
    def test_summarization_compression(self):
        """Test summarization compression strategy"""
        content = """
        This is a detailed analysis of the JIRA ticket ACM-12345 which involves
        implementing a new feature for cluster management. The ticket describes
        requirements for automated cluster upgrades, user interface improvements,
        and comprehensive testing strategies. The implementation requires careful
        consideration of backward compatibility and performance implications.
        """
        
        item = ContextItem(
            content=content,
            importance=0.8,
            item_type=ContextItemType.AGENT_OUTPUT,
            source="agent_a",
            timestamp=1234567890.0,
            token_count=len(content.split())
        )
        
        result = self.compressor.compress_context_item(
            item,
            target_ratio=0.5,
            strategy=CompressionStrategy.SUMMARIZATION
        )
        
        self.assertLess(len(result.compressed_content), len(content))
        self.assertIn("ACM-12345", result.compressed_content)  # Key info preserved
        self.assertEqual(result.strategy_used, CompressionStrategy.SUMMARIZATION)
    
    def test_temporal_compression(self):
        """Test temporal compression strategy"""
        # Create content with timestamps
        content = """
        2024-01-01: Initial analysis started
        2024-01-02: Requirements gathered
        2024-01-03: Implementation planning
        2024-01-04: Development phase
        2024-01-05: Testing phase
        2024-01-06: Final validation
        """
        
        item = ContextItem(
            content=content,
            importance=0.6,
            item_type=ContextItemType.METADATA,
            source="timeline_agent",
            timestamp=1234567890.0,
            token_count=len(content.split())
        )
        
        result = self.compressor.compress_context_item(
            item,
            target_ratio=0.4,
            strategy=CompressionStrategy.TEMPORAL
        )
        
        self.assertLess(len(result.compressed_content), len(content))
        # Should preserve most recent entries
        self.assertIn("2024-01-06", result.compressed_content)
        self.assertEqual(result.strategy_used, CompressionStrategy.TEMPORAL)
    
    def test_hybrid_compression(self):
        """Test hybrid compression strategy"""
        content = "A" * 1000  # Large repetitive content
        
        item = ContextItem(
            content=content,
            importance=0.5,
            item_type=ContextItemType.DEBUG,
            source="debug_agent",
            timestamp=1234567890.0,
            token_count=250  # Approximate token count
        )
        
        result = self.compressor.compress_context_item(
            item,
            target_ratio=0.3,
            strategy=CompressionStrategy.HYBRID
        )
        
        self.assertLess(len(result.compressed_content), len(content))
        self.assertEqual(result.strategy_used, CompressionStrategy.HYBRID)
    
    def test_compression_with_structure_preservation(self):
        """Test compression with structure preservation"""
        json_content = json.dumps({
            "analysis": {
                "requirements": ["req1", "req2", "req3"],
                "priorities": {"high": ["item1"], "medium": ["item2", "item3"]},
                "dependencies": ["dep1", "dep2", "dep3", "dep4"]
            },
            "metadata": {
                "timestamp": "2024-01-01",
                "agent": "test_agent",
                "confidence": 0.95
            }
        }, indent=2)
        
        item = ContextItem(
            content=json_content,
            importance=0.9,
            item_type=ContextItemType.AGENT_OUTPUT,
            source="structured_agent",
            timestamp=1234567890.0,
            token_count=len(json_content.split())
        )
        
        result = self.compressor.compress_context_item(
            item,
            target_ratio=0.7
        )
        
        # Should still be valid JSON after compression
        try:
            compressed_data = json.loads(result.compressed_content)
            self.assertIsInstance(compressed_data, dict)
            # Key structure should be preserved
            self.assertIn("analysis", compressed_data)
            self.assertIn("metadata", compressed_data)
        except json.JSONDecodeError:
            self.fail("Compressed content should remain valid JSON")
    
    def test_compression_quality_metrics(self):
        """Test compression quality metrics"""
        content = "Important analysis data that should be preserved during compression. " * 20
        
        item = ContextItem(
            content=content,
            importance=0.8,
            item_type=ContextItemType.FOUNDATION,
            source="quality_test",
            timestamp=1234567890.0,
            token_count=len(content.split())
        )
        
        result = self.compressor.compress_context_item(item, target_ratio=0.5)
        
        # Check quality metrics
        self.assertIsNotNone(result.quality_score)
        self.assertGreaterEqual(result.quality_score, 0.0)
        self.assertLessEqual(result.quality_score, 1.0)
        
        self.assertIsNotNone(result.information_loss)
        self.assertGreaterEqual(result.information_loss, 0.0)
        self.assertLessEqual(result.information_loss, 1.0)

class TestCompressionStrategies(unittest.TestCase):
    """Test individual compression strategies"""
    
    def setUp(self):
        if not CONTEXT_COMPRESSOR_AVAILABLE:
            self.skipTest("Context Compressor not available")
        self.compressor = AdvancedContextCompressor()
    
    def test_strategy_selection(self):
        """Test automatic strategy selection based on content type"""
        # Foundation content should use importance-based
        foundation_item = ContextItem(
            content="Foundation analysis data",
            importance=0.9,
            item_type=ContextItemType.FOUNDATION,
            source="foundation",
            timestamp=1234567890.0,
            token_count=10
        )
        
        profile = self.compressor.compression_profiles[ContextItemType.FOUNDATION]
        self.assertEqual(profile.strategy, CompressionStrategy.IMPORTANCE_BASED)
        
        # Debug content should use temporal
        debug_item = ContextItem(
            content="Debug log entries with timestamps",
            importance=0.3,
            item_type=ContextItemType.DEBUG,
            source="debug",
            timestamp=1234567890.0,
            token_count=10
        )
        
        debug_profile = self.compressor.compression_profiles[ContextItemType.DEBUG]
        self.assertEqual(debug_profile.strategy, CompressionStrategy.TEMPORAL)
    
    def test_compression_ratio_limits(self):
        """Test compression ratio limits"""
        content = "Test content for ratio limits"
        
        item = ContextItem(
            content=content,
            importance=0.7,
            item_type=ContextItemType.METADATA,
            source="ratio_test",
            timestamp=1234567890.0,
            token_count=len(content.split())
        )
        
        # Test minimum ratio
        result_min = self.compressor.compress_context_item(item, target_ratio=0.1)
        self.assertGreaterEqual(result_min.compression_ratio, 0.1)
        
        # Test maximum ratio (no compression)
        result_max = self.compressor.compress_context_item(item, target_ratio=1.0)
        self.assertEqual(result_max.compressed_content, content)
        self.assertEqual(result_max.compression_ratio, 1.0)

class TestCompressionIntegration(unittest.TestCase):
    """Test compression integration features"""
    
    def setUp(self):
        if not CONTEXT_COMPRESSOR_AVAILABLE:
            self.skipTest("Context Compressor not available")
    
    def test_framework_compressor_creation(self):
        """Test framework compressor factory function"""
        compressor = create_compressor_for_framework()
        
        self.assertIsInstance(compressor, AdvancedContextCompressor)
        self.assertIsNotNone(compressor.compression_profiles)
    
    def test_batch_compression(self):
        """Test batch compression of multiple items"""
        compressor = AdvancedContextCompressor()
        
        # Create multiple items
        items = []
        for i in range(5):
            item = ContextItem(
                content=f"Test content {i} with detailed information about topic {i}",
                importance=0.5 + (i * 0.1),
                item_type=ContextItemType.AGENT_OUTPUT,
                source=f"agent_{i}",
                timestamp=1234567890.0 + i,
                token_count=10
            )
            items.append(item)
        
        # Compress all items
        results = []
        for item in items:
            result = compressor.compress_context_item(item, target_ratio=0.6)
            results.append(result)
        
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertIsInstance(result, CompressionResult)
            self.assertLess(len(result.compressed_content), len(item.content))

class TestCompressionRobustness(unittest.TestCase):
    """Test compression robustness and edge cases"""
    
    def setUp(self):
        if not CONTEXT_COMPRESSOR_AVAILABLE:
            self.skipTest("Context Compressor not available")
        self.compressor = AdvancedContextCompressor()
    
    def test_empty_content_compression(self):
        """Test compression of empty content"""
        item = ContextItem(
            content="",
            importance=0.5,
            item_type=ContextItemType.METADATA,
            source="empty_test",
            timestamp=1234567890.0,
            token_count=0
        )
        
        result = self.compressor.compress_context_item(item)
        self.assertEqual(result.compressed_content, "")
        self.assertEqual(result.compression_ratio, 1.0)
    
    def test_very_short_content_compression(self):
        """Test compression of very short content"""
        item = ContextItem(
            content="Hi",
            importance=0.8,
            item_type=ContextItemType.FOUNDATION,
            source="short_test",
            timestamp=1234567890.0,
            token_count=1
        )
        
        result = self.compressor.compress_context_item(item, target_ratio=0.5)
        # Very short content should not be compressed much
        self.assertGreaterEqual(len(result.compressed_content), 1)
    
    def test_malformed_json_compression(self):
        """Test compression of malformed JSON content"""
        malformed_json = '{"key": "value", "incomplete": '
        
        item = ContextItem(
            content=malformed_json,
            importance=0.6,
            item_type=ContextItemType.AGENT_OUTPUT,
            source="malformed_test",
            timestamp=1234567890.0,
            token_count=5
        )
        
        # Should not crash on malformed JSON
        result = self.compressor.compress_context_item(item)
        self.assertIsInstance(result, CompressionResult)
        self.assertIsNotNone(result.compressed_content)
    
    def test_compression_performance(self):
        """Test compression performance with large content"""
        import time
        
        # Create large content
        large_content = "Performance test content. " * 1000
        
        item = ContextItem(
            content=large_content,
            importance=0.7,
            item_type=ContextItemType.AGENT_OUTPUT,
            source="performance_test",
            timestamp=1234567890.0,
            token_count=2000
        )
        
        # Measure compression time
        start_time = time.time()
        result = self.compressor.compress_context_item(item, target_ratio=0.5)
        compression_time = time.time() - start_time
        
        # Should complete within reasonable time (< 1 second for test)
        self.assertLess(compression_time, 1.0)
        self.assertLess(len(result.compressed_content), len(large_content))

def run_context_compressor_tests():
    """Run comprehensive context compressor tests"""
    print("🗜️ FACTOR 3 CONTEXT COMPRESSOR - COMPREHENSIVE UNIT TESTS")
    print("=" * 65)
    
    if not CONTEXT_COMPRESSOR_AVAILABLE:
        print("⚠️ Context Compressor not available - skipping tests")
        return False
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestCompressionProfile,
        TestAdvancedContextCompressor,
        TestCompressionStrategies,
        TestCompressionIntegration,
        TestCompressionRobustness
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
    success = run_context_compressor_tests()
    exit(0 if success else 1)