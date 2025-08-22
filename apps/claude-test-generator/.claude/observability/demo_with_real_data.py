#!/usr/bin/env python3
"""
Claude Test Generator - Observability Demo with Real ACM-22079 Data

Demonstrates the observability agent using actual data from the ACM-22079 
framework execution that just completed.
"""

import json
import sys
from pathlib import Path
from observability_command_handler import ObservabilityCommandHandler

def load_real_acm_22079_data():
    """Load actual ACM-22079 run data for demonstration"""
    
    # Find the ACM-22079 run directory
    runs_dir = Path("runs")
    acm_runs = [d for d in runs_dir.glob("ACM-22079-*") if d.is_dir()]
    
    if not acm_runs:
        print("❌ No ACM-22079 run data found.")
        print("Please run the framework first: 'Generate test plan for ACM-22079'")
        return None
    
    # Get the most recent ACM-22079 run
    latest_run = max(acm_runs, key=lambda d: d.stat().st_mtime)
    
    # Load run metadata
    metadata_path = latest_run / "run-metadata.json"
    if not metadata_path.exists():
        print(f"❌ No metadata found in {latest_run}")
        return None
    
    try:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        return {
            "run_directory": str(latest_run),
            "metadata": metadata
        }
    except json.JSONDecodeError as e:
        print(f"❌ Error loading metadata: {e}")
        return None

def simulate_real_framework_state(run_data):
    """Simulate framework state based on real ACM-22079 execution"""
    
    metadata = run_data["metadata"]
    
    # Simulate complete framework execution state
    return {
        "framework_state": {
            "current_phase": "completed",
            "start_time": "2025-08-21T20:50:52Z",
            "completion_percentage": 100,
            "estimated_completion": "0 minutes"
        },
        "agent_coordination": {
            "active_agents": [],
            "completed_agents": ["phase_0_pre", "phase_0", "agent_a", "agent_d", "agent_b", "agent_c", "qe_intelligence"],
            "context_chain_status": "A → A+D → A+D+B → A+D+B+C → Complete"
        },
        "key_insights": {
            "business_impact": "extracted",
            "technical_scope": "analyzed",
            "implementation_status": "validated",
            "environment_status": "validated",
            "version_awareness": "gap_detected"
        },
        "validation_status": {
            "implementation_reality": "passed",
            "evidence_validation": "passed",
            "cross_agent_validation": "passed",
            "format_enforcement": "passed"
        },
        "environment_context": metadata.get("test_environment", {}),
        "run_metadata": metadata,
        "risk_alerts": [
            {
                "level": "warning",
                "message": "Version gap detected - feature targets ACM 2.15.0 vs environment ACM 2.14.0",
                "timestamp": "2025-08-21T20:50:52Z",
                "mitigation": "Future-ready test design implemented"
            }
        ]
    }

def demonstrate_observability_commands(handler):
    """Demonstrate various observability commands with real data"""
    
    print("🔍 **OBSERVABILITY AGENT DEMONSTRATION**")
    print("Using real ACM-22079 execution data")
    print("=" * 70)
    print()
    
    commands_to_demo = [
        ("/status", "📊 **Framework Status Overview**"),
        ("/business", "🏢 **Business Impact Analysis**"),
        ("/technical", "🔧 **Technical Implementation Details**"),
        ("/environment", "🌐 **Environment Assessment**"),
        ("/agents", "🤖 **Agent Coordination Status**"),
        ("/context-flow", "🔄 **Progressive Context Architecture**"),
        ("/timeline", "⏱️ **Execution Timeline and Milestones**"),
        ("/risks", "⚠️ **Risk Analysis and Mitigation**"),
        ("/validation-status", "🔍 **Validation and Quality Checks**"),
        ("/performance", "📊 **Performance Metrics**"),
        ("/deep-dive agent_a", "🔬 **Deep Dive: JIRA Intelligence**"),
        ("/deep-dive environment", "🔬 **Deep Dive: Environment Intelligence**"),
        ("/help", "❓ **Available Commands**")
    ]
    
    for i, (command, description) in enumerate(commands_to_demo, 1):
        print(f"\n{i}. {description}")
        print("-" * 50)
        print(f"💻 **Command**: ./observe {command}")
        print()
        
        # Process the command
        response = handler.process_command(command)
        print(response)
        
        if i < len(commands_to_demo):
            print("\n" + "▼" * 70)

