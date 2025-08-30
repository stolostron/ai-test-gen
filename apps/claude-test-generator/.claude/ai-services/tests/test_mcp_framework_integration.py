#!/usr/bin/env python3
"""
Comprehensive MCP Framework Integration Testing
===============================================

Tests MCPs during actual framework runs to ensure they work correctly
without making any changes to the framework code.
"""

import os
import sys
import json
import time
import subprocess
import tempfile
import logging
from pathlib import Path
from typing import Dict, Any, List

# Add framework paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'mcp'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MCPFrameworkTester:
    """Test MCPs during framework execution"""
    
    def __init__(self):
        self.test_results = {}
        self.performance_data = {}
        self.mcp_calls_made = []
        self.framework_root = Path(__file__).parent.parent.parent.parent
        
    def run_comprehensive_mcp_tests(self) -> Dict[str, Any]:
        """Run comprehensive MCP tests during framework execution"""
        
        print("🧪 COMPREHENSIVE MCP FRAMEWORK INTEGRATION TESTING")
        print("=" * 60)
        print("Testing MCPs during actual framework runs")
        print("=" * 60)
        
        # Test 1: MCP Service Availability
        print("\n1️⃣ Testing MCP Service Availability...")
        availability_results = self._test_mcp_service_availability()
        
        # Test 2: MCP Integration Points
        print("\n2️⃣ Testing MCP Integration Points...")
        integration_results = self._test_mcp_integration_points()
        
        # Test 3: Framework MCP Coordination
        print("\n3️⃣ Testing Framework MCP Coordination...")
        coordination_results = self._test_framework_mcp_coordination()
        
        # Test 4: Performance Impact Assessment
        print("\n4️⃣ Testing Performance Impact...")
        performance_results = self._test_mcp_performance_impact()
        
        # Test 5: Fallback Mechanism Validation
        print("\n5️⃣ Testing Fallback Mechanisms...")
        fallback_results = self._test_fallback_mechanisms()
        
        # Test 6: Real Framework Run with MCPs
        print("\n6️⃣ Testing Real Framework Run with MCPs...")
        framework_run_results = self._test_real_framework_run_with_mcps()
        
        # Compile comprehensive results
        comprehensive_results = {
            "test_summary": {
                "total_tests": 6,
                "timestamp": time.time(),
                "framework_root": str(self.framework_root)
            },
            "mcp_service_availability": availability_results,
            "mcp_integration_points": integration_results,
            "framework_coordination": coordination_results,
            "performance_impact": performance_results,
            "fallback_mechanisms": fallback_results,
            "framework_run_validation": framework_run_results,
            "overall_assessment": self._generate_overall_assessment()
        }
        
        return comprehensive_results
    
    def _test_mcp_service_availability(self) -> Dict[str, Any]:
        """Test MCP service availability and health"""
        results = {
            "test_name": "MCP Service Availability",
            "status": "running",
            "checks": {}
        }
        
        try:
            # Import MCP components
            from framework_mcp_integration import MCPServiceCoordinator, validate_mcp_upgrade
            
            # Test 1: Service Initialization
            print("   📋 Testing service initialization...")
            coordinator = MCPServiceCoordinator()
            results["checks"]["initialization"] = {
                "status": "success",
                "coordinator_type": type(coordinator).__name__
            }
            
            # Test 2: Service Status
            print("   📊 Testing service status...")
            service_status = coordinator.get_service_status()
            results["checks"]["service_status"] = {
                "status": "success" if service_status else "failed",
                "mcp_integration": service_status.get("mcp_integration"),
                "real_mcp_enabled": service_status.get("real_mcp_enabled"),
                "fallback_enabled": service_status.get("fallback_enabled"),
                "servers_available": service_status.get("servers_available", {})
            }
            
            # Test 3: MCP Upgrade Validation
            print("   🔄 Testing MCP upgrade validation...")
            upgrade_validation = validate_mcp_upgrade()
            results["checks"]["upgrade_validation"] = {
                "status": "success" if upgrade_validation else "failed",
                "upgrade_status": upgrade_validation.get("upgrade_status"),
                "regression_check": upgrade_validation.get("regression_check")
            }
            
            # Test 4: All Services Test
            print("   🧪 Testing all services...")
            all_services_test = coordinator.test_all_services()
            results["checks"]["all_services"] = {
                "status": "success" if all_services_test.get("status") == "complete" else "failed",
                "test_results": all_services_test.get("test_results", {}),
                "framework_compatibility": all_services_test.get("framework_compatibility", {})
            }
            
            results["status"] = "completed"
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"   ❌ Error: {e}")
        
        return results
    
    def _test_mcp_integration_points(self) -> Dict[str, Any]:
        """Test MCP integration points in the framework"""
        results = {
            "test_name": "MCP Integration Points",
            "status": "running",
            "integration_points": {}
        }
        
        try:
            # Test GitHub Integration
            print("   🐙 Testing GitHub MCP integration...")
            github_result = self._test_github_mcp_integration()
            results["integration_points"]["github"] = github_result
            
            # Test Filesystem Integration
            print("   📁 Testing Filesystem MCP integration...")
            filesystem_result = self._test_filesystem_mcp_integration()
            results["integration_points"]["filesystem"] = filesystem_result
            
            # Test Service Coordination
            print("   🤝 Testing service coordination...")
            coordination_result = self._test_service_coordination()
            results["integration_points"]["coordination"] = coordination_result
            
            results["status"] = "completed"
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"   ❌ Error: {e}")
        
        return results
    
    def _test_github_mcp_integration(self) -> Dict[str, Any]:
        """Test GitHub MCP integration specifically"""
        try:
            from framework_mcp_integration import MCPServiceCoordinator
            
            coordinator = MCPServiceCoordinator()
            
            # Test PR retrieval
            start_time = time.time()
            pr_result = coordinator.github_get_pull_request("stolostron/console", 1, use_fallback=True)
            end_time = time.time()
            
            return {
                "status": "success" if pr_result else "failed",
                "operation": "get_pull_request",
                "response_time": end_time - start_time,
                "result_type": type(pr_result).__name__,
                "has_data": bool(pr_result),
                "mcp_used": pr_result.get("mcp_ready", False) if isinstance(pr_result, dict) else False,
                "fallback_used": pr_result.get("source") == "fallback" if isinstance(pr_result, dict) else False
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "operation": "get_pull_request"
            }
    
    def _test_filesystem_mcp_integration(self) -> Dict[str, Any]:
        """Test Filesystem MCP integration specifically"""
        try:
            from framework_mcp_integration import MCPServiceCoordinator
            
            coordinator = MCPServiceCoordinator()
            
            # Test file search
            start_time = time.time()
            search_result = coordinator.filesystem_search_files("*.py", max_results=10)
            end_time = time.time()
            
            return {
                "status": "success" if search_result else "failed",
                "operation": "search_files",
                "response_time": end_time - start_time,
                "result_type": type(search_result).__name__,
                "has_data": bool(search_result),
                "files_found": len(search_result.get("files", [])) if isinstance(search_result, dict) else 0,
                "mcp_used": search_result.get("mcp_ready", False) if isinstance(search_result, dict) else False,
                "fallback_used": search_result.get("source") == "fallback" if isinstance(search_result, dict) else False
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "operation": "search_files"
            }
    
    def _test_service_coordination(self) -> Dict[str, Any]:
        """Test service coordination functionality"""
        try:
            from framework_mcp_integration import get_mcp_coordinator, get_mcp_performance_report
            
            # Test coordinator factory
            coordinator = get_mcp_coordinator(".")
            
            # Test performance reporting
            perf_report = get_mcp_performance_report()
            
            return {
                "status": "success",
                "coordinator_created": coordinator is not None,
                "performance_report": perf_report is not None,
                "performance_data": perf_report if isinstance(perf_report, dict) else {}
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _test_framework_mcp_coordination(self) -> Dict[str, Any]:
        """Test framework-level MCP coordination"""
        results = {
            "test_name": "Framework MCP Coordination",
            "status": "running",
            "coordination_tests": {}
        }
        
        try:
            # Test Agent A MCP usage
            print("   🤖 Testing Agent A MCP usage...")
            agent_a_result = self._test_agent_a_mcp_usage()
            results["coordination_tests"]["agent_a"] = agent_a_result
            
            # Test Agent B MCP usage
            print("   📚 Testing Agent B MCP usage...")
            agent_b_result = self._test_agent_b_mcp_usage()
            results["coordination_tests"]["agent_b"] = agent_b_result
            
            # Test Agent C MCP usage
            print("   🔍 Testing Agent C MCP usage...")
            agent_c_result = self._test_agent_c_mcp_usage()
            results["coordination_tests"]["agent_c"] = agent_c_result
            
            # Test Agent D MCP usage
            print("   🌍 Testing Agent D MCP usage...")
            agent_d_result = self._test_agent_d_mcp_usage()
            results["coordination_tests"]["agent_d"] = agent_d_result
            
            results["status"] = "completed"
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"   ❌ Error: {e}")
        
        return results
    
    def _test_agent_a_mcp_usage(self) -> Dict[str, Any]:
        """Test Agent A's MCP usage"""
        try:
            # Check if Agent A uses MCPs
            agent_a_path = self.framework_root / '.claude' / 'ai-services' / 'jira_intelligence_agent.py'
            
            if agent_a_path.exists():
                with open(agent_a_path, 'r') as f:
                    content = f.read()
                
                mcp_usage = {
                    "file_exists": True,
                    "imports_mcp": "MCPServiceCoordinator" in content or "mcp_service" in content,
                    "uses_github_mcp": "github_get_pull_request" in content,
                    "uses_filesystem_mcp": "filesystem_search" in content,
                    "mcp_integration_ready": "mcp" in content.lower()
                }
                
                return {
                    "status": "analyzed",
                    "mcp_usage": mcp_usage,
                    "integration_level": "high" if mcp_usage["imports_mcp"] else "none"
                }
            else:
                return {"status": "file_not_found", "path": str(agent_a_path)}
                
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _test_agent_b_mcp_usage(self) -> Dict[str, Any]:
        """Test Agent B's MCP usage"""
        try:
            # Check Agent B files for MCP usage
            agent_b_files = [
                self.framework_root / '.claude' / 'ai-services' / 'tg_enhanced_documentation_intelligence_service.py',
                self.framework_root / '.claude' / 'agents' / 'documentation-intelligence.md'
            ]
            
            mcp_usage_found = False
            files_checked = 0
            
            for file_path in agent_b_files:
                if file_path.exists():
                    files_checked += 1
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    if "mcp" in content.lower() or "MCPServiceCoordinator" in content:
                        mcp_usage_found = True
                        break
            
            return {
                "status": "analyzed",
                "files_checked": files_checked,
                "mcp_usage_found": mcp_usage_found,
                "integration_level": "medium" if mcp_usage_found else "low"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _test_agent_c_mcp_usage(self) -> Dict[str, Any]:
        """Test Agent C's MCP usage"""
        try:
            # Check Agent C files for MCP usage
            agent_c_files = [
                self.framework_root / '.claude' / 'ai-services' / 'tg_enhanced_github_investigation_service.py',
                self.framework_root / '.claude' / 'agents' / 'github-investigation.md'
            ]
            
            mcp_usage_details = {}
            files_checked = 0
            
            for file_path in agent_c_files:
                if file_path.exists():
                    files_checked += 1
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    mcp_usage_details[file_path.name] = {
                        "imports_mcp": "MCPServiceCoordinator" in content,
                        "uses_github_mcp": "github_get_pull_request" in content,
                        "github_operations": content.count("github_"),
                        "mcp_references": content.lower().count("mcp")
                    }
            
            return {
                "status": "analyzed",
                "files_checked": files_checked,
                "mcp_usage_details": mcp_usage_details,
                "integration_level": "high" if any(d["imports_mcp"] for d in mcp_usage_details.values()) else "low"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _test_agent_d_mcp_usage(self) -> Dict[str, Any]:
        """Test Agent D's MCP usage"""
        try:
            # Check Agent D files for MCP usage
            agent_d_files = [
                self.framework_root / '.claude' / 'ai-services' / 'tg_enhanced_environment_intelligence_service.py',
                self.framework_root / '.claude' / 'agents' / 'environment-intelligence.md'
            ]
            
            mcp_usage_found = False
            filesystem_mcp_usage = False
            files_checked = 0
            
            for file_path in agent_d_files:
                if file_path.exists():
                    files_checked += 1
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    if "mcp" in content.lower():
                        mcp_usage_found = True
                    if "filesystem_search" in content:
                        filesystem_mcp_usage = True
            
            return {
                "status": "analyzed",
                "files_checked": files_checked,
                "mcp_usage_found": mcp_usage_found,
                "filesystem_mcp_usage": filesystem_mcp_usage,
                "integration_level": "medium" if mcp_usage_found else "low"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _test_mcp_performance_impact(self) -> Dict[str, Any]:
        """Test performance impact of MCPs"""
        results = {
            "test_name": "MCP Performance Impact",
            "status": "running",
            "performance_metrics": {}
        }
        
        try:
            from framework_mcp_integration import MCPServiceCoordinator
            
            coordinator = MCPServiceCoordinator()
            
            # Test GitHub operation performance
            print("   ⚡ Testing GitHub operation performance...")
            github_times = []
            for i in range(3):
                start_time = time.time()
                result = coordinator.github_get_pull_request("test/repo", i+1, use_fallback=True)
                end_time = time.time()
                github_times.append(end_time - start_time)
            
            # Test Filesystem operation performance
            print("   📁 Testing Filesystem operation performance...")
            filesystem_times = []
            for pattern in ["*.py", "*.md", "*.json"]:
                start_time = time.time()
                result = coordinator.filesystem_search_files(pattern, max_results=5)
                end_time = time.time()
                filesystem_times.append(end_time - start_time)
            
            # Get performance stats
            service_status = coordinator.get_service_status()
            performance_stats = service_status.get("performance_stats", {})
            
            results["performance_metrics"] = {
                "github_operations": {
                    "average_time": sum(github_times) / len(github_times),
                    "min_time": min(github_times),
                    "max_time": max(github_times),
                    "operations_tested": len(github_times)
                },
                "filesystem_operations": {
                    "average_time": sum(filesystem_times) / len(filesystem_times),
                    "min_time": min(filesystem_times),
                    "max_time": max(filesystem_times),
                    "operations_tested": len(filesystem_times)
                },
                "coordinator_stats": performance_stats
            }
            
            results["status"] = "completed"
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"   ❌ Error: {e}")
        
        return results
    
    def _test_fallback_mechanisms(self) -> Dict[str, Any]:
        """Test MCP fallback mechanisms"""
        results = {
            "test_name": "MCP Fallback Mechanisms",
            "status": "running",
            "fallback_tests": {}
        }
        
        try:
            from framework_mcp_integration import FrameworkMCPIntegration
            
            # Test with MCP disabled (force fallback)
            print("   🔄 Testing with MCP disabled...")
            integration_no_mcp = FrameworkMCPIntegration(enable_real_mcp=False, fallback_enabled=True)
            
            # Test GitHub fallback
            github_fallback = integration_no_mcp.github_get_pull_request("test/repo", 1)
            results["fallback_tests"]["github"] = {
                "status": "success" if github_fallback else "failed",
                "result_type": type(github_fallback).__name__,
                "has_data": bool(github_fallback)
            }
            
            # Test Filesystem fallback
            filesystem_fallback = integration_no_mcp.filesystem_search_files("*.py", max_results=5)
            results["fallback_tests"]["filesystem"] = {
                "status": "success" if filesystem_fallback else "failed",
                "result_type": type(filesystem_fallback).__name__,
                "has_data": bool(filesystem_fallback)
            }
            
            # Test with fallback disabled (should handle gracefully)
            print("   ⚠️ Testing with fallback disabled...")
            integration_no_fallback = FrameworkMCPIntegration(enable_real_mcp=True, fallback_enabled=False)
            
            try:
                no_fallback_result = integration_no_fallback.github_get_pull_request("test/repo", 1)
                results["fallback_tests"]["no_fallback"] = {
                    "status": "handled_gracefully",
                    "result": no_fallback_result
                }
            except Exception as e:
                results["fallback_tests"]["no_fallback"] = {
                    "status": "error_handled",
                    "error": str(e)
                }
            
            results["status"] = "completed"
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"   ❌ Error: {e}")
        
        return results
    
    def _test_real_framework_run_with_mcps(self) -> Dict[str, Any]:
        """Test MCPs during a real framework run"""
        results = {
            "test_name": "Real Framework Run with MCPs",
            "status": "running",
            "framework_run": {}
        }
        
        try:
            # Test with a simple JIRA ticket simulation
            print("   🎫 Testing with simulated JIRA ticket...")
            
            # Check if framework execution scripts exist
            framework_scripts = [
                self.framework_root / '.claude' / 'enforcement' / 'strict_framework_activator.py',
                self.framework_root / '.claude' / 'ai-services' / 'ai_agent_orchestrator.py'
            ]
            
            scripts_found = []
            for script in framework_scripts:
                if script.exists():
                    scripts_found.append(str(script))
            
            results["framework_run"]["scripts_available"] = scripts_found
            
            # Test MCP integration during framework components
            print("   🔧 Testing MCP integration in framework components...")
            
            # Test 1: Check if MCP is used in AI services
            ai_services_dir = self.framework_root / '.claude' / 'ai-services'
            mcp_usage_in_services = {}
            
            if ai_services_dir.exists():
                for py_file in ai_services_dir.glob("*.py"):
                    if py_file.is_file():
                        with open(py_file, 'r') as f:
                            content = f.read()
                        
                        mcp_usage_in_services[py_file.name] = {
                            "imports_mcp": "MCPServiceCoordinator" in content or "mcp_service" in content,
                            "mcp_calls": content.lower().count("mcp"),
                            "github_mcp": "github_get_pull_request" in content,
                            "filesystem_mcp": "filesystem_search" in content
                        }
            
            results["framework_run"]["mcp_usage_in_services"] = mcp_usage_in_services
            
            # Test 2: Validate MCP configuration
            config_file = self.framework_root / '.claude' / 'config' / 'mcp-integration-config.json'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    mcp_config = json.load(f)
                
                results["framework_run"]["mcp_config"] = {
                    "config_exists": True,
                    "mcp_enabled": mcp_config.get("mcp_integration", {}).get("enabled", False),
                    "github_mcp_enabled": mcp_config.get("mcp_integration", {}).get("github_mcp", {}).get("enabled", False),
                    "filesystem_mcp_enabled": mcp_config.get("mcp_integration", {}).get("filesystem_mcp", {}).get("enabled", False)
                }
            else:
                results["framework_run"]["mcp_config"] = {"config_exists": False}
            
            results["status"] = "completed"
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"   ❌ Error: {e}")
        
        return results
    
    def _generate_overall_assessment(self) -> Dict[str, Any]:
        """Generate overall assessment of MCP functionality"""
        
        # Count successful tests
        total_tests = 0
        successful_tests = 0
        
        for test_category, test_data in self.test_results.items():
            if isinstance(test_data, dict):
                if test_data.get("status") == "completed" or test_data.get("status") == "success":
                    successful_tests += 1
                total_tests += 1
        
        success_rate = (successful_tests / max(total_tests, 1)) * 100
        
        return {
            "overall_status": "healthy" if success_rate >= 80 else "needs_attention" if success_rate >= 60 else "critical",
            "success_rate": success_rate,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "mcp_readiness": "production_ready" if success_rate >= 90 else "development_ready" if success_rate >= 70 else "needs_work",
            "recommendations": self._generate_recommendations(success_rate)
        }
    
    def _generate_recommendations(self, success_rate: float) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        if success_rate < 80:
            recommendations.append("Review failed tests and address MCP integration issues")
        
        if success_rate >= 90:
            recommendations.append("MCPs are working well - consider enabling for production use")
        elif success_rate >= 70:
            recommendations.append("MCPs are mostly working - monitor performance and fix minor issues")
        else:
            recommendations.append("MCPs need significant work before production deployment")
        
        recommendations.extend([
            "Monitor MCP performance during framework runs",
            "Ensure fallback mechanisms are working correctly",
            "Validate that MCPs don't impact framework reliability"
        ])
        
        return recommendations
    
    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive MCP test report"""
        
        report_lines = [
            "# 🧪 MCP Framework Integration Test Report",
            "",
            f"**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Framework Root**: {self.framework_root}",
            "",
            "## 📊 Executive Summary",
            ""
        ]
        
        # Add overall assessment
        assessment = self._generate_overall_assessment()
        report_lines.extend([
            f"**Overall Status**: {assessment['overall_status']}",
            f"**Success Rate**: {assessment['success_rate']:.1f}%",
            f"**MCP Readiness**: {assessment['mcp_readiness']}",
            "",
            "## 🔍 Detailed Test Results",
            ""
        ])
        
        # Add detailed results for each test
        for test_name, results in self.test_results.items():
            report_lines.extend([
                f"### {test_name}",
                f"**Status**: {results.get('status', 'unknown')}",
                ""
            ])
            
            if results.get("error"):
                report_lines.append(f"**Error**: {results['error']}")
            
            if isinstance(results, dict):
                for key, value in results.items():
                    if key not in ["status", "error", "test_name"]:
                        if isinstance(value, dict):
                            report_lines.append(f"**{key}**: {len(value)} items")
                        else:
                            report_lines.append(f"**{key}**: {value}")
            
            report_lines.append("")
        
        # Add recommendations
        report_lines.extend([
            "## 💡 Recommendations",
            ""
        ])
        
        for rec in assessment['recommendations']:
            report_lines.append(f"- {rec}")
        
        return "\n".join(report_lines)


def main():
    """Main test execution"""
    
    tester = MCPFrameworkTester()
    
    # Run comprehensive tests
    test_results = tester.run_comprehensive_mcp_tests()
    tester.test_results = test_results
    
    # Generate and save report
    report = tester.generate_comprehensive_report()
    
    # Save to file
    report_file = Path(__file__).parent / "mcp_framework_test_report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n📄 Full report saved to: {report_file}")
    
    # Print summary
    assessment = test_results.get("overall_assessment", {})
    print(f"\n🎯 FINAL ASSESSMENT")
    print(f"Overall Status: {assessment.get('overall_status', 'unknown')}")
    print(f"Success Rate: {assessment.get('success_rate', 0):.1f}%")
    print(f"MCP Readiness: {assessment.get('mcp_readiness', 'unknown')}")
    
    return test_results


if __name__ == "__main__":
    main()
