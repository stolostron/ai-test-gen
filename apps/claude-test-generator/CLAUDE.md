# Claude Test Generator - Application Configuration

## Application Context
This application provides simple, Claude-focused test generation for rapid prototyping and quick test plan creation. It focuses on straightforward JIRA + PR analysis with minimal setup requirements.

## Application Overview
**Goal:** Simple, fast test plan generation from JIRA tickets and GitHub PRs using Claude Code integration.
**Focus:** Quick iteration and rapid prototyping for individual contributors.
**Target:** ACM Stories and general OpenShift/Kubernetes feature testing with minimal complexity.

## Available Tools
- **Jira CLI**: Installed and configured for ticket analysis
- **WebFetch**: For accessing GitHub PR details and analysis
- **kubectl/oc**: Kubernetes/OpenShift CLI for cluster validation
- **TodoWrite**: Task tracking and progress management

## Common Commands

### JIRA Analysis
```bash
# View ticket details with description and comments
jira issue view <TICKET-ID> --plain

# Get ticket with comments
jira issue view <TICKET-ID> --comments

# List subtasks and linked issues
jira issue view <TICKET-ID> # Shows linked tickets in output
```

### GitHub PR Analysis
```bash
# Use WebFetch tool with GitHub URLs for PR analysis
# Format: https://github.com/<owner>/<repo>/pull/<number>
```

## AI-Powered Analysis Workflow

### Prerequisites & Environment Validation
**DEFAULT ENVIRONMENT SETUP:** By default, use `source setup_clc qe6` to setup the environment and proceed with analysis.

**Environment Setup Process:**
```bash
# Default setup command
source setup_clc qe6

# This automatically:
# - Fetches latest successful deployment from Jenkins
# - Configures kubectl/oc access to qe6 environment  
# - Sets up ACM console environment variables
# - Logs into OpenShift cluster
```

**Setup Script Details:**
- **Script Location**: `/Users/ashafi/bin/setup_clc`
- **Purpose**: CLC Cypress Environment Setup for ACM testing
- **Capabilities**: 
  - Auto-fetch deployment info from Jenkins API
  - Support for multiple environments (qe6, qe7, qe8, qe9, qe10)
  - Automatic OpenShift login with deployment credentials
  - Environment variable export for Cypress testing
  - CLC repository detection and npm setup

**Environment Validation Commands:**
```bash
# Verify cluster connectivity  
kubectl version --client
kubectl cluster-info

# Check ACM/MCE installation
kubectl get operators -n openshift-operators | grep advanced-cluster-management
kubectl get mce -A

# List managed clusters
kubectl get managedclusters
```

## Workflow Stages

### Stage 1: Environment Setup & Validation
**Responsibilities:**
- Use default `source setup_clc qe6` command for environment setup
- Verify kubectl/oc CLI access and cluster connectivity
- Validate user has necessary permissions
- Validate if certain cli tools are setup such as jira
- Veriify if the user can connect and fecth info from relevant gits.
- **Continue with analysis even if cluster has limitations** - adapt test validation based on available resources

**Output:** Environment readiness report and configuration validation

### Stage 2: Dynamic GitHub Repository Access & JIRA Analysis

**Capabilities:**
- **Real-time Repository Detection**: Automatically identifies relevant repositories based on JIRA content
- **Cross-repository Pattern Analysis**: Examines related codebases for comprehensive understanding
- **Dynamic Content Access**: Provides live access to latest code changes and documentation

**Process:**
1. Read main JIRA ticket with `jira issue view <TICKET-ID> --plain`
2. Extract:
   - Description and value statement
   - Assignee and status
   - Comments for PR references and to understand context of the story/feature
   - List of subtasks
   - List of linked tickets

### Step 2a: Discover Related PRs
**Check these locations for Git PR references:**
1. **Main ticket comments** - Look for GitHub URLs
2. **All subtasks** - Many PRs are referenced in subtask comments
3. **Linked tickets** - Dependent/blocking tickets may have PRs
4. **Related tickets** - Parent/child relationships


