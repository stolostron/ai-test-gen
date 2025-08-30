#!/usr/bin/env python3
"""
Comprehensive unit tests for FrameworkStopHandler
Tests report generation, file handling, and error scenarios
"""

import unittest
import tempfile
import shutil
import os
import json
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework_stop_handler import FrameworkStopHandler, StopReport, InsufficientInformationError


class TestStopReport(unittest.TestCase):
    """Test cases for StopReport dataclass"""
    
    def test_stop_report_creation(self):
        """Test creating a StopReport instance"""
        report = StopReport(
            jira_id="ACM-12345",
            score=0.45,
            status="INSUFFICIENT_INFORMATION",
            timestamp=datetime.now().isoformat(),
            missing_critical=["PR references", "Technical design"],
            missing_optional=["Version info", "Environment details"],
            recommendations=["Add PR links", "Document design"],
            jira_update_suggestions=["## Add PRs", "- PR #123"],
            collected_data_summary={
                'jira_ticket_found': True,
                'pr_references_found': False,
                'acceptance_criteria_found': True
            },
            can_force_proceed=False
        )
        
        self.assertEqual(report.jira_id, "ACM-12345")
        self.assertEqual(report.score, 0.45)
        self.assertEqual(len(report.missing_critical), 2)
        self.assertEqual(len(report.missing_optional), 2)
        self.assertFalse(report.can_force_proceed)
    
    def test_stop_report_to_markdown(self):
        """Test markdown generation from StopReport"""
        report = StopReport(
            jira_id="ACM-99999",
            score=0.35,
            status="INSUFFICIENT_INFORMATION",
            timestamp="2025-01-01T10:00:00",
            missing_critical=["GitHub PR references", "Acceptance criteria"],
            missing_optional=["Target version"],
            recommendations=["Add PR links to JIRA", "Define acceptance criteria"],
            jira_update_suggestions=[
                "## Implementation Details",
                "**GitHub PRs**:",
                "- PR #1234: Feature implementation"
            ],
            collected_data_summary={
                'jira_ticket_found': True,
                'pr_references_found': False,
                'acceptance_criteria_found': False,
                'technical_design_found': True
            },
            can_force_proceed=True
        )
        
        markdown = report.to_markdown()
        
        # Verify key elements are present
        self.assertIn("# 🚨 FRAMEWORK STOP: Insufficient Information", markdown)
        self.assertIn("ACM-99999", markdown)
        self.assertIn("0.35 / 1.00", markdown)
        self.assertIn("GitHub PR references", markdown)
        self.assertIn("Acceptance criteria", markdown)
        self.assertIn("Add PR links to JIRA", markdown)
        self.assertIn("PR #1234: Feature implementation", markdown)
        self.assertIn("✅ Jira Ticket Found", markdown)
        self.assertIn("❌ Pr References Found", markdown)
        self.assertIn("--force", markdown)  # Force option mentioned
    
    def test_stop_report_markdown_without_force(self):
        """Test markdown when force proceed is not allowed"""
        report = StopReport(
            jira_id="ACM-11111",
            score=0.25,
            status="INSUFFICIENT_INFORMATION",
            timestamp="2025-01-01T10:00:00",
            missing_critical=["Everything"],
            missing_optional=[],
            recommendations=["Start over"],
            jira_update_suggestions=["Add everything"],
            collected_data_summary={'jira_ticket_found': True},
            can_force_proceed=False
        )
        
        markdown = report.to_markdown()
        self.assertNotIn("--force", markdown)
        self.assertNotIn("Alternative Options", markdown)


