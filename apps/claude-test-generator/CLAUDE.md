# Intelligent Test Analysis Engine - Advanced AI Configuration

## System Architecture
This is a **sophisticated AI-powered analysis engine** designed to perform human-level reasoning about complex software systems. It combines multiple AI techniques, deep learning from organizational patterns, and advanced analytical capabilities to deliver enterprise-grade test intelligence.

**Core Intelligence Features**: Multi-source analysis, adaptive learning, predictive modeling, risk assessment, and continuous optimization.

## Intelligent System Overview
**Mission:** Deploy advanced AI reasoning to understand complex software features at architectural, business, and technical levels, generating strategic test approaches that anticipate risks and optimize quality outcomes.
**Intelligence Level:** Expert-level analysis with continuous learning and adaptation capabilities.
**Scope:** Universal application to any software project - enterprise systems, web applications, microservices, cloud platforms, mobile apps, and beyond. Adapts intelligence level to project complexity and domain.

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

## Advanced AI Analysis Framework

### Stage 0: Intelligent Pre-Analysis Assessment
**SOPHISTICATED ENVIRONMENT AND CONTEXT ANALYSIS:** Deploy multi-layered intelligence to understand the complete analysis context before beginning.

```bash
# Advanced context detection and intelligence initialization
intelligent_context_analysis() {
    echo "🧠 Initializing Advanced AI Analysis Engine..."
    
    # 1. BUSINESS CONTEXT INTELLIGENCE
    analyze_business_impact() {
        echo "📊 Analyzing business impact and criticality..."
        # Extract customer names, SLA requirements, business value indicators
        # Classify feature type: customer-critical, internal-improvement, compliance, etc.
        # Assess risk level and business continuity impact
    }
    
    # 2. TECHNICAL COMPLEXITY ASSESSMENT  
    assess_technical_complexity() {
        echo "🔬 Performing technical complexity analysis..."
        # Analyze codebase complexity, integration points, dependency chains
        # Identify potential failure modes and technical risks
        # Classify testing complexity: simple, moderate, complex, expert-level
    }
    
    # 3. ORGANIZATIONAL LEARNING ACTIVATION
    activate_learning_systems() {
        echo "🎓 Activating organizational learning systems..."
        # Load historical patterns from similar features
        # Identify successful testing approaches from past tickets
        # Extract team-specific preferences and constraints
    }
    
    # 4. PREDICTIVE RISK MODELING
    generate_risk_predictions() {
        echo "⚠️ Generating predictive risk models..."
        # Predict likely failure scenarios based on feature type
        # Identify high-risk integration points
        # Assess deployment and operational risks
    }
}
```

**Enterprise Environment Setup Process:**
```bash
# Intelligent environment setup with ACM cluster auto-discovery
source setup_clc qe6

# The setup_clc script provides sophisticated environment management:
# 1. JENKINS INTEGRATION: Fetches latest successful deployment from ACM Jenkins CI/CD
# 2. CLUSTER AUTO-LOGIN: Automatically logs into OpenShift cluster with deployment credentials  
# 3. ACM ENVIRONMENT DISCOVERY: Auto-detects ACM/MCE namespaces and versions
# 4. CLC REPOSITORY DETECTION: Finds and configures CLC test repositories automatically
# 5. DEPENDENCY MANAGEMENT: Sets up npm dependencies and browserslist updates
# 6. ENVIRONMENT VALIDATION: Validates cluster access and prerequisite tools
```

**Why setup_clc? - Enterprise Testing Intelligence:**
The `setup_clc` script is **essential for sophisticated ACM testing** because it:

**🏗️ Infrastructure Automation:**
- **Auto-fetches deployment credentials** from Jenkins CI/CD pipeline artifacts
- **Maps environment names** (qe6, qe7, qe8, qe9, qe10) to actual cluster deployments
- **Handles authentication complexity** with multiple auth methods (user/pass, tokens)
- **Manages cluster API endpoints** and console URLs automatically

**🔍 CLC-Specific Intelligence & Test Repository Management:**

**Universal Project Intelligence?** The Intelligent Test Analysis Engine is **designed for any software project** with adaptive domain intelligence:

