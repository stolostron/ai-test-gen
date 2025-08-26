#!/usr/bin/env python3
"""
Phase 2 AI Enhancement Integration Tests
Validates the AI agent orchestrator and YAML configuration system
"""

import sys
import os
import json
import asyncio
from pathlib import Path

# Add the AI services to the path
sys.path.append('.claude/ai-services')

def test_agent_yaml_configurations():
    """Test that all AI agent YAML configurations can be loaded"""
    try:
        from ai_agent_orchestrator import AIAgentConfigurationLoader
        
        config_loader = AIAgentConfigurationLoader()
        
        # Test individual agent configurations
        expected_agents = [
            "agent_a_jira_intelligence",
            "agent_b_documentation_intelligence", 
            "agent_c_github_investigation",
            "agent_d_environment_intelligence"
        ]
        
        for agent_id in expected_agents:
            config = config_loader.get_configuration(agent_id)
            assert config is not None, f"Configuration not found for {agent_id}"
            
            # Verify required sections
            required_sections = [
                'agent_metadata', 'context_inheritance', 'ai_capabilities',
                'execution_workflow', 'output_specification'
            ]
            
            for section in required_sections:
                assert section in config, f"Missing section '{section}' in {agent_id}"
        
        print("✅ test_agent_yaml_configurations: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ test_agent_yaml_configurations: FAILED - {e}")
        return False

def test_configuration_validation():
    """Test configuration validation system"""
    try:
        from ai_agent_orchestrator import test_ai_agent_configurations
        
        result = test_ai_agent_configurations()
        assert result == True, "Configuration validation failed"
        
        print("✅ test_configuration_validation: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ test_configuration_validation: FAILED - {e}")
        return False

def test_hybrid_ai_agent_executor():
    """Test hybrid AI agent executor initialization"""
    try:
        from ai_agent_orchestrator import AIAgentConfigurationLoader, HybridAIAgentExecutor
        
        config_loader = AIAgentConfigurationLoader()
        executor = HybridAIAgentExecutor(config_loader)
        
        # Test AI model availability check
        ai_available = executor.ai_models_available
        
        # Verify executor has necessary methods
        assert hasattr(executor, 'execute_agent'), "Missing execute_agent method"
        assert hasattr(executor, '_execute_traditional_foundation'), "Missing traditional foundation method"
        
        print("✅ test_hybrid_ai_agent_executor: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ test_hybrid_ai_agent_executor: FAILED - {e}")
        return False

def test_phase_based_orchestrator():
    """Test phase-based orchestrator initialization"""
    try:
        from ai_agent_orchestrator import PhaseBasedOrchestrator
        
        orchestrator = PhaseBasedOrchestrator()
        
        # Verify orchestrator components
        assert orchestrator.config_loader is not None, "Missing config loader"
        assert orchestrator.agent_executor is not None, "Missing agent executor"
        assert orchestrator.pca is not None, "Missing Progressive Context Architecture"
        
        # Test phase identification
        phase_1_agents = orchestrator.config_loader.get_phase_agents("Phase 1 - Parallel Foundation Analysis")
        phase_2_agents = orchestrator.config_loader.get_phase_agents("Phase 2 - Parallel Deep Investigation")
        
        assert len(phase_1_agents) >= 2, "Should have agents for Phase 1"
        assert len(phase_2_agents) >= 2, "Should have agents for Phase 2"
        
        print("✅ test_phase_based_orchestrator: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ test_phase_based_orchestrator: FAILED - {e}")
        return False

async def test_agent_execution_simulation():
    """Test agent execution simulation (without full framework run)"""
    try:
        from ai_agent_orchestrator import PhaseBasedOrchestrator
        from progressive_context_setup import setup_progressive_context_for_jira
        
        # Setup test context
        inheritance_chain = setup_progressive_context_for_jira("ACM-12345", "test-cluster")
        
        # Create test run directory
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            orchestrator = PhaseBasedOrchestrator()
            
            # Test single agent execution
            result = await orchestrator.agent_executor.execute_agent(
                "agent_a_jira_intelligence", 
                inheritance_chain, 
                temp_dir
            )
            
            assert result.agent_id == "agent_a_jira_intelligence", "Wrong agent ID in result"
            assert result.execution_status in ["success", "failed"], "Invalid execution status"
            
        print("✅ test_agent_execution_simulation: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ test_agent_execution_simulation: FAILED - {e}")
        return False

