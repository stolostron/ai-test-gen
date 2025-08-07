#!/bin/bash
# Automated Research Update Script
# Updates all research sources with latest information

echo "🔄 Updating comprehensive research sources..."

# Update cloned repositories
for repo_dir in acm-docs/*/; do
    if [ -d "$repo_dir/.git" ]; then
        echo "Updating $(basename "$repo_dir")..."
        cd "$repo_dir"
        git pull origin main 2>/dev/null || true
        cd - > /dev/null
    fi
done

# Update main ClusterCurator repository
if [ -d "../../stolostron-cluster-curator-controller/.git" ]; then
    echo "Updating ClusterCurator repository..."
    cd "../../stolostron-cluster-curator-controller"
    git pull origin main 2>/dev/null || true
    cd - > /dev/null
fi

echo "✅ Research sources updated!"
