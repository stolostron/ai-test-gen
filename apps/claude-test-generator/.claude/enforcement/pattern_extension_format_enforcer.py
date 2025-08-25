#!/usr/bin/env python3
"""
Pattern Extension Format Enforcer
Enforces proper test case formatting during Pattern Extension Service execution
"""

import re
import json
from pathlib import Path

class PatternExtensionFormatEnforcer:
    def __init__(self):
        self.format_rules = self._load_format_rules()
        
    def _load_format_rules(self):
        """Load format rules from template requirements"""
        return {
            'mandatory_login_format': r'\*\*Step 1: Log into the ACM hub cluster\*\*',
            'html_tag_patterns': [r'<br/?>', r'<b>', r'</b>', r'<i>', r'</i>', r'<div>', r'</div>'],
            'internal_script_patterns': ['setup_clc', 'login_oc', 'bin/setup_clc'],
            'table_header_pattern': r'\| Step \| Expected Result \|',
            'sample_output_pattern': r'`[^`]+`',
            'test_case_header_pattern': r'## Test Case \d+:',
            'required_sections': ['**Description:**', '**Setup:**']
        }
        
    def validate_generated_content(self, content):
        """Validate generated test case content during Pattern Extension"""
        violations = []
        score = 0
        max_score = 100
        
        # Check mandatory login format (15 points)
        if re.search(self.format_rules['mandatory_login_format'], content):
            score += 15
        else:
            violations.append("❌ Missing mandatory login format: **Step 1: Log into the ACM hub cluster**")
            
        # Check for HTML tags (10 points)
        html_found = []
        for pattern in self.format_rules['html_tag_patterns']:
            if re.search(pattern, content, re.IGNORECASE):
                html_found.append(pattern)
                
        if not html_found:
            score += 10
        else:
            violations.append(f"❌ HTML tags found: {html_found}")
            
        # Check for internal scripts (10 points)
        scripts_found = []
        for script in self.format_rules['internal_script_patterns']:
            if script in content:
                scripts_found.append(script)
                
        if not scripts_found:
            score += 10
        else:
            violations.append(f"❌ Internal script references found: {scripts_found}")
            
        # Check table formatting (20 points)
        if re.search(self.format_rules['table_header_pattern'], content):
            score += 10
            
            # Check for proper single-line table formatting
            if not self._has_multiline_table_cells(content):
                score += 10
            else:
                violations.append("❌ Multi-line table cells detected - use single-line format")
        else:
            violations.append("❌ Missing proper table headers")
            
        # Check sample outputs (10 points)
        sample_outputs = re.findall(self.format_rules['sample_output_pattern'], content)
        if len(sample_outputs) >= 10:
            score += 10
        else:
            violations.append(f"❌ Insufficient sample outputs: {len(sample_outputs)} found, 10+ required")
            
        # Check test case structure (15 points)
        test_cases = re.findall(self.format_rules['test_case_header_pattern'], content)
        if len(test_cases) >= 3:
            score += 15
        else:
            violations.append(f"❌ Insufficient test cases: {len(test_cases)} found, 3+ required")
            
        # Check required sections (20 points)
        sections_found = 0
        for section in self.format_rules['required_sections']:
            if section in content:
                sections_found += 1
                
        score += (sections_found / len(self.format_rules['required_sections'])) * 20
        
        if sections_found < len(self.format_rules['required_sections']):
            missing_sections = [s for s in self.format_rules['required_sections'] if s not in content]
            violations.append(f"❌ Missing required sections: {missing_sections}")
            
        percentage = (score / max_score) * 100
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round(percentage, 1),
            'passed': percentage >= 85,
            'violations': violations
        }
        
    def _has_multiline_table_cells(self, content):
        """Check if table cells contain multi-line content"""
        # Look for table rows with multi-line code blocks
        multiline_pattern = r'\|[^|]*```[^|]*```[^|]*\|'
        return bool(re.search(multiline_pattern, content, re.DOTALL))
        
    def enforce_format_during_generation(self, generated_content):
        """Enforce format rules during test case generation"""
        # Validate current content
        validation_result = self.validate_generated_content(generated_content)
        
        if validation_result['passed']:
            return generated_content, True, validation_result
            
        # Apply automatic corrections where possible
        corrected_content = self._apply_automatic_corrections(generated_content)
        
        # Re-validate corrected content
        corrected_validation = self.validate_generated_content(corrected_content)
        
        return corrected_content, corrected_validation['passed'], corrected_validation
        
    def _apply_automatic_corrections(self, content):
        """Apply automatic corrections to common format issues"""
        corrected = content
        
        # Fix HTML tags
        corrected = re.sub(r'<br/?>', ' - ', corrected, flags=re.IGNORECASE)
        corrected = re.sub(r'<b>(.*?)</b>', r'**\1**', corrected, flags=re.IGNORECASE)
        corrected = re.sub(r'<i>(.*?)</i>', r'*\1*', corrected, flags=re.IGNORECASE)
        
        # Remove internal script references
        corrected = re.sub(r'setup_clc', 'oc login', corrected)
        corrected = re.sub(r'login_oc', 'oc login', corrected)
        corrected = re.sub(r'bin/setup_clc', 'oc login', corrected)
        
        # Fix multi-line table cells by converting to single-line format
        corrected = self._fix_multiline_table_cells(corrected)
        
        return corrected
        
    def _fix_multiline_table_cells(self, content):
        """Convert multi-line table cells to single-line format"""
        lines = content.split('\n')
        fixed_lines = []
        in_table = False
        
        for line in lines:
            # Detect table headers
            if '| Step | Expected Result |' in line:
                in_table = True
                fixed_lines.append(line)
                continue
                
            # Detect end of table
            if in_table and line.strip() == '':
                in_table = False
                
            # Process table rows
            if in_table and line.startswith('|') and line.endswith('|'):
                # Convert multi-line content to single-line with inline backticks
                fixed_line = self._convert_to_single_line_table_row(line)
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
                
        return '\n'.join(fixed_lines)
        
    def _convert_to_single_line_table_row(self, table_row):
        """Convert a table row with potential multi-line content to single-line"""
        # Remove multi-line code blocks and replace with inline code
        # This is a simplified conversion - more sophisticated logic could be added
        
        # Extract content between pipes
        parts = table_row.split('|')[1:-1]  # Remove empty first and last elements
        
        if len(parts) >= 2:
            step_part = parts[0].strip()
            result_part = parts[1].strip()
            
            # Clean up result part - convert multi-line code blocks to inline
            result_part = re.sub(r'```[^`]*```', '`sample output`', result_part, flags=re.DOTALL)
            
            return f"| {step_part} | {result_part} |"
            
        return table_row
        
    def generate_format_enforcement_prompt(self):
        """Generate prompt for Pattern Extension Service with format enforcement"""
        return """
CRITICAL FORMAT REQUIREMENTS - MANDATORY COMPLIANCE:

1. **Login Step Format (EXACT):** 
   **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>`

2. **Table Format (SINGLE-LINE ONLY):**
   | Step | Expected Result |
   |------|-----------------|
   | **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Login successful: `Login successful. You have access to 67 projects.` |

3. **NO HTML TAGS:** Never use <br/>, <b>, <i>, <div> - use markdown instead

4. **Sample Outputs Required:** Every expected result must include realistic output in backticks

5. **NO Internal Scripts:** Never mention setup_clc, login_oc, or bin/setup_clc

6. **Required Sections:** Each test case must have **Description:** and **Setup:**

7. **Single-Line Table Cells:** No multi-line code blocks in table cells - use inline backticks only

TARGET: 85+ points for framework acceptance
VALIDATION: Automatic format validation will be applied
"""

