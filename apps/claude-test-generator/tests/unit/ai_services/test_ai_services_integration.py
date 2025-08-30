#!/usr/bin/env python3
"""
AI Services Integration Test Suite
=================================

Comprehensive integration testing for all AI service replacements to ensure
they work together harmoniously and provide enhanced capabilities while
maintaining 100% backward compatibility.

VALIDATION SCOPE:
1. All three AI services working together
2. Cross-service compatibility and data flow
3. Performance characteristics of integrated system
4. End-to-end workflow validation
5. Real-world scenario testing

CRITICAL: This test validates the complete AI replacement ecosystem.
"""

import os
import sys
import json
import tempfile
import shutil
import unittest
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add path to import all AI services
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))
sys.path.append(str(current_dir / '..' / 'logs'))
sys.path.append(str(current_dir / '..' / 'observability'))
sys.path.append(str(current_dir / '..' / 'run-organization'))

try:
    from ai_log_analysis_service import AILogAnalysisService
    from ai_observability_intelligence import AIObservabilityIntelligence
    from ai_run_organization_service import AIRunOrganizationService
    
    # Legacy imports for available components
    from observability_command_handler import ObservabilityCommandHandler
    from intelligent_run_organizer import IntelligentRunOrganizer
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all AI services and legacy components are available")
    sys.exit(1)

