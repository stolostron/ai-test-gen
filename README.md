# AI Systems - Modular QE Automation Suite 🤖

> **Enterprise-grade AI-powered tools for QE teams working with Kubernetes and OpenShift**

A modular collection of independent AI applications that automate complex QE workflows. Each app solves specific problems while being completely self-contained and extensible.

## 🚀 Quick Start - Try It Now

**🌟 Intelligent Routing**: Work from anywhere in the repo! Claude automatically routes your requests to the right specialized app.

### Generate ACM Test Plans
```bash
"Analyze ACM-22079"
# → claude-test-generator V3.0 | 5-10 min analysis | saves to apps/claude-test-generator/runs/

/generate-e2e-test-plan https://github.com/org/repo/pull/123 "Feature Name" ACM-10659
# → Full E2E test plan with deployment validation
```

### Analyze Jenkins Pipeline Failures
```bash
"Analyze pipeline failure: https://jenkins.example.com/job/build/123"
# → z-stream-analysis | Root cause + fix recommendations | saves to apps/z-stream-analysis/runs/

/analyze-workflow https://jenkins.example.com/job/build/123 "failure-analysis"
# → Detailed investigation with automated suggestions
```

## 🏗️ Applications

### 1. **Intelligent Test Analysis Engine** 🎯
**Location**: [`apps/claude-test-generator/`](./apps/claude-test-generator/)

**What it does**: Automatically creates production-ready E2E test plans by analyzing JIRA tickets, GitHub PRs, and deployment status using AI.

**Key Features**:
- ✅ **5-10 minute analysis** (vs 2-4 hours manual)
- ✅ **AI investigates everything**: JIRA hierarchy, GitHub PRs, deployment status
- ✅ **Smart test scoping**: Only tests NEW functionality
- ✅ **Copy-paste ready**: Terminal commands with realistic sample outputs
- ✅ **Evidence-based validation**: Concrete deployment status assessment

**Perfect for**: ACM QE engineers who need reliable, comprehensive test plans for feature development.

**Quick Demo**:
```bash
"Analyze ACM-22079"
# → 3-5 comprehensive E2E test scenarios with deployment validation
```

### 2. **Z-Stream Analysis Engine** 🔍
**Location**: [`apps/z-stream-analysis/`](./apps/z-stream-analysis/)

**What it does**: AI-powered Jenkins pipeline failure analysis with intelligent root cause detection and automation fix recommendations.

**Key Features**:
- ✅ **90% time reduction** (2 hours → 10 minutes)
- ✅ **Root cause identification** with concrete evidence
- ✅ **Automated fix suggestions** for common CI/CD issues
- ✅ **Pattern recognition** across pipeline failures

**Perfect for**: DevOps and QE teams troubleshooting Jenkins pipeline failures and CI/CD issues.

## 🎯 Which App Should I Use?

| Your Need | Use This App | Example |
|-----------|--------------|---------|
| **Test ACM features** | `claude-test-generator` | Analyze JIRA ticket for new ACM functionality |
| **Debug Jenkins failures** | `z-stream-analysis` | Pipeline failed, need root cause analysis |
| **Validate deployments** | `claude-test-generator` | Check if feature is actually deployed |
| **Fix CI/CD issues** | `z-stream-analysis` | Automation scripts breaking, need fixes |

## 🌟 Why This Architecture?

### 🎯 **Intelligent Routing** - Work from Anywhere
- **Stay in root directory** - no need to navigate between apps
- **Natural language commands** - just describe what you want
- **Smart app selection** - Claude automatically chooses the right tool
- **Full app capabilities** - get all specialized features without the complexity

### Modular & Independent
- **Each app works alone** - no cross-dependencies
- **Easy to extend** - add new apps without affecting existing ones
- **Simple maintenance** - update one app without touching others
- **Team flexibility** - different teams can own different apps

### Claude AI Integration Layers
```
🌐 Global CLAUDE.md (root)     # Smart dispatcher + universal commands
├── 🎯 claude-test-generator   # V3.0 enterprise AI services
└── 🔍 z-stream-analysis       # Pipeline failure expertise
```

