#!/usr/bin/env python3
"""
Information Sufficiency Analyzer for Agent A - JIRA Intelligence
Determines if collected information is sufficient for comprehensive test planning
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class SufficiencyScore:
    """Result of sufficiency analysis"""
    overall_score: float
    component_scores: Dict[str, float]
    missing_critical: List[str]
    missing_optional: List[str]
    recommendations: List[str]
    can_proceed: bool
    needs_enhancement: bool


class InformationSufficiencyAnalyzer:
    """
    Analyzes collected information to determine if sufficient for test planning
    Uses weighted scoring based on critical information requirements
    """
    
    # Scoring thresholds
    MINIMUM_SUFFICIENCY_SCORE = 0.75  # 75% minimum for proceeding
    FALLBACK_THRESHOLD = 0.60         # 60% with warnings and enhancements
    
    # Updated scoring weights based on requirements
    SCORING_WEIGHTS = {
        'technical_details': 0.35,      # Increased from 0.30
        'pr_existence': 0.20,           # New direct PR impact
        'testing_requirements': 0.20,    # Same
        'environment_info': 0.15,        # Same
        'business_context': 0.10         # Reduced from 0.25
    }
    
    def __init__(self):
        """Initialize the analyzer"""
        self.critical_requirements = self._define_critical_requirements()
        self.optional_requirements = self._define_optional_requirements()
        
    def analyze_sufficiency(self, collected_data: Dict) -> SufficiencyScore:
        """
        Analyze if collected information is sufficient for test planning
        
        Args:
            collected_data: All collected information from JIRA and other sources
            
        Returns:
            SufficiencyScore with detailed analysis results
        """
        logger.info("Analyzing information sufficiency for test planning")
        
        # Calculate component scores
        component_scores = {
            'technical_details': self._assess_technical_details(collected_data),
            'pr_existence': self._assess_pr_existence(collected_data),
            'testing_requirements': self._assess_testing_requirements(collected_data),
            'environment_info': self._assess_environment_info(collected_data),
            'business_context': self._assess_business_context(collected_data)
        }
        
        # Calculate weighted overall score
        overall_score = sum(
            component_scores[component] * self.SCORING_WEIGHTS[component]
            for component in component_scores
        )
        
        # Identify missing information
        missing_critical, missing_optional = self._identify_missing_information(
            collected_data, component_scores
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            component_scores, missing_critical, missing_optional
        )
        
        # Determine if can proceed
        can_proceed = overall_score >= self.FALLBACK_THRESHOLD
        needs_enhancement = (
            overall_score < self.MINIMUM_SUFFICIENCY_SCORE and 
            overall_score >= self.FALLBACK_THRESHOLD
        )
        
        score = SufficiencyScore(
            overall_score=overall_score,
            component_scores=component_scores,
            missing_critical=missing_critical,
            missing_optional=missing_optional,
            recommendations=recommendations,
            can_proceed=can_proceed,
            needs_enhancement=needs_enhancement
        )
        
        logger.info(f"Sufficiency analysis complete: Score={overall_score:.2f}, "
                   f"Can proceed={can_proceed}, Needs enhancement={needs_enhancement}")
        
        return score
    
    def _assess_technical_details(self, data: Dict) -> float:
        """Assess technical implementation details (35% weight)"""
        score = 0.0
        max_points = 1.0
        
        # Check for code changes/PRs (40% of technical details)
        if data.get('pr_references') or data.get('github_prs'):
            score += 0.4
        elif data.get('jira_info') and data.get('jira_info', {}).get('description', '').lower().count('pr') > 0:
            score += 0.2  # Partial credit for PR mentions
            
        # Check for architecture/design info (30%)
        if (data.get('technical_design') or 
            data.get('architecture_details') or
            (data.get('jira_info') and 'design' in data.get('jira_info', {}).get('description', '').lower())):
            score += 0.3
            
        # Check for component/integration details (30%)
        if (data.get('affected_components') or 
            data.get('integration_points') or
            data.get('jira_info', {}).get('components')):
            score += 0.3
            
        return min(score, max_points)
    
    def _assess_pr_existence(self, data: Dict) -> float:
        """Assess PR existence and quality (20% weight)"""
        score = 0.0
        
        pr_count = 0
        pr_quality = 0.0
        
        # Check various PR sources
        if data.get('pr_references'):
            pr_count = len(data['pr_references'])
        
        if data.get('github_prs'):
            pr_count += len(data['github_prs'])
            
        # Check PR discovery results
        if data.get('pr_discoveries'):
            pr_count += len(data['pr_discoveries'])
            # Assess PR quality from discoveries
            for pr in data['pr_discoveries']:
                if pr.get('files_changed'):
                    pr_quality += 0.2
                if pr.get('deployment_components'):
                    pr_quality += 0.2
                    
        # Calculate score based on PR existence and quality
        if pr_count == 0:
            return 0.0
        elif pr_count == 1:
            return 0.6 + (pr_quality / pr_count) * 0.4
        else:  # Multiple PRs
            return min(1.0, 0.8 + (pr_quality / pr_count) * 0.2)
    
    def _assess_testing_requirements(self, data: Dict) -> float:
        """Assess testing requirements clarity (20% weight)"""
        score = 0.0
        
        # Check for acceptance criteria (50%)
        if (data.get('acceptance_criteria') or
            'acceptance' in data.get('jira_info', {}).get('description', '').lower() or
            'criteria' in data.get('jira_info', {}).get('description', '').lower()):
            score += 0.5
            
        # Check for test scenarios/cases (30%)
        if (data.get('test_scenarios') or
            data.get('test_cases') or
            'test' in data.get('jira_info', {}).get('description', '').lower()):
            score += 0.3
            
        # Check for success conditions (20%)
        if (data.get('success_conditions') or
            'success' in data.get('jira_info', {}).get('description', '').lower() or
            'verify' in data.get('jira_info', {}).get('description', '').lower()):
            score += 0.2
            
        return score
    
    def _assess_environment_info(self, data: Dict) -> float:
        """Assess environment and deployment information (15% weight)"""
        score = 0.0
        
        # Check for version information (40%)
        if (data.get('target_version') or 
            data.get('version_context')):
            score += 0.4
            
        # Check for platform/environment details (30%)
        if (data.get('environment_platform') or
            data.get('deployment_environment') or
            data.get('environment_baseline')):
            score += 0.3
            
        # Check for deployment instructions (30%)
        if (data.get('deployment_instruction') or
            data.get('deployment_status') or
            'deploy' in data.get('jira_info', {}).get('description', '').lower()):
            score += 0.3
            
        return score
    
    def _assess_business_context(self, data: Dict) -> float:
        """Assess business context and requirements (10% weight)"""
        score = 0.0
        
        # Check for feature purpose (40%)
        if (data.get('feature_purpose') or
            data.get('jira_info', {}).get('summary') or
            data.get('jira_info', {}).get('description')):
            score += 0.4
            
        # Check for user impact (30%)
        if (data.get('user_impact') or
            data.get('customer_impact') or
            'customer' in data.get('jira_info', {}).get('description', '').lower() or
            'user' in data.get('jira_info', {}).get('description', '').lower()):
            score += 0.3
            
        # Check for business value (30%)
        if (data.get('business_value') or
            data.get('strategic_value') or
            'value' in data.get('jira_info', {}).get('description', '').lower() or
            'benefit' in data.get('jira_info', {}).get('description', '').lower()):
            score += 0.3
            
        return score
    
    def _identify_missing_information(self, data: Dict, scores: Dict) -> Tuple[List[str], List[str]]:
        """Identify missing critical and optional information"""
        missing_critical = []
        missing_optional = []
        
        # Critical: PR information
        if scores['pr_existence'] < 0.5:
            missing_critical.append("GitHub PR references - No implementation details found")
            
        # Critical: Technical details
        if scores['technical_details'] < 0.5:
            if not (data.get('pr_references') or data.get('github_prs')):
                missing_critical.append("Code changes/PR links")
            if not (data.get('technical_design') or data.get('architecture_details')):
                missing_critical.append("Technical design or architecture details")
            if not (data.get('affected_components') or data.get('integration_points')):
                missing_critical.append("Affected components and integration points")
                
        # Critical: Testing requirements
        if scores['testing_requirements'] < 0.5:
            if not data.get('acceptance_criteria'):
                missing_critical.append("Acceptance criteria or success conditions")
            if not (data.get('test_scenarios') or data.get('test_cases')):
                missing_optional.append("Specific test scenarios or validation steps")
                
        # Optional: Environment details
        if scores['environment_info'] < 0.5:
            if not data.get('target_version'):
                missing_optional.append("Target version information")
            if not data.get('deployment_environment'):
                missing_optional.append("Deployment environment details")
                
        # Optional: Business context
        if scores['business_context'] < 0.5:
            if not data.get('user_impact'):
                missing_optional.append("User impact description")
            if not data.get('business_value'):
                missing_optional.append("Business value statement")
                
        return missing_critical, missing_optional
    
    def _generate_recommendations(self, scores: Dict, missing_critical: List[str], 
                                missing_optional: List[str]) -> List[str]:
        """Generate specific recommendations for improving information"""
        recommendations = []
        
        # PR-specific recommendations
        if scores['pr_existence'] < 0.5:
            recommendations.append(
                "Add GitHub PR links to JIRA ticket - PRs are critical for understanding implementation"
            )
            recommendations.append(
                "Search for PRs using JIRA ID in GitHub repositories"
            )
            
        # Technical details recommendations
        if scores['technical_details'] < 0.7:
            recommendations.append(
                "Add 'Technical Design' section to JIRA with architecture details"
            )
            recommendations.append(
                "Document affected components and their interactions"
            )
            
        # Testing requirements recommendations
        if scores['testing_requirements'] < 0.7:
            recommendations.append(
                "Add 'Acceptance Criteria' section with clear success conditions"
            )
            recommendations.append(
                "Define specific test scenarios that need validation"
            )
            
        # General recommendations
        if missing_critical:
            recommendations.append(
                f"Critical information missing: {', '.join(missing_critical[:3])}"
            )
            
        return recommendations
    
    def _define_critical_requirements(self) -> Dict[str, List[str]]:
        """Define critical information requirements by category"""
        return {
            'technical_details': [
                'pr_references',
                'code_changes',
                'affected_components',
                'integration_points'
            ],
            'testing_requirements': [
                'acceptance_criteria',
                'success_conditions',
                'validation_steps'
            ],
            'pr_existence': [
                'github_prs',
                'pr_links',
                'implementation_references'
            ]
        }
    
    def _define_optional_requirements(self) -> Dict[str, List[str]]:
        """Define optional but helpful information requirements"""
        return {
            'environment_info': [
                'target_version',
                'deployment_environment',
                'platform_details'
            ],
            'business_context': [
                'user_impact',
                'business_value',
                'customer_scenarios'
            ],
            'extended_details': [
                'performance_criteria',
                'edge_cases',
                'known_limitations'
            ]
        }
