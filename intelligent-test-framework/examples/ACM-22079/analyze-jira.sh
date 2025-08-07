#!/bin/bash

# analyze-jira.sh - Single Script Orchestrator for JIRA Analysis & Test Generation
# Usage: ./analyze-jira.sh <JIRA-TICKET> [OPTIONS]
# Example: ./analyze-jira.sh ACM-22079 --test-plan-only

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JIRA_TICKET=""
TEST_PLAN_ONLY=false
CONFIG_FILE="team-config.yaml"
VERBOSE=false
DRY_RUN=false

# Workflow state tracking
WORKFLOW_STATE_FILE="${SCRIPT_DIR}/workflow-state.json"
FEEDBACK_DB="${SCRIPT_DIR}/feedback-database.json"

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
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

print_banner() {
    echo "=========================================="
    echo "🚀 ACM JIRA Analysis & Test Generation"
    echo "🆕 AI-Powered Framework (Beta)"
    echo "=========================================="
    echo "Ticket: $JIRA_TICKET"
    echo "Mode: $([ "$TEST_PLAN_ONLY" = true ] && echo "Test Plan Only" || echo "Full Implementation")"
    echo "Config: $CONFIG_FILE"
    echo "Framework: AI-powered analysis with intelligent feedback"
    echo "=========================================="
    echo
}

usage() {
    cat << EOF
Usage: $0 <JIRA-TICKET> [OPTIONS]

DESCRIPTION:
    Single-command orchestrator for comprehensive JIRA analysis and test generation.
    Supports multiple testing frameworks and team configurations.

ARGUMENTS:
    JIRA-TICKET         JIRA ticket ID (e.g., ACM-22079)

OPTIONS:
    --test-plan-only    Generate test plan only, skip implementation
    --config=FILE       Use custom team configuration (default: team-config.yaml)
    --verbose           Enable verbose logging
    --dry-run           Show what would be executed without running
    --help              Show this help message

EXAMPLES:
    # Complete workflow
    $0 ACM-22079

    # Test plan generation only
    $0 ACM-22079 --test-plan-only

    # Custom team configuration
    $0 ACM-22079 --config=selenium-team-config.yaml

    # Verbose execution
    $0 ACM-22079 --verbose

WORKFLOW STAGES:
    1. Environment Setup & Validation
    2. Multi-Repository Access Configuration
    3. AI-Powered Comprehensive Analysis
    4. Test Plan Generation & Validation
    5. Human Review Gate
    6. Framework-Agnostic Test Implementation (if not --test-plan-only)
    7. Integration & Quality Validation

EOF
}

