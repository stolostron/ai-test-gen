# Enhanced Test Cases Template - Consistency Enforcement Framework

## MANDATORY STRUCTURE ENFORCEMENT

### STANDALONE TEST CASE REQUIREMENTS
```yaml
standalone_test_case_structure:
  each_test_case_must_include:
    - complete_description: "Full business context and testing purpose for THIS specific test case"
    - standalone_prerequisites: "All environment setup needed for THIS test case only"
    - independent_setup: "Complete setup commands and verification for THIS test case"
    - self_contained_steps: "All steps needed to execute THIS test case independently"
    - standalone_cleanup: "Cleanup commands specific to THIS test case"
    
enforcement_rule: "Every test case MUST be executable without reading any other test case or shared sections"
```

### Test Case Header Requirements (Per Individual Test Case)
```yaml
mandatory_fields_per_test_case:
  - description: "Complete business context and testing purpose for THIS specific scenario"
  - primary_coverage: "Main components being tested in THIS test case"
  - secondary_coverage: "Supporting/integration components for THIS test case"
  - related_jira_tickets: "Linked tickets relevant to THIS test case"
  - test_scope: "Specific scope and boundaries for THIS test case"
```

### Setup Section Requirements (Per Individual Test Case)
```yaml
mandatory_fields_per_test_case:
  - prerequisites: "Environment verification commands with expected outputs for THIS test case"
  - environment_config: "Complete configuration details needed for THIS test case"
  - rbac_setup: "RBAC user creation with specific scripts for THIS test case"
  - verification_commands: "Commands to verify environment readiness for THIS test case"
```

### Test Steps Table Requirements
```yaml
mandatory_columns:
  - step: "Sequential step number"
  - action: "MUST start with 'What We're Doing:' followed by business context"
  - commands: "CLI commands, UI navigation, expected outputs"
  - expected_result: "Specific concrete expectations (yes/no/specific values)"
```

## CONTENT VALIDATION RULES

### FORBIDDEN PATTERNS (Auto-Reject)
```python
FORBIDDEN_PATTERNS = [
    "Based on role configuration",       # Vague expectations
    "performance.*test",                 # No performance testing  
    "stress.*test",                      # No stress testing
    "load.*test",                        # No load testing
    "scale.*test",                       # No scale testing
    "<CLUSTER_.*>",                     # No env-specific in test cases
    "depending on.*",                   # Vague dependencies
    "according to.*configuration"       # Non-specific configuration refs
]
```

### REQUIRED PATTERNS (Auto-Enforce)
```python
REQUIRED_PATTERNS = [
    r"What We're Doing:.*[Tt]esting",   # Mandatory business explanations
    r"Expected.*:(.*yes|no|\w+)",       # Concrete expectations
    r"CLI.*:.*oc.*",                    # Specific CLI commands
    r"UI.*:.*Navigate",                 # Specific UI instructions
    r"kubeadmin.*<CLUSTER_CONSOLE_PASSWORD>.*<CLUSTER_CONSOLE_URL>" # Login standardization
]
```

### BUSINESS CONTEXT REQUIREMENTS
```yaml
test_step_action_format:
  pattern: "What We're Doing: [Business context explaining WHY this test step matters] **CLI**: [commands] **UI**: [navigation] **Expected**: [specific result]"
  
role_justification_requirements:
  - "[Role] needs [action] access for [business purpose]"
  - "[Admin role] requires full [feature] management capabilities"  
  - "[View role] should only see permitted [resources]"
  - "[Operator role] need cross-cluster permissions for [workflow] operations"
```

## ENVIRONMENT HANDLING RULES

### Test Cases File: ALWAYS Environment-Agnostic
```yaml
placeholder_usage:
  cluster_console: "<CLUSTER_CONSOLE_URL>"
  cluster_password: "<CLUSTER_CONSOLE_PASSWORD>"
  test_clusters: "<TEST_CLUSTER_1>", "<TEST_CLUSTER_2>"
  test_domains: "<TEST_DOMAIN>"
  test_users: "<TEST_USER>@<TEST_DOMAIN>"
```

