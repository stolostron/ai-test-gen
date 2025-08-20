# Detailed Workflow Stages

# Framework 3-Stage Intelligence Process

> **"Gather → Analyze → Build" methodology that maximizes accuracy and quality for any feature type**

## Stage 1: Data Collection (Phases 0-2.5)
**"Collect all relevant, useful data from every possible source"**

### Phase 0: Version Context Foundation
**SOPHISTICATED ENVIRONMENT AND CONTEXT ANALYSIS:** Deploy multi-layered intelligence to understand the complete analysis context before beginning.

```bash
# context detection and intelligence initialization
intelligent_context_analysis() {
    echo "🧠 Initializing AI Analysis Engine..."
    
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

### Phase 1: Enhanced Parallel Execution with Context Sharing
**4-Agent Coordination: Agent A (JIRA) + Agent D (Environment) with real-time context sharing**
**🔄 True Parallel Processing of Independent Tasks:**

### Agent A: JIRA Intelligence
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
    
    # 3. PR AND COMPONENT EXTRACTION
    echo "📋 Extracting PR references and component details..."
    # Extract GitHub PR links from JIRA comments
    # Identify specific components and repositories
    # Build complete context for Enhanced Agent D deployment assessment
    
    # OUTPUT: Complete JIRA context with PR context sharing
    JIRA_CONTEXT=$(generate_jira_context_output)
}
```

### Enhanced Agent D: Environment Intelligence with PR Context Awareness (Parallel)
**🌍 Comprehensive Environment + Deployment Assessment:**
- **Environment Health Assessment**: Multi-dimensional cluster health scoring and analysis
- **PR Context Integration**: Real-time context sharing from Agent A for informed deployment expectations
- **Comprehensive Deployment Assessment**: Combined environment + deployment validation in single agent
- **Extensive Real Data Collection**: Enhanced data collection with component-specific samples

```bash
execute_enhanced_environment_intelligence() {
    local base_context="$1"
    
    echo "🚀 Enhanced Agent D: Starting comprehensive environment intelligence..."
    
    # Stage 1: Environment Health Assessment (starts immediately in parallel)
    assess_environment_health() {
        echo "🌍 Assessing environment health and connectivity..."
        
        # Multi-dimensional health assessment
        local environment="${1:-qe6}"
        if source setup_clc "$environment" 2>/dev/null; then
            echo "✅ Environment $environment configured successfully"
            ENVIRONMENT_STATUS="available"
            
            # Cluster connectivity validation
            if oc version --client &>/dev/null && oc whoami &>/dev/null; then
                echo "✅ Cluster connectivity confirmed"
                CLUSTER_ACCESS="available"
            else
                echo "⚠️ Cluster access limited"
                CLUSTER_ACCESS="limited"
            fi
        else
            echo "⚠️ Environment $environment not accessible"
            ENVIRONMENT_STATUS="unavailable"
            CLUSTER_ACCESS="unavailable"
        fi
        
        # Version detection and compatibility analysis
        detect_environment_versions
    }
    
    # Stage 2: Mid-Stream Context Reception (non-blocking)
    receive_pr_context_stream() {
        echo "📥 Enhanced Agent D: Receiving PR context from Agent A..."
        
        # Non-blocking context reception from Agent A
        # Context includes: PR references, component targets, implementation scope
        PR_CONTEXT=$(receive_agent_a_context_stream)
        
        if [[ -n "$PR_CONTEXT" ]]; then
            echo "✅ PR context received: Enhanced deployment assessment enabled"
            CONTEXT_AVAILABLE=true
        else
            echo "⚠️ No PR context available: Using conservative deployment assessment"
            CONTEXT_AVAILABLE=false
        fi
    }
    
    # Stage 3: PR-Informed Deployment Assessment
    assess_deployment_with_pr_context() {
        echo "🎯 Enhanced Agent D: Performing PR-informed deployment assessment..."
        
        if [[ "$CONTEXT_AVAILABLE" == true ]]; then
            # Enhanced assessment with PR context
            echo "🔍 Analyzing deployment with PR timeline correlation..."
            
            # Component-specific deployment validation
            local components=$(echo "$PR_CONTEXT" | jq -r '.components[]')
            for component in $components; do
                echo "  📋 Validating $component deployment status..."
                validate_component_deployment "$component" "$PR_CONTEXT"
            done
            
            # Calculate informed deployment confidence
            DEPLOYMENT_CONFIDENCE=$(calculate_pr_informed_confidence)
            echo "📊 Deployment confidence: $DEPLOYMENT_CONFIDENCE (PR-informed)"
        else
            # Conservative assessment without PR context
            echo "🔍 Performing conservative deployment assessment..."
            DEPLOYMENT_CONFIDENCE=$(calculate_conservative_confidence)
            echo "📊 Deployment confidence: $DEPLOYMENT_CONFIDENCE (conservative)"
        fi
    }
    
    # Stage 4: Extensive Real Data Collection  
    collect_extensive_real_data() {
        echo "📊 Enhanced Agent D: Collecting extensive real data..."
        
        if [[ "$CONTEXT_AVAILABLE" == true && "$DEPLOYMENT_CONFIDENCE" > 0.8 ]]; then
            echo "🎯 Collecting component-specific data based on PR context..."
            collect_component_specific_data "$PR_CONTEXT"
        else
            echo "📋 Collecting standard real data..."
            collect_standard_real_data
        fi
    }
    
    # Execute enhanced workflow
    assess_environment_health "$base_context"
    receive_pr_context_stream &  # Non-blocking
    assess_deployment_with_pr_context
    collect_extensive_real_data
    
    # Generate comprehensive intelligence
    echo "✅ Enhanced Agent D: Comprehensive environment intelligence complete"
    echo "   Health Assessment: $ENVIRONMENT_STATUS"
    echo "   Deployment Assessment: $DEPLOYMENT_CONFIDENCE confidence"
    echo "   PR Context Integration: $CONTEXT_AVAILABLE"
    echo "   Real Data Collection: Enhanced with component-specific samples"
}
```

**Output:** Comprehensive environment intelligence with PR-informed deployment assessment

**🚨 Key Framework Simplification:**
- **Eliminates**: Redundant Agent E and Phase 1b complexity
- **Consolidates**: All environment and deployment assessment in Enhanced Agent D
- **Enhances**: PR context awareness for improved deployment confidence 85% → 95%
- **Maintains**: 30-second parallel execution performance

### Phase 2: Parallel Deep Investigation
**Agent B (Documentation) + Agent C (GitHub) parallel execution with Phase 1 context**

**CRITICAL**: **Smart Test Scope Analysis** - Focus ONLY on what actually changed in the feature implementation.

**Capabilities (with Phase 1 Enhanced Context):**
- **Intelligent Repository Network Analysis**: AI-driven discovery using JIRA-identified repositories
- **Deep Architectural Understanding**: Analysis of system architecture using specific component context  
- **Business Value Chain Analysis**: Understanding of feature impact using JIRA business context
- **Historical Pattern Correlation**: Learning from similar features using specific PR patterns
- **🎯 Code Change Impact Analysis**: Identify exactly what changed using specific PR references
- **📋 Test Scope Optimization**: Generate test cases ONLY for changed functionality using precise context

**Refer to `.claude/prompts/test-scoping-rules.md` for detailed smart scoping methodology.**

