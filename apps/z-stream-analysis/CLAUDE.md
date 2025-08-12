# Claude Configuration - Z-Stream Analysis Engine

> **AI-powered Jenkins pipeline failure analysis with intelligent root cause identification**

## 🎯 Application Purpose

The Z-Stream Analysis Engine specializes in automated Jenkins pipeline failure analysis, providing AI-driven insights into CI/CD issues with intelligent classification, pattern recognition, and actionable remediation strategies.

**Primary Focus Areas:**
- Jenkins pipeline failure triage and root cause analysis
- Automated test failure pattern recognition  
- Infrastructure and environment issue diagnosis
- Historical trend analysis and recurring failure identification
- Executive reporting and technical deep-dive documentation

## 🚀 Unified Interface Commands

These commands work from the root repository and automatically route to this application:

### Primary Commands

```bash
# Quick pipeline analysis (from root)
/analyze-pipeline-failures {JENKINS_URL}
/analyze-pipeline-failures {PIPELINE_ID} [OPTIONS]

# Intelligent workflow routing (from root)
/analyze-workflow pipeline-failure {PIPELINE_ID}
/analyze-workflow ci-debug {JENKINS_URL}

# Direct application launch (from root)
/quick-start z-stream-analysis {PIPELINE_ID}
```

### Application-Specific Commands

When working directly in this application directory:

```bash
# Application structure ready for development
# Note: Core scripts are framework placeholders - use Claude to implement analysis

# Check application structure
ls -la
tree . -L 2

# View documentation
cat scripts/README.md
cat templates/README.md

# Manual analysis (Claude-powered)
# Use Claude to analyze Jenkins URLs directly in this context
```

### Real-World Examples

```bash
# From root repository - immediate analysis
/analyze-pipeline-failures https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc-clc-e2e-pipeline/3223/

# Pipeline ID shorthand
/analyze-pipeline-failures clc-e2e-pipeline-3223 --extract-artifacts

# Pattern analysis across builds
/analyze-pipeline-failures clc-e2e-pipeline-3223 --pattern-analysis

# Comprehensive workflow analysis
/analyze-workflow pipeline-failure clc-e2e-pipeline-3223 --comprehensive

# Direct application usage
cd apps/z-stream-analysis
./quick-start.sh https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc-clc-e2e-pipeline/3223/
```

## 🔧 Core Features

### Automated Failure Analysis
- **Pattern Recognition**: AI-powered failure pattern identification
- **Root Cause Analysis**: Deep dive into failure causation chains
- **Failure Classification**: Categorizes failures by type (infrastructure, test, environment)
- **Trend Analysis**: Identifies recurring failure patterns across builds

### Jenkins Integration
- **Artifact Extraction**: Automated download and analysis of build artifacts
- **Console Log Processing**: Intelligent parsing of Jenkins console outputs
- **Multi-Format Support**: Handles various Jenkins job types and formats
- **API Integration**: Direct Jenkins API access for comprehensive data gathering

### Intelligence & Reporting
- **Executive Summaries**: High-level failure analysis for stakeholders
- **Detailed Technical Reports**: In-depth analysis for engineers
- **Actionable Recommendations**: Specific steps to resolve identified issues
- **Historical Context**: Links current failures to past patterns

## 📁 Project Structure

```
z-stream-analysis/                          # ← You are here
├── .claude/                               # Claude workspace configuration
├── .env                                   # Environment configuration
├── CLAUDE.md                              # Claude configuration (this file)
├── scripts/                               # Analysis scripts framework
│   └── README.md                          # Scripts documentation
├── templates/                             # Report and validation templates
│   ├── README.md                          # Templates documentation  
│   ├── report-templates/                  # Analysis report templates (empty - ready for development)
│   └── validation-scripts/                # Validation scripts (empty - ready for development)
├── runs/                                  # Active analysis runs
│   ├── README.md                          # Runs documentation
│   ├── clc-e2e-pipeline-3223/            # Example: Real pipeline analysis results
│   │   ├── Executive-Summary.md           # High-level analysis
│   │   └── Detailed-Analysis.md           # Technical deep-dive
│   └── <PIPELINE-ID>/                     # Per-pipeline analysis results
├── archive/                               # Historical data and completed runs
│   ├── test-runs/                         # Previous analysis runs (extensive history)
│   └── pipeline-3223-analysis/            # Specific pipeline analysis
├── logs/                                  # Application logs
│   └── zstream_errors_20250812.log        # Current error tracking
└── examples/                              # Usage examples and demos (empty - ready for content)
```

## 🎯 Current Application State

**Status:** ✅ **Production Ready** - Active analysis engine with curl-first Jenkins integration  
**Last Updated:** 2025-08-12  
**Implementation Stage:** Production framework with real analysis examples  
**Active Data:** `runs/clc-e2e-pipeline-3223/` (real pipeline analysis results available)

**Current Capabilities:**
- Production-ready Jenkins pipeline failure analysis
- Curl-first data extraction for reliable Jenkins access
- AI-powered failure pattern recognition and root cause analysis
- Structured reporting (Executive Summary + Detailed Analysis)
- Real-time console log processing and artifact analysis
- Integration points for unified command interface
- Historical analysis data and examples for reference

