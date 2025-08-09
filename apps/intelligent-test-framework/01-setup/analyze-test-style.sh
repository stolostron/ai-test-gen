#!/bin/bash
# Automated Test Style Analyzer
# Analyzes user-provided samples and generates style-matched templates

set -e

echo "🔍 Analyzing Test Style Preferences..."
echo "===================================="

STYLE_DIR="04-implementation/test-style-templates"
SAMPLES_DIR="$STYLE_DIR/user-samples"
PATTERNS_DIR="$STYLE_DIR/analyzed-patterns"
TEMPLATES_DIR="$STYLE_DIR/generated-templates"

# Check for user samples
SAMPLE_COUNT=$(find "$SAMPLES_DIR" -name "*.html" -o -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.txt" | wc -l)

echo "📊 Found $SAMPLE_COUNT sample files for analysis"

if [ "$SAMPLE_COUNT" -eq 0 ]; then
    echo ""
    echo "❌ No sample files found!"
    echo ""
    echo "Please provide sample test cases by:"
    echo "1. Adding files to: $SAMPLES_DIR"
    echo "2. Following the guide: $STYLE_DIR/test-style-collection-guide.md"
    echo "3. Or filling out: $SAMPLES_DIR/style-preferences-questionnaire.md"
    exit 1
fi

# Analyze file formats
echo ""
echo "📋 Sample Analysis:"
for format in html md json yaml txt; do
    count=$(find "$SAMPLES_DIR" -name "*.$format" | wc -l)
    if [ "$count" -gt 0 ]; then
        echo "  ✓ $format files: $count"
    fi
done

# Create analysis report
cat > "$PATTERNS_DIR/style-analysis-report.md" << EOF
# Test Style Analysis Report

## Sample Files Analyzed
$(find "$SAMPLES_DIR" -type f | sed 's|.*/|  - |')

## Format Distribution
$(for format in html md json yaml txt; do
    count=$(find "$SAMPLES_DIR" -name "*.$format" | wc -l)
    if [ "$count" -gt 0 ]; then
        echo "- $format: $count files"
    fi
done)

## Analysis Date
$(date)

## Detected Patterns
[This section will be populated by Claude Code analysis]

## Generated Templates
[Templates based on analysis will be listed here]

## Claude Code Usage Instructions
Use these templates with Claude Code by referencing:
@file:04-implementation/test-style-templates/generated-templates/

## Style-Aware Prompts
Generated prompts that understand your team's style preferences.
