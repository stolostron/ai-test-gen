#!/bin/bash

# Z-Stream Analysis Engine - Repository Cleanup Script
# Removes temporary repositories while preserving analysis results

echo "🧹 Z-Stream Analysis Engine - Repository Cleanup"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ] || [ ! -d ".claude" ]; then
    echo "❌ Error: Please run this script from the z-stream-analysis directory"
    exit 1
fi

# Function to safely remove temp repositories
cleanup_temp_repos() {
    if [ -d "temp-repos" ]; then
        echo "📁 Found temp-repos directory..."
        
        # Count items before cleanup
        REPO_COUNT=$(find temp-repos/ -mindepth 1 -maxdepth 1 -type d ! -name "analysis-results" | wc -l)
        
        if [ "$REPO_COUNT" -gt 0 ]; then
            echo "🗑️  Removing $REPO_COUNT cloned repository directories..."
            
            # Remove repository directories but preserve analysis-results
            find temp-repos/ -mindepth 1 -maxdepth 1 -type d ! -name "analysis-results" -exec rm -rf {} + 2>/dev/null
            
            echo "✅ Removed cloned repositories"
        else
            echo "ℹ️  No repository directories to clean"
        fi
        
        # Remove empty temp-repos directory if no content remains
        if [ -z "$(ls -A temp-repos/ 2>/dev/null)" ]; then
            rmdir temp-repos/
            echo "✅ Removed empty temp-repos directory"
        else
            echo "ℹ️  Preserved temp-repos/analysis-results/"
        fi
    else
        echo "ℹ️  No temp-repos directory found"
    fi
}

# Function to clean up stray git repositories
cleanup_stray_git() {
    echo "🔍 Checking for stray git repositories..."
    
    # Find git directories (excluding main repo)
    STRAY_GIT=$(find . -name ".git" -type d | grep -v "^\./\.git$" | wc -l)
    
    if [ "$STRAY_GIT" -gt 0 ]; then
        echo "🗑️  Found $STRAY_GIT stray git repositories, removing..."
        find . -name ".git" -type d | grep -v "^\./\.git$" | xargs rm -rf 2>/dev/null
        echo "✅ Removed stray git repositories"
    else
        echo "ℹ️  No stray git repositories found"
    fi
}

# Function to verify analysis preservation
verify_analysis_preserved() {
    echo "🔍 Verifying analysis results are preserved..."
    
    if [ -d "runs" ] && [ "$(ls -A runs/ 2>/dev/null)" ]; then
        ANALYSIS_COUNT=$(ls runs/ 2>/dev/null | wc -l)
        echo "✅ Analysis results preserved: $ANALYSIS_COUNT analysis runs"
    else
        echo "⚠️  Warning: No analysis results found in runs/ directory"
    fi
}

# Main cleanup execution
echo "🚀 Starting cleanup process..."
echo ""

cleanup_temp_repos
echo ""

cleanup_stray_git
echo ""

verify_analysis_preserved
echo ""

# Final status report
echo "📊 Cleanup Summary:"
echo "=================="
if [ -d "temp-repos" ]; then
    echo "📁 temp-repos: $(du -sh temp-repos/ 2>/dev/null | cut -f1) (analysis results preserved)"
else
    echo "📁 temp-repos: Removed (was empty)"
fi

if [ -d "runs" ]; then
    echo "📊 Analysis runs: $(ls runs/ 2>/dev/null | wc -l) preserved"
else
    echo "📊 Analysis runs: None found"
fi

echo "🎯 Git repositories: Only main repository preserved"
echo ""
echo "✅ Cleanup completed successfully!"
echo "ℹ️  All analysis results and metadata have been preserved."