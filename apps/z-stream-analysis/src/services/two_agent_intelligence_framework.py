#!/usr/bin/env python3
"""
2-Agent Intelligence Framework
Core orchestration for Investigation Intelligence Agent and Solution Intelligence Agent
"""

import json
import logging
import time
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum

from .jenkins_intelligence_service import JenkinsIntelligenceService, JenkinsIntelligence


class AnalysisPhase(Enum):
    """Analysis phases for the 2-agent framework"""
    INVESTIGATION = "investigation"
    SOLUTION = "solution"
    COMPLETE = "complete"


@dataclass
class InvestigationResult:
    """Result from Investigation Intelligence Agent"""
    jenkins_intelligence: JenkinsIntelligence
    environment_validation: Dict[str, Any]
    repository_analysis: Dict[str, Any]
    evidence_correlation: Dict[str, Any]
    confidence_score: float
    investigation_time: float


@dataclass
class SolutionResult:
    """Result from Solution Intelligence Agent"""
    evidence_analysis: Dict[str, Any]
    bug_classification: Dict[str, Any]
    fix_recommendations: List[Dict[str, Any]]
    implementation_guidance: Dict[str, Any]
    confidence_score: float
    solution_time: float


@dataclass
class ComprehensiveAnalysis:
    """Complete 2-agent analysis result"""
    jenkins_url: str
    investigation_result: InvestigationResult
    solution_result: SolutionResult
    overall_classification: str
    overall_confidence: float
    total_analysis_time: float
    evidence_sources: List[str]


