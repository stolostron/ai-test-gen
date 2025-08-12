# Intelligent Test Analysis Engine

> **Enterprise-grade AI-powered test generation with unified command interface**

An intelligent system that analyzes software features and generates comprehensive E2E test plans. Part of the AI Test Generation Suite with unified command interface and production-ready capabilities. Designed specifically for Red Hat Advanced Cluster Management (ACM) and Open Cluster Management (OCM) testing scenarios.

## What This Framework Does

The Intelligent Test Analysis Engine automatically:

1. **Analyzes JIRA tickets** - Extracts business requirements and technical specifications
2. **Processes GitHub PRs** - Understands code changes and implementation details  
3. **Generates E2E test plans** - Creates comprehensive test cases with realistic expected outputs
4. **Assesses deployment readiness** - Determines if features are available in test environments
5. **Provides structured output** - Delivers both detailed analysis and clean test cases

### Key Capabilities

- **Smart Test Scoping**: Focuses only on NEW/CHANGED functionality, avoiding redundant testing
- **E2E Coverage**: Complete end-to-end workflows for comprehensive validation
- **Environment Assessment**: Evaluates feature availability and deployment status
- **Multiple Output Formats**: Both detailed analysis and clean test cases for different use cases
- **Feedback Loop Integration**: Human review triggers and continuous improvement

## 🧠 How It Works

The framework follows an intelligent 5-stage approach with complete investigation protocol:

### 1. ⚙️ Intelligent Environment Setup & Validation
- **Flexible Environment Configuration**: Default qe6 or user-specified environment
- **Kubeconfig Handling**: Auto-detects QE environments or validates custom kubeconfig
- **Cluster Connectivity**: Verify access, permissions, and tool availability
- **Graceful Degradation**: Works with whatever environment is accessible

### 2. 🔍 Complete Investigation Protocol ⚠️ MANDATORY
- **JIRA Hierarchy Deep Dive**: Main ticket + ALL subtasks + dependency chains + epic context (up to 3 levels)
- **GitHub PR Discovery & Analysis**: Find and analyze ALL related PRs for implementation details
- **Internet Research**: Technology documentation, best practices, and domain knowledge
- **Comments Analysis**: Extract insights from ALL discovered tickets and PRs
- **Implementation Reality Validation**: Deep schema inspection and actual field verification

### 3. 🧠 AI Reasoning and Strategic Test Intelligence ⚠️ MANDATORY
- **Semantic Feature Analysis**: Understand feature intent and business requirements
- **Smart Test Scoping**: Focus ONLY on NEW/CHANGED functionality after complete understanding
- **Architectural Impact Assessment**: System design and integration considerations
- **Risk-Based Prioritization**: High-value, high-risk scenarios identification

### 4. 📋 Test Strategy Generation & Quality Optimization
- **Enhanced Test Case Format**: Description + Setup + Steps + Enhanced Expected Results
- **Production-Ready Commands**: Copy-paste CLI commands with expected outputs
- **YAML Samples**: Realistic expected results with sample data outputs
- **Standalone Test Cases**: Self-contained with no external dependencies
- **Schema-Aware YAML**: Required fields validation and proper structure

### 5. 📈 Analysis Report & Intelligent Feedback Loop
- **Dual File Output**: Complete-Analysis.md + Test-Cases.md
- **Implementation Status**: Feature deployment assessment with evidence
- **Environment Validation**: Cluster status and limitation reporting
- **Quality Assessment**: Automated scoring and human review triggers
- **Continuous Improvement**: Learning integration for future generations

### Output Structure

Each run generates organized outputs:
```
runs/ACM-XXXXX/run-###-YYYYMMDD-HHMM/
├── Test-Cases.md           # Clean test cases (Description, Setup, Steps/Expected Results)
├── Complete-Analysis.md    # Full analysis with deployment assessment
└── metadata.json          # Run details and quality metrics
```

## 🚀 Quick Start

### Prerequisites
- Claude Code CLI configured
- Access to ACM test environment (qe6, qe7, qe8, qe9, qe10, or custom kubeconfig)
- JIRA ticket available for analysis

### Unified Command Interface

**From anywhere in the repository:**
```bash
# Most common usage - JIRA-based test plan generation
/generate-e2e-test-plan ACM-22079

# With specific QE environment
/generate-e2e-test-plan ACM-22079 --env qe6

# With custom kubeconfig
/generate-e2e-test-plan ACM-22079 --kubeconfig /path/to/your/kubeconfig

# PR-based generation with JIRA context
/generate-e2e-test-plan https://github.com/stolostron/cluster-curator-controller/pull/203 "Feature Name" ACM-10659.txt
```

**Application-Specific Usage:**
```bash
# Navigate to the framework for advanced features
cd apps/claude-test-generator
# Access specialized Claude config and advanced tools
```

