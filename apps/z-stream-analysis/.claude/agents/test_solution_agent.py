#!/usr/bin/env python3
"""
Test script for Solution Intelligence Agent
Validates that the agent is properly implemented and functional
"""

import asyncio
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from solution_intelligence_agent import (
    SolutionIntelligenceAgent,
    SolutionContext,
    ClassificationType,
    BusinessImpactLevel,
    EscalationUrgency,
    create_solution_intelligence_agent
)

async def test_agent_initialization():
    """Test agent initialization and configuration loading"""
    print("🔧 Testing agent initialization...")
    
    try:
        agent = create_solution_intelligence_agent()
        
        # Verify agent properties
        assert agent.agent_id == "solution_intelligence_agent"
        assert agent.agent_name == "Solution Intelligence Agent"
        assert agent.agent_type == "solution_specialist"
        assert hasattr(agent, 'capabilities')
        assert hasattr(agent, 'config')
        
        print("✅ Agent initialization successful")
        return agent
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {str(e)}")
        traceback.print_exc()
        return None

async def test_system_prompt_generation(agent):
    """Test system prompt generation with context"""
    print("📝 Testing system prompt generation...")
    
    try:
        # Create test investigation context
        test_investigation_context = {
            "investigation_id": "test_inv_001",
            "jenkins_analysis": {"build_metadata": {"status": "FAILURE"}},
            "environment_assessment": {"connectivity_results": {"cluster_api_accessible": True}},
            "repository_intelligence": {"repository_analysis": {"clone_successful": True}},
            "evidence_correlation": {"cross_source_validation": {"overall_consistency": "high"}},
            "investigation_confidence": 0.9,
            "evidence_quality_score": 0.85,
            "solution_readiness": True
        }
        
        # Create test context
        test_context = SolutionContext(
            solution_id="test_sol_001",
            investigation_context=test_investigation_context,
            analysis_scope="comprehensive",
            business_context={"customer_impact": "medium", "escalation_urgency": "standard"},
            conversation_id="test_conv_001",
            session_id="test_session_001",
            user_context={"user_id": "test_user"},
            solution_history=[],
            agent_memory={},
            execution_constraints={"max_tokens": 4000},
            performance_requirements={"timeout": 120}
        )
        
        # Generate system prompt
        prompt = agent.get_system_prompt(test_context)
        
        # Verify prompt contains expected elements
        assert "Solution Intelligence Agent" in prompt
        assert test_context.solution_id in prompt
        assert "CURRENT SOLUTION CONTEXT" in prompt
        assert "INVESTIGATION CONTEXT INHERITANCE" in prompt
        
        print("✅ System prompt generation successful")
        print(f"📏 Prompt length: {len(prompt)} characters")
        return True
        
    except Exception as e:
        print(f"❌ System prompt generation failed: {str(e)}")
        traceback.print_exc()
        return False

