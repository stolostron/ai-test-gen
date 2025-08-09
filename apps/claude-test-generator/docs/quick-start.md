# Claude Test Generator - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Prerequisites Check
```bash
# Verify Claude Code CLI
claude --version

# Verify GitHub access (optional)
git ls-remote git@github.com:stolostron/console.git HEAD
```

### Step 2: Navigate to App
```bash
cd apps/claude-test-generator
```

### Step 3: Generate Your First Test Plan
```bash
# Use global slash command
/generate-e2e-test-plan https://github.com/stolostron/repo/pull/123 "Your Feature Name"
```

### Step 4: Review Output
```bash
# Check generated files
ls ../../e2e-test-generated/

# View your test plan
cat ../../e2e-test-generated/e2e-test-plan-Your-Feature-Name.md
```

## ✅ Success!

You should now have a professionally formatted test plan ready for:
- Manual execution
- Polarion import
- Team review
- Further refinement

## 🔄 Next Steps

1. **Customize**: Edit the generated test plan for your environment
2. **Iterate**: Run the command again with refined feature names
3. **Scale**: Consider the Intelligent Test Framework for complex features

## 🎯 Common Use Cases

### Quick PR Analysis
```bash
/analyze-workflow https://github.com/repo/pull/123 "test-plan"
```

### Bug Fix Validation
```bash
/generate-e2e-test-plan https://github.com/repo/pull/124 "Bug Fix Validation"
```

### Feature Documentation
```bash
/analyze-workflow https://github.com/repo/pull/125 "documentation" JIRA-123.txt
```
