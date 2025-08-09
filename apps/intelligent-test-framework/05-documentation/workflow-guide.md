# ACM-22079 Claude Analysis Workflow Guide

## Complete Step-by-Step Process

This guide provides detailed instructions for using Claude Code CLI to analyze ACM-22079 and generate comprehensive test cases.

## Prerequisites Checklist

Before starting, ensure you have:
- [ ] Claude Code CLI installed and configured
- [ ] Environment variables set correctly
- [ ] Google Cloud authentication working
- [ ] Access to ACM automation codebase
- [ ] Project structure initialized

**If any are missing, run**: `./01-setup/environment-check.sh`

## Phase 1: Project Setup and Initialization

### Step 1: Environment Verification
```bash
# Navigate to project directory
cd /Users/ashafi/Documents/work/ai/claude/ACM-22079

# Run environment check
./01-setup/environment-check.sh
```

**Expected Result**: All checks pass with green checkmarks

### Step 2: Project Initialization
```bash
# Initialize the complete project
./01-setup/project-init.sh
```

**Expected Result**: 
- Project structure created
- Claude Code tested
- Session tracking initialized
- Workflow status file created

### Step 3: Verify Setup
```bash
# Check project structure
ls -la

# View current session
cat 02-analysis/sessions/session_*.md

# Check workflow status
cat workflow-status.md
```

## Phase 2: Initial Analysis

### Step 4: Start Claude Code Interactive Session
```bash
# Start interactive Claude session
claude
```

**In Claude interactive mode:**
```
/status
```
Verify connection and project configuration.

### Step 5: Run Initial Analysis
Copy and paste the content from:
```bash
cat 02-analysis/prompts/initial-analysis.txt
```

**Paste this prompt into Claude Code interactive session**.

**Expected Output**: Comprehensive analysis covering:
- Conceptual understanding of digest-based upgrades
- Technical implementation details
- ACM integration points
- Initial test case recommendations

### Step 6: Save Initial Results
```bash
# Exit Claude (Ctrl+C or /exit)
# Create results file
cat > 03-results/feature-analysis.md << 'EOF'
# ACM-22079 Feature Analysis Results
[Paste Claude's response here]
EOF
```

## Phase 3: Deep Technical Analysis

### Step 7: Code Deep Dive Session
```bash
# Start new Claude session
claude
```

Use the prompt from:
```bash
cat 02-analysis/prompts/code-deep-dive.txt
```

**Expected Output**: Detailed technical analysis of:
- validateUpgradeVersion function changes
- ManagedClusterView integration
- retreiveAndUpdateClusterVersion modifications
- Error handling improvements
- Security and performance considerations

### Step 8: Save Technical Analysis
```bash
cat > 03-results/implementation-details.md << 'EOF'
# ACM-22079 Implementation Details
[Paste Claude's technical analysis here]
EOF
```

## Phase 4: Comprehensive Test Generation

### Step 9: Generate Test Cases
```bash
# Start new Claude session for test generation
claude
```

Use the prompt from:
```bash
cat 02-analysis/prompts/test-generation.txt
```

**Expected Output**: Complete test suite including:
- Unit test scenarios
- Integration test cases
- E2E test scenarios
- Error handling tests
- Performance tests

### Step 10: Organize Test Results
```bash
# Create organized test case files
cat > 03-results/test-cases/unit-tests.md << 'EOF'
# Unit Test Cases for ACM-22079
[Paste unit test section from Claude's response]
EOF

cat > 03-results/test-cases/integration-tests.md << 'EOF'
# Integration Test Cases for ACM-22079
[Paste integration test section from Claude's response]
EOF

cat > 03-results/test-cases/e2e-tests.md << 'EOF'
# E2E Test Cases for ACM-22079
[Paste E2E test section from Claude's response]
EOF

cat > 03-results/test-cases/acm-specific-tests.md << 'EOF'
# ACM-Specific Test Cases for ACM-22079
[Paste ACM-specific test section from Claude's response]
EOF
```

## Phase 5: Implementation Planning

### Step 11: Generate Implementation Code
```bash
# Start Claude session for implementation
claude
```

Use this prompt:
```
Based on our analysis of ACM-22079, generate implementation-ready code for:

1. Cypress E2E test suite for ClusterCurator digest-based upgrades
2. Go unit tests for validateUpgradeVersion function
3. Test data generation scripts for disconnected environments
4. Jenkins pipeline configuration updates
5. Test automation helper utilities

Focus on ACM QE testing patterns and existing automation frameworks.
Reference the ACM automation codebase at /Users/ashafi/Documents/work/automation
```

### Step 12: Save Implementation Files
```bash
# Create implementation files based on Claude's output
mkdir -p 04-implementation/cypress-tests/integration
mkdir -p 04-implementation/test-data
mkdir -p 04-implementation/automation-scripts

# Save each implementation file
# [Create files based on Claude's generated code]
```

