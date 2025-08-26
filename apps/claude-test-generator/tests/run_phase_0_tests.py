#!/usr/bin/env python3
"""
Phase 0 Unit Test Runner
Executes Phase 0 tests and provides comprehensive reporting
"""

import sys
import os
import unittest
import time
import json
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class TestExecutionReport:
    """Comprehensive test execution report"""
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    execution_time: float
    implementation_gaps: List[str]
    critical_failures: List[str]
    recommendations: List[str]


class Phase0TestRunner:
    """
    Comprehensive test runner for Phase 0 unit tests
    Provides detailed reporting on implementation gaps
    """
    
    def __init__(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.phase_0_test_dir = os.path.join(self.test_dir, 'unit', 'phase_0')
        
    def run_tests(self) -> TestExecutionReport:
        """Execute all Phase 0 tests and generate comprehensive report"""
        print("🔬 Starting Phase 0 Unit Test Execution")
        print("=" * 60)
        
        start_time = time.time()
        
        # Discover and load tests
        loader = unittest.TestLoader()
        suite = loader.discover(self.phase_0_test_dir, pattern='test_*.py')
        
        # Execute tests with custom result collector
        result_collector = DetailedTestResult()
        runner = unittest.TextTestRunner(
            stream=sys.stdout,
            verbosity=2,
            resultclass=lambda stream, descriptions, verbosity: result_collector
        )
        
        print(f"📂 Test Discovery: Found {suite.countTestCases()} tests in {self.phase_0_test_dir}")
        print("🚀 Executing tests...\n")
        
        test_result = runner.run(suite)
        
        execution_time = time.time() - start_time
        
        # Analyze results
        report = self._analyze_test_results(test_result, execution_time)
        
        # Print comprehensive report
        self._print_comprehensive_report(report)
        
        return report
    
    def _analyze_test_results(self, test_result, execution_time: float) -> TestExecutionReport:
        """Analyze test results and identify implementation gaps"""
        
        implementation_gaps = []
        critical_failures = []
        recommendations = []
        
        # Analyze failures for implementation gaps
        for test, error in test_result.failures + test_result.errors:
            test_name = test._testMethodName
            error_message = str(error)
            
            if "not found" in error_message.lower() or "import" in error_message.lower():
                implementation_gaps.append(f"{test_name}: Implementation missing")
                recommendations.append(f"Implement {test_name.replace('test_', '').replace('_', ' ')}")
            
            if "critical" in test_name.lower():
                critical_failures.append(f"{test_name}: {error_message.split(chr(10))[0]}")
        
        # Generate specific recommendations based on patterns
        if any("version_intelligence_service_exists" in gap for gap in implementation_gaps):
            recommendations.append("Create .claude/ai-services/version_intelligence_service.py")
            recommendations.append("Implement analyze_version_gap() function")
            recommendations.append("Implement create_foundation_context() function")
        
        if any("generates_actual_files" in gap for gap in implementation_gaps):
            recommendations.append("Ensure Phase 0 creates foundation-context.json output file")
            recommendations.append("Implement agent output reality validation")
        
        if any("foundation_context_completeness" in gap for gap in implementation_gaps):
            recommendations.append("Implement Progressive Context Architecture foundation")
            recommendations.append("Create Universal Context Manager service")
        
        return TestExecutionReport(
            total_tests=test_result.testsRun,
            passed_tests=test_result.testsRun - len(test_result.failures) - len(test_result.errors),
            failed_tests=len(test_result.failures) + len(test_result.errors),
            skipped_tests=len(test_result.skipped),
            execution_time=execution_time,
            implementation_gaps=implementation_gaps,
            critical_failures=critical_failures,
            recommendations=recommendations
        )
    
    def _print_comprehensive_report(self, report: TestExecutionReport):
        """Print comprehensive test execution report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE PHASE 0 TEST REPORT")
        print("=" * 60)
        
        # Test execution summary
        print(f"\n🎯 Test Execution Summary:")
        print(f"   Total Tests:    {report.total_tests}")
        print(f"   Passed:         {report.passed_tests} ✅")
        print(f"   Failed:         {report.failed_tests} ❌")
        print(f"   Skipped:        {report.skipped_tests} ⏸️")
        print(f"   Execution Time: {report.execution_time:.2f}s")
        
        # Success rate calculation
        success_rate = (report.passed_tests / report.total_tests * 100) if report.total_tests > 0 else 0
        print(f"   Success Rate:   {success_rate:.1f}%")
        
        # Implementation gaps analysis
        if report.implementation_gaps:
            print(f"\n🚨 Implementation Gaps Detected ({len(report.implementation_gaps)}):")
            for gap in report.implementation_gaps:
                print(f"   ❌ {gap}")
        else:
            print(f"\n✅ No Implementation Gaps Detected")
        
        # Critical failures
        if report.critical_failures:
            print(f"\n🔥 Critical Failures ({len(report.critical_failures)}):")
            for failure in report.critical_failures:
                print(f"   🔥 {failure}")
        
        # Recommendations
        if report.recommendations:
            print(f"\n💡 Recommendations ({len(report.recommendations)}):")
            for i, rec in enumerate(report.recommendations, 1):
                print(f"   {i}. {rec}")
        
        # Overall assessment
        print(f"\n🎯 Overall Assessment:")
        if report.failed_tests == 0:
            print("   ✅ Phase 0 implementation appears complete and functional")
        elif len(report.implementation_gaps) > 0:
            print("   ❌ Phase 0 has critical implementation gaps requiring attention")
        else:
            print("   ⚠️  Phase 0 has issues but implementation foundation exists")
        
        # Next steps
        print(f"\n🚀 Next Steps:")
        if report.failed_tests == 0:
            print("   1. Proceed with Phase 1 unit test development")
            print("   2. Implement integration tests for Progressive Context Architecture")
            print("   3. Add end-to-end framework execution tests")
        else:
            print("   1. Address implementation gaps identified above")
            print("   2. Re-run tests to validate fixes")
            print("   3. Consider creating mock implementations for testing")


class DetailedTestResult(unittest.TestResult):
    """Custom test result collector for detailed analysis"""
    
    def __init__(self):
        super().__init__()
        self.test_details = []
    
    def startTest(self, test):
        super().startTest(test)
        print(f"🔬 Running: {test._testMethodName}")
    
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"   ✅ PASSED")
    
    def addError(self, test, err):
        super().addError(test, err)
        print(f"   ❌ ERROR: {err[1]}")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"   ❌ FAILED: {err[1]}")
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        print(f"   ⏸️  SKIPPED: {reason}")


def main():
    """Main execution function"""
    print("🎯 Phase 0 Unit Test Framework")
    print("Comprehensive testing for Version Intelligence Service")
    print(f"Testing Framework Implementation vs Documentation Claims\n")
    
    # Check if we're in the right directory
    current_dir = os.getcwd()
    if not os.path.exists(os.path.join(current_dir, 'tests')):
        print("❌ Error: Must run from claude-test-generator directory")
        print("   Run: cd apps/claude-test-generator/")
        print("   Then: python tests/run_phase_0_tests.py")
        sys.exit(1)
    
    # Execute tests
    runner = Phase0TestRunner()
    report = runner.run_tests()
    
    # Save report to file
    report_file = os.path.join('tests', 'phase_0_test_report.json')
    with open(report_file, 'w') as f:
        json.dump({
            'total_tests': report.total_tests,
            'passed_tests': report.passed_tests,
            'failed_tests': report.failed_tests,
            'execution_time': report.execution_time,
            'implementation_gaps': report.implementation_gaps,
            'critical_failures': report.critical_failures,
            'recommendations': report.recommendations,
            'timestamp': time.time()
        }, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    # Exit with appropriate code
    exit_code = 0 if report.failed_tests == 0 else 1
    print(f"\n🏁 Test execution complete. Exit code: {exit_code}")
    sys.exit(exit_code)


if __name__ == '__main__':
    main()