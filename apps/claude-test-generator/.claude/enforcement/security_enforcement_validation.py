#!/usr/bin/env python3
"""
Security Enforcement Validation System
======================================

Comprehensive validation system to test framework security enforcement
and ensure credential exposure prevention works correctly.

This validation system:
1. Tests security detection capabilities
2. Validates auto-sanitization functions
3. Ensures template compliance enforcement
4. Validates framework integration points

Test Scenarios:
- Credential exposure detection
- Environment-specific data detection
- Auto-sanitization validation
- Template compliance checking
- Integration hook testing

"""

import os
import sys
import json
import tempfile
from typing import Dict, List, Tuple
from datetime import datetime

# Import security enforcement components
import sys
import os
sys.path.append(os.path.dirname(__file__))

from credential_exposure_prevention import (
    CredentialExposurePreventionSystem,
    PatternExtensionSecurityWrapper
)
from pattern_extension_security_integration import (
    PatternExtensionSecurityIntegration,
    FrameworkSecurityHook
)

class SecurityEnforcementValidationSuite:
    """
    Comprehensive validation suite for security enforcement system.
    """
    
    def __init__(self):
        """Initialize validation components."""
        self.security_system = CredentialExposurePreventionSystem()
        self.security_wrapper = PatternExtensionSecurityWrapper()
        self.security_integration = PatternExtensionSecurityIntegration()
        self.framework_hook = FrameworkSecurityHook()
        
        self.validation_results = []
        
    def run_comprehensive_validation(self) -> Dict:
        """
        Run comprehensive validation of security enforcement system.
        
        Returns:
            Dict with complete validation results
        """
        print("🔒 Starting Security Enforcement Validation Suite...")
        print("=" * 60)
        
        validation_summary = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_results': [],
            'overall_status': 'PENDING'
        }
        
        # Test 1: Credential Detection Validation
        print("\n1. Testing Credential Detection...")
        credential_test = self._test_credential_detection()
        validation_summary['test_results'].append(credential_test)
        
        # Test 2: Auto-Sanitization Validation
        print("\n2. Testing Auto-Sanitization...")
        sanitization_test = self._test_auto_sanitization()
        validation_summary['test_results'].append(sanitization_test)
        
        # Test 3: Template Compliance Validation
        print("\n3. Testing Template Compliance...")
        template_test = self._test_template_compliance()
        validation_summary['test_results'].append(template_test)
        
        # Test 4: Framework Integration Validation
        print("\n4. Testing Framework Integration...")
        integration_test = self._test_framework_integration()
        validation_summary['test_results'].append(integration_test)
        
        # Test 5: Real File Validation
        print("\n5. Testing Real File Security Enforcement...")
        file_test = self._test_real_file_enforcement()
        validation_summary['test_results'].append(file_test)
        
        # Calculate summary
        validation_summary['total_tests'] = len(validation_summary['test_results'])
        validation_summary['passed_tests'] = sum(1 for test in validation_summary['test_results'] if test['passed'])
        validation_summary['failed_tests'] = validation_summary['total_tests'] - validation_summary['passed_tests']
        validation_summary['overall_status'] = 'PASSED' if validation_summary['failed_tests'] == 0 else 'FAILED'
        
        # Print summary
        self._print_validation_summary(validation_summary)
        
        return validation_summary
    
    def _test_credential_detection(self) -> Dict:
        """Test credential detection capabilities."""
        test_result = {
            'test_name': 'Credential Detection',
            'passed': False,
            'details': [],
            'violations_detected': 0
        }
        
        # Test content with various credential patterns
        test_cases = [
            {
                'name': 'Real Password in Command',
                'content': 'oc login https://console.apps.cluster.com -u kubeadmin -p Gz7oJ-IHZgq-5MIQ9-Kdhid',
                'should_detect': True
            },
            {
                'name': 'Environment-Specific URL',
                'content': 'oc login https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com',
                'should_detect': True
            },
            {
                'name': 'Proper Placeholder Usage',
                'content': 'oc login <CLUSTER_CONSOLE_URL> -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>',
                'should_detect': False
            },
            {
                'name': 'Mixed Real and Placeholder',
                'content': 'oc login <CLUSTER_CONSOLE_URL> -u kubeadmin -p realpassword123',
                'should_detect': True
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            scan_result = self.security_system.scan_content(test_case['content'], 'test.md')
            violations_found = len(scan_result['violations']) > 0
            
            case_passed = violations_found == test_case['should_detect']
            
            test_result['details'].append({
                'case_name': test_case['name'],
                'expected_detection': test_case['should_detect'],
                'actual_detection': violations_found,
                'violations_count': len(scan_result['violations']),
                'passed': case_passed
            })
            
            if not case_passed:
                all_passed = False
            
            test_result['violations_detected'] += len(scan_result['violations'])
        
        test_result['passed'] = all_passed
        
        # Print details
        for detail in test_result['details']:
            status = "✅" if detail['passed'] else "❌"
            print(f"   {status} {detail['case_name']}: Expected detection={detail['expected_detection']}, Got={detail['actual_detection']}")
        
        return test_result
    
    def _test_auto_sanitization(self) -> Dict:
        """Test auto-sanitization capabilities."""
        test_result = {
            'test_name': 'Auto-Sanitization',
            'passed': False,
            'details': []
        }
        
        # Test content that should be auto-sanitized
        dirty_content = """
        # Test Plan
        oc login https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com -u kubeadmin -p Gz7oJ-IHZgq-5MIQ9-Kdhid
        
        Environment: mist10-0.qe.red-chesterfield.com
        Credentials: kubeadmin/Gz7oJ-IHZgq-5MIQ9-Kdhid
        """
        
        # Test sanitization
        success, sanitized_content = self.security_wrapper.secure_test_plan_generation(dirty_content, 'test.md')
        
        if success:
            # Verify sanitized content doesn't contain violations
            post_scan = self.security_system.scan_content(sanitized_content, 'test.md')
            sanitization_success = len(post_scan['violations']) == 0
            
            test_result['details'].append({
                'original_violations': 'Multiple credential exposures',
                'sanitization_applied': success,
                'post_sanitization_violations': len(post_scan['violations']),
                'sanitization_effective': sanitization_success
            })
            
            test_result['passed'] = sanitization_success
            print(f"   ✅ Auto-sanitization: {len(post_scan['violations'])} violations remaining")
        else:
            test_result['details'].append({
                'sanitization_failed': True,
                'error': sanitized_content
            })
            test_result['passed'] = False
            print(f"   ❌ Auto-sanitization failed: {sanitized_content}")
        
        return test_result
    
    def _test_template_compliance(self) -> Dict:
        """Test template compliance enforcement."""
        test_result = {
            'test_name': 'Template Compliance',
            'passed': False,
            'details': []
        }
        
        # Test compliant template
        compliant_template = """
        # Test Plan: ACM-22079
        
        ## 🔧 Environment Setup Instructions
        
        **Before running these tests**, replace the following placeholders:
        
        | Placeholder | Description |
        |-------------|-------------|
        | `<CLUSTER_CONSOLE_URL>` | Your OpenShift console URL |
        | `<CLUSTER_ADMIN_USER>` | Cluster admin username |
        | `<CLUSTER_ADMIN_PASSWORD>` | Cluster admin password |
        
        **Security Note**: Never commit real credentials to version control.
        
        ## Test Case 1
        oc login <CLUSTER_CONSOLE_URL> -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>
        """
        
        # Test non-compliant template
        non_compliant_template = """
        # Test Plan: ACM-22079
        
        oc login https://real-cluster.com -u admin -p password123
        """
        
        # Test compliance
        compliant_passed, compliant_report = self.security_integration.enforce_template_compliance(compliant_template)
        non_compliant_passed, non_compliant_report = self.security_integration.enforce_template_compliance(non_compliant_template)
        
        test_result['details'] = [
            {
                'template_type': 'compliant',
                'passed': compliant_passed,
                'report': compliant_report
            },
            {
                'template_type': 'non_compliant',
                'passed': not non_compliant_passed,  # Should fail compliance
                'report': non_compliant_report
            }
        ]
        
        test_result['passed'] = compliant_passed and not non_compliant_passed
        
        print(f"   ✅ Compliant template: {'PASSED' if compliant_passed else 'FAILED'}")
        print(f"   ✅ Non-compliant template: {'REJECTED' if not non_compliant_passed else 'INCORRECTLY ACCEPTED'}")
        
        return test_result
    
    def _test_framework_integration(self) -> Dict:
        """Test framework integration hooks."""
        test_result = {
            'test_name': 'Framework Integration',
            'passed': False,
            'details': []
        }
        
        # Test pre-generation hook with clean intelligence
        clean_intelligence = {
            'jira_ticket': 'ACM-22079',
            'feature_name': 'ClusterCurator Digest-Based Upgrades',
            'agent_results': {
                'agent_a': 'Analysis complete',
                'agent_b': 'Documentation analysis complete'
            }
        }
        
        # Test pre-generation hook with dirty intelligence
        dirty_intelligence = {
            'jira_ticket': 'ACM-22079',
            'credentials': 'kubeadmin/Gz7oJ-IHZgq-5MIQ9-Kdhid',
            'environment': 'mist10-0.qe.red-chesterfield.com'
        }
        
        # Test hooks
        clean_passed = self.framework_hook.pre_generation_hook(clean_intelligence)
        dirty_passed = self.framework_hook.pre_generation_hook(dirty_intelligence)
        
        test_result['details'] = [
            {
                'hook_type': 'pre_generation_clean',
                'passed': clean_passed,
                'expected': True
            },
            {
                'hook_type': 'pre_generation_dirty',
                'passed': not dirty_passed,  # Should be blocked
                'expected': False
            }
        ]
        
        test_result['passed'] = clean_passed and not dirty_passed
        
        print(f"   ✅ Clean intelligence: {'APPROVED' if clean_passed else 'INCORRECTLY BLOCKED'}")
        print(f"   ✅ Dirty intelligence: {'BLOCKED' if not dirty_passed else 'INCORRECTLY APPROVED'}")
        
        return test_result
    
    def _test_real_file_enforcement(self) -> Dict:
        """Test security enforcement on real files."""
        test_result = {
            'test_name': 'Real File Enforcement',
            'passed': False,
            'details': []
        }
        
        # Create temporary files for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as secure_file:
            secure_content = """
            # Test Plan
            oc login <CLUSTER_CONSOLE_URL> -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>
            """
            secure_file.write(secure_content)
            secure_file_path = secure_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as insecure_file:
            insecure_content = """
            # Test Plan
            oc login https://console.apps.mist10-0.qe.red-chesterfield.com -u kubeadmin -p Gz7oJ-IHZgq-5MIQ9-Kdhid
            """
            insecure_file.write(insecure_content)
            insecure_file_path = insecure_file.name
        
        try:
            # Test enforcement on files
            secure_passed = self.security_system.enforce_security(secure_file_path)
            insecure_passed = self.security_system.enforce_security(insecure_file_path)
            
            test_result['details'] = [
                {
                    'file_type': 'secure',
                    'enforcement_passed': secure_passed,
                    'expected': True
                },
                {
                    'file_type': 'insecure',
                    'enforcement_passed': insecure_passed,
                    'expected': False
                }
            ]
            
            test_result['passed'] = secure_passed and not insecure_passed
            
            print(f"   ✅ Secure file: {'APPROVED' if secure_passed else 'INCORRECTLY BLOCKED'}")
            print(f"   ✅ Insecure file: {'BLOCKED' if not insecure_passed else 'INCORRECTLY APPROVED'}")
            
        finally:
            # Clean up temporary files
            os.unlink(secure_file_path)
            os.unlink(insecure_file_path)
        
        return test_result
    
    def _print_validation_summary(self, summary: Dict):
        """Print comprehensive validation summary."""
        print("\n" + "=" * 60)
        print("🔒 SECURITY ENFORCEMENT VALIDATION SUMMARY")
        print("=" * 60)
        
        print(f"📊 Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}")
        print(f"🎯 Success Rate: {(summary['passed_tests']/summary['total_tests']*100):.1f}%")
        print(f"🏆 Overall Status: {summary['overall_status']}")
        
        if summary['failed_tests'] > 0:
            print("\n❌ FAILED TESTS:")
            for test in summary['test_results']:
                if not test['passed']:
                    print(f"   - {test['test_name']}")
        
        print("\n" + "=" * 60)
        
        if summary['overall_status'] == 'PASSED':
            print("✅ SECURITY ENFORCEMENT SYSTEM VALIDATION SUCCESSFUL")
            print("🔒 Framework security is properly enforced")
        else:
            print("❌ SECURITY ENFORCEMENT SYSTEM VALIDATION FAILED")
            print("🚨 Framework security enforcement needs fixes")
        
        print("=" * 60)

def validate_security_enforcement() -> bool:
    """
    Main validation function for framework security enforcement.
    
    Returns:
        bool: True if all security enforcement validation passes
    """
    validation_suite = SecurityEnforcementValidationSuite()
    results = validation_suite.run_comprehensive_validation()
    
    return results['overall_status'] == 'PASSED'

if __name__ == "__main__":
    success = validate_security_enforcement()
    exit(0 if success else 1)