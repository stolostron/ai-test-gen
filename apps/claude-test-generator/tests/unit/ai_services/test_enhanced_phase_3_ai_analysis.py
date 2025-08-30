#!/usr/bin/env python3
"""
Unit Tests for Enhanced Phase 3: AI Analysis
=============================================

Comprehensive unit tests for the Enhanced Phase 3 AI Analysis engine
that processes complete agent intelligence + QE insights for superior
strategic intelligence synthesis.

Test Coverage:
- Enhanced AI Analysis Engine functionality
- Complete context processing
- QE Intelligence integration
- Strategic intelligence synthesis
- Enhanced complexity detection
- Enhanced title generation
- Enhanced scoping analysis
"""

import unittest
import asyncio
import tempfile
import os
import sys
import json
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime

# Add the ai-services directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services'))

from phase_3_analysis import (
    AIAnalysisEngine,
    execute_phase_3_analysis
)
from parallel_data_flow import (
    Phase3Input,
    AgentIntelligencePackage,
    QEIntelligencePackage
)


class TestAIAnalysisEngine(unittest.TestCase):
    """Test Enhanced AI Analysis Engine functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.analysis_engine = AIAnalysisEngine()
        
        # Mock enhanced Phase 3 input with complete context
        self.mock_agent_packages = [
            AgentIntelligencePackage(
                agent_id="agent_a_jira_intelligence",
                agent_name="JIRA Intelligence Agent",
                execution_status="success",
                findings_summary={
                    'component': 'cluster-curator',
                    'priority': 'High'
                },
                detailed_analysis_file="",
                detailed_analysis_content={
                    'requirement_analysis': {
                        'primary_requirements': ['ClusterCurator digest-based upgrades', 'Amadeus disconnected environment'],
                        'component_focus': 'cluster-curator',
                        'priority_level': 'High',
                        'version_target': 'ACM 2.15.0',
                        'detailed_description': 'A' * 1000  # 1KB of detailed content
                    },
                    'dependency_mapping': {
                        'component_dependencies': ['ClusterCurator', 'Controller']
                    }
                },
                confidence_score=0.95,
                execution_time=1.5,
                context_metadata={}
            ),
            AgentIntelligencePackage(
                agent_id="agent_d_environment_intelligence",
                agent_name="Environment Intelligence Agent",
                execution_status="success",
                findings_summary={
                    'cluster': 'mist10',
                    'health': 'healthy'
                },
                detailed_analysis_file="",
                detailed_analysis_content={
                    'environment_assessment': {
                        'cluster_name': 'mist10',
                        'version': 'ACM 2.14.0',
                        'health_status': 'healthy'
                    },
                    'sample_data': {
                        'clustercurator_yamls': ['yaml1', 'yaml2'],
                        'controller_logs': ['log1', 'log2']
                    },
                    'tooling_analysis': {
                        'available_tools': {'oc': True, 'kubectl': True, 'gh': True}
                    }
                },
                confidence_score=0.88,
                execution_time=2.1,
                context_metadata={}
            ),
            AgentIntelligencePackage(
                agent_id="agent_b_documentation_intelligence",
                agent_name="Documentation Intelligence Agent",
                execution_status="success",
                findings_summary={
                    'docs_analyzed': 5,
                    'workflow_coverage': 'comprehensive'
                },
                detailed_analysis_file="",
                detailed_analysis_content={
                    'discovered_documentation': [
                        {'name': 'User Guide', 'coverage': 'high'},
                        {'name': 'API Reference', 'coverage': 'medium'},
                        {'name': 'Troubleshooting Guide', 'coverage': 'high'}
                    ],
                    'user_workflow_analysis': {
                        'primary_workflows': ['upgrade', 'configuration'],
                        'workflow_complexity': 'medium'
                    }
                },
                confidence_score=0.92,
                execution_time=1.8,
                context_metadata={}
            ),
            AgentIntelligencePackage(
                agent_id="agent_c_github_investigation",
                agent_name="GitHub Investigation Agent",
                execution_status="success",
                findings_summary={
                    'repositories_analyzed': 2,
                    'implementation_status': 'active'
                },
                detailed_analysis_file="",
                detailed_analysis_content={
                    'repository_analysis': {
                        'target_repositories': [
                            'stolostron/cluster-curator-controller',
                            'stolostron/multicloud-operators-foundation'
                        ],
                        'implementation_details': {
                            'pr_analysis': 'PR #468 implements 3-tier fallback algorithm',
                            'code_changes': '400+ lines of changes'
                        }
                    }
                },
                confidence_score=0.85,
                execution_time=1.6,
                context_metadata={}
            )
        ]
        
        self.mock_qe_intelligence = QEIntelligencePackage(
            service_name="QEIntelligenceService",
            execution_status="success",
            repository_analysis={
                'test_file_count': 78,
                'primary_repository': 'stolostron/clc-ui-e2e',
                'coverage_areas': ['UI', 'API', 'Integration']
            },
            test_patterns=[
                {
                    'pattern_name': 'Core Workflow Pattern',
                    'pattern_type': 'End-to-End',
                    'usage_frequency': 'High',
                    'test_steps_range': (6, 8)
                },
                {
                    'pattern_name': 'Error Handling Pattern',
                    'pattern_type': 'Validation',
                    'usage_frequency': 'Medium',
                    'test_steps_range': (4, 6)
                }
            ],
            coverage_gaps={
                'identified_gaps': ['Advanced scenarios', 'Edge cases'],
                'gap_priority': {
                    'Advanced scenarios': 'High',
                    'Edge cases': 'Medium'
                }
            },
            automation_insights={
                'frameworks_identified': ['Cypress'],
                'test_file_count': 78,
                'coverage_areas': ['UI automation', 'API testing']
            },
            testing_recommendations=[
                'Implement comprehensive E2E testing',
                'Add error handling test scenarios'
            ],
            execution_time=2.5,
            confidence_score=0.92
        )
        
        self.mock_phase_3_input = Phase3Input(
            phase_1_result=None,
            phase_2_result=None,
            agent_intelligence_packages=self.mock_agent_packages,
            qe_intelligence=self.mock_qe_intelligence,
            data_flow_timestamp=datetime.now().isoformat(),
            data_preservation_verified=True,
            total_context_size_kb=25.5
        )
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_enhanced_ai_analysis_engine_initialization(self):
        """Test Enhanced AI Analysis Engine initialization"""
        self.assertIsInstance(self.analysis_engine, AIAnalysisEngine)
        self.assertIsInstance(self.analysis_engine.analysis_results, dict)
    
    def test_process_complete_agent_intelligence(self):
        """Test processing complete agent intelligence with full context preservation"""
        complete_intelligence = self.analysis_engine._process_complete_agent_intelligence(
            self.mock_agent_packages
        )
        
        # Verify structure
        self.assertIn('agent_packages_count', complete_intelligence)
        self.assertIn('total_execution_time', complete_intelligence)
        self.assertIn('average_confidence', complete_intelligence)
        self.assertIn('agents', complete_intelligence)
        
        # Verify agent count
        self.assertEqual(complete_intelligence['agent_packages_count'], 4)
        
        # Verify all agents processed
        expected_agents = [
            'agent_a_jira_intelligence',
            'agent_d_environment_intelligence', 
            'agent_b_documentation_intelligence',
            'agent_c_github_investigation'
        ]
        
        for agent_id in expected_agents:
            self.assertIn(agent_id, complete_intelligence['agents'])
            agent_data = complete_intelligence['agents'][agent_id]
            self.assertIn('summary_findings', agent_data)
            self.assertIn('detailed_analysis', agent_data)
            self.assertIn('confidence', agent_data)
            self.assertTrue(len(agent_data['detailed_analysis']) > 0)
        
        # Verify intelligence extraction
        self.assertIn('jira_intelligence', complete_intelligence)
        self.assertIn('environment_intelligence', complete_intelligence)
        self.assertIn('documentation_intelligence', complete_intelligence)
        self.assertIn('github_intelligence', complete_intelligence)
        
        # Verify JIRA intelligence preservation
        jira_intel = complete_intelligence['jira_intelligence']
        self.assertTrue(jira_intel['preservation_verified'])
        self.assertEqual(jira_intel['confidence'], 0.95)
        self.assertIn('requirement_analysis', jira_intel['detailed'])
    
    def test_extract_complete_jira_intelligence(self):
        """Test JIRA intelligence extraction with full detail preservation"""
        jira_intelligence = self.analysis_engine._extract_complete_jira_intelligence(
            self.mock_agent_packages
        )
        
        self.assertIn('summary', jira_intelligence)
        self.assertIn('detailed', jira_intelligence)
        self.assertIn('confidence', jira_intelligence)
        self.assertIn('preservation_verified', jira_intelligence)
        
        # Verify detailed content preserved
        self.assertTrue(jira_intelligence['preservation_verified'])
        self.assertEqual(jira_intelligence['confidence'], 0.95)
        self.assertIn('requirement_analysis', jira_intelligence['detailed'])
        
        # Verify specific requirement analysis content
        req_analysis = jira_intelligence['detailed']['requirement_analysis']
        self.assertIn('primary_requirements', req_analysis)
        self.assertEqual(req_analysis['component_focus'], 'cluster-curator')
        self.assertEqual(req_analysis['priority_level'], 'High')
    
    def test_extract_complete_environment_intelligence(self):
        """Test environment intelligence extraction with full detail preservation"""
        env_intelligence = self.analysis_engine._extract_complete_environment_intelligence(
            self.mock_agent_packages
        )
        
        self.assertIn('summary', env_intelligence)
        self.assertIn('detailed', env_intelligence)
        self.assertIn('confidence', env_intelligence)
        self.assertIn('sample_data', env_intelligence)
        self.assertIn('preservation_verified', env_intelligence)
        
        # Verify detailed content preserved
        self.assertTrue(env_intelligence['preservation_verified'])
        self.assertEqual(env_intelligence['confidence'], 0.88)
        
        # Verify environment assessment content
        env_assessment = env_intelligence['detailed']['environment_assessment']
        self.assertEqual(env_assessment['cluster_name'], 'mist10')
        self.assertEqual(env_assessment['health_status'], 'healthy')
        
        # Verify sample data preserved
        sample_data = env_intelligence['sample_data']
        self.assertIn('clustercurator_yamls', sample_data)
        self.assertIn('controller_logs', sample_data)
    
    def test_integrate_qe_insights(self):
        """Test QE repository insights integration"""
        integrated_insights = self.analysis_engine._integrate_qe_insights(
            self.mock_qe_intelligence
        )
        
        # Verify integration structure
        self.assertIn('execution_status', integrated_insights)
        self.assertIn('confidence', integrated_insights)
        self.assertIn('integration_successful', integrated_insights)
        self.assertIn('qe_enhancement_available', integrated_insights)
        
        # Verify successful integration
        self.assertEqual(integrated_insights['execution_status'], 'success')
        self.assertEqual(integrated_insights['confidence'], 0.92)
        self.assertTrue(integrated_insights['integration_successful'])
        self.assertTrue(integrated_insights['qe_enhancement_available'])
        
        # Verify QE insights preserved
        self.assertIn('repository_analysis', integrated_insights)
        self.assertIn('test_patterns', integrated_insights)
        self.assertIn('coverage_gaps', integrated_insights)
        self.assertIn('automation_insights', integrated_insights)
        self.assertIn('testing_recommendations', integrated_insights)
        
        # Verify specific QE data
        self.assertEqual(len(integrated_insights['test_patterns']), 2)
        self.assertEqual(len(integrated_insights['testing_recommendations']), 2)
    
    async def test_enhanced_complexity_analysis(self):
        """Test enhanced complexity analysis using complete context + QE insights"""
        complete_intelligence = self.analysis_engine._process_complete_agent_intelligence(
            self.mock_agent_packages
        )
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        enhanced_complexity = await self.analysis_engine._enhanced_complexity_analysis(
            complete_intelligence, qe_insights
        )
        
        # Verify complexity structure
        self.assertIn('base_complexity', enhanced_complexity)
        self.assertIn('qe_complexity_factors', enhanced_complexity)
        self.assertIn('overall_complexity', enhanced_complexity)
        self.assertIn('complexity_level', enhanced_complexity)
        self.assertIn('optimal_test_steps', enhanced_complexity)
        self.assertIn('recommended_test_cases', enhanced_complexity)
        self.assertIn('qe_enhancement_applied', enhanced_complexity)
        self.assertIn('complete_context_used', enhanced_complexity)
        
        # Verify enhanced analysis
        self.assertTrue(enhanced_complexity['qe_enhancement_applied'])
        self.assertTrue(enhanced_complexity['complete_context_used'])
        self.assertIn(enhanced_complexity['complexity_level'], ['Low', 'Medium', 'High'])
        self.assertGreater(enhanced_complexity['optimal_test_steps'], 0)
        self.assertGreater(enhanced_complexity['recommended_test_cases'], 0)
        self.assertLessEqual(enhanced_complexity['recommended_test_cases'], 6)  # Capped at 6
        
        # Verify QE bonus test cases applied
        if qe_insights.get('test_patterns'):
            expected_bonus = len(qe_insights['test_patterns']) // 3
            self.assertGreaterEqual(enhanced_complexity['recommended_test_cases'], 2 + expected_bonus)
    
    async def test_calculate_base_complexity(self):
        """Test base complexity calculation from complete agent intelligence"""
        complete_intelligence = self.analysis_engine._process_complete_agent_intelligence(
            self.mock_agent_packages
        )
        
        base_complexity = await self.analysis_engine._calculate_base_complexity(complete_intelligence)
        
        self.assertIn('complexity_factors', base_complexity)
        self.assertIn('base_score', base_complexity)
        self.assertIn('complete_context_analyzed', base_complexity)
        
        # Verify complete context analysis
        self.assertTrue(base_complexity['complete_context_analyzed'])
        self.assertIsInstance(base_complexity['base_score'], float)
        self.assertGreaterEqual(base_complexity['base_score'], 0.0)
        self.assertLessEqual(base_complexity['base_score'], 1.0)
        
        # Verify complexity factors extraction
        factors = base_complexity['complexity_factors']
        self.assertIn('jira', factors)
        self.assertIn('environment', factors)
    
    def test_analyze_repository_complexity(self):
        """Test QE repository complexity analysis"""
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        repo_complexity = self.analysis_engine._analyze_repository_complexity(qe_insights)
        
        self.assertIsInstance(repo_complexity, float)
        self.assertGreaterEqual(repo_complexity, 0.0)
        self.assertLessEqual(repo_complexity, 1.0)
        
        # With 78 test files, complexity should be calculated appropriately
        expected_complexity = min(78 / 100.0, 0.8)
        self.assertEqual(repo_complexity, expected_complexity)
    
    def test_analyze_test_pattern_complexity(self):
        """Test test pattern complexity analysis"""
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        pattern_complexity = self.analysis_engine._analyze_test_pattern_complexity(qe_insights)
        
        self.assertIsInstance(pattern_complexity, float)
        self.assertGreaterEqual(pattern_complexity, 0.0)
        self.assertLessEqual(pattern_complexity, 1.0)
        
        # With 2 pattern types (End-to-End, Validation), complexity should be calculated
        pattern_types = {'End-to-End', 'Validation'}
        expected_complexity = min(len(pattern_types) / 5.0, 1.0)
        self.assertEqual(pattern_complexity, expected_complexity)
    
    def test_analyze_coverage_complexity(self):
        """Test coverage complexity analysis from QE insights"""
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        coverage_complexity = self.analysis_engine._analyze_coverage_complexity(qe_insights)
        
        self.assertIsInstance(coverage_complexity, float)
        self.assertGreaterEqual(coverage_complexity, 0.0)
        self.assertLessEqual(coverage_complexity, 1.0)
        
        # With 2 coverage gaps, complexity should be calculated
        gaps = ['Advanced scenarios', 'Edge cases']
        expected_complexity = min(len(gaps) / 8.0, 1.0)
        self.assertEqual(coverage_complexity, expected_complexity)
    
    async def test_enhanced_strategic_analysis(self):
        """Test enhanced strategic analysis with complete context + QE insights"""
        complete_intelligence = self.analysis_engine._process_complete_agent_intelligence(
            self.mock_agent_packages
        )
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        enhanced_strategic = await self.analysis_engine._enhanced_strategic_analysis(
            complete_intelligence, qe_insights
        )
        
        # Verify strategic structure
        self.assertIn('base_strategic_analysis', enhanced_strategic)
        self.assertIn('qe_strategic_enhancements', enhanced_strategic)
        self.assertIn('combined_strategic_priorities', enhanced_strategic)
        self.assertIn('enhanced_risk_factors', enhanced_strategic)
        self.assertIn('enhanced_testing_focus', enhanced_strategic)
        self.assertIn('combined_recommendations', enhanced_strategic)
        self.assertIn('confidence_score', enhanced_strategic)
        self.assertIn('qe_enhancement_applied', enhanced_strategic)
        
        # Verify QE enhancement applied
        self.assertTrue(enhanced_strategic['qe_enhancement_applied'])
        self.assertEqual(enhanced_strategic['confidence_score'], 0.95)
        
        # Verify combined recommendations include QE recommendations
        combined_recs = enhanced_strategic['combined_recommendations']
        self.assertGreater(len(combined_recs), 0)
        
        # Verify QE testing recommendations included
        qe_strategic = enhanced_strategic['qe_strategic_enhancements']
        self.assertIn('qe_testing_recommendations', qe_strategic)
        self.assertEqual(len(qe_strategic['qe_testing_recommendations']), 2)
    
    async def test_analyze_base_strategic_priorities(self):
        """Test base strategic priorities analysis"""
        complete_intelligence = self.analysis_engine._process_complete_agent_intelligence(
            self.mock_agent_packages
        )
        
        base_strategic = await self.analysis_engine._analyze_base_strategic_priorities(complete_intelligence)
        
        self.assertIn('strategic_priorities', base_strategic)
        self.assertIn('risk_factors', base_strategic)
        self.assertIn('testing_focus_areas', base_strategic)
        self.assertIn('strategic_recommendations', base_strategic)
        
        # Verify strategic priorities extracted from JIRA intelligence
        priorities = base_strategic['strategic_priorities']
        self.assertGreater(len(priorities), 0)
        
        # Should include component focus and priority level
        priority_text = ' '.join(priorities)
        self.assertIn('cluster-curator', priority_text)
        self.assertIn('High', priority_text)
        
        # Verify testing focus for high priority
        focus_areas = base_strategic['testing_focus_areas']
        self.assertIn('Critical Path Testing', focus_areas)
        self.assertIn('Rapid Validation', focus_areas)
    
    def test_extract_qe_coverage_priorities(self):
        """Test QE coverage priorities extraction"""
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        coverage_priorities = self.analysis_engine._extract_qe_coverage_priorities(qe_insights)
        
        self.assertIsInstance(coverage_priorities, list)
        # Should extract high priority gaps
        self.assertGreater(len(coverage_priorities), 0)
        self.assertIn('High Priority: Advanced scenarios', coverage_priorities)
    
    def test_extract_qe_automation_strategies(self):
        """Test QE automation strategies extraction"""
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        automation_strategies = self.analysis_engine._extract_qe_automation_strategies(qe_insights)
        
        self.assertIsInstance(automation_strategies, list)
        self.assertGreater(len(automation_strategies), 0)
        # Should include Cypress framework
        strategy_text = ' '.join(automation_strategies)
        self.assertIn('Cypress', strategy_text)
    
    def test_extract_qe_pattern_insights(self):
        """Test QE pattern insights extraction"""
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        pattern_insights = self.analysis_engine._extract_qe_pattern_insights(qe_insights)
        
        self.assertIsInstance(pattern_insights, list)
        self.assertGreater(len(pattern_insights), 0)
        self.assertLessEqual(len(pattern_insights), 5)  # Limited to top 5
        
        # Should include pattern names
        insight_text = ' '.join(pattern_insights)
        self.assertIn('Core Workflow Pattern', insight_text)
        self.assertIn('Error Handling Pattern', insight_text)
    
    async def test_enhanced_scoping_analysis(self):
        """Test enhanced scoping analysis with QE coverage insights"""
        complete_intelligence = self.analysis_engine._process_complete_agent_intelligence(
            self.mock_agent_packages
        )
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        # First get enhanced complexity
        enhanced_complexity = await self.analysis_engine._enhanced_complexity_analysis(
            complete_intelligence, qe_insights
        )
        
        enhanced_scoping = await self.analysis_engine._enhanced_scoping_analysis(
            complete_intelligence, qe_insights, enhanced_complexity
        )
        
        # Verify scoping structure
        self.assertIn('testing_scope', enhanced_scoping)
        self.assertIn('coverage_approach', enhanced_scoping)
        self.assertIn('optimal_test_steps', enhanced_scoping)
        self.assertIn('estimated_effort', enhanced_scoping)
        self.assertIn('testing_boundaries', enhanced_scoping)
        self.assertIn('resource_allocation', enhanced_scoping)
        self.assertIn('qe_enhancement_applied', enhanced_scoping)
        
        # Verify QE enhancement applied
        self.assertTrue(enhanced_scoping['qe_enhancement_applied'])
        self.assertIn('QE-Enhanced', enhanced_scoping['testing_scope'])
        self.assertIn('QE repository pattern integration', enhanced_scoping['coverage_approach'])
        
        # Verify testing boundaries include QE-specific items
        boundaries = enhanced_scoping['testing_boundaries']
        self.assertIn('in_scope', boundaries)
        self.assertIn('out_of_scope', boundaries)
        
        in_scope_text = ' '.join(boundaries['in_scope'])
        self.assertIn('QE repository-validated test patterns', in_scope_text)
        self.assertIn('Coverage gap: Advanced scenarios', in_scope_text)
    
    def test_calculate_enhanced_effort(self):
        """Test effort estimation enhanced by QE insights"""
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        # Test different complexity levels
        for complexity_level in ['Low', 'Medium', 'High']:
            effort = self.analysis_engine._calculate_enhanced_effort(complexity_level, qe_insights)
            
            self.assertIsInstance(effort, str)
            self.assertIn('QE-optimized', effort)  # QE enhancement should be applied
    
    async def test_enhanced_title_generation(self):
        """Test enhanced title generation with QE patterns"""
        complete_intelligence = self.analysis_engine._process_complete_agent_intelligence(
            self.mock_agent_packages
        )
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        # Get enhanced complexity for title generation
        enhanced_complexity = await self.analysis_engine._enhanced_complexity_analysis(
            complete_intelligence, qe_insights
        )
        
        enhanced_titles = await self.analysis_engine._enhanced_title_generation(
            complete_intelligence, qe_insights, enhanced_complexity
        )
        
        # Verify title structure
        self.assertIn('base_component', enhanced_titles)
        self.assertIn('title_patterns', enhanced_titles)
        self.assertIn('naming_convention', enhanced_titles)
        self.assertIn('recommended_count', enhanced_titles)
        self.assertIn('qe_enhancement_applied', enhanced_titles)
        
        # Verify component extracted from JIRA intelligence
        self.assertEqual(enhanced_titles['base_component'], 'cluster-curator')
        
        # Verify QE enhancement applied
        self.assertTrue(enhanced_titles['qe_enhancement_applied'])
        
        # Verify title patterns include QE-enhanced patterns
        title_patterns = enhanced_titles['title_patterns']
        self.assertGreater(len(title_patterns), 0)
        self.assertLessEqual(len(title_patterns), 6)  # Limited to 6 patterns
        
        # Should include QE-enhanced titles
        title_text = ' '.join(title_patterns)
        self.assertIn('cluster-curator', title_text)
        self.assertIn('QE-Pattern', title_text)
    
    def test_generate_base_title_patterns(self):
        """Test base title pattern generation"""
        # Test different complexity levels
        test_cases = [
            ('Low', 2),    # Low complexity should generate 2 patterns
            ('Medium', 3), # Medium complexity should generate 3 patterns  
            ('High', 4)    # High complexity should generate 4 patterns
        ]
        
        for complexity_level, expected_count in test_cases:
            patterns = self.analysis_engine._generate_base_title_patterns('cluster-curator', complexity_level)
            
            self.assertEqual(len(patterns), expected_count)
            self.assertTrue(all('cluster-curator' in pattern for pattern in patterns))
            
            if complexity_level == 'Low':
                self.assertIn('Verify cluster-curator Basic Functionality', patterns)
            elif complexity_level == 'Medium':
                self.assertIn('Comprehensive cluster-curator Functionality Testing', patterns)
            elif complexity_level == 'High':
                self.assertIn('Complete cluster-curator System Integration Testing', patterns)
    
    def test_generate_qe_enhanced_titles(self):
        """Test QE-enhanced title pattern generation"""
        test_patterns = [
            {'pattern_type': 'End-to-End'},
            {'pattern_type': 'Validation'},
            {'pattern_type': 'Integration'}
        ]
        
        qe_titles = self.analysis_engine._generate_qe_enhanced_titles('cluster-curator', test_patterns)
        
        self.assertEqual(len(qe_titles), 3)  # Top 3 patterns
        self.assertTrue(all('QE-Pattern cluster-curator' in title for title in qe_titles))
        self.assertIn('QE-Pattern cluster-curator End-to-End', qe_titles)
        self.assertIn('QE-Pattern cluster-curator Validation', qe_titles)
        self.assertIn('QE-Pattern cluster-curator Integration', qe_titles)
    
    def test_synthesize_enhanced_strategic_intelligence(self):
        """Test enhanced strategic intelligence synthesis"""
        complete_intelligence = self.analysis_engine._process_complete_agent_intelligence(
            self.mock_agent_packages
        )
        qe_insights = self.analysis_engine._integrate_qe_insights(self.mock_qe_intelligence)
        
        # Mock the other analysis results
        enhanced_complexity = {
            'complexity_level': 'Medium',
            'optimal_test_steps': 7,
            'recommended_test_cases': 3
        }
        
        enhanced_strategic = {
            'combined_recommendations': ['Test recommendation 1', 'Test recommendation 2'],
            'enhanced_testing_focus': ['Focus area 1', 'Focus area 2'],
            'enhanced_risk_factors': ['Risk factor 1'],
            'confidence_score': 0.95
        }
        
        enhanced_scoping = {
            'coverage_approach': 'Complete coverage with QE repository pattern integration'
        }
        
        enhanced_titles = {
            'title_patterns': ['Pattern 1', 'Pattern 2', 'Pattern 3'],
            'recommended_count': 3
        }
        
        strategic_intelligence = self.analysis_engine._synthesize_enhanced_strategic_intelligence(
            complete_intelligence, qe_insights, enhanced_complexity, enhanced_strategic,
            enhanced_scoping, enhanced_titles
        )
        
        # Verify complete strategic intelligence structure
        self.assertIn('analysis_timestamp', strategic_intelligence)
        self.assertIn('overall_confidence', strategic_intelligence)
        self.assertIn('data_preservation_verified', strategic_intelligence)
        self.assertIn('qe_enhancement_applied', strategic_intelligence)
        self.assertIn('complete_agent_intelligence', strategic_intelligence)
        self.assertIn('qe_insights_integration', strategic_intelligence)
        self.assertIn('enhanced_complexity_assessment', strategic_intelligence)
        self.assertIn('enhanced_strategic_priorities', strategic_intelligence)
        self.assertIn('enhanced_testing_scope', strategic_intelligence)
        self.assertIn('enhanced_title_generation', strategic_intelligence)
        self.assertIn('enhanced_phase_4_directives', strategic_intelligence)
        self.assertIn('enhanced_quality_indicators', strategic_intelligence)
        
        # Verify data preservation and QE enhancement
        self.assertTrue(strategic_intelligence['data_preservation_verified'])
        self.assertTrue(strategic_intelligence['qe_enhancement_applied'])
        
        # Verify overall confidence calculation
        self.assertIsInstance(strategic_intelligence['overall_confidence'], float)
        self.assertGreater(strategic_intelligence['overall_confidence'], 0.8)
        
        # Verify enhanced Phase 4 directives
        phase_4_directives = strategic_intelligence['enhanced_phase_4_directives']
        self.assertIn('test_case_count', phase_4_directives)
        self.assertIn('steps_per_case', phase_4_directives)
        self.assertIn('testing_approach', phase_4_directives)
        self.assertIn('title_patterns', phase_4_directives)
        self.assertIn('focus_areas', phase_4_directives)
        self.assertIn('risk_mitigations', phase_4_directives)
        self.assertIn('qe_patterns_available', phase_4_directives)
        self.assertIn('qe_recommendations', phase_4_directives)
        
        # Verify quality indicators
        quality_indicators = strategic_intelligence['enhanced_quality_indicators']
        self.assertTrue(quality_indicators['complete_context_processed'])
        self.assertEqual(quality_indicators['data_completeness_score'], 1.0)
        self.assertEqual(quality_indicators['qe_integration_score'], 1.0)  # QE available
    
    async def test_save_enhanced_analysis_results(self):
        """Test saving enhanced Phase 3 analysis results"""
        mock_strategic_intelligence = {
            'analysis_timestamp': datetime.now().isoformat(),
            'overall_confidence': 0.95,
            'test_result': 'mock strategic intelligence'
        }
        
        output_file = await self.analysis_engine._save_enhanced_analysis_results(
            mock_strategic_intelligence, self.temp_dir
        )
        
        # Verify file created
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(output_file.endswith('enhanced_phase_3_strategic_intelligence.json'))
        
        # Verify file content
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data['overall_confidence'], 0.95)
        self.assertEqual(saved_data['test_result'], 'mock strategic intelligence')
    
    async def test_execute_enhanced_ai_analysis_phase(self):
        """Test complete enhanced AI analysis phase execution"""
        result = await self.analysis_engine.execute_enhanced_ai_analysis_phase(
            self.mock_phase_3_input, self.temp_dir
        )
        
        # Verify result structure
        self.assertIn('phase_name', result)
        self.assertIn('execution_status', result)
        self.assertIn('execution_time', result)
        self.assertIn('output_file', result)
        self.assertIn('strategic_intelligence', result)
        self.assertIn('analysis_confidence', result)
        self.assertIn('data_preservation_verified', result)
        self.assertIn('total_context_processed_kb', result)
        self.assertIn('qe_intelligence_integrated', result)
        
        # Verify successful execution
        self.assertEqual(result['phase_name'], 'Phase 3 - Enhanced AI Analysis')
        self.assertEqual(result['execution_status'], 'success')
        self.assertIsInstance(result['execution_time'], float)
        self.assertGreater(result['execution_time'], 0)
        
        # Verify analysis confidence
        self.assertGreater(result['analysis_confidence'], 0.8)
        
        # Verify data preservation
        self.assertTrue(result['data_preservation_verified'])
        self.assertEqual(result['total_context_processed_kb'], 25.5)
        self.assertTrue(result['qe_intelligence_integrated'])
        
        # Verify output file created
        self.assertTrue(os.path.exists(result['output_file']))
        
        # Verify strategic intelligence structure
        strategic_intel = result['strategic_intelligence']
        self.assertIn('enhanced_phase_4_directives', strategic_intel)
        self.assertIn('enhanced_quality_indicators', strategic_intel)


class TestEnhancedPhase3Integration(unittest.TestCase):
    """Test Enhanced Phase 3 integration functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    async def test_execute_phase_3_analysis_function(self):
        """Test execute_phase_3_analysis integration function"""
        # Create mock enhanced input
        mock_agent_packages = [
            AgentIntelligencePackage(
                agent_id="agent_a_jira_intelligence",
                agent_name="JIRA Intelligence Agent",
                execution_status="success",
                findings_summary={'component': 'test-component'},
                detailed_analysis_file="",
                detailed_analysis_content={'requirement_analysis': {'component_focus': 'test-component'}},
                confidence_score=0.85,
                execution_time=1.2,
                context_metadata={}
            )
        ]
        
        mock_qe_intelligence = QEIntelligencePackage(
            service_name="QEIntelligenceService",
            execution_status="success",
            repository_analysis={'test_file_count': 50},
            test_patterns=[{'pattern_name': 'Test Pattern', 'pattern_type': 'Validation'}],
            coverage_gaps={'identified_gaps': ['Gap 1']},
            automation_insights={'frameworks_identified': ['Jest']},
            testing_recommendations=['Recommendation 1'],
            execution_time=2.0,
            confidence_score=0.90
        )
        
        mock_phase_3_input = Phase3Input(
            phase_1_result=None,
            phase_2_result=None,
            agent_intelligence_packages=mock_agent_packages,
            qe_intelligence=mock_qe_intelligence,
            data_flow_timestamp=datetime.now().isoformat(),
            data_preservation_verified=True,
            total_context_size_kb=10.0
        )
        
        # Test integration function
        result = await execute_phase_3_analysis(mock_phase_3_input, self.temp_dir)
        
        # Verify integration function works
        self.assertEqual(result['execution_status'], 'success')
        self.assertGreater(result['analysis_confidence'], 0.8)
        self.assertTrue(result['data_preservation_verified'])
        self.assertTrue(result['qe_intelligence_integrated'])


def run_enhanced_phase_3_tests():
    """Run all Enhanced Phase 3 AI Analysis tests"""
    print("🧪 Running Enhanced Phase 3: AI Analysis Unit Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestAIAnalysisEngine))
    test_suite.addTest(unittest.makeSuite(TestEnhancedPhase3Integration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success_rate = ((tests_run - failures - errors) / tests_run * 100) if tests_run > 0 else 0
    
    print(f"\n📊 Enhanced Phase 3 AI Analysis Test Results:")
    print(f"Tests Run: {tests_run}")
    print(f"Failures: {failures}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run async tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    success = run_enhanced_phase_3_tests()
    print(f"\n🎯 Enhanced Phase 3 AI Analysis Tests: {'✅ PASSED' if success else '❌ FAILED'}")