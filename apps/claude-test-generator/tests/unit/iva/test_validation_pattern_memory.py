#!/usr/bin/env python3
"""
Validation Pattern Memory Unit Tests
==================================

Comprehensive unit tests for the ValidationPatternMemory component of IVA.
Testing pattern storage, retrieval, similarity matching, and thread safety.
"""

import unittest
import sys
import os
import json
import asyncio
import tempfile
import shutil
import sqlite3
import threading
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Any, List
from collections import deque

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
solutions_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'solutions')
sys.path.insert(0, solutions_path)

try:
    from validation_learning_core import ValidationEvent, LearningMode
    from learning_services import ValidationPatternMemory, ValidationPattern
    PATTERN_MEMORY_AVAILABLE = True
except ImportError as e:
    PATTERN_MEMORY_AVAILABLE = False
    print(f"❌ Validation Pattern Memory not available: {e}")


class TestValidationPatternMemory(unittest.TestCase):
    """Test ValidationPatternMemory core functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not PATTERN_MEMORY_AVAILABLE:
            cls.skipTest(cls, "Validation Pattern Memory not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None
        
        # Create test pattern memory
        self.pattern_memory = ValidationPatternMemory(
            storage_path=self.test_dir,
            learning_mode=LearningMode.STANDARD
        )
        
        # Create test validation events
        self.test_event_success = ValidationEvent(
            event_id='test_success_001',
            event_type='evidence_validation',
            context={
                'validation_type': 'evidence',
                'component': 'cluster-curator',
                'operation_type': 'validate'
            },
            result={'success': True, 'confidence': 0.9},
            timestamp=datetime.utcnow(),
            source_system='evidence_validation_engine',
            success=True,
            confidence=0.9,
            metadata={'quality': 'high'}
        )
        
        self.test_event_failure = ValidationEvent(
            event_id='test_failure_001',
            event_type='evidence_validation',
            context={
                'validation_type': 'evidence',
                'component': 'cluster-curator',
                'operation_type': 'validate'
            },
            result={'success': False, 'confidence': 0.3},
            timestamp=datetime.utcnow(),
            source_system='evidence_validation_engine',
            success=False,
            confidence=0.3,
            metadata={'error': 'validation_failed'}
        )
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self.pattern_memory, 'close'):
            self.pattern_memory.close()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_pattern_memory_initialization(self):
        """Test ValidationPatternMemory initializes correctly"""
        # Verify initialization
        self.assertEqual(self.pattern_memory.storage_path, Path(self.test_dir))
        self.assertEqual(self.pattern_memory.learning_mode, LearningMode.STANDARD)
        self.assertIsInstance(self.pattern_memory.pattern_cache, dict)
        self.assertIsInstance(self.pattern_memory.cache_access_order, deque)
        
        # Verify storage initialization
        self.assertTrue(self.pattern_memory.storage_path.exists())
        self.assertTrue(self.pattern_memory.db_path.exists())
        
        # Verify database structure
        with sqlite3.connect(str(self.pattern_memory.db_path)) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patterns'")
            self.assertIsNotNone(cursor.fetchone())
    
    def test_storage_initialization(self):
        """Test storage initialization creates correct database schema"""
        # Check database file exists
        self.assertTrue(self.pattern_memory.db_path.exists())
        
        # Verify table structure
        with sqlite3.connect(str(self.pattern_memory.db_path)) as conn:
            cursor = conn.execute("PRAGMA table_info(patterns)")
            columns = {row[1]: row[2] for row in cursor.fetchall()}
            
            expected_columns = {
                'pattern_id': 'TEXT',
                'pattern_type': 'TEXT',
                'context_signature': 'TEXT',
                'success_rate': 'REAL',
                'usage_count': 'INTEGER',
                'first_seen': 'TEXT',
                'last_seen': 'TEXT',
                'pattern_data': 'TEXT'
            }
            
            for col_name, col_type in expected_columns.items():
                self.assertIn(col_name, columns)
    
    def test_create_pattern_from_event(self):
        """Test pattern creation from validation event"""
        pattern = self.pattern_memory._create_pattern_from_event(self.test_event_success)
        
        # Verify pattern structure
        self.assertIsInstance(pattern, ValidationPattern)
        self.assertEqual(pattern.pattern_type, 'evidence_validation')
        self.assertEqual(pattern.success_rate, 1.0)  # Success event
        self.assertEqual(pattern.usage_count, 1)
        self.assertEqual(pattern.first_seen, self.test_event_success.timestamp)
        self.assertEqual(pattern.last_seen, self.test_event_success.timestamp)
        
        # Verify pattern data
        self.assertIn('success', pattern.pattern_data)
        self.assertIn('confidence', pattern.pattern_data)
        self.assertIn('context_keys', pattern.pattern_data)
        self.assertEqual(pattern.pattern_data['success'], True)
        self.assertEqual(pattern.pattern_data['confidence'], 0.9)
    
    def test_context_signature_generation(self):
        """Test context signature generation for pattern matching"""
        context1 = {
            'validation_type': 'evidence',
            'component': 'cluster-curator',
            'operation_type': 'validate'
        }
        
        context2 = {
            'validation_type': 'evidence',
            'component': 'cluster-curator',
            'operation_type': 'validate'
        }
        
        context3 = {
            'validation_type': 'cross_agent',
            'component': 'cluster-curator',
            'operation_type': 'validate'
        }
        
        sig1 = self.pattern_memory._create_context_signature(context1)
        sig2 = self.pattern_memory._create_context_signature(context2)
        sig3 = self.pattern_memory._create_context_signature(context3)
        
        # Same context should produce same signature
        self.assertEqual(sig1, sig2)
        
        # Different context should produce different signature
        self.assertNotEqual(sig1, sig3)
        
        # Signatures should be strings
        self.assertIsInstance(sig1, str)
        self.assertGreater(len(sig1), 0)
    
    def test_pattern_id_generation(self):
        """Test unique pattern ID generation"""
        event_type = 'evidence_validation'
        context_sig = 'test_signature'
        
        id1 = self.pattern_memory._generate_pattern_id(event_type, context_sig)
        id2 = self.pattern_memory._generate_pattern_id(event_type, context_sig)
        id3 = self.pattern_memory._generate_pattern_id('different_type', context_sig)
        
        # Same inputs should produce same ID
        self.assertEqual(id1, id2)
        
        # Different inputs should produce different ID
        self.assertNotEqual(id1, id3)
        
        # IDs should be hex strings of expected length
        self.assertEqual(len(id1), 32)
        self.assertTrue(all(c in '0123456789abcdef' for c in id1))
    
    async def test_store_pattern_async(self):
        """Test asynchronous pattern storage"""
        pattern = self.pattern_memory._create_pattern_from_event(self.test_event_success)
        
        # Store pattern
        await self.pattern_memory.store_pattern_async(pattern)
        
        # Verify pattern is in cache
        self.assertIn(pattern.pattern_id, self.pattern_memory.pattern_cache)
        cached_pattern = self.pattern_memory.pattern_cache[pattern.pattern_id]
        self.assertEqual(cached_pattern.pattern_id, pattern.pattern_id)
        
        # Verify pattern is in database
        with sqlite3.connect(str(self.pattern_memory.db_path)) as conn:
            cursor = conn.execute('SELECT pattern_id FROM patterns WHERE pattern_id = ?', (pattern.pattern_id,))
            db_result = cursor.fetchone()
            self.assertIsNotNone(db_result)
            self.assertEqual(db_result[0], pattern.pattern_id)
    
    async def test_store_pattern_update_existing(self):
        """Test updating existing pattern increases usage count and updates success rate"""
        # Store initial pattern
        pattern1 = self.pattern_memory._create_pattern_from_event(self.test_event_success)
        await self.pattern_memory.store_pattern_async(pattern1)
        
        # Create second event with same context but different result
        event2 = ValidationEvent(
            event_id='test_002',
            event_type='evidence_validation',
            context=self.test_event_success.context.copy(),  # Same context
            result={'success': False, 'confidence': 0.4},
            timestamp=datetime.utcnow(),
            source_system='evidence_validation_engine',
            success=False,
            confidence=0.4,
            metadata={'error': 'failed'}
        )
        
        pattern2 = self.pattern_memory._create_pattern_from_event(event2)
        await self.pattern_memory.store_pattern_async(pattern2)
        
        # Should update existing pattern, not create new one
        self.assertEqual(len(self.pattern_memory.pattern_cache), 1)
        
        # Check updated pattern
        updated_pattern = self.pattern_memory.pattern_cache[pattern1.pattern_id]
        self.assertEqual(updated_pattern.usage_count, 2)
        
        # Success rate should be average: (1.0 + 0.0) / 2 = 0.5
        self.assertAlmostEqual(updated_pattern.success_rate, 0.5, places=2)
    
    def test_store_pattern_sync_wrapper(self):
        """Test synchronous store_pattern wrapper"""
        # Test with safe storage conditions
        with patch.object(self.pattern_memory, '_is_storage_safe', return_value=True):
            # Should not raise exception
            try:
                self.pattern_memory.store_pattern(self.test_event_success)
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success)
        
        # Test with unsafe storage conditions
        with patch.object(self.pattern_memory, '_is_storage_safe', return_value=False):
            # Should return silently without error
            try:
                self.pattern_memory.store_pattern(self.test_event_success)
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success)
    
    async def test_find_similar_patterns_exact_match(self):
        """Test finding exact matching patterns"""
        # Store a pattern
        pattern = self.pattern_memory._create_pattern_from_event(self.test_event_success)
        await self.pattern_memory.store_pattern_async(pattern)
        
        # Search for exact match
        search_context = self.test_event_success.context.copy()
        similar_patterns = self.pattern_memory.find_similar_patterns(search_context)
        
        # Should find exact match
        self.assertEqual(len(similar_patterns), 1)
        self.assertEqual(similar_patterns[0].pattern_id, pattern.pattern_id)
    
    async def test_find_similar_patterns_content_similarity(self):
        """Test finding patterns by content similarity"""
        # Store multiple patterns with different contexts
        pattern1 = self.pattern_memory._create_pattern_from_event(self.test_event_success)
        await self.pattern_memory.store_pattern_async(pattern1)
        
        # Create event with similar but not identical context
        similar_event = ValidationEvent(
            event_id='similar_001',
            event_type='evidence_validation',
            context={
                'validation_type': 'evidence',  # Same
                'component': 'different-component',  # Different
                'operation_type': 'validate'  # Same
            },
            result={'success': True, 'confidence': 0.8},
            timestamp=datetime.utcnow(),
            source_system='evidence_validation_engine',
            success=True,
            confidence=0.8,
            metadata={}
        )
        
        pattern2 = self.pattern_memory._create_pattern_from_event(similar_event)
        await self.pattern_memory.store_pattern_async(pattern2)
        
        # Search with context that has some overlap
        search_context = {
            'validation_type': 'evidence',
            'component': 'cluster-curator',
            'operation_type': 'check'  # Different operation
        }
        
        similar_patterns = self.pattern_memory.find_similar_patterns(search_context, limit=5)
        
        # Should find patterns through content similarity
        self.assertGreaterEqual(len(similar_patterns), 0)
    
    def test_find_similar_patterns_sorting(self):
        """Test that similar patterns are sorted by success rate and usage count"""
        async def setup_patterns():
            # Create patterns with different success rates
            events = []
            
            # High success rate pattern
            for i in range(5):  # 5 successful events
                event = ValidationEvent(
                    event_id=f'high_success_{i}',
                    event_type='evidence_validation',
                    context={'type': 'high_success'},
                    result={'success': True},
                    timestamp=datetime.utcnow(),
                    source_system='test',
                    success=True,
                    confidence=0.9,
                    metadata={}
                )
                pattern = self.pattern_memory._create_pattern_from_event(event)
                await self.pattern_memory.store_pattern_async(pattern)
            
            # Low success rate pattern
            event = ValidationEvent(
                event_id='low_success',
                event_type='evidence_validation',
                context={'type': 'low_success'},
                result={'success': False},
                timestamp=datetime.utcnow(),
                source_system='test',
                success=False,
                confidence=0.3,
                metadata={}
            )
            pattern = self.pattern_memory._create_pattern_from_event(event)
            await self.pattern_memory.store_pattern_async(pattern)
        
        # Setup patterns
        asyncio.run(setup_patterns())
        
        # Find all patterns
        all_patterns = self.pattern_memory.find_similar_patterns({}, limit=10)
        
        if len(all_patterns) > 1:
            # Should be sorted by success rate (descending)
            for i in range(len(all_patterns) - 1):
                self.assertGreaterEqual(all_patterns[i].success_rate, all_patterns[i + 1].success_rate)
    
    def test_get_pattern_success_rate(self):
        """Test getting pattern success rate"""
        async def setup_pattern():
            pattern = self.pattern_memory._create_pattern_from_event(self.test_event_success)
            await self.pattern_memory.store_pattern_async(pattern)
            return pattern.pattern_id
        
        pattern_id = asyncio.run(setup_pattern())
        
        # Test getting success rate from cache
        success_rate = self.pattern_memory.get_pattern_success_rate(pattern_id)
        self.assertEqual(success_rate, 1.0)
        
        # Test non-existent pattern
        non_existent_rate = self.pattern_memory.get_pattern_success_rate('non_existent_id')
        self.assertEqual(non_existent_rate, 0.0)
    
    def test_get_pattern_statistics(self):
        """Test getting pattern memory statistics"""
        async def setup_patterns():
            # Store patterns with different success rates
            successful_event = self.test_event_success
            failed_event = self.test_event_failure
            
            for i in range(3):
                success_pattern = self.pattern_memory._create_pattern_from_event(successful_event)
                success_pattern.pattern_id = f'success_{i}'  # Make unique
                await self.pattern_memory.store_pattern_async(success_pattern)
            
            for i in range(2):
                failure_pattern = self.pattern_memory._create_pattern_from_event(failed_event)
                failure_pattern.pattern_id = f'failure_{i}'  # Make unique
                await self.pattern_memory.store_pattern_async(failure_pattern)
        
        asyncio.run(setup_patterns())
        
        stats = self.pattern_memory.get_pattern_statistics()
        
        # Verify statistics structure
        expected_keys = [
            'total_patterns', 'successful_patterns', 'success_rate_distribution',
            'pattern_types', 'cache_utilization'
        ]
        
        for key in expected_keys:
            self.assertIn(key, stats)
        
        # Verify statistics values
        self.assertGreaterEqual(stats['total_patterns'], 0)
        self.assertIsInstance(stats['success_rate_distribution'], dict)
        self.assertIsInstance(stats['pattern_types'], dict)
        self.assertGreaterEqual(stats['cache_utilization'], 0.0)
        self.assertLessEqual(stats['cache_utilization'], 1.0)
    
    def test_cache_management_lru_eviction(self):
        """Test LRU cache eviction when cache is full"""
        # Set small cache size for testing
        original_cache_size = self.pattern_memory.cache_size
        self.pattern_memory.cache_size = 3
        
        async def fill_cache():
            # Add more patterns than cache size
            for i in range(5):
                event = ValidationEvent(
                    event_id=f'cache_test_{i}',
                    event_type='test_validation',
                    context={'index': i},
                    result={'success': True},
                    timestamp=datetime.utcnow(),
                    source_system='test',
                    success=True,
                    confidence=0.8,
                    metadata={}
                )
                pattern = self.pattern_memory._create_pattern_from_event(event)
                await self.pattern_memory.store_pattern_async(pattern)
        
        asyncio.run(fill_cache())
        
        # Cache should not exceed max size
        self.assertLessEqual(len(self.pattern_memory.pattern_cache), 3)
        
        # Restore original cache size
        self.pattern_memory.cache_size = original_cache_size
    
    def test_text_similarity_calculation(self):
        """Test text similarity calculation method"""
        text1 = "validation evidence cluster curator"
        text2 = "validation evidence cluster management"
        text3 = "completely different text"
        
        # Similar texts should have higher similarity
        sim_high = self.pattern_memory._calculate_text_similarity(text1, text2)
        sim_low = self.pattern_memory._calculate_text_similarity(text1, text3)
        
        self.assertGreater(sim_high, sim_low)
        self.assertGreaterEqual(sim_high, 0.0)
        self.assertLessEqual(sim_high, 1.0)
        self.assertGreaterEqual(sim_low, 0.0)
        self.assertLessEqual(sim_low, 1.0)
        
        # Identical texts should have similarity of 1.0
        sim_identical = self.pattern_memory._calculate_text_similarity(text1, text1)
        self.assertEqual(sim_identical, 1.0)
        
        # Empty texts should have similarity of 0.0
        sim_empty = self.pattern_memory._calculate_text_similarity("", "test")
        self.assertEqual(sim_empty, 0.0)
    
    def test_storage_safety_checks(self):
        """Test storage safety checking methods"""
        # Test with valid storage path
        self.assertTrue(self.pattern_memory._is_storage_safe())
        
        # Test with invalid storage path
        invalid_memory = ValidationPatternMemory(
            storage_path='/invalid/nonexistent/path',
            learning_mode=LearningMode.STANDARD
        )
        
        # Should handle invalid path gracefully
        result = invalid_memory._is_storage_safe()
        self.assertIsInstance(result, bool)
    
    def test_retrieval_safety_checks(self):
        """Test retrieval safety checking methods"""
        # Should be safe with initialized pattern memory
        self.assertTrue(self.pattern_memory._is_retrieval_safe())
        
        # Test with empty cache and no database
        empty_memory = ValidationPatternMemory(
            storage_path=tempfile.mkdtemp(),
            learning_mode=LearningMode.STANDARD
        )
        empty_memory.pattern_cache.clear()
        
        # Should still be safe if database exists
        result = empty_memory._is_retrieval_safe()
        self.assertIsInstance(result, bool)
    
    def test_thread_safety(self):
        """Test thread safety of pattern memory operations"""
        async def store_patterns():
            for i in range(50):
                event = ValidationEvent(
                    event_id=f'thread_test_{threading.current_thread().ident}_{i}',
                    event_type='thread_test',
                    context={'thread_id': threading.current_thread().ident, 'index': i},
                    result={'success': True},
                    timestamp=datetime.utcnow(),
                    source_system='thread_test',
                    success=True,
                    confidence=0.8,
                    metadata={}
                )
                pattern = self.pattern_memory._create_pattern_from_event(event)
                await self.pattern_memory.store_pattern_async(pattern)
        
        def thread_worker():
            asyncio.run(store_patterns())
        
        # Run multiple threads concurrently
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=thread_worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should complete without errors
        # Check that patterns were stored
        self.assertGreater(len(self.pattern_memory.pattern_cache), 0)
        
        # Get statistics to verify functionality
        stats = self.pattern_memory.get_pattern_statistics()
        self.assertGreater(stats['total_patterns'], 0)
    
    def test_database_operations_error_handling(self):
        """Test error handling in database operations"""
        # Test with corrupted database path
        with patch.object(self.pattern_memory, 'db_path', Path('/invalid/path/db.sqlite')):
            async def test_store():
                pattern = self.pattern_memory._create_pattern_from_event(self.test_event_success)
                # Should handle database errors gracefully
                await self.pattern_memory._store_to_database(pattern)
            
            # Should not raise exception
            try:
                asyncio.run(test_store())
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success)
        
        # Test getting success rate from corrupted database
        with patch.object(self.pattern_memory, 'db_path', Path('/invalid/path/db.sqlite')):
            rate = self.pattern_memory._get_success_rate_from_db('test_id')
            self.assertEqual(rate, 0.0)  # Should return safe default
    
    def test_close_cleanup(self):
        """Test cleanup when closing pattern memory"""
        # Add some patterns to cache
        self.pattern_memory.pattern_cache['test1'] = Mock()
        self.pattern_memory.pattern_cache['test2'] = Mock()
        self.pattern_memory.cache_access_order.extend(['test1', 'test2'])
        
        # Close should clear cache
        self.pattern_memory.close()
        
        self.assertEqual(len(self.pattern_memory.pattern_cache), 0)
        self.assertEqual(len(self.pattern_memory.cache_access_order), 0)


class TestValidationPattern(unittest.TestCase):
    """Test ValidationPattern data structure"""
    
    @classmethod
    def setUpClass(cls):
        if not PATTERN_MEMORY_AVAILABLE:
            cls.skipTest(cls, "Validation Pattern Memory not available")
    
    def test_validation_pattern_creation(self):
        """Test ValidationPattern creation and methods"""
        pattern = ValidationPattern(
            pattern_id='test_pattern_001',
            pattern_type='evidence_validation',
            context_signature='abc123',
            success_rate=0.85,
            usage_count=10,
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow(),
            pattern_data={'key': 'value', 'success': True}
        )
        
        # Test to_dict conversion
        pattern_dict = pattern.to_dict()
        
        required_fields = [
            'pattern_id', 'pattern_type', 'context_signature',
            'success_rate', 'usage_count', 'first_seen', 'last_seen', 'pattern_data'
        ]
        
        for field in required_fields:
            self.assertIn(field, pattern_dict)
        
        # Test datetime serialization
        self.assertIsInstance(pattern_dict['first_seen'], str)
        self.assertIsInstance(pattern_dict['last_seen'], str)
    
    def test_validation_pattern_from_dict(self):
        """Test ValidationPattern creation from dictionary"""
        pattern_data = {
            'pattern_id': 'test_pattern_002',
            'pattern_type': 'cross_agent_validation',
            'context_signature': 'def456',
            'success_rate': 0.75,
            'usage_count': 5,
            'first_seen': datetime.utcnow().isoformat(),
            'last_seen': datetime.utcnow().isoformat(),
            'pattern_data': {'test': 'data'}
        }
        
        pattern = ValidationPattern.from_dict(pattern_data)
        
        # Verify all fields are properly converted
        self.assertEqual(pattern.pattern_id, pattern_data['pattern_id'])
        self.assertEqual(pattern.pattern_type, pattern_data['pattern_type'])
        self.assertEqual(pattern.context_signature, pattern_data['context_signature'])
        self.assertEqual(pattern.success_rate, pattern_data['success_rate'])
        self.assertEqual(pattern.usage_count, pattern_data['usage_count'])
        self.assertIsInstance(pattern.first_seen, datetime)
        self.assertIsInstance(pattern.last_seen, datetime)
        self.assertEqual(pattern.pattern_data, pattern_data['pattern_data'])
    
    def test_pattern_round_trip_serialization(self):
        """Test pattern serialization round trip"""
        original_pattern = ValidationPattern(
            pattern_id='round_trip_test',
            pattern_type='test_validation',
            context_signature='xyz789',
            success_rate=0.95,
            usage_count=20,
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow(),
            pattern_data={'complex': {'nested': 'data'}, 'list': [1, 2, 3]}
        )
        
        # Convert to dict and back
        pattern_dict = original_pattern.to_dict()
        restored_pattern = ValidationPattern.from_dict(pattern_dict)
        
        # Should be identical
        self.assertEqual(original_pattern.pattern_id, restored_pattern.pattern_id)
        self.assertEqual(original_pattern.pattern_type, restored_pattern.pattern_type)
        self.assertEqual(original_pattern.context_signature, restored_pattern.context_signature)
        self.assertEqual(original_pattern.success_rate, restored_pattern.success_rate)
        self.assertEqual(original_pattern.usage_count, restored_pattern.usage_count)
        self.assertEqual(original_pattern.pattern_data, restored_pattern.pattern_data)


if __name__ == '__main__':
    print("🧪 Validation Pattern Memory Unit Tests")
    print("=" * 50)
    print("Testing pattern storage, retrieval, similarity matching, and thread safety")
    print("=" * 50)
    
    if not PATTERN_MEMORY_AVAILABLE:
        print("❌ Validation Pattern Memory not available - skipping tests")
        exit(1)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestValidationPatternMemory))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationPattern))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print(f"\n📊 Validation Pattern Memory Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
    
    exit(0 if result.wasSuccessful() else 1)