### What Happens
1. **Intelligent Environment Setup**: Connects to specified environment (default: qe6) or validates custom kubeconfig
2. **Complete Investigation Protocol**: Deep analysis of JIRA tickets, GitHub PRs, and internet research
3. **AI-Powered Test Intelligence**: Smart scoping focusing ONLY on NEW/CHANGED functionality
4. **Production-Ready Output**: Both detailed analysis and clean test cases with enhanced format
5. **Deployment Assessment**: Feature availability validation with implementation evidence
6. **Quality Assurance**: Automated linting, validation, and feedback loop integration

### Expected Output
- **Execution Time**: 5-10 minutes with complete investigation
- **Test Cases**: 3-5 comprehensive E2E scenarios with enhanced format (Description + Setup + Steps + Enhanced Expected Results)
- **Coverage**: All NEW functionality with smart scoping and realistic validation
- **Quality**: Production-ready with copy-paste commands, YAML samples, and expected outputs
- **Validation**: Automated linting, schema validation, and deployment assessment

## 🔧 Available Tools & Scripts

### Core AI & Analysis Tools
- **Claude Code AI**: Advanced reasoning and test generation
- **WebFetch**: GitHub PR details and internet research
- **TodoWrite**: Task tracking and progress management
- **Jira CLI**: Comprehensive ticket analysis and hierarchy traversal

### Environment & Cluster Tools
- **setup_clc** (`bin/setup_clc`): Intelligent environment setup for QE clusters (qe6-qe10) or custom kubeconfig
- **login_oc** (`bin/login_oc`): OpenShift authentication with cluster credentials
- **kubectl/oc**: Kubernetes/OpenShift CLI for cluster validation and testing

### Investigation & Research Tools
- **github-investigation** (`bin/github-investigation.sh`): Deep repository analysis with SSH access and comprehensive PR discovery
- **doc-investigation** (`bin/doc-investigation.sh`): Recursive JIRA ticket traversal with comments analysis and link extraction
- **cc_schema_helper** (`bin/cc_schema_helper.sh`): ClusterCurator-specific schema validation and field inspection
- **resource_schema_helper** (`bin/resource_schema_helper.sh`): Generic CRD schema helper for YAML skeleton generation

### Quality Assurance & Validation Tools
- **post_generation_linter** (`bin/post_generation_linter.sh`): Automated output validation, escaped pipe detection, ManagedClusterView guidance
- **inject_required_keys** (`bin/inject_required_keys.sh`): Automatic YAML field injection for required keys (non-destructive)
- **YAML Server Validation**: Optional `oc apply --dry-run=server` validation for schema compliance

## ⚙️ Configuration & Advanced Usage

### Environment Configuration

**Unified Command Options:**
```bash
# Default environment (qe6)
/generate-e2e-test-plan ACM-22079

# Specific QE environment
/generate-e2e-test-plan ACM-22079 --env qe7
/generate-e2e-test-plan ACM-22079 --env qe8

# Custom kubeconfig
/generate-e2e-test-plan ACM-22079 --kubeconfig /path/to/config
```

**Post-Generation Validation:**
```bash
# Run automated linting on outputs
apps/claude-test-generator/bin/post_generation_linter.sh \
  --path apps/claude-test-generator/runs/ACM-XXXXX/latest

# Enable YAML server validation (requires oc login)
apps/claude-test-generator/bin/post_generation_linter.sh \
  --path apps/claude-test-generator/runs/ACM-XXXXX/latest \
  --validate-yaml
```

**Why Configure Environment?**
- Different environments may have different feature deployment status
- Allows testing against specific cluster configurations
- Enables validation across multiple test environments

### Framework Configuration Files

This framework uses modular configuration for maintainability and professional standards:

**Core Configuration:**
- **CLAUDE.md**: Specialized Claude configuration with advanced features and investigation protocols
- **Test Case Format**: `.claude/templates/test-case-format-requirements.md` - Enhanced format (Description + Setup + Steps + Expected Results)
- **Test Scoping Rules**: `.claude/prompts/test-scoping-rules.md` - Smart scoping focusing ONLY on changed functionality

**Templates & Standards:**
- **YAML Sample Templates**: `.claude/templates/yaml-samples.md` - YAML samples with required fields for expected results
- **Environment Configuration**: `.claude/templates/environment-config.md` - Environment setup and validation procedures
- **Bash Command Patterns**: `.claude/templates/bash-command-patterns.md` - Command chaining and execution patterns

**Quality & Workflow Systems:**
- **Feedback Loop System**: `.claude/workflows/feedback-loop-system.md` - Human review triggers and continuous improvement
- **Investigation Protocol**: Complete methodology for JIRA + GitHub + Internet research
- **Post-Generation Linting**: Automated validation with `post_generation_linter.sh`

## 🌐 AI Test Generation Suite Integration

### Part of Enterprise Platform

This **Intelligent Test Analysis Engine** is part of the broader **AI Test Generation Suite** with unified command interface and multiple specialized applications.

### Suite Applications

