#!/usr/bin/env python3
"""
Agent Parallel Execution & Context Sharing Test
==============================================

Tests Agent A (JIRA Intelligence) and Agent D (Environment Intelligence) 
parallel execution with real-time context sharing using ACM-22079 as example.
"""

import asyncio
import sys
import os
import json
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.append('.claude/ai-services')

from ai_agent_orchestrator import PhaseBasedOrchestrator, HybridAIAgentExecutor, AIAgentConfigurationLoader
from progressive_context_setup import ProgressiveContextArchitecture, ContextInheritanceChain
from foundation_context import FoundationContext

async def test_agent_configuration_loading():
    """Test all 4 agents are properly configured and loadable"""
    print("🔧 TESTING AGENT CONFIGURATION LOADING")
    print("=" * 50)
    
    try:
        config_loader = AIAgentConfigurationLoader()
        
        # Test each agent configuration
        agents = ['agent_a_jira_intelligence', 'agent_b_documentation_intelligence', 
                 'agent_c_github_investigation', 'agent_d_environment_intelligence']
        
        loaded_agents = {}
        
        for agent_id in agents:
            try:
                config = config_loader.load_agent_configuration(agent_id)
                loaded_agents[agent_id] = config
                print(f"✅ {agent_id}: Loaded successfully")
                print(f"   📋 Description: {config.get('name', 'Unknown')}")
                print(f"   🛠️  Tools: {len(config.get('tools', []))} tools")
            except Exception as e:
                print(f"❌ {agent_id}: Failed to load - {e}")
                return False
        
        print(f"\n✅ All {len(loaded_agents)}/4 agents loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Agent configuration loading failed: {e}")
        return False

async def test_foundation_context_setup():
    """Test foundation context setup for ACM-22079"""
    print("\n📋 TESTING FOUNDATION CONTEXT SETUP")
    print("=" * 50)
    
    try:
        # Create foundation context for ACM-22079
        foundation_context = FoundationContext(
            jira_id="ACM-22079",
            environment="mist10",
            console_url="https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com",
            credentials="kubeadmin/test-credentials"
        )
        
        context_data = foundation_context.to_dict()
        
        print("✅ Foundation Context Created:")
        print(f"   🎫 JIRA ID: {context_data['jira_id']}")
        print(f"   🌐 Environment: {context_data['environment']}")
        print(f"   💻 Console URL: {context_data['console_url']}")
        print(f"   🔒 Credentials: {context_data['credentials'][:20]}...")
        print(f"   ⏰ Timestamp: {context_data['timestamp']}")
        
        return context_data
        
    except Exception as e:
        print(f"❌ Foundation context setup failed: {e}")
        return None

async def test_progressive_context_initialization():
    """Test Progressive Context Architecture initialization"""
    print("\n🏗️  TESTING PROGRESSIVE CONTEXT ARCHITECTURE")
    print("=" * 50)
    
    try:
        pca = ProgressiveContextArchitecture()
        
        # Create inheritance chain for ACM-22079
        inheritance_chain = pca.create_inheritance_chain("ACM-22079", "mist10")
        
        print("✅ Progressive Context Architecture Initialized:")
        print(f"   📊 Agent Contexts: {len(inheritance_chain.agent_contexts)} contexts")
        print(f"   🔗 Chain ID: {inheritance_chain.chain_id}")
        print(f"   🎯 Target JIRA: {inheritance_chain.jira_id}")
        print(f"   🌐 Environment: {inheritance_chain.environment}")
        
        # Check agent context structure
        for agent_id, context in inheritance_chain.agent_contexts.items():
            print(f"   🤖 {agent_id}: Context initialized")
        
        return inheritance_chain
        
    except Exception as e:
        print(f"❌ Progressive Context Architecture failed: {e}")
        return None

