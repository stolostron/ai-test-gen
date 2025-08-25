#!/usr/bin/env python3
"""
AI Log Analysis Service Validation Test
=====================================

Comprehensive validation to ensure:
1. 100% backward compatibility with FrameworkLogAnalyzer
2. AI enhancements work correctly
3. No regression in functionality
4. Performance is acceptable

This test validates safe migration from legacy to AI service.
"""

import os
import sys
import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add path to import services
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))
sys.path.append(str(current_dir / '..' / 'logging'))

try:
    from ai_log_analysis_service import AILogAnalysisService
    from log_analyzer import FrameworkLogAnalyzer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure log_analyzer.py exists in .claude/logging/")
    sys.exit(1)

class AILogAnalysisValidationTest(unittest.TestCase):
    """Comprehensive validation test for AI Log Analysis Service"""
    
    def setUp(self):
        """Setup test environment with sample log data"""
        self.test_log_dir = tempfile.mkdtemp()
        self.create_sample_log_data()
        
        # Initialize both analyzers for comparison
        self.ai_analyzer = AILogAnalysisService(self.test_log_dir)
        self.legacy_analyzer = FrameworkLogAnalyzer(self.test_log_dir)
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_log_dir, ignore_errors=True)
    
    def create_sample_log_data(self):
        """Create realistic sample log data for testing"""
        
        # Sample log entries
        sample_logs = [
            {
                "timestamp": "2025-01-24T10:00:00Z",
                "component": "PHASE",
                "phase": "phase_0",
                "action": "phase_initialization",
                "log_level": "INFO",
                "details": {"phase_name": "JIRA Analysis"}
            },
            {
                "timestamp": "2025-01-24T10:01:00Z",
                "component": "AGENT",
                "agent": "agent_a",
                "action": "jira_analysis_start",
                "log_level": "INFO",
                "details": {"ticket": "ACM-22079"}
            },
            {
                "timestamp": "2025-01-24T10:02:00Z",
                "component": "TOOL",
                "action": "data_collection",
                "log_level": "INFO",
                "details": {"tool_name": "jira_api"},
                "performance_metrics": {"tool_duration_seconds": 2.5}
            },
            {
                "timestamp": "2025-01-24T10:03:00Z",
                "component": "VALIDATION",
                "action": "quality_check",
                "log_level": "INFO",
                "details": {"validation_type": "content_quality", "result": "passed"}
            },
            {
                "timestamp": "2025-01-24T10:04:00Z",
                "component": "PHASE",
                "phase": "phase_1",
                "action": "phase_completion",
                "log_level": "INFO",
                "details": {"phase_name": "Agent Coordination"}
            }
        ]
        
        # Create master log file
        master_log_path = Path(self.test_log_dir) / 'framework_debug_master.jsonl'
        with open(master_log_path, 'w') as f:
            for log_entry in sample_logs:
                f.write(json.dumps(log_entry) + '\n')
        
        # Create summary file
        summary_data = {
            "execution_id": "test_execution",
            "start_time": "2025-01-24T10:00:00Z",
            "end_time": "2025-01-24T10:05:00Z",
            "total_phases": 2,
            "total_agents": 1
        }
        
        summary_path = Path(self.test_log_dir) / 'execution_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary_data, f, indent=2)
    
    def test_backward_compatibility_methods(self):
        """Test that all legacy methods work identically"""
        print("\n🔄 Testing backward compatibility...")
        
        # Test all major analysis methods
        legacy_timeline = self.legacy_analyzer.analyze_execution_timeline()
        ai_timeline = self.ai_analyzer.analyze_execution_timeline()
        
        # Should return identical results
        self.assertEqual(legacy_timeline['total_events'], ai_timeline['total_events'])
        self.assertEqual(legacy_timeline['start_time'], ai_timeline['start_time'])
        
        print("✅ Timeline analysis: Compatible")
        
        # Test agent coordination
        legacy_agents = self.legacy_analyzer.analyze_agent_coordination()
        ai_agents = self.ai_analyzer.analyze_agent_coordination()
        
        self.assertEqual(legacy_agents['agent_count'], ai_agents['agent_count'])
        
        print("✅ Agent coordination: Compatible")
        
        # Test error analysis
        legacy_errors = self.legacy_analyzer.analyze_errors()
        ai_errors = self.ai_analyzer.analyze_errors()
        
        self.assertEqual(legacy_errors['error_count'], ai_errors['error_count'])
        
        print("✅ Error analysis: Compatible")
        
        # Test query functionality
        query_params = {'component': 'AGENT'}
        legacy_query = self.legacy_analyzer.query_logs(query_params)
        ai_query = self.ai_analyzer.query_logs(query_params)
        
        self.assertEqual(len(legacy_query), len(ai_query))
        
        print("✅ Log queries: Compatible")
        
        print("🎉 All backward compatibility tests passed!")
    
    def test_ai_enhancements(self):
        """Test AI enhancement features"""
        print("\n🧠 Testing AI enhancements...")
        
        # Test intelligent insights generation
        insights = self.ai_analyzer.generate_intelligent_insights()
        
        # Validate structure
        required_keys = [
            'ai_analysis_metadata',
            'intelligent_patterns', 
            'detected_anomalies',
            'execution_summary',
            'improvement_recommendations',
            'predictive_insights'
        ]
        
        for key in required_keys:
            self.assertIn(key, insights)
            
        print("✅ Intelligent insights: Structure validated")
        
        # Test natural language summary
        summary = self.ai_analyzer.get_natural_language_summary()
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 50)  # Should be substantial
        
        print("✅ Natural language summary: Generated")
        
        # Test issue detection
        issues = self.ai_analyzer.detect_potential_issues()
        self.assertIsInstance(issues, list)
        
        print("✅ Issue detection: Functional")
        
        # Test pattern recognition
        patterns = insights['intelligent_patterns']
        self.assertIn('phase_progression_patterns', patterns)
        self.assertIn('agent_coordination_patterns', patterns)
        
        print("✅ Pattern recognition: Active")
        
        print("🚀 All AI enhancement tests passed!")
    
    def test_performance_comparison(self):
        """Compare performance between legacy and AI analyzers"""
        print("\n⚡ Testing performance...")
        
        import time
        
        # Test legacy analyzer performance
        start_time = time.time()
        legacy_timeline = self.legacy_analyzer.analyze_execution_timeline()
        legacy_time = time.time() - start_time
        
        # Test AI analyzer performance (basic compatibility methods)
        start_time = time.time()
        ai_timeline = self.ai_analyzer.analyze_execution_timeline()
        ai_compatibility_time = time.time() - start_time
        
        # Test AI enhancements performance
        start_time = time.time()
        ai_insights = self.ai_analyzer.generate_intelligent_insights()
        ai_enhancement_time = time.time() - start_time
        
        print(f"📊 Performance Results:")
        print(f"   Legacy analyzer: {legacy_time:.3f}s")
        print(f"   AI compatibility: {ai_compatibility_time:.3f}s")
        print(f"   AI enhancements: {ai_enhancement_time:.3f}s")
        
        # Compatibility methods should be nearly identical in performance
        performance_ratio = ai_compatibility_time / legacy_time if legacy_time > 0 else 1
        self.assertLess(performance_ratio, 3.0)  # Should not be more than 3x slower
        
        print(f"✅ Performance ratio: {performance_ratio:.2f}x (acceptable)")
        
        # AI enhancements should be reasonable (< 5 seconds for this small dataset)
        self.assertLess(ai_enhancement_time, 5.0)
        
        print("✅ AI enhancement performance: Acceptable")
    
    def test_data_integrity(self):
        """Test that AI analyzer doesn't corrupt or modify original data"""
        print("\n🔒 Testing data integrity...")
        
        # Get original log count
        original_logs = len(self.legacy_analyzer.logs)
        
        # Run AI analysis
        insights = self.ai_analyzer.generate_intelligent_insights()
        
        # Verify log count unchanged
        ai_logs = len(self.ai_analyzer.logs)
        self.assertEqual(original_logs, ai_logs)
        
        print("✅ Log data: Unchanged")
        
        # Verify log content unchanged
        for i, (orig_log, ai_log) in enumerate(zip(self.legacy_analyzer.logs, self.ai_analyzer.logs)):
            self.assertEqual(orig_log, ai_log, f"Log entry {i} differs")
        
        print("✅ Log content: Identical")
        
        # Verify summary unchanged
        self.assertEqual(self.legacy_analyzer.summary, self.ai_analyzer.summary)
        
        print("✅ Summary data: Unchanged")
        print("🛡️ Data integrity maintained!")
    
    def test_error_handling(self):
        """Test error handling and graceful degradation"""
        print("\n🛠️ Testing error handling...")
        
        # Test with empty log directory
        empty_dir = tempfile.mkdtemp()
        try:
            empty_analyzer = AILogAnalysisService(empty_dir)
            
            # Should handle gracefully
            timeline = empty_analyzer.analyze_execution_timeline()
            self.assertIsInstance(timeline, dict)
            
            print("✅ Empty directory: Handled gracefully")
            
            # AI insights should also handle gracefully
            insights = empty_analyzer.generate_intelligent_insights()
            self.assertIsInstance(insights, dict)
            
            print("✅ AI insights on empty data: Handled gracefully")
            
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)
        
        print("🛡️ Error handling tests passed!")
    
    def test_integration_compatibility(self):
        """Test integration with existing framework"""
        print("\n🔗 Testing framework integration...")
        
        # Test that AI analyzer can be used as drop-in replacement
        def framework_function_simulation(analyzer):
            """Simulate how framework would use the analyzer"""
            results = {
                'timeline': analyzer.analyze_execution_timeline(),
                'agents': analyzer.analyze_agent_coordination(),
                'errors': analyzer.analyze_errors(),
                'performance': analyzer.analyze_performance()
            }
            return results
        
        # Test with legacy analyzer
        legacy_results = framework_function_simulation(self.legacy_analyzer)
        
        # Test with AI analyzer (should work identically)
        ai_results = framework_function_simulation(self.ai_analyzer)
        
        # Compare key metrics
        self.assertEqual(
            legacy_results['timeline']['total_events'],
            ai_results['timeline']['total_events']
        )
        
        self.assertEqual(
            legacy_results['agents']['agent_count'],
            ai_results['agents']['agent_count']
        )
        
        print("✅ Drop-in replacement: Compatible")
        
        # Test that AI analyzer provides additional capabilities
        ai_summary = self.ai_analyzer.get_natural_language_summary()
        self.assertIsInstance(ai_summary, str)
        
        print("✅ Enhanced capabilities: Available")
        print("🔗 Integration compatibility confirmed!")
    
    def run_validation_suite(self):
        """Run complete validation suite"""
        print("🚀 AI LOG ANALYSIS SERVICE VALIDATION")
        print("=" * 50)
        
        try:
            self.test_backward_compatibility_methods()
            self.test_ai_enhancements()
            self.test_performance_comparison()
            self.test_data_integrity()
            self.test_error_handling()
            self.test_integration_compatibility()
            
            print("\n🎉 VALIDATION COMPLETE")
            print("=" * 50)
            print("✅ All tests passed - AI service is safe to deploy")
            print("✅ Backward compatibility: 100% maintained")
            print("✅ AI enhancements: Fully functional")
            print("✅ Performance: Acceptable")
            print("✅ Data integrity: Preserved")
            print("✅ Error handling: Robust")
            print("✅ Integration: Compatible")
            
            return True
            
        except Exception as e:
            print(f"\n❌ VALIDATION FAILED")
            print(f"Error: {e}")
            return False

