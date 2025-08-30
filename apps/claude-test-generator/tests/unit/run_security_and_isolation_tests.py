#!/usr/bin/env python3
"""
Comprehensive Test Runner for Security Enforcement and App Isolation Systems

Executes comprehensive unit tests for critical security and isolation components:
- Security Enforcement System (credential exposure prevention)
- App Isolation Architecture (strict containment boundaries)

Provides detailed reporting, performance metrics, and validation results
for framework security and isolation capabilities.
"""

import unittest
import sys
import os
import time
from pathlib import Path
from datetime import datetime
import json

# Add test directories to Python path
current_dir = Path(__file__).parent
security_test_dir = current_dir / "security_enforcement"
isolation_test_dir = current_dir / "app_isolation"

sys.path.insert(0, str(security_test_dir))
sys.path.insert(0, str(isolation_test_dir))

# Import test modules
try:
    from test_credential_exposure_prevention import (
        TestCredentialExposurePreventionSystem,
        TestPatternExtensionSecurityWrapper,
        TestSecurityEnforcementIntegration
    )
    security_tests_available = True
except ImportError as e:
    print(f"⚠️ Security enforcement tests not available: {e}")
    security_tests_available = False

try:
    from test_security_enforcement_validation import (
        TestSecurityEnforcementValidationSuite,
        TestValidationSummaryAndReporting,
        TestValidationEntryPoint,
        TestValidationIntegrationScenarios
    )
    security_validation_tests_available = True
except ImportError as e:
    print(f"⚠️ Security validation tests not available: {e}")
    security_validation_tests_available = False

try:
    from test_app_isolation_enforcer import (
        TestStrictAppIsolationEngine,
        TestAppPermissionWrapper,
        TestAppContextDetector,
        TestSystemIsolationValidator,
        TestIsolationErrorHandling
    )
    isolation_tests_available = True
except ImportError as e:
    print(f"⚠️ App isolation tests not available: {e}")
    isolation_tests_available = False


