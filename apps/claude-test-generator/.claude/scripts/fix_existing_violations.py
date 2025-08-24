#!/usr/bin/env python3
"""
Fix Existing Folder Naming Violations Script
Applies the definitive folder organization behavior to existing runs.

This script fixes the current violations by reorganizing existing runs
according to the definitive behavior rules.
"""

import os
import sys
import json
from pathlib import Path
from intelligent_run_organizer import IntelligentRunOrganizer

def analyze_current_violations(runs_directory: str) -> dict:
    """Analyze all current violations in runs directory"""
    runs_dir = Path(runs_directory)
    
    violations = {
        'total_runs': 0,
        'violations_found': [],
        'compliant_runs': [],
        'tickets_affected': set(),
        'summary': {}
    }
    
    # Scan all directories in runs
    for item in runs_dir.iterdir():
        if not item.is_dir():
            continue
            
        violations['total_runs'] += 1
        
        # Check if it's a timestamped run (potentially violating)
        if '-' in item.name and item.name.count('-') >= 2:
            parts = item.name.split('-')
            if len(parts) >= 3 and parts[1].isdigit() and len(parts[1]) == 8:
                # This is a timestamped run
                jira_id = parts[0] + '-' + parts[1]
                violations['tickets_affected'].add(jira_id)
                
                # Check if this ticket has multiple runs
                organizer = IntelligentRunOrganizer(runs_directory)
                existing_runs = organizer.scan_existing_runs(jira_id)
                
                if len(existing_runs) > 1:
                    violations['violations_found'].append({
                        'directory': item.name,
                        'jira_id': jira_id,
                        'issue': 'Multiple runs exist but not organized in ticket parent',
                        'run_count': len(existing_runs),
                        'all_runs': [r.name for r in existing_runs]
                    })
                else:
                    violations['compliant_runs'].append({
                        'directory': item.name,
                        'jira_id': jira_id,
                        'status': 'First run - correctly in root'
                    })
        else:
            # Check if it's a ticket parent directory
            if item.name.startswith('ACM-') and item.name.count('-') == 1:
                violations['compliant_runs'].append({
                    'directory': item.name,
                    'status': 'Ticket parent directory - correct organization'
                })
    
    violations['summary'] = {
        'total_tickets': len(violations['tickets_affected']),
        'violation_count': len(violations['violations_found']),
        'compliant_count': len(violations['compliant_runs']),
        'violation_percentage': len(violations['violations_found']) / violations['total_runs'] * 100 if violations['total_runs'] > 0 else 0
    }
    
    return violations

def fix_violations(runs_directory: str, dry_run: bool = True) -> dict:
    """Fix all identified violations"""
    violations = analyze_current_violations(runs_directory)
    organizer = IntelligentRunOrganizer(runs_directory)
    
    fix_results = {
        'dry_run': dry_run,
        'violations_to_fix': len(violations['violations_found']),
        'fixes_attempted': [],
        'fixes_successful': [],
        'fixes_failed': [],
        'summary': {}
    }
    
    # Group violations by JIRA ticket
    tickets_to_fix = {}
    for violation in violations['violations_found']:
        jira_id = violation['jira_id']
        if jira_id not in tickets_to_fix:
            tickets_to_fix[jira_id] = []
        tickets_to_fix[jira_id].append(violation)
    
    print(f"🔧 {'DRY RUN: ' if dry_run else ''}Fixing violations for {len(tickets_to_fix)} tickets...")
    
    for jira_id, ticket_violations in tickets_to_fix.items():
        print(f"\n📋 Processing {jira_id} ({len(ticket_violations)} violations)...")
        
        fix_attempt = {
            'jira_id': jira_id,
            'violations': ticket_violations,
            'success': False,
            'operations': [],
            'errors': []
        }
        
        try:
            if not dry_run:
                # Get current state before fix
                state_before = organizer.analyze_organization_state(jira_id)
                fix_attempt['state_before'] = state_before
                
                # Apply organization fix
                result = organizer.organize_run(jira_id)
                fix_attempt['organize_result'] = result
                
                if result['success']:
                    # Validate fix
                    validation = organizer.validate_organization(jira_id)
                    fix_attempt['validation'] = validation
                    
                    if validation['valid']:
                        fix_attempt['success'] = True
                        fix_results['fixes_successful'].append(fix_attempt)
                        print(f"  ✅ Successfully fixed {jira_id}")
                    else:
                        fix_attempt['errors'].append("Validation failed after fix")
                        fix_results['fixes_failed'].append(fix_attempt)
                        print(f"  ❌ Fix failed validation for {jira_id}")
                else:
                    fix_attempt['errors'].append("Organization operation failed")
                    fix_results['fixes_failed'].append(fix_attempt)
                    print(f"  ❌ Organization failed for {jira_id}")
            else:
                # Dry run - just analyze what would be done
                state = organizer.analyze_organization_state(jira_id)
                fix_attempt['would_perform'] = state['action_required']
                fix_attempt['current_state'] = state
                fix_results['fixes_attempted'].append(fix_attempt)
                print(f"  🔍 Would perform: {state['action_required']}")
                
        except Exception as e:
            fix_attempt['errors'].append(f"Exception during fix: {str(e)}")
            fix_results['fixes_failed'].append(fix_attempt)
            print(f"  ❌ Exception fixing {jira_id}: {str(e)}")
    
    fix_results['summary'] = {
        'successful_fixes': len(fix_results['fixes_successful']),
        'failed_fixes': len(fix_results['fixes_failed']),
        'success_rate': len(fix_results['fixes_successful']) / len(tickets_to_fix) * 100 if tickets_to_fix else 0
    }
    
    return fix_results

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python fix_existing_violations.py <command> [runs_directory]")
        print("Commands:")
        print("  analyze  - Analyze current violations")
        print("  dry-run  - Show what would be fixed")
        print("  fix      - Apply fixes")
        print("Example: python fix_existing_violations.py analyze /path/to/runs")
        sys.exit(1)
    
    command = sys.argv[1]
    runs_dir = sys.argv[2] if len(sys.argv) > 2 else "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs"
    
    if command == "analyze":
        print("🔍 Analyzing current violations...")
        violations = analyze_current_violations(runs_dir)
        print(json.dumps(violations, indent=2, default=str))
        
        print(f"\n📊 SUMMARY:")
        print(f"Total runs: {violations['total_runs']}")
        print(f"Violations: {violations['summary']['violation_count']}")
        print(f"Compliant: {violations['summary']['compliant_count']}")
        print(f"Violation rate: {violations['summary']['violation_percentage']:.1f}%")
        
    elif command == "dry-run":
        print("🔍 DRY RUN: Analyzing what would be fixed...")
        results = fix_violations(runs_dir, dry_run=True)
        print(json.dumps(results, indent=2, default=str))
        
    elif command == "fix":
        print("🔧 APPLYING FIXES...")
        print("⚠️  This will modify your directory structure!")
        
        response = input("Are you sure you want to proceed? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Fix cancelled by user")
            sys.exit(0)
        
        results = fix_violations(runs_dir, dry_run=False)
        print(json.dumps(results, indent=2, default=str))
        
        print(f"\n📊 FIX SUMMARY:")
        print(f"Successful: {results['summary']['successful_fixes']}")
        print(f"Failed: {results['summary']['failed_fixes']}")
        print(f"Success rate: {results['summary']['success_rate']:.1f}%")
        
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()