# Parse command line arguments
parse_arguments() {
    # Check for help first
    if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
        usage
        exit 0
    fi

    if [ $# -eq 0 ]; then
        usage
        exit 1
    fi

    JIRA_TICKET="$1"
    shift

    while [[ $# -gt 0 ]]; do
        case $1 in
            --test-plan-only)
                TEST_PLAN_ONLY=true
                shift
                ;;
            --config=*)
                CONFIG_FILE="${1#*=}"
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    # Validate JIRA ticket format
    if [[ ! "$JIRA_TICKET" =~ ^[A-Z]+-[0-9]+$ ]]; then
        print_error "Invalid JIRA ticket format. Expected format: ACM-22079"
        exit 1
    fi
}

# Initialize workflow state tracking
init_workflow_state() {
    cat > "$WORKFLOW_STATE_FILE" << EOF
{
  "ticket": "$JIRA_TICKET",
  "mode": "$([ "$TEST_PLAN_ONLY" = true ] && echo "test_plan_only" || echo "full_implementation")",
  "config": "$CONFIG_FILE",
  "started_at": "$(date -Iseconds)",
  "stages": {
    "environment_setup": {"status": "pending", "started_at": null, "completed_at": null},
    "repository_access": {"status": "pending", "started_at": null, "completed_at": null},
    "ai_analysis": {"status": "pending", "started_at": null, "completed_at": null},
    "test_plan_generation": {"status": "pending", "started_at": null, "completed_at": null},
    "human_review": {"status": "pending", "started_at": null, "completed_at": null},
    "test_implementation": {"status": "$([ "$TEST_PLAN_ONLY" = true ] && echo "skipped" || echo "pending")", "started_at": null, "completed_at": null},
    "quality_validation": {"status": "$([ "$TEST_PLAN_ONLY" = true ] && echo "skipped" || echo "pending")", "started_at": null, "completed_at": null}
  }
}
EOF
}

# Update workflow stage status
update_stage_status() {
    local stage="$1"
    local status="$2"
    local timestamp="$(date -Iseconds)"
    
    if [ "$status" = "started" ]; then
        jq ".stages.$stage.started_at = \"$timestamp\" | .stages.$stage.status = \"in_progress\"" "$WORKFLOW_STATE_FILE" > "${WORKFLOW_STATE_FILE}.tmp"
    elif [ "$status" = "completed" ]; then
        jq ".stages.$stage.completed_at = \"$timestamp\" | .stages.$stage.status = \"completed\"" "$WORKFLOW_STATE_FILE" > "${WORKFLOW_STATE_FILE}.tmp"
    elif [ "$status" = "failed" ]; then
        jq ".stages.$stage.completed_at = \"$timestamp\" | .stages.$stage.status = \"failed\"" "$WORKFLOW_STATE_FILE" > "${WORKFLOW_STATE_FILE}.tmp"
    fi
    
    mv "${WORKFLOW_STATE_FILE}.tmp" "$WORKFLOW_STATE_FILE"
}

# Stage 1: Environment Setup & Validation
stage_environment_setup() {
    print_status "🔧 Stage 1: Environment Setup & Validation"
    update_stage_status "environment_setup" "started"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would validate environment setup"
        update_stage_status "environment_setup" "completed"
        return 0
    fi
    
    # Validate Claude Code environment
    print_status "Validating Claude Code environment..."
    if ! command -v claude &> /dev/null; then
        print_error "Claude Code not found. Please install Claude Code first."
        update_stage_status "environment_setup" "failed"
        exit 1
    fi
    
    # Test Claude Code connectivity
    print_status "Testing Claude Code connectivity..."
    if ! claude --print "Environment validation test" &> /dev/null; then
        print_error "Claude Code connectivity test failed. Please check your configuration."
        update_stage_status "environment_setup" "failed"
        exit 1
    fi
    
    # Validate SSH GitHub access
    print_status "🔐 Validating SSH GitHub access to stolostron repositories..."
    if ./01-setup/ssh-github-validator.sh &> /dev/null; then
        print_success "SSH GitHub access validated - dynamic repository analysis enabled"
    else
        print_warning "SSH GitHub access issues detected - using GitHub API fallback"
        print_status "Some features may be limited, but analysis will continue"
    fi
    
    # Validate team configuration
    if [ ! -f "$CONFIG_FILE" ]; then
        print_warning "Team configuration not found: $CONFIG_FILE"
        print_status "Creating default configuration..."
        create_default_config
    fi
    
    # Load and validate configuration
    if ! python3 -c "import yaml; yaml.safe_load(open('$CONFIG_FILE'))" 2>/dev/null; then
        print_error "Invalid YAML configuration in $CONFIG_FILE"
        update_stage_status "environment_setup" "failed"
        exit 1
    fi
    
    print_success "Environment setup completed"
    update_stage_status "environment_setup" "completed"
}

# Stage 2: Dynamic GitHub Repository Access
stage_repository_access() {
    print_status "🔗 Stage 2: Dynamic GitHub Repository Access"
    update_stage_status "repository_access" "started"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would configure repository access"
        update_stage_status "repository_access" "completed"
        return 0
    fi
    
    # Execute dynamic repository access setup
    print_status "🔗 Setting up dynamic GitHub repository access..."
    if ./01-setup/dynamic-github-access.sh "$JIRA_TICKET" "$ANALYSIS_MODE" "$CONFIG_FILE"; then
        print_success "Dynamic repository access configured"
        print_status "✅ Real-time access to stolostron repositories enabled"
    else
        print_warning "Dynamic repository access setup had issues, using fallback"
    fi
    
    # Run static repository setup as fallback
    print_status "Setting up fallback repository access..."
    ./01-setup/enable-github-pr-access.sh || true
    
    # Run comprehensive research setup
    print_status "Setting up comprehensive research access..."
    ./01-setup/comprehensive-research-setup.sh || true
    
    # Validate repository access (more flexible validation)
    print_status "Validating repository access..."
    local access_validated=false
    
    # Check for dynamic access
    if [ -f "DYNAMIC_GITHUB_ACCESS_SUMMARY.md" ]; then
        print_success "Dynamic GitHub access validated"
        access_validated=true
    fi
    
    # Check for static access
    if [ -d "06-reference/comprehensive-research" ]; then
        print_success "Comprehensive research access validated"
        access_validated=true
    fi
    
    if [ "$access_validated" = false ]; then
        print_warning "Repository access setup incomplete - limited analysis available"
        print_status "Continuing with Claude Code's direct GitHub API access"
    fi
    
    print_success "Repository access configured"
    update_stage_status "repository_access" "completed"
}

# Stage 3: AI-Powered Comprehensive Analysis
stage_ai_analysis() {
    print_status "🤖 Stage 3: AI-Powered Comprehensive Analysis"
    update_stage_status "ai_analysis" "started"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would perform AI analysis"
        update_stage_status "ai_analysis" "completed"
        return 0
    fi
    
    # Create analysis session directory
    SESSION_DIR="02-analysis/sessions/session_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$SESSION_DIR"
    
    # Run comprehensive analysis with Claude Code
    print_status "Performing comprehensive feature analysis..."
    
    # Use the comprehensive research analysis prompt
    ANALYSIS_PROMPT=$(cat 02-analysis/prompts/comprehensive-research-analysis.txt)
    
    # Execute Claude Code analysis
    claude --print "$ANALYSIS_PROMPT" > "${SESSION_DIR}/feature-analysis.md" 2>&1
    
    if [ $? -ne 0 ]; then
        print_error "AI analysis failed"
        update_stage_status "ai_analysis" "failed"
        exit 1
    fi
    
    # Copy results to main analysis directory
    cp "${SESSION_DIR}/feature-analysis.md" "01-analysis/"
    
    print_success "AI analysis completed"
    update_stage_status "ai_analysis" "completed"
}

# Stage 4: Test Plan Generation & Validation
stage_test_plan_generation() {
    print_status "📋 Stage 4: Test Plan Generation & Validation"
    update_stage_status "test_plan_generation" "started"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would generate test plan"
        update_stage_status "test_plan_generation" "completed"
        return 0
    fi
    
    # Run smart environment validation first
    print_status "Running environment validation..."
    local validation_exit_code=0
    local validation_warnings=false
    
    if ./01-setup/smart-validation-engine.sh "$JIRA_TICKET" 2>/dev/null; then
        validation_exit_code=$?
        case $validation_exit_code in
            0)
                print_success "Environment validation passed"
                ;;
            2)
                print_warning "Environment validation passed with warnings"
                validation_warnings=true
                ;;
            *)
                print_warning "Environment validation failed - adapting test plan"
                validation_warnings=true
                ;;
        esac
    else
        print_warning "Environment validation encountered issues - proceeding with adaptations"
        validation_warnings=true
    fi
    
    # Run adaptive feedback integration for any validation issues
    if [ -f "validation-results.json" ]; then
        print_status "Analyzing validation results for test plan improvements..."
        ./01-setup/adaptive-feedback-integrator.sh "$JIRA_TICKET" "" "validation-results.json"
    fi
    
    # Store validation status for later review gates
    echo "$validation_warnings" > ".validation-warnings"
    
    # Generate test plan using AI with feedback insights
    print_status "Generating comprehensive test plan with adaptive insights..."
    
    # Create test plan generation session
    SESSION_DIR="02-analysis/sessions/session_$(date +%Y%m%d_%H%M%S)_testplan"
    mkdir -p "$SESSION_DIR"
    
    # Incorporate validation insights into test generation
    VALIDATION_INSIGHTS=""
    if [ -f "adaptive-feedback-report.md" ]; then
        VALIDATION_INSIGHTS="
        
