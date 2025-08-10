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
- **setup_clc**: Environment setup script (bin/setup_clc) - Configures kubeconfig for specified QE environments
- **login_oc**: OpenShift login script (bin/login_oc) - Handles authentication with cluster credentials

## Configuration Files
This framework uses modular configuration files for maintainability:

- **Test Scoping Rules**: `.claude/prompts/test-scoping-rules.md` - Smart test scoping methodology
- **YAML Sample Templates**: `.claude/templates/yaml-samples.md` - YAML samples for expected results
- **Environment Configuration**: `.claude/templates/environment-config.md` - Environment setup and validation
- **Bash Command Patterns**: `.claude/templates/bash-command-patterns.md` - Command chaining and execution patterns
- **Feedback Loop System**: `.claude/workflows/feedback-loop-system.md` - Human review and improvement integration
- **Framework Greetings**: `.claude/greetings/framework-greetings.md` - Welcome message and quick start guide

## Command Reference

**Detailed Command Patterns**: See `.claude/templates/bash-command-patterns.md` for comprehensive examples of:
- Environment setup and validation with proper command chaining
- JIRA analysis workflows
- GitHub PR analysis patterns  
- Testing and validation commands
- Troubleshooting procedures

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

The framework supports two environment setup options:

#### **Option 1: Automatic QE Setup** (Recommended)
- Uses qe6 environment (currently the only supported QE environment)
- Automatic credential fetching from Jenkins
- Framework calls `source setup_clc qe6` during environment setup

#### **Option 2: User-Provided Kubeconfig** (Maximum Flexibility)  
- Use any cluster with any authentication method
- Custom environments: production, staging, personal dev clusters
- User kubeconfig takes precedence over automatic setup

**Detailed Examples**: See `.claude/examples/environment-setup-examples.md`

### Framework Environment Setup Options

#### **Automatic Setup** (Uses Framework Scripts)
- **bin/setup_clc**: Automatically fetches latest credentials from Jenkins and configures kubeconfig
- **bin/login_oc**: Handles OpenShift authentication with various credential formats  
- **Supported Environment**: qe6 (default and currently only supported QE environment)
- **Auto-Detection**: Framework calls `source setup_clc qe6` during environment setup phase
- **Authentication Details**: See `.claude/templates/environment-config.md` for authentication persistence requirements

**⚠️ CRITICAL - Command Chaining for Environment Setup**:
- **Session Persistence Issue**: `setup_clc` modifies environment variables that don't persist across separate command executions
- **Required Approach**: Always chain commands with `&&` after setup to maintain session state
- **Correct Pattern**: `source setup_clc qe6 && oc whoami && oc get namespaces`
- **Avoid**: Running `setup_clc` separately from subsequent `oc` commands

**⚠️ IMPORTANT - Report Generation Guidelines**:
- **Framework Internal Use**: The framework uses `setup_clc` and `login_oc` scripts internally for robust authentication
- **Final Report Instructions**: All generated test cases MUST use generic `oc login` commands for broader team usability
- **Generic Format**: `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify`
- **Rationale**: Team members may not have access to framework scripts but can use standard oc login

#### **Manual Setup** (User-Provided Kubeconfig)
- **Flexibility**: Use any cluster with any authentication method
- **Custom Environments**: Production, staging, personal dev clusters
- **Authentication**: Token, certificate, or any oc login method
- **Override**: User kubeconfig takes precedence over automatic setup

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

## Missing Data Intelligence & Linked Ticket Investigation

### 🔍 Comprehensive Ticket Analysis Protocol

The framework performs **thorough investigation** of all related tickets:

#### **Multi-Level Ticket Investigation**
1. **Main Ticket Analysis**: Requirements, acceptance criteria, technical specifications
2. **All Subtasks Investigation**: Implementation status, PR links, completion state
3. **Dependency Chain Analysis**: Blocking/blocked tickets, prerequisites
4. **Epic Context Review**: Parent epics, strategic objectives, architectural decisions
5. **Related Ticket Mining**: Historical context, previous implementations, lessons learned
6. **Nested Link Traversal**: Following all linked tickets to full depth for complete context

#### **PR and Implementation Deep Dive**
- **Code Change Analysis**: Actual implementation details from attached PRs
- **Deployment Status Assessment**: Whether changes are live in test environments
- **Feature Availability Determination**: What can be tested now vs. future testing
- **Integration Point Identification**: How components connect and interact

#### **Missing Data Detection & Response**
When critical data is missing, the framework:
- **🚨 Identifies Gaps**: Missing PRs, inaccessible designs, undefined architectures
- **📊 Quantifies Impact**: What specific testing cannot be performed
- **✅ Scopes Available Work**: Focus on testable components
- **📋 Provides Future Roadmap**: Test cases ready for when missing data becomes available

**Detailed Examples**: See `.claude/workflows/missing-data-examples.md`

### 🎯 Investigation Quality Standards

- **100% Ticket Coverage**: Every linked ticket analyzed regardless of nesting level
- **PR Verification**: All attached PRs examined for implementation details
- **Cross-Reference Validation**: Ensuring consistency across related tickets
- **Context Preservation**: Understanding full feature history and evolution

## Framework Advantages

This framework delivers significant advancement in automated test generation:
- **AI-Powered Analysis**: Human-level reasoning about complex software systems
- **Smart Test Scoping**: Focus only on changed functionality for efficiency
- **Environment Adaptability**: Work with available resources, plan for ideal conditions
- **Comprehensive Investigation**: Deep analysis of all linked tickets and nested dependencies
- **Missing Data Intelligence**: Automatic detection and graceful handling of incomplete information
- **Modular Organization**: Maintainable configuration with specialized files
- **Team Collaboration**: Clean outputs usable by any team member

The modular design enables:
- **Easy Updates**: Modify specific functionality without touching core workflow
- **Team Collaboration**: Multiple experts can maintain different components
- **Reusable Templates**: Share YAML samples and scoping rules across projects
- **Flexible Configuration**: Adapt to different project types and requirements
- **Quality Investigation**: Standardized deep-dive analysis protocols