1. **Domain Adaptation**: Automatically recognizes project type (web app, microservice, platform, mobile, etc.)
2. **Technology Stack Intelligence**: Adapts to any tech stack - React, Java, Python, Go, .NET, mobile, cloud-native
3. **Business Impact Analysis**: Understands customer/user impact regardless of industry or domain
4. **Complexity Scaling**: Adjusts analysis depth from simple features to enterprise-scale systems

**CLC Test Repository Ecosystem:**
```bash
# PRIMARY TEST REPOSITORIES (Auto-detected by setup_clc):

~/Documents/work/automation/clc-ui/          # CLC UI E2E Tests (Cypress)
├── cypress/
│   ├── integration/                        # Main test suites
│   │   ├── create-cluster/                # Cluster creation workflows
│   │   ├── upgrade-cluster/               # Cluster upgrade scenarios  
│   │   ├── destroy-cluster/               # Cluster destruction flows
│   │   └── import-cluster/                # Cluster import processes
│   ├── fixtures/                          # Test data and configurations
│   └── support/                           # Common utilities and helpers

~/Documents/work/automation/clc-non-ui/     # CLC Backend/API Tests (Go)
├── pkg/
│   ├── clusterlifecycle/                  # Core CLC API testing
│   ├── clustercurator/                    # ClusterCurator controller tests
│   └── integration/                       # Cross-component integration tests

~/Documents/work/automation/alc-ui/         # Application Lifecycle Tests
├── tests/                                 # Application-focused test suites
└── cypress/                               # UI automation for app workflows
```

**How the System Knows Where Tests Are:**
The intelligent system uses **multi-layer test discovery**:

1. **Repository Auto-Detection**: `setup_clc` script automatically finds CLC repos
2. **Git Remote Analysis**: Validates repositories by checking Git remotes for `stolostron/clc*` patterns
3. **Test Pattern Recognition**: Analyzes existing test structures to understand team patterns
4. **Environment Integration**: Connects test locations with deployment environments (qe6, qe7, etc.)

**Strategic CLC Focus Benefits:**
- **Domain Expertise**: Deep understanding of CLC-specific testing challenges
- **Pattern Recognition**: Learning from extensive CLC test history and patterns  
- **Integration Intelligence**: Knowledge of CLC dependencies and failure modes
- **Enterprise Scenarios**: Specialized handling of disconnected, air-gapped, and enterprise clusters

**📊 Enterprise QE Workflow Integration:**
- **Jenkins API Integration**: Direct connection to ACM QE Jenkins pipelines
- **Multi-Environment Support**: Seamless switching between QE environments
- **Credential Management**: Secure handling of cluster credentials and tokens
- **Team Collaboration**: Standardized environment setup across QE team

**This is why we use `setup_clc qe6` instead of manual setup** - it provides enterprise-grade automation for the complex ACM testing infrastructure.

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

### Stage 2: Comprehensive Multi-Source Intelligence Gathering

**Advanced Capabilities:**
- **Intelligent Repository Network Analysis**: AI-driven discovery of related repositories and components
- **Deep Architectural Understanding**: Analysis of system architecture and component interactions  
- **Business Value Chain Analysis**: Understanding of feature impact on customer workflows
- **Historical Pattern Correlation**: Learning from similar features across the organization

**Sophisticated Analysis Process:**

#### Phase A: Advanced JIRA Intelligence
```bash
perform_advanced_jira_analysis() {
    local ticket_id="$1"
    
    echo "🔍 Performing sophisticated JIRA analysis..."
    
    # 1. MULTI-DIMENSIONAL TICKET ANALYSIS
    jira issue view "$ticket_id" --plain | analyze_ticket_intelligence
    
    # Extract and analyze:
    # - Business value propositions and customer impact
    # - Technical complexity indicators and architectural changes
    # - Risk factors and compliance requirements
    # - Dependencies and integration touchpoints
    # - Acceptance criteria sophistication and edge cases
    
    # 2. RELATIONSHIP NETWORK ANALYSIS
    echo "🕸️ Analyzing ticket relationship networks..."
    # Map subtasks, blockers, dependencies, and related features
    # Identify impact propagation across feature sets
    # Understand epic-level strategic context
    
    # 3. STAKEHOLDER AND TEAM CONTEXT
    echo "👥 Analyzing stakeholder and team context..."  
    # Identify key stakeholders and their concerns
    # Understand team expertise and testing preferences
    # Extract customer-specific requirements and constraints
}
```