Environment Validation Insights:
$(head -50 adaptive-feedback-report.md)
        
Please incorporate these insights when generating the test plan."
    fi
    
    # Use table-format test generation for user's preferred format
    if [ -f "02-analysis/prompts/table-format-test-generation.txt" ]; then
        print_status "Using improved table-format prompt for test generation"
        TEST_GEN_PROMPT=$(cat 02-analysis/prompts/table-format-test-generation.txt)
    elif [ -f "02-analysis/prompts/style-aware-test-generation.txt" ]; then
        print_status "Falling back to style-aware prompt"
        TEST_GEN_PROMPT=$(cat 02-analysis/prompts/style-aware-test-generation.txt)
    else
        print_status "Using basic test generation prompt"
        TEST_GEN_PROMPT=$(cat 02-analysis/prompts/test-generation.txt)
    fi
    
    # Enhance prompt with validation insights
    ENHANCED_PROMPT="$TEST_GEN_PROMPT$VALIDATION_INSIGHTS"
    
    # Generate test plan
    claude --print "$ENHANCED_PROMPT" > "${SESSION_DIR}/test-plan-raw.md" 2>&1
    
    if [ $? -ne 0 ]; then
        print_error "Test plan generation failed"
        update_stage_status "test_plan_generation" "failed"
        exit 1
    fi
    
    # Validate test plan using comprehensive validation prompt
    print_status "Validating test plan with intelligent analysis..."
    
    # Create validation prompt that preserves table format
    VALIDATION_PROMPT="CRITICAL: You must preserve the exact table format with '| Test Steps | Expected Results |' while improving content quality.

