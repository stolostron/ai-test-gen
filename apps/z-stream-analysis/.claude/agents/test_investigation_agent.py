#!/usr/bin/env python3
"""
Test script for Investigation Intelligence Agent
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

from investigation_intelligence_agent import (
    InvestigationIntelligenceAgent,
    InvestigationContext,
    create_investigation_intelligence_agent
)

async def test_agent_initialization():
    """Test agent initialization and configuration loading"""
    print("🔧 Testing agent initialization...")
    
    try:
        agent = create_investigation_intelligence_agent()
        
        # Verify agent properties
        assert agent.agent_id == "investigation_intelligence_agent"
        assert agent.agent_name == "Investigation Intelligence Agent"
        assert agent.agent_type == "investigation_specialist"
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
        # Create test context
        test_context = InvestigationContext(
            investigation_id="test_inv_001",
            jenkins_url="https://jenkins.example.com/job/test/123/",
            build_id="123",
            investigation_scope="full",
            environment_context={"cluster_url": "https://test-cluster.example.com"},
            conversation_id="test_conv_001",
            session_id="test_session_001",
            user_context={"user_id": "test_user"},
            investigation_history=[],
            agent_memory={},
            execution_constraints={"max_tokens": 4000},
            performance_requirements={"timeout": 120}
        )
        
        # Generate system prompt
        prompt = agent.get_system_prompt(test_context)
        
        # Verify prompt contains expected elements
        assert "Investigation Intelligence Agent" in prompt
        assert test_context.investigation_id in prompt
        assert test_context.jenkins_url in prompt
        assert "CURRENT INVESTIGATION CONTEXT" in prompt
        
        print("✅ System prompt generation successful")
        print(f"📏 Prompt length: {len(prompt)} characters")
        return True
        
    except Exception as e:
        print(f"❌ System prompt generation failed: {str(e)}")
        traceback.print_exc()
        return False

async def test_investigation_operation(agent):
    """Test investigation operation execution"""
    print("🔍 Testing investigation operation...")
    
    try:
        # Create test context
        test_context = InvestigationContext(
            investigation_id="test_inv_002",
            jenkins_url="https://jenkins.example.com/job/test/456/",
            build_id="456",
            investigation_scope="targeted",
            environment_context={"cluster_url": "https://test-cluster.example.com"},
            conversation_id="test_conv_002",
            session_id="test_session_002",
            user_context={"user_id": "test_user"},
            investigation_history=[],
            agent_memory={},
            execution_constraints={"max_tokens": 4000},
            performance_requirements={"timeout": 120}
        )
        
        # Test parameters
        test_parameters = {
            "jenkins_url": "https://jenkins.example.com/job/test/456/",
            "build_id": "456",
            "investigation_scope": "targeted"
        }
        
        # Execute investigation operation
        result = await agent.execute_operation(
            operation="investigate_pipeline_failure",
            parameters=test_parameters,
            context=test_context
        )
        
        # Verify result structure
        assert hasattr(result, 'investigation_id')
        assert hasattr(result, 'jenkins_analysis')
        assert hasattr(result, 'environment_assessment')
        assert hasattr(result, 'repository_intelligence')
        assert hasattr(result, 'evidence_correlation')
        assert hasattr(result, 'investigation_confidence')
        assert hasattr(result, 'evidence_quality_score')
        assert hasattr(result, 'solution_readiness')
        
        # Verify result values
        assert result.investigation_id == test_context.investigation_id
        assert isinstance(result.investigation_confidence, float)
        assert 0.0 <= result.investigation_confidence <= 1.0
        assert isinstance(result.evidence_quality_score, float)
        assert 0.0 <= result.evidence_quality_score <= 1.0
        assert isinstance(result.solution_readiness, bool)
        
        print("✅ Investigation operation successful")
        print(f"📊 Investigation confidence: {result.investigation_confidence:.2f}")
        print(f"📊 Evidence quality score: {result.evidence_quality_score:.2f}")
        print(f"📊 Solution readiness: {result.solution_readiness}")
        return result
        
    except Exception as e:
        print(f"❌ Investigation operation failed: {str(e)}")
        traceback.print_exc()
        return None

async def test_individual_operations(agent):
    """Test individual investigation operations"""
    print("🧪 Testing individual operations...")
    
    try:
        # Create test context
        test_context = InvestigationContext(
            investigation_id="test_inv_003",
            jenkins_url="https://jenkins.example.com/job/test/789/",
            build_id="789",
            investigation_scope="rapid",
            environment_context={},
            conversation_id="test_conv_003",
            session_id="test_session_003", 
            user_context={},
            investigation_history=[],
            agent_memory={},
            execution_constraints={},
            performance_requirements={}
        )
        
        test_parameters = {"jenkins_url": "https://jenkins.example.com/job/test/789/"}
        
        # Test individual operations
        operations = [
            "jenkins_intelligence_extraction",
            "environment_validation_testing",
            "repository_analysis_and_cloning"
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

async def test_agent_memory(agent):
    """Test agent memory functionality"""
    print("🧠 Testing agent memory...")
    
    try:
        # Check initial memory state
        initial_memory_keys = len(agent.conversation_memory)
        
        # Create test context and run investigation (this should store memory)
        test_context = InvestigationContext(
            investigation_id="test_inv_memory",
            jenkins_url="https://jenkins.example.com/job/memory-test/100/",
            build_id="100",
            investigation_scope="full",
            environment_context={},
            conversation_id="memory_test_conv",
            session_id="memory_test_session",
            user_context={},
            investigation_history=[],
            agent_memory={},
            execution_constraints={},
            performance_requirements={}
        )
        
        test_parameters = {
            "jenkins_url": "https://jenkins.example.com/job/memory-test/100/",
            "build_id": "100"
        }
        
        # Execute investigation to trigger memory storage
        result = await agent.execute_operation(
            "investigate_pipeline_failure",
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
        config_path = Path(__file__).parent / "investigation-intelligence-agent.yaml"
        
        if not config_path.exists():
            print(f"❌ Configuration file not found: {config_path}")
            return False
        
        agent = InvestigationIntelligenceAgent(str(config_path))
        
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
    """Run comprehensive test suite for Investigation Intelligence Agent"""
    print("🚀 Starting Investigation Intelligence Agent Comprehensive Test")
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
    
    # Test 4: Investigation Operation
    investigation_result = await test_investigation_operation(agent)
    test_results['investigation_operation'] = investigation_result is not None
    
    # Test 5: Individual Operations
    individual_results = await test_individual_operations(agent)
    test_results['individual_operations'] = individual_results is not None
    
    # Test 6: Agent Memory
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
        print("🎉 All tests passed! Investigation Intelligence Agent is fully functional.")
    else:
        print("⚠️  Some tests failed. Review the errors above.")
    
    return test_results

if __name__ == "__main__":
    # Run the comprehensive test
    asyncio.run(run_comprehensive_test())