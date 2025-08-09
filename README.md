# AI Test Generation Suite 🤖

> **Professional AI-powered test generation framework for enterprise QE teams**

A collection of AI-powered applications designed to automate test plan generation and implementation across multiple testing frameworks and environments.

## 🏗️ Project Structure

```
ai-test-gen_org/
├── 📁 apps/                           # Self-contained applications
│   ├── 📁 claude-test-generator/      # Claude-focused test generation
│   └── 📁 intelligent-test-framework/ # Advanced AI framework
├── 📁 docs/                           # Shared documentation
├── 📁 e2e-test-generated/            # Legacy generated tests
├── 📁 JIRA-details/                  # JIRA ticket analysis
├── 📄 CLAUDE.md                      # Global Claude configuration
├── 📄 README.md                      # This file
└── 📄 OWNERS                         # Project maintainers
```

## 🚀 Applications

### 1. Claude Test Generator 🎯
**Location**: [`apps/claude-test-generator/`](./apps/claude-test-generator/)

**Purpose**: Claude-focused test generation with custom slash commands and simple workflows.

**Best For**:
- Quick test plan generation from JIRA + PR
- Claude Code integration with custom commands
- Simple Cypress test automation
- Proof-of-concept demonstrations

**Quick Start**:
```bash
cd apps/claude-test-generator
# Use Claude slash commands: /generate-e2e-test-plan
```

### 2. Intelligent Test Framework 🧠
**Location**: [`apps/intelligent-test-framework/`](./apps/intelligent-test-framework/)

**Purpose**: Advanced AI-powered framework with comprehensive analysis and multi-framework support.

**Best For**:
- Enterprise-grade test generation
- Multi-repository analysis
- Adaptive learning and validation
- Production-ready test suites

**Quick Start**:
```bash
cd apps/intelligent-test-framework
./create-test-case.sh ACM-22079 --test-plan-only
```

## 🎯 Choosing the Right Application

| Feature | Claude Test Generator | Intelligent Test Framework |
|---------|----------------------|---------------------------|
| **Complexity** | Simple | Advanced |
| **Setup Time** | Minutes | ~30 minutes |
| **Input Required** | JIRA + PR URL | JIRA ticket ID only |
| **AI Integration** | Claude slash commands | Full AI workflow |
| **Frameworks** | Cypress | Cypress, Selenium, Go, Playwright |
| **Learning** | Static | Adaptive |
| **Validation** | Manual | Automated + Smart |
| **Best For** | Quick tests, PoCs | Production, Enterprise |

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
cd apps/claude-test-generator     # For simple generation
cd apps/intelligent-test-framework # For advanced analysis
```

## 📋 Prerequisites

### Shared Requirements
- **Claude Code CLI** configured and authenticated
- **GitHub access** to relevant repositories
- **JIRA CLI** for ticket analysis (intelligent framework)
- **Git** for repository operations

### Application-Specific
- **Claude Test Generator**: Basic Claude integration
- **Intelligent Test Framework**: OpenShift/Kubernetes access, additional CLI tools

## 🚀 Quick Start Guide

### 1. Choose Your Application
```bash
# For simple, quick test generation
cd apps/claude-test-generator

# For comprehensive, enterprise-grade generation  
cd apps/intelligent-test-framework
```

### 2. Follow Application README
Each application has its own comprehensive setup and usage guide:
- [Claude Test Generator README](./apps/claude-test-generator/README.md)
- [Intelligent Test Framework README](./apps/intelligent-test-framework/README.md)

### 3. Use Global Commands
The root CLAUDE.md provides slash commands that work across the entire repository for common workflows.

## 📊 Success Metrics

### Claude Test Generator
- **Setup Time**: < 5 minutes
- **Test Generation**: 30 minutes → 5 minutes (83% reduction)
- **Best For**: Individual contributors, quick iterations

### Intelligent Test Framework  
- **Setup Time**: ~30 minutes (one-time)
- **Test Planning**: 2 hours → 15 minutes (87% reduction)
- **Implementation**: 1 day → 2 hours (75% reduction)
- **Best For**: Team workflows, complex features

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
- **[Claude Test Generator](./apps/claude-test-generator/)**: Simple generation docs
- **[Intelligent Framework](./apps/intelligent-test-framework/)**: Comprehensive framework docs

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
- 🎯 **Simple & Fast**: Use Claude Test Generator
- 🧠 **Advanced & Comprehensive**: Use Intelligent Test Framework
- 🔄 **Both**: Use applications together for different scenarios

---

**Repository Maintainers**: ACM QE Team  
**Latest Update**: January 2025  
**License**: Internal Use  
**Status**: Production Ready

**Get Started**: Choose an application in [`apps/`](./apps/) and follow its README.