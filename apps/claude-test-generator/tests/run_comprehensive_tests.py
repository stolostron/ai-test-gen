#!/usr/bin/env python3
"""
Comprehensive Unit Test Runner
Runs all unit tests for the Hybrid AI-Traditional Architecture implementation
"""

import unittest
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import importlib.util

def load_test_module(module_path):
    """Load a test module from file path"""
    module_name = Path(module_path).stem
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def discover_unit_tests():
    """Discover all unit test files"""
    test_files = []
    
    # Find unit test files
    unit_test_dirs = [
        "tests/unit/ai_services",
        "tests/unit/phase_0"
    ]
    
    for test_dir in unit_test_dirs:
        if os.path.exists(test_dir):
            for file_path in Path(test_dir).glob("test_*.py"):
                test_files.append(str(file_path))
    
    return test_files

def run_integration_tests():
    """Run integration tests"""
    integration_tests = [
        "tests/test_phase_0_validation.py",
        "tests/test_phase_2_ai_integration.py"
    ]
    
    results = {}
    
    for test_file in integration_tests:
        if os.path.exists(test_file):
            print(f"\n🧪 Running Integration Test: {test_file}")
            print("=" * 60)
            
            # Run the test file
            result = os.system(f"python3 {test_file}")
            results[test_file] = result == 0
            
            if result == 0:
                print(f"✅ {test_file}: PASSED")
            else:
                print(f"❌ {test_file}: FAILED")
    
    return results

def run_unit_tests():
    """Run all unit tests"""
    print("🔬 Discovering Unit Tests...")
    test_files = discover_unit_tests()
    
    if not test_files:
        print("⚠️  No unit test files found")
        return {}
    
    print(f"📋 Found {len(test_files)} unit test files:")
    for test_file in test_files:
        print(f"   - {test_file}")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    results = {}
    
    for test_file in test_files:
        print(f"\n🧪 Running Unit Tests: {test_file}")
        print("-" * 60)
        
        try:
            # Load test module
            module = load_test_module(test_file)
            
            # Add tests to suite
            test_module_suite = loader.loadTestsFromModule(module)
            
            # Run tests for this module
            runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
            result = runner.run(test_module_suite)
            
            # Record results
            results[test_file] = {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'success': len(result.failures) == 0 and len(result.errors) == 0
            }
            
            if results[test_file]['success']:
                print(f"✅ {test_file}: ALL TESTS PASSED ({result.testsRun} tests)")
            else:
                print(f"❌ {test_file}: {results[test_file]['failures']} failures, {results[test_file]['errors']} errors")
                
        except Exception as e:
            print(f"❌ Failed to run {test_file}: {e}")
            results[test_file] = {
                'tests_run': 0,
                'failures': 0,
                'errors': 1,
                'success': False,
                'error': str(e)
            }
    
    return results

def generate_test_report(unit_results, integration_results):
    """Generate comprehensive test report"""
    report = {
        'test_execution_timestamp': datetime.now().isoformat(),
        'test_summary': {
            'unit_tests': {},
            'integration_tests': {},
            'overall': {}
        },
        'detailed_results': {
            'unit_tests': unit_results,
            'integration_tests': integration_results
        }
    }
    
    # Calculate unit test summary
    total_unit_files = len(unit_results)
    successful_unit_files = sum(1 for r in unit_results.values() if isinstance(r, dict) and r.get('success', False))
    total_unit_tests = sum(r.get('tests_run', 0) for r in unit_results.values() if isinstance(r, dict))
    total_unit_failures = sum(r.get('failures', 0) for r in unit_results.values() if isinstance(r, dict))
    total_unit_errors = sum(r.get('errors', 0) for r in unit_results.values() if isinstance(r, dict))
    
    report['test_summary']['unit_tests'] = {
        'total_test_files': total_unit_files,
        'successful_test_files': successful_unit_files,
        'total_tests': total_unit_tests,
        'total_failures': total_unit_failures,
        'total_errors': total_unit_errors,
        'success_rate': successful_unit_files / total_unit_files if total_unit_files > 0 else 0
    }
    
    # Calculate integration test summary
    total_integration_files = len(integration_results)
    successful_integration_files = sum(1 for r in integration_results.values() if r)
    
    report['test_summary']['integration_tests'] = {
        'total_test_files': total_integration_files,
        'successful_test_files': successful_integration_files,
        'success_rate': successful_integration_files / total_integration_files if total_integration_files > 0 else 0
    }
    
    # Calculate overall summary
    total_files = total_unit_files + total_integration_files
    successful_files = successful_unit_files + successful_integration_files
    
    report['test_summary']['overall'] = {
        'total_test_files': total_files,
        'successful_test_files': successful_files,
        'overall_success_rate': successful_files / total_files if total_files > 0 else 0,
        'all_tests_passed': successful_files == total_files
    }
    
    return report