VALIDATION FOCUS - Improve these aspects ONLY:
1. Test step completeness and clarity
2. Command accuracy and specificity  
3. Expected results precision
4. Edge case coverage
5. Environment considerations

DO NOT CHANGE:
- Table format structure
- Markdown table headers
- Overall test case organization

MANDATORY FORMAT PRESERVATION:
- Keep '| Test Steps | Expected Results |' format exactly
- Maintain Setup sections as bullet points
- Preserve test case numbering and structure

Review this test plan and provide an improved version with the SAME format but better content:

$(cat ${SESSION_DIR}/test-plan-raw.md)

VALIDATION REQUIREMENTS:
✅ Verify all oc commands are complete and accurate
✅ Ensure expected results are specific and verifiable  
✅ Check for missing test scenarios or edge cases
✅ Validate environment setup requirements
✅ Confirm cleanup steps are included

OUTPUT: Improved test plan with EXACT same table format but enhanced content quality."
    
    claude --print "$VALIDATION_PROMPT" > "${SESSION_DIR}/test-plan-validation.md" 2>&1
    
    # Smart selection: prefer validated content that maintains table format
    if [ -f "${SESSION_DIR}/test-plan-validation.md" ] && grep -q "| Test Steps | Expected Results |" "${SESSION_DIR}/test-plan-validation.md"; then
        print_status "✅ Using validated test plan with preserved table format"
        cp "${SESSION_DIR}/test-plan-validation.md" "02-test-planning/test-plan.md"
    elif [ -f "${SESSION_DIR}/test-plan-raw.md" ] && grep -q "| Test Steps | Expected Results |" "${SESSION_DIR}/test-plan-raw.md"; then
        print_status "✅ Using raw test plan with correct table format (validation may have corrupted format)"
        cp "${SESSION_DIR}/test-plan-raw.md" "02-test-planning/test-plan.md"
    elif [ -f "test-plan-refined.md" ] && grep -q "| Test Steps | Expected Results |" "test-plan-refined.md"; then
        print_status "✅ Using refined test plan with table format"
        cp "test-plan-refined.md" "02-test-planning/test-plan.md"
    else
        print_warning "⚠️  No test plan found with correct table format, using best available"
        if [ -f "${SESSION_DIR}/test-plan-validation.md" ]; then
            cp "${SESSION_DIR}/test-plan-validation.md" "02-test-planning/test-plan.md"
        elif [ -f "${SESSION_DIR}/test-plan-raw.md" ]; then
            cp "${SESSION_DIR}/test-plan-raw.md" "02-test-planning/test-plan.md"
        else
            print_error "No test plan files found"
            return 1
        fi
    fi
    
    print_success "Test plan generation completed with intelligent validation"
    update_stage_status "test_plan_generation" "completed"
}

