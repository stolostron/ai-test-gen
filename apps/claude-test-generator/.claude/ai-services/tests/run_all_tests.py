#!/usr/bin/env python3
"""
Test suite runner for Information Sufficiency feature
Runs all unit and integration tests with detailed reporting
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
import test_information_sufficiency_analyzer
import test_framework_stop_handler
import test_jira_agent_integration


def run_test_suite():
    """Run complete test suite with detailed reporting"""
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test modules
    suite.addTests(loader.loadTestsFromModule(test_information_sufficiency_analyzer))
    suite.addTests(loader.loadTestsFromModule(test_framework_stop_handler))
    suite.addTests(loader.loadTestsFromModule(test_jira_agent_integration))
    
    # Count total tests
    total_tests = suite.countTestCases()
    
    print("=" * 70)
    print("INFORMATION SUFFICIENCY FEATURE - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"\nTotal tests to run: {total_tests}")
    print("\nTest Modules:")
    print("1. InformationSufficiencyAnalyzer - Unit Tests")
    print("2. FrameworkStopHandler - Unit Tests")
    print("3. JIRA Intelligence Agent - Integration Tests")
    print("\n" + "-" * 70)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUITE SUMMARY")
    print("=" * 70)
    print(f"\nTotal Tests Run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"\nExecution Time: {end_time - start_time:.2f} seconds")
    
    # Print failures if any
    if result.failures:
        print("\n" + "-" * 70)
        print("FAILURES:")
        for test, traceback in result.failures:
            print(f"\n{test}:")
            print(traceback)
    
    # Print errors if any
    if result.errors:
        print("\n" + "-" * 70)
        print("ERRORS:")
        for test, traceback in result.errors:
            print(f"\n{test}:")
            print(traceback)
    
    # Overall result
    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED! The Information Sufficiency feature is working correctly.")
    else:
        print("❌ SOME TESTS FAILED. Please review the errors above.")
    print("=" * 70)
    
    return result.wasSuccessful()


def run_specific_test_module(module_name):
    """Run tests from a specific module"""
    
    modules = {
        'analyzer': test_information_sufficiency_analyzer,
        'handler': test_framework_stop_handler,
        'integration': test_jira_agent_integration
    }
    
    if module_name not in modules:
        print(f"Unknown module: {module_name}")
        print(f"Available modules: {', '.join(modules.keys())}")
        return False
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(modules[module_name])
    
    print(f"\nRunning tests for: {module_name}")
    print("-" * 50)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Run specific module
        module = sys.argv[1]
        success = run_specific_test_module(module)
    else:
        # Run all tests
        success = run_test_suite()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
