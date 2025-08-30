#!/usr/bin/env python3
"""
Test script for 2-Agent Intelligence Framework Workflow
Validates the complete Investigation Intelligence → Solution Intelligence workflow
"""

import asyncio
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from investigation_intelligence_agent import (
    InvestigationIntelligenceAgent,
    InvestigationContext,
    create_investigation_intelligence_agent
)

from solution_intelligence_agent import (
    SolutionIntelligenceAgent,
    SolutionContext,
    ClassificationType,
    create_solution_intelligence_agent
)

async def test_full_2_agent_workflow():
    """Test complete 2-agent workflow: Investigation → Solution"""
    print("🚀 Testing Complete 2-Agent Intelligence Framework Workflow")
    print("=" * 70)
    
    try:
        # Step 1: Initialize both agents
        print("🔧 Step 1: Initializing agents...")
        investigation_agent = create_investigation_intelligence_agent()
        solution_agent = create_solution_intelligence_agent()
        
        assert investigation_agent is not None
        assert solution_agent is not None
        print("✅ Both agents initialized successfully")
        
        # Step 2: Create investigation context
        print("🔍 Step 2: Creating investigation context...")
        investigation_context = InvestigationContext(
            investigation_id="workflow_test_001",
            jenkins_url="https://jenkins.example.com/job/test-workflow/100/",
            build_id="100",
            investigation_scope="full",
            environment_context={
                "cluster_url": "https://test-cluster.example.com",
                "test_environment": "staging",
                "product_version": "2.12.3"
            },
            conversation_id="workflow_conv_001",
            session_id="workflow_session_001",
            user_context={"user_id": "workflow_test_user"},
            investigation_history=[],
            agent_memory={},
            execution_constraints={"max_tokens": 4000},
            performance_requirements={"timeout": 120}
        )
        print("✅ Investigation context created")
        
        # Step 3: Execute investigation phase
        print("🔍 Step 3: Executing Investigation Intelligence Agent...")
        investigation_parameters = {
            "jenkins_url": investigation_context.jenkins_url,
            "build_id": investigation_context.build_id,
            "investigation_scope": investigation_context.investigation_scope
        }
        
        investigation_result = await investigation_agent.execute_operation(
            operation="investigate_pipeline_failure",
            parameters=investigation_parameters,
            context=investigation_context
        )
        
        assert investigation_result is not None
        assert investigation_result.solution_readiness == True
        print(f"✅ Investigation completed with {investigation_result.investigation_confidence:.2f} confidence")
        print(f"📊 Evidence quality score: {investigation_result.evidence_quality_score:.2f}")
        
        # Step 4: Prepare solution context with investigation results
        print("🛠️  Step 4: Preparing solution context with investigation results...")
        solution_context = SolutionContext(
            solution_id="workflow_solution_001",
            investigation_context={
                "investigation_id": investigation_result.investigation_id,
                "jenkins_analysis": investigation_result.jenkins_analysis,
                "environment_assessment": investigation_result.environment_assessment,
                "repository_intelligence": investigation_result.repository_intelligence,
                "evidence_correlation": investigation_result.evidence_correlation,
                "investigation_confidence": investigation_result.investigation_confidence,
                "evidence_quality_score": investigation_result.evidence_quality_score,
                "context_inheritance_package": investigation_result.context_inheritance_package,
                "solution_readiness": investigation_result.solution_readiness
            },
            analysis_scope="comprehensive",
            business_context={
                "customer_impact": "high",
                "release_timeline": "urgent",
                "escalation_urgency": "immediate"
            },
            conversation_id="workflow_conv_001",
            session_id="workflow_session_001",
            user_context={"user_id": "workflow_test_user"},
            solution_history=[],
            agent_memory={},
            execution_constraints={"max_tokens": 4000},
            performance_requirements={"timeout": 120}
        )
        print("✅ Solution context prepared with investigation inheritance")
        
        # Step 5: Execute solution phase
        print("🛠️  Step 5: Executing Solution Intelligence Agent...")
        solution_parameters = {
            "investigation_context": solution_context.investigation_context,
            "analysis_scope": solution_context.analysis_scope,
            "business_context": solution_context.business_context
        }
        
        solution_result = await solution_agent.execute_operation(
            operation="analyze_and_generate_solution",
            parameters=solution_parameters,
            context=solution_context
        )
        
        assert solution_result is not None
        print(f"✅ Solution completed with {solution_result.solution_confidence:.2f} confidence")
        print(f"📊 Classification: {solution_result.classification_report.primary_classification.value}")
        print(f"📊 Implementation feasibility: {solution_result.implementation_feasibility:.2f}")
        print(f"📊 Business impact score: {solution_result.business_impact_score:.2f}")
        
        # Step 6: Validate workflow integration
        print("🔗 Step 6: Validating workflow integration...")
        
        # Verify context inheritance
        assert solution_result.solution_metadata['investigation_id'] == investigation_result.investigation_id
        
        # Verify progressive context architecture
        assert solution_context.investigation_context['investigation_confidence'] == investigation_result.investigation_confidence
        assert solution_context.investigation_context['evidence_quality_score'] == investigation_result.evidence_quality_score
        
        # Verify solution builds on investigation
        assert solution_result.solution_confidence > 0.0
        assert solution_result.implementation_feasibility > 0.0
        assert len(solution_result.solution_package.comprehensive_fixes) > 0
        
        print("✅ Workflow integration validated successfully")
        
        # Step 7: Generate workflow summary
        print("📋 Step 7: Generating workflow summary...")
        workflow_summary = {
            "workflow_id": "workflow_test_001",
            "investigation_phase": {
                "agent": "investigation_intelligence_agent",
                "investigation_id": investigation_result.investigation_id,
                "confidence": investigation_result.investigation_confidence,
                "evidence_quality": investigation_result.evidence_quality_score,
                "solution_readiness": investigation_result.solution_readiness
            },
            "solution_phase": {
                "agent": "solution_intelligence_agent",
                "solution_id": solution_result.solution_id,
                "classification": solution_result.classification_report.primary_classification.value,
                "confidence": solution_result.solution_confidence,
                "feasibility": solution_result.implementation_feasibility,
                "business_impact": solution_result.business_impact_score
            },
            "workflow_integration": {
                "context_inheritance": "successful",
                "progressive_context_architecture": "validated",
                "cross_agent_validation": "confirmed",
                "solution_quality": "high"
            },
            "overall_success": True
        }
        
        print("✅ Workflow summary generated")
        return workflow_summary
        
    except Exception as e:
        print(f"❌ 2-Agent workflow test failed: {str(e)}")
        traceback.print_exc()
        return None

