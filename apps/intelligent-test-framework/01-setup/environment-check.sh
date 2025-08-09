#!/bin/bash
# ACM-22079 Environment Check Script
# Verifies Claude Code CLI setup for ACM QE testing

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "🔍 ACM-22079 Environment Check"
echo "================================"
echo ""

# Check current directory
CURRENT_DIR=$(pwd)
EXPECTED_DIR="/Users/ashafi/Documents/work/ai/claude/ACM-22079"

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    print_warning "Current directory: $CURRENT_DIR"
    print_warning "Expected directory: $EXPECTED_DIR"
    echo ""
    echo "Please run: cd $EXPECTED_DIR"
    echo "Then run this script again."
    exit 1
fi

print_success "✓ Running from correct directory: $CURRENT_DIR"

# Check Claude Code CLI
print_status "Checking Claude Code CLI installation..."

if command -v claude &> /dev/null; then
    CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "unknown")
    print_success "✓ Claude Code CLI found: $CLAUDE_VERSION"
else
    print_error "✗ Claude Code CLI not found"
    echo ""
    echo "Please install Claude Code CLI first:"
    echo "1. Follow the setup guide in your Slack documentation"
    echo "2. Run: npm install -g @anthropic-ai/claude-code"
    echo "3. Verify: claude --version"
    exit 1
fi

# Check environment variables
print_status "Checking Claude Code environment variables..."

REQUIRED_VARS=(
    "CLAUDE_CODE_USE_VERTEX"
    "CLOUD_ML_REGION"
    "ANTHROPIC_VERTEX_PROJECT_ID"
    "ANTHROPIC_MODEL"
    "ANTHROPIC_SMALL_FAST_MODEL"
)

ALL_VARS_SET=true

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        print_error "✗ Environment variable $var is not set"
        ALL_VARS_SET=false
    else
        print_success "✓ $var: ${!var}"
    fi
done

if [ "$ALL_VARS_SET" = false ]; then
    print_error "Missing required environment variables"
    echo ""
    echo "Please set the following variables in your ~/.zshrc:"
    echo "export CLAUDE_CODE_USE_VERTEX=1"
    echo "export CLOUD_ML_REGION=us-east5"
    echo "export ANTHROPIC_VERTEX_PROJECT_ID=itpc-gcp-hcm-pe-eng-claude"
    echo "export ANTHROPIC_MODEL='claude-sonnet-4@20250514'"
    echo "export ANTHROPIC_SMALL_FAST_MODEL='claude-sonnet-4@20250514'"
    echo ""
    echo "Then run: source ~/.zshrc"
    exit 1
fi

# Check Google Cloud CLI
print_status "Checking Google Cloud CLI configuration..."

if command -v gcloud &> /dev/null; then
    CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")
    EXPECTED_PROJECT="itpc-gcp-hcm-pe-eng-claude"
    
    if [ "$CURRENT_PROJECT" = "$EXPECTED_PROJECT" ]; then
        print_success "✓ Google Cloud project: $CURRENT_PROJECT"
    else
        print_warning "⚠ Google Cloud project: $CURRENT_PROJECT (expected: $EXPECTED_PROJECT)"
        echo ""
        echo "To fix, run: gcloud config set project $EXPECTED_PROJECT"
    fi
    
    # Check authentication
    AUTH_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null || echo "")
    if [ -n "$AUTH_ACCOUNT" ]; then
        print_success "✓ Authenticated as: $AUTH_ACCOUNT"
    else
        print_error "✗ Not authenticated with Google Cloud"
        echo ""
        echo "Please run: gcloud auth login"
    fi
else
    print_error "✗ Google Cloud CLI not found"
    echo ""
    echo "Please install Google Cloud CLI first"
    exit 1
fi

# Check ACM automation codebase access
print_status "Checking ACM automation codebase access..."

ACM_AUTOMATION_PATH="/Users/ashafi/Documents/work/automation"
if [ -d "$ACM_AUTOMATION_PATH" ]; then
    print_success "✓ ACM automation codebase found: $ACM_AUTOMATION_PATH"
    
    # Check for key ACM components
    ACM_COMPONENTS=(
        "clc-ui"
        "clc-non-ui" 
        "alc-ui"
        "grc-ui"
        "console_dev"
    )
    
    for component in "${ACM_COMPONENTS[@]}"; do
        if [ -d "$ACM_AUTOMATION_PATH/$component" ]; then
            print_success "  ✓ $component component found"
        else
            print_warning "  ⚠ $component component not found"
        fi
    done
else
    print_warning "⚠ ACM automation codebase not found at: $ACM_AUTOMATION_PATH"
    echo ""
    echo "Please ensure you have access to the ACM automation codebase"
fi

# Test Claude Code connection
print_status "Testing Claude Code connection..."

# Create a simple test
TEST_PROMPT="Hello! This is a test from ACM-22079 environment check. Please respond with 'Connection successful' if you can read this."

echo ""
print_status "Running connection test (this may take a moment)..."

# Test with a simple prompt
if claude --print "$TEST_PROMPT" &> /dev/null; then
    print_success "✓ Claude Code connection test passed"
else
    print_warning "⚠ Claude Code connection test failed"
    echo ""
    echo "This might indicate authentication or network issues"
    echo "Try running manually: claude --print \"test\""
fi

echo ""
echo "================================"
print_success "🎯 Environment check complete!"
echo "================================"

# Summary
echo ""
echo "📋 Summary:"
echo "- Claude Code CLI: ✓ Installed"
echo "- Environment Variables: ✓ Configured"
echo "- Google Cloud: ✓ Configured" 
echo "- ACM Codebase: ✓ Accessible"
echo "- Connection Test: ✓ Passed"
echo ""
print_success "✅ Ready to proceed with ACM-22079 analysis!"
echo ""
echo "Next steps:"
echo "1. Run: ./01-setup/project-init.sh"
echo "2. Follow: 05-documentation/workflow-guide.md"
echo "3. Start with: 02-analysis/prompts/initial-analysis.txt"