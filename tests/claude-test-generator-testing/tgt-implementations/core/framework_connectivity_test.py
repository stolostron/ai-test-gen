#!/usr/bin/env python3
"""
Framework Connectivity Test - Implementation First Approach
Learning from main framework patterns with real executable tests
"""

import os
import subprocess
import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class FrameworkConnectivityTester:
    """
    Real executable testing following main framework patterns
    Implementation-first approach with evidence collection
    """
    
    def __init__(self):
        self.test_results = {}
        self.evidence = {}
        self.main_framework_path = Path("../../apps/claude-test-generator/")
        self.test_start_time = datetime.now()
        
    def collect_evidence(self, test_name: str, data: Any) -> None:
        """Collect REAL evidence from test execution"""
        if 'evidence' not in self.test_results:
            self.test_results['evidence'] = {}
        
        self.test_results['evidence'][test_name] = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'test_duration': (datetime.now() - self.test_start_time).total_seconds()
        }
    
    def assert_with_evidence(self, condition: bool, message: str, evidence_data: Any = None) -> bool:
        """Assert with evidence collection - learn from main framework pattern"""
        if evidence_data:
            self.collect_evidence(f"assertion_{len(self.evidence)}", evidence_data)
        
        if not condition:
            raise AssertionError(f"FAILED: {message}")
        
        return True
    
    def test_main_framework_accessibility(self) -> Dict[str, Any]:
        """Test read access to main framework - REAL functionality test"""
        print("🔍 Testing main framework accessibility...")
        
        test_result = {
            'test_name': 'main_framework_accessibility',
            'start_time': datetime.now().isoformat()
        }
        
        try:
            # Test CLAUDE.md accessibility
            claude_md_path = self.main_framework_path / "CLAUDE.md"
            claude_md_exists = claude_md_path.exists()
            
            # Test .claude directory structure
            claude_dir_path = self.main_framework_path / ".claude"
            claude_dir_exists = claude_dir_path.exists()
            
            # Test ai-services directory
            services_dir_path = claude_dir_path / "ai-services"
            services_dir_exists = services_dir_path.exists()
            
            # Collect real evidence
            evidence = {
                'claude_md_exists': claude_md_exists,
                'claude_md_path': str(claude_md_path),
                'claude_dir_exists': claude_dir_exists,
                'services_dir_exists': services_dir_exists,
                'framework_path_resolved': str(self.main_framework_path.resolve())
            }
            
            # REAL assertions with evidence
            self.assert_with_evidence(
                claude_md_exists, 
                "Main framework CLAUDE.md not accessible",
                evidence
            )
            
            self.assert_with_evidence(
                claude_dir_exists,
                "Main framework .claude directory not accessible", 
                evidence
            )
            
            self.assert_with_evidence(
                services_dir_exists,
                "Main framework ai-services directory not accessible",
                evidence
            )
            
            test_result['status'] = 'PASSED'
            test_result['evidence'] = evidence
            
            print("✅ Main framework accessibility test PASSED")
            return test_result
            
        except Exception as e:
            test_result['status'] = 'FAILED'
            test_result['error'] = str(e)
            print(f"❌ Main framework accessibility test FAILED: {e}")
            return test_result
    
    def test_service_count_audit(self) -> Dict[str, Any]:
        """Audit actual service counts - addressing service architecture gap"""
        print("📊 Auditing service counts...")
        
        test_result = {
            'test_name': 'service_count_audit',
            'start_time': datetime.now().isoformat()
        }
        
        try:
            # Count main framework services using git
            main_services_result = subprocess.run([
                'git', 'ls-files', '../../apps/claude-test-generator/.claude/ai-services/*.md'
            ], capture_output=True, text=True, cwd='.')
            
            main_services_count = len([line for line in main_services_result.stdout.strip().split('\n') if line])
            
            # Count testing framework services
            testing_services_result = subprocess.run([
                'find', '.claude/ai-services/', '-name', '*.md'
            ], capture_output=True, text=True, cwd='.')
            
            testing_services_count = len([line for line in testing_services_result.stdout.strip().split('\n') if line])
            
            # Calculate gap
            service_gap = main_services_count - testing_services_count
            service_coverage = (testing_services_count / main_services_count) * 100 if main_services_count > 0 else 0
            
            evidence = {
                'main_framework_services': main_services_count,
                'testing_framework_services': testing_services_count,
                'service_gap': service_gap,
                'coverage_percentage': service_coverage,
                'main_services_output': main_services_result.stdout,
                'testing_services_output': testing_services_result.stdout
            }
            
            # Evidence-based assertions
            print(f"📈 Main framework services: {main_services_count}")
            print(f"📉 Testing framework services: {testing_services_count}")
            print(f"📊 Coverage: {service_coverage:.1f}%")
            print(f"🔧 Service gap: {service_gap}")
            
            test_result['status'] = 'COMPLETED'
            test_result['evidence'] = evidence
            self.collect_evidence('service_audit', evidence)
            
            return test_result
            
        except Exception as e:
            test_result['status'] = 'FAILED'
            test_result['error'] = str(e)
            print(f"❌ Service count audit FAILED: {e}")
            return test_result
    
    def test_framework_execution_capability(self) -> Dict[str, Any]:
        """Test ability to execute framework commands - REAL execution test"""
        print("⚡ Testing framework execution capability...")
        
        test_result = {
            'test_name': 'framework_execution_capability',
            'start_time': datetime.now().isoformat()
        }
        
        try:
            # Test git status on main framework
            git_status_result = subprocess.run([
                'git', 'status', '--porcelain', '../../apps/claude-test-generator/'
            ], capture_output=True, text=True, cwd='.')
            
            # Test directory listing
            ls_result = subprocess.run([
                'ls', '-la', '../../apps/claude-test-generator/.claude/'
            ], capture_output=True, text=True, cwd='.')
            
            evidence = {
                'git_status_exit_code': git_status_result.returncode,
                'git_status_output': git_status_result.stdout,
                'git_status_error': git_status_result.stderr,
                'ls_exit_code': ls_result.returncode,
                'ls_output': ls_result.stdout,
                'ls_error': ls_result.stderr,
                'execution_timestamp': datetime.now().isoformat()
            }
            
            # REAL assertions based on execution results
            self.assert_with_evidence(
                git_status_result.returncode == 0,
                "Git status command failed",
                evidence
            )
            
            self.assert_with_evidence(
                ls_result.returncode == 0,
                "Directory listing command failed", 
                evidence
            )
            
            test_result['status'] = 'PASSED'
            test_result['evidence'] = evidence
            
            print("✅ Framework execution capability test PASSED")
            return test_result
            
        except Exception as e:
            test_result['status'] = 'FAILED'
            test_result['error'] = str(e)
            print(f"❌ Framework execution capability test FAILED: {e}")
            return test_result
    
    def test_isolation_enforcement(self) -> Dict[str, Any]:
        """Test isolation enforcement - critical security test"""
        print("🛡️ Testing isolation enforcement...")
        
        test_result = {
            'test_name': 'isolation_enforcement',
            'start_time': datetime.now().isoformat()
        }
        
        try:
            # Test write attempt to main framework (should fail)
            test_file_path = self.main_framework_path / "TEST_ISOLATION_CHECK.tmp"
            
            write_attempt_success = False
            write_error = None
            
            try:
                with open(test_file_path, 'w') as f:
                    f.write("This should not be allowed")
                write_attempt_success = True
                
                # Clean up if write succeeded (isolation failed)
                if test_file_path.exists():
                    test_file_path.unlink()
                    
            except Exception as e:
                write_error = str(e)
            
            evidence = {
                'write_attempt_success': write_attempt_success,
                'write_error': write_error,
                'test_file_path': str(test_file_path),
                'isolation_test_timestamp': datetime.now().isoformat()
            }
            
            # Isolation should PREVENT writes
            if write_attempt_success:
                test_result['status'] = 'FAILED'
                test_result['isolation_status'] = 'VIOLATION'
                test_result['message'] = 'CRITICAL: Write access to main framework detected'
                print("❌ CRITICAL: Isolation enforcement FAILED - write access detected")
            else:
                test_result['status'] = 'PASSED'
                test_result['isolation_status'] = 'ENFORCED'
                test_result['message'] = 'Isolation properly enforced'
                print("✅ Isolation enforcement test PASSED")
            
            test_result['evidence'] = evidence
            self.collect_evidence('isolation_test', evidence)
            
            return test_result
            
        except Exception as e:
            test_result['status'] = 'ERROR'
            test_result['error'] = str(e)
            print(f"⚠️ Isolation enforcement test ERROR: {e}")
            return test_result
    
    def run_comprehensive_connectivity_test(self) -> Dict[str, Any]:
        """Run comprehensive connectivity test suite"""
        print("🚀 Starting Comprehensive Framework Connectivity Test")
        print("=" * 60)
        
        comprehensive_results = {
            'test_suite': 'comprehensive_connectivity_test',
            'start_time': self.test_start_time.isoformat(),
            'tests': {}
        }
        
        # Run all tests
        test_methods = [
            self.test_main_framework_accessibility,
            self.test_service_count_audit,
            self.test_framework_execution_capability,
            self.test_isolation_enforcement
        ]
        
        for test_method in test_methods:
            try:
                result = test_method()
                comprehensive_results['tests'][result['test_name']] = result
            except Exception as e:
                print(f"❌ Test {test_method.__name__} failed with exception: {e}")
                comprehensive_results['tests'][test_method.__name__] = {
                    'status': 'EXCEPTION',
                    'error': str(e)
                }
        
        # Calculate overall results
        total_tests = len(comprehensive_results['tests'])
        passed_tests = sum(1 for test in comprehensive_results['tests'].values() 
                          if test.get('status') == 'PASSED')
        failed_tests = sum(1 for test in comprehensive_results['tests'].values() 
                          if test.get('status') == 'FAILED')
        
        comprehensive_results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
            'end_time': datetime.now().isoformat(),
            'total_duration': (datetime.now() - self.test_start_time).total_seconds()
        }
        
        # Store evidence
        comprehensive_results['evidence'] = self.test_results.get('evidence', {})
        
        print("\n" + "=" * 60)
        print("🎯 Comprehensive Test Results:")
        print(f"✅ Passed: {passed_tests}/{total_tests}")
        print(f"❌ Failed: {failed_tests}/{total_tests}")
        print(f"📊 Success Rate: {comprehensive_results['summary']['success_rate']:.1f}%")
        print(f"⏱️ Total Duration: {comprehensive_results['summary']['total_duration']:.2f}s")
        
        return comprehensive_results


def main():
    """Main execution function - implementation first approach"""
    print("🧪 Framework Connectivity Test - Implementation First")
    print("Learning from main framework patterns with real execution")
    print("-" * 60)
    
    tester = FrameworkConnectivityTester()
    results = tester.run_comprehensive_connectivity_test()
    
    # Save results for evidence and learning
    results_file = Path("tgt-implementations/evidence/connectivity_test_results.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to: {results_file}")
    
    # Return exit code based on results
    if results['summary']['failed_tests'] > 0:
        print("⚠️ Some tests failed - see results for details")
        return 1
    else:
        print("🎉 All tests passed successfully!")
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)