#### Phase B: Intelligent Repository and Code Analysis
```bash
perform_intelligent_code_analysis() {
    echo "💻 Performing advanced code and architecture analysis..."
    
    # 1. ARCHITECTURAL IMPACT ANALYSIS
    analyze_architectural_changes() {
        # Identify modified components and their architectural role
        # Assess impact on system reliability and performance
        # Map integration points and data flow changes
        # Evaluate security and compliance implications
    }
    
    # 2. QUALITY AND RISK ASSESSMENT
    assess_code_quality_risks() {
        # Analyze code complexity and maintainability impact
        # Identify potential performance bottlenecks
        # Assess backward compatibility and migration risks
        # Evaluate operational and monitoring implications
    }
    
    # 3. CROSS-COMPONENT DEPENDENCY ANALYSIS
    analyze_system_dependencies() {
        # Map dependencies across microservices and components
        # Identify cascade failure scenarios
        # Assess integration testing requirements
        # Understand deployment coordination needs
    }
}
```

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


### Stage 3: Advanced AI Reasoning and Strategic Test Intelligence

**Sophisticated Analysis Dimensions:**

#### Deep Feature Understanding with AI Reasoning
```bash
perform_ai_feature_reasoning() {
    echo "🧠 Deploying advanced AI reasoning for feature understanding..."
    
    # 1. SEMANTIC FEATURE ANALYSIS
    analyze_feature_semantics() {
        # Use natural language processing to understand feature intent
        # Extract implicit requirements from feature descriptions
        # Identify unstated assumptions and edge conditions
        # Map feature to business process workflows
    }
    
    # 2. ARCHITECTURAL REASONING
    perform_architectural_reasoning() {
        # Understand system design patterns and their implications
        # Reason about scalability and performance characteristics  
        # Identify potential architectural debt and technical risks
        # Assess alignment with enterprise architecture principles
    }
    
    # 3. BUSINESS IMPACT MODELING
    model_business_impact() {
        # Quantify business value and revenue impact
        # Assess customer experience implications
        # Identify compliance and regulatory considerations
        # Map to organizational strategic objectives
    }
}
```

#### Strategic Test Planning with Predictive Intelligence
```bash
generate_strategic_test_approach() {
    echo "🎯 Generating strategic test approach with predictive intelligence..."
    
    # 1. RISK-BASED TEST PRIORITIZATION
    prioritize_tests_by_risk() {
        # Calculate risk scores based on:
        # - Business impact severity
        # - Technical complexity factors
        # - Historical failure patterns
        # - Customer usage patterns
        # - Regulatory compliance requirements
    }
    
    # 2. INTELLIGENT TEST COVERAGE OPTIMIZATION
    optimize_test_coverage() {
        # Apply coverage optimization algorithms:
        # - Identify critical paths through feature logic
        # - Minimize test redundancy while maximizing coverage
        # - Focus on high-value, high-risk scenarios
        # - Balance thoroughness with execution efficiency
    }
    
    # 3. ADAPTIVE TEST SCENARIO GENERATION
    generate_adaptive_scenarios() {
        # Advanced scenario generation:
        # - **Positive Flows**: Business-value-driven happy paths
        # - **Intelligent Edge Cases**: AI-predicted boundary conditions
        # - **Failure Mode Analysis**: Systematic failure scenario modeling
        # - **Integration Complexity**: Cross-system interaction patterns
        # - **Performance and Scale**: Load and stress testing scenarios
        # - **Security and Compliance**: Risk-based security testing
        # - **Operational Readiness**: Production deployment validation
    }
}
```