## Phase 6: Documentation and Integration

### Step 13: Create Team Documentation
```bash
# Generate team sharing documentation
claude
```

Use this prompt:
```
Create comprehensive documentation for the ACM QE team covering:

1. Summary of ACM-22079 analysis findings
2. Test implementation guide with step-by-step instructions
3. Integration instructions for existing ACM test automation
4. Troubleshooting guide for common issues
5. Best practices for digest-based upgrade testing

Format for easy team consumption and implementation.
```

### Step 14: Update Project Status
```bash
# Update workflow status
nano workflow-status.md
# Mark completed phases and update progress
```

### Step 15: Create Team Handoff Package
```bash
# Create comprehensive summary
cat > 03-results/recommendations.md << 'EOF'
# ACM-22079 Implementation Recommendations
[Paste team documentation from Claude]
EOF

# Create quick reference
cat > 05-documentation/team-sharing.md << 'EOF'
# ACM-22079 Team Sharing Package
[Include summary, key findings, and next steps]
EOF
```

## Phase 7: Validation and Quality Assurance

### Step 16: Review and Validate Results
```bash
# Review all generated files
find . -name "*.md" -exec echo "=== {} ===" \; -exec head -10 {} \; -exec echo \;

# Validate completeness
./validate-results.sh  # [Create this script to check deliverables]
```

### Step 17: Test Implementation Validation
```bash
# If implementing immediately, run initial validation
cd /Users/ashafi/Documents/work/automation

# Test any generated automation scripts
# Validate test data generation
# Check CI/CD pipeline configurations
```

## Advanced Usage Patterns

### Iterative Analysis
For complex aspects, use multiple focused sessions:

```bash
# Session 1: Focus on specific function
claude --print "Analyze only the validateUpgradeVersion function changes in ACM-22079"

# Session 2: Focus on testing
claude --print "Generate only unit tests for digest discovery logic in ACM-22079"

# Session 3: Focus on integration
claude --print "How to integrate ACM-22079 tests into existing Cypress automation?"
```

### Non-Interactive Quick Queries
For specific questions during development:

```bash
# Quick code explanation
claude --print "Explain why force flag is not needed with digest-based upgrades in ACM-22079"

# Quick test idea
claude --print "Generate test case for conditionalUpdates array processing in ACM-22079"

# Quick troubleshooting
claude --print "What could cause digest discovery to fail in disconnected environment for ACM-22079?"
```

### Session Management
Track your progress with session logs:

```bash
# View current session
ls 02-analysis/sessions/

# Create session summary
echo "Session completed: $(date)" >> 02-analysis/sessions/session_$(date +%Y%m%d_%H%M%S).md
echo "Key outputs: [list key deliverables]" >> 02-analysis/sessions/session_$(date +%Y%m%d_%H%M%S).md
```

## Troubleshooting Common Issues

### Claude Code Connection Issues
```bash
# Clear command cache
hash -r

# Test connection
claude --print "test connection"

# Check environment
env | grep ANTHROPIC
```

### Session Context Issues
```bash
# Restart Claude with fresh context
claude
/init

# Provide context manually
# [Copy relevant background information]
```

### Large Output Management
```bash
# For very long Claude responses, save incrementally
claude > temp_output.txt
# Then process sections into appropriate files
```

## Quality Checkpoints

### After Each Phase
- [ ] Outputs saved to appropriate directories
- [ ] Session logged with timestamp and key findings
- [ ] Workflow status updated
- [ ] Key insights documented

### Before Team Handoff
- [ ] All deliverables complete and organized
- [ ] Documentation clear and actionable
- [ ] Implementation code validated
- [ ] Next steps clearly defined

## Expected Timeline

- **Phase 1-2 (Setup & Initial Analysis)**: 30-45 minutes
- **Phase 3 (Technical Deep Dive)**: 45-60 minutes
- **Phase 4 (Test Generation)**: 60-90 minutes
- **Phase 5 (Implementation)**: 90-120 minutes
- **Phase 6-7 (Documentation & Validation)**: 45-60 minutes

**Total**: 4-6 hours for comprehensive analysis and implementation

## Success Criteria

✅ **Complete Understanding**: Thorough grasp of ACM-22079 feature and implementation  
✅ **Comprehensive Test Suite**: Ready-to-implement test cases for all scenarios  
✅ **Implementation Code**: Working automation code for ACM QE frameworks  
✅ **Team Documentation**: Clear guidance for QE team adoption  
✅ **Process Documentation**: Reusable workflow for future JIRA analysis  

## Next Steps After Completion

1. **Immediate**: Share results with ACM QE team
2. **Short-term**: Implement test cases in ACM automation
3. **Medium-term**: Validate with actual ClusterCurator deployments
4. **Long-term**: Use process for other JIRA ticket analysis

---
**Remember**: This is a comprehensive workflow. Adjust based on your specific needs and time constraints. The modular approach allows you to focus on specific phases as needed.