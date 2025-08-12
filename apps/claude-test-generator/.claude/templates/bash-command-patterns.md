# Bash Command Patterns for Framework Operations

## Environment Setup & Validation

### Correct Command Chaining Patterns

```bash
# Basic environment setup with validation
source setup_clc qe6 && oc whoami && oc get namespaces

# Multi-step cluster validation
source setup_clc qe6 && oc cluster-info && oc get routes -n ocm

# Environment setup with permission verification
source setup_clc qe6 && oc auth can-i '*' '*' --all-namespaces

# Complete environment validation chain
source setup_clc qe6 && oc whoami && oc get namespace ocm multicluster-engine && oc get routes -n ocm

# Feature-specific validation (example: RBAC UI testing)
source setup_clc qe6 && oc whoami && oc get crd roleassignments.rbac.open-cluster-management.io
```

### Incorrect Patterns (Avoid These)

```bash
# Wrong: Separate commands lose environment state
source setup_clc qe6
oc whoami  # This will fail with authentication errors

# Wrong: Multiple separate bash calls
source setup_clc qe6
oc get namespaces  # Authentication context lost

# Wrong: Assuming persistent authentication
setup_clc qe6  # (without source)
oc cluster-info  # Will not have proper kubeconfig
```

## JIRA Analysis Commands

```bash
# Basic ticket analysis
jira issue view <TICKET-ID> --plain

# Ticket with full comments
jira issue view <TICKET-ID> --comments

# Multiple ticket analysis (for investigation)
jira issue view ACM-12345 --plain && jira issue view ACM-12346 --plain

# Batch ticket analysis with linked issues
jira issue view <PARENT-TICKET> --plain && jira issue view <SUBTASK-1> --plain && jira issue view <SUBTASK-2> --plain
```

## GitHub PR Analysis

```bash
# Use WebFetch tool with GitHub URLs for PR analysis
# Format: https://github.com/<owner>/<repo>/pull/<number>

# Example WebFetch patterns (used within framework tools)
# WebFetch: https://github.com/stolostron/console/pull/4858
# WebFetch: https://github.com/open-cluster-management-io/api/pull/123
```

## Testing & Validation Workflows

### Pre-Test Environment Validation

```bash
# Complete pre-test validation chain
source setup_clc qe6 && oc whoami && oc version && oc get nodes && oc get namespace ocm multicluster-engine

# ACM-specific validation
source setup_clc qe6 && oc get multiclusterhub -n ocm && oc get clustermanager -n multicluster-engine

# RBAC feature validation
source setup_clc qe6 && oc get crd | grep rbac && oc get rolebinding -A | head -5
```

### Post-Test Cleanup (if needed)

```bash
# Clean up test resources (example pattern)
source setup_clc qe6 && oc delete roleassignment test-assignment -n test-namespace

# Verify cleanup
source setup_clc qe6 && oc get roleassignments -A | grep test-
```

### Shell piping and alternation (grep) correctness

```bash
# Correct: do not escape the pipe character in shell
oc get clustercurator test -n ns -o yaml | grep -A1 annotations

# Correct alternation with grep: use -E for extended regex
oc logs -n multicluster-engine deployment/cluster-curator-controller | grep -E -i "digest|conditional"

# Incorrect: escaping the pipe within a normal shell pipeline will literally print '|'
# Avoid patterns like: oc get ... -o yaml \| grep -A1 annotations
```

## Framework Internal Patterns

### Run Directory Management

```bash
# Create timestamped run directory
TIMESTAMP=$(date +%Y%m%d-%H%M) && mkdir -p runs/<TICKET-ID>/run-001-$TIMESTAMP

# Create latest symlink
cd runs/<TICKET-ID> && ln -sfn run-001-<TIMESTAMP> latest

# Batch directory operations
mkdir -p runs/<TICKET-ID>/run-001-<TIMESTAMP> && cd runs/<TICKET-ID> && ln -sfn run-001-<TIMESTAMP> latest
```

### Environment Detection and Fallback

```bash
# Try automatic setup, fallback to manual if needed
source setup_clc qe6 && oc whoami || echo "Manual setup required"

# Validate environment with graceful degradation
source setup_clc qe6 && oc get namespace ocm || echo "ACM not installed or accessible"
```

## Key Principles

1. **Always Chain with &&**: Environment setup commands must be chained to maintain session state
2. **Validate Immediately**: Check authentication and permissions right after setup
3. **Graceful Degradation**: Handle cases where automatic setup fails
4. **Batch Operations**: Group related commands to minimize bash tool calls
5. **Clear Error Handling**: Use `|| echo "fallback message"` for diagnostics

## Common Troubleshooting

### Authentication Issues
```bash
# Debug authentication state
source setup_clc qe6 && oc whoami && oc auth can-i get pods

# Check kubeconfig
source setup_clc qe6 && echo $KUBECONFIG && oc config current-context
```

### Environment Connectivity
```bash
# Basic connectivity test
source setup_clc qe6 && oc cluster-info && oc get nodes

# ACM-specific connectivity
source setup_clc qe6 && oc get routes -n ocm && curl -k $(oc get route -n ocm -o jsonpath='{.items[0].spec.host}')
```