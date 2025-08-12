# Quick Start Guide

## 🚀 Most Common Usage

### Navigate to Framework
```bash
cd apps/claude-test-generator
```

### Analyze JIRA Ticket
Simply ask Claude:
```
"Please analyze ACM-12345 and generate E2E test cases"
```

### Alternative Commands
```bash
# With specific environment
"Analyze ACM-12345 using my current kubeconfig"

# With PR context
"Analyze ACM-12345 and include PR analysis from https://github.com/org/repo/pull/123"
```

## ⚡ What You Get
- **Execution Time**: 5-10 minutes
- **Test Cases**: 3-5 comprehensive E2E scenarios
- **Coverage**: All NEW functionality with realistic validation steps
- **Format**: Ready for manual execution or Polarion import
- **Dual Output**: Both detailed analysis and clean test cases

## 🌍 Environment Options
- **Default**: qe6 environment (automatic setup)
- **Custom**: Use your own kubeconfig/cluster
- **Flexible**: Framework adapts to available resources

## 📁 Output Location
```
runs/<TICKET-ID>/run-XXX-YYYYMMDD-HHMM/
├── Complete-Analysis.md     # Comprehensive analysis
├── Test-Cases.md           # Clean test cases only
└── metadata.json           # Run metadata
```

## 🎯 Alternative: Global Slash Commands

### Quick E2E Test Plan from PR
```bash
/generate-e2e-test-plan https://github.com/repo/pull/123 "Feature Name"
```

### Workflow Analysis
```bash
/analyze-workflow https://github.com/repo/pull/123 "test-plan" ACM-123.txt
```
