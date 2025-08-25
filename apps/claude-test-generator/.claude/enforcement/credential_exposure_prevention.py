#!/usr/bin/env python3
"""
Credential Exposure Prevention System
=====================================

Critical security component to prevent credential exposure in generated test plans.
This system enforces zero-tolerance for real credentials, environment-specific data,
and non-templated content in all framework outputs.

Framework Security Requirements:
- Zero credential exposure with real-time masking
- Template enforcement with placeholder validation
- Environment-agnostic content generation
- Pre-delivery security scanning

"""

import re
import json
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class CredentialExposurePreventionSystem:
    """
    Framework security enforcement for credential exposure prevention.
    
    Implements zero-tolerance policy for:
    - Real credentials in test plans
    - Environment-specific hardcoding
    - Non-placeholder content
    """
    
    def __init__(self):
        """Initialize security patterns and enforcement rules."""
        
        # Credential Detection Patterns  
        self.credential_patterns = [
            # Password patterns (exclude JSON patches and placeholders)
            r'-p\s+(?!<|\'|\{)[^\s]*',  # -p password (not placeholder, quote, or JSON)
            r'kubeadmin/[^<\s][^\s]*',  # kubeadmin/password
            
            # URL patterns with specific domains (exclude examples)
            r'https://[a-zA-Z0-9.-]+\.qe\.red-chesterfield\.com',  # Specific QE domains
            r'https://console-openshift-console\.apps\.(?!cluster\.example\.com)[a-zA-Z0-9.-]+\.com',  # Specific console URLs (not examples)
            
            # Environment-specific identifiers
            r'mist\d+-\d+',  # mist10-0 style environments
            r'Gz7oJ-[A-Za-z0-9-]+',  # Specific credential patterns
            
            # Real IP addresses (not examples)
            r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        ]
        
        # Required Placeholder Patterns
        self.required_placeholders = [
            '<CLUSTER_CONSOLE_URL>',
            '<CLUSTER_ADMIN_USER>',
            '<CLUSTER_ADMIN_PASSWORD>',
            '<ACM_VERSION>',
        ]
        
        # Template Validation Rules
        self.template_rules = {
            'login_commands': r'oc login <CLUSTER_CONSOLE_URL> -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>',
            'url_format': r'<[A-Z_]+_URL>',
            'credential_format': r'<[A-Z_]+_(USER|PASSWORD|TOKEN)>',
            'version_format': r'<[A-Z_]+_VERSION>',
        }
        
        self.enforcement_log = []
        
    def scan_content(self, content: str, file_path: str) -> Dict:
        """
        Comprehensive security scan of content for credential exposure.
        
        Args:
            content: Content to scan
            file_path: Path to file being scanned
            
        Returns:
            Dict with scan results and violations
        """
        scan_result = {
            'file_path': file_path,
            'timestamp': datetime.now().isoformat(),
            'violations': [],
            'security_score': 100,
            'passed': True,
            'required_fixes': []
        }
        
        # Scan for credential patterns
        credential_violations = self._detect_credentials(content)
        scan_result['violations'].extend(credential_violations)
        
        # Validate placeholder usage
        placeholder_violations = self._validate_placeholders(content)
        scan_result['violations'].extend(placeholder_violations)
        
        # Check template compliance
        template_violations = self._validate_templates(content)
        scan_result['violations'].extend(template_violations)
        
        # Calculate security score
        violation_count = len(scan_result['violations'])
        scan_result['security_score'] = max(0, 100 - (violation_count * 25))
        scan_result['passed'] = violation_count == 0
        
        # Generate required fixes
        if violation_count > 0:
            scan_result['required_fixes'] = self._generate_fixes(scan_result['violations'])
        
        return scan_result
    
    def _detect_credentials(self, content: str) -> List[Dict]:
        """Detect credential exposure patterns."""
        violations = []
        
        for pattern in self.credential_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                violations.append({
                    'type': 'CREDENTIAL_EXPOSURE',
                    'severity': 'CRITICAL',
                    'pattern': pattern,
                    'match': match.group(0),
                    'position': match.span(),
                    'description': f'Real credential or environment-specific data detected: {match.group(0)}'
                })
        
        return violations
    
    def _validate_placeholders(self, content: str) -> List[Dict]:
        """Validate that required placeholders are used."""
        violations = []
        
        # Check for missing placeholders in login commands
        if 'oc login' in content:
            for placeholder in self.required_placeholders:
                if placeholder not in content:
                    violations.append({
                        'type': 'MISSING_PLACEHOLDER',
                        'severity': 'HIGH',
                        'placeholder': placeholder,
                        'description': f'Required placeholder {placeholder} not found in login commands'
                    })
        
        return violations
    
    def _validate_templates(self, content: str) -> List[Dict]:
        """Validate template format compliance."""
        violations = []
        
        # Check login command format
        login_pattern = r'oc login [^<\s]+'
        if re.search(login_pattern, content):
            violations.append({
                'type': 'TEMPLATE_VIOLATION',
                'severity': 'HIGH',
                'description': 'Login command contains non-placeholder values'
            })
        
        return violations
    
    def _generate_fixes(self, violations: List[Dict]) -> List[str]:
        """Generate required fixes for violations."""
        fixes = []
        
        for violation in violations:
            if violation['type'] == 'CREDENTIAL_EXPOSURE':
                if 'password' in violation['match'].lower():
                    fixes.append('Replace real password with <CLUSTER_ADMIN_PASSWORD>')
                elif 'http' in violation['match'].lower():
                    fixes.append('Replace real URL with <CLUSTER_CONSOLE_URL>')
                else:
                    fixes.append(f"Replace '{violation['match']}' with appropriate placeholder")
            
            elif violation['type'] == 'MISSING_PLACEHOLDER':
                fixes.append(f"Add {violation['placeholder']} to content")
            
            elif violation['type'] == 'TEMPLATE_VIOLATION':
                fixes.append('Use placeholder format: oc login <CLUSTER_CONSOLE_URL> -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>')
        
        return list(set(fixes))  # Remove duplicates
    
    def enforce_security(self, file_path: str) -> bool:
        """
        Enforce security on a generated file.
        
        Args:
            file_path: Path to file to enforce security on
            
        Returns:
            bool: True if security passed, False if violations found
        """
        if not os.path.exists(file_path):
            return False
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        scan_result = self.scan_content(content, file_path)
        
        self.enforcement_log.append(scan_result)
        
        if not scan_result['passed']:
            self._report_security_violations(scan_result)
            return False
        
        return True
    
    def _report_security_violations(self, scan_result: Dict):
        """Report security violations for remediation."""
        print("\n🚨 CRITICAL SECURITY VIOLATION DETECTED 🚨")
        print(f"File: {scan_result['file_path']}")
        print(f"Security Score: {scan_result['security_score']}/100")
        print(f"Violations: {len(scan_result['violations'])}")
        print("\nViolations Found:")
        
        for i, violation in enumerate(scan_result['violations'], 1):
            print(f"{i}. {violation['severity']}: {violation['description']}")
        
        print("\nRequired Fixes:")
        for i, fix in enumerate(scan_result['required_fixes'], 1):
            print(f"{i}. {fix}")
        
        print("\n⚠️ FRAMEWORK ENFORCEMENT: Test plan delivery blocked until security violations are resolved.")
    
    def get_enforcement_report(self) -> Dict:
        """Get comprehensive enforcement report."""
        total_scans = len(self.enforcement_log)
        passed_scans = sum(1 for scan in self.enforcement_log if scan['passed'])
        
        return {
            'total_scans': total_scans,
            'passed_scans': passed_scans,
            'failed_scans': total_scans - passed_scans,
            'success_rate': (passed_scans / total_scans * 100) if total_scans > 0 else 0,
            'enforcement_log': self.enforcement_log,
            'last_scan': self.enforcement_log[-1] if self.enforcement_log else None
        }

