#!/usr/bin/env python3
"""
Comprehensive unit tests for Framework Observability Agent - Framework Integration

Tests the FrameworkObservabilityIntegration functionality including:
- Real-time framework event handling
- Integration hooks and callbacks
- State updates and coordination
- Error handling and resilience
- Global convenience functions
"""

import unittest
import json
import tempfile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the observability directory to the path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../.claude/observability'))

from framework_integration import (
    FrameworkObservabilityIntegration,
    get_observability_integration,
    init_observability,
    observe_phase_transition,
    observe_agent_spawn,
    observe_agent_completion,
    observe_context_inheritance,
    observe_validation_checkpoint,
    observe_framework_completion,
    observe_error,
    process_observability_command,
    update_observability_metadata
)


class TestFrameworkObservabilityIntegration(unittest.TestCase):
    """Test suite for FrameworkObservabilityIntegration core functionality"""
    
    def setUp(self):
        """Set up test environment with temporary directories and mock data"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_run_dir = os.path.join(self.temp_dir, "runs", "ACM-22079", "ACM-22079-20250826-120000")
        os.makedirs(self.test_run_dir, exist_ok=True)
        
        # Reset global integration instance
        import framework_integration
        framework_integration._observability_integration = None
        
        # Sample configuration for testing
        self.sample_config = {
            "observability_agent": {
                "enabled": True,
                "service_id": "tg_framework_observability_agent",
                "integration_points": {
                    "progressive_context_monitoring": True,
                    "sub_agent_tracking": True,
                    "validation_engine_access": True,
                    "run_metadata_streaming": True,
                    "phase_transition_hooks": True,
                    "error_detection_alerts": True
                }
            }
        }
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        # Reset global integration instance
        import framework_integration
        framework_integration._observability_integration = None
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_initialization_enabled(self, mock_handler_class):
        """Test integration initialization when observability is enabled"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Verify initialization
        self.assertTrue(integration.is_enabled)
        self.assertEqual(len(integration.integration_hooks), 8)
        mock_handler_class.assert_called_once_with(self.test_run_dir)
        
        # Verify hook setup
        expected_hooks = [
            "framework_start", "phase_transition", "agent_spawn", "agent_completion",
            "context_inheritance", "validation_checkpoint", "framework_completion", "error_event"
        ]
        for hook in expected_hooks:
            self.assertIn(hook, integration.integration_hooks)
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_initialization_disabled(self, mock_handler_class):
        """Test integration initialization when observability is disabled"""
        disabled_config = {
            "observability_agent": {"enabled": False}
        }
        
        mock_handler = Mock()
        mock_handler.config = disabled_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Verify disabled state
        self.assertFalse(integration.is_enabled)
    
    @patch('framework_integration.ObservabilityCommandHandler')
    @patch('builtins.print')
    def test_on_framework_start(self, mock_print, mock_handler_class):
        """Test framework start event handling"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test framework start event
        integration.on_framework_start(
            jira_ticket="ACM-22079",
            feature="Digest-based upgrades",
            customer="Amadeus",
            priority="Critical"
        )
        
        # Verify handler update was called
        mock_handler.update_state.assert_called_once()
        
        # Verify the data structure passed to update_state
        call_args = mock_handler.update_state.call_args[0][0]
        self.assertIn("framework_state", call_args)
        self.assertIn("run_metadata", call_args)
        self.assertEqual(call_args["run_metadata"]["jira_ticket"], "ACM-22079")
        self.assertEqual(call_args["run_metadata"]["feature"], "Digest-based upgrades")
        self.assertEqual(call_args["run_metadata"]["customer"], "Amadeus")
        self.assertEqual(call_args["framework_state"]["current_phase"], "initializing")
        
        # Verify console output
        mock_print.assert_called()
        self.assertTrue(any("Observability Agent" in str(call) for call in mock_print.call_args_list))
    
    @patch('framework_integration.ObservabilityCommandHandler')
    @patch('builtins.print')
    def test_on_framework_start_disabled(self, mock_print, mock_handler_class):
        """Test framework start event handling when disabled"""
        disabled_config = {"observability_agent": {"enabled": False}}
        mock_handler = Mock()
        mock_handler.config = disabled_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test framework start when disabled
        integration.on_framework_start("ACM-22079", "Test feature")
        
        # Should not call handler update
        mock_handler.update_state.assert_not_called()
        # Should not print console messages
        mock_print.assert_not_called()
    
    @patch('framework_integration.ObservabilityCommandHandler')
    @patch('builtins.print')
    def test_on_phase_transition(self, mock_print, mock_handler_class):
        """Test phase transition event handling"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test phase transition
        integration.on_phase_transition(
            phase="phase_1",
            status="in_progress",
            agent_data={"agents": ["agent_a", "agent_d"]}
        )
        
        # Verify handler update
        mock_handler.update_state.assert_called_once()
        call_args = mock_handler.update_state.call_args[0][0]
        self.assertIn("framework_state", call_args)
        self.assertEqual(call_args["framework_state"]["current_phase"], "phase_1")
        self.assertIn("phase_data", call_args)
        
        # Verify console output for in_progress
        mock_print.assert_called()
        self.assertTrue(any("Started" in str(call) for call in mock_print.call_args_list))
        
        # Test completed status
        mock_print.reset_mock()
        integration.on_phase_transition("phase_1", "completed")
        self.assertTrue(any("Completed" in str(call) for call in mock_print.call_args_list))
    
    @patch('framework_integration.ObservabilityCommandHandler')
    @patch('builtins.print')
    def test_on_agent_spawn(self, mock_print, mock_handler_class):
        """Test agent spawn event handling"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test agent spawn
        inherited_context = {"jira_ticket": "ACM-22079", "feature": "Test feature"}
        integration.on_agent_spawn(
            agent_type="agent_a",
            inherited_context=inherited_context,
            additional_data="test"
        )
        
        # Verify handler update
        mock_handler.update_state.assert_called_once()
        call_args = mock_handler.update_state.call_args[0][0]
        self.assertIn("agent_coordination", call_args)
        self.assertEqual(call_args["agent_coordination"]["active_agents"], ["agent_a"])
        self.assertIn("last_spawn", call_args["agent_coordination"])
        self.assertEqual(call_args["agent_coordination"]["last_spawn"]["agent"], "agent_a")
        
        # Verify console output
        mock_print.assert_called()
        self.assertTrue(any("AGENT A" in str(call) and "Spawned" in str(call) for call in mock_print.call_args_list))
    
    @patch('framework_integration.ObservabilityCommandHandler')
    @patch('builtins.print')
    def test_on_agent_completion(self, mock_print, mock_handler_class):
        """Test agent completion event handling"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler.state = {"agent_coordination": {"active_agents": ["agent_a", "agent_d"]}}
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test agent completion
        results = {"analysis": "completed", "findings": ["finding1", "finding2"]}
        context_contribution = {"business_context": "critical customer requirement"}
        
        integration.on_agent_completion(
            agent_type="agent_a",
            results=results,
            context_contribution=context_contribution
        )
        
        # Verify handler update
        mock_handler.update_state.assert_called_once()
        call_args = mock_handler.update_state.call_args[0][0]
        self.assertIn("agent_coordination", call_args)
        self.assertEqual(call_args["agent_coordination"]["completed_agents"], ["agent_a"])
        self.assertIn("last_completion", call_args["agent_coordination"])
        
        # Verify active agents list updated
        expected_active = ["agent_d"]  # agent_a should be removed
        self.assertEqual(call_args["agent_coordination"]["active_agents"], expected_active)
        
        # Verify console output
        mock_print.assert_called()
        self.assertTrue(any("AGENT A" in str(call) and "Completed" in str(call) for call in mock_print.call_args_list))
    
    @patch('framework_integration.ObservabilityCommandHandler')
    @patch('builtins.print')
    def test_on_context_inheritance(self, mock_print, mock_handler_class):
        """Test context inheritance event handling"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test successful context inheritance
        context_data = {"business_requirements": "test", "environment_data": "test"}
        integration.on_context_inheritance(
            source_agent="agent_a",
            target_agent="agent_d",
            context_data=context_data,
            validation_status="passed"
        )
        
        # Verify handler update
        mock_handler.update_state.assert_called_once()
        call_args = mock_handler.update_state.call_args[0][0]
        self.assertIn("context_inheritance", call_args)
        self.assertIn("agent_coordination", call_args)
        self.assertEqual(call_args["context_inheritance"]["last_inheritance"]["source"], "agent_a")
        self.assertEqual(call_args["context_inheritance"]["last_inheritance"]["target"], "agent_d")
        self.assertEqual(call_args["context_inheritance"]["last_inheritance"]["validation_status"], "passed")
        
        # Verify console output for success
        mock_print.assert_called()
        self.assertTrue(any("Context Flow" in str(call) and "validated" in str(call) for call in mock_print.call_args_list))
        
        # Test failed validation
        mock_print.reset_mock()
        integration.on_context_inheritance("agent_a", "agent_d", context_data, "failed")
        self.assertTrue(any("Context Conflict" in str(call) for call in mock_print.call_args_list))
    
    @patch('framework_integration.ObservabilityCommandHandler')
    @patch('builtins.print')
    def test_on_validation_checkpoint(self, mock_print, mock_handler_class):
        """Test validation checkpoint event handling"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test passed validation
        details = {"confidence": 95.5, "issues": []}
        integration.on_validation_checkpoint(
            checkpoint_type="evidence_validation",
            status="passed",
            details=details
        )
        
        # Verify handler update
        mock_handler.update_state.assert_called_once()
        call_args = mock_handler.update_state.call_args[0][0]
        self.assertIn("validation_status", call_args)
        self.assertIn("last_validation", call_args)
        self.assertEqual(call_args["validation_status"]["evidence_validation"], "passed")
        self.assertEqual(call_args["last_validation"]["checkpoint"], "evidence_validation")
        self.assertEqual(call_args["last_validation"]["details"], details)
        
        # Verify console output for success
        mock_print.assert_called()
        self.assertTrue(any("Validation" in str(call) and "Evidence Validation" in str(call) and "passed" in str(call) for call in mock_print.call_args_list))
        
        # Test failed validation
        mock_print.reset_mock()
        integration.on_validation_checkpoint("cross_agent_validation", "failed")
        self.assertTrue(any("Validation" in str(call) and "failed" in str(call) for call in mock_print.call_args_list))
    
    @patch('framework_integration.ObservabilityCommandHandler')
    @patch('builtins.print')
    def test_on_framework_completion(self, mock_print, mock_handler_class):
        """Test framework completion event handling"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler.state = {"framework_state": {"start_time": "2025-08-26T12:00:00Z"}}
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test framework completion
        deliverables = ["ACM-22079-Test-Cases.md", "ACM-22079-Complete-Analysis.md"]
        quality_metrics = {"format_compliance": 100, "evidence_validation": 95.5}
        
        integration.on_framework_completion(
            run_directory=self.test_run_dir,
            deliverables=deliverables,
            quality_metrics=quality_metrics
        )
        
        # Verify handler update
        mock_handler.update_state.assert_called_once()
        call_args = mock_handler.update_state.call_args[0][0]
        self.assertIn("framework_state", call_args)
        self.assertIn("completion_summary", call_args)
        self.assertEqual(call_args["framework_state"]["current_phase"], "completed")
        self.assertEqual(call_args["framework_state"]["completion_percentage"], 100)
        self.assertEqual(call_args["completion_summary"]["deliverables"], deliverables)
        self.assertEqual(call_args["completion_summary"]["quality_metrics"], quality_metrics)
        
        # Verify console output
        mock_print.assert_called()
        self.assertTrue(any("Framework Complete" in str(call) for call in mock_print.call_args_list))
        self.assertTrue(any("2 files generated" in str(call) for call in mock_print.call_args_list))
    
    @patch('framework_integration.ObservabilityCommandHandler')
    @patch('builtins.print')
    def test_on_error_event(self, mock_print, mock_handler_class):
        """Test error event handling"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test error event
        integration.on_error_event(
            error_type="ValidationError",
            error_message="Context inheritance validation failed",
            phase="phase_2",
            agent="agent_b"
        )
        
        # Verify handler update
        mock_handler.update_state.assert_called_once()
        call_args = mock_handler.update_state.call_args[0][0]
        self.assertIn("error_events", call_args)
        self.assertIn("risk_alerts", call_args)
        
        error_event = call_args["error_events"][0]
        self.assertEqual(error_event["type"], "ValidationError")
        self.assertEqual(error_event["message"], "Context inheritance validation failed")
        self.assertEqual(error_event["phase"], "phase_2")
        self.assertEqual(error_event["agent"], "agent_b")
        
        risk_alert = call_args["risk_alerts"][0]
        self.assertEqual(risk_alert["level"], "error")
        
        # Verify console output
        mock_print.assert_called()
        self.assertTrue(any("Error Detected" in str(call) for call in mock_print.call_args_list))
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_process_user_command_enabled(self, mock_handler_class):
        """Test user command processing when enabled"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler.process_command.return_value = "Test response"
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        response = integration.process_user_command("/status")
        
        # Verify command was processed
        mock_handler.process_command.assert_called_once_with("/status")
        self.assertEqual(response, "Test response")
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_process_user_command_disabled(self, mock_handler_class):
        """Test user command processing when disabled"""
        disabled_config = {"observability_agent": {"enabled": False}}
        mock_handler = Mock()
        mock_handler.config = disabled_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        response = integration.process_user_command("/status")
        
        # Should return disabled message
        self.assertIn("disabled", response)
        mock_handler.process_command.assert_not_called()
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_get_current_status(self, mock_handler_class):
        """Test current status retrieval"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler.state = {
            "framework_state": {
                "current_phase": "phase_2",
                "completion_percentage": 50
            },
            "agent_coordination": {
                "active_agents": ["agent_b", "agent_c"]
            }
        }
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        status = integration.get_current_status()
        
        # Verify status structure
        self.assertEqual(status["status"], "enabled")
        self.assertEqual(status["current_phase"], "phase_2")
        self.assertEqual(status["completion_percentage"], 50)
        self.assertEqual(status["active_agents"], ["agent_b", "agent_c"])
        self.assertIn("last_update", status)
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_update_run_metadata(self, mock_handler_class):
        """Test run metadata updates"""
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        metadata_updates = {
            "target_version": "2.15.0",
            "test_results": {
                "total_test_cases": 5,
                "coverage_areas": ["UI", "CLI", "API"]
            }
        }
        
        integration.update_run_metadata(metadata_updates)
        
        # Verify handler update
        mock_handler.update_state.assert_called_once()
        call_args = mock_handler.update_state.call_args[0][0]
        self.assertIn("run_metadata", call_args)
        self.assertEqual(call_args["run_metadata"], metadata_updates)
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_calculate_total_time(self, mock_handler_class):
        """Test total execution time calculation"""
        # Mock start time 2 minutes ago
        start_time = (datetime.now(timezone.utc).timestamp() - 120)
        start_time_iso = datetime.fromtimestamp(start_time, timezone.utc).isoformat()
        
        mock_handler = Mock()
        mock_handler.config = self.sample_config
        mock_handler.state = {
            "framework_state": {
                "start_time": start_time_iso
            }
        }
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        total_time = integration._calculate_total_time()
        
        # Should return approximately "2m 0s"
        self.assertIn("2m", total_time)
        
        # Test with no start time
        mock_handler.state = {"framework_state": {}}
        total_time = integration._calculate_total_time()
        self.assertEqual(total_time, "unknown")
        
        # Test with invalid start time
        mock_handler.state = {"framework_state": {"start_time": "invalid-time"}}
        total_time = integration._calculate_total_time()
        self.assertEqual(total_time, "unknown")


