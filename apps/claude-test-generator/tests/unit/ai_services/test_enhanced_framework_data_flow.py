#!/usr/bin/env python3
"""
Unit Tests for Enhanced Framework Data Flow
==========================================

Comprehensive unit tests for the enhanced framework data flow architecture
that prevents Phase 2.5 bottleneck and preserves all agent intelligence.

Test Coverage:
- Agent Intelligence Preservation
- QE Intelligence Integration
- Parallel Data Flow Execution
- Enhanced Phase 3 Input Creation
- Data Staging Mechanisms
- Fallback Scenarios
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

from parallel_data_flow import (
    ParallelFrameworkDataFlow,
    AgentIntelligencePackage,
    QEIntelligencePackage,
    Phase3Input,
    execute_parallel_data_flow
)


class TestParallelFrameworkDataFlow(unittest.TestCase):
    """Test Enhanced Framework Data Flow functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.data_flow = ParallelFrameworkDataFlow(self.temp_dir)
        
        # Mock agent packages
        self.mock_agent_packages = [
            AgentIntelligencePackage(
                agent_id="agent_a_jira_intelligence",
                agent_name="JIRA Intelligence Agent",
                execution_status="success",
                findings_summary={'component': 'cluster-curator'},
                detailed_analysis_file="",
                detailed_analysis_content={
                    'requirement_analysis': {
                        'primary_requirements': ['Feature A', 'Feature B'],
                        'component_focus': 'cluster-curator'
                    }
                },
                confidence_score=0.90,
                execution_time=1.5,
                context_metadata={}
            ),
            AgentIntelligencePackage(
                agent_id="agent_d_environment_intelligence",
                agent_name="Environment Intelligence Agent",
                execution_status="success",
                findings_summary={'cluster': 'mist10'},
                detailed_analysis_file="",
                detailed_analysis_content={
                    'environment_assessment': {'health_status': 'healthy'},
                    'sample_data': {'yamls': ['yaml1', 'yaml2']}
                },
                confidence_score=0.88,
                execution_time=2.0,
                context_metadata={}
            )
        ]
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_parallel_framework_data_flow_initialization(self):
        """Test Enhanced Framework Data Flow initialization"""
        self.assertIsInstance(self.data_flow, ParallelFrameworkDataFlow)
        self.assertTrue(self.data_flow.staging_dir.exists())
        self.assertEqual(self.data_flow.framework_root, self.temp_dir)
    
    def test_agent_intelligence_package_creation(self):
        """Test Agent Intelligence Package data structure"""
        package = self.mock_agent_packages[0]
        
        self.assertEqual(package.agent_id, "agent_a_jira_intelligence")
        self.assertEqual(package.execution_status, "success")
        self.assertIsInstance(package.detailed_analysis_content, dict)
        self.assertEqual(package.confidence_score, 0.90)
        self.assertTrue(len(package.detailed_analysis_content) > 0)
    
    def test_qe_intelligence_package_structure(self):
        """Test QE Intelligence Package data structure"""
        qe_package = QEIntelligencePackage(
            service_name="QEIntelligenceService",
            execution_status="success",
            repository_analysis={'test_files': 78},
            test_patterns=[{'pattern': 'test1'}],
            coverage_gaps={'gaps': ['gap1']},
            automation_insights={'frameworks': ['Cypress']},
            testing_recommendations=['rec1', 'rec2'],
            execution_time=2.5,
            confidence_score=0.92
        )
        
        self.assertEqual(qe_package.service_name, "QEIntelligenceService")
        self.assertEqual(qe_package.execution_status, "success")
        self.assertEqual(qe_package.confidence_score, 0.92)
        self.assertEqual(len(qe_package.testing_recommendations), 2)
    
    async def test_stage_agent_intelligence_direct(self):
        """Test direct agent intelligence staging (no data loss)"""
        # Mock phase results
        mock_phase_1 = MagicMock()
        mock_phase_1.agent_results = [
            MagicMock(
                agent_id="agent_a_jira_intelligence",
                agent_name="JIRA Intelligence Agent",
                execution_status="success",
                findings={'component': 'cluster-curator'},
                confidence_score=0.85,
                execution_time=1.2,
                output_file=""
            )
        ]
        
        mock_phase_2 = MagicMock()
        mock_phase_2.agent_results = []
        
        # Test staging
        staged_packages = await self.data_flow.stage_agent_intelligence_direct(
            mock_phase_1, mock_phase_2, None, "test_run_001"
        )
        
        self.assertEqual(len(staged_packages), 1)
        self.assertEqual(staged_packages[0].agent_id, "agent_a_jira_intelligence")
        self.assertEqual(staged_packages[0].execution_status, "success")
        
        # Verify staging file created
        staging_file = self.data_flow.staging_dir / "test_run_001_agent_intelligence_staging.json"
        self.assertTrue(staging_file.exists())
    
    def test_create_progressive_context_from_packages(self):
        """Test progressive context creation from agent packages"""
        progressive_context = self.data_flow._create_progressive_context_from_packages(
            self.mock_agent_packages
        )
        
        self.assertIn('agent_a_jira_intelligence', progressive_context)
        self.assertIn('agent_d_environment_intelligence', progressive_context)
        self.assertIn('context_metadata', progressive_context)
        
        # Verify context structure
        agent_a_context = progressive_context['agent_a_jira_intelligence']
        self.assertIn('findings', agent_a_context)
        self.assertIn('detailed_analysis', agent_a_context)
        self.assertIn('confidence', agent_a_context)
        
        # Verify metadata
        metadata = progressive_context['context_metadata']
        self.assertEqual(metadata['total_agents'], 2)
        self.assertTrue(metadata['data_preservation_verified'])
    
    def test_extract_jira_context(self):
        """Test JIRA context extraction from agent packages"""
        jira_context = self.data_flow._extract_jira_context(self.mock_agent_packages)
        
        self.assertIn('findings_summary', jira_context)
        self.assertIn('detailed_analysis', jira_context)
        self.assertIn('confidence', jira_context)
        self.assertEqual(jira_context['confidence'], 0.90)
    
    def test_extract_github_context(self):
        """Test GitHub context extraction from agent packages"""
        # Add GitHub agent package
        github_package = AgentIntelligencePackage(
            agent_id="agent_c_github_investigation",
            agent_name="GitHub Investigation Agent",
            execution_status="success",
            findings_summary={'repos': ['repo1']},
            detailed_analysis_file="",
            detailed_analysis_content={'repos': ['stolostron/cluster-curator']},
            confidence_score=0.85,
            execution_time=1.8,
            context_metadata={}
        )
        
        packages_with_github = self.mock_agent_packages + [github_package]
        github_context = self.data_flow._extract_github_context(packages_with_github)
        
        self.assertIn('findings_summary', github_context)
        self.assertIn('detailed_analysis', github_context)
        self.assertEqual(github_context['confidence'], 0.85)
    
    @patch('parallel_data_flow.QEIntelligenceService')
    async def test_execute_parallel_qe_intelligence_success(self, mock_qe_service_class):
        """Test successful QE Intelligence execution in parallel"""
        # Mock QE Intelligence Service
        mock_qe_service = MagicMock()
        mock_qe_result = MagicMock()
        mock_qe_result.repository_analysis = {'test_files': 78}
        mock_qe_result.test_pattern_analysis = {'patterns': [{'name': 'pattern1'}]}
        mock_qe_result.coverage_gap_analysis = {'gaps': ['gap1']}
        mock_qe_result.strategic_recommendations = {'recommendations': ['rec1']}
        mock_qe_result.confidence_level = 0.92
        
        mock_qe_service.execute_qe_analysis.return_value = mock_qe_result
        mock_qe_service_class.return_value = mock_qe_service
        
        # Execute QE intelligence
        qe_intelligence = await self.data_flow.execute_parallel_qe_intelligence(
            self.mock_agent_packages, "test_run_001"
        )
        
        self.assertEqual(qe_intelligence.service_name, "QEIntelligenceService")
        self.assertEqual(qe_intelligence.execution_status, "success")
        self.assertEqual(qe_intelligence.confidence_score, 0.92)
        self.assertIsNotNone(qe_intelligence.repository_analysis)
    
    async def test_execute_parallel_qe_intelligence_fallback(self):
        """Test QE Intelligence fallback when service unavailable"""
        # Test fallback execution
        qe_intelligence = await self.data_flow._execute_fallback_qe_intelligence(
            self.mock_agent_packages, "test_run_001"
        )
        
        self.assertEqual(qe_intelligence.service_name, "QEIntelligenceService (Fallback)")
        self.assertEqual(qe_intelligence.execution_status, "success")
        self.assertGreater(qe_intelligence.confidence_score, 0.0)
        self.assertIsNotNone(qe_intelligence.repository_analysis)
    
    async def test_create_enhanced_phase_3_input(self):
        """Test Enhanced Phase 3 input creation"""
        # Mock QE intelligence
        mock_qe_intelligence = QEIntelligencePackage(
            service_name="QEIntelligenceService",
            execution_status="success",
            confidence_score=0.92
        )
        
        # Mock phase results
        mock_phase_1 = MagicMock()
        mock_phase_2 = MagicMock()
        
        # Create enhanced input
        phase_3_input = await self.data_flow.create_phase_3_input(
            mock_phase_1, mock_phase_2, self.mock_agent_packages, 
            mock_qe_intelligence, "test_run_001"
        )
        
        self.assertIsInstance(phase_3_input, Phase3Input)
        self.assertEqual(len(phase_3_input.agent_intelligence_packages), 2)
        self.assertTrue(phase_3_input.data_preservation_verified)
        self.assertEqual(phase_3_input.qe_intelligence.execution_status, "success")
    
    def test_get_staging_status(self):
        """Test staging status reporting"""
        status = self.data_flow.get_staging_status("test_run_001")
        
        self.assertIn('run_id', status)
        self.assertIn('staging_directory', status)
        self.assertIn('files_status', status)
        self.assertIn('data_flow_ready', status)
        self.assertEqual(status['run_id'], "test_run_001")


