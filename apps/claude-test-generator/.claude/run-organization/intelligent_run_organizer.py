#!/usr/bin/env python3
"""
Intelligent Run Organization Service - Automatic Enforcement
=========================================================

FRAMEWORK INTEGRATION: Automatically enforces proper ticket-based run organization
for all framework executions, ensuring consistent structure:

runs/
├── ACM-XXXXX/
│   ├── ACM-XXXXX-20250823-170246/
│   ├── ACM-XXXXX-20250824-091502/
│   └── latest -> ACM-XXXXX-20250824-091502

This service is called automatically during framework execution to ensure
proper organization without requiring manual intervention.
"""

import os
import json
import shutil
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class IntelligentRunOrganizer:
    """
    Intelligent run organization with ticket-based grouping
    """
    
    def __init__(self, runs_directory: str = "runs"):
        self.runs_dir = Path(runs_directory)
        self.runs_dir.mkdir(exist_ok=True)
        
    def detect_existing_runs(self, jira_ticket: str) -> List[str]:
        """
        Scan runs directory for existing instances of same ticket
        Returns list of existing run directories for the ticket
        """
        existing_runs = []
        
        # Pattern for individual run directories: TICKET-YYYYMMDD-HHMMSS
        individual_pattern = re.compile(rf'^{re.escape(jira_ticket)}-\d{{8}}-\d{{6}}$')
        
        # Pattern for incomplete runs (like progressive-context)
        incomplete_pattern = re.compile(rf'^{re.escape(jira_ticket)}-.*$')
        
        for item in self.runs_dir.iterdir():
            if item.is_dir():
                # Check for individual run directories
                if individual_pattern.match(item.name):
                    existing_runs.append(item.name)
                # Check for incomplete runs
                elif incomplete_pattern.match(item.name) and not individual_pattern.match(item.name):
                    existing_runs.append(item.name)
        
        return sorted(existing_runs)
    
    def analyze_run_organization(self, jira_ticket: str) -> Dict:
        """
        Analyze current organization state for ticket
        """
        existing_runs = self.detect_existing_runs(jira_ticket)
        ticket_parent = self.runs_dir / jira_ticket
        
        return {
            'existing_runs': existing_runs,
            'run_count': len(existing_runs),
            'needs_reorganization': len(existing_runs) >= 1,  # Reorganize on second run
            'parent_exists': ticket_parent.exists(),
            'recommended_action': self._determine_action(existing_runs, ticket_parent.exists())
        }
    
    def _determine_action(self, existing_runs: List[str], parent_exists: bool) -> str:
        """Determine what action should be taken"""
        if len(existing_runs) == 0:
            return "create_first_run"
        elif len(existing_runs) == 1 and not parent_exists:
            return "reorganize_and_add_second"
        elif parent_exists:
            return "add_to_existing_organization"
        else:
            return "reorganize_existing_runs"
    
    def generate_run_id(self, jira_ticket: str) -> str:
        """Generate new run ID with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{jira_ticket}-{timestamp}"
    
    def organize_ticket_runs(self, jira_ticket: str, new_run_id: str = None) -> str:
        """
        Intelligently organize runs for ticket
        Returns final run directory path
        """
        if new_run_id is None:
            new_run_id = self.generate_run_id(jira_ticket)
            
        analysis = self.analyze_run_organization(jira_ticket)
        action = analysis['recommended_action']
        
        if action == "create_first_run":
            # First run - use standard format
            run_path = self.runs_dir / new_run_id
            run_path.mkdir(exist_ok=True)
            return str(run_path)
            
        elif action == "reorganize_and_add_second":
            # Second run - reorganize existing and add new
            return self._reorganize_for_second_run(jira_ticket, analysis['existing_runs'][0], new_run_id)
            
        elif action == "add_to_existing_organization":
            # Add to existing ticket organization
            ticket_parent = self.runs_dir / jira_ticket
            new_run_path = ticket_parent / new_run_id
            new_run_path.mkdir(exist_ok=True)
            # Update latest symlink
            self.create_latest_symlink(jira_ticket, new_run_id)
            return str(new_run_path)
            
        else:
            # Fallback - create in ticket organization
            ticket_parent = self.runs_dir / jira_ticket
            ticket_parent.mkdir(exist_ok=True)
            new_run_path = ticket_parent / new_run_id
            new_run_path.mkdir(exist_ok=True)
            # Update latest symlink
            self.create_latest_symlink(jira_ticket, new_run_id)
            return str(new_run_path)
    
    def _reorganize_for_second_run(self, jira_ticket: str, existing_run: str, new_run_id: str) -> str:
        """
        Reorganize when adding second run - creates ticket parent and migrates existing
        """
        print(f"🔄 Reorganizing runs for {jira_ticket} - creating ticket-based organization...")
        
        # Create ticket parent directory
        ticket_parent = self.runs_dir / jira_ticket
        ticket_parent.mkdir(exist_ok=True)
        
        # Move existing run into ticket parent
        existing_path = self.runs_dir / existing_run
        new_existing_path = ticket_parent / existing_run
        
        print(f"📁 Moving {existing_run} → {jira_ticket}/{existing_run}")
        shutil.move(str(existing_path), str(new_existing_path))
        
        # Create new run directory
        new_run_path = ticket_parent / new_run_id
        new_run_path.mkdir(exist_ok=True)
        
        # Create latest symlink pointing to newest run
        self.create_latest_symlink(jira_ticket, new_run_id)
        
        print(f"✅ Organization complete: {jira_ticket}/ now contains multiple runs")
        return str(new_run_path)
    
    def create_latest_symlink(self, jira_ticket: str, latest_run_id: str) -> None:
        """
        Creates/updates 'latest' symlink pointing to most recent run
        """
        ticket_parent = self.runs_dir / jira_ticket
        if not ticket_parent.exists():
            return  # No ticket organization
            
        latest_link = ticket_parent / "latest"
        
        try:
            # Remove existing symlink
            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()
            
            # Create new symlink pointing to latest run
            latest_link.symlink_to(latest_run_id)
            print(f"🔗 Updated latest symlink: {jira_ticket}/latest -> {latest_run_id}")
            
        except Exception as e:
            print(f"❌ Failed to create latest symlink: {e}")

    def create_latest_run_metadata(self, jira_ticket: str, run_metadata: Dict) -> None:
        """
        Creates/updates latest-run-metadata.json in ticket parent directory
        """
        ticket_parent = self.runs_dir / jira_ticket
        if not ticket_parent.exists():
            return  # No ticket organization
            
        latest_metadata = {
            "latest_run_id": run_metadata.get("run_id"),
            "latest_timestamp": run_metadata.get("generation_timestamp"),
            "jira_ticket": jira_ticket,
            "feature_title": run_metadata.get("feature_title"),
            "total_runs": len([d for d in ticket_parent.iterdir() if d.is_dir() and d.name != "latest"]),
            "organization_type": "ticket_based",
            "last_updated": datetime.now().isoformat()
        }
        
        latest_file = ticket_parent / "latest-run-metadata.json"
        with open(latest_file, 'w') as f:
            json.dump(latest_metadata, f, indent=2)
    
    def migrate_existing_runs(self, jira_ticket: str, existing_runs: List[str]) -> bool:
        """
        Safely migrate existing runs into ticket-based organization
        """
        if not existing_runs:
            return True
            
        try:
            ticket_parent = self.runs_dir / jira_ticket
            ticket_parent.mkdir(exist_ok=True)
            
            for run_dir in existing_runs:
                source_path = self.runs_dir / run_dir
                target_path = ticket_parent / run_dir
                
                if source_path.exists() and not target_path.exists():
                    shutil.move(str(source_path), str(target_path))
                    print(f"✅ Migrated: {run_dir} → {jira_ticket}/{run_dir}")
                    
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
    
    def get_organized_structure(self, jira_ticket: str) -> Dict:
        """
        Get current organized structure for a ticket
        """
        ticket_parent = self.runs_dir / jira_ticket
        
        if ticket_parent.exists():
            # Ticket-based organization
            runs = [d.name for d in ticket_parent.iterdir() if d.is_dir()]
            return {
                "organization_type": "ticket_based",
                "parent_directory": str(ticket_parent),
                "runs": sorted(runs),
                "run_count": len(runs),
                "latest_metadata_exists": (ticket_parent / "latest-run-metadata.json").exists()
            }
        else:
            # Check for individual runs
            individual_runs = self.detect_existing_runs(jira_ticket)
            return {
                "organization_type": "individual" if len(individual_runs) <= 1 else "needs_organization",
                "parent_directory": str(self.runs_dir),
                "runs": individual_runs,
                "run_count": len(individual_runs),
                "latest_metadata_exists": False
            }
    
    def cleanup_incomplete_runs(self, jira_ticket: str) -> List[str]:
        """
        Clean up incomplete runs (like progressive-context directories)
        """
        cleaned = []
        
        # Pattern for incomplete runs
        incomplete_pattern = re.compile(rf'^{re.escape(jira_ticket)}-(?!.*\d{{8}}-\d{{6}}$).*$')
        
        for item in self.runs_dir.iterdir():
            if item.is_dir() and incomplete_pattern.match(item.name):
                print(f"🧹 Cleaning up incomplete run: {item.name}")
                shutil.rmtree(item)
                cleaned.append(item.name)
                
        return cleaned

def main():
    """Test the intelligent run organization"""
    organizer = IntelligentRunOrganizer()
    
    # Test scenarios
    test_tickets = ["ACM-22079", "ACM-15207", "ACM-13644"]
    
    for ticket in test_tickets:
        print(f"\n🔍 Analyzing {ticket}:")
        structure = organizer.get_organized_structure(ticket)
        print(f"  Organization: {structure['organization_type']}")
        print(f"  Runs: {structure['run_count']} - {structure['runs']}")
        
        # Clean up incomplete runs
        cleaned = organizer.cleanup_incomplete_runs(ticket)
        if cleaned:
            print(f"  Cleaned: {cleaned}")

if __name__ == "__main__":
    main()