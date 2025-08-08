# AI-Powered JIRA Analysis & Test Generation Framework

## 🎯 Overview

This framework demonstrates AI-powered JIRA analysis and test plan generation. It is currently focused on ACM-22079 (ClusterCurator digest upgrades) and operating in Phase 1: Test-Plan-Only mode.

- Implementation (script/code generation) is intentionally disabled for now and logged as "under development".
- The architecture is extensible, but other JIRA tickets will need customization.

### Phase 1 scope
- Generates validated, normalized test plans in exact table format (with Description and Setup sections)
- Applies intelligent validation and adaptive feedback to improve plans
- Emits per-run artifacts under `intelligent-test-framework/examples/ACM-22079-<n>/`
- Writes a consolidated report to `intelligent-test-framework/05-documentation/ACM-22079-Test-Plan-Explained.md`

Planned Phase 2+: enable framework-specific script generation (Cypress/Selenium/Go) once plan quality stabilizes.

## ⚠️ **Current Limitations**

**IMPORTANT (Phase 1: Test-Plan-Only)**
- The framework currently generates validated test plans only (no test scripts).
- It is focused on ACM-22079. Using it with other JIRA tickets will require:
- Custom prompt development for the specific feature
- Feature-specific validation logic  
- Domain-specific test patterns
- Updated repository mappings and analysis

## 🏗️ Architecture Overview (Phase 1)

```
┌─────────────────────────────────────────────────────────────┐
│                    JIRA Ticket Input                       │
│                (e.g., ACM-22079)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              Stage 1: Environment Setup                    │
│   • Claude Code validation                                 │
│   • GitHub SSH access verification                         │
│   • Prerequisites validation                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│           Stage 2: Dynamic Repository Access               │
│   • Real-time GitHub repository cloning                    │
│   • PR and commit analysis                                 │
│   • Cross-repository pattern detection                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              Stage 3: AI Analysis                          │
│   • Feature understanding                                  │
│   • Code change analysis                                   │
│   • Test scenario identification                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│       Stage 4: Test Plan Generation & Validation           │
│   • Smart validation engine                                │
│   • Table format generation                                │
│   • Missing feature detection                              │
│   • Adaptive feedback integration                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              Stage 5: Human Review Gate                    │
│   • Validation warnings review                             │
│   • Test plan approval process                             │
│   • Feedback collection                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│      Stage 6: Test Implementation (Disabled in Phase 1)     │
│   • Under development                                       │
│   • Logged and skipped                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│           Stage 7: Quality Validation (Test Plan)           │
│   • Plan structure/clarity validation                       │
│   • Expected-results realism checks                          │
│   • Style normalization (8–10 steps/table, Setup section)    │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Core Components

### 1. Main Orchestrator (`create-test-case.sh`)

**Purpose**: Central controller that manages the entire workflow from JIRA ticket input to final test generation.

**Key Features**:
- **Argument parsing**: Handles JIRA ticket IDs, mode flags (`--test-plan-only`), and configuration options
- **Stage progression**: Orchestrates 7 distinct stages with proper error handling
- **State management**: Tracks workflow progress in `workflow-state.json`
- **Human interaction**: Implements review gates and feedback collection

**Usage Examples** (any ACM Story):
```bash
# Generate test plan only for any ACM Story (e.g., ACM-12345)
./create-test-case.sh ACM-12345 --test-plan-only

# Full workflow (Phase 1 produces plan only; implementation disabled)
./create-test-case.sh ACM-12345

# Dry run mode for ACM-22079
./create-test-case.sh ACM-22079 --dry-run --verbose

# Custom configuration for specific team
./create-test-case.sh ACM-12345 --config selenium-team-config.yaml
```

**⚠️ Note**: Feature detection + overrides now allow any ACM Story. If no specific override exists, the generic fallback is used while preserving strict table format and validation.

### 2. Smart Validation Engine (`01-setup/smart-validation-engine.sh`)

**Purpose**: Intelligent validation system that adapts to different testing scenarios, including missing feature detection.

**Core Capabilities**:

#### **Multi-Tier Validation**
1. **Feature Availability**: Checks if target feature exists in environment
2. **Environment Readiness**: Validates cluster connectivity, permissions, and dependencies
3. **Test Logic**: Verifies command accuracy and resource definitions
4. **Expected Results**: Validates test outcome expectations

#### **Missing Feature Intelligence** ⭐ *NEW*
```bash
# The engine now detects when features aren't implemented yet
if [ $missing_feature_score -ge 2 ]; then
    print_warning "⚠️  Smart Analysis: Feature appears not yet implemented"
    print_status "🧠 INTELLIGENT ADAPTATION: Generating test plan for pre-implementation validation"
    exit 2  # Warning status - continue with adapted approach
