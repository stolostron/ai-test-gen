#!/usr/bin/env python3
"""
Phase 3 AI Analysis Unit Tests
============================

Comprehensive unit tests for Phase 3: AI Analysis Implementation
Testing all components of the AIAnalysisEngine with thorough validation.
"""

import unittest
import sys
import os
import json
import asyncio
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass
from typing import Dict, Any, List

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ai_services_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services')
sys.path.insert(0, ai_services_path)

try:
    from phase_3_ai_analysis import (
        AIAnalysisEngine,
        execute_phase_3_analysis
    )
    AI_ANALYSIS_AVAILABLE = True
except ImportError as e:
    AI_ANALYSIS_AVAILABLE = False
    print(f"❌ Phase 3 AI Analysis not available: {e}")


@dataclass
class MockAgentResult:
    """Mock agent result for testing"""
    agent_id: str
    agent_name: str
    execution_status: str
    execution_time: float
    output_file: str
    findings: Dict[str, Any]
    confidence_score: float


@dataclass
class MockPhaseResult:
    """Mock phase result for testing"""
    agent_results: List[MockAgentResult]
    phase_success: bool
    total_execution_time: float


class TestAIAnalysisEngine(unittest.TestCase):
    """Test AI Analysis Engine core functionality"""
    
    @classmethod
    def setUpClass(cls):
        if not AI_ANALYSIS_AVAILABLE:
            cls.skipTest(cls, "Phase 3 AI Analysis not available")
    
    def setUp(self):
        """Set up test environment"""
        self.engine = AIAnalysisEngine()
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None
        
        # Create comprehensive mock data
        self.mock_phase_1_result = MockPhaseResult(
            agent_results=[
                MockAgentResult(
                    agent_id='agent_a_jira_intelligence',
                    agent_name='Agent A - JIRA Intelligence',
                    execution_status='success',
                    execution_time=1.5,
                    output_file='/test/agent_a.json',
                    findings={
                        'requirement_analysis': {
                            'primary_requirements': ['Cluster Management', 'Policy Enforcement'],
                            'component_focus': 'cluster-curator-controller',
                            'priority_level': 'High',
                            'version_target': '2.15.0'
                        },
                        'dependency_mapping': {
                            'component_dependencies': ['cluster-curator-controller', 'multicluster-engine'],
                            'version_dependencies': ['2.15.0']
                        }
                    },
                    confidence_score=0.85
                ),
                MockAgentResult(
                    agent_id='agent_d_environment_intelligence',
                    agent_name='Agent D - Environment Intelligence',
                    execution_status='success',
                    execution_time=1.2,
                    output_file='/test/agent_d.json',
                    findings={
                        'environment_assessment': {
                            'cluster_name': 'test-cluster',
                            'version': '4.12.0',
                            'platform': 'OpenShift',
                            'health_status': 'healthy',
                            'connectivity_confirmed': True
                        },
                        'tooling_analysis': {
                            'available_tools': {'oc': True, 'kubectl': True, 'gh': True, 'curl': True, 'docker': True},
                            'primary_tool': 'oc'
                        }
                    },
                    confidence_score=0.92
                )
            ],
            phase_success=True,
            total_execution_time=2.7
        )
        
        self.mock_phase_2_result = MockPhaseResult(
            agent_results=[
                MockAgentResult(
                    agent_id='agent_b_documentation_intelligence',
                    agent_name='Agent B - Documentation Intelligence',
                    execution_status='success',
                    execution_time=2.1,
                    output_file='/test/agent_b.json',
                    findings={
                        'discovered_documentation': [
                            'https://access.redhat.com/documentation/cluster-curator',
                            'https://docs.openshift.com/cluster-curator/2.15.0',
                            'https://github.com/stolostron/cluster-curator-controller/docs'
                        ],
                        'relevance_analysis': {
                            'high_relevance': 'cluster-curator-controller 2.15.0 documentation',
                            'medium_relevance': 'cluster-curator general documentation'
                        }
                    },
                    confidence_score=0.78
                ),
                MockAgentResult(
                    agent_id='agent_c_github_investigation',
                    agent_name='Agent C - GitHub Investigation',
                    execution_status='success',
                    execution_time=1.8,
                    output_file='/test/agent_c.json',
                    findings={
                        'repository_analysis': {
                            'target_repositories': [
                                'stolostron/cluster-curator-controller',
                                'open-cluster-management-io/cluster-curator-controller'
                            ],
                            'search_queries': [
                                'ACM-22079 in:comments',
                                'cluster-curator-controller is:pr'
                            ]
                        },
                        'implementation_details': {
                            'pr_references': ['#468', '#475'],
                            'code_changes': ['digest-based upgrades', 'fallback algorithm']
                        }
                    },
                    confidence_score=0.88
                )
            ],
            phase_success=True,
            total_execution_time=3.9
        )
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_ai_analysis_engine_initialization(self):
        """Test AI Analysis Engine initializes correctly"""
        engine = AIAnalysisEngine()
        
        self.assertIsInstance(engine.analysis_results, dict)
        self.assertEqual(len(engine.analysis_results), 0)
        
        # Verify initial state
        self.assertIsNotNone(engine)
    
    def test_collect_agent_intelligence(self):
        """Test collection of agent intelligence from Phase 1 & 2"""
        intelligence = self.engine._collect_agent_intelligence(
            self.mock_phase_1_result, 
            self.mock_phase_2_result
        )
        
        # Verify structure
        self.assertIn('jira_intelligence', intelligence)
        self.assertIn('environment_intelligence', intelligence)
        self.assertIn('documentation_intelligence', intelligence)
        self.assertIn('github_intelligence', intelligence)
        self.assertIn('collection_timestamp', intelligence)
        
        # Verify JIRA intelligence
        jira_intel = intelligence['jira_intelligence']
        self.assertIn('findings', jira_intel)
        self.assertIn('confidence', jira_intel)
        self.assertEqual(jira_intel['confidence'], 0.85)
        self.assertIn('requirement_analysis', jira_intel['findings'])
        
        # Verify Environment intelligence
        env_intel = intelligence['environment_intelligence']
        self.assertEqual(env_intel['confidence'], 0.92)
        self.assertIn('environment_assessment', env_intel['findings'])
        
        # Verify Documentation intelligence
        doc_intel = intelligence['documentation_intelligence']
        self.assertEqual(doc_intel['confidence'], 0.78)
        self.assertEqual(len(doc_intel['findings']['discovered_documentation']), 3)
        
        # Verify GitHub intelligence
        github_intel = intelligence['github_intelligence']
        self.assertEqual(github_intel['confidence'], 0.88)
        self.assertEqual(len(github_intel['findings']['repository_analysis']['target_repositories']), 2)
    
    async def test_analyze_complexity(self):
        """Test complexity analysis functionality"""
        intelligence = self.engine._collect_agent_intelligence(
            self.mock_phase_1_result, 
            self.mock_phase_2_result
        )
        
        complexity_analysis = await self.engine._analyze_complexity(intelligence)
        
        # Verify structure
        self.assertIn('complexity_factors', complexity_analysis)
        self.assertIn('overall_complexity', complexity_analysis)
        self.assertIn('complexity_level', complexity_analysis)
        self.assertIn('optimal_test_steps', complexity_analysis)
        self.assertIn('recommended_test_cases', complexity_analysis)
        
        # Verify complexity factors
        factors = complexity_analysis['complexity_factors']
        self.assertIn('jira_complexity', factors)
        self.assertIn('technical_complexity', factors)
        self.assertIn('integration_complexity', factors)
        self.assertIn('environment_complexity', factors)
        
        # Verify calculated values
        self.assertGreaterEqual(complexity_analysis['overall_complexity'], 0.0)
        self.assertLessEqual(complexity_analysis['overall_complexity'], 1.0)
        self.assertIn(complexity_analysis['complexity_level'], ['Low', 'Medium', 'High'])
        self.assertGreaterEqual(complexity_analysis['optimal_test_steps'], 4)
        self.assertLessEqual(complexity_analysis['optimal_test_steps'], 10)
        self.assertGreaterEqual(complexity_analysis['recommended_test_cases'], 2)
    
    async def test_perform_ultrathink_analysis(self):
        """Test ultrathink strategic analysis"""
        intelligence = self.engine._collect_agent_intelligence(
            self.mock_phase_1_result, 
            self.mock_phase_2_result
        )
        
        strategic_analysis = await self.engine._perform_ultrathink_analysis(intelligence)
        
        # Verify structure
        self.assertIn('strategic_priorities', strategic_analysis)
        self.assertIn('risk_factors', strategic_analysis)
        self.assertIn('testing_focus_areas', strategic_analysis)
        self.assertIn('strategic_recommendations', strategic_analysis)
        self.assertIn('confidence_score', strategic_analysis)
        
        # Verify content
        self.assertIsInstance(strategic_analysis['strategic_priorities'], list)
        self.assertIsInstance(strategic_analysis['risk_factors'], list)
        self.assertIsInstance(strategic_analysis['testing_focus_areas'], list)
        self.assertIsInstance(strategic_analysis['strategic_recommendations'], list)
        
        # Verify confidence score
        self.assertGreaterEqual(strategic_analysis['confidence_score'], 0.8)
        self.assertLessEqual(strategic_analysis['confidence_score'], 1.0)
        
        # Check for key priorities based on mock data
        priorities_text = ' '.join(strategic_analysis['strategic_priorities'])
        self.assertIn('cluster-curator-controller', priorities_text)
        self.assertIn('High', priorities_text)
    
    async def test_perform_smart_scoping(self):
        """Test smart scoping analysis"""
        intelligence = self.engine._collect_agent_intelligence(
            self.mock_phase_1_result, 
            self.mock_phase_2_result
        )
        complexity_analysis = await self.engine._analyze_complexity(intelligence)
        
        scoping_analysis = await self.engine._perform_smart_scoping(intelligence, complexity_analysis)
        
        # Verify structure
        self.assertIn('testing_scope', scoping_analysis)
        self.assertIn('coverage_approach', scoping_analysis)
        self.assertIn('optimal_test_steps', scoping_analysis)
        self.assertIn('estimated_effort', scoping_analysis)
        self.assertIn('testing_boundaries', scoping_analysis)
        self.assertIn('resource_allocation', scoping_analysis)
        
        # Verify testing scope
        self.assertIn(scoping_analysis['testing_scope'], ['Focused', 'Comprehensive', 'Extensive'])
        
        # Verify testing boundaries
        boundaries = scoping_analysis['testing_boundaries']
        self.assertIn('in_scope', boundaries)
        self.assertIn('out_of_scope', boundaries)
        self.assertIsInstance(boundaries['in_scope'], list)
        self.assertIsInstance(boundaries['out_of_scope'], list)
        
        # Verify resource allocation
        allocation = scoping_analysis['resource_allocation']
        self.assertIn('preparation', allocation)
        self.assertIn('execution', allocation)
        self.assertIn('validation', allocation)
    
    async def test_generate_professional_titles(self):
        """Test professional title generation"""
        intelligence = self.engine._collect_agent_intelligence(
            self.mock_phase_1_result, 
            self.mock_phase_2_result
        )
        complexity_analysis = await self.engine._analyze_complexity(intelligence)
        
        title_recommendations = await self.engine._generate_professional_titles(intelligence, complexity_analysis)
        
        # Verify structure
        self.assertIn('base_component', title_recommendations)
        self.assertIn('title_patterns', title_recommendations)
        self.assertIn('naming_convention', title_recommendations)
        self.assertIn('recommended_count', title_recommendations)
        
        # Verify content
        self.assertEqual(title_recommendations['base_component'], 'cluster-curator-controller')
        self.assertIsInstance(title_recommendations['title_patterns'], list)
        self.assertGreater(len(title_recommendations['title_patterns']), 0)
        
        # Verify naming convention
        self.assertIn('Action', title_recommendations['naming_convention'])
        self.assertIn('Component', title_recommendations['naming_convention'])
        
        # Check title patterns contain component name
        for pattern in title_recommendations['title_patterns']:
            self.assertIn('cluster-curator-controller', pattern)
    
    def test_synthesize_strategic_intelligence(self):
        """Test strategic intelligence synthesis"""
        intelligence = self.engine._collect_agent_intelligence(
            self.mock_phase_1_result, 
            self.mock_phase_2_result
        )
        
        # Create mock analysis results
        complexity_analysis = {
            'complexity_level': 'High',
            'overall_complexity': 0.75,
            'optimal_test_steps': 10,
            'recommended_test_cases': 4
        }
        
        strategic_analysis = {
            'strategic_priorities': ['Priority 1', 'Priority 2'],
            'risk_factors': ['Risk 1'],
            'testing_focus_areas': ['Focus 1', 'Focus 2'],
            'strategic_recommendations': ['Recommendation 1'],
            'confidence_score': 0.92
        }
        
        scoping_analysis = {
            'testing_scope': 'Extensive',
            'coverage_approach': 'Complete coverage including stress testing',
            'optimal_test_steps': 10
        }
        
        title_recommendations = {
            'base_component': 'cluster-curator-controller',
            'title_patterns': ['Pattern 1', 'Pattern 2'],
            'recommended_count': 4
        }
        
        strategic_intelligence = self.engine._synthesize_strategic_intelligence(
            intelligence, complexity_analysis, strategic_analysis, 
            scoping_analysis, title_recommendations
        )
        
        # Verify structure
        self.assertIn('analysis_timestamp', strategic_intelligence)
        self.assertIn('overall_confidence', strategic_intelligence)
        self.assertIn('agent_intelligence_summary', strategic_intelligence)
        self.assertIn('complexity_assessment', strategic_intelligence)
        self.assertIn('strategic_priorities', strategic_intelligence)
        self.assertIn('testing_scope', strategic_intelligence)
        self.assertIn('title_generation', strategic_intelligence)
        self.assertIn('phase_4_directives', strategic_intelligence)
        self.assertIn('quality_indicators', strategic_intelligence)
        
        # Verify confidence calculation
        self.assertGreaterEqual(strategic_intelligence['overall_confidence'], 0.0)
        self.assertLessEqual(strategic_intelligence['overall_confidence'], 1.0)
        
        # Verify phase 4 directives
        directives = strategic_intelligence['phase_4_directives']
        self.assertIn('test_case_count', directives)
        self.assertIn('steps_per_case', directives)
        self.assertIn('testing_approach', directives)
        self.assertIn('title_patterns', directives)
        
        # Verify quality indicators
        quality = strategic_intelligence['quality_indicators']
        self.assertIn('data_completeness', quality)
        self.assertIn('analysis_depth', quality)
        self.assertIn('strategic_clarity', quality)
    
    async def test_save_analysis_results(self):
        """Test saving analysis results to file"""
        strategic_intelligence = {
            'test_data': 'value',
            'analysis_timestamp': '2025-01-01T00:00:00'
        }
        
        output_file = await self.engine._save_analysis_results(strategic_intelligence, self.test_dir)
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(output_file.endswith('phase_3_strategic_intelligence.json'))
        
        # Verify file content
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data, strategic_intelligence)
    
    async def test_execute_ai_analysis_phase_success(self):
        """Test complete AI analysis phase execution - success case"""
        result = await self.engine.execute_ai_analysis_phase(
            self.mock_phase_1_result,
            self.mock_phase_2_result,
            None,  # inheritance_chain not used in current implementation
            self.test_dir
        )
        
        # Verify result structure
        self.assertIn('phase_name', result)
        self.assertIn('execution_status', result)
        self.assertIn('execution_time', result)
        self.assertIn('output_file', result)
        self.assertIn('strategic_intelligence', result)
        self.assertIn('analysis_confidence', result)
        
        # Verify success
        self.assertEqual(result['execution_status'], 'success')
        self.assertEqual(result['phase_name'], 'Phase 3 - AI Analysis')
        self.assertGreaterEqual(result['execution_time'], 0)
        self.assertIsNotNone(result['output_file'])
        self.assertTrue(os.path.exists(result['output_file']))
        
        # Verify strategic intelligence
        intelligence = result['strategic_intelligence']
        self.assertIn('overall_confidence', intelligence)
        self.assertIn('phase_4_directives', intelligence)
    
    async def test_execute_ai_analysis_phase_failure(self):
        """Test AI analysis phase execution - failure case"""
        # Create invalid phase results to trigger failure
        invalid_phase_result = None
        
        result = await self.engine.execute_ai_analysis_phase(
            invalid_phase_result,
            self.mock_phase_2_result,
            None,
            self.test_dir
        )
        
        # Verify failure handling
        self.assertEqual(result['execution_status'], 'failed')
        self.assertIn('error_message', result)


