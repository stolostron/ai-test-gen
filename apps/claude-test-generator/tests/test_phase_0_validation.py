#!/usr/bin/env python3
"""
Quick validation test for Phase 0 implementation
Tests the critical functionality identified by the unit tests
"""

import sys
import os
import json
from pathlib import Path

# Add the AI services to the path
sys.path.append('.claude/ai-services')

def test_version_intelligence_service_exists():
    """Test that Version Intelligence Service can be imported"""
    try:
        from version_intelligence_service import VersionIntelligenceService
        print("✅ test_version_intelligence_service_exists: PASSED")
        return True
    except ImportError as e:
        print(f"❌ test_version_intelligence_service_exists: FAILED - {e}")
        return False

def test_foundation_context_creation():
    """Test that foundation context can be created"""
    try:
        from version_intelligence_service import VersionIntelligenceService
        
        service = VersionIntelligenceService()
        context = service.create_foundation_context("ACM-12345")
        
        # Verify context has required fields
        assert context.jira_info.jira_id == "ACM-12345"
        assert context.version_context.target_version
        assert context.version_context.environment_version
        assert context.deployment_instruction
        
        print("✅ test_foundation_context_creation: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_foundation_context_creation: FAILED - {e}")
        return False

def test_foundation_context_completeness():
    """Test foundation context completeness validation"""
    try:
        from version_intelligence_service import VersionIntelligenceService
        
        service = VersionIntelligenceService()
        context = service.create_foundation_context("ACM-12345")
        
        # Test completeness validation
        validation_results = context.validate_completeness()
        ready = context.is_ready_for_agent_inheritance()
        
        assert ready == True, "Foundation context should be ready for agent inheritance"
        assert context.metadata.consistency_score > 0.8, "Consistency score should be high"
        
        print("✅ test_foundation_context_completeness: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_foundation_context_completeness: FAILED - {e}")
        return False

def test_phase_0_generates_actual_files():
    """Test that Phase 0 generates actual output files"""
    try:
        from version_intelligence_service import VersionIntelligenceService
        
        service = VersionIntelligenceService()
        
        # Create context with file output
        output_file = "test-foundation-context.json"
        context = service.create_foundation_context("ACM-12345", output_file=output_file)
        
        # Check if file was created
        assert os.path.exists(output_file), "Foundation context file should be created"
        
        # Verify file content
        with open(output_file, 'r') as f:
            file_content = json.load(f)
        
        assert 'jira_info' in file_content, "File should contain JIRA info"
        assert 'version_context' in file_content, "File should contain version context"
        
        # Cleanup
        os.remove(output_file)
        
        print("✅ test_phase_0_generates_actual_files: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_phase_0_generates_actual_files: FAILED - {e}")
        return False

def test_phase_0_input_output_flow():
    """Test complete Phase 0 input/output flow"""
    try:
        from version_intelligence_service import analyze_jira_ticket
        
        # Test complete analysis flow
        results = analyze_jira_ticket("ACM-22079", environment="test-cluster")
        
        # Verify output structure
        assert 'phase_0_summary' in results, "Results should contain phase 0 summary"
        summary = results['phase_0_summary']
        
        assert 'jira_ticket' in summary, "Summary should contain JIRA ticket info"
        assert 'version_analysis' in summary, "Summary should contain version analysis"
        assert 'environment_status' in summary, "Summary should contain environment status"
        assert 'readiness' in summary, "Summary should contain readiness info"
        
        # Verify agent readiness
        assert summary['readiness']['agent_inheritance_ready'] == True, "Should be ready for agents"
        
        print("✅ test_phase_0_input_output_flow: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_phase_0_input_output_flow: FAILED - {e}")
        return False

def test_phase_0_version_gap_analysis():
    """Test version gap analysis functionality"""
    try:
        from version_intelligence_service import VersionIntelligenceService
        
        service = VersionIntelligenceService()
        context = service.analyze_version_gap("ACM-22079")
        
        # Verify version analysis
        version_context = context.version_context
        assert version_context.target_version == "2.15.0", "Target version should be detected"
        
        # Environment version can be real (from actual cluster) or simulated
        env_version = version_context.environment_version
        assert env_version is not None and env_version != "", "Environment version should be detected"
        
        # Verify comparison result is logical (including context mismatch)
        valid_results = ["newer", "same", "older", "context_mismatch", "not_installed"]
        assert version_context.comparison_result in valid_results, f"Should have valid comparison result, got: {version_context.comparison_result}"
        
        # Verify deployment instruction exists and is logical
        instruction = context.deployment_instruction.upper()
        assert len(instruction) > 0, "Should have deployment instruction"
        
        # Check that instruction matches the comparison result
        if version_context.comparison_result == "newer":
            assert any(keyword in instruction for keyword in ["UPGRADE", "UPDATE"]), "Should contain upgrade instruction for newer target"
        elif version_context.comparison_result == "same":
            assert any(keyword in instruction for keyword in ["NO ACTION", "PROCEED", "TESTING"]), "Should indicate no upgrade needed"
        elif version_context.comparison_result == "older":
            assert any(keyword in instruction for keyword in ["REVIEW", "DOWNGRADE", "VERSION"]), "Should indicate version review needed"
        elif version_context.comparison_result == "context_mismatch":
            assert any(keyword in instruction for keyword in ["CONTEXT MISMATCH", "VERSION CONTEXT", "ACM VERSION"]), "Should indicate context mismatch"
        elif version_context.comparison_result == "not_installed":
            assert any(keyword in instruction for keyword in ["NOT INSTALLED", "INSTALL ACM", "ACM NOT"]), "Should indicate ACM not installed"
        
        print("✅ test_phase_0_version_gap_analysis: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_phase_0_version_gap_analysis: FAILED - {e}")
        return False

def test_progressive_context_architecture_setup():
    """Test that context is set up for Progressive Context Architecture"""
    try:
        from version_intelligence_service import VersionIntelligenceService
        
        service = VersionIntelligenceService()
        context = service.create_foundation_context("ACM-22079")
        
        # Test agent context inheritance readiness
        agent_summary = context.get_agent_context_summary()
        
        # Verify required fields for agent inheritance
        required_fields = [
            'jira_id', 'target_version', 'environment_version', 
            'version_gap', 'environment', 'deployment_instruction'
        ]
        
        for field in required_fields:
            assert field in agent_summary, f"Agent context should contain {field}"
        
        assert agent_summary['ready_for_agents'] == True, "Should be ready for agent inheritance"
        
        print("✅ test_progressive_context_architecture_setup: PASSED")
        return True
    except Exception as e:
        print(f"❌ test_progressive_context_architecture_setup: FAILED - {e}")
        return False

def main():
    """Run all validation tests"""
    print("🔬 Running Phase 0 Implementation Validation Tests")
    print("=" * 60)
    
    tests = [
        test_version_intelligence_service_exists,
        test_foundation_context_creation,
        test_foundation_context_completeness,
        test_phase_0_generates_actual_files,
        test_phase_0_input_output_flow,
        test_phase_0_version_gap_analysis,
        test_progressive_context_architecture_setup
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All Phase 0 implementation tests passed!")
        print("✅ Phase 0 traditional foundation is ready for agent integration")
    else:
        print(f"❌ {failed} tests failed - implementation needs fixes")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)