class TestFrameworkStopHandler(unittest.TestCase):
    """Test cases for FrameworkStopHandler"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.handler = FrameworkStopHandler(run_dir=self.test_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test handler initialization"""
        self.assertEqual(self.handler.run_dir, self.test_dir)
        reports_dir = os.path.join(self.test_dir, "insufficient_info_reports")
        self.assertTrue(os.path.exists(reports_dir))
        
        # Test initialization without run_dir
        handler_no_dir = FrameworkStopHandler()
        self.assertEqual(handler_no_dir.run_dir, os.getcwd())
    
    def test_trigger_stop_basic(self):
        """Test basic stop trigger functionality"""
        collected_data = {
            'jira_info': {
                'jira_id': 'ACM-TEST1',
                'description': 'Test ticket'
            },
            'pr_references': [],
            'acceptance_criteria': ''
        }
        
        missing_info = {
            'critical': ['PR references', 'Acceptance criteria'],
            'optional': ['Version info']
        }
        
        report = self.handler.trigger_stop(
            jira_id='ACM-TEST1',
            collected_data=collected_data,
            score=0.30,
            missing_info=missing_info
        )
        
        self.assertIsInstance(report, StopReport)
        self.assertEqual(report.jira_id, 'ACM-TEST1')
        self.assertEqual(report.score, 0.30)
        self.assertEqual(report.status, 'INSUFFICIENT_INFORMATION')
        self.assertEqual(len(report.missing_critical), 2)
        self.assertEqual(len(report.missing_optional), 1)
        self.assertFalse(report.can_force_proceed)  # Score < 0.60
    
    def test_trigger_stop_with_force_allowed(self):
        """Test stop trigger when force proceed is allowed"""
        report = self.handler.trigger_stop(
            jira_id='ACM-TEST2',
            collected_data={'jira_info': {'jira_id': 'ACM-TEST2'}},
            score=0.65,  # Above fallback threshold
            missing_info={'critical': ['Some info'], 'optional': []}
        )
        
        self.assertTrue(report.can_force_proceed)
    
    def test_analyze_collected_data(self):
        """Test analysis of collected data"""
        complete_data = {
            'jira_info': {'jira_id': 'ACM-123'},
            'pr_references': ['#123'],
            'github_prs': [{'number': '123'}],
            'subtasks': ['SUB-1', 'SUB-2'],
            'linked_issues': ['LINK-1'],
            'comments': ['Comment 1'],
            'acceptance_criteria': 'Criteria',
            'technical_design': 'Design',
            'affected_components': ['Comp1'],
            'environment_info': {'platform': 'OpenShift'},
            'target_version': '2.12'
        }
        
        summary = self.handler._analyze_collected_data(complete_data)
        
        self.assertTrue(summary['jira_ticket_found'])
        self.assertTrue(summary['pr_references_found'])
        self.assertTrue(summary['subtasks_analyzed'])
        self.assertTrue(summary['linked_issues_analyzed'])
        self.assertTrue(summary['comments_extracted'])
        self.assertTrue(summary['acceptance_criteria_found'])
        self.assertTrue(summary['technical_design_found'])
        self.assertTrue(summary['components_identified'])
        self.assertTrue(summary['environment_info_found'])
        self.assertTrue(summary['version_info_found'])
    
    def test_generate_jira_suggestions(self):
        """Test JIRA update suggestions generation"""
        missing_critical = [
            'GitHub PR references - No implementation details found',
            'Acceptance criteria or success conditions',
            'Technical design or architecture details'
        ]
        missing_optional = ['Test scenarios']
        
        suggestions = self.handler._generate_jira_suggestions(
            missing_critical, missing_optional, {}
        )
        
        # Check that suggestions contain expected sections
        suggestions_text = '\n'.join(suggestions)
        self.assertIn('## Implementation Details', suggestions_text)
        self.assertIn('GitHub PRs', suggestions_text)
        self.assertIn('## Acceptance Criteria', suggestions_text)
        self.assertIn('## Technical Design', suggestions_text)
        self.assertIn('## Test Scenarios', suggestions_text)
    
    def test_generate_detailed_recommendations(self):
        """Test detailed recommendations generation"""
        missing_info = {
            'critical': ['GitHub PR references'],
            'optional': []
        }
        collected_data = {
            'jira_info': {'jira_id': 'ACM-333'}
        }
        
        # Test with very low score
        recommendations = self.handler._generate_detailed_recommendations(
            missing_info, collected_data, score=0.45
        )
        
        self.assertGreater(len(recommendations), 0)
        critical_rec = any('Critical' in rec for rec in recommendations)
        self.assertTrue(critical_rec)
        
        # Test PR-specific recommendations
        pr_rec = any('Search for PRs' in rec for rec in recommendations)
        self.assertTrue(pr_rec)
    
    def test_save_report(self):
        """Test report saving functionality"""
        report = StopReport(
            jira_id="ACM-SAVE1",
            score=0.40,
            status="INSUFFICIENT_INFORMATION",
            timestamp="2025-01-01T10:00:00",
            missing_critical=["Test critical"],
            missing_optional=["Test optional"],
            recommendations=["Test recommendation"],
            jira_update_suggestions=["Test suggestion"],
            collected_data_summary={'jira_ticket_found': True},
            can_force_proceed=False
        )
        
        self.handler._save_report(report)
        
        # Check that files were created
        reports_dir = os.path.join(self.test_dir, "insufficient_info_reports")
        
        # Check JSON file
        json_files = [f for f in os.listdir(reports_dir) if f.endswith('.json') and 'ACM-SAVE1' in f]
        self.assertEqual(len(json_files), 1)
        
        # Check Markdown file
        md_files = [f for f in os.listdir(reports_dir) if f.endswith('.md') and 'ACM-SAVE1' in f and 'latest' not in f]
        self.assertEqual(len(md_files), 1)
        
        # Check latest symlink
        latest_link = os.path.join(reports_dir, "ACM-SAVE1_latest.md")
        self.assertTrue(os.path.exists(latest_link))
        self.assertTrue(os.path.islink(latest_link))
        
        # Verify JSON content
        json_path = os.path.join(reports_dir, json_files[0])
        with open(json_path, 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data['jira_id'], 'ACM-SAVE1')
        self.assertEqual(saved_data['score'], 0.40)
    
    def test_get_latest_report(self):
        """Test retrieving latest report"""
        # First, save a report
        report = StopReport(
            jira_id="ACM-GET1",
            score=0.35,
            status="INSUFFICIENT_INFORMATION",
            timestamp=datetime.now().isoformat(),
            missing_critical=["Test"],
            missing_optional=[],
            recommendations=["Test rec"],
            jira_update_suggestions=["Test sug"],
            collected_data_summary={'jira_ticket_found': True},
            can_force_proceed=False
        )
        
        self.handler._save_report(report)
        
        # Now retrieve it
        retrieved = self.handler.get_latest_report("ACM-GET1")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.jira_id, "ACM-GET1")
        self.assertEqual(retrieved.score, 0.35)
        
        # Test retrieving non-existent report
        non_existent = self.handler.get_latest_report("ACM-NOTEXIST")
        self.assertIsNone(non_existent)
    
    def test_insufficient_information_error(self):
        """Test InsufficientInformationError exception"""
        report = StopReport(
            jira_id="ACM-ERROR1",
            score=0.25,
            status="INSUFFICIENT_INFORMATION",
            timestamp=datetime.now().isoformat(),
            missing_critical=["Everything"],
            missing_optional=[],
            recommendations=[],
            jira_update_suggestions=[],
            collected_data_summary={},
            can_force_proceed=False
        )
        
        error = InsufficientInformationError(report)
        
        self.assertIsInstance(error, Exception)
        self.assertEqual(error.report, report)
        self.assertIn("ACM-ERROR1", str(error))
        self.assertIn("0.25", str(error))
        self.assertIn("0.75", str(error))
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Test with empty missing info
        report = self.handler.trigger_stop(
            jira_id='ACM-EDGE1',
            collected_data={},
            score=0.10,
            missing_info={}
        )
        
        self.assertEqual(report.jira_id, 'ACM-EDGE1')
        self.assertEqual(len(report.missing_critical), 0)
        self.assertEqual(len(report.missing_optional), 0)
        
        # Test with None values
        report = self.handler.trigger_stop(
            jira_id='ACM-EDGE2',
            collected_data={'jira_info': None},
            score=0.20,
            missing_info={'critical': None, 'optional': None}
        )
        
        self.assertEqual(report.jira_id, 'ACM-EDGE2')
        self.assertIsNotNone(report.timestamp)
        
        # Test with special characters in JIRA ID
        report = self.handler.trigger_stop(
            jira_id='ACM-123/456',
            collected_data={},
            score=0.15,
            missing_info={'critical': [], 'optional': []}
        )
        
        self.assertEqual(report.jira_id, 'ACM-123/456')


class TestIntegration(unittest.TestCase):
    """Integration tests for stop handler with analyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.handler = FrameworkStopHandler(run_dir=self.test_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_full_workflow(self):
        """Test complete workflow from trigger to retrieval"""
        # Trigger stop
        missing_info = {
            'critical': ['PR references', 'Technical design'],
            'optional': ['Version info']
        }
        
        report = self.handler.trigger_stop(
            jira_id='ACM-FLOW1',
            collected_data={
                'jira_info': {'jira_id': 'ACM-FLOW1'},
                'pr_references': []
            },
            score=0.30,
            missing_info=missing_info
        )
        
        # Verify report
        self.assertEqual(report.jira_id, 'ACM-FLOW1')
        self.assertFalse(report.can_force_proceed)
        
        # Retrieve report
        retrieved = self.handler.get_latest_report('ACM-FLOW1')
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.score, report.score)
        
        # Verify markdown generation
        markdown = retrieved.to_markdown()
        self.assertIn('ACM-FLOW1', markdown)
        self.assertIn('PR references', markdown)
        
        # Verify files exist
        reports_dir = os.path.join(self.test_dir, "insufficient_info_reports")
        files = os.listdir(reports_dir)
        self.assertGreater(len(files), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
