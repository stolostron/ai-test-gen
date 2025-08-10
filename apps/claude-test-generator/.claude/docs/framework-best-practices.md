# Framework Best Practices

## Analysis Best Practices

1. **Environment First**: Use `source setup_clc qe6` for automatic environment setup
2. **Systematic Approach**: Check ALL subtasks and linked tickets methodically
3. **Use TodoWrite**: Track progress when analyzing multiple tickets and stages
4. **Pattern Recognition**: PRs often referenced in comments with specific formats
5. **Status Awareness**: Note if PRs are open, merged, or require approval
6. **Repository Context**: Understand which repo the PRs belong to

## Test Plan Generation Best Practices

1. **Dual File Output**: ALWAYS generate both complete analysis and test-cases-only files
2. **Table Format**: Use consistent markdown table format for Polarion compatibility
3. **Complete Commands**: Include full commands with expected outputs
4. **Environment Awareness**: Design tests considering cluster state variations
5. **Validation Strategy**: Plan for cluster connectivity issues
6. **QE Integration**: Reference QE tasks and automation requirements
7. **Feature Availability Analysis**: Always validate if feature is deployed in target environment

## Workflow Execution Best Practices - BALANCED VALIDATION APPROACH

1. **Automatic Setup**: Use `source setup_clc qe6` for default environment configuration
2. **Progress Tracking**: Use TodoWrite for all workflow stages
3. **Comprehensive Analysis**: Don't skip subtasks or linked tickets
4. **FEATURE VALIDATION**: Run comprehensive feature validation to assess current deployment status
5. **COMPREHENSIVE TEST PLANS**: ALWAYS generate complete test cases assuming feature is fully implemented
6. **Balanced Reporting**: Document deployment status while providing maximum test plan value
7. **Future Readiness**: Ensure test plans are immediately executable when feature is deployed
8. **Clear Execution Guidance**: Specify what can be tested now vs. post-deployment
9. **Error Handling**: Document limitations and environmental constraints gracefully
10. **Dual File Generation**: Create both complete analysis and comprehensive test-cases files

## Common JIRA Ticket Types

- **Story**: Main feature tickets (like ACM-20640)
- **Sub-task**: Implementation pieces (often contain PR references)
- **Epic**: High-level initiatives (may block stories)
- **Bug**: Issue fixes (usually have specific PRs)
- **Task**: QE and automation work

## Key Repositories to Watch

- `stolostron/console` - ACM Console UI
- `stolostron/*` - Red Hat ACM components
- Enterprise repositories as discovered

## Enhanced Error Handling & Recovery

1. **Graceful Degradation**: Continue analysis even if some components fail
2. **Retry Logic**: Automatically retry failed operations with exponential backoff
3. **Validation Checkpoints**: Verify each step before proceeding
4. **Rollback Capability**: Restore previous state if current run fails
5. **Resource Cleanup**: Clean up partial runs and temporary files

## Input Validation & Sanitization

```bash
# JIRA Ticket ID validation
if [[ ! "$TICKET_ID" =~ ^[A-Z]+-[0-9]+$ ]]; then
    echo "❌ Invalid JIRA ticket format. Expected: PROJECT-NUMBER (e.g., ACM-22079)"
    exit 1
fi

# GitHub URL validation  
if [[ "$PR_URL" =~ ^https://github\.com/[^/]+/[^/]+/pull/[0-9]+$ ]]; then
    echo "✅ Valid GitHub PR URL"
else
    echo "⚠️ Invalid GitHub URL format, proceeding with JIRA-only analysis"
fi

# Feature name sanitization
FEATURE_SAFE=$(echo "$FEATURE_NAME" | sed 's/[^a-zA-Z0-9-]/-/g' | sed 's/--*/-/g')
```

## Improved Workflow Automation

```bash
# Pre-flight checks before starting analysis
pre_flight_check() {
    echo "🔍 Running pre-flight checks..."
    
    # Check Claude CLI availability
    if ! command -v claude &> /dev/null; then
        echo "❌ Claude CLI not found. Please install and configure."
        return 1
    fi
    
    # Check JIRA CLI availability and auth
    if ! jira issue view DUMMY-1 &> /dev/null; then
        echo "❌ JIRA CLI not authenticated. Run: jira auth login"
        return 1
    fi
    
    # Check git configuration
    if ! git config user.name &> /dev/null; then
        echo "⚠️ Git user not configured. Some features may not work."
    fi
    
    # Check disk space
    AVAILABLE_SPACE=$(df . | tail -1 | awk '{print $4}')
    if [ "$AVAILABLE_SPACE" -lt 100000 ]; then  # Less than ~100MB
        echo "⚠️ Low disk space. Consider cleaning up old runs."
    fi
    
    echo "✅ Pre-flight checks completed"
}

# Post-analysis validation
post_analysis_validation() {
    echo "🔍 Validating generated files..."
    
    # Check file sizes
    for file in "$CURRENT_RUN_DIR"/*.md; do
        if [ -f "$file" ] && [ $(wc -c < "$file") -lt 1000 ]; then
            echo "⚠️ $(basename $file) seems unusually small"
        fi
    done
    
    # Validate markdown syntax
    if command -v markdownlint &> /dev/null; then
        markdownlint "$CURRENT_RUN_DIR"/*.md || echo "⚠️ Markdown syntax issues detected"
    fi
    
    # Check for required sections
    if ! grep -q "## Test Case" "$CURRENT_RUN_DIR/Test-Cases.md"; then
        echo "⚠️ No test cases found in Test-Cases.md"
    fi
    
    echo "✅ File validation completed"
}
```

## Critical Requirements & Dependencies

- **Claude CLI**: Version 1.0+ with proper authentication
- **JIRA CLI**: Configured with valid API token
- **Git**: For repository access and change tracking
- **Shell**: Bash 4.0+ or Zsh for script compatibility
- **Disk Space**: Minimum 1GB free for run storage
- **Network**: Stable connection for GitHub/JIRA API calls

## Enhanced Troubleshooting Guide

1. **Permission Issues**: 
   - Check file/directory permissions: `ls -la runs/`
   - Ensure write access: `touch runs/.test && rm runs/.test`

2. **API Rate Limits**:
   - GitHub: Max 5000 requests/hour (authenticated)
   - JIRA: Varies by instance, typically 300 requests/hour
   - Implement automatic backoff when limits hit

3. **File System Issues**:
   - Monitor for special characters in filenames
   - Handle long file paths gracefully
   - Implement atomic file operations

4. **Network Connectivity**:
   - Detect connectivity issues and degrade gracefully
   - Cache frequently accessed data where appropriate

5. **Memory Management**:
   - Monitor for large file processing
   - Implement streaming for big datasets
   - Clear temporary files regularly

## Framework Advancements

This framework represents significant advancement in automated test generation, combining:
- AI capabilities with intelligent validation
- Adaptive learning and human oversight
- Real-world robustness across development/testing scenarios
- Ability to handle missing features and adapt to different environments
- Dual output generation for different stakeholder needs
- Feature deployment verification and environment awareness

The framework's ability to handle missing features, adapt to different environments, verify deployment status, and generate both comprehensive analysis and clean test cases makes it invaluable for QE teams working on complex enterprise software like Advanced Cluster Management.