# Stage 5: Human Review Gate
stage_human_review() {
    print_status "👥 Stage 5: Human Review Gate"
    update_stage_status "human_review" "started"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would request human review"
        update_stage_status "human_review" "completed"
        return 0
    fi
    
    # Present test plan for human review
    print_status "Test plan ready for review!"
    print_status "Location: 02-test-planning/test-plan.md"
    echo
    
    if [ "$VERBOSE" = true ]; then
        print_status "Test plan preview:"
        echo "----------------------------------------"
        head -50 "02-test-planning/test-plan.md"
        echo "----------------------------------------"
        echo
    fi
    
    # Check for validation warnings that require user attention
    local has_validation_warnings=false
    if [ -f ".validation-warnings" ] && [ "$(cat .validation-warnings)" = "true" ]; then
        has_validation_warnings=true
        print_warning "⚠️  VALIDATION WARNINGS DETECTED"
        print_warning "Environment validation found issues that may affect test execution"
        
        if [ -f "validation-results.json" ]; then
            print_status "Validation issues summary:"
            jq -r '.validation_stages | to_entries[] | select(.value.status != "passed") | "  - \(.key): \(.value.status)"' validation-results.json 2>/dev/null
        fi
        
        print_status "These issues have been documented and the test plan has been adapted accordingly"
        print_status "Please review the test plan and validation warnings before proceeding"
        echo
    fi
    
    # Interactive review process
    while true; do
        if [ "$has_validation_warnings" = true ]; then
            read -p "Environment validation warnings detected. Review test plan now? (y/n): " review_choice
        else
            read -p "Would you like to review the test plan now? (y/n): " review_choice
        fi
        
        case $review_choice in
            [Yy]* )
                if command -v code &> /dev/null; then
                    code "02-test-planning/test-plan.md"
                elif command -v cursor &> /dev/null; then
                    cursor "02-test-planning/test-plan.md"
                else
                    ${EDITOR:-nano} "02-test-planning/test-plan.md"
                fi
                
                # Also show validation results if warnings exist
                if [ "$has_validation_warnings" = true ] && [ -f "validation-results.json" ]; then
                    print_status "Opening validation results for review..."
                    ${EDITOR:-cat} "validation-results.json"
                fi
                break
                ;;
            [Nn]* )
                print_status "Test plan available for review at: 02-test-planning/test-plan.md"
                if [ "$has_validation_warnings" = true ]; then
                    print_status "Validation warnings available at: validation-results.json"
                fi
                break
                ;;
            * )
                echo "Please answer yes or no."
                ;;
        esac
    done
    
    # Approval gate with validation warning handling
    while true; do
        if [ "$has_validation_warnings" = true ]; then
            echo
            print_warning "⚠️  IMPORTANT: Validation warnings were detected"
            print_warning "The test plan has been adapted but may require manual verification"
            echo
            read -p "Do you approve the test plan despite validation warnings? (y/n/modify): " approval_choice
        else
            read -p "Do you approve the test plan to proceed? (y/n/modify): " approval_choice
        fi
        
        case $approval_choice in
            [Yy]* )
                if [ "$has_validation_warnings" = true ]; then
                    print_warning "Test plan approved with validation warnings acknowledged"
                    print_warning "Additional verification may be required during test execution"
                    # Store approval with warnings for test implementation stage
                    echo "approved_with_warnings" > ".approval-status"
                else
                    print_success "Test plan approved. Proceeding to implementation..."
                    echo "approved" > ".approval-status"
                fi
                break
                ;;
            [Nn]* )
                print_error "Test plan not approved. Exiting..."
                update_stage_status "human_review" "failed"
                exit 1
                ;;
            [Mm]* )
                print_status "Please modify the test plan and run the script again."
                update_stage_status "human_review" "failed"
                exit 1
                ;;
            * )
                echo "Please answer yes, no, or modify."
                ;;
        esac
    done
    
    print_success "Human review completed"
    update_stage_status "human_review" "completed"
}

# Stage 6: Framework-Agnostic Test Implementation
stage_test_implementation() {
    if [ "$TEST_PLAN_ONLY" = true ]; then
        print_status "⏭️  Stage 6: Test Implementation (SKIPPED - Test Plan Only Mode)"
        return 0
    fi
    
    print_status "⚙️  Stage 6: Framework-Agnostic Test Implementation"
    update_stage_status "test_implementation" "started"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would implement test scripts"
        update_stage_status "test_implementation" "completed"
        return 0
    fi
    
    # Check approval status for additional warnings
    local approval_status="approved"
    if [ -f ".approval-status" ]; then
        approval_status=$(cat .approval-status)
    fi
    
    if [ "$approval_status" = "approved_with_warnings" ]; then
        print_warning "Implementing tests with validation warnings acknowledged"
        print_warning "Generated tests may require additional manual verification"
    fi
    
    # Load team configuration to determine framework
    FRAMEWORK=$(python3 -c "import yaml; config=yaml.safe_load(open('$CONFIG_FILE')); print(config.get('team', {}).get('framework', 'cypress'))")
    
    print_status "Implementing tests for framework: $FRAMEWORK"
    
    # Generate framework-specific implementation
    IMPLEMENTATION_PROMPT="Based on the approved test plan, generate complete test implementation for $FRAMEWORK framework.

    Test Plan:
    $(cat 02-test-planning/test-plan.md)
    
    Framework: $FRAMEWORK
    
    Please generate:
    1. Complete test specification files
    2. Page object models (if applicable)
    3. Test utilities and helpers
    4. Test data and fixtures
    5. Integration instructions
    
    Ensure the code is production-ready, well-documented, and follows best practices."
    
    SESSION_DIR="02-analysis/sessions/session_$(date +%Y%m%d_%H%M%S)_implementation"
    mkdir -p "$SESSION_DIR"
    
    claude --print "$IMPLEMENTATION_PROMPT" > "${SESSION_DIR}/test-implementation.md" 2>&1
    
    if [ $? -ne 0 ]; then
        print_error "Test implementation failed"
        update_stage_status "test_implementation" "failed"
        exit 1
    fi
    
    # Copy implementation to appropriate directories
    mkdir -p "03-implementation/$FRAMEWORK"
    cp "${SESSION_DIR}/test-implementation.md" "03-implementation/$FRAMEWORK/"
    
    # Validate generated test scripts
    print_status "Validating generated test implementation..."
    validate_test_implementation "$FRAMEWORK" "03-implementation/$FRAMEWORK/test-implementation.md"
    
    # Final test implementation review
    print_status "Test implementation completed - requesting final review"
    if [ "$approval_status" = "approved_with_warnings" ]; then
        print_warning "⚠️  Additional review recommended due to validation warnings"
    fi
    
    while true; do
        read -p "Would you like to review the generated test implementation? (y/n): " impl_review_choice
        case $impl_review_choice in
            [Yy]* )
                if command -v code &> /dev/null; then
                    code "03-implementation/$FRAMEWORK/"
                elif command -v cursor &> /dev/null; then
                    cursor "03-implementation/$FRAMEWORK/"
                else
                    ${EDITOR:-cat} "03-implementation/$FRAMEWORK/test-implementation.md"
                fi
                break
                ;;
            [Nn]* )
                print_status "Implementation available at: 03-implementation/$FRAMEWORK/"
                break
                ;;
            * )
                echo "Please answer yes or no."
                ;;
        esac
    done
    
    print_success "Test implementation completed"
    update_stage_status "test_implementation" "completed"
}

