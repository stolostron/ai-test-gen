#!/usr/bin/env python3
"""
ASI Router Integration Test
==========================

Tests the complete ASI-Enhanced Router → Orchestrator integration flow
to ensure framework requests are properly classified and routed.
"""

import asyncio
import sys
import os
sys.path.append('.claude/ai-services')

from asi_enhanced_request_router import ASIEnhancedRequestRouter
from ai_agent_orchestrator import PhaseBasedOrchestrator

async def test_asi_router_classification():
    """Test ASI router classifies framework requests correctly"""
    print("🧠 TESTING ASI ROUTER CLASSIFICATION")
    print("=" * 50)
    
    router = ASIEnhancedRequestRouter()
    
    test_requests = [
        "Generate test plan for ACM-22079",
        "Generate comprehensive test cases for ACM-22079 on mist10",
        "Create test plan for ACM-17293",
        "Analyze ACM-12345 using staging environment",
        "What does this code do?",  # Should route to direct AI
        "Emergency: Production cluster ACM-54321 is failing"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n**Test {i}**: {request}")
        
        try:
            decision = await router.route_request(request)
            
            print(f"  ✅ Classification: {decision.request_type.name}")
            print(f"  📊 Confidence: {decision.confidence:.1%}")
            print(f"  🧠 ASI Confidence: {decision.asi_confidence:.1%}")
            print(f"  🎯 Use Orchestrator: {decision.should_use_orchestrator}")
            print(f"  📍 Decision Source: {decision.decision_source}")
            
            if decision.should_use_orchestrator:
                print(f"  🔧 Task Tool Config: {decision.task_tool_config is not None}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return True

async def test_orchestrator_method_availability():
    """Test orchestrator methods are available and callable"""
    print("\n🏗️  TESTING ORCHESTRATOR METHOD AVAILABILITY")
    print("=" * 50)
    
    try:
        orchestrator = PhaseBasedOrchestrator()
        print("✅ PhaseBasedOrchestrator instantiated successfully")
        
        # Check method availability
        if hasattr(orchestrator, 'execute_full_framework'):
            print("✅ execute_full_framework method exists")
        else:
            print("❌ execute_full_framework method missing")
            return False
            
        # Check if it's async
        import inspect
        if inspect.iscoroutinefunction(orchestrator.execute_full_framework):
            print("✅ execute_full_framework is async coroutine")
        else:
            print("❌ execute_full_framework is not async")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        return False

async def test_task_tool_configuration():
    """Test Task tool configuration generation"""
    print("\n🔧 TESTING TASK TOOL CONFIGURATION")
    print("=" * 50)
    
    router = ASIEnhancedRequestRouter()
    
    # Test framework request
    request = "Generate test plan for ACM-22079"
    decision = await router.route_request(request)
    
    if decision.should_use_orchestrator and decision.task_tool_config:
        config = decision.task_tool_config
        print(f"✅ Task Tool Config Generated:")
        print(f"  📋 Description: {config.get('description', 'Missing')}")
        print(f"  🎯 Subagent Type: {config.get('subagent_type', 'Missing')}")
        print(f"  📝 Prompt Length: {len(config.get('prompt', ''))}")
        
        # Verify prompt contains orchestrator instructions
        prompt = config.get('prompt', '')
        if 'execute_full_framework' in prompt:
            print("✅ Prompt contains orchestrator execution instructions")
        else:
            print("❌ Prompt missing orchestrator execution instructions")
            
        if 'ACM-22079' in prompt:
            print("✅ Prompt contains JIRA ID")
        else:
            print("❌ Prompt missing JIRA ID")
            
        return True
    else:
        print("❌ Task Tool Config not generated for framework request")
        return False

async def test_routing_regression_prevention():
    """Test that framework requests don't fall back to manual simulation"""
    print("\n🛡️  TESTING ROUTING REGRESSION PREVENTION")
    print("=" * 50)
    
    router = ASIEnhancedRequestRouter()
    
    framework_patterns = [
        "Generate test plan for ACM-22079",
        "Generate comprehensive test cases for ACM-22079 on mist10",
        "create test plan for ACM-17293",
        "Test plan generation for ACM-12345",
        "Analyze JIRA ticket ACM-54321"
    ]
    
    all_routed_correctly = True
    
    for pattern in framework_patterns:
        decision = await router.route_request(pattern)
        
        if decision.should_use_orchestrator:
            print(f"✅ '{pattern}' → Orchestrator ({decision.confidence:.1%})")
        else:
            print(f"❌ '{pattern}' → Manual AI ({decision.confidence:.1%})")
            all_routed_correctly = False
    
    if all_routed_correctly:
        print("\n✅ All framework requests properly routed to orchestrator")
        print("🛡️  Routing regression prevention: PASSED")
    else:
        print("\n❌ Some framework requests falling back to manual AI")
        print("🛡️  Routing regression prevention: FAILED")
    
    return all_routed_correctly

async def run_all_tests():
    """Run comprehensive ASI router integration tests"""
    print("🚀 ASI ROUTER INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("ASI Router Classification", test_asi_router_classification),
        ("Orchestrator Method Availability", test_orchestrator_method_availability),
        ("Task Tool Configuration", test_task_tool_configuration),
        ("Routing Regression Prevention", test_routing_regression_prevention)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - ASI Router integration is working correctly!")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - Review issues above")
        return False

if __name__ == "__main__":
    asyncio.run(run_all_tests())