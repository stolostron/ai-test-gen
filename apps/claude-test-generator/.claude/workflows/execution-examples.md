# Workflow Execution Examples

## Input Requirements

User MUST provide:
- **JIRA Ticket ID** (e.g., ACM-22079) 

User MAY provide:
- **Target Environment** (qe6, qe7, qe8, custom) - defaults to qe6
- **Custom Environment Config** (if not using standard QE environments)

**Automatic Handling:**
- **Environment setup** will be attempted via `source setup_clc <environment>`
- **Graceful fallback** if environment unavailable - test generation continues
- **Clear status reporting** about environment accessibility and feature availability

**Output Format** (markdown preferred)
**Repository Access** (public repos supported)

## Framework 4-Agent Architecture Execution Pattern
**Phase 1: Enhanced Parallel Execution with Context Sharing**

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
CURRENT_RUN_DIR="$RUN_DIR/run-$(printf "%03d" $NEXT_RUN)-$(date +%Y%m%d-%H%M)"
mkdir -p "$CURRENT_RUN_DIR"

# PHASE 1a: Independent Parallel Execution
echo "🚀 **PHASE 1a: Independent Parallel Execution**"

# Launch Agent A and Agent D simultaneously
execute_phase_1a() {
    # Agent A: JIRA Analysis (background process)
    {
        echo "📋 Agent A (JIRA Analysis) → Deep hierarchy analysis of $TICKET_ID..."
        jira issue view $TICKET_ID --plain
        # Extract subtask IDs and analyze each
        # Extract PR references and component details  
        # Generate complete JIRA context
        echo "✅ Agent A (JIRA Analysis) → Complete (PRs: extracted, Components: identified)"
        JIRA_CONTEXT_READY=true
    } &
    AGENT_A_PID=$!
    
    # Agent D: Environment Validation (background process)  
    {
        echo "📋 Agent D (Environment) → Cluster authentication and validation..."
        ENVIRONMENT="${USER_ENVIRONMENT:-qe6}"
        if source setup_clc "$ENVIRONMENT" 2>/dev/null; then
            echo "✅ Environment $ENVIRONMENT configured successfully"
            ENV_STATUS="available"
        else
            echo "⚠️ Environment $ENVIRONMENT unavailable - proceeding with test generation"
            ENV_STATUS="unavailable"
        fi
        echo "✅ Agent D (Environment) → Complete (Cluster: $ENV_STATUS, ACM version: detected)"
        ENV_CONTEXT_READY=true
    } &
    AGENT_D_PID=$!
    
    # Parallel execution with real-time context sharing completed
    wait $AGENT_A_PID
    echo "📋 Phase 1 Agent A + Agent D completed with context sharing"
}

# PHASE 1b: Context-Informed Feature Detection
execute_phase_1b() {
    echo "🚀 **PHASE 1b: Context-Informed Feature Detection**"
    
    # Agent E: Feature Detection (with Agent A context)
    echo "📋 Agent E (Feature Detection) → deployment analysis with JIRA context..."
    
    # Now has specific context from Agent A:
    # - Exact PRs: from JIRA comment extraction
    # - Specific components: from JIRA analysis  
    # - Feature scope: from ticket hierarchy
    # - Implementation timeline: from PR dates
    
    # Targeted deployment validation
    perform_targeted_deployment_analysis "$JIRA_CONTEXT" "$ENV_CONTEXT"
    
    echo "✅ Agent E (Feature Detection) → Complete (Confidence: 95%+, Evidence-based)"
    
    # Wait for Agent D if still running
    wait $AGENT_D_PID 2>/dev/null || true
}

# Execute optimized workflow
execute_phase_1a
execute_phase_1b

# 6. Generate organized output files in current run directory
# Create: $CURRENT_RUN_DIR/Complete-Analysis.md
# Create: $CURRENT_RUN_DIR/Test-Cases.md  
# Create: $CURRENT_RUN_DIR/metadata.json

