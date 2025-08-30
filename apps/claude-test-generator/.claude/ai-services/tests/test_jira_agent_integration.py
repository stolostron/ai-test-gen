#!/usr/bin/env python3
"""
Integration tests for JIRA Intelligence Agent with Information Sufficiency
Tests the complete workflow including sufficiency checking and error handling
"""

import unittest
import asyncio
import tempfile
import shutil
import os
import sys
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jira_intelligence_agent import JIRAIntelligenceAgent, PRDiscoveryResult
from information_sufficiency_analyzer import InformationSufficiencyAnalyzer, SufficiencyScore
from framework_stop_handler import FrameworkStopHandler, InsufficientInformationError


class MockJiraApiClient:
    """Mock JIRA API client for testing"""
    
    def __init__(self):
        self.test_data = {
            'ACM-GOOD': Mock(
                jira_id='ACM-GOOD',
                title='Feature with PR references',
                description='Implement new feature. See PR #1234 and PR #5678',
                status='In Progress',
                priority='High',
                component='Cluster Lifecycle',
                fix_version='2.12',
                assignee='test_user',
                labels=['feature', 'tested']
            ),
            'ACM-NOPR': Mock(
                jira_id='ACM-NOPR',
                title='Feature without PR',
                description='Implement something but no PR references',
                status='New',
                priority='Medium',
                component='Console',
                fix_version='2.13',
                assignee='another_user',
                labels=['feature']
            ),
            'ACM-MINIMAL': Mock(
                jira_id='ACM-MINIMAL',
                title='Minimal information',
                description='Do something',
                status='New',
                priority='Low',
                component='Unknown',
                fix_version='',
                assignee='',
                labels=[]
            )
        }
    
    def get_ticket_information(self, jira_id):
        """Mock get ticket information"""
        if jira_id in self.test_data:
            return self.test_data[jira_id]
        raise Exception(f"Ticket {jira_id} not found")


class MockCommunicationHub:
    """Mock communication hub for testing"""
    
    def __init__(self):
        self.messages = []
        self.status = 'idle'
    
    def send_message(self, message):
        self.messages.append(message)
    
    def update_status(self, status):
        self.status = status


class MockAgentCommunicationInterface:
    """Mock agent communication interface"""
    
    def __init__(self, agent_id, hub):
        self.agent_id = agent_id
        self.hub = hub
        self.messages_sent = []
        self.status = 'idle'
    
    def update_status(self, status):
        self.status = status
        self.hub.update_status(status)
    
    async def send_discovery(self, discovery_type, data):
        self.messages_sent.append({
            'type': discovery_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })


