#!/usr/bin/env python3
"""
Validation Analytics Service Unit Tests
=====================================

Comprehensive unit tests for the ValidationAnalyticsService component of IVA.
Testing insights generation, trend analysis, predictions, and analytics capabilities.
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
from collections import defaultdict, deque

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
solutions_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'solutions')
sys.path.insert(0, solutions_path)

try:
    from validation_learning_core import ValidationEvent, ValidationInsights, LearningMode
    from learning_services import ValidationAnalyticsService
    ANALYTICS_SERVICE_AVAILABLE = True
except ImportError as e:
    ANALYTICS_SERVICE_AVAILABLE = False
    print(f"❌ Validation Analytics Service not available: {e}")


class TestValidationAnalyticsService(unittest.TestCase):
    """Test ValidationAnalyticsService core functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not ANALYTICS_SERVICE_AVAILABLE:
            cls.skipTest(cls, "Validation Analytics Service not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None
        
        # Create test analytics service
        self.analytics_service = ValidationAnalyticsService(
            storage_path=self.test_dir,
            learning_mode=LearningMode.STANDARD
        )
        
        # Create test validation events
        self.base_time = datetime.utcnow()
        self.test_events = [
            ValidationEvent(
                event_id=f'test_event_{i:03d}',
                event_type='evidence_validation',
                context={
                    'validation_type': 'evidence',
                    'component': f'component_{i % 3}',
                    'operation_type': 'validate'
                },
                result={'success': i % 2 == 0, 'confidence': 0.8 + (i % 5) * 0.04},
                timestamp=self.base_time - timedelta(hours=i),
                source_system='evidence_validation_engine',
                success=i % 2 == 0,  # Alternating success/failure
                confidence=0.8 + (i % 5) * 0.04,
                metadata={'test_index': i}
            )
            for i in range(20)
        ]
    
    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self.analytics_service, 'close'):
            self.analytics_service.close()
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_analytics_service_initialization(self):
        """Test ValidationAnalyticsService initializes correctly"""
        # Verify initialization
        self.assertEqual(self.analytics_service.storage_path, Path(self.test_dir))
        self.assertEqual(self.analytics_service.learning_mode, LearningMode.STANDARD)
        self.assertIsInstance(self.analytics_service.validation_history, deque)
        self.assertIsInstance(self.analytics_service.trend_data, defaultdict)
        
        # Verify storage initialization
        self.assertTrue(self.analytics_service.storage_path.exists())
        self.assertTrue(self.analytics_service.analytics_db.exists())
        
        # Verify database structure
        with sqlite3.connect(str(self.analytics_service.analytics_db)) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='validation_events'")
            self.assertIsNotNone(cursor.fetchone())
            
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trend_data'")
            self.assertIsNotNone(cursor.fetchone())
    
    def test_storage_initialization(self):
        """Test analytics storage initialization creates correct database schema"""
        # Check database file exists
        self.assertTrue(self.analytics_service.analytics_db.exists())
        
        # Verify validation_events table structure
        with sqlite3.connect(str(self.analytics_service.analytics_db)) as conn:
            cursor = conn.execute("PRAGMA table_info(validation_events)")
            columns = {row[1]: row[2] for row in cursor.fetchall()}
            
            expected_columns = {
                'event_id': 'TEXT',
                'event_type': 'TEXT',
                'timestamp': 'TEXT',
                'success': 'INTEGER',
                'confidence': 'REAL',
                'source_system': 'TEXT',
                'processing_time_ms': 'REAL'
            }
            
            for col_name, col_type in expected_columns.items():
                self.assertIn(col_name, columns)
            
            # Verify trend_data table structure
            cursor = conn.execute("PRAGMA table_info(trend_data)")
            trend_columns = {row[1]: row[2] for row in cursor.fetchall()}
            
            expected_trend_columns = {
                'date': 'TEXT',
                'metric_name': 'TEXT',
                'metric_value': 'REAL'
            }
            
            for col_name, col_type in expected_trend_columns.items():
                self.assertIn(col_name, trend_columns)
    
    def test_record_validation_event(self):
        """Test recording validation events for analytics"""
        event = self.test_events[0]
        processing_time = 15.5
        
        # Record event
        self.analytics_service.record_validation_event(event, processing_time)
        
        # Verify event is in history
        self.assertEqual(len(self.analytics_service.validation_history), 1)
        recorded_event = self.analytics_service.validation_history[0]
        
        self.assertEqual(recorded_event['event_id'], event.event_id)
        self.assertEqual(recorded_event['event_type'], event.event_type)
        self.assertEqual(recorded_event['success'], event.success)
        self.assertEqual(recorded_event['confidence'], event.confidence)
        self.assertEqual(recorded_event['processing_time_ms'], processing_time)
        
        # Verify event is added to trend data
        date_key = event.timestamp.strftime('%Y-%m-%d')
        self.assertIn(date_key, self.analytics_service.trend_data)
        self.assertEqual(len(self.analytics_service.trend_data[date_key]), 1)
    
    def test_record_multiple_validation_events(self):
        """Test recording multiple validation events"""
        # Record multiple events
        for i, event in enumerate(self.test_events[:5]):
            self.analytics_service.record_validation_event(event, i * 2.0)
        
        # Verify all events are recorded
        self.assertEqual(len(self.analytics_service.validation_history), 5)
        
        # Verify trend data organization by date
        total_trend_events = sum(len(events) for events in self.analytics_service.trend_data.values())
        self.assertEqual(total_trend_events, 5)
    
    def test_find_similar_events(self):
        """Test finding similar validation events"""
        # Record several events
        for event in self.test_events[:10]:
            self.analytics_service.record_validation_event(event)
        
        # Search for similar events
        search_context = {
            'validation_type': 'evidence',
            'source_system': 'evidence_validation_engine'
        }
        
        similar_events = self.analytics_service._find_similar_events(search_context)
        
        # Should find events with same validation type or source system
        self.assertGreater(len(similar_events), 0)
        self.assertLessEqual(len(similar_events), 50)  # Limited to last 50
        
        # Verify similarity logic
        for event in similar_events:
            self.assertTrue(
                event.get('event_type') == 'evidence_validation' or
                event.get('source_system') == 'evidence_validation_engine'
            )
    
    def test_generate_insights_insufficient_data(self):
        """Test insights generation with insufficient data"""
        # No events recorded
        insights = self.analytics_service.generate_insights({'test': 'context'})
        self.assertIsNone(insights)
        
        # Record one event (insufficient for insights)
        self.analytics_service.record_validation_event(self.test_events[0])
        
        insights = self.analytics_service.generate_insights({'validation_type': 'different'})
        self.assertIsNone(insights)  # No similar events
    
    def test_generate_insights_with_similar_events(self):
        """Test insights generation with sufficient similar events"""
        # Record multiple similar events
        for event in self.test_events[:10]:
            self.analytics_service.record_validation_event(event, 10.0 + event.confidence * 5)
        
        # Generate insights for similar context
        search_context = {
            'validation_type': 'evidence',
            'source_system': 'evidence_validation_engine'
        }
        
        insights = self.analytics_service.generate_insights(search_context)
        
        # Should generate insights
        self.assertIsNotNone(insights)
        self.assertIsInstance(insights, ValidationInsights)
        
        # Verify insights structure
        self.assertEqual(insights.insight_type, 'analytics_insights')
        self.assertGreater(insights.confidence, 0.0)
        self.assertLessEqual(insights.confidence, 1.0)
        self.assertIsInstance(insights.recommendations, list)
        self.assertIsInstance(insights.predictions, list)
        self.assertIsInstance(insights.patterns_matched, list)
    
    def test_generate_recommendations(self):
        """Test recommendation generation based on similar events"""
        # Create events with different success patterns
        successful_events = [
            {
                'success': True,
                'confidence': 0.9,
                'processing_time_ms': 10.0,
                'source_system': 'test'
            } for _ in range(8)
        ]
        
        failed_events = [
            {
                'success': False,
                'confidence': 0.3,
                'processing_time_ms': 50.0,
                'source_system': 'test'
            } for _ in range(2)
        ]
        
        all_events = successful_events + failed_events
        
        recommendations = self.analytics_service._generate_recommendations(all_events)
        
        # Should generate recommendations
        self.assertIsInstance(recommendations, list)
        
        # Check for performance recommendation (since we have successful events)
        performance_recs = [r for r in recommendations if r['type'] == 'performance']
        self.assertGreater(len(performance_recs), 0)
        
        # Test with high failure rate
        mostly_failed_events = [
            {'success': False, 'confidence': 0.3, 'processing_time_ms': 20.0} for _ in range(8)
        ] + [
            {'success': True, 'confidence': 0.9, 'processing_time_ms': 10.0} for _ in range(2)
        ]
        
        caution_recommendations = self.analytics_service._generate_recommendations(mostly_failed_events)
        
        # Should generate caution recommendation
        caution_recs = [r for r in caution_recommendations if r['type'] == 'caution']
        self.assertGreater(len(caution_recs), 0)
    
    def test_generate_predictions(self):
        """Test prediction generation based on similar events"""
        # Create events with known success pattern
        events_with_pattern = []
        for i in range(10):
            events_with_pattern.append({
                'success': i < 7,  # 70% success rate
                'confidence': 0.8 if i < 7 else 0.4,
                'processing_time_ms': 15.0
            })
        
        predictions = self.analytics_service._generate_predictions(events_with_pattern, {})
        
        # Should generate predictions
        self.assertIsInstance(predictions, list)
        self.assertGreater(len(predictions), 0)
        
        # Check for success probability prediction
        success_predictions = [p for p in predictions if p['type'] == 'success_probability']
        self.assertGreater(len(success_predictions), 0)
        
        success_pred = success_predictions[0]
        self.assertAlmostEqual(success_pred['value'], 0.7, places=1)  # 70% success rate
        
        # Check for confidence prediction
        confidence_predictions = [p for p in predictions if p['type'] == 'expected_confidence']
        self.assertGreater(len(confidence_predictions), 0)
    
    def test_analyze_validation_trends_insufficient_data(self):
        """Test trend analysis with insufficient data"""
        # No events recorded
        trends = self.analytics_service.analyze_validation_trends()
        self.assertIsNone(trends)
        
        # Record insufficient events (< 10)
        for event in self.test_events[:5]:
            self.analytics_service.record_validation_event(event)
        
        trends = self.analytics_service.analyze_validation_trends()
        self.assertIsNone(trends)
    
    def test_analyze_validation_trends_with_data(self):
        """Test trend analysis with sufficient data"""
        # Record events with different timestamps
        current_time = datetime.utcnow()
        for i, event in enumerate(self.test_events[:15]):
            # Distribute events across different time periods
            event.timestamp = current_time - timedelta(hours=i * 2)
            self.analytics_service.record_validation_event(event, 10.0 + i)
        
        trends = self.analytics_service.analyze_validation_trends()
        
        # Should generate trends
        self.assertIsNotNone(trends)
        self.assertIsInstance(trends, dict)
        
        # Check for expected trend periods
        expected_periods = ['last_24h', 'last_7d', 'overall']
        for period in expected_periods:
            if period in trends:
                self.assertIn('total_events', trends[period])
                self.assertIn('success_rate', trends[period])
                self.assertIn('avg_confidence', trends[period])
    
    def test_calculate_trend_metrics(self):
        """Test trend metrics calculation"""
        # Create test events with known metrics
        test_events = []
        for i in range(10):
            test_events.append({
                'success': i < 6,  # 60% success rate
                'confidence': 0.7 + (i % 3) * 0.1,
                'processing_time_ms': 20.0 + i * 2,
                'source_system': f'system_{i % 2}'
            })
        
        metrics = self.analytics_service._calculate_trend_metrics(test_events)
        
        # Verify metrics calculation
        self.assertEqual(metrics['total_events'], 10)
        self.assertAlmostEqual(metrics['success_rate'], 0.6, places=2)
        self.assertGreater(metrics['avg_confidence'], 0.0)
        self.assertGreater(metrics['avg_processing_time_ms'], 0.0)
        
        # Verify by_system breakdown
        self.assertIn('by_system', metrics)
        self.assertIn('system_0', metrics['by_system'])
        self.assertIn('system_1', metrics['by_system'])
        
        # Each system should have 5 events
        self.assertEqual(metrics['by_system']['system_0']['event_count'], 5)
        self.assertEqual(metrics['by_system']['system_1']['event_count'], 5)
    
    def test_predict_validation_outcome_insufficient_data(self):
        """Test outcome prediction with insufficient data"""
        # No events recorded
        prediction = self.analytics_service.predict_validation_outcome({'test': 'context'})
        self.assertIsNone(prediction)
        
        # Record insufficient similar events
        for event in self.test_events[:2]:
            self.analytics_service.record_validation_event(event)
        
        prediction = self.analytics_service.predict_validation_outcome({'validation_type': 'different'})
        self.assertIsNone(prediction)
    
    def test_predict_validation_outcome_with_data(self):
        """Test outcome prediction with sufficient data"""
        # Record events with known success pattern
        for event in self.test_events[:10]:
            self.analytics_service.record_validation_event(event)
        
        # Predict outcome for similar context
        search_context = {'validation_type': 'evidence'}
        prediction = self.analytics_service.predict_validation_outcome(search_context)
        
        # Should generate prediction
        self.assertIsNotNone(prediction)
        self.assertIsInstance(prediction, dict)
        
        # Verify prediction structure
        expected_fields = [
            'success_probability', 'expected_confidence',
            'sample_size', 'prediction_confidence'
        ]
        
        for field in expected_fields:
            self.assertIn(field, prediction)
        
        # Verify prediction values
        self.assertGreaterEqual(prediction['success_probability'], 0.0)
        self.assertLessEqual(prediction['success_probability'], 1.0)
        self.assertGreaterEqual(prediction['expected_confidence'], 0.0)
        self.assertLessEqual(prediction['expected_confidence'], 1.0)
        self.assertGreater(prediction['sample_size'], 0)
    
    async def test_store_event_to_db(self):
        """Test storing event to analytics database"""
        event_record = {
            'event_id': 'test_db_001',
            'event_type': 'test_validation',
            'timestamp': datetime.utcnow(),
            'success': True,
            'confidence': 0.85,
            'source_system': 'test_system',
            'processing_time_ms': 12.5
        }
        
        # Store event to database
        await self.analytics_service._store_event_to_db(event_record)
        
        # Verify event is in database
        with sqlite3.connect(str(self.analytics_service.analytics_db)) as conn:
            cursor = conn.execute('SELECT event_id FROM validation_events WHERE event_id = ?', 
                                (event_record['event_id'],))
            db_result = cursor.fetchone()
            self.assertIsNotNone(db_result)
            self.assertEqual(db_result[0], event_record['event_id'])
    
    def test_analytics_safety_checks(self):
        """Test analytics safety checking methods"""
        # Should not be safe with no data
        empty_service = ValidationAnalyticsService(
            storage_path=tempfile.mkdtemp(),
            learning_mode=LearningMode.STANDARD
        )
        self.assertFalse(empty_service._is_analytics_safe())
        
        # Should be safe with data
        self.analytics_service.record_validation_event(self.test_events[0])
        self.assertTrue(self.analytics_service._is_analytics_safe())
    
    def test_thread_safety(self):
        """Test thread safety of analytics operations"""
        def record_events():
            for i in range(20):
                event = ValidationEvent(
                    event_id=f'thread_{threading.current_thread().ident}_{i}',
                    event_type='thread_test',
                    context={'thread_id': threading.current_thread().ident},
                    result={'success': True},
                    timestamp=datetime.utcnow(),
                    source_system='thread_test',
                    success=True,
                    confidence=0.8,
                    metadata={}
                )
                self.analytics_service.record_validation_event(event, i * 1.5)
        
        # Run multiple threads concurrently
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=record_events)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should complete without errors
        # Check that events were recorded
        self.assertGreater(len(self.analytics_service.validation_history), 0)
        
        # Generate insights to verify functionality
        insights = self.analytics_service.generate_insights({'thread_test': True})
        # May or may not generate insights depending on timing, but should not crash
        self.assertIsInstance(insights, (ValidationInsights, type(None)))
    
    def test_error_handling_in_analytics(self):
        """Test error handling in analytics operations"""
        # Test with corrupted database path
        with patch.object(self.analytics_service, 'analytics_db', Path('/invalid/path/analytics.db')):
            async def test_store():
                event_record = {
                    'event_id': 'error_test',
                    'event_type': 'test',
                    'timestamp': datetime.utcnow(),
                    'success': True,
                    'confidence': 0.8,
                    'source_system': 'test',
                    'processing_time_ms': 10.0
                }
                # Should handle database errors gracefully
                await self.analytics_service._store_event_to_db(event_record)
            
            # Should not raise exception
            try:
                asyncio.run(test_store())
                success = True
            except Exception:
                success = False
            
            self.assertTrue(success)
        
        # Test insights generation with broken similar events finding
        with patch.object(self.analytics_service, '_find_similar_events', side_effect=Exception("Error")):
            insights = self.analytics_service.generate_insights({'test': 'context'})
            self.assertIsNone(insights)  # Should return None on error
        
        # Test trend analysis with broken metrics calculation
        self.analytics_service.record_validation_event(self.test_events[0])  # Add some data
        with patch.object(self.analytics_service, '_calculate_trend_metrics', side_effect=Exception("Error")):
            trends = self.analytics_service.analyze_validation_trends()
            self.assertIsNone(trends)  # Should return None on error
    
    def test_close_cleanup(self):
        """Test cleanup when closing analytics service"""
        # Add some data to history and trend data
        for event in self.test_events[:5]:
            self.analytics_service.record_validation_event(event)
        
        # Verify data exists
        self.assertGreater(len(self.analytics_service.validation_history), 0)
        self.assertGreater(len(self.analytics_service.trend_data), 0)
        
        # Close should clear data
        self.analytics_service.close()
        
        self.assertEqual(len(self.analytics_service.validation_history), 0)
        self.assertEqual(len(self.analytics_service.trend_data), 0)
    
    def test_validation_history_maxlen(self):
        """Test validation history respects maximum length"""
        # Record more events than maxlen (10000)
        maxlen = self.analytics_service.validation_history.maxlen
        
        # Record events beyond maxlen
        for i in range(maxlen + 100):
            event = ValidationEvent(
                event_id=f'maxlen_test_{i}',
                event_type='maxlen_test',
                context={'index': i},
                result={'success': True},
                timestamp=datetime.utcnow(),
                source_system='maxlen_test',
                success=True,
                confidence=0.8,
                metadata={}
            )
            self.analytics_service.record_validation_event(event)
        
        # Should not exceed maxlen
        self.assertEqual(len(self.analytics_service.validation_history), maxlen)
    
    def test_insights_confidence_calculation(self):
        """Test insights confidence calculation based on sample size"""
        # Record varying numbers of similar events
        test_cases = [1, 5, 10, 15, 20]
        
        for num_events in test_cases:
            # Clear previous data
            self.analytics_service.validation_history.clear()
            
            # Record specific number of events
            for i in range(num_events):
                event = ValidationEvent(
                    event_id=f'confidence_test_{i}',
                    event_type='confidence_test',
                    context={'confidence_test': True},
                    result={'success': True},
                    timestamp=datetime.utcnow(),
                    source_system='confidence_test',
                    success=True,
                    confidence=0.8,
                    metadata={}
                )
                self.analytics_service.record_validation_event(event)
            
            insights = self.analytics_service.generate_insights({'confidence_test': True})
            
            if insights:  # May be None for insufficient data
                # Confidence should increase with more events (capped at 0.9)
                expected_confidence = min(0.9, num_events / 10.0)
                self.assertAlmostEqual(insights.confidence, expected_confidence, places=2)


if __name__ == '__main__':
    print("🧪 Validation Analytics Service Unit Tests")
    print("=" * 55)
    print("Testing insights generation, trend analysis, predictions, and analytics capabilities")
    print("=" * 55)
    
    if not ANALYTICS_SERVICE_AVAILABLE:
        print("❌ Validation Analytics Service not available - skipping tests")
        exit(1)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestValidationAnalyticsService))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print(f"\n📊 Validation Analytics Service Test Summary:")
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