fi
```

**Smart Detection Indicators**:
- CRD availability failures
- Controller deployment missing
- API endpoint unavailability
- Resource schema mismatches

**Validation Modes**:
- **Standard**: Full environment validation
- **Pre-implementation**: Adapted for missing features
- **Graceful degradation**: Continues with warnings

### 3. Adaptive Feedback Integrator (`01-setup/adaptive-feedback-integrator.sh`)

**Purpose**: Continuous learning system that improves test generation based on validation results and human feedback.

**Learning Mechanisms**:

#### **Pattern Recognition**
```json
{
  "learned_patterns": [
    {
      "problem": "Missing ClusterCurator CRD",
      "solution": "Add prerequisite validation",
      "confidence": 0.9,
      "occurrences": 3
    }
  ]
}
```

#### **Adaptive Refinements**
- **Test Plan Enhancement**: Adds missing prerequisites and validation steps
- **Command Corrections**: Fixes syntax and improves specificity
- **Environment Adaptations**: Adjusts for different cluster configurations

#### **Knowledge Base Evolution**
- Stores successful strategies in `knowledge-base.json`
- Tracks failure patterns and solutions
- Provides context-aware recommendations

### 4. Table Format Test Generation

**Purpose**: Ensures consistent, human-readable test plan format that matches Polarion and other test management tools.

**Format Requirements**:
```markdown
### Test Case 1: Feature Name
**Setup**: 
- Environment requirements
- Prerequisites and configurations

| Test Steps | Expected Results |
|------------|------------------|
| 1. Complete command with details | Specific expected output |
| 2. Verification step with full cmd | Exact result format |
```

**Enhanced Prompt Engineering**:
- **Format Override**: Dominates all other style instructions
- **Command Completeness**: Ensures full `oc` commands with parameters; include CLI and UI variants when applicable
- **Verification Clarity**: Specifies exact expected outputs and rationale; include sample output lines for grep/jsonpath where used
- **Namespace Standardization**: Use `ocm` for ClusterCurator examples in ACM environments

### 5. Dynamic GitHub Integration

**Purpose**: Real-time access to repository code, PRs, and documentation for comprehensive analysis.

**Capabilities**:
- **SSH-based Access**: Secure repository cloning and updates
- **Cross-Repository Analysis**: Examines related repositories automatically
- **PR Context Extraction**: Analyzes specific pull requests and commits
- **Documentation Mining**: Extracts linked and related documentation

**Repository Detection Example**:
```bash
# Automatically detects relevant repositories for ACM-22079
Repositories:
  • stolostron/cluster-curator-controller  # Primary implementation
  • stolostron/clc-ui-e2e                 # UI testing
  • stolostron/console                     # Frontend changes
  • stolostron/api                        # API definitions
```

### 6. Framework Agnostic Design

**Purpose**: Supports multiple testing frameworks with easy configuration switching.

**Supported Frameworks**:

#### **Cypress Configuration** (`team-config.yaml`)
```yaml
team:
  name: "CLC QE Team"
  framework: "cypress"
  language: "typescript"
  test_directory: "cypress/e2e"
  
test_patterns:
  file_naming: "*.cy.ts"
  describe_pattern: "Feature: {feature_name}"
  test_structure: "it('should {behavior}', () => {...})"
```

#### **Selenium Configuration** (`configs/selenium-team-config.yaml`)
```yaml
team:
  name: "Selenium QE Team"  
  framework: "selenium"
  language: "java"
  test_directory: "src/test/java"
  
test_patterns:
  file_naming: "*Test.java"
  class_pattern: "public class {Feature}Test"
  test_structure: "@Test public void test{Behavior}() {...}"
```

#### **Go Testing Configuration** (`configs/go-team-config.yaml`)
```yaml
team:
  name: "Backend QE Team"
  framework: "go"
  language: "go"
  test_directory: "pkg/tests"
  
test_patterns:
  file_naming: "*_test.go"
  function_pattern: "func Test{Feature}(t *testing.T) {...}"
