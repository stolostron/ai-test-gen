# Claude Configuration - AI Test Generation Suite

> **Enterprise-grade AI-powered test generation and analysis platform with unified command interface**

## 🎯 Universal Application Control

These commands work from anywhere in the repository and provide streamlined access to all applications while maintaining their independence. Each command intelligently routes to the appropriate application based on your needs.

### /generate-e2e-test-plan
**Application:** Intelligent Test Analysis Engine  
**Description:** Generate comprehensive E2E test plans with AI-powered analysis and smart scoping.

**Usage:** 
```
/generate-e2e-test-plan {JIRA_TICKET} [OPTIONS]
/generate-e2e-test-plan {PR_URL} {FEATURE_NAME} [JIRA_SOURCE]
```

**Examples:**
```bash
# JIRA-based generation
/generate-e2e-test-plan ACM-22079

# PR-based generation with JIRA context
/generate-e2e-test-plan https://github.com/stolostron/cluster-curator-controller/pull/203 "Implement pushing custom labels to pods" ACM-10659.txt

# With custom kubeconfig
/generate-e2e-test-plan ACM-22079 --kubeconfig /path/to/your/kubeconfig

# With specific QE environment
/generate-e2e-test-plan ACM-22079 --env qe6
```

**Features:**
- ✅ **Always Deep Analysis**: Comprehensive analysis is the default behavior
- ✅ Smart test scoping (focuses only on changed functionality)
- ✅ **Intelligent Environment Handling**: Auto-detects QE environments or uses custom kubeconfig
- ✅ Production-ready test cases with copy-paste commands
- ✅ Feedback loops and continuous improvement
- ✅ Multiple output formats (analysis + clean test cases)

---

### /analyze-pipeline-failures
**Application:** Z-Stream Analysis Engine  
**Description:** Analyze Jenkins pipeline failures with AI-powered failure classification and troubleshooting.

**Usage:**
```
/analyze-pipeline-failures {JENKINS_URL}
/analyze-pipeline-failures {PIPELINE_ID} [OPTIONS]
```

**Examples:**
```bash
# Analyze specific Jenkins pipeline
/analyze-pipeline-failures https://jenkins.example.com/job/clc-e2e-pipeline/3223/

# Quick pipeline ID analysis
/analyze-pipeline-failures clc-e2e-pipeline-3223

# Comprehensive analysis with artifact extraction
/analyze-pipeline-failures clc-e2e-pipeline-3223 --extract-artifacts

# Pattern analysis across multiple runs
/analyze-pipeline-failures clc-e2e-pipeline-3223 --pattern-analysis
```

**Features:**
- ✅ Automated failure pattern recognition
- ✅ Intelligent test failure classification
- ✅ Root cause analysis with AI insights
- ✅ Jenkins artifact extraction and analysis
- ✅ Comprehensive troubleshooting recommendations

---

### /analyze-workflow
**Application:** Multi-Application Router  
**Description:** Intelligent workflow analysis that routes to the best application based on task type.

**Usage:**
```
/analyze-workflow {TASK_TYPE} {TARGET} [OPTIONS]
```

**Examples:**
```bash
# Test plan generation (routes to Claude Test Generator)
/analyze-workflow test-plan ACM-22079

# Pipeline failure analysis (routes to Z-Stream Analysis)
/analyze-workflow pipeline-failure clc-e2e-pipeline-3223

# Research and documentation (routes to Legacy Framework)
/analyze-workflow research ACM-22079 --comprehensive

# PR and code analysis
/analyze-workflow pr-review https://github.com/stolostron/cluster-curator-controller/pull/203
```

**Task Routing:**
- **test-plan, e2e-test, validation** → Intelligent Test Analysis Engine
- **pipeline-failure, ci-debug, jenkins** → Z-Stream Analysis Engine
- **research, documentation, comprehensive** → Intelligent Test Analysis Engine
- **pr-review, code-analysis** → Auto-detect best application