# 7. Update latest symlink
cd "$RUN_DIR" && ln -sfn "$(basename $CURRENT_RUN_DIR)" latest

# 8. Report completion
echo "✅ Optimized analysis complete in: $CURRENT_RUN_DIR"
echo "📂 Quick access via: $RUN_DIR/latest/"

# Supporting Functions for Context-Enhanced Environment Analysis
perform_targeted_deployment_analysis() {
    local jira_context="$1"
    local env_context="$2"
    
    echo "🎯 Performing targeted deployment analysis with complete context..."
    
    # Extract specific details from JIRA context
    local specific_prs=$(echo "$jira_context" | jq -r '.extracted_prs[]')
    local components=$(echo "$jira_context" | jq -r '.identified_components[]')
    local feature_scope=$(echo "$jira_context" | jq -r '.feature_details.scope')
    
    # 1. TARGETED CONTAINER IMAGE ANALYSIS
    for component in $components; do
        echo "🔍 Checking deployment of specific component: $component"
        oc get pods -n multicluster-engine | grep "$component"
        oc get pod <${component}-pod> -n multicluster-engine -o jsonpath='{.spec.containers[0].image}'
    done
    
    # 2. SPECIFIC BEHAVIORAL TESTING  
    echo "🧪 Testing specific feature behavior: $feature_scope"
    # Test exactly what was implemented in the PRs
    # Use specific annotations and fields identified from JIRA/PR analysis
    
    # 3. PRECISE VERSION CORRELATION
    echo "📅 Correlating PR timeline with deployment evidence..."
    # Compare PR merge dates with deployed image build dates
    # Provide specific evidence for deployment gap analysis
    
    # 4. CONFIDENCE ASSESSMENT
    echo "📊 Generating confidence assessment based on evidence..."
    # Higher confidence due to targeted analysis vs broad pattern matching
}
```

## Execution Status Reporting

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

## Phase 2 Agent B and C Execution Examples

### Phase 2 Parallel Execution with Corrected Agent B

```bash
# Phase 2: Context-Aware Parallel Execution
execute_phase_2_parallel() {
    local phase_1_context="$1"  # Results from Phase 1a+1b
    
    echo "🚀 **PHASE 2: Context-Aware Parallel Execution**"
    
    # Launch Agent B and Agent C simultaneously with Phase 1 context
    
    # Agent B: AI-Powered Documentation Intelligence (background)
    {
        echo "📋 Agent B (Documentation) → AI-powered documentation analysis..."
        
        # Method detection (sequence control - script handles)
        if gh --version &>/dev/null && gh auth status &>/dev/null; then
            METHOD="gh_cli"
            echo "✅ GitHub CLI detected - using enhanced documentation analysis"
        else
            METHOD="webfetch"
            echo "🔄 GitHub CLI not available - using WebFetch fallback"
        fi
        
        # AI Documentation Intelligence Service (decision logic - AI handles)
        echo "🤖 Invoking AI Documentation Intelligence Service..."
        
        local documentation_result=$(ai_documentation_intelligence_service.comprehensive_analysis \
            --feature-context="$phase_1_context" \
            --target-method="$METHOD" \
            --repository="stolostron/rhacm-docs" \
            --e2e-focus-required=true \
            --console-workflow-priority=true)
        
        # Execute AI-determined plan (sequence control - script handles)
        local execution_plan=$(echo "$documentation_result" | jq -r '.execution_plan')
        local optimal_branch=$(echo "$execution_plan" | jq -r '.optimal_branch')
        
        if [[ "$METHOD" == "gh_cli" ]]; then
            # Execute AI-provided GitHub CLI commands in sequence
            gh api repos/stolostron/rhacm-docs/contents/clusters --ref $optimal_branch
            local search_patterns=$(echo "$execution_plan" | jq -r '.search_patterns[]')
            for pattern in $search_patterns; do
                gh search code --repo stolostron/rhacm-docs "$pattern" --ref $optimal_branch
            done
        else
            # Execute AI-provided WebFetch commands in sequence
            local webfetch_urls=$(echo "$execution_plan" | jq -r '.webfetch_urls[]')
            for url in $webfetch_urls; do
                WebFetch: $url
            done
        fi
        
        # AI-triggered internet search if needed (AI decides, script executes)
        local internet_search_needed=$(echo "$execution_plan" | jq -r '.internet_search_required')
        if [[ "$internet_search_needed" == "true" ]]; then
            echo "📋 Agent B (Documentation) → AI detected gaps - executing targeted internet search..."
            local search_queries=$(echo "$execution_plan" | jq -r '.internet_search_strategy.search_queries[]')
            for query in $search_queries; do
                WebSearch: "$query"
            done
        fi
        
        echo "✅ Agent B (Documentation) → Complete (E2E patterns: extracted, Console workflows: identified)"
    } &
    AGENT_B_PID=$!
    
    # Agent C: AI-Powered GitHub Investigation (background)
    {
        echo "📋 Agent C (GitHub) → AI-powered GitHub investigation with JIRA context..."
        
        # Method detection (sequence control - script handles)
        if gh --version &>/dev/null && gh auth status &>/dev/null; then
            METHOD="gh_cli"
            echo "✅ GitHub CLI detected - using enhanced PR analysis"
        else
            METHOD="webfetch"
            echo "🔄 GitHub CLI not available - using WebFetch fallback"
        fi
        
        # AI GitHub Investigation Service (decision logic - AI handles)
        echo "🤖 Invoking AI GitHub Investigation Service for strategic analysis..."
        
        local investigation_strategy=$(ai_github_investigation_service.generate_investigation_strategy \
            --jira-context="$phase_1_context" \
            --target-method="$METHOD" \
            --investigation-scope="comprehensive" \
            --e2e-focus-required=true)
        
        echo "📋 AI strategy: Analyzing ALL PRs with intelligent prioritization"
        echo "📋 AI determined: $(echo "$investigation_strategy" | jq -r '.strategy_summary')"
        
        # Execute AI-determined investigation plan (script handles execution)
        local pr_strategies=$(echo "$investigation_strategy" | jq -c '.pr_analysis_plans[]')
        
        for pr_strategy in $pr_strategies; do
            local pr=$(echo "$pr_strategy" | jq -r '.pr_reference')
            local depth=$(echo "$pr_strategy" | jq -r '.investigation_depth')
            local impact_score=$(echo "$pr_strategy" | jq -r '.impact_score')
            
            echo "🔍 AI-guided analysis of PR $pr (depth: $depth, impact: $impact_score)"
            
            local repo=$(echo "$pr" | cut -d'#' -f1)
            local pr_number=$(echo "$pr" | cut -d'#' -f2)
            
            # Execute AI-determined analysis depth
            if [[ "$METHOD" == "gh_cli" ]]; then
                case "$depth" in
                    "deep")
                        gh pr view $pr_number --repo $repo --json title,body,state,files,reviews,comments
                        gh pr diff $pr_number --repo $repo
                        gh pr checks $pr_number --repo $repo
                        ;;
                    "moderate")
                        gh pr view $pr_number --repo $repo --json title,body,state,files
                        gh pr diff $pr_number --repo $repo
                        ;;
                    "summary")
                        gh pr view $pr_number --repo $repo --json title,body,state
                        ;;
                esac
            else
                # WebFetch execution of AI strategy
                case "$depth" in
                    "deep")
                        WebFetch: https://github.com/$pr
                        WebFetch: https://github.com/$pr/files
                        WebFetch: https://github.com/$pr/commits
                        ;;
                    "moderate"|"summary")
                        WebFetch: https://github.com/$pr
                        ;;
                esac
            fi
        done
        
        # AI-determined repository investigation
        local repo_strategies=$(echo "$investigation_strategy" | jq -c '.repository_analysis_plans[]')
        for repo_strategy in $repo_strategies; do
            local repo=$(echo "$repo_strategy" | jq -r '.repository')
            local search_terms=$(echo "$repo_strategy" | jq -r '.search_terms[]')
            
            echo "📂 AI-guided repository investigation: $repo"
            
            if [[ "$METHOD" == "gh_cli" ]]; then
                gh repo view $repo --json description,topics,primaryLanguage
                for term in $search_terms; do
                    gh search code --repo $repo "$term" --limit $(echo "$repo_strategy" | jq -r '.search_limit')
                done
            else
                WebFetch: https://github.com/$repo
            fi
        done
        
        echo "✅ Agent C (GitHub) → Complete (ALL PRs analyzed, Impact-prioritized, E2E patterns: identified)"
    } &
    AGENT_C_PID=$!
    
    # Wait for both agents to complete
    wait $AGENT_B_PID $AGENT_C_PID
    
    echo "📋 Phase 2 complete - both agents finished with enhanced context"
}
```

## Agent B Three-Stage Process Example

### ACM-22079 Real Execution Example

```bash
# Agent B Process for ACM-22079
execute_agent_b_enhanced() {
    echo "📚 Agent B (Documentation) → documentation analysis..."
    
    # Stage 1: GitHub CLI Documentation Investigation  
    TARGET_VERSION="2.15"  # From JIRA analysis
    COMPONENT="ClusterCurator"  # From Agent A
    
    # Check actual branch structure (corrected)
    if gh api repos/stolostron/rhacm-docs/branches/2.15_stage &>/dev/null; then
        DOCS_BRANCH="2.15_stage"
    elif gh api repos/stolostron/rhacm-docs/branches/2.14_stage &>/dev/null; then
        DOCS_BRANCH="2.14_stage"  # Fallback to available version
    fi
    
    echo "📋 Using documentation branch: $DOCS_BRANCH"
    
    # GitHub CLI investigation
    gh api repos/stolostron/rhacm-docs/contents/clusters/cluster-lifecycle --ref $DOCS_BRANCH
    gh search code --repo stolostron/rhacm-docs "ClusterCurator upgrade" --ref $DOCS_BRANCH
    
    # Stage 2: Assess Documentation Completeness
    DOC_COMPLETENESS=$(assess_findings)
    
    if [[ $DOC_COMPLETENESS -lt 80 ]]; then
        # Stage 3: Intelligent Internet Search
        echo "📋 Agent B (Documentation) → Documentation insufficient - initiating intelligent internet search..."
        
        WebSearch: "Red Hat ACM ClusterCurator digest-based upgrades"
        WebSearch: "OpenShift conditional updates digest configuration"
        WebFetch: https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes
        
        # Synthesize all findings
        synthesize_documentation_and_internet_research
    fi
    
    echo "✅ Agent B (Documentation) → Complete (Official patterns: extracted, Research: comprehensive)"
}
```

## Example Usage Scenarios

### Scenario 1: Standard Analysis with Agent B
```bash
# User provides: ACM-22079
# Phase 1: Agent A extracts PRs and components + Agent D validates qe6 with real-time context sharing
# Phase 2: Agent B uses GitHub CLI for docs (branch: 2.14_stage) + Agent C investigates PR #468
# Phase 2.5: QE Intelligence Service with ultrathink reasoning
# Phase 3: AI Strategic Analysis (Complexity, Ultrathink, Scoping, Titles)
# Phase 4: Pattern Extension Service test generation
# Expected: Complete analysis with official documentation + implementation details
```

### Scenario 2: Documentation Gaps Trigger Internet Search
```bash
# User provides: ACM-22079
# Phase 2: Agent B finds limited documentation in stolostron/rhacm-docs
# Agent B triggers: Intelligent internet search for additional context
# Expected: analysis combining git docs + internet research
```

### Scenario 3: GitHub CLI Unavailable - Graceful Fallback
```bash
# User provides: ACM-22079  
# Phase 2: Agent B detects GitHub CLI unavailable
# Agent B falls back: WebFetch method for documentation analysis
# Expected: Reliable analysis with WebFetch + internet search enhancement
```
