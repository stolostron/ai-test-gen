#!/usr/bin/env python3
"""
Test creating new runs with the intelligent organization system
"""

from intelligent_run_organizer import IntelligentRunOrganizer

def test_new_run_scenarios():
    """Test various scenarios for new run creation"""
    
    organizer = IntelligentRunOrganizer()
    
    print("🧪 Testing Intelligent Run Organization Scenarios\n")
    
    # Scenario 1: ACM-22079 (already has 2 runs - should add to existing organization)
    print("📋 Scenario 1: Adding third run to ACM-22079 (existing ticket organization)")
    new_run_path = organizer.organize_ticket_runs("ACM-22079", "ACM-22079-20250823-130000")
    print(f"   Result: {new_run_path}")
    structure = organizer.get_organized_structure("ACM-22079")
    print(f"   Structure: {structure['organization_type']} with {structure['run_count']} runs")
    print(f"   Runs: {structure['runs']}\n")
    
    # Scenario 2: ACM-15207 (has 1 run - second run should trigger reorganization)
    print("📋 Scenario 2: Adding second run to ACM-15207 (should trigger reorganization)")
    analysis = organizer.analyze_run_organization("ACM-15207")
    print(f"   Current state: {analysis['run_count']} run(s), action: {analysis['recommended_action']}")
    new_run_path = organizer.organize_ticket_runs("ACM-15207", "ACM-15207-20250823-130000")
    print(f"   Result: {new_run_path}")
    structure = organizer.get_organized_structure("ACM-15207")
    print(f"   New structure: {structure['organization_type']} with {structure['run_count']} runs")
    print(f"   Runs: {structure['runs']}\n")
    
    # Scenario 3: ACM-99999 (new ticket - first run should use standard format)
    print("📋 Scenario 3: Creating first run for ACM-99999 (new ticket)")
    analysis = organizer.analyze_run_organization("ACM-99999")
    print(f"   Current state: {analysis['run_count']} run(s), action: {analysis['recommended_action']}")
    new_run_path = organizer.organize_ticket_runs("ACM-99999", "ACM-99999-20250823-130000")
    print(f"   Result: {new_run_path}")
    structure = organizer.get_organized_structure("ACM-99999")
    print(f"   Structure: {structure['organization_type']} with {structure['run_count']} runs")
    print(f"   Runs: {structure['runs']}\n")

if __name__ == "__main__":
    test_new_run_scenarios()