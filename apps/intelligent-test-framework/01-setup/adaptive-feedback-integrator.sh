#!/bin/bash

# adaptive-feedback-integrator.sh - Adaptive Test Plan Refinement System
# Integrates validation feedback to continuously improve test generation

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FEEDBACK_DB="$PROJECT_ROOT/feedback-database.json"
KNOWLEDGE_BASE="$PROJECT_ROOT/knowledge-base.json"
REFINEMENT_LOG="$PROJECT_ROOT/test-plan-refinements.json"

print_status() {
    echo -e "${BLUE}[ADAPTIVE]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_learning() {
    echo -e "${PURPLE}[LEARNING]${NC} $1"
}

# Initialize adaptive refinement system
init_adaptive_system() {
    print_status "🧠 Initializing adaptive feedback integration system"
    
    # Create refinement tracking
    cat > "$REFINEMENT_LOG" << EOF
{
  "refinement_session": {
    "started_at": "$(date -Iseconds)",
    "jira_ticket": "$JIRA_TICKET",
    "original_test_plan": "$ORIGINAL_TEST_PLAN",
    "refinements_applied": []
  },
  "learning_insights": {
    "patterns_detected": [],
    "improvements_made": [],
    "confidence_scores": {}
  },
  "next_iteration_recommendations": []
}
EOF
}

# Analyze validation feedback to identify improvement opportunities
analyze_validation_feedback() {
    local validation_results="$1"
    
    print_status "📊 Analyzing validation feedback for improvement opportunities"
    
    if [ ! -f "$validation_results" ]; then
        print_error "Validation results not found: $validation_results"
        return 1
    fi
    
    # Check for smart analysis indicating missing feature scenario
    local validation_type=$(jq -r '.validation_type // "standard"' "$validation_results")
    local smart_analysis=$(jq -r '.smart_analysis // ""' "$validation_results")
    
    # Extract failure patterns
    local failed_stages=$(jq -r '.validation_stages | to_entries[] | select(.value.status == "failed") | .key' "$validation_results")
    local root_cause=$(jq -r '.feedback_analysis.root_cause // "unknown"' "$validation_results")
    local recommended_actions=$(jq -r '.feedback_analysis.recommended_actions[]?' "$validation_results")
    
    if [ "$validation_type" = "pre_implementation" ]; then
        print_learning "🧠 SMART DETECTION: Missing feature scenario identified"
        print_learning "📋 Adapting feedback for pre-implementation testing approach"
        root_cause="missing_feature: Feature not yet implemented - expected scenario for early testing"
    else
        print_learning "Detected failure patterns:"
        echo "$failed_stages" | while read -r stage; do
            if [ -n "$stage" ]; then
                print_learning "  - Failed stage: $stage"
                analyze_stage_failure "$stage" "$validation_results"
            fi
        done
    fi
    
    if [ "$root_cause" != "unknown" ] && [ "$root_cause" != "null" ]; then
        print_learning "Root cause identified: $root_cause"
        generate_refinement_recommendations "$root_cause"
    fi
}

# Analyze specific stage failures for learning
analyze_stage_failure() {
    local stage="$1"
    local validation_results="$2"
    
    local stage_details=$(jq -r ".validation_stages.$stage.details[]?" "$validation_results")
    
    case "$stage" in
        "feature_availability")
            analyze_feature_availability_patterns "$stage_details"
            ;;
        "environment_readiness")
            analyze_environment_patterns "$stage_details"
            ;;
        "test_logic")
            analyze_test_logic_patterns "$stage_details"
            ;;
        "expected_results")
            analyze_results_patterns "$stage_details"
            ;;
    esac
}

analyze_feature_availability_patterns() {
    local details="$1"
    
    print_learning "Feature availability analysis:"
    
    if echo "$details" | grep -q "CRD not found"; then
        record_learning_insight "feature_crd_missing" \
            "ClusterCurator CRD not available - likely version or deployment issue" \
            "Add CRD availability check to test prerequisites"
    fi
    
    if echo "$details" | grep -q "controller not found"; then
        record_learning_insight "feature_controller_missing" \
            "ClusterCurator controller not running - operator issue" \
            "Add controller readiness validation to test plan"
    fi
    
    if echo "$details" | grep -q "API not available"; then
        record_learning_insight "feature_api_unavailable" \
            "ClusterCurator API not accessible - RBAC or version issue" \
            "Enhance API availability validation in test setup"
    fi
}

