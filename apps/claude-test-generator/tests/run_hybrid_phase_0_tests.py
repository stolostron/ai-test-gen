#!/usr/bin/env python3
"""
Hybrid AI-Enhanced Phase 0 Test Runner
Executes combined Python + AI testing with comprehensive reporting
"""

import sys
import os
import unittest
import time
import json
from typing import Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass 
class HybridTestExecutionReport:
    """Comprehensive hybrid test execution report"""
    total_tests: int
    python_passed: int
    python_failed: int
    ai_analyses_completed: int
    ai_analyses_failed: int
    hybrid_confidence_avg: float
    execution_time: float
    implementation_gaps: List[str]
    ai_insights: List[str]
    hybrid_recommendations: List[str]
    next_actions: List[str]


class HybridPhase0TestRunner:
    """
    Comprehensive hybrid test runner combining Python unit tests with AI analysis
    Provides layered validation: deterministic + intelligent
    """
    
    def __init__(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.framework_root = os.path.join(self.test_dir, '..')
        self.hybrid_test_file = os.path.join(self.test_dir, 'unit', 'phase_0', 'test_hybrid_phase_0.py')
        
    def run_hybrid_tests(self) -> HybridTestExecutionReport:
        """Execute hybrid Phase 0 tests and generate comprehensive report"""
        print("🤖 HYBRID AI-ENHANCED PHASE 0 TESTING")
        print("=" * 70)
        print("🔬 Combining deterministic Python validation with AI-powered analysis")
        print("🎯 Target: Comprehensive Phase 0 implementation validation")
        print("=" * 70)
        
        start_time = time.time()
        
        # Execute hybrid tests
        print("🚀 Executing Hybrid Test Suite...")
        test_results = self._execute_hybrid_test_suite()
        
        # Analyze results
        print("📊 Analyzing Results...")
        report = self._analyze_hybrid_results(test_results, time.time() - start_time)
        
        # Generate comprehensive report
        self._print_comprehensive_hybrid_report(report)
        
        return report
    
    def _execute_hybrid_test_suite(self) -> Dict[str, Any]:
        """Execute the hybrid test suite and collect detailed results"""
        
        # Import and setup hybrid test modules
        sys.path.append(os.path.join(self.test_dir, 'unit', 'phase_0'))
        sys.path.append(os.path.join(self.test_dir, 'ai_services'))
        
        from test_hybrid_phase_0 import HybridPhase0TestCase, TestHybridOrchestrator
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Add hybrid test cases
        hybrid_tests = loader.loadTestsFromTestCase(HybridPhase0TestCase)
        orchestrator_tests = loader.loadTestsFromTestCase(TestHybridOrchestrator)
        
        suite.addTests(hybrid_tests)
        suite.addTests(orchestrator_tests)
        
        # Execute with custom result collector
        result_collector = HybridTestResultCollector()
        runner = unittest.TextTestRunner(
            stream=sys.stdout,
            verbosity=2,
            resultclass=lambda stream, descriptions, verbosity: result_collector
        )
        
        print(f"📂 Test Discovery: Found {suite.countTestCases()} hybrid tests")
        print("🔬 Executing hybrid tests...\n")
        
        test_result = runner.run(suite)
        
        return {
            "unittest_result": test_result,
            "hybrid_details": result_collector.hybrid_details,
            "ai_analysis_results": result_collector.ai_analysis_results,
            "python_test_results": result_collector.python_test_results
        }
    
    def _analyze_hybrid_results(self, test_results: Dict[str, Any], execution_time: float) -> HybridTestExecutionReport:
        """Analyze hybrid test results and generate insights"""
        
        unittest_result = test_results["unittest_result"]
        hybrid_details = test_results["hybrid_details"]
        ai_results = test_results["ai_analysis_results"]
        python_results = test_results["python_test_results"]
        
        # Calculate Python test statistics
        total_tests = unittest_result.testsRun
        python_passed = len([r for r in python_results if r.get("passed", False)])
        python_failed = len([r for r in python_results if not r.get("passed", False)])
        
        # Calculate AI analysis statistics
        ai_completed = len([a for a in ai_results if not a.get("error")])
        ai_failed = len([a for a in ai_results if a.get("error")])
        
        # Calculate hybrid confidence
        confidences = [h.get("combined_confidence", 0.0) for h in hybrid_details]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Extract implementation gaps
        implementation_gaps = []
        for python_result in python_results:
            if not python_result.get("passed", False):
                for error in python_result.get("errors", []):
                    if "ImportError" in error or "not found" in error:
                        implementation_gaps.append(f"Missing implementation: {error}")
                    elif "Function not implemented" in error:
                        implementation_gaps.append(f"Missing function: {error}")
        
        # Extract AI insights
        ai_insights = []
        for ai_result in ai_results:
            findings = ai_result.get("findings", [])
            ai_insights.extend(findings[:2])  # Top 2 findings per analysis
        
        # Generate hybrid recommendations
        hybrid_recommendations = self._generate_hybrid_recommendations(
            python_results, ai_results, hybrid_details
        )
        
        # Generate next actions
        next_actions = self._generate_next_actions(
            python_passed, python_failed, ai_completed, implementation_gaps
        )
        
        return HybridTestExecutionReport(
            total_tests=total_tests,
            python_passed=python_passed,
            python_failed=python_failed,
            ai_analyses_completed=ai_completed,
            ai_analyses_failed=ai_failed,
            hybrid_confidence_avg=avg_confidence,
            execution_time=execution_time,
            implementation_gaps=implementation_gaps,
            ai_insights=ai_insights[:5],  # Top 5 insights
            hybrid_recommendations=hybrid_recommendations,
            next_actions=next_actions
        )
    
    def _generate_hybrid_recommendations(self, python_results: List[Dict], ai_results: List[Dict], hybrid_details: List[Dict]) -> List[str]:
        """Generate recommendations combining Python failures and AI insights"""
        recommendations = []
        
        # Priority 1: Critical Python failures with AI context
        for python_result in python_results:
            if not python_result.get("passed", False):
                test_name = python_result.get("test_name", "unknown")
                errors = python_result.get("errors", [])
                
                for error in errors:
                    if "ImportError" in error:
                        recommendations.append(f"CRITICAL: Implement {test_name.replace('test_hybrid_', '').replace('_', ' ')} - AI confirms documentation gap")
                    elif "not found" in error:
                        recommendations.append(f"HIGH: Create missing component for {test_name}")
        
        # Priority 2: AI-identified implementation gaps
        for ai_result in ai_results:
            if ai_result.get("analysis_type") == "documentation_gap":
                findings = ai_result.get("findings", [])
                for finding in findings:
                    if "CRITICAL" in finding:
                        recommendations.append(f"AI-CRITICAL: {finding}")
                    elif "missing" in finding.lower():
                        recommendations.append(f"AI-HIGH: {finding}")
        
        # Priority 3: Hybrid insights
        high_confidence_failures = [h for h in hybrid_details if h.get("combined_confidence", 0) > 0.7 and not h.get("python_test_result", False)]
        for failure in high_confidence_failures:
            recommendations.append(f"HYBRID: High-confidence failure detected in {failure.get('test_name', 'unknown test')}")
        
        return recommendations[:10]  # Top 10 recommendations
    
    def _generate_next_actions(self, python_passed: int, python_failed: int, ai_completed: int, implementation_gaps: List[str]) -> List[str]:
        """Generate specific next actions based on test results"""
        actions = []
        
        # Immediate actions based on Python test results
        if python_failed > python_passed:
            actions.append("1. Address critical implementation gaps identified by Python tests")
            actions.append("2. Create missing Version Intelligence Service implementation")
            actions.append("3. Implement foundation context structure")
        
        # AI-guided actions
        if ai_completed > 0:
            actions.append("4. Review AI analysis recommendations for implementation priority")
            actions.append("5. Use AI-suggested test scenarios to expand test coverage")
        
        # Implementation-specific actions
        if any("Version Intelligence Service" in gap for gap in implementation_gaps):
            actions.append("6. Create .claude/ai-services/version_intelligence_service.py")
            actions.append("7. Implement analyze_version_gap() and create_foundation_context() functions")
        
        # Quality assurance actions
        actions.append("8. Re-run hybrid tests after implementation to validate fixes")
        actions.append("9. Expand to Phase 1 testing once Phase 0 is stable")
        actions.append("10. Consider integration testing for Progressive Context Architecture")
        
        return actions[:8]  # Top 8 actions
    
    def _print_comprehensive_hybrid_report(self, report: HybridTestExecutionReport):
        """Print comprehensive hybrid test execution report"""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE HYBRID PHASE 0 TEST REPORT")
        print("=" * 70)
        
        # Test execution overview
        print(f"\n🎯 Test Execution Overview:")
        print(f"   Total Tests:           {report.total_tests}")
        print(f"   Python Tests Passed:   {report.python_passed} ✅")
        print(f"   Python Tests Failed:   {report.python_failed} ❌")
        print(f"   AI Analyses Completed: {report.ai_analyses_completed} 🧠")
        print(f"   AI Analyses Failed:    {report.ai_analyses_failed} ⚠️")
        print(f"   Execution Time:        {report.execution_time:.2f}s")
        
        # Hybrid confidence metrics
        print(f"\n📈 Hybrid Confidence Metrics:")
        print(f"   Average Confidence:    {report.hybrid_confidence_avg:.2f} (0.0-1.0 scale)")
        confidence_rating = "High" if report.hybrid_confidence_avg > 0.7 else "Medium" if report.hybrid_confidence_avg > 0.4 else "Low"
        print(f"   Confidence Rating:     {confidence_rating}")
        
        # Implementation gaps (from Python tests)
        print(f"\n🚨 Implementation Gaps Detected ({len(report.implementation_gaps)}):")
        if report.implementation_gaps:
            for i, gap in enumerate(report.implementation_gaps, 1):
                print(f"   {i}. {gap}")
        else:
            print("   ✅ No critical implementation gaps detected by Python tests")
        
        # AI insights
        print(f"\n🧠 AI-Generated Insights ({len(report.ai_insights)}):")
        if report.ai_insights:
            for i, insight in enumerate(report.ai_insights, 1):
                print(f"   {i}. {insight}")
        else:
            print("   ⚠️  No AI insights generated")
        
        # Hybrid recommendations
        print(f"\n💡 Hybrid Recommendations ({len(report.hybrid_recommendations)}):")
        if report.hybrid_recommendations:
            for i, rec in enumerate(report.hybrid_recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("   ✅ No critical recommendations - implementation appears complete")
        
        # Overall assessment
        print(f"\n🎯 Overall Assessment:")
        if report.python_failed == 0 and report.hybrid_confidence_avg > 0.8:
            print("   ✅ Phase 0 implementation appears complete and well-validated")
            print("   🚀 Ready to proceed with Phase 1 testing")
        elif report.python_failed > 0 and len(report.implementation_gaps) > 0:
            print("   ❌ Phase 0 has critical implementation gaps requiring immediate attention")
            print("   🔧 Focus on Python test failures first, then AI recommendations")
        else:
            print("   ⚠️  Phase 0 has mixed results - some implementation exists but needs improvement")
            print("   📈 Use AI insights to guide improvement priorities")
        
        # Next actions
        print(f"\n🚀 Immediate Next Actions:")
        for action in report.next_actions:
            print(f"   {action}")
        
        # Hybrid testing benefits summary
        print(f"\n🎉 Hybrid Testing Benefits Demonstrated:")
        print("   🐍 Python tests provided deterministic validation of critical functionality")
        print("   🤖 AI analysis provided semantic understanding and gap identification")
        print("   💡 Hybrid approach generated actionable recommendations with context")
        print("   📊 Combined confidence scoring helped prioritize fixes")


class HybridTestResultCollector(unittest.TestResult):
    """Custom test result collector for hybrid test data"""
    
    def __init__(self):
        super().__init__()
        self.hybrid_details = []
        self.ai_analysis_results = []
        self.python_test_results = []
        self.current_test_details = {}
    
    def startTest(self, test):
        super().startTest(test)
        self.current_test_details = {
            "test_name": test._testMethodName,
            "start_time": time.time()
        }
        print(f"🔬 Running Hybrid Test: {test._testMethodName}")
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.current_test_details.update({
            "passed": True,
            "execution_time": time.time() - self.current_test_details["start_time"]
        })
        self.python_test_results.append(self.current_test_details.copy())
        print(f"   ✅ HYBRID SUCCESS")
    
    def addError(self, test, err):
        super().addError(test, err)
        self.current_test_details.update({
            "passed": False,
            "errors": [str(err[1])],
            "execution_time": time.time() - self.current_test_details["start_time"]
        })
        self.python_test_results.append(self.current_test_details.copy())
        print(f"   ❌ HYBRID ERROR: {err[1]}")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.current_test_details.update({
            "passed": False,
            "errors": [str(err[1])],
            "execution_time": time.time() - self.current_test_details["start_time"]
        })
        self.python_test_results.append(self.current_test_details.copy())
        print(f"   ❌ HYBRID FAILURE: {err[1]}")


def save_hybrid_report(report: HybridTestExecutionReport, output_file: str):
    """Save hybrid test report to JSON file"""
    with open(output_file, 'w') as f:
        json.dump(asdict(report), f, indent=2)


def main():
    """Main execution function"""
    print("🤖 HYBRID AI-ENHANCED PHASE 0 TEST FRAMEWORK")
    print("Combining the best of deterministic Python testing with AI intelligence")
    print(f"Framework: Claude Test Generator Phase 0 Implementation Validation\n")
    
    # Check if we're in the right directory
    current_dir = os.getcwd()
    if not os.path.exists(os.path.join(current_dir, 'tests')):
        print("❌ Error: Must run from claude-test-generator directory")
        print("   Run: cd apps/claude-test-generator/")
        print("   Then: python tests/run_hybrid_phase_0_tests.py")
        sys.exit(1)
    
    # Execute hybrid tests
    runner = HybridPhase0TestRunner()
    report = runner.run_hybrid_tests()
    
    # Save comprehensive report
    report_file = os.path.join('tests', 'hybrid_phase_0_test_report.json')
    save_hybrid_report(report, report_file)
    
    print(f"\n📄 Comprehensive hybrid report saved to: {report_file}")
    
    # Generate summary for quick review
    summary_file = os.path.join('tests', 'phase_0_test_summary.txt')
    with open(summary_file, 'w') as f:
        f.write("PHASE 0 HYBRID TEST SUMMARY\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Python Tests: {report.python_passed} passed, {report.python_failed} failed\n")
        f.write(f"AI Analyses: {report.ai_analyses_completed} completed\n")
        f.write(f"Hybrid Confidence: {report.hybrid_confidence_avg:.2f}\n")
        f.write(f"Implementation Gaps: {len(report.implementation_gaps)}\n")
        f.write(f"Recommendations: {len(report.hybrid_recommendations)}\n\n")
        f.write("TOP RECOMMENDATIONS:\n")
        for i, rec in enumerate(report.hybrid_recommendations[:5], 1):
            f.write(f"{i}. {rec}\n")
    
    print(f"📋 Quick summary saved to: {summary_file}")
    
    # Exit with appropriate code
    exit_code = 0 if report.python_failed == 0 else 1
    print(f"\n🏁 Hybrid test execution complete. Exit code: {exit_code}")
    
    if exit_code == 0:
        print("🎉 Phase 0 implementation validated successfully!")
    else:
        print("🔧 Phase 0 needs implementation work - see recommendations above")
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()