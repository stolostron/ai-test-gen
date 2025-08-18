# AI Systems Suite - Usage Guide

> **Quick reference for using the isolated multi-app Claude configuration**

## 🚀 Quick Start

### Choose Your Application

#### Test Generator (ACM Test Plans with Real Data)
```bash
cd apps/claude-test-generator/
"Generate test plan for ACM-22079"
```

#### Z-Stream Analysis (Jenkins Failures)
```bash
cd apps/z-stream-analysis/
"Analyze https://jenkins-url/job/pipeline/123/"
```

## 📋 Common Commands

### Test Generator App
```bash
# Navigate to app
cd apps/claude-test-generator/

# Natural language (recommended)
"Analyze ACM-22079"
"Generate test plan for feature X"
"Investigate PR: https://github.com/org/repo/pull/123"

# Direct commands
/analyze ACM-22079
/generate https://github.com/org/repo/pull/123 "Feature Name" ACM-10659

# Output includes real environment data in Expected Results
# Works with any component (ClusterCurator, Policy, Application, etc.)
```

### Z-Stream Analysis App
```bash
# Navigate to app
cd apps/z-stream-analysis/

# Natural language (recommended)
"Analyze https://jenkins-url/job/pipeline/123/"
"Analyze clc-e2e-pipeline-3313"

# Direct commands
/analyze https://jenkins-url/job/pipeline/123/
/investigate clc-e2e-pipeline-3313
```

## 🎯 Global Routing (Alternative)

From the root directory, you can route requests to specific apps:

```bash
# Test generation
/test-generator Generate test plan for ACM-22079

# Z-stream analysis
/z-stream-analysis Analyze https://jenkins-url/job/pipeline/123/
```

## 📁 Results and Output

### Test Generator Results
```
apps/claude-test-generator/runs/
├── ACM-22079_August_18_2025/
│   ├── complete_analysis_report.md
│   ├── test_cases_only.md
│   └── run_metadata.json
```

### Z-Stream Analysis Results
```
apps/z-stream-analysis/runs/
├── clc-e2e-pipeline-3313_20250815_174500/
│   ├── detailed_analysis.md
│   ├── analysis_metadata.json
│   └── jenkins_metadata.json
```

## 🔧 Setup Requirements

### Shared Prerequisites
- Claude Code CLI configured
- Git access to repositories
- Network access for web requests

### App-Specific Requirements

**Test Generator:**
- JIRA access (see `shared/docs/JIRA_API_SETUP.md`)
- kubectl/oc for ACM clusters and real data collection
- Optional: GitHub CLI (`gh`) for enhanced analysis
- Cluster access for real environment data integration

**Z-Stream Analysis:**
- Jenkins URL access
- Optional: Jenkins credentials for private instances
- Optional: Cluster access for environment validation

## 🛡️ Isolation Benefits

### Architecture Benefits
- **Clean Design**: Isolated apps that never interfere with each other
- **No Context Mixing**: Claude never confuses which app you're using
- **Independent Operation**: Each app works without the other
- **Clear Boundaries**: Know exactly which app handles your task
- **Easy Extension**: Add new apps without breaking existing ones
- **Real Data Integration**: Apps collect actual environment data during execution
- **Universal Support**: Framework adapts to any component automatically

## 🔍 Troubleshooting

### If Commands Don't Work
1. **Check Current Directory**: Make sure you're in the right app directory
2. **Verify App Config**: Look for `.app-config` file in the app directory
3. **Check Dependencies**: Review app-specific requirements above

### If Results Aren't Saved
- **Test Generator**: Results save to `apps/claude-test-generator/runs/` with real environment data
- **Z-Stream Analysis**: Results save to `apps/z-stream-analysis/runs/`

### If Apps Seem to Interfere
This shouldn't happen with the isolation architecture! If it does:
1. Check that you're in the correct app directory
2. Verify the app's CLAUDE.md starts with isolation headers
3. Report as a configuration issue

## 📖 Documentation

### Quick References
- **This Guide**: Daily usage patterns and commands
- **Isolation Architecture**: `shared/docs/isolation-architecture.md` - Technical details
- **Extension Guide**: `shared/templates/app-extension-guide.md` - Adding new apps

### App-Specific Documentation
- **Test Generator**: `apps/claude-test-generator/README.md` and `docs/` - Includes real data integration and phase-based architecture
- **Z-Stream Analysis**: `apps/z-stream-analysis/README.md` and `docs/` - Jenkins pipeline analysis and automation

## 💡 Pro Tips

### Efficiency
- **Direct Navigation**: `cd` into app directories for focused work
- **Global Routing**: Use from root for quick one-off requests
- **Natural Language**: More intuitive than remembering exact commands

### Organization
- **One App at a Time**: Focus on one type of work in one app directory
- **Check Results**: Each app saves to its own `runs/` directory
- **Share Setups**: Common setup guides are in `shared/docs/`

### Development
- **App Independence**: Each app works completely on its own
- **Clean Configs**: Focused configuration files for each app
- **Easy Extension**: Follow patterns in existing apps to add new ones
- **Modern Capabilities**: Real data integration, universal component support, professional formatting

---

**The isolated architecture provides clean, predictable, and powerful AI-powered QE automation with real environment data integration, without complexity or conflicts.**