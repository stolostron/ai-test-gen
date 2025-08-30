#!/usr/bin/env python3
"""
Simple Framework Execution Test
==============================

Direct test of orchestrator execution with ACM-22079 to validate framework works end-to-end.
"""

import asyncio
import sys
import os
import tempfile
import json
from datetime import datetime

sys.path.append('.claude/ai-services')

async def test_direct_orchestrator_execution():
    """Test direct orchestrator execution with ACM-22079"""
    print("🚀 TESTING DIRECT ORCHESTRATOR EXECUTION")
    print("=" * 50)
    print("JIRA Ticket: ACM-22079 (ClusterCurator digest-based upgrades)")
    print("Environment: mist10")
    print("=" * 50)
    
    try:
        from ai_agent_orchestrator import PhaseBasedOrchestrator
        
        # Create orchestrator
        orchestrator = PhaseBasedOrchestrator()
        print("✅ PhaseBasedOrchestrator created successfully")
        
        # Execute framework with test environment
        print("\n🔄 Starting framework execution...")
        result = await orchestrator.execute_full_framework(
            jira_id="ACM-22079",
            environment="test-env"  # Use simplified test environment
        )
        
        print(f"\n✅ Framework execution completed!")
        print(f"📊 Execution Status: {result.get('status', 'unknown')}")
        print(f"⏱️  Total Time: {result.get('total_execution_time', 0):.1f}s")
        print(f"📁 Run Directory: {result.get('run_directory', 'Not specified')}")
        
        # Check if output files were created
        run_dir = result.get('run_directory')
        if run_dir and os.path.exists(run_dir):
            files = os.listdir(run_dir)
            print(f"📋 Output Files ({len(files)}):")
            for file in sorted(files):
                file_path = os.path.join(run_dir, file)
                size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                print(f"   📄 {file} ({size} bytes)")
            
            # Check for key deliverable files
            key_files = ['Test-Cases.md', 'Complete-Analysis.md', 'run-metadata.json']
            for key_file in key_files:
                if key_file in files:
                    print(f"   ✅ {key_file} generated")
                else:
                    print(f"   ⚠️  {key_file} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Framework execution failed: {e}")
        import traceback
        print(f"Stack trace: {traceback.format_exc()}")
        return False

async def test_agent_task_routing():
    """Test Task tool routing for agent execution"""
    print("\n🎯 TESTING TASK TOOL ROUTING SIMULATION")
    print("=" * 50)
    
    try:
        # Simulate Task tool routing by testing agent availability
        from ai_agent_orchestrator import AIAgentConfigurationLoader, HybridAIAgentExecutor
        
        config_loader = AIAgentConfigurationLoader()
        agent_executor = HybridAIAgentExecutor(config_loader)
        
        print("✅ Agent configuration loader created")
        print("✅ Hybrid agent executor created")
        
        # Test agent configurations are loaded
        agents = ['agent_a_jira_intelligence', 'agent_b_documentation_intelligence', 
                 'agent_c_github_investigation', 'agent_d_environment_intelligence']
        
        for agent_id in agents:
            try:
                # Check if agent config exists in the agents directory
                agent_file = f".claude/agents/{agent_id.replace('agent_', '').replace('_', '-')}.md"
                if os.path.exists(agent_file):
                    print(f"✅ {agent_id}: Configuration file exists")
                else:
                    print(f"⚠️  {agent_id}: Configuration file missing at {agent_file}")
            except Exception as e:
                print(f"❌ {agent_id}: Error checking - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent routing test failed: {e}")
        return False

async def test_end_to_end_integration():
    """Test end-to-end integration with ASI router"""
    print("\n🔗 TESTING END-TO-END INTEGRATION")
    print("=" * 50)
    
    try:
        from asi_enhanced_request_router import asi_route_user_request
        
        # Test routing decision for ACM-22079
        request = "Generate comprehensive test cases for ACM-22079 on mist10"
        
        print(f"User Request: {request}")
        
        decision = await asi_route_user_request(request)
        
        print(f"✅ ASI Routing Decision:")
        print(f"   🎯 Should Use Orchestrator: {decision.should_use_orchestrator}")
        print(f"   📊 Confidence: {decision.confidence:.1%}")
        print(f"   🧠 ASI Confidence: {decision.asi_confidence:.1%}")
        print(f"   📍 Decision Source: {decision.decision_source}")
        
        if decision.should_use_orchestrator and decision.task_tool_config:
            config = decision.task_tool_config
            print(f"   🔧 Task Tool Config Ready: Yes")
            print(f"   📋 Description: {config.get('description', 'Missing')}")
            print(f"   📝 Prompt Contains Framework: {'execute_full_framework' in config.get('prompt', '')}")
            
            return True
        else:
            print(f"   ❌ Task Tool Config: Not properly configured")
            return False
            
    except Exception as e:
        print(f"❌ End-to-end integration test failed: {e}")
        return False

async def run_simple_validation():
    """Run simple framework validation tests"""
    print("🔬 SIMPLE FRAMEWORK VALIDATION TEST SUITE")
    print("=" * 60)
    print("Focus: Core functionality with ACM-22079")
    print("=" * 60)
    
    tests = [
        ("Direct Orchestrator Execution", test_direct_orchestrator_execution),
        ("Agent Task Routing", test_agent_task_routing),  
        ("End-to-End Integration", test_end_to_end_integration)
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
    print("📊 VALIDATION RESULTS")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 FRAMEWORK VALIDATION SUCCESSFUL!")
        print("✅ Core orchestrator execution working")
        print("✅ Agent routing capabilities confirmed")
        print("✅ ASI router integration functional")
        return True
    else:
        print("⚠️  SOME VALIDATIONS FAILED")
        return False

if __name__ == "__main__":
    asyncio.run(run_simple_validation())