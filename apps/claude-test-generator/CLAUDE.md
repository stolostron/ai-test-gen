# Intelligent Test Analysis Engine

## 🎯 Framework Introduction

> **Quick Start & Welcome Message**: See `.claude/greetings/framework-greetings.md`

---

## System Architecture

This AI-powered analysis engine performs human-level reasoning about complex software systems, combining multiple AI techniques with deep learning from organizational patterns to deliver comprehensive test intelligence.

**Core Intelligence Features**: Multi-source analysis, adaptive learning, predictive modeling, risk assessment, smart test scoping, and continuous optimization.

**🎯 Smart Test Scoping Philosophy**: The framework focuses ONLY on testing what actually changed in the implementation, avoiding redundant testing of existing stable functionality. This ensures efficient, targeted test coverage that maximizes value while minimizing execution time.

## Available Tools
- **Jira CLI**: Installed and configured for ticket analysis
- **WebFetch**: For accessing GitHub PR details and analysis
- **kubectl/oc**: Kubernetes/OpenShift CLI for cluster validation
- **TodoWrite**: Task tracking and progress management

## Configuration Files
This framework uses modular configuration files for maintainability:

- **Test Scoping Rules**: `.claude/prompts/test-scoping-rules.md` - Smart test scoping methodology
- **YAML Sample Templates**: `.claude/templates/yaml-samples.md` - YAML samples for expected results
- **Environment Configuration**: `.claude/templates/environment-config.md` - Environment setup and validation
- **Feedback Loop System**: `.claude/workflows/feedback-loop-system.md` - Human review and improvement integration
- **Framework Greetings**: `.claude/greetings/framework-greetings.md` - Welcome message and quick start guide

## Common Commands

### JIRA Analysis
```bash
# View ticket details with description and comments
jira issue view <TICKET-ID> --plain

# Get ticket with comments
jira issue view <TICKET-ID> --comments

# List subtasks and linked issues
jira issue view <TICKET-ID> # Shows linked tickets in output
```

### GitHub PR Analysis
```bash
# Use WebFetch tool with GitHub URLs for PR analysis
# Format: https://github.com/<owner>/<repo>/pull/<number>
```

## Workflow Overview

The framework follows a structured 5-stage approach:

### Stage 1: Environment Setup & Validation
- **Flexible Environment Configuration**: Default qe6 or user-specified
- **Environment Validation**: Graceful handling of unavailable environments
- **Cluster Connectivity**: Verify access and permissions
- **Status Reporting**: Clear execution guidance

### Stage 2: Multi-Source Intelligence Gathering
- **Smart Test Scope Analysis**: Focus ONLY on changed functionality
- **JIRA Intelligence**: Comprehensive ticket and relationship analysis
- **Repository Analysis**: Code changes and architectural impact
- **Test Scope Optimization**: Skip unchanged functionality

### Stage 3: AI Reasoning and Strategic Test Intelligence
- **Semantic Feature Analysis**: Understand feature intent and requirements
- **Architectural Reasoning**: Assess system design impact
- **Business Impact Modeling**: Quantify customer and revenue impact
- **Risk-Based Prioritization**: Focus on high-value, high-risk scenarios

### Stage 4: Test Strategy Generation & Quality Optimization
- **E2E Test Coverage**: Complete end-to-end workflows covering all NEW functionality
- **Structured Test Cases**: Description, Setup, and clear Steps/Expected Result tables
- **Actual Expected Results**: Show real terminal output, not validation commands
- **Simple Execution**: Keep steps straightforward and easy to follow
- **Multiple Focused Tables**: OK to create multiple tables for clarity
- **Terminal-Ready Commands**: Copy-pasteable commands with clear expected outputs

### Stage 5: Analysis Report & Intelligent Feedback Loop
- **Organized Output Generation**: Timestamped runs with proper structure
- **Deployment Status Analysis**: Feature availability assessment
- **Future Readiness**: Test plans ready when feature is deployed
- **Clear Status Reporting**: What can be tested now vs. post-deployment
- **🔄 Intelligent Feedback Loop**: Automated quality assessment and human review integration
- **📊 Run Comparison Analysis**: Quality progression tracking and improvement identification
- **👥 Human Review Triggers**: Automated requests for human feedback within current execution cycle only
- **🎯 Continuous Improvement**: Learning integration from human feedback into subsequent generations

