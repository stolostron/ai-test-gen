# Claude Configuration - AI Test Generation Suite

> **Global Claude slash commands for the AI Test Generation Suite**

## 🎯 Global Slash Commands

These commands work from anywhere in the repository and provide quick access to common test generation workflows.

### /generate-e2e-test-plan

**Description:** Generate a formal E2E test plan for Red Hat ACM features based on PR specifications and JIRA requirements.

**Usage:** `/generate-e2e-test-plan {PR_URL} {FEATURE_NAME} [JIRA_SOURCE]`

**Example (either form):**
 - Local file: `/generate-e2e-test-plan https://github.com/stolostron/cluster-curator-controller/pull/203 "Implement pushing custom labels to pods" ACM-10659.txt`
 - JIRA key: `/generate-e2e-test-plan https://github.com/org/repo/pull/123 "Feature Name" ACM-10659`

**Note:** `JIRA_SOURCE` is optional and can be either:
 - A local file stored under `JIRA-details/` (e.g., `ACM-10659.txt`)
 - A JIRA issue key (e.g., `ACM-10659`), if your environment supports live JIRA fetch

If live JIRA access isn't available, place a plain-text/markdown export in `JIRA-details/` and reference the filename.

**Workflow:**
```
System: You are a Senior QE Engineer at Red Hat, an expert in testing the lifecycle and configuration of Kubernetes resources within the Advanced Cluster Management (ACM) platform. Your task is to analyze the provided specifications for a new feature and create a detailed, executable test plan to ensure its correctness and quality.

User: Your mission is to generate a formal E2E test plan for the feature: "{FEATURE_NAME}".

CONTEXT GATHERING:
1. Fetch PR at {PR_URL} details and associated test specifications
2. If {JIRA_SOURCE} is provided:
   - If it matches a file in JIRA-details/, read details from that file
   - Otherwise, treat it as a JIRA key and fetch details (when supported)
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

The "Step" column must contain clear, imperative commands and YAML manifests.

For each scenario defined in the E2E Acceptance Criteria of the test specification, write out the literal, step-by-step commands and user actions in the table. Do not summarize the scenarios; generate the table steps for them.

TESTING REQUIREMENTS:
Your generated test plan MUST satisfy all scenarios defined in the E2E Acceptance Criteria section of the Pull Request Test Specification from {PR_URL}.

Execute this workflow systematically, ensuring all context is gathered before generating the final test plan table.

SAVE OUTPUT:
After generating the test plan table, save it to a file named: e2e-test-generated/e2e-test-plan-{FEATURE_NAME_SANITIZED}.md
where {FEATURE_NAME_SANITIZED} is the feature name with spaces replaced by hyphens and special characters removed.
```

### /analyze-workflow

**Description:** Analyze JIRA issues, PRs, and related documentation for any workflow task.

**Usage:** `/analyze-workflow {PR_URL} {ACTION_TYPE} [JIRA_SOURCE]`

**Example:** `/analyze-workflow https://github.com/repo/pull/203 "test-plan" ACM-10659.txt`

**Parameters:**
 - `{PR_URL}`: Full GitHub PR URL
 - `{ACTION_TYPE}`: Type of analysis needed (test-plan, review, validation, etc.)
 - `{JIRA_SOURCE}`: Optional JIRA input. Either a local file from `JIRA-details/` or a JIRA key (e.g., `ACM-10659`)

**Workflow:**
```
1. Analyze PR at {PR_URL} for technical specifications
2. If `{JIRA_SOURCE}` is provided:
   - If it matches a file in `JIRA-details/`, read details from that file
   - Otherwise, treat it as a JIRA key and fetch details (when supported)
3. Gather related documentation and context files
4. Perform {ACTION_TYPE} analysis based on gathered information
5. Generate appropriate output format for the requested action type
```

## 🏗️ Application-Specific Configurations

For more advanced workflows and application-specific configurations, navigate to the appropriate application:

### Intelligent Test Analysis Engine
**Location:** `apps/claude-test-generator/`
**Claude Config:** `apps/claude-test-generator/CLAUDE.md`
**Best For:** AI-powered test analysis, E2E test generation, smart test scoping, environment assessment, production-ready test plans, feedback loops, and continuous improvement

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

**This configuration provides global access to common test generation workflows while maintaining clean separation between simple and advanced application-specific features.**