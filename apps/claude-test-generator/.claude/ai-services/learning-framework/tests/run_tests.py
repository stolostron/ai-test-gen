#!/usr/bin/env python3
"""
Test runner for Agent Learning Framework

Runs all tests and validates framework functionality
"""

import sys
import os
import asyncio
import unittest
from pathlib import Path

# Add parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import test modules
from test_learning_framework import (
    TestLearningFrameworkNonBlocking,
    TestPatternDatabase,
    TestPerformanceTracker,
    TestAsyncExecutor,
    TestEndToEndIntegration
)


def run_async_test(test_func):
    """Helper to run async test functions"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(test_func())
    finally:
        loop.close()


def main():
    """Run all tests and report results"""
    print("=" * 70)
    print("Agent Learning Framework - Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestLearningFrameworkNonBlocking,
        TestPatternDatabase,
        TestPerformanceTracker,
        TestAsyncExecutor,
        TestEndToEndIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    # Validation checks
    print()
    print("Validation Checks:")
    print("-" * 40)
    
    validations = [
        ("Non-blocking execution", len([t for t in result.failures if 'non_blocking' in str(t)]) == 0),
        ("Failure isolation", len([t for t in result.failures if 'isolation' in str(t)]) == 0),
        ("Pattern storage", len([t for t in result.failures if 'pattern' in str(t)]) == 0),
        ("Performance tracking", len([t for t in result.failures if 'performance' in str(t)]) == 0),
        ("Async processing", len([t for t in result.failures if 'async' in str(t)]) == 0)
    ]
    
    all_valid = True
    for check_name, passed in validations:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name:.<35} {status}")
        if not passed:
            all_valid = False
    
    print()
    print("=" * 70)
    
    if result.wasSuccessful() and all_valid:
        print("✅ All tests passed! Learning Framework is ready for integration.")
        return 0
    else:
        print("❌ Some tests failed. Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