### Step 2b: Discover Related Docs
**Check these locations for document references:**
1. **Main ticket comments** - Look for any Doc related links
2. **All subtasks** - Many docss are referenced in subtask comments
3. **Linked tickets** - Dependent/blocking/linked tickets may have docs
4. **Related tickets** - Parent/child relationships
5. **Internets** - Finally, to understand the feature better, search internet for any relevant info


### Stage 3: AI-Powered Comprehensive Analysis

**Analysis Dimensions:**

#### Feature Understanding
- **Business Logic**: Extracts value propositions and use cases from JIRA
- **Technical Implementation**: Analyzes code changes, architectural decisions, official docs for relevant info
- **Integration Points**: Identifies dependencies and interaction patterns

#### PR Analysis Process
For each PR found:
1. Extract PR number and repository from JIRA comments
2. Use WebFetch with full GitHub URL to get:
   - Title and description
   - Author and reviewers
   - Status (open/merged/closed)
   - Files changed and lines modified
   - Related JIRA tickets
   - Review status and approvals

#### Test Scenario Generation
- **Positive Flows**: Happy path testing scenarios
- **Edge Cases**: Boundary conditions and error scenarios
- **Integration Testing**: Cross-component interaction validation

Note that all test scenario geentayion should be done after thorughly understanding the feature (via analysis from all collected info) 

### Stage 4: Test Plan Generation & Validation

**Intelligent Generation Process:**

#### Table Format Test Generation
**Purpose**: Ensures consistent, human-readable test plan format matching Polarion and other test management tools. Each table shouldn't have more than 8-10 steps. If needed (to cover all the scenarios/areas), generate more tables.

**Format Requirements:**
```markdown
### Test Case N: Feature Name
**Description**: 
- Clear description of the feature being tested
- Outline/Explain key scenarios needed to be tested

**Setup**: 
- Environment requirements
- Prerequisites and configurations

| Test Steps | Expected Results |
|------------|------------------|
| 1. Complete command with details | Specific expected output |
| 2. Verification step with full cmd | Exact result format |
```

#### Example Test Table Pattern Analysis
Based on existing CLC test cases, follow these proven patterns:

**Step Structure Pattern:**
- **Action-oriented steps**: Each step clearly describes what the user should do
- **Goal-oriented subsections**: Use "Goal:" to explain the purpose of complex steps
- **Detailed sub-actions**: Use bullet points for multi-part steps
- **Specific UI elements**: Reference exact button names, menu paths, and field names

**Example Step Patterns:**
```markdown
| From the ACM dashboard, select **Infrastructure** > **Clusters**, Click on Create Cluster and choose "OpenShift Virtualization" as the control plane type. | The cluster creation wizard opens with the first configuration step displayed. |

| **Verify Presence of Networking Options Section**<br>**Goal:** Confirm the "Networking Options" section is available under the "Node Pools" configuration step.<br>• Navigate to the **Node Pools** step in the wizard.<br>• Expand the "Networking Options" section in the node pool configuration. | A collapsible section titled "Networking Options" is present, containing fields for additional networks and a checkbox for the default pod network. |

| **Verify Additional Network Name Validation**<br>**Goal:** Validate that additional network names follow the required format: lower-case letters and hyphens only.<br>• Enter a value with uppercase letters (e.g., Invalid/Name) and observe.<br>• Enter a value with special characters (e.g., namespace/n@me) and observe. | The system rejects invalid names and displays an appropriate error message. Both parts of the namespace/name must contain only lower-case letters and hyphens. |
```

**Best Practices from Examples:**
1. **Bold formatting for section headers** in test steps (e.g., **Verify Feature Name**)
2. **Goal statements** to clarify the purpose of complex validation steps
3. **Specific examples** in parentheses (e.g., "default/my-network", "Invalid/Name")
4. **UI navigation paths** with exact menu structure (Infrastructure > Clusters)
5. **Precise expected results** that can be objectively verified
6. **Progressive complexity** - start with basic actions, build to complex validations
7. **Multiple validation scenarios** in single steps using bullet points

