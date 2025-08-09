# Claude Test Generator 🎯

> **Simple, Claude-focused test generation for quick workflows**

A lightweight application designed for rapid test plan generation using Claude Code integration with custom slash commands and straightforward workflows.

## 🎯 Purpose

Perfect for QE engineers who need **quick, simple test generation** without the complexity of advanced AI frameworks. Ideal for:

- ✅ **Rapid prototyping** of test plans
- ✅ **Individual contributor workflows**
- ✅ **Proof-of-concept demonstrations**
- ✅ **Learning AI test generation concepts**
- ✅ **Simple JIRA + PR analysis**

## 🚀 Quick Start

### 1. Prerequisites
- Claude Code CLI configured and authenticated
- Access to GitHub repositories
- Basic familiarity with JIRA tickets and PRs

### 2. Basic Usage
```bash
# Navigate to the app
cd apps/claude-test-generator

# Use Claude slash commands (available globally)
/generate-e2e-test-plan https://github.com/repo/pull/123 "Feature Name"

# Or analyze existing JIRA details
/generate-e2e-test-plan https://github.com/repo/pull/123 "Feature Name" ACM-10659.txt
```

## 📋 Generated Test Plans

This application generates clean, table-format test plans optimized for **Polarion import** and **manual execution**.

### Example Output Format

```markdown
### Test Case: Implement Custom Labels for ClusterCurator Job Pods

| Step | Expected Result |
|------|-----------------|
| 1. Create ClusterCurator with custom labels in annotations | ClusterCurator resource created successfully |
| 2. Verify Job pod inherits custom labels: `oc get pods -l job-name=clustercurator-job -o jsonpath='{.items[0].metadata.labels}'` | Pod shows custom labels from ClusterCurator annotations |
| 3. Validate label propagation across multiple job executions | All subsequent Job pods inherit the same custom labels |
```

### Output Locations
- **Generated Plans**: `e2e-test-generated/`
- **JIRA Analysis**: `JIRA-details/` (if using JIRA files)
- **Documentation**: This directory

## 🔧 Features

### ✨ Core Capabilities
- **Claude Slash Commands**: Pre-configured workflows for common scenarios
- **JIRA Integration**: Read ticket details from local files
- **PR Analysis**: Extract test requirements from GitHub pull requests
- **Table Format**: Human-readable test plans ready for Polarion
- **Quick Iteration**: Fast generation for rapid feedback cycles

### 📊 Supported Workflows
1. **JIRA + PR → Test Plan**: Primary workflow for feature testing
2. **PR Analysis Only**: When JIRA details are embedded in PR
3. **Manual Review**: Generated plans optimized for human validation

## 🎛️ Claude Configuration

This app includes its own `CLAUDE.md` with specific configurations:

### Available Commands
- `/generate-e2e-test-plan` - Core test plan generation
- `/analyze-workflow` - General workflow analysis

### Configuration Features
- **Pre-built prompts** for common ACM testing scenarios
- **Output format templates** for consistent results
- **Integration patterns** for JIRA and GitHub workflows

## 📂 Project Structure

```
claude-test-generator/
├── 📄 README.md                    # This file
├── 📄 CLAUDE.md                    # App-specific Claude config
├── 📁 src/                         # Source files and utilities
├── 📁 docs/                        # Application documentation
└── 📁 examples/                    # Example generated tests
```

## 🔄 Workflow Examples

### Scenario 1: New Feature Test Plan
```bash
# Input: JIRA ticket + GitHub PR
/generate-e2e-test-plan https://github.com/stolostron/repo/pull/203 "Custom Labels Feature"

# Output: Clean test plan table in e2e-test-generated/
# Time: ~5 minutes vs 30+ minutes manual
```

### Scenario 2: Bug Fix Validation  
```bash
# Input: Bug fix PR with acceptance criteria
/analyze-workflow https://github.com/stolostron/repo/pull/204 "test-plan"

# Output: Focused test scenarios for regression validation
# Time: ~3 minutes vs 15+ minutes manual
```

