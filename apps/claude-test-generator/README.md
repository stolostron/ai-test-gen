# Intelligent Test Analysis Engine

> **AI-powered test analysis and generation system for ACM/OCM components**

**Latest Version**: AI-powered framework with integrated investigation, validation, and generation services
**Framework Status**: Production-ready with complete AI service integration and intelligent quality assurance

An intelligent system that uses integrated AI services to analyze software features and generate comprehensive E2E test plans. Designed specifically for Red Hat Advanced Cluster Management (ACM) and Open Cluster Management (OCM) testing scenarios.

## 🚨 CRITICAL FRAMEWORK POLICY

**⚠️ MANDATORY INTERNAL vs EXTERNAL USAGE**:
- **Framework Internal**: Uses `setup_clc` and `login_oc` scripts for robust environment operations
- **Generated Test Cases**: ALWAYS show generic `oc login <cluster-url>` commands for team usability
- **Final Reports**: NEVER mention setup_clc or login_oc scripts - use standard OpenShift patterns
- **End User Experience**: Clean, professional test cases without internal framework details

## What This Framework Does

The AI-powered Test Analysis Engine automatically:

1. **🔍 AI Documentation Service** - JIRA hierarchy analysis with recursive link traversal
2. **📊 AI GitHub Investigation Service** - PR discovery and implementation validation  
3. **⚙️ AI Schema Service** - Dynamic CRD analysis and intelligent YAML generation
4. **✅ AI Validation Service** - Automated quality assurance and compliance verification
5. **📝 Structured Output** - Delivers both detailed analysis and clean test cases with AI-generated examples

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

# Ask Claude to analyze any ACM JIRA ticket
# Claude will automatically use AI services for complete analysis
# Example: "Analyze ACM-22079"
```

**🚨 CRITICAL**: Framework uses internal setup_clc/login_oc scripts but generated test cases show generic `oc login <cluster-url>` commands for team usability.

### AI-Powered Process
1. **Environment Setup**: Framework connects to specified environment (default: qe6) using internal utilities
2. **AI Investigation**: Automatic JIRA + GitHub + Internet research via AI Documentation and GitHub Investigation Services
3. **AI Validation**: Real-time schema and deployment validation via AI Schema Service
4. **AI Generation**: Enhanced test cases with AI-generated YAML samples and Expected Results
5. **AI Quality Assurance**: Automated validation via AI Validation Service (escaped pipes, ManagedClusterView guidance, server-side YAML validation)

### Expected Output
- **Execution Time**: 5-10 minutes
- **Test Cases**: 3-5 comprehensive E2E scenarios  
- **Coverage**: All NEW functionality with realistic validation steps
- **Format**: Ready for manual execution or Polarion import

## Configuration Options

The framework can be configured in several ways:

### 1. Environment Selection
**Ask Claude to analyze with environment specification:**
- "Analyze ACM-22079" (uses default qe6)
- "Analyze ACM-22079 using qe7 environment"
- "Analyze ACM-22079 using qe8 environment"

**Internal Operations**: Framework uses setup_clc/login_oc scripts internally but shows generic `oc login <cluster-url>` in test cases.

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

## Polarion Integration

> **Setup Guide**: [Polarion Setup Documentation](docs/polarion-setup-guide.md)  
> **CLI Reference**: [Complete CLI Command Reference](docs/polarion-cli-reference.md)  
> **Workflow Integration**: [Polarion Integration Workflow](.claude/workflows/polarion-integration.md)

The framework includes optional Polarion integration for enterprise test case management:

### Key Features
- **Learning from Existing Test Cases**: Analyze patterns from existing Polarion test cases
- **Direct Test Case Posting**: Post generated test cases directly to Polarion
- **Metadata Enhancement**: Automatically add relevant metadata and links
- **Pattern Recognition**: Learn validation approaches and naming conventions

### Quick Start
```bash
# Setup Polarion integration (optional)
python3 -m polarion.cli setup-config
export POLARION_PAT_TOKEN='your-token'
export POLARION_URL='https://polarion.company.com'

# Use in workflow (when needed)
python3 -m polarion.cli fetch-learning --search-terms "ACM" "upgrade"
# ... run normal test generation ...
python3 -m polarion.cli post-test-cases Test-Cases.md
```

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
- **claude-test-generator**: AI-service based, fast, focused on immediate test generation with integrated quality assurance
- **intelligent-test-framework**: Comprehensive analysis framework with advanced automation capabilities

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
├── README.md                    # This file - Project overview and usage
├── CLAUDE.md                    # Claude AI configuration and services
├── bin/                         # Internal utilities (setup_clc, login_oc only)
├── .claude/                     # AI service configuration
│   ├── prompts/                 # AI reasoning and scoping rules
│   ├── templates/               # AI-generated output formats
│   ├── workflows/               # AI feedback loop and processes
│   ├── advanced/                # Advanced AI service features
│   └── greetings/               # Framework welcome messages
├── runs/                        # Generated test runs by ticket
│   └── <TICKET-ID>/             # Organized by JIRA ticket
│       ├── run-XXX-YYYYMMDD-HHMM/ # Timestamped executions
│       │   ├── Test-Cases.md    # Clean test cases (generic oc login)
│       │   ├── Complete-Analysis.md # Full AI analysis
│       │   └── metadata.json    # Run metadata
│       └── latest -> run-XXX    # Symlink to latest run
├── examples/                    # Example AI-generated outputs
└── docs/                        # Additional documentation
```

**Key Components**:
- **AI Services**: 4 integrated services (Documentation, GitHub Investigation, Schema, Validation)
- **Internal Scripts**: Only setup_clc/login_oc (never exposed to users)
- **Generated Outputs**: Professional test cases with standard OpenShift commands

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
- **Polarion Setup**: See `docs/polarion-setup-guide.md` for Polarion integration setup
- **CLI Reference**: See `docs/polarion-cli-reference.md` for complete command documentation
- **Configuration**: Check `.claude/` directory for customization options
- **Examples**: Review `examples/` for sample outputs and patterns

### Troubleshooting
- **Environment Issues**: Verify cluster access and tool availability
- **Output Quality**: Check JIRA ticket completeness and feature deployment status
- **Framework Errors**: Review metadata.json for execution details and error logs

---

**Framework Version**: 2.0 (AI Services Integration)  
**Maintained by**: ACM QE Team  
**Core Technology**: Claude AI with integrated Documentation, GitHub Investigation, Schema, and Validation services  
**Environment Management**: Internal setup_clc/login_oc utilities (hidden from end users)  
**Output Format**: Professional test cases with generic OpenShift commands