# Stage 7: Integration & Quality Validation
stage_quality_validation() {
    if [ "$TEST_PLAN_ONLY" = true ]; then
        print_status "⏭️  Stage 7: Quality Validation (SKIPPED - Test Plan Only Mode)"
        return 0
    fi
    
    print_status "✅ Stage 7: Integration & Quality Validation"
    update_stage_status "quality_validation" "started"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN: Would perform quality validation"
        update_stage_status "quality_validation" "completed"
        return 0
    fi
    
    # Validate test environment if configured
    if [ -f "$CONFIG_FILE" ]; then
        TEST_ENV_CONFIG=$(python3 -c "import yaml; config=yaml.safe_load(open('$CONFIG_FILE')); print(config.get('test_environment', {}).get('cluster_config_path', ''))")
        
        if [ -n "$TEST_ENV_CONFIG" ] && [ -f "$TEST_ENV_CONFIG" ]; then
            print_status "Validating test environment connectivity..."
            export KUBECONFIG="$TEST_ENV_CONFIG"
            
            if oc cluster-info &> /dev/null; then
                print_success "Test environment connectivity validated"
                
                # Run validation commands from config
                VALIDATION_COMMANDS=$(python3 -c "import yaml; config=yaml.safe_load(open('$CONFIG_FILE')); print('\\n'.join(config.get('test_environment', {}).get('validation_commands', [])))")
                
                if [ -n "$VALIDATION_COMMANDS" ]; then
                    print_status "Running environment validation commands..."
                    echo "$VALIDATION_COMMANDS" | while read -r cmd; do
                        if [ -n "$cmd" ]; then
                            print_status "Executing: $cmd"
                            if eval "$cmd" &> /dev/null; then
                                print_success "✓ $cmd"
                            else
                                print_warning "⚠ $cmd (non-critical)"
                            fi
                        fi
                    done
                fi
            else
                print_warning "Test environment not accessible (non-critical for test generation)"
            fi
        fi
    fi
    
    # Generate quality report
    print_status "Generating quality validation report..."
    
    QUALITY_PROMPT="Please review the complete test implementation and provide a quality validation report.
    
    Evaluate:
    1. Test plan completeness and coverage
    2. Implementation quality and best practices
    3. Integration readiness
    4. Documentation completeness
    5. Recommendations for improvement
    
    Test Plan: $(cat 02-test-planning/test-plan.md)
    Implementation: $(cat 03-implementation/*/test-implementation.md 2>/dev/null || echo "Implementation files not found")
    
    Provide a comprehensive quality report."
    
    SESSION_DIR="02-analysis/sessions/session_$(date +%Y%m%d_%H%M%S)_quality"
    mkdir -p "$SESSION_DIR"
    
    claude --print "$QUALITY_PROMPT" > "${SESSION_DIR}/quality-validation.md" 2>&1
    
    cp "${SESSION_DIR}/quality-validation.md" "04-quality/"
    
    print_success "Quality validation completed"
    update_stage_status "quality_validation" "completed"
}

# Create default configuration if not exists
create_default_config() {
    cat > "$CONFIG_FILE" << 'EOF'
team:
  name: "CLC QE"
  framework: "cypress"
  repositories:
    automation: "clc-ui"
    feature_repos: 
      - "cluster-curator-controller"
      - "lifecycle-apis"

test_environment:
  cluster_config_path: ""
  acm_namespace: "open-cluster-management"
  validation_commands:
    - "oc get pods -n open-cluster-management"
    - "oc get clustercurator"

frameworks:
  cypress:
    test_directory: "cypress/tests"
    spec_pattern: "**/*.spec.js"
    page_objects: "cypress/views"
    utilities: "cypress/support"
  
  selenium:
    test_directory: "src/test/java"
    spec_pattern: "**/*Test.java"
    page_objects: "src/main/java/pages"
    utilities: "src/main/java/utils"

ai_prompts:
  analysis_depth: "comprehensive"
  test_coverage: "exhaustive"
  validation_rigor: "production"
EOF
    
    print_success "Created default configuration: $CONFIG_FILE"
    print_warning "Please review and customize the configuration before running again"
}

# Validate generated test implementation
validate_test_implementation() {
    local framework="$1"
    local implementation_file="$2"
    
    print_status "Validating $framework test implementation..."
    
    local validation_issues=()
    
    # Framework-specific validation
    case "$framework" in
        "cypress")
            # Check for common Cypress patterns
            if ! grep -q "describe\|it\|cy\." "$implementation_file"; then
                validation_issues+=("Missing Cypress test structure (describe/it blocks)")
            fi
            if ! grep -q "cy\.get\|cy\.visit\|cy\.contains" "$implementation_file"; then
                validation_issues+=("Missing Cypress commands")
            fi
            ;;
        "selenium")
            # Check for Selenium patterns
            if ! grep -q "@Test\|WebDriver\|driver\." "$implementation_file"; then
                validation_issues+=("Missing Selenium test structure")
            fi
            ;;
        "go")
            # Check for Go test patterns
            if ! grep -q "func Test\|testing\.T" "$implementation_file"; then
                validation_issues+=("Missing Go test structure")
            fi
            ;;
    esac
    
    # Check for ACM-specific validation commands
    if ! grep -q "oc get\|oc describe\|kubectl" "$implementation_file"; then
        validation_issues+=("Missing Kubernetes/ACM validation commands")
    fi
    
    # Report validation results
    if [ ${#validation_issues[@]} -eq 0 ]; then
        print_success "Test implementation validation passed"
    else
        print_warning "Test implementation validation found issues:"
        for issue in "${validation_issues[@]}"; do
            print_warning "  - $issue"
        done
        print_warning "These issues should be addressed during manual review"
    fi
}

# Collect execution feedback for continuous improvement
collect_execution_feedback() {
    print_status "📊 Collecting execution feedback for continuous learning"
    
    # Create feedback collection
    local feedback_file="execution-feedback-$(date +%Y%m%d_%H%M%S).json"
    
    cat > "$feedback_file" << EOF
{
  "execution_session": {
    "jira_ticket": "$JIRA_TICKET",
    "mode": "$([ "$TEST_PLAN_ONLY" = true ] && echo "test_plan_only" || echo "full_implementation")",
    "config": "$CONFIG_FILE",
    "completed_at": "$(date -Iseconds)"
  },
  "stage_performance": $(jq '.stages' "$WORKFLOW_STATE_FILE" 2>/dev/null || echo '{}'),
  "validation_results": $(cat validation-results.json 2>/dev/null || echo '{}'),
  "learning_opportunities": [],
  "user_satisfaction": null,
  "improvement_suggestions": []
}
EOF
    
    # Collect interactive feedback if not in quiet mode
    if [ "$VERBOSE" = true ] && [ "$DRY_RUN" = false ]; then
        print_status "🔍 Would you like to provide feedback for continuous improvement? (y/n)"
        read -t 10 -p "Feedback: " feedback_choice 2>/dev/null || feedback_choice="n"
        
        case $feedback_choice in
            [Yy]*)
                collect_interactive_feedback "$feedback_file"
                ;;
            *)
                print_status "Feedback collection skipped"
                ;;
        esac
    fi
    
    # Store feedback for learning
    if [ -f "$FEEDBACK_DB" ]; then
        jq ".execution_feedback += [$(cat $feedback_file)]" "$FEEDBACK_DB" > "${FEEDBACK_DB}.tmp"
        mv "${FEEDBACK_DB}.tmp" "$FEEDBACK_DB"
    else
        echo "{\"execution_feedback\": [$(cat $feedback_file)], \"feedback_patterns\": [], \"learning_insights\": []}" > "$FEEDBACK_DB"
    fi
    
    rm -f "$feedback_file"
    print_status "Execution feedback recorded for future improvements"
}

