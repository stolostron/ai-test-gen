# AI Test Generation Suite 🤖

> **Professional AI-powered test generation framework for enterprise QE teams**

A collection of AI-powered applications designed to automate test plan generation and implementation across multiple testing frameworks and environments.

## 🏗️ Project Structure

```
ai-test-gen_org/
├── 📁 apps/                                    # Self-contained applications
│   ├── 📁 claude-test-generator/               # AI-powered test analysis engine
│   ├── 📁 z-stream-analysis/                   # Z-stream pipeline analysis
│   └── 📁 intelligent-test-framework [old]/    # Legacy test framework (archived)
├── 📁 docs/                                    # Shared documentation
├── 📁 e2e-test-generated/                     # Legacy generated tests
├── 📁 JIRA-details/                           # JIRA ticket analysis
├── 📄 CLAUDE.md                               # Global Claude configuration
├── 📄 README.md                               # This file
└── 📄 OWNERS                                  # Project maintainers
```

## 🚀 Applications

### 1. Intelligent Test Analysis Engine 🎯
**Location**: [`apps/claude-test-generator/`](./apps/claude-test-generator/)

**Purpose**: AI-powered test analysis with smart scoping, E2E generation, and production-ready test plans.

**Best For**:
- AI-powered test analysis and E2E generation
- Smart test scoping and environment assessment
- Production-ready test plans with feedback loops
- Continuous improvement and quality optimization

**Quick Start**:
```bash
cd apps/claude-test-generator
# Use Claude slash commands: /generate-e2e-test-plan
```

### 2. Z-Stream Analysis Engine 📊
**Location**: [`apps/z-stream-analysis/`](./apps/z-stream-analysis/)

**Purpose**: Specialized analysis engine for Jenkins pipeline failures and CI/CD troubleshooting.

**Best For**:
- Jenkins pipeline failure analysis
- CI/CD pipeline troubleshooting and optimization
- Test failure pattern recognition
- Build and deployment issue diagnosis

**Quick Start**:
```bash
cd apps/z-stream-analysis
./quick-start.sh
```

### 3. Legacy Test Framework (Archived) 📚
**Location**: [`apps/intelligent-test-framework [old]/`](./apps/intelligent-test-framework%20[old]/)

**Status**: Archived - moved to legacy status. For new projects, use the Intelligent Test Analysis Engine instead.

**Purpose**: Historical comprehensive AI framework (no longer actively maintained).

## 🎯 Choosing the Right Application

| Feature | Intelligent Test Analysis Engine | Z-Stream Analysis Engine | Legacy Test Framework |
|---------|----------------------------------|--------------------------|----------------------|
| **Approach** | AI-powered test intelligence | Pipeline failure analysis | Multi-repository automation (archived) |
| **Setup Time** | Minutes | < 10 minutes | ~30 minutes |
| **Input Required** | JIRA ticket ID | Jenkins pipeline URL | JIRA ticket ID + codebase |
| **AI Integration** | Claude-based analysis | AI failure classification | Shell-script workflows |
| **Focus** | E2E test generation | CI/CD troubleshooting | Multi-component analysis |
| **Learning** | Feedback loops | Pattern recognition | Adaptive patterns |
| **Validation** | Environment assessment | Pipeline diagnostics | Automated validation |
| **Best For** | Production test plans | Pipeline debugging | Historical reference only |

## 🔧 Global Configuration

### Claude Code Integration

The repository provides **global Claude slash commands** via the root `CLAUDE.md`:

#### Available Commands:
- `/generate-e2e-test-plan` - Generate formal E2E test plans
- `/analyze-workflow` - Comprehensive JIRA and PR analysis

#### Usage:
```bash
# Global slash command (works anywhere in the repo)
/generate-e2e-test-plan {PR_URL} {FEATURE_NAME} [JIRA_FILE]

# Application-specific workflows
cd apps/claude-test-generator      # For AI-powered test intelligence
cd apps/z-stream-analysis          # For pipeline failure analysis
```

## 📋 Prerequisites

### Shared Requirements
- **Claude Code CLI** configured and authenticated
- **GitHub access** to relevant repositories
- **JIRA CLI** for ticket analysis (intelligent framework)
- **Git** for repository operations

### Application-Specific
- **Intelligent Test Analysis Engine**: Claude Code CLI and ACM cluster access
- **Z-Stream Analysis Engine**: Jenkins API access, Python 3.8+, optional Claude CLI
- **Legacy Test Framework**: OpenShift/Kubernetes access, additional CLI tools (archived)

## 🚀 Quick Start Guide

