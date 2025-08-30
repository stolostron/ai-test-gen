#!/usr/bin/env python3
"""
Debug script to investigate AI Agent Orchestrator configuration loading
"""

import sys
import os
from pathlib import Path

# Add the AI services directory to path
sys.path.insert(0, '.claude/ai-services')

from ai_agent_orchestrator import AIAgentConfigurationLoader

def debug_configuration_loading():
    """Debug configuration loading step by step"""
    print("🔍 Debugging AI Agent Orchestrator Configuration Loading")
    print("=" * 60)
    
    # Step 1: Check current working directory
    print(f"📁 Current working directory: {os.getcwd()}")
    print(f"📁 Expected agents directory: .claude/ai-services/agents")
    
    # Step 2: Check if agents directory exists
    agents_dir = Path(".claude/ai-services/agents")
    print(f"📁 Agents directory exists: {agents_dir.exists()}")
    print(f"📁 Agents directory path: {agents_dir.absolute()}")
    
    if agents_dir.exists():
        yaml_files = list(agents_dir.glob("*.yaml"))
        print(f"📄 YAML files found: {len(yaml_files)}")
        for yaml_file in yaml_files:
            print(f"   - {yaml_file.name}")
    
    # Step 3: Try to load configurations
    try:
        print("\n🤖 Attempting to load configurations...")
        loader = AIAgentConfigurationLoader()
        print(f"📊 Configurations loaded: {len(loader.configurations)}")
        
        if loader.configurations:
            print("✅ Successfully loaded agent configurations:")
            for agent_id in loader.configurations.keys():
                print(f"   - {agent_id}")
        else:
            print("❌ No configurations loaded!")
            
        # Step 4: Test validation
        print(f"\n🔍 Validation result: {loader.validate_configurations()}")
        
    except Exception as e:
        print(f"❌ Error loading configurations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_configuration_loading()