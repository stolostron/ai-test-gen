#!/usr/bin/env python3
"""
Complete Analysis Report Format Enforcer
Validates and enforces the fixed Complete Report template format
"""

import re
import json
import os
from pathlib import Path

class CompleteReportFormatEnforcer:
    def __init__(self):
        self.score = 0
        self.max_score = 100
        self.violations = []
        
        # Fixed template format scoring weights
        self.weights = {
            'environment_feature_status': 25,  # Phase 0: Test env has feature + working status
            'implementation_analysis': 25,    # Real code fetches from dev repo + brief explanation
            'test_scenarios_coverage': 25,    # Main test scenarios + clear why explanation
            'business_impact': 20,           # Business impact of the feature
            'required_structure': 5          # Basic structure and formatting
        }
        
        # Required sections for the fixed template
        self.required_sections = {
            'environment_status': [
                'Test Environment Feature Analysis',
                'Feature Availability',
                'Feature Working Status'
            ],
            'implementation_analysis': [
                'Implementation Analysis',
                'Code Repository Analysis',
                'Change Analysis'
            ],
            'test_scenarios': [
                'Test Scenarios Coverage',
                'Test Case Rationale'
            ],
            'business_impact': [
                'Business Impact',
                'Customer Value'
            ]
        }
        
    def validate_complete_report(self, file_path):
        """Main validation method for Complete Analysis Report"""
        if not os.path.exists(file_path):
            self.violations.append(f"❌ Complete Analysis Report not found: {file_path}")
            return self._calculate_final_score()
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Template format validation checks
        self._check_environment_feature_status(content)
        self._check_implementation_analysis(content)  
        self._check_test_scenarios_coverage(content)
        self._check_business_impact(content)
        self._check_required_structure(content)
        
        return self._calculate_final_score()
        
    def _check_environment_feature_status(self, content):
        """Check for environment feature status analysis (25 points)"""
        # Look for Phase 0 environment assessment information
        env_patterns = [
            r'Test Environment.*Feature.*Analysis',
            r'Feature.*Availability.*in.*Environment',
            r'Feature.*Working.*Status',
            r'Environment.*Version.*Detection',
            r'ClusterCurator.*Available.*in.*Environment'
        ]
        
        found_env_sections = 0
        for pattern in env_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_env_sections += 1
                
        # Check for clear statements about feature availability and working status
        status_patterns = [
            r'feature.*is.*available',
            r'feature.*is.*working',
            r'feature.*is.*not.*available',
            r'feature.*is.*not.*working',
            r'ClusterCurator.*operator.*is.*installed',
            r'environment.*supports.*digest.*based.*upgrades'
        ]
        
        found_status = 0
        for pattern in status_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_status += 1
                
        if found_env_sections >= 2 and found_status >= 2:
            self.score += self.weights['environment_feature_status']
        else:
            self.violations.append(f"❌ Missing environment feature status analysis. Found {found_env_sections} env sections, {found_status} status statements. Required: Phase 0 info, feature availability, working status (-{self.weights['environment_feature_status']} points)")
            
    def _check_implementation_analysis(self, content):
        """Check for implementation analysis with real code fetches (25 points)"""
        # Look for code repository analysis
        code_patterns = [
            r'Implementation.*Analysis',
            r'Code.*Repository.*Analysis', 
            r'GitHub.*Repository.*Analysis',
            r'PR.*#\d+',  # Pull request references
            r'```[a-z]*\n[\s\S]*?```',  # Code blocks
            r'stolostron/.*',  # Repository references
            r'conditionalUpdates.*→.*availableUpdates.*→.*image.*tag'  # Specific implementation details
        ]
        
        found_code_sections = 0
        for pattern in code_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found_code_sections += len(matches)
            
        # Check for brief explanation of changes
        explanation_patterns = [
            r'changes.*briefly',
            r'implementation.*includes',
            r'algorithm.*implements',
            r'fallback.*mechanism',
            r'three.*tier.*fallback'
        ]
        
        found_explanations = 0
        for pattern in explanation_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_explanations += 1
                
        if found_code_sections >= 3 and found_explanations >= 2:
            self.score += self.weights['implementation_analysis']
        else:
            self.violations.append(f"❌ Missing implementation analysis with real code fetches. Found {found_code_sections} code references, {found_explanations} explanations. Required: dev repo code + brief change explanation (-{self.weights['implementation_analysis']} points)")
            
    def _check_test_scenarios_coverage(self, content):
        """Check for test scenarios coverage with clear rationale (25 points)"""
        # Look for main test scenarios mentioned
        scenario_patterns = [
            r'Test.*Scenarios.*Coverage',
            r'Verify.*ClusterCurator.*Digest.*Based.*Upgrade.*Basic.*Flow',
            r'Verify.*ClusterCurator.*Fallback.*Mechanism',
            r'Verify.*ClusterCurator.*Three.*Tier.*Fallback.*Chain',
            r'disconnected.*environment',
            r'Amadeus.*requirements'
        ]
        
        found_scenarios = 0
        for pattern in scenario_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_scenarios += 1
                
        # Check for clear rationale (why these scenarios)
        rationale_patterns = [
            r'why.*clearly',
            r'Test.*Case.*Rationale',
            r'rationale.*for.*testing',
            r'why.*these.*scenarios',
            r'coverage.*ensures',
            r'scenarios.*address.*customer.*requirements'
        ]
        
        found_rationale = 0
        for pattern in rationale_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_rationale += 1
                
        if found_scenarios >= 3 and found_rationale >= 2:
            self.score += self.weights['test_scenarios_coverage']
        else:
            self.violations.append(f"❌ Missing test scenarios coverage with clear rationale. Found {found_scenarios} scenarios, {found_rationale} rationale explanations. Required: main test scenarios + clear why explanation (-{self.weights['test_scenarios_coverage']} points)")
            
    def _check_business_impact(self, content):
        """Check for business impact analysis (20 points)"""
        # Look for business impact section
        business_patterns = [
            r'Business.*Impact',
            r'Customer.*Value',
            r'customer.*benefits',
            r'business.*value',
            r'operational.*improvement',
            r'disconnected.*environments.*support',
            r'Amadeus.*customer.*requirements',
            r'enterprise.*value'
        ]
        
        found_business = 0
        for pattern in business_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_business += 1
                
        if found_business >= 3:
            self.score += self.weights['business_impact']
        else:
            self.violations.append(f"❌ Missing business impact analysis. Found {found_business} business references. Required: business impact of the feature (-{self.weights['business_impact']} points)")
            
    def _check_required_structure(self, content):
        """Check for basic required structure (5 points)"""
        structure_patterns = [
            r'# Complete Analysis Report',
            r'## .*Analysis',
            r'## .*Summary',
            r'**Generated:**'
        ]
        
        found_structure = 0
        for pattern in structure_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_structure += 1
                
        if found_structure >= 3:
            self.score += self.weights['required_structure']
        else:
            self.violations.append(f"❌ Missing required report structure. Found {found_structure} structure elements (-{self.weights['required_structure']} points)")
            
    def _calculate_final_score(self):
        """Calculate final score and generate result"""
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
        
    def generate_template_enforcement_report(self, file_path):
        """Generate comprehensive template enforcement report"""
        result = self.validate_complete_report(file_path)
        
        report = f"""
# COMPLETE ANALYSIS REPORT TEMPLATE VALIDATION

**File:** {file_path}
**Score:** {result['score']}/{result['max_score']} ({result['percentage']}%)
**Target:** {result['target']}% (template compliance)
**Status:** {'✅ PASSED' if result['passed'] else '❌ FAILED'}

## Fixed Template Format Requirements

### 1. Environment Feature Status Analysis (25 points)
- Address if test env has the feature (Phase 0 info)
- Clearly state if feature is working in test env or not
- If not available, clearly state that

### 2. Implementation Analysis (25 points)
- Provide real code fetches from dev repo (collected earlier)
- Explain the changes briefly
- Include repository analysis and PR references

### 3. Test Scenarios Coverage (25 points)
- Address main test scenarios covered in test report
- Explain why these scenarios clearly
- Provide test case rationale

### 4. Business Impact (20 points)
- Business impact of the feature
- Customer value and benefits
- Operational improvements

### 5. Required Structure (5 points)
- Proper report structure and formatting
- Required sections and headers

## Validation Results

### Violations Found:
"""
        
        if result['violations']:
            for violation in result['violations']:
                report += f"- {violation}\n"
        else:
            report += "- ✅ No violations found - Template compliance achieved\n"
            
        report += f"""
### Template Example Structure:

```markdown
# Complete Analysis Report for ACM-XXXXX

## 1. Test Environment Feature Analysis
**Feature Availability in Environment**: [YES/NO based on Phase 0 info]
**Feature Working Status**: [WORKING/NOT WORKING/UNKNOWN - clear statement]
**Environment Details**: [Version, platform, capabilities from Phase 0]

## 2. Implementation Analysis
**Code Repository Analysis**: [Real code fetches from dev repo]
**Implementation Changes**: [Brief explanation of changes]
**PR References**: [PR #XXX details and implementation]

## 3. Test Scenarios Coverage
**Main Test Scenarios**: 
- Verify ClusterCurator Digest-Based Upgrade Basic Flow
- Verify ClusterCurator Fallback Mechanism
- Verify ClusterCurator Three-Tier Fallback Chain

**Test Case Rationale**: [Why these scenarios clearly - customer requirements, etc.]

## 4. Business Impact
**Customer Value**: [Business impact of the feature]
**Operational Benefits**: [Improvements for customers]
**Enterprise Value**: [Strategic importance]
```

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report

def main():
    """Main function for command-line usage"""
    import sys
    from datetime import datetime
    
    if len(sys.argv) != 2:
        print("Usage: python complete_report_format_enforcer.py <complete_analysis_file.md>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    enforcer = CompleteReportFormatEnforcer()
    result = enforcer.validate_complete_report(file_path)
    
    print(f"Score: {result['score']}/{result['max_score']} ({result['percentage']}%)")
    print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}")
    
    if result['violations']:
        print("\nViolations:")
        for violation in result['violations']:
            print(f"  {violation}")
            
    # Generate full report
    report = enforcer.generate_template_enforcement_report(file_path)
    report_path = file_path.replace('.md', '_template_validation_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"\nFull template validation report saved to: {report_path}")

if __name__ == "__main__":
    main()