#### Continuous Learning and Pattern Recognition
```bash
apply_organizational_learning() {
    echo "📚 Applying organizational learning and pattern recognition..."
    
    # 1. HISTORICAL PATTERN ANALYSIS
    analyze_historical_patterns() {
        # Extract successful testing patterns from organization history
        # Identify common failure modes for similar features
        # Learn from past test execution results and defect patterns
        # Adapt based on team-specific testing effectiveness data
    }
    
    # 2. PREDICTIVE DEFECT MODELING
    predict_likely_defects() {
        # Use machine learning on historical defect data
        # Predict where bugs are most likely to occur
        # Identify high-risk code areas requiring focused testing
        # Generate targeted test cases for predicted failure points
    }
    
    # 3. INTELLIGENT TEST OPTIMIZATION
    optimize_test_execution() {
        # Optimize test execution order and dependency management
        # Predict test execution duration and resource requirements
        # Identify opportunities for parallel test execution
        # Recommend test environment and data requirements
    }
}
``` 

### Stage 4: Sophisticated Test Strategy Generation & Quality Optimization

**Enterprise-Grade Intelligent Generation Process:**

#### Sophisticated Test Architecture Design with Intelligent Table Structure
**Purpose**: Generate comprehensive, strategically-designed test suites with **optimal table organization**. Each test case table contains **8-10 steps maximum** for cognitive efficiency, with multiple tables generated as needed to achieve complete coverage.

```bash
design_sophisticated_test_architecture() {
    echo "🏗️ Designing sophisticated test architecture with intelligent table structure..."
    
    # 1. INTELLIGENT TABLE ORGANIZATION STRATEGY
    organize_test_tables() {
        # COGNITIVE LOAD OPTIMIZATION: Maximum 8-10 steps per table
        # - Human attention span: 7±2 items (Miller's Law)
        # - Polarion import efficiency: Tables under 10 steps
        # - Test execution focus: Single logical workflow per table
        
        # BUSINESS-CRITICAL TEST SUITES (Priority 1)
        generate_business_critical_tables() {
            # Table 1: Core Feature Validation (8-10 steps)
            # Table 2: Customer Impact Scenarios (8-10 steps)  
            # Table 3: Revenue Protection Workflows (8-10 steps)
            # Table 4: Compliance Verification (8-10 steps)
        }
        
        # TECHNICAL EXCELLENCE TEST SUITES (Priority 2)
        generate_technical_excellence_tables() {
            # Table 5: Integration Testing (8-10 steps)
            # Table 6: Performance Validation (8-10 steps)
            # Table 7: Security Assessment (8-10 steps)
            # Table 8: Error Handling & Edge Cases (8-10 steps)
        }
        
        # OPERATIONAL READINESS TEST SUITES (Priority 3)
        generate_operational_readiness_tables() {
            # Table 9: Deployment Verification (8-10 steps)
            # Table 10: Monitoring & Observability (8-10 steps)
            # Table 11: Disaster Recovery (8-10 steps)
            # Table 12: Scalability Testing (8-10 steps)
        }
    }
    
    # 2. INTELLIGENT TEST CASE DEPTH OPTIMIZATION
    optimize_test_case_depth() {
        # DYNAMIC COMPLEXITY-BASED TABLE GENERATION:
        
        # Simple Features (5-8 tables total):
        # - 1-2 Business validation tables
        # - 2-3 Technical verification tables  
        # - 1-2 Operational readiness tables
        
        # Moderate Features (8-15 tables total):
        # - 3-4 Business validation tables
        # - 5-7 Technical verification tables
        # - 3-4 Operational readiness tables
        
        # Complex Features (15-25 tables total):
        # - 5-7 Business validation tables
        # - 8-12 Technical verification tables
        # - 5-8 Operational readiness tables
        
        # Expert-Level Features (25-50 tables total):
        # - 8-12 Business validation tables
        # - 12-25 Technical verification tables
        # - 8-15 Operational readiness tables
    }
}
```