class PatternExtensionSecurityWrapper:
    """
    Security wrapper for Pattern Extension Service to enforce template generation.
    """
    
    def __init__(self):
        self.security_system = CredentialExposurePreventionSystem()
    
    def secure_test_plan_generation(self, generated_content: str, output_path: str) -> Tuple[bool, str]:
        """
        Apply security enforcement to generated test plan content.
        
        Args:
            generated_content: The generated test plan content
            output_path: Path where content will be written
            
        Returns:
            Tuple[bool, str]: (success, sanitized_content or error_message)
        """
        # Pre-generation security scan
        scan_result = self.security_system.scan_content(generated_content, output_path)
        
        if scan_result['passed']:
            return True, generated_content
        
        # Attempt automatic sanitization
        sanitized_content = self._auto_sanitize(generated_content, scan_result['violations'])
        
        # Re-scan sanitized content
        sanitized_scan = self.security_system.scan_content(sanitized_content, output_path)
        
        if sanitized_scan['passed']:
            return True, sanitized_content
        else:
            error_message = f"Security enforcement failed: {len(sanitized_scan['violations'])} violations remain after auto-sanitization"
            return False, error_message
    
    def _auto_sanitize(self, content: str, violations: List[Dict]) -> str:
        """
        Attempt automatic sanitization of security violations.
        """
        sanitized = content
        
        # Auto-fix common credential patterns
        sanitized = re.sub(r'-p\s+[^\s<][^\s]*', '-p <CLUSTER_ADMIN_PASSWORD>', sanitized)
        sanitized = re.sub(r'kubeadmin/[^<\s][^\s]*', '<CLUSTER_ADMIN_USER>/<CLUSTER_ADMIN_PASSWORD>', sanitized)
        sanitized = re.sub(r'https://[a-zA-Z0-9.-]+\.qe\.red-chesterfield\.com[^\s]*', '<CLUSTER_CONSOLE_URL>', sanitized)
        sanitized = re.sub(r'https://console-openshift-console\.apps\.[a-zA-Z0-9.-]+\.com[^\s]*', '<CLUSTER_CONSOLE_URL>', sanitized)
        
        return sanitized

def enforce_framework_security(file_path: str) -> bool:
    """
    Main security enforcement entry point for framework integration.
    
    Args:
        file_path: Path to file requiring security enforcement
        
    Returns:
        bool: True if security enforcement passed
    """
    security_system = CredentialExposurePreventionSystem()
    return security_system.enforce_security(file_path)

if __name__ == "__main__":
    # Test the security system
    security_system = CredentialExposurePreventionSystem()
    
    # Test content with violations
    test_content = """
    oc login https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com -u kubeadmin -p Gz7oJ-IHZgq-5MIQ9-Kdhid
    """
    
    result = security_system.scan_content(test_content, "test.md")
    print(json.dumps(result, indent=2))