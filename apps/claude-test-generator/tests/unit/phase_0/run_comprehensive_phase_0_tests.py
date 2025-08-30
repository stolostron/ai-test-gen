#!/usr/bin/env python3
"""
Comprehensive Phase 0 Test Runner
Runs all Phase 0 unit tests and provides detailed reporting
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add AI services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services'))

# Import all test modules
from test_version_intelligence_service import TestVersionIntelligenceService, TestFoundationContextValidation
from test_phase_0_version_logic import TestPhase0VersionLogic, TestVersionIntelligenceServiceRealDataIssues
from test_phase_0_deterministic_connection import TestPhase0DeterministicConnection, TestPhase0DeterministicConnectionRealData


class Phase0TestRunner:
    """Comprehensive test runner for Phase 0 validation"""
    
    def __init__(self):
        self.test_suites = []
        self.results = {}
        
    def add_test_suite(self, test_class, name):
        """Add a test suite to the runner"""
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(test_class)
        self.test_suites.append((suite, name))
        
    def run_all_tests(self):
        """Run all test suites and collect results"""
        
        print("=" * 80)
        print("🚀 COMPREHENSIVE PHASE 0 UNIT TEST VALIDATION")
        print("=" * 80)
        print()
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_errors = 0
        
        start_time = time.time()
        
        for suite, name in self.test_suites:
            print(f"📋 Running {name}...")
            print("-" * 60)
            
            # Capture test output
            test_output = StringIO()
            runner = unittest.TextTestRunner(
                stream=test_output,
                verbosity=2,
                buffer=True
            )
            
            suite_start_time = time.time()
            result = runner.run(suite)
            suite_end_time = time.time()
            
            # Store results
            suite_tests = result.testsRun
            suite_passed = suite_tests - len(result.failures) - len(result.errors)
            suite_failed = len(result.failures)
            suite_errors = len(result.errors)
            
            self.results[name] = {
                'tests': suite_tests,
                'passed': suite_passed,
                'failed': suite_failed,
                'errors': suite_errors,
                'success_rate': (suite_passed / suite_tests * 100) if suite_tests > 0 else 0,
                'duration': suite_end_time - suite_start_time,
                'result': result
            }
            
            # Update totals
            total_tests += suite_tests
            total_passed += suite_passed
            total_failed += suite_failed
            total_errors += suite_errors
            
            # Print suite summary
            success_rate = self.results[name]['success_rate']
            duration = self.results[name]['duration']
            
            print(f"✅ Tests: {suite_tests}")
            print(f"✅ Passed: {suite_passed}")
            print(f"❌ Failed: {suite_failed}")
            print(f"⚠️  Errors: {suite_errors}")
            print(f"📊 Success Rate: {success_rate:.1f}%")
            print(f"⏱️  Duration: {duration:.2f}s")
            
            if result.failures:
                print(f"🔍 Failures:")
                for test, traceback in result.failures:
                    print(f"   • {test}: {traceback.split('AssertionError:')[-1].strip() if 'AssertionError:' in traceback else 'Unknown failure'}")
            
            if result.errors:
                print(f"⚠️  Errors:")
                for test, traceback in result.errors:
                    print(f"   • {test}: {traceback.split('Exception:')[-1].strip() if 'Exception:' in traceback else 'Unknown error'}")
            
            print()
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Print comprehensive summary
        print("=" * 80)
        print("📊 COMPREHENSIVE PHASE 0 TEST RESULTS SUMMARY")
        print("=" * 80)
        
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"🎯 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {total_passed}")
        print(f"   ❌ Failed: {total_failed}")
        print(f"   ⚠️  Errors: {total_errors}")
        print(f"   📊 Overall Success Rate: {overall_success_rate:.1f}%")
        print(f"   ⏱️  Total Duration: {total_duration:.2f}s")
        print()
        
        # Test suite breakdown
        print(f"📋 TEST SUITE BREAKDOWN:")
        for name, result in self.results.items():
            status = "✅ PASS" if result['failed'] == 0 and result['errors'] == 0 else "❌ FAIL"
            print(f"   {status} {name}: {result['success_rate']:.1f}% ({result['passed']}/{result['tests']})")
        print()
        
        # Critical assessment
        print(f"🔍 CRITICAL ASSESSMENT:")
        
        # Deterministic connection tests
        deterministic_tests = [name for name in self.results.keys() if 'deterministic' in name.lower()]
        if deterministic_tests:
            det_success = sum(self.results[name]['passed'] for name in deterministic_tests)
            det_total = sum(self.results[name]['tests'] for name in deterministic_tests)
            det_rate = (det_success / det_total * 100) if det_total > 0 else 0
            print(f"   🔗 Deterministic Connection Logic: {det_rate:.1f}% ({det_success}/{det_total})")
        
        # Version logic tests
        version_tests = [name for name in self.results.keys() if 'version' in name.lower()]
        if version_tests:
            ver_success = sum(self.results[name]['passed'] for name in version_tests)
            ver_total = sum(self.results[name]['tests'] for name in version_tests)
            ver_rate = (ver_success / ver_total * 100) if ver_total > 0 else 0
            print(f"   📊 Version Gap Analysis Logic: {ver_rate:.1f}% ({ver_success}/{ver_total})")
        
        # Foundation context tests
        foundation_tests = [name for name in self.results.keys() if 'foundation' in name.lower() or 'context' in name.lower()]
        if foundation_tests:
            found_success = sum(self.results[name]['passed'] for name in foundation_tests)
            found_total = sum(self.results[name]['tests'] for name in foundation_tests)
            found_rate = (found_success / found_total * 100) if found_total > 0 else 0
            print(f"   🏗️  Foundation Context Generation: {found_rate:.1f}% ({found_success}/{found_total})")
        
        print()
        
        # Final assessment
        if overall_success_rate >= 90:
            print(f"🎉 EXCELLENT: Phase 0 implementation is highly validated with {overall_success_rate:.1f}% success rate")
        elif overall_success_rate >= 75:
            print(f"✅ GOOD: Phase 0 implementation is well validated with {overall_success_rate:.1f}% success rate")
        elif overall_success_rate >= 60:
            print(f"⚠️  ACCEPTABLE: Phase 0 implementation is adequately validated with {overall_success_rate:.1f}% success rate")
        else:
            print(f"❌ NEEDS WORK: Phase 0 implementation needs improvement with {overall_success_rate:.1f}% success rate")
        
        print()
        print("=" * 80)
        
        return overall_success_rate >= 75


def main():
    """Main execution function"""
    
    runner = Phase0TestRunner()
    
    # Add all test suites
    runner.add_test_suite(TestVersionIntelligenceService, "Core Version Intelligence Service")
    runner.add_test_suite(TestFoundationContextValidation, "Foundation Context Validation")
    runner.add_test_suite(TestPhase0VersionLogic, "Version Gap Analysis Logic")
    runner.add_test_suite(TestVersionIntelligenceServiceRealDataIssues, "Real Data Issues Validation")
    runner.add_test_suite(TestPhase0DeterministicConnection, "Deterministic Environment Connection")
    runner.add_test_suite(TestPhase0DeterministicConnectionRealData, "Real Data Connection Scenarios")
    
    # Run all tests
    success = runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()