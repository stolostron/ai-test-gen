#\!/usr/bin/env python3
"""
MANDATORY COMPREHENSIVE ANALYSIS ENFORCEMENT SYSTEM
==================================================

CRITICAL PURPOSE: Prevent ALL framework shortcuts and force comprehensive analysis
SCOPE: Universal application for ANY test plan generation request
ENFORCEMENT LEVEL: ABSOLUTE - No exceptions, no optimizations, no shortcuts

This system ensures 100% comprehensive analysis regardless of:
- Previous runs existence
- Chat session context
- Time proximity to other runs  
- User familiarity with ticket
- Environment similarities
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

class MandatoryComprehensiveAnalysisEnforcer:
    """Absolute enforcement of comprehensive analysis for all test plan requests"""
    
    def __init__(self):
        self.enforcement_active = True
        self.shortcut_violations = []
        self.analysis_requirements = {
            "agent_a_jira": "MANDATORY_FRESH_ANALYSIS",
            "agent_b_documentation": "MANDATORY_FRESH_ANALYSIS", 
            "agent_c_github": "MANDATORY_FRESH_ANALYSIS",
            "agent_d_environment": "MANDATORY_FRESH_ANALYSIS",
            "qe_intelligence": "MANDATORY_FRESH_ANALYSIS"
        }
        
    def detect_test_plan_generation_request(self, user_input: str) -> bool:
        """
        Detect ANY test plan generation request that requires comprehensive analysis
        
        Triggers include:
        - "generate test plan"
        - "test plan for ACM-XXXXX" 
        - "using this env"
        - Any JIRA ticket reference with generation intent
        """
        test_plan_patterns = [
            r'generate.*test.*plan',
            r'test.*plan.*for.*ACM-\d+',
            r'ACM-\d+.*test.*plan',
            r'using.*env.*test',
            r'create.*test.*cases',
            r'test.*generation',
            r'comprehensive.*test'
        ]
        
        user_input_lower = user_input.lower()
        
        for pattern in test_plan_patterns:
            if re.search(pattern, user_input_lower):
                print(f"🚨 TEST PLAN GENERATION DETECTED: {pattern}")
                return True
                
        return False
        
    def enforce_comprehensive_analysis(self, ticket_id: str) -> dict:
        """
        MANDATORY: Force comprehensive analysis regardless of previous runs
        
        Returns enforcement configuration that PREVENTS all shortcuts
        """
        enforcement_config = {
            "execution_mode": "MANDATORY_COMPREHENSIVE",
            "ignore_previous_runs": True,
            "ignore_chat_context": True, 
            "ignore_time_proximity": True,
            "force_fresh_analysis": True,
            "prevent_agent_shortcuts": True,
            "require_environment_validation": True,
            "mandate_full_4_agent_execution": True,
            "block_context_reuse": True,
            "enforcement_level": "ABSOLUTE",
            "shortcut_tolerance": "ZERO"
        }
        
        print(f"🔒 COMPREHENSIVE ANALYSIS ENFORCED FOR {ticket_id}")
        print("📋 ALL SHORTCUTS BLOCKED - FULL FRAMEWORK EXECUTION REQUIRED")
        
        return enforcement_config
        
    def validate_no_shortcuts_taken(self, execution_log: dict) -> bool:
        """
        Post-execution validation to ensure no shortcuts were taken
        
        Validates:
        - All 4+ agents executed fresh analysis
        - No reuse of previous run data
        - Full environment assessment completed
        - Complete JIRA analysis performed
        """
        violations = []
        
        # Check agent execution freshness
        required_agents = ["agent_a_jira", "agent_b_documentation", "agent_c_github", "agent_d_environment"]
        
        for agent in required_agents:
            if agent not in execution_log.get("agents_executed", {}):
                violations.append(f"Missing agent execution: {agent}")
            elif "reused" in str(execution_log["agents_executed"][agent]).lower():
                violations.append(f"Agent shortcut detected: {agent} reused previous analysis")
                
        # Check for environment assessment freshness
        if "simulated" in str(execution_log).lower():
            violations.append("Environment simulation detected - fresh assessment required")
            
        # Check for JIRA analysis freshness  
        if "previous analysis" in str(execution_log).lower():
            violations.append("JIRA analysis shortcut detected - fresh analysis required")
            
        if violations:
            print("🚨 SHORTCUT VIOLATIONS DETECTED:")
            for violation in violations:
                print(f"   - {violation}")
            return False
            
        print("✅ COMPREHENSIVE ANALYSIS VALIDATED - NO SHORTCUTS DETECTED")
        return True

# GLOBAL ENFORCEMENT INSTANCE
_comprehensive_enforcer = MandatoryComprehensiveAnalysisEnforcer()

def enforce_comprehensive_analysis_for_test_plan(user_input: str, ticket_id: str = None) -> dict:
    """
    MAIN ENFORCEMENT FUNCTION
    
    Call this BEFORE any framework execution when test plan generation detected
    """
    if _comprehensive_enforcer.detect_test_plan_generation_request(user_input):
        
        # Extract ticket ID if not provided
        if not ticket_id:
            ticket_match = re.search(r'ACM-\d+', user_input, re.IGNORECASE)
            if ticket_match:
                ticket_id = ticket_match.group(0).upper()
                
        if ticket_id:
            return _comprehensive_enforcer.enforce_comprehensive_analysis(ticket_id)
        else:
            print("⚠️  Test plan generation detected but no ticket ID found")
            
    return {"enforcement_required": False}

def validate_comprehensive_execution(execution_log: dict) -> bool:
    """Validate that comprehensive analysis was actually performed"""
    return _comprehensive_enforcer.validate_no_shortcuts_taken(execution_log)

if __name__ == "__main__":
    # Test the enforcement system
    test_inputs = [
        "Generate test plan for ACM-22079 using this env",
        "ok now generate actual test plan for the ticket provided", 
        "Create comprehensive test cases for ACM-12345",
        "Just analyzing the ticket"  # Should NOT trigger
    ]
    
    for test_input in test_inputs:
        print(f"
Testing: {test_input}")
        result = enforce_comprehensive_analysis_for_test_plan(test_input)
        print(f"Enforcement: {result.get('execution_mode', 'NONE')}
")
