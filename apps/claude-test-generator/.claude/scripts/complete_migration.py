#!/usr/bin/env python3
"""
Complete Migration Script - Fix All Violations
Migrates ALL existing runs to follow the definitive folder organization behavior.
"""

import os
import re
import shutil
import json
from pathlib import Path
from datetime import datetime
from intelligent_run_organizer import IntelligentRunOrganizer

def get_jira_id_from_directory(dir_name: str) -> str:
    """Extract JIRA ID from directory name"""
    # Handle both timestamped and clean formats
    if re.match(r'^[A-Z]+-\d+$', dir_name):
        return dir_name  # Already clean format
    elif re.match(r'^[A-Z]+-\d+-\d{8}-\d{6}$', dir_name):
        parts = dir_name.split('-')
        return f"{parts[0]}-{parts[1]}"  # Extract JIRA ID
    return None

def analyze_all_runs(runs_directory: str) -> dict:
    """Analyze all runs and group by JIRA ticket"""
    runs_dir = Path(runs_directory)
    
    analysis = {
        'tickets': {},
        'orphaned_runs': [],
        'clean_directories': [],
        'total_runs': 0
    }
    
    for item in runs_dir.iterdir():
        if not item.is_dir():
            continue
            
        analysis['total_runs'] += 1
        jira_id = get_jira_id_from_directory(item.name)
        
        if jira_id:
            if jira_id not in analysis['tickets']:
                analysis['tickets'][jira_id] = {
                    'jira_id': jira_id,
                    'timestamped_runs': [],
                    'clean_directory': None,
                    'total_runs': 0,
                    'needs_migration': False
                }
            
            ticket_data = analysis['tickets'][jira_id]
            
            # Check if it's a timestamped run or clean directory
            if re.match(r'^[A-Z]+-\d+-\d{8}-\d{6}$', item.name):
                ticket_data['timestamped_runs'].append(str(item))
                ticket_data['total_runs'] += 1
            elif re.match(r'^[A-Z]+-\d+$', item.name):
                ticket_data['clean_directory'] = str(item)
                # Count runs inside clean directory
                if item.is_dir():
                    for subitem in item.iterdir():
                        if subitem.is_dir():
                            ticket_data['total_runs'] += 1
            
            # Determine if migration is needed
            if len(ticket_data['timestamped_runs']) > 0:
                ticket_data['needs_migration'] = True
        else:
            analysis['orphaned_runs'].append(str(item))
    
    return analysis

def migrate_ticket_runs(jira_id: str, ticket_data: dict, runs_directory: str, dry_run: bool = True) -> dict:
    """Migrate all runs for a specific ticket"""
    runs_dir = Path(runs_directory)
    ticket_parent = runs_dir / jira_id
    
    migration = {
        'jira_id': jira_id,
        'dry_run': dry_run,
        'success': False,
        'operations': [],
        'errors': []
    }
    
    try:
        # Step 1: Create ticket parent directory if it doesn't exist
        if not ticket_parent.exists():
            if not dry_run:
                ticket_parent.mkdir(exist_ok=True)
            migration['operations'].append(f"{'Would create' if dry_run else 'Created'} parent directory: {ticket_parent}")
        
        # Step 2: Move timestamped runs into parent directory
        for timestamped_run in ticket_data['timestamped_runs']:
            source_path = Path(timestamped_run)
            target_path = ticket_parent / source_path.name
            
            if source_path.exists():
                if not dry_run:
                    if target_path.exists():
                        # Handle conflict - add suffix
                        timestamp = datetime.now().strftime("%H%M%S")
                        target_path = ticket_parent / f"{source_path.name}-moved-{timestamp}"
                    
                    shutil.move(str(source_path), str(target_path))
                
                migration['operations'].append(f"{'Would move' if dry_run else 'Moved'}: {source_path.name} → {jira_id}/{target_path.name}")
        
        # Step 3: Handle clean directory content if it exists
        if ticket_data['clean_directory']:
            clean_dir = Path(ticket_data['clean_directory'])
            if clean_dir.exists() and clean_dir != ticket_parent:
                # Move content from clean directory to proper parent
                for item in clean_dir.iterdir():
                    if item.is_dir():
                        target_path = ticket_parent / item.name
                        if not dry_run:
                            if target_path.exists():
                                # Merge or handle conflict
                                shutil.rmtree(target_path)
                            shutil.move(str(item), str(target_path))
                        migration['operations'].append(f"{'Would move' if dry_run else 'Moved'} content: {item.name} → {jira_id}/{item.name}")
                    else:
                        # Move file to parent
                        target_path = ticket_parent / item.name
                        if not dry_run:
                            shutil.move(str(item), str(target_path))
                        migration['operations'].append(f"{'Would move' if dry_run else 'Moved'} file: {item.name} → {jira_id}/{item.name}")
                
                # Remove empty clean directory if it's different from target
                if not dry_run and clean_dir != ticket_parent:
                    try:
                        clean_dir.rmdir()
                        migration['operations'].append(f"Removed empty directory: {clean_dir.name}")
                    except OSError:
                        migration['operations'].append(f"Could not remove directory (not empty): {clean_dir.name}")
        
        # Step 4: Create latest-run metadata
        if not dry_run and ticket_parent.exists():
            # Find the most recent run
            runs_in_parent = [d for d in ticket_parent.iterdir() if d.is_dir()]
            if runs_in_parent:
                latest_run = max(runs_in_parent, key=lambda p: p.name)
                organizer = IntelligentRunOrganizer(runs_directory)
                organizer.create_latest_run_metadata(jira_id, latest_run.name)
                migration['operations'].append("Created latest-run-metadata.json")
        
        migration['success'] = True
        
    except Exception as e:
        migration['errors'].append(f"Exception during migration: {str(e)}")
    
    return migration