### Complete Analysis File: ALWAYS Environment-Specific
```yaml
specific_details_required:
  test_environment: "actual.domain.com"
  console_url: "https://console-openshift-console.apps.actual.domain.com"
  acm_version: "2.14.0 (Target: 2.15+ required)"
  openshift_version: "Captured during environment assessment OR 'Not captured'"
```

## E2E FEATURE TESTING FOCUS ENFORCEMENT

### E2E Feature Testing ONLY
```yaml
testing_scope:
  allowed:
    - Feature functionality validation
    - Cross-component integration workflows
    - User access and permission verification (when applicable)
    - Error handling and recovery scenarios
    - Component integration scenarios (when applicable)
  
  forbidden:
    - Performance benchmarking
    - Stress testing under load
    - Concurrent user scenarios
    - Response time measurements
    - Scale testing (large datasets/high volume)
```

### Login Instructions Standardization
```yaml
mandatory_login_step:
  pattern: |
    | 1 | Login to ACM Hub Cluster | Successfully authenticated to hub with admin privileges | 
    **CLI**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>`
    **UI**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with kubeadmin credentials
    **Expected Output**: `Login successful. You have access to XX projects.`
    **Verify Login**: `oc whoami` returns `kubeadmin` |
```

## PERMISSION EXPECTATIONS CLARITY

### Feature-Specific Permission Expectations (When Applicable)
```yaml
feature_permission_examples:
  primary_action: "yes ([Role] needs [action] access for [business justification])"
  secondary_action: "yes ([Role] handles [workflow] operations as core responsibility)"
  cross_cluster_action: "yes ([Role] performs cross-cluster [operations] workflows)"
  restricted_action: "no (if role is [role], not admin - scoped permissions)"
  scoped_access: "no (if [resource]-specific names were specified in assignment)"
```

### Permission Test Patterns (For RBAC Features)
```yaml
permission_validation_format:
  positive_test: 'oc auth can-i [action] [resource] --as=[user] --context [cluster]'
  expected_positive: 'Expected: `yes` ([business justification for why user needs this])'
  negative_test: 'oc auth can-i [forbidden-action] [resource] --as=[user] --context [cluster]' 
  expected_negative: 'Expected: `no` ([scoping rationale])'
```

## INTEGRATION WITH PHASE 4 PROCESSING

### Template Application Trigger Points
```yaml
phase_4_integration:
  trigger_condition: "Phase 3 data available + Phase 4 pattern extension initiated"
  validation_sequence:
    1. "Apply template structure enforcement"
    2. "Run content validation rules engine"
    3. "Execute schema-based structure enforcement"
    4. "Perform business context enhancement"
    5. "Validate final output against quality gates"
```

### Quality Gates
```yaml
quality_gates:
  structure_compliance: "100% (all mandatory sections present)"
  forbidden_pattern_detection: "0 violations"
  required_pattern_presence: "100% (all mandatory patterns found)"
  business_context_completeness: "All test steps have 'What We're Doing' explanations"
  environment_handling_correctness: "Placeholders in test cases, specifics in analysis"
```

## AUTOMATIC ENHANCEMENT RULES

### Vague Language Auto-Fix
```python
AUTO_FIX_PATTERNS = {
    "Based on role configuration": "Specific expectation based on [role] permissions",
    "depending on": "specifically configured for",
    "according to configuration": "as defined in the [specific configuration]",
    "may vary": "should consistently show"
}
```

### Missing Context Auto-Addition
```python
# These are EXAMPLES of context patterns, not fixed injections
CONTEXT_PATTERN_EXAMPLES = {
    "integration_pattern": "Testing [discovered component] integration with [related components] to ensure [business workflow] functions correctly",
    "access_pattern": "Validating [feature] access controls ensure [user roles] have appropriate permissions for [use case]",
    "multi_cluster_pattern": "Verifying [functionality] operates consistently across hub and managed clusters",
    "user_journey_pattern": "Ensuring [user type] can successfully complete [workflow] from start to finish"
}

# The AI adapts these based on the specific feature being tested
```

---

**IMPLEMENTATION NOTE**: This template serves as the enforcement specification for the template-driven generation system. All test case generation MUST validate against these rules before delivery.