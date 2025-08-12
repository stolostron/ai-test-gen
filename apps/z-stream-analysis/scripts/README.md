# Scripts Directory - Z-Stream Analysis Engine

**DEPRECATED:** This directory has been replaced with pure AI-powered workflows.

> **Migration Notice:** All shell scripts have been replaced with AI services for robust, consistent analysis. See .claude/docs/AI-ANALYSIS-SERVICE.md for the new AI-powered interface.

## Overview

The Z-Stream Analysis Engine uses a **Claude-first approach** where the primary analysis is performed by Claude AI rather than traditional scripts. This directory serves as a framework for supporting automation and integration.

## Current Status

**Status:** ⚠️  DEPRECATED - Replaced with AI Services  
**Migration:** All functionality moved to pure AI workflows  
**Location:** See `.claude/workflows/` for AI-powered implementations  
**Interface:** Use .claude/docs/AI-ANALYSIS-SERVICE.md for pipeline analysis

## Framework Structure

```
scripts/
├── README.md                    # This file - Scripts documentation
├── extract-jenkins-data.sh      # Framework: Jenkins data extraction (future)
├── analyze-logs.sh              # Framework: Log analysis automation (future)
├── generate-reports.sh          # Framework: Report generation automation (future)
└── utils/                       # Framework: Utility scripts (future)
    ├── jenkins-api.sh           # Framework: Jenkins API helpers (future)
    ├── data-processing.sh       # Framework: Data processing utilities (future)
    └── notification.sh          # Framework: Notification utilities (future)
```

## Current Implementation Approach

### AI-Managed Data Extraction

**NEW APPROACH:** AI services manage curl-based data extraction intelligently:

```markdown
# AI handles all data extraction with intelligent error handling
"Analyze this Jenkins pipeline failure: https://jenkins-server/job/pipeline/123/"

# AI automatically executes:
# - curl -k -s "${JENKINS_URL}/api/json" → metadata.json
# - curl -k -s "${JENKINS_URL}/consoleText" → console.log
# - curl -k -s "${JENKINS_URL}/testReport/api/json" → test-results.json
# - Intelligent retry logic and error recovery
# - WebFetch fallback for certificate issues
```

### AI-Powered Complete Workflow

Replaced shell scripts with comprehensive AI services:
- **Data Extraction:** AI-managed curl with intelligent error handling
- **Analysis Processing:** AI failure classification and root cause analysis
- **Report Generation:** AI-created Executive + Detailed + Action Plan reports
- **Quality Assurance:** AI validation of completeness and accuracy
- **Workflow Orchestration:** End-to-end AI service management

## NEW Usage Pattern

### Pure AI Service Interface (Current)

```markdown
# Simple natural language interface - no shell commands needed
"Analyze this Jenkins pipeline failure: [JENKINS_URL]"

# AI automatically handles:
# ✅ Jenkins data extraction (curl + WebFetch fallback)
# ✅ Data processing and failure analysis
# ✅ Professional report generation (Executive + Detailed + Action Plan)
# ✅ Quality validation and organization in runs/ directory
# ✅ Error recovery and intelligent retry logic
```

### Migration Guide
```markdown
# OLD shell script approach (deprecated):
./quick-start.sh https://jenkins-url/

# NEW AI service approach (current):
"Analyze this Jenkins pipeline failure: https://jenkins-url/"
```

### Framework Integration Points

Future script development will focus on:

1. **Data Extraction Automation**
   - Automated Jenkins API polling
   - Batch artifact downloading
   - Historical data collection

2. **Integration Utilities**
   - CI/CD pipeline hooks
   - Notification systems
   - Dashboard data export

3. **Workflow Automation**
   - Scheduled analysis runs
   - Pattern detection alerts
   - Report distribution

## Development Guidelines

### When to Create Scripts

Scripts should be developed for:
- **Repetitive Data Collection**: Automated Jenkins polling and artifact extraction
- **Integration Points**: CI/CD hooks, notification systems, dashboard exports
- **Batch Operations**: Historical analysis, pattern detection across multiple builds
- **Deployment Automation**: Environment setup, configuration management

### What Claude Handles

Claude AI excels at:
- **Intelligent Analysis**: Pattern recognition, root cause identification
- **Content Generation**: Executive summaries, detailed technical reports
- **Contextual Understanding**: Complex log interpretation, multi-source correlation
- **Adaptive Processing**: Handling varied Jenkins configurations and log formats

## Framework Development

### Script Template Structure

```bash
#!/bin/bash
# Template for Z-Stream Analysis scripts

set -euo pipefail

# Source environment configuration
source "$(dirname "$0")/../.env"

# Claude integration point
# Scripts should prepare data for Claude analysis
# Claude handles the intelligent processing

# Example:
# 1. Extract Jenkins data via curl
# 2. Prepare structured input for Claude
# 3. Invoke Claude for analysis
# 4. Process Claude output for automation needs
```

### Integration with Claude

Scripts should:
1. **Prepare Data**: Extract and structure Jenkins data for Claude analysis
2. **Invoke Claude**: Pass structured data to Claude for intelligent processing
3. **Process Output**: Handle Claude-generated reports for automation needs
4. **Handle Integration**: Connect to external systems (notifications, dashboards)

## Example Workflow

```bash
# Current workflow (Claude-centric)
cd apps/z-stream-analysis
# Analyze: "Analyze this Jenkins pipeline: https://jenkins-url/job/pipeline/123/"
# Claude handles everything: data extraction, analysis, reporting

# Future workflow (script-enhanced)
./scripts/extract-jenkins-data.sh pipeline-123
# -> Prepares structured data
# -> Invokes Claude for analysis
# -> Generates reports
# -> Triggers notifications
```

## Best Practices

1. **Claude-First**: Use Claude for intelligent analysis, scripts for automation
2. **Curl-Based**: Prefer curl for Jenkins data extraction (reliable, secure)
3. **Structured Data**: Prepare clean, structured input for Claude analysis
4. **Error Handling**: Graceful degradation when Jenkins access is limited
5. **Modular Design**: Small, focused scripts that integrate well with Claude

---

**Framework Status:** Ready for development - Core analysis handled by Claude AI with curl-based Jenkins data extraction