**📖 For detailed examples and patterns, see the [Test Table Writing Reference](#test-table-writing-reference) section below.**

#### Smart Validation with Missing Feature Detection
- After creating test steps/table, validate on connected cluster
- Ensure tests are correct through cluster validation
- **Environment Awareness**: Cluster might not have feature/code changes the story describes
- **Intelligent Validation**: If validations fail, investigate environment state and proceed accordingly
- **Flexible Approach**: Don't be too strict in validation; inform user of validation failures

#### Feature Availability Analysis
**Critical Step**: Always determine if the feature being tested is actually deployed in the validation environment.

**Analysis Process:**
1. **Version Detection**: Check deployment/pod image digests against known implementation commits
2. **Feature Deployment Validation**: Compare target cluster's component versions with PR merge dates
3. **Capability Assessment**: Determine what can be tested vs. what needs newer environment
4. **Timeline Analysis**: Provide deployment status and expected availability dates

**Commands for Feature Detection:**
```bash
# Check component image versions
oc get deployment <component> -n <namespace> -o jsonpath='{.spec.template.spec.containers[0].image}'

# Compare against known implementation commits
# Use WebFetch to verify if PR commits are included in current image

# Document feature availability status in test plan
```

**Test Plan Impact:**
- **Feature Available**: Full validation possible, execute all test cases
- **Feature Missing**: Document expected behavior, provide test readiness validation
- **Partial Feature**: Identify which aspects can be tested with current deployment

### Cluster Validation
**Process:**
- Attempt to validate test steps on connected cluster
- If cluster unreachable, note limitation in test plan
- Document environment-specific validation requirements
- Provide guidance for when cluster access is restored


### Stage 5: Comprehensive Analysis Report & Feedback Loop

#### Final Analysis Report Format
**Required Components:**
1. **Feature Implementation Status**
   - PR merge status and commit information
   - Current environment capability analysis  
   - Feature availability timeline

2. **Test Plan Validation Results**
   - Which test cases can be executed immediately
   - Which require newer environment deployment
   - Specific validation failures and their root causes

3. **Environment Deployment Analysis**
   - Current image versions vs. implementation requirements
   - Expected deployment timeline for feature availability
   - Alternative testing approaches if feature unavailable

#### Feedback Loop Process
- With each generation of table, collect relevant validation info
- Feed that info back to AI to help generate better table
- Attempt few times (if validation is not 100%)
- After present a comprehensive report to the user including deployment status analysis
- Ask to review: a. Stop (no test table) b. Give feedback (AI will use feedback to improve) c. Finish and save results/tables

#### Dual Output File Generation
**MANDATORY**: Always generate TWO markdown files for every analysis:

1. **Complete Analysis Report**: `<TICKET-ID>-<FEATURE>-Complete-Analysis.md`
   - Feature description and business value
   - Implementation analysis (PR details, merge status)
   - Feature availability analysis (environment deployment status)
   - Test plan validation results
   - Complete test cases with setup and validation context
   - Linked tickets analysis
   - Testing readiness assessment

2. **Test Cases Only**: `<TICKET-ID>-<FEATURE>-Test-Cases.md`
   - Clean, focused test case format for Polarion import
   - Only test case descriptions, setup, and table steps
   - No implementation analysis or environment status
   - Ready for copy-paste into test management tools

#### Example File Structure
```markdown
# Complete Analysis Report Format
- Feature Overview & Business Value
- Implementation Status & PR Analysis  
- Environment Deployment Analysis
- Test Plan Validation Results
- Complete Test Cases (6+ comprehensive scenarios)
- Sample Resource YAMLs
- Linked Tickets Analysis
- Testing Readiness & Next Steps

# Test Cases Only Format  
- Test Case 1: Feature Name
  - Description
  - Setup 
  - Test Steps Table
- Test Case 2: Feature Name...
- (Clean format optimized for test management tools)
```

## Workflow Execution Example

### Input Requirements
User MUST provide:
- **JIRA Ticket ID** (e.g., ACM-20640) 
- **Environment setup** will be handled automatically via `source setup_clc qe6`

**Output Format** (markdown preferred)
**Repository Access** (public repos supported)

### Complete Analysis Pattern
```bash
# 1. Environment setup (automatic)
source setup_clc qe6

# 2. Main ticket analysis
jira issue view ACM-20640 --plain

# 3. Systematic subtask analysis
jira issue view ACM-22925 --plain  # Critical subtasks first
jira issue view ACM-22755 --plain  # Blocker subtasks
# ... continue for all subtasks

# 4. QE and dependency analysis
jira issue view ACM-22799 --plain  # QE tasks
jira issue view ACM-22800 --plain  # QE automation

# 5. PR analysis via WebFetch
# WebFetch: https://github.com/stolostron/console/pull/4858
# WebFetch: https://github.com/stolostron/console/pull/4851

# 6. Generate dual test plan output files
# Create: <TICKET-ID>-<FEATURE>-Complete-Analysis.md (comprehensive report)
# Create: <TICKET-ID>-<FEATURE>-Test-Cases.md (test tables only)
```

## Key Repositories to Watch
- `stolostron/console` - ACM Console UI
- `stolostron/*` - Red Hat ACM components
- Enterprise repositories as discovered

## Framework Best Practices

### Analysis Best Practices
1. **Environment First**: Use `source setup_clc qe6` for automatic environment setup
2. **Systematic Approach**: Check ALL subtasks and linked tickets methodically
3. **Use TodoWrite**: Track progress when analyzing multiple tickets and stages
4. **Pattern Recognition**: PRs often referenced in comments with specific formats
5. **Status Awareness**: Note if PRs are open, merged, or require approval
6. **Repository Context**: Understand which repo the PRs belong to

### Test Plan Generation Best Practices
1. **Dual File Output**: ALWAYS generate both complete analysis and test-cases-only files
2. **Table Format**: Use consistent markdown table format for Polarion compatibility
3. **Complete Commands**: Include full commands with expected outputs
4. **Environment Awareness**: Design tests considering cluster state variations
5. **Validation Strategy**: Plan for cluster connectivity issues
6. **QE Integration**: Reference QE tasks and automation requirements
7. **Feature Availability Analysis**: Always validate if feature is deployed in target environment

### Workflow Execution Best Practices
1. **Automatic Setup**: Use `source setup_clc qe6` for default environment configuration
2. **Progress Tracking**: Use TodoWrite for all workflow stages
3. **Comprehensive Analysis**: Don't skip subtasks or linked tickets
4. **Error Handling**: Document limitations and environmental constraints
5. **Dual File Generation**: Create both complete analysis and clean test-cases-only files
6. **Feature Deployment Verification**: Always check if implementation is deployed in validation environment

## Common JIRA Ticket Types
- **Story**: Main feature tickets (like ACM-20640)
- **Sub-task**: Implementation pieces (often contain PR references)
- **Epic**: High-level initiatives (may block stories)
- **Bug**: Issue fixes (usually have specific PRs)
- **Task**: QE and automation work

## Test Table Writing Reference

### Comprehensive Example Patterns

Based on analysis of successful Polarion test cases, these patterns ensure high-quality, executable test steps:

#### Pattern 1: Basic Action-Verification Steps
```markdown
| Log in to ACM Console | User is successfully logged in, and the ACM dashboard is displayed. |
```

#### Pattern 2: Navigation with UI Element Specification
```markdown
| From the ACM dashboard, select **Infrastructure** > **Clusters**, Click on Create Cluster and choose "OpenShift Virtualization" as the control plane type. | The cluster creation wizard opens with the first configuration step displayed. |
```

#### Pattern 3: Complex Validation with Goal and Sub-actions
```markdown
| **Verify Presence of Networking Options Section**<br>**Goal:** Confirm the "Networking Options" section is available under the "Node Pools" configuration step.<br>• Navigate to the **Node Pools** step in the wizard.<br>• Expand the "Networking Options" section in the node pool configuration. | A collapsible section titled "Networking Options" is present, containing fields for additional networks and a checkbox for the default pod network. |
```

#### Pattern 4: Input Validation Testing
```markdown
| **Verify Additional Network Name Validation**<br>**Goal:** Validate that additional network names follow the required format: lower-case letters and hyphens only.<br>• Enter a value with uppercase letters (e.g., Invalid/Name) and observe.<br>• Enter a value with special characters (e.g., namespace/n@me) and observe. | The system rejects invalid names and displays an appropriate error message. Both parts of the namespace/name must contain only lower-case letters and hyphens. |
```

#### Pattern 5: Configuration Persistence Testing
```markdown
| **Verify Networking Options Persist Across Wizard Navigation**<br>**Goal:** Validate that entered data in the "Networking Options" section persists when navigating between steps.<br>• Configure the Networking Options section with valid data (e.g., additional networks and default pod network state).<br>• Navigate to a different step in the wizard.<br>• Return to the Networking Options section. | Previously entered data is retained and displayed correctly. |
```

#### Pattern 6: Integration and Output Verification
```markdown
| **Verify Networking Options Integration with Node Pools**<br>**Goal:** Confirm the networking configuration is applied correctly for node pools.<br>• Complete the Networking Options section with valid data.<br>• Proceed through the wizard and create the cluster.<br>• After creation, inspect the resulting NodePool configuration via the YAML view or API. | Networking options (additional networks and default pod network state) are reflected accurately in the NodePool configuration. |
```

### Test Table Writing Guidelines

**Step Numbering**: Use consecutive numbering (1, 2, 3...) for each test step

**Formatting Standards**:
- **Bold text** for section headers and key UI elements
- `Code formatting` for commands, field names, and technical terms
- Bullet points (•) for sub-actions within a step
- `<br>` tags for line breaks in table cells
- Parenthetical examples: (e.g., "default/my-network")

**Action Verbs to Use**:
- Navigate, Click, Select, Enter, Verify, Confirm, Validate, Inspect, Observe, Toggle

**Expected Results Precision**:
- Use specific, measurable outcomes
- Include exact UI text that should appear
- Specify system responses and state changes
- Define clear success criteria

**Progressive Test Structure**:
1. **Setup/Login steps** (1-2 steps)
2. **Basic navigation** (1-2 steps) 
3. **Feature verification** (3-6 steps)
4. **Edge case validation** (2-4 steps)
5. **Integration testing** (1-3 steps)

## Framework Limitations & Troubleshooting

### Critical Requirements
- **Environment Setup**: Framework uses `setup_clc qe6` for automatic configuration OR points to current env set in kubeconfig
- **JIRA Authentication**: JIRA CLI must be properly configured
- **Repository Access**: Public GitHub repositories supported; private repos may require authentication

### Common Issues
1. **Environment Setup**: Use `source setup_clc qe6` to automatically resolve connectivity and authentication
2. **JIRA CLI Authentication**: Ensure proper JIRA setup before starting
3. **WebFetch Rate Limits**: Space out GitHub PR requests if needed
4. **Missing PRs**: Some tasks/subtasks may not have PR references yet
5. **Missing Docs**: Some tasks/subtasks may not have doc references yet
6. **Feature Not Deployed**: Implementation merged but not yet deployed to validation environment
7. **Image Version Mismatch**: Current cluster components may lack latest feature commits

### Framework Advancements
This framework represents significant advancement in automated test generation, combining:
- AI capabilities with intelligent validation
- Adaptive learning and human oversight
- Real-world robustness across development/testing scenarios
- Ability to handle missing features and adapt to different environments
- Dual output generation for different stakeholder needs
- Feature deployment verification and environment awareness

The framework's ability to handle missing features, adapt to different environments, verify deployment status, and generate both comprehensive analysis and clean test cases makes it invaluable for QE teams working on complex enterprise software like Advanced Cluster Management.

