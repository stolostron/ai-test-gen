# Runs Directory - Z-Stream Analysis Engine

This directory contains active pipeline failure analysis runs and results.

## Overview

The `runs/` directory stores all pipeline analysis outputs, organized by pipeline ID for easy access and historical reference. Each analysis run produces standardized reports following the Executive + Detailed format.

## Directory Structure

```
runs/
├── README.md                           # This file - Runs documentation
├── clc-e2e-pipeline-3223/              # Example: Active pipeline analysis
│   ├── Executive-Summary.md            # High-level stakeholder report
│   ├── Detailed-Analysis.md            # Technical deep-dive report
│   ├── pipeline_data.json              # Structured build metadata (optional)
│   ├── failed_tests.json               # Test failure details (optional)
│   ├── intelligent_analysis.json       # AI analysis results (optional)
│   └── artifacts/                      # Downloaded Jenkins artifacts (optional)
│       ├── console.log                 # Build console output
│       ├── test-results/               # Test result files
│       └── screenshots/                # Failure screenshots
└── <PIPELINE-ID>/                      # Template for new analysis runs
    ├── metadata.json                   # Analysis run metadata
    └── latest -> run-001-YYYYMMDD-HHMM # Symlink to latest run (optional)
```

## Current Status

**Active Analyses:** 1 pipeline (clc-e2e-pipeline-3223)  
**Analysis Format:** AI-Generated Executive + Detailed + Action Plan  
**Storage Method:** AI-organized file structure with quality validation  
**Enhancement:** Pure AI workflow with intelligent error handling

## Analysis Output Format

### Standard Files

Every pipeline analysis includes:
1. **Executive-Summary.md** - Stakeholder-focused overview
2. **Detailed-Analysis.md** - Technical deep-dive with recommendations

### Optional Files

