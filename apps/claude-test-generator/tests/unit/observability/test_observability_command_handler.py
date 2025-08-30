#!/usr/bin/env python3
"""
Comprehensive unit tests for Framework Observability Agent - Command Handler

Tests the core ObservabilityCommandHandler functionality including:
- All 13 command interface handlers
- State management and updates
- Configuration loading and validation
- Data processing and response formatting
- Real-time command processing
"""

import unittest
import json
import tempfile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add the observability directory to the path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../.claude/observability'))

from observability_command_handler import ObservabilityCommandHandler


class TestObservabilityCommandHandler(unittest.TestCase):
    """Test suite for ObservabilityCommandHandler core functionality"""
    
    def setUp(self):
        """Set up test environment with temporary directories and mock data"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_run_dir = os.path.join(self.temp_dir, "runs", "ACM-22079", "ACM-22079-20250826-120000")
        os.makedirs(self.test_run_dir, exist_ok=True)
        
        # Sample configuration data
        self.sample_config = {
            "observability_agent": {
                "enabled": True,
                "service_id": "tg_framework_observability_agent",
                "execution_mode": "on_demand",
                "authority_level": "read_only",
                "command_interface": {
                    "enabled": True,
                    "response_formatting": "detailed"
                },
                "data_access": {
                    "framework_state": True,
                    "sub_agent_outputs": True,
                    "performance_metrics": True
                }
            },
            "command_definitions": {
                "primary_commands": {
                    "/status": {
                        "description": "Current execution status and progress",
                        "access_level": "public"
                    }
                }
            }
        }
        
        # Sample run metadata
        self.sample_run_metadata = {
            "jira_ticket": "ACM-22079",
            "feature": "Digest-based upgrades via ClusterCurator",
            "customer": "Amadeus",
            "priority": "Critical",
            "framework_execution": {
                "phase_0_pre": {"status": "completed", "timestamp": "2025-08-26T12:00:00Z"},
                "phase_0": {"status": "completed", "timestamp": "2025-08-26T12:01:00Z"},
                "phase_1": {"status": "in_progress", "timestamp": "2025-08-26T12:02:00Z"}
            },
            "test_environment": {
                "cluster": "qe6",
                "health_score": "8.5/10",
                "acm_version": "2.14.0",
                "platform": "aws",
                "region": "us-east-1",
                "console_url": "https://console-openshift-console.apps.qe6.example.com"
            },
            "implementation_details": {
                "primary_pr": "stolostron/cluster-curator-controller#468",
                "pr_status": "merged",
                "component": "cluster-curator-controller",
                "annotation_required": "cluster.open-cluster-management.io/allow-unsupported-upgrade",
                "fallback_chain": "conditionalUpdates → availableUpdates → image tag"
            }
        }
        
        # Create metadata file
        metadata_path = os.path.join(self.test_run_dir, "run-metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(self.sample_run_metadata, f, indent=2)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization_with_run_directory(self):
        """Test handler initialization with specific run directory"""
        with patch('observability_command_handler.Path') as mock_path:
            mock_path.return_value.exists.return_value = False
            
            handler = ObservabilityCommandHandler(run_directory=self.test_run_dir)
            
            self.assertEqual(handler.run_directory, self.test_run_dir)
            self.assertIsInstance(handler.config, dict)
            self.assertIsInstance(handler.state, dict)
            self.assertEqual(handler.command_history, [])
    
    def test_initialization_auto_detect_run(self):
        """Test handler initialization with automatic run detection"""
        with patch('observability_command_handler.Path') as mock_path:
            # Mock run directory detection
            mock_runs_dir = Mock()
            mock_path.return_value = mock_runs_dir
            mock_runs_dir.exists.return_value = True
            
            # Mock run directories
            mock_run_dir = Mock()
            mock_run_dir.is_dir.return_value = True
            mock_run_dir.stat.return_value.st_mtime = 1640995200  # Mock timestamp
            mock_runs_dir.iterdir.return_value = [mock_run_dir]
            
            with patch('observability_command_handler.max', return_value=mock_run_dir):
                with patch('str', return_value="/test/run/dir"):
                    handler = ObservabilityCommandHandler()
                    
                    # Should have detected a run directory
                    self.assertIsNotNone(handler.run_directory)
    
    def test_configuration_loading(self):
        """Test configuration loading from file"""
        config_dir = os.path.join(self.temp_dir, ".claude", "config")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "observability-config.json")
        
        with open(config_path, 'w') as f:
            json.dump(self.sample_config, f)
        
        with patch('observability_command_handler.Path') as mock_path:
            mock_path.return_value.exists.return_value = True
            
            with patch('builtins.open', mock_open(read_data=json.dumps(self.sample_config))):
                handler = ObservabilityCommandHandler(run_directory=self.test_run_dir)
                
                self.assertEqual(handler.config["observability_agent"]["enabled"], True)
                self.assertEqual(handler.config["observability_agent"]["service_id"], "tg_framework_observability_agent")
    
    def test_configuration_default_when_missing(self):
        """Test default configuration when config file is missing"""
        with patch('observability_command_handler.Path') as mock_path:
            mock_path.return_value.exists.return_value = False
            
            handler = ObservabilityCommandHandler(run_directory=self.test_run_dir)
            
            # Should have default configuration
            self.assertTrue(handler.config["observability_agent"]["enabled"])
    
    def test_state_initialization(self):
        """Test initial state structure and values"""
        handler = ObservabilityCommandHandler(run_directory=self.test_run_dir)
        
        # Verify state structure
        required_keys = [
            "framework_state", "agent_coordination", "key_insights", 
            "validation_status", "environment_context", "run_metadata",
            "performance_metrics", "risk_alerts"
        ]
        
        for key in required_keys:
            self.assertIn(key, handler.state)
        
        # Verify initial values
        self.assertEqual(handler.state["framework_state"]["current_phase"], "unknown")
        self.assertEqual(handler.state["framework_state"]["completion_percentage"], 0)
        self.assertEqual(handler.state["agent_coordination"]["active_agents"], [])
        self.assertEqual(handler.state["agent_coordination"]["completed_agents"], [])
    
    def test_state_update_functionality(self):
        """Test state update with deep merging"""
        handler = ObservabilityCommandHandler(run_directory=self.test_run_dir)
        
        # Test simple update
        update_data = {
            "framework_state": {
                "current_phase": "phase_1",
                "completion_percentage": 25
            }
        }
        
        handler.update_state(update_data)
        
        self.assertEqual(handler.state["framework_state"]["current_phase"], "phase_1")
        self.assertEqual(handler.state["framework_state"]["completion_percentage"], 25)
        # Original start_time should still exist
        self.assertIn("start_time", handler.state["framework_state"])
    
    def test_state_deep_update_functionality(self):
        """Test deep update with nested dictionary merging"""
        handler = ObservabilityCommandHandler(run_directory=self.test_run_dir)
        
        # Set initial nested state
        handler.state["test_nested"] = {
            "level1": {
                "keep_this": "original_value",
                "update_this": "old_value"
            }
        }
        
        # Update with partial nested data
        update_data = {
            "test_nested": {
                "level1": {
                    "update_this": "new_value",
                    "add_this": "added_value"
                }
            }
        }
        
        handler.update_state(update_data)
        
        # Should preserve original keys and add/update new ones
        self.assertEqual(handler.state["test_nested"]["level1"]["keep_this"], "original_value")
        self.assertEqual(handler.state["test_nested"]["level1"]["update_this"], "new_value")
        self.assertEqual(handler.state["test_nested"]["level1"]["add_this"], "added_value")


class TestObservabilityCommands(unittest.TestCase):
    """Test suite for individual command handlers"""
    
    def setUp(self):
        """Set up test environment for command testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_run_dir = os.path.join(self.temp_dir, "runs", "ACM-22079", "ACM-22079-20250826-120000")
        os.makedirs(self.test_run_dir, exist_ok=True)
        
        # Create handler with test data
        self.handler = ObservabilityCommandHandler(run_directory=self.test_run_dir)
        
        # Add sample run metadata to state
        self.handler.state["run_metadata"] = {
            "jira_ticket": "ACM-22079",
            "feature": "Digest-based upgrades via ClusterCurator",
            "customer": "Amadeus",
            "priority": "Critical",
            "framework_execution": {
                "phase_0": {"status": "completed"},
                "phase_1": {"status": "in_progress"}
            },
            "test_environment": {
                "cluster": "qe6",
                "health_score": "8.5/10",
                "acm_version": "2.14.0"
            }
        }
        
        # Add agent coordination state
        self.handler.state["agent_coordination"] = {
            "active_agents": ["agent_d"],
            "completed_agents": ["agent_a"],
            "context_chain_status": "agent_a → agent_d validated"
        }
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_status_command(self):
        """Test /status command output and formatting"""
        response = self.handler.process_command("/status")
        
        # Verify response structure
        self.assertIn("FRAMEWORK EXECUTION STATUS", response)
        self.assertIn("ACM-22079", response)
        self.assertIn("Digest-based upgrades", response)
        self.assertIn("ACTIVE EXECUTION", response)
        self.assertIn("COMPLETED PHASES", response)
        self.assertIn("CONTEXT INHERITANCE", response)
        self.assertIn("NEXT STEPS", response)
        
        # Verify command history tracking
        self.assertEqual(len(self.handler.command_history), 1)
        self.assertEqual(self.handler.command_history[0]["command"], "/status")
    
    def test_business_command(self):
        """Test /business command output and customer context"""
        response = self.handler.process_command("/business")
        
        # Verify business analysis content
        self.assertIn("BUSINESS IMPACT ANALYSIS", response)
        self.assertIn("Customer", response)
        self.assertIn("Amadeus", response)
        self.assertIn("Priority", response)
        self.assertIn("Critical", response)
        self.assertIn("CUSTOMER PAIN POINT", response)
        self.assertIn("SUCCESS CRITERIA", response)
    
    def test_technical_command(self):
        """Test /technical command output and implementation details"""
        # Add implementation details to state
        self.handler.state["run_metadata"]["implementation_details"] = {
            "primary_pr": "stolostron/cluster-curator-controller#468",
            "pr_status": "merged",
            "annotation_required": "cluster.open-cluster-management.io/allow-unsupported-upgrade",
            "fallback_chain": "conditionalUpdates → availableUpdates → image tag"
        }
        
        response = self.handler.process_command("/technical")
        
        # Verify technical analysis content
        self.assertIn("TECHNICAL IMPLEMENTATION ANALYSIS", response)
        self.assertIn("stolostron/cluster-curator-controller#468", response)
        self.assertIn("CORE LOGIC FLOW", response)
        self.assertIn("VALIDATION STATUS", response)
    
    def test_agents_command(self):
        """Test /agents command output and agent coordination"""
        response = self.handler.process_command("/agents")
        
        # Verify agent status content
        self.assertIn("SUB-AGENT STATUS AND COORDINATION", response)
        self.assertIn("AGENT EXECUTION STATUS", response)
        self.assertIn("Agent A (JIRA Intelligence)", response)
        self.assertIn("Agent D (Environment Intelligence)", response)
        self.assertIn("✅ Completed", response)  # agent_a should be completed
        self.assertIn("🔄 Active", response)     # agent_d should be active
        self.assertIn("CONTEXT INHERITANCE FLOW", response)
        self.assertIn("DATA FLOW SUMMARY", response)
    
    def test_environment_command(self):
        """Test /environment command output and environment assessment"""
        response = self.handler.process_command("/environment")
        
        # Verify environment analysis content
        self.assertIn("ENVIRONMENT ASSESSMENT", response)
        self.assertIn("Cluster Health", response)
        self.assertIn("8.5/10", response)
        self.assertIn("Test Environment", response)
        self.assertIn("qe6", response)
        self.assertIn("ACM Version", response)
        self.assertIn("2.14.0", response)
        self.assertIn("TESTING READINESS", response)
    
    def test_risks_command(self):
        """Test /risks command output and risk analysis"""
        # Add target version to create version compatibility risk
        self.handler.state["run_metadata"]["target_version"] = "2.15.0"
        
        response = self.handler.process_command("/risks")
        
        # Verify risk analysis content
        self.assertIn("RISK ANALYSIS AND MITIGATION STATUS", response)
        self.assertIn("VERSION COMPATIBILITY RISK", response)
        self.assertIn("2.15.0", response)
        self.assertIn("2.14.0", response)
        self.assertIn("Mitigation", response)
    
    def test_timeline_command(self):
        """Test /timeline command output and execution timeline"""
        response = self.handler.process_command("/timeline")
        
        # Verify timeline content
        self.assertIn("EXECUTION TIMELINE AND MILESTONES", response)
        self.assertIn("Execution Time", response)
        self.assertIn("PHASE MILESTONES", response)
        self.assertIn("Phase 0", response)
        self.assertIn("Phase 1", response)
        self.assertIn("Phase 2", response)
    
    def test_context_flow_command(self):
        """Test /context-flow command output and context visualization"""
        response = self.handler.process_command("/context-flow")
        
        # Verify context flow content
        self.assertIn("PROGRESSIVE CONTEXT ARCHITECTURE STATUS", response)
        self.assertIn("CONTEXT INHERITANCE CHAIN", response)
        self.assertIn("Agent A Foundation", response)
        self.assertIn("Agent D Enhancement", response)
        self.assertIn("VALIDATION CHECKPOINTS", response)
    
    def test_validation_status_command(self):
        """Test /validation-status command output and validation engines"""
        # Add validation status to state
        self.handler.state["validation_status"] = {
            "implementation_reality": "passed",
            "evidence_validation": "in_progress",
            "cross_agent_validation": "pending"
        }
        
        response = self.handler.process_command("/validation-status")
        
        # Verify validation status content
        self.assertIn("VALIDATION STATUS AND QUALITY CHECKS", response)
        self.assertIn("VALIDATION ENGINES", response)
        self.assertIn("Implementation Reality Agent", response)
        self.assertIn("Evidence Validation Engine", response)
        self.assertIn("✅", response)  # Should show passed validation
        self.assertIn("🔄", response)  # Should show in-progress validation
    
    def test_performance_command(self):
        """Test /performance command output and performance metrics"""
        response = self.handler.process_command("/performance")
        
        # Verify performance content
        self.assertIn("FRAMEWORK PERFORMANCE METRICS", response)
        self.assertIn("AGENT PERFORMANCE", response)
        self.assertIn("RESOURCE UTILIZATION", response)
        self.assertIn("PERFORMANCE FEATURES", response)
        self.assertIn("Parallel Execution", response)
        self.assertIn("Progressive Context", response)
    
    def test_help_command(self):
        """Test /help command output and command reference"""
        response = self.handler.process_command("/help")
        
        # Verify help content
        self.assertIn("OBSERVABILITY AGENT COMMANDS", response)
        self.assertIn("PRIMARY COMMANDS", response)
        self.assertIn("ADVANCED COMMANDS", response)
        self.assertIn("/status", response)
        self.assertIn("/business", response)
        self.assertIn("/deep-dive", response)
        self.assertIn("USAGE EXAMPLES", response)
    
    def test_unknown_command(self):
        """Test handling of unknown commands"""
        response = self.handler.process_command("/invalid-command")
        
        # Verify unknown command handling
        self.assertIn("UNKNOWN COMMAND", response)
        self.assertIn("/invalid-command", response)
        self.assertIn("Available commands", response)
        self.assertIn("/help", response)