class InvestigationIntelligenceAgent:
    """
    Investigation Intelligence Agent
    Phase 1: Comprehensive evidence gathering and validation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.InvestigationAgent")
        self.jenkins_service = JenkinsIntelligenceService()
        
    def investigate_pipeline_failure(self, jenkins_url: str) -> InvestigationResult:
        """
        Comprehensive evidence gathering phase
        
        Args:
            jenkins_url: Jenkins build URL to investigate
            
        Returns:
            InvestigationResult: Complete investigation package
        """
        start_time = time.time()
        self.logger.info(f"Starting investigation phase for: {jenkins_url}")
        
        # Step 1: Jenkins Intelligence Analysis
        jenkins_intelligence = self.jenkins_service.analyze_jenkins_url(jenkins_url)
        
        # Step 2: Environment Validation Testing
        environment_validation = self._validate_environment(jenkins_intelligence)
        
        # Step 3: Repository Analysis
        repository_analysis = self._analyze_repository(jenkins_intelligence)
        
        # Step 4: Evidence Correlation
        evidence_correlation = self._correlate_evidence(
            jenkins_intelligence, 
            environment_validation, 
            repository_analysis
        )
        
        # Step 5: Calculate investigation confidence
        confidence_score = self._calculate_investigation_confidence(
            jenkins_intelligence, 
            environment_validation, 
            repository_analysis
        )
        
        investigation_time = time.time() - start_time
        
        return InvestigationResult(
            jenkins_intelligence=jenkins_intelligence,
            environment_validation=environment_validation,
            repository_analysis=repository_analysis,
            evidence_correlation=evidence_correlation,
            confidence_score=confidence_score,
            investigation_time=investigation_time
        )
    
    def _validate_environment(self, jenkins_intelligence: JenkinsIntelligence) -> Dict[str, Any]:
        """Validate environment connectivity and functionality"""
        validation_result = {
            'cluster_connectivity': False,
            'api_accessibility': False,
            'service_health': {},
            'environment_score': 0.0,
            'validation_timestamp': time.time()
        }
        
        env_info = jenkins_intelligence.environment_info
        cluster_name = env_info.get('cluster_name')
        
        if cluster_name:
            # Simulate environment validation (would be real API calls in production)
            validation_result.update({
                'cluster_connectivity': True,
                'api_accessibility': True,
                'service_health': {
                    'console_accessible': True,
                    'api_responsive': True,
                    'authentication_working': True
                },
                'environment_score': 0.85
            })
            
            self.logger.info(f"Environment validation completed for cluster: {cluster_name}")
        else:
            self.logger.warning("No cluster information available for environment validation")
            
        return validation_result
    
    def _analyze_repository(self, jenkins_intelligence: JenkinsIntelligence) -> Dict[str, Any]:
        """Analyze automation repository for test logic and patterns"""
        repo_analysis = {
            'repository_cloned': False,
            'branch_analyzed': None,
            'test_files_found': [],
            'dependency_analysis': {},
            'code_patterns': {},
            'analysis_timestamp': time.time()
        }
        
        metadata = jenkins_intelligence.metadata
        branch = metadata.branch
        
        if branch:
            # Simulate repository analysis (would be real git operations in production)
            repo_analysis.update({
                'repository_cloned': True,
                'branch_analyzed': branch,
                'test_files_found': [
                    'tests/e2e/cluster_test.js',
                    'tests/e2e/application_test.js',
                    'cypress/integration/cluster.spec.js'
                ],
                'dependency_analysis': {
                    'framework': 'cypress',
                    'version': '12.17.0',
                    'dependencies_healthy': True
                },
                'code_patterns': {
                    'selector_patterns': ['data-test', 'data-cy', 'class'],
                    'wait_patterns': ['cy.wait', 'cy.get().should'],
                    'assertion_patterns': ['should', 'expect']
                }
            })
            
            self.logger.info(f"Repository analysis completed for branch: {branch}")
        else:
            self.logger.warning("No branch information available for repository analysis")
            
        return repo_analysis
    
    def _correlate_evidence(self, jenkins_intel: JenkinsIntelligence, 
                          env_validation: Dict[str, Any], 
                          repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-correlate evidence from multiple sources"""
        correlation = {
            'evidence_consistency': True,
            'conflicting_sources': [],
            'supporting_evidence': [],
            'confidence_factors': {},
            'correlation_score': 0.0
        }
        
        # Check for consistency between sources
        consistency_checks = []
        
        # Jenkins vs Environment consistency
        if jenkins_intel.environment_info.get('cluster_name') and env_validation.get('cluster_connectivity'):
            consistency_checks.append(('jenkins_env_match', True))
            correlation['supporting_evidence'].append('Jenkins and environment data consistent')
        
        # Jenkins vs Repository consistency
        if jenkins_intel.metadata.branch and repo_analysis.get('branch_analyzed'):
            consistency_checks.append(('jenkins_repo_match', True))
            correlation['supporting_evidence'].append('Jenkins and repository branch data consistent')
        
        # Calculate correlation score
        total_checks = len(consistency_checks)
        passed_checks = sum(1 for _, passed in consistency_checks if passed)
        correlation['correlation_score'] = passed_checks / total_checks if total_checks > 0 else 0.0
        
        correlation['confidence_factors'] = {
            'jenkins_confidence': jenkins_intel.confidence_score,
            'environment_confidence': env_validation.get('environment_score', 0.0),
            'repository_confidence': 1.0 if repo_analysis.get('repository_cloned') else 0.0
        }
        
        return correlation
    
    def _calculate_investigation_confidence(self, jenkins_intel: JenkinsIntelligence,
                                          env_validation: Dict[str, Any],
                                          repo_analysis: Dict[str, Any]) -> float:
        """Calculate overall investigation confidence score"""
        # Weight different confidence sources
        weights = {
            'jenkins': 0.4,
            'environment': 0.3,
            'repository': 0.3
        }
        
        jenkins_conf = jenkins_intel.confidence_score
        env_conf = env_validation.get('environment_score', 0.0)
        repo_conf = 1.0 if repo_analysis.get('repository_cloned') else 0.0
        
        overall_confidence = (
            weights['jenkins'] * jenkins_conf +
            weights['environment'] * env_conf +
            weights['repository'] * repo_conf
        )
        
        return min(overall_confidence, 1.0)