def migrate_all_violations(runs_directory: str, dry_run: bool = True) -> dict:
    """Migrate all violations to proper organization"""
    analysis = analyze_all_runs(runs_directory)
    
    results = {
        'dry_run': dry_run,
        'total_tickets': len(analysis['tickets']),
        'tickets_needing_migration': 0,
        'migrations': [],
        'summary': {}
    }
    
    for jira_id, ticket_data in analysis['tickets'].items():
        if ticket_data['needs_migration']:
            results['tickets_needing_migration'] += 1
            
            print(f"{'🔍 [DRY RUN]' if dry_run else '🔧 [MIGRATING]'} {jira_id}: {len(ticket_data['timestamped_runs'])} timestamped runs")
            
            migration = migrate_ticket_runs(jira_id, ticket_data, runs_directory, dry_run)
            results['migrations'].append(migration)
            
            if migration['success']:
                print(f"  ✅ Migration {'planned' if dry_run else 'completed'} successfully")
                for op in migration['operations']:
                    print(f"    - {op}")
            else:
                print(f"  ❌ Migration failed: {migration['errors']}")
    
    results['summary'] = {
        'successful_migrations': len([m for m in results['migrations'] if m['success']]),
        'failed_migrations': len([m for m in results['migrations'] if not m['success']]),
        'success_rate': len([m for m in results['migrations'] if m['success']]) / len(results['migrations']) * 100 if results['migrations'] else 0
    }
    
    return results

def main():
    """Command-line interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python complete_migration.py <command> [runs_directory]")
        print("Commands:")
        print("  analyze    - Analyze all runs and show migration plan")
        print("  dry-run    - Show what would be migrated")
        print("  migrate    - Actually perform the migration")
        print("Example: python complete_migration.py analyze")
        sys.exit(1)
    
    command = sys.argv[1]
    runs_dir = sys.argv[2] if len(sys.argv) > 2 else "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs"
    
    if command == "analyze":
        print("🔍 Analyzing all runs for migration...")
        analysis = analyze_all_runs(runs_dir)
        
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"Total runs: {analysis['total_runs']}")
        print(f"Total tickets: {len(analysis['tickets'])}")
        print(f"Orphaned runs: {len(analysis['orphaned_runs'])}")
        
        print(f"\n📋 TICKETS REQUIRING MIGRATION:")
        for jira_id, data in analysis['tickets'].items():
            if data['needs_migration']:
                print(f"  {jira_id}: {len(data['timestamped_runs'])} timestamped runs, clean_dir: {bool(data['clean_directory'])}")
        
        print(json.dumps(analysis, indent=2, default=str))
        
    elif command == "dry-run":
        print("🔍 DRY RUN: Planning migration for all violations...")
        results = migrate_all_violations(runs_dir, dry_run=True)
        print(f"\n📊 MIGRATION PLAN SUMMARY:")
        print(f"Tickets needing migration: {results['tickets_needing_migration']}")
        print(f"Success rate: {results['summary']['success_rate']:.1f}%")
        
    elif command == "migrate":
        print("🔧 MIGRATING ALL VIOLATIONS...")
        print("⚠️  This will modify your directory structure!")
        
        response = input("Are you sure you want to proceed? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled by user")
            sys.exit(0)
        
        results = migrate_all_violations(runs_dir, dry_run=False)
        print(f"\n📊 MIGRATION SUMMARY:")
        print(f"Successful: {results['summary']['successful_migrations']}")
        print(f"Failed: {results['summary']['failed_migrations']}")
        print(f"Success rate: {results['summary']['success_rate']:.1f}%")
        
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()