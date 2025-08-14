# Claude Configuration - AI Test Generation Suite

> **Global Claude slash commands for the AI Test Generation Suite**

## 🎯 Global Slash Commands

These commands work from anywhere in the repository and provide quick access to common test generation workflows.

### /generate-e2e-test-plan

**Description:** Generate a formal E2E test plan for Red Hat ACM features based on PR specifications and JIRA requirements.

**Usage:** `/generate-e2e-test-plan {PR_URL} {FEATURE_NAME} [JIRA_SOURCE]`

**Example:**
`/generate-e2e-test-plan https://github.com/org/repo/pull/123 "Feature Name" ACM-10659`

**Note:** `JIRA_SOURCE` is optional and should be a JIRA issue key (e.g., `ACM-10659`) when your environment supports live JIRA fetch.

**Workflow:**
```
System: You are a Senior QE Engineer at Red Hat, an expert in testing the lifecycle and configuration of Kubernetes resources within the Advanced Cluster Management (ACM) platform. Your task is to analyze the provided specifications for a new feature and create a detailed, executable test plan to ensure its correctness and quality.

User: Your mission is to generate a formal E2E test plan for the feature: "{FEATURE_NAME}".

CONTEXT GATHERING:
1. Fetch PR at {PR_URL} details and associated test specifications
2. If {JIRA_SOURCE} is provided, treat it as a JIRA key and fetch details (when supported)
3. Review architectural documentation and related files if provided
4. Use E2E Acceptance Criteria in JIRA to create the test plan

ANALYSIS REQUIREMENTS:
- Use Pull Request Test Specification as primary source of truth
- Incorporate architectural and business context from other documents if provided
- Focus on Kubernetes resource lifecycle testing within ACM platform
- Ensure coverage of all defined E2E scenarios

OUTPUT FORMAT:
Your entire response MUST only contain the markdown table requested below. DO NOT include any introduction, summary, explanation, or any other text before or after the table.

Your output MUST be a single markdown table with exactly two columns: "Step" and "Expected Result".

CRITICAL FORMAT REQUIREMENTS:
- ✅ **2-Column Format ONLY**: Never create 3-column tables (Step | Action | Expected Result)
- ✅ **Step Column Content**: Include verbal instructions + full commands (e.g., "**Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster.example.com:6443 --username=kubeadmin --password=<password>`")
- ✅ **Full Commands Required**: Provide complete commands with proper placeholders, not generic `<cluster-url>`
- ✅ **Expected Result Content**: Include verbal explanations + sample outputs in code blocks for all data fetch/update operations
- ✅ **NO HTML Tags**: Never use `<br/>`, `<b>`, `<i>` - use proper markdown formatting only

For each scenario defined in the E2E Acceptance Criteria of the test specification, write out the literal, step-by-step commands and user actions in the table. Do not summarize the scenarios; generate the table steps for them.

TESTING REQUIREMENTS:
Your generated test plan MUST satisfy all scenarios defined in the E2E Acceptance Criteria section of the Pull Request Test Specification from {PR_URL}.

Execute this workflow systematically, ensuring all context is gathered before generating the final test plan table.

SAVE OUTPUT:
Generated test plans are saved within the application-specific runs directories for organized tracking and version control.
```

### /analyze-workflow

**Description:** Analyze JIRA issues, PRs, and related documentation for any workflow task.

**Usage:** `/analyze-workflow {PR_URL} {ACTION_TYPE} [JIRA_SOURCE]`

**Example:** `/analyze-workflow https://github.com/repo/pull/203 "test-plan" ACM-10659`

**Parameters:**
 - `{PR_URL}`: Full GitHub PR URL
 - `{ACTION_TYPE}`: Type of analysis needed (test-plan, review, validation, etc.)
 - `{JIRA_SOURCE}`: Optional JIRA key (e.g., `ACM-10659`)

**Workflow:**
```
1. Analyze PR at {PR_URL} for technical specifications
2. If `{JIRA_SOURCE}` is provided, treat it as a JIRA key and fetch details (when supported)
3. Gather related documentation and context files
4. Perform {ACTION_TYPE} analysis based on gathered information
5. Generate appropriate output format for the requested action type
```

## 🏗️ Application-Specific Configurations

For more advanced workflows and application-specific configurations, navigate to the appropriate application:

### Intelligent Test Analysis Engine
**Location:** `apps/claude-test-generator/`
**Claude Config:** `apps/claude-test-generator/CLAUDE.md`
**Latest Version:** V2.0 - Enhanced AI validation with deployment verification
**Best For:** AI-powered test analysis, E2E test generation, smart test scoping, environment assessment, production-ready test plans, feedback loops, and continuous improvement
**Key Features:** 
- ✅ AI-powered deployment validation with version correlation
- ✅ 2-column test format enforcement 
- ✅ Complete command generation with full placeholders
- ✅ Evidence-based deployment status assessment

### Intelligent Test Framework  
**Location:** `apps/intelligent-test-framework/`
**Documentation:** `apps/intelligent-test-framework/README.md`
**Best For:** Advanced AI-powered comprehensive test generation

## 🎯 Quick Navigation

```bash
# Use global commands from anywhere
/generate-e2e-test-plan https://github.com/repo/pull/123 "Feature Name"

# Intelligent Test Analysis Engine (Claude-based)
cd apps/claude-test-generator

# Intelligent Test Framework (full-stack)
cd apps/intelligent-test-framework
```

## 📋 Global Prerequisites

- **Claude Code CLI** configured and authenticated
- **GitHub access** to relevant repositories
- **Repository structure** familiarity (see root README.md)
- **Enhanced Format Compliance**: All outputs must follow updated format requirements
- **AI Validation Requirements**: Deployment status must be validated with supporting evidence

## 🔄 Command Workflow Integration

The global commands integrate with both applications:

1. **Quick Generation**: Use global commands for immediate results
2. **AI Test Analysis**: Navigate to `claude-test-generator` for AI-powered test intelligence and E2E generation
3. **Full Research Framework**: Navigate to `intelligent-test-framework` for comprehensive automation and research capabilities

## 📚 Documentation Hierarchy

```
Root CLAUDE.md (this file)          # Global slash commands
├── apps/claude-test-generator/      
│   └── CLAUDE.md                   # App-specific Claude config
└── apps/intelligent-test-framework/
    └── README.md                   # Advanced framework docs
```

---

## 🚨 Critical Updates Based on Learning

**ACM-22079 Analysis Results** - Enhanced validation requirements implemented:

### ✅ Format Corrections Applied:
- **2-Column Table Format**: Strictly enforced (Step | Expected Result)
- **Complete Commands**: Full commands with proper placeholders required
- **Step Integration**: Verbal instructions + commands combined in Step column
- **No HTML Tags**: Markdown formatting only

### ✅ AI Validation Enhancements:
- **Deployment Status Verification**: AI must correlate ACM/MCE versions with feature availability
- **Evidence-Based Assessment**: Multi-source validation with concrete supporting data
- **Version Correlation**: Clear distinction between "implemented" vs. "deployed"
- **Error Prevention**: AI prevents incorrect deployment assessments through rigorous validation

### 📊 Quality Targets:
- **Base Score**: 75 points for format compliance
- **Category Enhancement**: +20-25 points for category-specific validation
- **Target Range**: 85-95+ points with intelligent scoring

**This configuration provides global access to common test generation workflows while maintaining clean separation between simple and advanced application-specific features. All outputs now leverage enhanced AI validation for accurate deployment assessment and proper formatting compliance.**