**Sophisticated Table Structure Format:**
```markdown
### Test Case N: [Business Context] - [Technical Focus]

**Business Value**: Clear statement of customer/business impact
**Technical Scope**: Specific technical components and integration points  
**Risk Level**: High/Medium/Low based on business impact analysis
**Execution Environment**: Specific cluster and tool requirements

**Prerequisites**: 
- Environment and tools set up (e.g., cluster access, API auth) as applicable
- Test data/configs available
- Validation tools and access permissions

| Test Steps (Max 8-10 for cognitive efficiency) | Expected Results (with specific validation criteria) |
|------------|------------------|
| **Step 1**: [Action with business context]<br/>**Goal**: [Why this step matters]<br/>**Command**: `oc apply -f -` (stdin)<br/>Example YAML:<br/>```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  featureFlag: "enabled"
``` | **Success Criteria**: Specific, measurable outcome<br/>Validation (example): `oc get configmap app-config -o jsonpath='{.data.featureFlag}'` → `enabled` |
| **Step 2-10**: [Continue pattern...] | [Continue pattern...] |

**Sample YAML snippets (generic, simple) to embed inline with steps:**

Use these minimal examples directly inside a table cell when it helps clarify the action or expected state. Keep them short (3-10 lines).

1) Small config value (ConfigMap)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  featureFlag: "enabled"
```

2) Deployment readiness probe (fragment)
```yaml
readinessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

3) Simple job/pipeline step
```yaml
name: build
run: npm ci && npm test
```

4) Minimal API payload example
```yaml
user:
  id: 123
  email: user@example.com
```

**Inline YAML in table cells (both columns) - examples:**

```markdown
| Test Steps | Expected Results |
|---|---|
| Create a readiness probe on the service deployment.<br/>Apply patch:<br/>```yaml
readinessProbe:
  httpGet:
    path: /healthz
    port: 8080
``` | Deployment becomes Ready within 30s.<br/>`kubectl get deploy svc -o jsonpath='{.status.readyReplicas}'` → `1` |

| Send a POST request with payload below to /users API.<br/>Payload:<br/>```yaml
user:
  id: 123
  email: user@example.com
``` | API responds `201 Created` and returns the created user.<br/>Body contains:<br/>```yaml
user:
  id: 123
  email: user@example.com
``` |
```

**Essential CLC-Specific CLI Commands with Expected Outputs**:

**1. Environment Discovery & Validation:**
```bash
# ACM/MCE namespace auto-discovery (from setup_clc)
export ACM_NS=$(oc get subscriptions.operators.coreos.com -A -o json | jq -r '.items[] | select(.spec.name=="advanced-cluster-management").metadata.namespace')
export MCE_NS=$(oc get mce -ojsonpath="{.items[0].spec.targetNamespace}")

echo "ACM Namespace: $ACM_NS"    # Expected: "open-cluster-management" or custom
echo "MCE Namespace: $MCE_NS"    # Expected: "multicluster-engine" or custom

# Cluster connectivity validation
oc whoami --show-server
# Expected: https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443

oc get clusterversion
# Expected: 
# NAME      VERSION   AVAILABLE   PROGRESSING   SINCE   STATUS
# version   4.15.10   True        False         5d      Cluster version is 4.15.10
```

**2. ACM Component Status Verification:**
```bash
# ACM Hub Status
oc get multiclusterhub -n $ACM_NS
# Expected:
# NAME                STATUS    AGE
# multiclusterhub     Running   25d

# MCE Engine Status  
oc get multiclusterengine -n $MCE_NS
# Expected:
# NAME                        STATUS      AGE
# multiclusterengine-sample   Available   25d

# Managed Cluster Inventory
oc get managedclusters
# Expected:
# NAME              HUB ACCEPTED   MANAGED CLUSTER URLS                                            JOINED   AVAILABLE   AGE
# local-cluster     true           https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com   True     True        25d
# spoke-cluster-1   true           https://api.spoke1.company.com:6443                             True     True        10d
```

**3. CLC Operations Monitoring:**
```bash
# ClusterCurator Status (Upgrade Operations)
oc get clustercurator -A -o wide
# Expected:
# NAMESPACE        NAME                     CURATION   STATUS        AGE
# cluster-ns-1     production-upgrade       upgrade    InProgress    15m
# cluster-ns-2     staging-upgrade          upgrade    Succeeded     2h