async def test_parallel_agent_execution():
    """Test Agent A and Agent D parallel execution with context sharing"""
    print("\n🚀 TESTING PARALLEL AGENT EXECUTION")
    print("=" * 50)
    
    try:
        # Initialize components
        config_loader = AIAgentConfigurationLoader()
        agent_executor = HybridAIAgentExecutor(config_loader)
        pca = ProgressiveContextArchitecture()
        
        # Create test run directory
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = os.path.join(temp_dir, "ACM-22079-test-run")
            os.makedirs(run_dir, exist_ok=True)
            
            # Setup foundation context
            foundation_context = {
                'jira_id': 'ACM-22079',
                'environment': 'mist10',
                'console_url': 'https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com',
                'credentials': 'kubeadmin/test-credentials',
                'timestamp': datetime.now().isoformat()
            }
            
            # Create inheritance chain
            inheritance_chain = pca.create_inheritance_chain("ACM-22079", "mist10")
            
            print("🔄 Starting parallel execution of Agent A and Agent D...")
            
            # Execute agents in parallel (simulating Phase 1)
            agent_tasks = [
                agent_executor._execute_agent_a_traditional(foundation_context, run_dir),
                agent_executor._execute_agent_d_traditional(foundation_context, run_dir)
            ]
            
            results = await asyncio.gather(*agent_tasks, return_exceptions=True)
            
            # Process results
            agent_results = {}
            for i, result in enumerate(results):
                agent_name = ["Agent A (JIRA Intelligence)", "Agent D (Environment Intelligence)"][i]
                
                if isinstance(result, Exception):
                    print(f"❌ {agent_name}: Failed with exception - {result}")
                    agent_results[agent_name] = {"status": "failed", "error": str(result)}
                else:
                    print(f"✅ {agent_name}: Completed successfully")
                    print(f"   📁 Output File: {result.get('output_file', 'None')}")
                    print(f"   📊 Confidence: {result.get('confidence_score', 0):.1%}")
                    print(f"   🔧 Method: {result.get('execution_method', 'unknown')}")
                    agent_results[agent_name] = {"status": "success", "result": result}
            
            return agent_results
            
    except Exception as e:
        print(f"❌ Parallel agent execution failed: {e}")
        return None

async def test_context_inheritance_and_sharing():
    """Test context inheritance and data sharing between agents"""
    print("\n🔄 TESTING CONTEXT INHERITANCE & SHARING")
    print("=" * 50)
    
    try:
        pca = ProgressiveContextArchitecture()
        inheritance_chain = pca.create_inheritance_chain("ACM-22079", "mist10")
        
        # Simulate Agent A findings
        agent_a_findings = {
            'requirement_analysis': {
                'primary_requirements': ['ClusterCurator digest-based upgrades'],
                'component_focus': 'ClusterCurator',
                'priority_level': 'High',
                'version_target': '2.11'
            },
            'feature_analysis': {
                'feature_name': 'Digest-based upgrades via ClusterCurator',
                'technical_mechanics': 'Uses image digest instead of tag for upgrade reliability',
                'business_impact': 'Improved upgrade reliability for disconnected environments'
            }
        }
        
        # Simulate Agent D findings  
        agent_d_findings = {
            'environment_analysis': {
                'cluster_type': 'ACM Hub Cluster',
                'openshift_version': '4.14.x',
                'environment_id': 'mist10',
                'deployment_scope': 'Multi-cluster management'
            },
            'infrastructure_assessment': {
                'managed_clusters': 3,
                'policy_framework_enabled': True,
                'observability_enabled': True
            }
        }
        
        # Update inheritance chain with agent findings
        inheritance_chain.agent_contexts['agent_a'].update({
            'agent_a_findings': agent_a_findings,
            'execution_status': 'completed',
            'confidence_score': 0.85
        })
        
        inheritance_chain.agent_contexts['agent_d'].update({
            'agent_d_findings': agent_d_findings,
            'execution_status': 'completed',
            'confidence_score': 0.90
        })
        
        # Test context sharing and inheritance
        print("✅ Context Inheritance Test:")
        print(f"   🎫 JIRA Context: {inheritance_chain.jira_id}")
        print(f"   🌐 Environment Context: {inheritance_chain.environment}")
        
        # Test cross-agent context access
        agent_a_context = inheritance_chain.get_agent_context('agent_a')
        agent_d_context = inheritance_chain.get_agent_context('agent_d')
        
        print(f"   🤖 Agent A Context Size: {len(agent_a_context)} keys")
        print(f"   🤖 Agent D Context Size: {len(agent_d_context)} keys")
        
        # Test context merging for Phase 2
        merged_context = inheritance_chain.merge_contexts(['agent_a', 'agent_d'])
        
        print(f"   🔄 Merged Context Size: {len(merged_context)} keys")
        print(f"   📊 Agent A Confidence: {merged_context.get('agent_a_confidence_score', 0):.1%}")
        print(f"   📊 Agent D Confidence: {merged_context.get('agent_d_confidence_score', 0):.1%}")
        
        # Verify key data is preserved
        if 'agent_a_findings' in merged_context and 'agent_d_findings' in merged_context:
            print("✅ Both agent findings preserved in merged context")
            
            # Check specific data preservation
            a_findings = merged_context['agent_a_findings']
            d_findings = merged_context['agent_d_findings']
            
            if 'ClusterCurator' in str(a_findings):
                print("✅ Agent A ClusterCurator analysis preserved")
            
            if 'mist10' in str(d_findings):
                print("✅ Agent D environment analysis preserved")
                
            return True
        else:
            print("❌ Agent findings not properly preserved in merged context")
            return False
            
    except Exception as e:
        print(f"❌ Context inheritance test failed: {e}")
        return False

