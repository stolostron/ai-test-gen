#!/bin/bash

# GitHub Investigation Helper Script
# Enhanced repository access for Complete Investigation Protocol

set -e

INVESTIGATION_DIR="/tmp/claude-investigation-repos"
TICKET_ID="${1:-}"
SEARCH_TERMS="${2:-}"

if [ -z "$TICKET_ID" ]; then
    echo "Usage: $0 <TICKET_ID> [SEARCH_TERMS]"
    echo "Example: $0 ACM-22079 'desiredUpdate,digest,upgrade'"
    exit 1
fi

echo "🔍 Starting GitHub Investigation for $TICKET_ID"

# Create investigation directory
mkdir -p "$INVESTIGATION_DIR"
cd "$INVESTIGATION_DIR"

# Function to clone or update repository
clone_or_update_repo() {
    local repo_name="$1"
    local repo_url="git@github.com:stolostron/${repo_name}.git"
    
    if [ -d "$repo_name" ]; then
        echo "📂 Updating existing repo: $repo_name"
        cd "$repo_name"
        git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || echo "⚠️ Could not update $repo_name"
        cd ..
    else
        echo "📥 Cloning repo: $repo_name"
        git clone "$repo_url" "$repo_name" 2>/dev/null || echo "⚠️ Could not clone $repo_name"
    fi
}

# Clone key repositories for investigation
echo "📦 Cloning/updating stolostron repositories..."
clone_or_update_repo "cluster-curator-controller"
clone_or_update_repo "multicloud-operators-subscription"
clone_or_update_repo "console"
clone_or_update_repo "ocm"

# Search for ticket references
echo "🔍 Searching for $TICKET_ID in commit messages..."
for repo in */; do
    if [ -d "$repo/.git" ]; then
        echo "--- Repository: $repo ---"
        cd "$repo"
        git log --oneline --grep="$TICKET_ID" --all || echo "No commits found for $TICKET_ID"
        cd ..
    fi
done

# Search for code implementations
if [ -n "$SEARCH_TERMS" ]; then
    echo "🔍 Searching for implementation terms: $SEARCH_TERMS"
    IFS=',' read -ra TERMS <<< "$SEARCH_TERMS"
    for term in "${TERMS[@]}"; do
        echo "--- Searching for: $term ---"
        for repo in */; do
            if [ -d "$repo" ]; then
                echo "Repository: $repo"
                grep -r "$term" "$repo" --include="*.go" --include="*.yaml" --include="*.yml" | head -5 || echo "No matches"
            fi
        done
    done
fi

# Search for recent commits (last 30 days)
echo "🔍 Recent commits (last 30 days) potentially related to $TICKET_ID..."
for repo in */; do
    if [ -d "$repo/.git" ]; then
        echo "--- Repository: $repo ---"
        cd "$repo"
        git log --since="30 days ago" --oneline --grep="upgrade\|curator\|digest" | head -5 || echo "No recent related commits"
        cd ..
    fi
done

echo "✅ GitHub Investigation complete for $TICKET_ID"
echo "📁 Investigation results stored in: $INVESTIGATION_DIR"