# Intelligent Test Analysis Engine

## 🎯 Framework Introduction

> **Quick Start Guide**: See `docs/quick-start.md`
> **Welcome Message**: See `.claude/greetings/framework-greetings.md`

**Latest Version**: AI-powered framework with integrated investigation, comprehensive feature deployment validation, and generation services
**Framework Status**: Production-ready with complete AI service integration, thorough feature deployment validation, and intelligent quality assurance

## 🚨 CRITICAL FRAMEWORK POLICY

### 🤖 MANDATORY AI-POWERED VALIDATION & FEEDBACK LOOP SYSTEM ⚠️ ENFORCED
**AI-Powered Framework Requirements** (STRICTLY ENFORCED):
- 🔒 **AI Investigation Protocol**: MANDATORY execution of ALL AI service steps - NO EXCEPTIONS OR SHORTCUTS
- 🔒 **AI FEATURE DEPLOYMENT VALIDATION**: **MANDATORY THOROUGH VERIFICATION** - Complete validation of feature implementation in test environment
- 🔒 **AI Validation Service**: MANDATORY real-time quality validation during generation
- 🔒 **AI Feedback Loop**: MANDATORY quality assessment and continuous improvement process
- 🔒 **AI Schema Service**: MANDATORY dynamic CRD analysis and server-side validation
- 🔒 **AI Complete Investigation**: FAILURE TO EXECUTE THOROUGH FEATURE VALIDATION = INVALID TEST GENERATION

**ENFORCEMENT MECHANISM**:
- ❌ **BLOCKED**: Any test generation without complete AI investigation protocol
- ❌ **BLOCKED**: Test generation without thorough feature deployment validation
- ❌ **BLOCKED**: Skipping AI validation services or feedback loop steps
- ❌ **BLOCKED**: Manual shortcuts bypassing AI-powered intelligence
- ❌ **BLOCKED**: Assumptions about deployment without concrete evidence
- ✅ **REQUIRED**: Full AI service integration with comprehensive feature implementation validation for every analysis request

### ⚠️ MANDATORY TEST TABLE FORMAT REQUIREMENTS
**Enhanced Test Case Standards** (Recently Updated):
- ✅ **Verbal Explanations Required**: NEVER start test steps with only commands - always include verbal instructions
- ✅ **Sample Outputs Mandatory**: Include realistic sample outputs for ALL steps that fetch/update data
- ✅ **NO HTML Tags Policy**: Strictly enforce markdown-only formatting throughout all generated content
- ✅ **Enhanced Tester Experience**: Provide clear expectations with realistic data examples

