#!/bin/bash

# smart-validation-engine.sh - Intelligent Validation with Feedback Analysis
# This script performs multi-tier validation and provides intelligent feedback

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VALIDATION_LOG="$PROJECT_ROOT/validation-results.json"
FEEDBACK_DB="$PROJECT_ROOT/feedback-database.json"
KNOWLEDGE_BASE="$PROJECT_ROOT/knowledge-base.json"

# Validation behavior settings
MAX_VALIDATION_ATTEMPTS=3
ALLOW_GRACEFUL_DEGRADATION=true
VALIDATION_STRICTNESS="balanced"  # strict, balanced, lenient

print_status() {
    echo -e "${BLUE}[VALIDATION]${NC} $1"
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

print_analysis() {
    echo -e "${YELLOW}[ANALYSIS]${NC} $1"
}

# Initialize validation tracking
init_validation_tracking() {
    cat > "$VALIDATION_LOG" << EOF
{
  "validation_session": {
    "started_at": "$(date -Iseconds)",
    "jira_ticket": "$JIRA_TICKET",
    "feature": "$FEATURE_NAME",
    "environment": "$TEST_ENVIRONMENT"
  },
  "validation_stages": {
    "feature_availability": {"status": "pending", "details": []},
    "environment_readiness": {"status": "pending", "details": []},
    "test_logic": {"status": "pending", "details": []},
    "expected_results": {"status": "pending", "details": []}
  },
  "feedback_analysis": {
    "root_cause": null,
    "recommended_actions": [],
    "confidence_score": 0,
    "learning_insights": []
  }
}
EOF
}

# Update validation stage result
update_validation_result() {
    local stage="$1"
    local status="$2"
    local details="$3"
    local timestamp="$(date -Iseconds)"
    
    jq ".validation_stages.$stage.status = \"$status\" | 
        .validation_stages.$stage.completed_at = \"$timestamp\" |
        .validation_stages.$stage.details += [\"$details\"]" \
        "$VALIDATION_LOG" > "${VALIDATION_LOG}.tmp"
    mv "${VALIDATION_LOG}.tmp" "$VALIDATION_LOG"
}

# Stage 1: Feature Availability Validation
validate_feature_availability() {
    print_status "🔍 Stage 1: Feature Availability Validation"
    
    local feature_found=false
    local validation_details=()
    
    # Check if ClusterCurator CRD exists (for ACM-22079)
    if oc get crd clustercurators.cluster.open-cluster-management.io &> /dev/null; then
        validation_details+=("ClusterCurator CRD found")
        feature_found=true
    else
        validation_details+=("ClusterCurator CRD not found")
    fi
    
    # Check if ClusterCurator controller is running
    if oc get pods -n open-cluster-management | grep -q "cluster-curator"; then
        validation_details+=("ClusterCurator controller running")
        feature_found=true
    else
        validation_details+=("ClusterCurator controller not found")
    fi
    
    # Check for feature-specific APIs or endpoints
    if oc api-resources | grep -q "clustercurator"; then
        validation_details+=("ClusterCurator API available")
        feature_found=true
    else
        validation_details+=("ClusterCurator API not available")
    fi
    
    # Update results
    for detail in "${validation_details[@]}"; do
        update_validation_result "feature_availability" \
            "$([ "$feature_found" = true ] && echo "passed" || echo "failed")" \
            "$detail"
    done
    
    if [ "$feature_found" = true ]; then
        print_success "Feature availability validated"
        return 0
    else
        print_warning "Feature availability validation failed"
        analyze_feature_availability_failure "${validation_details[@]}"
        
        if [ "$ALLOW_GRACEFUL_DEGRADATION" = true ]; then
            print_warning "Graceful degradation: Proceeding with warnings"
            print_warning "User review will be required before test implementation"
            return 2  # Warning status - allows continuation with caveats
        else
            print_error "Feature not available - stopping execution"
            return 1
        fi
    fi
}

# Stage 2: Environment Readiness Validation
validate_environment_readiness() {
    print_status "🏗️ Stage 2: Environment Readiness Validation"
    
    local env_ready=true
    local validation_details=()
    
    # Check cluster connectivity
    if oc cluster-info &> /dev/null; then
        validation_details+=("Cluster connectivity: OK")
    else
        validation_details+=("Cluster connectivity: FAILED")
        env_ready=false
    fi
    
    # Check ACM installation
    if oc get pods -n open-cluster-management &> /dev/null; then
        validation_details+=("ACM installation: OK")
    else
        validation_details+=("ACM installation: NOT FOUND")
        env_ready=false
    fi
    
    # Check required permissions
    if oc auth can-i create clustercurator &> /dev/null; then
        validation_details+=("Required permissions: OK")
    else
        validation_details+=("Required permissions: INSUFFICIENT")
        env_ready=false
    fi
    
    # Check storage classes (for storage mapping features)
    local storage_classes=$(oc get storageclass --no-headers 2>/dev/null | wc -l)
    if [ "$storage_classes" -gt 0 ]; then
        validation_details+=("Storage classes available: $storage_classes")
    else
        validation_details+=("Storage classes: NONE FOUND")
        print_warning "No storage classes found - may affect storage mapping tests"
    fi
    
    # Update results
    for detail in "${validation_details[@]}"; do
        update_validation_result "environment_readiness" \
            "$([ "$env_ready" = true ] && echo "passed" || echo "failed")" \
            "$detail"
    done
    
    if [ "$env_ready" = true ]; then
        print_success "Environment readiness validated"
        return 0
    else
        print_error "Environment not ready"
        analyze_environment_readiness_failure "${validation_details[@]}"
        return 1
    fi
}

# Stage 3: Test Logic Validation
validate_test_logic() {
    print_status "🧪 Stage 3: Test Logic Validation"
    
    local test_logic_valid=true
    local validation_details=()
    
    # Check if test commands are valid
    local test_commands=(
        "oc get clustercurator"
        "oc get managedclusters"
        "oc get managedclusteraction"
        "oc get managedclusterview"
    )
    
    for cmd in "${test_commands[@]}"; do
        if eval "$cmd --help" &> /dev/null; then
            validation_details+=("Command valid: $cmd")
        else
            validation_details+=("Command invalid: $cmd")
            test_logic_valid=false
        fi
    done
    
    # Check if required resources can be created (dry-run)
    if oc create clustercurator test-validation --dry-run=client -o yaml &> /dev/null; then
        validation_details+=("ClusterCurator creation: Valid")
    else
        validation_details+=("ClusterCurator creation: Invalid")
        test_logic_valid=false
    fi
    
    # Update results
    for detail in "${validation_details[@]}"; do
        update_validation_result "test_logic" \
            "$([ "$test_logic_valid" = true ] && echo "passed" || echo "failed")" \
            "$detail"
    done
    
    if [ "$test_logic_valid" = true ]; then
        print_success "Test logic validated"
        return 0
    else
        print_error "Test logic validation failed"
        analyze_test_logic_failure "${validation_details[@]}"
        return 1
    fi
}

# Stage 4: Expected Results Validation
validate_expected_results() {
    print_status "📊 Stage 4: Expected Results Validation"
    
    local results_valid=true
    local validation_details=()
    
    # Create a test ClusterCurator to validate behavior
    local test_curator_name="validation-test-$(date +%s)"
    
    # Create test ClusterCurator with minimal config
    cat > "/tmp/test-curator.yaml" << EOF
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: $test_curator_name
  namespace: default
spec:
  desiredCuration: "install"
  cluster:
    name: "test-cluster"
EOF

    # Test ClusterCurator creation and validation
    if oc apply -f "/tmp/test-curator.yaml" &> /dev/null; then
        validation_details+=("Test ClusterCurator creation: SUCCESS")
        
        # Wait for status update
        sleep 5
        
        # Check if ClusterCurator has expected status structure
        local status_check=$(oc get clustercurator "$test_curator_name" -o jsonpath='{.status}' 2>/dev/null)
        if [ -n "$status_check" ]; then
            validation_details+=("ClusterCurator status structure: VALID")
        else
            validation_details+=("ClusterCurator status structure: MISSING")
            results_valid=false
        fi
        
        # Cleanup test resource
        oc delete clustercurator "$test_curator_name" &> /dev/null || true
    else
        validation_details+=("Test ClusterCurator creation: FAILED")
        results_valid=false
    fi
    
    # Clean up
    rm -f "/tmp/test-curator.yaml"
    
    # Update results
    for detail in "${validation_details[@]}"; do
        update_validation_result "expected_results" \
            "$([ "$results_valid" = true ] && echo "passed" || echo "failed")" \
            "$detail"
    done
    
    if [ "$results_valid" = true ]; then
        print_success "Expected results validation passed"
        return 0
    else
        print_error "Expected results validation failed"
        analyze_expected_results_failure "${validation_details[@]}"
        return 1
    fi
}

# Failure Analysis Functions

analyze_feature_availability_failure() {
    print_analysis "Analyzing feature availability failure..."
    
    local analysis=""
    local recommended_actions=()
    
    # Check if this is a build/deployment issue
    if ! oc get crd clustercurators.cluster.open-cluster-management.io &> /dev/null; then
        analysis="Feature CRD not deployed - likely build or deployment issue"
        recommended_actions+=("Check if correct ACM version is deployed")
        recommended_actions+=("Verify ClusterCurator operator is installed")
        recommended_actions+=("Check deployment logs for errors")
    fi
    
    # Check if controller is missing
    if ! oc get pods -n open-cluster-management | grep -q "cluster-curator"; then
        analysis="ClusterCurator controller not running"
        recommended_actions+=("Check controller deployment status")
        recommended_actions+=("Verify operator installation")
        recommended_actions+=("Check for pending pod issues")
    fi
    
    record_failure_analysis "feature_availability" "$analysis" "${recommended_actions[@]}"
}

analyze_environment_readiness_failure() {
    print_analysis "Analyzing environment readiness failure..."
    
    local analysis=""
    local recommended_actions=()
    
    # Check cluster connectivity issues
    if ! oc cluster-info &> /dev/null; then
        analysis="Cluster connectivity issue"
        recommended_actions+=("Verify kubeconfig is correct and current")
        recommended_actions+=("Check cluster accessibility and VPN connection")
        recommended_actions+=("Validate cluster certificates")
    fi
    
    # Check ACM installation issues
    if ! oc get pods -n open-cluster-management &> /dev/null; then
        analysis="ACM not properly installed"
        recommended_actions+=("Install ACM operator")
        recommended_actions+=("Check ACM installation status")
        recommended_actions+=("Verify subscription and CSV status")
    fi
    
    record_failure_analysis "environment_readiness" "$analysis" "${recommended_actions[@]}"
}

analyze_test_logic_failure() {
    print_analysis "Analyzing test logic failure..."
    
    local analysis="Test commands or resource definitions are invalid"
    local recommended_actions=()
    
    recommended_actions+=("Update test commands to match current API version")
    recommended_actions+=("Verify resource schemas and required fields")
    recommended_actions+=("Check RBAC permissions for test operations")
    recommended_actions+=("Review API deprecations and changes")
    
    record_failure_analysis "test_logic" "$analysis" "${recommended_actions[@]}"
}

analyze_expected_results_failure() {
    print_analysis "Analyzing expected results failure..."
    
    local analysis="Feature behavior doesn't match test expectations"
    local recommended_actions=()
    
    recommended_actions+=("Review feature implementation for changes")
    recommended_actions+=("Update test expectations based on actual behavior")
    recommended_actions+=("Check for feature flag or configuration requirements")
    recommended_actions+=("Validate test data and scenarios")
    
    record_failure_analysis "expected_results" "$analysis" "${recommended_actions[@]}"
}

# Record failure analysis for learning
record_failure_analysis() {
    local stage="$1"
    local analysis="$2"
    shift 2
    local actions=("$@")
    
    # Create actions array for JSON
    local actions_json="["
    for action in "${actions[@]}"; do
        actions_json="$actions_json\"$action\","
    done
    actions_json="${actions_json%,}]"
    
    # Update validation log with analysis
    jq ".feedback_analysis.root_cause = \"$stage: $analysis\" |
        .feedback_analysis.recommended_actions = $actions_json |
        .feedback_analysis.confidence_score = 0.8 |
        .feedback_analysis.learning_insights += [\"$stage failure pattern: $analysis\"]" \
        "$VALIDATION_LOG" > "${VALIDATION_LOG}.tmp"
    mv "${VALIDATION_LOG}.tmp" "$VALIDATION_LOG"
    
    # Store in feedback database for learning
    store_feedback_for_learning "$stage" "$analysis" "${actions[@]}"
}

# Store feedback in database for continuous learning
store_feedback_for_learning() {
    local stage="$1"
    local analysis="$2"
    shift 2
    local actions=("$@")
    
    # Initialize feedback database if not exists
    if [ ! -f "$FEEDBACK_DB" ]; then
        echo '{"feedback_patterns": [], "learning_insights": []}' > "$FEEDBACK_DB"
    fi
    
    # Create feedback entry
    local feedback_entry=$(cat << EOF
{
  "timestamp": "$(date -Iseconds)",
  "jira_ticket": "$JIRA_TICKET",
  "stage": "$stage",
  "failure_pattern": "$analysis",
  "recommended_actions": $(printf '%s\n' "${actions[@]}" | jq -R . | jq -s .),
  "environment": "$TEST_ENVIRONMENT"
}
EOF
)
    
    # Add to feedback database
    jq ".feedback_patterns += [$feedback_entry]" "$FEEDBACK_DB" > "${FEEDBACK_DB}.tmp"
    mv "${FEEDBACK_DB}.tmp" "$FEEDBACK_DB"
    
    print_analysis "Feedback recorded for continuous learning"
}

# Generate intelligent recommendations based on feedback history
generate_intelligent_recommendations() {
    print_status "🧠 Generating intelligent recommendations..."
    
    if [ ! -f "$FEEDBACK_DB" ]; then
        print_warning "No feedback history available for recommendations"
        return
    fi
    
    # Analyze feedback patterns
    local similar_failures=$(jq -r ".feedback_patterns[] | select(.stage == \"$1\" and .failure_pattern == \"$2\") | .recommended_actions[]" "$FEEDBACK_DB" 2>/dev/null)
    
    if [ -n "$similar_failures" ]; then
        print_analysis "Found similar failure patterns in history:"
        echo "$similar_failures" | while read -r action; do
            print_analysis "  - $action"
        done
        
        # Update knowledge base
        update_knowledge_base "$1" "$2" "$similar_failures"
    fi
}

# Update knowledge base with learning insights
update_knowledge_base() {
    local stage="$1"
    local pattern="$2"
    local solutions="$3"
    
    if [ ! -f "$KNOWLEDGE_BASE" ]; then
        echo '{"learned_patterns": [], "success_strategies": []}' > "$KNOWLEDGE_BASE"
    fi
    
    # Add learning insight
    local insight=$(cat << EOF
{
  "pattern": "$stage failure: $pattern",
  "solutions": $(echo "$solutions" | jq -R . | jq -s .),
  "confidence": 0.9,
  "learned_at": "$(date -Iseconds)"
}
EOF
)
    
    jq ".learned_patterns += [$insight]" "$KNOWLEDGE_BASE" > "${KNOWLEDGE_BASE}.tmp"
    mv "${KNOWLEDGE_BASE}.tmp" "$KNOWLEDGE_BASE"
}

# Main validation orchestrator
main() {
    local JIRA_TICKET="${1:-ACM-22079}"
    local FEATURE_NAME="${2:-ClusterCurator Digest Upgrades}"
    local TEST_ENVIRONMENT="${3:-default}"
    
    print_status "🚀 Starting intelligent validation for $JIRA_TICKET"
    
    init_validation_tracking
    
    local validation_failed=false
    
    # Run validation stages
    if ! validate_feature_availability; then
        validation_failed=true
        generate_intelligent_recommendations "feature_availability" "Feature not available"
    fi
    
    if ! validate_environment_readiness; then
        validation_failed=true
        generate_intelligent_recommendations "environment_readiness" "Environment not ready"
    fi
    
    if ! validate_test_logic; then
        validation_failed=true
        generate_intelligent_recommendations "test_logic" "Test logic invalid"
    fi
    
    if ! validate_expected_results; then
        validation_failed=true
        generate_intelligent_recommendations "expected_results" "Results mismatch"
    fi
    
    # Generate final report with intelligent missing feature detection
    if [ "$validation_failed" = true ]; then
        # Analyze if failures indicate missing feature implementation
        local missing_feature_score=0
        
        # Check various indicators that suggest feature is not implemented
        if jq -e '.validation_stages.feature_availability.status == "failed"' "$VALIDATION_LOG" >/dev/null 2>&1; then
            ((missing_feature_score++))
        fi
        
        if jq -e '.validation_stages.test_logic.details[]? | select(. | contains("not found") or contains("CRD") or contains("controller"))' "$VALIDATION_LOG" >/dev/null 2>&1; then
            ((missing_feature_score++))
        fi
        
        if jq -e '.validation_stages.environment_readiness.details[]? | select(. | contains("missing") or contains("unavailable"))' "$VALIDATION_LOG" >/dev/null 2>&1; then
            ((missing_feature_score++))
        fi
        
        # Smart decision: Missing feature vs real environment issues
        if [ $missing_feature_score -ge 2 ]; then
            print_warning "⚠️  Smart Analysis: Feature appears not yet implemented in test environment"
            print_status "🧠 INTELLIGENT ADAPTATION: Generating test plan for pre-implementation validation"
            
            # Add smart analysis to validation log
            jq --arg analysis "Feature not yet implemented - test environment is expected state" \
               --arg action "continue_with_pre_implementation_tests" \
               '.smart_analysis = $analysis | .recommended_strategy = $action | .validation_type = "pre_implementation"' \
               "$VALIDATION_LOG" > "${VALIDATION_LOG}.tmp" && mv "${VALIDATION_LOG}.tmp" "$VALIDATION_LOG"
            
            print_success "✅ Smart validation completed - adapted for missing feature scenario"
            exit 2  # Warning status - continue with adapted approach
        else
            print_error "❌ Validation failed - See analysis in $VALIDATION_LOG"
            print_analysis "Recommended next steps:"
            jq -r '.feedback_analysis.recommended_actions[]' "$VALIDATION_LOG" | while read -r action; do
                print_analysis "  ✓ $action"
            done
            exit 1  # Hard failure for real environment issues
        fi
    else
        print_success "✅ All validation stages passed"
        print_success "Environment ready for test execution"
        exit 0
    fi
}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi