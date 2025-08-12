# Detailed Workflow Stages

## Stage 0: Intelligent Pre-Analysis Assessment
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

## Stage 1: Environment Setup & Validation
**🌍 Flexible Environment Configuration:**
- **Default Environment**: Use `source setup_clc qe6` if no specific environment provided
- **Custom Environment Support**: Accept user-specified environment (qe7, qe8, staging, dev, etc.)
- **Environment Override**: Allow users to provide custom cluster credentials and endpoints
- **Graceful Validation**: Continue with test generation even if environment validation fails

**Environment Validation Process:**
```bash
validate_test_environment() {
    local environment="${1:-qe6}"  # Default to qe6 if not specified
    
    echo "🌍 Validating test environment: $environment"
    
    # Try environment setup
    if source setup_clc "$environment" 2>/dev/null; then
        echo "✅ Environment $environment configured successfully"
        ENVIRONMENT_STATUS="available"
    else
        echo "⚠️ Environment $environment not accessible"
        echo "📋 Proceeding with test generation for future execution"
        ENVIRONMENT_STATUS="unavailable"
    fi
    
    # Validate cluster connectivity if environment available
    if [[ "$ENVIRONMENT_STATUS" == "available" ]]; then
        if oc version --client &>/dev/null && oc whoami &>/dev/null; then
            echo "✅ Cluster connectivity confirmed"
            CLUSTER_ACCESS="available"
        else
            echo "⚠️ Cluster access limited"
            CLUSTER_ACCESS="limited"
        fi
    else
        CLUSTER_ACCESS="unavailable"
    fi
    
    # Set execution status for test plan generation
    case "$ENVIRONMENT_STATUS-$CLUSTER_ACCESS" in
        "available-available")
            echo "🟢 Full validation possible - tests can be executed immediately"
            EXECUTION_STATUS="immediate"
            ;;
        "available-limited")
            echo "🟡 Partial validation possible - some tests can be executed"
            EXECUTION_STATUS="partial"
            ;;
        *)
            echo "🔴 Environment unavailable - test plan ready for future execution"
            EXECUTION_STATUS="future"
            ;;
    esac
}
```

**🚨 Critical Validation Philosophy:**
- **Always Generate Tests**: Create comprehensive test plans regardless of environment status
- **Clear Status Reporting**: Document what can/cannot be validated in current environment
- **Future Readiness**: Ensure test plans work when proper environment is available

**Output:** Environment readiness report with clear execution guidance

## Stage 2: Comprehensive Multi-Source Intelligence Gathering

**CRITICAL**: **Smart Test Scope Analysis** - Focus ONLY on what actually changed in the feature implementation.

**Advanced Capabilities:**
- **Intelligent Repository Network Analysis**: AI-driven discovery of related repositories and components
- **Deep Architectural Understanding**: Analysis of system architecture and component interactions  
- **Business Value Chain Analysis**: Understanding of feature impact on customer workflows
- **Historical Pattern Correlation**: Learning from similar features across the organization
- **🎯 Code Change Impact Analysis**: Identify exactly what code paths, functions, and workflows were modified
- **📋 Test Scope Optimization**: Generate test cases ONLY for changed functionality, skip existing stable features

**Refer to `.claude/prompts/test-scoping-rules.md` for detailed smart scoping methodology.**

### Phase A: Advanced JIRA Intelligence
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

### Phase B: Intelligent Repository and Code Analysis with Smart Test Scoping
```bash
perform_intelligent_code_analysis() {
    echo "💻 Performing advanced code and architecture analysis..."
    
    # 1. PRECISE CHANGE SCOPE ANALYSIS
    analyze_exact_code_changes() {
        echo "🎯 Analyzing exactly what changed in the implementation..."
        # Extract specific files modified from PR analysis
        # Identify new functions, modified functions, and unchanged functions
        # Map code changes to business logic flows
        # Categorize changes: NEW functionality vs MODIFIED functionality vs UNCHANGED
        
        # Example for digest-based upgrades:
        # NEW: validateUpgradeVersion() returns digest string
        # NEW: Digest discovery algorithm (conditionalUpdates → availableUpdates → fallback)
        # NEW: Smart force flag logic (no force with digests)
        # UNCHANGED: General upgrade monitoring, timeout handling, error recovery
    }
    
    # 2. TEST SCOPE OPTIMIZATION
    optimize_test_scope() {
        echo "📋 Optimizing test scope to focus on changed functionality..."
        # Generate test cases ONLY for:
        # - NEW code paths and functions
        # - MODIFIED business logic flows
        # - Integration points between new and existing code
        
        # SKIP test cases for:
        # - Existing unchanged functionality
        # - General error handling (unless specifically modified)
        # - Monitoring and logging (unless enhanced for new feature)
        # - UI components (unless changed for new feature)
    }
    
    # 3. ARCHITECTURAL IMPACT ANALYSIS
    analyze_architectural_changes() {
        # Identify modified components and their architectural role
        # Assess impact on system reliability and performance
        # Map integration points and data flow changes
        # Evaluate security and compliance implications
    }
    
    # 4. DEPENDENCY AND INTEGRATION TESTING REQUIREMENTS
    analyze_integration_requirements() {
        # Map dependencies between new and existing functionality
        # Identify critical integration points requiring testing
        # Focus on workflows that span new and existing code
        # Skip pure existing-to-existing integrations
    }
}
```

## Stage 3: Advanced AI Reasoning and Strategic Test Intelligence

### Deep Feature Understanding with AI Reasoning
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

### Strategic Test Planning with Predictive Intelligence
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

## Stage 4: Sophisticated Test Strategy Generation & Quality Optimization

**🎯 CRITICAL: Smart Test Scope Analysis Before Test Generation**

**MANDATORY Pre-Test Generation Analysis:**
```bash
analyze_implementation_scope() {
    echo "🔍 Analyzing exact implementation scope for targeted testing..."
    
    # 1. EXTRACT PRECISE CODE CHANGES
    extract_code_changes() {
        # From PR analysis, identify:
        # - Files modified (with line counts)
        # - Functions added/modified/unchanged
        # - New business logic vs unchanged logic
        # - Integration points between new and existing code
        
        # Example output:
        # NEW: validateUpgradeVersion() - returns digest string
        # NEW: Digest discovery algorithm (conditionalUpdates → availableUpdates → fallback)
        # NEW: Smart force flag logic (digest vs tag-based)
        # UNCHANGED: General upgrade monitoring, timeout handling
        # UNCHANGED: UI components, error recovery, networking
    }
    
    # 2. GENERATE FOCUSED TEST SCOPE
    generate_test_scope() {
        echo "📋 Generating focused test scope..."
        
        # TEST THESE (New/Modified functionality):
        TEST_SCOPE_INCLUDE=(
            "New annotation processing logic"
            "Digest discovery from conditionalUpdates"
            "Fallback mechanism to availableUpdates"
            "Smart force flag behavior (digest vs tag)"
            "Integration between new digest logic and existing upgrade workflow"
        )
        
        # SKIP THESE (Unchanged functionality):
        TEST_SCOPE_EXCLUDE=(
            "General upgrade monitoring (unchanged)"
            "Timeout handling (unchanged)"
            "Network error recovery (unchanged)"
            "UI components (unchanged)"
            "Logging and metrics (unchanged unless enhanced)"
        )
        
        echo "✅ Will test: ${TEST_SCOPE_INCLUDE[@]}"
        echo "❌ Will skip: ${TEST_SCOPE_EXCLUDE[@]}"
    }
    
    # 3. OPTIMIZE TABLE COUNT
    optimize_table_count() {
        # Rule: Aim for 1-3 tables that test the NEW functionality comprehensively
        # Avoid: 10+ tables testing every possible scenario including unchanged logic
        # Focus: E2E scenarios that exercise the new code paths
        
        RECOMMENDED_TABLES=(
            "Core Digest Discovery Workflow (annotation → conditionalUpdates → digest)"
            "Fallback Mechanism Validation (conditionalUpdates → availableUpdates → tag)"
            "Integration with Existing Upgrade Flow (new digest logic + existing ClusterCurator)"
        )
        
        echo "🎯 Recommended test tables: ${#RECOMMENDED_TABLES[@]}"
    }
}
```

### Sophisticated Test Architecture Design with Intelligent Table Structure
**Purpose**: Generate comprehensive, strategically-designed test suites with **optimal table organization**. Each test case table contains **8-10 steps maximum** for cognitive efficiency, with multiple tables generated as needed to achieve complete coverage.

**Enhanced Table Structure Format with YAML Samples:**
```markdown
### Test Case N: [Business Context] - [Technical Focus]

**Business Value**: Clear statement of customer/business impact
**Technical Scope**: Specific technical components and integration points  
**Risk Level**: High/Medium/Low based on business impact analysis
**Execution Environment**: Default qe6 (or user-specified environment)

**Prerequisites**: 
- Environment and tools set up (e.g., cluster access, API auth) as applicable
- Test data/configs available
- Validation tools and access permissions

|| Test Steps (Max 8-10 for cognitive efficiency) | Expected Results (with YAML samples & validation details) |
||------------|------------------|
|| **Step 1**: [Action with business context]<br/>**Goal**: [Why this step matters]<br/>**Command**: `oc apply -f -` (stdin)<br/>Example YAML:<br/>```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  featureFlag: "enabled"
``` | **Success Criteria**: Specific, measurable outcome<br/>**Validation**: `oc get configmap app-config -o jsonpath='{.data.featureFlag}'`<br/>**Expected Output**: `enabled`<br/>**Sample YAML Result** (if environment accessible):<br/>```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  featureFlag: "enabled"
``` |
|| **Step 2-10**: [Continue pattern...] | [Continue pattern...] |
```

**Refer to `.claude/templates/yaml-samples.md` for comprehensive YAML sample templates.**

## Stage 5: Comprehensive Analysis Report & Feedback Loop

### Final Analysis Report Format
**Required Components:**
1. **Feature Implementation Status** (first)
   - PR merge status and commit information
   - Key behaviors introduced and scope
   - Backwards compatibility and risk notes

2. **Environment & Validation Status** (second)
   - Which test cases can be executed immediately
   - Which require newer environment deployment
   - Specific validation failures and their root causes

3. **Environment Deployment Analysis**
   - Current image versions vs. implementation requirements
   - Expected deployment timeline for feature availability
   - Alternative testing approaches if feature unavailable

### Organized Output File Generation & Run Management
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

**Test Plan Generation Philosophy:**

**🎯 ALWAYS GENERATE COMPREHENSIVE TEST PLANS**: Regardless of current deployment status, always create complete, thorough test cases that assume the feature is fully implemented. The test plan should be ready for a build that has the feature.

**Test Plan Impact Classification with Environment Flexibility:**
- **🟢 FEATURE FULLY DEPLOYED**: All test cases executable immediately on current environment
- **🟡 FEATURE PARTIALLY DEPLOYED**: Some test cases executable now, others ready for full deployment  
- **🔴 FEATURE NOT DEPLOYED**: Complete test plan ready for execution on environment with feature
- **🟠 DEPLOYMENT STATUS UNCLEAR**: Full test plan ready, manual verification recommended
- **🌍 ENVIRONMENT UNAVAILABLE**: Test plan ready for execution when environment accessible

**Execution Status Reporting Format:**
```markdown
## Execution Status
**Environment**: [qe6/qe7/custom/unavailable]
**Feature Deployment**: [✅ Available / ⚠️ Partial / ❌ Not Available / 🔍 Unknown]
**Immediate Execution**: [✅ Ready / ⚠️ Limited / ❌ Requires Deployment / 🌍 Requires Environment]

### Current Limitations
- Environment access: [Details about environment accessibility]
- Feature availability: [Details about feature deployment status]
- Validation scope: [What can/cannot be validated currently]

### Future Execution
- When environment available: [All test cases executable]
- When feature deployed: [All test cases executable]  
- Alternative environments: [List other suitable environments]
```
