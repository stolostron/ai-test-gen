#!/usr/bin/env python3
"""
Post-Generation Format Hook
Validates generated test cases and provides corrections
"""

from .test_case_format_enforcer import TestCaseFormatEnforcer
from .framework_format_integration import FrameworkFormatIntegration

def post_generation_format_validation(ticket_id, run_path):
    """Validate generated test cases"""
    integration = FrameworkFormatIntegration(run_path.parent.parent.parent)
    passed, result = integration.validate_generated_test_cases(ticket_id, run_path)
    
    if not passed:
        print(f"⚠️  Format validation warning: {result['percentage']}% (Target: 85%)")
        print("📋 Review format guidance for corrections")
        
    return {
        'validation_passed': passed,
        'score': result['score'],
        'percentage': result['percentage'],
        'violations': result['violations']
    }
