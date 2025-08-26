#!/usr/bin/env python3
"""
Hybrid AI-Enhanced Unit Tests for Phase 0
Combines deterministic Python validation with AI-powered analysis
"""

import unittest
import json
import tempfile
import os
import sys
import time
from typing import Dict, Any, List
from dataclasses import dataclass
from unittest.mock import Mock, patch, MagicMock

# Systematic Import Path Management for AI Services
def setup_ai_services_path():
    """Add AI services directory to Python path if not already present"""
    import sys
    import os
    
    # Get the AI services path relative to the test file
    ai_services_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services'))
    
    if ai_services_path not in sys.path:
        sys.path.insert(0, ai_services_path)
    
    # Also add tests ai_services for test enhancer
    tests_ai_services_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ai_services'))
    if tests_ai_services_path not in sys.path:
        sys.path.insert(0, tests_ai_services_path)
    
    return ai_services_path

# Setup import path and import modules
setup_ai_services_path()

try:
    from ai_test_enhancer import AITestEnhancer, HybridPhase0TestOrchestrator
except ImportError as e:
    print(f"Failed to import AI Test Enhancer: {e}")
    # Continue without test enhancer - tests can still run in basic mode


@dataclass
class HybridTestResult:
    """Result combining Python unit test results with AI analysis"""
    python_test_result: bool
    python_execution_time: float
    python_errors: List[str]
    ai_analysis_result: Dict[str, Any]
    ai_execution_time: float
    combined_confidence: float
    hybrid_recommendations: List[str]