**Development Approach:**
- Curl-based Jenkins data extraction as primary method
- Claude-powered analysis with structured output generation
- Standardized Executive + Detailed reporting format
- Real-time failure classification and actionable recommendations
- Extensible framework for custom analysis patterns

## 🛠️ Technical Capabilities

### AI-Powered Analysis
- **Claude-based Processing**: Advanced language model analysis of failure patterns
- **Contextual Understanding**: Comprehends complex technical logs and error messages
- **Multi-source Correlation**: Combines data from multiple sources for comprehensive analysis
- **Adaptive Learning**: Improves analysis quality based on historical data

### Data Processing
- **Curl-First Jenkins Integration**: Uses `curl -k -s` for secure, reliable Jenkins data extraction as primary method
- **Jenkins API Access**: Direct API calls for build metadata, status, and artifacts
- **Console Log Processing**: Streams Jenkins console output for real-time failure analysis
- **Log Parsing**: Intelligent extraction of relevant information from verbose logs
- **Artifact Analysis**: Automated processing of test results, screenshots, and reports
- **Metadata Extraction**: Systematic collection of build environment and configuration data

### Output Formats
- **Executive Summary**: High-level overview for management and stakeholders
- **Detailed Analysis**: Technical deep-dive for engineering teams
- **JSON Data**: Structured data for programmatic access and integration
- **Markdown Reports**: Human-readable documentation with actionable insights

## 🎯 Use Cases

### Primary Use Cases
1. **Pipeline Failure Triage**: Quickly identify and categorize build failures
2. **Root Cause Analysis**: Deep investigation into failure causation
3. **Pattern Recognition**: Identify recurring issues across multiple builds
4. **Team Efficiency**: Reduce time spent on manual failure analysis
5. **Quality Insights**: Understand test quality and infrastructure stability

### Team Integration
- **QE Teams**: Automated analysis of test pipeline failures
- **DevOps Teams**: Infrastructure and deployment failure analysis
- **Development Teams**: Understanding of code-related build failures
- **Management**: High-level insights into build quality and trends

## 🔧 Configuration & Setup

### Prerequisites
- **Claude Code CLI** configured and authenticated
- **Jenkins API Access** to target instances (optional - can analyze public URLs)
- **Python 3.8+** for advanced analysis scripts
- **Network Access** to Jenkins instances and artifact storage

### Environment Configuration

**Method 1: Environment Variables (Recommended)**
```bash
# Jenkins configuration (optional)
export JENKINS_URL="https://jenkins-csb-rhacm-tests.dno.corp.redhat.com"
export JENKINS_USER="your-username"
export JENKINS_TOKEN="your-api-token"

# Analysis configuration  
export ANALYSIS_OUTPUT_DIR="./runs"
export ARCHIVE_RETENTION_DAYS="90"
export DEBUG_MODE="false"
```

**Method 2: Application Defaults**
- Application works without Jenkins authentication for public URLs
- Interactive prompts for credentials when needed
- Auto-detection of pipeline IDs from URLs
- Graceful degradation when artifacts are inaccessible

### Quick Setup Verification

```bash
# Navigate to application
cd apps/z-stream-analysis

# Verify clean structure
ls -la
tree . -L 2

# Check existing analysis examples
cat runs/clc-e2e-pipeline-3223/Executive-Summary.md
cat runs/clc-e2e-pipeline-3223/Detailed-Analysis.md

# Review framework documentation
cat scripts/README.md
cat templates/README.md

# Check historical data
ls archive/test-runs/

# Verify environment configuration
cat .env
```

### Claude-Powered Analysis Workflow

The framework prioritizes curl-based Jenkins data extraction for reliable analysis:

```bash
# 1. Navigate to application context
cd apps/z-stream-analysis

# 2. Framework automatically uses curl for Jenkins data extraction:
# - curl -k -s "${JENKINS_URL}/api/json" for build metadata
# - curl -k -s "${JENKINS_URL}/consoleText" for console logs  
# - curl -k -s "${JENKINS_URL}/artifacts/" for artifact access

# 3. Use Claude to analyze Jenkins URLs
# Example: "Analyze this Jenkins pipeline failure: https://jenkins-url/job/pipeline/123/"

# 4. Claude creates structured analysis in runs/ directory
# 5. Results follow the established Executive + Detailed format
# 6. Historical context available in archive/ for reference
```

### Jenkins Data Extraction Methods

**Primary Method (Preferred):**
```bash
# Build metadata
curl -k -s "https://jenkins-server/job/pipeline/123/api/json"

# Console output (full)
curl -k -s "https://jenkins-server/job/pipeline/123/consoleText"

# Console output (tail for failures)
curl -k -s "https://jenkins-server/job/pipeline/123/consoleText" | tail -200

# Specific data extraction
curl -k -s "https://jenkins-server/job/pipeline/123/api/json" | jq '.result, .duration, .timestamp'
```

**Fallback Methods:**
- WebFetch tool for when curl encounters certificate issues
- Direct API access with authentication for private instances
- Local artifact processing for downloaded build data

