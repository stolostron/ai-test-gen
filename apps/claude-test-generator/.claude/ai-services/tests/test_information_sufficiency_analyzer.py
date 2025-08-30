#!/usr/bin/env python3
"""
Comprehensive unit tests for InformationSufficiencyAnalyzer
Tests all methods, edge cases, and scoring calculations
"""

import unittest
import sys
import os
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from information_sufficiency_analyzer import InformationSufficiencyAnalyzer, SufficiencyScore


class TestInformationSufficiencyAnalyzer(unittest.TestCase):
    """Test cases for InformationSufficiencyAnalyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = InformationSufficiencyAnalyzer()
        
    def test_initialization(self):
        """Test analyzer initialization"""
        self.assertEqual(self.analyzer.MINIMUM_SUFFICIENCY_SCORE, 0.75)
        self.assertEqual(self.analyzer.FALLBACK_THRESHOLD, 0.60)
        
        # Verify weights sum to 1.0
        total_weight = sum(self.analyzer.SCORING_WEIGHTS.values())
        self.assertAlmostEqual(total_weight, 1.0, places=2)
        
        # Verify specific weights
        self.assertEqual(self.analyzer.SCORING_WEIGHTS['technical_details'], 0.35)
        self.assertEqual(self.analyzer.SCORING_WEIGHTS['pr_existence'], 0.20)
        self.assertEqual(self.analyzer.SCORING_WEIGHTS['testing_requirements'], 0.20)
        self.assertEqual(self.analyzer.SCORING_WEIGHTS['environment_info'], 0.15)
        self.assertEqual(self.analyzer.SCORING_WEIGHTS['business_context'], 0.10)
    
    def test_perfect_score_scenario(self):
        """Test scenario with all information present"""
        perfect_data = {
            'jira_info': {
                'jira_id': 'ACM-99999',
                'description': 'Complete feature with PR #123',
                'summary': 'Feature summary',
                'components': ['Component1']
            },
            'pr_references': ['#123', '#456'],
            'github_prs': [
                {'number': '123', 'files_changed': ['file1.go', 'file2.yaml']},
                {'number': '456', 'files_changed': ['file3.go']}
            ],
            'pr_discoveries': [
                {
                    'pr_number': '123',
                    'files_changed': ['file1.go'],
                    'deployment_components': ['Component1']
                }
            ],
            'acceptance_criteria': 'Clear acceptance criteria',
            'technical_design': 'Detailed technical design',
            'architecture_details': 'Architecture documented',
            'affected_components': ['Component1', 'Component2'],
            'integration_points': ['API1', 'API2'],
            'target_version': '2.12',
            'environment_platform': 'OpenShift',
            'deployment_environment': 'Production',
            'deployment_instruction': 'Deploy using operator',
            'feature_purpose': 'Clear purpose',
            'user_impact': 'Significant user impact',
            'business_value': 'High business value',
            'test_scenarios': ['Scenario 1', 'Scenario 2'],
            'success_conditions': 'Success defined'
        }
        
        result = self.analyzer.analyze_sufficiency(perfect_data)
        
        self.assertIsInstance(result, SufficiencyScore)
        self.assertGreaterEqual(result.overall_score, 0.90)
        self.assertTrue(result.can_proceed)
        self.assertFalse(result.needs_enhancement)
        self.assertEqual(len(result.missing_critical), 0)
    
    def test_no_pr_scenario(self):
        """Test scenario with no PR information"""
        no_pr_data = {
            'jira_info': {
                'jira_id': 'ACM-11111',
                'description': 'Feature without PR references',
                'summary': 'No PR feature'
            },
            'pr_references': [],
            'github_prs': [],
            'pr_discoveries': [],
            'acceptance_criteria': 'Some criteria',
            'technical_design': 'Some design',
            'affected_components': ['Component1'],
            'target_version': '2.12',
            'feature_purpose': 'Purpose',
            'user_impact': 'Impact',
            'business_value': 'Value'
        }
        
        result = self.analyzer.analyze_sufficiency(no_pr_data)
        
        # PR existence should be 0, affecting overall score by 20%
        self.assertEqual(result.component_scores['pr_existence'], 0.0)
        self.assertLess(result.overall_score, 0.80)  # Lost at least 20% from PR
        self.assertIn('GitHub PR references', ' '.join(result.missing_critical))
    
    def test_minimal_information_scenario(self):
        """Test with minimal information - should fail"""
        minimal_data = {
            'jira_info': {
                'jira_id': 'ACM-22222',
                'description': 'Minimal info'
            }
        }
        
        result = self.analyzer.analyze_sufficiency(minimal_data)
        
        self.assertLess(result.overall_score, 0.60)
        self.assertFalse(result.can_proceed)
        self.assertFalse(result.needs_enhancement)
        self.assertGreater(len(result.missing_critical), 0)
        self.assertGreater(len(result.recommendations), 0)
    
    def test_marginal_information_scenario(self):
        """Test with marginal information - should need enhancement"""
        marginal_data = {
            'jira_info': {
                'jira_id': 'ACM-33333',
                'description': 'Feature with PR #789',
                'summary': 'Marginal feature',
                'components': ['Component1']
            },
            'pr_references': ['#789'],
            'github_prs': [{'number': '789', 'files_changed': ['file.go']}],
            'technical_design': 'Basic design',
            'affected_components': ['Component1'],
            'feature_purpose': 'Some purpose',
            'user_impact': 'Some impact'
        }
        
        result = self.analyzer.analyze_sufficiency(marginal_data)
        
        self.assertGreaterEqual(result.overall_score, 0.60)
        self.assertLess(result.overall_score, 0.75)
        self.assertTrue(result.can_proceed)
        self.assertTrue(result.needs_enhancement)
    
    def test_technical_details_scoring(self):
        """Test technical details component scoring"""
        # Test with PRs but no design
        data_with_pr = {
            'pr_references': ['#123'],
            'github_prs': [{'number': '123'}],
            'jira_info': {'description': 'Has PR'}
        }
        score = self.analyzer._assess_technical_details(data_with_pr)
        self.assertEqual(score, 0.4)  # 40% for PR presence
        
        # Test with design but no PRs
        data_with_design = {
            'technical_design': 'Detailed design',
            'jira_info': {'description': 'Has design'}
        }
        score = self.analyzer._assess_technical_details(data_with_design)
        self.assertEqual(score, 0.3)  # 30% for design
        
        # Test with components
        data_with_components = {
            'affected_components': ['Comp1', 'Comp2'],
            'jira_info': {'description': 'Has components'}
        }
        score = self.analyzer._assess_technical_details(data_with_components)
        self.assertEqual(score, 0.3)  # 30% for components
        
        # Test with everything
        complete_data = {
            'pr_references': ['#123'],
            'technical_design': 'Design',
            'affected_components': ['Comp1'],
            'jira_info': {'description': 'Complete'}
        }
        score = self.analyzer._assess_technical_details(complete_data)
        self.assertEqual(score, 1.0)  # 100% for all present
    
    def test_pr_existence_scoring(self):
        """Test PR existence component scoring"""
        # No PRs
        no_pr_data = {'pr_references': [], 'github_prs': [], 'pr_discoveries': []}
        score = self.analyzer._assess_pr_existence(no_pr_data)
        self.assertEqual(score, 0.0)
        
        # Single PR without details
        single_pr_data = {
            'pr_references': ['#123'],
            'github_prs': [],
            'pr_discoveries': []
        }
        score = self.analyzer._assess_pr_existence(single_pr_data)
        self.assertEqual(score, 0.6)  # Base score for single PR
        
        # Multiple PRs
        multiple_pr_data = {
            'pr_references': ['#123', '#456'],
            'github_prs': [{'number': '789'}],
            'pr_discoveries': []
        }
        score = self.analyzer._assess_pr_existence(multiple_pr_data)
        self.assertGreaterEqual(score, 0.8)  # Higher score for multiple PRs
        
        # PRs with quality details
        quality_pr_data = {
            'pr_references': [],
            'github_prs': [],
            'pr_discoveries': [
                {
                    'pr_number': '123',
                    'files_changed': ['file1.go', 'file2.go'],
                    'deployment_components': ['Component1']
                }
            ]
        }
        score = self.analyzer._assess_pr_existence(quality_pr_data)
        self.assertGreater(score, 0.6)  # Higher than base due to quality
    
    def test_testing_requirements_scoring(self):
        """Test testing requirements component scoring"""
        # With acceptance criteria
        data_with_criteria = {
            'acceptance_criteria': 'Clear criteria',
            'jira_info': {'description': 'Feature description'}
        }
        score = self.analyzer._assess_testing_requirements(data_with_criteria)
        self.assertEqual(score, 0.5)  # 50% for criteria
        
        # With test scenarios
        data_with_scenarios = {
            'test_scenarios': ['Test 1', 'Test 2'],
            'jira_info': {'description': 'Feature'}
        }
        score = self.analyzer._assess_testing_requirements(data_with_scenarios)
        self.assertEqual(score, 0.3)  # 30% for scenarios
        
        # With success conditions
        data_with_success = {
            'success_conditions': 'Clear success metrics',
            'jira_info': {'description': 'Feature'}
        }
        score = self.analyzer._assess_testing_requirements(data_with_success)
        self.assertEqual(score, 0.2)  # 20% for success conditions
        
        # With keywords in description
        data_with_keywords = {
            'jira_info': {'description': 'Feature with acceptance test verify'}
        }
        score = self.analyzer._assess_testing_requirements(data_with_keywords)
        self.assertGreater(score, 0.0)  # Some score for keywords
    
    def test_environment_info_scoring(self):
        """Test environment info component scoring"""
        # Complete environment info
        complete_env_data = {
            'target_version': '2.12',
            'environment_platform': 'OpenShift',
            'deployment_instruction': 'Deploy using operator',
            'jira_info': {'description': 'Feature'}
        }
        score = self.analyzer._assess_environment_info(complete_env_data)
        self.assertEqual(score, 1.0)
        
        # Partial environment info
        partial_env_data = {
            'target_version': '2.12',
            'jira_info': {'description': 'Feature to deploy'}
        }
        score = self.analyzer._assess_environment_info(partial_env_data)
        self.assertGreater(score, 0.4)  # Version + keyword
        self.assertLess(score, 1.0)
    
    def test_business_context_scoring(self):
        """Test business context component scoring"""
        # Complete business context
        complete_biz_data = {
            'feature_purpose': 'Clear purpose',
            'user_impact': 'Significant impact',
            'business_value': 'High value',
            'jira_info': {'description': 'Feature', 'summary': 'Summary'}
        }
        score = self.analyzer._assess_business_context(complete_biz_data)
        self.assertEqual(score, 1.0)
        
        # Keywords in description
        keyword_data = {
            'jira_info': {
                'description': 'Feature for customer with business value and user benefit',
                'summary': 'Feature summary'
            }
        }
        score = self.analyzer._assess_business_context(keyword_data)
        self.assertGreater(score, 0.5)  # Good score from keywords
    
    def test_missing_information_identification(self):
        """Test identification of missing information"""
        # Data missing PRs and acceptance criteria
        incomplete_data = {
            'jira_info': {'description': 'Feature'},
            'technical_design': 'Some design',
            'affected_components': ['Comp1'],
            'target_version': '2.12',
            'business_value': 'Some value'
        }
        
        result = self.analyzer.analyze_sufficiency(incomplete_data)
        
        # Should identify missing PRs as critical
        pr_missing = any('PR' in item for item in result.missing_critical)
        self.assertTrue(pr_missing)
        
        # Should identify missing acceptance criteria
        criteria_missing = any('criteria' in item.lower() for item in result.missing_critical)
        self.assertTrue(criteria_missing)
    
    def test_recommendations_generation(self):
        """Test that appropriate recommendations are generated"""
        # Data with low PR score
        low_pr_data = {
            'jira_info': {'jira_id': 'ACM-44444', 'description': 'No PRs'},
            'pr_references': [],
            'technical_design': 'Good design',
            'acceptance_criteria': 'Good criteria'
        }
        
        result = self.analyzer.analyze_sufficiency(low_pr_data)
        
        # Should recommend adding PR links
        pr_recommendation = any('GitHub PR' in rec for rec in result.recommendations)
        self.assertTrue(pr_recommendation)
        
        # Should recommend searching for PRs
        search_recommendation = any('Search for PRs' in rec for rec in result.recommendations)
        self.assertTrue(search_recommendation)
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Empty data
        empty_result = self.analyzer.analyze_sufficiency({})
        self.assertLess(empty_result.overall_score, 0.5)
        self.assertFalse(empty_result.can_proceed)
        
        # None values in data
        none_data = {
            'jira_info': None,
            'pr_references': None,
            'acceptance_criteria': None
        }
        result = self.analyzer.analyze_sufficiency(none_data)
        self.assertIsInstance(result, SufficiencyScore)
        self.assertLess(result.overall_score, 0.5)
        
        # Data with empty strings
        empty_string_data = {
            'jira_info': {'description': ''},
            'pr_references': [],
            'acceptance_criteria': '',
            'technical_design': '',
            'business_value': ''
        }
        result = self.analyzer.analyze_sufficiency(empty_string_data)
        self.assertLess(result.overall_score, 0.5)
    
    def test_score_calculation_accuracy(self):
        """Test that weighted scores are calculated correctly"""
        # Create data that should give specific scores
        test_data = {
            'jira_info': {'description': 'Test'},
            'pr_references': ['#123'],  # Should give 0.6 for single PR
            'acceptance_criteria': 'Criteria',  # Should give 0.5 for criteria
            'target_version': '2.12',  # Should give 0.4 for version
            'feature_purpose': 'Purpose'  # Should give 0.4 for purpose
        }
        
        result = self.analyzer.analyze_sufficiency(test_data)
        
        # Calculate expected score manually
        expected_technical = 0.4 * 0.35  # PR presence only
        expected_pr = 0.6 * 0.20  # Single PR
        expected_testing = 0.5 * 0.20  # Criteria only
        expected_env = 0.4 * 0.15  # Version only
        expected_business = 0.4 * 0.10  # Purpose only
        
        expected_total = (expected_technical + expected_pr + expected_testing + 
                         expected_env + expected_business)
        
        self.assertAlmostEqual(result.overall_score, expected_total, places=2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
