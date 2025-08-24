#!/usr/bin/env python3
"""
Reorganize existing runs to use the new intelligent folder organization
"""

from intelligent_run_organizer import IntelligentRunOrganizer
import os

def reorganize_existing_runs():
    """Reorganize existing runs that need ticket-based organization"""
    
    organizer = IntelligentRunOrganizer()
    
    # Tickets that need reorganization
    tickets_to_reorganize = ["ACM-22079"]
    
    for ticket in tickets_to_reorganize:
        print(f"\n🔄 Reorganizing {ticket}...")
        
        # Get current structure
        structure = organizer.get_organized_structure(ticket)
        print(f"Current: {structure['organization_type']} with {structure['run_count']} runs")
        
        if structure['organization_type'] == 'needs_organization':
            # Migrate existing runs
            existing_runs = structure['runs']
            print(f"Found runs to migrate: {existing_runs}")
            
            success = organizer.migrate_existing_runs(ticket, existing_runs)
            
            if success:
                print(f"✅ Successfully reorganized {ticket}")
                
                # Create latest metadata for most recent run
                if existing_runs:
                    # Get metadata from most recent run (highest timestamp)
                    latest_run = sorted(existing_runs)[-1]
                    metadata_file = f"runs/{ticket}/{latest_run}/run-metadata.json"
                    
                    if os.path.exists(metadata_file):
                        import json
                        with open(metadata_file, 'r') as f:
                            run_metadata = json.load(f)
                        organizer.create_latest_run_metadata(ticket, run_metadata)
                        print(f"📋 Created latest-run-metadata.json for {ticket}")
                
                # Verify new structure
                new_structure = organizer.get_organized_structure(ticket)
                print(f"New structure: {new_structure['organization_type']} with {new_structure['run_count']} runs")
                print(f"Organized runs: {new_structure['runs']}")
            else:
                print(f"❌ Failed to reorganize {ticket}")

if __name__ == "__main__":
    reorganize_existing_runs()