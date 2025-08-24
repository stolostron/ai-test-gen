#!/usr/bin/env python3
"""
Functional Test Suite - Implementation First Approach
Testing framework components using main framework patterns
"""

import subprocess
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import tempfile

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from evidence.real_evidence_collector import RealEvidenceCollector

class FunctionalTestSuite:
    """
    Real functional test suite following main framework patterns
    Tests actual framework components with executable validation
    """
    
    def __init__(self):
        self.test_results = {}
        self.evidence_collector = RealEvidenceCollector()
        self.framework_path = "../../../../apps/claude-test-generator"
        self.test_session_id = self.generate_test_session_id()
        
    def generate_test_session_id(self) -> str:
        """Generate unique test session ID"""
        return f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def test_framework_accessibility(self) -> Dict[str, Any]:
        """Test framework accessibility and basic structure"""
        print("🔍 Testing framework accessibility...")
        
        test_result = {
            'test_name': 'framework_accessibility',
            'start_time': datetime.now().isoformat(),
            'test_category': 'infrastructure'
        }
        
        try:
            framework_dir = Path(self.framework_path)
            
            # Test basic accessibility
            accessibility_checks = {
                'framework_directory_exists': framework_dir.exists(),
                'claude_directory_exists': (framework_dir / '.claude').exists(),
                'ai_services_directory_exists': (framework_dir / '.claude' / 'ai-services').exists(),
                'main_claude_md_exists': (framework_dir / 'CLAUDE.md').exists(),
                'runs_directory_exists': (framework_dir / 'runs').exists()
            }
            
            # Test git accessibility
            git_result = subprocess.run([
                'git', 'status', '--porcelain', self.framework_path
            ], capture_output=True, text=True, timeout=10)
            
            accessibility_checks['git_accessible'] = git_result.returncode == 0
            
            # Calculate accessibility score
            accessibility_score = sum(accessibility_checks.values()) / len(accessibility_checks) * 100
            
            test_result.update({
                'status': 'PASSED' if accessibility_score >= 80 else 'FAILED',
                'accessibility_checks': accessibility_checks,
                'accessibility_score': accessibility_score,
                'git_status_result': {
                    'exit_code': git_result.returncode,
                    'stdout': git_result.stdout,
                    'stderr': git_result.stderr
                }
            })
            
            print(f"✅ Framework accessibility: {accessibility_score:.1f}%")
            
        except Exception as e:
            test_result.update({
                'status': 'ERROR',
                'error': str(e)
            })
            print(f"❌ Framework accessibility test failed: {e}")
        
        return test_result
    
    def test_service_discovery(self) -> Dict[str, Any]:
        """Test AI service discovery capabilities"""
        print("🔍 Testing service discovery...")
        
        test_result = {
            'test_name': 'service_discovery',
            'start_time': datetime.now().isoformat(),
            'test_category': 'service_architecture'
        }
        
        try:
            # Test main framework service discovery
            main_services_result = subprocess.run([
                'git', 'ls-files', f'{self.framework_path}/.claude/ai-services/*.md'
            ], capture_output=True, text=True, timeout=30)
            
            main_services = []
            if main_services_result.returncode == 0 and main_services_result.stdout.strip():
                main_services = [f for f in main_services_result.stdout.strip().split('\n') if f]
            
            # Test testing framework service discovery
            testing_services_dir = Path("../../.claude/ai-services")
            testing_services = []
            if testing_services_dir.exists():
                testing_services = list(testing_services_dir.glob("*.md"))
            
            # Analyze service patterns
            main_tg_services = [s for s in main_services if 'tg-' in Path(s).stem]
            testing_tgt_services = [s for s in testing_services if 'tgt-' in s.stem]
            
            service_analysis = {
                'main_framework_total_services': len(main_services),
                'main_framework_tg_services': len(main_tg_services),
                'testing_framework_services': len(testing_services),
                'testing_framework_tgt_services': len(testing_tgt_services),
                'service_coverage_ratio': len(testing_services) / len(main_services) if main_services else 0,
                'tg_to_tgt_mapping_ratio': len(testing_tgt_services) / len(main_tg_services) if main_tg_services else 0
            }
            
            # Validate service discovery quality
            discovery_quality_score = min(100, service_analysis['service_coverage_ratio'] * 100)
            
            test_result.update({
                'status': 'PASSED' if discovery_quality_score >= 15 else 'FAILED',
                'service_analysis': service_analysis,
                'discovery_quality_score': discovery_quality_score,
                'git_command_result': {
                    'exit_code': main_services_result.returncode,
                    'services_found': len(main_services)
                }
            })
            
            print(f"✅ Service discovery: {len(main_services)} main services, {len(testing_services)} testing services")
            
        except Exception as e:
            test_result.update({
                'status': 'ERROR',
                'error': str(e)
            })
            print(f"❌ Service discovery test failed: {e}")
        
        return test_result
    
    def test_evidence_collection_capability(self) -> Dict[str, Any]:
        """Test evidence collection engine functionality"""
        print("🔍 Testing evidence collection capability...")
        
        test_result = {
            'test_name': 'evidence_collection_capability',
            'start_time': datetime.now().isoformat(),
            'test_category': 'evidence_collection'
        }
        
        try:
            # Test evidence collection with a simple command
            test_command = "echo 'Evidence collection test' && date && pwd"
            
            # Collect evidence
            evidence = self.evidence_collector.collect_framework_execution_evidence(
                test_command, timeout=30
            )
            
            # Validate evidence collection
            validation = self.evidence_collector.validate_evidence_quality(evidence)
            
            # Test evidence storage
            evidence_file = self.evidence_collector.store_evidence(evidence)
            evidence_file_exists = Path(evidence_file).exists()
            
            test_result.update({
                'status': 'PASSED' if validation['evidence_valid'] and evidence_file_exists else 'FAILED',
                'evidence_collection_result': {
                    'collection_status': evidence.get('collection_status'),
                    'collection_duration': evidence.get('collection_duration'),
                    'validation_score': validation.get('validation_score'),
                    'evidence_valid': validation.get('evidence_valid')
                },
                'evidence_storage': {
                    'file_created': evidence_file_exists,
                    'file_path': evidence_file
                }
            })
            
            print(f"✅ Evidence collection: {validation.get('validation_score', 0):.1f}% validation score")
            
        except Exception as e:
            test_result.update({
                'status': 'ERROR',
                'error': str(e)
            })
            print(f"❌ Evidence collection test failed: {e}")
        
        return test_result
    
    def test_html_violation_detection(self) -> Dict[str, Any]:
        """Test HTML violation detection capability"""
        print("🔍 Testing HTML violation detection...")
        
        test_result = {
            'test_name': 'html_violation_detection',
            'start_time': datetime.now().isoformat(),
            'test_category': 'quality_validation'
        }
        
        try:
            # Create test content with known HTML violations
            test_content_clean = "This is clean content without HTML."
            test_content_dirty = """
            This has HTML violations:
            <br>
            <div>content</div>
            &nbsp;
            <code>example</code>
            This should be detected.
            """
            
            # Test HTML detection on clean content
            clean_analysis = self.evidence_collector.analyze_html_violations(test_content_clean)
            
            # Test HTML detection on dirty content
            dirty_analysis = self.evidence_collector.analyze_html_violations(test_content_dirty)
            
            # Validate detection accuracy
            detection_accuracy = {
                'clean_content_correctly_identified': clean_analysis['html_clean'],
                'dirty_content_correctly_identified': not dirty_analysis['html_clean'],
                'violation_count_accurate': dirty_analysis['total_violations'] > 0,
                'pattern_detection_working': len(dirty_analysis['violation_patterns']) > 0
            }
            
            detection_score = sum(detection_accuracy.values()) / len(detection_accuracy) * 100
            
            test_result.update({
                'status': 'PASSED' if detection_score >= 100 else 'FAILED',
                'detection_results': {
                    'clean_content_analysis': clean_analysis,
                    'dirty_content_analysis': dirty_analysis,
                    'detection_accuracy': detection_accuracy,
                    'detection_score': detection_score
                }
            })
            
            print(f"✅ HTML violation detection: {detection_score:.1f}% accuracy")
            
        except Exception as e:
            test_result.update({
                'status': 'ERROR',
                'error': str(e)
            })
            print(f"❌ HTML violation detection test failed: {e}")
        
        return test_result
    
    def test_quality_scoring_engine(self) -> Dict[str, Any]:
        """Test quality scoring engine functionality"""
        print("🔍 Testing quality scoring engine...")
        
        test_result = {
            'test_name': 'quality_scoring_engine',
            'start_time': datetime.now().isoformat(),
            'test_category': 'quality_validation'
        }
        
        try:
            # Create test quality evidence
            high_quality_evidence = {
                'html_violation_analysis': {'html_clean': True, 'total_violations': 0},
                'citation_analysis': {'total_citations': 10},
                'error_pattern_analysis': {'error_free': True, 'total_error_indicators': 0},
                'output_structure_analysis': {
                    'structure_quality': {'structure_quality_score': 95}
                }
            }
            
            low_quality_evidence = {
                'html_violation_analysis': {'html_clean': False, 'total_violations': 15},
                'citation_analysis': {'total_citations': 2},
                'error_pattern_analysis': {'error_free': False, 'total_error_indicators': 8},
                'output_structure_analysis': {
                    'structure_quality': {'structure_quality_score': 30}
                }
            }
            
            # Test quality score calculation
            high_quality_score = self.evidence_collector.calculate_quality_score(high_quality_evidence)
            low_quality_score = self.evidence_collector.calculate_quality_score(low_quality_evidence)
            
            # Validate scoring accuracy
            scoring_validation = {
                'high_quality_scored_high': high_quality_score >= 80,
                'low_quality_scored_low': low_quality_score <= 50,
                'score_differentiation': abs(high_quality_score - low_quality_score) >= 30,
                'scores_in_valid_range': 0 <= high_quality_score <= 100 and 0 <= low_quality_score <= 100
            }
            
            scoring_accuracy = sum(scoring_validation.values()) / len(scoring_validation) * 100
            
            test_result.update({
                'status': 'PASSED' if scoring_accuracy >= 100 else 'FAILED',
                'scoring_results': {
                    'high_quality_score': high_quality_score,
                    'low_quality_score': low_quality_score,
                    'scoring_validation': scoring_validation,
                    'scoring_accuracy': scoring_accuracy
                }
            })
            
            print(f"✅ Quality scoring: High={high_quality_score:.1f}, Low={low_quality_score:.1f}")
            
        except Exception as e:
            test_result.update({
                'status': 'ERROR',
                'error': str(e)
            })
            print(f"❌ Quality scoring test failed: {e}")
        
        return test_result
    
    def test_performance_measurement(self) -> Dict[str, Any]:
        """Test performance measurement capabilities"""
        print("🔍 Testing performance measurement...")
        
        test_result = {
            'test_name': 'performance_measurement',
            'start_time': datetime.now().isoformat(),
            'test_category': 'performance'
        }
        
        try:
            # Test performance measurement with timed operations
            operations = [
                ("echo 'Fast operation'", 0.1),
                ("sleep 0.5 && echo 'Medium operation'", 0.8),
                ("echo 'Another fast operation'", 0.1)
            ]
            
            performance_results = []
            
            for command, expected_max_time in operations:
                start_time = time.time()
                
                # Execute command and measure time
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True, timeout=5
                )
                
                execution_time = time.time() - start_time
                
                performance_results.append({
                    'command': command,
                    'execution_time': execution_time,
                    'expected_max_time': expected_max_time,
                    'within_expected_time': execution_time <= expected_max_time,
                    'success': result.returncode == 0
                })
            
            # Analyze performance measurement accuracy
            timing_accuracy = sum(1 for r in performance_results if r['within_expected_time']) / len(performance_results) * 100
            execution_success_rate = sum(1 for r in performance_results if r['success']) / len(performance_results) * 100
            
            test_result.update({
                'status': 'PASSED' if timing_accuracy >= 60 and execution_success_rate >= 100 else 'FAILED',
                'performance_results': performance_results,
                'timing_accuracy': timing_accuracy,
                'execution_success_rate': execution_success_rate
            })
            
            print(f"✅ Performance measurement: {timing_accuracy:.1f}% timing accuracy")
            
        except Exception as e:
            test_result.update({
                'status': 'ERROR',
                'error': str(e)
            })
            print(f"❌ Performance measurement test failed: {e}")
        
        return test_result
    
    def run_comprehensive_functional_test_suite(self) -> Dict[str, Any]:
        """Run comprehensive functional test suite"""
        print("🧪 Comprehensive Functional Test Suite")
        print("=" * 50)
        
        suite_start_time = time.time()
        
        suite_results = {
            'test_suite': 'comprehensive_functional_tests',
            'session_id': self.test_session_id,
            'start_time': datetime.now().isoformat(),
            'tests': {}
        }
        
        # Define test methods
        test_methods = [
            self.test_framework_accessibility,
            self.test_service_discovery,
            self.test_evidence_collection_capability,
            self.test_html_violation_detection,
            self.test_quality_scoring_engine,
            self.test_performance_measurement
        ]
        
        # Run all tests
        for test_method in test_methods:
            try:
                test_result = test_method()
                suite_results['tests'][test_result['test_name']] = test_result
            except Exception as e:
                print(f"❌ Test {test_method.__name__} failed with exception: {e}")
                suite_results['tests'][test_method.__name__] = {
                    'status': 'EXCEPTION',
                    'error': str(e),
                    'test_name': test_method.__name__
                }
        
        # Calculate suite summary
        total_tests = len(suite_results['tests'])
        passed_tests = sum(1 for test in suite_results['tests'].values() if test.get('status') == 'PASSED')
        failed_tests = sum(1 for test in suite_results['tests'].values() if test.get('status') == 'FAILED')
        error_tests = sum(1 for test in suite_results['tests'].values() if test.get('status') in ['ERROR', 'EXCEPTION'])
        
        suite_duration = time.time() - suite_start_time
        
        suite_results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'error_tests': error_tests,
            'success_rate': (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
            'suite_duration': suite_duration,
            'end_time': datetime.now().isoformat()
        }
        
        # Display results
        print("\n" + "=" * 50)
        print("🎯 Functional Test Suite Results:")
        print(f"✅ Passed: {passed_tests}/{total_tests}")
        print(f"❌ Failed: {failed_tests}/{total_tests}")
        print(f"⚠️  Errors: {error_tests}/{total_tests}")
        print(f"📊 Success Rate: {suite_results['summary']['success_rate']:.1f}%")
        print(f"⏱️ Duration: {suite_duration:.2f}s")
        
        # Store results
        self.store_test_results(suite_results)
        
        return suite_results
    
    def store_test_results(self, results: Dict[str, Any]) -> str:
        """Store test results to file"""
        results_dir = Path("../evidence")
        results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"functional_test_results_{self.test_session_id}_{timestamp}.json"
        filepath = results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📄 Test results saved: {filepath}")
        return str(filepath)


def main():
    """Main execution function"""
    print("🧪 Functional Test Suite - Implementation First")
    print("Testing framework components with real validation")
    print("-" * 50)
    
    test_suite = FunctionalTestSuite()
    results = test_suite.run_comprehensive_functional_test_suite()
    
    # Return exit code based on results
    if results['summary']['failed_tests'] > 0 or results['summary']['error_tests'] > 0:
        print("\n⚠️ Some tests failed - see results for details")
        return 1
    else:
        print("\n🎉 All functional tests passed!")
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)