## Framework Execution

### Basic Usage
```bash
# Navigate to framework
cd apps/claude-test-generator

# Analyze any ACM JIRA ticket
analyze_ticket ACM-22079

# With custom environment
USER_ENVIRONMENT=qe7 analyze_ticket ACM-22079
```

### What Happens
1. Framework connects to specified environment (default: qe6)
2. Analyzes JIRA ticket for business and technical requirements
3. Generates comprehensive E2E test plan focused on NEW functionality
4. Creates both detailed analysis and clean test cases
5. Provides deployment assessment (feature available or not)

### Expected Output
- **Execution Time**: 5-10 minutes
- **Test Cases**: 3-5 comprehensive E2E scenarios
- **Coverage**: All NEW functionality with realistic validation steps
- **Format**: Ready for manual execution or Polarion import

## Output Structure

```
runs/
├── <TICKET-ID>/                     # Main ticket folder (e.g., ACM-22079/)
│   ├── run-001-YYYYMMDD-HHMM/      # First run with timestamp
│   │   ├── Complete-Analysis.md     # Comprehensive analysis
│   │   ├── Test-Cases.md           # Clean test cases only
│   │   └── metadata.json           # Run metadata and settings
│   ├── run-002-YYYYMMDD-HHMM/      # Additional runs
│   └── latest -> run-XXX-YYYYMMDD-HHMM  # Symlink to latest run
```

## Core Principles

### 🎯 Smart Test Scoping
- **Focus on Changes**: Test ONLY what was modified in the implementation
- **Skip Unchanged**: Avoid redundant testing of existing stable functionality
- **Efficient Coverage**: Maximize value while minimizing execution time

### 🌍 Environment Flexibility
- **Default Gracefully**: Use qe6 if no environment specified
- **Adapt to Availability**: Work with whatever environment is accessible
- **Future Ready**: Generate complete test plans regardless of current limitations

### 📋 Comprehensive Output
- **Dual File Generation**: Both complete analysis and clean test cases
- **Clear Status Reporting**: What can be tested now vs. later
- **Organized Structure**: Timestamped runs with proper file organization

### 🔧 Integration Features
- **ACM/CLC Specific**: Domain expertise for cluster lifecycle testing
- **E2E Test Coverage**: Complete end-to-end workflows for all NEW functionality
- **Structured Test Format**: Description, Setup, Steps/Expected Result format
- **Clear Expected Outputs**: Show actual terminal output, not validation commands
- **Feedback Loop System**: Automated human review triggers with quality assessment
- **Task-Focused Reports**: Clean outputs without framework self-references

## Latest Enhancements

### Recent Improvements
- **Fixed Feedback Loop Logic**: Now properly tracks current execution cycle (not historical runs)
- **Task-Focused Reports**: Removed framework references, reports focus purely on testing tasks
- **Generic Login Instructions**: Reports use placeholder format for broader team usability
- **Early Environment Assessment**: Clear feature availability status in report headers
- **Enhanced Test Case Structure**: Consistent Description, Setup, and table formats

### Quality Features
- **Environment Assessment**: Early determination of feature deployment status
- **Realistic Expected Outputs**: Show actual terminal output, not commands
- **Copy-Pasteable Commands**: Generic format that works across different environments
- **Human Review Integration**: Smart feedback loop system with quality tracking
- **Continuous Improvement**: Learning from feedback to enhance future generations

## Framework Advantages

This framework delivers significant advancement in automated test generation:
- **AI-Powered Analysis**: Human-level reasoning about complex software systems
- **Smart Test Scoping**: Focus only on changed functionality for efficiency
- **Environment Adaptability**: Work with available resources, plan for ideal conditions
- **Modular Organization**: Maintainable configuration with specialized files
- **Team Collaboration**: Clean outputs usable by any team member

The modular design enables:
- **Easy Updates**: Modify specific functionality without touching core workflow
- **Team Collaboration**: Multiple experts can maintain different components
- **Reusable Templates**: Share YAML samples and scoping rules across projects
- **Flexible Configuration**: Adapt to different project types and requirements