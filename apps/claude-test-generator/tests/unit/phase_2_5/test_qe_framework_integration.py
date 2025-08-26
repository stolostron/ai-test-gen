#!/usr/bin/env python3
"""
Unit Tests for QE Intelligence Service - Framework Integration (Chunk 6)
======================================================================

Comprehensive unit tests for framework integration and observability connection.
Tests service registration, observability hooks, and cross-framework validation.
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch
from typing import Dict, Any, List

# Import path setup
def setup_test_paths():
    """Set up import paths for testing environment"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..', '..')
    ai_services_path = os.path.join(project_root, '.claude', 'ai-services')
    
    if ai_services_path not in sys.path:
        sys.path.insert(0, ai_services_path)
    
    return ai_services_path

setup_test_paths()

try:
    from qe_intelligence_service import QEIntelligenceService, QEIntelligenceResult
    IMPLEMENTATION_AVAILABLE = True
    print("✅ QE Intelligence Service implementation found for framework integration testing")
except ImportError as e:
    print(f"❌ QE Intelligence Service implementation not available: {e}")
    IMPLEMENTATION_AVAILABLE = False


class TestQEFrameworkIntegration(unittest.TestCase):
    """Unit tests for QE Intelligence Service framework integration functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        if not IMPLEMENTATION_AVAILABLE:
            cls.skipTest(cls, "QE Intelligence Service implementation not available")
    
    def setUp(self):
        """Set up each test"""
        self.qe_service = QEIntelligenceService()
    
    def test_framework_registration(self):
        """Test framework registration functionality"""
        registration = self.qe_service.register_with_framework()
        
        # Verify registration structure
        required_fields = [
            'service_id', 'service_name', 'phase', 'service_type',
            'framework_integration', 'capabilities', 'integration_endpoints'
        ]
        
        for field in required_fields:
            self.assertIn(field, registration)
        
        # Verify service identification
        self.assertEqual(registration['service_id'], 'qe_intelligence_service')
        self.assertEqual(registration['service_name'], 'QE Intelligence Service')
        self.assertEqual(registration['phase'], '2.5')
        self.assertEqual(registration['service_type'], 'ai_enhanced_intelligence_service')
        
        # Verify framework integration capabilities
        framework_integration = registration['framework_integration']
        expected_capabilities = [
            'progressive_context_aware',
            'observability_enabled',
            'cross_agent_validation_ready',
            'evidence_validation_integrated',
            'comprehensive_logging_active'
        ]
        
        for capability in expected_capabilities:
            self.assertTrue(framework_integration[capability])
        
        # Verify service capabilities
        capabilities = registration['capabilities']
        expected_capabilities = [
            'repository_analysis',
            'test_pattern_extraction',
            'coverage_gap_analysis',
            'strategic_recommendations',
            'evidence_validation',
            'ultrathink_insights'
        ]
        
        for capability in expected_capabilities:
            self.assertIn(capability, capabilities)
    
    def test_service_status_observability(self):
        """Test service status for observability integration"""
        status = self.qe_service.get_service_status()
        
        # Verify status structure
        required_sections = [
            'service_id', 'service_name', 'phase', 'status', 'health',
            'capabilities_operational', 'framework_integration_status',
            'performance_metrics', 'last_execution'
        ]
        
        for section in required_sections:
            self.assertIn(section, status)
        
        # Verify service operational status
        self.assertEqual(status['status'], 'operational')
        self.assertEqual(status['health'], 'excellent')
        
        # Verify capabilities are operational
        capabilities = status['capabilities_operational']
        for capability, operational in capabilities.items():
            self.assertTrue(operational, f"Capability {capability} should be operational")
        
        # Verify framework integration status
        integration_status = status['framework_integration_status']
        expected_integrations = [
            'progressive_context_integration',
            'observability_hooks',
            'cross_agent_validation',
            'evidence_validation_engine',
            'comprehensive_logging'
        ]
        
        for integration in expected_integrations:
            self.assertIn(integration, integration_status)
    
    def test_framework_health_metrics(self):
        """Test framework health metrics functionality"""
        health = self.qe_service.get_framework_health_metrics()
        
        # Verify health metrics structure
        required_sections = [
            'framework_integration_health',
            'component_health',
            'framework_compliance_metrics',
            'performance_indicators'
        ]
        
        for section in required_sections:
            self.assertIn(section, health)
        
        # Verify integration health
        integration_health = health['framework_integration_health']
        self.assertEqual(integration_health['overall_health'], 'excellent')
        self.assertEqual(integration_health['integration_completeness'], '100%')
        self.assertEqual(integration_health['service_availability'], '100%')
        
        # Verify component health
        component_health = health['component_health']
        expected_components = [
            'repository_analysis_engine',
            'test_pattern_extraction',
            'coverage_gap_analysis',
            'strategic_recommendations',
            'evidence_validation',
            'ultrathink_synthesis'
        ]
        
        for component in expected_components:
            self.assertEqual(component_health[component], 'operational')
        
        # Verify compliance metrics
        compliance = health['framework_compliance_metrics']
        compliance_areas = [
            'progressive_context_compliance',
            'evidence_validation_compliance',
            'cross_agent_validation_readiness',
            'observability_integration',
            'comprehensive_logging_compliance'
        ]
        
        for area in compliance_areas:
            self.assertEqual(compliance[area], '100%')
    
    def test_real_time_analysis_status(self):
        """Test real-time analysis status monitoring"""
        status = self.qe_service.get_real_time_analysis_status()
        
        # Verify real-time status structure
        required_sections = [
            'current_status',
            'service_readiness',
            'real_time_metrics',
            'monitoring_capabilities'
        ]
        
        for section in required_sections:
            self.assertIn(section, status)
        
        # Verify current status
        self.assertEqual(status['current_status'], 'ready_for_analysis')
        
        # Verify service readiness
        readiness = status['service_readiness']
        expected_services = [
            'qe_intelligence_service',
            'framework_integration',
            'observability_hooks',
            'evidence_validation'
        ]
        
        for service in expected_services:
            self.assertIn(service, readiness)
        
        # Verify monitoring capabilities
        monitoring = status['monitoring_capabilities']
        expected_capabilities = [
            'live_execution_tracking',
            'real_time_confidence_scoring',
            'progressive_context_monitoring',
            'evidence_validation_tracking',
            'business_impact_calculation'
        ]
        
        for capability in expected_capabilities:
            self.assertTrue(monitoring[capability])
    
    def test_framework_integration_status(self):
        """Test comprehensive framework integration status"""
        integration = self.qe_service.get_framework_integration_status()
        
        # Verify integration status structure
        required_sections = [
            'integration_status',
            'framework_components',
            'service_discovery',
            'framework_readiness'
        ]
        
        for section in required_sections:
            self.assertIn(section, integration)
        
        # Verify integration status
        self.assertEqual(integration['integration_status'], 'fully_integrated')
        
        # Verify framework components
        components = integration['framework_components']
        expected_components = [
            'progressive_context_architecture',
            'observability_system',
            'evidence_validation_engine',
            'cross_agent_validation',
            'comprehensive_logging'
        ]
        
        for component in expected_components:
            self.assertIn(component, components)
            self.assertIn('status', components[component])
            self.assertIn('capabilities', components[component])
        
        # Verify service discovery
        discovery = integration['service_discovery']
        self.assertTrue(discovery['registered'])
        self.assertTrue(discovery['discoverable'])
        self.assertTrue(discovery['endpoints_available'])
        
        # Verify framework readiness
        readiness = integration['framework_readiness']
        readiness_indicators = [
            'production_ready',
            'enterprise_grade',
            'observability_compliant',
            'evidence_validated'
        ]
        
        for indicator in readiness_indicators:
            self.assertTrue(readiness[indicator])
    
    def test_observability_registration(self):
        """Test observability system registration"""
        # This tests the internal registration method
        result = self.qe_service._register_with_observability_system()
        
        # Registration should complete successfully (even if mocked)
        self.assertTrue(result)
    
    def test_evidence_validation_registration(self):
        """Test evidence validation engine registration"""
        # This tests the internal registration method
        result = self.qe_service._register_with_evidence_validation_engine()
        
        # Registration should complete successfully (even if mocked)
        self.assertTrue(result)
    
    def test_cross_agent_validation_registration(self):
        """Test cross-agent validation system registration"""
        # This tests the internal registration method
        result = self.qe_service._register_with_cross_agent_validation()
        
        # Registration should complete successfully (even if mocked)
        self.assertTrue(result)
    
    def test_framework_execution_notifications(self):
        """Test framework execution start and completion notifications"""
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {'test': 'data'},
                'agent_d_environment': {'test': 'data'}
            }
        }
        
        # Test execution start notification (should not raise exception)
        try:
            self.qe_service.notify_framework_execution_start(test_context)
            start_notification_success = True
        except Exception:
            start_notification_success = False
        
        self.assertTrue(start_notification_success)
        
        # Create mock result for completion notification
        mock_result = Mock()
        mock_result.confidence_level = 0.942
        mock_result.execution_metadata = {'execution_time': 2.5}
        mock_result.strategic_recommendations = {
            'immediate_actions': ['action1', 'action2'],
            'business_impact_assessment': {'total_coverage_improvement': 20.5}
        }
        mock_result.evidence_validation = {'validation_status': 'passed_all_checks'}
        
        # Test execution completion notification (should not raise exception)
        try:
            self.qe_service.notify_framework_execution_complete(mock_result)
            completion_notification_success = True
        except Exception:
            completion_notification_success = False
        
        self.assertTrue(completion_notification_success)
    
    def test_enhanced_evidence_validation_integration(self):
        """Test enhanced evidence validation with framework integration"""
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {'customer_requirements': {'test': 'data'}},
                'agent_b_documentation': {'architecture_analysis': {'test': 'data'}},
                'agent_c_github': {'implementation_validation': {'test': 'data'}},
                'agent_d_environment': {'infrastructure_readiness': True}
            },
            'progressive_context_architecture': {
                'validation_status': 'passed',
                'context_completeness': 'comprehensive'
            }
        }
        
        test_recommendations = {
            'immediate_actions': [
                {'business_justification': 'test', 'evidence': 'test_evidence'}
            ],
            'evidence_traceability': {'test': 'data'},
            'business_impact_assessment': {'test': 'data'},
            'customer_success_metrics': {'test': 'data'},
            'implementation_guidance': {'test': 'data'}
        }
        
        validation = self.qe_service._validate_evidence_chain(test_context, test_recommendations)
        
        # Verify enhanced validation structure
        expected_fields = [
            'evidence_completeness',
            'traceability_score',
            'validation_results',
            'framework_integration',
            'blocking_conditions_checked',
            'validation_status',
            'evidence_chain_integrity',
            'cross_service_validation',
            'observability_hooks'
        ]
        
        for field in expected_fields:
            self.assertIn(field, validation)
        
        # Verify framework integration compliance
        framework_integration = validation['framework_integration']
        expected_compliance = [
            'progressive_context_compliance',
            'observability_integration',
            'cross_agent_validation_ready',
            'evidence_validation_engine_compatible',
            'framework_hooks_enabled',
            'service_discovery_registered'
        ]
        
        for compliance in expected_compliance:
            self.assertTrue(framework_integration[compliance])
        
        # Verify observability hooks
        hooks = validation['observability_hooks']
        self.assertTrue(hooks['evidence_tracking_enabled'])
        self.assertTrue(hooks['real_time_validation'])
        self.assertTrue(hooks['comprehensive_logging'])


class TestFrameworkIntegrationEndToEnd(unittest.TestCase):
    """Test end-to-end framework integration scenarios"""
    
    def setUp(self):
        """Set up each test"""
        if not IMPLEMENTATION_AVAILABLE:
            self.skipTest("QE Intelligence Service implementation not available")
        
        self.qe_service = QEIntelligenceService()
    
    def test_complete_framework_integration_workflow(self):
        """Test complete framework integration workflow"""
        # Step 1: Register with framework
        registration = self.qe_service.register_with_framework()
        self.assertEqual(registration['service_id'], 'qe_intelligence_service')
        
        # Step 2: Verify service status
        status = self.qe_service.get_service_status()
        self.assertEqual(status['status'], 'operational')
        
        # Step 3: Check framework health
        health = self.qe_service.get_framework_health_metrics()
        self.assertEqual(health['framework_integration_health']['overall_health'], 'excellent')
        
        # Step 4: Verify real-time monitoring
        realtime = self.qe_service.get_real_time_analysis_status()
        self.assertEqual(realtime['current_status'], 'ready_for_analysis')
        
        # Step 5: Check complete integration status
        integration = self.qe_service.get_framework_integration_status()
        self.assertEqual(integration['integration_status'], 'fully_integrated')
    
    def test_framework_aware_qe_analysis_execution(self):
        """Test QE analysis execution with framework awareness"""
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'customer_requirements': {
                        'amadeus_disconnected_env': True,
                        'three_tier_fallback': True
                    }
                },
                'agent_d_environment': {
                    'infrastructure_readiness': True
                }
            },
            'progressive_context_architecture': {
                'validation_status': 'passed',
                'context_completeness': 'comprehensive'
            }
        }
        
        # Execute QE analysis with framework integration
        result = self.qe_service.execute_qe_analysis(test_context)
        
        # Verify framework compliance in results
        self.assertIsInstance(result, QEIntelligenceResult)
        
        # Verify evidence validation includes framework compliance
        evidence_validation = result.evidence_validation
        self.assertIn('framework_integration', evidence_validation)
        self.assertTrue(evidence_validation['framework_integration']['observability_integration'])
        
        # Verify ultrathink insights include framework intelligence
        ultrathink_insights = result.ultrathink_insights
        self.assertIn('framework_compliance', ultrathink_insights)
        self.assertTrue(ultrathink_insights['framework_compliance']['observability_hooks_active'])


if __name__ == '__main__':
    print("🔗 QE Intelligence Service - Framework Integration Unit Tests")
    print("=" * 80)
    print("Testing Chunk 6 implementation: Framework integration and observability")
    print("🎯 Focus: Service registration, observability hooks, and framework compliance")
    print("=" * 80)
    
    unittest.main(verbosity=2)