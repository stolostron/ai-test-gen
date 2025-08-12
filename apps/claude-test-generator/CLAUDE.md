# Intelligent Test Analysis Engine

## 🎯 Framework Introduction

> **Quick Start Guide**: See `docs/quick-start.md`
> **Welcome Message**: See `.claude/greetings/framework-greetings.md`

**Latest Version**: Enhanced format with Description + Setup + YAML outputs in Expected Results
**Framework Status**: Production-ready with complete investigation protocol and intelligent feedback loop

## 📖 Table of Contents
- [🚀 Quick Start](#quick-start)
- [🏗️ System Architecture](#system-architecture) 
- [🛠️ Available Tools](#available-tools)
- [⚙️ Environment Setup](#environment-setup)
- [📋 Workflow Overview](#workflow-overview)
- [🎯 Core Principles](#core-principles)
- [📁 Output Structure](#output-structure)
- [🔧 Advanced Features](#advanced-features)

---

## 🚀 Quick Start

> **Complete Guide**: See `docs/quick-start.md`

**Most Common Usage:** Navigate to framework and ask Claude to analyze any JIRA ticket

**What You Get:** 5-10 minute analysis with 3-5 comprehensive E2E test scenarios

**Environment:** Default qe6 or use your own cluster

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
- **resource_schema_helper**: Generic schema helper (bin/resource_schema_helper.sh) - Emits minimal YAML skeletons for any CRD-backed resource
- **github-investigation**: Enhanced GitHub repository access script (bin/github-investigation.sh) - Deep repository analysis with SSH access
- **doc-investigation**: JIRA documentation extraction script (bin/doc-investigation.sh) - Recursive ticket traversal and comments analysis

## Configuration Files
This framework uses modular configuration files for maintainability:

- **Test Case Format Requirements**: `.claude/templates/test-case-format-requirements.md` - Complete test case structure and format standards
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

### Stage 2: Multi-Source Intelligence Gathering ⚠️ MANDATORY
- **Complete Investigation Protocol**: ALWAYS perform ALL steps below - NO EXCEPTIONS
- **PR Discovery & Analysis**: Find and analyze ALL related PRs for implementation details
- **Internet Research**: Research relevant technology, documentation, and best practices
- **JIRA Intelligence**: Comprehensive ticket + ALL subtasks + dependency chains + epic context
- **Repository Analysis**: Code changes, architectural impact, and integration points
- **Implementation Reality Validation**: Deep schema validation and actual field inspection
- **Smart Test Scope Analysis**: Focus ONLY on changed functionality after complete understanding

### Stage 3: AI Reasoning and Strategic Test Intelligence
- **Semantic Feature Analysis**: Understand feature intent and requirements
- **Architectural Reasoning**: Assess system design impact
- **Business Impact Modeling**: Quantify customer and revenue impact
- **Risk-Based Prioritization**: Focus on high-value, high-risk scenarios

### Stage 4: Test Strategy Generation & Quality Optimization
- **E2E Test Coverage**: Complete end-to-end workflows covering all NEW functionality
- **Required Test Case Structure** ⚠️ MANDATORY: 
  - **Description**: Clear explanation of what the test case does/tests exactly
  - **Setup**: Required setup/prerequisites needed for the test case  
  - **Test Steps Table**: Step-by-step execution with enhanced format requirements
- **Test Step Format Requirements** ⚠️ MANDATORY:
  All test steps MUST include:
  1. **Verbal instruction** describing what to do
  2. **CLI command** (when applicable) 
  3. **UI guidance** (when applicable)
- **Expected Result Format Requirements** ⚠️ MANDATORY:
  Expected Results MUST contain:
  1. **Verbal explanation** of what should happen
  2. **Sample YAML/data outputs** when relevant and helpful
  3. **Expected command outputs** when commands/grep are used (so testers can easily see and match probable outputs)
  4. **Specific values** or output descriptions
- **Standalone Test Cases**: Each test case must be completely self-contained with no setup dependencies
- **Simple Execution**: Keep steps straightforward and easy to follow
- **Multiple Focused Tables**: OK to create multiple tables for clarity
- **Terminal-Ready Commands**: Copy-pasteable commands with clear expected outputs
- **Generic oc login**: MUST use generic format for broader team usability
 - **Schema-Aware YAML**: ClusterCurator examples include required fields (`towerAuthSecret`, `prehook`, `posthook`, `install`)
 - **ManagedClusterView Usage**: When reading managed cluster resources (e.g., `ClusterVersion`), use `ManagedClusterView` from the hub

### Stage 5: Analysis Report & Intelligent Feedback Loop
- **Dual File Output**: Complete-Analysis.md + Test-Cases.md
- **Streamlined Analysis Reports**: 
  - **Environment & Validation Status Section** ⚠️ MANDATORY at report beginning:
    - **Environment Used**: Full environment details (cluster URL, versions, namespaces)
    - **Validation Status**: Clear success/failure with evidence
    - **Potential Failure Causes**: Document possible issues (test build delays, feature flags, CRD mismatches, connectivity)
  - **Concise Feature Summary**: Brief feature explanation + data collection summary (no detailed framework process explanations)
  - **Implementation Status**: Feature deployment status with environment context
- **Deployment Status Analysis**: Feature availability assessment  
- **Clear Status Reporting**: What can be tested now vs. post-deployment
- **Intelligent Feedback Loop System**:
  - **Quality Assessment**: Test coverage, business alignment, technical depth scoring
  - **Human Review Triggers**: After 3 runs, quality plateau, low scores, or production requests
  - **Structured Feedback Collection**: Quality ratings, improvement suggestions, missing requirements
  - **Learning Integration**: Updates generation parameters based on feedback for continuous improvement
- **Task-Focused Reports**: Clean outputs without framework self-references

## ⚙️ Environment Setup

> **Complete Details**: See `.claude/advanced/environment-setup-details.md`

### Environment Options
- **Option 1 (Recommended)**: Automatic qe6 setup with Jenkins credentials
- **Option 2**: User-provided kubeconfig (any cluster, any auth method)

### ⚠️ CRITICAL Instructions

**Command Chaining**: Always chain commands after setup to maintain session state
```bash
# Correct: source setup_clc qe6 && oc whoami && oc get namespaces
# Avoid: Running setup_clc separately from oc commands
```

**Report Generation**: Generated test cases MUST use generic `oc login` commands for team usability
```bash
# Format: oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify
```

### Framework Process
1. Connect to environment (default: qe6)
2. **COMPLETE INVESTIGATION PROTOCOL**: JIRA + PRs + Internet Research - REQUIRED
3. **Deep Implementation Validation**: Schemas, architecture, actual testing
4. **Professional Test Case Generation**: Description + Setup + Enhanced Expected Results format
5. **Streamlined Analysis Reports**: Concise feature summaries with environment specification
6. **Intelligent Feedback Loop Execution**: Quality assessment and iterative improvement
7. Create dual output with full investigation transparency
8. Provide deployment assessment with investigation evidence

### Expected Output
- **Time**: 5-10 minutes | **Cases**: 3-5 E2E scenarios | **Format**: Production-ready with enhanced structure
- **Test Case Format**: Description + Setup + Steps with verbal instructions + Enhanced Expected Results
- **Expected Results Include**: Verbal explanations + Sample YAML/data outputs + Expected command outputs
- **Analysis Reports**: Environment & validation status upfront + Concise feature summaries with investigation transparency
- **Quality Assurance**: Intelligent feedback loop for continuous improvement and human oversight

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
- **Professional Test Format**: Description + Setup + Enhanced Expected Results with sample YAML/data outputs
- **Universal Test Generation**: Works for any ACM story ticket with consistent quality standards
- **Intelligent Feedback Loop**: Automated quality assessment, human review triggers, and continuous improvement
- **Complete Investigation Protocol**: JIRA hierarchy + GitHub analysis + Internet research + Implementation validation
- **Task-Focused Reports**: Clean outputs without framework self-references

## 🔧 Advanced Features

> **Implementation Validation**: See `.claude/advanced/implementation-validation.md`
> **Investigation Protocol**: See `.claude/workflows/investigation-protocol.md`  
> **Framework Advantages**: See `.claude/advanced/framework-advantages.md`

### 🔍 Critical Validation Requirements ⚠️ MANDATORY

**BEFORE generating test cases**, the framework MUST ALWAYS:
1. **Complete PR Analysis**: Find and analyze ALL implementation PRs - NO EXCEPTIONS
2. **Conduct Internet Research**: Research technology, docs, and best practices - REQUIRED
3. **Perform Deep Schema Validation**: Inspect actual field structures and behaviors
4. **Discover Component Architecture**: Understand operational patterns through investigation
5. **Assess Implementation Reality**: Validate actual deployment and feature availability
6. **Execute Feedback Loop**: Quality assessment and iterative improvement
7. **Document Investigation Results**: Full transparency of research and validation process

**FAILURE TO COMPLETE INVESTIGATION = INVALID TEST GENERATION**

### 🎯 Investigation Protocol ⚠️ MANDATORY

**ALWAYS EXECUTE COMPLETE INVESTIGATION - NO SHORTCUTS ALLOWED**

**Step 1: Complete JIRA Hierarchy Deep Dive** (100% coverage requirement):
1. **Main ticket + ALL nested linked tickets** (up to 3 levels deep with recursion protection)
2. **ALL subtasks + dependency chains + epic context + related tickets**
3. **Comments analysis across ALL discovered tickets** for additional insights and links
4. **Cross-reference validation + consistency checking across entire ticket network**

**Step 2: PR Investigation** (MANDATORY):
1. Find ALL related PRs through GitHub search
2. Analyze implementation details and code changes
3. Review PR discussions and technical decisions
4. Validate deployment status and integration points

**Step 3: Internet Research** (MANDATORY):
1. Research relevant technology and documentation
2. Understand best practices and common patterns
3. Learn domain-specific knowledge for accurate testing
4. Validate assumptions against authoritative sources

**Step 4: Implementation Reality Validation** (MANDATORY):
1. Deep schema inspection and field validation
2. Actual cluster testing of components and behaviors
3. Architecture discovery and operational pattern analysis
4. Feature availability assessment with proof

**Step 5: Missing Data Handling** (MANDATORY):
1. Detect gaps and quantify impact
2. Document limitations and assumptions
3. Provide future roadmap for complete testing

### 📊 Quality Standards

**Always Generate Best Possible Test Plan**:
- Create comprehensive cases even with incomplete validation
- Use generic inspection commands when specific validation fails
- Provide multiple validation approaches for uncertain scenarios
- Ensure test plans work when limitations are resolved