### Scenario 3: Documentation Review
```bash
# Input: JIRA details file + analysis type
/analyze-workflow https://github.com/repo/pull/203 "documentation" ACM-12345.txt

# Output: Documentation gaps and test coverage analysis
```

## 📊 Success Metrics

### Time Savings
- **Test Plan Creation**: 30 minutes → 5 minutes (83% reduction)
- **PR Analysis**: 15 minutes → 3 minutes (80% reduction)
- **Quick Iteration**: Multiple plans in minutes vs hours

### Quality Benefits  
- **Consistent Format**: Standardized table format for all plans
- **Complete Coverage**: AI identifies scenarios often missed manually
- **Ready for Import**: Direct compatibility with Polarion and test management tools

## 🎯 Best Practices

### Input Optimization
1. **Clear PR Descriptions**: Better PR descriptions = better test plans
2. **Complete JIRA Details**: Include acceptance criteria in JIRA files
3. **Specific Feature Names**: Use descriptive names for better output file naming

### Output Usage
1. **Review Generated Plans**: Always review AI-generated content
2. **Customize for Environment**: Adapt commands for your specific cluster setup
3. **Iterate Quickly**: Use fast generation for multiple approaches

### Integration Workflow
1. **Start Simple**: Begin with this app for quick wins
2. **Scale Up**: Move to Intelligent Test Framework for complex features
3. **Combine Approaches**: Use both apps for different scenarios

## 🔗 Integration with Intelligent Framework

This app works alongside the **Intelligent Test Framework** for complete coverage:

| Use Case | Claude Test Generator | Intelligent Framework |
|----------|----------------------|---------------------|
| **Quick Test Plans** | ✅ Perfect | ❌ Overkill |
| **Simple PRs** | ✅ Ideal | ❌ Too complex |
| **Learning** | ✅ Great starting point | ❌ Steep learning curve |
| **Complex Features** | ❌ Limited analysis | ✅ Comprehensive |
| **Multi-Repository** | ❌ Single PR focus | ✅ Full analysis |
| **Production Testing** | ❌ Manual validation needed | ✅ Automated validation |

## 🚀 Getting Support

### Quick Help
- **Global Commands**: Available from repository root via global CLAUDE.md
- **App Documentation**: This README and local CLAUDE.md
- **Examples**: Check `examples/` directory for patterns

### Community
- **Issues**: Report via GitHub repository issues
- **Discussions**: Team Slack channels for usage patterns
- **Contributions**: Simple improvements welcome via PRs

## 🛣️ Roadmap

### Current Capabilities ✅
- Claude slash command integration
- Basic JIRA + PR analysis
- Table format test plan generation
- Quick iteration workflows

### Near Term (Q1 2025)
- [ ] Enhanced PR analysis patterns
- [ ] Additional output formats (JSON, XML)
- [ ] Integration with test management APIs

### Future Enhancements
- [ ] Basic validation capabilities
- [ ] Simple automation script generation
- [ ] Team collaboration features

---

## 🎯 When to Use This App

**Choose Claude Test Generator when**:
- ✅ You need quick test plans (< 5 minutes)
- ✅ Working with simple feature PRs
- ✅ Learning AI test generation
- ✅ Prototyping test approaches
- ✅ Individual contributor workflows

**Consider Intelligent Framework when**:
- 🔄 Complex multi-component features
- 🔄 Production-ready test suites needed
- 🔄 Advanced validation requirements
- 🔄 Team-wide standardization
- 🔄 Continuous learning and improvement

---

**Application Version**: 1.0  
**Maintained by**: ACM QE Team  
**Compatible with**: Claude Code CLI, GitHub, JIRA  

**Get Started**: `/generate-e2e-test-plan {PR_URL} {FEATURE_NAME}`