---

### /quick-start
**Application:** Application Launcher  
**Description:** Quick launcher for any application with guided setup.

**Usage:**
```
/quick-start {APPLICATION} [TASK]
```

**Examples:**
```bash
# Launch Intelligent Test Analysis Engine
/quick-start claude-test-generator

# Start pipeline analysis
/quick-start z-stream-analysis

# Quick test generation
/quick-start test-plan ACM-22079

# Application help
/quick-start help
```

## 🏗️ Available Applications

Each application is fully independent and can be used standalone or via the unified commands above.

### 🎯 Intelligent Test Analysis Engine (Production)
**Location:** `apps/claude-test-generator/`  
**Status:** ✅ Active - Production Ready  
**Claude Config:** `apps/claude-test-generator/CLAUDE.md`

**Purpose:** AI-powered test analysis with smart scoping and production-ready output  
**Best For:**
- E2E test plan generation
- Smart test scoping (only tests what changed)
- Environment assessment and validation
- Production-ready test cases with copy-paste commands
- Feedback loops and continuous improvement

**Quick Start:**
```bash
cd apps/claude-test-generator
# Use specialized Claude config for advanced features
```

---

### 📊 Z-Stream Analysis Engine (Production)
**Location:** `apps/z-stream-analysis/`  
**Status:** ✅ Active - Production Ready  
**Claude Config:** `apps/z-stream-analysis/CLAUDE.md`

**Purpose:** Jenkins pipeline failure analysis and CI/CD troubleshooting  
**Best For:**
- Jenkins pipeline failure analysis
- CI/CD troubleshooting and optimization
- Test failure pattern recognition
- Build and deployment issue diagnosis
- Automated artifact extraction and analysis

**Quick Start:**
```bash
cd apps/z-stream-analysis
./quick-start.sh
```

---


## 🚀 Unified Command Interface

### Command Routing Logic
Commands automatically route to the appropriate application:

| Command Pattern | Routes To | Purpose |
|----------------|-----------|---------|
| `/generate-e2e-test-plan` | Intelligent Test Analysis Engine | E2E test generation with smart scoping |
| `/analyze-pipeline-failures` | Z-Stream Analysis | Jenkins pipeline debugging |
| `/analyze-workflow test-plan` | Intelligent Test Analysis Engine | Intelligent task routing |
| `/analyze-workflow pipeline-failure` | Z-Stream Analysis | Intelligent task routing |
| `/quick-start {app}` | Specified Application | Direct application launch |

### Quick Commands Reference

```bash
# 🎯 TEST GENERATION (Intelligent Test Analysis Engine)
/generate-e2e-test-plan ACM-22079                              # JIRA-based test plan (always deep analysis)
/generate-e2e-test-plan ACM-22079 --env qe6                   # With QE environment
/generate-e2e-test-plan ACM-22079 --kubeconfig /path/to/config # With custom kubeconfig
/analyze-workflow test-plan ACM-22079                     # Via routing

# 📊 PIPELINE ANALYSIS (Z-Stream Analysis Engine)  
/analyze-pipeline-failures clc-e2e-pipeline-3223           # Pipeline debugging
/analyze-pipeline-failures pipeline-3223 --extract-artifacts  # With artifacts
/analyze-workflow pipeline-failure clc-e2e-pipeline-3223   # Via routing

# 🚀 APPLICATION LAUNCHING
/quick-start claude-test-generator              # Launch test generator
/quick-start z-stream-analysis                  # Launch pipeline analyzer
/quick-start help                               # Show all options

# 📂 DIRECT ACCESS (Bypass routing for advanced features)
cd apps/claude-test-generator                   # Advanced test generation
cd apps/z-stream-analysis                       # Advanced pipeline analysis
```

## 📋 Prerequisites & Setup

### Global Requirements
- ✅ **Claude Code CLI** configured and authenticated
- ✅ **GitHub access** to relevant repositories  
- ✅ **Basic CLI tools** (curl, jq, git)

