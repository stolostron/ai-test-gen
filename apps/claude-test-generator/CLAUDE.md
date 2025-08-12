# Intelligent Test Analysis Engine

## 🎯 Framework Introduction

> **Quick Start Guide**: See `docs/quick-start.md`
> **Welcome Message**: See `.claude/greetings/framework-greetings.md`

**Latest Version**: 2.2 - Advanced AI Service Integration & Intelligent Quality Assurance  
**Framework Status**: Production-ready with AI-powered investigation, comprehensive quality assurance, and enterprise-grade test generation using intelligent service orchestration  
**Integration**: Part of AI Test Generation Suite with global `/generate-e2e-test-plan` commands

## 📖 Table of Contents
- [🚀 Quick Start](#quick-start)
- [🏢 System Architecture](#system-architecture)
- [🛠️ Available Tools & Scripts](#available-tools--scripts)
- [⚙️ Configuration Files](#configuration-files)
- [📋 Command Reference](#command-reference)
- [📋 Workflow Overview](#workflow-overview)
- [⚙️ Environment Setup](#environment-setup)
- [📁 Enhanced Output Structure](#enhanced-output-structure)
- [🎯 Core Principles](#core-principles)
- [🔧 Advanced Features](#advanced-features)

---

## 🚀 Quick Start

> **Complete Guide**: See `docs/quick-start.md`  
> **Unified Commands**: See [⚙️ Environment Setup](#environment-setup) for `/generate-e2e-test-plan` usage examples

**Most Common Usage:** Use unified commands from anywhere in the repository or navigate to framework for advanced features

**What You Get:** 5-10 minute analysis with 3-5 comprehensive E2E test scenarios with complete investigation protocol

**Environment:** Intelligent environment handling - default qe6 or custom kubeconfig with graceful degradation

---

## 🏢 System Architecture

This AI-powered analysis engine performs human-level reasoning about complex software systems, combining multiple AI techniques with deep learning from organizational patterns to deliver comprehensive test intelligence.

### 🌐 Enterprise Integration
- **Part of AI Test Generation Suite**: Unified command interface with global `/generate-e2e-test-plan` commands
- **Standalone Capability**: Fully independent operation with specialized Claude configuration
- **Cross-Application Routing**: Intelligent command routing to appropriate engines based on task type
- **Professional Grade**: Enterprise-ready with quality assurance and feedback loops

### 🧠 Advanced AI Intelligence Features
- **Always Deep Analysis**: Comprehensive AI-powered investigation is the default behavior - no shortcuts or surface-level analysis
- **AI Service Orchestration**: JIRA hierarchy + GitHub PR + Internet research + Implementation validation using Task tool and AI services
- **Intelligent Environment Handling**: Auto-detects QE environments or uses custom kubeconfig with graceful degradation
- **Smart Test Scoping**: AI-driven focus ONLY on NEW/CHANGED functionality for maximum efficiency
- **AI Quality Assurance**: Comprehensive validation replacing script-based approaches with intelligent analysis
- **Predictive Modeling**: AI-powered risk-based prioritization and architectural impact assessment
- **Continuous AI Learning**: Learning integration for iterative improvement with intelligent quality scoring

### 🎯 Smart Test Scoping Philosophy
The framework focuses ONLY on testing what actually changed in the implementation, avoiding redundant testing of existing stable functionality. This ensures efficient, targeted test coverage that maximizes value while minimizing execution time.

### 🔧 AI-Powered Quality Assurance Architecture
- **Complete AI Investigation Protocol**: Mandatory deep analysis across multiple data sources using AI services
- **Intelligent Feature Availability Analysis**: AI-powered version compatibility validation with root cause assessment
- **AI Quality Validation**: Post-generation AI assessment replacing script-based validation with intelligent analysis
- **Evidence-Based Assessment**: Implementation validation with deployment proof and supporting data via AI analysis
- **Professional Output Standards**: Enhanced test case format with copy-paste commands and expected outputs
- **Robust AI Test Generation**: Complete test plans generated regardless of current feature availability using AI orchestration

## 🛠️ Available Tools & Scripts

### Core AI & Analysis Tools
- **Claude Code AI**: Advanced reasoning and test generation with intelligent feedback loop
- **Jira CLI**: Comprehensive ticket analysis with hierarchy traversal
- **WebFetch**: GitHub PR details and internet research for complete investigation
- **TodoWrite**: Task tracking and progress management

### Environment & Cluster Tools
- **setup_clc** (`bin/setup_clc`): Intelligent environment setup for QE clusters (qe6-qe10) or custom kubeconfig validation
- **login_oc** (`bin/login_oc`): OpenShift authentication with cluster credentials
- **kubectl/oc**: Kubernetes/OpenShift CLI for cluster validation and testing

### Investigation & Research Tools
- **AI-Powered Investigation**: Advanced JIRA hierarchy analysis with comprehensive ticket traversal and comment analysis
- **GitHub PR Analysis**: Intelligent repository analysis with SSH access and comprehensive PR discovery  
- **cc_schema_helper** (`bin/cc_schema_helper.sh`): ClusterCurator-specific schema validation and field inspection
- **resource_schema_helper** (`bin/resource_schema_helper.sh`): Generic CRD schema helper for YAML skeleton generation

### Quality Assurance & Validation Tools
- **AI Quality Assurance**: Comprehensive validation replacing script-based approaches with intelligent analysis
- **Schema Validation**: Automated CRD compliance checking and YAML validation
- **inject_required_keys** (`bin/inject_required_keys.sh`): Automatic YAML field injection for required keys (non-destructive)
- **YAML Server Validation**: Optional `oc apply --dry-run=server` validation for schema compliance

## ⚙️ Configuration Files

This framework uses modular configuration files for enterprise-grade maintainability and professional standards:

### Core Configuration
- **CLAUDE.md**: Specialized Claude configuration with advanced features and investigation protocols
- **Test Case Format Requirements**: `.claude/templates/test-case-format-requirements.md` - Enhanced test case structure (Description + Setup + Steps + Expected Results)
- **Test Scoping Rules**: `.claude/prompts/test-scoping-rules.md` - Smart test scoping methodology focusing ONLY on changed functionality

### Templates & Standards
- **YAML Sample Templates**: `.claude/templates/yaml-samples.md` - YAML samples with required fields for expected results
- **Environment Configuration**: `.claude/templates/environment-config.md` - Environment setup and validation procedures
- **Bash Command Patterns**: `.claude/templates/bash-command-patterns.md` - Command chaining and execution patterns

### Quality & Workflow Systems
- **Feedback Loop System**: `.claude/workflows/feedback-loop-system.md` - Human review triggers and continuous improvement
- **Investigation Protocol**: Complete methodology for JIRA + GitHub + Internet research
- **Framework Greetings**: `.claude/greetings/framework-greetings.md` - Welcome message and quick start guide

## Command Reference

**Detailed Command Patterns**: See `.claude/templates/bash-command-patterns.md` for comprehensive examples of:
- Environment setup and validation with proper command chaining
- JIRA analysis workflows
- GitHub PR analysis patterns  
- Testing and validation commands
- Troubleshooting procedures

**Quality Assurance Tools**: See [🔧 Advanced Features](#advanced-features) section for:
- Post-generation linting and validation
- YAML server validation procedures
- Quality metrics and feedback loop systems
- Investigation protocol requirements

## Workflow Overview

The framework follows a structured 5-stage approach:

### Stage 1: Environment Setup & Validation
- **Flexible Environment Configuration**: Default qe6 or user-specified
- **Environment Validation**: Graceful handling of unavailable environments
- **Cluster Connectivity**: Verify access and permissions
- **Status Reporting**: Clear execution guidance

### Stage 2: AI-Powered Multi-Source Intelligence Gathering ⚠️ MANDATORY
- **Complete Investigation Protocol**: ALWAYS perform ALL steps below using AI services - NO EXCEPTIONS
- **AI-Powered JIRA Analysis**: Advanced ticket hierarchy analysis with comprehensive subtask traversal
- **Intelligent PR Discovery**: AI-driven GitHub repository analysis for implementation details
- **AI Internet Research**: Research relevant technology, documentation, and best practices using AI services
- **Repository Intelligence**: Code changes, architectural impact, and integration points via AI analysis
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
- **Mandatory Login Step**: ALL test cases MUST start with cluster login as Step 1
- **Clean Markdown**: No HTML tags (`<br>`, etc.), inline commands with backticks, no unnecessary line breaks in tables

### Stage 5: Analysis Report & Intelligent Feedback Loop
- **Dual File Output**: Complete-Analysis.md + Test-Cases.md
- **Enhanced Analysis Reports**: 
  - **Implementation Status** (first): What is implemented, PRs, key behavior, version targeting
  - **Environment & Validation Status** (second): Environment used, validation results, feature availability testing with supporting evidence
  - **Root Cause Assessment**: AI analysis determining if missing features are expected (version mismatch) or indicate potential bugs
  - **Concise Feature Summary**: Brief feature explanation + data collection summary (no detailed framework process explanations)
- **Intelligent Deployment Analysis**: Feature availability assessment with evidence-based reasoning
- **Comprehensive Status Reporting**: Current testing capability, missing feature diagnosis, future testing roadmap
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

### 🌐 Unified Command Interface

**Global Commands (from anywhere in repository):**
```bash
# Most common usage - JIRA-based test plan generation
/generate-e2e-test-plan ACM-22079

# With specific QE environment
/generate-e2e-test-plan ACM-22079 --env qe6

# With custom kubeconfig
/generate-e2e-test-plan ACM-22079 --kubeconfig /path/to/your/kubeconfig

# PR-based generation with JIRA context
/generate-e2e-test-plan https://github.com/repo/pull/203 "Feature Name" ACM-10659.txt
```

**Application-Specific Usage:**
```bash
# Navigate to framework for advanced features
cd apps/claude-test-generator
# Access specialized Claude config and investigation tools
```

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

## 📁 Enhanced Output Structure

```
runs/
├── <TICKET-ID>/                          # Main ticket folder (e.g., ACM-22079/)
│   ├── run-001-YYYYMMDD-HHMM/           # Timestamped execution
│   │   ├── Complete-Analysis.md          # 🔍 Comprehensive investigation and deployment assessment
│   │   ├── Test-Cases.md                # 🎯 Production-ready test cases (Description + Setup + Steps + Enhanced Expected Results)
│   │   └── metadata.json                # 📊 Run metadata, quality metrics, and feedback loop data
│   ├── run-002-YYYYMMDD-HHMM/           # Additional runs for iterative improvement
│   ├── archived-runs/                   # Historical runs for reference
│   └── latest -> run-XXX-YYYYMMDD-HHMM  # 🔗 Symlink to latest run
```

### Enhanced Content Quality

**Complete-Analysis.md Structure:**
- **Implementation Status** (first): Feature deployment, PRs analyzed, key behaviors discovered
- **Environment & Validation Status** (second): Cluster used, validation results, limitations encountered
- **Investigation Summary**: JIRA hierarchy, GitHub analysis, internet research findings
- **Deployment Assessment**: Feature availability with evidence and implementation proof

**Test-Cases.md Structure:**
- **Enhanced Test Case Format**: Description + Setup + Steps + Enhanced Expected Results
- **Copy-Paste Commands**: Terminal-ready CLI commands with realistic expected outputs
- **YAML Samples**: Sample data outputs and expected results for easy validation
- **Self-Contained Cases**: No external dependencies, complete standalone execution

**metadata.json Structure:**
- **Quality Metrics**: Test coverage score, investigation depth, business alignment rating
- **Feedback Loop Data**: Human review triggers, improvement suggestions, learning integration
- **Run Details**: Environment used, investigation sources, validation results
- **Continuous Improvement**: Quality trends, feedback history, optimization recommendations

## 🎯 Core Principles

### 🎯 Smart Test Scoping
- **Focus on Changes**: Test ONLY what was modified in the implementation
- **Skip Unchanged**: Avoid redundant testing of existing stable functionality
- **Efficient Coverage**: Maximize value while minimizing execution time

### 🌍 Environment Flexibility & Intelligence
- **Default Gracefully**: Use qe6 if no environment specified
- **Adapt to Availability**: Work with whatever environment is accessible
- **Version Intelligence**: AI-powered analysis of feature availability vs environment capability
- **Future Ready**: Generate complete test plans regardless of current limitations with intelligent deployment assessment

### 📋 Comprehensive & Intelligent Output
- **Dual File Generation**: Both complete analysis and clean test cases
- **Intelligent Status Reporting**: Root cause analysis for missing features - expected vs potential bugs
- **Evidence-Based Assessment**: Supporting data from actual environment validation
- **Organized Structure**: Timestamped runs with proper file organization

### 🔧 Enterprise Integration Features
- **AI Test Generation Suite Integration**: Part of unified command interface with global `/generate-e2e-test-plan` commands
- **ACM/CLC Domain Expertise**: Specialized knowledge for cluster lifecycle and management testing
- **Production-Ready Output**: Enhanced test case format with copy-paste commands and expected outputs
- **Universal Test Generation**: Works for any ACM story ticket with consistent enterprise-grade quality
- **Intelligent Feedback Loop**: Automated quality assessment, human review triggers, and continuous learning
- **Complete Investigation Protocol**: Mandatory deep analysis across JIRA + GitHub + Internet + Implementation validation
- **Intelligent Feature Availability Analysis**: AI-powered version compatibility validation with root cause assessment
- **Quality Assurance Pipeline**: Post-generation linting, YAML validation, and schema compliance
- **Robust Test Generation**: Complete test plans generated regardless of current feature availability
- **Professional Standards**: Clean outputs without framework self-references, optimized for team collaboration
- **Cross-Application Compatibility**: Seamless integration with Z-Stream Analysis Engine and other suite applications

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

**Step 1: AI-Powered JIRA Hierarchy Analysis** (100% coverage requirement):
1. **AI Service JIRA Investigation**: Use Task tool with general-purpose agent for comprehensive ticket analysis
2. **Ticket Network Discovery**: Main ticket + ALL nested linked tickets (up to 3 levels deep with recursion protection)
3. **Intelligent Comment Analysis**: AI-powered analysis across ALL discovered tickets for additional insights
4. **Cross-reference Validation**: AI-driven consistency checking across entire ticket network

**Step 2: AI-Driven PR Investigation** (MANDATORY):
1. **Task Tool PR Analysis**: Use AI services to find ALL related PRs through intelligent GitHub search
2. **Implementation Deep Dive**: AI analysis of implementation details and code changes
3. **Technical Decision Analysis**: AI-powered review of PR discussions and technical decisions
4. **Deployment Status Validation**: AI assessment of deployment status and integration points

**Step 3: AI Internet Research** (MANDATORY):
1. **WebFetch Intelligence**: Use AI services to research relevant technology and documentation
2. **Best Practices Discovery**: AI-powered understanding of best practices and common patterns
3. **Domain Knowledge Acquisition**: AI learning of domain-specific knowledge for accurate testing
4. **Assumption Validation**: AI validation of assumptions against authoritative sources

**Step 4: Implementation Reality Validation** (MANDATORY):
1. Deep schema inspection and field validation
2. Actual cluster testing of components and behaviors
3. Architecture discovery and operational pattern analysis
4. Feature availability assessment with proof

**Step 5: Intelligent Feature Availability Analysis** (MANDATORY):
1. **Version Intelligence Gathering**: Extract JIRA Fix Version and environment ACM version
2. **Environment Validation**: Perform actual feature testing during cluster validation
3. **Root Cause Analysis**: AI determines if missing features are expected (version mismatch) or indicate potential bugs
4. **Evidence Collection**: Document validation commands executed and their outputs
5. **Comprehensive Assessment**: Report deployment status with supporting data regardless of current availability

**Framework ALWAYS generates complete test plans - maximum value regardless of current feature availability**

**Step 6: Missing Data Handling** (MANDATORY):
1. Detect gaps and quantify impact
2. Document limitations and assumptions
3. Provide future roadmap for complete testing

### 🔍 AI-Powered Post-Generation Quality Assurance

**AI-Driven Validation & Quality Assessment:**

Replace script-based validation with comprehensive AI-powered quality assurance using Task tool and AI services for:

- **Test Case Format Compliance**: AI validation of Description + Setup + Steps + Expected Results format
- **Technical Accuracy Assessment**: AI review of ClusterCurator YAML schema compliance and command syntax
- **Content Quality Analysis**: AI assessment of copy-paste commands, expected outputs, and YAML samples
- **Implementation Readiness**: AI evaluation of test case execution readiness and self-containment

**AI Quality Checks Performed:**
- ✅ **Enhanced Format Validation**: AI-powered test case structure and content quality assessment  
- ✅ **Technical Accuracy**: AI validation of bash commands, YAML syntax, and expected outputs
- ✅ **Schema Compliance**: AI-driven validation of generated YAML against CRD schemas
- ✅ **Best Practices**: AI enforcement of ManagedClusterView usage and team usability standards
- ✅ **Command Syntax**: AI validation of bash commands for proper quoting and execution
- ✅ **Expected Results Quality**: AI assessment of sample YAML outputs and expected command results
- ✅ **Version Compatibility**: AI-powered analysis of feature availability vs environment capability
- ✅ **Root Cause Analysis**: AI diagnosis of missing features - expected vs potential bugs

**AI-Enhanced Features:**
- **Intelligent Quality Scoring**: Comprehensive quality metrics with 0-100 scoring system
- **Evidence-Based Assessment**: AI analysis with supporting data and deployment evidence
- **Continuous Learning**: Quality assessment feeds back into framework improvement
- **Professional Standards**: AI enforcement of enterprise-grade documentation and test case quality

### 📊 Quality Standards

**Always Generate Best Possible Test Plan**:
- Create comprehensive cases even with incomplete validation
- Use generic inspection commands when specific validation fails
- Provide multiple validation approaches for uncertain scenarios
- Ensure test plans work when limitations are resolved
- Apply automated quality assurance through post-generation linting
- Integrate feedback loop for continuous improvement