class TestObservabilityDeepDive(unittest.TestCase):
    """Test suite for deep-dive command functionality"""
    
    def setUp(self):
        """Set up test environment for deep-dive testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_run_dir = os.path.join(self.temp_dir, "runs", "ACM-22079", "ACM-22079-20250826-120000")
        os.makedirs(self.test_run_dir, exist_ok=True)
        
        self.handler = ObservabilityCommandHandler(run_directory=self.test_run_dir)
        
        # Add comprehensive run metadata for deep-dive testing
        self.handler.state["run_metadata"] = {
            "jira_ticket": "ACM-22079",
            "feature": "Digest-based upgrades via ClusterCurator",
            "customer": "Amadeus",
            "priority": "Critical",
            "implementation_details": {
                "primary_pr": "stolostron/cluster-curator-controller#468",
                "pr_status": "merged",
                "component": "cluster-curator-controller",
                "annotation_required": "cluster.open-cluster-management.io/allow-unsupported-upgrade",
                "fallback_chain": "conditionalUpdates → availableUpdates → image tag"
            },
            "test_environment": {
                "cluster": "qe6",
                "health_score": "8.5/10",
                "acm_version": "2.14.0",
                "ocp_version": "4.15.0",
                "platform": "aws",
                "region": "us-east-1",
                "console_url": "https://console-openshift-console.apps.qe6.example.com"
            }
        }
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_deep_dive_agent_a(self):
        """Test deep-dive analysis for Agent A (JIRA Intelligence)"""
        response = self.handler.process_command("/deep-dive agent_a")
        
        # Verify Agent A deep-dive content
        self.assertIn("AGENT A (JIRA INTELLIGENCE) - DEEP DIVE", response)
        self.assertIn("MISSION COMPLETED", response)
        self.assertIn("Requirements extraction", response)
        self.assertIn("Business context", response)
        self.assertIn("KEY EXTRACTIONS", response)
        self.assertIn("ACM-22079", response)
        self.assertIn("Amadeus", response)
        self.assertIn("IMPLEMENTATION INTELLIGENCE", response)
        self.assertIn("stolostron/cluster-curator-controller#468", response)
        self.assertIn("CONTEXT FOUNDATION PROVIDED", response)
    
    def test_deep_dive_agent_d(self):
        """Test deep-dive analysis for Agent D (Environment Intelligence)"""
        response = self.handler.process_command("/deep-dive agent_d")
        
        # Verify Agent D deep-dive content
        self.assertIn("AGENT D (ENVIRONMENT INTELLIGENCE) - DEEP DIVE", response)
        self.assertIn("MISSION COMPLETED", response)
        self.assertIn("environment health assessment", response)
        self.assertIn("ENVIRONMENT ASSESSMENT", response)
        self.assertIn("qe6", response)
        self.assertIn("8.5/10", response)
        self.assertIn("VERSION INTELLIGENCE", response)
        self.assertIn("2.14.0", response)
        self.assertIn("DEPLOYMENT CONFIDENCE", response)
        self.assertIn("CONTEXT ENHANCEMENT", response)
    
    def test_deep_dive_agent_b(self):
        """Test deep-dive analysis for Agent B (Documentation Intelligence)"""
        response = self.handler.process_command("/deep-dive agent_b")
        
        # Verify Agent B deep-dive content
        self.assertIn("AGENT B (DOCUMENTATION INTELLIGENCE) - DEEP DIVE", response)
        self.assertIn("MISSION COMPLETED", response)
        self.assertIn("documentation analysis", response)
        self.assertIn("TECHNICAL UNDERSTANDING ACHIEVED", response)
        self.assertIn("ClusterCurator Functionality", response)
        self.assertIn("KEY TECHNICAL CONCEPTS MASTERED", response)
        self.assertIn("Image Tags vs Digests", response)
        self.assertIn("E2E TESTING PATTERNS EXTRACTED", response)
        self.assertIn("Console Navigation", response)
    
    def test_deep_dive_agent_c(self):
        """Test deep-dive analysis for Agent C (GitHub Investigation)"""
        response = self.handler.process_command("/deep-dive agent_c")
        
        # Verify Agent C deep-dive content
        self.assertIn("AGENT C (GITHUB INVESTIGATION) - DEEP DIVE", response)
        self.assertIn("MISSION COMPLETED", response)
        self.assertIn("GitHub code investigation", response)
        self.assertIn("IMPLEMENTATION ANALYSIS", response)
        self.assertIn("stolostron/cluster-curator-controller#468", response)
        self.assertIn("DIGEST FALLBACK MECHANISM", response)
        self.assertIn("CODE CHANGES VALIDATED", response)
        self.assertIn("INTEGRATION POINTS IDENTIFIED", response)
        self.assertIn("TESTING SCENARIOS EXTRACTED", response)
    
    def test_deep_dive_qe_intelligence(self):
        """Test deep-dive analysis for QE Intelligence Service"""
        response = self.handler.process_command("/deep-dive qe")
        
        # Verify QE Intelligence deep-dive content
        self.assertIn("QE INTELLIGENCE SERVICE - DEEP DIVE", response)
        self.assertIn("MISSION COMPLETED", response)
        self.assertIn("ultrathink reasoning", response)
        self.assertIn("ULTRATHINK ANALYSIS RESULTS", response)
        self.assertIn("Pattern Recognition", response)
        self.assertIn("EXISTING TESTING PATTERNS ANALYZED", response)
        self.assertIn("STRATEGIC GAP ANALYSIS", response)
        self.assertIn("TESTING STRATEGY RECOMMENDATIONS", response)
        self.assertIn("ULTRATHINK STRATEGIC INSIGHTS", response)
    
    def test_deep_dive_alternative_names(self):
        """Test deep-dive with alternative agent names"""
        # Test alternative names for agents
        jira_response = self.handler.process_command("/deep-dive jira")
        self.assertIn("AGENT A (JIRA INTELLIGENCE)", jira_response)
        
        environment_response = self.handler.process_command("/deep-dive environment")
        self.assertIn("AGENT D (ENVIRONMENT INTELLIGENCE)", environment_response)
        
        documentation_response = self.handler.process_command("/deep-dive documentation")
        self.assertIn("AGENT B (DOCUMENTATION INTELLIGENCE)", documentation_response)
        
        github_response = self.handler.process_command("/deep-dive github")
        self.assertIn("AGENT C (GITHUB INVESTIGATION)", github_response)
        
        qe_response = self.handler.process_command("/deep-dive qe_intelligence")
        self.assertIn("QE INTELLIGENCE SERVICE", qe_response)
    
    def test_deep_dive_unknown_agent(self):
        """Test deep-dive with unknown agent parameter"""
        response = self.handler.process_command("/deep-dive unknown_agent")
        
        # Should show available agents
        self.assertIn("Available Agents for Deep Dive", response)
        self.assertIn("agent_a", response)
        self.assertIn("agent_d", response)
        self.assertIn("agent_b", response)
        self.assertIn("agent_c", response)
        self.assertIn("qe", response)
        self.assertIn("Usage", response)
    
    def test_deep_dive_no_parameter(self):
        """Test deep-dive without agent parameter"""
        response = self.handler.process_command("/deep-dive")
        
        # Should show available agents when no parameter provided
        self.assertIn("Available Agents for Deep Dive", response)
        self.assertIn("JIRA Intelligence", response)
        self.assertIn("Environment Intelligence", response)
        self.assertIn("Documentation Intelligence", response)
        self.assertIn("GitHub Investigation", response)


class TestObservabilityDataProcessing(unittest.TestCase):
    """Test suite for data processing and utility methods"""
    
    def setUp(self):
        """Set up test environment for data processing testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_run_dir = os.path.join(self.temp_dir, "runs", "ACM-22079", "ACM-22079-20250826-120000")
        os.makedirs(self.test_run_dir, exist_ok=True)
        
        self.handler = ObservabilityCommandHandler(run_directory=self.test_run_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_refresh_run_data_with_metadata(self):
        """Test refreshing run data from metadata file"""
        # Create metadata file
        metadata = {
            "jira_ticket": "ACM-22079",
            "feature": "Test feature",
            "framework_execution": {
                "phase_0": {"status": "completed"},
                "phase_1": {"status": "in_progress"}
            }
        }
        
        metadata_path = os.path.join(self.test_run_dir, "run-metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        # Refresh data
        self.handler._refresh_run_data()
        
        # Verify metadata was loaded
        self.assertEqual(self.handler.state["run_metadata"]["jira_ticket"], "ACM-22079")
        self.assertEqual(self.handler.state["run_metadata"]["feature"], "Test feature")
    
    def test_refresh_run_data_no_metadata(self):
        """Test refreshing run data when metadata file doesn't exist"""
        # Ensure no metadata file exists
        metadata_path = os.path.join(self.test_run_dir, "run-metadata.json")
        if os.path.exists(metadata_path):
            os.remove(metadata_path)
        
        # Should not raise error
        self.handler._refresh_run_data()
    
    def test_refresh_run_data_invalid_json(self):
        """Test refreshing run data with invalid JSON metadata"""
        # Create invalid JSON metadata file
        metadata_path = os.path.join(self.test_run_dir, "run-metadata.json")
        with open(metadata_path, 'w') as f:
            f.write("{ invalid json content")
        
        # Should not raise error
        self.handler._refresh_run_data()
    
    def test_determine_current_phase(self):
        """Test phase determination from execution data"""
        execution_data = {
            "phase_0": {"status": "completed"},
            "phase_1": {"status": "in_progress"},
            "phase_2": {"status": "pending"}
        }
        
        current_phase = self.handler._determine_current_phase(execution_data)
        self.assertEqual(current_phase, "Phase 1")
        
        # Test all completed phases
        completed_execution = {
            "phase_0": {"status": "completed"},
            "phase_1": {"status": "completed"}
        }
        
        completed_phase = self.handler._determine_current_phase(completed_execution)
        self.assertEqual(completed_phase, "Phase 2 Complete")
    
    def test_calculate_completion_percentage(self):
        """Test completion percentage calculation"""
        execution_data = {
            "phase_0": {"status": "completed"},
            "phase_1": {"status": "completed"},
            "phase_2": {"status": "in_progress"}
        }
        
        percentage = self.handler._calculate_completion_percentage(execution_data)
        # 2 completed out of 8 total phases = 25%
        self.assertEqual(percentage, 25)
        
        # Test 100% cap
        all_completed = {
            f"phase_{i}": {"status": "completed"} for i in range(10)
        }
        
        max_percentage = self.handler._calculate_completion_percentage(all_completed)
        self.assertEqual(max_percentage, 100)
    
    def test_get_business_context(self):
        """Test business context extraction"""
        # Test disconnected environment context
        self.handler.state["run_metadata"] = {
            "feature": "Digest-based upgrades for disconnected environments"
        }
        
        context = self.handler._get_business_context()
        self.assertIn("disconnected", context.lower())
        
        # Test customer context
        self.handler.state["run_metadata"] = {
            "customer": "Amadeus",
            "feature": "Regular feature"
        }
        
        context = self.handler._get_business_context()
        self.assertIn("Amadeus", context)
    
    def test_get_agent_activity(self):
        """Test agent activity description"""
        agent_a_activity = self.handler._get_agent_activity("agent_a")
        self.assertIn("JIRA", agent_a_activity)
        
        agent_d_activity = self.handler._get_agent_activity("agent_d")
        self.assertIn("Environment", agent_d_activity)
        
        unknown_activity = self.handler._get_agent_activity("unknown_agent")
        self.assertIn("Processing framework data", unknown_activity)
    
    def test_get_completed_phases(self):
        """Test completed phases extraction"""
        self.handler.state["run_metadata"] = {
            "framework_execution": {
                "phase_0": {"status": "completed"},
                "phase_1": {"status": "completed"},
                "phase_2": {"status": "in_progress"}
            }
        }
        
        completed = self.handler._get_completed_phases()
        
        self.assertEqual(len(completed), 2)
        self.assertEqual(completed[0]["name"], "Phase 0")
        self.assertIn("description", completed[0])
    
    def test_command_history_management(self):
        """Test command history tracking and limits"""
        # Add commands up to limit
        for i in range(55):  # Exceed the 50 command limit
            self.handler.process_command("/status")
        
        # Should maintain only last 50 commands
        self.assertEqual(len(self.handler.command_history), 50)
        
        # Verify each history entry has required fields
        for entry in self.handler.command_history:
            self.assertIn("command", entry)
            self.assertIn("timestamp", entry)
            self.assertEqual(entry["command"], "/status")


if __name__ == '__main__':
    # Create comprehensive test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestObservabilityCommandHandler,
        TestObservabilityCommands,
        TestObservabilityDeepDive,
        TestObservabilityDataProcessing
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n" + "="*60)
    print(f"OBSERVABILITY COMMAND HANDLER UNIT TESTS SUMMARY")
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