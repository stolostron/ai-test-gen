#!/bin/bash

# simple-test.sh - Quick Framework Testing
set -e

echo "🧪 Quick Framework Validation"
echo "=============================="

# Test 1: Script Syntax
echo "1. Testing script syntax..."
bash -n analyze-jira.sh && echo "✅ Main script syntax OK"
bash -n 01-setup/smart-validation-engine.sh && echo "✅ Smart validation syntax OK"
bash -n 01-setup/adaptive-feedback-integrator.sh && echo "✅ Adaptive feedback syntax OK"

# Test 2: File Permissions
echo
echo "2. Checking file permissions..."
[ -x analyze-jira.sh ] && echo "✅ Main script executable" || echo "❌ Main script not executable"
[ -x 01-setup/smart-validation-engine.sh ] && echo "✅ Smart validation executable" || echo "❌ Smart validation not executable"

# Test 3: Configuration Files
echo
echo "3. Testing configuration files..."
if python3 -c "import yaml; yaml.safe_load(open('team-config.yaml'))" 2>/dev/null; then
    echo "✅ Main config valid"
else
    echo "❌ Main config invalid"
fi

# Test 4: Help Function
echo
echo "4. Testing help functionality..."
if ./analyze-jira.sh --help >/dev/null 2>&1; then
    echo "✅ Help function works"
else
    echo "❌ Help function failed"
fi

# Test 5: Dry Run
echo
echo "5. Testing dry run..."
if ./analyze-jira.sh ACM-22079 --dry-run --test-plan-only >/dev/null 2>&1; then
    echo "✅ Dry run successful"
else
    echo "❌ Dry run failed"
fi

# Test 6: Dependencies
echo
echo "6. Checking dependencies..."
command -v python3 >/dev/null && echo "✅ Python3 available" || echo "❌ Python3 missing"
command -v jq >/dev/null && echo "✅ jq available" || echo "❌ jq missing"
command -v claude >/dev/null && echo "✅ Claude Code available" || echo "⚠️  Claude Code not in PATH"

echo
echo "🎯 Quick test complete!"