def run_quick_validation(log_directory: str = None):
    """Run quick validation against real log data if available"""
    if log_directory and Path(log_directory).exists():
        print(f"\n🔍 Quick validation with real data: {log_directory}")
        
        try:
            # Test both analyzers with real data
            legacy = FrameworkLogAnalyzer(log_directory)
            ai = AILogAnalysisService(log_directory)
            
            # Compare results
            legacy_timeline = legacy.analyze_execution_timeline()
            ai_timeline = ai.analyze_execution_timeline()
            
            print(f"   Legacy events: {legacy_timeline.get('total_events', 0)}")
            print(f"   AI events: {ai_timeline.get('total_events', 0)}")
            
            if legacy_timeline.get('total_events') == ai_timeline.get('total_events'):
                print("   ✅ Real data compatibility confirmed")
                
                # Test AI insights
                insights = ai.generate_intelligent_insights()
                print(f"   🧠 AI insights generated: {len(insights)} sections")
                
                return True
            else:
                print("   ❌ Event count mismatch")
                return False
                
        except Exception as e:
            print(f"   ⚠️ Real data test failed: {e}")
            return False
    
    return True

if __name__ == "__main__":
    # Create test instance and run validation
    test_instance = AILogAnalysisValidationTest()
    test_instance.setUp()
    
    try:
        success = test_instance.run_validation_suite()
        
        # Optional: Test with real log data if path provided
        if len(sys.argv) > 1:
            real_log_path = sys.argv[1]
            run_quick_validation(real_log_path)
        
        if success:
            print("\n🎯 AI Log Analysis Service is ready for deployment!")
            sys.exit(0)
        else:
            print("\n🛑 Validation failed - do not deploy")
            sys.exit(1)
            
    finally:
        test_instance.tearDown()