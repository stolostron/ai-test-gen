#!/bin/bash
# ACM-22079 Quick Start Script
# One-command setup and validation

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

clear
echo "🚀 ACM-22079 Quick Start"
echo "========================"
echo ""

# Check if we're in the right directory
CURRENT_DIR=$(pwd)
EXPECTED_DIR="/Users/ashafi/Documents/work/ai/claude/ACM-22079"

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    echo "Navigating to project directory..."
    cd "$EXPECTED_DIR"
fi

print_status "Running comprehensive setup detection and auto-configuration..."
./01-setup/comprehensive-setup-check.sh

if [ $? -eq 0 ]; then
    print_success "Environment check passed!"
    echo ""
    
    print_status "Running project initialization..."
    ./01-setup/project-init.sh
    
    if [ $? -eq 0 ]; then
        print_success "Project initialization complete!"
        echo ""
        echo "🎯 READY TO START ANALYSIS!"
        echo ""
        echo "📋 Next Steps:"
        echo "1. 📖 Read the workflow guide: cat 05-documentation/workflow-guide.md"
        echo "2. 🚀 Start with first prompt: cat 02-analysis/prompts/initial-analysis.txt"
        echo "3. 💻 Run Claude interactive: claude"
        echo ""
        echo "📚 Quick Reference:"
        echo "- Workflow guide: 05-documentation/workflow-guide.md"
        echo "- Next steps: 05-documentation/next-steps.md"
        echo "- Session tracking: 02-analysis/sessions/"
        echo "- Save results to: 03-results/"
        echo ""
        print_success "✅ All systems ready for ACM-22079 analysis!"
    else
        echo "Project initialization failed. Please check errors above."
        exit 1
    fi
else
    echo "Environment check failed. Please fix issues before continuing."
    exit 1
fi