# ClusterDeployment Status (Creation Operations)
oc get clusterdeployment -A
# Expected:
# NAMESPACE      NAME                    PLATFORM   REGION      AGE
# spoke-ns-1     new-cluster-deploy      vsphere    us-east-1   45m
# spoke-ns-2     backup-cluster-deploy   aws        us-west-2   2h

# Hive ClusterImageSet Availability
oc get clusterimageset
# Expected:
# NAME                      RELEASE
# img4.15.10-x86-64         quay.io/openshift-release-dev/ocp-release:4.15.10-x86_64
# img4.14.15-x86-64         quay.io/openshift-release-dev/ocp-release:4.14.15-x86_64
```

**4. Digest-Based Upgrade Verification (ACM-22079):**
```bash
# Verify digest annotation support  
oc get clustercurator production-upgrade -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/digest-source}'
# Expected: "disconnected-registry" (if digest-based) or empty (if version-based)

# Check digest validation status
oc get clustercurator production-upgrade -o jsonpath='{.status.conditions[?(@.type=="DigestValidationSuccessful")].status}'
# Expected: "True" (success) or "False" (failure)

# Monitor upgrade progress with digest details
oc describe clustercurator production-upgrade | grep -A 5 -B 5 digest
# Expected: Event logs showing digest validation and download progress
```

**5. Troubleshooting & Debug Commands:**
```bash
# ClusterCurator Controller Logs
oc logs deployment/cluster-curator-controller -n $ACM_NS -f
# Expected: Real-time controller logs showing upgrade operations

# Hive Controller Logs for ClusterDeployment issues
oc logs deployment/hive-controllers -n hive -f
# Expected: Logs from Hive controllers managing cluster lifecycle

# ACM Console Pod Status (for UI testing)
oc get pods -n $ACM_NS | grep console
# Expected:
# console-chart-v2-console-v2-abc123-xyz789   1/1     Running   0          25d

# Check for failed pods across ACM components
oc get pods -A | grep -E "(Error|CrashLoopBackOff|ImagePullBackOff)"
# Expected: Empty output (no failed pods) or specific failure details to investigate
```
```

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

#### Organized Output File Generation & Run Management
**MANDATORY**: Always use organized folder structure for every analysis:

**Directory Structure:**
```
runs/
├── <TICKET-ID>/                     # Main ticket folder (e.g., ACM-22079/)
│   ├── run-001-YYYYMMDD-HHMM/      # First run with timestamp
│   │   ├── Complete-Analysis.md     # Comprehensive analysis
│   │   ├── Test-Cases.md           # Clean test cases only
│   │   ├── Test-Plan.md            # Original format for compatibility
│   │   └── metadata.json           # Run metadata and settings
│   ├── run-002-YYYYMMDD-HHMM/      # Second run (different approach/update)
│   │   └── ...
│   └── latest -> run-XXX-YYYYMMDD-HHMM  # Symlink to latest run
└── archived-runs/                   # Completed/old ticket runs
```

**Automatic Run Numbering Process:**
1. **Check existing runs**: Look for `runs/<TICKET-ID>/` directory
2. **Generate run number**: Auto-increment based on existing `run-XXX` folders
3. **Create timestamp**: Use format `YYYYMMDD-HHMM` for uniqueness
4. **Update latest symlink**: Point to newest run for easy access

**Required Sophisticated Output Files:**
1. **Complete-Analysis.md**: Deep enterprise-level analysis with AI reasoning
2. **Strategic-Test-Plan.md**: Comprehensive test strategy with risk assessment
3. **Test-Cases.md**: Sophisticated test cases with business context
4. **Quality-Assessment.md**: AI-driven quality metrics and optimization recommendations  
5. **Risk-Analysis.md**: Predictive risk modeling and mitigation strategies
6. **metadata.json**: Advanced metadata with AI insights and learning data

