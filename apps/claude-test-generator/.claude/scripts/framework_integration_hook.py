#!/usr/bin/env python3
"""
Framework Integration Hook for Intelligent Run Organization
Integrates the intelligent run organizer with the claude-test-generator framework.

This hook ensures the definitive folder organization behavior is enforced
automatically during framework execution.
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from intelligent_run_organizer import IntelligentRunOrganizer

# Add the parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

class FrameworkIntegrationHook:
    def __init__(self, runs_directory: str, log_level: str = "INFO"):
        self.runs_dir = runs_directory
        self.organizer = IntelligentRunOrganizer(runs_directory)
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('FrameworkIntegrationHook')
        
    def pre_framework_execution(self, jira_id: str) -> dict:
        """
        Execute before framework starts test generation.
        Returns the target directory path where framework should create content.
        """
        self.logger.info(f"🚀 PRE-FRAMEWORK: Organizing run for {jira_id}")
        
        try:
            # Analyze current state
            state = self.organizer.analyze_organization_state(jira_id)
            self.logger.info(f"Current state: {state['action_required']}")
            
            # Organize run according to definitive behavior
            result = self.organizer.organize_run(jira_id)
            
            if result['success']:
                target_directory = result['new_run_path']
                self.logger.info(f"✅ Run organized successfully. Target directory: {target_directory}")
                
                return {
                    'success': True,
                    'target_directory': target_directory,
                    'organization_state': state,
                    'organization_result': result,
                    'framework_instruction': f"Create all content in: {target_directory}"
                }
            else:
                self.logger.error(f"❌ Run organization failed: {result.get('errors', [])}")
                return {
                    'success': False,
                    'error': f"Run organization failed: {result.get('errors', [])}",
                    'fallback_directory': f"{self.runs_dir}/{jira_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                }
                
        except Exception as e:
            self.logger.error(f"❌ Exception during pre-framework execution: {str(e)}")
            return {
                'success': False,
                'error': f"Exception: {str(e)}",
                'fallback_directory': f"{self.runs_dir}/{jira_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            }
    
    def post_framework_execution(self, jira_id: str, target_directory: str) -> dict:
        """
        Execute after framework completes test generation.
        Validates organization and performs any cleanup.
        """
        self.logger.info(f"🏁 POST-FRAMEWORK: Validating organization for {jira_id}")
        
        try:
            # Validate organization
            validation = self.organizer.validate_organization(jira_id)
            
            # Check if target directory has content
            target_path = Path(target_directory)
            if target_path.exists():
                files_created = list(target_path.iterdir())
                self.logger.info(f"Files created in target directory: {[f.name for f in files_created]}")
            else:
                self.logger.warning(f"Target directory does not exist: {target_directory}")
            
            # Update latest-run metadata if needed
            if validation['valid'] and validation['run_count'] > 1:
                ticket_parent = Path(self.runs_dir) / jira_id
                if ticket_parent.exists():
                    latest_run_name = Path(target_directory).name
                    self.organizer.create_latest_run_metadata(jira_id, latest_run_name)
                    self.logger.info("Updated latest-run-metadata.json")
            
            return {
                'success': True,
                'validation': validation,
                'target_directory': target_directory,
                'organization_valid': validation['valid'],
                'recommendations': validation.get('issues', [])
            }
            
        except Exception as e:
            self.logger.error(f"❌ Exception during post-framework execution: {str(e)}")
            return {
                'success': False,
                'error': f"Exception: {str(e)}",
                'validation': {'valid': False, 'issues': [str(e)]}
            }
    
    def emergency_cleanup(self, jira_id: str) -> dict:
        """
        Emergency cleanup if framework execution fails.
        Attempts to maintain organization consistency.
        """
        self.logger.warning(f"🚨 EMERGENCY CLEANUP: Attempting cleanup for {jira_id}")
        
        try:
            # Check for any orphaned or incomplete runs
            existing_runs = self.organizer.scan_existing_runs(jira_id)
            cleanup_actions = []
            
            for run in existing_runs:
                # Check if run directory is empty or incomplete
                if run.exists() and run.is_dir():
                    files = list(run.iterdir())
                    if len(files) == 0:
                        # Empty directory - remove it
                        run.rmdir()
                        cleanup_actions.append(f"Removed empty directory: {run.name}")
                        self.logger.info(f"Cleaned up empty directory: {run.name}")
                    elif len(files) < 3:
                        # Incomplete run - log warning but keep
                        cleanup_actions.append(f"Warning: Incomplete run detected: {run.name} ({len(files)} files)")
                        self.logger.warning(f"Incomplete run detected: {run.name}")
            
            return {
                'success': True,
                'cleanup_actions': cleanup_actions,
                'message': 'Emergency cleanup completed'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Exception during emergency cleanup: {str(e)}")
            return {
                'success': False,
                'error': f"Emergency cleanup failed: {str(e)}"
            }

def get_target_directory_for_framework(jira_id: str, runs_directory: str = None) -> str:
    """
    Utility function to get target directory for framework execution.
    This is the main entry point for framework integration.
    """
    if runs_directory is None:
        runs_directory = "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs"
    
    hook = FrameworkIntegrationHook(runs_directory)
    result = hook.pre_framework_execution(jira_id)
    
    if result['success']:
        return result['target_directory']
    else:
        # Return fallback directory if organization fails
        return result['fallback_directory']

def validate_framework_completion(jira_id: str, target_directory: str, runs_directory: str = None) -> dict:
    """
    Utility function to validate framework completion.
    Called after framework finishes test generation.
    """
    if runs_directory is None:
        runs_directory = "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs"
    
    hook = FrameworkIntegrationHook(runs_directory)
    return hook.post_framework_execution(jira_id, target_directory)

def main():
    """Command-line interface for testing integration"""
    if len(sys.argv) < 3:
        print("Usage: python framework_integration_hook.py <command> <jira_id> [runs_directory]")
        print("Commands:")
        print("  pre-framework   - Get target directory for framework")
        print("  post-framework  - Validate framework completion")
        print("  emergency-cleanup - Emergency cleanup")
        print("Example: python framework_integration_hook.py pre-framework ACM-1234")
        sys.exit(1)
    
    command = sys.argv[1]
    jira_id = sys.argv[2]
    runs_dir = sys.argv[3] if len(sys.argv) > 3 else "/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator/runs"
    
    hook = FrameworkIntegrationHook(runs_dir)
    
    if command == "pre-framework":
        result = hook.pre_framework_execution(jira_id)
        print(json.dumps(result, indent=2))
        if result['success']:
            print(f"\n🎯 FRAMEWORK TARGET DIRECTORY: {result['target_directory']}")
        else:
            print(f"\n❌ ORGANIZATION FAILED. Use fallback: {result['fallback_directory']}")
    
    elif command == "post-framework":
        # For testing, assume target directory from pre-framework result
        pre_result = hook.pre_framework_execution(jira_id)
        if pre_result['success']:
            target_dir = pre_result['target_directory']
            result = hook.post_framework_execution(jira_id, target_dir)
            print(json.dumps(result, indent=2))
        else:
            print("❌ Cannot validate - pre-framework failed")
    
    elif command == "emergency-cleanup":
        result = hook.emergency_cleanup(jira_id)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()