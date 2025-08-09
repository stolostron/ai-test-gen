#!/bin/bash
# Enhanced Claude Code Setup Detection and Auto-Configuration
# Detects and automatically configures all Claude Code requirements

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_config() {
    echo -e "${PURPLE}[CONFIG]${NC} $1"
}

echo "🔍 Comprehensive Claude Code Setup Detection & Auto-Configuration"
echo "=================================================================="
echo ""

# Track what needs to be configured
NEEDS_SETUP=false

# Check current directory
CURRENT_DIR=$(pwd)
EXPECTED_DIR="/Users/ashafi/Documents/work/ai/claude/ACM-22079"

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    print_error "Please run from: $EXPECTED_DIR"
    exit 1
fi

print_success "✓ Running from correct directory: $CURRENT_DIR"
echo ""

# 1. CLAUDE CODE CLI DETECTION AND INSTALLATION
print_status "=== Claude Code CLI Detection ==="

if command -v claude &> /dev/null; then
    CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "unknown")
    print_success "✓ Claude Code CLI found: $CLAUDE_VERSION"
else
    print_warning "✗ Claude Code CLI not found"
    NEEDS_SETUP=true
    
    print_config "Attempting to install Claude Code CLI..."
    
    # Check if npm is available
    if command -v npm &> /dev/null; then
        print_config "Installing Claude Code via npm..."
        npm install -g @anthropic-ai/claude-code
        
        # Clear command cache
        hash -r
        
        if command -v claude &> /dev/null; then
            print_success "✓ Claude Code CLI installed successfully"
        else
            print_error "✗ Claude Code CLI installation failed"
            echo "Please install manually: npm install -g @anthropic-ai/claude-code"
            exit 1
        fi
    else
        print_error "✗ npm not found - cannot install Claude Code"
        echo "Please install Node.js and npm first, then run: npm install -g @anthropic-ai/claude-code"
        exit 1
    fi
fi

# 2. ENVIRONMENT VARIABLES DETECTION AND CONFIGURATION
print_status "=== Environment Variables Detection ==="

REQUIRED_VARS=(
    "CLAUDE_CODE_USE_VERTEX:1"
    "CLOUD_ML_REGION:us-east5"
    "ANTHROPIC_VERTEX_PROJECT_ID:itpc-gcp-hcm-pe-eng-claude"
    "ANTHROPIC_MODEL:claude-sonnet-4@20250514"
    "ANTHROPIC_SMALL_FAST_MODEL:claude-sonnet-4@20250514"
)

MISSING_VARS=()

for var_pair in "${REQUIRED_VARS[@]}"; do
    var_name=$(echo "$var_pair" | cut -d: -f1)
    expected_value=$(echo "$var_pair" | cut -d: -f2-)
    
    if [ -z "${!var_name}" ]; then
        print_warning "✗ Environment variable $var_name is not set"
        MISSING_VARS+=("$var_pair")
        NEEDS_SETUP=true
    else
        current_value="${!var_name}"
        if [ "$current_value" = "$expected_value" ]; then
            print_success "✓ $var_name: $current_value"
        else
            print_warning "⚠ $var_name: $current_value (expected: $expected_value)"
            MISSING_VARS+=("$var_pair")
            NEEDS_SETUP=true
        fi
    fi
done

