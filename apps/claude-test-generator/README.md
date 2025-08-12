# Intelligent Test Analysis Engine

> **AI-powered test analysis and generation system for ACM/OCM components**

An intelligent system that analyzes software features and generates comprehensive E2E test plans. Designed specifically for Red Hat Advanced Cluster Management (ACM) and Open Cluster Management (OCM) testing scenarios.

## What This Framework Does

The Intelligent Test Analysis Engine automatically:

1. **Analyzes JIRA tickets** - Extracts business requirements and technical specifications
2. **Processes GitHub PRs** - Understands code changes and implementation details  
3. **Generates E2E test plans** - Creates comprehensive test cases with realistic expected outputs
4. **Assesses deployment readiness** - Determines if features are available in test environments
5. **Provides structured output** - Delivers both detailed analysis and clean test cases

### Key Capabilities

- **Smart Test Scoping**: Focuses only on NEW/CHANGED functionality, avoiding redundant testing
- **E2E Coverage**: Complete end-to-end workflows for comprehensive validation
- **Environment Assessment**: Evaluates feature availability and deployment status
- **Multiple Output Formats**: Both detailed analysis and clean test cases for different use cases
- **Feedback Loop Integration**: Human review triggers and continuous improvement

## How It Works

The framework follows a 5-stage intelligent workflow:

1. **Environment Setup**: Validates cluster access and tool availability
2. **JIRA Analysis**: Extracts ticket details, business context, and requirements
3. **AI Reasoning**: Applies smart scoping and strategic test intelligence  
4. **Test Generation**: Creates E2E test cases with proper format and realistic outputs
5. **Analysis Report**: Provides deployment assessment and complete documentation

### Output Structure

Each run generates organized outputs:
```
runs/ACM-XXXXX/run-###-YYYYMMDD-HHMM/
├── Test-Cases.md           # Clean test cases (Description, Setup, Steps/Expected Results)
├── Complete-Analysis.md    # Full analysis with deployment assessment
└── metadata.json          # Run details and quality metrics
```

## Simplest Way to Run

### Prerequisites
- Claude Code CLI configured
- Access to ACM test environment
- JIRA ticket available for analysis

### Basic Execution
```bash
# Navigate to the framework
cd apps/claude-test-generator

# Run analysis on any ACM JIRA ticket
analyze_ticket ACM-22079

# Or with custom environment  
USER_ENVIRONMENT=qe7 analyze_ticket ACM-22079
```

### What Happens
1. Framework connects to your specified environment (default: qe6)
2. Analyzes the JIRA ticket for business and technical requirements
3. Generates comprehensive E2E test plan focused on NEW functionality
4. Creates both detailed analysis and clean test cases
5. Provides deployment assessment (feature available or not)

### Expected Output
- **Execution Time**: 5-10 minutes
- **Test Cases**: 3-5 comprehensive E2E scenarios  
- **Coverage**: All NEW functionality with realistic validation steps
- **Format**: Ready for manual execution or Polarion import

## Configuration Options

The framework can be configured in several ways:

### 1. Environment Selection
```bash
# Use default environment (qe6)
analyze_ticket ACM-22079

# Specify different environment
USER_ENVIRONMENT=qe7 analyze_ticket ACM-22079
USER_ENVIRONMENT=qe8 analyze_ticket ACM-22079
```

**Why Configure Environment?**
- Different environments may have different feature deployment status
- Allows testing against specific cluster configurations
- Enables validation across multiple test environments

### 2. Test Scoping Configuration
Located in `.claude/prompts/test-scoping-rules.md`:

- **Smart Scoping Rules**: Define what constitutes "new" vs "existing" functionality
- **E2E Focus Requirements**: Specify end-to-end workflow coverage expectations
- **Expected Output Format**: Control test case structure and validation criteria

**Why Configure Scoping?**
- Ensures tests focus on changed functionality only
- Reduces redundant testing of stable components
- Maintains consistent test coverage standards

### 3. Output Format Configuration
Located in `.claude/templates/`:

- **YAML Sample Templates**: Control expected result formatting
- **Environment Configuration**: Standardize setup and validation procedures
- **Test Case Structure**: Define Description, Setup, and table formats