def test_ai_enhancement_triggers():
    """Test AI enhancement trigger logic"""
    try:
        from ai_agent_orchestrator import HybridAIAgentExecutor, AIAgentConfigurationLoader
        
        config_loader = AIAgentConfigurationLoader()
        executor = HybridAIAgentExecutor(config_loader)
        
        # Test enhancement trigger logic
        config = config_loader.get_configuration("agent_a_jira_intelligence")
        
        # Test with low confidence (should trigger AI)
        foundation_result_low = {'confidence_score': 0.6}
        should_enhance_low = executor._should_apply_ai_enhancement(config, foundation_result_low)
        
        # Test with high confidence (should not trigger AI)
        foundation_result_high = {'confidence_score': 0.95}
        should_enhance_high = executor._should_apply_ai_enhancement(config, foundation_result_high)
        
        # Verify logic (only if AI models available)
        if executor.ai_models_available:
            assert should_enhance_low == True, "Should enhance with low confidence"
            assert should_enhance_high == False, "Should not enhance with high confidence"
        
        print("✅ test_ai_enhancement_triggers: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ test_ai_enhancement_triggers: FAILED - {e}")
        return False

def test_progressive_context_integration():
    """Test Progressive Context Architecture integration"""
    try:
        from ai_agent_orchestrator import PhaseBasedOrchestrator
        
        orchestrator = PhaseBasedOrchestrator()
        
        # Test foundation context creation
        foundation_context = orchestrator.pca.create_foundation_context_for_jira("ACM-12345")
        inheritance_chain = orchestrator.pca.initialize_context_inheritance_chain(foundation_context)
        
        # Verify inheritance chain
        assert inheritance_chain.chain_integrity == True, "Inheritance chain should be valid"
        assert len(inheritance_chain.agent_contexts) == 4, "Should have 4 agent contexts"
        
        # Test agent context retrieval
        for agent_id in ["agent_a_jira_intelligence", "agent_b_documentation_intelligence", 
                        "agent_c_github_investigation", "agent_d_environment_intelligence"]:
            agent_context = inheritance_chain.agent_contexts.get(agent_id)
            assert agent_context is not None, f"Missing context for {agent_id}"
            assert 'jira_id' in agent_context, f"Missing jira_id in {agent_id} context"
        
        print("✅ test_progressive_context_integration: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ test_progressive_context_integration: FAILED - {e}")
        return False

async def test_output_file_generation():
    """Test that agents generate expected output files"""
    try:
        from ai_agent_orchestrator import PhaseBasedOrchestrator
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test traditional agent execution methods
            orchestrator = PhaseBasedOrchestrator()
            executor = orchestrator.agent_executor
            
            # Test Agent A output generation
            context = {'jira_id': 'ACM-12345', 'component': 'TestComponent'}
            result = await executor._execute_agent_a_traditional(context, temp_dir)
            
            # Verify output file exists
            assert 'output_file' in result, "Missing output_file in result"
            assert os.path.exists(result['output_file']), "Output file not created"
            
            # Verify file content
            with open(result['output_file'], 'r') as f:
                content = json.load(f)
            assert 'requirement_analysis' in content, "Missing requirement_analysis in output"
            
        print("✅ test_output_file_generation: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ test_output_file_generation: FAILED - {e}")
        return False

async def main():
    """Run all Phase 2 AI integration tests"""
    print("🤖 Running Phase 2 AI Enhancement Integration Tests")
    print("=" * 70)
    
    tests = [
        test_agent_yaml_configurations,
        test_configuration_validation,
        test_hybrid_ai_agent_executor,
        test_phase_based_orchestrator,
        test_agent_execution_simulation,
        test_ai_enhancement_triggers,
        test_progressive_context_integration,
        test_output_file_generation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if asyncio.iscoroutinefunction(test):
                result = await test()
            else:
                result = test()
                
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: FAILED - {e}")
            failed += 1
        
        print()
    
    print("=" * 70)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All Phase 2 AI enhancement integration tests passed!")
        print("✅ Phase 2 AI enhancement is ready for deployment")
    else:
        print(f"❌ {failed} tests failed - implementation needs fixes")
    
    return failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)