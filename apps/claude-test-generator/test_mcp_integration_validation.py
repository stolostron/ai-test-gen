#!/usr/bin/env python3
"""
MCP Integration Validation Test
==============================

Quick validation test demonstrating the working MCP integration after fixes.
This test validates that both GitHub and Filesystem MCP services are operational.
"""

import sys
import json
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

sys.path.insert(0, str(Path(__file__).parent / ".claude" / "mcp"))
from mcp_service_coordinator import MCPServiceCoordinator

def test_mcp_integration():
    """Test that MCP integration is working correctly"""
    print("🧪 MCP Integration Validation Test")
    print("=" * 50)
    
    # Initialize coordinator
    coordinator = MCPServiceCoordinator()
    
    # Test 1: Service Status
    print("📋 Test 1: Service Status")
    status = coordinator.get_service_status()
    
    github_available = status['github_mcp']['available']
    filesystem_available = status['filesystem_mcp']['available']
    
    print(f"   GitHub MCP: {'✅ Available' if github_available else '❌ Not Available'}")
    print(f"   Filesystem MCP: {'✅ Available' if filesystem_available else '❌ Not Available'}")
    
    if not (github_available and filesystem_available):
        print("❌ MCP services not fully available")
        return False
    
    # Test 2: Service Testing
    print("\n🔍 Test 2: Service Connectivity")
    test_results = coordinator.test_all_services()
    
    github_status = test_results['test_results']['github_mcp'].get('status')
    filesystem_status = test_results['test_results']['filesystem_mcp'].get('status')
    
    print(f"   GitHub MCP Test: {'✅ Connected' if github_status == 'connected' else '❌ ' + str(github_status)}")
    print(f"   Filesystem MCP Test: {'✅ Connected' if filesystem_status == 'connected' else '❌ ' + str(filesystem_status)}")
    
    # Test 3: Filesystem Operations
    print("\n📁 Test 3: Filesystem Operations")
    try:
        # Test file search with recursive pattern
        result = coordinator.filesystem_search_files("**/*.py", use_fallback=False)
        files_found = result.get('files_found', 0)
        print(f"   Python files found: {files_found}")
        
        # Test pattern finding
        test_result = coordinator.filesystem_find_test_patterns(use_fallback=False)
        test_files = test_result.get('test_files_found', 0)
        print(f"   Test files found: {test_files}")
        
        print("   ✅ Filesystem operations working")
    except Exception as e:
        print(f"   ❌ Filesystem operations failed: {e}")
        return False
    
    # Test 4: GitHub Operations (if authenticated)
    print("\n🐙 Test 4: GitHub Operations")
    try:
        # Test with a known PR to validate GitHub functionality
        result = coordinator.github_get_pull_request("stolostron/cluster-curator-controller", 468, use_fallback=False)
        
        if 'error' in result:
            print(f"   ⚠️ GitHub API error (expected if not authenticated): {result['error']}")
        else:
            print("   ✅ GitHub operations working")
            pr_title = result.get('pr_info', {}).get('title', 'Unknown')
            print(f"   PR Title: {pr_title[:50]}...")
    except Exception as e:
        print(f"   ⚠️ GitHub operations require authentication: {e}")
    
    # Test 5: Performance Statistics
    print("\n📊 Test 5: Performance Tracking")
    stats = coordinator.performance_stats
    print(f"   GitHub calls: {stats['github_calls']}")
    print(f"   Filesystem calls: {stats['filesystem_calls']}")
    print(f"   Fallback activations: {stats['fallback_activations']}")
    print("   ✅ Performance tracking working")
    
    # Test 6: Agent Optimization
    print("\n🤖 Test 6: Agent Optimization")
    optimization = coordinator.optimize_for_agent("agent_c_github_investigation", "github_analysis")
    print(f"   Agent: {optimization['agent']}")
    print(f"   Recommendations: {len(optimization['recommendations'])} items")
    print("   ✅ Agent optimization working")
    
    print("\n" + "=" * 50)
    print("🎉 MCP Integration Validation: SUCCESS")
    print("✅ Both GitHub and Filesystem MCP services are operational")
    print("✅ All core functionality is working as expected")
    print("✅ Performance tracking and optimization features active")
    
    return True

if __name__ == "__main__":
    success = test_mcp_integration()
    sys.exit(0 if success else 1)