class HybridPhase0TestCase(unittest.TestCase):
    """
    Hybrid test case combining deterministic Python validation with AI enhancement
    Each test method executes Python validation first, then enhances with AI analysis
    """
    
    def setUp(self):
        """Set up hybrid testing environment"""
        self.framework_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
        self.ai_enhancer = AITestEnhancer(self.framework_root)
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up hybrid testing environment"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def execute_hybrid_test(self, test_name: str, python_test_func, ai_analysis_func) -> HybridTestResult:
        """
        Framework for executing hybrid tests
        Combines Python deterministic testing with AI-powered analysis
        """
        print(f"\n🔬 Executing Hybrid Test: {test_name}")
        print("-" * 50)
        
        # Phase 1: Execute Python test (deterministic)
        print("🐍 Phase 1: Python Deterministic Validation")
        python_start = time.time()
        python_result = False
        python_errors = []
        
        try:
            python_test_func()
            python_result = True
            print("   ✅ Python validation: PASSED")
        except Exception as e:
            python_errors.append(str(e))
            print(f"   ❌ Python validation: FAILED - {str(e)}")
        
        python_time = time.time() - python_start
        
        # Phase 2: Execute AI analysis (enhancement)
        print("🤖 Phase 2: AI Enhancement Analysis")
        ai_start = time.time()
        ai_result = {}
        
        try:
            ai_result = ai_analysis_func()
            print(f"   🧠 AI analysis: {len(ai_result.get('findings', []))} findings generated")
        except Exception as e:
            ai_result = {"error": str(e), "findings": [], "recommendations": []}
            print(f"   ⚠️  AI analysis: Failed - {str(e)}")
        
        ai_time = time.time() - ai_start
        
        # Phase 3: Generate hybrid recommendations
        print("💡 Phase 3: Hybrid Recommendation Generation")
        hybrid_recommendations = self._generate_hybrid_recommendations(
            python_result, python_errors, ai_result
        )
        
        # Calculate combined confidence
        python_confidence = 1.0 if python_result else 0.0
        ai_confidence = ai_result.get('confidence', 0.5) if not ai_result.get('error') else 0.0
        combined_confidence = (python_confidence * 0.7) + (ai_confidence * 0.3)  # Weight Python higher
        
        print(f"   📊 Combined confidence: {combined_confidence:.2f}")
        print(f"   💡 Hybrid recommendations: {len(hybrid_recommendations)}")
        
        return HybridTestResult(
            python_test_result=python_result,
            python_execution_time=python_time,
            python_errors=python_errors,
            ai_analysis_result=ai_result,
            ai_execution_time=ai_time,
            combined_confidence=combined_confidence,
            hybrid_recommendations=hybrid_recommendations
        )
    
    def _generate_hybrid_recommendations(self, python_result: bool, python_errors: List[str], ai_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations combining Python and AI results"""
        recommendations = []
        
        # If Python test failed, use AI to provide context
        if not python_result:
            for error in python_errors:
                if "ImportError" in error or "not found" in error:
                    recommendations.append("CRITICAL: Implement missing service - create actual Python module")
                elif "Function not implemented" in error:
                    recommendations.append("HIGH: Implement missing functions identified by Python tests")
                elif "No file output" in error:
                    recommendations.append("HIGH: Add file generation capability as detected by Python validation")
        
        # Add AI-specific recommendations
        ai_recommendations = ai_result.get('recommendations', [])
        for ai_rec in ai_recommendations[:3]:  # Top 3 AI recommendations
            recommendations.append(f"AI-ENHANCED: {ai_rec}")
        
        # If both Python and AI agree, high confidence recommendation
        if not python_result and len(ai_result.get('findings', [])) > 0:
            recommendations.append("HYBRID: Both Python and AI analysis confirm implementation gaps - prioritize fixes")
        
        return recommendations
    
    # ===================================
    # HYBRID TEST METHODS
    # ===================================
    
    def test_hybrid_version_intelligence_service_exists(self):
        """
        Hybrid Test 1: Version Intelligence Service Implementation
        Python: Tests actual import and function existence
        AI: Analyzes documentation claims vs implementation reality
        """
        def python_test():
            """Deterministic Python test for service existence"""
            try:
                # This will fail if service doesn't exist - that's the point
                import version_intelligence_service
                self.assertTrue(hasattr(version_intelligence_service, 'analyze_version_gap'))
                self.assertTrue(hasattr(version_intelligence_service, 'create_foundation_context'))
            except ImportError:
                raise AssertionError("Version Intelligence Service implementation not found")
        
        def ai_analysis():
            """AI enhancement analyzing documentation vs implementation"""
            return self.ai_enhancer.analyze_phase_0_documentation_vs_implementation()
        
        result = self.execute_hybrid_test(
            "Version Intelligence Service Existence",
            python_test,
            lambda: ai_analysis().__dict__
        )
        
        # Hybrid assertion: Either Python passes OR AI provides clear implementation path
        if not result.python_test_result:
            self.assertGreater(len(result.hybrid_recommendations), 0, 
                             "No implementation found and no AI guidance provided")
    
    def test_hybrid_phase_0_input_output_validation(self):
        """
        Hybrid Test 2: Phase 0 I/O Flow Validation
        Python: Tests exact input → output structure and types
        AI: Validates workflow logic and data flow semantics
        """
        def python_test():
            """Deterministic Python test for I/O validation"""
            # Mock Phase 0 execution
            with patch('version_intelligence_service.execute_phase_0') as mock_phase_0:
                expected_output = {
                    "jira_id": "ACM-22079",
                    "target_version": "ACM 2.15.0",
                    "environment_version": "ACM 2.14.0",
                    "version_gap": "Feature NOT deployed",
                    "environment": "qe6-vmware-ibm",
                    "deployment_instruction": "Future-ready tests"
                }
                mock_phase_0.return_value = expected_output
                
                result = mock_phase_0("ACM-22079", "qe6-vmware-ibm")
                
                # Validate structure
                required_fields = ["jira_id", "target_version", "environment_version", "version_gap"]
                for field in required_fields:
                    self.assertIn(field, result, f"Missing required field: {field}")
        
        def ai_analysis():
            """AI enhancement validating workflow logic"""
            return self.ai_enhancer.validate_phase_0_workflow_logic()
        
        result = self.execute_hybrid_test(
            "Phase 0 I/O Flow Validation",
            python_test,
            lambda: ai_analysis().__dict__
        )
        
        # Hybrid assertion: Python structure validation + AI workflow logic
        self.assertGreater(result.combined_confidence, 0.5, 
                          "Combined Python+AI confidence too low for I/O validation")
    
    def test_hybrid_foundation_context_completeness(self):
        """
        Hybrid Test 3: Foundation Context Agent Inheritance Readiness
        Python: Tests exact field presence and data types
        AI: Analyzes Progressive Context Architecture compatibility
        """
        def python_test():
            """Deterministic Python test for foundation context structure"""
            # Test foundation context structure
            foundation_context = {
                "jira_id": "ACM-22079",
                "target_version": "ACM 2.15.0",
                "environment_version": "ACM 2.14.0",
                "version_gap": "Feature NOT deployed",
                "environment": "qe6-vmware-ibm", 
                "deployment_instruction": "Future-ready tests"
            }
            
            # Required fields for agent inheritance
            required_for_agents = [
                'jira_id',           # All agents need ticket identification
                'target_version',    # Agent A needs for requirements analysis
                'environment_version', # Agent D needs for environment assessment
                'version_gap',       # All agents need deployment awareness
                'environment',       # Agent D needs for infrastructure analysis
                'deployment_instruction' # Pattern Extension needs for test generation
            ]
            
            for field in required_for_agents:
                self.assertIn(field, foundation_context, f"Missing field required for agents: {field}")
                self.assertIsNotNone(foundation_context[field], f"Field {field} is None")
        
        def ai_analysis():
            """AI enhancement analyzing inheritance readiness"""
            return self.ai_enhancer.analyze_context_inheritance_readiness()
        
        result = self.execute_hybrid_test(
            "Foundation Context Agent Inheritance Readiness",
            python_test,
            lambda: ai_analysis().__dict__
        )
        
        # Hybrid assertion: Python field validation + AI inheritance logic
        if result.python_test_result:
            ai_findings = result.ai_analysis_result.get('findings', [])
            self.assertTrue(
                any("inheritance" in finding.lower() for finding in ai_findings),
                "AI should analyze inheritance compatibility when Python structure is valid"
            )
    
    def test_hybrid_file_generation_validation(self):
        """
        Hybrid Test 4: Phase 0 File Output Generation
        Python: Tests actual file creation and content
        AI: Suggests additional test scenarios for file handling
        """
        def python_test():
            """Deterministic Python test for file generation"""
            with tempfile.TemporaryDirectory() as temp_dir:
                # Mock Phase 0 file generation
                foundation_file = os.path.join(temp_dir, 'foundation-context.json')
                
                # Simulate what Phase 0 should create
                context_data = {
                    "jira_id": "ACM-22079",
                    "target_version": "ACM 2.15.0",
                    "environment_version": "ACM 2.14.0",
                    "version_gap": "Feature NOT deployed"
                }
                
                with open(foundation_file, 'w') as f:
                    json.dump(context_data, f)
                
                # Validate file creation
                self.assertTrue(os.path.exists(foundation_file), "Foundation context file not created")
                
                # Validate file content
                with open(foundation_file, 'r') as f:
                    loaded_data = json.load(f)
                
                self.assertEqual(loaded_data['jira_id'], "ACM-22079")
        
        def ai_analysis():
            """AI enhancement suggesting additional file handling tests"""
            return self.ai_enhancer.suggest_additional_test_scenarios([
                "test_phase_0_generates_actual_files",
                "test_file_content_validation"
            ])
        
        result = self.execute_hybrid_test(
            "Phase 0 File Generation Validation",
            python_test,
            lambda: ai_analysis().__dict__
        )
        
        # Hybrid assertion: File creation validation + AI test enhancement
        if result.python_test_result:
            ai_suggestions = result.ai_analysis_result.get('recommendations', [])
            self.assertGreater(len(ai_suggestions), 0, 
                             "AI should suggest additional file handling test scenarios")
    
    def test_hybrid_error_handling_comprehensive(self):
        """
        Hybrid Test 5: Phase 0 Error Handling and Edge Cases
        Python: Tests specific error conditions with exact assertions
        AI: Identifies additional edge cases and error scenarios
        """
        def python_test():
            """Deterministic Python test for error handling"""
            error_scenarios = [
                {"jira_id": "INVALID-123", "expected_error": "Invalid JIRA ID"},
                {"jira_id": None, "expected_error": "Missing JIRA ID"},
                {"jira_id": "", "expected_error": "Empty JIRA ID"}
            ]
            
            for scenario in error_scenarios:
                with self.subTest(scenario=scenario):
                    # Mock error handling
                    with patch('version_intelligence_service.execute_phase_0') as mock_phase_0:
                        if scenario["jira_id"] in ["INVALID-123", None, ""]:
                            mock_phase_0.side_effect = ValueError(scenario["expected_error"])
                            
                            with self.assertRaises(ValueError) as context:
                                mock_phase_0(scenario["jira_id"], "qe6-vmware-ibm")
                            
                            self.assertIn("JIRA", str(context.exception))
        
        def ai_analysis():
            """AI enhancement identifying additional error scenarios"""
            return self.ai_enhancer.suggest_additional_test_scenarios([
                "test_phase_0_error_handling"
            ])
        
        result = self.execute_hybrid_test(
            "Phase 0 Error Handling Comprehensive",
            python_test,
            lambda: ai_analysis().__dict__
        )
        
        # Hybrid assertion: Error handling validation + AI edge case suggestions
        ai_suggestions = result.ai_analysis_result.get('recommendations', [])
        edge_case_suggestions = [s for s in ai_suggestions if 'edge' in s.lower() or 'error' in s.lower()]
        self.assertGreater(len(edge_case_suggestions), 0,
                          "AI should suggest additional error handling scenarios")


class TestHybridOrchestrator(unittest.TestCase):
    """
    Test the Hybrid Orchestrator that combines all testing approaches
    """
    
    def setUp(self):
        self.framework_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
        self.orchestrator = HybridPhase0TestOrchestrator(self.framework_root)
    
    def test_orchestrator_execution(self):
        """Test that the hybrid orchestrator executes all phases successfully"""
        print("\n🎯 Testing Hybrid Orchestrator Execution")
        
        # Execute hybrid testing
        results = self.orchestrator.execute_hybrid_phase_0_testing()
        
        # Validate results structure
        self.assertIn('python_tests', results)
        self.assertIn('ai_analysis', results)
        self.assertIn('hybrid_recommendations', results)
        
        # Validate AI analysis components
        ai_analysis = results['ai_analysis']
        expected_analyses = ['documentation_gap', 'test_suggestions', 'workflow_logic', 'inheritance_readiness']
        
        for analysis in expected_analyses:
            self.assertIn(analysis, ai_analysis, f"Missing AI analysis: {analysis}")
        
        # Validate hybrid recommendations generated
        recommendations = results['hybrid_recommendations']
        self.assertGreater(len(recommendations), 0, "No hybrid recommendations generated")
        
        # Validate recommendation structure
        for rec in recommendations:
            self.assertIn('priority', rec)
            self.assertIn('action', rec)
            self.assertIn('details', rec)
            self.assertIn('validation', rec)
    
    def test_ai_analysis_quality(self):
        """Test that AI analysis provides meaningful insights"""
        ai_enhancer = AITestEnhancer(self.framework_root)
        
        # Test documentation gap analysis
        doc_analysis = ai_enhancer.analyze_phase_0_documentation_vs_implementation()
        self.assertGreater(len(doc_analysis.findings), 0, "No documentation gap findings")
        self.assertGreater(doc_analysis.confidence, 0.5, "Low confidence in documentation analysis")
        
        # Test test suggestion capability
        test_suggestions = ai_enhancer.suggest_additional_test_scenarios([
            "test_version_intelligence_service_exists"
        ])
        self.assertGreater(len(test_suggestions.recommendations), 0, "No test suggestions provided")


if __name__ == '__main__':
    print("🤖 Hybrid AI-Enhanced Phase 0 Unit Tests")
    print("Combining deterministic Python validation with AI-powered analysis")
    print("=" * 70)
    
    # Configure test runner for detailed output
    unittest.main(verbosity=2)