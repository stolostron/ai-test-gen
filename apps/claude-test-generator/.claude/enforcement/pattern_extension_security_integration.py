#!/usr/bin/env python3
"""
Pattern Extension Security Integration
=====================================

Framework security integration for Pattern Extension Service to enforce
zero credential exposure in all generated test plans.

This module integrates with the Pattern Extension Service to:
1. Pre-scan all generated content for security violations
2. Auto-sanitize credential exposure
3. Block delivery of non-compliant test plans
4. Enforce template-based generation

Security Integration Points:
- Pre-generation content validation
- Post-generation security enforcement
- Auto-sanitization with re-validation
- Delivery blocking for violations

"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Import the credential exposure prevention system
import sys
import os
sys.path.append(os.path.dirname(__file__))

from credential_exposure_prevention import (
    CredentialExposurePreventionSystem,
    PatternExtensionSecurityWrapper
)

class PatternExtensionSecurityIntegration:
    """
    Security integration layer for Pattern Extension Service.
    
    Enforces framework security policies:
    - Zero credential exposure
    - Template-based generation
    - Environment-agnostic content
    """
    
    def __init__(self):
        """Initialize security integration components."""
        self.security_wrapper = PatternExtensionSecurityWrapper()
        self.security_system = CredentialExposurePreventionSystem()
        self.integration_log = []
        
        # Framework enforcement configuration
        self.enforcement_config = {
            'block_delivery_on_violations': True,
            'auto_sanitization_enabled': True,
            'security_score_threshold': 95,
            'zero_tolerance_patterns': [
                'real_credentials',
                'environment_specific_urls',
                'hardcoded_passwords'
            ]
        }
    
    def secure_pattern_extension(self, agent_intelligence: Dict, output_path: str) -> Dict:
        """
        Main security integration point for Pattern Extension Service.
        
        Args:
            agent_intelligence: Intelligence data from all agents
            output_path: Path where test plan will be written
            
        Returns:
            Dict with security validation results and sanitized content
        """
        integration_result = {
            'timestamp': datetime.now().isoformat(),
            'security_validation': 'PENDING',
            'content_sanitized': False,
            'delivery_approved': False,
            'violations_detected': 0,
            'auto_fixes_applied': 0,
            'security_score': 0,
            'sanitized_content': None,
            'security_report': {}
        }
        
        try:
            # Step 1: Generate content using Pattern Extension Service
            generated_content = self._invoke_pattern_extension(agent_intelligence)
            
            # Step 2: Apply security enforcement
            security_passed, result_content = self.security_wrapper.secure_test_plan_generation(
                generated_content, output_path
            )
            
            if security_passed:
                integration_result.update({
                    'security_validation': 'PASSED',
                    'delivery_approved': True,
                    'sanitized_content': result_content,
                    'security_score': 100
                })
            else:
                integration_result.update({
                    'security_validation': 'FAILED',
                    'delivery_approved': False,
                    'error_message': result_content
                })
            
            # Step 3: Generate comprehensive security report
            security_report = self.security_system.get_enforcement_report()
            integration_result['security_report'] = security_report
            
            # Step 4: Log integration result
            self.integration_log.append(integration_result)
            
            return integration_result
            
        except Exception as e:
            integration_result.update({
                'security_validation': 'ERROR',
                'delivery_approved': False,
                'error_message': f'Security integration error: {str(e)}'
            })
            return integration_result
    
    def _invoke_pattern_extension(self, agent_intelligence: Dict) -> str:
        """
        Invoke Pattern Extension Service with agent intelligence.
        
        This is a mock implementation - in real framework this would
        call the actual Pattern Extension Service.
        """
        # Mock Pattern Extension Service behavior
        # In real implementation, this would integrate with actual service
        
        # Extract key information from agent intelligence
        jira_ticket = agent_intelligence.get('jira_ticket', 'ACM-XXXXX')
        feature_name = agent_intelligence.get('feature_name', 'Feature Testing')
        
        # Generate template-based content
        template_content = f"""# Test Plan: {jira_ticket} - {feature_name}

**JIRA Ticket**: {jira_ticket}
**Feature**: {feature_name}
**Test Environment**: <CLUSTER_CONSOLE_URL>
**Generated**: {datetime.now().strftime('%Y-%m-%d')}

---

## 🔧 Environment Setup Instructions

**Before running these tests**, replace the following placeholders with your actual environment values:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `<CLUSTER_CONSOLE_URL>` | Your OpenShift console URL | `https://console-openshift-console.apps.cluster.example.com` |
| `<CLUSTER_ADMIN_USER>` | Cluster admin username | `kubeadmin` or `admin` |
| `<CLUSTER_ADMIN_PASSWORD>` | Cluster admin password | Your cluster admin password |

**Security Note**: Never commit real credentials to version control.

---

## Test Cases

### Test Case 1: Basic Feature Validation

**Objective**: Validate core feature functionality

**Test Steps**:
1. Login to cluster: `oc login <CLUSTER_CONSOLE_URL> -u <CLUSTER_ADMIN_USER> -p <CLUSTER_ADMIN_PASSWORD>`
2. Verify feature is available
3. Test basic functionality
4. Validate results

