# Usage Examples and Best Practices

This document provides practical examples and best practices for using the Z-Stream Analysis Engine.

## Command Examples

### Application-Specific Commands

When working directly in this application directory:

```bash
# Enterprise AI Services Integration (V4.0)
# Pure AI workflow with comprehensive services - 100% script-free, self-contained operation

# Quick status check
ls -la runs/  # View recent analysis results

# Enterprise AI Services (natural language interface) - ALWAYS COMPREHENSIVE BY DEFAULT
# When given ANY Jenkins URL, Claude automatically performs complete analysis including:
# - Branch validation and correct repository cloning
# - Environment validation and cluster connectivity  
# - Real repository analysis with exact code examination
# - Cross-service evidence correlation and definitive verdict generation
# - Precise automation fix generation with verified implementations
# - Comprehensive reporting saved to runs/ directory

# Simply provide Jenkins URL - full analysis is performed automatically:
"Analyze https://jenkins-url/job/pipeline/123/"
"https://jenkins-url/job/pipeline/123/"  # Even just the URL triggers full analysis

# AI Cleanup Service (automatic and on-demand)
"Clean up temporary repositories after analysis"
"Remove cloned repositories while preserving analysis results"
"Execute post-analysis cleanup"

# View enhanced documentation
cat README.md               # Simple user guide: What it does + How to use it
cat docs/framework-architecture.md    # How it works: Clear step-by-step explanation
cat docs/configuration-guide.md       # Setup guide: Configuration and customization
cat docs/use-cases-guide.md           # Examples: Real-world scenarios and outcomes
```

### Real-World Examples

```bash
# From root repository - immediate analysis
/analyze-pipeline-failures https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc-clc-e2e-pipeline/3223/

# Pipeline ID shorthand
/analyze-pipeline-failures clc-e2e-pipeline-3223 --extract-artifacts

# Pattern analysis across builds
/analyze-pipeline-failures clc-e2e-pipeline-3223 --pattern-analysis

# Comprehensive workflow analysis
/analyze-workflow pipeline-failure clc-e2e-pipeline-3223 --comprehensive

# Direct application usage (AI-powered)
cd apps/z-stream-analysis
"Analyze this Jenkins pipeline failure: https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc-clc-e2e-pipeline/3223/"
```

## Team-Specific Workflows

### For QE Teams (V4.0 AI Services)
```bash
# Daily failure triage with environment validation
/analyze-pipeline-failures pipeline-XXXX --comprehensive-ai-analysis

# Comprehensive investigation with all AI services
cd apps/z-stream-analysis
"Execute comprehensive AI investigation with environment validation and repository analysis for pipeline failure: <jenkins-url>"

# Precise fix generation based on real repository analysis
"Generate precise automation fixes based on real repository analysis for this failure: <jenkins-url>"
```

### For DevOps Teams (V4.0 AI Services)
```bash
# Infrastructure failure analysis with environment validation
/analyze-workflow ci-debug <jenkins-url> --ai-environment-validation

# Comprehensive analysis with real repository integration
/analyze-pipeline-failures pipeline-XXXX --real-repository-analysis --precise-fixes

# Pattern analysis with real repository examination
/analyze-pipeline-failures pipeline-XXXX --real-repository-analysis --precise-fixes
```

### For Management (V4.0 AI Services)
```bash
# Executive reporting with definitive verdicts
/analyze-pipeline-failures pipeline-XXXX --ai-executive-summary
# Generates comprehensive reports with environment validation, repository analysis, and fix implementation status
# Location: runs/pipeline-XXXX_YYYYMMDD_HHMMSS/Detailed-Analysis.md

# Business impact assessment with AI services metrics
"Provide executive summary with business impact assessment and AI services performance metrics for pipeline failure: <jenkins-url>"
```

## Setup Verification

### Quick Setup Verification

```bash
# Navigate to application
cd apps/z-stream-analysis

# Verify clean structure
ls -la
tree . -L 2

# Check standardized analysis examples  
cat runs/clc-e2e-pipeline-3223_20250812_182522/Detailed-Analysis.md
ls -la runs/clc-e2e-pipeline-3223_*/

# Review comprehensive documentation
cat README.md                          # Simple user guide: What it does + How to use it
cat docs/framework-architecture.md     # How it works: Clear step-by-step explanation
cat docs/configuration-guide.md        # Setup guide: Configuration and customization
cat docs/use-cases-guide.md            # Examples: Real-world scenarios and outcomes

# Review AI workflows
ls .claude/workflows/

# Verify environment configuration (optional)
cat .env
```

## Integration Patterns

### Integration with Unified Commands

**Root Repository Usage (Recommended):**
- Use `/analyze-pipeline-failures` for immediate analysis
- Use `/analyze-workflow pipeline-failure` for intelligent routing
- All results stored in `apps/z-stream-analysis/runs/`

**Direct Application Usage (Advanced):**
- `cd apps/z-stream-analysis` for specialized features
- Access to AI-powered templates and enhanced analysis
- Custom analysis configurations and debugging

### Team Collaboration (V4.0 AI Services)
- **Standardized Reports**: All analysis follows consistent single comprehensive report format with real repository analysis integration
- **Timestamped History**: Multiple analysis runs preserved with unique timestamps and real repository analysis metrics
- **Actionable Insights**: Reports include precise automation fixes with exact file paths and line numbers
- **Environment Validation**: Concrete evidence of product functionality vs automation issues
- **Real Repository Integration**: Actual automation repository cloning and code examination for precise analysis
- **Cross-Service Evidence**: Multi-source evidence correlation with real repository validation for definitive classification
- **Knowledge Base**: Real code patterns automatically captured and referenced across analysis runs with verified implementations

## Notification Integration Examples
- **Slack Integration**: Automated failure notifications with comprehensive analysis summaries and precise automation fixes based on real repository analysis
- **Email Reports**: Scheduled executive summaries with definitive verdicts and fix implementation status
- **JIRA Integration**: Automatic ticket creation for critical failures with environment validation results
- **Dashboard Integration**: Export comprehensive analysis data including AI services metrics and fix success rates
- **Pull Request Integration**: Automated PR creation and tracking for generated automation fixes