### Application-Specific Requirements
**Intelligent Test Analysis Engine:**
- OpenShift/ACM cluster access (qe6, qe8, qe9, qe10, or custom kubeconfig)
- JIRA CLI access (optional)
- Intelligent environment detection and kubeconfig handling

**Z-Stream Analysis Engine:**
- Jenkins API access
- Python 3.8+ (for advanced analysis)

**Setup Verification:**
```bash
# Check Claude CLI
claude --version

# Check cluster access (for test generation)
oc whoami

# Check repository structure
ls apps/
```

## 🔧 Advanced Usage & Integration

### Application Independence
Each application maintains full independence:
- **Standalone Operation**: Apps work without global commands
- **Independent Configuration**: Each has its own setup and config
- **Isolated Dependencies**: No cross-application dependencies
- **Dedicated Workspaces**: Separate working directories and state

### Workflow Integration Patterns

**Pattern 1: Quick Analysis**
```bash
# Single command for immediate results
/generate-e2e-test-plan ACM-22079
```

**Pattern 2: Deep Dive**
```bash
# Use global command, then switch to app for advanced features
/generate-e2e-test-plan ACM-22079
cd apps/claude-test-generator
# Access advanced Claude config and specialized tools
```

**Pattern 3: Multi-Application Workflow**
```bash
# Generate test plan
/generate-e2e-test-plan ACM-22079

# Analyze related pipeline failures
/analyze-pipeline-failures clc-e2e-pipeline-3223

# Generate comprehensive report combining both
/analyze-workflow comprehensive-report ACM-22079
```

### Error Handling & Fallbacks
- **Application Unavailable**: Commands gracefully degrade to available alternatives
- **Missing Dependencies**: Clear error messages with setup instructions
- **Invalid Routing**: Intelligent suggestions for correct command usage
- **Partial Failures**: Continue with available functionality, report limitations
- **Custom Kubeconfig**: Framework automatically detects and validates kubeconfig paths
- **Environment Issues**: Graceful handling of QE environment access problems

## 📚 Documentation Structure

```
📁 AI Test Generation Suite
├── 📄 CLAUDE.md (this file)                    # Global unified commands
├── 📄 README.md                                # Project overview and application guide
├── 📁 JIRA-details/                            # Shared JIRA ticket analysis
├── 📁 docs/                                    # Shared documentation
├── 📁 e2e-test-generated/                      # Generated test outputs
├── 📁 apps/
│   ├── 📁 claude-test-generator/               # 🎯 Production: Intelligent Test Analysis Engine
│   │   ├── 📄 CLAUDE.md                        # Specialized Claude config
│   │   ├── 📄 README.md                        # Application guide
│   │   └── 📁 runs/                            # Test generation runs
│   └── 📁 z-stream-analysis/                   # 📊 Production: Pipeline Analysis
│       ├── 📄 CLAUDE.md                        # Specialized Claude config
│       ├── 📄 README.md                        # Application guide
│       └── 📁 runs/                            # Analysis runs
```

## 🎯 Getting Started

### For Test Generation
```bash
# Quick start (always includes deep analysis)
/generate-e2e-test-plan ACM-22079

# With QE environment
/generate-e2e-test-plan ACM-22079 --env qe6

# With custom kubeconfig (framework handles gracefully)
/generate-e2e-test-plan ACM-22079 --kubeconfig /path/to/your/cluster/kubeconfig
```

### For Pipeline Analysis
```bash
# Quick start
/analyze-pipeline-failures clc-e2e-pipeline-3223

# Or with artifact extraction
/analyze-pipeline-failures clc-e2e-pipeline-3223 --extract-artifacts
```

### For Help
```bash
/quick-start help
```

---

**🏢 Enterprise-Ready Platform:** This unified interface provides streamlined access to all applications while maintaining their independence and specialized capabilities. Choose the command style that fits your workflow - from quick single commands to deep application-specific analysis.