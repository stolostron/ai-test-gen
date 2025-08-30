#!/usr/bin/env python3
"""
Unit Tests for 2-Agent Intelligence Framework
Tests the core functionality of Investigation and Solution Intelligence Agents
"""

import unittest
import json
import time
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass
from typing import Dict, Any, Optional

# Add source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from services.two_agent_intelligence_framework import (
    TwoAgentIntelligenceFramework,
    InvestigationIntelligenceAgent,
    SolutionIntelligenceAgent,
    InvestigationResult,
    SolutionResult,
    ComprehensiveAnalysis,
    AnalysisPhase
)
from services.jenkins_intelligence_service import JenkinsIntelligence, JenkinsMetadata


class TestInvestigationIntelligenceAgent(unittest.TestCase):
    """
    Test suite for Investigation Intelligence Agent
    
    CRITICAL TESTING GOALS:
    1. Verify comprehensive evidence gathering capabilities
    2. Test environment validation accuracy
    3. Validate repository analysis functionality
    4. Ensure evidence correlation works correctly
    5. Test confidence scoring accuracy
    """
    
    def setUp(self):
        """Set up test environment"""
        self.agent = InvestigationIntelligenceAgent()
        self.sample_jenkins_url = "https://jenkins-server.com/job/test-pipeline/123/"
        self.sample_jenkins_intelligence = self._create_sample_jenkins_intelligence()
        
    def _create_sample_jenkins_intelligence(self) -> JenkinsIntelligence:
        """Create sample Jenkins intelligence for testing"""
        metadata = JenkinsMetadata(
            build_url=self.sample_jenkins_url,
            job_name="test-pipeline",
            build_number=123,
            build_result="FAILURE",
            timestamp="2024-08-17T17:55:40Z",
            parameters={"CLUSTER_NAME": "qe6-vmware-ibm", "BRANCH": "release-2.9"},
            console_log_snippet="TimeoutError: timeout waiting for element",
            artifacts=["results.xml"],
            branch="release-2.9",
            commit_sha="abc123"
        )
        
        return JenkinsIntelligence(
            metadata=metadata,
            failure_analysis={
                'patterns': {'timeout_errors': ['TimeoutError']},
                'total_failures': 1,
                'primary_failure_type': 'timeout_errors'
            },
            environment_info={'cluster_name': 'qe6-vmware-ibm'},
            evidence_sources=["[Jenkins:test-pipeline:123:FAILURE]"],
            confidence_score=0.8
        )

    # CRITICAL TEST 1: Complete Investigation Pipeline
    @patch.object(InvestigationIntelligenceAgent, '_validate_environment')
    @patch.object(InvestigationIntelligenceAgent, '_analyze_repository')
    @patch.object(InvestigationIntelligenceAgent, '_correlate_evidence')
    def test_complete_investigation_pipeline(self, mock_correlate, mock_repo, mock_env):
        """
        CRITICAL: Test complete investigation pipeline execution
        """
        # Mock the Jenkins service
        with patch.object(self.agent.jenkins_service, 'analyze_jenkins_url') as mock_jenkins:
            mock_jenkins.return_value = self.sample_jenkins_intelligence
            
            # Mock other investigation steps
            mock_env.return_value = {
                'cluster_connectivity': True,
                'environment_score': 0.85,
                'validation_timestamp': time.time()
            }
            
            mock_repo.return_value = {
                'repository_cloned': True,
                'branch_analyzed': 'release-2.9',
                'test_files_found': ['tests/e2e/cluster_test.js']
            }
            
            mock_correlate.return_value = {
                'evidence_consistency': True,
                'correlation_score': 0.9
            }
            
            # Execute investigation
            result = self.agent.investigate_pipeline_failure(self.sample_jenkins_url)
            
            # Validate result structure
            self.assertIsInstance(result, InvestigationResult)
            self.assertEqual(result.jenkins_intelligence.metadata.job_name, "test-pipeline")
            self.assertTrue(result.environment_validation['cluster_connectivity'])
            self.assertTrue(result.repository_analysis['repository_cloned'])
            self.assertGreater(result.confidence_score, 0.5)
            self.assertGreater(result.investigation_time, 0)

    # CRITICAL TEST 2: Environment Validation Logic
    def test_environment_validation_logic(self):
        """
        CRITICAL: Test environment validation with different scenarios
        """
        test_cases = [
            {
                "name": "Valid Cluster Information",
                "jenkins_intel": self.sample_jenkins_intelligence,
                "expected_connectivity": True,
                "expected_score_min": 0.7
            },
            {
                "name": "Missing Cluster Information",
                "jenkins_intel": JenkinsIntelligence(
                    metadata=JenkinsMetadata(
                        build_url="https://test.com/job/test/123/",
                        job_name="test",
                        build_number=123,
                        build_result="FAILURE",
                        timestamp="",
                        parameters={},
                        console_log_snippet="",
                        artifacts=[]
                    ),
                    failure_analysis={},
                    environment_info={},
                    evidence_sources=[],
                    confidence_score=0.5
                ),
                "expected_connectivity": False,
                "expected_score_min": 0.0
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                result = self.agent._validate_environment(case["jenkins_intel"])
                
                # Validate structure
                self.assertIn('cluster_connectivity', result)
                self.assertIn('environment_score', result)
                self.assertIn('validation_timestamp', result)
                
                # Validate expected behavior
                self.assertEqual(result['cluster_connectivity'], case["expected_connectivity"])
                self.assertGreaterEqual(result['environment_score'], case["expected_score_min"])

    # CRITICAL TEST 3: Repository Analysis Logic
    def test_repository_analysis_logic(self):
        """
        CRITICAL: Test repository analysis with different branch scenarios
        """
        test_cases = [
            {
                "name": "Valid Branch Information",
                "jenkins_intel": self.sample_jenkins_intelligence,
                "expected_cloned": True,
                "expected_branch": "release-2.9"
            },
            {
                "name": "Missing Branch Information",
                "jenkins_intel": JenkinsIntelligence(
                    metadata=JenkinsMetadata(
                        build_url="https://test.com/job/test/123/",
                        job_name="test",
                        build_number=123,
                        build_result="FAILURE",
                        timestamp="",
                        parameters={},
                        console_log_snippet="",
                        artifacts=[],
                        branch=None
                    ),
                    failure_analysis={},
                    environment_info={},
                    evidence_sources=[],
                    confidence_score=0.5
                ),
                "expected_cloned": False,
                "expected_branch": None
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                result = self.agent._analyze_repository(case["jenkins_intel"])
                
                # Validate structure
                self.assertIn('repository_cloned', result)
                self.assertIn('branch_analyzed', result)
                self.assertIn('test_files_found', result)
                self.assertIn('analysis_timestamp', result)
                
                # Validate expected behavior
                self.assertEqual(result['repository_cloned'], case["expected_cloned"])
                self.assertEqual(result['branch_analyzed'], case["expected_branch"])

    # CRITICAL TEST 4: Evidence Correlation Logic
    def test_evidence_correlation_logic(self):
        """
        CRITICAL: Test evidence correlation across multiple sources
        """
        env_validation = {
            'cluster_connectivity': True,
            'environment_score': 0.85
        }
        
        repo_analysis = {
            'repository_cloned': True,
            'branch_analyzed': 'release-2.9'
        }
        
        result = self.agent._correlate_evidence(
            self.sample_jenkins_intelligence,
            env_validation,
            repo_analysis
        )
        
        # Validate structure
        self.assertIn('evidence_consistency', result)
        self.assertIn('supporting_evidence', result)
        self.assertIn('confidence_factors', result)
        self.assertIn('correlation_score', result)
        
        # Validate correlation logic
        self.assertTrue(result['evidence_consistency'])
        self.assertGreater(len(result['supporting_evidence']), 0)
        self.assertGreater(result['correlation_score'], 0.5)
        
        # Validate confidence factors
        confidence_factors = result['confidence_factors']
        self.assertIn('jenkins_confidence', confidence_factors)
        self.assertIn('environment_confidence', confidence_factors)
        self.assertIn('repository_confidence', confidence_factors)

    # CRITICAL TEST 5: Investigation Confidence Calculation
    def test_investigation_confidence_calculation(self):
        """
        CRITICAL: Test investigation confidence calculation accuracy
        """
        test_cases = [
            {
                "name": "High Confidence Scenario",
                "env_validation": {'environment_score': 0.9},
                "repo_analysis": {'repository_cloned': True},
                "expected_min": 0.7
            },
            {
                "name": "Medium Confidence Scenario",
                "env_validation": {'environment_score': 0.5},
                "repo_analysis": {'repository_cloned': True},
                "expected_min": 0.4
            },
            {
                "name": "Low Confidence Scenario",
                "env_validation": {'environment_score': 0.2},
                "repo_analysis": {'repository_cloned': False},
                "expected_min": 0.2
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                result = self.agent._calculate_investigation_confidence(
                    self.sample_jenkins_intelligence,
                    case["env_validation"],
                    case["repo_analysis"]
                )
                
                self.assertIsInstance(result, float)
                self.assertGreaterEqual(result, 0.0)
                self.assertLessEqual(result, 1.0)
                self.assertGreaterEqual(result, case["expected_min"])


class TestSolutionIntelligenceAgent(unittest.TestCase):
    """
    Test suite for Solution Intelligence Agent
    
    CRITICAL TESTING GOALS:
    1. Test evidence analysis accuracy
    2. Validate bug classification logic (PRODUCT vs AUTOMATION)
    3. Test fix recommendation generation
    4. Validate implementation guidance creation
    5. Test solution confidence scoring
    """
    
    def setUp(self):
        """Set up test environment"""
        self.agent = SolutionIntelligenceAgent()
        self.sample_investigation_result = self._create_sample_investigation_result()
        
    def _create_sample_investigation_result(self) -> InvestigationResult:
        """Create sample investigation result for testing"""
        jenkins_intelligence = JenkinsIntelligence(
            metadata=JenkinsMetadata(
                build_url="https://jenkins.com/job/test/123/",
                job_name="test",
                build_number=123,
                build_result="FAILURE",
                timestamp="",
                parameters={"CLUSTER_NAME": "test-cluster"},
                console_log_snippet="TimeoutError: timeout waiting",
                artifacts=[],
                branch="release-2.9"
            ),
            failure_analysis={
                'patterns': {'timeout_errors': ['TimeoutError', 'timed out']},
                'total_failures': 2,
                'primary_failure_type': 'timeout_errors'
            },
            environment_info={'cluster_name': 'test-cluster'},
            evidence_sources=["[Jenkins:test:123:FAILURE]"],
            confidence_score=0.8
        )
        
        return InvestigationResult(
            jenkins_intelligence=jenkins_intelligence,
            environment_validation={'cluster_connectivity': True, 'environment_score': 0.85},
            repository_analysis={'repository_cloned': True, 'branch_analyzed': 'release-2.9'},
            evidence_correlation={'evidence_consistency': True, 'correlation_score': 0.9},
            confidence_score=0.8,
            investigation_time=2.5
        )

    # CRITICAL TEST 6: Complete Solution Generation Pipeline
    def test_complete_solution_generation_pipeline(self):
        """
        CRITICAL: Test complete solution generation pipeline
        """
        result = self.agent.generate_solution(self.sample_investigation_result)
        
        # Validate result structure
        self.assertIsInstance(result, SolutionResult)
        self.assertIn('primary_failure_indicators', result.evidence_analysis)
        self.assertIn('primary_classification', result.bug_classification)
        self.assertIsInstance(result.fix_recommendations, list)
        self.assertIn('implementation_order', result.implementation_guidance)
        self.assertGreater(result.confidence_score, 0.0)
        self.assertGreater(result.solution_time, 0.0)

    # CRITICAL TEST 7: Bug Classification Logic
    def test_bug_classification_logic(self):
        """
        CRITICAL: Test PRODUCT BUG vs AUTOMATION BUG classification
        """
        test_cases = [
            {
                "name": "Timeout Errors - Automation Bug",
                "failure_type": "timeout_errors",
                "env_healthy": True,
                "expected_classification": "AUTOMATION BUG",
                "expected_confidence_min": 0.6
            },
            {
                "name": "Element Not Found - Automation Bug",
                "failure_type": "element_not_found",
                "env_healthy": True,
                "expected_classification": "AUTOMATION BUG",
                "expected_confidence_min": 0.6
            },
            {
                "name": "Network Errors with Healthy Env - Product Bug",
                "failure_type": "network_errors",
                "env_healthy": True,
                "expected_classification": "PRODUCT BUG",
                "expected_confidence_min": 0.5
            },
            {
                "name": "Network Errors with Unhealthy Env - Infrastructure Bug",
                "failure_type": "network_errors",
                "env_healthy": False,
                "expected_classification": "INFRASTRUCTURE BUG",
                "expected_confidence_min": 0.7
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                # Create modified investigation result
                investigation = self.sample_investigation_result
                investigation.jenkins_intelligence.failure_analysis['primary_failure_type'] = case["failure_type"]
                investigation.environment_validation['environment_score'] = 0.8 if case["env_healthy"] else 0.3
                
                # Create evidence analysis
                evidence_analysis = {
                    'primary_failure_indicators': [{
                        'source': 'jenkins_console',
                        'type': case["failure_type"],
                        'confidence': 0.8
                    }]
                }
                
                result = self.agent._classify_bug_type(investigation, evidence_analysis)
                
                self.assertEqual(result['primary_classification'], case["expected_classification"])
                self.assertGreaterEqual(result['confidence'], case["expected_confidence_min"])
                self.assertGreater(len(result['reasoning']), 0)

    # CRITICAL TEST 8: Fix Recommendation Generation
    def test_fix_recommendation_generation(self):
        """
        CRITICAL: Test fix recommendation generation for different bug types
        """
        # Test automation bug recommendations
        evidence_analysis = {
            'primary_failure_indicators': [{
                'source': 'jenkins_console',
                'type': 'timeout_errors',
                'confidence': 0.8
            }]
        }
        
        bug_classification = {
            'primary_classification': 'AUTOMATION BUG',
            'confidence': 0.8
        }
        
        recommendations = self.agent._generate_fix_recommendations(
            self.sample_investigation_result,
            evidence_analysis,
            bug_classification
        )
        
        # Should have at least 2 recommendations (specific fix + general analysis)
        self.assertGreaterEqual(len(recommendations), 2)
        
        # Check for automation-specific recommendations
        automation_recs = [r for r in recommendations if r.get('type') == 'code_fix']
        self.assertGreater(len(automation_recs), 0)
        
        # Validate recommendation structure
        for rec in recommendations:
            self.assertIn('type', rec)
            self.assertIn('priority', rec)
            self.assertIn('title', rec)
            self.assertIn('description', rec)
            self.assertIn('implementation', rec)
            self.assertIn('confidence', rec)

    # CRITICAL TEST 9: Implementation Guidance Generation
    def test_implementation_guidance_generation(self):
        """
        CRITICAL: Test implementation guidance creation
        """
        sample_recommendations = [
            {
                'type': 'code_fix',
                'priority': 'high',
                'title': 'Fix timeout issues',
                'confidence': 0.8
            },
            {
                'type': 'analysis',
                'priority': 'medium',
                'title': 'Review test suite',
                'confidence': 0.9
            }
        ]
        
        guidance = self.agent._generate_implementation_guidance(
            sample_recommendations,
            self.sample_investigation_result
        )
        
        # Validate structure
        self.assertIn('implementation_order', guidance)
        self.assertIn('prerequisites', guidance)
        self.assertIn('validation_steps', guidance)
        self.assertIn('rollback_plan', guidance)
        
        # Validate content
        self.assertEqual(len(guidance['implementation_order']), 2)
        self.assertGreater(len(guidance['prerequisites']), 0)
        self.assertGreater(len(guidance['validation_steps']), 0)
        self.assertGreater(len(guidance['rollback_plan']), 0)

    # CRITICAL TEST 10: Solution Confidence Calculation
    def test_solution_confidence_calculation(self):
        """
        CRITICAL: Test solution confidence calculation accuracy
        """
        test_cases = [
            {
                "name": "High Confidence Solution",
                "evidence_analysis": {
                    'primary_failure_indicators': [
                        {'confidence': 0.9},
                        {'confidence': 0.8}
                    ]
                },
                "bug_classification": {'confidence': 0.85},
                "fix_recommendations": [
                    {'confidence': 0.8},
                    {'confidence': 0.9}
                ],
                "expected_min": 0.6
            },
            {
                "name": "Low Confidence Solution",
                "evidence_analysis": {
                    'primary_failure_indicators': []
                },
                "bug_classification": {'confidence': 0.3},
                "fix_recommendations": [
                    {'confidence': 0.4}
                ],
                "expected_max": 0.5
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                result = self.agent._calculate_solution_confidence(
                    case["evidence_analysis"],
                    case["bug_classification"],
                    case["fix_recommendations"]
                )
                
                self.assertIsInstance(result, float)
                self.assertGreaterEqual(result, 0.0)
                self.assertLessEqual(result, 1.0)
                
                if "expected_min" in case:
                    self.assertGreaterEqual(result, case["expected_min"])
                if "expected_max" in case:
                    self.assertLessEqual(result, case["expected_max"])


class TestTwoAgentIntelligenceFramework(unittest.TestCase):
    """
    Test suite for complete 2-Agent Intelligence Framework
    
    CRITICAL TESTING GOALS:
    1. Test complete end-to-end analysis pipeline
    2. Validate agent coordination and progressive context
    3. Test overall confidence calculation
    4. Validate serialization and data persistence
    5. Test error handling and edge cases
    """
    
    def setUp(self):
        """Set up test environment"""
        self.framework = TwoAgentIntelligenceFramework()
        self.sample_jenkins_url = "https://jenkins-server.com/job/test-pipeline/123/"

    # CRITICAL TEST 11: Complete End-to-End Analysis Pipeline
    @patch.object(InvestigationIntelligenceAgent, 'investigate_pipeline_failure')
    @patch.object(SolutionIntelligenceAgent, 'generate_solution')
    def test_complete_end_to_end_analysis_pipeline(self, mock_solution, mock_investigation):
        """
        CRITICAL: Test complete 2-agent analysis pipeline execution
        """
        # Mock investigation result
        mock_investigation_result = InvestigationResult(
            jenkins_intelligence=JenkinsIntelligence(
                metadata=JenkinsMetadata(
                    build_url=self.sample_jenkins_url,
                    job_name="test-pipeline",
                    build_number=123,
                    build_result="FAILURE",
                    timestamp="",
                    parameters={},
                    console_log_snippet="",
                    artifacts=[]
                ),
                failure_analysis={'primary_failure_type': 'timeout_errors'},
                environment_info={},
                evidence_sources=["[Jenkins:test-pipeline:123:FAILURE]"],
                confidence_score=0.8
            ),
            environment_validation={'environment_score': 0.85},
            repository_analysis={'repository_cloned': True},
            evidence_correlation={'correlation_score': 0.9},
            confidence_score=0.8,
            investigation_time=2.5
        )
        
        # Mock solution result
        mock_solution_result = SolutionResult(
            evidence_analysis={'primary_failure_indicators': []},
            bug_classification={'primary_classification': 'AUTOMATION BUG', 'confidence': 0.8},
            fix_recommendations=[{'type': 'code_fix', 'confidence': 0.8}],
            implementation_guidance={'implementation_order': []},
            confidence_score=0.75,
            solution_time=1.8
        )
        
        mock_investigation.return_value = mock_investigation_result
        mock_solution.return_value = mock_solution_result
        
        # Execute complete analysis
        result = self.framework.analyze_pipeline_failure(self.sample_jenkins_url)
        
        # Validate result structure
        self.assertIsInstance(result, ComprehensiveAnalysis)
        self.assertEqual(result.jenkins_url, self.sample_jenkins_url)
        self.assertEqual(result.overall_classification, 'AUTOMATION BUG')
        self.assertGreater(result.overall_confidence, 0.5)
        self.assertGreater(result.total_analysis_time, 0.0)
        self.assertIsInstance(result.evidence_sources, list)
        
        # Validate agent coordination
        mock_investigation.assert_called_once_with(self.sample_jenkins_url)
        mock_solution.assert_called_once_with(mock_investigation_result)

    # CRITICAL TEST 12: Overall Confidence Calculation
    def test_overall_confidence_calculation(self):
        """
        CRITICAL: Test overall framework confidence calculation
        """
        investigation_result = InvestigationResult(
            jenkins_intelligence=None,
            environment_validation={},
            repository_analysis={},
            evidence_correlation={},
            confidence_score=0.8,
            investigation_time=2.0
        )
        
        solution_result = SolutionResult(
            evidence_analysis={},
            bug_classification={},
            fix_recommendations=[],
            implementation_guidance={},
            confidence_score=0.7,
            solution_time=1.5
        )
        
        overall_confidence = self.framework._calculate_overall_confidence(
            investigation_result,
            solution_result
        )
        
        # Should be weighted average: 0.6 * 0.8 + 0.4 * 0.7 = 0.76
        expected_confidence = 0.6 * 0.8 + 0.4 * 0.7
        self.assertAlmostEqual(overall_confidence, expected_confidence, places=2)
        self.assertLessEqual(overall_confidence, 1.0)

    # CRITICAL TEST 13: Serialization and Data Persistence
    def test_serialization_and_data_persistence(self):
        """
        CRITICAL: Test complete analysis serialization for persistence
        """
        # Create sample comprehensive analysis
        analysis = ComprehensiveAnalysis(
            jenkins_url=self.sample_jenkins_url,
            investigation_result=InvestigationResult(
                jenkins_intelligence=JenkinsIntelligence(
                    metadata=JenkinsMetadata(
                        build_url=self.sample_jenkins_url,
                        job_name="test-pipeline",
                        build_number=123,
                        build_result="FAILURE",
                        timestamp="",
                        parameters={},
                        console_log_snippet="",
                        artifacts=[]
                    ),
                    failure_analysis={},
                    environment_info={},
                    evidence_sources=[],
                    confidence_score=0.8
                ),
                environment_validation={},
                repository_analysis={},
                evidence_correlation={},
                confidence_score=0.8,
                investigation_time=2.0
            ),
            solution_result=SolutionResult(
                evidence_analysis={},
                bug_classification={'primary_classification': 'AUTOMATION BUG'},
                fix_recommendations=[],
                implementation_guidance={},
                confidence_score=0.7,
                solution_time=1.5
            ),
            overall_classification='AUTOMATION BUG',
            overall_confidence=0.75,
            total_analysis_time=3.5,
            evidence_sources=["[Jenkins:test-pipeline:123:FAILURE]"]
        )
        
        # Test serialization
        serialized = self.framework.to_dict(analysis)
        
        # Validate serialized structure
        required_keys = [
            'jenkins_url', 'investigation_result', 'solution_result',
            'overall_classification', 'overall_confidence', 
            'total_analysis_time', 'evidence_sources'
        ]
        
        for key in required_keys:
            self.assertIn(key, serialized)
        
        # Test JSON serialization
        json_str = json.dumps(serialized)
        self.assertIsInstance(json_str, str)
        
        # Test JSON deserialization
        restored = json.loads(json_str)
        self.assertEqual(restored['jenkins_url'], self.sample_jenkins_url)
        self.assertEqual(restored['overall_classification'], 'AUTOMATION BUG')

    # CRITICAL TEST 14: Agent Coordination and Progressive Context
    @patch.object(InvestigationIntelligenceAgent, 'investigate_pipeline_failure')
    @patch.object(SolutionIntelligenceAgent, 'generate_solution')
    def test_agent_coordination_and_progressive_context(self, mock_solution, mock_investigation):
        """
        CRITICAL: Test progressive context inheritance between agents
        """
        # Create investigation result with specific data
        investigation_data = InvestigationResult(
            jenkins_intelligence=JenkinsIntelligence(
                metadata=JenkinsMetadata(
                    build_url=self.sample_jenkins_url,
                    job_name="test-pipeline",
                    build_number=123,
                    build_result="FAILURE",
                    timestamp="",
                    parameters={"CLUSTER_NAME": "test-cluster"},
                    console_log_snippet="TimeoutError: timeout",
                    artifacts=[]
                ),
                failure_analysis={'primary_failure_type': 'timeout_errors'},
                environment_info={'cluster_name': 'test-cluster'},
                evidence_sources=["[Jenkins:test-pipeline:123:FAILURE]"],
                confidence_score=0.8
            ),
            environment_validation={'cluster_connectivity': True},
            repository_analysis={'repository_cloned': True},
            evidence_correlation={'correlation_score': 0.9},
            confidence_score=0.8,
            investigation_time=2.5
        )
        
        mock_investigation.return_value = investigation_data
        mock_solution.return_value = SolutionResult(
            evidence_analysis={},
            bug_classification={'primary_classification': 'AUTOMATION BUG'},
            fix_recommendations=[],
            implementation_guidance={},
            confidence_score=0.7,
            solution_time=1.5
        )
        
        # Execute analysis
        result = self.framework.analyze_pipeline_failure(self.sample_jenkins_url)
        
        # Verify progressive context: investigation result passed to solution agent
        mock_solution.assert_called_once()
        passed_investigation = mock_solution.call_args[0][0]
        
        self.assertEqual(passed_investigation.confidence_score, investigation_data.confidence_score)
        self.assertEqual(
            passed_investigation.jenkins_intelligence.environment_info['cluster_name'],
            'test-cluster'
        )

    # CRITICAL TEST 15: Performance and Timing Validation
    @patch.object(InvestigationIntelligenceAgent, 'investigate_pipeline_failure')
    @patch.object(SolutionIntelligenceAgent, 'generate_solution')
    def test_performance_and_timing_validation(self, mock_solution, mock_investigation):
        """
        CRITICAL: Test framework performance and timing requirements
        """
        # Mock with realistic timing
        def slow_investigation(*args):
            time.sleep(0.1)  # Simulate 100ms investigation
            return InvestigationResult(
                jenkins_intelligence=JenkinsIntelligence(
                    metadata=JenkinsMetadata(
                        build_url="https://test.com/job/test/123/",
                        job_name="test",
                        build_number=123,
                        build_result="FAILURE",
                        timestamp="",
                        parameters={},
                        console_log_snippet="",
                        artifacts=[]
                    ),
                    failure_analysis={},
                    environment_info={},
                    evidence_sources=["[Jenkins:test:123:FAILURE]"],
                    confidence_score=0.8
                ),
                environment_validation={},
                repository_analysis={},
                evidence_correlation={},
                confidence_score=0.8,
                investigation_time=0.1
            )
        
        def slow_solution(*args):
            time.sleep(0.05)  # Simulate 50ms solution
            return SolutionResult(
                evidence_analysis={},
                bug_classification={'primary_classification': 'AUTOMATION BUG'},
                fix_recommendations=[],
                implementation_guidance={},
                confidence_score=0.7,
                solution_time=0.05
            )
        
        mock_investigation.side_effect = slow_investigation
        mock_solution.side_effect = slow_solution
        
        start_time = time.time()
        result = self.framework.analyze_pipeline_failure(self.sample_jenkins_url)
        total_time = time.time() - start_time
        
        # Framework should complete within reasonable time (< 1 second for mocked operations)
        self.assertLess(total_time, 1.0)
        self.assertGreater(result.total_analysis_time, 0.0)
        
        # Individual agent times should be tracked
        self.assertGreater(result.investigation_result.investigation_time, 0.0)
        self.assertGreater(result.solution_result.solution_time, 0.0)


if __name__ == '__main__':
    # Set up test discovery and execution
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestInvestigationIntelligenceAgent))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestSolutionIntelligenceAgent))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestTwoAgentIntelligenceFramework))
    
    # Run tests with detailed output
    test_runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = test_runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)