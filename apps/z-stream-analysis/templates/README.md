# Templates Directory - Z-Stream Analysis Engine

This directory contains report templates and validation scripts for consistent Jenkins pipeline failure analysis.

## Overview

The templates directory provides standardized formats for analysis output and validation procedures to ensure consistent, high-quality reporting across all pipeline failure investigations.

## Directory Structure

```
templates/
├── README.md                    # This file - Templates documentation
├── report-templates/            # Standardized report formats
│   ├── executive-summary.md     # Template for stakeholder reports
│   ├── detailed-analysis.md     # Template for technical deep-dives
│   ├── failure-classification.md # Template for failure categorization
│   └── action-items.md          # Template for remediation steps
└── validation-scripts/          # Analysis validation procedures
    ├── data-validation.sh       # Validate extracted Jenkins data
    ├── report-validation.sh     # Validate generated reports
    └── completeness-check.sh    # Ensure analysis completeness
```

## Current Status

**Status:** ✅ Enhanced with AI-Powered Generation  
**Templates:** AI-generated reports using intelligent workflows  
**Validation:** AI-powered quality assurance and validation  
**Location:** See `.claude/workflows/ai-report-generation.md` for AI templates

## Report Templates

### Executive Summary Template

**Purpose:** High-level analysis for stakeholders and management  
**Audience:** Project managers, team leads, executives  
**Format:** Concise, action-oriented, business-focused

**Template Sections:**
- **Pipeline Overview**: Build identification and context
- **Failure Summary**: High-level failure description
- **Impact Assessment**: Business and timeline impact
- **Root Cause**: Primary failure reason (non-technical)
- **Action Plan**: Immediate and long-term remediation steps
- **Risk Assessment**: Potential for recurrence and mitigation

### Detailed Analysis Template

**Purpose:** Technical deep-dive for engineering teams  
**Audience:** Developers, QE engineers, DevOps teams  
**Format:** Comprehensive, technical, actionable

**Template Sections:**
- **Build Metadata**: Technical build information
- **Failure Timeline**: Chronological failure analysis
- **Error Analysis**: Detailed error investigation
- **System State**: Environment and configuration analysis
- **Pattern Recognition**: Historical context and trends
- **Technical Recommendations**: Specific remediation steps
- **Prevention Measures**: Long-term improvement suggestions

### Failure Classification Template

**Purpose:** Systematic categorization of failure types  
**Categories:**
- **Infrastructure Failures**: Network, resources, environment
- **Test Failures**: Application logic, test code, data issues
- **Build Failures**: Compilation, dependencies, configuration
- **Timeout Failures**: Performance, resource contention
- **External Failures**: Third-party services, network dependencies

### Action Items Template

**Purpose:** Structured remediation planning  
**Format:**
- **Immediate Actions**: Critical fixes required within 24 hours
- **Short-term Actions**: Fixes required within 1 week
- **Long-term Actions**: Process improvements and prevention measures
- **Ownership**: Clear assignment of responsibilities
- **Timeline**: Realistic delivery expectations
- **Success Criteria**: Measurable outcomes

## Validation Scripts Framework

### Data Validation

**Purpose:** Ensure extracted Jenkins data is complete and accurate

```bash
# Framework for data validation
#!/bin/bash
# validate-jenkins-data.sh

# Check required data fields
validate_build_metadata() {
    # Verify build ID, status, duration, timestamp
    # Ensure console log completeness
    # Validate artifact accessibility
}

validate_test_results() {
    # Check test result format
    # Verify failure details
    # Ensure error message completeness
}
```

### Report Validation

**Purpose:** Ensure generated reports meet quality standards

```bash
# Framework for report validation
#!/bin/bash
# validate-report-quality.sh

# Check report completeness
validate_executive_summary() {
    # Verify all required sections present
    # Check business impact assessment
    # Ensure action plan completeness
}

validate_technical_analysis() {
    # Verify technical depth
    # Check error analysis completeness
    # Ensure remediation specificity
}
```

### Completeness Check

**Purpose:** Ensure analysis covers all required aspects

```bash
# Framework for completeness validation
#!/bin/bash
# check-analysis-completeness.sh

# Verify analysis coverage
check_failure_classification() {
    # Ensure proper categorization
    # Verify root cause identification
    # Check pattern recognition
}

check_actionability() {
    # Ensure specific action items
    # Verify ownership assignment
    # Check timeline realism
}
```

## Template Usage

### For AI Analysis Services

AI services use intelligent template generation to ensure:
1. **Dynamic Structure**: AI adapts report format to analysis content
2. **Comprehensive Coverage**: AI ensures all relevant areas are addressed
3. **Professional Quality**: AI validates presentation and formatting standards
4. **Audience Adaptation**: AI customizes content for different stakeholders
5. **Quality Assurance**: AI validates completeness and actionability

### Integration with AI Analysis Workflow

```markdown
# AI-powered workflow with intelligent template generation
1. AI extracts Jenkins data (curl + intelligent error handling)
2. AI processes data through analysis workflows
3. AI generates reports using dynamic templates
4. AI validates report quality and completeness
5. AI organizes output in runs/ directory with metadata
```

## Template Customization

### Organizational Adaptation

Templates can be customized for:
- **Team-specific needs**: Adjust sections based on team requirements
- **Process integration**: Align with existing workflow tools
- **Reporting standards**: Match organizational documentation standards
- **Stakeholder preferences**: Adapt format for audience needs

### Tool Integration

Templates support integration with:
- **JIRA**: Automatic ticket creation from action items
- **Slack**: Formatted notifications with summary data
- **Dashboards**: Structured data export for monitoring tools
- **Email**: Professional report distribution

## Quality Assurance

### Template Standards

All templates maintain:
- **Professional formatting**: Clean, readable structure
- **Consistent terminology**: Standardized technical language
- **Actionable content**: Specific, implementable recommendations
- **Stakeholder focus**: Appropriate detail level for audience

### Validation Criteria

Reports must pass:
- **Completeness checks**: All required sections present
- **Quality standards**: Professional content and formatting
- **Actionability tests**: Specific, implementable recommendations
- **Accuracy validation**: Technical details verified against source data

## Example Usage

### Current Analysis Format

Based on existing examples in `runs/clc-e2e-pipeline-3223/`:
- **Executive-Summary.md**: Stakeholder-focused overview
- **Detailed-Analysis.md**: Technical deep-dive with specific recommendations

### Template Application

Templates ensure:
1. **Consistency**: All analyses follow the same structure
2. **Completeness**: No critical information is missed
3. **Quality**: Professional standards maintained
4. **Actionability**: Clear, implementable next steps provided

---

**Framework Status:** Ready for development - Templates based on proven analysis formats with validation framework for quality assurance