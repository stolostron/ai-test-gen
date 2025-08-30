#!/usr/bin/env python3
"""
Test Case Format Enforcer
Validates and enforces proper test case formatting according to template requirements
"""

import re
import json
import os
from pathlib import Path

class TestCaseFormatEnforcer:
    def __init__(self):
        self.score = 0
        self.max_score = 100
        self.violations = []
        
        # Enhanced scoring weights for comprehensive template enforcement
        self.weights = {
            'files_exist': 20,
            'no_html_tags': 5,
            'correct_login_step': 10,
            'ui_cli_instructions': 20,  # NEW: UI/CLI instructions with verbal explanations
            'sample_data_in_steps': 15,  # NEW: Sample YAMLs/logs/outputs in steps
            'proper_table_structure': 10,  # NEW: Proper table headers with UI/CLI/Expected columns
            'required_sections': 10,  # Description/Setup sections
            'sample_outputs': 5,
            'no_internal_scripts': 5
        }
        
    def validate_test_cases(self, file_path):
        """Main validation method"""
        if not os.path.exists(file_path):
            self.violations.append(f"❌ Test cases file not found: {file_path}")
            return self._calculate_final_score()
            
        # Files exist check
        self.score += self.weights['files_exist']
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Enhanced validation checks
        self._check_html_tags(content)
        self._check_login_step_format(content)
        self._check_ui_cli_instructions(content)  # NEW: UI/CLI instructions with verbal explanations
        self._check_sample_data_in_steps(content)  # NEW: Sample YAMLs/logs/outputs in steps
        self._check_proper_table_structure(content)  # NEW: Proper table headers
        self._check_required_sections(content)  # NEW: Description/Setup sections
        self._check_sample_outputs(content)
        self._check_internal_scripts(content)
        self._check_table_formatting(content)
        self._check_markdown_structure(content)
        
        return self._calculate_final_score()
        
    def _check_html_tags(self, content):
        """Check for HTML tags (10-point deduction)"""
        html_patterns = [
            r'<br/?>', r'<b>', r'</b>', r'<i>', r'</i>',
            r'<div>', r'</div>', r'<span>', r'</span>'
        ]
        
        found_html = []
        for pattern in html_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_html.extend(matches)
                
        if found_html:
            self.violations.append(f"❌ HTML tags found: {found_html} (-{self.weights['no_html_tags']} points)")
        else:
            self.score += self.weights['no_html_tags']
            
    def _check_login_step_format(self, content):
        """Check for exact login step format (15-point deduction)"""
        required_pattern = r'\*\*Step 1: Log into the ACM hub cluster\*\*'
        
        if re.search(required_pattern, content):
            self.score += self.weights['correct_login_step']
        else:
            self.violations.append(f"❌ Incorrect login step format. Must be exactly: **Step 1: Log into the ACM hub cluster** (-{self.weights['correct_login_step']} points)")
            
    def _check_deployment_status_header(self, content):
        """Check for deployment status header in Complete Analysis (15-point deduction)"""
        # This check would be for Complete-Analysis.md file
        # For now, just checking if the test cases have proper structure
        if "## Test Case" in content:
            self.score += self.weights['deployment_status_header']
        else:
            self.violations.append(f"❌ Missing proper test case structure (-{self.weights['deployment_status_header']} points)")
            
    def _check_sample_outputs(self, content):
        """Check for sample outputs in backticks (10-point deduction)"""
        # Count code blocks with realistic outputs
        code_block_pattern = r'`[^`]+`'
        code_blocks = re.findall(code_block_pattern, content)
        
        if len(code_blocks) >= 10:  # Expect multiple sample outputs
            self.score += self.weights['sample_outputs']
        else:
            self.violations.append(f"❌ Insufficient sample outputs in backticks. Found {len(code_blocks)}, expected 10+ (-{self.weights['sample_outputs']} points)")
            
    def _check_internal_scripts(self, content):
        """Check for internal script references (10-point deduction)"""
        internal_script_patterns = [
            r'setup_clc', r'login_oc', r'bin/setup_clc'
        ]
        
        found_scripts = []
        for pattern in internal_script_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_scripts.append(pattern)
                
        if found_scripts:
            self.violations.append(f"❌ Internal script references found: {found_scripts} (-{self.weights['no_internal_scripts']} points)")
        else:
            self.score += self.weights['no_internal_scripts']
            
    def _check_table_formatting(self, content):
        """Check for proper table formatting"""
        table_pattern = r'\| Step \| Expected Result \|'
        
        if re.search(table_pattern, content):
            # Check for broken table formatting (multi-line cells)
            broken_table_pattern = r'\|[^|]*```[^|]*\|'
            if re.search(broken_table_pattern, content, re.DOTALL):
                self.violations.append("❌ Broken table formatting - multi-line code blocks in table cells")
                return
                
            # Check that all table rows are single-line
            table_rows = re.findall(r'\|.*\|.*\|', content)
            broken_rows = [row for row in table_rows if '\n' in row]
            
            if broken_rows:
                self.violations.append(f"❌ Multi-line table rows found: {len(broken_rows)} rows")
            else:
                self.score += 5  # Partial credit for other formatting
        else:
            self.violations.append("❌ Missing proper table headers")
            
    def _check_markdown_structure(self, content):
        """Check for proper markdown structure"""
        # Check for test case headers
        test_case_pattern = r'## Test Case \d+:'
        test_cases = re.findall(test_case_pattern, content)
        
        if len(test_cases) >= 3:  # Expect multiple test cases
            self.score += 3  # Partial credit for other formatting
        else:
            self.violations.append(f"❌ Insufficient test cases. Found {len(test_cases)}, expected 3+")
            
        # Check for description and setup sections
        required_sections = ['**Description:**', '**Setup:**']
        for section in required_sections:
            if section not in content:
                self.violations.append(f"❌ Missing required section: {section}")
            else:
                self.score += 1  # Partial credit for other formatting
    
    def _check_ui_cli_instructions(self, content):
        """Check for UI/CLI instructions with verbal explanations in tables (20-point deduction)"""
        # Look for tables with proper UI/CLI instruction columns
        table_pattern = r'\|.*Action.*\|.*Expected Result.*\|'
        tables_found = re.findall(table_pattern, content, re.IGNORECASE)
        
        # Check for verbal explanations in table cells
        ui_cli_pattern = r'Navigate to.*\|.*oc .*\|.*Login successful'
        ui_cli_matches = re.findall(ui_cli_pattern, content, re.IGNORECASE)
        
        if len(ui_cli_matches) >= 3:  # Expect multiple UI/CLI instructions
            self.score += self.weights['ui_cli_instructions']
        else:
            self.violations.append(f"❌ Insufficient UI/CLI instructions with verbal explanations. Found {len(ui_cli_matches)}, expected 3+ (-{self.weights['ui_cli_instructions']} points)")
    
    def _check_sample_data_in_steps(self, content):
        """Check for sample YAMLs/logs/terminal outputs in test steps (15-point deduction)"""
        # Look for YAML blocks
        yaml_pattern = r'```yaml[\s\S]*?```'
        yaml_blocks = re.findall(yaml_pattern, content)
        
        # Look for terminal output samples
        terminal_pattern = r'`[^`]*status.*[^`]*`|`[^`]*created.*[^`]*`|`[^`]*Ready.*[^`]*`'
        terminal_outputs = re.findall(terminal_pattern, content)
        
        total_samples = len(yaml_blocks) + len(terminal_outputs)
        
        if total_samples >= 5:  # Expect multiple sample data elements
            self.score += self.weights['sample_data_in_steps']
        else:
            self.violations.append(f"❌ Insufficient sample YAMLs/logs/terminal outputs. Found {total_samples}, expected 5+ (-{self.weights['sample_data_in_steps']} points)")
    
    def _check_proper_table_structure(self, content):
        """Check for proper table headers with UI/CLI/Expected columns (10-point deduction)"""
        # Look for tables with proper headers
        proper_header_pattern = r'\|\s*Step\s*\|\s*Action\s*\|\s*Expected Result\s*\|'
        proper_headers = re.findall(proper_header_pattern, content, re.IGNORECASE)
        
        if len(proper_headers) >= 3:  # Expect multiple properly formatted tables
            self.score += self.weights['proper_table_structure']
        else:
            self.violations.append(f"❌ Missing proper table headers with Step|Action|Expected Result format (-{self.weights['proper_table_structure']} points)")
    
    def _check_required_sections(self, content):
        """Check for required Description and Setup sections (10-point deduction)"""
        required_sections = ['**Description**:', '**Setup**:']
        found_sections = 0
        
        for section in required_sections:
            if section in content:
                found_sections += 1
        
        if found_sections >= 2:
            self.score += self.weights['required_sections']
        else:
            missing = [s for s in required_sections if s not in content]
            self.violations.append(f"❌ Missing required sections: {missing} (-{self.weights['required_sections']} points)")
                
    def _calculate_final_score(self):
        """Calculate final score and generate report"""
        percentage = (self.score / self.max_score) * 100
        
        result = {
            'score': self.score,
            'max_score': self.max_score,
            'percentage': round(percentage, 1),
            'passed': percentage >= 85,
            'violations': self.violations,
            'target': 85
        }
        
        return result
        
    def generate_enforcement_report(self, file_path):
        """Generate comprehensive enforcement report"""
        result = self.validate_test_cases(file_path)
        
        report = f"""
# TEST CASE FORMAT VALIDATION REPORT

**File:** {file_path}
**Score:** {result['score']}/{result['max_score']} ({result['percentage']}%)
**Target:** {result['target']}% (target compliances)
**Status:** {'✅ PASSED' if result['passed'] else '❌ FAILED'}

## Validation Results

### Scoring Breakdown:
- Files exist: 30 points
- No HTML tags: 10 points  
- Correct login step: 15 points
- Deployment status header: 15 points
- Sample outputs: 10 points
- No internal scripts: 10 points
- Other formatting: 10 points

### Violations Found:
"""
        
        if result['violations']:
            for violation in result['violations']:
                report += f"- {violation}\n"
        else:
            report += "- ✅ No violations found\n"
            
        report += f"""
### Recommendations:

1. **Mandatory Login Format:** Use exact text: "**Step 1: Log into the ACM hub cluster**"
2. **Table Formatting:** Keep all table cells single-line, no multi-line code blocks
3. **Sample Outputs:** Include realistic outputs in backticks: `namespace/test-ns created`
4. **HTML Tags:** Never use `<br/>`, `<b>`, `<i>` - use markdown instead
5. **Internal Scripts:** Never mention `setup_clc` or `login_oc`

### Format Example:
```markdown
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Login successful: `Login successful. You have access to 67 projects.` |
```

**Generated:** {result}
"""
        
        return report

def main():
    """Main function for command-line usage"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python test_case_format_enforcer.py <test_cases_file.md>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    enforcer = TestCaseFormatEnforcer()
    result = enforcer.validate_test_cases(file_path)
    
    print(f"Score: {result['score']}/{result['max_score']} ({result['percentage']}%)")
    print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}")
    
    if result['violations']:
        print("\nViolations:")
        for violation in result['violations']:
            print(f"  {violation}")
            
    # Generate full report
    report = enforcer.generate_enforcement_report(file_path)
    report_path = file_path.replace('.md', '_validation_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"\nFull report saved to: {report_path}")

if __name__ == "__main__":
    main()