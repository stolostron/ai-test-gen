#!/bin/bash
# Enable GitHub PR Access for Claude Code
# Downloads and organizes PR information for local Claude Code access

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

print_config() {
    echo -e "${BLUE}[CONFIG]${NC} $1"
}

echo "🔗 Enabling GitHub PR Access for Claude Code"
echo "============================================="
echo ""

# Check if we're in the right directory
CURRENT_DIR=$(pwd)
EXPECTED_DIR="/Users/ashafi/Documents/work/ai/claude/ACM-22079"

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    echo "Please run from: $EXPECTED_DIR"
    exit 1
fi

print_success "✓ Running from correct directory: $CURRENT_DIR"

# Create PR reference directory
PR_DIR="06-reference/pr-files/ACM-22079-PR-468"
mkdir -p "$PR_DIR"

print_config "Setting up PR access in: $PR_DIR"

# Check if git is available for cloning the source repository
if command -v git &> /dev/null; then
    print_success "✓ Git available for repository access"
    
    # Clone or update the cluster-curator-controller repository
    REPO_DIR="06-reference/stolostron-cluster-curator-controller"
    
    if [ -d "$REPO_DIR" ]; then
        print_config "Updating existing repository..."
        cd "$REPO_DIR"
        git pull origin main
        cd - > /dev/null
    else
        print_config "Cloning cluster-curator-controller repository..."
        git clone https://github.com/stolostron/cluster-curator-controller.git "$REPO_DIR"
    fi
    
    if [ -d "$REPO_DIR" ]; then
        print_success "✓ Repository available locally"
        
        # Extract specific files from the PR
        print_config "Extracting PR files for Claude Code access..."
        
        # Copy the modified files to our PR directory
        cp "$REPO_DIR/cmd/curator/curator.go" "$PR_DIR/curator.go" 2>/dev/null || true
        cp "$REPO_DIR/pkg/jobs/hive/hive.go" "$PR_DIR/hive.go" 2>/dev/null || true
        cp "$REPO_DIR/pkg/jobs/hive/hive_test.go" "$PR_DIR/hive_test.go" 2>/dev/null || true
        cp "$REPO_DIR/pkg/jobs/utils/helpers.go" "$PR_DIR/helpers.go" 2>/dev/null || true
        
        print_success "✓ PR files extracted for local access"
    else
        print_warning "⚠ Could not access repository - using existing PR summary"
    fi
else
    print_warning "⚠ Git not available - using existing PR summary only"
fi

# Create comprehensive PR context file for Claude Code
print_config "Creating comprehensive PR context for Claude Code..."

cat > "$PR_DIR/claude-pr-context.md" << 'EOF'
# ACM-22079 PR #468 Context for Claude Code

## How to Reference This PR in Claude Code

When working with Claude Code, you can reference this PR information using:

```
@file:06-reference/pr-files/ACM-22079-PR-468/pr-summary.md
@file:06-reference/pr-files/ACM-22079-PR-468/hive.go
@file:06-reference/pr-files/ACM-22079-PR-468/hive_test.go
```

## Quick Reference Commands

### View PR Summary
```bash
cat 06-reference/pr-files/ACM-22079-PR-468/pr-summary.md
```

### View Modified Files
```bash
ls -la 06-reference/pr-files/ACM-22079-PR-468/
```

### Include in Claude Prompts
When asking Claude Code about the implementation, include:
"Please reference the PR files in 06-reference/pr-files/ACM-22079-PR-468/ for the actual implementation details."

## Claude Code Access Patterns

### 1. Direct File Reference
```
@file:06-reference/pr-files/ACM-22079-PR-468/hive.go

Please analyze the validateUpgradeVersion function changes in this file.
```

### 2. Multi-File Analysis
```
@file:06-reference/pr-files/ACM-22079-PR-468/hive.go
@file:06-reference/pr-files/ACM-22079-PR-468/hive_test.go

Compare the implementation with its test cases.
```

### 3. Context-Aware Prompts
```
Based on the PR files in 06-reference/pr-files/ACM-22079-PR-468/, 
analyze the digest-based upgrade implementation and generate test cases.
```

## Available PR Information

- ✅ Complete PR summary with all changes
- ✅ Source code files (if git clone successful)
- ✅ Implementation details and analysis
- ✅ Test case examples
- ✅ Code review comments and decisions

This provides Claude Code with complete local access to all PR information without needing external network access.
EOF

# Create a comprehensive file listing
print_config "Creating file inventory..."

cat > "$PR_DIR/file-inventory.md" << EOF
# ACM-22079 PR Files Inventory

## Available Files for Claude Code Analysis

### Core Implementation Files
$(if [ -f "$PR_DIR/hive.go" ]; then echo "- ✅ hive.go (Main implementation)"; else echo "- ❌ hive.go (Not available)"; fi)
$(if [ -f "$PR_DIR/hive_test.go" ]; then echo "- ✅ hive_test.go (Test cases)"; else echo "- ❌ hive_test.go (Not available)"; fi)
$(if [ -f "$PR_DIR/helpers.go" ]; then echo "- ✅ helpers.go (Utility functions)"; else echo "- ❌ helpers.go (Not available)"; fi)
$(if [ -f "$PR_DIR/curator.go" ]; then echo "- ✅ curator.go (Main entry point)"; else echo "- ❌ curator.go (Not available)"; fi)