class TestPhase3ConvenienceFunctions(unittest.TestCase):
    """Test Phase 3 convenience functions"""
    
    @classmethod
    def setUpClass(cls):
        if not AI_ANALYSIS_AVAILABLE:
            cls.skipTest(cls, "Phase 3 AI Analysis not available")
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        
        # Create mock phase results
        self.mock_phase_1 = MockPhaseResult(
            agent_results=[
                MockAgentResult(
                    agent_id='agent_a_jira_intelligence',
                    agent_name='Agent A',
                    execution_status='success',
                    execution_time=1.0,
                    output_file='/test/a.json',
                    findings={'test': 'data'},
                    confidence_score=0.8
                )
            ],
            phase_success=True,
            total_execution_time=1.0
        )
        
        self.mock_phase_2 = MockPhaseResult(
            agent_results=[
                MockAgentResult(
                    agent_id='agent_b_documentation_intelligence',
                    agent_name='Agent B',
                    execution_status='success',
                    execution_time=1.0,
                    output_file='/test/b.json',
                    findings={'test': 'data'},
                    confidence_score=0.8
                )
            ],
            phase_success=True,
            total_execution_time=1.0
        )
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    async def test_execute_phase_3_analysis_convenience_function(self):
        """Test the convenience function for Phase 3 execution"""
        result = await execute_phase_3_analysis(
            self.mock_phase_1,
            self.mock_phase_2, 
            None,
            self.test_dir
        )
        
        # Verify result
        self.assertIn('execution_status', result)
        self.assertEqual(result['execution_status'], 'success')
        self.assertIn('strategic_intelligence', result)