analyze_environment_patterns() {
    local details="$1"
    
    print_learning "Environment readiness analysis:"
    
    if echo "$details" | grep -q "connectivity.*FAILED"; then
        record_learning_insight "env_connectivity_issue" \
            "Cluster connectivity problems detected" \
            "Add network connectivity validation to test prerequisites"
    fi
    
    if echo "$details" | grep -q "ACM installation.*NOT FOUND"; then
        record_learning_insight "env_acm_missing" \
            "ACM not properly installed or accessible" \
            "Add ACM installation validation to environment setup"
    fi
    
    if echo "$details" | grep -q "permissions.*INSUFFICIENT"; then
        record_learning_insight "env_rbac_issue" \
            "Insufficient permissions for test operations" \
            "Add RBAC validation and setup instructions to test plan"
    fi
}

analyze_test_logic_patterns() {
    local details="$1"
    
    print_learning "Test logic analysis:"
    
    if echo "$details" | grep -q "Command invalid"; then
        record_learning_insight "test_invalid_commands" \
            "Test commands are invalid or outdated" \
            "Update test commands to match current API versions"
    fi
    
    if echo "$details" | grep -q "creation.*Invalid"; then
        record_learning_insight "test_invalid_resources" \
            "Resource definitions don't match current schema" \
            "Update resource definitions and validation logic"
    fi
}

analyze_results_patterns() {
    local details="$1"
    
    print_learning "Expected results analysis:"
    
    if echo "$details" | grep -q "creation.*FAILED"; then
        record_learning_insight "results_creation_failed" \
            "Resource creation failed - schema or permission issue" \
            "Review resource creation logic and permissions"
    fi
    
    if echo "$details" | grep -q "status structure.*MISSING"; then
        record_learning_insight "results_status_missing" \
            "Expected status structure not found - API change" \
            "Update status validation logic for current API version"
    fi
}

# Record learning insights for knowledge base evolution
record_learning_insight() {
    local insight_type="$1"
    local problem_description="$2"
    local recommended_solution="$3"
    
    local insight_entry=$(cat << EOF
{
  "timestamp": "$(date -Iseconds)",
  "type": "$insight_type",
  "problem": "$problem_description",
  "solution": "$recommended_solution",
  "confidence": 0.8,
  "source": "adaptive_analysis"
}
EOF
)
    
    jq ".learning_insights.patterns_detected += [$insight_entry]" "$REFINEMENT_LOG" > "${REFINEMENT_LOG}.tmp"
    mv "${REFINEMENT_LOG}.tmp" "$REFINEMENT_LOG"
    
    print_learning "Recorded insight: $insight_type"
}

# Generate refinement recommendations based on analysis
generate_refinement_recommendations() {
    local root_cause="$1"
    
    print_status "🎯 Generating refinement recommendations"
    
    # Analyze historical patterns for similar issues
    if [ -f "$FEEDBACK_DB" ]; then
        local similar_patterns=$(jq -r ".feedback_patterns[] | select(.failure_pattern | contains(\"$root_cause\")) | .recommended_actions[]" "$FEEDBACK_DB" 2>/dev/null)
        
        if [ -n "$similar_patterns" ]; then
            print_learning "Found similar historical patterns:"
            echo "$similar_patterns" | while read -r action; do
                if [ -n "$action" ]; then
                    print_learning "  - Historical solution: $action"
                    add_refinement_recommendation "historical" "$action"
                fi
            done
        fi
    fi
    
    # Generate AI-powered refinement recommendations
    generate_ai_refinement_recommendations "$root_cause"
}

# Generate AI-powered refinement recommendations
generate_ai_refinement_recommendations() {
    local root_cause="$1"
    
    print_status "🤖 Generating AI-powered refinement recommendations"
    
    # Create AI prompt for test plan refinement with format preservation
    local refinement_prompt="CRITICAL: Improve test plan content while preserving exact table format with '| Test Steps | Expected Results |'.

VALIDATION ANALYSIS:
Root Cause: $root_cause

Historical Patterns: $(jq -r '.learning_insights.patterns_detected[].problem' "$REFINEMENT_LOG" 2>/dev/null | tail -5)

Current Test Plan Issues:
$(jq -r '.validation_stages | to_entries[] | select(.value.status == "failed") | "\(.key): \(.value.details | join(", "))"' "$PROJECT_ROOT/validation-results.json" 2>/dev/null)

CONTENT IMPROVEMENTS NEEDED (keep table format):
1. Fix test environment setup based on validation failures
2. Correct command accuracy and completeness 
3. Improve expected results specificity
4. Add missing test scenarios identified in validation
5. Enhance error handling and cleanup procedures

FORMAT PRESERVATION REQUIREMENTS:
- MUST maintain '| Test Steps | Expected Results |' table structure
- Keep Setup sections as bullet points  
- Preserve test case organization and numbering
- Do NOT change table format or structure

Provide actionable content improvements that address validation issues while maintaining exact table format."

    # Execute AI refinement analysis
    if command -v claude &> /dev/null; then
        local ai_recommendations=$(claude --print "$refinement_prompt" 2>/dev/null)
        
        if [ -n "$ai_recommendations" ]; then
            print_learning "AI-generated recommendations:"
            echo "$ai_recommendations" | head -20
            
            # Store AI recommendations
            echo "$ai_recommendations" > "$PROJECT_ROOT/ai-refinement-recommendations.md"
            add_refinement_recommendation "ai_generated" "See ai-refinement-recommendations.md"
        fi
    else
        print_warning "Claude Code not available for AI refinement recommendations"
    fi
}

