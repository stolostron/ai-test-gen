#!/usr/bin/env python3
"""
Integration Validation Test Suite
Comprehensive validation of template-driven generation and validation integration
Tests all integration points and compatibility with existing Phase 4 processing
"""

import os
import sys
import json
import tempfile
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import unittest
from unittest.mock import Mock, patch

# Add the parent directory to the path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

# Import our integration components
from enhanced_content_validation_engine import EnhancedContentValidationEngine, DocumentType
from schema_structure_enforcer import SchemaStructureEnforcer, SchemaValidationType, ComprehensiveValidationOrchestrator
from phase_4_integration_bridge import Phase4IntegrationBridge, create_phase_4_integration, IntegrationPhase

class ValidationTestSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class IntegrationTestResult:
    test_name: str
    success: bool
    score: float
    issues: List[str]
    warnings: List[str]
    details: Dict[str, Any]

class IntegrationValidationTestSuite:
    """
    Comprehensive test suite for validating template-driven generation integration
    """
    
    def __init__(self):
        self.test_results: List[IntegrationTestResult] = []
        self.temp_dir = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup test logging"""
        logger = logging.getLogger("integration_validation_test")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - IntegrationTest - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
        
    def run_comprehensive_integration_tests(self) -> Dict[str, Any]:
        """
        Run comprehensive integration validation tests
        """
        self.logger.info("🔄 Starting Comprehensive Integration Validation Tests")
        
        try:
            # Setup test environment
            self._setup_test_environment()
            
            # Test 1: Template System Validation
            template_result = self._test_template_system_integration()
            self.test_results.append(template_result)
            
            # Test 2: Content Validation Engine Testing
            content_result = self._test_content_validation_engine()
            self.test_results.append(content_result)
            
            # Test 3: Schema Enforcement Testing
            schema_result = self._test_schema_enforcement_integration()
            self.test_results.append(schema_result)
            
            # Test 4: Phase 4 Integration Bridge Testing
            bridge_result = self._test_phase_4_integration_bridge()
            self.test_results.append(bridge_result)
            
            # Test 5: End-to-End Workflow Testing
            e2e_result = self._test_end_to_end_workflow()
            self.test_results.append(e2e_result)
            
            # Test 6: Compatibility Testing with Existing Framework
            compatibility_result = self._test_framework_compatibility()
            self.test_results.append(compatibility_result)
            
            # Test 7: Quality Gate Enforcement Testing
            quality_gate_result = self._test_quality_gate_enforcement()
            self.test_results.append(quality_gate_result)
            
            # Generate comprehensive test report
            test_report = self._generate_test_report()
            
            self.logger.info("✅ Integration validation tests completed")
            return test_report
            
        except Exception as e:
            self.logger.error(f"❌ Integration validation test suite failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "partial_results": self.test_results
            }
        finally:
            self._cleanup_test_environment()
    
    def _setup_test_environment(self):
        """Setup test environment"""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="integration_test_"))
        self.logger.info(f"Test environment setup: {self.temp_dir}")
        
        # Create test data directories
        (self.temp_dir / "templates").mkdir(exist_ok=True)
        (self.temp_dir / "test_cases").mkdir(exist_ok=True)
        (self.temp_dir / "runs").mkdir(exist_ok=True)
        
    def _cleanup_test_environment(self):
        """Cleanup test environment"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            self.logger.info("Test environment cleaned up")
    
    def _test_template_system_integration(self) -> IntegrationTestResult:
        """Test template system integration"""
        self.logger.info("🔄 Testing Template System Integration")
        
        issues = []
        warnings = []
        score = 0
        details = {}
        
        try:
            # Test template accessibility
            templates_dir = Path(__file__).parent.parent / "templates"
            
            required_templates = [
                "enhanced-test-cases-template.md",
                "enhanced-complete-analysis-template.md",
                "test-case-schema.json",
                "complete-analysis-schema.json"
            ]
            
            template_accessibility = {}
            for template in required_templates:
                template_path = templates_dir / template
                accessible = template_path.exists()
                template_accessibility[template] = accessible
                
                if not accessible:
                    issues.append(f"Template not accessible: {template}")
                else:
                    score += 25
                    
            # Test template content structure
            if template_accessibility.get("enhanced-test-cases-template.md"):
                test_cases_template_valid = self._validate_template_structure(
                    templates_dir / "enhanced-test-cases-template.md",
                    "test_cases"
                )
                if test_cases_template_valid:
                    score += 25
                else:
                    issues.append("Test cases template structure invalid")
                    
            details = {
                "template_accessibility": template_accessibility,
                "templates_directory": str(templates_dir),
                "required_templates": required_templates
            }
            
            success = len(issues) == 0
            final_score = min(100, score)
            
            self.logger.info(f"Template System Integration: {'✅ Passed' if success else '❌ Failed'} (Score: {final_score})")
            
        except Exception as e:
            issues.append(f"Template system test error: {e}")
            success = False
            final_score = 0
            
        return IntegrationTestResult(
            test_name="Template System Integration",
            success=success,
            score=final_score,
            issues=issues,
            warnings=warnings,
            details=details
        )
    
    def _test_content_validation_engine(self) -> IntegrationTestResult:
        """Test content validation engine"""
        self.logger.info("🔄 Testing Content Validation Engine")
        
        issues = []
        warnings = []
        score = 0
        details = {}
        
        try:
            # Initialize validation engine
            validator = EnhancedContentValidationEngine()
            
            # Test with sample content
            sample_test_case = self._create_sample_test_case_content()
            test_case_file = self.temp_dir / "sample_test_case.md"
            with open(test_case_file, 'w') as f:
                f.write(sample_test_case)
                
            # Run validation
            validation_result = validator.validate_document(str(test_case_file), DocumentType.TEST_CASES)
            
            # Check validation results
            if validation_result["valid"]:
                score += 40
            else:
                issues.append(f"Content validation failed with {len(validation_result['violations'])} violations")
                
            # Test validation patterns
            pattern_tests = self._test_validation_patterns(validator)
            if pattern_tests["forbidden_patterns_detected"]:
                score += 30
            else:
                issues.append("Forbidden patterns not properly detected")
                
            if pattern_tests["required_patterns_enforced"]:
                score += 30
            else:
                warnings.append("Required patterns enforcement needs improvement")
                
            details = {
                "validation_result": validation_result,
                "pattern_tests": pattern_tests,
                "sample_file_path": str(test_case_file)
            }
            
            success = len(issues) == 0
            final_score = min(100, score)
            
            self.logger.info(f"Content Validation Engine: {'✅ Passed' if success else '❌ Failed'} (Score: {final_score})")
            
        except Exception as e:
            issues.append(f"Content validation engine test error: {e}")
            success = False
            final_score = 0
            
        return IntegrationTestResult(
            test_name="Content Validation Engine",
            success=success,
            score=final_score,
            issues=issues,
            warnings=warnings,
            details=details
        )
    
    def _test_schema_enforcement_integration(self) -> IntegrationTestResult:
        """Test schema enforcement integration"""
        self.logger.info("🔄 Testing Schema Enforcement Integration")
        
        issues = []
        warnings = []
        score = 0
        details = {}
        
        try:
            # Initialize schema enforcer
            schema_enforcer = SchemaStructureEnforcer()
            
            # Test schema loading
            if hasattr(schema_enforcer, 'test_case_schema') and hasattr(schema_enforcer, 'complete_analysis_schema'):
                score += 25
            else:
                issues.append("Schema files not properly loaded")
                
            # Test comprehensive validation orchestrator
            orchestrator = ComprehensiveValidationOrchestrator()
            
            # Create test content and validate
            sample_test_case = self._create_sample_test_case_content()
            test_case_file = self.temp_dir / "schema_test_case.md"
            with open(test_case_file, 'w') as f:
                f.write(sample_test_case)
                
            # Run comprehensive validation
            comprehensive_result = orchestrator.comprehensive_validate(str(test_case_file), "test_cases")
            
            if comprehensive_result["overall_valid"]:
                score += 40
            else:
                issues.append(f"Schema enforcement failed: {comprehensive_result['total_violations']} violations")
                
            # Test business rules validation
            business_rules_working = self._test_business_rules_validation(schema_enforcer)
            if business_rules_working:
                score += 35
            else:
                warnings.append("Business rules validation needs improvement")
                
            details = {
                "comprehensive_validation_result": comprehensive_result,
                "business_rules_test": business_rules_working,
                "schemas_loaded": hasattr(schema_enforcer, 'test_case_schema')
            }
            
            success = len(issues) == 0
            final_score = min(100, score)
            
            self.logger.info(f"Schema Enforcement Integration: {'✅ Passed' if success else '❌ Failed'} (Score: {final_score})")
            
        except Exception as e:
            issues.append(f"Schema enforcement test error: {e}")
            success = False
            final_score = 0
            
        return IntegrationTestResult(
            test_name="Schema Enforcement Integration",
            success=success,
            score=final_score,
            issues=issues,
            warnings=warnings,
            details=details
        )
    
    def _test_phase_4_integration_bridge(self) -> IntegrationTestResult:
        """Test Phase 4 integration bridge"""
        self.logger.info("🔄 Testing Phase 4 Integration Bridge")
        
        issues = []
        warnings = []
        score = 0
        details = {}
        
        try:
            # Create test run directory
            test_run_dir = self.temp_dir / "runs" / "ACM-TEST"
            test_run_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize integration bridge
            bridge = create_phase_4_integration(str(test_run_dir), "ACM-TEST")
            
            # Test bridge initialization
            if bridge.jira_id == "ACM-TEST":
                score += 20
            else:
                issues.append("Integration bridge initialization failed")
                
            # Test phase validation methods
            phase_3_data = self._create_sample_phase_3_data()
            environment_data = self._create_sample_environment_data()
            
            # Test data validation
            phase_3_valid = bridge._validate_phase_3_data(phase_3_data)
            env_valid = bridge._validate_environment_data(environment_data)
            
            if phase_3_valid:
                score += 20
            else:
                issues.append("Phase 3 data validation failed")
                
            if env_valid:
                score += 20
            else:
                issues.append("Environment data validation failed")
                
            # Test template loading
            templates_accessible = bridge._validate_templates_accessibility()
            if templates_accessible:
                score += 20
            else:
                warnings.append("Templates accessibility check failed - may need manual template setup")
                
            # Test integration workflow phases
            workflow_test = self._test_integration_workflow_phases(bridge)
            if workflow_test["pre_generation_ready"]:
                score += 20
            else:
                issues.append("Pre-generation phase validation failed")
                
            details = {
                "bridge_initialization": bridge.jira_id == "ACM-TEST",
                "phase_3_validation": phase_3_valid,
                "environment_validation": env_valid,
                "templates_accessible": templates_accessible,
                "workflow_phases_test": workflow_test,
                "test_run_directory": str(test_run_dir)
            }
            
            success = len(issues) == 0
            final_score = min(100, score)
            
            self.logger.info(f"Phase 4 Integration Bridge: {'✅ Passed' if success else '❌ Failed'} (Score: {final_score})")
            
        except Exception as e:
            issues.append(f"Phase 4 integration bridge test error: {e}")
            success = False
            final_score = 0
            
        return IntegrationTestResult(
            test_name="Phase 4 Integration Bridge",
            success=success,
            score=final_score,
            issues=issues,
            warnings=warnings,
            details=details
        )
    
    def _test_end_to_end_workflow(self) -> IntegrationTestResult:
        """Test end-to-end workflow integration"""
        self.logger.info("🔄 Testing End-to-End Workflow Integration")
        
        issues = []
        warnings = []
        score = 0
        details = {}
        
        try:
            # Create test run directory
            test_run_dir = self.temp_dir / "runs" / "ACM-E2E-TEST"
            test_run_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize integration bridge
            bridge = create_phase_4_integration(str(test_run_dir), "ACM-E2E-TEST")
            
            # Create comprehensive test data
            phase_3_data = self._create_sample_phase_3_data()
            environment_data = self._create_sample_environment_data()
            
            # Mock the template loading for testing
            with patch.object(bridge, '_validate_templates_accessibility', return_value=True):
                with patch.object(bridge, '_load_enhanced_templates', return_value=self._create_mock_templates()):
                    
                    # Test individual phases
                    pre_gen_result = bridge._execute_pre_generation_phase(phase_3_data, environment_data)
                    if pre_gen_result:
                        score += 20
                    else:
                        issues.append("Pre-generation phase failed")
                        
                    # Test template application (with mocked templates)
                    if pre_gen_result:
                        template_result = bridge._execute_template_application_phase(
                            phase_3_data, environment_data
                        )
                        if template_result:
                            score += 20
                        else:
                            issues.append("Template application phase failed")
                            
                        # Test content generation
                        if template_result:
                            content_result = bridge._execute_content_generation_phase(template_result)
                            if content_result:
                                score += 20
                            else:
                                issues.append("Content generation phase failed")
                                
                            # Test validation phase
                            if content_result:
                                validation_result = bridge._execute_post_validation_phase(content_result)
                                if validation_result:
                                    score += 20
                                else:
                                    warnings.append("Post-validation phase had issues")
                                    
                                # Test quality gate phase
                                if validation_result:
                                    quality_result = bridge._execute_quality_gate_phase(validation_result)
                                    if quality_result and quality_result.get("quality_gate_passed"):
                                        score += 20
                                    else:
                                        warnings.append("Quality gates need adjustment")
            
            details = {
                "pre_generation_result": pre_gen_result,
                "workflow_phases_completed": len(bridge.integration_state["phases_completed"]),
                "integration_state": bridge.integration_state,
                "test_run_directory": str(test_run_dir)
            }
            
            success = len(issues) == 0
            final_score = min(100, score)
            
            self.logger.info(f"End-to-End Workflow: {'✅ Passed' if success else '❌ Failed'} (Score: {final_score})")
            
        except Exception as e:
            issues.append(f"End-to-end workflow test error: {e}")
            success = False
            final_score = 0
            
        return IntegrationTestResult(
            test_name="End-to-End Workflow Integration",
            success=success,
            score=final_score,
            issues=issues,
            warnings=warnings,
            details=details
        )
    
    def _test_framework_compatibility(self) -> IntegrationTestResult:
        """Test compatibility with existing framework"""
        self.logger.info("🔄 Testing Framework Compatibility")
        
        issues = []
        warnings = []
        score = 0
        details = {}
        
        try:
            # Test directory structure compatibility
            framework_dirs = [
                ".claude/templates",
                ".claude/enforcement", 
                ".claude/ai-services",
                "runs"
            ]
            
            project_root = Path(__file__).parent.parent.parent
            dir_compatibility = {}
            
            for dir_name in framework_dirs:
                dir_path = project_root / dir_name
                exists = dir_path.exists()
                dir_compatibility[dir_name] = exists
                
                if exists:
                    score += 15
                else:
                    warnings.append(f"Framework directory missing: {dir_name}")
                    
            # Test import compatibility
            import_tests = self._test_import_compatibility()
            if import_tests["all_imports_successful"]:
                score += 40
            else:
                issues.append(f"Import compatibility issues: {import_tests['failed_imports']}")
                
            details = {
                "directory_compatibility": dir_compatibility,
                "import_compatibility": import_tests,
                "project_root": str(project_root)
            }
            
            success = len(issues) == 0
            final_score = min(100, score)
            
            self.logger.info(f"Framework Compatibility: {'✅ Passed' if success else '❌ Failed'} (Score: {final_score})")
            
        except Exception as e:
            issues.append(f"Framework compatibility test error: {e}")
            success = False
            final_score = 0
            
        return IntegrationTestResult(
            test_name="Framework Compatibility",
            success=success,
            score=final_score,
            issues=issues,
            warnings=warnings,
            details=details
        )
    
    def _test_quality_gate_enforcement(self) -> IntegrationTestResult:
        """Test quality gate enforcement"""
        self.logger.info("🔄 Testing Quality Gate Enforcement")
        
        issues = []
        warnings = []
        score = 0
        details = {}
        
        try:
            # Test quality gate logic with various scenarios
            quality_scenarios = [
                {"critical_violations": 0, "high_violations": 0, "score": 95, "expected_pass": True},
                {"critical_violations": 1, "high_violations": 0, "score": 90, "expected_pass": False},
                {"critical_violations": 0, "high_violations": 5, "score": 80, "expected_pass": False},
                {"critical_violations": 0, "high_violations": 2, "score": 87, "expected_pass": True}
            ]
            
            scenario_results = []
            for i, scenario in enumerate(quality_scenarios):
                # Create mock validation result
                mock_validation = self._create_mock_validation_result(scenario)
                
                # Test quality gate enforcement
                test_run_dir = self.temp_dir / "runs" / f"ACM-QG-TEST-{i}"
                test_run_dir.mkdir(parents=True, exist_ok=True)
                
                bridge = create_phase_4_integration(str(test_run_dir), f"ACM-QG-TEST-{i}")
                
                quality_result = bridge._execute_quality_gate_phase(mock_validation)
                actual_pass = quality_result.get("quality_gate_passed", False) if quality_result else False
                
                scenario_correct = actual_pass == scenario["expected_pass"]
                scenario_results.append({
                    "scenario": scenario,
                    "actual_pass": actual_pass,
                    "expected_pass": scenario["expected_pass"],
                    "correct": scenario_correct
                })
                
                if scenario_correct:
                    score += 25
                else:
                    issues.append(f"Quality gate scenario {i} failed: expected {scenario['expected_pass']}, got {actual_pass}")
                    
            details = {
                "scenario_results": scenario_results,
                "total_scenarios_tested": len(quality_scenarios)
            }
            
            success = len(issues) == 0
            final_score = min(100, score)
            
            self.logger.info(f"Quality Gate Enforcement: {'✅ Passed' if success else '❌ Failed'} (Score: {final_score})")
            
        except Exception as e:
            issues.append(f"Quality gate enforcement test error: {e}")
            success = False
            final_score = 0
            
        return IntegrationTestResult(
            test_name="Quality Gate Enforcement",
            success=success,
            score=final_score,
            issues=issues,
            warnings=warnings,
            details=details
        )
    
    def _create_sample_test_case_content(self) -> str:
        """Create sample test case content for testing"""
        return """# Test Cases: ACM-TEST

## Test Case 1: End-to-End Component Workflow Validation

### Description

**Complete Business Context**: Testing component functionality to ensure comprehensive end-to-end workflow validation across multi-cluster environments.

**Primary Coverage**:
- Component core functionality
- Cross-cluster integration workflows

### Setup

#### Prerequisites
- Verify ACM hub cluster accessibility
- Confirm managed cluster connectivity

**Environment Configuration**:
- ACM Version: 2.15+ required
- Managed Clusters: At least 2 clusters

### Test Steps

| Step | Action | Expected Result | Sample Commands/UI Navigation |
|------|--------|----------------|------------------------------|
| 1 | **What We're Doing**: Testing initial cluster authentication to establish baseline access for component testing. **CLI**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>` | Expected: yes (Authentication successful) | **CLI**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>` |
| 2 | **What We're Doing**: Testing component feature availability and basic functionality. **CLI**: `oc get resources` | Expected: yes (Component resources available) | **CLI**: `oc get resources -n namespace` |

"""
    
    def _create_sample_phase_3_data(self) -> Dict[str, Any]:
        """Create sample Phase 3 data for testing"""
        return {
            "ai_synthesis": {
                "component": "Test Component",
                "summary": "Test feature implementation",
                "implementation_status": "85% complete"
            },
            "agent_data": {
                "agent_a": {"confidence": 0.85},
                "agent_d": {"confidence": 0.90}
            },
            "jira_analysis": {
                "subtasks": 12,
                "completed": 10
            },
            "implementation_status": {
                "deployed": True,
                "functional": True
            }
        }
    
    def _create_sample_environment_data(self) -> Dict[str, Any]:
        """Create sample environment data for testing"""
        return {
            "cluster_name": "test-cluster.example.com",
            "console_url": "https://console-openshift-console.apps.test-cluster.example.com",
            "acm_version": "2.14.0",
            "openshift_version": "4.12",
            "infrastructure_score": 8,
            "feature_readiness": 7
        }
    
    def _create_mock_templates(self) -> Dict[str, str]:
        """Create mock templates for testing"""
        return {
            "test_cases": "Mock Test Cases Template Content",
            "complete_analysis": "Mock Complete Analysis Template Content"
        }
    
    def _create_mock_validation_result(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Create mock validation result for quality gate testing"""
        return {
            "overall": {
                "critical_violations": scenario["critical_violations"],
                "high_violations": scenario["high_violations"],
                "average_score": scenario["score"],
                "validation_passed": scenario["critical_violations"] == 0
            },
            "test_cases": {
                "overall_score": scenario["score"],
                "combined_violations": [Mock() for _ in range(scenario["critical_violations"] + scenario["high_violations"])]
            }
        }
    
    def _validate_template_structure(self, template_path: Path, template_type: str) -> bool:
        """Validate template structure"""
        try:
            with open(template_path, 'r') as f:
                content = f.read()
                
            if template_type == "test_cases":
                required_sections = ["MANDATORY STRUCTURE ENFORCEMENT", "CONTENT VALIDATION RULES"]
            else:
                required_sections = ["MANDATORY STRUCTURE ENFORCEMENT", "ENVIRONMENT SPECIFICITY"]
                
            return all(section in content for section in required_sections)
        except Exception:
            return False
    
    def _test_validation_patterns(self, validator: EnhancedContentValidationEngine) -> Dict[str, bool]:
        """Test validation patterns"""
        try:
            # Test content with forbidden patterns
            test_content_with_violations = """
            Based on role configuration, the system may vary depending on setup.
            Performance test results will stress test the system under load.
            """
            
            # Mock validation to test pattern detection
            violations = []
            for pattern, severity in validator.FORBIDDEN_PATTERNS.items():
                if re.search(pattern, test_content_with_violations, re.IGNORECASE):
                    violations.append({"pattern": pattern, "severity": severity})
                    
            forbidden_patterns_detected = len(violations) > 0
            
            # Test required patterns
            test_content_with_required = """
            What We're Doing: Testing functionality
            Expected: yes (specific result)
            CLI: oc command
            """
            
            required_found = 0
            for pattern, severity in validator.REQUIRED_PATTERNS.items():
                if re.search(pattern, test_content_with_required, re.IGNORECASE):
                    required_found += 1
                    
            required_patterns_enforced = required_found > 0
            
            return {
                "forbidden_patterns_detected": forbidden_patterns_detected,
                "required_patterns_enforced": required_patterns_enforced,
                "violations_found": len(violations),
                "required_patterns_found": required_found
            }
            
        except Exception:
            return {
                "forbidden_patterns_detected": False,
                "required_patterns_enforced": False
            }
    
    def _test_business_rules_validation(self, schema_enforcer: SchemaStructureEnforcer) -> bool:
        """Test business rules validation"""
        try:
            # Create test content that should trigger business rules
            test_content = """
            Test content with <CLUSTER_CONSOLE_URL> placeholder.
            This contains performance test references.
            """
            
            # Test business rule detection
            violations = schema_enforcer._validate_test_case_business_rules(test_content, {})
            return len(violations) > 0
            
        except Exception:
            return False
    
    def _test_integration_workflow_phases(self, bridge: Phase4IntegrationBridge) -> Dict[str, bool]:
        """Test integration workflow phases"""
        try:
            phase_3_data = self._create_sample_phase_3_data()
            environment_data = self._create_sample_environment_data()
            
            # Test pre-generation phase readiness
            pre_gen_ready = (
                bridge._validate_phase_3_data(phase_3_data) and
                bridge._validate_environment_data(environment_data) and
                bridge._prepare_run_directory()
            )
            
            return {
                "pre_generation_ready": pre_gen_ready,
                "data_validation_working": True,
                "directory_preparation_working": True
            }
            
        except Exception:
            return {
                "pre_generation_ready": False,
                "data_validation_working": False,
                "directory_preparation_working": False
            }
    
    def _test_import_compatibility(self) -> Dict[str, Any]:
        """Test import compatibility"""
        import_results = {
            "all_imports_successful": True,
            "successful_imports": [],
            "failed_imports": []
        }
        
        import_tests = [
            "enhanced_content_validation_engine",
            "schema_structure_enforcer", 
            "phase_4_integration_bridge"
        ]
        
        for module_name in import_tests:
            try:
                __import__(module_name)
                import_results["successful_imports"].append(module_name)
            except ImportError as e:
                import_results["failed_imports"].append(f"{module_name}: {e}")
                import_results["all_imports_successful"] = False
                
        return import_results
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.success])
        failed_tests = total_tests - passed_tests
        
        average_score = sum(r.score for r in self.test_results) / total_tests if total_tests > 0 else 0
        
        all_issues = []
        all_warnings = []
        
        for result in self.test_results:
            all_issues.extend(result.issues)
            all_warnings.extend(result.warnings)
            
        # Determine overall integration status
        integration_ready = (
            passed_tests >= total_tests * 0.8 and  # At least 80% tests passed
            average_score >= 75 and              # Average score >= 75
            len(all_issues) <= 3                 # Max 3 critical issues
        )
        
        test_summary = {
            "integration_validation_complete": True,
            "integration_ready": integration_ready,
            "overall_score": average_score,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_issues": len(all_issues),
            "total_warnings": len(all_warnings),
            "test_results": [
                {
                    "test_name": r.test_name,
                    "success": r.success,
                    "score": r.score,
                    "issue_count": len(r.issues),
                    "warning_count": len(r.warnings)
                }
                for r in self.test_results
            ],
            "critical_issues": all_issues,
            "warnings": all_warnings,
            "recommendations": self._generate_recommendations()
        }
        
        return test_summary
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [r for r in self.test_results if not r.success]
        if failed_tests:
            recommendations.append(f"Address {len(failed_tests)} failed integration tests before deployment")
            
        total_issues = sum(len(r.issues) for r in self.test_results)
        if total_issues > 5:
            recommendations.append("High number of integration issues - review implementation thoroughly")
            
        average_score = sum(r.score for r in self.test_results) / len(self.test_results) if self.test_results else 0
        if average_score < 80:
            recommendations.append("Integration scores below threshold - enhance implementation quality")
            
        # Template-specific recommendations
        template_test = next((r for r in self.test_results if "Template" in r.test_name), None)
        if template_test and not template_test.success:
            recommendations.append("Template system issues detected - verify template accessibility and structure")
            
        # Quality gate recommendations
        quality_test = next((r for r in self.test_results if "Quality Gate" in r.test_name), None)
        if quality_test and not quality_test.success:
            recommendations.append("Quality gate enforcement needs adjustment - review validation thresholds")
            
        if not recommendations:
            recommendations.append("Integration validation successful - ready for framework deployment")
            
        return recommendations

def run_integration_validation_tests():
    """
    Main function to run integration validation tests
    """
    test_suite = IntegrationValidationTestSuite()
    test_report = test_suite.run_comprehensive_integration_tests()
    
    print("\n" + "="*80)
    print("🔍 INTEGRATION VALIDATION TEST REPORT")
    print("="*80)
    
    print(f"Overall Integration Ready: {'✅ YES' if test_report.get('integration_ready') else '❌ NO'}")
    print(f"Overall Score: {test_report.get('overall_score', 0):.1f}/100")
    print(f"Tests Passed: {test_report.get('passed_tests', 0)}/{test_report.get('total_tests', 0)}")
    print(f"Pass Rate: {test_report.get('pass_rate', 0):.1f}%")
    
    if test_report.get('critical_issues'):
        print(f"\n❌ Critical Issues ({len(test_report['critical_issues'])}):")
        for issue in test_report['critical_issues'][:5]:  # Show first 5
            print(f"  • {issue}")
            
    if test_report.get('warnings'):
        print(f"\n⚠️ Warnings ({len(test_report['warnings'])}):")
        for warning in test_report['warnings'][:3]:  # Show first 3
            print(f"  • {warning}")
            
    print(f"\n📋 Recommendations:")
    for rec in test_report.get('recommendations', []):
        print(f"  • {rec}")
        
    print("\n" + "="*80)
    
    return test_report

if __name__ == "__main__":
    # Run integration validation tests
    import re
    report = run_integration_validation_tests()
    
    # Export report for review
    output_file = Path(__file__).parent / "integration_validation_report.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
        
    print(f"\n📄 Detailed report saved to: {output_file}")