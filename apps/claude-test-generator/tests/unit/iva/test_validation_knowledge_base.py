#!/usr/bin/env python3
"""
Validation Knowledge Base Unit Tests
==================================

Comprehensive unit tests for the ValidationKnowledgeBase component of IVA.
Testing knowledge storage, retrieval, updates, and knowledge management capabilities.
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
import hashlib
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
solutions_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'solutions')
sys.path.insert(0, solutions_path)

try:
    from validation_learning_core import ValidationEvent, LearningMode
    from learning_services import ValidationKnowledgeBase
    KNOWLEDGE_BASE_AVAILABLE = True
except ImportError as e:
    KNOWLEDGE_BASE_AVAILABLE = False
    print(f"❌ Validation Knowledge Base not available: {e}")


class TestValidationKnowledgeBase(unittest.TestCase):
    """Test ValidationKnowledgeBase core functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not KNOWLEDGE_BASE_AVAILABLE:
            cls.skipTest(cls, "Validation Knowledge Base not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None
        
        # Create test knowledge base
        self.knowledge_base = ValidationKnowledgeBase(
            storage_path=self.test_dir,
            learning_mode=LearningMode.ADVANCED
        )
        
        # Create test validation events
        self.successful_event = ValidationEvent(
            event_id='knowledge_success_001',
            event_type='evidence_validation',
            context={
                'validation_type': 'evidence',
                'component': 'cluster-curator',
                'operation_type': 'validate',
                'environment': 'test'
            },
            result={
                'success': True,
                'confidence': 0.9,
                'evidence_quality': 'high',
                'validation_method': 'comprehensive'
            },
            timestamp=datetime.utcnow(),
            source_system='evidence_validation_engine',
            success=True,
            confidence=0.9,
            metadata={
                'performance_metrics': {'processing_time': 150},
                'quality_indicators': ['complete_coverage', 'high_confidence'],
                'validation_strategy': 'multi_layer'
            }
        )
        
        self.failed_event = ValidationEvent(
            event_id='knowledge_failure_001',
            event_type='cross_agent_validation',
            context={
                'validation_type': 'cross_agent',
                'component': 'cluster-curator',
                'operation_type': 'conflict_resolution',
                'agents_involved': ['agent_a', 'agent_b']
            },
            result={
                'success': False,
                'confidence': 0.3,
                'conflict_type': 'semantic_inconsistency',
                'resolution_attempted': True
            },
            timestamp=datetime.utcnow(),
            source_system='cross_agent_validation_engine',
            success=False,
            confidence=0.3,
            metadata={
                'failure_indicators': ['conflicting_evidence', 'low_consensus'],
                'conflict_severity': 'high',
                'resolution_strategy': 'fallback_to_primary'
            }
        )
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self.knowledge_base, 'close'):
            self.knowledge_base.close()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_knowledge_base_initialization(self):
        """Test ValidationKnowledgeBase initializes correctly"""
        # Verify initialization
        self.assertEqual(self.knowledge_base.storage_path, Path(self.test_dir))
        self.assertEqual(self.knowledge_base.learning_mode, LearningMode.ADVANCED)
        self.assertTrue(self.knowledge_base.storage_path.exists())
        self.assertTrue(self.knowledge_base.knowledge_db_path.exists())
        
        # Verify database structure
        with sqlite3.connect(str(self.knowledge_base.knowledge_db_path)) as conn:
            # Check knowledge_entries table
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge_entries'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Check knowledge_relationships table
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge_relationships'")
            self.assertIsNotNone(cursor.fetchone())
    
    def test_storage_initialization(self):
        """Test knowledge storage initialization creates correct database schema"""
        # Check database file exists
        self.assertTrue(self.knowledge_base.knowledge_db_path.exists())
        
        # Verify knowledge_entries table structure
        with sqlite3.connect(str(self.knowledge_base.knowledge_db_path)) as conn:
            cursor = conn.execute("PRAGMA table_info(knowledge_entries)")
            columns = {row[1]: row[2] for row in cursor.fetchall()}
            
            expected_columns = {
                'entry_id': 'TEXT',
                'knowledge_type': 'TEXT',
                'subject': 'TEXT',
                'content': 'TEXT',
                'confidence': 'REAL',
                'evidence_count': 'INTEGER',
                'created_at': 'TEXT',
                'updated_at': 'TEXT'
            }
            
            for col_name, col_type in expected_columns.items():
                self.assertIn(col_name, columns)
            
            # Verify knowledge_relationships table structure
            cursor = conn.execute("PRAGMA table_info(knowledge_relationships)")
            rel_columns = {row[1]: row[2] for row in cursor.fetchall()}
            
            expected_rel_columns = {
                'relationship_id': 'TEXT',
                'from_entry_id': 'TEXT',
                'to_entry_id': 'TEXT',
                'relationship_type': 'TEXT',
                'strength': 'REAL',
                'created_at': 'TEXT'
            }
            
            for col_name, col_type in expected_rel_columns.items():
                self.assertIn(col_name, rel_columns)
            
            # Verify indexes exist
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
            indexes = [row[0] for row in cursor.fetchall()]
            self.assertIn('idx_knowledge_type', indexes)
            self.assertIn('idx_subject', indexes)
    
    def test_extract_knowledge_from_successful_event(self):
        """Test knowledge extraction from successful validation event"""
        knowledge_entries = self.knowledge_base._extract_knowledge_from_event(self.successful_event)
        
        # Should extract multiple knowledge entries
        self.assertIsInstance(knowledge_entries, list)
        self.assertGreater(len(knowledge_entries), 0)
        
        # Check for successful pattern knowledge
        successful_patterns = [e for e in knowledge_entries if e['knowledge_type'] == 'successful_pattern']
        self.assertGreater(len(successful_patterns), 0)
        
        pattern_entry = successful_patterns[0]
        self.assertEqual(pattern_entry['subject'], 'evidence_validation:evidence_validation_engine')
        self.assertEqual(pattern_entry['confidence'], 0.9)
        self.assertIn('context_keys', pattern_entry['content'])
        self.assertIn('success_factors', pattern_entry['content'])
        
        # Check for system behavior knowledge
        system_entries = [e for e in knowledge_entries if e['knowledge_type'] == 'system_behavior']
        self.assertGreater(len(system_entries), 0)
        
        system_entry = system_entries[0]
        self.assertEqual(system_entry['subject'], 'evidence_validation_engine')
        self.assertEqual(system_entry['content']['success_rate'], 1.0)
    
    def test_extract_knowledge_from_failed_event(self):
        """Test knowledge extraction from failed validation event"""
        knowledge_entries = self.knowledge_base._extract_knowledge_from_event(self.failed_event)
        
        # Should extract multiple knowledge entries
        self.assertIsInstance(knowledge_entries, list)
        self.assertGreater(len(knowledge_entries), 0)
        
        # Check for failure pattern knowledge
        failure_patterns = [e for e in knowledge_entries if e['knowledge_type'] == 'failure_pattern']
        self.assertGreater(len(failure_patterns), 0)
        
        failure_entry = failure_patterns[0]
        self.assertEqual(failure_entry['subject'], 'cross_agent_validation:cross_agent_validation_engine')
        self.assertEqual(failure_entry['confidence'], 1.0 - 0.3)  # 1.0 - event.confidence
        self.assertIn('context', failure_entry['content'])
        self.assertIn('result', failure_entry['content'])
        self.assertIn('failure_indicators', failure_entry['content'])
        
        # Check for system behavior knowledge
        system_entries = [e for e in knowledge_entries if e['knowledge_type'] == 'system_behavior']
        self.assertGreater(len(system_entries), 0)
        
        system_entry = system_entries[0]
        self.assertEqual(system_entry['subject'], 'cross_agent_validation_engine')
        self.assertEqual(system_entry['content']['success_rate'], 0.0)
    
    def test_generate_entry_id(self):
        """Test unique entry ID generation"""
        knowledge_type = 'successful_pattern'
        subject = 'evidence_validation:test_system'
        
        id1 = self.knowledge_base._generate_entry_id(knowledge_type, subject)
        id2 = self.knowledge_base._generate_entry_id(knowledge_type, subject)
        id3 = self.knowledge_base._generate_entry_id('different_type', subject)
        
        # Same inputs should produce same ID
        self.assertEqual(id1, id2)
        
        # Different inputs should produce different ID
        self.assertNotEqual(id1, id3)
        
        # IDs should be hex strings of expected length
        self.assertEqual(len(id1), 32)
        self.assertTrue(all(c in '0123456789abcdef' for c in id1))
    
    async def test_update_knowledge_entry_new(self):
        """Test creating new knowledge entry"""
        entry_data = {
            'knowledge_type': 'test_pattern',
            'subject': 'test_subject',
            'content': {'test_key': 'test_value', 'quality': 'high'},
            'confidence': 0.85,
            'evidence_count': 1
        }
        
        await self.knowledge_base._update_knowledge_entry(entry_data)
        
        # Verify entry was created in database
        entry_id = self.knowledge_base._generate_entry_id(entry_data['knowledge_type'], entry_data['subject'])
        
        with sqlite3.connect(str(self.knowledge_base.knowledge_db_path)) as conn:
            cursor = conn.execute('SELECT * FROM knowledge_entries WHERE entry_id = ?', (entry_id,))
            db_result = cursor.fetchone()
            
            self.assertIsNotNone(db_result)
            self.assertEqual(db_result[0], entry_id)  # entry_id
            self.assertEqual(db_result[1], entry_data['knowledge_type'])  # knowledge_type
            self.assertEqual(db_result[2], entry_data['subject'])  # subject
            self.assertEqual(db_result[4], entry_data['confidence'])  # confidence
            self.assertEqual(db_result[5], entry_data['evidence_count'])  # evidence_count
            
            # Verify content is properly stored as JSON
            stored_content = json.loads(db_result[3])
            self.assertEqual(stored_content, entry_data['content'])
    
    async def test_update_knowledge_entry_existing(self):
        """Test updating existing knowledge entry"""
        # Create initial entry
        initial_entry = {
            'knowledge_type': 'update_test',
            'subject': 'update_subject',
            'content': {'initial': 'data'},
            'confidence': 0.7,
            'evidence_count': 1
        }
        
        await self.knowledge_base._update_knowledge_entry(initial_entry)
        
        # Update with new evidence
        update_entry = {
            'knowledge_type': 'update_test',
            'subject': 'update_subject',
            'content': {'updated': 'data'},
            'confidence': 0.9,
            'evidence_count': 1
        }
        
        await self.knowledge_base._update_knowledge_entry(update_entry)
        
        # Verify entry was updated (not duplicated)
        entry_id = self.knowledge_base._generate_entry_id(initial_entry['knowledge_type'], initial_entry['subject'])
        
        with sqlite3.connect(str(self.knowledge_base.knowledge_db_path)) as conn:
            cursor = conn.execute('SELECT confidence, evidence_count FROM knowledge_entries WHERE entry_id = ?', (entry_id,))
            db_result = cursor.fetchone()
            
            self.assertIsNotNone(db_result)
            
            # Should have updated confidence (weighted average)
            # (0.7 * 1 + 0.9 * 1) / (1 + 1) = 1.6 / 2 = 0.8
            expected_confidence = (0.7 * 1 + 0.9 * 1) / (1 + 1)
            self.assertAlmostEqual(db_result[0], expected_confidence, places=2)
            
            # Should have increased evidence count
            self.assertEqual(db_result[1], 2)  # 1 + 1
    
    def test_update_knowledge_sync_wrapper(self):
        """Test synchronous update_knowledge wrapper"""
        # Test with safe update conditions
        with patch.object(self.knowledge_base, '_is_update_safe', return_value=True):
            # Should not raise exception
            try:
                self.knowledge_base.update_knowledge(self.successful_event)
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success)
        
        # Test with unsafe update conditions
        with patch.object(self.knowledge_base, '_is_update_safe', return_value=False):
            # Should return silently without error
            try:
                self.knowledge_base.update_knowledge(self.successful_event)
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success)
    
    async def test_update_knowledge_async(self):
        """Test asynchronous knowledge update"""
        # Update knowledge with successful event
        await self.knowledge_base.update_knowledge_async(self.successful_event)
        
        # Verify knowledge entries were created
        with sqlite3.connect(str(self.knowledge_base.knowledge_db_path)) as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM knowledge_entries')
            count = cursor.fetchone()[0]
            self.assertGreater(count, 0)
            
            # Check for specific knowledge types
            cursor = conn.execute('SELECT knowledge_type FROM knowledge_entries')
            types = [row[0] for row in cursor.fetchall()]
            self.assertIn('successful_pattern', types)
            self.assertIn('system_behavior', types)
    
    async def test_query_knowledge_by_subject(self):
        """Test querying knowledge by subject"""
        # Add some knowledge entries
        await self.knowledge_base.update_knowledge_async(self.successful_event)
        await self.knowledge_base.update_knowledge_async(self.failed_event)
        
        # Query by subject
        subject = 'evidence_validation_engine'
        result = self.knowledge_base.query_knowledge(subject)
        
        # Should return results
        self.assertIsNotNone(result)
        self.assertEqual(result['subject'], subject)
        self.assertIn('entries', result)
        self.assertIn('total_entries', result)
        
        # Should have entries for this subject
        self.assertGreater(result['total_entries'], 0)
        self.assertIsInstance(result['entries'], list)
        
        # Verify entry structure
        if result['entries']:
            entry = result['entries'][0]
            expected_fields = [
                'entry_id', 'knowledge_type', 'subject', 'content',
                'confidence', 'evidence_count', 'created_at', 'updated_at'
            ]
            for field in expected_fields:
                self.assertIn(field, entry)
            
            # Content should be properly deserialized
            self.assertIsInstance(entry['content'], dict)
    
    async def test_query_knowledge_by_type(self):
        """Test querying knowledge by subject and type"""
        # Add knowledge entries
        await self.knowledge_base.update_knowledge_async(self.successful_event)
        await self.knowledge_base.update_knowledge_async(self.failed_event)
        
        # Query by subject and specific knowledge type
        subject = 'evidence_validation:evidence_validation_engine'
        knowledge_type = 'successful_pattern'
        
        result = self.knowledge_base.query_knowledge(subject, knowledge_type)
        
        # Should return filtered results
        if result and result['entries']:
            for entry in result['entries']:
                self.assertEqual(entry['knowledge_type'], knowledge_type)
                self.assertEqual(entry['subject'], subject)
    
    def test_query_knowledge_nonexistent(self):
        """Test querying knowledge for nonexistent subject"""
        result = self.knowledge_base.query_knowledge('nonexistent_subject')
        
        # Should return empty result structure
        self.assertIsNotNone(result)
        self.assertEqual(result['subject'], 'nonexistent_subject')
        self.assertEqual(result['total_entries'], 0)
        self.assertEqual(len(result['entries']), 0)
    
    async def test_get_knowledge_summary(self):
        """Test getting knowledge base summary"""
        # Empty knowledge base
        empty_summary = self.knowledge_base.get_knowledge_summary()
        self.assertEqual(empty_summary['total_entries'], 0)
        
        # Add knowledge entries
        await self.knowledge_base.update_knowledge_async(self.successful_event)
        await self.knowledge_base.update_knowledge_async(self.failed_event)
        
        summary = self.knowledge_base.get_knowledge_summary()
        
        # Verify summary structure
        expected_fields = [
            'total_entries', 'average_confidence',
            'entries_by_type', 'last_updated'
        ]
        for field in expected_fields:
            self.assertIn(field, summary)
        
        # Should have entries
        self.assertGreater(summary['total_entries'], 0)
        self.assertGreaterEqual(summary['average_confidence'], 0.0)
        self.assertLessEqual(summary['average_confidence'], 1.0)
        self.assertIsInstance(summary['entries_by_type'], dict)
        
        # Should have different knowledge types
        self.assertIn('successful_pattern', summary['entries_by_type'])
        self.assertIn('system_behavior', summary['entries_by_type'])
    
    def test_update_safety_checks(self):
        """Test update safety checking methods"""
        # Test with valid storage path
        self.assertTrue(self.knowledge_base._is_update_safe())
        
        # Test with invalid storage path
        invalid_kb = ValidationKnowledgeBase(
            storage_path='/invalid/nonexistent/path',
            learning_mode=LearningMode.ADVANCED
        )
        
        # Should handle invalid path gracefully
        result = invalid_kb._is_update_safe()
        self.assertIsInstance(result, bool)
    
    def test_thread_safety(self):
        """Test thread safety of knowledge base operations"""
        async def update_knowledge():
            for i in range(20):
                event = ValidationEvent(
                    event_id=f'thread_kb_{threading.current_thread().ident}_{i}',
                    event_type='thread_test',
                    context={'thread_id': threading.current_thread().ident, 'index': i},
                    result={'success': i % 2 == 0},
                    timestamp=datetime.utcnow(),
                    source_system='thread_test',
                    success=i % 2 == 0,
                    confidence=0.8,
                    metadata={'thread_data': True}
                )
                await self.knowledge_base.update_knowledge_async(event)
        
        def thread_worker():
            asyncio.run(update_knowledge())
        
        # Run multiple threads concurrently
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=thread_worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should complete without errors
        # Verify knowledge was stored
        summary = self.knowledge_base.get_knowledge_summary()
        self.assertGreater(summary['total_entries'], 0)
        
        # Query for thread test knowledge
        result = self.knowledge_base.query_knowledge('thread_test')
        self.assertGreater(result['total_entries'], 0)
    
    def test_error_handling_in_knowledge_operations(self):
        """Test error handling in knowledge base operations"""
        # Test with corrupted database path
        with patch.object(self.knowledge_base, 'knowledge_db_path', Path('/invalid/path/knowledge.db')):
            async def test_update():
                entry_data = {
                    'knowledge_type': 'error_test',
                    'subject': 'error_subject',
                    'content': {'test': 'data'},
                    'confidence': 0.8,
                    'evidence_count': 1
                }
                # Should handle database errors gracefully
                await self.knowledge_base._update_knowledge_entry(entry_data)
            
            # Should not raise exception
            try:
                asyncio.run(test_update())
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success)
        
        # Test query with corrupted database
        with patch.object(self.knowledge_base, 'knowledge_db_path', Path('/invalid/path/knowledge.db')):
            result = self.knowledge_base.query_knowledge('test_subject')
            self.assertIsNone(result)  # Should return None on error
        
        # Test summary with corrupted database
        with patch.object(self.knowledge_base, 'knowledge_db_path', Path('/invalid/path/knowledge.db')):
            summary = self.knowledge_base.get_knowledge_summary()
            self.assertEqual(summary, {})  # Should return empty dict on error
    
    def test_knowledge_extraction_edge_cases(self):
        """Test knowledge extraction with edge cases"""
        # Event with minimal context
        minimal_event = ValidationEvent(
            event_id='minimal_test',
            event_type='minimal_validation',
            context={},
            result={},
            timestamp=datetime.utcnow(),
            source_system='minimal_system',
            success=True,
            confidence=0.5,
            metadata={}
        )
        
        knowledge_entries = self.knowledge_base._extract_knowledge_from_event(minimal_event)
        
        # Should still extract some knowledge
        self.assertIsInstance(knowledge_entries, list)
        self.assertGreater(len(knowledge_entries), 0)
        
        # Should include system behavior knowledge
        system_entries = [e for e in knowledge_entries if e['knowledge_type'] == 'system_behavior']
        self.assertGreater(len(system_entries), 0)
    
    def test_knowledge_confidence_thresholds(self):
        """Test knowledge extraction with different confidence thresholds"""
        # High confidence event (should create successful pattern)
        high_conf_event = ValidationEvent(
            event_id='high_conf_test',
            event_type='confidence_test',
            context={'test': 'high_confidence'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='confidence_test',
            success=True,
            confidence=0.95,  # High confidence
            metadata={'quality': 'excellent'}
        )
        
        high_conf_knowledge = self.knowledge_base._extract_knowledge_from_event(high_conf_event)
        successful_patterns = [e for e in high_conf_knowledge if e['knowledge_type'] == 'successful_pattern']
        self.assertGreater(len(successful_patterns), 0)
        
        # Low confidence event (should not create successful pattern)
        low_conf_event = ValidationEvent(
            event_id='low_conf_test',
            event_type='confidence_test',
            context={'test': 'low_confidence'},
            result={'success': True},
            timestamp=datetime.utcnow(),
            source_system='confidence_test',
            success=True,
            confidence=0.6,  # Low confidence (< 0.7 threshold)
            metadata={'quality': 'poor'}
        )
        
        low_conf_knowledge = self.knowledge_base._extract_knowledge_from_event(low_conf_event)
        successful_patterns = [e for e in low_conf_knowledge if e['knowledge_type'] == 'successful_pattern']
        self.assertEqual(len(successful_patterns), 0)  # Should not create successful pattern
    
    def test_close_cleanup(self):
        """Test cleanup when closing knowledge base"""
        # Close should not raise any errors
        try:
            self.knowledge_base.close()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    async def test_comprehensive_knowledge_workflow(self):
        """Test complete knowledge workflow from event to query"""
        # Add various types of knowledge
        events = [
            self.successful_event,
            self.failed_event,
            ValidationEvent(
                event_id='workflow_test_001',
                event_type='context_validation',
                context={'validation_type': 'context', 'workflow': 'test'},
                result={'success': True, 'context_score': 0.88},
                timestamp=datetime.utcnow(),
                source_system='context_validation_engine',
                success=True,
                confidence=0.88,
                metadata={'workflow_stage': 'final'}
            )
        ]
        
        # Update knowledge with all events
        for event in events:
            await self.knowledge_base.update_knowledge_async(event)
        
        # Verify knowledge was stored
        summary = self.knowledge_base.get_knowledge_summary()
        self.assertGreater(summary['total_entries'], 0)
        
        # Query different types of knowledge
        evidence_knowledge = self.knowledge_base.query_knowledge('evidence_validation_engine')
        self.assertGreater(evidence_knowledge['total_entries'], 0)
        
        cross_agent_knowledge = self.knowledge_base.query_knowledge('cross_agent_validation_engine')
        self.assertGreater(cross_agent_knowledge['total_entries'], 0)
        
        context_knowledge = self.knowledge_base.query_knowledge('context_validation_engine')
        self.assertGreater(context_knowledge['total_entries'], 0)
        
        # Query by specific type
        successful_patterns = self.knowledge_base.query_knowledge(
            'evidence_validation:evidence_validation_engine',
            'successful_pattern'
        )
        if successful_patterns and successful_patterns['entries']:
            self.assertEqual(successful_patterns['entries'][0]['knowledge_type'], 'successful_pattern')
        
        # Verify knowledge types in summary
        self.assertIn('successful_pattern', summary['entries_by_type'])
        self.assertIn('failure_pattern', summary['entries_by_type'])
        self.assertIn('system_behavior', summary['entries_by_type'])


if __name__ == '__main__':
    print("🧪 Validation Knowledge Base Unit Tests")
    print("=" * 50)
    print("Testing knowledge storage, retrieval, updates, and knowledge management capabilities")
    print("=" * 50)
    
    if not KNOWLEDGE_BASE_AVAILABLE:
        print("❌ Validation Knowledge Base not available - skipping tests")
        exit(1)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestValidationKnowledgeBase))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print(f"\n📊 Validation Knowledge Base Test Summary:")
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