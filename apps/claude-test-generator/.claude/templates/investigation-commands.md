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

### AI Enhanced GitHub Investigation Service
**Claude Command Pattern**: Use AI-powered GitHub analysis with `gh` CLI priority and intelligent WebFetch fallback

**🚀 Dual-Method Investigation Protocol**:
1. **Smart Detection**: Automatically detect `gh` CLI availability and authentication status
2. **Method Selection**: Prioritize `gh` CLI for enhanced capabilities, fallback to WebFetch for reliability
3. **Enhanced Analysis**: Leverage rich metadata when available, maintain quality with content analysis
4. **Intelligent Fallback**: Seamless transition between methods without user intervention

**Method 1: GitHub CLI (Priority)**:
```bash
# Enhanced investigation with rich metadata (when gh CLI available)
gh pr view <PR_NUMBER> --repo <ORG/REPO> --json title,body,state,files,reviews
gh pr list --repo <ORG/REPO> --search "<KEYWORDS>" --json number,title,state,author
gh pr diff <PR_NUMBER> --repo <ORG/REPO>
gh pr checks <PR_NUMBER> --repo <ORG/REPO>

# Advanced repository analysis
gh repo view <ORG/REPO> --json description,topics,primaryLanguage
gh api repos/<ORG/REPO>/pulls/<PR_NUMBER>/files --jq '.[].filename'
```

**Method 2: WebFetch (Fallback)**:
```bash
# Reliable content analysis (when gh CLI unavailable)
WebFetch: https://github.com/<ORG/REPO>/pull/<PR_NUMBER>
WebFetch: https://github.com/<ORG/REPO>/pull/<PR_NUMBER>/files
WebFetch: https://github.com/<ORG/REPO>/pulls?q=<KEYWORDS>
```

**🤖 AI Intelligence Benefits**:
- **With gh CLI**: 3x faster analysis, rich metadata, advanced search, CI status validation
- **With WebFetch**: Universal compatibility, content parsing, link discovery
- **Always Available**: 100% reliability with automatic method selection
- **Enhanced When Possible**: Better results when gh CLI present, consistent quality always

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

### Step 2: AI Enhanced GitHub Investigation
**AI Service**: Dual-method GitHub analysis with `gh` CLI priority and WebFetch fallback
- **Smart Method Selection**: Automatic detection and optimal method selection
- **Enhanced Capabilities**: Rich metadata analysis when gh CLI available
- **Reliable Fallback**: Content analysis via WebFetch when CLI unavailable
- **Comprehensive Coverage**: PR discovery, implementation validation, architecture analysis

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