class TestPhase3EdgeCases(unittest.TestCase):
    """Test Phase 3 edge cases and error conditions"""
    
    @classmethod
    def setUpClass(cls):
        if not AI_ANALYSIS_AVAILABLE:
            cls.skipTest(cls, "Phase 3 AI Analysis not available")
    
    def setUp(self):
        """Set up test environment"""
        self.engine = AIAnalysisEngine()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_collect_intelligence_empty_phases(self):
        """Test intelligence collection with empty phase results"""
        empty_phase = MockPhaseResult(agent_results=[], phase_success=False, total_execution_time=0)
        
        intelligence = self.engine._collect_agent_intelligence(empty_phase, empty_phase)
        
        # Verify structure is maintained
        self.assertIn('jira_intelligence', intelligence)
        self.assertIn('environment_intelligence', intelligence)
        self.assertIn('documentation_intelligence', intelligence)
        self.assertIn('github_intelligence', intelligence)
        
        # Verify empty data handling
        self.assertEqual(intelligence['jira_intelligence'], {})
        self.assertEqual(intelligence['environment_intelligence'], {})
    
    async def test_complexity_analysis_missing_data(self):
        """Test complexity analysis with missing agent data"""
        minimal_intelligence = {
            'jira_intelligence': {},
            'environment_intelligence': {},
            'documentation_intelligence': {},
            'github_intelligence': {},
            'collection_timestamp': '2025-01-01T00:00:00'
        }
        
        complexity_analysis = await self.engine._analyze_complexity(minimal_intelligence)
        
        # Verify graceful handling
        self.assertIn('complexity_factors', complexity_analysis)
        self.assertIn('overall_complexity', complexity_analysis)
        self.assertIn('complexity_level', complexity_analysis)
        
        # Should provide default values
        self.assertGreaterEqual(complexity_analysis['optimal_test_steps'], 4)
        self.assertLessEqual(complexity_analysis['optimal_test_steps'], 10)
    
    async def test_strategic_analysis_minimal_input(self):
        """Test strategic analysis with minimal input"""
        minimal_intelligence = {
            'jira_intelligence': {'findings': {}},
            'environment_intelligence': {'findings': {}},
            'documentation_intelligence': {'findings': {}},
            'github_intelligence': {'findings': {}}
        }
        
        strategic_analysis = await self.engine._perform_ultrathink_analysis(minimal_intelligence)
        
        # Verify structure maintained
        self.assertIn('strategic_priorities', strategic_analysis)
        self.assertIn('risk_factors', strategic_analysis)
        self.assertIn('testing_focus_areas', strategic_analysis)
        self.assertIn('strategic_recommendations', strategic_analysis)
        
        # Should provide sensible defaults
        self.assertIsInstance(strategic_analysis['strategic_priorities'], list)
        self.assertIsInstance(strategic_analysis['strategic_recommendations'], list)


if __name__ == '__main__':
    print("🧪 Phase 3 AI Analysis Unit Tests")
    print("=" * 45)
    print("Testing AI Analysis Engine comprehensive functionality")
    print("=" * 45)
    
    if not AI_ANALYSIS_AVAILABLE:
        print("❌ Phase 3 AI Analysis not available - skipping tests")
        exit(1)
    
    # Run tests with async support
    def run_async_test(test_func):
        """Helper to run async test functions"""
        return asyncio.run(test_func())
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestAIAnalysisEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase3ConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase3EdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print(f"\n📊 Phase 3 Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
    
    exit(0 if result.wasSuccessful() else 1)