### Phase A: Documentation Intelligence (with JIRA Context)
```bash
perform_enhanced_documentation_intelligence() {
    local jira_context="$1"     # Complete context from Agent A (JIRA Analysis)
    local environment_context="$2"  # Results from Enhanced Agent D
    
    echo "📚 Agent B (Documentation) → AI-powered documentation analysis with JIRA context..."
    
    # 1. METHOD DETECTION (Sequence Control - KEEP as Script)
    if gh --version &>/dev/null && gh auth status &>/dev/null; then
        METHOD="gh_cli"
        echo "✅ GitHub CLI detected - using enhanced documentation analysis"
    else
        METHOD="webfetch"
        echo "🔄 GitHub CLI not available - using WebFetch fallback"
    fi
    
    # 2. AI DOCUMENTATION INTELLIGENCE SERVICE (Replace Decision Logic)
    echo "🤖 Invoking AI Documentation Intelligence Service..."
    
    # Use existing AI service instead of script decision logic
    local documentation_result=$(ai_documentation_intelligence_service.comprehensive_analysis \
        --feature-context="$jira_context" \
        --target-method="$METHOD" \
        --repository="stolostron/rhacm-docs" \
        --e2e-focus-required=true \
        --console-workflow-priority=true)
    
    # AI service handles:
    # ✅ Intelligent branch discovery and selection  
    # ✅ Documentation completeness assessment
    # ✅ Gap identification and internet search triggering
    # ✅ E2E scenario mapping from documentation
    # ✅ Console workflow pattern extraction
    # ✅ Comprehensive synthesis with E2E focus
    
    echo "✅ Agent B (Documentation) → AI service complete (E2E patterns: extracted, Console workflows: identified)"
    
    # 3. EXECUTION METHOD (Sequence Control - KEEP as Script)
    # AI service provides execution instructions, script follows sequence
    local execution_plan=$(echo "$documentation_result" | jq -r '.execution_plan')
    
    if [[ "$METHOD" == "gh_cli" ]]; then
        # Execute GitHub CLI commands provided by AI service
        execute_gh_cli_documentation_plan "$execution_plan"
    else
        # Execute WebFetch commands provided by AI service  
        execute_webfetch_documentation_plan "$execution_plan"
    fi
}

execute_gh_cli_documentation_plan() {
    local execution_plan="$1"
    
    # Execute AI-determined GitHub CLI commands in sequence
    local optimal_branch=$(echo "$execution_plan" | jq -r '.optimal_branch')
    local search_patterns=$(echo "$execution_plan" | jq -r '.search_patterns[]')
    
    echo "📋 AI selected documentation branch: $optimal_branch"
    
    # Execute AI-provided commands in deterministic sequence
    gh api repos/stolostron/rhacm-docs/contents/clusters --ref $optimal_branch
    
    for pattern in $search_patterns; do
        gh search code --repo stolostron/rhacm-docs "$pattern" --ref $optimal_branch
    done
}

execute_webfetch_documentation_plan() {
    local execution_plan="$1"
    
    # Execute AI-determined WebFetch commands in sequence
    local optimal_branch=$(echo "$execution_plan" | jq -r '.optimal_branch')
    local webfetch_urls=$(echo "$execution_plan" | jq -r '.webfetch_urls[]')
    
    echo "📋 AI selected documentation branch: $optimal_branch"
    
    # Execute AI-provided WebFetch commands in sequence
    for url in $webfetch_urls; do
        WebFetch: $url
    done
    
    # AI-triggered internet search if gaps detected
    local internet_search_needed=$(echo "$execution_plan" | jq -r '.internet_search_required')
    if [[ "$internet_search_needed" == "true" ]]; then
        execute_ai_internet_search_plan "$execution_plan"
    fi
}

execute_ai_internet_search_plan() {
    local execution_plan="$1"
    
    echo "🌐 AI-triggered intelligent internet search..."
    
    # Execute AI-determined search strategy (not fixed patterns)
    local search_strategy=$(echo "$execution_plan" | jq -r '.internet_search_strategy')
    local search_queries=$(echo "$search_strategy" | jq -r '.search_queries[]')
    local webfetch_targets=$(echo "$search_strategy" | jq -r '.webfetch_targets[]')
    
    # AI-determined search execution
    for query in $search_queries; do
        WebSearch: "$query"
    done
    
    for target in $webfetch_targets; do
        WebFetch: "$target"
    done
}
```