def integrate_with_pattern_extension():
    """Integration point for Pattern Extension Service"""
    enforcer = PatternExtensionFormatEnforcer()
    
    # Return enforcement functions for Pattern Extension Service to use
    return {
        'validate_content': enforcer.validate_generated_content,
        'enforce_format': enforcer.enforce_format_during_generation,
        'format_prompt': enforcer.generate_format_enforcement_prompt(),
        'format_rules': enforcer.format_rules
    }

def main():
    """Test the format enforcer"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python pattern_extension_format_enforcer.py <test_cases_file.md>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    enforcer = PatternExtensionFormatEnforcer()
    result = enforcer.validate_generated_content(content)
    
    print(f"Format Validation Score: {result['score']}/{result['max_score']} ({result['percentage']}%)")
    print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}")
    
    if result['violations']:
        print("\nViolations:")
        for violation in result['violations']:
            print(f"  {violation}")
            
    # Test automatic corrections
    corrected_content, passed, corrected_result = enforcer.enforce_format_during_generation(content)
    
    if corrected_result['percentage'] > result['percentage']:
        print(f"\nAfter automatic corrections: {corrected_result['percentage']}%")
        
        # Save corrected version
        corrected_path = file_path.replace('.md', '_corrected.md')
        with open(corrected_path, 'w', encoding='utf-8') as f:
            f.write(corrected_content)
        print(f"Corrected version saved to: {corrected_path}")

if __name__ == "__main__":
    main()