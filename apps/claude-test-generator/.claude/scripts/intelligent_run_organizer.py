#!/usr/bin/env python3
"""
Intelligent Run Organizer Script
Enforces definitive folder organization behavior for test generation runs.

DEFINITIVE BEHAVIOR:
- First run: ACM-XXXX-YYYYMMDD-HHMMSS/ (timestamped in root)
- Second+ runs: Create ACM-XXXX/ parent, move existing runs inside, create new runs inside

This script provides robust enforcement independent of framework configuration.
"""

import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class IntelligentRunOrganizer:
    def __init__(self, runs_directory: str):
        self.runs_dir = Path(runs_directory)
        self.runs_dir.mkdir(exist_ok=True)
        
    def get_jira_pattern(self, jira_id: str) -> str:
        """Get regex pattern for matching runs of specific JIRA ticket"""
        return rf"^{re.escape(jira_id)}-\d{{8}}-\d{{6}}$"
    
    def scan_existing_runs(self, jira_id: str) -> List[Path]:
        """Find all existing runs for a JIRA ticket"""
        pattern = self.get_jira_pattern(jira_id)
        existing_runs = []
        
        # Check for timestamped runs in root
        for item in self.runs_dir.iterdir():
            if item.is_dir() and re.match(pattern, item.name):
                existing_runs.append(item)
        
        # Check for runs inside ticket parent directory
        ticket_parent = self.runs_dir / jira_id
        if ticket_parent.exists() and ticket_parent.is_dir():
            for item in ticket_parent.iterdir():
                if item.is_dir() and re.match(pattern, item.name):
                    existing_runs.append(item)
        
        return sorted(existing_runs, key=lambda p: p.name)
    
    def analyze_organization_state(self, jira_id: str) -> Dict:
        """Analyze current organization state for ticket"""
        existing_runs = self.scan_existing_runs(jira_id)
        ticket_parent = self.runs_dir / jira_id
        
        state = {
            'jira_id': jira_id,
            'existing_run_count': len(existing_runs),
            'existing_runs': [str(run) for run in existing_runs],
            'ticket_parent_exists': ticket_parent.exists(),
            'needs_reorganization': False,
            'action_required': 'none'
        }
        
        # Determine action required
        if len(existing_runs) == 0:
            state['action_required'] = 'create_first_run'
        elif len(existing_runs) == 1 and not ticket_parent.exists():
            state['action_required'] = 'reorganize_for_second_run'
            state['needs_reorganization'] = True
        elif ticket_parent.exists():
            state['action_required'] = 'create_subsequent_run'
        else:
            state['action_required'] = 'complex_state_needs_analysis'
        
        return state
    
    def create_timestamped_directory_name(self, jira_id: str) -> str:
        """Create timestamped directory name for new run"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{jira_id}-{timestamp}"
    
    def reorganize_for_second_run(self, jira_id: str, existing_runs: List[Path]) -> Dict:
        """Reorganize when second run is created"""
        ticket_parent = self.runs_dir / jira_id
        new_run_name = self.create_timestamped_directory_name(jira_id)
        
        operations = {
            'success': False,
            'operations_performed': [],
            'ticket_parent_created': False,
            'runs_moved': [],
            'new_run_created': False,
            'new_run_path': None,
            'errors': []
        }
        
        try:
            # Step 1: Create ticket parent directory
            ticket_parent.mkdir(exist_ok=True)
            operations['ticket_parent_created'] = True
            operations['operations_performed'].append(f"Created parent directory: {ticket_parent}")
            
            # Step 2: Move existing runs into parent directory
            for existing_run in existing_runs:
                if existing_run.parent == self.runs_dir:  # Only move if in root
                    target_path = ticket_parent / existing_run.name
                    shutil.move(str(existing_run), str(target_path))
                    operations['runs_moved'].append({
                        'from': str(existing_run),
                        'to': str(target_path)
                    })
                    operations['operations_performed'].append(f"Moved: {existing_run.name} → {ticket_parent.name}/{existing_run.name}")
            
            # Step 3: Create new run directory inside parent
            new_run_path = ticket_parent / new_run_name
            new_run_path.mkdir(exist_ok=True)
            operations['new_run_created'] = True
            operations['new_run_path'] = str(new_run_path)
            operations['operations_performed'].append(f"Created new run: {new_run_path}")
            
            # Step 4: Create latest-run metadata
            self.create_latest_run_metadata(jira_id, new_run_name)
            operations['operations_performed'].append("Created latest-run-metadata.json")
            
            operations['success'] = True
            
        except Exception as e:
            operations['errors'].append(f"Error during reorganization: {str(e)}")
            # Attempt rollback on error
            try:
                if ticket_parent.exists():
                    # Move runs back if they were moved
                    for move_op in operations['runs_moved']:
                        if Path(move_op['to']).exists():
                            shutil.move(move_op['to'], move_op['from'])
                    # Remove parent directory if it was created
                    if operations['ticket_parent_created']:
                        shutil.rmtree(ticket_parent, ignore_errors=True)
                operations['operations_performed'].append("Rollback completed due to error")
            except Exception as rollback_error:
                operations['errors'].append(f"Rollback error: {str(rollback_error)}")
        
        return operations
    
    def create_subsequent_run(self, jira_id: str) -> Dict:
        """Create new run in existing ticket parent directory"""
        ticket_parent = self.runs_dir / jira_id
        new_run_name = self.create_timestamped_directory_name(jira_id)
        new_run_path = ticket_parent / new_run_name
        
        operations = {
            'success': False,
            'new_run_created': False,
            'new_run_path': None,
            'operations_performed': [],
            'errors': []
        }
        
        try:
            new_run_path.mkdir(exist_ok=True)
            operations['new_run_created'] = True
            operations['new_run_path'] = str(new_run_path)
            operations['operations_performed'].append(f"Created subsequent run: {new_run_path}")
            
            # Update latest-run metadata
            self.create_latest_run_metadata(jira_id, new_run_name)
            operations['operations_performed'].append("Updated latest-run-metadata.json")
            
            operations['success'] = True
            
        except Exception as e:
            operations['errors'].append(f"Error creating subsequent run: {str(e)}")
        
        return operations
    
    def create_first_run(self, jira_id: str) -> Dict:
        """Create first run directory (timestamped in root)"""
        new_run_name = self.create_timestamped_directory_name(jira_id)
        new_run_path = self.runs_dir / new_run_name
        
        operations = {
            'success': False,
            'new_run_created': False,
            'new_run_path': None,
            'operations_performed': [],
            'errors': []
        }
        
        try:
            new_run_path.mkdir(exist_ok=True)
            operations['new_run_created'] = True
            operations['new_run_path'] = str(new_run_path)
            operations['operations_performed'].append(f"Created first run: {new_run_path}")
            operations['success'] = True
            
        except Exception as e:
            operations['errors'].append(f"Error creating first run: {str(e)}")
        
        return operations
    
    def create_latest_run_metadata(self, jira_id: str, latest_run_name: str) -> None:
        """Create/update latest-run-metadata.json in ticket parent directory"""
        ticket_parent = self.runs_dir / jira_id
        metadata_file = ticket_parent / "latest-run-metadata.json"
        
        metadata = {
            "jira_ticket": jira_id,
            "latest_run": latest_run_name,
            "latest_run_path": f"{jira_id}/{latest_run_name}",
            "updated_timestamp": datetime.now().isoformat(),
            "total_runs": len([d for d in ticket_parent.iterdir() if d.is_dir() and d.name != "latest-run-metadata.json"])
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def organize_run(self, jira_id: str) -> Dict:
        """Main method: Organize run according to definitive behavior"""
        # Validate JIRA ID format
        if not re.match(r'^[A-Z]+-\d+$', jira_id):
            return {
                'success': False,
                'error': f"Invalid JIRA ID format: {jira_id}",
                'operations_performed': []
            }
        
        # Analyze current state
        state = self.analyze_organization_state(jira_id)
        
        # Execute appropriate action
        if state['action_required'] == 'create_first_run':
            return self.create_first_run(jira_id)
        
        elif state['action_required'] == 'reorganize_for_second_run':
            existing_runs = [Path(run) for run in state['existing_runs']]
            return self.reorganize_for_second_run(jira_id, existing_runs)
        
        elif state['action_required'] == 'create_subsequent_run':
            return self.create_subsequent_run(jira_id)
        
        else:
            return {
                'success': False,
                'error': f"Complex organization state requires manual analysis: {state}",
                'operations_performed': []
            }
    
    def validate_organization(self, jira_id: str) -> Dict:
        """Validate that organization follows definitive behavior"""
        existing_runs = self.scan_existing_runs(jira_id)
        ticket_parent = self.runs_dir / jira_id
        
        validation = {
            'jira_id': jira_id,
            'valid': True,
            'run_count': len(existing_runs),
            'validation_results': [],
            'issues': []
        }
        
        if len(existing_runs) == 0:
            validation['validation_results'].append("No runs found - valid state")
        elif len(existing_runs) == 1:
            # Should be in root as timestamped directory
            run = existing_runs[0]
            if run.parent == self.runs_dir:
                validation['validation_results'].append("Single run in root - valid first run state")
            else:
                validation['valid'] = False
                validation['issues'].append("Single run should be in root directory")
        else:
            # Multiple runs should be in ticket parent directory
            if not ticket_parent.exists():
                validation['valid'] = False
                validation['issues'].append("Multiple runs exist but no ticket parent directory")
            else:
                runs_in_parent = [run for run in existing_runs if run.parent == ticket_parent]
                runs_in_root = [run for run in existing_runs if run.parent == self.runs_dir]
                
                if runs_in_root:
                    validation['valid'] = False
                    validation['issues'].append(f"Found runs in root that should be in parent: {[r.name for r in runs_in_root]}")
                
                if len(runs_in_parent) == len(existing_runs):
                    validation['validation_results'].append("All runs properly organized in ticket parent directory")
                else:
                    validation['valid'] = False
                    validation['issues'].append("Run organization inconsistent")
        
        return validation

def main():
    """Command-line interface for testing"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python intelligent_run_organizer.py <JIRA_ID> [runs_directory]")
        print("Example: python intelligent_run_organizer.py ACM-1234 /path/to/runs")
        sys.exit(1)
    
    jira_id = sys.argv[1]
    runs_dir = sys.argv[2] if len(sys.argv) > 2 else "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs"
    
    organizer = IntelligentRunOrganizer(runs_dir)
    
    # Show current state
    print(f"🔍 Analyzing organization state for {jira_id}...")
    state = organizer.analyze_organization_state(jira_id)
    print(json.dumps(state, indent=2))
    
    # Organize run
    print(f"\n🛠️ Organizing run for {jira_id}...")
    result = organizer.organize_run(jira_id)
    print(json.dumps(result, indent=2))
    
    # Validate organization
    print(f"\n✅ Validating organization for {jira_id}...")
    validation = organizer.validate_organization(jira_id)
    print(json.dumps(validation, indent=2))

if __name__ == "__main__":
    main()