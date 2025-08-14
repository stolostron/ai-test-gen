# Intelligent Test Analysis Engine

## 🎯 Framework Introduction

> **Quick Start Guide**: See `docs/quick-start.md`
> **Welcome Message**: See `.claude/greetings/framework-greetings.md`

**Latest Version**: V2.0 - Intelligent, adaptive test generation with AI-powered category classification, enhanced validation, and continuous learning
**Framework Status**: Production-ready with complete AI service integration, intelligent category-aware validation, and self-improving quality assurance
**Polarion Integration**: Optional AI-powered enterprise test case management (user-driven, clean 3-file architecture with secure PAT storage)

## 🚨 CRITICAL FRAMEWORK POLICY

### 🤖 MANDATORY AI-POWERED VALIDATION & FEEDBACK LOOP SYSTEM ⚠️ ENFORCED
**AI-Powered Framework Requirements** (STRICTLY ENFORCED):
- 🔒 **🔍 AI Complete Investigation Protocol**: MANDATORY execution of ALL AI service steps - NO EXCEPTIONS OR SHORTCUTS
  - **3-Level Deep JIRA Analysis**: ALL nested links, subtasks, dependencies, and comments
  - **Documentation Investigation**: ALL documentation links with nested discovery
  - **Internet Research**: Comprehensive technology and best practices research
  - **GitHub Analysis**: ALL related PRs with implementation details
- 🔒 **AI FEATURE DEPLOYMENT VALIDATION**: **MANDATORY THOROUGH VERIFICATION** - Complete validation of feature implementation in test environment
- 🔒 **🎯 AI Category Classification**: MANDATORY intelligent ticket categorization and template selection
- 🔒 **📊 AI Category-Aware Validation**: MANDATORY category-specific quality checks and scoring
- 🔒 **🤖 AI Validation Feedback Loop**: MANDATORY real-time quality optimization with iterative refinement
- 🔒 **🧠 AI Learning System**: MANDATORY continuous improvement through pattern recognition and feedback
- 🔒 **AI Schema Service**: MANDATORY dynamic CRD analysis and server-side validation
- 🔒 **AI Complete Investigation**: FAILURE TO EXECUTE THOROUGH INVESTIGATION = INVALID TEST GENERATION

**ENFORCEMENT MECHANISM**:
- ❌ **BLOCKED**: Any test generation without complete AI investigation protocol
- ❌ **BLOCKED**: Test generation without 3-level deep JIRA hierarchy analysis (ALL nested links)
- ❌ **BLOCKED**: Test generation without comprehensive documentation link investigation
- ❌ **BLOCKED**: Test generation without thorough GitHub PR analysis and internet research
- ❌ **BLOCKED**: Test generation without thorough feature deployment validation
- ❌ **BLOCKED**: Test generation without AI category classification and template selection
- ❌ **BLOCKED**: Test generation without AI-powered validation feedback loop execution
- ❌ **BLOCKED**: Outputs not meeting category-specific quality targets (85-95+ points)
- ❌ **BLOCKED**: Skipping AI validation services or feedback loop steps
- ❌ **BLOCKED**: Manual shortcuts bypassing AI-powered intelligence
- ❌ **BLOCKED**: Assumptions about deployment without concrete evidence
- ✅ **REQUIRED**: Full AI service integration with intelligent category-aware validation for every analysis request

### 🚨 CRITICAL FORMAT REQUIREMENTS - ENFORCED BY VALIDATION

**Quality Target: 85-95+ points** (Category-aware scoring with AI validation - Upgrade/Security: 95+, Import/Export: 92+, UI: 90+, Tech Preview: 88+)

### ❌ ZERO TOLERANCE FAILURES (CAUSES IMMEDIATE VALIDATION FAILURE)
1. **2-COLUMN TABLE FORMAT**: Must use exactly 2 columns (Step | Expected Result) - causes 15-point deduction for 3-column format
2. **ACCURATE DEPLOYMENT VALIDATION**: Must correlate ACM/MCE versions with feature availability - causes 20-point deduction for incorrect status
3. **FULL COMMANDS**: Must provide complete commands with proper placeholders - causes 10-point deduction for generic placeholders
4. **🚨 CRITICAL: NO HTML TAGS ANYWHERE**: STRICTLY FORBIDDEN - Never use `<br/>`, `<b>`, `<i>`, `<div>`, or any HTML tags in markdown code blocks or anywhere else - causes 25-point deduction for ANY HTML tag usage (AI-powered detection enabled)
5. **EXACT LOGIN FORMAT**: Must use exact Step 1 format - causes 15-point deduction if wrong
6. **DEPLOYMENT STATUS HEADER**: Must use `## 🚨 DEPLOYMENT STATUS` exactly - causes 15-point deduction if wrong
7. **VERBAL EXPLANATION REQUIREMENT**: Expected Results MUST include verbal explanation of what terminal outputs mean, not just raw output - causes 20-point deduction if missing
8. **DEFINITIVE TEST CASE FOCUS**: All test cases must clearly outline verification procedures for specific features or aspects, using clear testing language (e.g., "Verify...", "Test...", "Validate...") with definitive steps that prove functionality - causes 15-point deduction for vague investigative language
9. **NO INTERNAL SCRIPTS**: Never mention `setup_clc` or `login_oc` in user-facing content - causes 10-point deduction (AI-powered prevention enabled)

### ⚠️ MANDATORY TEST TABLE FORMAT REQUIREMENTS
**Enhanced Test Case Standards** (85+ points required):
- ✅ **CRITICAL: 2-Column Format ONLY**: Test tables MUST use exactly 2 columns (Step | Expected Result) - NO 3-column formats
- ✅ **Step Column Content**: Include verbal instructions + commands in Step column (e.g., "**Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster.com:6443 --username=kubeadmin --password=<password>`")
- ✅ **Full Commands Required**: Provide complete commands with proper placeholders (not generic `<cluster-url>`)
- ✅ **Verbal Explanations Required**: NEVER start test steps with only commands - always include verbal instructions
- ✅ **Sample Outputs Mandatory**: Include realistic sample outputs in triple backticks for ALL steps that fetch/update data
- ✅ **NO HTML Tags Policy**: STRICTLY FORBIDDEN - use ` - ` instead of `<br/>` tags
- ✅ **Enhanced Tester Experience**: Provide clear expectations with realistic data examples