### Real-World Benefits
- **Zero friction**: Work from anywhere in the repo
- **Fast onboarding**: Jump into any workflow in seconds
- **Focused expertise**: Each app masters its domain while staying accessible
- **Easy scaling**: Add more apps that integrate seamlessly
- **No cognitive overhead**: Focus on your problem, not navigation

## 🚀 Getting Started

### Prerequisites
- **Claude Code CLI** configured and authenticated
- **GitHub access** to relevant repositories (if not public)
- **kubectl/oc** for cluster operations (test generator)
- **JIRA access** for ticket analysis (test generator)

### 2-Step Setup
1. **Clone the repo** 
2. **Ask Claude** to perform your task using natural language

### Available Commands
```bash
# Natural language (recommended)
"Analyze ACM-22079"
"Analyze pipeline failure: [JENKINS_URL]"

# Explicit global commands
/generate-e2e-test-plan {PR_URL} {FEATURE_NAME} [JIRA_KEY]
/analyze-workflow {TARGET_URL} {ACTION_TYPE} [CONTEXT]
```


## 📚 Learn More

| Resource | Description |
|----------|-------------|
| **[claude-test-generator README](./apps/claude-test-generator/README.md)** | Complete guide for ACM test generation |
| **[z-stream-analysis README](./apps/z-stream-analysis/README.md)** | Pipeline failure analysis documentation |
| **[docs/](./docs/)** | Shared documentation and advanced guides |
| **[Project Structure Guide](./docs/project-structure.md)** | Architecture and extension patterns |

## 🔮 Extensibility - Add Your Own Apps

### The Vision
This architecture makes it **trivial to add new AI-powered QE tools**. Each app is completely independent, so you can:

1. **Create a new app directory** under `apps/`
2. **Add your own CLAUDE.md** with specialized prompts
3. **Build domain-specific functionality** 
4. **Leverage Claude AI** for your use case

### Example Future Apps We Could Add

#### ACM Security Testing Suite
```bash
apps/acm-security-scanner/
├── CLAUDE.md              # Security-focused prompts
├── README.md              # Security testing workflows  
└── templates/             # CVE analysis templates
```
**Use case**: Automated security vulnerability scanning, CVE analysis, compliance testing

#### Performance Baseline Generator  
```bash
apps/performance-baseline/
├── CLAUDE.md              # Performance analysis prompts
├── scripts/               # Load testing automation
└── baselines/             # Historical performance data
```
**Use case**: Generate performance baselines, detect regressions, capacity planning

#### Documentation Assistant
```bash
apps/docs-generator/
├── CLAUDE.md              # Documentation generation prompts
├── templates/             # Doc templates for features  
└── outputs/               # Generated documentation
```
**Use case**: Auto-generate feature docs, API documentation, troubleshooting guides

#### Multi-Cloud Test Orchestrator
```bash
apps/multi-cloud-testing/
├── CLAUDE.md              # Cloud-specific testing prompts
├── providers/             # AWS, Azure, GCP configurations
└── scenarios/             # Cross-cloud test scenarios
```
**Use case**: Test ACM across different cloud providers, hybrid scenarios

### How to Extend

1. **Copy existing app structure** as a template
2. **Customize CLAUDE.md** for your domain
3. **Add your specific tools** and configurations  
4. **Update root README.md** to include your app
5. **Share with the team!**

### Benefits of This Pattern
- ✅ **Zero conflicts** - apps don't interfere with each other
- ✅ **Easy experimentation** - try new ideas without risk
- ✅ **Team ownership** - different teams can own different apps
- ✅ **Gradual adoption** - teams adopt apps at their own pace

## 📊 Current Results

| App | Time Saved | Quality Improvement | Adoption |
|-----|------------|-------------------|----------|
| **claude-test-generator** | 83% (4hrs → 40min) | Production-ready test plans | Active use |
| **z-stream-analysis** | 90% (2hrs → 12min) | Automated root cause analysis | Active use |

**Ready to add your own app?** See [`docs/project-structure.md`](./docs/project-structure.md) for detailed guidelines.

---

**🎯 Get Started**: Choose an app in [`apps/`](./apps/) and start automating your QE workflows!