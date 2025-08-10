# Environment Configuration Templates

## Default Environment Setup

### ⚠️ CRITICAL: Authentication Persistence

**The setup_clc script creates temporary kubeconfig files that MUST be exported for all subsequent commands:**

```bash
# After running setup_clc, ALWAYS export the kubeconfig path
source bin/setup_clc qe6                    # Creates /tmp/kubeconfig_XXXXX
export KUBECONFIG=/tmp/kubeconfig_XXXXX     # Use actual path from setup output

# OR combine all oc commands with export:
export KUBECONFIG=/tmp/kubeconfig_XXXXX && oc [command]
```

**Common Authentication Errors:**
- `Error: User "system:anonymous" cannot get resource` → Missing KUBECONFIG export
- `Error from server (Forbidden)` → Authentication context not preserved

**Framework Requirements:**
- ALL oc/kubectl commands MUST include KUBECONFIG export
- Framework should detect and export kubeconfig automatically
- Bash tool calls must persist authentication between commands

```bash
# Default to qe6 if no environment specified
ENVIRONMENT="${USER_ENVIRONMENT:-qe6}"

validate_test_environment() {
    local environment="${1:-qe6}"
    
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

## Environment Status Reporting Template

```markdown
## Execution Status
**Environment**: ${ENVIRONMENT}
**Feature Deployment**: ${FEATURE_STATUS}
**Immediate Execution**: ${EXECUTION_STATUS}

### Current Limitations
- Environment access: ${ENVIRONMENT_STATUS}
- Feature availability: ${FEATURE_AVAILABILITY} 
- Validation scope: ${VALIDATION_SCOPE}

### Future Execution
- When environment available: All test cases executable
- When feature deployed: All test cases executable
- Alternative environments: ${ALTERNATIVE_ENVIRONMENTS}
```

## Supported Environments

### Standard QE Environments
- **qe6**: Default environment
- **qe7**: Alternative QE environment
- **qe8**: Alternative QE environment  
- **qe9**: Alternative QE environment
- **qe10**: Alternative QE environment

### Custom Environment Support
```bash
# Custom environment example
CUSTOM_KUBECONFIG="/path/to/custom/kubeconfig"
CUSTOM_NAMESPACE="custom-acm-namespace"

# Override default setup
export KUBECONFIG="$CUSTOM_KUBECONFIG"
export ACM_NS="$CUSTOM_NAMESPACE"
```

## Environment-Specific Configurations

### qe6 Configuration
```yaml
cluster_api: "https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443"
acm_namespace: "open-cluster-management"
mce_namespace: "multicluster-engine"
openshift_version: "4.19.6"
```

### Custom Environment Template
```yaml
cluster_api: "${CUSTOM_API_URL}"
acm_namespace: "${CUSTOM_ACM_NS}"
mce_namespace: "${CUSTOM_MCE_NS}"
openshift_version: "${CUSTOM_OCP_VERSION}"
```
