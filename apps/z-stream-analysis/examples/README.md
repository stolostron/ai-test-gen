# Examples Directory - Z-Stream Analysis Engine

This directory contains usage examples, demos, and reference implementations for the Z-Stream Analysis Engine.

## Overview

The examples directory provides practical demonstrations of pipeline failure analysis workflows, from basic Jenkins URL analysis to advanced pattern recognition and integration scenarios.

## Directory Structure

```
examples/
├── README.md                    # This file - Examples documentation
├── basic-analysis/              # Simple pipeline analysis examples
│   ├── single-pipeline.md       # Analyze one Jenkins pipeline
│   ├── curl-examples.sh         # Curl-based data extraction examples
│   └── claude-prompts.md        # Example prompts for Claude analysis
├── advanced-analysis/           # Complex analysis scenarios
│   ├── pattern-recognition.md   # Multi-pipeline pattern analysis
│   ├── historical-trends.md     # Trend analysis across time periods
│   └── root-cause-analysis.md   # Deep-dive investigation examples
├── integration-examples/        # External tool integration
│   ├── jira-integration.md      # JIRA ticket creation from analysis
│   ├── slack-notifications.md   # Team notification examples
│   └── dashboard-export.md      # Dashboard data export examples
└── workflow-demos/              # End-to-end workflow demonstrations
    ├── qe-team-workflow.md      # QE team daily failure triage
    ├── devops-workflow.md       # DevOps infrastructure analysis
    └── management-reporting.md  # Executive reporting examples
```

## Current Status

**Status:** ✅ AI-Powered Examples Available  
**Examples:** Real AI service usage patterns and workflows  
**Reference:** Live AI analysis results in `runs/clc-e2e-pipeline-3223/`  
**Enhancement:** Pure AI interface with intelligent orchestration

## Basic Analysis Examples

### Single Pipeline Analysis

**Scenario:** Analyze a single Jenkins pipeline failure  
**Input:** Jenkins URL or Pipeline ID  
**Output:** Executive Summary + Detailed Analysis

```markdown
# Example 1: Direct AI Service (Recommended)
"Analyze this Jenkins pipeline failure: https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc-clc-e2e-pipeline/3223/"

# Example 2: Unified Command (Routes to AI)
/analyze-pipeline-failures clc-e2e-pipeline-3223

# Example 3: Comprehensive Analysis
"Execute comprehensive pipeline analysis with artifact extraction for: [JENKINS_URL]"

# Example 4: Pattern Analysis
"Perform pattern analysis for these pipeline failures: [URL1], [URL2], [URL3]"
```

**AI-Generated Output:**
- `runs/clc-e2e-pipeline-3223/Executive-Summary.md` (AI: Stakeholder-focused)
- `runs/clc-e2e-pipeline-3223/Detailed-Analysis.md` (AI: Technical deep-dive)
- `runs/clc-e2e-pipeline-3223/Action-Plan.md` (AI: Remediation steps)
- `runs/clc-e2e-pipeline-3223/Quality-Assessment.json` (AI: Quality validation)

### Curl-Based Data Extraction

**Primary Methods:**
```bash
# Build metadata extraction
curl -k -s "https://jenkins-server/job/pipeline/123/api/json" | jq '.'

# Console log extraction (full)
curl -k -s "https://jenkins-server/job/pipeline/123/consoleText"

# Console log extraction (tail for failures)
curl -k -s "https://jenkins-server/job/pipeline/123/consoleText" | tail -200

# Specific metadata fields
curl -k -s "https://jenkins-server/job/pipeline/123/api/json" | jq '.result, .duration, .timestamp'

# Test results (if available)
curl -k -s "https://jenkins-server/job/pipeline/123/testReport/api/json"
```

### Claude Analysis Prompts

**Basic Analysis:**
```
Analyze this Jenkins pipeline failure and provide an executive summary and detailed analysis:
[Jenkins URL]
```

**Comprehensive Analysis:**
```
Perform a comprehensive analysis of this Jenkins pipeline failure. Include:
1. Executive summary for stakeholders
2. Detailed technical analysis
3. Root cause identification
4. Actionable remediation steps
5. Pattern recognition from console logs

Jenkins URL: [URL]
```

**Pattern-Focused Analysis:**
```
Analyze this pipeline failure with focus on identifying patterns and trends:
- Historical context
- Recurring failure indicators
- Infrastructure vs. application issues
- Preventive measures

Pipeline: [URL or ID]
```

## Advanced Analysis Examples

### Pattern Recognition

**Multi-Pipeline Analysis:**
```bash
# Analyze multiple related pipelines
/analyze-pipeline-failures clc-e2e-pipeline-3220 --pattern-analysis
/analyze-pipeline-failures clc-e2e-pipeline-3221 --pattern-analysis
/analyze-pipeline-failures clc-e2e-pipeline-3222 --pattern-analysis
/analyze-pipeline-failures clc-e2e-pipeline-3223 --pattern-analysis

# Claude prompt for pattern analysis:
"Analyze these pipeline failures for patterns:
- clc-e2e-pipeline-3220: [URL]
- clc-e2e-pipeline-3221: [URL]  
- clc-e2e-pipeline-3222: [URL]
- clc-e2e-pipeline-3223: [URL]

Identify:
1. Common failure patterns
2. Environmental factors
3. Timing correlations
4. Infrastructure trends"
```