# Add refinement recommendation to tracking
add_refinement_recommendation() {
    local source="$1"
    local recommendation="$2"
    
    local rec_entry=$(cat << EOF
{
  "source": "$source",
  "recommendation": "$recommendation",
  "timestamp": "$(date -Iseconds)",
  "applied": false
}
EOF
)
    
    jq ".next_iteration_recommendations += [$rec_entry]" "$REFINEMENT_LOG" > "${REFINEMENT_LOG}.tmp"
    mv "${REFINEMENT_LOG}.tmp" "$REFINEMENT_LOG"
}

# Apply refinements to test plan
apply_refinements_to_test_plan() {
    local original_test_plan="$1"
    local refined_test_plan="$2"
    
    print_status "✏️ Applying refinements to test plan"
    
    if [ ! -f "$original_test_plan" ]; then
        print_error "Original test plan not found: $original_test_plan"
        return 1
    fi
    
    # Create refined test plan with improvements
    cp "$original_test_plan" "$refined_test_plan"
    
    # Apply specific refinements based on learning insights
    local refinement_count=0
    
    # Add prerequisite checks based on learned patterns
    if jq -e '.learning_insights.patterns_detected[] | select(.type == "feature_crd_missing")' "$REFINEMENT_LOG" > /dev/null 2>&1; then
        add_prerequisite_to_test_plan "$refined_test_plan" "Verify ClusterCurator CRD availability" "oc get crd clustercurators.cluster.open-cluster-management.io"
        ((refinement_count++))
    fi
    
    if jq -e '.learning_insights.patterns_detected[] | select(.type == "env_connectivity_issue")' "$REFINEMENT_LOG" > /dev/null 2>&1; then
        add_prerequisite_to_test_plan "$refined_test_plan" "Validate cluster connectivity" "oc cluster-info"
        ((refinement_count++))
    fi
    
    if jq -e '.learning_insights.patterns_detected[] | select(.type == "env_rbac_issue")' "$REFINEMENT_LOG" > /dev/null 2>&1; then
        add_prerequisite_to_test_plan "$refined_test_plan" "Verify required permissions" "oc auth can-i create clustercurator"
        ((refinement_count++))
    fi
    
    # Record applied refinements
    jq ".refinement_session.refinements_applied += [\"Applied $refinement_count prerequisite improvements\"]" "$REFINEMENT_LOG" > "${REFINEMENT_LOG}.tmp"
    mv "${REFINEMENT_LOG}.tmp" "$REFINEMENT_LOG"
    
    print_success "Applied $refinement_count refinements to test plan"
    print_success "Refined test plan: $refined_test_plan"
}

# Add prerequisite to test plan
add_prerequisite_to_test_plan() {
    local test_plan_file="$1"
    local description="$2"
    local validation_command="$3"
    
    # Add prerequisite section if it doesn't exist
    if ! grep -q "## Prerequisites" "$test_plan_file"; then
        echo -e "## Prerequisites\n\n$(cat $test_plan_file)" > "$test_plan_file"
    fi
    
    # Add the new prerequisite using echo instead of problematic sed
    local temp_file=$(mktemp)
    awk '/## Prerequisites/ {print; print ""; print "### " desc; print "```bash"; print cmd; print "```"; print ""; next} 1' \
        desc="$description" cmd="$validation_command" "$test_plan_file" > "$temp_file"
    mv "$temp_file" "$test_plan_file"
    
    print_learning "Added prerequisite: $description"
}