def print_test_summary(report):
    """Print formatted test summary"""
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
    print("=" * 80)
    
    # Unit tests summary
    unit_summary = report['test_summary']['unit_tests']
    print(f"\n🔬 Unit Tests:")
    print(f"   📁 Test Files: {unit_summary['successful_test_files']}/{unit_summary['total_test_files']} passed")
    print(f"   🧪 Total Tests: {unit_summary['total_tests']}")
    print(f"   ✅ Passed: {unit_summary['total_tests'] - unit_summary['total_failures'] - unit_summary['total_errors']}")
    print(f"   ❌ Failed: {unit_summary['total_failures']}")
    print(f"   🚫 Errors: {unit_summary['total_errors']}")
    print(f"   📈 Success Rate: {unit_summary['success_rate']:.1%}")
    
    # Integration tests summary
    integration_summary = report['test_summary']['integration_tests']
    print(f"\n🔗 Integration Tests:")
    print(f"   📁 Test Files: {integration_summary['successful_test_files']}/{integration_summary['total_test_files']} passed")
    print(f"   📈 Success Rate: {integration_summary['success_rate']:.1%}")
    
    # Overall summary
    overall_summary = report['test_summary']['overall']
    print(f"\n🎯 Overall Results:")
    print(f"   📁 Total Test Files: {overall_summary['successful_test_files']}/{overall_summary['total_test_files']} passed")
    print(f"   📈 Overall Success Rate: {overall_summary['overall_success_rate']:.1%}")
    
    if overall_summary['all_tests_passed']:
        print(f"\n🎉 ALL TESTS PASSED! Hybrid AI-Traditional Architecture is fully validated")
        print(f"✅ Unit Tests: {unit_summary['success_rate']:.1%} success rate")
        print(f"✅ Integration Tests: {integration_summary['success_rate']:.1%} success rate")
        print(f"✅ Overall: {overall_summary['overall_success_rate']:.1%} success rate")
    else:
        print(f"\n⚠️  Some tests failed. Implementation needs attention.")
        failed_files = []
        
        # Check unit test failures
        for test_file, result in report['detailed_results']['unit_tests'].items():
            if isinstance(result, dict) and not result.get('success', False):
                failed_files.append(f"   ❌ {test_file}")
        
        # Check integration test failures
        for test_file, success in report['detailed_results']['integration_tests'].items():
            if not success:
                failed_files.append(f"   ❌ {test_file}")
        
        if failed_files:
            print(f"\n📋 Failed Test Files:")
            for failed_file in failed_files:
                print(failed_file)

def save_test_report(report):
    """Save test report to file"""
    # Create reports directory if it doesn't exist
    reports_dir = Path("tests/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = reports_dir / f"comprehensive_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Test report saved to: {report_file}")
    return str(report_file)

def main():
    """Main test execution function"""
    print("🚀 Starting Comprehensive Test Suite for Hybrid AI-Traditional Architecture")
    print("=" * 80)
    
    # Run unit tests
    print("\n🔬 PHASE 1: Running Unit Tests")
    print("=" * 80)
    unit_results = run_unit_tests()
    
    # Run integration tests
    print("\n🔗 PHASE 2: Running Integration Tests")
    print("=" * 80)
    integration_results = run_integration_tests()
    
    # Generate and display report
    report = generate_test_report(unit_results, integration_results)
    print_test_summary(report)
    
    # Save report
    report_file = save_test_report(report)
    
    # Return success status
    return report['test_summary']['overall']['all_tests_passed']

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)