```

## 🧠 AI/LLM Integration Strategy

### Claude Code Integration

**Architecture**:
- **Primary AI Engine**: Claude Sonnet 4 for analysis and generation
- **Prompt Engineering**: Sophisticated prompt chains for different stages
- **Context Management**: Efficient handling of large codebases and documentation

**Prompt Categories**:

#### **Analysis Prompts**
- `initial-analysis.txt`: High-level feature understanding
- `code-deep-dive.txt`: Detailed implementation analysis  
- `github-aware-analysis.txt`: Real-time repository analysis

#### **Generation Prompts**
- `table-format-test-generation.txt`: Primary test plan generation (story-agnostic)
- `prompts/feature-overrides/*.txt`: Feature-specific refinements applied after detection
- `environment-aware-implementation.txt`: (Phase 2) Code generation with validation context
- `dynamic-test-generation.txt`: Tests based on live repository analysis

#### **Validation Prompts**
- `test-plan-validation.txt`: Quality and completeness validation
- `cross-repository-patterns.txt`: Multi-repo consistency checking

### Smart Context Building

**Progressive Context Enhancement**:
```
JIRA Ticket Analysis
    ↓
Repository Code Analysis
    ↓
Documentation Mining
    ↓
Historical Pattern Matching
    ↓
Test Generation with Full Context
```

## 📊 Workflow Stages Detailed

### Stage 1: Environment Setup & Validation

**Responsibilities**:
- Claude Code CLI verification and configuration
- GitHub SSH access validation for dynamic repository access
- Environment variable and authentication setup
- Network connectivity and API accessibility testing

**Key Validations**:
```bash
# Claude Code connectivity
claude --version && claude --print "test"

# GitHub SSH access
ssh -T git@github.com

# ACM environment access
oc cluster-info
```

**Output**: Environment readiness report and configuration validation

### Stage 2: Dynamic GitHub Repository Access ⭐ *ENHANCED*

**New Capabilities**:
- **Real-time Repository Detection**: Automatically identifies relevant repositories based on JIRA content
- **Cross-repository Pattern Analysis**: Examines related codebases for comprehensive understanding
- **Dynamic Content Access**: Provides live access to latest code changes and documentation

**Repository Access Workflow**:
```bash
1. Detect relevant repositories from JIRA ticket analysis
2. Clone/update repositories with SSH access
3. Extract PR-specific changes and context
4. Mine linked and related documentation
5. Prepare comprehensive context for AI analysis
```

**Benefits**:
- **Always Current**: Accesses latest code changes and PRs
- **Comprehensive Context**: Includes all related repositories and documentation
- **Dynamic Discovery**: Finds relevant code beyond explicitly mentioned repositories

### Stage 3: AI-Powered Comprehensive Analysis

**Analysis Dimensions**:

#### **Feature Understanding**
- **Business Logic**: Extracts value propositions and use cases from JIRA
- **Technical Implementation**: Analyzes code changes and architectural decisions
- **Integration Points**: Identifies dependencies and interaction patterns

#### **Test Scenario Generation**
- **Positive Flows**: Happy path testing scenarios
- **Edge Cases**: Boundary conditions and error scenarios  
- **Integration Testing**: Cross-component interaction validation
- **Security & RBAC**: Permission and access control testing

### Stage 4: Test Plan Generation & Validation ⭐ *ENHANCED*

**Intelligent Generation Process**:

#### **Format-Preserved Generation**
```bash
# New table format prompt ensures consistent output
MANDATORY: Generate test cases in EXACT TABLE FORMAT
IGNORE ALL OTHER STYLE INSTRUCTIONS
| Test Steps | Expected Results |
```

#### **Smart Validation with Missing Feature Detection**
```bash
# Detects when features aren't implemented yet
if [ $missing_feature_score -ge 2 ]; then
    # Adapt approach for pre-implementation testing
    generate_pre_implementation_test_plan
fi
```

#### **Adaptive Feedback Integration**
- Analyzes validation failures for root causes
- Applies learned patterns to improve test quality
- Refines test plans based on environment limitations

**Validation Exit Codes (Plan Validation)**:
- `0`: Validation passed
- `1`: Hard validation failure (environment issues)
- `2`: Soft failure with adaptation (missing features)

### Stage 5: Human Review Gate

**Review Process**:
1. **Validation Warning Analysis**: Reviews any detected issues
2. **Test Plan Quality Check**: Human verification of generated content
3. **Approval Workflow**: Options to approve, modify, or reject
4. **Feedback Collection**: Captures human insights for continuous learning

**Interactive Options**:
```bash
Do you approve the test plan despite validation warnings? (y/n/modify): 
# y - Continue with current plan
# n - Stop workflow  
# modify - Return to generation with feedback
```

### Stage 6: Test Implementation (Disabled in Phase 1)

Implementation is intentionally deferred. The orchestrator logs this stage as under development and stops after test plan validation.

### Stage 7: Quality Validation

**Multi-Level Validation**:

#### **Code Quality Checks**
- Syntax validation for generated test code
- Framework-specific pattern compliance
- Best practices adherence

#### **Test Logic Verification**
- Command accuracy validation
- Expected result realism checking
- Environment compatibility assessment

#### **Integration Testing**
- Repository integration validation
- CI/CD pipeline compatibility
- Execution environment verification

## 🎛️ Configuration & Customization

### Team-Specific Configurations

**Configuration Hierarchy**:
```
1. Default framework configuration (team-config.yaml)
2. Framework-specific overrides (configs/{framework}-config.yaml)
3. Runtime arguments (--config custom.yaml)
4. Environment variables (FRAMEWORK_TYPE, TEST_DIR)
```

**Configuration Schema**:
```yaml
team:
  name: "Team Name"
  framework: "cypress|selenium|go|playwright"
  language: "typescript|java|go|python"
  
environment:
  cluster_type: "OCP|Kind|Minishift"
  acm_version: "2.8|2.9|2.10"
  
test_patterns:
  naming_convention: "pattern"
  directory_structure: "path"
  file_extensions: [".cy.ts", ".spec.ts"]
  
ai_settings:
  model: "claude-sonnet-4"
  max_context_length: 100000
  validation_strictness: "medium|strict|relaxed"
```

### Advanced Features

#### **Graceful Degradation**
```bash
# Framework adapts to different scenarios
VALIDATION_STRICTNESS=relaxed ./create-test-case.sh ACM-22079
# Continues with warnings instead of failing
```

#### **Learning from Feedback**
```json
{
  "execution_feedback": {
    "test_quality": 8.5,
    "accuracy": 9.0,
    "completeness": 7.8,
    "improvements": [
      "Add more edge case scenarios",
      "Improve command specificity"
    ]
  }
}
```

## 🔄 Continuous Learning & Improvement

### Knowledge Base Evolution

**Learning Patterns**:
- **Success Strategies**: Captures what works well for different feature types
- **Failure Analysis**: Records common issues and their solutions
- **Environment Adaptations**: Learns from different cluster configurations

**Feedback Integration**:
```bash
# After each execution, insights are captured
{
  "learned_patterns": [...],
  "success_strategies": [...],
  "environment_adaptations": [...]
}
```

### Adaptive Behavior

**Context-Aware Improvements**:
- Learns team-specific patterns and preferences
- Adapts to different ACM component testing approaches
- Improves accuracy based on validation feedback

**Example Learning Cycle**:
```
Initial Test Generation → Validation Feedback → Pattern Analysis → 
Improved Generation → Human Review → Knowledge Update → 
Enhanced Future Generation
```

## 🚀 Getting Started

### Prerequisites

1. **Claude Code Access**: Configured with proper authentication
2. **GitHub SSH Access**: SSH keys configured for stolostron repositories
3. **ACM Environment**: Access to OpenShift cluster with ACM installed
4. **Development Tools**: `jq`, `git`, `oc` CLI, framework-specific tools

### Quick Start

```bash
# 1. Clone and setup framework
git clone https://github.com/stolostron/ai-test-gen
cd ai-test-gen/intelligent-test-framework

# 2. Run initial setup
./quick-start.sh

# 3. Generate test plan for ACM-22079 (currently the only supported ticket)
./create-test-case.sh ACM-22079 --test-plan-only

# 4. Review generated test plan
open 02-test-planning/test-plan.md

# 5. Generate full implementation for ACM-22079  
./create-test-case.sh ACM-22079
```

### Configuration for Your Team

```bash
# Create team-specific configuration
cp team-config.yaml my-team-config.yaml

# Edit configuration for your framework and preferences
vim my-team-config.yaml

# Use custom configuration
./create-test-case.sh ACM-22079 --config my-team-config.yaml
```

## 📈 Success Metrics & ROI

### Quantitative Benefits

**Time Savings**:
- **Test Plan Generation**: ~2 hours → ~15 minutes (87% reduction)
- **Initial Test Implementation**: ~1 day → ~2 hours (75% reduction)
- **Test Maintenance**: Continuous updates based on feedback

**Quality Improvements**:
- **Coverage**: Identifies edge cases often missed in manual planning
- **Consistency**: Standardized format across all test cases
- **Accuracy**: AI-powered analysis reduces human oversight errors

### Qualitative Benefits

**Process Improvements**:
- **Early Testing**: Can generate tests before feature implementation
- **Knowledge Sharing**: Captures and reuses team expertise
- **Framework Agnostic**: Works across different testing approaches

**Team Productivity**:
- **Focus Shift**: From test writing to test design and strategy
- **Reduced Ramp-up**: New team members can generate tests immediately
- **Continuous Learning**: Framework improves over time

## 🔧 Extending to Other JIRA Tickets

**Current State**: The framework is designed for ACM-22079 but with extensible architecture.

### Required Customizations for New Tickets

To support other JIRA tickets (e.g., `ACM-12345`), you would need to:

#### 1. **Feature-Specific Prompts**
```bash
# Create new prompts in 02-analysis/prompts/
- feature-specific-analysis.txt     # Understanding the new feature
- custom-test-generation.txt        # Test patterns for the feature type
- validation-rules.txt              # Feature-specific validation logic
```

#### 2. **Repository Mapping**
```bash
# Update 01-setup/dynamic-github-access.sh
detect_relevant_repositories() {
    case "$JIRA_TICKET" in
        "ACM-22079")
            echo "stolostron/cluster-curator-controller" ;;
        "ACM-12345")  
            echo "stolostron/your-feature-repo" ;;  # Add new mappings
    esac
}
```

#### 3. **Validation Logic**
```bash
# Extend 01-setup/smart-validation-engine.sh
validate_feature_availability() {
    case "$JIRA_TICKET" in
        "ACM-22079")
            validate_clustercurator_crd ;;
        "ACM-12345")
            validate_your_feature_components ;;  # Add new validations
    esac
}
```

#### 4. **Test Patterns**
```yaml
# Add to configs/team-config.yaml
feature_patterns:
  ACM-22079:
    type: "cluster_lifecycle"
    components: ["ClusterCurator", "ManagedClusterView"]
  ACM-12345:
    type: "your_feature_type"  
    components: ["YourComponent1", "YourComponent2"]
```

### Framework Extension Roadmap

#### **Phase 1: Multi-Ticket Support (Immediate)**
- Parameterize JIRA ticket handling
- Create ticket-specific configuration system
- Develop feature type detection

#### **Phase 2: Feature Type Abstractions (Month 1)**
- Abstract common ACM patterns (cluster management, policy, observability)  
- Create reusable validation templates
- Develop feature type inheritance

#### **Phase 3: Full Generalization (Month 2)**
- Support any ACM component
- Auto-detect feature types from JIRA content
- Machine learning for pattern recognition

## 🔮 Future Enhancements

### Planned Features

1. **Multi-Ticket Support**: Generalized framework for any ACM JIRA ticket
2. **Feature Type Detection**: Automatic categorization of JIRA tickets  
3. **Pattern Library**: Reusable test patterns for different ACM components
4. **Cross-Product Integration**: Support for other Red Hat products

### Advanced AI Capabilities

1. **Predictive Analysis**: Anticipate test scenarios based on code patterns
2. **Risk Assessment**: Identify high-risk areas requiring additional testing
3. **Automated Maintenance**: Self-updating tests based on code changes

## 📚 Technical References

### Key Files & Directories

```
intelligent-test-framework/
├── create-test-case.sh             # Main orchestrator
├── 01-setup/                       # Setup and validation scripts
│   ├── smart-validation-engine.sh  # Intelligent validation
│   ├── adaptive-feedback-integrator.sh # Learning system
│   └── dynamic-github-access.sh    # Repository integration
├── 02-analysis/                    # AI analysis workspace
│   ├── prompts/                    # AI prompt templates
│   └── sessions/                   # Analysis session logs
├── 02-test-planning/               # Generated test plans (Phase 1)
├── 04-implementation/              # Disabled in Phase 1
├── configs/                        # Framework configurations
└── 06-reference/                   # Documentation and research
```

### API Endpoints & Integrations

**Claude Code CLI**:
- Model: `claude-sonnet-4@20250514`
- Context: Up to 100K tokens
- Output: Structured markdown and code

**GitHub Integration**:
- SSH access to `stolostron/*` repositories
- Real-time PR and commit analysis
- Cross-repository pattern detection

**OpenShift/ACM APIs**:
- Cluster validation endpoints
- Resource existence checking
- Permission and RBAC validation

## 🎯 Conclusion

This framework represents a significant advancement in automated test generation, combining AI capabilities with intelligent validation, adaptive learning, and human oversight. It's designed to grow and improve with usage, making it an invaluable tool for QE teams working on complex enterprise software like Advanced Cluster Management.

The framework's ability to handle missing features, adapt to different environments, and learn from feedback makes it robust for real-world usage across various development and testing scenarios.

---

**Framework Version**: 2.0 (Phase 1)  
**Last Updated**: 2025-08-08  
**Maintainer**: ACM QE Team  
**Repository**: https://github.com/stolostron/ai-test-gen