# Generate human-readable feedback report
generate_feedback_report() {
    print_status "📋 Generating comprehensive feedback report"
    
    local report_file="$PROJECT_ROOT/adaptive-feedback-report.md"
    
    cat > "$report_file" << EOF
# Adaptive Feedback Report

**Generated**: $(date)
**JIRA Ticket**: $JIRA_TICKET
**Session**: $(jq -r '.refinement_session.started_at' "$REFINEMENT_LOG")

## Validation Results Summary

$(jq -r '.validation_stages | to_entries[] | "- **\(.key)**: \(.value.status)" | @base64' "$PROJECT_ROOT/validation-results.json" 2>/dev/null | base64 -d 2>/dev/null || echo "No validation results available")

## Learning Insights Discovered

$(jq -r '.learning_insights.patterns_detected[] | "### \(.type)\n**Problem**: \(.problem)\n**Solution**: \(.solution)\n"' "$REFINEMENT_LOG" 2>/dev/null)

## Refinement Recommendations

$(jq -r '.next_iteration_recommendations[] | "- **\(.source)**: \(.recommendation)"' "$REFINEMENT_LOG" 2>/dev/null)

## Applied Improvements

$(jq -r '.refinement_session.refinements_applied[]' "$REFINEMENT_LOG" 2>/dev/null | sed 's/^/- /')

## Next Steps

1. Review refined test plan with applied improvements
2. Execute validation with updated prerequisites
3. Monitor results for further learning opportunities
4. Update team knowledge base with insights

EOF

    print_success "Feedback report generated: $report_file"
}

# Update team knowledge base with learned insights
update_team_knowledge_base() {
    print_status "📚 Updating team knowledge base"
    
    if [ ! -f "$KNOWLEDGE_BASE" ]; then
        echo '{"version": "1.0", "learned_patterns": [], "success_strategies": [], "common_failures": []}' > "$KNOWLEDGE_BASE"
    fi
    
    # Add learned patterns to knowledge base
    local patterns=$(jq -c '.learning_insights.patterns_detected[]' "$REFINEMENT_LOG" 2>/dev/null)
    if [ -n "$patterns" ]; then
        echo "$patterns" | while IFS= read -r insight; do
            if [ -n "$insight" ] && [ "$insight" != "null" ]; then
                jq --argjson pattern "$insight" '.learned_patterns += [$pattern]' "$KNOWLEDGE_BASE" > "${KNOWLEDGE_BASE}.tmp"
                mv "${KNOWLEDGE_BASE}.tmp" "$KNOWLEDGE_BASE"
            fi
        done
    fi
    
    # Add successful refinements as strategies
    local refinements=$(jq -r '.refinement_session.refinements_applied[]' "$REFINEMENT_LOG" 2>/dev/null)
    if [ -n "$refinements" ]; then
        echo "$refinements" | while IFS= read -r refinement; do
            if [ -n "$refinement" ] && [ "$refinement" != "null" ]; then
                local strategy_entry=$(cat << EOF
{
  "strategy": "$refinement",
  "effectiveness": "high",
  "learned_at": "$(date -Iseconds)",
  "source": "adaptive_feedback"
}
EOF
)
                jq --argjson strategy "$strategy_entry" '.success_strategies += [$strategy]' "$KNOWLEDGE_BASE" > "${KNOWLEDGE_BASE}.tmp"
                mv "${KNOWLEDGE_BASE}.tmp" "$KNOWLEDGE_BASE"
            fi
        done
    fi
    
    print_success "Knowledge base updated with new insights"
}

# Main adaptive feedback integration function
main() {
    local JIRA_TICKET="${1:-ACM-22079}"
    local ORIGINAL_TEST_PLAN="${2:-02-test-planning/test-plan.md}"
    local VALIDATION_RESULTS="${3:-validation-results.json}"
    
    print_status "🚀 Starting adaptive feedback integration for $JIRA_TICKET"
    
    init_adaptive_system
    
    # Analyze validation feedback
    if [ -f "$VALIDATION_RESULTS" ]; then
        analyze_validation_feedback "$VALIDATION_RESULTS"
    else
        print_warning "No validation results found - running in learning mode only"
    fi
    
    # Generate refinement recommendations
    generate_refinement_recommendations "validation_analysis"
    
    # Apply refinements if original test plan exists
    if [ -f "$ORIGINAL_TEST_PLAN" ]; then
        local refined_plan="${ORIGINAL_TEST_PLAN%.md}-refined.md"
        apply_refinements_to_test_plan "$ORIGINAL_TEST_PLAN" "$refined_plan"
    fi
    
    # Generate reports and update knowledge base
    generate_feedback_report
    update_team_knowledge_base
    
    print_success "✅ Adaptive feedback integration completed"
    print_success "📊 Report: adaptive-feedback-report.md"
    print_success "📚 Knowledge base updated for future improvements"
}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi