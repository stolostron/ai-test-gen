# AI Test Generation Suite 🤖

> **Professional AI-powered test generation framework for enterprise QE teams**

A collection of AI-powered applications designed to automate test plan generation and implementation across multiple testing frameworks and environments.

## 🏗️ Project Structure

```
ai_systems/
├── 📁 apps/                           # Self-contained applications
│   ├── 📁 claude-test-generator/      # AI-powered test analysis engine
│   └── 📁 z-stream-analysis/          # Z-stream pipeline failure analysis engine
├── 📁 docs/                           # Shared documentation and guides
├── 📄 CLAUDE.md                      # Global Claude configuration
├── 📄 README.md                      # This file
└── 📄 OWNERS                         # Project maintainers
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

### 2. Z-Stream Analysis Engine 🔍
**Location**: [`apps/z-stream-analysis/`](./apps/z-stream-analysis/)

**Purpose**: AI-powered Jenkins pipeline failure analysis with intelligent root cause detection and automation fix generation.

**Best For**:
- Jenkins pipeline failure analysis
- CI/CD debugging and troubleshooting
- Automated root cause identification
- Infrastructure and automation issue resolution

**Quick Start**:
```bash
cd apps/z-stream-analysis
# Use Claude slash commands for pipeline analysis
```

## 🎯 Choosing the Right Application

| Feature | Intelligent Test Analysis Engine | Z-Stream Analysis Engine |
|---------|----------------------------------|--------------------------|
| **Approach** | AI-powered test intelligence | AI-powered failure analysis |
| **Setup Time** | Minutes | Minutes |
| **Input Required** | JIRA ticket ID | Jenkins pipeline URL |
| **AI Integration** | Claude-based analysis | Claude-based analysis |
| **Focus** | E2E test generation | Pipeline failure diagnosis |
| **Learning** | Feedback loops | Pattern recognition |
| **Validation** | Environment assessment | Root cause validation |
| **Best For** | Production test plans | CI/CD troubleshooting |

## 🔧 Global Configuration

### Claude Code Integration

The repository provides **global Claude slash commands** via the root `CLAUDE.md`:

#### Available Commands:
- `/generate-e2e-test-plan` - Generate formal E2E test plans
- `/analyze-workflow` - Comprehensive JIRA and PR analysis

#### Usage:
```bash
# Global slash command (works anywhere in the repo)
/generate-e2e-test-plan {PR_URL} {FEATURE_NAME} [JIRA_KEY]

# Application-specific workflows
cd apps/claude-test-generator # For AI-powered test intelligence
cd apps/z-stream-analysis     # For pipeline failure analysis
```

## 📋 Prerequisites

### Shared Requirements
- **Claude Code CLI** configured and authenticated
- **GitHub access** to relevant repositories
- **JIRA CLI** for ticket analysis (intelligent framework)
- **Git** for repository operations

### Application-Specific
- **Intelligent Test Analysis Engine**: Claude Code CLI and ACM cluster access
- **Z-Stream Analysis Engine**: Jenkins access and pipeline URLs

## 🚀 Quick Start Guide

### 1. Choose Your Application
```bash
# For AI-powered test intelligence and E2E generation
cd apps/claude-test-generator

# For pipeline failure analysis and CI/CD troubleshooting
cd apps/z-stream-analysis
```

### 2. Follow Application README
Each application has its own comprehensive setup and usage guide:
- [Intelligent Test Analysis Engine README](./apps/claude-test-generator/README.md)
- [Z-Stream Analysis Engine README](./apps/z-stream-analysis/README.md)

### 3. Use Global Commands
The root CLAUDE.md provides slash commands that work across the entire repository for common workflows.

## 📊 Success Metrics

### Intelligent Test Analysis Engine
- **Setup Time**: < 5 minutes
- **Test Generation**: 30 minutes → 5 minutes (83% reduction)
- **Quality**: Production-ready E2E test plans with environment assessment
- **Best For**: AI-powered test intelligence, smart scoping, continuous improvement

### Z-Stream Analysis Engine
- **Setup Time**: < 5 minutes
- **Failure Analysis**: 1-2 hours → 10 minutes (90% reduction)
- **Quality**: Intelligent root cause detection with automated fix recommendations
- **Best For**: Jenkins pipeline troubleshooting, CI/CD failure resolution

## 🤝 Contributing

### Project Structure Guidelines
1. **Applications are self-contained** - each app should work independently
2. **Shared resources** go in root-level directories (`docs/`)
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

### Application Documentation
- **[Intelligent Test Analysis Engine](./apps/claude-test-generator/)**: AI-powered test intelligence docs
- **[Z-Stream Analysis Engine](./apps/z-stream-analysis/)**: Pipeline failure analysis docs

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
- 🔍 **Pipeline Failure Analysis**: Use Z-Stream Analysis Engine
- 🔄 **Both**: Use applications together for comprehensive QE coverage

---

**Repository Maintainers**: ACM QE Team  
**Latest Update**: January 2025  
**License**: Internal Use  
**Status**: Production Ready

**Get Started**: Choose an application in [`apps/`](./apps/) and follow its README.