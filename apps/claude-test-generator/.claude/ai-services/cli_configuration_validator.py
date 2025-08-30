#!/usr/bin/env python3
"""
CLI Configuration Validator for Agent D Environment Intelligence
Ensures all CLI tools are properly configured and accessible
"""

import subprocess
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CLIConfigurationValidator:
    """Validates CLI tool configuration for framework operations"""
    
    def __init__(self):
        self.validation_results = {}
        self.overall_status = True
    
    def validate_all_cli_tools(self) -> Dict[str, Any]:
        """Perform comprehensive CLI tool validation"""
        logger.info("Starting comprehensive CLI tool validation...")
        
        validation_start = datetime.now()
        
        # Validate each CLI tool
        self._validate_github_cli()
        self._validate_openshift_cli()
        self._validate_kubernetes_cli()
        self._validate_ssh_configuration()
        self._validate_additional_tools()
        
        validation_duration = (datetime.now() - validation_start).total_seconds()
        
        # Compile results
        results = {
            'overall_status': self.overall_status,
            'validation_timestamp': validation_start.isoformat(),
            'validation_duration_seconds': validation_duration,
            'tool_results': self.validation_results,
            'summary': self._generate_summary()
        }
        
        logger.info(f"CLI validation completed in {validation_duration:.2f}s")
        return results
    
    def _validate_github_cli(self):
        """Validate GitHub CLI configuration and authentication"""
        tool_name = 'github_cli'
        result = {'name': 'GitHub CLI (gh)', 'status': 'unknown', 'details': {}}
        
        try:
            # Check availability
            version_result = subprocess.run(['gh', 'version'], 
                                          capture_output=True, text=True, timeout=5)
            if version_result.returncode != 0:
                result['status'] = 'unavailable'
                result['error'] = f"gh version failed: {version_result.stderr}"
                self.overall_status = False
                self.validation_results[tool_name] = result
                return
            
            # Check authentication
            auth_result = subprocess.run(['gh', 'auth', 'status'], 
                                       capture_output=True, text=True, timeout=5)
            if auth_result.returncode == 0:
                result['status'] = 'authenticated'
                result['details']['auth_status'] = 'authenticated'
                result['details']['protocol'] = 'ssh' if 'ssh' in auth_result.stderr else 'https'
            else:
                result['status'] = 'unauthenticated'
                result['details']['auth_status'] = 'unauthenticated'
                result['error'] = auth_result.stderr
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            self.overall_status = False
        
        self.validation_results[tool_name] = result
    
    def _validate_openshift_cli(self):
        """Validate OpenShift CLI configuration"""
        tool_name = 'openshift_cli'
        result = {'name': 'OpenShift CLI (oc)', 'status': 'unknown', 'details': {}}
        
        try:
            # Check availability
            version_result = subprocess.run(['oc', 'version', '--client=true'], 
                                          capture_output=True, text=True, timeout=5)
            if version_result.returncode != 0:
                result['status'] = 'unavailable'
                result['error'] = f"oc version failed: {version_result.stderr}"
                self.validation_results[tool_name] = result
                return
            
            result['details']['version'] = version_result.stdout.strip()
            
            # Check authentication
            whoami_result = subprocess.run(['oc', 'whoami'], 
                                         capture_output=True, text=True, timeout=5)
            if whoami_result.returncode == 0:
                result['status'] = 'authenticated'
                result['details']['user'] = whoami_result.stdout.strip()
                
                # Get current context
                context_result = subprocess.run(['oc', 'config', 'current-context'], 
                                              capture_output=True, text=True, timeout=5)
                if context_result.returncode == 0:
                    result['details']['context'] = context_result.stdout.strip()
            else:
                result['status'] = 'unauthenticated'
                result['details']['auth_status'] = 'not logged in'
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        self.validation_results[tool_name] = result
    
    def _validate_kubernetes_cli(self):
        """Validate Kubernetes CLI configuration"""
        tool_name = 'kubernetes_cli'
        result = {'name': 'Kubernetes CLI (kubectl)', 'status': 'unknown', 'details': {}}
        
        try:
            # Check availability
            version_result = subprocess.run(['kubectl', 'version', '--client=true'], 
                                          capture_output=True, text=True, timeout=5)
            if version_result.returncode != 0:
                result['status'] = 'unavailable'
                result['error'] = f"kubectl version failed: {version_result.stderr}"
                self.validation_results[tool_name] = result
                return
            
            # Check current context
            context_result = subprocess.run(['kubectl', 'config', 'current-context'], 
                                          capture_output=True, text=True, timeout=5)
            if context_result.returncode == 0:
                result['status'] = 'configured'
                result['details']['context'] = context_result.stdout.strip()
            else:
                result['status'] = 'unconfigured'
                result['details']['context'] = 'no context set'
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        self.validation_results[tool_name] = result
    
    def _validate_ssh_configuration(self):
        """Validate SSH configuration for GitHub"""
        tool_name = 'ssh_github'
        result = {'name': 'SSH GitHub Access', 'status': 'unknown', 'details': {}}
        
        try:
            # Test SSH to GitHub
            ssh_result = subprocess.run(['ssh', '-T', 'git@github.com'], 
                                      capture_output=True, text=True, timeout=10)
            
            # SSH to GitHub returns exit code 1 on successful auth (expected)
            if 'successfully authenticated' in ssh_result.stderr:
                result['status'] = 'authenticated'
                result['details']['auth_method'] = 'ssh_key'
            else:
                result['status'] = 'unauthenticated'
                result['error'] = ssh_result.stderr
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        self.validation_results[tool_name] = result
    
    def _validate_additional_tools(self):
        """Validate additional CLI tools needed by Agent D"""
        additional_tools = {
            'curl': ['--version'],
            'docker': ['--version']
        }
        
        for tool, cmd in additional_tools.items():
            result = {'name': f'{tool.title()}', 'status': 'unknown', 'details': {}}
            
            try:
                tool_result = subprocess.run([tool] + cmd, 
                                           capture_output=True, text=True, timeout=5)
                if tool_result.returncode == 0:
                    result['status'] = 'available'
                    result['details']['version_info'] = tool_result.stdout.split('\n')[0]
                else:
                    result['status'] = 'unavailable'
                    result['error'] = tool_result.stderr
                    
            except Exception as e:
                result['status'] = 'error'
                result['error'] = str(e)
            
            self.validation_results[tool] = result
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate validation summary"""
        total_tools = len(self.validation_results)
        authenticated_tools = sum(1 for r in self.validation_results.values() 
                                if r['status'] in ['authenticated', 'available', 'configured'])
        
        summary = {
            'total_tools_checked': total_tools,
            'tools_operational': authenticated_tools,
            'success_rate': f"{(authenticated_tools/total_tools)*100:.1f}%" if total_tools > 0 else "0%",
            'critical_tools_status': {
                'github_cli': self.validation_results.get('github_cli', {}).get('status', 'unknown'),
                'openshift_cli': self.validation_results.get('openshift_cli', {}).get('status', 'unknown'),
                'ssh_github': self.validation_results.get('ssh_github', {}).get('status', 'unknown')
            },
            'agent_d_readiness': self.overall_status and authenticated_tools >= 4
        }
        
        return summary


def run_cli_validation() -> Dict[str, Any]:
    """Run comprehensive CLI validation and return results"""
    validator = CLIConfigurationValidator()
    return validator.validate_all_cli_tools()


if __name__ == "__main__":
    # Run validation when script is executed directly
    import json
    results = run_cli_validation()
    print(json.dumps(results, indent=2))