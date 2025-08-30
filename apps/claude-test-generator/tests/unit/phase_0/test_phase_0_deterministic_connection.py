#!/usr/bin/env python3
"""
Comprehensive Phase 0 Deterministic Environment Connection Unit Tests
Tests all aspects of the deterministic environment connection logic implemented and validated
"""

import unittest
import json
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock, call
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

# Add AI services to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services'))

from version_intelligence_service import VersionIntelligenceService, VersionIntelligenceError
from environment_assessment_client import EnvironmentAssessmentClient, EnvironmentData, EnvironmentAssessmentConfig
from foundation_context import FoundationContext


class TestPhase0DeterministicConnection(unittest.TestCase):
    """
    Comprehensive test suite for Phase 0 deterministic environment connection logic
    
    CRITICAL TESTING COVERAGE:
    1. User-provided environment priority and connection
    2. QE6 default environment fetching from Jenkins  
    3. Build staleness detection and user notification
    4. Credential parsing and validation
    5. Deterministic login and connection logic
    6. Graceful no-environment workflow completion
    7. ACM-first version detection in connected environments
    8. Complete foundation context generation
    """
    
    def setUp(self):
        """Set up test environment"""
        self.service = VersionIntelligenceService()
        self.env_client = EnvironmentAssessmentClient()
        
        # Real test data from validated scenarios
        self.mist10_environment = "Console: https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com, Creds: kubeadmin/Gz7oJ-IHZgq-5MIQ9-Kdhid"
        self.qe6_jenkins_response = {
            "Console": "https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com",
            "PASSWORD": "BzDnQ-UFLYz-MpYpt-VAQae",
            "USERNAME": "kubeadmin",
            "API_URL": "https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443"
        }
    
    # TEST 1: User Environment Priority and Deterministic Connection
    def test_user_provided_environment_deterministic_connection(self):
        """Test that user-provided environments are prioritized and connected deterministically"""
        
        with patch.object(self.env_client, '_parse_environment_credentials') as mock_parse:
            with patch.object(self.env_client, '_login_to_target_environment') as mock_login:
                with patch.object(self.env_client, '_perform_connected_assessment') as mock_assess:
                    
                    # Mock successful credential parsing
                    mock_parse.return_value = {
                        'valid': True,
                        'console_url': 'https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com',
                        'username': 'kubeadmin',
                        'password': 'Gz7oJ-IHZgq-5MIQ9-Kdhid',
                        'cluster_name': 'mist10-0',
                        'api_url': 'https://api.mist10-0.qe.red-chesterfield.com:6443'
                    }
                    
                    # Mock successful login
                    mock_login.return_value = {
                        'success': True,
                        'method': 'oc_username_password',
                        'logged_in_user': 'kubeadmin'
                    }
                    
                    # Mock successful assessment with ACM version
                    mock_assess.return_value = EnvironmentData(
                        cluster_name='mist10-0',
                        version='2.14.0-62',
                        api_url='https://api.mist10-0.qe.red-chesterfield.com:6443',
                        console_url='https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com',
                        platform='openshift',
                        region='unknown',
                        health_status='healthy',
                        connectivity_confirmed=True,
                        platform_details={'platform': 'openshift'},
                        detection_method='oc_deterministic_connection',
                        assessment_timestamp='2025-08-26T23:21:55.682005',
                        tools_available={'oc': True}
                    )
                    
                    # Execute assessment
                    result = self.env_client.assess_environment(self.mist10_environment)
                    
                    # Verify deterministic connection path
                    mock_parse.assert_called_once()
                    mock_login.assert_called_once()
                    mock_assess.assert_called_once()
                    
                    # Verify successful connection
                    self.assertTrue(result.connectivity_confirmed)
                    self.assertEqual(result.cluster_name, 'mist10-0')
                    self.assertEqual(result.version, '2.14.0-62')
                    self.assertEqual(result.detection_method, 'oc_deterministic_connection')
    
    # TEST 2: QE6 Default Environment Fetching from Jenkins with Build Information
    def test_qe6_default_environment_jenkins_fetching_with_build_info(self):
        """Test automatic qe6 deployment fetching when no environment provided with Jenkins build information"""
        
        with patch.object(self.env_client, '_fetch_qe6_latest_deployment') as mock_fetch:
            with patch.object(self.env_client, '_check_deployment_staleness') as mock_staleness:
                with patch.object(self.env_client, '_parse_environment_credentials') as mock_parse:
                    
                    # Mock successful Jenkins fetch
                    qe6_env_string = "Console: https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com, Creds: kubeadmin/BzDnQ-UFLYz-MpYpt-VAQae"
                    mock_fetch.return_value = qe6_env_string
                    
                    # Mock build staleness with comprehensive Jenkins info
                    mock_staleness.return_value = {
                        'is_stale': False,
                        'successful_build': '661',
                        'successful_build_result': 'SUCCESS',
                        'latest_build': '661',
                        'latest_build_result': 'SUCCESS',
                        'jenkins_job_url': 'https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/CI-Jobs/job/deploy-qe6-vmware-ibm',
                        'status': 'checked'
                    }
                    
                    # Mock credential parsing failure (URL-only format)
                    mock_parse.return_value = {
                        'valid': False,
                        'console_url': 'https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com',
                        'username': 'kubeadmin',
                        'password': 'BzDnQ-UFLYz-MpYpt-VAQae',
                        'cluster_name': 'qe6-vmware-ibm',
                        'api_url': None
                    }
                    
                    # Execute assessment with no environment (should default to qe6)
                    result = self.env_client.assess_environment(None)
                    
                    # Verify Jenkins fetch was attempted
                    mock_fetch.assert_called_once()
                    mock_staleness.assert_called_once()
                    
                    # Verify graceful no-environment handling
                    self.assertEqual(result.cluster_name, 'NO_TEST_ENVIRONMENT')
                    self.assertEqual(result.version, 'environment_unavailable')
                    self.assertEqual(result.platform, 'no_environment')
                    self.assertFalse(result.connectivity_confirmed)
                    
                    # Verify Jenkins build information is included
                    jenkins_metadata = result.raw_data.get('jenkins_deployment_metadata', {})
                    self.assertEqual(jenkins_metadata.get('jenkins_successful_build'), '661')
                    self.assertEqual(jenkins_metadata.get('jenkins_successful_build_result'), 'SUCCESS')
                    self.assertEqual(jenkins_metadata.get('jenkins_deployment_status'), 'fetched_but_connection_failed')
                    self.assertFalse(jenkins_metadata.get('jenkins_is_stale', True))
    
    # TEST 3: Build Staleness Detection and User Notification
    def test_build_staleness_detection_and_notification(self):
        """Test build staleness detection following setup_clc.sh patterns"""
        
        with patch('requests.get') as mock_requests:
            # Mock Jenkins API response for stale build scenario
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'number': 665}  # Latest build is 665
            mock_requests.return_value = mock_response
            
            # Test staleness detection
            staleness_result = self.env_client._check_deployment_staleness(
                "https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/CI-Jobs/job/deploy-qe6-vmware-ibm",
                "https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/CI-Jobs/job/deploy-qe6-vmware-ibm/661"  # Successful is 661
            )
            
            # Verify staleness detection
            self.assertTrue(staleness_result['is_stale'])
            self.assertEqual(staleness_result['latest_build'], '665')
            self.assertEqual(staleness_result['successful_build'], '661')
            self.assertEqual(staleness_result['status'], 'checked')
    
    # TEST 4: Credential Parsing and Validation
    def test_credential_parsing_comprehensive(self):
        """Test credential parsing for various environment string formats"""
        
        test_cases = [
            {
                'name': 'Standard mist10 format',
                'input': 'Console: https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com, Creds: kubeadmin/Gz7oJ-IHZgq-5MIQ9-Kdhid',
                'expected_valid': True,
                'expected_cluster': 'mist10-0'
            },
            {
                'name': 'QE6 format',
                'input': 'Console: https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com, Creds: kubeadmin/BzDnQ-UFLYz-MpYpt-VAQae',
                'expected_valid': True,
                'expected_cluster': 'qe6-vmware-ibm'
            },
            {
                'name': 'URL-only format (invalid)',
                'input': 'Console: https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com',
                'expected_valid': False,
                'expected_cluster': None
            },
            {
                'name': 'Malformed credentials',
                'input': 'Console: https://example.com, Creds: invalid',
                'expected_valid': False,
                'expected_cluster': None
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case['name']):
                result = self.env_client._parse_environment_credentials(case['input'])
                
                self.assertEqual(result['valid'], case['expected_valid'])
                if case['expected_cluster']:
                    self.assertEqual(result['cluster_name'], case['expected_cluster'])
    
    # TEST 5: Deterministic Login and Connection Logic
    def test_deterministic_login_and_connection_logic(self):
        """Test the complete deterministic connection workflow"""
        
        with patch('subprocess.run') as mock_subprocess:
            # Mock successful oc logout
            mock_subprocess.side_effect = [
                Mock(returncode=0),  # oc logout
                Mock(returncode=0, stdout='Login successful.', stderr=''),  # oc login
                Mock(returncode=0, stdout='kubeadmin', stderr='')  # oc whoami
            ]
            
            credentials = {
                'username': 'kubeadmin',
                'password': 'test-password',
                'api_url': 'https://api.test-cluster.example.com:6443',
                'cluster_name': 'test-cluster'
            }
            
            result = self.env_client._login_to_target_environment(credentials)
            
            # Verify login sequence
            self.assertEqual(mock_subprocess.call_count, 3)
            self.assertTrue(result['success'])
            self.assertEqual(result['method'], 'oc_username_password')
            self.assertEqual(result['logged_in_user'], 'kubeadmin')
    
    # TEST 6: Graceful No-Environment Workflow Completion with Jenkins Metadata
    def test_graceful_no_environment_workflow_completion_with_jenkins_metadata(self):
        """Test that framework completes workflow gracefully when no environment is available and includes Jenkins metadata"""
        
        with patch.object(self.service, '_assess_environment_version') as mock_assess:
            with patch.object(self.service, '_extract_jira_information') as mock_jira:
                
                # Mock JIRA extraction
                mock_jira.return_value = {
                    'id': 'ACM-22079',
                    'title': 'Support digest-based upgrades via ClusterCurator for non-recommended upgrades',
                    'status': 'Review',
                    'fix_version': '2.15.0',
                    'priority': 'Critical',
                    'component': 'Cluster Lifecycle'
                }
                
                # Mock no-environment assessment with Jenkins metadata
                mock_assess.return_value = {
                    'version': 'environment_unavailable',
                    'cluster_name': 'NO_TEST_ENVIRONMENT',
                    'api_url': 'unavailable',
                    'console_url': 'unavailable',
                    'platform': 'no_environment',
                    'region': 'unavailable',
                    'health_status': 'no_connection',
                    'connectivity_confirmed': False,
                    'detection_method': 'no_environment_available',
                    'platform_details': {
                        'error': 'invalid_credentials',
                        'root_cause': 'Could not parse credentials',
                        'jenkins_successful_build': '661',
                        'jenkins_successful_build_result': 'SUCCESS',
                        'jenkins_latest_build': '661',
                        'jenkins_latest_build_result': 'SUCCESS',
                        'jenkins_is_stale': False,
                        'jenkins_job_url': 'https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/CI-Jobs/job/deploy-qe6-vmware-ibm',
                        'jenkins_deployment_status': 'fetched_but_connection_failed'
                    },
                    'tools_available': {},
                    'assessment_timestamp': '2025-08-26T23:22:18.063044',
                    'api_source': 'no_environment',
                    'raw_data': {
                        'jenkins_deployment_metadata': {
                            'jenkins_successful_build': '661',
                            'jenkins_successful_build_result': 'SUCCESS',
                            'jenkins_latest_build': '661',
                            'jenkins_latest_build_result': 'SUCCESS',
                            'jenkins_is_stale': False,
                            'jenkins_job_url': 'https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/CI-Jobs/job/deploy-qe6-vmware-ibm',
                            'jenkins_deployment_status': 'fetched_but_connection_failed'
                        }
                    }
                }
                
                # Execute Phase 0 with no environment
                context = self.service.analyze_version_gap('ACM-22079', None)
                
                # Verify graceful completion
                self.assertEqual(context.version_context.comparison_result, 'no_environment')
                self.assertEqual(context.environment_baseline.cluster_name, 'NO_TEST_ENVIRONMENT')
                self.assertFalse(context.environment_baseline.connectivity_confirmed)
                self.assertIn('NO TEST ENVIRONMENT AVAILABLE', context.deployment_instruction)
                
                # Framework should still be ready for agent inheritance
                self.assertTrue(context.agent_inheritance_ready)
                
                # Verify Jenkins metadata is included
                self.assertIsNotNone(context.environment_baseline.jenkins_deployment_metadata)
                jenkins_metadata = context.environment_baseline.jenkins_deployment_metadata
                self.assertEqual(jenkins_metadata['jenkins_successful_build'], '661')
                self.assertEqual(jenkins_metadata['jenkins_successful_build_result'], 'SUCCESS')
                self.assertEqual(jenkins_metadata['jenkins_deployment_status'], 'fetched_but_connection_failed')
                self.assertFalse(jenkins_metadata['jenkins_is_stale'])
    
    # TEST 7: ACM-First Version Detection in Connected Environments  
    def test_acm_first_version_detection_connected(self):
        """Test ACM-first version detection when connected to environment"""
        
        with patch('subprocess.run') as mock_subprocess:
            # Mock ACM version detection success
            mock_subprocess.return_value = Mock(
                returncode=0,
                stdout='2.14.0-62',
                stderr=''
            )
            
            result = self.env_client._get_acm_version_info()
            
            # Verify ACM detection
            self.assertEqual(result['version'], '2.14.0-62')
            self.assertEqual(result['product'], 'ACM')
            self.assertEqual(result['detection_method'], 'acm_mch_detection')
            self.assertIn('oc get mch -A', result['command_used'])
    
    # TEST 8: Complete Foundation Context Generation
    def test_complete_foundation_context_generation(self):
        """Test complete foundation context generation with all required fields"""
        
        with patch.object(self.service, '_extract_jira_information') as mock_jira:
            with patch.object(self.service, '_assess_environment_version') as mock_env:
                
                # Mock complete JIRA data
                mock_jira.return_value = {
                    'id': 'ACM-22079',
                    'title': 'Support digest-based upgrades via ClusterCurator for non-recommended upgrades',
                    'status': 'Review',
                    'fix_version': '2.15.0',
                    'priority': 'Critical',
                    'component': 'Cluster Lifecycle',
                    'description': 'Test description',
                    'assignee': 'Test assignee',
                    'reporter': 'Test reporter',
                    'created': '2025-01-01T00:00:00.000+0000',
                    'updated': '2025-01-02T00:00:00.000+0000',
                    'labels': ['test'],
                    'api_source': 'jira_api'
                }
                
                # Mock successful environment assessment
                mock_env.return_value = {
                    'version': '2.14.0-62',
                    'cluster_name': 'mist10-0',
                    'api_url': 'https://api.mist10-0.qe.red-chesterfield.com:6443',
                    'console_url': 'https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com',
                    'platform': 'openshift',
                    'region': 'unknown',
                    'health_status': 'healthy',
                    'connectivity_confirmed': True,
                    'detection_method': 'oc_deterministic_connection',
                    'platform_details': {'platform': 'openshift'},
                    'tools_available': {'oc': True},
                    'assessment_timestamp': '2025-08-26T23:21:55.682005',
                    'api_source': 'environment_assessment',
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
                
                # Execute complete Phase 0
                context = self.service.analyze_version_gap('ACM-22079', self.mist10_environment)
                
                # Verify complete foundation context structure
                self.assertIsNotNone(context.metadata)
                self.assertIsNotNone(context.jira_info)
                self.assertIsNotNone(context.version_context)
                self.assertIsNotNone(context.environment_baseline)
                self.assertIsNotNone(context.deployment_instruction)
                
                # Verify specific field values
                self.assertEqual(context.jira_info.jira_id, 'ACM-22079')
                self.assertEqual(context.version_context.target_version, '2.15.0')
                self.assertEqual(context.version_context.environment_version, '2.14.0-62')
                self.assertEqual(context.version_context.comparison_result, 'newer')
                self.assertEqual(context.environment_baseline.cluster_name, 'mist10-0')
                self.assertTrue(context.environment_baseline.connectivity_confirmed)
                
                # Verify agent inheritance readiness
                self.assertTrue(context.agent_inheritance_ready)
                self.assertTrue(context.validation_results['jira_id_present'])
                self.assertTrue(context.validation_results['environment_assessed'])
                self.assertTrue(context.validation_results['connectivity_confirmed'])
    
    # TEST 9: Error Handling and Edge Cases
    def test_error_handling_credential_parsing_failure(self):
        """Test error handling when credential parsing fails"""
        
        with patch.object(self.env_client, '_parse_environment_credentials') as mock_parse:
            # Mock credential parsing failure
            mock_parse.return_value = {
                'valid': False,
                'console_url': None,
                'username': None,
                'password': None,
                'cluster_name': None,
                'api_url': None
            }
            
            # Execute connection attempt
            connection_result = self.env_client._attempt_deterministic_connection(
                "invalid environment string", {}
            )
            
            # Verify graceful error handling
            self.assertFalse(connection_result['success'])
            self.assertEqual(connection_result['error'], 'invalid_credentials')
            self.assertIn('Could not parse credentials', connection_result['root_cause'])
    
    # TEST 10: Integration Test - Complete Workflow
    def test_complete_deterministic_workflow_integration(self):
        """Integration test covering complete deterministic environment workflow"""
        
        # Test both scenarios: successful connection and no-environment
        test_scenarios = [
            {
                'name': 'Successful MIST10 Connection',
                'environment': self.mist10_environment,
                'expected_connectivity': True,
                'expected_cluster': 'mist10-0',
                'expected_version': '2.14.0-62'
            },
            {
                'name': 'No Environment Available',
                'environment': None,
                'expected_connectivity': False,
                'expected_cluster': 'NO_TEST_ENVIRONMENT',
                'expected_version': 'environment_unavailable'
            }
        ]
        
        for scenario in test_scenarios:
            with self.subTest(scenario=scenario['name']):
                
                # Mock complete workflow based on scenario
                with patch.object(self.service, '_extract_jira_information') as mock_jira:
                    with patch.object(self.service, '_assess_environment_version') as mock_env:
                        
                        # Always mock JIRA extraction
                        mock_jira.return_value = {
                            'id': 'ACM-22079',
                            'title': 'Support digest-based upgrades via ClusterCurator for non-recommended upgrades',
                            'status': 'Review',
                            'fix_version': '2.15.0',
                            'priority': 'Critical',
                            'component': 'Cluster Lifecycle'
                        }
                        
                        if scenario['expected_connectivity']:
                            # Mock successful environment assessment
                            mock_env.return_value = {
                                'version': scenario['expected_version'],
                                'cluster_name': scenario['expected_cluster'],
                                'api_url': 'https://api.mist10-0.qe.red-chesterfield.com:6443',
                                'console_url': 'https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com',
                                'platform': 'openshift',
                                'region': 'unknown',
                                'health_status': 'healthy',
                                'connectivity_confirmed': True,
                                'detection_method': 'oc_deterministic_connection',
                                'platform_details': {'platform': 'openshift'},
                                'tools_available': {'oc': True},
                                'assessment_timestamp': '2025-08-26T23:21:55.682005',
                                'api_source': 'environment_assessment'
                            }
                        else:
                            # Mock no-environment assessment
                            mock_env.return_value = {
                                'version': scenario['expected_version'],
                                'cluster_name': scenario['expected_cluster'],
                                'api_url': 'unavailable',
                                'console_url': 'unavailable',
                                'platform': 'no_environment',
                                'region': 'unavailable',
                                'health_status': 'no_connection',
                                'connectivity_confirmed': False,
                                'detection_method': 'no_environment_available',
                                'platform_details': {
                                    'error': 'invalid_credentials',
                                    'root_cause': 'Could not parse credentials'
                                },
                                'tools_available': {},
                                'assessment_timestamp': '2025-08-26T23:22:18.063044',
                                'api_source': 'no_environment'
                            }
                        
                        # Execute complete workflow
                        context = self.service.analyze_version_gap('ACM-22079', scenario['environment'])
                        
                        # Verify workflow completion
                        self.assertIsNotNone(context)
                        self.assertEqual(context.environment_baseline.connectivity_confirmed, scenario['expected_connectivity'])
                        self.assertEqual(context.environment_baseline.cluster_name, scenario['expected_cluster'])
                        self.assertEqual(context.version_context.environment_version, scenario['expected_version'])
                        
                        # Both scenarios should be ready for agent inheritance
                        self.assertTrue(context.agent_inheritance_ready)


class TestPhase0DeterministicConnectionRealData(unittest.TestCase):
    """Test deterministic connection with exact real data formats"""
    
    def test_mist10_real_data_format(self):
        """Test with exact MIST10 real data format that was validated"""
        
        service = VersionIntelligenceService()
        
        with patch.object(service, '_extract_jira_information') as mock_jira:
            with patch.object(service, '_assess_environment_version') as mock_env:
                
                # Exact real JIRA data format
                mock_jira.return_value = {
                    'id': 'ACM-22079',
                    'title': 'Support digest-based upgrades via ClusterCurator for non-recommended upgrades',
                    'status': 'Review',
                    'fix_version': '2.15.0',
                    'priority': 'Critical',
                    'component': 'Cluster Lifecycle',
                    'description': 'Test description',
                    'assignee': 'Test assignee',
                    'reporter': 'Test reporter', 
                    'created': '2025-01-01T00:00:00.000+0000',
                    'updated': '2025-01-02T00:00:00.000+0000',
                    'labels': ['test'],
                    'api_source': 'jira_api'
                }
                
                # Exact real environment data format from successful test
                mock_env.return_value = {
                    'version': '2.14.0-62',
                    'cluster_name': 'mist10-0',
                    'api_url': 'https://api.mist10-0.qe.red-chesterfield.com:6443\u001b[0m',
                    'console_url': 'https://console.mist10-0.qe.red-chesterfield.com:6443\u001b[0m',
                    'platform': 'openshift',
                    'region': 'unknown',
                    'health_status': 'healthy',
                    'connectivity_confirmed': True,
                    'detection_method': 'oc_deterministic_connection',
                    'platform_details': {'platform': 'openshift'},
                    'tools_available': {'oc': True},
                    'assessment_timestamp': '2025-08-26T23:21:55.682005',
                    'api_source': 'environment_assessment'
                }
                
                # Execute with real environment string
                real_mist10_env = "Console: https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com, Creds: kubeadmin/Gz7oJ-IHZgq-5MIQ9-Kdhid"
                context = service.analyze_version_gap('ACM-22079', real_mist10_env)
                
                # Verify exact real data results
                self.assertEqual(context.version_context.target_version, '2.15.0')
                self.assertEqual(context.version_context.environment_version, '2.14.0-62')
                self.assertEqual(context.version_context.comparison_result, 'newer')
                self.assertEqual(context.environment_baseline.cluster_name, 'mist10-0')
                self.assertTrue(context.environment_baseline.connectivity_confirmed)
                self.assertIn('MINOR UPGRADE REQUIRED', context.deployment_instruction)
                self.assertIn('2.14.0-62 to 2.15.0', context.deployment_instruction)
    
    def test_qe6_no_environment_real_data_format(self):
        """Test with exact QE6 no-environment real data format that was validated"""
        
        service = VersionIntelligenceService()
        
        with patch.object(service, '_extract_jira_information') as mock_jira:
            with patch.object(service, '_assess_environment_version') as mock_env:
                
                # Exact real JIRA data format
                mock_jira.return_value = {
                    'id': 'ACM-22079',
                    'title': 'Support digest-based upgrades via ClusterCurator for non-recommended upgrades',
                    'status': 'Review',
                    'fix_version': '2.15.0',
                    'priority': 'Critical',
                    'component': 'Cluster Lifecycle',
                    'description': 'Test description',
                    'assignee': 'Test assignee',
                    'reporter': 'Test reporter',
                    'created': '2025-01-01T00:00:00.000+0000',
                    'updated': '2025-01-02T00:00:00.000+0000',
                    'labels': ['test'],
                    'api_source': 'jira_api'
                }
                
                # Exact real no-environment data format from validated test
                mock_env.return_value = {
                    'version': 'environment_unavailable',
                    'cluster_name': 'NO_TEST_ENVIRONMENT',
                    'api_url': 'unavailable',
                    'console_url': 'unavailable',
                    'platform': 'no_environment',
                    'region': 'unavailable',
                    'health_status': 'no_connection',
                    'connectivity_confirmed': False,
                    'detection_method': 'no_environment_available',
                    'platform_details': {
                        'platform': 'no_environment',
                        'error': 'invalid_credentials',
                        'root_cause': 'Could not parse credentials from: Console: https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red...',
                        'target_environment': 'Console: https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com, Creds: kubeadmin/BzDnQ-UFLYz-MpYpt-VAQae'
                    },
                    'tools_available': {},
                    'assessment_timestamp': '2025-08-26T23:22:18.063044',
                    'api_source': 'no_environment',
                    'raw_data': {
                        'connection_failure': {
                            'success': False,
                            'error': 'invalid_credentials',
                            'root_cause': 'Could not parse credentials from: Console: https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com, Creds: kubeadmin/BzDnQ-UFLYz-MpYpt-VAQae'
                        },
                        'target_environment': 'Console: https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com, Creds: kubeadmin/BzDnQ-UFLYz-MpYpt-VAQae',
                        'workflow_completion_mode': 'no_test_environment'
                    }
                }
                
                # Execute with no environment (defaults to qe6)
                context = service.analyze_version_gap('ACM-22079', None)
                
                # Verify exact real no-environment results
                self.assertEqual(context.version_context.target_version, '2.15.0')
                self.assertEqual(context.version_context.environment_version, 'environment_unavailable')
                self.assertEqual(context.version_context.comparison_result, 'no_environment')
                self.assertEqual(context.environment_baseline.cluster_name, 'NO_TEST_ENVIRONMENT')
                self.assertFalse(context.environment_baseline.connectivity_confirmed)
                self.assertIn('NO TEST ENVIRONMENT AVAILABLE', context.deployment_instruction)
                self.assertIn('invalid_credentials', context.deployment_instruction)


if __name__ == '__main__':
    # Run comprehensive deterministic connection tests
    unittest.main(verbosity=2)