**Why Configure Output?**
- Maintains consistency across different testers
- Ensures compatibility with test management systems
- Provides realistic, actionable test steps

### 4. Feedback Loop Configuration
Located in `.claude/workflows/feedback-loop-system.md`:

- **Review Triggers**: When to request human feedback
- **Quality Thresholds**: Minimum quality score requirements  
- **Improvement Integration**: How to apply human feedback

**Why Configure Feedback?**
- Enables continuous quality improvement
- Integrates human expertise with AI generation
- Prevents quality regression over time

## Integration with Intelligent Framework


### Current Relationship

Both frameworks exist in the same repository but serve different purposes:

| Framework | Primary Use | Complexity | Team Focus |
|-----------|-------------|------------|------------|
| **claude-test-generator** | Quick E2E test generation | Simple, focused | Day-to-day QE work |
| **intelligent-test-framework** | Comprehensive analysis | Complex, full-featured | Advanced research/analysis |

### Integration Details

**Shared Elements:**
- Both use similar JIRA analysis approaches
- Both generate test plans for ACM/OCM components
- Both store outputs in organized run structures
- Both support multiple environment configurations

**Different Approaches:**
- **claude-test-generator**: Claude-based, fast, focused on immediate test generation
- **intelligent-test-framework**: Shell-script based, comprehensive, includes research and automation

**When to Use Which:**
- **Daily QE Work**: Use claude-test-generator for quick, reliable test plan generation
- **Research Projects**: Use intelligent-test-framework for comprehensive analysis with automation
- **Team Collaboration**: claude-test-generator is more accessible for general team use

### Migration Path

The frameworks complement each other:
1. Start with claude-test-generator for immediate test generation needs
2. Use intelligent-test-framework for complex research or automation projects
3. Both can analyze the same JIRA tickets with different depth/approach

There's no technical dependency - they're separate tools that can be used independently based on your specific needs.

## Project Structure

```
claude-test-generator/
├── README.md                    # This file
├── CLAUDE.md                    # Claude configuration
├── .claude/                     # Framework configuration
│   ├── prompts/                 # Test scoping and generation rules
│   ├── templates/               # Output format templates
│   ├── workflows/               # Feedback loop and process definitions
│   └── docs/                    # Implementation guidance
├── runs/                        # Generated test runs by ticket
│   └── <TICKET-ID>/             # Organized by JIRA ticket
│       ├── run-XXX-YYYYMMDD-HHMM/ # Timestamped executions
│       │   ├── Test-Cases.md    # Clean test cases
│       │   ├── Complete-Analysis.md # Full analysis
│       │   └── metadata.json    # Run metadata
│       └── latest -> run-XXX    # Symlink to latest run
├── examples/                    # Example outputs
└── docs/                        # Additional documentation
```

## Best Practices

### Input Optimization
1. **Clear JIRA Details**: Ensure tickets have acceptance criteria and complete descriptions
2. **Environment Access**: Verify cluster connectivity before running analysis
3. **Feature Context**: Understand whether feature is deployed in target environment

### Output Usage
1. **Review Generated Plans**: Always validate AI-generated test cases for accuracy
2. **Adapt to Environment**: Modify generic commands for your specific cluster setup
3. **Execute Systematically**: Follow test cases in order for proper validation flow

### Quality Assurance
1. **Check Deployment Status**: Verify if features are available before manual testing
2. **Validate Expected Outputs**: Ensure expected results match actual environment behavior
3. **Provide Feedback**: Use feedback loop system to improve future generations

## Getting Support

### Documentation
- **Quick Start**: See `docs/quick-start.md` for detailed setup guidance
- **Configuration**: Check `.claude/` directory for customization options
- **Examples**: Review `examples/` for sample outputs and patterns

### Troubleshooting
- **Environment Issues**: Verify cluster access and tool availability
- **Output Quality**: Check JIRA ticket completeness and feature deployment status
- **Framework Errors**: Review metadata.json for execution details and error logs

---

**Framework Version**: 1.0  
**Maintained by**: ACM QE Team  
**Integrations**: Claude Code AI, GitHub, JIRA, OpenShift CLI