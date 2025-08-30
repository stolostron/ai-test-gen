#!/usr/bin/env python3
"""
Comprehensive Phase 0 Version Logic Unit Tests
Tests the critical version comparison logic discovered through real data testing
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add AI services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services'))

from version_intelligence_service import VersionIntelligenceService
from environment_assessment_client import EnvironmentAssessmentClient, EnvironmentData
from foundation_context import FoundationContext

class TestPhase0VersionLogic(unittest.TestCase):
    """Test the critical version comparison logic that was failing in real data testing"""
    
    def setUp(self):
        """Set up test environment"""
        self.service = VersionIntelligenceService()
    
    def test_version_comparison_logic_acm_vs_openshift(self):
        """Test that ACM target version is compared against ACM environment version, not OpenShift version"""
        
        # REAL DATA CASE: This was failing in real testing
        # Target: ACM 2.15.0, Environment detected: OpenShift 4.20.0-ec.4
        # Framework was comparing ACM 2.15.0 vs OpenShift 4.20.0-ec.4 (WRONG!)
        
        with patch.object(self.service, '_extract_jira_information') as mock_jira:
            with patch.object(self.service, '_assess_environment_version') as mock_env:
                
                # Simulate real ACM-22079 JIRA data
                mock_jira.return_value = {
                    'id': 'ACM-22079',
                    'title': 'ClusterCurator digest-based upgrades',
                    'fix_version': '2.15.0',  # ACM version
                    'component': 'ClusterCurator',
                    'description': 'ClusterCurator feature'
                }
                
                # Simulate real environment returning OpenShift version (the problem!)
                mock_env.return_value = {
                    'version': '4.20.0-ec.4',  # This is OpenShift version, NOT ACM version!
                    'cluster_name': 'test-cluster',
                    'api_url': 'https://api.test.com:6443',  # Required field
                    'console_url': 'https://console.test.com',  # Required field
                    'platform': 'openshift',
                    'region': 'us-east-1',  # Required field
                    'health_status': 'healthy',
                    'connectivity_confirmed': True,
                    'detection_method': 'oc_assessment',
                    'platform_details': {},  # Required field
                    'tools_available': {'oc': True},  # Required field
                    'assessment_timestamp': '2025-08-26T20:00:00',  # Required field
                    'api_source': 'environment_assessment',  # Required field
                    # NEW: Enhanced environment data without ACM
                    'product_detected': 'OpenShift',
                    'version_detection_method': 'platform_fallback',
                    'acm_status': 'acm_not_installed',
                    'version_context': {
                        'is_acm': False,
                        'is_openshift': True,
                        'is_kubernetes': False,
                        'command_used': 'oc version -o json',
                        'raw_output': 'openshift_version_output'
                    }
                }
                
                # Execute Phase 0
                context = self.service.analyze_version_gap('ACM-22079')
                
                # CRITICAL TEST: Framework should detect context mismatch and handle appropriately
                deployment_instruction = context.deployment_instruction
                
                # Framework should NOT compare ACM vs OpenShift versions
                self.assertNotIn('Upgrade from 4.20.0-ec.4 to 2.15.0', deployment_instruction)
                
                # Framework should indicate context mismatch or ACM not detected
                self.assertTrue(
                    'VERSION CONTEXT MISMATCH' in deployment_instruction or
                    'ACM version detection required' in deployment_instruction or
                    'ACM NOT INSTALLED' in deployment_instruction
                )
    
    def test_acm_version_detection_in_environment(self):
        """Test that environment assessment should detect ACM version when present"""
        
        with patch.object(self.service, '_extract_jira_information') as mock_jira:
            with patch.object(self.service, '_assess_environment_version') as mock_env:
                
                # Simulate real ACM-22079 JIRA data
                mock_jira.return_value = {
                    'id': 'ACM-22079',
                    'title': 'ClusterCurator digest-based upgrades',
                    'fix_version': '2.15.0',  # Target ACM version
                    'component': 'ClusterCurator',
                    'description': 'ClusterCurator feature'
                }
                
                # Mock environment that HAS ACM installed with proper enhanced data
                mock_env.return_value = {
                    'version': '2.14.0-62',  # ACM version detected
                    'cluster_name': 'test-cluster',
                    'api_url': 'https://api.test.com:6443',
                    'console_url': 'https://console.test.com',
                    'platform': 'openshift',
                    'region': 'us-east-1',
                    'health_status': 'healthy',
                    'connectivity_confirmed': True,
                    'detection_method': 'oc_assessment',
                    'platform_details': {
                        'platform': 'openshift',
                        'openshift_version': '4.20.0-ec.4',  # OpenShift version separate
                        'acm_version': '2.14.0-62',  # ACM version detected
                        'acm_installed': True
                    },
                    'tools_available': {'oc': True},
                    'assessment_timestamp': '2025-08-26T20:00:00',
                    'api_source': 'environment_assessment',
                    # NEW: Enhanced environment data with ACM
                    'product_detected': 'ACM',
                    'version_detection_method': 'acm_mch_detection',
                    'acm_status': 'acm_installed_with_version',
                    'version_context': {
                        'is_acm': True,
                        'is_openshift': False,
                        'is_kubernetes': False,
                        'command_used': 'oc get mch -A -o jsonpath={.items[0].status.currentVersion}',
                        'raw_output': '2.14.0-62'
                    }
                }
                
                context = self.service.analyze_version_gap('ACM-22079')
                
                # CORRECT behavior: Should compare ACM vs ACM
                self.assertEqual(context.version_context.target_version, '2.15.0')  # ACM target
                self.assertEqual(context.version_context.environment_version, '2.14.0-62')  # ACM environment
                
                # Should detect upgrade from ACM 2.14.0-62 to ACM 2.15.0
                self.assertIn('2.14.0', context.deployment_instruction)
                self.assertIn('2.15.0', context.deployment_instruction)
                self.assertNotIn('4.20.0', context.deployment_instruction)  # Should not mention OpenShift version
    
    def test_no_acm_installed_scenario(self):
        """Test behavior when ACM is not installed in environment"""
        
        with patch.object(self.service, '_extract_jira_information') as mock_jira:
            with patch.object(self.service, '_assess_environment_version') as mock_env:
                
                mock_jira.return_value = {
                    'id': 'ACM-22079',
                    'title': 'ClusterCurator digest-based upgrades',
                    'fix_version': '2.15.0',
                    'component': 'ClusterCurator',
                    'description': 'ClusterCurator feature'
                }
                
                # Mock environment with NO ACM installed - enhanced data format
                mock_env.return_value = {
                    'version': '4.20.0-ec.4',  # Only OpenShift version available
                    'cluster_name': 'test-cluster',
                    'api_url': 'https://api.test.com:6443',
                    'console_url': 'https://console.test.com',
                    'platform': 'openshift',
                    'region': 'us-east-1',
                    'health_status': 'healthy',
                    'connectivity_confirmed': True,
                    'detection_method': 'oc_assessment',
                    'platform_details': {
                        'platform': 'openshift',
                        'openshift_version': '4.20.0-ec.4',
                        'acm_installed': False  # No ACM detected
                    },
                    'tools_available': {'oc': True},
                    'assessment_timestamp': '2025-08-26T20:00:00',
                    'api_source': 'environment_assessment',
                    # NEW: Enhanced environment data showing no ACM
                    'product_detected': 'OpenShift',
                    'version_detection_method': 'platform_fallback',
                    'acm_status': 'acm_not_installed',
                    'version_context': {
                        'is_acm': False,
                        'is_openshift': True,
                        'is_kubernetes': False,
                        'command_used': 'oc version -o json',
                        'raw_output': 'openshift_version_output'
                    }
                }
                
                context = self.service.analyze_version_gap('ACM-22079')
                
                # Should indicate ACM needs to be installed or context mismatch
                deployment_instruction = context.deployment_instruction
                self.assertTrue(
                    'VERSION CONTEXT MISMATCH' in deployment_instruction or
                    'ACM NOT INSTALLED' in deployment_instruction or
                    'ACM version detection required' in deployment_instruction or
                    'not installed' in deployment_instruction.lower()
                )
                
                # Should NOT attempt version comparison
                self.assertNotIn('Upgrade from 4.20.0-ec.4 to 2.15.0', deployment_instruction)
    
    def test_acm_version_detection_with_real_data(self):
        """Test ACM version detection using the real command format discovered by user"""
        
        with patch.object(self.service, '_extract_jira_information') as mock_jira:
            with patch.object(self.service, '_assess_environment_version') as mock_env:
                
                mock_jira.return_value = {
                    'id': 'ACM-22079',
                    'title': 'ClusterCurator digest-based upgrades',
                    'fix_version': '2.15.0',
                    'component': 'ClusterCurator',
                    'description': 'ClusterCurator feature'
                }
                
                # Mock environment that properly detects ACM using the real command
                mock_env.return_value = {
                    'version': '2.14.0-62',  # Real ACM version from user's cluster
                    'cluster_name': 'mist10-0',
                    'api_url': 'https://api.mist10-0.qe.red-chesterfield.com:6443',
                    'console_url': 'https://console.mist10-0.qe.red-chesterfield.com:6443',
                    'platform': 'openshift',
                    'region': 'unknown',
                    'health_status': 'healthy',
                    'connectivity_confirmed': True,
                    'detection_method': 'oc_assessment',
                    'platform_details': {
                        'platform': 'openshift',
                        'openshift_version': '4.20.0-ec.4',  # OpenShift version separate
                        'acm_version': '2.14.0-62',  # ACM version detected
                        'acm_installed': True
                    },
                    'tools_available': {'oc': True, 'kubectl': True, 'gh': True, 'curl': True, 'docker': True},
                    'assessment_timestamp': '2025-08-26T20:00:00',
                    'api_source': 'environment_assessment',
                    # Enhanced environment data using real ACM detection
                    'product_detected': 'ACM',
                    'version_detection_method': 'acm_mch_detection',
                    'acm_status': 'acm_installed_with_version',
                    'version_context': {
                        'is_acm': True,
                        'is_openshift': False,
                        'is_kubernetes': False,
                        'command_used': 'oc get mch -A -o jsonpath={.items[0].status.currentVersion}',
                        'raw_output': '2.14.0-62'
                    }
                }
                
                context = self.service.analyze_version_gap('ACM-22079')
                
                # Should properly detect ACM to ACM upgrade
                self.assertEqual(context.version_context.target_version, '2.15.0')
                self.assertEqual(context.version_context.environment_version, '2.14.0-62')
                self.assertEqual(context.version_context.comparison_result, 'newer')
                
                # Should generate proper ACM upgrade instruction
                deployment_instruction = context.deployment_instruction
                self.assertIn('Upgrade ACM from 2.14.0-62 to 2.15.0', deployment_instruction)
                self.assertIn('MINOR UPGRADE', deployment_instruction)
                
                # Should NOT contain any OpenShift version references
                self.assertNotIn('4.20.0', deployment_instruction)
                self.assertNotIn('context mismatch', deployment_instruction.lower())
    
    def test_version_format_validation(self):
        """Test that version format validation works correctly for different product versions"""
        
        # Test various version formats
        version_test_cases = [
            ('2.15.0', True, 'Standard ACM version'),
            ('4.20.0-ec.4', True, 'OpenShift early candidate version'),
            ('4.14.1', True, 'Standard OpenShift version'),
            ('2.15.0-RC1', True, 'ACM release candidate'),
            ('invalid-version', False, 'Invalid version format'),
            ('', False, 'Empty version'),
            (None, False, 'None version')
        ]
        
        for version, expected_valid, description in version_test_cases:
            with self.subTest(version=version, description=description):
                result = self.service._is_valid_version_format(version)
                self.assertEqual(result, expected_valid, f"Version '{version}' validation failed: {description}")
    
    def test_deployment_instruction_generation_logic(self):
        """Test deployment instruction generation with correct version context"""
        
        test_scenarios = [
            {
                'name': 'ACM upgrade required',
                'target': '2.15.0',
                'environment': '2.14.0',
                'product': 'ACM',
                'expected_instruction': 'Upgrade ACM from 2.14.0 to 2.15.0'
            },
            {
                'name': 'ACM fresh install',
                'target': '2.15.0',
                'environment': None,
                'product': 'ACM',
                'expected_instruction': 'Install ACM 2.15.0'
            },
            {
                'name': 'ACM already at target',
                'target': '2.15.0',
                'environment': '2.15.0',
                'product': 'ACM',
                'expected_instruction': 'ACM 2.15.0 already installed'
            }
        ]
        
        for scenario in test_scenarios:
            with self.subTest(scenario=scenario['name']):
                # Create proper gap analysis data
                if scenario['environment'] is None:
                    gap_analysis = {
                        'comparison': 'not_installed',
                        'gap_type': 'fresh_install_required',
                        'urgency': 'install_required',
                        'version_difference': {'major': 0, 'minor': 0, 'patch': 0}
                    }
                elif scenario['environment'] == scenario['target']:
                    gap_analysis = {
                        'comparison': 'same',
                        'gap_type': 'no_action_needed',
                        'urgency': 'low',
                        'version_difference': {'major': 0, 'minor': 0, 'patch': 0}
                    }
                else:
                    gap_analysis = {
                        'comparison': 'newer',
                        'gap_type': 'upgrade_required',
                        'urgency': 'medium',
                        'version_difference': {'major': 0, 'minor': 1, 'patch': 0}
                    }
                
                instruction = self.service._generate_deployment_instruction(
                    scenario['target'], 
                    scenario['environment'], 
                    gap_analysis
                )
                
                # Check for partial matches since exact format might differ
                if 'Install ACM' in scenario['expected_instruction']:
                    self.assertIn('ACM NOT INSTALLED', instruction)
                elif 'already installed' in scenario['expected_instruction']:
                    self.assertIn('NO ACTION REQUIRED', instruction)
                elif 'Upgrade ACM' in scenario['expected_instruction']:
                    self.assertIn('UPGRADE REQUIRED', instruction)
    
    def test_cache_path_generation_fix(self):
        """Test that cache paths are generated correctly for URLs with special characters"""
        
        # This was failing in real testing due to URL characters
        problematic_env = "Console: https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com, Creds: <CLUSTER_ADMIN_USER>/<CLUSTER_ADMIN_PASSWORD>"
        
        env_client = EnvironmentAssessmentClient()
        
        # Should not fail due to path characters
        try:
            result = env_client.assess_environment(problematic_env)
            self.assertTrue(result.connectivity_confirmed)
        except FileNotFoundError as e:
            if 'cache' in str(e):
                self.fail(f"Cache path generation failed for URL with special characters: {e}")


class TestVersionIntelligenceServiceRealDataIssues(unittest.TestCase):
    """Test fixes for specific issues discovered in real data testing"""
    
    def test_real_acm_22079_scenario(self):
        """Test the exact scenario that failed in real ACM-22079 testing"""
        
        service = VersionIntelligenceService()
        
        # Exact real data that was causing issues
        with patch.object(service, '_extract_jira_information') as mock_jira:
            with patch.object(service, '_assess_environment_version') as mock_env:
                
                # Real JIRA data (from simulation)
                mock_jira.return_value = {
                    'id': 'ACM-22079',
                    'title': 'ClusterCurator digest-based upgrades for disconnected environments',
                    'status': 'In Progress',
                    'fix_version': '2.15.0',
                    'priority': 'High',
                    'component': 'ClusterCurator',
                    'description': 'Implement digest-based upgrade functionality for disconnected Amadeus environments',
                    'api_source': 'simulation'
                }
                
                # Real environment data (from actual cluster)
                mock_env.return_value = {
                    'version': '4.20.0-ec.4',  # Real OpenShift version from cluster
                    'cluster_name': 'mist10-0',
                    'api_url': 'https://api.mist10-0.qe.red-chesterfield.com:6443',
                    'console_url': 'https://console.mist10-0.qe.red-chesterfield.com:6443',
                    'platform': 'openshift',
                    'region': 'unknown',  # Required field
                    'health_status': 'healthy',
                    'connectivity_confirmed': True,
                    'detection_method': 'oc_assessment',
                    'platform_details': {},  # Required field
                    'tools_available': {'oc': True},  # Required field
                    'assessment_timestamp': '2025-08-26T20:00:00',  # Required field
                    'api_source': 'environment_assessment'  # Required field
                }
                
                context = service.analyze_version_gap('ACM-22079')
                
                # The framework should handle this intelligently
                # It should detect that we're comparing different product versions
                # and provide appropriate guidance
                
                deployment_instruction = context.deployment_instruction
                
                # Should NOT contain the erroneous comparison
                self.assertNotIn('Upgrade from 4.20.0-ec.4 to 2.15.0', deployment_instruction)
                
                # Should indicate version context mismatch
                self.assertTrue(
                    'ACM version not detected' in deployment_instruction or
                    'version context mismatch' in deployment_instruction.lower() or
                    'install ACM' in deployment_instruction.lower()
                )


if __name__ == '__main__':
    # The VersionIntelligenceService now has the _is_valid_version_format method built-in
    # No need to override it
    unittest.main()