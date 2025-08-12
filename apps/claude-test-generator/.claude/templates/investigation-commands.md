# Investigation Command Reference

## 🔍 Complete Investigation Protocol Commands

### AI Documentation Service
**Claude Command Pattern**: Use AI-powered JIRA analysis via TodoWrite and structured investigation

**AI Investigation Protocol**:
1. **Ticket Analysis**: Use `jira issue view <TICKET-ID>` for main ticket details
2. **Hierarchical Discovery**: Recursively analyze all linked tickets, subtasks, and dependencies
3. **Comment Analysis**: Extract URLs, GitHub links, PR references from descriptions AND comments
4. **Quality Assessment**: Generate comprehensive investigation summary with quality metrics
5. **Documentation Categorization**: Provide categorized documentation URLs for WebFetch investigation

**Example AI Documentation Workflow**:
```bash
# Primary ticket analysis
jira issue view ACM-22079

# Linked ticket discovery and analysis via AI reasoning
# AI will automatically identify and analyze ALL nested relationships up to 3 levels deep
```

### AI GitHub Investigation Service
**Claude Command Pattern**: Use AI-powered GitHub analysis via WebFetch and intelligent search patterns

**AI GitHub Investigation Protocol**:
1. **PR Discovery**: Intelligent search for related PRs using GitHub API patterns
2. **Repository Analysis**: Deep code analysis using WebFetch for GitHub PR content
3. **Implementation Validation**: AI-powered code change analysis and impact assessment
4. **Architecture Discovery**: Intelligent pattern recognition for system design understanding

**Example AI GitHub Workflow**:
```bash
# AI will automatically:
# - Discover related PRs through intelligent search patterns
# - Analyze PR content via WebFetch for implementation details
# - Perform semantic code analysis for architectural understanding
# - Validate feature implementation status and deployment readiness
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

### Step 1: AI Documentation Discovery
**AI Service**: Comprehensive JIRA hierarchy analysis with intelligent link traversal
- Automatic ticket relationship mapping
- Comment analysis for hidden documentation links
- Quality-scored investigation summaries

### Step 2: AI Repository Investigation
**AI Service**: Intelligent GitHub analysis with PR discovery and code understanding
- Semantic PR search and discovery
- Implementation status validation
- Architecture pattern recognition

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