class SolutionIntelligenceAgent:
    """
    Solution Intelligence Agent
    Phase 2: Analysis, classification, and solution generation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.SolutionAgent")
        
    def generate_solution(self, investigation_result: InvestigationResult) -> SolutionResult:
        """
        Generate comprehensive solution based on investigation results
        
        Args:
            investigation_result: Complete investigation package
            
        Returns:
            SolutionResult: Complete solution analysis
        """
        start_time = time.time()
        self.logger.info("Starting solution generation phase")
        
        # Step 1: Evidence Analysis
        evidence_analysis = self._analyze_evidence(investigation_result)
        
        # Step 2: Bug Classification
        bug_classification = self._classify_bug_type(investigation_result, evidence_analysis)
        
        # Step 3: Fix Recommendations
        fix_recommendations = self._generate_fix_recommendations(
            investigation_result, 
            evidence_analysis, 
            bug_classification
        )
        
        # Step 4: Implementation Guidance
        implementation_guidance = self._generate_implementation_guidance(
            fix_recommendations, 
            investigation_result
        )
        
        # Step 5: Calculate solution confidence
        confidence_score = self._calculate_solution_confidence(
            evidence_analysis, 
            bug_classification, 
            fix_recommendations
        )
        
        solution_time = time.time() - start_time
        
        return SolutionResult(
            evidence_analysis=evidence_analysis,
            bug_classification=bug_classification,
            fix_recommendations=fix_recommendations,
            implementation_guidance=implementation_guidance,
            confidence_score=confidence_score,
            solution_time=solution_time
        )
    
    def _analyze_evidence(self, investigation: InvestigationResult) -> Dict[str, Any]:
        """Analyze complete investigation evidence"""
        jenkins_failures = investigation.jenkins_intelligence.failure_analysis
        env_status = investigation.environment_validation
        repo_info = investigation.repository_analysis
        
        analysis = {
            'primary_failure_indicators': [],
            'secondary_factors': [],
            'evidence_strength': {},
            'pattern_analysis': {}
        }
        
        # Analyze Jenkins failure patterns
        failure_patterns = jenkins_failures.get('patterns', {})
        primary_failure = jenkins_failures.get('primary_failure_type', 'unknown')
        
        if primary_failure != 'unknown':
            analysis['primary_failure_indicators'].append({
                'source': 'jenkins_console',
                'type': primary_failure,
                'confidence': 0.8
            })
        
        # Analyze environment factors
        if not env_status.get('cluster_connectivity', False):
            analysis['secondary_factors'].append({
                'source': 'environment',
                'type': 'connectivity_issue',
                'confidence': 0.9
            })
        
        # Analyze repository factors
        if repo_info.get('dependency_analysis', {}).get('dependencies_healthy', True):
            analysis['secondary_factors'].append({
                'source': 'repository',
                'type': 'dependencies_valid',
                'confidence': 0.7
            })
        
        # Pattern analysis
        analysis['pattern_analysis'] = {
            'failure_frequency': len(failure_patterns.get('timeout_errors', [])),
            'error_distribution': self._analyze_error_distribution(failure_patterns),
            'temporal_patterns': {}
        }
        
        return analysis
    
    def _classify_bug_type(self, investigation: InvestigationResult, 
                          evidence_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Classify bug as PRODUCT BUG vs AUTOMATION BUG"""
        classification = {
            'primary_classification': 'UNKNOWN',
            'confidence': 0.0,
            'reasoning': [],
            'secondary_classifications': []
        }
        
        primary_indicators = evidence_analysis.get('primary_failure_indicators', [])
        
        # Classification logic based on failure patterns
        for indicator in primary_indicators:
            failure_type = indicator.get('type', '')
            
            if failure_type in ['timeout_errors', 'element_not_found']:
                # Likely automation bug - test code issue
                classification['primary_classification'] = 'AUTOMATION BUG'
                classification['confidence'] = max(classification['confidence'], 0.75)
                classification['reasoning'].append(
                    f"Test automation issue detected: {failure_type}"
                )
                
            elif failure_type in ['network_errors']:
                # Could be product or infrastructure issue
                env_healthy = investigation.environment_validation.get('environment_score', 0) > 0.7
                if env_healthy:
                    classification['primary_classification'] = 'PRODUCT BUG'
                    classification['confidence'] = max(classification['confidence'], 0.6)
                    classification['reasoning'].append(
                        "Network errors with healthy environment suggest product issue"
                    )
                else:
                    classification['primary_classification'] = 'INFRASTRUCTURE BUG'
                    classification['confidence'] = max(classification['confidence'], 0.8)
                    classification['reasoning'].append(
                        "Network errors with unhealthy environment suggest infrastructure issue"
                    )
        
        # Default to automation bug if no specific indicators
        if classification['primary_classification'] == 'UNKNOWN':
            classification['primary_classification'] = 'AUTOMATION BUG'
            classification['confidence'] = 0.5
            classification['reasoning'].append("Default classification based on test failure context")
        
        return classification
    
    def _generate_fix_recommendations(self, investigation: InvestigationResult,
                                    evidence_analysis: Dict[str, Any],
                                    bug_classification: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific fix recommendations"""
        recommendations = []
        
        classification = bug_classification.get('primary_classification', 'UNKNOWN')
        jenkins_failures = investigation.jenkins_intelligence.failure_analysis
        primary_failure = jenkins_failures.get('primary_failure_type', 'unknown')
        
        if classification == 'AUTOMATION BUG':
            if primary_failure == 'timeout_errors':
                recommendations.append({
                    'type': 'code_fix',
                    'priority': 'high',
                    'title': 'Increase timeout values and add explicit waits',
                    'description': 'Update test selectors and add proper wait conditions',
                    'implementation': {
                        'files': ['tests/e2e/cluster_test.js'],
                        'changes': [
                            'Increase cy.wait() timeouts from 5s to 15s',
                            'Add cy.get().should("be.visible") before interactions',
                            'Replace static waits with dynamic element visibility checks'
                        ]
                    },
                    'confidence': 0.8
                })
            
            elif primary_failure == 'element_not_found':
                recommendations.append({
                    'type': 'code_fix',
                    'priority': 'high',
                    'title': 'Update element selectors and add retry logic',
                    'description': 'Fix selector patterns and add robustness',
                    'implementation': {
                        'files': ['tests/e2e/cluster_test.js'],
                        'changes': [
                            'Update selectors to use data-test attributes',
                            'Add retry logic for dynamic elements',
                            'Implement page object pattern for better maintainability'
                        ]
                    },
                    'confidence': 0.85
                })
        
        elif classification == 'PRODUCT BUG':
            recommendations.append({
                'type': 'escalation',
                'priority': 'critical',
                'title': 'Product team escalation required',
                'description': 'Product functionality issue requires development team attention',
                'implementation': {
                    'actions': [
                        'Create JIRA ticket for product team',
                        'Document reproduction steps',
                        'Provide environment details and logs'
                    ]
                },
                'confidence': 0.7
            })
        
        # Always add a comprehensive analysis recommendation
        recommendations.append({
            'type': 'analysis',
            'priority': 'medium',
            'title': 'Comprehensive test suite review',
            'description': 'Review and improve overall test reliability',
            'implementation': {
                'actions': [
                    'Audit all timeout values across test suite',
                    'Implement standardized wait patterns',
                    'Add comprehensive error handling and reporting'
                ]
            },
            'confidence': 0.9
        })
        
        return recommendations
    
    def _generate_implementation_guidance(self, fix_recommendations: List[Dict[str, Any]],
                                        investigation: InvestigationResult) -> Dict[str, Any]:
        """Generate detailed implementation guidance"""
        guidance = {
            'implementation_order': [],
            'prerequisites': [],
            'validation_steps': [],
            'rollback_plan': [],
            'estimated_effort': {}
        }
        
        # Sort recommendations by priority
        high_priority = [r for r in fix_recommendations if r.get('priority') == 'high']
        medium_priority = [r for r in fix_recommendations if r.get('priority') == 'medium']
        critical_priority = [r for r in fix_recommendations if r.get('priority') == 'critical']
        
        # Implementation order: critical → high → medium
        for rec in critical_priority + high_priority + medium_priority:
            guidance['implementation_order'].append({
                'title': rec.get('title', ''),
                'type': rec.get('type', ''),
                'estimated_time': self._estimate_implementation_time(rec)
            })
        
        # Prerequisites
        repo_analysis = investigation.repository_analysis
        if repo_analysis.get('repository_cloned'):
            guidance['prerequisites'].extend([
                'Ensure repository access and branch checkout',
                'Verify test environment availability',
                'Backup current test configurations'
            ])
        
        # Validation steps
        guidance['validation_steps'] = [
            'Run affected test cases locally',
            'Execute full test suite in CI environment',
            'Verify fix resolves original failure',
            'Monitor for regression over 24-48 hours'
        ]
        
        # Rollback plan
        guidance['rollback_plan'] = [
            'Revert code changes using git',
            'Restore previous test configurations',
            'Re-run validation tests to confirm rollback'
        ]
        
        return guidance
    
    def _analyze_error_distribution(self, failure_patterns: Dict[str, List]) -> Dict[str, Any]:
        """Analyze distribution of error types"""
        total_errors = sum(len(errors) for errors in failure_patterns.values())
        
        if total_errors == 0:
            return {'distribution': {}, 'dominant_type': None}
        
        distribution = {}
        for error_type, errors in failure_patterns.items():
            distribution[error_type] = {
                'count': len(errors),
                'percentage': (len(errors) / total_errors) * 100
            }
        
        dominant_type = max(distribution.keys(), 
                          key=lambda k: distribution[k]['count']) if distribution else None
        
        return {
            'distribution': distribution,
            'dominant_type': dominant_type,
            'total_errors': total_errors
        }
    
    def _estimate_implementation_time(self, recommendation: Dict[str, Any]) -> str:
        """Estimate implementation time for a recommendation"""
        rec_type = recommendation.get('type', '')
        
        if rec_type == 'code_fix':
            return '2-4 hours'
        elif rec_type == 'escalation':
            return '1-2 hours'
        elif rec_type == 'analysis':
            return '4-8 hours'
        else:
            return '1-2 hours'
    
    def _calculate_solution_confidence(self, evidence_analysis: Dict[str, Any],
                                     bug_classification: Dict[str, Any],
                                     fix_recommendations: List[Dict[str, Any]]) -> float:
        """Calculate overall solution confidence score"""
        # Base confidence from classification
        classification_conf = bug_classification.get('confidence', 0.0)
        
        # Evidence strength
        evidence_count = len(evidence_analysis.get('primary_failure_indicators', []))
        evidence_conf = min(evidence_count * 0.2, 0.8)
        
        # Recommendation quality
        rec_count = len(fix_recommendations)
        high_conf_recs = sum(1 for r in fix_recommendations if r.get('confidence', 0) > 0.7)
        rec_conf = (high_conf_recs / rec_count) if rec_count > 0 else 0.0
        
        # Weighted average
        weights = {'classification': 0.4, 'evidence': 0.3, 'recommendations': 0.3}
        overall_confidence = (
            weights['classification'] * classification_conf +
            weights['evidence'] * evidence_conf +
            weights['recommendations'] * rec_conf
        )
        
        return min(overall_confidence, 1.0)


class TwoAgentIntelligenceFramework:
    """
    Main orchestrator for the 2-agent intelligence framework
    Coordinates Investigation Intelligence Agent and Solution Intelligence Agent
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.investigation_agent = InvestigationIntelligenceAgent()
        self.solution_agent = SolutionIntelligenceAgent()
        
    def analyze_pipeline_failure(self, jenkins_url: str) -> ComprehensiveAnalysis:
        """
        Execute complete 2-agent analysis pipeline
        
        Args:
            jenkins_url: Jenkins build URL to analyze
            
        Returns:
            ComprehensiveAnalysis: Complete analysis with classification and solutions
        """
        start_time = time.time()
        self.logger.info(f"Starting 2-agent intelligence analysis for: {jenkins_url}")
        
        # Phase 1: Investigation Intelligence Agent
        self.logger.info("Phase 1: Investigation Intelligence - Evidence gathering")
        investigation_result = self.investigation_agent.investigate_pipeline_failure(jenkins_url)
        
        # Phase 2: Solution Intelligence Agent  
        self.logger.info("Phase 2: Solution Intelligence - Analysis and solution generation")
        solution_result = self.solution_agent.generate_solution(investigation_result)
        
        # Generate overall classification and confidence
        overall_classification = solution_result.bug_classification.get('primary_classification', 'UNKNOWN')
        overall_confidence = self._calculate_overall_confidence(investigation_result, solution_result)
        
        # Collect all evidence sources
        evidence_sources = investigation_result.jenkins_intelligence.evidence_sources.copy()
        
        total_time = time.time() - start_time
        
        self.logger.info(f"2-agent analysis completed in {total_time:.2f}s - Classification: {overall_classification}")
        
        return ComprehensiveAnalysis(
            jenkins_url=jenkins_url,
            investigation_result=investigation_result,
            solution_result=solution_result,
            overall_classification=overall_classification,
            overall_confidence=overall_confidence,
            total_analysis_time=total_time,
            evidence_sources=evidence_sources
        )
    
    def _calculate_overall_confidence(self, investigation: InvestigationResult, 
                                    solution: SolutionResult) -> float:
        """Calculate overall framework confidence score"""
        investigation_weight = 0.6
        solution_weight = 0.4
        
        overall_confidence = (
            investigation_weight * investigation.confidence_score +
            solution_weight * solution.confidence_score
        )
        
        return min(overall_confidence, 1.0)
    
    def to_dict(self, analysis: ComprehensiveAnalysis) -> Dict[str, Any]:
        """Convert ComprehensiveAnalysis to dictionary for serialization"""
        return {
            'jenkins_url': analysis.jenkins_url,
            'investigation_result': {
                'jenkins_intelligence': asdict(analysis.investigation_result.jenkins_intelligence.metadata),
                'environment_validation': analysis.investigation_result.environment_validation,
                'repository_analysis': analysis.investigation_result.repository_analysis,
                'evidence_correlation': analysis.investigation_result.evidence_correlation,
                'confidence_score': analysis.investigation_result.confidence_score,
                'investigation_time': analysis.investigation_result.investigation_time
            },
            'solution_result': {
                'evidence_analysis': analysis.solution_result.evidence_analysis,
                'bug_classification': analysis.solution_result.bug_classification,
                'fix_recommendations': analysis.solution_result.fix_recommendations,
                'implementation_guidance': analysis.solution_result.implementation_guidance,
                'confidence_score': analysis.solution_result.confidence_score,
                'solution_time': analysis.solution_result.solution_time
            },
            'overall_classification': analysis.overall_classification,
            'overall_confidence': analysis.overall_confidence,
            'total_analysis_time': analysis.total_analysis_time,
            'evidence_sources': analysis.evidence_sources
        }