### Phase B: GitHub Investigation (with JIRA Context)
```bash
perform_enhanced_github_investigation() {
    local jira_context="$1"     # Complete context from Phase 1a
    local deployment_context="$2"  # Results from Phase 1b
    
    echo "💻 Agent C (GitHub) → AI-powered GitHub investigation with JIRA context..."
    
    # 1. METHOD DETECTION (Script - Sequence Control)
    if gh --version &>/dev/null && gh auth status &>/dev/null; then
        METHOD="gh_cli"
        echo "✅ GitHub CLI detected - using enhanced PR analysis"
    else
        METHOD="webfetch"
        echo "🔄 GitHub CLI not available - using WebFetch fallback"
    fi
    
    # 2. AI GITHUB INVESTIGATION SERVICE (AI - Strategic Decision Making)
    echo "🤖 Invoking AI GitHub Investigation Service for strategic analysis..."
    
    # AI service analyzes ALL PRs and determines investigation strategy
    local investigation_strategy=$(ai_github_investigation_service.generate_investigation_strategy \
        --jira-context="$jira_context" \
        --deployment-context="$deployment_context" \
        --target-method="$METHOD" \
        --investigation-scope="comprehensive" \
        --e2e-focus-required=true)
    
    # AI service determines for EACH PR:
    # ✅ Investigation depth (deep|moderate|summary) based on PR impact
    # ✅ Focus areas (implementation|testing|integration) per PR
    # ✅ Code analysis scope (full-diff|key-files|summary) per PR
    # ✅ Related work importance (critical|helpful|skip) per PR
    # ✅ Search strategy per repository (targeted|broad|focused)
    
    echo "📋 AI strategy: $(echo "$investigation_strategy" | jq -r '.strategy_summary')"
    
    # 3. EXECUTE AI-DETERMINED INVESTIGATION PLAN (Script - Reliable Execution)
    if [[ "$METHOD" == "gh_cli" ]]; then
        execute_ai_gh_cli_investigation_plan "$investigation_strategy"
    else
        execute_ai_webfetch_investigation_plan "$investigation_strategy"
    fi
    
    # 4. AI ANALYSIS AND SYNTHESIS (AI - Intelligence Processing)
    echo "🤖 AI analyzing investigation results for E2E testing implications..."
    local final_analysis=$(ai_github_investigation_service.synthesize_results \
        --investigation-data="$INVESTIGATION_RESULTS" \
        --strategy="$investigation_strategy" \
        --e2e-requirements=true)
    
    echo "✅ Agent C (GitHub) → Complete (Implementation: analyzed, E2E patterns: identified, Testing strategy: optimized)"
}

execute_ai_gh_cli_investigation_plan() {
    local investigation_strategy="$1"
    
    echo "📋 Executing AI-determined GitHub CLI investigation plan..."
    
    # AI provides specific investigation plan for EACH PR
    local pr_strategies=$(echo "$investigation_strategy" | jq -c '.pr_analysis_plans[]')
    
    for pr_strategy in $pr_strategies; do
        local pr=$(echo "$pr_strategy" | jq -r '.pr_reference')
        local depth=$(echo "$pr_strategy" | jq -r '.investigation_depth')
        local focus_areas=$(echo "$pr_strategy" | jq -r '.focus_areas[]')
        
        echo "🔍 AI-guided analysis of PR $pr (depth: $depth, focus: $focus_areas)"
        
        local repo=$(echo "$pr" | cut -d'#' -f1)
        local pr_number=$(echo "$pr" | cut -d'#' -f2)
        
        # Execute AI-determined commands based on depth and focus
        case "$depth" in
            "deep")
                # Comprehensive analysis for high-impact PRs
                gh pr view $pr_number --repo $repo --json title,body,state,author,files,reviews,comments
                gh pr diff $pr_number --repo $repo
                gh pr checks $pr_number --repo $repo
                gh api repos/$repo/pulls/$pr_number/files --jq '.[].filename'
                ;;
            "moderate")
                # Focused analysis for medium-impact PRs
                gh pr view $pr_number --repo $repo --json title,body,state,files
                gh pr diff $pr_number --repo $repo
                ;;
            "summary")
                # Basic analysis for low-impact PRs
                gh pr view $pr_number --repo $repo --json title,body,state
                ;;
        esac
        
        # AI-determined related work analysis
        local related_work_needed=$(echo "$pr_strategy" | jq -r '.analyze_related_work')
        if [[ "$related_work_needed" == "true" ]]; then
            local search_terms=$(echo "$pr_strategy" | jq -r '.related_search_terms[]')
            for term in $search_terms; do
                gh pr list --repo $repo --search "in:title $term" --json number,title,state --limit 5
            done
        fi
    done
    
    # Execute AI-determined repository investigation plan
    local repo_strategies=$(echo "$investigation_strategy" | jq -c '.repository_analysis_plans[]')
    
    for repo_strategy in $repo_strategies; do
        local repo=$(echo "$repo_strategy" | jq -r '.repository')
        local search_scope=$(echo "$repo_strategy" | jq -r '.search_scope')
        local search_terms=$(echo "$repo_strategy" | jq -r '.search_terms[]')
        
        echo "📂 AI-guided repository investigation: $repo (scope: $search_scope)"
        
        # Repository metadata (always collected)
        gh repo view $repo --json description,topics,primaryLanguage,defaultBranch,updatedAt
        
        # AI-determined search strategy
        for term in $search_terms; do
            echo "🔍 AI-determined search: $term"
            gh search code --repo $repo "$term" --limit $(echo "$repo_strategy" | jq -r '.search_limit')
        done
        
        # AI-determined repository analysis depth
        case "$search_scope" in
            "comprehensive")
                gh pr list --repo $repo --state merged --limit 20 --json number,title,mergedAt
                gh release list --repo $repo --limit 10 --json tagName,publishedAt
                ;;
            "focused")
                gh pr list --repo $repo --state merged --limit 5 --json number,title,mergedAt
                ;;
            "minimal")
                # Basic repository overview only
                ;;
        esac
    done
}

execute_ai_webfetch_investigation_plan() {
    local investigation_strategy="$1"
    
    echo "📋 Executing AI-determined WebFetch investigation plan..."
    
    # AI provides WebFetch strategy for each PR
    local pr_strategies=$(echo "$investigation_strategy" | jq -c '.pr_analysis_plans[]')
    
    for pr_strategy in $pr_strategies; do
        local pr=$(echo "$pr_strategy" | jq -r '.pr_reference')
        local depth=$(echo "$pr_strategy" | jq -r '.investigation_depth')
        
        echo "🔍 AI-guided WebFetch analysis of PR $pr (depth: $depth)"
        
        # Execute AI-determined WebFetch commands
        case "$depth" in
            "deep")
                WebFetch: https://github.com/$pr
                WebFetch: https://github.com/$pr/files
                WebFetch: https://github.com/$pr/commits
                ;;
            "moderate")
                WebFetch: https://github.com/$pr
                WebFetch: https://github.com/$pr/files
                ;;
            "summary")
                WebFetch: https://github.com/$pr
                ;;
        esac
    done
    
    # Execute AI-determined repository WebFetch plan
    local repo_strategies=$(echo "$investigation_strategy" | jq -c '.repository_analysis_plans[]')
    
    for repo_strategy in $repo_strategies; do
        local repo=$(echo "$repo_strategy" | jq -r '.repository')
        local webfetch_targets=$(echo "$repo_strategy" | jq -r '.webfetch_targets[]')
        
        echo "📂 AI-guided repository WebFetch: $repo"
        
        for target in $webfetch_targets; do
            WebFetch: $target
        done
    done
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

### Phase 2.5: QE Intelligence Analysis with Ultrathink
**Strategic testing pattern analysis using sophisticated reasoning**

---

## Stage 2: AI Analysis (Phase 3)
**"Make sense of ALL collected data and create strategic intelligence"**

### AI Strategic Services Sequential Analysis

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
        # scenario generation:
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

---

## Stage 3: Report Construction (Phase 4)
**"Build professional test plan using strategic intelligence"**

### Pattern Extension Service Test Generation

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
**Purpose**: Generate comprehensive, strategically-designed test suites with **optimal table organization**. Each test case table contains **4-10 steps optimized for workflow complexity** for cognitive efficiency, with multiple tables generated as needed to achieve complete coverage.

**Table Structure Format with YAML Samples:**
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
|| **Step 1**: [Action with business context] - **Goal**: [Why this step matters] - **Command**: `oc apply -f -` (stdin) - Example YAML:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  featureFlag: "enabled"
``` | **Success Criteria**: Specific, measurable outcome - **Validation**: `oc get configmap app-config -o jsonpath='{.data.featureFlag}'` - **Expected Output**: `enabled` - **Sample YAML Result** (if environment accessible):
```yaml
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

### Final Report Generation and Quality Assurance

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
