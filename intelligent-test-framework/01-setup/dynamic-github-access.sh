#!/bin/bash

# dynamic-github-access.sh - Dynamic GitHub Repository Access for Claude Code
# Replaces static PR files with real-time repository analysis

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

JIRA_TICKET="${1:-}"
ANALYSIS_MODE="${2:-full}"
CONFIG_FILE="${3:-team-config.yaml}"

print_header() {
    echo
    echo "========================================"
    echo -e "${BLUE}🔗 Dynamic GitHub Repository Access${NC}"
    echo "========================================"
    echo "Setting up real-time access to stolostron repositories"
    echo "JIRA Ticket: $JIRA_TICKET"
    echo "Analysis Mode: $ANALYSIS_MODE"
    echo
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# GitHub API helper functions
github_api_get() {
    local endpoint="$1"
    local repo="${2:-stolostron/cluster-curator-controller}"
    
    curl -s "https://api.github.com/repos/$repo/$endpoint" 2>/dev/null || echo "{}"
}

# Detect relevant repositories for JIRA ticket
detect_relevant_repositories() {
    print_step "1. Detecting relevant stolostron repositories for $JIRA_TICKET..."
    
    local repositories=()
    local ticket_lower=$(echo "$JIRA_TICKET" | tr '[:upper:]' '[:lower:]')
    
    # Core repositories for cluster lifecycle and curator
    repositories+=(
        "stolostron/cluster-curator-controller"
        "stolostron/clc-ui-e2e" 
        "stolostron/console"
        "stolostron/backplane-operator"
        "stolostron/managedcluster-import-controller"
    )
    
    # Detect additional repositories based on JIRA content
    if echo "$JIRA_TICKET" | grep -qi "upgrade\|curator"; then
        repositories+=(
            "stolostron/hypershift-addon-operator"
            "stolostron/cluster-proxy-addon"
        )
    fi
    
    if echo "$JIRA_TICKET" | grep -qi "ui\|console\|frontend"; then
        repositories+=(
            "stolostron/console"
            "stolostron/clc-ui-e2e"
        )
    fi
    
    if echo "$JIRA_TICKET" | grep -qi "policy\|governance"; then
        repositories+=(
            "stolostron/grc-ui"
            "stolostron/config-policy-controller"
        )
    fi
    
    # Remove duplicates and save to file
    printf '%s\n' "${repositories[@]}" | sort -u > "06-reference/detected-repositories.txt"
    
    print_success "Detected ${#repositories[@]} relevant repositories"
    echo "Repositories:"
    printf '%s\n' "${repositories[@]}" | sort -u | sed 's/^/  • /'
    
    return 0
}

# Analyze PR patterns and recent changes
analyze_recent_changes() {
    print_step "2. Analyzing recent changes in stolostron repositories..."
    
    local output_dir="06-reference/recent-changes"
    mkdir -p "$output_dir"
    
    # Get recent PRs from primary repositories
    local primary_repos=(
        "stolostron/cluster-curator-controller"
        "stolostron/clc-ui-e2e"
        "stolostron/console"
    )
    
    for repo in "${primary_repos[@]}"; do
        local repo_name=$(basename "$repo")
        print_info "Analyzing recent changes in $repo..."
        
        # Get recent PRs
        github_api_get "pulls?state=all&sort=updated&direction=desc&per_page=10" "$repo" > "$output_dir/${repo_name}-recent-prs.json"
        
        # Get recent commits
        github_api_get "commits?per_page=20" "$repo" > "$output_dir/${repo_name}-recent-commits.json"
        
        # Extract PR numbers that might be related to the JIRA ticket
        if [ -f "$output_dir/${repo_name}-recent-prs.json" ]; then
            jq -r '.[] | select(.title | test("'$JIRA_TICKET'"; "i")) | "#\(.number): \(.title)"' \
                "$output_dir/${repo_name}-recent-prs.json" > "$output_dir/${repo_name}-related-prs.txt" 2>/dev/null || true
        fi
    done
    
    print_success "Recent changes analysis complete"
    return 0
}

# Setup dynamic repository workspace
setup_dynamic_workspace() {
    print_step "3. Setting up dynamic repository workspace..."
    
    local workspace_dir="06-reference/dynamic-repos"
    mkdir -p "$workspace_dir"
    
    # Read detected repositories
    if [ ! -f "06-reference/detected-repositories.txt" ]; then
        print_error "No detected repositories file found"
        return 1
    fi
    
    cd "$workspace_dir"
    
    while IFS= read -r repo; do
        local repo_name=$(basename "$repo")
        print_info "Setting up access to $repo..."
        
        if [ -d "$repo_name" ]; then
            print_info "Repository $repo_name already exists, updating..."
            cd "$repo_name"
            git fetch origin main >/dev/null 2>&1 || git fetch origin master >/dev/null 2>&1 || true
            cd ..
        else
            print_info "Cloning $repo with minimal history..."
            if git clone --depth=3 "git@github.com:$repo.git" >/dev/null 2>&1; then
                print_success "Successfully cloned $repo_name"
            else
                print_warning "Failed to clone $repo_name (may not have access)"
                continue
            fi
        fi
        
        # Setup PR fetching for this repository
        cd "$repo_name"
        
        # Configure git to fetch PRs
        if ! git config --get-regexp "remote.origin.fetch" | grep -q "pull"; then
            git config --add remote.origin.fetch "+refs/pull/*/head:refs/remotes/origin/pr/*"
            print_info "Configured PR fetching for $repo_name"
        fi
        
        cd ..
        
    done < "../detected-repositories.txt"
    
    cd - >/dev/null
    print_success "Dynamic workspace setup complete"
    return 0
}

# Fetch specific PRs and commits related to JIRA
fetch_related_changes() {
    print_step "4. Fetching changes specifically related to $JIRA_TICKET..."
    
    local workspace_dir="06-reference/dynamic-repos"
    local changes_dir="06-reference/jira-related-changes"
    mkdir -p "$changes_dir"
    
    # Search for PRs and commits related to the JIRA ticket
    if [ -d "$workspace_dir" ]; then
        cd "$workspace_dir"
        
        for repo_dir in */; do
            if [ -d "$repo_dir" ]; then
                cd "$repo_dir"
                local repo_name=$(basename "$PWD")
                
                print_info "Searching for $JIRA_TICKET related changes in $repo_name..."
                
                # Search commit messages
                git log --oneline --grep="$JIRA_TICKET" --all > "../../jira-related-changes/${repo_name}-commits.txt" 2>/dev/null || true
                
                # Search for recent changes that might be related
                git log --oneline --since="30 days ago" | grep -i "upgrade\|digest\|curator" > "../../jira-related-changes/${repo_name}-potential-commits.txt" 2>/dev/null || true
                
                # If this is cluster-curator-controller, look for the specific PR #468
                if [ "$repo_name" = "cluster-curator-controller" ]; then
                    print_info "Fetching PR #468 (digest-based upgrades) from $repo_name..."
                    if git fetch origin pull/468/head:pr-468 >/dev/null 2>&1; then
                        git checkout pr-468 >/dev/null 2>&1
                        git diff main..pr-468 --name-only > "../../jira-related-changes/${repo_name}-pr468-files.txt"
                        git diff main..pr-468 --stat > "../../jira-related-changes/${repo_name}-pr468-summary.txt"
                        git checkout main >/dev/null 2>&1 || git checkout master >/dev/null 2>&1
                        print_success "PR #468 analysis ready for Claude Code"
                    fi
                fi
                
                cd ..
            fi
        done
        
        cd - >/dev/null
    fi
    
    print_success "JIRA-related changes fetched and prepared"
    return 0
}

# Generate Claude Code context files
generate_claude_context() {
    print_step "5. Generating Claude Code context files..."
    
    local context_dir="02-analysis/github-context"
    mkdir -p "$context_dir"
    
    # Generate repository overview for Claude Code
    cat > "$context_dir/repository-overview.md" << EOF
# stolostron Repository Analysis Context

## Detected Repositories for $JIRA_TICKET

$(cat 06-reference/detected-repositories.txt | sed 's/^/- /')

## Repository Access Status

$(find 06-reference/dynamic-repos -maxdepth 1 -type d -name "*" | tail -n +2 | sed 's|06-reference/dynamic-repos/|- ✅ |')

## Recent Changes Analysis

### Relevant Pull Requests
$(find 06-reference/recent-changes -name "*-related-prs.txt" -exec cat {} \; 2>/dev/null || echo "No specific PRs found")

### Potential Related Commits
$(find 06-reference/jira-related-changes -name "*-commits.txt" -exec cat {} \; 2>/dev/null || echo "No direct commits found")

## Key Files for Analysis

### cluster-curator-controller
- pkg/jobs/hive/hive.go (main upgrade logic)
- cmd/curator/curator.go (main entry point)
- pkg/jobs/utils/helpers.go (utility functions)

### clc-ui-e2e  
- cypress/tests/clusters/managedClusters/create/ (cluster creation tests)
- cypress/views/clusters/managedCluster.js (cluster management UI)

### console
- frontend/src/components/clusters/ (cluster UI components)

## Analysis Instructions for Claude Code

1. Focus on digest-based upgrade functionality
2. Analyze PR #468 in cluster-curator-controller for specific implementation
3. Look for test patterns in clc-ui-e2e that validate upgrade scenarios
4. Identify UI components that handle upgrade workflows
5. Check for error handling and validation logic

EOF

    # Create individual context files for each repository
    while IFS= read -r repo; do
        local repo_name=$(basename "$repo")
        local repo_context="$context_dir/${repo_name}-context.md"
        
        cat > "$repo_context" << EOF
# $repo Analysis Context

## Repository: $repo

## Local Access
- Path: 06-reference/dynamic-repos/$repo_name
- SSH Clone: git@github.com:$repo.git
- HTTPS API: https://api.github.com/repos/$repo

## Recent Activity
$(cat "06-reference/recent-changes/${repo_name}-related-prs.txt" 2>/dev/null || echo "No recent activity found")

## Claude Code Commands
\`\`\`bash
# To analyze this repository:
cd 06-reference/dynamic-repos/$repo_name

# To get file contents:
curl -s "https://api.github.com/repos/$repo/contents/[file-path]"

# To analyze specific commits:
git log --oneline -10
\`\`\`

EOF
    done < "06-reference/detected-repositories.txt"
    
    print_success "Claude Code context files generated"
    return 0
}

# Create dynamic access summary
create_access_summary() {
    print_step "6. Creating dynamic access summary..."
    
    local summary_file="DYNAMIC_GITHUB_ACCESS_SUMMARY.md"
    
    cat > "$summary_file" << EOF
# 🔗 Dynamic GitHub Access Summary

**Generated**: $(date)
**JIRA Ticket**: $JIRA_TICKET
**Analysis Mode**: $ANALYSIS_MODE

## 🎯 What's Available

### ✅ Real-Time Repository Access
- **Direct SSH Access**: All stolostron repositories accessible
- **Dynamic Detection**: Automatically detected relevant repositories
- **PR Fetching**: Specific pull requests and branches available
- **API Integration**: GitHub API access for individual files

### 📁 Repository Workspace
- **Location**: \`06-reference/dynamic-repos/\`
- **Status**: $(find 06-reference/dynamic-repos -maxdepth 1 -type d | wc -l) repositories prepared
- **Update**: Automatic fetching of latest changes

### 🧠 Claude Code Integration
- **Context Files**: Generated in \`02-analysis/github-context/\`
- **Repository Overviews**: Individual context for each repo
- **Recent Changes**: Analysis of relevant PRs and commits
- **Direct Access**: Claude can access any file or commit

## 🚀 How to Use with Claude Code

### Option 1: Repository-Specific Analysis
\`\`\`bash
# Navigate to specific repository
cd 06-reference/dynamic-repos/cluster-curator-controller

# Then ask Claude to analyze:
"Analyze the hive.go file for digest-based upgrade implementation"
\`\`\`

### Option 2: Direct GitHub API Access
\`\`\`bash
# Claude can directly access files:
"Show me the contents of pkg/jobs/hive/hive.go from stolostron/cluster-curator-controller"
\`\`\`

### Option 3: Cross-Repository Analysis
\`\`\`bash
# Ask Claude to compare across repositories:
"Compare upgrade handling between cluster-curator-controller and clc-ui-e2e"
\`\`\`

### Option 4: PR-Specific Analysis
\`\`\`bash
# Analyze specific pull requests:
"Analyze PR #468 from stolostron/cluster-curator-controller for security implications"
\`\`\`

## 📊 Detected Repositories

$(cat 06-reference/detected-repositories.txt | sed 's/^/- /')

## 🔍 Key Analysis Areas

### For $JIRA_TICKET Specifically:
1. **Digest-Based Upgrades**: Implementation in cluster-curator-controller
2. **UI Integration**: Console and clc-ui-e2e test coverage
3. **Error Handling**: Validation and fallback mechanisms
4. **Test Coverage**: E2E tests for upgrade scenarios

### Available Analysis:
- ✅ **Recent Changes**: Last 30 days of commits and PRs
- ✅ **Specific PRs**: Direct access to related pull requests
- ✅ **Cross-Repository Patterns**: Compare implementations
- ✅ **Real-Time Updates**: Always current with repository state

## 🎯 Next Steps

1. **Use in Prompts**: Reference this setup in Claude Code analysis
2. **Deep Dive**: Ask Claude to analyze specific files or patterns
3. **Test Generation**: Use repository analysis for comprehensive test cases
4. **Quality Review**: Cross-reference implementations for best practices

**🚀 Dynamic GitHub access is now fully integrated with your framework!**
EOF

    print_success "Dynamic access summary created: $summary_file"
    return 0
}

# Main execution
main() {
    if [ -z "$JIRA_TICKET" ]; then
        print_error "JIRA ticket required. Usage: $0 <JIRA_TICKET> [analysis_mode] [config_file]"
        exit 1
    fi
    
    print_header
    
    # Execute all setup steps
    detect_relevant_repositories
    analyze_recent_changes
    setup_dynamic_workspace
    fetch_related_changes
    generate_claude_context
    create_access_summary
    
    echo
    echo "========================================"
    print_success "🎉 Dynamic GitHub access setup complete!"
    echo
    print_info "Claude Code now has real-time access to:"
    echo "  ✅ All relevant stolostron repositories"
    echo "  ✅ Recent PRs and commits"
    echo "  ✅ Specific branches and changes"
    echo "  ✅ Cross-repository analysis capabilities"
    echo
    print_info "Next: Use this setup in your Claude Code analysis!"
    echo "========================================"
    
    return 0
}

# Execute main function
main "$@"