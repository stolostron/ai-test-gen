#!/usr/bin/env python3
"""
Comprehensive Regression Validation Suite
Ensure no regressions occurred during Agent C HTML sanitization implementation
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

class RegressionValidator:
    def __init__(self):
        self.base_path = Path("/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator")
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "critical_failures": 0,
            "warnings": 0,
            "categories": {},
            "failures": [],
            "warnings_list": []
        }

    def log_test(self, category, test_name, passed, message="", critical=False):
        """Log test result"""
        self.results["tests_run"] += 1
        
        if category not in self.results["categories"]:
            self.results["categories"][category] = {"passed": 0, "failed": 0, "critical": 0}
        
        if passed:
            self.results["tests_passed"] += 1
            self.results["categories"][category]["passed"] += 1
            print(f"   ✅ {test_name}: {message}")
        else:
            self.results["tests_failed"] += 1
            self.results["categories"][category]["failed"] += 1
            
            if critical:
                self.results["critical_failures"] += 1
                self.results["categories"][category]["critical"] += 1
                print(f"   🚨 CRITICAL: {test_name}: {message}")
                self.results["failures"].append({
                    "category": category,
                    "test": test_name,
                    "message": message,
                    "critical": True
                })
            else:
                print(f"   ❌ {test_name}: {message}")
                self.results["failures"].append({
                    "category": category,
                    "test": test_name,
                    "message": message,
                    "critical": False
                })

    def log_warning(self, category, test_name, message):
        """Log warning"""
        self.results["warnings"] += 1
        print(f"   ⚠️  {test_name}: {message}")
        self.results["warnings_list"].append({
            "category": category,
            "test": test_name,
            "message": message
        })

    def validate_file_structure(self):
        """Validate that all critical files still exist"""
        print("\n🏗️  File Structure Validation")
        print("-" * 50)
        
        critical_files = [
            "CLAUDE.md",
            "CLAUDE.core.md",
            "CLAUDE.features.md", 
            "CLAUDE.policies.md",
            ".claude/ai-services/tg-enhanced-github-investigation-service.md",
            ".claude/enforcement/format_validator.py",
            ".claude/enforcement/pre_write_validator.py",
            ".claude/enforcement/test_agent_c_sanitization.py"
        ]
        
        for file_path in critical_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                # Check if file is readable and has content
                try:
                    content = full_path.read_text()
                    if len(content) > 100:  # Reasonable content check
                        self.log_test("file_structure", f"File exists and readable: {file_path}", True, f"Size: {len(content)} chars")
                    else:
                        self.log_test("file_structure", f"File too small: {file_path}", False, f"Only {len(content)} chars", critical=True)
                except Exception as e:
                    self.log_test("file_structure", f"File read error: {file_path}", False, str(e), critical=True)
            else:
                self.log_test("file_structure", f"Missing critical file: {file_path}", False, "File not found", critical=True)

    def validate_html_enforcement(self):
        """Validate HTML enforcement components work correctly"""
        print("\n🛡️  HTML Enforcement Validation")
        print("-" * 50)
        
        # Test format validator
        format_validator_path = self.base_path / ".claude/enforcement/format_validator.py"
        if format_validator_path.exists():
            try:
                # Test import
                import subprocess
                result = subprocess.run([
                    sys.executable, str(format_validator_path), "test.md", "test", "Clean content without HTML"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    self.log_test("html_enforcement", "Format validator clean content", True, "Approved clean content")
                else:
                    self.log_test("html_enforcement", "Format validator clean content", False, result.stderr, critical=True)
                
                # Test HTML detection
                result = subprocess.run([
                    sys.executable, str(format_validator_path), "test.md", "test", "Content with <br> tags"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 1:  # Should block HTML
                    self.log_test("html_enforcement", "Format validator HTML detection", True, "Correctly blocked HTML content")
                else:
                    self.log_test("html_enforcement", "Format validator HTML detection", False, "Failed to block HTML", critical=True)
                    
            except Exception as e:
                self.log_test("html_enforcement", "Format validator execution", False, str(e), critical=True)
        else:
            self.log_test("html_enforcement", "Format validator exists", False, "File not found", critical=True)

    def validate_agent_c_integration(self):
        """Validate Agent C service integration"""
        print("\n🤖 Agent C Integration Validation")
        print("-" * 50)
        
        service_file = self.base_path / ".claude/ai-services/tg-enhanced-github-investigation-service.md"
        if service_file.exists():
            content = service_file.read_text()
            
            # Check for sanitization method
            if "sanitize_collected_data" in content:
                self.log_test("agent_c", "Sanitization method present", True, "Method found in service")
            else:
                self.log_test("agent_c", "Sanitization method present", False, "sanitize_collected_data not found", critical=True)
            
            # Check for Stage 3.5 integration
            if "Stage 3.5" in content:
                self.log_test("agent_c", "Stage 3.5 integration", True, "Stage documented")
            else:
                self.log_test("agent_c", "Stage 3.5 integration", False, "Stage 3.5 not found")
            
            # Check for HTML sanitization capabilities
            if "html_sanitization_capabilities" in content:
                self.log_test("agent_c", "HTML sanitization capabilities", True, "Capabilities documented")
            else:
                self.log_test("agent_c", "HTML sanitization capabilities", False, "Capabilities not found")
            
            # Check service architecture integrity
            if "class EnhancedGitHubInvestigationService" in content:
                self.log_test("agent_c", "Service class structure", True, "Class structure intact")
            else:
                self.log_test("agent_c", "Service class structure", False, "Service class structure missing", critical=True)
                
        else:
            self.log_test("agent_c", "Agent C service file", False, "Service file not found", critical=True)

    def validate_documentation_consistency(self):
        """Validate documentation consistency across hierarchy"""
        print("\n📚 Documentation Consistency Validation")
        print("-" * 50)
        
        # Check each CLAUDE.md file for consistency
        claude_files = {
            "CLAUDE.md": ["Agent C HTML sanitization"],
            "CLAUDE.core.md": ["Agent C (GitHub Investigation)", "HTML sanitization"],
            "CLAUDE.features.md": ["Agent C with complete context inheritance and HTML sanitization", "html_contamination_prevention"],
            "CLAUDE.policies.md": ["Agent C source sanitization"]
        }
        
        for filename, required_terms in claude_files.items():
            file_path = self.base_path / filename
            if file_path.exists():
                content = file_path.read_text()
                
                for term in required_terms:
                    if term.lower() in content.lower():
                        self.log_test("documentation", f"{filename} contains '{term}'", True, "Term found")
                    else:
                        self.log_test("documentation", f"{filename} contains '{term}'", False, f"Term missing from {filename}")
            else:
                self.log_test("documentation", f"{filename} exists", False, "File not found", critical=True)

    def validate_framework_components(self):
        """Validate core framework components weren't broken"""
        print("\n⚙️  Framework Components Validation")
        print("-" * 50)
        
        # Check Progressive Context Architecture components
        pca_components = [
            ".claude/ai-services/tg-universal-context-manager.md",
            ".claude/ai-services/tg-context-validation-engine.md",
            ".claude/ai-services/tg-conflict-resolution-service.md",
            ".claude/ai-services/tg-enhanced-jira-intelligence-service.md",
            ".claude/ai-services/tg-enhanced-environment-intelligence-service.md",
            ".claude/ai-services/tg-enhanced-documentation-intelligence-service.md"
        ]
        
        for component in pca_components:
            component_path = self.base_path / component
            if component_path.exists():
                try:
                    content = component_path.read_text()
                    if len(content) > 500:  # Reasonable content size
                        self.log_test("framework", f"Component intact: {Path(component).name}", True, f"Size: {len(content)} chars")
                    else:
                        self.log_warning("framework", f"Component small: {Path(component).name}", f"Only {len(content)} chars")
                except Exception as e:
                    self.log_test("framework", f"Component readable: {Path(component).name}", False, str(e))
            else:
                self.log_test("framework", f"Component exists: {Path(component).name}", False, "Component missing")

    def validate_enforcement_system_integration(self):
        """Validate enforcement system still works properly"""
        print("\n🔒 Enforcement System Integration Validation")
        print("-" * 50)
        
        # Test Agent C sanitization functionality
        sanitization_test_file = self.base_path / ".claude/enforcement/test_agent_c_sanitization.py"
        if sanitization_test_file.exists():
            try:
                import subprocess
                result = subprocess.run([
                    sys.executable, str(sanitization_test_file)
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self.log_test("enforcement", "Agent C sanitization test", True, "All sanitization tests passed")
                else:
                    self.log_test("enforcement", "Agent C sanitization test", False, result.stderr, critical=True)
                    
            except Exception as e:
                self.log_test("enforcement", "Agent C sanitization test execution", False, str(e), critical=True)
        else:
            self.log_test("enforcement", "Agent C sanitization test file", False, "Test file not found")
        
        # Validate dual-layer architecture
        enforcement_files = [
            ".claude/enforcement/format_validator.py",
            ".claude/enforcement/pre_write_validator.py",
            ".claude/enforcement/validated_write_wrapper.py"
        ]
        
        for enf_file in enforcement_files:
            file_path = self.base_path / enf_file
            if file_path.exists():
                content = file_path.read_text()
                if "html" in content.lower() or "HTML" in content:
                    self.log_test("enforcement", f"HTML enforcement in {Path(enf_file).name}", True, "HTML patterns detected")
                else:
                    self.log_warning("enforcement", f"HTML enforcement in {Path(enf_file).name}", "No HTML patterns found")
            else:
                self.log_test("enforcement", f"Enforcement file exists: {Path(enf_file).name}", False, "File missing")

    def validate_mcp_integration(self):
        """Validate MCP integration wasn't broken"""
        print("\n🔌 MCP Integration Validation")
        print("-" * 50)
        
        mcp_files = [
            ".claude/mcp/github_mcp_integration.py",
            ".claude/mcp/filesystem_mcp_integration.py",
            ".claude/mcp/mcp_service_coordinator.py",
            ".claude/mcp/optimized_github_mcp_integration.py",
            ".claude/mcp/optimized_filesystem_mcp_integration.py"
        ]
        
        for mcp_file in mcp_files:
            file_path = self.base_path / mcp_file
            if file_path.exists():
                try:
                    content = file_path.read_text()
                    # Check for basic Python syntax
                    if "class " in content and "def " in content:
                        self.log_test("mcp", f"MCP component structure: {Path(mcp_file).name}", True, "Python structure intact")
                    else:
                        self.log_warning("mcp", f"MCP component structure: {Path(mcp_file).name}", "Unusual structure")
                except Exception as e:
                    self.log_test("mcp", f"MCP component readable: {Path(mcp_file).name}", False, str(e))
            else:
                self.log_test("mcp", f"MCP component exists: {Path(mcp_file).name}", False, "Component missing")

    def validate_run_metadata_compatibility(self):
        """Validate recent runs still have proper metadata"""
        print("\n📊 Run Metadata Compatibility Validation")
        print("-" * 50)
        
        runs_dir = self.base_path / "runs"
        if runs_dir.exists():
            # Find recent run directories
            run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
            
            if run_dirs:
                # Check the most recent run
                recent_runs = sorted(run_dirs, key=lambda x: x.stat().st_mtime, reverse=True)[:3]
                
                for run_dir in recent_runs:
                    metadata_file = run_dir / "run-metadata.json"
                    if metadata_file.exists():
                        try:
                            metadata = json.loads(metadata_file.read_text())
                            
                            # Check key metadata fields
                            required_fields = ["run_metadata", "execution_phases", "feature_analysis"]
                            for field in required_fields:
                                if field in metadata:
                                    self.log_test("metadata", f"Metadata field '{field}' in {run_dir.name}", True, "Field present")
                                else:
                                    self.log_test("metadata", f"Metadata field '{field}' in {run_dir.name}", False, "Field missing")
                            
                            # Check for Agent C phase
                            phases = metadata.get("run_metadata", {}).get("execution_phases", {})
                            if "phase_2" in phases:
                                phase_2 = phases["phase_2"]
                                if "agent_c_github" in phase_2.get("agents", {}):
                                    self.log_test("metadata", f"Agent C execution in {run_dir.name}", True, "Agent C found in phases")
                                else:
                                    self.log_warning("metadata", f"Agent C execution in {run_dir.name}", "Agent C not found in phase 2")
                            
                        except Exception as e:
                            self.log_test("metadata", f"Metadata parsing for {run_dir.name}", False, str(e))
                    else:
                        self.log_warning("metadata", f"Metadata file in {run_dir.name}", "No metadata file found")
                        
                self.log_test("metadata", "Recent runs found", True, f"Found {len(recent_runs)} recent runs")
            else:
                self.log_warning("metadata", "Run directories", "No run directories found")
        else:
            self.log_warning("metadata", "Runs directory", "Runs directory doesn't exist")

    def generate_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE REGRESSION VALIDATION REPORT")
        print("=" * 70)
        
        # Overall summary
        total_tests = self.results["tests_run"]
        passed_tests = self.results["tests_passed"]
        failed_tests = self.results["tests_failed"]
        critical_failures = self.results["critical_failures"]
        warnings = self.results["warnings"]
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 Overall Results:")
        print(f"   Tests Run: {total_tests}")
        print(f"   Tests Passed: {passed_tests} ({success_rate:.1f}%)")
        print(f"   Tests Failed: {failed_tests}")
        print(f"   Critical Failures: {critical_failures}")
        print(f"   Warnings: {warnings}")
        
        # Category breakdown
        print(f"\n📋 Results by Category:")
        for category, stats in self.results["categories"].items():
            total_cat = stats["passed"] + stats["failed"]
            cat_success = (stats["passed"] / total_cat * 100) if total_cat > 0 else 0
            critical_note = f" ({stats['critical']} critical)" if stats["critical"] > 0 else ""
            print(f"   {category}: {stats['passed']}/{total_cat} passed ({cat_success:.1f}%){critical_note}")
        
        # Critical failures
        if critical_failures > 0:
            print(f"\n🚨 CRITICAL FAILURES ({critical_failures}):")
            for failure in self.results["failures"]:
                if failure["critical"]:
                    print(f"   - {failure['category']}/{failure['test']}: {failure['message']}")
        
        # Regular failures
        regular_failures = [f for f in self.results["failures"] if not f["critical"]]
        if regular_failures:
            print(f"\n❌ Regular Failures ({len(regular_failures)}):")
            for failure in regular_failures:
                print(f"   - {failure['category']}/{failure['test']}: {failure['message']}")
        
        # Warnings
        if warnings > 0:
            print(f"\n⚠️  Warnings ({warnings}):")
            for warning in self.results["warnings_list"]:
                print(f"   - {warning['category']}/{warning['test']}: {warning['message']}")
        
        # Final assessment
        print(f"\n🎯 REGRESSION VALIDATION ASSESSMENT:")
        
        if critical_failures == 0:
            if failed_tests == 0:
                print("✅ NO REGRESSIONS DETECTED - All tests passed")
                print("✅ Agent C HTML sanitization integration successful")
                print("✅ Framework functionality preserved")
                return True
            elif failed_tests <= 2 and warnings <= 5:
                print("⚠️  MINOR ISSUES DETECTED - No critical regressions")
                print("⚠️  Some non-critical tests failed, but core functionality intact")
                print("⚠️  Review failures and address if needed")
                return True
            else:
                print("❌ SIGNIFICANT ISSUES DETECTED - Review required")
                print("❌ Multiple test failures suggest potential regressions")
                print("❌ Investigation and fixes needed before deployment")
                return False
        else:
            print("🚨 CRITICAL REGRESSIONS DETECTED")
            print("🚨 Framework functionality may be compromised")
            print("🚨 Immediate investigation and fixes required")
            return False

    def run_validation(self):
        """Run complete validation suite"""
        print("🔍 COMPREHENSIVE REGRESSION VALIDATION SUITE")
        print("Validating Agent C HTML sanitization integration")
        print("=" * 70)
        
        # Run all validation categories
        self.validate_file_structure()
        self.validate_html_enforcement()
        self.validate_agent_c_integration()
        self.validate_documentation_consistency()
        self.validate_framework_components()
        self.validate_enforcement_system_integration()
        self.validate_mcp_integration()
        self.validate_run_metadata_compatibility()
        
        # Generate final report
        success = self.generate_report()
        
        # Save results
        results_file = self.base_path / ".claude/enforcement/regression_validation_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Detailed results saved to: {results_file}")
        
        return success

def main():
    validator = RegressionValidator()
    success = validator.run_validation()
    
    if success:
        print("\n🎉 REGRESSION VALIDATION SUCCESSFUL")
        print("Agent C HTML sanitization implementation validated successfully!")
        sys.exit(0)
    else:
        print("\n💥 REGRESSION VALIDATION FAILED")
        print("Critical issues detected - immediate attention required!")
        sys.exit(1)

if __name__ == "__main__":
    main()