**Enhanced Metadata Structure:**
```json
{
  "analysis_intelligence": {
    "ai_confidence_score": 0.95,
    "complexity_assessment": "expert-level",
    "business_impact_score": 9.2,
    "technical_risk_score": 7.1,
    "predicted_test_execution_time": "4.5 hours",
    "recommended_environment": "staging-cluster-high-spec"
  },
  "learning_data": {
    "patterns_applied": ["cluster-lifecycle-v2", "enterprise-validation"],
    "historical_references": ["ACM-21890", "ACM-20642"],
    "optimization_suggestions": [
      "Focus on disconnected environment testing",
      "Emphasize digest validation workflows",
      "Include failure rollback scenarios"
    ]
  },
  "quality_metrics": {
    "test_coverage_score": 94,
    "business_value_alignment": 96,
    "technical_depth_score": 91,
    "risk_mitigation_coverage": 89
  }
}
```

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

### Enhanced Analysis Pattern with Organized Output
```bash
# 1. Determine run directory and number
TICKET_ID="ACM-22079"  # Extract from user input or JIRA analysis
RUN_DIR="runs/${TICKET_ID}"

# Check existing runs and auto-increment
if [ -d "$RUN_DIR" ]; then
    NEXT_RUN=$(ls -1 "$RUN_DIR" | grep "^run-" | wc -l | xargs expr 1 +)
else
    mkdir -p "$RUN_DIR"
    NEXT_RUN=1
fi

# Create timestamped run directory
TIMESTAMP=$(date +%Y%m%d-%H%M)
CURRENT_RUN_DIR="$RUN_DIR/run-$(printf "%03d" $NEXT_RUN)-$TIMESTAMP"
mkdir -p "$CURRENT_RUN_DIR"

# 2. Environment setup (automatic)
source setup_clc qe6

# 3. Systematic JIRA analysis
jira issue view $TICKET_ID --plain

# 4. Subtask and linked ticket analysis
# (Extract subtask IDs from main ticket and analyze each)

# 5. PR analysis via WebFetch
# (Extract GitHub URLs from JIRA comments and analyze)

# 6. Generate organized output files in current run directory
# Create: $CURRENT_RUN_DIR/Complete-Analysis.md
# Create: $CURRENT_RUN_DIR/Test-Cases.md  
# Create: $CURRENT_RUN_DIR/Test-Plan.md
# Create: $CURRENT_RUN_DIR/metadata.json

# 7. Update latest symlink
cd "$RUN_DIR" && ln -sfn "$(basename $CURRENT_RUN_DIR)" latest

# 8. Report completion
echo "✅ Analysis complete in: $CURRENT_RUN_DIR"
echo "📂 Quick access via: $RUN_DIR/latest/"
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

<!-- Offline-mode content removed to keep the system universally applicable and simple. -->

## Framework Robustness & Best Practices

### Enhanced Error Handling & Recovery
1. **Graceful Degradation**: Continue analysis even if some components fail
2. **Retry Logic**: Automatically retry failed operations with exponential backoff
3. **Validation Checkpoints**: Verify each step before proceeding
4. **Rollback Capability**: Restore previous state if current run fails
5. **Resource Cleanup**: Clean up partial runs and temporary files

### Input Validation & Sanitization
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

### Improved Workflow Automation
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

### Critical Requirements & Dependencies
- **Claude CLI**: Version 1.0+ with proper authentication
- **JIRA CLI**: Configured with valid API token
- **Git**: For repository access and change tracking
- **Shell**: Bash 4.0+ or Zsh for script compatibility
- **Disk Space**: Minimum 1GB free for run storage
- **Network**: Stable connection for GitHub/JIRA API calls

### Enhanced Troubleshooting Guide
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

### Framework Advancements
This framework represents significant advancement in automated test generation, combining:
- AI capabilities with intelligent validation
- Adaptive learning and human oversight
- Real-world robustness across development/testing scenarios
- Ability to handle missing features and adapt to different environments
- Dual output generation for different stakeholder needs
- Feature deployment verification and environment awareness

The framework's ability to handle missing features, adapt to different environments, verify deployment status, and generate both comprehensive analysis and clean test cases makes it invaluable for QE teams working on complex enterprise software like Advanced Cluster Management.

