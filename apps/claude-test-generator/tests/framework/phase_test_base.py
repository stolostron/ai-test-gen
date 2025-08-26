#!/usr/bin/env python3
"""
Base Testing Framework for Phase Unit Tests
Provides common functionality for testing all framework phases
"""

import unittest
import json
import tempfile
import os
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from unittest.mock import Mock, patch, MagicMock


@dataclass
class PhaseTestResult:
    """Standard result structure for phase testing"""
    phase_name: str
    execution_time: float
    success: bool
    output_files: List[str]
    output_data: Dict[str, Any]
    errors: List[str]
    warnings: List[str]


class PhaseTestBase(unittest.TestCase, ABC):
    """
    Abstract base class for all phase unit tests
    Provides common testing infrastructure and utilities
    """
    
    def setUp(self):
        """Set up common test environment"""
        self.test_temp_dir = tempfile.mkdtemp()
        self.start_time = time.time()
        self.phase_name = self.get_phase_name()
        self.required_outputs = self.get_required_outputs()
        self.test_fixtures = self.load_test_fixtures()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        if os.path.exists(self.test_temp_dir):
            shutil.rmtree(self.test_temp_dir)
    
    @abstractmethod
    def get_phase_name(self) -> str:
        """Return the name of the phase being tested"""
        pass
    
    @abstractmethod 
    def get_required_outputs(self) -> List[str]:
        """Return list of required output files/data for this phase"""
        pass
    
    @abstractmethod
    def load_test_fixtures(self) -> Dict[str, Any]:
        """Load test data fixtures for this phase"""
        pass
    
    def validate_phase_execution(self, phase_func, inputs: Dict[str, Any]) -> PhaseTestResult:
        """
        Standard validation framework for phase execution
        Tests: implementation exists, I/O correctness, file generation, timing
        """
        start_time = time.time()
        errors = []
        warnings = []
        output_files = []
        output_data = {}
        success = False
        
        try:
            # Test 1: Implementation exists
            if not self.test_implementation_exists(phase_func):
                errors.append("Phase implementation not found")
                return PhaseTestResult(
                    phase_name=self.phase_name,
                    execution_time=time.time() - start_time,
                    success=False,
                    output_files=[],
                    output_data={},
                    errors=errors,
                    warnings=warnings
                )
            
            # Test 2: Execute phase
            result = phase_func(**inputs)
            output_data = result if isinstance(result, dict) else {"result": result}
            
            # Test 3: Validate outputs
            output_files = self.validate_output_files()
            if len(output_files) < len(self.required_outputs):
                warnings.append(f"Expected {len(self.required_outputs)} output files, found {len(output_files)}")
            
            # Test 4: Validate data structure
            if not self.validate_output_data_structure(output_data):
                errors.append("Output data structure validation failed")
            
            success = len(errors) == 0
            
        except Exception as e:
            errors.append(f"Phase execution failed: {str(e)}")
            
        execution_time = time.time() - start_time
        
        return PhaseTestResult(
            phase_name=self.phase_name,
            execution_time=execution_time,
            success=success,
            output_files=output_files,
            output_data=output_data,
            errors=errors,
            warnings=warnings
        )
    
    def test_implementation_exists(self, phase_func) -> bool:
        """Test that the phase implementation actually exists"""
        return callable(phase_func)
    
    def validate_output_files(self) -> List[str]:
        """Check for expected output files in temp directory"""
        if not os.path.exists(self.test_temp_dir):
            return []
            
        files = []
        for root, dirs, filenames in os.walk(self.test_temp_dir):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files
    
    def validate_output_data_structure(self, data: Dict[str, Any]) -> bool:
        """Validate the structure of output data"""
        # Override in subclasses for specific validation
        return isinstance(data, dict) and len(data) > 0
    
    def create_mock_input(self, input_type: str) -> Dict[str, Any]:
        """Create mock input data for testing"""
        mock_inputs = {
            "jira_ticket": {
                "jira_id": "ACM-22079",
                "title": "ClusterCurator digest-based upgrades",
                "fixVersion": "ACM 2.15.0",
                "status": "Closed"
            },
            "environment": {
                "name": "qe6-vmware-ibm",
                "acm_version": "ACM 2.14.0",
                "health_score": 8.7
            }
        }
        return mock_inputs.get(input_type, {})
    
    def assert_phase_success(self, result: PhaseTestResult):
        """Assert that phase execution was successful"""
        self.assertTrue(result.success, f"Phase {result.phase_name} failed: {result.errors}")
        self.assertGreater(len(result.output_data), 0, "No output data generated")
        if self.required_outputs:
            self.assertGreaterEqual(len(result.output_files), len(self.required_outputs), 
                                    "Missing required output files")
    
    def assert_performance_acceptable(self, result: PhaseTestResult, max_time: float = 5.0):
        """Assert that phase execution completed within acceptable time"""
        self.assertLess(result.execution_time, max_time,
                       f"Phase {result.phase_name} took too long: {result.execution_time:.2f}s")


class Phase0TestBase(PhaseTestBase):
    """
    Specialized base class for Phase 0 (Version Intelligence Service) testing
    """
    
    def get_phase_name(self) -> str:
        return "Phase 0 - Version Intelligence Service"
    
    def get_required_outputs(self) -> List[str]:
        return ["foundation-context.json"]
    
    def load_test_fixtures(self) -> Dict[str, Any]:
        return {
            "sample_jira": {
                "ACM-22079": {
                    "id": "ACM-22079",
                    "fixVersion": "ACM 2.15.0",
                    "title": "ClusterCurator digest-based upgrades"
                }
            },
            "sample_environments": {
                "qe6-vmware-ibm": {
                    "acm_version": "ACM 2.14.0",
                    "health_score": 8.7
                }
            }
        }
    
    def validate_foundation_context_structure(self, context_data: Dict[str, Any]) -> bool:
        """Validate Phase 0 specific output structure"""
        required_fields = [
            'jira_id', 'target_version', 'environment_version', 
            'version_gap', 'environment', 'deployment_instruction'
        ]
        
        for field in required_fields:
            if field not in context_data:
                return False
                
        return True
    
    def validate_output_data_structure(self, data: Dict[str, Any]) -> bool:
        """Override to validate foundation context structure"""
        if not super().validate_output_data_structure(data):
            return False
            
        # Check for foundation context in the data
        if 'foundation_context' in data:
            return self.validate_foundation_context_structure(data['foundation_context'])
        elif 'jira_id' in data:  # Direct context data
            return self.validate_foundation_context_structure(data)
            
        return False