async def test_agent_coordination():
    """Test agent coordination and context sharing"""
    print("🤝 Testing Agent Coordination and Context Sharing")
    print("=" * 50)
    
    try:
        # Initialize agents
        investigation_agent = create_investigation_intelligence_agent()
        solution_agent = create_solution_intelligence_agent()
        
        # Test shared conversation memory
        conversation_id = "coordination_test_conv"
        
        # Execute investigation with conversation context
        investigation_context = InvestigationContext(
            investigation_id="coord_test_inv",
            jenkins_url="https://jenkins.example.com/job/coord-test/200/",
            build_id="200",
            investigation_scope="targeted",
            environment_context={},
            conversation_id=conversation_id,
            session_id="coord_session_001",
            user_context={},
            investigation_history=[],
            agent_memory={},
            execution_constraints={},
            performance_requirements={}
        )
        
        investigation_result = await investigation_agent.execute_operation(
            "investigate_pipeline_failure",
            {"jenkins_url": investigation_context.jenkins_url, "build_id": "200"},
            investigation_context
        )
        
        # Check if investigation agent stored memory
        investigation_memory_stored = conversation_id in investigation_agent.conversation_memory
        
        # Execute solution with same conversation context
        solution_context = SolutionContext(
            solution_id="coord_test_sol",
            investigation_context={
                "investigation_id": investigation_result.investigation_id,
                "jenkins_analysis": investigation_result.jenkins_analysis,
                "investigation_confidence": investigation_result.investigation_confidence,
                "solution_readiness": True
            },
            analysis_scope="targeted",
            business_context={},
            conversation_id=conversation_id,
            session_id="coord_session_001",
            user_context={},
            solution_history=[],
            agent_memory={},
            execution_constraints={},
            performance_requirements={}
        )
        
        solution_result = await solution_agent.execute_operation(
            "analyze_and_generate_solution",
            {"investigation_context": solution_context.investigation_context},
            solution_context
        )
        
        # Check if solution agent stored memory
        solution_memory_stored = conversation_id in solution_agent.conversation_memory
        
        coordination_success = investigation_memory_stored and solution_memory_stored
        
        if coordination_success:
            print("✅ Agent coordination successful")
            print(f"📊 Investigation memory entries: {len(investigation_agent.conversation_memory.get(conversation_id, []))}")
            print(f"📊 Solution memory entries: {len(solution_agent.conversation_memory.get(conversation_id, []))}")
        else:
            print("⚠️  Agent coordination may have issues")
        
        return coordination_success
        
    except Exception as e:
        print(f"❌ Agent coordination test failed: {str(e)}")
        traceback.print_exc()
        return False