### ⚠️ MANDATORY INTERNAL vs EXTERNAL USAGE
**Framework Internal Operations** (Claude's AI process):
- ✅ **Environment Setup**: Uses `bin/setup_clc` and `bin/login_oc` for robust cluster connectivity
- ✅ **AI Services**: Leverages integrated AI Documentation, GitHub Investigation, Schema, and Validation services
- ✅ **Quality Assurance**: Automated validation and continuous improvement via AI

**Generated Output Requirements** (User-facing content):
- 🎯 **Test Cases**: ALWAYS show generic `oc login <cluster-url>` commands
- 🎯 **Final Reports**: NEVER mention setup_clc or login_oc scripts
- 🎯 **User Experience**: Clean, standard OpenShift patterns without internal framework details
- 🎯 **Professional Format**: Production-ready test cases with enhanced Expected Results

### 🔒 SCRIPT USAGE ENFORCEMENT
- **FRAMEWORK MUST USE**: `setup_clc` and `login_oc` for all environment operations
- **OUTPUTS MUST SHOW**: Generic `oc login <cluster-url>` commands only
- **USERS MUST SEE**: Standard OpenShift workflows without internal implementation details

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
- [📋 Enhanced Test Table Format Requirements](#mandatory-test-table-format-requirements)

---

## 🚀 Quick Start

> **Complete Guide**: See `docs/quick-start.md`

### 🎯 Most Common Usage
1. **Navigate** to the framework directory: `cd apps/claude-test-generator`
2. **Ask Claude** to analyze any JIRA ticket: "Analyze ACM-XXXXX"
3. **Get Results** in 5-10 minutes with production-ready test cases

### 📊 What You Get
- **🕐 Time**: 5-10 minute analysis
- **📋 Test Cases**: 3-5 comprehensive E2E scenarios  
- **🎯 Quality**: AI-validated, production-ready format
- **📝 Reports**: Complete analysis + clean test cases
- **🔒 Deployment Status**: Evidence-based assessment (DEPLOYED/PARTIALLY/NOT DEPLOYED/BUG)
- **🌐 Environment**: Default qe6 or your specified cluster

### 🤖 AI-Powered Process
- **Investigation**: Automatic JIRA + GitHub + Internet research
- **🔒 Feature Deployment Validation**: Thorough verification of ALL PR changes deployed and operational
- **Validation**: Real-time schema and deployment validation
- **Generation**: Enhanced test cases with Expected Results
- **Quality**: Automated feedback loop and continuous improvement

---

## 🏗️ System Architecture

**AI-Powered Test Intelligence Engine**: Performs human-level reasoning about complex software systems using integrated AI services for comprehensive test analysis and generation.

**Core AI Services**:
- **AI Documentation Service**: JIRA hierarchy analysis and recursive link discovery
- **AI GitHub Investigation Service**: PR discovery and implementation validation  
- **🔒 AI Feature Deployment Validation Service**: Thorough verification of ALL PR changes deployed and operational in test environment
- **AI Schema Service**: Dynamic CRD analysis and intelligent YAML generation
- **AI Validation Service**: Automated quality assurance and compliance verification

**🎯 Smart Test Scoping**: Focus ONLY on changed functionality, avoiding redundant testing of stable components.

## 🛠️ Available Tools

### 🤖 Core AI Services
- **🔍 AI Documentation Service**: 
  - JIRA hierarchy analysis with 3-level recursive link traversal
  - Comment analysis and URL extraction
  - Quality-scored investigation summaries
- **📊 AI GitHub Investigation Service**: 
  - Intelligent PR discovery and analysis
  - Implementation status validation via WebFetch
  - Code change impact assessment
- **🔒 AI Feature Deployment Validation Service**: 
  - Comprehensive verification of ALL PR changes deployed and operational in test environment
  - Behavioral testing to confirm actual feature functionality
  - Evidence-based deployment status assessment (DEPLOYED/PARTIALLY/NOT DEPLOYED/BUG)
  - Integration validation and dependency verification
- **⚙️ AI Schema Service**: 
  - Dynamic CRD inspection and OpenAPI schema analysis
  - Intelligent YAML generation with required fields
  - Server-side validation via `oc apply --dry-run=server`
- **✅ AI Validation Service**: 
  - Automated escaped pipe detection
  - ManagedClusterView guidance enforcement
  - Test case structure and quality validation

### 🔧 Infrastructure Tools
- **📋 Jira CLI**: Ticket analysis and hierarchical discovery
- **🌐 WebFetch**: GitHub PR content analysis and documentation fetch
- **⚡ kubectl/oc**: Kubernetes/OpenShift cluster operations
- **📝 TodoWrite**: Task tracking and progress management
- **🔐 setup_clc**: Environment setup utility (internal framework use only)
- **🔑 login_oc**: OpenShift authentication utility (internal framework use only)

## 🔒 Framework Self-Containment Policy

**MANDATORY CONSTRAINT**: This framework MUST be completely self-contained within `/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator` and NEVER use external scripts, resources, or dependencies from the broader repository unless explicitly specified.

**APPROVED INTERNAL DEPENDENCIES** ⚠️ MANDATORY:
- ✅ `bin/setup_clc` - FRAMEWORK INTERNAL USE ONLY for environment setup
- ✅ `bin/login_oc` - FRAMEWORK INTERNAL USE ONLY for cluster authentication
- ✅ AI-powered services within framework
- ✅ Standard `kubectl/oc` CLI usage

**CRITICAL TEST CASE POLICY** ⚠️ MANDATORY:
- ✅ **ALWAYS use generic `oc login <cluster-url>` commands in ALL generated test tables**
- ✅ **NEVER mention setup_clc or login_oc scripts in final reports or test cases**
- ✅ **NEVER expose internal framework scripts to end users**
- ✅ **Framework uses setup_clc/login_oc internally but test cases show standard OpenShift login**

**PROHIBITED EXTERNAL DEPENDENCIES**:
- ❌ Any `bin/` scripts from parent directories
- ❌ External shell scripts or utilities
- ❌ References to `../../../bin/` or similar external paths
- ❌ Deprecated script dependencies (replaced by AI services)

## 📋 Configuration Files
**Modular AI Service Configuration**:

- **Test Case Standards**: `.claude/templates/test-case-format-requirements.md`
- **Test Scoping Rules**: `.claude/prompts/test-scoping-rules.md` 
- **YAML Templates**: `.claude/templates/yaml-samples.md` - AI-generated samples
- **Environment Setup**: `.claude/templates/environment-config.md`
- **Command Patterns**: `.claude/templates/bash-command-patterns.md`
- **Deployment Validation**: `.claude/templates/deployment-validation-checklist.md`
- **Feedback System**: `.claude/workflows/feedback-loop-system.md`
- **Quick Start**: `.claude/greetings/framework-greetings.md`

## 🤖 AI Service Architecture

**Integrated AI Intelligence Pipeline**:
- **🔍 Documentation Intelligence**: JIRA hierarchy analysis via AI Documentation Service
- **📊 Code Intelligence**: GitHub PR discovery via AI GitHub Investigation Service  
- **🔒 Deployment Intelligence**: Comprehensive feature deployment validation via AI Feature Deployment Validation Service
- **⚙️ Schema Intelligence**: Dynamic CRD analysis via AI Schema Service
- **✅ Quality Intelligence**: Automated validation via AI Validation Service
- **🌐 Environment Management**: Internal cluster connectivity (setup_clc/login_oc for framework operations only)

### AI Validation Service

The framework uses AI-powered validation services for intelligent output analysis and quality assurance.

**Intelligent Validation Features:**
- **Escaped Pipe Detection**: Automated scanning of bash code blocks for problematic escaped pipes
- **ManagedClusterView Enforcement**: Smart guidance for managed-cluster resource reads
- **Server-side YAML Validation**: Dynamic validation via `oc apply --dry-run=server -f -`
- **Test Case Structure Validation**: Context-aware validation of test format requirements
- **Quality Assessment**: Intelligent error detection and correction suggestions

**AI Validation Process:**
1. **Real-time Analysis**: Continuous validation during test case generation
2. **Pattern Recognition**: AI identifies common validation issues and anti-patterns
3. **Automated Correction**: AI suggests and applies corrections where possible
4. **Quality Scoring**: AI provides quality metrics for generated content
5. **Compliance Verification**: Ensures adherence to framework standards and best practices

**🔒 MANDATORY ENFORCEMENT**:
- ❌ **BLOCKED**: Test generation without AI validation service execution
- ❌ **BLOCKED**: Bypassing quality scoring and compliance verification
- ✅ **REQUIRED**: All validation occurs automatically during generation without manual intervention
- 🚨 **CRITICAL**: Framework enforces validation compliance - no exceptions allowed

## Workflow Overview

The framework follows a structured 6-stage approach with mandatory feature deployment validation:

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
- **🔒 THOROUGH FEATURE IMPLEMENTATION VALIDATION**: **MANDATORY** - Comprehensive validation of ALL PR changes deployed and operational in test environment
- **Smart Test Scope Analysis**: Focus ONLY on changed functionality after complete understanding

### Stage 3: 🔒 AI FEATURE DEPLOYMENT VALIDATION ⚠️ **MANDATORY - NEW CRITICAL STAGE**
- **🚨 COMPREHENSIVE IMPLEMENTATION VERIFICATION**: Use AI to thoroughly validate that ALL specific changes from the PR are actually deployed and functional in the test environment
- **Behavioral Testing**: AI-driven testing of actual feature behavior to confirm operational status
- **Evidence Collection**: Gather concrete proof of deployment status with supporting data
- **Deployment Assessment**: Generate definitive verdict on feature availability:
  - **FULLY DEPLOYED**: Complete feature operational with evidence
  - **PARTIALLY DEPLOYED**: Specific components missing with detailed analysis
  - **NOT DEPLOYED**: Feature unavailable with timeline and reasons
  - **IMPLEMENTATION BUG**: Deployed but malfunctioning with error details
- **Integration Validation**: Verify all integration points and dependencies are functional

### Stage 4: AI Reasoning and Strategic Test Intelligence
- **Semantic Feature Analysis**: Understand feature intent and requirements
- **Architectural Reasoning**: Assess system design impact
- **Business Impact Modeling**: Quantify customer and revenue impact
- **Risk-Based Prioritization**: Focus on high-value, high-risk scenarios

### Stage 5: Test Strategy Generation & Quality Optimization
- **E2E Test Coverage**: Complete end-to-end workflows covering all NEW functionality
- **Required Test Case Structure** ⚠️ MANDATORY: 
  - **Description**: Clear explanation of what the test case does/tests exactly
  - **Setup**: Required setup/prerequisites needed for the test case  
  - **Test Steps Table**: Step-by-step execution with enhanced format requirements
- **Test Step Format Requirements** ⚠️ MANDATORY:
  All test steps MUST include:
  1. **Verbal instruction** describing what to do (NEVER only put a CLI command)
  2. **CLI command** (when applicable) 
  3. **UI guidance** (when applicable)
  **CRITICAL**: Never start a step with only a command like "oc login <cluster-url>". Always prefix with verbal explanation like "Log into the ACM hub cluster: oc login <cluster-url>"
- **Expected Result Format Requirements** ⚠️ MANDATORY:
  Expected Results MUST contain:
  1. **Verbal explanation** of what should happen
  2. **Sample YAML/data outputs** when getting or updating resources (use realistic examples)
  3. **Expected command outputs** when commands/grep are used (so testers can easily see and match probable outputs)
  4. **Specific values** or output descriptions with realistic sample data
  **CRITICAL**: When steps fetch or update data, ALWAYS include sample outputs in markdown code blocks (```)
- **Standalone Test Cases**: Each test case must be completely self-contained with no setup dependencies
- **Simple Execution**: Keep steps straightforward and easy to follow
- **Multiple Focused Tables**: OK to create multiple tables for clarity
- **Terminal-Ready Commands**: Copy-pasteable commands with clear expected outputs
- **⚠️ MANDATORY Generic Commands**: ALWAYS use standard `oc login <cluster-url>` in test tables (NEVER mention framework's internal setup_clc/login_oc scripts)
- **Schema-Aware YAML**: ClusterCurator examples include required fields (`towerAuthSecret`, `prehook`, `posthook`, `install`)
- **ManagedClusterView Usage**: When reading managed cluster resources (e.g., `ClusterVersion`), use `ManagedClusterView` from the hub
- **⚠️ MANDATORY Login Step**: ALL test cases MUST start with generic `oc login <cluster-url>` as Step 1 (NEVER mention setup_clc/login_oc)
- **⚠️ MANDATORY Script Policy**: NEVER mention setup_clc or login_oc in any test case or report - use standard OpenShift commands only
- **Clean Markdown**: ⚠️ MANDATORY - NO HTML tags (`<br>`, `<div>`, etc.) anywhere in test cases or reports, use proper markdown formatting only, inline commands with backticks, no unnecessary line breaks in tables

### Stage 6: Analysis Report & Intelligent Feedback Loop
- **Dual File Output**: Complete-Analysis.md + Test-Cases.md
- **Streamlined Analysis Reports**: 
  - **🚨 DEPLOYMENT STATUS** (first): Clear, evidence-based feature availability with supporting data
  - **Implementation Status** (second): What is implemented, PRs, key behavior
  - **Environment & Validation Status** (third): Environment used, validation results, limitations
  - **Concise Feature Summary**: Brief feature explanation + data collection summary (no detailed framework process explanations)
- **🚨 MANDATORY DEPLOYMENT STATUS ANALYSIS**: Definitive evidence-based feature availability assessment with comprehensive validation data
- **🔒 THOROUGH IMPLEMENTATION VERIFICATION**: Complete validation of ALL PR changes deployed and operational in test environment
- **🎯 DEPLOYMENT VERDICT**: Clear, unambiguous deployment status with concrete supporting evidence:
  - **✅ FULLY DEPLOYED**: All feature components operational with validation proof
  - **🔄 PARTIALLY DEPLOYED**: Specific deployed/missing components with detailed breakdown
  - **❌ NOT DEPLOYED**: Feature unavailable with clear evidence and timeline
  - **🐛 DEPLOYMENT BUG**: Feature deployed but malfunctioning with error analysis
- **📊 EVIDENCE-BASED REPORTING**: What can be tested immediately vs. post-deployment with concrete validation data
- **⚠️ MANDATORY Report Policy**: ALWAYS use generic `oc login <cluster-url>` commands in test tables - NEVER expose framework's internal setup_clc/login_oc scripts to end users
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

### ⚠️ AI Service Integration

**Framework Internal Operations**:
- **🌐 Environment**: setup_clc/login_oc (INTERNAL USE ONLY - never shown in test cases)
- **🔍 Investigation**: AI Documentation + GitHub Investigation Services
- **🔒 Deployment Validation**: AI Feature Deployment Validation Service for thorough implementation verification
- **✅ Validation**: AI Validation Service for automated quality assurance
- **⚙️ Schema Generation**: AI Schema Service for intelligent YAML creation

**⚠️ CRITICAL RULE**: Test cases ALWAYS show `oc login <cluster-url>` - NEVER mention internal scripts

### AI-Powered Framework Process
1. **Environment Setup**: Connect to environment (default: qe6) using internal setup_clc/login_oc utilities (NEVER mention these in test cases - use generic `oc login` instead)
2. **AI Investigation Protocol**: JIRA + PRs + Internet Research via AI Documentation and GitHub Investigation Services - REQUIRED
3. **AI THOROUGH FEATURE DEPLOYMENT VALIDATION**: **MANDATORY** - Comprehensive validation that ALL PR changes are deployed and operational in test environment via AI services
4. **AI Test Case Generation**: Description + Setup + Enhanced Expected Results format with AI-generated YAML samples
5. **AI Quality Assurance**: Automated validation via AI Validation Service (escaped pipes, ManagedClusterView guidance, server-side YAML validation)
6. **AI Analysis Reports**: Concise feature summaries with environment specification and **EVIDENCE-BASED deployment status assessment**
7. **AI Feedback Loop**: Quality assessment, continuous improvement, and iterative optimization
8. **Dual Output Generation**: Complete analysis + clean test cases with full AI investigation transparency and definitive deployment status

### 📈 Expected Output
- **⏱️ Time**: 5-10 minutes | **📋 Cases**: 3-5 E2E scenarios | **🎯 Format**: Production-ready
- **📝 Test Cases**: Description + Setup + Enhanced Expected Results with AI-generated YAML
- **📊 Analysis**: Environment status + Feature summary + Investigation transparency
- **🔒 Deployment Status**: Evidence-based verdict (DEPLOYED/PARTIALLY/NOT DEPLOYED/BUG) with concrete proof
- **✅ Quality**: AI-powered validation and continuous improvement

## 📁 Output Structure

**Dual Output Format**:
- **Complete-Analysis.md**: Full investigation + deployment status + environment validation
- **Test-Cases.md**: Clean, executable test scenarios with AI-generated examples
- **Organized Runs**: Timestamped directories for version control and tracking

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
- **🔒 Deployment Validation**: Thorough verification that ALL PR changes are deployed and operational
- **Professional Test Format**: Description + Setup + Enhanced Expected Results with sample YAML/data outputs
- **Universal Test Generation**: Works for any ACM story ticket with consistent quality standards
- **AI Feedback Loop**: Automated quality assessment, intelligent review triggers, and continuous improvement
- **AI Investigation Protocol**: JIRA hierarchy + GitHub analysis + Internet research + Comprehensive feature deployment validation via AI services
- **Task-Focused Reports**: Clean outputs without framework self-references

## 🔧 Advanced Features

> **Implementation Validation**: See `.claude/advanced/implementation-validation.md`
> **Investigation Protocol**: See `.claude/workflows/investigation-protocol.md`  
> **Framework Advantages**: See `.claude/advanced/framework-advantages.md`

### 🔍 Critical Feature Implementation Validation ⚠️ MANDATORY

**🚨 ABSOLUTE REQUIREMENT: THOROUGH FEATURE DEPLOYMENT VALIDATION 🚨**

**ENFORCEMENT POLICY**: The framework MUST perform comprehensive validation of actual feature implementation in the test environment - NOT just infrastructure availability.

**BEFORE generating test cases**, the AI framework MUST ALWAYS:
1. **AI PR Analysis**: Find and analyze ALL implementation PRs via AI GitHub Investigation Service - NO EXCEPTIONS
2. **AI Internet Research**: Research technology, docs, and best practices via AI services - REQUIRED
3. **AI Schema Validation**: Inspect actual field structures and behaviors via AI Schema Service
4. **AI Architecture Discovery**: Understand operational patterns through AI investigation
5. **🔒 AI FEATURE IMPLEMENTATION VALIDATION**: **MANDATORY THOROUGH VALIDATION** - Validate that ALL specific changes from the PR are actually deployed and working in the test environment
6. **🔒 AI DEPLOYMENT VERIFICATION**: **MANDATORY EVIDENCE-BASED ASSESSMENT** - Use AI to thoroughly test and verify the feature is operational with concrete evidence
7. **AI Feedback Loop**: Quality assessment and iterative improvement via AI
8. **AI Documentation**: Full transparency of research and validation process via AI services

**🚨 CRITICAL: FEATURE DEPLOYMENT VALIDATION REQUIREMENTS**:
- ❌ **NEVER ASSUME**: Infrastructure availability = Feature deployment
- ✅ **ALWAYS VALIDATE**: Every specific change from the PR is deployed and functional
- ✅ **PROVIDE EVIDENCE**: Concrete validation data proving feature deployment status
- ✅ **TEST BEHAVIOR**: Actual feature behavior validation through intelligent testing
- ✅ **CLEAR VERDICT**: Definitive deployment status with supporting evidence

**FAILURE TO COMPLETE THOROUGH IMPLEMENTATION VALIDATION = INVALID TEST GENERATION**

### 🎯 Investigation Protocol ⚠️ MANDATORY - STRICTLY ENFORCED

**🔒 ABSOLUTE REQUIREMENT: COMPLETE AI INVESTIGATION PROTOCOL 🔒**

**ENFORCEMENT POLICY**: 
- ❌ **BLOCKED**: Any attempt to bypass or skip AI investigation steps
- ❌ **BLOCKED**: Manual shortcuts or incomplete research
- ❌ **BLOCKED**: Test generation without full AI validation
- 🚨 **CRITICAL**: Framework will REFUSE to generate test cases without complete AI investigation

**ALWAYS EXECUTE COMPLETE INVESTIGATION - NO SHORTCUTS ALLOWED - NO EXCEPTIONS**

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

**Step 4: AI THOROUGH FEATURE IMPLEMENTATION VALIDATION** (MANDATORY):

**🔒 COMPREHENSIVE FEATURE DEPLOYMENT VERIFICATION** - This is the CRITICAL validation stage that determines if the feature is actually deployed and operational.

**4A. AI Schema & Infrastructure Validation**:
1. **AI Schema Service**: Deep schema inspection and field validation
2. **AI Cluster Testing**: Components and behaviors analysis
3. **AI Architecture Discovery**: Operational pattern analysis

**4B. AI FEATURE-SPECIFIC IMPLEMENTATION VALIDATION** ⚠️ **MANDATORY THOROUGH TESTING**:
1. **PR Change Validation**: For EACH specific change in the implementation PR:
   - Validate the exact code change is deployed in the environment
   - Test the specific behavior modification is functional
   - Verify new fields, annotations, or logic are operational
   - Confirm integration points work as implemented

2. **Behavioral Validation**: Use AI to intelligently test feature behavior:
   - Create and apply test resources with the new functionality
   - Validate expected behaviors occur as designed
   - Test edge cases and error conditions
   - Verify integration with existing systems

3. **Evidence-Based Assessment**: Generate concrete evidence of deployment status:
   - **DEPLOYED**: Feature fully operational with validation evidence
   - **PARTIALLY DEPLOYED**: Some components working, others missing (with specifics)
   - **NOT DEPLOYED**: Feature not available in environment (with evidence)
   - **IMPLEMENTATION BUG**: Feature deployed but not working correctly (with error details)

4. **Version & Release Correlation**:
   - Container image analysis and version correlation
   - PR merge date to release cycle mapping
   - Clear distinction between "implemented" vs. "deployed"
   - Deployment timeline analysis and availability prediction

**🚨 ENFORCEMENT**: The framework MUST provide definitive deployment status with concrete supporting evidence. Speculation or assumptions are PROHIBITED.

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

---

## 🔒 FINAL ENFORCEMENT DECLARATION

### 🚨 ABSOLUTE FRAMEWORK REQUIREMENTS - NO EXCEPTIONS

**THIS FRAMEWORK WILL STRICTLY ENFORCE THE FOLLOWING:**

1. **🤖 COMPLETE AI INVESTIGATION PROTOCOL**: 
   - ❌ Framework REFUSES to generate test cases without executing ALL AI service steps
   - ❌ NO shortcuts, NO manual bypasses, NO exceptions
   - ✅ MANDATORY: JIRA hierarchy + PR analysis + Internet research + Schema validation + **THOROUGH FEATURE IMPLEMENTATION VALIDATION**

2. **🔒 MANDATORY FEATURE DEPLOYMENT VALIDATION**:
   - ❌ Framework BLOCKS test generation without comprehensive feature deployment verification
   - ❌ NO assumptions about deployment based on infrastructure availability
   - ✅ MANDATORY: Thorough validation of ALL PR changes deployed and operational
   - ✅ MANDATORY: Evidence-based deployment status with concrete supporting data
   - 🚨 **CRITICAL**: Framework must definitively determine if feature is deployed, partially deployed, not deployed, or has implementation bugs

3. **🔄 AI VALIDATION & FEEDBACK LOOP**:
   - ❌ Framework BLOCKS any generation without AI validation service
   - ❌ NO bypassing quality scoring or compliance verification
   - ✅ MANDATORY: Real-time validation, quality assessment, continuous improvement

4. **📋 ENHANCED TEST FORMAT REQUIREMENTS**:
   - ❌ Framework REJECTS test cases without verbal explanations and sample outputs
   - ❌ NO HTML tags, NO command-only steps, NO missing expected results
   - ✅ MANDATORY: Professional format with realistic examples and complete validation

5. **🔒 DEPLOYMENT STATUS ENFORCEMENT**:
   - ❌ Framework REFUSES to generate deployment status without thorough feature validation
   - ❌ NO speculation or assumptions about feature availability
   - ✅ MANDATORY: Evidence-based deployment assessment with concrete supporting data
   - ✅ MANDATORY: Clear deployment verdict (DEPLOYED/PARTIALLY DEPLOYED/NOT DEPLOYED/BUG) with proof

**🚨 ENFORCEMENT MECHANISM**: Framework operates under STRICT compliance mode - any attempt to bypass these requirements will result in BLOCKED execution and REFUSED test generation.

**🔒 FEATURE DEPLOYMENT VALIDATION GUARANTEE**: The framework MUST perform thorough validation of actual feature implementation and provide definitive deployment status with concrete evidence. Infrastructure availability does NOT equal feature deployment.

**✅ COMPLIANCE GUARANTEE**: Following this protocol ensures production-ready, AI-validated, comprehensive test plans with intelligent quality assurance, thorough feature deployment validation, and continuous improvement.