| Application | Purpose | Best For |
|------------|---------|----------|
| **Intelligent Test Analysis Engine** (This App) | AI-powered test generation | E2E test plans, smart scoping, environment assessment |
| **Z-Stream Analysis Engine** | Jenkins pipeline analysis | CI/CD troubleshooting, pipeline failure diagnosis |

### Unified Command Interface

All applications are accessible via **global slash commands** from anywhere in the repository:

```bash
# Test generation (routes to this application)
/generate-e2e-test-plan ACM-22079

# Pipeline analysis (routes to Z-Stream Analysis)
/analyze-pipeline-failures clc-e2e-pipeline-3223

# Intelligent workflow routing
/analyze-workflow test-plan ACM-22079
/analyze-workflow pipeline-failure pipeline-3223
```

### Application Independence

- **Standalone Operation**: Each app works independently
- **Specialized Configuration**: Individual CLAUDE.md configs for advanced features
- **Dedicated Workspaces**: Separate working directories and state
- **Flexible Usage**: Use unified commands OR navigate to apps for advanced features

### Workflow Integration

**Pattern 1: Quick Analysis**
```bash
# Single command for immediate results
/generate-e2e-test-plan ACM-22079
```

**Pattern 2: Advanced Features**
```bash
# Use global command, then access advanced features
/generate-e2e-test-plan ACM-22079
cd apps/claude-test-generator
# Access specialized Claude config and advanced tools
```

## 📁 Project Structure

```
ai-test-generation-suite/
├── 📄 CLAUDE.md                           # Global unified commands
├── 📁 apps/
│   ├── 🎯 claude-test-generator/           # This Application
│   │   ├── 📄 README.md                  # This file
│   │   ├── 📄 CLAUDE.md                  # Specialized Claude config
│   │   ├── 📁 .claude/                   # Framework configuration
│   │   │   ├── prompts/               # Test scoping and generation rules
│   │   │   ├── templates/             # Output format templates
│   │   │   ├── workflows/             # Feedback loop and process definitions
│   │   │   └── greetings/             # Welcome messages
│   │   ├── 📁 bin/                       # Production tools & scripts
│   │   │   ├── setup_clc              # Environment setup
│   │   │   ├── login_oc               # OpenShift authentication
│   │   │   ├── github-investigation.sh # PR discovery & analysis
│   │   │   ├── doc-investigation.sh   # JIRA hierarchy analysis
│   │   │   ├── post_generation_linter.sh # Output validation
│   │   │   ├── cc_schema_helper.sh    # ClusterCurator schema helper
│   │   │   ├── resource_schema_helper.sh # Generic CRD helper
│   │   │   └── inject_required_keys.sh # YAML field injection
│   │   ├── 📁 runs/                     # Generated test runs by ticket
│   │   │   └── <TICKET-ID>/           # Organized by JIRA ticket
│   │   │       ├── run-XXX-YYYYMMDD-HHMM/ # Timestamped executions
│   │   │       │   ├── Test-Cases.md      # Clean test cases
│   │   │       │   ├── Complete-Analysis.md # Full analysis
│   │   │       │   └── metadata.json      # Run metadata & quality metrics
│   │   │       └── latest -> run-XXX      # Symlink to latest run
│   │   ├── 📁 examples/                 # Example outputs
│   │   └── 📁 docs/                     # Application documentation
│   └── 📉 z-stream-analysis/              # Pipeline Analysis Engine
├── 📁 docs/                              # Shared documentation
├── 📁 JIRA-details/                      # Shared JIRA analysis
└── 📁 e2e-test-generated/                # Legacy test outputs
```

## Best Practices

### Input Optimization
1. **Clear JIRA Details**: Ensure tickets have acceptance criteria and complete descriptions
2. **Environment Access**: Verify cluster connectivity before running analysis
3. **Feature Context**: Understand whether feature is deployed in target environment

### Output Usage
1. **Review Generated Plans**: Always validate AI-generated test cases for accuracy
2. **Adapt to Environment**: Modify generic commands for your specific cluster setup
3. **Execute Systematically**: Follow test cases in order for proper validation flow

### Quality Assurance
1. **Check Deployment Status**: Verify if features are available before manual testing
2. **Validate Expected Outputs**: Ensure expected results match actual environment behavior
3. **Provide Feedback**: Use feedback loop system to improve future generations

## Getting Support

### Documentation
- **Quick Start**: See `docs/quick-start.md` for detailed setup guidance
- **Configuration**: Check `.claude/` directory for customization options
- **Examples**: Review `examples/` for sample outputs and patterns

### Troubleshooting
- **Environment Issues**: Verify cluster access and tool availability
- **Output Quality**: Check JIRA ticket completeness and feature deployment status
- **Framework Errors**: Review metadata.json for execution details and error logs

---

**Framework Version**: 1.0  
**Maintained by**: ACM QE Team  
**Integrations**: Claude Code AI, GitHub, JIRA, OpenShift CLI