async def test_solution_operation(agent):
    """Test solution operation execution"""
    print("🔍 Testing solution operation...")
    
    try:
        # Create test investigation context
        test_investigation_context = {
            "investigation_id": "test_inv_002",
            "jenkins_analysis": {
                "build_metadata": {"status": "FAILURE", "url": "https://jenkins.example.com/job/test/456/"},
                "console_analysis": {"error_patterns": ["timeout", "assertion_failed"]},
                "extraction_confidence": 0.9
            },
            "environment_assessment": {
                "connectivity_results": {"cluster_api_accessible": True},
                "product_functionality": {"core_features_working": True},
                "validation_confidence": 0.95
            },
            "repository_intelligence": {
                "repository_analysis": {"clone_successful": True, "code_analysis_complete": True},
                "prerequisite_mapping": {"dependency_chain": [], "missing_prerequisites": []},
                "analysis_confidence": 0.85
            },
            "evidence_correlation": {
                "cross_source_validation": {"overall_consistency": "high"},
                "correlation_confidence": 0.9
            },
            "investigation_confidence": 0.9,
            "evidence_quality_score": 0.88,
            "solution_readiness": True
        }
        
        # Create test context
        test_context = SolutionContext(
            solution_id="test_sol_002",
            investigation_context=test_investigation_context,
            analysis_scope="comprehensive",
            business_context={"customer_impact": "high", "escalation_urgency": "immediate"},
            conversation_id="test_conv_002",
            session_id="test_session_002",
            user_context={"user_id": "test_user"},
            solution_history=[],
            agent_memory={},
            execution_constraints={"max_tokens": 4000},
            performance_requirements={"timeout": 120}
        )
        
        # Test parameters
        test_parameters = {
            "investigation_context": test_investigation_context,
            "analysis_scope": "comprehensive",
            "business_context": {"customer_impact": "high"}
        }
        
        # Execute solution operation
        result = await agent.execute_operation(
            operation="analyze_and_generate_solution",
            parameters=test_parameters,
            context=test_context
        )
        
        # Verify result structure
        assert hasattr(result, 'solution_id')
        assert hasattr(result, 'classification_report')
        assert hasattr(result, 'solution_package')
        assert hasattr(result, 'implementation_guidance')
        assert hasattr(result, 'business_impact_assessment')
        assert hasattr(result, 'solution_confidence')
        assert hasattr(result, 'implementation_feasibility')
        assert hasattr(result, 'business_impact_score')
        
        # Verify result values
        assert result.solution_id == test_context.solution_id
        assert isinstance(result.solution_confidence, float)
        assert 0.0 <= result.solution_confidence <= 1.0
        assert isinstance(result.implementation_feasibility, float)
        assert 0.0 <= result.implementation_feasibility <= 1.0
        assert isinstance(result.business_impact_score, float)
        assert 0.0 <= result.business_impact_score <= 1.0
        assert isinstance(result.classification_report.primary_classification, ClassificationType)
        
        print("✅ Solution operation successful")
        print(f"📊 Classification: {result.classification_report.primary_classification.value}")
        print(f"📊 Solution confidence: {result.solution_confidence:.2f}")
        print(f"📊 Implementation feasibility: {result.implementation_feasibility:.2f}")
        print(f"📊 Business impact score: {result.business_impact_score:.2f}")
        return result
        
    except Exception as e:
        print(f"❌ Solution operation failed: {str(e)}")
        traceback.print_exc()
        return None

async def test_individual_operations(agent):
    """Test individual solution operations"""
    print("🧪 Testing individual operations...")
    
    try:
        # Create test investigation context
        test_investigation_context = {
            "investigation_id": "test_inv_003",
            "jenkins_analysis": {"build_metadata": {"status": "FAILURE"}},
            "environment_assessment": {"connectivity_results": {"cluster_api_accessible": True}},
            "repository_intelligence": {"repository_analysis": {"clone_successful": True}},
            "evidence_correlation": {"cross_source_validation": {"overall_consistency": "high"}},
            "investigation_confidence": 0.85,
            "evidence_quality_score": 0.8,
            "solution_readiness": True
        }
        
        # Create test context
        test_context = SolutionContext(
            solution_id="test_sol_003",
            investigation_context=test_investigation_context,
            analysis_scope="targeted",
            business_context={},
            conversation_id="test_conv_003",
            session_id="test_session_003",
            user_context={},
            solution_history=[],
            agent_memory={},
            execution_constraints={},
            performance_requirements={}
        )
        
        test_parameters = {"investigation_context": test_investigation_context}
        
        # Test individual operations
        operations = [
            "evidence_analysis_and_pattern_recognition",
            "definitive_classification_generation",
            "prerequisite_aware_solution_development"
        ]
        
        results = {}
        for operation in operations:
            print(f"  🔄 Testing {operation}...")
            try:
                result = await agent.execute_operation(operation, test_parameters, test_context)
                results[operation] = result
                print(f"  ✅ {operation} successful")
            except Exception as e:
                print(f"  ❌ {operation} failed: {str(e)}")
                results[operation] = None
        
        successful_operations = sum(1 for r in results.values() if r is not None)
        print(f"✅ Individual operations test: {successful_operations}/{len(operations)} successful")
        return results
        
    except Exception as e:
        print(f"❌ Individual operations test failed: {str(e)}")
        traceback.print_exc()
        return None

async def test_classification_types():
    """Test classification type enumeration"""
    print("🏷️  Testing classification types...")
    
    try:
        # Test all classification types
        classifications = [
            ClassificationType.PRODUCT_BUG,
            ClassificationType.AUTOMATION_BUG,
            ClassificationType.AUTOMATION_GAP,
            ClassificationType.MIXED,
            ClassificationType.INFRASTRUCTURE
        ]
        
        for classification in classifications:
            assert isinstance(classification.value, str)
            assert len(classification.value) > 0
        
        print("✅ Classification types validation successful")
        print(f"📊 Available classifications: {[c.value for c in classifications]}")
        return True
        
    except Exception as e:
        print(f"❌ Classification types test failed: {str(e)}")
        traceback.print_exc()
        return False