# Collect interactive feedback from user
collect_interactive_feedback() {
    local feedback_file="$1"
    
    print_status "Please rate your experience (1-5):"
    read -t 30 -p "Overall satisfaction: " satisfaction 2>/dev/null || satisfaction="3"
    
    print_status "Any suggestions for improvement?"
    read -t 60 -p "Suggestions: " suggestions 2>/dev/null || suggestions=""
    
    # Update feedback file
    jq ".user_satisfaction = $satisfaction | 
        .improvement_suggestions += [\"$suggestions\"]" \
        "$feedback_file" > "${feedback_file}.tmp"
    mv "${feedback_file}.tmp" "$feedback_file"
}

# Generate final summary
generate_summary() {
    print_status "📊 Generating workflow summary..."
    
    SUMMARY_FILE="WORKFLOW_SUMMARY_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$SUMMARY_FILE" << EOF
# Workflow Summary: $JIRA_TICKET

**Generated**: $(date)
**Mode**: $([ "$TEST_PLAN_ONLY" = true ] && echo "Test Plan Only" || echo "Full Implementation")
**Configuration**: $CONFIG_FILE

## Workflow Status
$(cat "$WORKFLOW_STATE_FILE" | jq -r '.stages | to_entries[] | "- \(.key): \(.value.status)"')

## Deliverables Generated

### Analysis
- Feature Analysis: 01-analysis/feature-analysis.md
- Implementation Details: Available in session logs

### Test Planning
- Comprehensive Test Plan: 02-test-planning/test-plan.md
- Validation Matrix: Generated during planning phase

$([ "$TEST_PLAN_ONLY" = false ] && cat << 'IMPL_SECTION'
### Implementation
- Framework-Specific Tests: 03-implementation/
- Integration Guide: Available in implementation directory

### Quality Validation
- Quality Report: 04-quality/quality-validation.md
- Environment Validation: Completed during workflow
IMPL_SECTION
)

## Next Steps

$([ "$TEST_PLAN_ONLY" = true ] && cat << 'PLAN_NEXT'
1. Review the generated test plan
2. Run with full implementation mode: ./analyze-jira.sh $JIRA_TICKET
3. Integrate generated tests with existing test suite
PLAN_NEXT
)

$([ "$TEST_PLAN_ONLY" = false ] && cat << 'IMPL_NEXT'
1. Review generated test implementation
2. Integrate with existing test automation framework
3. Execute tests in target environment
4. Update team documentation and processes
IMPL_NEXT
)

## Session Logs
- All Claude Code interactions: 02-analysis/sessions/
- Workflow state: workflow-state.json

EOF

    print_success "Workflow summary generated: $SUMMARY_FILE"
}

# Main workflow execution
main() {
    parse_arguments "$@"
    print_banner
    init_workflow_state
    
    # Check for required tools
    for tool in jq python3; do
        if ! command -v "$tool" &> /dev/null; then
            print_error "$tool is required but not installed"
            exit 1
        fi
    done
    
    # Execute workflow stages
    stage_environment_setup
    stage_repository_access
    stage_ai_analysis
    stage_test_plan_generation
    stage_human_review
    stage_test_implementation
    stage_quality_validation
    
    generate_summary
    
    # Collect final feedback for continuous learning
    collect_execution_feedback
    
    print_success "🎉 Workflow completed successfully!"
    print_status "Summary: $(ls WORKFLOW_SUMMARY_*.md | tail -1)"
    
    if [ "$TEST_PLAN_ONLY" = true ]; then
        print_status "Test plan ready for review: 02-test-planning/test-plan.md"
        print_status "To generate implementation, run: ./analyze-jira.sh $JIRA_TICKET"
    else
        print_status "Complete test implementation ready for integration"
        print_status "Review implementation: 03-implementation/"
    fi
    
    # Display feedback insights if available
    if [ -f "adaptive-feedback-report.md" ]; then
        print_status "📊 Feedback insights available: adaptive-feedback-report.md"
    fi
}

# Execute main function with all arguments
main "$@"