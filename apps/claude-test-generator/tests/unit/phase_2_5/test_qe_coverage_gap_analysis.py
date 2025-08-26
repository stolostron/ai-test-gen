#!/usr/bin/env python3
"""
Unit Tests for QE Intelligence Service - Coverage Gap Analysis (Chunk 4)
=======================================================================

Comprehensive unit tests specifically for the coverage gap analysis implementation.
Tests each component of the gap analysis engine independently and validates the 
evidence-based, customer-focused prioritization logic.
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
    print("✅ QE Intelligence Service implementation found for gap analysis testing")
except ImportError as e:
    print(f"❌ QE Intelligence Service implementation not available: {e}")
    IMPLEMENTATION_AVAILABLE = False


class TestQECoverageGapAnalysis(unittest.TestCase):
    """Unit tests for QE Intelligence Service coverage gap analysis functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        if not IMPLEMENTATION_AVAILABLE:
            cls.skipTest(cls, "QE Intelligence Service implementation not available")
    
    def setUp(self):
        """Set up each test"""
        self.qe_service = QEIntelligenceService()
        
        # Test data for gap analysis
        self.test_customer_requirements = {
            'core_requirements': {
                'disconnected_environment': True,
                'three_tier_fallback': True,
                'manual_override_capability': True,
                'audit_compliance': True
            },
            'environment_requirements': {
                'air_gapped_operation': True,
                'local_registry_support': True
            },
            'customer_priority': 'amadeus_disconnected_environment_focus',
            'requirement_sources': ['agent_a_jira_analysis', 'agent_d_environment_intelligence']
        }
        
        self.test_patterns = {
            'proven_patterns': [
                'cluster_lifecycle_workflow_validation',
                'cluster_upgrade_workflow_validation',
                'ui_workflow_automation_patterns'
            ],
            'pattern_analysis': {
                'frequency_distribution': {
                    'upgrade_tests': 0.403,
                    'ui_validation': 0.256,
                    'cluster_mgmt': 0.371,
                    'automation_workflow_tests': 0.026,
                    'security_rbac_tests': 0.051
                },
                'total_test_basis': 78
            },
            'evidence_traceability': {
                'evidence_quality': 'high',
                'scan_method': 'real_github_api'
            }
        }
    
    def test_extract_comprehensive_customer_requirements(self):
        """Test customer requirements extraction from progressive context"""
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'customer_requirements': {
                        'amadeus_disconnected_env': True,
                        'three_tier_fallback': True,
                        'manual_override_capability': True
                    }
                },
                'agent_d_environment': {
                    'environment_constraints': {
                        'security_requirements': ['rbac', 'audit_trail']
                    }
                },
                'agent_b_documentation': {
                    'feature_requirements': {'api_reliability': 'high_availability_required'}
                },
                'agent_c_github': {
                    'implementation_requirements': {'acm_version_compatibility': 'ACM 2.15+'}
                }
            }
        }
        
        requirements = self.qe_service._extract_comprehensive_customer_requirements(test_context)
        
        # Verify core requirements structure
        self.assertIn('core_requirements', requirements)
        self.assertIn('environment_requirements', requirements)
        self.assertIn('technical_requirements', requirements)
        self.assertIn('operational_requirements', requirements)
        
        # Verify Amadeus-specific requirements
        self.assertTrue(requirements['core_requirements']['disconnected_environment'])
        self.assertTrue(requirements['core_requirements']['three_tier_fallback'])
        self.assertTrue(requirements['environment_requirements']['air_gapped_operation'])
        
        # Verify customer priority
        self.assertEqual(requirements['customer_priority'], 'amadeus_disconnected_environment_focus')
        
        # Verify requirement sources
        expected_sources = [
            'agent_a_jira_analysis',
            'agent_d_environment_intelligence',
            'agent_b_documentation_analysis',
            'agent_c_implementation_validation'
        ]
        for source in expected_sources:
            self.assertIn(source, requirements['requirement_sources'])
    
    def test_assess_requirement_coverage(self):
        """Test requirement coverage assessment against test patterns"""
        coverage_assessment = self.qe_service._assess_requirement_coverage(
            self.test_customer_requirements, 
            self.test_patterns
        )
        
        # Verify coverage assessment structure
        expected_areas = [
            'disconnected_environment_simulation',
            'three_tier_fallback_edge_cases',
            'upgrade_workflow_coverage',
            'automation_coverage',
            'security_coverage'
        ]
        
        for area in expected_areas:
            self.assertIn(area, coverage_assessment)
            area_assessment = coverage_assessment[area]
            
            # Verify required fields
            self.assertIn('current_coverage', area_assessment)
            self.assertIn('requirement_level', area_assessment)
            self.assertIn('customer_impact', area_assessment)
            self.assertIn('gap_severity', area_assessment)
            
            # Verify coverage is a valid percentage
            coverage = area_assessment['current_coverage']
            self.assertIsInstance(coverage, (int, float))
            self.assertGreaterEqual(coverage, 0.0)
            self.assertLessEqual(coverage, 1.0)
            
            # Verify requirement levels are valid
            self.assertIn(area_assessment['requirement_level'], ['critical', 'high', 'medium', 'low'])
            
            # Verify gap severity is valid
            self.assertIn(area_assessment['gap_severity'], ['high', 'medium', 'low'])
        
        # Verify overall assessment
        self.assertIn('overall_assessment', coverage_assessment)
        overall = coverage_assessment['overall_assessment']
        self.assertIn('pattern_effectiveness', overall)
        self.assertIn('coverage_completeness', overall)
    
    def test_assess_disconnected_coverage(self):
        """Test disconnected environment coverage assessment"""
        # Test with no disconnected patterns
        patterns_no_disconnected = ['cluster_lifecycle_workflow_validation', 'ui_workflow_automation']
        frequencies = {'ecosystem_integration_tests': 0.1}
        
        coverage = self.qe_service._assess_disconnected_coverage(patterns_no_disconnected, frequencies)
        self.assertLess(coverage, 0.2)  # Should be low without disconnected patterns
        
        # Test with disconnected patterns
        patterns_with_disconnected = ['disconnected_environment_simulation', 'air_gapped_testing']
        coverage_with_patterns = self.qe_service._assess_disconnected_coverage(patterns_with_disconnected, frequencies)
        self.assertGreater(coverage_with_patterns, coverage)  # Should be higher with relevant patterns
    
    def test_assess_fallback_coverage(self):
        """Test three-tier fallback algorithm coverage assessment"""
        # Test with no fallback patterns
        patterns_no_fallback = ['ui_workflow_automation', 'basic_cluster_tests']
        frequencies = {'upgrade_tests': 0.4}
        
        coverage = self.qe_service._assess_fallback_coverage(patterns_no_fallback, frequencies)
        self.assertGreater(coverage, 0.0)  # Should have some coverage from upgrade tests
        
        # Test with fallback patterns
        patterns_with_fallback = ['three_tier_fallback_verification', 'upgrade_algorithm_testing']
        coverage_with_patterns = self.qe_service._assess_fallback_coverage(patterns_with_fallback, frequencies)
        self.assertGreater(coverage_with_patterns, coverage)  # Should be higher with relevant patterns
    
    def test_identify_evidence_based_gaps(self):
        """Test evidence-based gap identification"""
        # Create test coverage assessment with known gaps
        coverage_assessment = {
            'disconnected_environment_simulation': {
                'current_coverage': 0.2,  # Below critical threshold (0.8)
                'requirement_level': 'critical',
                'customer_impact': 'amadeus_requirement',
                'gap_severity': 'high'
            },
            'upgrade_workflow_coverage': {
                'current_coverage': 0.5,  # Below high threshold (0.7)
                'requirement_level': 'high',
                'customer_impact': 'core_functionality',
                'gap_severity': 'medium'
            },
            'security_coverage': {
                'current_coverage': 0.9,  # Above high threshold
                'requirement_level': 'high',
                'customer_impact': 'enterprise_compliance',
                'gap_severity': 'low'
            }
        }
        
        identified_gaps = self.qe_service._identify_evidence_based_gaps(coverage_assessment, self.test_patterns)
        
        # Verify gap identification structure
        self.assertIn('raw_gaps', identified_gaps)
        raw_gaps = identified_gaps['raw_gaps']
        
        # Should identify 2 gaps (disconnected and upgrade) but not security
        self.assertEqual(len(raw_gaps), 2)
        
        # Verify gap details
        gap_areas = [gap['area'] for gap in raw_gaps]
        self.assertIn('disconnected_environment_simulation', gap_areas)
        self.assertIn('upgrade_workflow_coverage', gap_areas)
        self.assertNotIn('security_coverage', gap_areas)  # Above threshold
        
        # Verify gap structure
        for gap in raw_gaps:
            self.assertIn('area', gap)
            self.assertIn('current_coverage', gap)
            self.assertIn('requirement_level', gap)
            self.assertIn('gap_severity', gap)
            self.assertIn('customer_impact', gap)
            self.assertIn('evidence', gap)
            self.assertIn('actionability', gap)
    
    def test_is_significant_gap(self):
        """Test gap significance determination logic"""
        # Test critical requirement thresholds
        self.assertTrue(self.qe_service._is_significant_gap(0.5, 'critical'))  # Below 80%
        self.assertFalse(self.qe_service._is_significant_gap(0.9, 'critical'))  # Above 80%
        
        # Test high requirement thresholds
        self.assertTrue(self.qe_service._is_significant_gap(0.6, 'high'))  # Below 70%
        self.assertFalse(self.qe_service._is_significant_gap(0.8, 'high'))  # Above 70%
        
        # Test medium requirement thresholds
        self.assertTrue(self.qe_service._is_significant_gap(0.5, 'medium'))  # Below 60%
        self.assertFalse(self.qe_service._is_significant_gap(0.7, 'medium'))  # Above 60%
        
        # Test edge cases
        self.assertTrue(self.qe_service._is_significant_gap(0.79, 'critical'))  # Just below threshold
        self.assertFalse(self.qe_service._is_significant_gap(0.80, 'critical'))  # Exactly at threshold
    
    def test_prioritize_gaps_customer_focused(self):
        """Test customer-focused gap prioritization"""
        # Create test gaps with different characteristics
        test_gaps = {
            'raw_gaps': [
                {
                    'area': 'disconnected_environment_simulation',
                    'requirement_level': 'critical',
                    'customer_impact': 'amadeus_requirement',
                    'actionability': 'high_actionability'
                },
                {
                    'area': 'security_coverage',
                    'requirement_level': 'high',
                    'customer_impact': 'enterprise_compliance',
                    'actionability': 'medium_actionability'
                },
                {
                    'area': 'automation_coverage',
                    'requirement_level': 'medium',
                    'customer_impact': 'operational_efficiency',
                    'actionability': 'requires_new_pattern_development'
                }
            ]
        }
        
        prioritized_gaps = self.qe_service._prioritize_gaps_customer_focused(
            test_gaps, 
            self.test_customer_requirements
        )
        
        # Verify prioritization structure
        expected_categories = ['critical_gaps', 'high_gaps', 'medium_gaps', 'low_gaps']
        for category in expected_categories:
            self.assertIn(category, prioritized_gaps)
        
        # Verify Amadeus gap gets highest priority (critical category)
        critical_gaps = prioritized_gaps['critical_gaps']
        self.assertGreater(len(critical_gaps), 0)
        
        amadeus_gap = next((g for g in critical_gaps if 'amadeus' in g.get('customer_impact', '')), None)
        self.assertIsNotNone(amadeus_gap, "Amadeus gap should be in critical category")
        
        # Verify priority scores are assigned
        for category in expected_categories:
            for gap in prioritized_gaps[category]:
                self.assertIn('priority_score', gap)
                self.assertIn('business_justification', gap)
                self.assertIsInstance(gap['priority_score'], (int, float))
        
        # Verify Amadeus focus is applied
        self.assertTrue(prioritized_gaps['amadeus_focus_applied'])
    
    def test_calculate_realistic_gap_percentages(self):
        """Test realistic gap percentage calculation"""
        # Create test prioritized gaps
        prioritized_gaps = {
            'critical_gaps': [
                {'area': 'disconnected_environment_simulation'},
                {'area': 'three_tier_fallback_edge_cases'}
            ],
            'high_gaps': [
                {'area': 'security_coverage'}
            ],
            'medium_gaps': [
                {'area': 'automation_coverage'}
            ],
            'low_gaps': []
        }
        
        gap_percentages = self.qe_service._calculate_realistic_gap_percentages(
            prioritized_gaps, 
            self.test_patterns
        )
        
        # Verify gap percentage structure
        expected_fields = [
            'critical_gap_percentage',
            'high_gap_percentage', 
            'medium_gap_percentage',
            'low_gap_percentage',
            'total_calculated_gap',
            'calculation_method',
            'baseline_test_count',
            'confidence_level'
        ]
        
        for field in expected_fields:
            self.assertIn(field, gap_percentages)
        
        # Verify percentages are reasonable
        self.assertGreater(gap_percentages['critical_gap_percentage'], 0)
        self.assertGreater(gap_percentages['high_gap_percentage'], 0)
        self.assertGreater(gap_percentages['medium_gap_percentage'], 0)
        self.assertEqual(gap_percentages['low_gap_percentage'], 0)  # No low gaps
        
        # Verify total equals sum of parts
        expected_total = (
            gap_percentages['critical_gap_percentage'] +
            gap_percentages['high_gap_percentage'] +
            gap_percentages['medium_gap_percentage'] +
            gap_percentages['low_gap_percentage']
        )
        self.assertEqual(gap_percentages['total_calculated_gap'], expected_total)
        
        # Verify baseline test count matches input
        self.assertEqual(gap_percentages['baseline_test_count'], 78)
    
    def test_assess_customer_gap_alignment(self):
        """Test customer gap alignment assessment"""
        # Create test gaps with Amadeus focus
        test_gaps = {
            'critical_gaps': [
                {'area': 'disconnected_environment_simulation', 'customer_impact': 'amadeus_requirement'},
                {'area': 'three_tier_fallback_edge_cases', 'customer_impact': 'reliability_assurance'}
            ],
            'high_gaps': [
                {'area': 'security_coverage', 'customer_impact': 'enterprise_compliance'}
            ],
            'medium_gaps': [],
            'low_gaps': []
        }
        
        alignment_assessment = self.qe_service._assess_customer_gap_alignment(
            test_gaps, 
            self.test_customer_requirements
        )
        
        # Verify alignment assessment structure
        expected_fields = [
            'amadeus_alignment_score',
            'disconnected_environment_coverage',
            'critical_requirement_coverage',
            'customer_priority_alignment',
            'requirement_satisfaction_outlook'
        ]
        
        for field in expected_fields:
            self.assertIn(field, alignment_assessment)
        
        # Verify Amadeus alignment (1 out of 2 critical gaps = 50%)
        self.assertAlmostEqual(alignment_assessment['amadeus_alignment_score'], 0.5, places=2)
        
        # Verify disconnected environment coverage is detected
        self.assertTrue(alignment_assessment['disconnected_environment_coverage'])
        
        # Verify customer priority alignment
        self.assertIn(alignment_assessment['customer_priority_alignment'], ['high', 'medium', 'low'])
        
        # Verify satisfaction outlook
        self.assertIn(alignment_assessment['requirement_satisfaction_outlook'], [
            'high_satisfaction_expected',
            'good_satisfaction_with_gap_resolution',
            'moderate_satisfaction_gaps_addressable',
            'satisfaction_requires_comprehensive_gap_resolution'
        ])
    
    def test_calculate_gap_analysis_confidence(self):
        """Test gap analysis confidence calculation"""
        # Create test gaps and patterns with known characteristics
        test_gaps = {
            'critical_gaps': [{'area': 'test_gap'}],
            'high_gaps': [],
            'medium_gaps': [],
            'low_gaps': []
        }
        
        high_quality_patterns = {
            'proven_patterns': ['pattern1', 'pattern2', 'pattern3', 'pattern4', 
                              'pattern5', 'pattern6', 'pattern7', 'pattern8'],  # 8+ patterns
            'pattern_analysis': {'total_test_basis': 60},  # 50+ tests
            'evidence_traceability': {'evidence_quality': 'high'}
        }
        
        confidence = self.qe_service._calculate_gap_analysis_confidence(test_gaps, high_quality_patterns)
        
        # Verify confidence is a valid float between 0 and 1
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
        
        # Should be high confidence with good inputs
        self.assertGreater(confidence, 0.8)
        
        # Test with lower quality inputs
        low_quality_patterns = {
            'proven_patterns': ['pattern1', 'pattern2'],  # Few patterns
            'pattern_analysis': {'total_test_basis': 20},  # Few tests
            'evidence_traceability': {'evidence_quality': 'medium'}
        }
        
        low_confidence = self.qe_service._calculate_gap_analysis_confidence(test_gaps, low_quality_patterns)
        self.assertLess(low_confidence, confidence)  # Should be lower confidence
    
    def test_generate_gap_recommendations_preview(self):
        """Test gap recommendations preview generation"""
        # Create test gaps representing different scenarios
        test_gaps = {
            'critical_gaps': [
                {'area': 'disconnected_environment_simulation'},
                {'area': 'three_tier_fallback_edge_cases'}
            ],
            'high_gaps': [
                {'area': 'security_coverage'}
            ]
        }
        
        recommendations = self.qe_service._generate_gap_recommendations_preview(test_gaps)
        
        # Verify recommendations structure
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Verify specific recommendations for known gap types
        recommendation_text = ' '.join(recommendations).lower()
        self.assertIn('disconnected', recommendation_text)  # Should recommend disconnected environment tests
        self.assertIn('fallback', recommendation_text)      # Should recommend fallback algorithm tests
        
        # Test with no gaps
        empty_gaps = {'critical_gaps': [], 'high_gaps': [], 'medium_gaps': [], 'low_gaps': []}
        empty_recommendations = self.qe_service._generate_gap_recommendations_preview(empty_gaps)
        
        self.assertEqual(len(empty_recommendations), 1)
        self.assertIn('maintain', empty_recommendations[0].lower())  # Should suggest maintaining standards
    
    def test_end_to_end_gap_analysis(self):
        """Test complete end-to-end gap analysis workflow"""
        # Create comprehensive test context
        test_context = {
            'agent_contributions': {
                'agent_a_jira': {
                    'customer_requirements': {
                        'amadeus_disconnected_env': True,
                        'three_tier_fallback': True,
                        'manual_override_capability': True
                    }
                },
                'agent_d_environment': {
                    'environment_constraints': {
                        'security_requirements': ['rbac', 'audit_trail']
                    }
                }
            }
        }
        
        # Execute complete QE analysis to test gap analysis integration
        result = self.qe_service.execute_qe_analysis(test_context)
        gap_analysis = result.coverage_gap_analysis
        
        # Verify complete gap analysis structure
        required_fields = [
            'identified_gaps',
            'gap_calculation_details',
            'customer_alignment_assessment',
            'evidence_traceability',
            'total_gap_percentage',
            'gap_analysis_method',
            'priority_assessment',
            'analysis_confidence',
            'recommendations_preview'
        ]
        
        for field in required_fields:
            self.assertIn(field, gap_analysis)
        
        # Verify gap categorization
        identified_gaps = gap_analysis['identified_gaps']
        for category in ['critical_gaps', 'high_gaps', 'medium_gaps', 'low_gaps']:
            self.assertIn(category, identified_gaps)
            self.assertIsInstance(identified_gaps[category], list)
        
        # Verify total gap percentage is reasonable (should match expected 18.8%)
        total_gap = gap_analysis['total_gap_percentage']
        self.assertIsInstance(total_gap, (int, float))
        self.assertGreater(total_gap, 0)
        self.assertLess(total_gap, 50)  # Should be reasonable percentage
        
        # Verify analysis confidence
        confidence = gap_analysis['analysis_confidence']
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
        
        # Verify evidence traceability
        evidence = gap_analysis['evidence_traceability']
        self.assertIn('repository_evidence', evidence)
        self.assertIn('pattern_evidence', evidence)
        self.assertIn('customer_evidence', evidence)


class TestGapAnalysisEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions for gap analysis"""
    
    def setUp(self):
        """Set up each test"""
        if not IMPLEMENTATION_AVAILABLE:
            self.skipTest("QE Intelligence Service implementation not available")
        
        self.qe_service = QEIntelligenceService()
    
    def test_empty_context_handling(self):
        """Test gap analysis with empty or minimal context"""
        # Test with completely empty context
        empty_result = self.qe_service.execute_qe_analysis({})
        self.assertIsNotNone(empty_result.coverage_gap_analysis)
        
        # Test with minimal context
        minimal_context = {'agent_contributions': {}}
        minimal_result = self.qe_service.execute_qe_analysis(minimal_context)
        self.assertIsNotNone(minimal_result.coverage_gap_analysis)
        
        # Should still have valid structure even with minimal input
        gap_analysis = minimal_result.coverage_gap_analysis
        self.assertIn('total_gap_percentage', gap_analysis)
        self.assertIn('analysis_confidence', gap_analysis)
    
    def test_no_gaps_scenario(self):
        """Test scenario where no significant gaps are identified"""
        # Mock high coverage for all areas
        with patch.object(self.qe_service, '_is_significant_gap', return_value=False):
            result = self.qe_service.execute_qe_analysis({})
            gaps = result.coverage_gap_analysis['identified_gaps']
            
            # Should have empty gap categories
            for category in ['critical_gaps', 'high_gaps', 'medium_gaps', 'low_gaps']:
                self.assertEqual(len(gaps[category]), 0)
            
            # Should still provide recommendations (maintain standards)
            recommendations = result.coverage_gap_analysis['recommendations_preview']
            self.assertGreater(len(recommendations), 0)
    
    def test_invalid_input_handling(self):
        """Test handling of invalid or malformed inputs"""
        # Test with None patterns
        coverage_assessment = {
            'test_area': {
                'current_coverage': 0.5,
                'requirement_level': 'high',
                'customer_impact': 'test_impact',
                'gap_severity': 'medium'
            }
        }
        
        # Should not crash with None patterns
        gaps = self.qe_service._identify_evidence_based_gaps(coverage_assessment, None)
        self.assertIn('raw_gaps', gaps)
        
        # Test with malformed patterns
        malformed_patterns = {'invalid_structure': True}
        gaps_malformed = self.qe_service._identify_evidence_based_gaps(coverage_assessment, malformed_patterns)
        self.assertIn('raw_gaps', gaps_malformed)


if __name__ == '__main__':
    print("🧪 QE Intelligence Service - Coverage Gap Analysis Unit Tests")
    print("=" * 80)
    print("Testing Chunk 4 implementation: Evidence-based gap analysis with customer prioritization")
    print("🎯 Focus: Gap identification, prioritization, and customer alignment")
    print("=" * 80)
    
    unittest.main(verbosity=2)