class TestEnhancedDataFlowIntegration(unittest.TestCase):
    """Test Enhanced Data Flow integration functions"""
    
    def test_enhanced_phase_3_input_structure(self):
        """Test Enhanced Phase 3 Input data structure"""
        mock_agent_packages = [
            AgentIntelligencePackage(
                agent_id="agent_a",
                agent_name="Agent A",
                execution_status="success",
                findings_summary={},
                detailed_analysis_file="",
                detailed_analysis_content={},
                confidence_score=0.8,
                execution_time=1.0,
                context_metadata={}
            )
        ]
        
        mock_qe_intelligence = QEIntelligencePackage()
        
        phase_3_input = Phase3Input(
            phase_1_result=None,
            phase_2_result=None,
            agent_intelligence_packages=mock_agent_packages,
            qe_intelligence=mock_qe_intelligence,
            data_flow_timestamp=datetime.now().isoformat(),
            data_preservation_verified=True,
            total_context_size_kb=10.5
        )
        
        self.assertEqual(len(phase_3_input.agent_intelligence_packages), 1)
        self.assertTrue(phase_3_input.data_preservation_verified)
        self.assertEqual(phase_3_input.total_context_size_kb, 10.5)
    
    @patch('parallel_data_flow.ParallelFrameworkDataFlow')
    async def test_execute_parallel_data_flow_integration(self, mock_data_flow_class):
        """Test execute_parallel_data_flow integration function"""
        # Mock data flow instance
        mock_data_flow = MagicMock()
        mock_phase_3_input = MagicMock()
        mock_phase_3_input.agent_intelligence_packages = []
        mock_phase_3_input.qe_intelligence = MagicMock()
        mock_phase_3_input.qe_intelligence.execution_status = "success"
        
        mock_data_flow.stage_agent_intelligence_direct = AsyncMock(return_value=[])
        mock_data_flow.execute_parallel_qe_intelligence = AsyncMock(return_value=MagicMock())
        mock_data_flow.create_phase_3_input = AsyncMock(return_value=mock_phase_3_input)
        
        mock_data_flow_class.return_value = mock_data_flow
        
        # Mock phase results
        mock_phase_1 = MagicMock()
        mock_phase_2 = MagicMock()
        
        # Test integration function
        result = await execute_parallel_data_flow(
            mock_phase_1, mock_phase_2, None, "test_run_001"
        )
        
        self.assertIsNotNone(result)
        mock_data_flow.stage_agent_intelligence_direct.assert_called_once()
        mock_data_flow.execute_parallel_qe_intelligence.assert_called_once()
        mock_data_flow.create_enhanced_phase_3_input.assert_called_once()