### 1. Choose Your Application
```bash
# For AI-powered test intelligence and E2E generation
cd apps/claude-test-generator

# For Jenkins pipeline failure analysis and CI/CD troubleshooting
cd apps/z-stream-analysis

# For legacy framework reference (archived)
cd apps/intelligent-test-framework\ [old]
```

### 2. Follow Application README
Each application has its own comprehensive setup and usage guide:
- [Intelligent Test Analysis Engine README](./apps/claude-test-generator/README.md)
- [Z-Stream Analysis Engine README](./apps/z-stream-analysis/README.md)
- [Legacy Test Framework README](./apps/intelligent-test-framework%20[old]/README.md) (archived)

### 3. Use Global Commands
The root CLAUDE.md provides slash commands that work across the entire repository for common workflows.

## 📊 Success Metrics

### Intelligent Test Analysis Engine
- **Setup Time**: < 5 minutes
- **Test Generation**: 30 minutes → 5 minutes (83% reduction)
- **Quality**: Production-ready E2E test plans with environment assessment
- **Best For**: AI-powered test intelligence, smart scoping, continuous improvement

### Z-Stream Analysis Engine
- **Setup Time**: < 10 minutes
- **Pipeline Analysis**: Manual debugging → 5 minutes (95% reduction)
- **Failure Classification**: Hours → Minutes with AI insights
- **Best For**: CI/CD troubleshooting, Jenkins pipeline optimization, test failure patterns

### Legacy Test Framework (Archived)
- **Setup Time**: ~30 minutes (one-time)
- **Test Planning**: 2 hours → 15 minutes (87% reduction)
- **Implementation**: 1 day → 2 hours (75% reduction)
- **Status**: No longer actively maintained - use Claude Test Generator instead

## 🤝 Contributing

### Project Structure Guidelines
1. **Applications are self-contained** - each app should work independently
2. **Shared resources** go in root-level directories (`docs/`, `JIRA-details/`)
3. **Global configurations** in root `CLAUDE.md`
4. **App-specific configs** in each app's directory

### Development Workflow
```bash
# Fork and clone
git clone https://github.com/YOUR-USERNAME/ai-test-gen.git
cd ai-test-gen_org

# Work on specific application
cd apps/[application-name]

# Make changes and test
# ... development work ...

# Commit and push
git add .
git commit -m "feat(app-name): description"
git push origin feature-branch
```

## 📚 Documentation

### Global Documentation
- **[Root CLAUDE.md](./CLAUDE.md)**: Global slash commands and workflows
- **[Project docs/](./docs/)**: Shared documentation and guides
- **[JIRA Details](./JIRA-details/)**: Ticket analysis examples

### Application Documentation
- **[Intelligent Test Analysis Engine](./apps/claude-test-generator/)**: AI-powered test intelligence docs
- **[Z-Stream Analysis Engine](./apps/z-stream-analysis/)**: Jenkins pipeline analysis and CI/CD troubleshooting docs
- **[Legacy Test Framework](./apps/intelligent-test-framework%20[old]/)**: Multi-repository automation docs (archived)

## 🛣️ Roadmap

### Phase 1: ✅ Structure Organization (Current)
- Separate applications into clean, self-contained modules
- Professional project structure
- Clear documentation hierarchy

### Phase 2: Integration Enhancement (Q1 2025)
- Cross-application workflows
- Shared learning between applications
- Unified reporting and metrics

### Phase 3: Advanced Features (Q2+ 2025)
- Multi-language support
- Custom AI model training
- Enterprise dashboard and analytics

## 🎯 Support & Community

### Getting Help
- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Comprehensive guides in each application
- **Community**: Team Slack channels for discussions

### Professional Support
- **Enterprise Setup**: Contact maintainers for team onboarding
- **Custom Integrations**: Available for enterprise requirements
- **Training**: Workshops and training sessions available

---

## 🏢 Enterprise Ready

This suite is designed for **professional QE teams** working on complex enterprise software. Each application serves different needs while maintaining consistency and quality standards.

**Choose your path**:
- 🎯 **AI-Powered Test Intelligence**: Use Intelligent Test Analysis Engine
- 📊 **Pipeline Failure Analysis**: Use Z-Stream Analysis Engine  
- 🧠 **Legacy Reference**: Use archived Intelligent Test Framework (historical)
- 🔄 **Multiple Tools**: Use applications together for comprehensive coverage

---

**Repository Maintainers**: ACM QE Team  
**Latest Update**: January 2025  
**License**: Internal Use  
**Status**: Production Ready

**Get Started**: Choose an application in [`apps/`](./apps/) and follow its README.