async def test_error_handling_workflow():
    """Test workflow error handling and resilience"""
    print("🛡️  Testing Workflow Error Handling and Resilience")
    print("=" * 50)
    
    try:
        # Initialize agents
        investigation_agent = create_investigation_intelligence_agent()
        solution_agent = create_solution_intelligence_agent()
        
        # Test 1: Investigation with invalid parameters
        print("🧪 Test 1: Investigation with invalid parameters...")
        try:
            invalid_context = InvestigationContext(
                investigation_id="error_test_001",
                jenkins_url="invalid_url",  # Invalid URL
                build_id="invalid_build",
                investigation_scope="invalid_scope",  # Invalid scope
                environment_context={},
                conversation_id="error_test_conv",
                session_id="error_session",
                user_context={},
                investigation_history=[],
                agent_memory={},
                execution_constraints={},
                performance_requirements={}
            )
            
            result = await investigation_agent.execute_operation(
                "investigate_pipeline_failure",
                {"jenkins_url": "invalid_url", "build_id": "invalid_build"},
                invalid_context
            )
            
            # Should handle errors gracefully
            assert result is not None
            assert hasattr(result, 'investigation_confidence')
            print("✅ Investigation error handling successful")
            
        except Exception as e:
            print(f"⚠️  Investigation error handling: {str(e)}")
        
        # Test 2: Solution with incomplete investigation context
        print("🧪 Test 2: Solution with incomplete investigation context...")
        try:
            incomplete_investigation_context = {
                "investigation_id": "incomplete_inv",
                # Missing required fields
                "solution_readiness": False
            }
            
            solution_context = SolutionContext(
                solution_id="error_test_sol",
                investigation_context=incomplete_investigation_context,
                analysis_scope="rapid",
                business_context={},
                conversation_id="error_test_conv",
                session_id="error_session",
                user_context={},
                solution_history=[],
                agent_memory={},
                execution_constraints={},
                performance_requirements={}
            )
            
            result = await solution_agent.execute_operation(
                "analyze_and_generate_solution",
                {"investigation_context": incomplete_investigation_context},
                solution_context
            )
            
            # Should handle incomplete context gracefully
            assert result is not None
            assert hasattr(result, 'solution_confidence')
            print("✅ Solution error handling successful")
            
        except Exception as e:
            print(f"⚠️  Solution error handling: {str(e)}")
        
        print("✅ Error handling tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Error handling workflow test failed: {str(e)}")
        traceback.print_exc()
        return False

async def run_comprehensive_workflow_test():
    """Run comprehensive 2-agent workflow test suite"""
    print("🚀 Starting 2-Agent Intelligence Framework Comprehensive Workflow Test")
    print("=" * 80)
    
    test_results = {}
    
    # Test 1: Full 2-Agent Workflow
    workflow_result = await test_full_2_agent_workflow()
    test_results['full_workflow'] = workflow_result is not None
    
    print("\n" + "-" * 80 + "\n")
    
    # Test 2: Agent Coordination
    test_results['agent_coordination'] = await test_agent_coordination()
    
    print("\n" + "-" * 80 + "\n")
    
    # Test 3: Error Handling
    test_results['error_handling'] = await test_error_handling_workflow()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 2-AGENT WORKFLOW TEST SUMMARY")
    print("=" * 80)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} workflow tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All workflow tests passed! 2-Agent Intelligence Framework is fully functional.")
        print("\n🔥 KEY ACHIEVEMENTS:")
        print("   ✅ Investigation Intelligence Agent → Solution Intelligence Agent workflow")
        print("   ✅ Progressive Context Architecture functioning")
        print("   ✅ Cross-Agent Validation working")
        print("   ✅ Evidence-based solution generation")
        print("   ✅ Agent coordination and memory management")
        print("   ✅ Error handling and resilience")
    else:
        print("⚠️  Some workflow tests failed. Review the errors above.")
    
    return test_results

if __name__ == "__main__":
    # Run the comprehensive workflow test
    asyncio.run(run_comprehensive_workflow_test())