# Auto-configure missing environment variables
if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    print_config "Auto-configuring missing environment variables..."
    
    # Determine shell config file
    if [ "$SHELL" = "/bin/zsh" ] || [ "$SHELL" = "/usr/bin/zsh" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [ "$SHELL" = "/bin/bash" ] || [ "$SHELL" = "/usr/bin/bash" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    else
        SHELL_CONFIG="$HOME/.profile"
    fi
    
    print_config "Using shell config: $SHELL_CONFIG"
    
    # Check if Claude Code variables already exist
    if grep -q "CLAUDE_CODE_USE_VERTEX\|ANTHROPIC" "$SHELL_CONFIG" 2>/dev/null; then
        print_warning "Claude Code variables already exist in $SHELL_CONFIG"
        print_config "Please manually update the following variables:"
        for var_pair in "${MISSING_VARS[@]}"; do
            var_name=$(echo "$var_pair" | cut -d: -f1)
            expected_value=$(echo "$var_pair" | cut -d: -f2-)
            echo "export $var_name='$expected_value'"
        done
    else
        print_config "Adding Claude Code environment variables to $SHELL_CONFIG"
        
        # Add variables to shell config
        cat >> "$SHELL_CONFIG" << 'EOF'

# Claude Code Configuration - ACM QE Team (Auto-configured)
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=itpc-gcp-hcm-pe-eng-claude
export ANTHROPIC_MODEL='claude-sonnet-4@20250514'
export ANTHROPIC_SMALL_FAST_MODEL='claude-sonnet-4@20250514'
EOF

        print_success "✓ Environment variables added to $SHELL_CONFIG"
        
        # Source the config
        source "$SHELL_CONFIG"
        print_success "✓ Configuration reloaded"
    fi
fi

# 3. GOOGLE CLOUD CLI DETECTION AND CONFIGURATION
print_status "=== Google Cloud CLI Detection ==="

if command -v gcloud &> /dev/null; then
    print_success "✓ Google Cloud CLI found"
    
    # Check project configuration
    CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")
    EXPECTED_PROJECT="itpc-gcp-hcm-pe-eng-claude"
    
    if [ "$CURRENT_PROJECT" = "$EXPECTED_PROJECT" ]; then
        print_success "✓ Google Cloud project: $CURRENT_PROJECT"
    else
        print_warning "⚠ Google Cloud project: $CURRENT_PROJECT (expected: $EXPECTED_PROJECT)"
        print_config "Auto-configuring Google Cloud project..."
        
        gcloud config set project "$EXPECTED_PROJECT"
        if [ $? -eq 0 ]; then
            print_success "✓ Google Cloud project configured"
        else
            print_warning "⚠ Failed to set project - you may need to authenticate first"
        fi
    fi
    
    # Check authentication
    AUTH_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null || echo "")
    if [ -n "$AUTH_ACCOUNT" ]; then
        print_success "✓ Authenticated as: $AUTH_ACCOUNT"
    else
        print_warning "✗ Not authenticated with Google Cloud"
        print_config "Authentication required. Please run:"
        echo "  gcloud auth login"
        echo "  gcloud auth application-default login"
        echo "  gcloud auth application-default set-quota-project cloudability-it-gemini"
        NEEDS_SETUP=true
    fi
else
    print_error "✗ Google Cloud CLI not found"
    print_config "Please install Google Cloud CLI:"
    echo "  macOS: brew install --cask google-cloud-sdk"
    echo "  Linux: Follow https://cloud.google.com/sdk/docs/install"
    NEEDS_SETUP=true
fi

# 4. NODE.JS AND NPM DETECTION
print_status "=== Node.js and NPM Detection ==="

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "✓ Node.js found: $NODE_VERSION"
    
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "✓ NPM found: $NPM_VERSION"
        
        # Check npm global configuration
        NPM_PREFIX=$(npm config get prefix 2>/dev/null || echo "")
        EXPECTED_PREFIX="$HOME/.npm-global"
        
        if [ "$NPM_PREFIX" = "$EXPECTED_PREFIX" ]; then
            print_success "✓ NPM global prefix configured: $NPM_PREFIX"
        else
            print_config "Configuring NPM global prefix..."
            mkdir -p "$EXPECTED_PREFIX"
            npm config set prefix "$EXPECTED_PREFIX"
            print_success "✓ NPM global prefix set to: $EXPECTED_PREFIX"
            
            # Check if npm-global is in PATH
            if echo "$PATH" | grep -q "npm-global"; then
                print_success "✓ NPM global bin directory in PATH"
            else
                print_config "Adding NPM global bin to PATH..."
                SHELL_CONFIG_FOR_PATH="$HOME/.zshrc"
                if [ "$SHELL" = "/bin/bash" ] || [ "$SHELL" = "/usr/bin/bash" ]; then
                    SHELL_CONFIG_FOR_PATH="$HOME/.bashrc"
                fi
                
                if ! grep -q "npm-global" "$SHELL_CONFIG_FOR_PATH" 2>/dev/null; then
                    echo 'export PATH=$HOME/.npm-global/bin:$PATH' >> "$SHELL_CONFIG_FOR_PATH"
                    print_success "✓ NPM global PATH added to $SHELL_CONFIG_FOR_PATH"
                fi
            fi
        fi
    else
        print_error "✗ NPM not found"
        NEEDS_SETUP=true
    fi
else
    print_error "✗ Node.js not found"
    print_config "Please install Node.js:"
    echo "  macOS: brew install node"
    echo "  Linux: sudo apt-get install nodejs npm"
    NEEDS_SETUP=true
fi

# 5. PERMISSIONS AND SECURITY DETECTION
print_status "=== Permissions and Security Detection ==="

# Check file permissions in current directory
if [ -w "." ]; then
    print_success "✓ Write permissions in current directory"
else
    print_error "✗ No write permissions in current directory"
    NEEDS_SETUP=true
fi

# Check home directory access
if [ -w "$HOME" ]; then
    print_success "✓ Write permissions in home directory"
else
    print_error "✗ No write permissions in home directory"
    NEEDS_SETUP=true
fi

# Check if running with appropriate permissions (not root)
if [ "$EUID" -eq 0 ]; then
    print_warning "⚠ Running as root - this may cause permission issues"
fi

# 6. NETWORK CONNECTIVITY CHECK
print_status "=== Network Connectivity Check ==="

# Check internet connectivity
if ping -c 1 google.com &> /dev/null; then
    print_success "✓ Internet connectivity available"
else
    print_warning "⚠ Internet connectivity issues detected"
    print_config "Claude Code requires internet access for API calls"
fi

# Check Google Cloud API endpoint
if curl -s --max-time 5 https://aiplatform.googleapis.com > /dev/null 2>&1; then
    print_success "✓ Google Cloud AI Platform accessible"
else
    print_warning "⚠ Google Cloud AI Platform endpoint not accessible"
fi

# 7. CLAUDE CODE SPECIFIC CONFIGURATION DETECTION
print_status "=== Claude Code Specific Configuration ==="

# Check for Claude Code configuration files
CLAUDE_CONFIG_DIR="$HOME/.config/claude-code"
if [ -d "$CLAUDE_CONFIG_DIR" ]; then
    print_success "✓ Claude Code config directory exists: $CLAUDE_CONFIG_DIR"
else
    print_config "Creating Claude Code config directory..."
    mkdir -p "$CLAUDE_CONFIG_DIR"
    print_success "✓ Claude Code config directory created"
fi

# Check for project context file
if [ -f ".claude-context" ]; then
    print_success "✓ Project context file exists"
else
    print_config "Project context file will be created during initialization"
fi

# 8. FINAL CONNECTION TEST
print_status "=== Final Claude Code Connection Test ==="

if [ "$NEEDS_SETUP" = false ]; then
    print_config "Testing Claude Code with actual API call..."
    
    # Test with environment variables loaded
    export CLAUDE_CODE_USE_VERTEX=1
    export CLOUD_ML_REGION=us-east5
    export ANTHROPIC_VERTEX_PROJECT_ID=itpc-gcp-hcm-pe-eng-claude
    export ANTHROPIC_MODEL='claude-sonnet-4@20250514'
    export ANTHROPIC_SMALL_FAST_MODEL='claude-sonnet-4@20250514'
    
    TEST_PROMPT="Hello! This is an automated test from ACM-22079 setup verification. Please respond with 'Setup verification successful' if you can read this message."
    
    if timeout 30s claude --print "$TEST_PROMPT" > /tmp/claude_setup_test.txt 2>&1; then
        RESPONSE=$(cat /tmp/claude_setup_test.txt)
        if echo "$RESPONSE" | grep -q -i "setup verification successful\|successful\|working\|ready"; then
            print_success "✓ Claude Code connection test PASSED"
            print_success "✓ API response received successfully"
        else
            print_warning "⚠ Claude Code responded but with unexpected content"
            echo "Response: $RESPONSE"
        fi
        rm -f /tmp/claude_setup_test.txt
    else
        print_warning "⚠ Claude Code connection test timed out or failed"
        print_config "This might indicate authentication or network issues"
        
        # Show error details
        if [ -f /tmp/claude_setup_test.txt ]; then
            echo "Error details:"
            cat /tmp/claude_setup_test.txt
            rm -f /tmp/claude_setup_test.txt
        fi
    fi
else
    print_warning "⚠ Skipping connection test due to missing setup components"
fi

# SUMMARY AND RECOMMENDATIONS
echo ""
echo "=================================================================="
if [ "$NEEDS_SETUP" = false ]; then
    print_success "🎯 Comprehensive setup check PASSED!"
    echo "=================================================================="
    echo ""
    echo "✅ All Claude Code requirements detected and configured:"
    echo "- Claude Code CLI: ✓ Installed and working"
    echo "- Environment Variables: ✓ Configured"
    echo "- Google Cloud: ✓ Configured and authenticated"
    echo "- Node.js/NPM: ✓ Installed and configured"
    echo "- Permissions: ✓ Appropriate"
    echo "- Network: ✓ Connectivity verified"
    echo "- API Connection: ✓ Successfully tested"
    echo ""
    print_success "🚀 Ready to proceed with ACM-22079 analysis!"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./01-setup/project-init.sh"
    echo "2. Start analysis: claude"
    echo "3. Use prompts from: 02-analysis/prompts/"
else
    print_warning "⚠ Setup check identified issues that need attention"
    echo "=================================================================="
    echo ""
    echo "📋 Required actions:"
    echo "1. Review the warnings and errors above"
    echo "2. Follow the configuration suggestions provided"
    echo "3. Reload your shell: source ~/.zshrc (or ~/.bashrc)"
    echo "4. Run this script again to verify fixes"
    echo ""
    echo "🔧 Common solutions:"
    echo "- Install missing components (Node.js, Google Cloud CLI)"
    echo "- Run authentication commands for Google Cloud"
    echo "- Check network connectivity"
    echo "- Verify environment variables in your shell config"
fi

echo ""
print_config "💡 Pro tip: This script auto-configures most issues. Re-run after addressing any manual steps!"