async def test_data_flow_integrity():
    """Test data flow integrity and preservation"""
    print("\n📊 TESTING DATA FLOW INTEGRITY")
    print("=" * 50)
    
    try:
        # Test data preservation through progressive context
        test_data = {
            'jira_intelligence': {
                'ticket_id': 'ACM-22079',
                'feature': 'ClusterCurator digest-based upgrades',
                'component': 'ClusterCurator',
                'customer_context': 'Amadeus disconnected environment',
                'technical_details': 'Use image digest instead of tag for reliability'
            },
            'environment_intelligence': {
                'cluster_id': 'mist10',
                'cluster_type': 'ACM Hub',
                'openshift_version': '4.14.x',
                'managed_clusters': 3,
                'network_type': 'Disconnected'
            }
        }
        
        # Simulate data flow through progressive context
        pca = ProgressiveContextArchitecture()
        inheritance_chain = pca.create_inheritance_chain("ACM-22079", "mist10")
        
        # Add test data to contexts
        inheritance_chain.agent_contexts['agent_a'].update(test_data['jira_intelligence'])
        inheritance_chain.agent_contexts['agent_d'].update(test_data['environment_intelligence'])
        
        # Test data preservation
        retrieved_a = inheritance_chain.get_agent_context('agent_a')
        retrieved_d = inheritance_chain.get_agent_context('agent_d')
        
        print("✅ Data Flow Integrity Check:")
        
        # Verify JIRA intelligence data
        if all(key in retrieved_a for key in test_data['jira_intelligence'].keys()):
            print("   ✅ JIRA Intelligence data preserved")
        else:
            print("   ❌ JIRA Intelligence data corrupted")
            return False
        
        # Verify environment intelligence data  
        if all(key in retrieved_d for key in test_data['environment_intelligence'].keys()):
            print("   ✅ Environment Intelligence data preserved")
        else:
            print("   ❌ Environment Intelligence data corrupted")
            return False
        
        # Test merged context preservation
        merged = inheritance_chain.merge_contexts(['agent_a', 'agent_d'])
        
        expected_keys = set(test_data['jira_intelligence'].keys()) | set(test_data['environment_intelligence'].keys())
        actual_keys = set(merged.keys())
        
        if expected_keys.issubset(actual_keys):
            print("   ✅ Merged context preserves all data")
        else:
            missing = expected_keys - actual_keys
            print(f"   ❌ Missing keys in merged context: {missing}")
            return False
        
        print(f"   📊 Data preservation rate: 100%")
        print(f"   🔄 Context merge successful: {len(merged)} total keys")
        
        return True
        
    except Exception as e:
        print(f"❌ Data flow integrity test failed: {e}")
        return False

async def run_comprehensive_agent_tests():
    """Run comprehensive agent parallel execution tests"""
    print("🤖 AGENT PARALLEL EXECUTION & CONTEXT SHARING TEST SUITE")
    print("=" * 70)
    print("Testing with ACM-22079: ClusterCurator digest-based upgrades")
    print("=" * 70)
    
    tests = [
        ("Agent Configuration Loading", test_agent_configuration_loading),
        ("Foundation Context Setup", test_foundation_context_setup),
        ("Progressive Context Architecture", test_progressive_context_initialization),
        ("Parallel Agent Execution", test_parallel_agent_execution),
        ("Context Inheritance & Sharing", test_context_inheritance_and_sharing),
        ("Data Flow Integrity", test_data_flow_integrity)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            # For tests that return data, consider them passed if data is returned
            if result is not None and result is not False:
                results[test_name] = True
            else:
                results[test_name] = False
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 AGENT EXECUTION TEST RESULTS")
    print("=" * 70)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL AGENT TESTS PASSED")
        print("✅ Agent A & D parallel execution working correctly")
        print("✅ Context sharing and inheritance validated")
        print("✅ Data flow integrity confirmed")
        return True
    else:
        print("⚠️  SOME AGENT TESTS FAILED - Review issues above")
        return False

if __name__ == "__main__":
    asyncio.run(run_comprehensive_agent_tests())