### ⚠️ MANDATORY INTERNAL vs EXTERNAL USAGE
**Framework Internal Operations** (Claude's AI process):
- ✅ **Environment Setup**: Uses `bin/setup_clc` and `bin/login_oc` for robust cluster connectivity
- ✅ **AI Services**: Leverages integrated AI Documentation, GitHub Investigation, Schema, and Validation services
- ✅ **Quality Assurance**: Automated validation and continuous improvement via AI

**Generated Output Requirements** (User-facing content):
- 🎯 **Test Cases**: ALWAYS show generic `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` commands
- 🎯 **Final Reports**: NEVER mention setup_clc or login_oc scripts
- 🎯 **User Experience**: Clean, standard OpenShift patterns without internal framework details
- 🎯 **Professional Format**: Production-ready test cases with enhanced Expected Results

### 🔒 SCRIPT USAGE ENFORCEMENT
- **FRAMEWORK MUST USE**: `setup_clc` and `login_oc` for all environment operations
- **OUTPUTS MUST SHOW**: Generic `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` commands only
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
- [🔗 Polarion Integration](#polarion-integration)
- [📋 Enhanced Test Table Format Requirements](#mandatory-test-table-format-requirements)

---

## 🚀 Quick Start

> **Complete Guide**: See `docs/quick-start.md`

### 🎯 Most Common Usage
1. **Navigate** to the framework directory: `cd apps/claude-test-generator`
2. **Ask Claude** to analyze any JIRA ticket: "Analyze ACM-XXXXX"
3. **Get Results** in 5-10 minutes with production-ready test cases

### 📊 What You Get (V2.0 Enhanced)
- **🕐 Time**: 5-10 minute analysis with intelligent optimization
- **📋 Test Cases**: 3-5 comprehensive E2E scenarios tailored to ticket category
- **🎯 Quality**: 85-95+ points with category-aware AI validation
- **📝 Reports**: Complete analysis + clean test cases with intelligent categorization
- **🔒 Deployment Status**: Evidence-based assessment (DEPLOYED/PARTIALLY/NOT DEPLOYED/BUG)
- **🔗 Polarion Integration**: Optional posting to Polarion (when explicitly requested) with test case IDs and links
- **🧠 Intelligence**: AI category detection, adaptive templates, and continuous learning
- **🌐 Environment**: Default qe6 or your specified cluster

### 🤖 AI-Powered Process (V2.0)
- **🎯 Category Classification**: AI automatically identifies ticket type and selects optimal template
- **🔍 Complete Investigation Protocol**: 
  - **3-Level Deep JIRA Analysis**: ALL nested links, subtasks, dependencies, comments
  - **Documentation Research**: ALL documentation links with nested discovery
  - **Internet Research**: Comprehensive technology and best practices study
  - **GitHub Analysis**: ALL related PRs with implementation details
- **🔒 Feature Deployment Validation**: Thorough verification of ALL PR changes deployed and operational
- **📊 Category-Aware Generation**: Enhanced test cases tailored to specific ticket category with AI feedback loop
- **🤖 Real-time Validation**: AI validates during generation with iterative refinement until optimal quality
- **🧠 Learning Integration**: Continuous improvement through pattern recognition and feedback
- **🔗 Optional Polarion Integration**: Enterprise test case management with learning and direct posting
- **Quality**: 85-95+ point targets with adaptive scoring and continuous optimization

---

## 🏗️ System Architecture (V2.0)

**Intelligent, Adaptive Test Generation Engine**: AI-powered system that performs human-level reasoning with category classification, adaptive template selection, and continuous learning for optimal test generation.

**Core AI Services**:
- **AI Documentation Service**: JIRA hierarchy analysis and recursive link discovery
- **AI GitHub Investigation Service**: PR discovery and implementation validation  
- **🔒 AI Feature Deployment Validation Service**: Thorough verification of ALL PR changes deployed and operational in test environment
- **🎯 AI Category Classification Service**: Intelligent ticket categorization and template selection
- **📊 AI Category-Aware Validation Service**: Category-specific quality checks and adaptive scoring
- **AI Schema Service**: Dynamic CRD analysis and intelligent YAML generation
- **🧠 AI Learning and Feedback Service**: Continuous improvement through pattern recognition
- **AI Validation Service**: Automated quality assurance and compliance verification
- **🔗 AI Polarion Service**: Optional enterprise test case management with intelligent posting (user-driven)

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

### 🚨 Core Framework Standards:
- **Test Case Standards**: `.claude/templates/test-case-format-requirements.md`
- **🚨 Standard Headers**: `.claude/templates/standard-headers.md` - Exact format requirements
- **🤖 AI Validation Enhancement**: `.claude/templates/ai-validation-enhancement.md` - AI-powered quality assurance with HTML tag and script detection
- **🚨 HTML Tag Validation**: `.claude/templates/html-tag-validation-system.md` - Comprehensive HTML tag detection and prevention
- **Deployment Validation**: `.claude/templates/deployment-validation-checklist.md`

### 🧠 Intelligent Enhancement System:
- **🎯 Intelligent Classification**: `.claude/templates/intelligent-classification-system.md` - AI-powered ticket categorization
- **📊 Enhanced Category Scenarios**: `.claude/templates/enhanced-category-scenarios.md` - Advanced category-specific templates
- **🔍 Category-Aware Validation**: `.claude/templates/category-aware-validation.md` - Smart validation by category
- **🧠 AI Feedback Learning**: `.claude/templates/ai-feedback-learning-system.md` - Continuous improvement system

### 🔗 Optional Polarion AI Service:
- **AI Polarion Service**: `polarion/ai_polarion_service.py` - Single comprehensive AI service (replaces 9 scripts)
- **Credential Management**: Secure local storage with AI-guided setup
- **Connection Testing**: Multi-phase diagnostics with intelligent error handling
- **Test Case Posting**: Smart parsing and metadata enhancement (user-driven only)

### 📝 Supporting Templates:
- **🎯 Category Templates**: `.claude/templates/category-specific-templates.md` - Quick templates for common ticket types
- **Test Scoping Rules**: `.claude/prompts/test-scoping-rules.md` 
- **YAML Templates**: `.claude/templates/yaml-samples.md` - AI-generated samples
- **Environment Setup**: `.claude/templates/environment-config.md`
- **Command Patterns**: `.claude/templates/bash-command-patterns.md`
- **Feedback System**: `.claude/workflows/feedback-loop-system.md`
- **Quick Start**: `.claude/greetings/framework-greetings.md`

### 🔗 Enterprise Integration:
- **Polarion Setup**: `docs/polarion-setup-guide.md` - Complete Polarion integration setup
- **Polarion CLI**: `docs/polarion-cli-reference.md` - Comprehensive CLI command reference
- **Polarion Workflow**: `.claude/workflows/polarion-integration.md` - Enhanced workflow integration

## 🤖 AI Service Architecture

**Integrated AI Intelligence Pipeline**:
- **🔍 Documentation Intelligence**: JIRA hierarchy analysis via AI Documentation Service
- **📊 Code Intelligence**: GitHub PR discovery via AI GitHub Investigation Service  
- **🔒 Deployment Intelligence**: Comprehensive feature deployment validation via AI Feature Deployment Validation Service
- **⚙️ Schema Intelligence**: Dynamic CRD analysis via AI Schema Service
- **✅ Quality Intelligence**: Automated validation via AI Validation Service
- **🎯 Classification Intelligence**: AI-powered ticket categorization and template selection
- **📈 Category Intelligence**: Category-aware scenario generation and validation
- **🧠 Learning Intelligence**: Continuous improvement through pattern recognition and feedback
- **🌐 Environment Management**: Internal cluster connectivity (setup_clc/login_oc for framework operations only)
- **🔗 Optional Polarion Intelligence**: Enterprise test case management with user-driven posting and AI enhancement

### AI Validation Service

The framework uses AI-powered validation services for intelligent output analysis and quality assurance.

**🤖 Enhanced AI Validation Features:**
- **🚨 Real-time HTML Tag Detection**: AI scans and blocks ANY HTML tags (`<br/>`, `<b>`, `<i>`, `<div>`, etc.) with 25-point deduction
- **🔒 Internal Script Prevention**: AI detects and prevents setup_clc/login_oc exposure in user content with 10-point deduction  
- **Login Step Pattern Recognition**: AI validates exact login format and provides corrections
- **Deployment Status Header Verification**: AI ensures exact header format compliance
- **Sample Output Analysis**: AI verifies realistic sample outputs in code blocks
- **🎯 Intelligent Category Recognition**: AI identifies ticket types and applies category-specific validation
- **📊 Category-Aware Quality Scoring**: AI adapts quality targets and checks based on ticket category
- **🧠 Pattern Learning and Adaptation**: AI learns from validation results to improve future outputs
- **Consistency Enforcement**: AI maintains standardization across all outputs
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

## Workflow Overview (V2.0)

The framework follows an intelligent 7-stage approach with AI category classification and mandatory feature deployment validation:

### Stage 0: 🎯 AI Category Classification & Template Selection (NEW)
- **Intelligent Ticket Analysis**: AI analyzes JIRA content for category indicators
- **Category Classification**: AI determines primary/secondary categories with confidence scoring
- **Template Selection**: AI selects optimal template based on classification
- **Quality Target Setting**: AI sets category-appropriate quality targets (85-95+ points)

### Stage 1: Environment Setup & Validation
- **Flexible Environment Configuration**: Default qe6 or user-specified
- **Environment Validation**: Graceful handling of unavailable environments
- **Cluster Connectivity**: Verify access and permissions
- **Status Reporting**: Clear execution guidance

### Stage 2: Multi-Source Intelligence Gathering ⚠️ MANDATORY
- **🔒 COMPLETE INVESTIGATION PROTOCOL**: ALWAYS perform ALL steps below - NO EXCEPTIONS OR SHORTCUTS
- **🔍 MANDATORY JIRA HIERARCHY ANALYSIS**: 
  - **3-Level Deep Recursion**: Main ticket + ALL subtasks + ALL linked tickets + nested dependencies
  - **ALL Documentation Links**: Extract and analyze EVERY documentation link with nested discovery
  - **Comment Analysis**: Review ALL comments across entire ticket network for additional insights
  - **Dependency Chain Mapping**: Map complete dependency relationships and blocking issues
- **📊 MANDATORY GITHUB INVESTIGATION**:
  - **ALL Related PRs**: Find and analyze EVERY related PR through intelligent search
  - **Implementation Details**: Code changes, architectural impact, and integration points
  - **PR Discussion Analysis**: Technical decisions, review comments, and implementation choices
- **🌐 MANDATORY COMPREHENSIVE INTERNET RESEARCH**:
  - **Technology Deep Dive**: Research relevant technology, frameworks, and best practices
  - **Domain Knowledge**: Understand business context and industry standards
  - **Pattern Analysis**: Identify common implementation patterns and testing approaches
- **🔒 THOROUGH FEATURE IMPLEMENTATION VALIDATION**: **MANDATORY** - Comprehensive validation of ALL PR changes deployed and operational in test environment
- **🎯 Smart Test Scope Analysis**: Focus ONLY on changed functionality after complete understanding

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

### Stage 5: 📊 Category-Aware Test Strategy Generation & AI-Powered Quality Optimization
- **🤖 MANDATORY AI-POWERED VALIDATION FEEDBACK LOOP**: 
  - **Real-time AI Validation**: AI validates test cases during generation with immediate feedback
  - **Pattern Learning**: AI learns from validation results to improve future test generation
  - **Quality Prediction**: AI predicts quality scores and suggests improvements before generation
  - **Iterative Refinement**: AI continuously refines test cases until optimal quality achieved
- **Category-Specific Test Coverage**: E2E workflows tailored to ticket category requirements
- **Adaptive Scenario Selection**: AI selects optimal scenarios based on category and context
- **Required Test Case Structure** ⚠️ MANDATORY: 
  - **Description**: Clear explanation of what the test case does/tests exactly
  - **Setup**: Required setup/prerequisites needed for the test case  
  - **Test Steps Table**: Step-by-step execution with enhanced format requirements
  - **First Step MUST BE**: `**Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: oc login...`
  - **NO HTML TAGS**: Never use `<br/>`, use ` - ` or line breaks instead
- **Test Step Format Requirements** ⚠️ MANDATORY:
  All test steps MUST include:
  1. **🚨 CRITICAL: Verbal instruction FIRST** - ALWAYS start with verbal description of what to do (NEVER only put a CLI command)
  2. **CLI command** (when applicable) 
  3. **UI guidance** (when applicable)
  **CRITICAL ENFORCEMENT**: 
  - NEVER start a step with only a command like "oc login <cluster-url>"
  - ALWAYS prefix with verbal explanation like "Log into the ACM hub cluster: oc login <cluster-url>"
  - NEVER use HTML tags (`<br/>`, `<b>`, `<i>`) anywhere in step descriptions
- **Expected Result Format Requirements** ⚠️ MANDATORY:
  Expected Results MUST contain:
  1. **🚨 CRITICAL: Verbal explanation FIRST** - ALWAYS start Expected Results with verbal description of what the output means and what it indicates
  2. **Terminal/Command outputs** in proper markdown code blocks (NO HTML tags like `<br/>` anywhere)
  3. **Sample YAML/data outputs** when getting or updating resources (use realistic examples)
  4. **Interpretation guidance** - Explain what success looks like and what the tester should understand from the output
  5. **Specific values** or output descriptions with realistic sample data
  **CRITICAL ENFORCEMENT**: 
  - NEVER use only raw terminal output without verbal explanation
  - NEVER use HTML tags (`<br/>`, `<b>`, `<i>`) in code blocks or anywhere else
  - ALWAYS explain what the output indicates about the system state or feature status
- **Standalone Test Cases**: Each test case must be completely self-contained with no setup dependencies
- **Simple Execution**: Keep steps straightforward and easy to follow
- **🚨 CRITICAL: Table Size Limit**: Each test table MUST have maximum 8-10 steps - create multiple tables if more steps needed
- **Multiple Focused Tables**: REQUIRED to create multiple tables for comprehensive coverage when verification needs more than 10 steps
- **Terminal-Ready Commands**: Copy-pasteable commands with clear expected outputs
- **⚠️ MANDATORY Generic Commands**: ALWAYS use standard `oc login <cluster-url>` in test tables (NEVER mention framework's internal setup_clc/login_oc scripts)
- **Schema-Aware YAML**: ClusterCurator examples include required fields (`towerAuthSecret`, `prehook`, `posthook`, `install`)
- **ManagedClusterView Usage**: When reading managed cluster resources (e.g., `ClusterVersion`), use `ManagedClusterView` from the hub
- **⚠️ MANDATORY Login Step**: ALL test cases MUST start with generic `oc login <cluster-url>` as Step 1 (NEVER mention setup_clc/login_oc)
- **⚠️ MANDATORY Script Policy**: NEVER mention setup_clc or login_oc in any test case or report - use standard OpenShift commands only
- **Clean Markdown**: ⚠️ MANDATORY - NO HTML tags (`<br>`, `<div>`, etc.) anywhere in test cases or reports, use proper markdown formatting only, inline commands with backticks, no unnecessary line breaks in tables

### Stage 6: 📊 Category-Aware Analysis Report & 🧠 Intelligent Learning Loop
**CRITICAL OUTPUT REQUIREMENTS:**
- **Complete-Analysis.md MUST include**: `## 🚨 DEPLOYMENT STATUS` header exactly
- **Test-Cases.md MUST start with**: Login step in exact required format
- **NO HTML tags anywhere**: Use markdown formatting only
- **Dual File Output**: Complete-Analysis.md + Test-Cases.md
- **🔗 Polarion Integration**: Optional posting of test cases to Polarion (when explicitly requested by user)
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
- **📊 Category-Aware Quality Validation**: AI validates outputs against category-specific requirements (85-95+ points)
- **🔗 Optional Polarion Integration Workflow**:
  - **User-Driven Activation**: Polarion integration only when explicitly requested by user
  - **AI-Powered Detection**: Framework detects Polarion configuration availability
  - **Optional Posting**: Test cases posted to Polarion only when user specifically requests it
  - **Metadata Enhancement**: JIRA ticket ID and generation metadata added via AI service
  - **Status Reporting**: Polarion availability status always included in Complete-Analysis.md
  - **Independent Operation**: Framework works perfectly without Polarion integration
- **🧠 Intelligent Learning System**:
  - **Pattern Recognition**: AI learns from successful and failed validation patterns
  - **Template Evolution**: Automatic improvement of category templates based on outcomes
  - **Quality Prediction**: AI predicts quality scores before generation
  - **Adaptive Optimization**: Continuous refinement of classification and validation logic
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
6. **🔗 Polarion Integration**: Optional posting of generated test cases to Polarion (when explicitly requested) with metadata from JIRA ticket
7. **AI Analysis Reports**: Concise feature summaries with environment specification, **EVIDENCE-BASED deployment status assessment**, and Polarion integration status
8. **AI Feedback Loop**: Quality assessment, continuous improvement, and iterative optimization
9. **Dual Output Generation**: Complete analysis + clean test cases with full AI investigation transparency, definitive deployment status, and Polarion integration results

### 📈 Expected Output
- **⏱️ Time**: 5-10 minutes | **📋 Cases**: 3-5 E2E scenarios | **🎯 Format**: Production-ready
- **📝 Test Cases**: Description + Setup + Enhanced Expected Results with AI-generated YAML
- **📊 Analysis**: Environment status + Feature summary + Investigation transparency
- **🔒 Deployment Status**: Evidence-based verdict (DEPLOYED/PARTIALLY/NOT DEPLOYED/BUG) with concrete proof
- **🔗 Polarion Integration**: Optional posting to Polarion (when explicitly requested) with test case IDs and direct links
- **✅ Quality**: AI-powered validation and continuous improvement

## 📁 Output Structure

**Dual Output Format**:
- **Complete-Analysis.md**: Full investigation + deployment status + environment validation
- **Test-Cases.md**: Clean, executable test scenarios with AI-generated examples
- **Organized Runs**: Timestamped directories for version control and tracking

## Core Principles (V2.0)

### 🧠 Intelligent Adaptation
- **Category-Aware Generation**: AI automatically adapts test generation to ticket type
- **Continuous Learning**: Framework improves through pattern recognition and feedback
- **Predictive Quality**: AI predicts and optimizes quality scores before generation
- **Adaptive Templates**: Dynamic template selection and customization based on context

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

### 🔧 Integration Features (V2.0)
- **🧠 Intelligent Classification**: AI-powered ticket categorization and template selection
- **📊 Category-Aware Testing**: Tailored test generation for 7 primary categories (Upgrade, UI, Import/Export, Resource Management, Global Hub, Tech Preview, Security/RBAC)
- **🎯 Adaptive Quality Targets**: Category-specific quality scores (85-95+ points) with intelligent optimization
- **ACM/CLC Specific**: Domain expertise for cluster lifecycle testing
- **E2E Test Coverage**: Complete end-to-end workflows for all NEW functionality
- **🔒 Deployment Validation**: Thorough verification that ALL PR changes are deployed and operational
- **Professional Test Format**: Description + Setup + Enhanced Expected Results with sample YAML/data outputs
- **🧠 Learning System**: Continuous improvement through pattern recognition and feedback
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

4. **Version & Release Correlation** ⚠️ **CRITICAL ADDITION**:
   - **ACM/MCE Version Checking**: Correlate current environment version with feature availability
   - **Container image analysis and version correlation**
   - **PR merge date to release cycle mapping**
   - **Clear distinction between "implemented" vs. "deployed"**
   - **Feature roadmap analysis**: When will feature be available in current environment
   - **Deployment timeline analysis and availability prediction**

5. **AI-Powered Enhanced Validation System** ⚠️ **DEFINITIVE DEPLOYMENT ASSESSMENT**:
   - **Multi-Source Evidence Collection**: Combine version checking, behavioral testing, and schema validation
   - **Concrete Supporting Data**: Generate irrefutable proof of deployment status with specific evidence
   - **Intelligent Cross-Validation**: AI correlates multiple data points to eliminate false positives/negatives
   - **Definitive Verdict Generation**: AI provides unambiguous deployment status with comprehensive justification
   - **Evidence Documentation**: Full transparency of all validation data and reasoning used in assessment
   - **Error Prevention**: AI prevents incorrect deployment assessments through rigorous multi-stage validation

**🚨 ENHANCED ENFORCEMENT**: The AI-powered framework MUST leverage its enhanced validation system to provide definitive deployment status with irrefutable supporting evidence. The AI system prevents incorrect assessments through multi-source validation and intelligent cross-correlation. Speculation or assumptions are STRICTLY PROHIBITED.

**Step 5: AI Missing Data Handling** (MANDATORY):
1. **AI Gap Detection**: Detect gaps and quantify impact
2. **AI Documentation**: Limitations and assumptions via AI services
3. **AI Roadmap**: Future roadmap for complete testing via AI planning

### 📊 Quality Standards

**🚨 MANDATORY: Always Generate Comprehensive E2E Test Plans**:
- **REGARDLESS OF DEPLOYMENT STATUS**: Generate complete test plans even if feature is not deployed, partially deployed, or validation fails
- **COMPREHENSIVE COVERAGE**: Test cases must cover ALL aspects of the feature using E2E approach with different scenarios
- **DEFINITIVE VERIFICATION**: Each test case must clearly outline how to verify specific functionality with concrete steps
- **FEATURE-COMPLETE TESTING**: Cover happy path, error scenarios, edge cases, and integration points
- **DEPLOYMENT-INDEPENDENT**: Test cases should work when feature becomes available, regardless of current limitations
- **E2E METHODOLOGY**: Follow end-to-end testing patterns from setup through cleanup
- **SCENARIO DIVERSITY**: Include multiple test scenarios to ensure comprehensive feature validation
- **🚨 CRITICAL: TEST TABLE SIZE LIMIT**: Each test table MUST have maximum 8-10 steps - if verification requires more steps, create additional test tables to ensure full coverage

---

## 🔒 FINAL ENFORCEMENT DECLARATION

### 🚨 ABSOLUTE FRAMEWORK REQUIREMENTS - NO EXCEPTIONS

**THIS FRAMEWORK WILL STRICTLY ENFORCE THE FOLLOWING:**

1. **🤖 COMPLETE AI INVESTIGATION PROTOCOL**: 
   - ❌ Framework REFUSES to generate test cases without executing ALL AI service steps
   - ❌ NO shortcuts, NO manual bypasses, NO exceptions
   - ✅ MANDATORY: 3-level deep JIRA hierarchy analysis with ALL nested links
   - ✅ MANDATORY: Comprehensive documentation link investigation with nested discovery
   - ✅ MANDATORY: Thorough internet research on technology and best practices
   - ✅ MANDATORY: Complete GitHub PR analysis with implementation details
   - ✅ MANDATORY: **THOROUGH FEATURE IMPLEMENTATION VALIDATION**

2. **🔒 MANDATORY FEATURE DEPLOYMENT VALIDATION**:
   - ❌ Framework BLOCKS test generation without comprehensive feature deployment verification
   - ❌ NO assumptions about deployment based on infrastructure availability
   - ✅ MANDATORY: Thorough validation of ALL PR changes deployed and operational
   - ✅ MANDATORY: Evidence-based deployment status with concrete supporting data
   - 🚨 **CRITICAL**: Framework must definitively determine if feature is deployed, partially deployed, not deployed, or has implementation bugs

3. **🔄 AI VALIDATION & FEEDBACK LOOP**:
   - ❌ Framework BLOCKS any generation without AI validation service
   - ❌ NO bypassing quality scoring or compliance verification
   - ❌ Framework BLOCKS test generation without AI-powered validation feedback loop execution
   - ✅ MANDATORY: Real-time AI validation during test case generation
   - ✅ MANDATORY: Pattern learning and iterative refinement until optimal quality
   - ✅ MANDATORY: Quality prediction and improvement suggestions

4. **📋 ENHANCED TEST FORMAT REQUIREMENTS (85+ POINTS TARGET)**:
   - ❌ Framework REJECTS test cases without verbal explanations and sample outputs
   - ❌ NO HTML tags (`<br/>`, `<b>`, `<i>`), NO command-only steps, NO missing expected results  
   - ❌ Framework BLOCKS outputs with wrong login format or deployment status header
   - ✅ MANDATORY: Professional format with realistic examples and complete validation
   - ✅ MANDATORY: Quality scoring 85+ points with validation checklist compliance

5. **🔒 DEPLOYMENT STATUS ENFORCEMENT**:
   - ❌ Framework REFUSES to generate deployment status without thorough feature validation
   - ❌ NO speculation or assumptions about feature availability
   - ✅ MANDATORY: Evidence-based deployment assessment with concrete supporting data
   - ✅ MANDATORY: Clear deployment verdict (DEPLOYED/PARTIALLY DEPLOYED/NOT DEPLOYED/BUG) with proof

**🚨 ENFORCEMENT MECHANISM**: Framework operates under STRICT compliance mode - any attempt to bypass these requirements will result in BLOCKED execution and REFUSED test generation.

**🔒 FEATURE DEPLOYMENT VALIDATION GUARANTEE**: The framework MUST perform thorough validation of actual feature implementation and provide definitive deployment status with concrete evidence. Infrastructure availability does NOT equal feature deployment.

**✅ COMPLIANCE GUARANTEE**: Following this protocol ensures production-ready, AI-validated, comprehensive test plans with intelligent quality assurance, thorough feature deployment validation, and continuous improvement.

## 📊 QUALITY SCORING SYSTEM (V2.0)

**CATEGORY-AWARE VALIDATION SCORING (TARGET: 85-95+ POINTS)**

### 🎯 Base Quality Score (90 points):
- **Files exist** (Complete-Analysis.md, Test-Cases.md, metadata.json): 20 points
- **No HTML tags** anywhere in outputs: 25 points (ENHANCED - Zero tolerance)
- **No internal scripts** mentioned: 10 points (AI-powered prevention)
- **Correct login step** format exactly: 15 points  
- **Deployment status header** exactly: 15 points
- **Sample outputs** in code blocks: 10 points

### 📊 Category Enhancement Layer (+10-15 points):
- **Upgrade/Security**: Version validation, rollback procedures, compatibility checks (+15 points, Target: 95+)
- **Import/Export**: State validation, error recovery, timeout handling (+12 points, Target: 92+)
- **UI Component**: Visual validation, accessibility, cross-browser testing (+10 points, Target: 90+)
- **Resource Management**: Performance baselines, limit testing, stress testing (+13 points, Target: 93+)
- **Global Hub**: Hub coordination, cross-hub management (+12 points, Target: 92+)
- **Tech Preview**: Feature gates, GA transition, backward compatibility (+10 points, Target: 88+)

**TOTAL POSSIBLE: 100 points | CATEGORY-AWARE TARGETS: 85-95+ points**

### ❌ CRITICAL VALIDATION CHECKLIST:
**BEFORE GENERATING ANY OUTPUT, VERIFY:**
- [ ] 🔍 **MANDATORY JIRA HIERARCHY ANALYSIS**: 3-level deep recursion with ALL nested links completed
- [ ] 📄 **MANDATORY DOCUMENTATION INVESTIGATION**: ALL documentation links analyzed with nested discovery
- [ ] 🌐 **MANDATORY INTERNET RESEARCH**: Comprehensive technology and best practices research completed
- [ ] 📊 **MANDATORY GITHUB INVESTIGATION**: ALL related PRs analyzed with implementation details
- [ ] 🎯 AI category classification completed with confidence score
- [ ] 🔒 **AI-POWERED DEPLOYMENT VALIDATION**: Multi-source evidence collected and cross-validated
- [ ] 📊 **DEFINITIVE DEPLOYMENT STATUS**: ACM/MCE version correlation completed with concrete proof
- [ ] 🤖 **AI VALIDATION FEEDBACK LOOP**: Real-time AI validation and iterative refinement completed
- [ ] 📋 **2-COLUMN TABLE FORMAT**: Test tables use exactly Step | Expected Result format
- [ ] 🔧 **FULL COMMANDS**: Complete commands with proper placeholders provided
- [ ] 🚨 **AI HTML TAG DETECTION**: NO HTML tags (`<br/>`, `<b>`, `<i>`, `<div>`, etc.) anywhere - 25-point deduction
- [ ] 🔒 **AI SCRIPT PREVENTION**: No `setup_clc` or `login_oc` mentioned in any user-facing content - 10-point deduction
- [ ] ✅ First step EXACTLY: "**Step 1: Log into the ACM hub cluster**"
- [ ] ✅ Header EXACTLY: "## 🚨 DEPLOYMENT STATUS"
- [ ] ✅ Sample outputs in triple backticks for all fetch/update operations
- [ ] ✅ Files generated (Complete-Analysis.md, Test-Cases.md, metadata.json)
- [ ] ✅ Verbal instructions before all commands in test steps
- [ ] 📊 Category-specific validation checks completed
- [ ] 🧠 Learning feedback integrated for continuous improvement

**QUALITY ENFORCEMENT**: Framework tracks and validates outputs with category-aware scoring to maintain 85-95+ point quality standards through intelligent automation and continuous learning.

## 🧠 INTELLIGENT ENHANCEMENT SYSTEM (V2.0)

**AI-POWERED FRAMEWORK EVOLUTION** - Advanced intelligence layer for adaptive, category-aware test generation.

### 🎯 Key Enhancements Implemented:

#### **1. Intelligent Ticket Classification**
- **AI Category Detection**: Automatic identification of ticket types (Upgrade, UI, Import/Export, Resource Management, Global Hub, Tech Preview, Security/RBAC)
- **Confidence Scoring**: AI provides classification confidence levels (0.0-1.0)
- **Multi-Category Support**: Handles complex tickets with primary/secondary categories
- **Pattern Learning**: AI improves classification accuracy through feedback

#### **2. Category-Specific Test Generation**
- **Adaptive Templates**: AI selects optimal templates based on ticket category
- **Enhanced Scenarios**: Category-specific test scenarios with targeted validation
- **Quality Targets**: Category-aware quality score targets (88-95+ points)
- **Smart Customization**: AI adapts scenarios to ticket context and complexity

#### **3. Category-Aware Validation System**
- **Dynamic Scoring**: Base score (75 points) + category enhancement (20-25 points)
- **Specialized Checks**: Category-specific validation requirements
- **Adaptive Thresholds**: Quality targets adapt to category criticality
- **Intelligence Insights**: AI provides targeted improvement recommendations

#### **4. Continuous Learning and Improvement**
- **Pattern Recognition**: AI learns from successful and failed patterns
- **Template Evolution**: Automatic template improvement based on outcomes
- **Predictive Quality**: AI predicts quality scores before generation
- **Feedback Integration**: Continuous improvement through validation results

### 📊 Expected Performance Improvements:

**Quality Score Progression:**
- **Current Baseline**: 60/100 average → **Target**: 95+/100 consistent
- **Phase 1** (Immediate): 85+ through format fixes and category detection
- **Phase 2** (Week 2-4): 90+ through intelligent template selection
- **Phase 3** (Month 2): 93+ through learning system optimization
- **Phase 4** (Month 3): 95+ through advanced pattern recognition

**Efficiency Gains:**
- **Test Generation Time**: 50% reduction through intelligent automation
- **First-Pass Success**: 95% through category-aware generation  
- **Manual Review**: 70% reduction through quality prediction
- **Framework Consistency**: 98% through AI standardization

This intelligent enhancement system transforms the framework from static template application to adaptive, learning-based test generation that continuously evolves to deliver higher quality results.

## 🔗 Polarion Integration

**Optional AI-Powered Enterprise Test Case Management**

> **Quick Setup**: Use AI service for guided PAT setup (see below)  
> **Setup Guide**: [Polarion Setup Documentation](docs/polarion-setup-guide.md)  
> **CLI Reference**: [Complete CLI Command Reference](docs/polarion-cli-reference.md)  
> **Workflow Integration**: [Polarion Integration Workflow](.claude/workflows/polarion-integration.md)

### 🔐 PAT Setup Guide (REQUIRED for Polarion Integration)

**🚀 RECOMMENDED: AI-Guided Setup**
```bash
# One-command setup with AI guidance
python3 -c "from polarion import ai_setup_credentials; ai_setup_credentials()"
```

**What this does:**
- ✅ **Interactive prompts** for Polarion URL, Project ID, and PAT (hidden input)
- ✅ **Secure storage** in `.polarion/credentials.json` (protected by .gitignore)
- ✅ **File permissions** automatically set to 600 (owner read/write only)
- ✅ **Connection testing** with AI diagnostics and troubleshooting
- ✅ **Validation** ensures everything works before completing setup

**📍 Where Your PAT is Stored:**
```
claude-test-generator/
├── .polarion/                    # 🔒 Protected by .gitignore
│   └── credentials.json          # Your PAT stored here securely
├── polarion/
│   └── ai_polarion_service.py    # AI service that uses credentials
└── .gitignore                    # Contains .polarion/ protection
```

**🔒 Security Features:**
- ✅ **Git-Safe**: `.polarion/` directory protected by .gitignore
- ✅ **Local Storage**: Never stored in environment or shared locations  
- ✅ **Secure Permissions**: 600 (owner read/write only)
- ✅ **Hidden Input**: PAT entry is hidden during interactive setup

**⚡ Alternative: Environment Variables** (less secure)
```bash
export POLARION_URL='https://your-polarion-server.com'
export POLARION_PAT_TOKEN='your-pat-token-here'  
export POLARION_PROJECT_ID='YOUR_PROJECT_ID'
```

**🧪 Test Your Setup:**
```bash
# Check credential status
python3 -c "from polarion import ai_credential_status; result = ai_credential_status(); print('\\n'.join(result.recommendations))"

# Test connection with AI diagnostics
python3 -c "from polarion import ai_test_connection; result = ai_test_connection(); print('✅ Ready!' if result.success else '❌ Check config')"
```

### 🤖 Claude Integration Instructions

**OPTIONAL**: Polarion integration is now OPTIONAL - only when user explicitly requests it. Claude should use the AI-powered Polarion service:

```python
# Claude executes this ONLY when user specifically requests Polarion posting
from polarion import (
    post_test_cases_if_enabled, 
    get_polarion_status_for_framework,
    get_ai_polarion_service
)

# 1. OPTIONAL: Post test cases to Polarion (only if user requested)
if user_requested_polarion_posting:  # Only when explicitly requested
    ticket_id = "ACM-XXXXX"  # Extract from current analysis
    test_cases_file = "runs/ACM-XXXXX/latest/Test-Cases.md"
    
    posting_result = post_test_cases_if_enabled(
        test_cases_file=test_cases_file,
        ticket_id=ticket_id,
        user_requested=True  # REQUIRED - explicit user request
    )
    
    # Generate Polarion section with AI service
    service = get_ai_polarion_service()
    polarion_section = service.ai_generate_polarion_section(posting_result)
else:
    # 2. Always show Polarion status (shows "Optional" when not requested)
    polarion_section = get_polarion_status_for_framework()
```

**🚨 CRITICAL Integration Requirements:**
- ❌ **NO Automatic Posting**: Never attempt Polarion posting unless user explicitly requests it
- ✅ **User-Driven**: Only post when user specifically mentions Polarion in their request
- ✅ **AI Service**: Use the comprehensive AI-powered Polarion service (replaces all scripts)
- ✅ **Status Reporting**: Always include Polarion status in Complete-Analysis.md (shows availability)
- ✅ **Graceful Operation**: Framework works perfectly without Polarion integration
- ✅ **Optional Enhancement**: Treat Polarion as an optional enterprise feature

### 🎯 Integration Overview

The framework includes optional Polarion integration via a comprehensive AI service for enterprise environments:

**🤖 AI Service Features:**
- **🔐 Secure PAT Management**: AI-guided credential setup with local storage (see setup guide above)
- **🧠 Intelligent Connection Testing**: Multi-phase diagnostics with AI troubleshooting
- **📤 Smart Test Case Posting**: AI-enhanced parsing with automatic metadata detection
- **🔗 User-Driven Integration**: Only posts when explicitly requested (no automatic posting)
- **📊 Advanced Analytics**: Connection confidence scoring and detailed error analysis
- **🛡️ Enterprise Security**: Local credential storage protected by .gitignore

### 🚀 Quick Integration

**AI Service Setup:**
```bash
# Install minimal dependencies (only 3 packages)
pip3 install -r requirements.txt

# Setup credentials with AI service (creates .polarion/credentials.json)
python3 -c "from polarion import ai_setup_credentials; ai_setup_credentials()"

# Test connection with AI diagnostics
python3 -c "from polarion import ai_test_connection; result = ai_test_connection(); print(result.recommendations)"
```

**AI-Powered Workflow (OPTIONAL - when user requests):**
```bash
# 1. Check AI service status
python3 -c "from polarion import ai_credential_status; result = ai_credential_status(); print(result.recommendations)"

# 2. Run normal test generation (Polarion posting only if user specifically requests)
# ... Claude analysis (framework automatically shows Polarion availability) ...

# 3. Manual AI posting (if needed outside framework)
python3 -c "from polarion import ai_post_test_cases; ai_post_test_cases('Test-Cases.md', 'ACM-12345')"
```

### 🔧 Available AI Service Functions

**🤖 AI Setup & Testing:**
- `ai_setup_credentials()` - Interactive AI-guided credential setup
- `ai_test_connection()` - Intelligent connection diagnostics with multi-phase validation
- `ai_credential_status()` - Comprehensive AI status analysis

**🤖 AI Operations:**
- `ai_post_test_cases()` - Intelligent test case posting with metadata enhancement
- `post_test_cases_if_enabled()` - Framework integration (requires user_requested=True)
- `get_ai_polarion_service()` - Access to full AI service capabilities

**🧠 AI Features:**
- Intelligent credential management with secure local storage
- Multi-source configuration discovery (local files + environment)
- AI-powered connection testing with detailed diagnostics
- Smart test case parsing from markdown with category detection
- Adaptive error handling and retry strategies

### 📚 Documentation Structure

**Complete Setup Documentation:**
- **[Setup Guide](docs/polarion-setup-guide.md)** - Step-by-step setup with troubleshooting
- **[CLI Reference](docs/polarion-cli-reference.md)** - Complete command documentation with examples
- **[Workflow Integration](.claude/workflows/polarion-integration.md)** - Enhanced workflow patterns

**Key Benefits of AI Service:**
- ✅ **User Control** - Polarion posting only when explicitly requested (no automatic posting)
- ✅ **🔐 Security First** - PAT stored locally in `.polarion/credentials.json` (protected by .gitignore)
- ✅ **AI Intelligence** - Smart credential management, connection diagnostics, and test case parsing
- ✅ **Simplified Architecture** - Single AI service replaces 9 separate scripts (80% size reduction)
- ✅ **Enhanced Quality** - Intelligent metadata enhancement and category detection
- ✅ **Robust Reliability** - Multi-phase validation and adaptive error handling
- ✅ **Enterprise Ready** - Optional integration that never interferes with normal operation

### 🚨 Migration to AI Service

**Complete Script-to-AI Migration Completed:**
- **9 scripts replaced** with single comprehensive AI service (`ai_polarion_service.py`)
- **All functionality enhanced** with AI intelligence and user-driven activation
- **Deprecated scripts removed**: `setup_polarion.sh`, `provide-feedback-to-claude.sh`
- **75% file reduction** achieved while improving capabilities
- **Zero regressions** - framework works perfectly with or without Polarion

**Scripts Replaced by AI Service:**
- `api_client.py` → AI-powered connection management
- `config.py` → Intelligent configuration discovery
- `credentials.py` → AI-guided secure credential management
- `test_case_fetcher.py` → Smart test case operations
- `test_case_poster.py` → Enhanced posting with metadata
- `cli.py` → Replaced with AI service functions
- `framework_integration.py` → Integrated into AI service
- `setup_polarion.sh` → Replaced with AI-guided setup
- Plus additional AI enhancement scripts

**Final Clean Architecture:**
- **3 core files**: `ai_polarion_service.py`, `__init__.py`, `README.md`
- **Secure storage**: `.polarion/credentials.json` (protected by .gitignore)
- **Minimal dependencies**: `requirements.txt` optimized for AI service (3 packages)
- **Cache cleanup**: Removed `__pycache__/` (auto-generated bytecode)
- **Total size**: ~61KB (down from 100KB+ originally)

**New Usage Pattern (OPTIONAL):**
1. **PAT Setup**: `from polarion import ai_setup_credentials; ai_setup_credentials()` (stores securely in `.polarion/credentials.json`)
2. **Framework Integration**: Automatically shows Polarion availability in analysis reports
3. **User-Driven Posting**: Only when user explicitly requests Polarion integration in their analysis request
4. **Security**: PAT protected by .gitignore, never committed to git

## 📝 FRAMEWORK VERSION HISTORY

### V2.0 (Current) - Intelligent Enhancement System
**Release**: August 2025  
**Major Features**:
- 🎯 AI-powered ticket classification with 7 primary categories
- 📊 Category-aware validation with adaptive quality targets (85-95+ points)
- 🔍 **MANDATORY 3-level deep JIRA hierarchy analysis** with complete nested link investigation
- 📄 **MANDATORY comprehensive documentation research** with nested discovery
- 🌐 **MANDATORY thorough internet research** for technology and best practices
- 📊 **MANDATORY complete GitHub PR analysis** with implementation details
- 🤖 **MANDATORY AI-powered validation feedback loop** with real-time quality optimization
- 🚨 Enhanced HTML tag detection and prevention (25-point deduction)
- 🔒 Advanced internal script exposure prevention (10-point deduction)
- 🧠 Continuous learning system with pattern recognition
- 📈 Enhanced category-specific scenario templates
- 🔍 Intelligent template selection and customization
- 📊 Quality score progression tracking and optimization
- 🤖 **Complete AI Service Replacement**: Replaced 9 Polarion scripts with single comprehensive AI service
- 🎯 **Optional Polarion Integration**: Made Polarion posting user-driven (not automatic)
- 🧹 **Complete Cleanup**: Removed all deprecated scripts and Python cache (`setup_polarion.sh`, `provide-feedback-to-claude.sh`, `__pycache__/`)
- ⚡ **80% Size Reduction**: Optimized from 100KB+ to ~61KB total
- 🏗️ **Minimal Architecture**: Clean 3-file structure with documentation
- 🔒 **Secure PAT Storage**: AI-guided setup with `.gitignore` protection

### V1.0 - Foundation Framework
**Release**: December 2024  
**Major Features**:
- 🤖 AI investigation protocol with JIRA + GitHub + Internet research
- 🔒 Mandatory feature deployment validation
- ✅ Real-time quality validation (85+ point target)
- 📋 Enhanced test format requirements
- 🚨 Critical format enforcement (HTML tags, login format, deployment status)
- 🔄 Basic feedback loop system

### Evolution Path:
- **V1.0 → V2.0**: Static templates → Intelligent, adaptive generation
- **Quality Improvement**: 60/100 average → 85-95+ category-aware targets
- **Intelligence Layer**: Added classification, learning, and pattern recognition
- **Future Roadmap**: Advanced ML models, predictive analytics, autonomous optimization