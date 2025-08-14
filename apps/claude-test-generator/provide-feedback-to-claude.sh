#!/bin/bash
# Script to provide framework feedback to Claude

echo "🔄 Providing framework feedback to Claude..."
echo ""
echo "The framework has been updated with critical feedback based on validation results."
echo ""
echo "Key files updated:"
echo "1. FRAMEWORK-FEEDBACK-20250813.md - Critical feedback summary"
echo "2. .claude/templates/test-case-format-requirements.md - Fixed formatting rules"
echo "3. .claude/templates/enhanced-analysis-report-template.md - Fixed deployment status header"
echo "4. CLAUDE.md - Updated with mandatory requirements"
echo ""
echo "To use the framework with these improvements:"
echo ""
echo "Option 1 - Direct prompt with feedback:"
echo "----------------------------------------"
cat << 'EOF'
Generate test plans for [TICKET-ID] following these CRITICAL requirements:

1. NEVER use HTML tags like <br/> - use markdown only
2. First step MUST be: "**Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login...`"
3. Use header "## 🚨 DEPLOYMENT STATUS" exactly in Complete-Analysis.md
4. Show actual outputs in expected results, not commands
5. Include sample YAML/JSON outputs in triple backticks

Reference: FRAMEWORK-FEEDBACK-20250813.md for complete requirements.
EOF
echo ""
echo "Option 2 - Reference the feedback file:"
echo "----------------------------------------"
echo "Generate test plans for [TICKET-ID]. Follow all requirements in FRAMEWORK-FEEDBACK-20250813.md"
echo ""
echo "The framework will now enforce these requirements automatically."
