# Investigation Command Reference

## 🔍 Complete Investigation Protocol Commands

### Documentation Investigation
```bash
# Comprehensive documentation discovery from JIRA tickets with complete hierarchy traversal
bin/doc-investigation.sh <TICKET-ID>

# Example: Extract ALL documentation links from ACM-22079 + ALL nested linked tickets + comments
bin/doc-investigation.sh ACM-22079

# This will automatically:
# 1. Analyze main ticket + all linked tickets (up to 3 levels deep)
# 2. Extract URLs, GitHub links, PR references from descriptions AND comments
# 3. Generate comprehensive investigation summary with quality metrics
# 4. Provide categorized documentation URLs for WebFetch investigation
```

### GitHub Repository Investigation  
```bash
# Enhanced GitHub repository access with SSH
bin/github-investigation.sh <TICKET-ID> "search-terms"

# Example: Deep repository search for implementation details
bin/github-investigation.sh ACM-22079 "desiredUpdate,digest,upgrade"

# Manual repository cloning for detailed analysis
git clone git@github.com:stolostron/cluster-curator-controller.git /tmp/investigation/

# Search within cloned repositories
grep -r "TICKET-ID" /tmp/investigation/*/
grep -r "implementation-keywords" /tmp/investigation/*/ --include="*.go" --include="*.yaml"
```

### Internet Research Protocol
```bash
# Technology foundation research
WebFetch: "https://docs.openshift.com/container-platform/latest/updating/"
WebFetch: "https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management/"

# Feature-specific research  
Search: "<TECHNOLOGY> <FEATURE> implementation examples"
Search: "<TECHNOLOGY> <FEATURE> best practices"
Search: "<TECHNOLOGY> <FEATURE> troubleshooting"

# Community knowledge research
Search: "<TECHNOLOGY> <FEATURE> github examples"
Search: "stolostron <COMPONENT> examples github"
```

### Environment Validation Commands
```bash
# Environment setup with command chaining
source bin/setup_clc qe6 && oc whoami && oc get namespaces

# CRD schema deep inspection
oc get crd <CRD-NAME> -o jsonpath='{.spec.versions[0].schema.openAPIV3Schema.properties.spec.properties}' | jq '.'

# Practical feature testing
oc create namespace test-validation
oc apply -f test-resource.yaml
oc get <RESOURCE> -o yaml
```

## 🎯 Investigation Workflow

### Step 1: Documentation Discovery
```bash
bin/doc-investigation.sh <TICKET-ID>
# Review: /tmp/claude-doc-investigation/investigation_summary.md
```

### Step 2: Repository Investigation
```bash  
bin/github-investigation.sh <TICKET-ID> "key-terms"
# Review: /tmp/claude-investigation-repos/
```

### Step 3: Internet Research
```bash
# Follow enhanced research protocol
# See: .claude/workflows/enhanced-internet-research.md
```

### Step 4: Environment Validation
```bash
# Environment setup and practical testing
source bin/setup_clc qe6 && [validation commands]
```

## 📋 Command Success Criteria

- **Documentation**: All JIRA ticket documentation links discovered and analyzed
- **Repository**: Complete repository access with implementation details found
- **Research**: Minimum 3+ authoritative sources, 2+ implementation examples
- **Validation**: Practical testing confirms implementation status and behavior