Depending on analysis depth:
- **pipeline_data.json** - Structured build metadata
- **failed_tests.json** - Test failure classifications
- **intelligent_analysis.json** - AI analysis insights
- **artifacts/** - Downloaded Jenkins artifacts when accessible

### File Naming Convention

```
runs/
└── {PIPELINE-ID}/
    ├── Executive-Summary.md
    ├── Detailed-Analysis.md
    ├── metadata.json (optional)
    └── artifacts/ (optional)
```

Pipeline ID formats:
- `clc-e2e-pipeline-3223` (Jenkins job name + build number)
- `pipeline-XXXX` (simplified format)
- `{JOB-NAME}-{BUILD-NUMBER}` (full Jenkins format)

## Analysis Workflow

### AI-Enhanced Input Processing
1. **Intelligent URL Analysis**: AI parses and validates Jenkins URLs
2. **Smart Data Collection**: AI-managed curl with intelligent error recovery
3. **AI Analysis Workflows**: Multi-stage AI processing and classification
4. **AI Report Generation**: Professional Executive + Detailed + Action Plan
5. **AI Quality Assurance**: Validation and organized storage
6. **Intelligent Storage**: AI-organized output with metadata and quality metrics

### Data Extraction Methods

**AI-Managed Data Extraction:**
```markdown
# AI intelligently manages all data extraction
"Analyze this Jenkins pipeline failure: [JENKINS_URL]"

# AI automatically executes with error handling:
# ✅ curl -k -s "${JENKINS_URL}/api/json" → metadata.json
# ✅ curl -k -s "${JENKINS_URL}/consoleText" → console.log  
# ✅ curl -k -s "${JENKINS_URL}/testReport/api/json" → test-results.json
# ✅ Intelligent retry logic for transient failures
# ✅ WebFetch fallback for certificate issues
# ✅ Data validation before proceeding to analysis
```

**Enhanced Capabilities:**
- ✅ **Intelligent Error Recovery**: AI handles network issues and retries
- ✅ **Adaptive Extraction**: AI adjusts strategy based on Jenkins response
- ✅ **Quality Validation**: AI ensures data completeness before analysis
- ✅ **Graceful Degradation**: AI provides analysis even with partial data

## Active Analyses

### clc-e2e-pipeline-3223

**Status:** ✅ Complete analysis available  
**Jenkins URL:** `https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc-clc-e2e-pipeline/3223/`  
**Analysis Date:** Recent (example analysis)  
**Reports:**
- `Executive-Summary.md` - Stakeholder overview
- `Detailed-Analysis.md` - Technical deep-dive

**Key Findings:**
- Real pipeline failure analysis
- Demonstrates analysis output format
- Shows Executive + Detailed reporting structure

## Usage Patterns

### Creating New Analyses

**From Root Repository:**
```bash
# Quick analysis
/analyze-pipeline-failures clc-e2e-pipeline-3223

# Comprehensive analysis with artifacts
/analyze-pipeline-failures clc-e2e-pipeline-3223 --extract-artifacts

# Pattern analysis
/analyze-pipeline-failures clc-e2e-pipeline-3223 --pattern-analysis
```

**From Application Directory:**
```bash
cd apps/z-stream-analysis

# Use Claude to analyze Jenkins URLs
# Example: "Analyze this Jenkins pipeline failure: https://jenkins-url/job/pipeline/123/"
# Results automatically stored in runs/{PIPELINE-ID}/
```

### Accessing Analysis Results

```bash
# View executive summary
cat runs/clc-e2e-pipeline-3223/Executive-Summary.md

# View detailed analysis
cat runs/clc-e2e-pipeline-3223/Detailed-Analysis.md

# List all analyses
ls runs/

# Check analysis completeness
ls runs/clc-e2e-pipeline-3223/
```

## Analysis Quality Standards

### Executive Summary Requirements
- **Stakeholder Focus**: Non-technical language for management
- **Business Impact**: Timeline and resource implications
- **Action Plan**: Clear next steps with ownership
- **Risk Assessment**: Recurrence potential and mitigation

### Detailed Analysis Requirements
- **Technical Depth**: Complete error investigation
- **Root Cause**: Specific failure identification
- **Historical Context**: Pattern recognition and trends
- **Actionable Recommendations**: Specific remediation steps

## Integration Points

### Unified Commands
- Analysis results accessible via root repository commands
- Consistent output format across all analysis types
- Integration with broader AI test generation suite

### External Tools
- **JIRA Integration**: Action items can be converted to tickets
- **Slack Notifications**: Summary reports for team communication
- **Dashboard Export**: Structured data for monitoring tools
- **Email Reports**: Professional distribution of analysis results

## Data Retention

### Active Runs
- Stored in `runs/` directory
- Accessible for immediate reference
- Used for pattern analysis across pipelines

### Archive Policy
- Historical data moved to `archive/` directory (if needed)
- Retention based on organizational requirements
- Pattern data preserved for trend analysis

## Troubleshooting

### Common Issues

**Missing Analysis Files:**
- Check pipeline ID format
- Verify Jenkins URL accessibility
- Confirm curl/WebFetch data extraction success

**Incomplete Analysis:**
- Review Jenkins permissions and artifact availability
- Check network access to Jenkins instance
- Verify Claude analysis completion

**Format Inconsistencies:**
- Ensure templates are followed
- Validate Executive + Detailed format
- Check for required sections in reports

### Analysis Validation

```bash
# Check analysis completeness
ls runs/{PIPELINE-ID}/

# Verify required files
test -f runs/{PIPELINE-ID}/Executive-Summary.md
test -f runs/{PIPELINE-ID}/Detailed-Analysis.md

# Review analysis quality
head -20 runs/{PIPELINE-ID}/Executive-Summary.md
```

## Best Practices

### Naming Conventions
- Use full Jenkins job name + build number when possible
- Maintain consistency across similar pipeline types
- Include date stamps for multiple analysis runs of same pipeline

### Analysis Depth
- Always provide both Executive and Detailed reports
- Include specific remediation recommendations
- Link to historical patterns when relevant
- Ensure actionable outcomes for all stakeholders

### Quality Assurance
- Review analysis completeness before distribution
- Validate technical accuracy of recommendations
- Ensure appropriate detail level for each audience
- Maintain professional formatting and language

---

**Active Status:** Production-ready analysis storage with real examples available for reference and pattern development