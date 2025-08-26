#!/usr/bin/env python3
"""
Pattern Extension Service Format Integration
Ensures Pattern Extension Service generates properly formatted test cases
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from pattern_extension_format_enforcer import PatternExtensionFormatEnforcer

class PatternExtensionFormatIntegration:
    def __init__(self):
        self.enforcer = PatternExtensionFormatEnforcer()
        
    def enhance_pattern_extension_prompt(self, base_prompt):
        """Enhance Pattern Extension prompt with format requirements"""
        format_requirements = self.enforcer.generate_format_enforcement_prompt()
        
        enhanced_prompt = f"""
{base_prompt}

{format_requirements}

CRITICAL: Generated test cases will be automatically validated. 
Target: target compliances for framework acceptance.
Format violations will trigger corrective guidance generation.
"""
        return enhanced_prompt
        
    def validate_and_correct_generated_test_cases(self, generated_content):
        """Validate and apply corrections to generated test cases"""
        corrected_content, passed, result = self.enforcer.enforce_format_during_generation(generated_content)
        
        return {
            'content': corrected_content,
            'passed': passed,
            'validation_result': result,
            'auto_corrected': result['percentage'] > self.enforcer.validate_generated_content(generated_content)['percentage']
        }

# Export integration functions
def get_format_enhanced_prompt(base_prompt):
    integration = PatternExtensionFormatIntegration()
    return integration.enhance_pattern_extension_prompt(base_prompt)
    
def validate_generated_content(content):
    integration = PatternExtensionFormatIntegration()
    return integration.validate_and_correct_generated_test_cases(content)