async def test_agent_memory(agent):
    """Test agent memory functionality"""
    print("🧠 Testing agent memory...")
    
    try:
        # Check initial memory state
        initial_memory_keys = len(agent.conversation_memory)
        
        # Create test investigation context
        test_investigation_context = {
            "investigation_id": "test_inv_memory",
            "jenkins_analysis": {"build_metadata": {"status": "FAILURE"}},
            "environment_assessment": {"connectivity_results": {"cluster_api_accessible": True}},
            "repository_intelligence": {"repository_analysis": {"clone_successful": True}},
            "evidence_correlation": {"cross_source_validation": {"overall_consistency": "high"}},
            "investigation_confidence": 0.9,
            "evidence_quality_score": 0.85,
            "solution_readiness": True
        }
        
        # Create test context and run solution (this should store memory)
        test_context = SolutionContext(
            solution_id="test_sol_memory",
            investigation_context=test_investigation_context,
            analysis_scope="comprehensive",
            business_context={},
            conversation_id="memory_test_conv",
            session_id="memory_test_session",
            user_context={},
            solution_history=[],
            agent_memory={},
            execution_constraints={},
            performance_requirements={}
        )
        
        test_parameters = {
            "investigation_context": test_investigation_context,
            "analysis_scope": "comprehensive"
        }
        
        # Execute solution to trigger memory storage
        result = await agent.execute_operation(
            "analyze_and_generate_solution",
            test_parameters,
            test_context
        )
        
        # Check if memory was stored
        final_memory_keys = len(agent.conversation_memory)
        memory_stored = final_memory_keys > initial_memory_keys
        
        if memory_stored:
            print("✅ Agent memory functionality working")
            print(f"📊 Memory entries: {final_memory_keys}")
        else:
            print("⚠️  Agent memory may not be storing correctly")
        
        return memory_stored
        
    except Exception as e:
        print(f"❌ Agent memory test failed: {str(e)}")
        traceback.print_exc()
        return False

async def test_agent_configuration():
    """Test agent configuration loading and validation"""
    print("⚙️  Testing agent configuration...")
    
    try:
        config_path = Path(__file__).parent / "solution-intelligence-agent.yaml"
        
        if not config_path.exists():
            print(f"❌ Configuration file not found: {config_path}")
            return False
        
        agent = SolutionIntelligenceAgent(str(config_path))
        
        # Verify configuration elements
        assert 'agent_name' in agent.config
        assert 'identity' in agent.config
        assert 'capabilities' in agent.config
        assert 'ai_configuration' in agent.config
        assert 'security' in agent.config
        
        print("✅ Agent configuration validation successful")
        return True
        
    except Exception as e:
        print(f"❌ Agent configuration test failed: {str(e)}")
        traceback.print_exc()
        return False

async def run_comprehensive_test():
    """Run comprehensive test suite for Solution Intelligence Agent"""
    print("🚀 Starting Solution Intelligence Agent Comprehensive Test")
    print("=" * 70)
    
    test_results = {}
    
    # Test 1: Configuration
    test_results['configuration'] = await test_agent_configuration()
    
    # Test 2: Initialization
    agent = await test_agent_initialization()
    test_results['initialization'] = agent is not None
    
    if agent is None:
        print("❌ Cannot continue tests - agent initialization failed")
        return test_results
    
    # Test 3: System Prompt
    test_results['system_prompt'] = await test_system_prompt_generation(agent)
    
    # Test 4: Classification Types
    test_results['classification_types'] = await test_classification_types()
    
    # Test 5: Solution Operation
    solution_result = await test_solution_operation(agent)
    test_results['solution_operation'] = solution_result is not None
    
    # Test 6: Individual Operations
    individual_results = await test_individual_operations(agent)
    test_results['individual_operations'] = individual_results is not None
    
    # Test 7: Agent Memory
    test_results['agent_memory'] = await test_agent_memory(agent)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Solution Intelligence Agent is fully functional.")
    else:
        print("⚠️  Some tests failed. Review the errors above.")
    
    return test_results

if __name__ == "__main__":
    # Run the comprehensive test
    asyncio.run(run_comprehensive_test())