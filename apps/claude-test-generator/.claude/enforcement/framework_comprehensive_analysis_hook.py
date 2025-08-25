#\!/usr/bin/env python3
"""
FRAMEWORK INTEGRATION HOOK - COMPREHENSIVE ANALYSIS ENFORCEMENT
==============================================================

CRITICAL PURPOSE: Intercept ALL framework executions and enforce comprehensive analysis
INTEGRATION POINT: Framework initialization before agent spawning
AUTHORITY: BLOCKING - Can prevent framework execution until compliance achieved
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Import the comprehensive analysis enforcer
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mandatory_comprehensive_analysis_enforcer import enforce_comprehensive_analysis_for_test_plan

class FrameworkComprehensiveAnalysisHook:
    """Integration hook that enforces comprehensive analysis in framework execution"""
    
    def __init__(self):
        self.hook_active = True
        self.enforcement_log = []
        
    def intercept_framework_execution(self, execution_context: dict) -> dict:
        """
        CRITICAL: Intercept framework execution and enforce comprehensive analysis
        
        Must be called BEFORE any agent spawning or framework execution begins
        """
        print("🔒 FRAMEWORK COMPREHENSIVE ANALYSIS HOOK ACTIVATED")
        
        # Extract user input and ticket information
        user_input = execution_context.get('user_input', '')
        ticket_id = execution_context.get('ticket_id', '')
        
        # Enforce comprehensive analysis
        enforcement_result = enforce_comprehensive_analysis_for_test_plan(user_input, ticket_id)
        
        if enforcement_result.get('execution_mode') == 'MANDATORY_COMPREHENSIVE':
            print("🚨 COMPREHENSIVE ANALYSIS MANDATE ACTIVATED")
            
            # Override any framework shortcuts or optimizations
            execution_context.update({
                'force_comprehensive_analysis': True,
                'ignore_previous_runs': True,
                'ignore_chat_context': True,
                'prevent_agent_shortcuts': True,
                'mandate_fresh_analysis': True,
                'enforcement_level': 'ABSOLUTE'
            })
            
            # Log enforcement action
            self.log_enforcement_action('COMPREHENSIVE_ANALYSIS_ENFORCED', {
                'ticket_id': ticket_id,
                'user_input': user_input[:100] + '...' if len(user_input) > 100 else user_input,
                'enforcement_timestamp': datetime.now().isoformat()
            })
            
            print("✅ FRAMEWORK EXECUTION CONTEXT UPDATED FOR COMPREHENSIVE ANALYSIS")
            
        return execution_context
        
    def log_enforcement_action(self, action: str, details: dict):
        """Log enforcement actions for audit trail"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details,
            'hook': 'FrameworkComprehensiveAnalysisHook'
        }
        self.enforcement_log.append(log_entry)
        
    def validate_framework_execution(self, execution_metadata: dict) -> bool:
        """
        Post-execution validation to ensure comprehensive analysis was performed
        """
        print("🔍 VALIDATING FRAMEWORK EXECUTION FOR COMPREHENSIVE ANALYSIS...")
        
        # Check for agent execution completeness
        agents_executed = execution_metadata.get('agents_executed', {})
        required_agents = ['agent_a_jira', 'agent_b_documentation', 'agent_c_github', 'agent_d_environment']
        
        violations = []
        
        for agent in required_agents:
            if agent not in agents_executed:
                violations.append(f"Missing required agent: {agent}")
            else:
                agent_data = agents_executed[agent]
                if isinstance(agent_data, dict):
                    # Check for shortcut indicators
                    if 'reused' in str(agent_data).lower():
                        violations.append(f"Agent {agent} took shortcuts - reused previous analysis")
                    if 'simulated' in str(agent_data).lower():
                        violations.append(f"Agent {agent} used simulated data instead of fresh analysis")
                        
        # Check execution metadata for shortcut indicators
        if 'previous_analysis' in str(execution_metadata).lower():
            violations.append("Framework reused previous analysis - fresh analysis required")
            
        if violations:
            print("🚨 COMPREHENSIVE ANALYSIS VIOLATIONS DETECTED:")
            for violation in violations:
                print(f"   - {violation}")
            return False
            
        print("✅ COMPREHENSIVE ANALYSIS VALIDATION PASSED")
        return True
        
    def save_enforcement_audit(self, run_directory: str):
        """Save enforcement audit trail"""
        audit_path = os.path.join(run_directory, 'comprehensive-analysis-enforcement-audit.json')
        
        audit_data = {
            'hook': 'FrameworkComprehensiveAnalysisHook',
            'version': '1.0-MANDATORY',
            'enforcement_active': self.hook_active,
            'enforcement_actions': self.enforcement_log,
            'guarantee': 'ABSOLUTE_COMPREHENSIVE_ANALYSIS_FOR_ALL_TEST_PLAN_REQUESTS'
        }
        
        os.makedirs(os.path.dirname(audit_path), exist_ok=True)
        with open(audit_path, 'w') as f:
            json.dump(audit_data, f, indent=2)
            
        print(f"📋 Comprehensive analysis enforcement audit: {audit_path}")

# GLOBAL HOOK INSTANCE
_framework_hook = FrameworkComprehensiveAnalysisHook()

def activate_comprehensive_analysis_enforcement():
    """Activate the comprehensive analysis enforcement hook"""
    print("🔒 COMPREHENSIVE ANALYSIS ENFORCEMENT HOOK ACTIVATED")
    print("📋 ALL TEST PLAN GENERATION REQUESTS WILL TRIGGER COMPREHENSIVE ANALYSIS")
    return _framework_hook

def enforce_framework_comprehensive_analysis(execution_context: dict) -> dict:
    """Main enforcement function - call before framework execution"""
    return _framework_hook.intercept_framework_execution(execution_context)

def validate_framework_comprehensive_execution(execution_metadata: dict) -> bool:
    """Validation function - call after framework execution"""
    return _framework_hook.validate_framework_execution(execution_metadata)

def save_comprehensive_analysis_audit(run_directory: str):
    """Save audit trail for comprehensive analysis enforcement"""
    _framework_hook.save_enforcement_audit(run_directory)

# AUTOMATIC ACTIVATION
_framework_hook = activate_comprehensive_analysis_enforcement()

if __name__ == "__main__":
    print("FRAMEWORK COMPREHENSIVE ANALYSIS HOOK")
    print("=====================================")
    
    # Test enforcement
    test_context = {
        'user_input': 'Generate test plan for ACM-22079 using this environment',
        'ticket_id': 'ACM-22079'
    }
    
    result = enforce_framework_comprehensive_analysis(test_context)
    print(f"Enforcement Result: {result.get('force_comprehensive_analysis', False)}")