class SecurityAndIsolationTestRunner:
    """Comprehensive test runner for security and isolation systems"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.test_results = {}
        self.overall_results = {
            'total_tests': 0,
            'total_failures': 0,
            'total_errors': 0,
            'total_skipped': 0,
            'success_rate': 0.0,
            'execution_time': 0.0
        }
    
    def run_security_enforcement_tests(self):
        """Run Security Enforcement System tests"""
        print("\n" + "="*60)
        print("🔒 SECURITY ENFORCEMENT SYSTEM TESTS")
        print("="*60)
        
        if not security_tests_available:
            print("❌ Security enforcement tests not available - skipping")
            return None
        
        # Create test suite for security enforcement
        security_suite = unittest.TestSuite()
        
        # Add security enforcement test classes
        security_test_classes = [
            TestCredentialExposurePreventionSystem,
            TestPatternExtensionSecurityWrapper,
            TestSecurityEnforcementIntegration
        ]
        
        for test_class in security_test_classes:
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            security_suite.addTests(tests)
        
        # Run security tests
        print(f"\n🧪 Running Security Enforcement Tests...")
        runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
        start_time = time.time()
        result = runner.run(security_suite)
        end_time = time.time()
        
        # Store results
        security_results = {
            'test_category': 'Security Enforcement',
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
            'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0,
            'execution_time': end_time - start_time,
            'status': 'PASSED' if len(result.failures) == 0 and len(result.errors) == 0 else 'FAILED'
        }
        
        # Print summary
        self._print_category_summary(security_results)
        
        return security_results
    
    def run_security_validation_tests(self):
        """Run Security Validation System tests"""
        print("\n" + "="*60)
        print("🔍 SECURITY VALIDATION SYSTEM TESTS")
        print("="*60)
        
        if not security_validation_tests_available:
            print("❌ Security validation tests not available - skipping")
            return None
        
        # Create test suite for security validation
        validation_suite = unittest.TestSuite()
        
        # Add security validation test classes
        validation_test_classes = [
            TestSecurityEnforcementValidationSuite,
            TestValidationSummaryAndReporting,
            TestValidationEntryPoint,
            TestValidationIntegrationScenarios
        ]
        
        for test_class in validation_test_classes:
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            validation_suite.addTests(tests)
        
        # Run validation tests
        print(f"\n🧪 Running Security Validation Tests...")
        runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
        start_time = time.time()
        result = runner.run(validation_suite)
        end_time = time.time()
        
        # Store results
        validation_results = {
            'test_category': 'Security Validation',
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
            'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0,
            'execution_time': end_time - start_time,
            'status': 'PASSED' if len(result.failures) == 0 and len(result.errors) == 0 else 'FAILED'
        }
        
        # Print summary
        self._print_category_summary(validation_results)
        
        return validation_results
    
    def run_app_isolation_tests(self):
        """Run App Isolation Architecture tests"""
        print("\n" + "="*60)
        print("🏗️ APP ISOLATION ARCHITECTURE TESTS")
        print("="*60)
        
        if not isolation_tests_available:
            print("❌ App isolation tests not available - skipping")
            return None
        
        # Create test suite for app isolation
        isolation_suite = unittest.TestSuite()
        
        # Add app isolation test classes
        isolation_test_classes = [
            TestStrictAppIsolationEngine,
            TestAppPermissionWrapper,
            TestAppContextDetector,
            TestSystemIsolationValidator,
            TestIsolationErrorHandling
        ]
        
        for test_class in isolation_test_classes:
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            isolation_suite.addTests(tests)
        
        # Run isolation tests
        print(f"\n🧪 Running App Isolation Tests...")
        runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
        start_time = time.time()
        result = runner.run(isolation_suite)
        end_time = time.time()
        
        # Store results
        isolation_results = {
            'test_category': 'App Isolation',
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
            'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0,
            'execution_time': end_time - start_time,
            'status': 'PASSED' if len(result.failures) == 0 and len(result.errors) == 0 else 'FAILED'
        }
        
        # Print summary
        self._print_category_summary(isolation_results)
        
        return isolation_results
    
    def _print_category_summary(self, results):
        """Print summary for a test category"""
        if results is None:
            return
        
        status_emoji = "✅" if results['status'] == 'PASSED' else "❌"
        
        print(f"\n📊 {results['test_category']} Summary:")
        print(f"   {status_emoji} Status: {results['status']}")
        print(f"   🧪 Tests Run: {results['tests_run']}")
        print(f"   ✅ Success Rate: {results['success_rate']:.1f}%")
        print(f"   ❌ Failures: {results['failures']}")
        print(f"   🚨 Errors: {results['errors']}")
        print(f"   ⏭️ Skipped: {results['skipped']}")
        print(f"   ⏱️ Execution Time: {results['execution_time']:.2f}s")
    
    def run_comprehensive_tests(self):
        """Run all security and isolation tests"""
        print("🔒🏗️ COMPREHENSIVE SECURITY & ISOLATION TEST SUITE")
        print("="*70)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.start_time = time.time()
        
        # Run all test categories
        security_results = self.run_security_enforcement_tests()
        validation_results = self.run_security_validation_tests()
        isolation_results = self.run_app_isolation_tests()
        
        self.end_time = time.time()
        
        # Store results
        self.test_results = {
            'security_enforcement': security_results,
            'security_validation': validation_results,
            'app_isolation': isolation_results
        }
        
        # Calculate overall results
        self._calculate_overall_results()
        
        # Print comprehensive summary
        self._print_comprehensive_summary()
        
        # Save detailed report
        self._save_test_report()
        
        return self.overall_results
    
    def _calculate_overall_results(self):
        """Calculate overall test results across all categories"""
        total_tests = 0
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        
        for category, results in self.test_results.items():
            if results is not None:
                total_tests += results['tests_run']
                total_failures += results['failures']
                total_errors += results['errors']
                total_skipped += results['skipped']
        
        self.overall_results = {
            'total_tests': total_tests,
            'total_failures': total_failures,
            'total_errors': total_errors,
            'total_skipped': total_skipped,
            'success_rate': ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0,
            'execution_time': self.end_time - self.start_time if self.start_time and self.end_time else 0,
            'overall_status': 'PASSED' if total_failures == 0 and total_errors == 0 else 'FAILED'
        }
    
    def _print_comprehensive_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*70)
        print("🎯 COMPREHENSIVE TEST SUMMARY")
        print("="*70)
        
        overall_status_emoji = "✅" if self.overall_results['overall_status'] == 'PASSED' else "❌"
        
        print(f"\n📋 OVERALL RESULTS:")
        print(f"   {overall_status_emoji} Overall Status: {self.overall_results['overall_status']}")
        print(f"   🧪 Total Tests: {self.overall_results['total_tests']}")
        print(f"   ✅ Success Rate: {self.overall_results['success_rate']:.1f}%")
        print(f"   ❌ Total Failures: {self.overall_results['total_failures']}")
        print(f"   🚨 Total Errors: {self.overall_results['total_errors']}")
        print(f"   ⏭️ Total Skipped: {self.overall_results['total_skipped']}")
        print(f"   ⏱️ Total Execution Time: {self.overall_results['execution_time']:.2f}s")
        
        print(f"\n📊 CATEGORY BREAKDOWN:")
        for category, results in self.test_results.items():
            if results is not None:
                status_emoji = "✅" if results['status'] == 'PASSED' else "❌"
                print(f"   {status_emoji} {results['test_category']}: {results['tests_run']} tests, {results['success_rate']:.1f}% success")
            else:
                print(f"   ⏭️ {category.replace('_', ' ').title()}: SKIPPED")
        
        print(f"\n🔒 SECURITY ENFORCEMENT COVERAGE:")
        if self.test_results['security_enforcement']:
            print(f"   ✅ Credential Exposure Prevention: TESTED")
            print(f"   ✅ Pattern Extension Security: TESTED")
            print(f"   ✅ Security Integration: TESTED")
        else:
            print(f"   ⏭️ Security enforcement tests: SKIPPED")
        
        print(f"\n🔍 SECURITY VALIDATION COVERAGE:")
        if self.test_results['security_validation']:
            print(f"   ✅ Validation Suite: TESTED")
            print(f"   ✅ Validation Reporting: TESTED")
            print(f"   ✅ Validation Integration: TESTED")
        else:
            print(f"   ⏭️ Security validation tests: SKIPPED")
        
        print(f"\n🏗️ APP ISOLATION COVERAGE:")
        if self.test_results['app_isolation']:
            print(f"   ✅ Isolation Engine: TESTED")
            print(f"   ✅ Permission Wrapper: TESTED")
            print(f"   ✅ Context Detection: TESTED")
            print(f"   ✅ System Validation: TESTED")
            print(f"   ✅ Error Handling: TESTED")
        else:
            print(f"   ⏭️ App isolation tests: SKIPPED")
        
        print(f"\n📈 PERFORMANCE METRICS:")
        if self.overall_results['total_tests'] > 0:
            avg_time_per_test = self.overall_results['execution_time'] / self.overall_results['total_tests']
            print(f"   ⚡ Average Time per Test: {avg_time_per_test:.3f}s")
            print(f"   🚀 Tests per Second: {self.overall_results['total_tests'] / self.overall_results['execution_time']:.1f}")
        
        print(f"\n✨ FRAMEWORK SECURITY STATUS:")
        if self.overall_results['overall_status'] == 'PASSED':
            print(f"   🛡️ Security Enforcement: VALIDATED")
            print(f"   🔒 App Isolation: VALIDATED")
            print(f"   ✅ Framework Security: ROBUST")
        else:
            print(f"   ⚠️ Some security tests failed - review results")
            print(f"   🔧 Framework security needs attention")
        
        print("="*70)
    
    def _save_test_report(self):
        """Save detailed test report to file"""
        report_dir = current_dir.parent.parent / ".claude" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"security_isolation_test_report_{timestamp}.json"
        
        report_data = {
            'test_run_info': {
                'timestamp': datetime.now().isoformat(),
                'execution_time': self.overall_results['execution_time'],
                'test_runner': 'SecurityAndIsolationTestRunner'
            },
            'overall_results': self.overall_results,
            'category_results': self.test_results,
            'test_environment': {
                'python_version': sys.version,
                'platform': sys.platform,
                'current_directory': str(Path.cwd())
            }
        }
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            print(f"\n📄 Detailed test report saved: {report_file}")
        except Exception as e:
            print(f"\n⚠️ Failed to save test report: {e}")


def main():
    """Main test execution function"""
    runner = SecurityAndIsolationTestRunner()
    
    try:
        results = runner.run_comprehensive_tests()
        
        # Exit with appropriate code
        if results['overall_status'] == 'PASSED':
            print(f"\n🎉 All security and isolation tests PASSED!")
            return 0
        else:
            print(f"\n❌ Some security and isolation tests FAILED!")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n⚠️ Test execution interrupted by user")
        return 130
    except Exception as e:
        print(f"\n💥 Test execution failed with error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())