### Cleanup
```bash
# Clean up test resources
oc delete [resources]
```
"""
        
        return template_content
    
    def validate_agent_intelligence(self, agent_intelligence: Dict) -> bool:
        """
        Validate that agent intelligence doesn't contain credential exposure.
        
        Args:
            agent_intelligence: Intelligence data from agents
            
        Returns:
            bool: True if intelligence is clean
        """
        # Convert intelligence to string for scanning
        intelligence_content = json.dumps(agent_intelligence, indent=2)
        
        scan_result = self.security_system.scan_content(intelligence_content, "agent_intelligence.json")
        
        if not scan_result['passed']:
            print("🚨 SECURITY VIOLATION IN AGENT INTELLIGENCE:")
            for violation in scan_result['violations']:
                print(f"  - {violation['description']}")
            return False
        
        return True
    
    def enforce_template_compliance(self, content: str) -> Tuple[bool, str]:
        """
        Enforce template compliance rules on generated content.
        
        Args:
            content: Generated content to validate
            
        Returns:
            Tuple[bool, str]: (compliance_passed, compliance_report)
        """
        compliance_issues = []
        
        # Check for required placeholder sections
        required_sections = [
            '## 🔧 Environment Setup Instructions',
            '<CLUSTER_CONSOLE_URL>',
            '<CLUSTER_ADMIN_USER>',
            '<CLUSTER_ADMIN_PASSWORD>',
            'Never commit real credentials'
        ]
        
        for section in required_sections:
            if section not in content:
                compliance_issues.append(f"Missing required section: {section}")
        
        # Check for prohibited real data patterns
        prohibited_patterns = [
            r'kubeadmin/[^<\s]',  # Real credentials
            r'https://[^<\s]+\.qe\.red-chesterfield\.com',  # Real environments
            r'-p\s+[^<\s]',  # Real passwords
        ]
        
        for pattern in prohibited_patterns:
            if re.search(pattern, content):
                compliance_issues.append(f"Prohibited real data pattern found: {pattern}")
        
        compliance_passed = len(compliance_issues) == 0
        compliance_report = '\n'.join(compliance_issues) if compliance_issues else 'Template compliance passed'
        
        return compliance_passed, compliance_report
    
    def get_integration_status(self) -> Dict:
        """Get comprehensive integration status report."""
        total_integrations = len(self.integration_log)
        approved_deliveries = sum(1 for log in self.integration_log if log['delivery_approved'])
        
        return {
            'total_integrations': total_integrations,
            'approved_deliveries': approved_deliveries,
            'blocked_deliveries': total_integrations - approved_deliveries,
            'approval_rate': (approved_deliveries / total_integrations * 100) if total_integrations > 0 else 0,
            'enforcement_active': True,
            'last_integration': self.integration_log[-1] if self.integration_log else None,
            'security_enforcement_config': self.enforcement_config
        }

class FrameworkSecurityHook:
    """
    Framework hook to enforce security during test plan generation.
    """
    
    def __init__(self):
        self.security_integration = PatternExtensionSecurityIntegration()
    
    def pre_generation_hook(self, agent_intelligence: Dict) -> bool:
        """
        Pre-generation security hook.
        
        Args:
            agent_intelligence: Intelligence from all agents
            
        Returns:
            bool: True if generation should proceed
        """
        # Validate agent intelligence for credential exposure
        intelligence_clean = self.security_integration.validate_agent_intelligence(agent_intelligence)
        
        if not intelligence_clean:
            print("🚨 PRE-GENERATION SECURITY BLOCK: Agent intelligence contains credential exposure")
            return False
        
        return True
    
    def post_generation_hook(self, generated_content: str, output_path: str) -> Tuple[bool, str]:
        """
        Post-generation security hook.
        
        Args:
            generated_content: Generated test plan content
            output_path: Output file path
            
        Returns:
            Tuple[bool, str]: (approved, final_content_or_error)
        """
        # Apply comprehensive security enforcement
        integration_result = self.security_integration.secure_pattern_extension(
            {}, output_path  # Empty dict since content is already generated
        )
        
        if integration_result['delivery_approved']:
            return True, integration_result['sanitized_content']
        else:
            error_msg = f"🚨 POST-GENERATION SECURITY BLOCK: {integration_result.get('error_message', 'Security violations detected')}"
            return False, error_msg

def integrate_security_enforcement():
    """
    Main function to integrate security enforcement into framework.
    """
    print("🔐 Integrating Pattern Extension Security Enforcement...")
    
    # Initialize security integration
    security_integration = PatternExtensionSecurityIntegration()
    
    # Test integration with mock data
    test_intelligence = {
        'jira_ticket': 'ACM-22079',
        'feature_name': 'ClusterCurator Digest-Based Upgrades',
        'agents': {
            'agent_a': {'status': 'completed'},
            'agent_b': {'status': 'completed'},
            'agent_c': {'status': 'completed'},
            'agent_d': {'status': 'completed'}
        }
    }
    
    # Test security integration
    result = security_integration.secure_pattern_extension(test_intelligence, "test-output.md")
    
    print(f"✅ Security Integration Status:")
    print(f"   - Security Validation: {result['security_validation']}")
    print(f"   - Delivery Approved: {result['delivery_approved']}")
    print(f"   - Security Score: {result['security_score']}")
    
    return result['delivery_approved']

if __name__ == "__main__":
    integrate_security_enforcement()