## 📊 Analysis Workflow

### Standard Workflow
1. **Input Processing**: Parse Jenkins URL or pipeline ID
2. **Data Collection**: Extract build logs, artifacts, and metadata using curl-first approach
   - Primary: `curl -k -s` for Jenkins API and console data
   - Fallback: WebFetch tool for certificate-protected instances
   - Metadata: Extract build status, duration, timestamps, parameters
3. **AI Analysis**: Apply Claude-based analysis for pattern recognition
4. **Classification**: Categorize failures by type and severity
5. **Report Generation**: Create executive and detailed reports
6. **Action Items**: Generate specific remediation recommendations

### Output Structure

**Standard Analysis Output:**
```
runs/<PIPELINE-ID>/
├── Executive-Summary.md         # High-level analysis for stakeholders
├── Detailed-Analysis.md         # Technical deep-dive for engineers
├── pipeline_data.json          # Structured build data and metadata
├── failed_tests.json           # Test failure details and classifications
├── intelligent_analysis.json   # AI analysis results and insights
├── artifacts/                  # Downloaded Jenkins artifacts (when available)
│   ├── console.log             # Build console output
│   ├── test-results/           # Test result files
│   └── screenshots/            # Failure screenshots
├── metadata.json               # Analysis run metadata
└── latest -> run-001-YYYYMMDD-HHMM  # Symlink to latest run
```

**Available Examples:**
- `runs/clc-e2e-pipeline-3223/` - Real pipeline analysis results
- See actual analysis output structure in existing runs

## 🔍 Analysis Types

### Failure Classification
- **Infrastructure Failures**: Environment, network, resource issues
- **Test Failures**: Application logic, test code, data issues
- **Build Failures**: Compilation, dependency, configuration issues
- **Timeout Failures**: Performance, resource contention issues

### Pattern Analysis
- **Recurring Failures**: Issues appearing across multiple builds
- **Environmental Patterns**: Failures specific to environments or configurations
- **Temporal Patterns**: Time-based failure trends
- **Dependency Patterns**: Failures related to external dependencies

## 🚨 Error Handling & Diagnostics

### Robust Processing
- **Partial Failure Handling**: Continue analysis even when some data is unavailable
- **Rate Limiting**: Respect Jenkins API limits and retry policies
- **Error Recovery**: Graceful handling of network issues and malformed data
- **Validation**: Comprehensive input validation and error reporting

### Diagnostic Features
- **Health Checks**: Validate Jenkins connectivity and permissions
- **Debug Mode**: Verbose logging for troubleshooting analysis issues
- **Artifact Validation**: Verify downloaded artifacts and data integrity
- **Performance Monitoring**: Track analysis execution time and resource usage

## 🔄 Integration Patterns

### CI/CD Integration
```bash
# Post-build analysis (Jenkins pipeline)
post {
    failure {
        sh './analyze-pipeline-failures.sh ${BUILD_URL}'
    }
}

# Scheduled analysis (cron)
0 8 * * * /path/to/z-stream-analysis/quick-start.sh --pattern-analysis
```

### Notification Integration
- **Slack Integration**: Automated failure notifications with analysis summaries
- **Email Reports**: Scheduled executive summaries for stakeholders
- **JIRA Integration**: Automatic ticket creation for critical failures
- **Dashboard Integration**: Export data for monitoring dashboards

## 🎯 Best Practices & Usage Patterns

### Efficient Analysis Workflows

**For QE Teams:**
```bash
# Daily failure triage
/analyze-pipeline-failures pipeline-XXXX --quick-summary

# Deep investigation  
cd apps/z-stream-analysis
./quick-start.sh <jenkins-url> --comprehensive
```

**For DevOps Teams:**
```bash
# Infrastructure failure analysis
/analyze-workflow ci-debug <jenkins-url> --focus-infrastructure

# Pattern analysis across environments
/analyze-pipeline-failures pipeline-XXXX --pattern-analysis --env-comparison
```

**For Management:**
```bash
# Executive reporting
/analyze-pipeline-failures pipeline-XXXX --executive-summary
# Generates stakeholder-ready reports in runs/pipeline-XXXX/Executive-Summary.md
```

### Team Collaboration
- **Standardized Reports**: All analysis follows consistent Executive + Detailed format
- **Historical Context**: Each analysis links to previous similar failures
- **Actionable Insights**: Reports include specific remediation steps
- **Knowledge Base**: Failed patterns are automatically captured and referenced

### Integration with Unified Commands

**Root Repository Usage (Recommended):**
- Use `/analyze-pipeline-failures` for immediate analysis
- Use `/analyze-workflow pipeline-failure` for intelligent routing
- All results stored in `apps/z-stream-analysis/runs/`

**Direct Application Usage (Advanced):**
- `cd apps/z-stream-analysis` for specialized features
- Access to advanced scripts and templates
- Custom analysis configurations and debugging

---

**🏢 Enterprise Platform:** The Z-Stream Analysis Engine integrates seamlessly with the unified AI test generation suite, providing specialized Jenkins pipeline failure analysis with Claude-powered insights and automated remediation guidance.