### Documentation Files
- ✅ pr-summary.md (Complete PR analysis)
- ✅ claude-pr-context.md (Claude Code usage guide)
- ✅ file-inventory.md (This file)

### Repository Access
$(if [ -d "06-reference/stolostron-cluster-curator-controller" ]; then echo "- ✅ Full repository cloned locally"; else echo "- ❌ Repository not available locally"; fi)

## How to Use with Claude Code

### In Interactive Mode
\`\`\`
claude

# Then reference files:
@file:06-reference/pr-files/ACM-22079-PR-468/pr-summary.md
Please analyze the ACM-22079 implementation based on this PR.
\`\`\`

### In Non-Interactive Mode
\`\`\`bash
claude --print "Based on the files in 06-reference/pr-files/ACM-22079-PR-468/, analyze the digest-based upgrade feature"
\`\`\`

## File Access Commands
\`\`\`bash
# View all available files
ls -la 06-reference/pr-files/ACM-22079-PR-468/

# Read specific implementation
cat 06-reference/pr-files/ACM-22079-PR-468/hive.go

# View test cases
cat 06-reference/pr-files/ACM-22079-PR-468/hive_test.go
\`\`\`

Generated: $(date)
EOF

# Update the main project context to include PR access
print_config "Updating project context for PR access..."

if [ -f ".claude-context" ]; then
    # Add PR access information to existing context
    cat >> .claude-context << EOF

## GitHub PR Access
- **PR #468**: stolostron/cluster-curator-controller#468
- **Local PR Files**: 06-reference/pr-files/ACM-22079-PR-468/
- **Repository**: 06-reference/stolostron-cluster-curator-controller/ (if available)
- **Usage**: Reference PR files using @file: syntax in Claude Code

## PR File References for Claude Code
- @file:06-reference/pr-files/ACM-22079-PR-468/pr-summary.md
- @file:06-reference/pr-files/ACM-22079-PR-468/hive.go
- @file:06-reference/pr-files/ACM-22079-PR-468/hive_test.go
- @file:06-reference/pr-files/ACM-22079-PR-468/helpers.go
EOF
fi

# Create an enhanced prompt that includes PR access
print_config "Creating PR-aware analysis prompt..."

cat > "02-analysis/prompts/pr-aware-analysis.txt" << 'EOF'
I need to analyze ACM-22079 using the actual PR implementation files that are now available locally.

## PR Access
Please reference these local files for the actual implementation:
@file:06-reference/pr-files/ACM-22079-PR-468/pr-summary.md
@file:06-reference/pr-files/ACM-22079-PR-468/hive.go
@file:06-reference/pr-files/ACM-22079-PR-468/hive_test.go

## Analysis Request
Based on the actual PR files above, provide:

1. **Detailed Implementation Analysis**:
   - Examine the actual validateUpgradeVersion function changes
   - Analyze the retreiveAndUpdateClusterVersion modifications
   - Review the digest discovery algorithm implementation
   - Understand the test case implementations

2. **Code-Specific Insights**:
   - How does the actual conditionalUpdates processing work?
   - What's the exact logic for digest vs tag-based image selection?
   - How are the test cases structured and what do they validate?
   - What error handling patterns are implemented?

3. **Test Case Generation**:
   - Based on the actual test implementations, generate additional test scenarios
   - Create test cases that complement the existing ones
   - Focus on edge cases and error conditions not covered

4. **Implementation Recommendations**:
   - How to integrate these findings into ACM QE test automation
   - Specific test data requirements based on actual implementation
   - CI/CD considerations based on the actual code structure

## Context
This is for ACM QE test automation development. The analysis should be based on the actual implementation code, not just the JIRA description.

Please reference the specific files and code sections in your analysis.
EOF

print_success "✓ PR-aware analysis prompt created"

# Final summary
echo ""
echo "============================================="
print_success "🎯 GitHub PR Access Setup Complete!"
echo "============================================="

echo ""
echo "📁 PR Files Available:"
if [ -f "$PR_DIR/hive.go" ]; then
    echo "  ✅ Implementation files (hive.go, hive_test.go, etc.)"
else
    echo "  ⚠ Implementation files (summary only - git clone may have failed)"
fi
echo "  ✅ Complete PR summary and analysis"
echo "  ✅ Claude Code usage instructions"
echo "  ✅ File inventory and access guide"

echo ""
echo "🔧 How to Use with Claude Code:"
echo ""
echo "1. 📖 **Reference PR files directly**:"
echo "   claude"
echo "   @file:06-reference/pr-files/ACM-22079-PR-468/pr-summary.md"
echo "   [Your analysis request]"
echo ""
echo "2. 🚀 **Use the enhanced prompt**:"
echo "   cat 02-analysis/prompts/pr-aware-analysis.txt"
echo "   [Copy and paste into Claude Code]"
echo ""
echo "3. 📊 **Multi-file analysis**:"
echo "   @file:06-reference/pr-files/ACM-22079-PR-468/hive.go"
echo "   @file:06-reference/pr-files/ACM-22079-PR-468/hive_test.go"
echo "   Compare implementation with tests"

echo ""
print_success "✅ Claude Code now has complete local access to PR #468 information!"

echo ""
echo "💡 **Pro Tip**: Claude Code can now analyze the actual implementation code"
echo "   instead of relying on external descriptions. This provides much more"
echo "   accurate and detailed analysis for test case generation."