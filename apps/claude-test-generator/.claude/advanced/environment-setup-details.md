# Advanced Environment Setup

## Framework Environment Setup Options

### Option 1: Automatic QE Setup (Recommended)
- Uses qe6 environment (currently the only supported QE environment)
- Automatic credential fetching from Jenkins
- Framework calls `source setup_clc qe6` during environment setup

### Option 2: User-Provided Kubeconfig (Maximum Flexibility)  
- Use any cluster with any authentication method
- Custom environments: production, staging, personal dev clusters
- User kubeconfig takes precedence over automatic setup

## Automatic Setup (Uses Framework Scripts)
- **bin/setup_clc**: Automatically fetches latest credentials from Jenkins and configures kubeconfig
- **bin/login_oc**: Handles OpenShift authentication with various credential formats  
- **Supported Environment**: qe6 (default and currently only supported QE environment)
- **Auto-Detection**: Framework calls `source setup_clc qe6` during environment setup phase
- **Authentication Details**: See `.claude/templates/environment-config.md` for authentication persistence requirements

## ⚠️ CRITICAL - Command Chaining for Environment Setup
- **Session Persistence Issue**: `setup_clc` modifies environment variables that don't persist across separate command executions
- **Required Approach**: Always chain commands with `&&` after setup to maintain session state
- **Correct Pattern**: `source setup_clc qe6 && oc whoami && oc get namespaces`
- **Avoid**: Running `setup_clc` separately from subsequent `oc` commands

## ⚠️ IMPORTANT - Report Generation Guidelines
- **Framework Internal Use**: The framework uses `setup_clc` and `login_oc` scripts internally for robust authentication
- **Final Report Instructions**: All generated test cases MUST use generic `oc login` commands for broader team usability
- **Generic Format**: `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify`
- **Rationale**: Team members may not have access to framework scripts but can use standard oc login

## Manual Setup (User-Provided Kubeconfig)
- **Flexibility**: Use any cluster with any authentication method
- **Custom Environments**: Production, staging, personal dev clusters
- **Authentication**: Token, certificate, or any oc login method
- **Override**: User kubeconfig takes precedence over automatic setup