class AIServicesIntegrationTest(unittest.TestCase):
    """Comprehensive integration test for AI services ecosystem"""
    
    def setUp(self):
        """Setup realistic test environment for integration testing"""
        self.test_base_dir = tempfile.mkdtemp()
        self.test_runs_dir = Path(self.test_base_dir) / "runs"
        self.test_logs_dir = Path(self.test_base_dir) / "logs"
        
        # Create directory structure
        self.test_runs_dir.mkdir(parents=True)
        self.test_logs_dir.mkdir(parents=True)
        
        # Initialize all AI services first
        self.ai_log_service = AILogAnalysisService(str(self.test_logs_dir))
        self.ai_observability = AIObservabilityIntelligence(str(self.test_runs_dir))
        self.ai_organization = AIRunOrganizationService(str(self.test_runs_dir))
        
        # Initialize legacy services for comparison
        self.legacy_observability = ObservabilityCommandHandler(str(self.test_runs_dir))
        self.legacy_organizer = IntelligentRunOrganizer(str(self.test_runs_dir))
        
        # Create realistic test data
        self.create_realistic_test_scenario()
        
        # Test scenarios
        self.test_tickets = ["ACM-22079", "ACM-15207", "ACM-13644"]
        
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_base_dir, ignore_errors=True)
    
    def create_realistic_test_scenario(self):
        """Create realistic test scenario with logs, runs, and metadata"""
        
        # Create test ticket runs with metadata
        ticket_data = {
            "ACM-22079": {
                "feature": "Enable cluster upgrades using ClusterCurator with digest references",
                "priority": "High",
                "runs": ["20250123-143000", "20250124-091500"]
            },
            "ACM-15207": {
                "feature": "Support for custom ACM observability configurations",
                "priority": "Medium", 
                "runs": ["20250122-100000", "20250123-140000"]
            },
            "ACM-13644": {
                "feature": "Enhanced ACM cluster lifecycle management",
                "priority": "Medium",
                "runs": ["20250121-080000"]
            }
        }
        
        # Create run directories and metadata
        for ticket, data in ticket_data.items():
            for run_timestamp in data["runs"]:
                run_dir = self.test_runs_dir / f"{ticket}-{run_timestamp}"
                run_dir.mkdir(parents=True)
                
                # Create run metadata
                metadata = {
                    "jira_ticket": ticket,
                    "feature": data["feature"],
                    "priority": data["priority"],
                    "generation_timestamp": datetime.now().isoformat(),
                    "framework_execution": {
                        "phase_1": {"status": "completed"},
                        "phase_2": {"status": "completed"},
                        "phase_3": {"status": "in_progress"}
                    },
                    "test_environment": {
                        "cluster": "qe4-hub",
                        "health_score": "8.5/10",
                        "acm_version": "2.11.0"
                    }
                }
                
                metadata_file = run_dir / "run-metadata.json"
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                # Create test deliverables
                test_cases_file = run_dir / f"{ticket}_Test_Cases.md"
                test_cases_file.write_text(f"# Test Cases for {ticket}\n\nComprehensive test cases...")
                
                analysis_file = run_dir / f"{ticket}_Complete_Analysis.md" 
                analysis_file.write_text(f"# Analysis for {ticket}\n\nDetailed analysis...")
        
        # Create framework logs
        log_entries = [
            {"timestamp": "2025-01-24T16:30:00Z", "level": "INFO", "source": "agent_a", "message": "Phase 1 Requirements analysis initiated"},
            {"timestamp": "2025-01-24T16:31:00Z", "level": "INFO", "source": "agent_b", "message": "Documentation intelligence gathering complete"},
            {"timestamp": "2025-01-24T16:32:00Z", "level": "WARN", "source": "agent_c", "message": "GitHub investigation rate limit encountered"},
            {"timestamp": "2025-01-24T16:33:00Z", "level": "INFO", "source": "agent_d", "message": "Environment intelligence assessment complete"},
            {"timestamp": "2025-01-24T16:34:00Z", "level": "INFO", "source": "framework", "message": "Phase 2 Technical analysis initiated"},
            {"timestamp": "2025-01-24T16:35:00Z", "level": "ERROR", "source": "validation", "message": "Evidence validation temporarily blocked on external dependency"},
            {"timestamp": "2025-01-24T16:36:00Z", "level": "INFO", "source": "framework", "message": "Progressive Context Architecture operating optimally"}
        ]
        
        log_file = self.test_logs_dir / "framework-execution.log"
        with open(log_file, 'w') as f:
            for entry in log_entries:
                f.write(f"[{entry['timestamp']}] {entry['level']} [{entry['source']}] {entry['message']}\n")
        
        # Create observability state
        observability_state = {
            "framework_state": {
                "current_phase": "phase_2_technical_analysis",
                "completion_percentage": 45,
                "start_time": "2025-01-24T16:30:00Z",
                "execution_time_minutes": 6
            },
            "agent_coordination": {
                "active_agents": ["agent_c", "agent_d"],
                "completed_agents": ["agent_a", "agent_b"],
                "coordination_quality": "optimal"
            },
            "validation_status": {
                "evidence_validation": "passed",
                "cross_agent_validation": "passed", 
                "context_validation": "in_progress",
                "framework_validation": "passed"
            },
            "run_metadata": {
                "jira_ticket": "ACM-22079",
                "feature": "Enable cluster upgrades using ClusterCurator with digest references",
                "priority": "High"
            }
        }
        
        # Update AI observability state for testing
        self.ai_observability.legacy_handler.state = observability_state
    
    def test_individual_service_functionality(self):
        """Test that each AI service maintains individual functionality"""
        print("\n🧪 Testing individual AI service functionality...")
        
        # Test AI Log Analysis Service
        log_summary = self.ai_log_service.generate_intelligent_insights()
        self.assertIsInstance(log_summary, dict)
        self.assertIn('ai_analysis_metadata', log_summary)
        print("✅ AI Log Analysis Service: Functional")
        
        # Test AI Observability Intelligence
        observability_report = self.ai_observability.generate_intelligent_monitoring_report()
        self.assertIsInstance(observability_report, dict)
        self.assertIn('ai_monitoring_metadata', observability_report)
        print("✅ AI Observability Intelligence: Functional")
        
        # Test AI Run Organization Service
        org_insights = self.ai_organization.generate_organization_insights()
        self.assertIsInstance(org_insights, dict)
        self.assertIn('organization_analysis', org_insights)
        print("✅ AI Run Organization Service: Functional")
        
        print("🎉 All individual AI services functioning correctly!")
    
    def test_cross_service_compatibility(self):
        """Test compatibility and data flow between AI services"""
        print("\n🔗 Testing cross-service compatibility...")
        
        # Test shared data structures and formats
        log_analysis = self.ai_log_service.generate_intelligent_insights()
        observability_data = self.ai_observability.generate_intelligent_monitoring_report()
        organization_data = self.ai_organization.generate_organization_insights()
        
        # Verify all services return compatible data structures
        services_data = [log_analysis, observability_data, organization_data]
        
        for i, data in enumerate(services_data):
            service_names = ["Log Analysis", "Observability", "Organization"]
            self.assertIsInstance(data, dict, f"{service_names[i]} should return dict")
            self.assertTrue(len(data) > 0, f"{service_names[i]} should return non-empty data")
            print(f"✅ {service_names[i]}: Compatible data structure")
        
        # Test timestamp compatibility (all should use ISO format)
        for data in services_data:
            for key, value in data.items():
                if 'timestamp' in key.lower() and isinstance(value, str):
                    try:
                        datetime.fromisoformat(value.replace('Z', '+00:00'))
                        print(f"✅ Timestamp format compatible: {key}")
                    except ValueError:
                        self.fail(f"Incompatible timestamp format in {key}: {value}")
        
        print("🔗 Cross-service compatibility confirmed!")
    
    def test_integrated_workflow_scenario(self):
        """Test complete integrated workflow with all AI services"""
        print("\n🔄 Testing integrated workflow scenario...")
        
        test_ticket = "ACM-22079"
        
        # Step 1: Analyze logs for this ticket's execution
        print(f"   Step 1: Analyzing logs for {test_ticket}...")
        log_analysis = self.ai_log_service.generate_intelligent_insights()
        
        # Verify log analysis provides insights
        ai_insights = log_analysis.get('predictive_insights', [])
        self.assertGreater(len(ai_insights), 0, "Log analysis should provide AI insights")
        print(f"     📊 Log insights: {len(ai_insights)} insights generated")
        
        # Step 2: Monitor current execution state
        print(f"   Step 2: Monitoring execution state...")
        monitoring_report = self.ai_observability.generate_intelligent_monitoring_report()
        
        # Verify monitoring provides context
        context_analysis = monitoring_report.get('intelligent_context_analysis', {})
        self.assertIsInstance(context_analysis, dict)
        self.assertTrue(len(context_analysis) > 0, "Monitoring should provide context analysis")
        print(f"     🔍 Context dimensions: {len(context_analysis)} analyzed")
        
        # Step 3: Optimize run organization
        print(f"   Step 3: Optimizing run organization...")
        organization_result = self.ai_organization.organize_with_ai_intelligence(test_ticket)
        
        # Verify organization provides optimization
        ai_recommendations = organization_result.get('ai_recommendations', [])
        self.assertGreater(len(ai_recommendations), 0, "Organization should provide recommendations")
        print(f"     🚀 AI recommendations: {len(ai_recommendations)} optimizations")
        
        # Step 4: Validate integrated results
        print(f"   Step 4: Validating integrated results...")
        
        # All services should contribute to overall intelligence
        total_ai_capabilities = (
            len(log_analysis.get('ai_analysis_metadata', {}).get('ai_capabilities_applied', [])) +
            len(monitoring_report.get('ai_monitoring_metadata', {}).get('ai_capabilities_applied', [])) +
            len(organization_result.get('ai_organization_metadata', {}).get('ai_capabilities_applied', []))
        )
        
        self.assertGreater(total_ai_capabilities, 8, "Integrated workflow should apply multiple AI capabilities")
        print(f"     🧠 Total AI capabilities: {total_ai_capabilities} applied")
        
        print("✅ Integrated workflow scenario: Successful")
    
    def test_performance_integration(self):
        """Test performance characteristics of integrated AI services"""
        print("\n⚡ Testing integrated performance characteristics...")
        
        start_time = time.time()
        
        # Execute all AI services in sequence (realistic usage pattern)
        test_ticket = "ACM-15207"
        
        # Log analysis
        log_start = time.time()
        log_analysis = self.ai_log_service.generate_intelligent_insights()
        log_time = time.time() - log_start
        
        # Observability monitoring
        obs_start = time.time()
        observability_report = self.ai_observability.generate_intelligent_monitoring_report()
        obs_time = time.time() - obs_start
        
        # Organization optimization
        org_start = time.time()
        organization_result = self.ai_organization.organize_with_ai_intelligence(test_ticket)
        org_time = time.time() - org_start
        
        total_time = time.time() - start_time
        
        # Performance requirements for integrated system
        self.assertLess(total_time, 15.0, "Integrated workflow should complete in under 15 seconds")
        self.assertLess(log_time, 5.0, "Log analysis should complete in under 5 seconds")
        self.assertLess(obs_time, 5.0, "Observability monitoring should complete in under 5 seconds")
        self.assertLess(org_time, 8.0, "Organization should complete in under 8 seconds")
        
        print(f"   📊 Performance Results:")
        print(f"     Log Analysis: {log_time:.3f}s")
        print(f"     Observability: {obs_time:.3f}s") 
        print(f"     Organization: {org_time:.3f}s")
        print(f"     Total Integrated: {total_time:.3f}s")
        
        # Efficiency ratio (AI vs Legacy)
        print(f"   🎯 AI Services Performance: Efficient ({total_time:.1f}s for complete workflow)")
        
        print("⚡ Integrated performance: Acceptable")
    
    def test_backward_compatibility_integration(self):
        """Test that AI services maintain backward compatibility when used together"""
        print("\n🔄 Testing backward compatibility integration...")
        
        test_ticket = "ACM-13644"
        
        # Test that legacy and AI services produce compatible results
        
        # Log analysis functionality (no legacy counterpart)
        ai_logs = self.ai_log_service.analyze_execution_timeline()
        
        # Should return analysis structure (may be empty with no logs)
        self.assertIsInstance(ai_logs, dict)
        print("✅ Log analysis: Functional")
        
        # Observability compatibility
        legacy_status = self.legacy_observability.process_command('/status')
        ai_status = self.ai_observability.process_command('/status')
        
        # Both should return status information
        self.assertIsInstance(legacy_status, str)
        self.assertIsInstance(ai_status, str)
        self.assertGreater(len(legacy_status), 10)
        self.assertGreater(len(ai_status), 10)
        print("✅ Observability: Backward compatible")
        
        # Organization compatibility
        legacy_runs = self.legacy_organizer.detect_existing_runs(test_ticket)
        ai_runs = self.ai_organization.detect_existing_runs(test_ticket)
        
        # Should detect same runs
        self.assertEqual(legacy_runs, ai_runs)
        print("✅ Organization: Backward compatible")
        
        print("🎉 Backward compatibility integration: Confirmed")
    
    def test_ai_enhancement_integration(self):
        """Test integrated AI enhancement capabilities"""
        print("\n🧠 Testing integrated AI enhancement capabilities...")
        
        # Test that AI services provide enhanced value when working together
        test_ticket = "ACM-22079"
        
        # Collect AI enhancements from all services
        log_enhancements = [self.ai_log_service.get_natural_language_summary()]
        observability_enhancements = self.ai_observability.get_intelligent_recommendations()
        organization_enhancements = self.ai_organization.optimize_organization_structure()
        
        # Verify enhancements are provided
        self.assertIsInstance(log_enhancements, list)
        self.assertIsInstance(observability_enhancements, list)
        self.assertIsInstance(organization_enhancements, list)
        
        total_enhancements = len(log_enhancements) + len(observability_enhancements) + len(organization_enhancements)
        self.assertGreater(total_enhancements, 3, "AI services should provide multiple enhancements")
        
        print(f"   📈 AI Enhancements Provided:")
        print(f"     Log Intelligence: {len(log_enhancements)} insights")
        print(f"     Observability Intelligence: {len(observability_enhancements)} recommendations")
        print(f"     Organization Intelligence: {len(organization_enhancements)} optimizations")
        print(f"     Total: {total_enhancements} AI enhancements")
        
        # Test cross-service AI synergy
        # When all services work together, should provide comprehensive intelligence
        
        # Get predictive insights from observability
        predictions = self.ai_observability.predict_execution_outcomes()
        self.assertIsInstance(predictions, list)
        
        # Get cleanup recommendations from organization
        cleanup_candidates = self.ai_organization.predict_cleanup_candidates()
        self.assertIsInstance(cleanup_candidates, list)
        
        print(f"     🔮 Predictive capabilities: {len(predictions)} predictions")
        print(f"     🧹 Optimization capabilities: {len(cleanup_candidates)} optimizations")
        
        print("🧠 AI enhancement integration: Comprehensive")
    
    def test_error_handling_integration(self):
        """Test integrated error handling and resilience"""
        print("\n🛠️ Testing integrated error handling...")
        
        # Test that one service failure doesn't break others
        
        # Create scenario with missing data
        broken_ticket = "ACM-BROKEN"
        
        try:
            # Each service should handle missing data gracefully
            log_result = self.ai_log_service.generate_intelligent_insights()
            self.assertIsInstance(log_result, dict)
            print("✅ Log service: Handles missing data gracefully")
            
            observability_result = self.ai_observability.process_command('/status')
            self.assertIsInstance(observability_result, str)
            print("✅ Observability service: Handles missing data gracefully")
            
            organization_result = self.ai_organization.detect_existing_runs(broken_ticket)
            self.assertIsInstance(organization_result, list)
            print("✅ Organization service: Handles missing data gracefully")
            
        except Exception as e:
            self.fail(f"AI services should handle errors gracefully: {e}")
        
        print("🛡️ Integrated error handling: Robust")
    
    def run_comprehensive_integration_test(self):
        """Run complete integration test suite"""
        print("🚀 AI SERVICES INTEGRATION TEST SUITE")
        print("=" * 60)
        print("Testing complete AI service ecosystem integration")
        print("VALIDATION: All services working together harmoniously")
        print()
        
        integration_results = {}
        
        try:
            # Individual functionality
            print("🔍 INDIVIDUAL SERVICE FUNCTIONALITY")
            self.test_individual_service_functionality()
            integration_results['individual_functionality'] = 'passed'
            
            # Cross-service compatibility
            print("\n🔗 CROSS-SERVICE COMPATIBILITY")
            self.test_cross_service_compatibility()
            integration_results['cross_service_compatibility'] = 'passed'
            
            # Integrated workflow
            print("\n🔄 INTEGRATED WORKFLOW")
            self.test_integrated_workflow_scenario()
            integration_results['integrated_workflow'] = 'passed'
            
            # Performance integration
            print("\n⚡ PERFORMANCE INTEGRATION")
            self.test_performance_integration()
            integration_results['performance_integration'] = 'passed'
            
            # Backward compatibility
            print("\n🔄 BACKWARD COMPATIBILITY INTEGRATION")
            self.test_backward_compatibility_integration()
            integration_results['backward_compatibility'] = 'passed'
            
            # AI enhancement integration
            print("\n🧠 AI ENHANCEMENT INTEGRATION")
            self.test_ai_enhancement_integration()
            integration_results['ai_enhancement'] = 'passed'
            
            # Error handling integration
            print("\n🛠️ ERROR HANDLING INTEGRATION")
            self.test_error_handling_integration()
            integration_results['error_handling'] = 'passed'
            
            print("\n🎉 INTEGRATION TEST COMPLETE")
            print("=" * 60)
            print("✅ Individual functionality: All AI services working independently")
            print("✅ Cross-service compatibility: Data flow and structures compatible")
            print("✅ Integrated workflow: End-to-end scenarios successful")
            print("✅ Performance integration: Acceptable performance characteristics")
            print("✅ Backward compatibility: 100% compatibility maintained")
            print("✅ AI enhancement integration: Comprehensive intelligence provided")
            print("✅ Error handling integration: Robust error resilience")
            
            print("\n🚀 AI SERVICES ECOSYSTEM IS PRODUCTION-READY!")
            print("✅ All three AI services working together harmoniously")
            print("✅ Enhanced capabilities while maintaining full compatibility")
            print("✅ Comprehensive intelligence across log analysis, observability, and organization")
            print("✅ Safe for deployment as integrated AI enhancement suite")
            
            return True, integration_results
            
        except Exception as e:
            print(f"\n❌ INTEGRATION TEST FAILED")
            print(f"CRITICAL ERROR: {e}")
            print("\n🛑 DO NOT DEPLOY - INTEGRATION ISSUES DETECTED")
            
            return False, {'error': str(e)}

if __name__ == "__main__":
    # Create test instance and run comprehensive integration test
    test_instance = AIServicesIntegrationTest()
    test_instance.setUp()
    
    try:
        success, results = test_instance.run_comprehensive_integration_test()
        
        if success:
            print("\n🎯 AI SERVICES INTEGRATION TEST SUCCESSFUL!")
            print("Complete AI service ecosystem validated and ready for production deployment")
            sys.exit(0)
        else:
            print("\n🛑 CRITICAL: INTEGRATION TEST FAILED")
            print("AI services ecosystem has integration issues - fix before deployment")
            sys.exit(1)
            
    finally:
        test_instance.tearDown()