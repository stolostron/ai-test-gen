#!/bin/bash
# ACM-22079 Project Initialization Script
# Sets up the complete project structure and initial files

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

echo "🚀 ACM-22079 Project Initialization"
echo "===================================="
echo ""

# Verify we're in the right directory
CURRENT_DIR=$(pwd)
EXPECTED_DIR="/Users/ashafi/Documents/work/ai/claude/ACM-22079"

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    print_error "Please run from: $EXPECTED_DIR"
    exit 1
fi

print_success "✓ Initializing project in: $CURRENT_DIR"

# Run environment check first
print_status "Running environment check..."
if [ -x "./01-setup/environment-check.sh" ]; then
    ./01-setup/environment-check.sh
    if [ $? -ne 0 ]; then
        print_error "Environment check failed. Please fix issues before continuing."
        exit 1
    fi
else
    print_error "Environment check script not found or not executable"
    exit 1
fi

# Initialize Claude Code with project context
print_status "Initializing Claude Code project context..."

# Create project context file
cat > .claude-context << EOF
# ACM-22079 Project Context for Claude Code

## Project Information
- **JIRA Ticket**: ACM-22079
- **Title**: Support digest-based upgrades via ClusterCurator for non-recommended upgrades
- **Component**: Advanced Cluster Management (ACM) - ClusterCurator
- **Team**: ACM QE Team
- **Analysis Tool**: Claude Code CLI

## Project Goals
1. Analyze the digest-based upgrade feature implementation
2. Generate comprehensive test cases for ACM QE testing
3. Create implementation-ready test automation code
4. Document process for future JIRA analysis

## Key Directories
- ACM Automation Codebase: /Users/ashafi/Documents/work/automation
- This Analysis Project: /Users/ashafi/Documents/work/ai/claude/ACM-22079

## Focus Areas
- ClusterCurator digest-based upgrades
- Non-recommended upgrade paths
- Disconnected environment support
- Test case generation for ACM components

## Reference Links
- JIRA: https://issues.redhat.com/browse/ACM-22079
- PR: stolostron/cluster-curator-controller#468
EOF

print_success "✓ Created .claude-context file"

# Create session tracking
print_status "Setting up session tracking..."

SESSION_DIR="02-analysis/sessions"
mkdir -p "$SESSION_DIR"

TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
SESSION_FILE="$SESSION_DIR/session_${TIMESTAMP}.md"

cat > "$SESSION_FILE" << EOF
# Claude Analysis Session - $(date "+%Y-%m-%d %H:%M:%S")

## Session Information
- **Started**: $(date)
- **JIRA Ticket**: ACM-22079
- **Analyst**: $(whoami)
- **Session ID**: ${TIMESTAMP}

## Session Goals
- [ ] Complete initial JIRA analysis
- [ ] Understand feature implementation
- [ ] Generate test cases
- [ ] Create implementation recommendations

## Session Log
[Session commands and outputs will be logged here]

---
EOF

print_success "✓ Created session file: $SESSION_FILE"

# Test Claude Code with project initialization
print_status "Testing Claude Code with project context..."

# Create initialization prompt
INIT_PROMPT="I'm starting analysis of JIRA ticket ACM-22079: 'Support digest-based upgrades via ClusterCurator for non-recommended upgrades'. This is for ACM QE testing. Please confirm you can see this project context and are ready to help with ClusterCurator digest-based upgrade analysis and test case generation."

echo "Running Claude Code initialization test..."
if claude --print "$INIT_PROMPT" > /tmp/claude_init_test.txt 2>&1; then
    print_success "✓ Claude Code initialization successful"
    
    # Save the response
    cat /tmp/claude_init_test.txt >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"
    echo "---" >> "$SESSION_FILE"
    echo "" >> "$SESSION_FILE"
    
    rm /tmp/claude_init_test.txt
else
    print_warning "⚠ Claude Code test failed - check manually"
fi

# Create workflow status tracker
print_status "Creating workflow status tracker..."

cat > "workflow-status.md" << EOF
# ACM-22079 Workflow Status

## Project Initialization
- [x] Environment check completed
- [x] Project structure created
- [x] Claude Code tested
- [x] Session tracking setup

## Analysis Phase
- [ ] JIRA ticket analyzed
- [ ] PR details reviewed  
- [ ] Feature understanding complete
- [ ] Implementation details documented

## Test Generation Phase
- [ ] Unit test cases generated
- [ ] Integration test cases generated
- [ ] E2E test cases generated
- [ ] ACM-specific test cases generated

## Implementation Phase
- [ ] Cypress tests created
- [ ] Test data generated
- [ ] Automation scripts created
- [ ] Jenkins configs updated

## Documentation Phase
- [ ] Analysis documented
- [ ] Test cases documented
- [ ] Implementation guide created
- [ ] Team sharing materials ready

## Completion
- [ ] All deliverables complete
- [ ] Quality review passed
- [ ] Team handoff complete

---
Last Updated: $(date)
EOF

print_success "✓ Created workflow status tracker"

# Display next steps
echo ""
echo "===================================="
print_success "🎯 Project initialization complete!"
echo "===================================="

echo ""
echo "📁 Project Structure:"
echo "├── 01-setup/                 ✓ Setup scripts"
echo "├── 02-analysis/              ✓ Analysis workspace"
echo "├── 03-results/               ✓ Generated outputs"
echo "├── 04-implementation/        ✓ Implementation files"
echo "├── 05-documentation/         ✓ Documentation"
echo "├── 06-reference/             ✓ Reference materials"
echo "├── .claude-context           ✓ Claude project context"
echo "├── workflow-status.md        ✓ Progress tracker"
echo "└── Current session:          ✓ $SESSION_FILE"

echo ""
echo "🎯 Ready to Start Analysis!"
echo ""
echo "📋 Next Steps:"
echo "1. 📖 Read: 05-documentation/workflow-guide.md"
echo "2. 📝 Review: 02-analysis/jira-details.md"
echo "3. 🚀 Start: Use prompts from 02-analysis/prompts/"
echo "4. 📊 Track: Update workflow-status.md as you progress"
echo ""
echo "🔧 Quick Start Commands:"
echo "# Interactive analysis session"
echo "claude"
echo ""
echo "# Quick non-interactive test"
echo "claude --print \"Ready to analyze ACM-22079 ClusterCurator digest-based upgrades\""
echo ""
echo "# View current session"
echo "cat $SESSION_FILE"

echo ""
print_success "✅ All systems ready - begin your analysis!"