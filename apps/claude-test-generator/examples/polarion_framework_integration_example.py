#!/usr/bin/env python3
"""
Example: Polarion Framework Integration Usage
Demonstrates how Claude uses the Polarion integration in the main workflow
"""

import os
import sys
from pathlib import Path

# Add the polarion module to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

def demonstrate_polarion_integration():
    """
    Example of how Claude would use Polarion integration during test case generation
    """
    print("🤖 Claude Test Generation with Polarion Integration")
    print("=" * 60)
    
    # Step 1: Claude generates test cases (simulated)
    ticket_id = "ACM-12345"
    test_cases_file = "examples/sample-test-plan.md"  # Using existing sample file
    
    print(f"📋 Analyzing ticket: {ticket_id}")
    print(f"📝 Generated test cases: {test_cases_file}")
    
    # Step 2: Claude attempts Polarion integration
    print("\n🔗 Attempting Polarion Integration...")
    
    try:
        from polarion import (
            post_test_cases_if_enabled,
            get_polarion_status_for_framework,
            integrate_polarion_with_framework
        )
        
        # Check Polarion status first
        print("🔍 Checking Polarion availability...")
        service = integrate_polarion_with_framework()
        
        if service._ai_has_valid_credentials():
            print("✅ Polarion integration available")
            
            # Attempt to post test cases
            print(f"📤 Posting test cases to Polarion...")
            posting_result = post_test_cases_if_enabled(
                test_cases_file=test_cases_file,
                ticket_id=ticket_id
            )
            
            if posting_result and posting_result.get("success"):
                print(f"✅ Successfully posted {posting_result.get('count', 0)} test cases")
                print(f"📊 Project: {posting_result.get('project_id')}")
                print(f"🔗 Test Case IDs: {posting_result.get('test_case_ids', [])}")
                
                # Generate Polarion section for Complete-Analysis.md
                polarion_section = service.ai_generate_polarion_section(posting_result)
                
            else:
                print(f"❌ Polarion posting failed: {posting_result.get('message') if posting_result else 'Unknown error'}")
                polarion_section = get_polarion_status_for_framework()
        else:
            print("ℹ️ Polarion integration not configured")
            polarion_section = get_polarion_status_for_framework()
        
        # Step 3: Claude includes Polarion status in Complete-Analysis.md
        print("\n📋 Complete-Analysis.md Polarion Section:")
        print("-" * 50)
        print(polarion_section)
        
        return True
        
    except ImportError as e:
        print(f"⚠️ Polarion integration not available: {e}")
        print("💡 To enable: pip install requests python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Polarion integration error: {e}")
        return False

def show_setup_instructions():
    """Show setup instructions for Polarion integration"""
    print("\n📚 Polarion Setup Instructions")
    print("=" * 40)
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Set up Polarion credentials:")
    print("   python3 -c \"from polarion import ai_setup_credentials; ai_setup_credentials()\"")
    print()
    print("3. Test connection:")
    print("   python3 -c \"from polarion import ai_test_connection; result = ai_test_connection(); print(result.recommendations)\"")
    print()
    print("4. Framework will automatically use Polarion when configured")

if __name__ == "__main__":
    print("🎯 Polarion Framework Integration Example\n")
    
    # Demonstrate the integration
    success = demonstrate_polarion_integration()
    
    if not success:
        show_setup_instructions()
    
    print("\n" + "=" * 60)
    print("💡 This demonstrates how Claude automatically integrates with Polarion")
    print("   during the test case generation workflow.")