class TestJIRAAgentIntegration(unittest.TestCase):
    """Integration tests for JIRA Intelligence Agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.mock_hub = MockCommunicationHub()
        
        # Patch the imports
        self.patcher_comm = patch('jira_intelligence_agent.AgentCommunicationInterface', MockAgentCommunicationInterface)
        self.patcher_jira = patch('jira_intelligence_agent.JiraApiClient', MockJiraApiClient)
        
        self.patcher_comm.start()
        self.patcher_jira.start()
        
        # Create agent
        self.agent = JIRAIntelligenceAgent(self.mock_hub, self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.patcher_comm.stop()
        self.patcher_jira.stop()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_agent_initialization(self):
        """Test agent initializes correctly with sufficiency components"""
        self.assertIsNotNone(self.agent.sufficiency_analyzer)
        self.assertIsInstance(self.agent.sufficiency_analyzer, InformationSufficiencyAnalyzer)
        
        self.assertIsNotNone(self.agent.stop_handler)
        self.assertIsInstance(self.agent.stop_handler, FrameworkStopHandler)
        
        self.assertTrue(self.agent.config['enable_sufficiency_check'])
        self.assertEqual(self.agent.config['minimum_score'], 0.75)
        self.assertEqual(self.agent.config['fallback_score'], 0.60)
    
    async def test_successful_analysis_with_sufficient_information(self):
        """Test successful analysis when information is sufficient"""
        context = {'jira_id': 'ACM-GOOD'}
        
        result = await self.agent.execute_enhanced_jira_analysis(context)
        
        self.assertEqual(result['findings']['jira_info']['jira_id'], 'ACM-GOOD')
        self.assertIn('sufficiency_score', result['findings'])
        self.assertGreaterEqual(result['findings']['sufficiency_score'], 0.60)
        self.assertEqual(result['findings']['sufficiency_status'], 'sufficient')
        self.assertEqual(self.agent.comm.status, 'completed')
    
    async def test_analysis_with_insufficient_information(self):
        """Test analysis fails gracefully when information is insufficient"""
        context = {'jira_id': 'ACM-MINIMAL'}
        
        # Temporarily set allow_force to False to ensure it stops
        self.agent.config['allow_force'] = False
        
        with self.assertRaises(InsufficientInformationError) as cm:
            await self.agent.execute_enhanced_jira_analysis(context)
        
        error = cm.exception
        self.assertEqual(error.report.jira_id, 'ACM-MINIMAL')
        self.assertLess(error.report.score, 0.60)
        self.assertEqual(self.agent.comm.status, 'failed')
        
        # Verify stop report was created
        reports_dir = os.path.join(self.test_dir, "insufficient_info_reports")
        self.assertTrue(os.path.exists(reports_dir))
        files = os.listdir(reports_dir)
        self.assertGreater(len(files), 0)
        self.assertTrue(any('ACM-MINIMAL' in f for f in files))
    
    async def test_analysis_with_marginal_information(self):
        """Test analysis proceeds with warnings for marginal information"""
        context = {'jira_id': 'ACM-NOPR'}
        
        result = await self.agent.execute_enhanced_jira_analysis(context)
        
        self.assertIn('sufficiency_score', result['findings'])
        score = result['findings']['sufficiency_score']
        
        # Should be marginal (between 0.60 and 0.75)
        self.assertGreaterEqual(score, 0.60)
        self.assertLess(score, 0.75)
        self.assertEqual(result['findings']['sufficiency_status'], 'marginal')
    
    async def test_force_proceed_option(self):
        """Test force proceed bypasses sufficiency check"""
        context = {'jira_id': 'ACM-MINIMAL'}
        
        # Enable force proceed
        self.agent.config['allow_force'] = True
        
        result = await self.agent.execute_enhanced_jira_analysis(context)
        
        # Should proceed despite low score
        self.assertIn('sufficiency_score', result['findings'])
        self.assertLess(result['findings']['sufficiency_score'], 0.60)
        self.assertEqual(self.agent.comm.status, 'completed')
    
    async def test_disable_sufficiency_check(self):
        """Test disabling sufficiency check"""
        context = {'jira_id': 'ACM-MINIMAL'}
        
        # Disable sufficiency check
        self.agent.config['enable_sufficiency_check'] = False
        
        result = await self.agent.execute_enhanced_jira_analysis(context)
        
        # Should proceed without sufficiency score
        self.assertNotIn('sufficiency_score', result['findings'])
        self.assertNotIn('sufficiency_status', result['findings'])
        self.assertEqual(self.agent.comm.status, 'completed')
    
    def test_prepare_data_for_sufficiency_check(self):
        """Test data preparation for sufficiency checking"""
        analysis_data = {
            'jira_info': {'jira_id': 'ACM-TEST', 'fix_version': '2.12'},
            'pr_discoveries': [
                PRDiscoveryResult(
                    pr_number='123',
                    pr_title='Test PR',
                    pr_url='https://github.com/test/pr/123',
                    files_changed=['file1.go'],
                    deployment_components=['Component1'],
                    yaml_files=[],
                    config_changes=[],
                    api_changes=[],
                    operator_changes=[],
                    confidence_score=0.9
                )
            ],
            'requirement_analysis': {
                'acceptance_criteria': 'Test criteria',
                'technical_scope': 'Test scope'
            },
            'component_analysis': {
                'affected_components': ['Comp1', 'Comp2'],
                'integration_points': ['API1']
            },
            'business_context': {
                'customer_impact': 'High impact'
            }
        }
        
        prepared_data = self.agent._prepare_data_for_sufficiency_check(analysis_data)
        
        self.assertEqual(prepared_data['jira_info']['jira_id'], 'ACM-TEST')
        self.assertEqual(len(prepared_data['pr_references']), 1)
        self.assertEqual(prepared_data['pr_references'][0], '123')
        self.assertEqual(len(prepared_data['github_prs']), 1)
        self.assertEqual(prepared_data['acceptance_criteria'], 'Test criteria')
        self.assertEqual(prepared_data['technical_design'], 'Test scope')
        self.assertEqual(len(prepared_data['affected_components']), 2)
        self.assertEqual(prepared_data['target_version'], '2.12')
        self.assertEqual(prepared_data['business_value'], 'High impact')
    
    async def test_web_search_enhancement(self):
        """Test web search enhancement for marginal information"""
        collected_data = {
            'jira_info': {'jira_id': 'ACM-TEST', 'component': 'TestComponent'}
        }
        
        sufficiency_result = SufficiencyScore(
            overall_score=0.65,
            component_scores={},
            missing_critical=['GitHub PR references', 'Technical design', 'Acceptance criteria'],
            missing_optional=[],
            recommendations=[],
            can_proceed=True,
            needs_enhancement=True
        )
        
        enhanced_data = await self.agent._enhance_with_web_search(collected_data, sufficiency_result)
        
        self.assertTrue(enhanced_data['web_enhancement_attempted'])
        self.assertIn('enhancement_queries', enhanced_data)
    
    def test_extract_requirements(self):
        """Test requirement extraction from description"""
        description = """
        Feature Requirements:
        - User should be able to create clusters
        - System must validate permissions
        - Integration with RBAC required
        
        Acceptance Criteria:
        - Cluster creation successful
        - Permission denied for unauthorized users
        """
        
        requirements = self.agent._extract_requirements(description)
        
        self.assertGreater(len(requirements), 0)
        self.assertTrue(any('create clusters' in req for req in requirements))
    
    def test_extract_acceptance_criteria(self):
        """Test acceptance criteria extraction"""
        description = """
        Acceptance Criteria:
        - Feature works as expected
        - No errors in console
        - User can perform action
        """
        
        criteria = self.agent._extract_acceptance_criteria(description)
        
        self.assertGreater(len(criteria), 0)
        self.assertTrue(any('Feature works' in c for c in criteria))
    
    async def test_error_handling_in_analysis(self):
        """Test error handling during analysis"""
        context = {'jira_id': 'ACM-NOTEXIST'}
        
        with self.assertRaises(Exception):
            await self.agent.execute_enhanced_jira_analysis(context)
        
        self.assertEqual(self.agent.comm.status, 'failed')
    
    async def test_pr_discovery_and_publishing(self):
        """Test PR discovery and real-time publishing"""
        jira_id = 'ACM-GOOD'
        basic_analysis = {
            'jira_info': {
                'description': 'Feature with PR #1234 and PR #5678'
            }
        }
        
        pr_discoveries = await self.agent._discover_and_publish_pr_information(jira_id, basic_analysis)
        
        self.assertEqual(len(pr_discoveries), 2)
        self.assertEqual(pr_discoveries[0].pr_number, '1234')
        self.assertEqual(pr_discoveries[1].pr_number, '5678')
        
        # Verify messages were sent
        self.assertGreater(len(self.agent.comm.messages_sent), 0)
    
    def test_analyze_technical_scope(self):
        """Test technical scope analysis"""
        ticket_data = Mock(
            description='Technical implementation using controller pattern',
            component='Cluster Lifecycle'
        )
        
        scope = self.agent._analyze_technical_scope(ticket_data)
        
        self.assertIsInstance(scope, str)
        self.assertGreater(len(scope), 0)
    
    def test_classify_feature_type(self):
        """Test feature type classification"""
        ticket_data = Mock(
            title='Add cluster import feature',
            component='Cluster Lifecycle',
            labels=['feature', 'cluster-management']
        )
        
        feature_type = self.agent._classify_feature_type(ticket_data)
        
        self.assertIsInstance(feature_type, str)
        self.assertIn('cluster', feature_type.lower())


class TestPerformanceImpact(unittest.TestCase):
    """Test performance impact of sufficiency checking"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = InformationSufficiencyAnalyzer()
        
    def test_analyzer_performance(self):
        """Test analyzer performance with large data sets"""
        import time
        
        # Create large test data
        large_data = {
            'jira_info': {
                'description': 'Test ' * 1000,  # Large description
                'jira_id': 'ACM-PERF'
            },
            'pr_references': [f'#{i}' for i in range(100)],  # Many PRs
            'affected_components': [f'Component{i}' for i in range(50)],
            'test_scenarios': [f'Scenario {i}' for i in range(100)],
            'acceptance_criteria': 'Criteria ' * 100
        }
        
        start_time = time.time()
        result = self.analyzer.analyze_sufficiency(large_data)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Should complete within reasonable time (< 1 second)
        self.assertLess(execution_time, 1.0)
        self.assertIsInstance(result, SufficiencyScore)
    
    def test_stop_handler_performance(self):
        """Test stop handler performance"""
        import time
        
        handler = FrameworkStopHandler()
        
        # Large missing info lists
        missing_info = {
            'critical': [f'Missing item {i}' for i in range(50)],
            'optional': [f'Optional item {i}' for i in range(50)]
        }
        
        start_time = time.time()
        report = handler.trigger_stop(
            jira_id='ACM-PERF',
            collected_data={'jira_info': {'jira_id': 'ACM-PERF'}},
            score=0.30,
            missing_info=missing_info
        )
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Should complete within reasonable time (< 1 second)
        self.assertLess(execution_time, 1.0)
        self.assertIsInstance(report.to_markdown(), str)


def async_test(coro):
    """Decorator to run async tests"""
    def wrapper(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(coro(self))
    return wrapper


# Apply decorator to async test methods
for attr_name in dir(TestJIRAAgentIntegration):
    attr = getattr(TestJIRAAgentIntegration, attr_name)
    if callable(attr) and attr_name.startswith('test_') and asyncio.iscoroutinefunction(attr):
        setattr(TestJIRAAgentIntegration, attr_name, async_test(attr))


if __name__ == '__main__':
    unittest.main(verbosity=2)