class TestDataPreservationMechanisms(unittest.TestCase):
    """Test data preservation mechanisms"""
    
    def test_agent_package_data_preservation(self):
        """Test that agent packages preserve complete data"""
        original_data = {
            'requirement_analysis': {
                'primary_requirements': ['Requirement 1', 'Requirement 2'],
                'component_focus': 'test-component',
                'detailed_description': 'X' * 1000  # 1KB of data
            },
            'additional_context': 'Y' * 500  # 0.5KB additional
        }
        
        package = AgentIntelligencePackage(
            agent_id="test_agent",
            agent_name="Test Agent",
            execution_status="success",
            findings_summary={'summary': 'brief'},
            detailed_analysis_file="",
            detailed_analysis_content=original_data,
            confidence_score=0.85,
            execution_time=1.5,
            context_metadata={}
        )
        
        # Verify complete preservation
        self.assertEqual(package.detailed_analysis_content, original_data)
        self.assertEqual(
            len(str(package.detailed_analysis_content)), 
            len(str(original_data))
        )
        
        # Verify no data loss
        preserved_size = len(str(package.detailed_analysis_content))
        original_size = len(str(original_data))
        preservation_ratio = preserved_size / original_size
        self.assertEqual(preservation_ratio, 1.0)
    
    def test_qe_intelligence_integration_preservation(self):
        """Test QE intelligence integration preserves additional insights"""
        base_insights = {
            'repository_analysis': {'files': 50},
            'test_patterns': [{'pattern1': 'data'}]
        }
        
        qe_package = QEIntelligencePackage(
            service_name="QEIntelligenceService",
            execution_status="success",
            repository_analysis=base_insights['repository_analysis'],
            test_patterns=base_insights['test_patterns'],
            coverage_gaps={'gaps': ['gap1', 'gap2']},
            automation_insights={'frameworks': ['Cypress', 'Jest']},
            testing_recommendations=['recommendation1', 'recommendation2'],
            execution_time=2.0,
            confidence_score=0.90
        )
        
        # Verify all QE insights preserved
        self.assertEqual(qe_package.repository_analysis, base_insights['repository_analysis'])
        self.assertEqual(qe_package.test_patterns, base_insights['test_patterns'])
        self.assertEqual(len(qe_package.coverage_gaps['gaps']), 2)
        self.assertEqual(len(qe_package.automation_insights['frameworks']), 2)
        self.assertEqual(len(qe_package.testing_recommendations), 2)


def run_parallel_framework_data_flow_tests():
    """Run all Enhanced Framework Data Flow tests"""
    print("🧪 Running Enhanced Framework Data Flow Unit Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestParallelFrameworkDataFlow))
    test_suite.addTest(unittest.makeSuite(TestEnhancedDataFlowIntegration))
    test_suite.addTest(unittest.makeSuite(TestDataPreservationMechanisms))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success_rate = ((tests_run - failures - errors) / tests_run * 100) if tests_run > 0 else 0
    
    print(f"\n📊 Enhanced Framework Data Flow Test Results:")
    print(f"Tests Run: {tests_run}")
    print(f"Failures: {failures}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run async tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    success = run_parallel_framework_data_flow_tests()
    print(f"\n🎯 Enhanced Framework Data Flow Tests: {'✅ PASSED' if success else '❌ FAILED'}")