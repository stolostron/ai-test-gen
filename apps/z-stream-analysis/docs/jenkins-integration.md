# Jenkins Integration Guide

This document provides comprehensive technical details for Jenkins integration with the Z-Stream Analysis Engine.

## Data Extraction Methods

### Primary Method - Intelligent Parameter Extraction

The AI Environment Validation Service automatically discovers test environment details from Jenkins run parameters:

```bash
# AI automatically extracts from Jenkins parameters endpoint:
# https://jenkins-server/job/pipeline/123/parameters/
# 
# Extracted parameters include:
# - CLUSTER_URL, OCP_CLUSTER, K8S_SERVER (target test cluster)
# - KUBECONFIG, CLUSTER_KUBECONFIG (authentication credentials)
# - NAMESPACE, TARGET_NAMESPACE (test namespace)
# - ENVIRONMENT, TEST_ENV (environment context)
# - CREDENTIALS, AUTH_TOKEN (access credentials)
```

### Jenkins API Commands

**Primary Method - Intelligent Parameter Extraction:**
```bash
# Test environment parameters (actual test environment used)
curl -k -s "https://jenkins-server/job/pipeline/123/parameters/"

# Build metadata
curl -k -s "https://jenkins-server/job/pipeline/123/api/json"

# Console output (full)
curl -k -s "https://jenkins-server/job/pipeline/123/consoleText"

# Console output (tail for failures)
curl -k -s "https://jenkins-server/job/pipeline/123/consoleText" | tail -200

# Specific data extraction with environment context
curl -k -s "https://jenkins-server/job/pipeline/123/api/json" | jq '.result, .duration, .timestamp'
curl -k -s "https://jenkins-server/job/pipeline/123/parameters/" | jq '.parameter[] | {name, value}'
```

### Real-World Examples

```bash
# Extract environment from UI test pipeline
curl -k -s "https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/CI-Jobs/job/e2e_ui_test_pipeline/520/parameters/"

# Extract environment from CLC E2E pipeline  
curl -k -s "https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc/job/clc-e2e-pipeline/3223/parameters/"
```

**Fallback Methods:**
- WebFetch tool for when curl encounters certificate issues
- Direct API access with authentication for private instances
- Local artifact processing for downloaded build data

## Environment Discovery Process

**Intelligent Discovery Process**
- **Primary**: Extract test environment from Jenkins build parameters via AI parameter analysis
- **Secondary**: Parse environment details from console logs using AI pattern recognition
- **Tertiary**: Use Jenkins artifacts for kubeconfig/credentials via AI artifact analysis
- **Fallback**: Interactive prompts for missing critical information with intelligent guidance

## CI/CD Integration Examples

### Jenkins Pipeline Integration
```bash
# Post-build analysis (Jenkins pipeline) - AI-powered with full services
post {
    failure {
        // Use comprehensive AI services with natural language interface
        sh 'cd /path/to/z-stream-analysis && echo "Execute comprehensive AI analysis for Jenkins pipeline failure: ${BUILD_URL}" | claude-code'
    }
}

# Scheduled analysis (cron) - AI-powered with pattern analysis
0 8 * * * cd /path/to/z-stream-analysis && echo "Perform comprehensive pattern analysis with environment validation for recent pipeline failures" | claude-code
```

### AI Services Integration Commands
```bash
# Comprehensive AI-powered analysis with all services
"Analyze this Jenkins pipeline failure with complete investigation: ${BUILD_URL}"

# Environment validation focused analysis
"Validate product functionality for this Jenkins failure: ${BUILD_URL}"

# Repository analysis and fix generation
"Generate precise automation fixes based on real repository analysis for this automation failure: ${BUILD_URL}"

# Cross-service evidence correlation
"Provide definitive verdict with environment and repository validation: ${BUILD_URL}"
```

## Default Comprehensive Analysis

**CRITICAL:** When provided with ANY Jenkins URL, Claude automatically performs complete Enterprise AI Services analysis:

```bash
# 1. Simply provide Jenkins URL - NO configuration needed:
"https://jenkins-server/job/pipeline/123/"

# 2. Claude AUTOMATICALLY executes full V4.0 workflow:
# - Extract Jenkins metadata: curl -k -s "${JENKINS_URL}/api/json"
# - Extract console logs: curl -k -s "${JENKINS_URL}/consoleText" 
# - Extract parameters: curl -k -s "${JENKINS_URL}/parameters/"
# - AI Branch Validation: Parse console for git checkout commands
# - Repository Cloning: git clone -b {correct_branch} {repository_url}
# - Real Code Analysis: Examine actual failing test files and implementations
# - Environment Validation: Test cluster connectivity if credentials available
# - Cross-Service Evidence: Correlate all findings for definitive verdict
# - Fix Generation: Create precise automation solutions with exact code changes
# - Report Generation: Save comprehensive analysis to runs/{pipeline-id}_{timestamp}_v31/
# - Cleanup: Remove temporary repositories while preserving analysis results

# 3. NO additional commands or configuration required
# 4. Results automatically saved to runs/ directory with timestamped format
# 5. Complete Enterprise AI Services integration executed by default
```

**Examples of Default Comprehensive Analysis:**
```bash
# All of these trigger FULL analysis automatically:
"Analyze https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc/job/clc-e2e-pipeline/3313/"
"https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc/job/clc-e2e-pipeline/3313/"
"clc-e2e-pipeline-3313"  # Pipeline ID also triggers full analysis
```

## Real-World Pipeline Examples

- **UI Test Pipeline**: `https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/CI-Jobs/job/e2e_ui_test_pipeline/520/parameters/`
- **CLC E2E Pipeline**: `https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc/job/clc-e2e-pipeline/3223/parameters/`