class TestGlobalConvenienceFunctions(unittest.TestCase):
    """Test suite for global convenience functions"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_run_dir = os.path.join(self.temp_dir, "runs", "ACM-22079", "ACM-22079-20250826-120000")
        os.makedirs(self.test_run_dir, exist_ok=True)
        
        # Reset global integration instance
        import framework_integration
        framework_integration._observability_integration = None
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        # Reset global integration instance
        import framework_integration
        framework_integration._observability_integration = None
    
    @patch('framework_integration.FrameworkObservabilityIntegration')
    def test_get_observability_integration_singleton(self, mock_integration_class):
        """Test global integration instance singleton pattern"""
        mock_integration = Mock()
        mock_integration_class.return_value = mock_integration
        
        # First call should create instance
        integration1 = get_observability_integration(self.test_run_dir)
        mock_integration_class.assert_called_once_with(self.test_run_dir)
        
        # Second call should return same instance
        integration2 = get_observability_integration()
        self.assertEqual(integration1, integration2)
        
        # Should not create new instance
        self.assertEqual(mock_integration_class.call_count, 1)
    
    @patch('framework_integration.get_observability_integration')
    def test_init_observability(self, mock_get_integration):
        """Test observability initialization convenience function"""
        mock_integration = Mock()
        mock_get_integration.return_value = mock_integration
        
        init_observability(
            jira_ticket="ACM-22079",
            feature="Test feature",
            customer="Test customer"
        )
        
        # Verify integration method called
        mock_integration.on_framework_start.assert_called_once_with(
            "ACM-22079", "Test feature", customer="Test customer"
        )
    
    @patch('framework_integration.get_observability_integration')
    def test_observe_phase_transition(self, mock_get_integration):
        """Test phase transition observation convenience function"""
        mock_integration = Mock()
        mock_get_integration.return_value = mock_integration
        
        observe_phase_transition(
            phase="phase_2",
            status="completed",
            duration=120,
            agents=["agent_b", "agent_c"]
        )
        
        # Verify integration method called
        mock_integration.on_phase_transition.assert_called_once_with(
            "phase_2", "completed", duration=120, agents=["agent_b", "agent_c"]
        )
    
    @patch('framework_integration.get_observability_integration')
    def test_observe_agent_spawn(self, mock_get_integration):
        """Test agent spawn observation convenience function"""
        mock_integration = Mock()
        mock_get_integration.return_value = mock_integration
        
        inherited_context = {"business_requirements": "test"}
        observe_agent_spawn("agent_b", inherited_context, confidence=95.0)
        
        # Verify integration method called
        mock_integration.on_agent_spawn.assert_called_once_with(
            "agent_b", inherited_context, confidence=95.0
        )
    
    @patch('framework_integration.get_observability_integration')
    def test_observe_agent_completion(self, mock_get_integration):
        """Test agent completion observation convenience function"""
        mock_integration = Mock()
        mock_get_integration.return_value = mock_integration
        
        results = {"analysis": "completed"}
        context_contribution = {"technical_understanding": "comprehensive"}
        observe_agent_completion("agent_b", results, context_contribution, execution_time=45.2)
        
        # Verify integration method called
        mock_integration.on_agent_completion.assert_called_once_with(
            "agent_b", results, context_contribution, execution_time=45.2
        )
    
    @patch('framework_integration.get_observability_integration')
    def test_observe_context_inheritance(self, mock_get_integration):
        """Test context inheritance observation convenience function"""
        mock_integration = Mock()
        mock_get_integration.return_value = mock_integration
        
        context_data = {"inherited_data": "test"}
        observe_context_inheritance("agent_a", "agent_b", context_data, "passed", conflict_count=0)
        
        # Verify integration method called
        mock_integration.on_context_inheritance.assert_called_once_with(
            "agent_a", "agent_b", context_data, "passed", conflict_count=0
        )
    
    @patch('framework_integration.get_observability_integration')
    def test_observe_validation_checkpoint(self, mock_get_integration):
        """Test validation checkpoint observation convenience function"""
        mock_integration = Mock()
        mock_get_integration.return_value = mock_integration
        
        details = {"confidence": 98.5, "issues": []}
        observe_validation_checkpoint("evidence_validation", "passed", details, validator="EVE")
        
        # Verify integration method called
        mock_integration.on_validation_checkpoint.assert_called_once_with(
            "evidence_validation", "passed", details, validator="EVE"
        )
    
    @patch('framework_integration.get_observability_integration')
    def test_observe_framework_completion(self, mock_get_integration):
        """Test framework completion observation convenience function"""
        mock_integration = Mock()
        mock_get_integration.return_value = mock_integration
        
        deliverables = ["test-cases.md", "analysis.md"]
        quality_metrics = {"compliance": 100}
        observe_framework_completion(self.test_run_dir, deliverables, quality_metrics, success=True)
        
        # Verify integration method called
        mock_integration.on_framework_completion.assert_called_once_with(
            self.test_run_dir, deliverables, quality_metrics, success=True
        )
    
    @patch('framework_integration.get_observability_integration')
    def test_observe_error(self, mock_get_integration):
        """Test error observation convenience function"""
        mock_integration = Mock()
        mock_get_integration.return_value = mock_integration
        
        observe_error("ValidationError", "Test error message", "phase_2", "agent_b", severity="high")
        
        # Verify integration method called
        mock_integration.on_error_event.assert_called_once_with(
            "ValidationError", "Test error message", "phase_2", "agent_b", severity="high"
        )
    
    @patch('framework_integration.get_observability_integration')
    def test_process_observability_command(self, mock_get_integration):
        """Test observability command processing convenience function"""
        mock_integration = Mock()
        mock_integration.process_user_command.return_value = "Test response"
        mock_get_integration.return_value = mock_integration
        
        response = process_observability_command("/status")
        
        # Verify integration method called and response returned
        mock_integration.process_user_command.assert_called_once_with("/status")
        self.assertEqual(response, "Test response")
    
    @patch('framework_integration.get_observability_integration')
    def test_update_observability_metadata(self, mock_get_integration):
        """Test observability metadata update convenience function"""
        mock_integration = Mock()
        mock_get_integration.return_value = mock_integration
        
        metadata_updates = {"target_version": "2.15.0"}
        update_observability_metadata(metadata_updates)
        
        # Verify integration method called
        mock_integration.update_run_metadata.assert_called_once_with(metadata_updates)


class TestFrameworkIntegrationErrorHandling(unittest.TestCase):
    """Test suite for error handling and edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_run_dir = os.path.join(self.temp_dir, "runs", "ACM-22079", "ACM-22079-20250826-120000")
        os.makedirs(self.test_run_dir, exist_ok=True)
        
        # Reset global integration instance
        import framework_integration
        framework_integration._observability_integration = None
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        # Reset global integration instance
        import framework_integration
        framework_integration._observability_integration = None
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_handler_initialization_failure(self, mock_handler_class):
        """Test handling of handler initialization failures"""
        mock_handler_class.side_effect = Exception("Handler init failed")
        
        # Should not raise exception during integration init
        try:
            integration = FrameworkObservabilityIntegration(self.test_run_dir)
            # Integration should still be created but with limited functionality
            self.assertIsNotNone(integration)
        except Exception as e:
            self.fail(f"Integration initialization should handle handler failures gracefully: {e}")
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_handler_update_failure(self, mock_handler_class):
        """Test handling of handler update failures"""
        mock_handler = Mock()
        mock_handler.config = {"observability_agent": {"enabled": True}}
        mock_handler.update_state.side_effect = Exception("Update failed")
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Should not raise exception during event handling
        try:
            integration.on_framework_start("ACM-22079", "Test feature")
            integration.on_phase_transition("phase_1", "in_progress")
            integration.on_agent_spawn("agent_a", {})
        except Exception as e:
            self.fail(f"Event handling should be resilient to handler failures: {e}")
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_missing_configuration(self, mock_handler_class):
        """Test handling of missing or invalid configuration"""
        mock_handler = Mock()
        mock_handler.config = {}  # Empty configuration
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Should default to disabled when configuration is missing
        self.assertFalse(integration.is_enabled)
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_none_parameters_handling(self, mock_handler_class):
        """Test handling of None parameters in event methods"""
        mock_handler = Mock()
        mock_handler.config = {"observability_agent": {"enabled": True}}
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Test methods with None parameters
        integration.on_agent_spawn("agent_a", inherited_context=None)
        integration.on_agent_completion("agent_a", results=None, context_contribution=None)
        integration.on_context_inheritance("agent_a", "agent_b", context_data=None)
        integration.on_validation_checkpoint("test_checkpoint", "passed", details=None)
        integration.on_framework_completion(self.test_run_dir, [], quality_metrics=None)
        
        # Should handle None parameters gracefully
        self.assertEqual(mock_handler.update_state.call_count, 5)
    
    @patch('framework_integration.ObservabilityCommandHandler')
    def test_agent_completion_with_missing_agent(self, mock_handler_class):
        """Test agent completion when agent is not in active list"""
        mock_handler = Mock()
        mock_handler.config = {"observability_agent": {"enabled": True}}
        mock_handler.state = {"agent_coordination": {"active_agents": ["agent_b"]}}  # agent_a not in list
        mock_handler_class.return_value = mock_handler
        
        integration = FrameworkObservabilityIntegration(self.test_run_dir)
        
        # Should not raise error when removing non-existent agent
        integration.on_agent_completion("agent_a", {}, {})
        
        # Should still update state
        mock_handler.update_state.assert_called_once()


if __name__ == '__main__':
    # Create comprehensive test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestFrameworkObservabilityIntegration,
        TestGlobalConvenienceFunctions,
        TestFrameworkIntegrationErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n" + "="*60)
    print(f"FRAMEWORK INTEGRATION UNIT TESTS SUMMARY")
    print(f"="*60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure.split(chr(10))[0]}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, error in result.errors:
            print(f"  - {test}: {error.split(chr(10))[0]}")