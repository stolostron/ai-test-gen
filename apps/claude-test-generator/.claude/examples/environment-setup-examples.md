# Environment Setup Examples

## Option 1: Automatic Environment Setup (Recommended)

```bash
# Navigate to framework
cd apps/claude-test-generator

# Analyze any ACM JIRA ticket (uses qe6 by default)
analyze_ticket ACM-22079

# With custom environment variable (if supported)
USER_ENVIRONMENT=qe6 analyze_ticket ACM-22079
```

## Option 2: User-Provided Kubeconfig

```bash
# Set your own kubeconfig before running
export KUBECONFIG=/path/to/your/kubeconfig
analyze_ticket ACM-22079

# Or inline for single run
KUBECONFIG=/path/to/your/kubeconfig analyze_ticket ACM-22079
```

## Environment Setup Commands

### Automatic Setup Examples
```bash
# Currently supported QE environment
source setup_clc qe6

# Framework will use this environment for analysis
```

### Custom Environment Examples
```bash
# Personal/staging/production clusters
export KUBECONFIG=/path/to/your/kubeconfig
oc login https://api.your-cluster.com:6443 -u username -p password

# Alternative authentication methods
oc login --token=<token> <cluster-url>
oc login --certificate-authority=<ca-file> --client-certificate=<cert-file> --client-key=<key-file> <cluster-url>
```

## Test Case Prerequisites Examples

### For QE Environment
```bash
# Hub cluster access using automatic setup
source setup_clc qe6
oc whoami && oc get namespaces | grep ocm
```

### For Custom Environment  
```bash
# Hub cluster access using custom kubeconfig
export KUBECONFIG=/path/to/your/kubeconfig
oc login <cluster-url> -u <username> -p <password>
oc whoami && oc get namespaces | grep ocm
```