def interactive_demo(handler):
    """Interactive demonstration allowing user to try commands"""
    
    print("\n🎯 **INTERACTIVE OBSERVABILITY DEMO**")
    print("=" * 50)
    print()
    print("You can now try any observability command!")
    print("Examples:")
    print("  /status")
    print("  /business") 
    print("  /deep-dive agent_a")
    print("  /help")
    print()
    print("Type 'quit' to exit")
    print()
    
    while True:
        try:
            command = input("💻 ./observe ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Demo complete!")
                break
            
            if not command:
                continue
                
            if not command.startswith('/'):
                command = '/' + command
            
            print()
            response = handler.process_command(command)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main demonstration function"""
    
    print("🚀 **CLAUDE TEST GENERATOR - OBSERVABILITY AGENT DEMO**")
    print("Real-time framework monitoring and user interface demonstration")
    print("=" * 80)
    print()
    
    # Load real ACM-22079 data
    print("📊 Loading real ACM-22079 execution data...")
    run_data = load_real_acm_22079_data()
    
    if not run_data:
        print("\n🔧 **Setup Instructions:**")
        print("1. Run the test generator: 'Generate test plan for ACM-22079'")
        print("2. Wait for completion")
        print("3. Run this demo again")
        return
    
    print(f"✅ Loaded data from: {run_data['run_directory']}")
    print()
    
    # Initialize observability handler with real data
    handler = ObservabilityCommandHandler(run_data["run_directory"])
    
    # Simulate the complete framework state
    framework_state = simulate_real_framework_state(run_data)
    handler.update_state(framework_state)
    
    print("🎯 **Real Framework Data Loaded:**")
    metadata = run_data["metadata"]
    print(f"  📋 JIRA Ticket: {metadata.get('jira_ticket', 'Unknown')}")
    print(f"  🎯 Feature: {metadata.get('feature', 'Unknown')}")
    print(f"  🏢 Customer: {metadata.get('customer', 'Unknown')}")
    print(f"  🌐 Environment: {metadata.get('test_environment', {}).get('cluster', 'Unknown')}")
    print(f"  📊 Test Cases: {metadata.get('test_results', {}).get('total_test_cases', 0)}")
    print()
    
    # Check command line arguments for demo mode
    if len(sys.argv) > 1:
        demo_mode = sys.argv[1].lower()
        
        if demo_mode == "full":
            # Full automated demonstration
            demonstrate_observability_commands(handler)
        elif demo_mode == "interactive":
            # Interactive mode
            interactive_demo(handler)
        elif demo_mode.startswith("/"):
            # Single command mode
            command = sys.argv[1]
            print(f"💻 **Command**: ./observe {command}")
            print()
            response = handler.process_command(command)
            print(response)
        else:
            print(f"❓ Unknown demo mode: {demo_mode}")
            print("Available modes: full, interactive, or any command like /status")
    else:
        # Default: show key commands
        key_commands = ["/status", "/business", "/technical", "/deep-dive agent_a"]
        
        print("🔍 **Key Observability Commands Demonstration:**")
        print()
        
        for command in key_commands:
            print(f"💻 **Command**: ./observe {command}")
            print("-" * 40)
            response = handler.process_command(command)
            print(response)
            print("\n" + "▼" * 50 + "\n")
        
        print("🎯 **Try More Commands:**")
        print("  python demo_with_real_data.py interactive  # Interactive mode")
        print("  python demo_with_real_data.py full         # Full demonstration")
        print("  python demo_with_real_data.py /help        # Command reference")

if __name__ == "__main__":
    main()