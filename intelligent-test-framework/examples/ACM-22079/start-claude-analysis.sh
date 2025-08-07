#!/bin/bash

# start-claude-analysis.sh - Quick Start Script for Claude Code Analysis
# This script guides you through your first Claude Code analysis of ACM-22079

set -e

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo
echo "🚀 Welcome to Claude Code JIRA Analysis"
echo "======================================="
echo -e "${BLUE}Framework: AI-Powered Test Generation for ACM-22079${NC}"
echo

# Quick environment check
echo "🔍 Quick Environment Check..."
if command -v claude &> /dev/null; then
    echo -e "✅ ${GREEN}Claude Code CLI available${NC}"
else
    echo -e "❌ ${RED}Claude Code CLI not found. Please install and configure Claude Code first.${NC}"
    echo "   Refer to: Claude_Code_Setup_Guide_ACM_QE.md"
    exit 1
fi

if [ -f "analyze-jira.sh" ]; then
    echo -e "✅ ${GREEN}Framework ready${NC}"
else
    echo -e "❌ ${RED}Framework not found. Please run from the ACM-22079 directory.${NC}"
    exit 1
fi

echo

# Show options
echo "📋 Choose your analysis approach:"
echo
echo "1️⃣  Test Plan Only (Recommended First Time)"
echo "   - Generates comprehensive test plan"
echo "   - Reviews and validates with Claude Code"
echo "   - Stops for your approval before implementation"
echo
echo "2️⃣  Full Implementation"
echo "   - Complete analysis + Cypress test code generation"
echo "   - Includes test plan + automation scripts"
echo "   - Multiple review gates for quality"
echo
echo "3️⃣  Safe Dry Run"
echo "   - Shows what would happen without execution"
echo "   - Perfect for understanding the workflow"
echo "   - No actual changes made"
echo
echo "4️⃣  Interactive Claude Session"
echo "   - Start Claude Code in this project directory"
echo "   - Manual exploration and analysis"
echo "   - Full control over the process"
echo

read -p "Choose option (1-4): " choice

case $choice in
    1)
        echo
        echo -e "${BLUE}🧠 Starting Test Plan Generation with Claude Code...${NC}"
        echo "This will:"
        echo "  • Analyze JIRA ticket ACM-22079"
        echo "  • Use Claude Code for comprehensive analysis" 
        echo "  • Generate detailed test scenarios"
        echo "  • Pause for your review and approval"
        echo
        read -p "Continue? (y/n): " confirm
        if [[ $confirm == [yY] ]]; then
            echo
            echo -e "${GREEN}🚀 Executing: ./analyze-jira.sh ACM-22079 --test-plan-only --verbose${NC}"
            echo
            ./analyze-jira.sh ACM-22079 --test-plan-only --verbose
        else
            echo "Analysis cancelled."
        fi
        ;;
    2)
        echo
        echo -e "${BLUE}🔧 Starting Full Implementation with Claude Code...${NC}"
        echo "This will:"
        echo "  • Complete test plan generation"
        echo "  • Generate Cypress test code for clc-ui"
        echo "  • Create automation and validation scripts"
        echo "  • Multiple review checkpoints"
        echo
        echo -e "${YELLOW}⚠️  This is the complete workflow. Recommended after reviewing test plan first.${NC}"
        echo
        read -p "Continue with full implementation? (y/n): " confirm
        if [[ $confirm == [yY] ]]; then
            echo
            echo -e "${GREEN}🚀 Executing: ./analyze-jira.sh ACM-22079 --verbose${NC}"
            echo
            ./analyze-jira.sh ACM-22079 --verbose
        else
            echo "Analysis cancelled."
        fi
        ;;
    3)
        echo
        echo -e "${BLUE}🧪 Starting Safe Dry Run...${NC}"
        echo "This will show you exactly what the framework would do without making changes."
        echo
        echo -e "${GREEN}🚀 Executing: ./analyze-jira.sh ACM-22079 --test-plan-only --dry-run --verbose${NC}"
        echo
        ./analyze-jira.sh ACM-22079 --test-plan-only --dry-run --verbose
        ;;
    4)
        echo
        echo -e "${BLUE}💬 Starting Interactive Claude Code Session...${NC}"
        echo
        echo "Claude Code will start in this project directory."
        echo "Useful commands in Claude:"
        echo "  /init    - Analyze the project structure"
        echo "  /help    - Show all available commands"
        echo "  /status  - Check connection and configuration"
        echo "  /exit    - Exit Claude Code"
        echo
        echo "You can also ask Claude to:"
        echo "  • Analyze the JIRA ticket details"
        echo "  • Review the PR #468 code changes"
        echo "  • Suggest test scenarios"
        echo "  • Generate specific test cases"
        echo
        read -p "Start interactive Claude session? (y/n): " confirm
        if [[ $confirm == [yY] ]]; then
            echo
            echo -e "${GREEN}🚀 Starting Claude Code...${NC}"
            echo
            claude
        else
            echo "Interactive session cancelled."
        fi
        ;;
    *)
        echo
        echo "Invalid choice. Please run the script again and choose 1-4."
        exit 1
        ;;
esac

echo
echo "📚 For more information:"
echo "  • CLAUDE_CODE_NEXT_STEPS.md - Detailed usage guide"
echo "  • COMPLETE_WORKFLOW_GUIDE.md - Complete framework documentation"
echo "  • ./analyze-jira.sh --help - Framework help"
echo
echo -e "${GREEN}🎯 Happy analyzing with Claude Code!${NC}"