### Historical Trend Analysis

**Time-Based Analysis:**
```bash
# Weekly failure analysis
/analyze-workflow pipeline-failure clc-e2e-pipeline --time-range "2025-08-05 to 2025-08-12"

# Monthly trend analysis
/analyze-workflow pattern-analysis clc-e2e-pipeline --monthly-trends

# Claude prompt for trend analysis:
"Perform historical trend analysis on these pipeline failures:
[List of pipeline URLs/IDs with timestamps]

Focus on:
1. Failure frequency trends
2. Seasonal patterns
3. Environmental correlations
4. Success rate evolution"
```

## Integration Examples

### JIRA Integration

**Automatic Ticket Creation:**
```bash
# Generate JIRA-ready action items
/analyze-pipeline-failures clc-e2e-pipeline-3223 --generate-jira-tickets

# Claude prompt for JIRA integration:
"Analyze this pipeline failure and generate JIRA ticket content:
Pipeline: [URL]

For each major issue identified, provide:
1. Ticket title
2. Description
3. Acceptance criteria
4. Priority level
5. Component assignment"
```

### Slack Notifications

**Team Notifications:**
```bash
# Generate Slack-ready summaries
/analyze-pipeline-failures clc-e2e-pipeline-3223 --slack-summary

# Claude prompt for Slack notifications:
"Create a Slack notification for this pipeline failure:
Pipeline: [URL]

Include:
1. Brief failure summary (2-3 lines)
2. Impact assessment
3. Immediate action required
4. Point of contact
5. Link to detailed analysis"
```

### Dashboard Export

**Monitoring Integration:**
```bash
# Export structured data for dashboards
/analyze-pipeline-failures clc-e2e-pipeline-3223 --export-dashboard-data

# Claude prompt for dashboard integration:
"Extract dashboard metrics from this pipeline failure:
Pipeline: [URL]

Provide JSON output with:
1. Failure categorization
2. Duration metrics
3. Success/failure rates
4. Trend indicators
5. Alert conditions"
```

## Workflow Demonstrations

### QE Team Daily Workflow

**Morning Failure Triage:**
```bash
# 1. Check overnight failures
/analyze-pipeline-failures overnight-failures --quick-summary

# 2. Prioritize critical failures
/analyze-pipeline-failures clc-e2e-pipeline-XXXX --priority-assessment

# 3. Generate team summary
/analyze-workflow team-summary overnight-failures --qe-focused
```

### DevOps Infrastructure Analysis

**Infrastructure Health Check:**
```bash
# 1. Analyze infrastructure-related failures
/analyze-pipeline-failures pipeline-XXXX --focus-infrastructure

# 2. Cross-environment comparison
/analyze-workflow infrastructure-health --env-comparison

# 3. Capacity planning insights
/analyze-workflow capacity-analysis --resource-trends
```

### Management Reporting

**Weekly Executive Summary:**
```bash
# 1. Generate executive summary
/analyze-workflow executive-summary --weekly-pipelines

# 2. Create trend report
/analyze-workflow trend-analysis --management-focused

# 3. Generate action plan
/analyze-workflow action-planning --stakeholder-ready
```

## Real-World Reference

### clc-e2e-pipeline-3223 Analysis

**Available Example:**
- Location: `runs/clc-e2e-pipeline-3223/`
- Executive Summary: Stakeholder-focused overview
- Detailed Analysis: Technical deep-dive
- Jenkins URL: Real pipeline failure analysis

**Usage as Reference:**
```bash
# Review existing analysis structure
cat runs/clc-e2e-pipeline-3223/Executive-Summary.md
cat runs/clc-e2e-pipeline-3223/Detailed-Analysis.md

# Use as template for new analyses
cp runs/clc-e2e-pipeline-3223/Executive-Summary.md runs/new-pipeline/
# Edit content for new pipeline analysis
```

## Best Practices

### Analysis Preparation
1. **Verify Jenkins Access**: Ensure URL accessibility before analysis
2. **Check Data Availability**: Confirm console logs and artifacts are available
3. **Set Context**: Understand pipeline purpose and expected behavior
4. **Define Scope**: Determine analysis depth based on stakeholder needs

### Claude Prompt Engineering
1. **Be Specific**: Clearly define analysis objectives
2. **Provide Context**: Include relevant background information
3. **Request Structure**: Ask for specific output formats
4. **Include Examples**: Reference successful analysis patterns

### Output Optimization
1. **Audience-Appropriate**: Match detail level to reader needs
2. **Actionable Content**: Ensure specific, implementable recommendations
3. **Professional Format**: Maintain consistent, professional presentation
4. **Follow Templates**: Use established formats for consistency

## Development Guidelines

### Creating New Examples

When adding examples:
1. **Real-World Focus**: Base examples on actual pipeline scenarios
2. **Complete Workflows**: Show end-to-end processes
3. **Multiple Audiences**: Include examples for different user types
4. **Integration Points**: Demonstrate external tool connections

### Maintaining Examples

Keep examples current by:
1. **Regular Updates**: Refresh based on new analysis patterns
2. **Tool Evolution**: Update for new feature capabilities
3. **User Feedback**: Incorporate learnings from real usage
4. **Best Practice Evolution**: Update based on improved workflows

---

**Framework Status:** Ready for development - Template structure prepared with real analysis reference available in runs/ directory