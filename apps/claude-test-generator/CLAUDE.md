# Intelligent Test Analysis Engine

## 🎯 Framework Introduction

> **Quick Start Guide**: See `docs/quick-start.md`
> **Welcome Message**: See `.claude/greetings/framework-greetings.md`

**Latest Version**: Enhanced format with Description + Setup + YAML outputs in Expected Results + Evidence-based deployment validation
**Framework Status**: Production-ready with complete investigation protocol, intelligent feedback loop, and robust deployment status validation

## 📖 Table of Contents
- [🚀 Quick Start](#quick-start)
- [🏗️ System Architecture](#system-architecture) 
- [🛠️ Available Tools](#available-tools)
- [🔒 Framework Self-Containment Policy](#framework-self-containment-policy)
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
- **AI Analysis Engine**: Core AI-powered analysis service for intelligent test generation and validation
- **Jira CLI**: Installed and configured for ticket analysis
- **WebFetch**: For accessing GitHub PR details and analysis
- **kubectl/oc**: Kubernetes/OpenShift CLI for cluster validation
- **TodoWrite**: Task tracking and progress management
- **setup_clc**: Environment setup script (bin/setup_clc) - Configures kubeconfig for specified QE environments
- **login_oc**: OpenShift login script (bin/login_oc) - Handles authentication with cluster credentials
- **AI Schema Service**: Intelligent schema analysis - Provides dynamic YAML skeletons for any CRD-backed resource
- **AI Validation Service**: Intelligent output validation - Flags escaped pipes, enforces ManagedClusterView guidance, performs YAML validation
- **AI GitHub Investigation Service**: Intelligent GitHub repository analysis - Deep repository analysis with robust access patterns
- **AI Documentation Service**: Intelligent JIRA documentation extraction - Recursive ticket traversal and comments analysis

## 🔒 Framework Self-Containment Policy

**MANDATORY CONSTRAINT**: This framework MUST be completely self-contained within `/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator` and NEVER use external scripts, resources, or dependencies from the broader repository unless explicitly specified.

**APPROVED INTERNAL DEPENDENCIES**:
- ✅ `bin/setup_clc` (within framework directory) - For framework operations only
- ✅ `bin/login_oc` (within framework directory) - For framework operations only  
- ✅ AI-powered services within framework
- ✅ Standard `kubectl/oc` CLI usage
- ✅ Framework-internal utilities only

**GENERATED TEST CASE POLICY**:
- ✅ Use generic `oc login` commands in test tables for broader team usability
- ✅ Avoid exposing internal framework scripts to end users
- ✅ Provide clear, standard OpenShift login instructions

**PROHIBITED EXTERNAL DEPENDENCIES**:
- ❌ Any `bin/` scripts from parent directories
- ❌ `resource_schema_helper` scripts from external locations
- ❌ Any shell scripts outside the framework directory
- ❌ References to `../../../bin/` or similar external paths

## Configuration Files
This framework uses modular configuration files for maintainability:

- **Test Case Format Requirements**: `.claude/templates/test-case-format-requirements.md` - Complete test case structure and format standards
- **Test Scoping Rules**: `.claude/prompts/test-scoping-rules.md` - Smart test scoping methodology
- **YAML Sample Templates**: `.claude/templates/yaml-samples.md` - YAML samples for expected results
- **Environment Configuration**: `.claude/templates/environment-config.md` - Environment setup and validation
- **Bash Command Patterns**: `.claude/templates/bash-command-patterns.md` - Command chaining and execution patterns
- **Deployment Validation Checklist**: `.claude/templates/deployment-validation-checklist.md` - Evidence-based feature availability validation
- **Feedback Loop System**: `.claude/workflows/feedback-loop-system.md` - Human review and improvement integration
- **Framework Greetings**: `.claude/greetings/framework-greetings.md` - Welcome message and quick start guide

## Command Reference

**AI-Powered Analysis Patterns**: The framework uses intelligent AI services for:
- Environment setup and validation with automated command chaining
- JIRA analysis workflows through AI Documentation Service
- GitHub PR analysis via AI GitHub Investigation Service
- Testing and validation through AI Validation Service
- Troubleshooting with intelligent error detection and resolution

### AI Validation Service

The framework uses AI-powered validation services for intelligent output analysis and quality assurance.

**Intelligent Validation Features:**
- Automated detection of escaped pipes in bash code blocks
- Smart enforcement of ManagedClusterView guidance for managed-cluster reads
- Dynamic YAML server-side validation via `oc apply --dry-run=server -f -`
- Context-aware test case structure validation
- Intelligent error detection and correction suggestions

**Validation Process:**
All generated test cases and analysis reports are automatically processed through the AI Validation Service during generation, ensuring consistent quality and adherence to framework standards without manual intervention.

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
- **Generic Test Case Commands**: Use standard `oc login` commands in generated test tables for broader team usability (framework uses internal scripts for setup operations)
- **Schema-Aware YAML**: ClusterCurator examples include required fields (`towerAuthSecret`, `prehook`, `posthook`, `install`)
- **ManagedClusterView Usage**: When reading managed cluster resources (e.g., `ClusterVersion`), use `ManagedClusterView` from the hub
- **Mandatory Login Step**: ALL test cases MUST start with cluster login as Step 1
- **Clean Markdown**: No HTML tags (`<br>`, etc.), inline commands with backticks, no unnecessary line breaks in tables

### Stage 5: Analysis Report & Intelligent Feedback Loop
- **Dual File Output**: Complete-Analysis.md + Test-Cases.md
- **Streamlined Analysis Reports**: 
  - **🚨 DEPLOYMENT STATUS** (first): Clear, evidence-based feature availability with supporting data
  - **Implementation Status** (second): What is implemented, PRs, key behavior
  - **Environment & Validation Status** (third): Environment used, validation results, limitations
  - **Concise Feature Summary**: Brief feature explanation + data collection summary (no detailed framework process explanations)
- **⚠️ MANDATORY Deployment Status Analysis**: Evidence-based feature availability assessment with supporting validation data
- **Clear Status Reporting**: What can be tested now vs. post-deployment with concrete evidence
- **Self-Contained Report Generation**: Use generic `oc login` commands in test tables while framework uses internal scripts for operations
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

**Command Usage**: See `.claude/references/command-examples.md` for:
- Command chaining patterns and session state management
- Generic login formats for team usability
- Environment setup best practices

### AI-Powered Framework Process
1. Connect to environment (default: qe6) using setup utilities
2. **AI INVESTIGATION PROTOCOL**: JIRA + PRs + Internet Research via AI services - REQUIRED
3. **AI Implementation Validation**: Intelligent schemas, architecture, and testing analysis
4. **AI Test Case Generation**: Description + Setup + Enhanced Expected Results format
5. **AI Analysis Reports**: Concise feature summaries with environment specification
6. **AI Feedback Loop Execution**: Quality assessment and iterative improvement
7. Create dual output with full AI investigation transparency
8. Provide deployment assessment with AI-generated investigation evidence

### Expected Output
- **Time**: 5-10 minutes | **Cases**: 3-5 E2E scenarios | **Format**: Production-ready with enhanced structure
- **Test Case Format**: Description + Setup + Steps with verbal instructions + Enhanced Expected Results
- **Expected Results Include**: Verbal explanations + Sample YAML/data outputs + Expected command outputs
- **Analysis Reports**: Environment & validation status upfront + Concise feature summaries with investigation transparency
- **Quality Assurance**: AI-powered feedback loop for continuous improvement and intelligent oversight

## Output Structure

> **Detailed Structure**: See `.claude/references/command-examples.md` for complete directory layout and file organization patterns.

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
- **AI Feedback Loop**: Automated quality assessment, intelligent review triggers, and continuous improvement
- **AI Investigation Protocol**: JIRA hierarchy + GitHub analysis + Internet research + Implementation validation via AI services
- **Task-Focused Reports**: Clean outputs without framework self-references

## 🔧 Advanced Features

> **Implementation Validation**: See `.claude/advanced/implementation-validation.md`
> **Investigation Protocol**: See `.claude/workflows/investigation-protocol.md`  
> **Framework Advantages**: See `.claude/advanced/framework-advantages.md`

### 🔍 Critical Validation Requirements ⚠️ MANDATORY

**BEFORE generating test cases**, the AI framework MUST ALWAYS:
1. **AI PR Analysis**: Find and analyze ALL implementation PRs via AI GitHub Investigation Service - NO EXCEPTIONS
2. **AI Internet Research**: Research technology, docs, and best practices via AI services - REQUIRED
3. **AI Schema Validation**: Inspect actual field structures and behaviors via AI Schema Service
4. **AI Architecture Discovery**: Understand operational patterns through AI investigation
5. **AI Implementation Assessment**: Validate actual deployment and feature availability via AI services
6. **AI Feedback Loop**: Quality assessment and iterative improvement via AI
7. **AI Documentation**: Full transparency of research and validation process via AI services

**FAILURE TO COMPLETE INVESTIGATION = INVALID TEST GENERATION**

### 🎯 Investigation Protocol ⚠️ MANDATORY

**ALWAYS EXECUTE COMPLETE INVESTIGATION - NO SHORTCUTS ALLOWED**

**Step 1: AI JIRA Hierarchy Deep Dive** (100% coverage requirement):
1. **AI Documentation Service**: Main ticket + ALL nested linked tickets (up to 3 levels deep with recursion protection)
2. **AI Analysis**: ALL subtasks + dependency chains + epic context + related tickets
3. **AI Comments Analysis**: Across ALL discovered tickets for additional insights and links
4. **AI Cross-reference Validation**: Consistency checking across entire ticket network

**Step 2: AI PR Investigation** (MANDATORY):
1. **AI GitHub Investigation Service**: Find ALL related PRs through intelligent search
2. **AI Code Analysis**: Implementation details and code changes
3. **AI Discussion Analysis**: PR discussions and technical decisions
4. **AI Deployment Validation**: Status and integration points

**Step 3: AI Internet Research** (MANDATORY):
1. **AI Research Service**: Relevant technology and documentation
2. **AI Pattern Analysis**: Best practices and common patterns
3. **AI Domain Learning**: Domain-specific knowledge for accurate testing
4. **AI Assumption Validation**: Against authoritative sources

**Step 4: AI Implementation Reality Validation** (MANDATORY):
1. **AI Schema Service**: Deep schema inspection and field validation
2. **AI Cluster Testing**: Components and behaviors analysis
3. **AI Architecture Discovery**: Operational pattern analysis
4. **⚠️ AI Feature Deployment Validation**: Evidence-based verification of feature availability in test environment
   - Container image analysis and version correlation
   - Actual feature behavior testing
   - PR merge date to release cycle mapping
   - Clear distinction between "implemented" vs. "deployed"

**Step 5: AI Missing Data Handling** (MANDATORY):
1. **AI Gap Detection**: Detect gaps and quantify impact
2. **AI Documentation**: Limitations and assumptions via AI services
3. **AI Roadmap**: Future roadmap for complete testing via AI planning

### 📊 Quality Standards

**Always Generate Best Possible Test Plan**:
- Create comprehensive cases even with incomplete validation
- Use generic inspection commands when specific validation fails
- Provide multiple validation approaches for uncertain scenarios
- Ensure test plans work when limitations are resolved