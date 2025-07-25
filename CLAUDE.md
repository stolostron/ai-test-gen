# Claude Configuration

## Custom Slash Commands

### QE Test Plan Generator

#### /generate-e2e-test-plan

**Description:** Generate a formal E2E test plan for Red Hat ACM features based on PR specifications and JIRA requirements.

**Usage:** `/generate-e2e-test-plan {PR_URL} {FEATURE_NAME} [JIRA_FILE]`

**Example:** `/generate-e2e-test-plan https://github.com/stolostron/cluster-curator-controller/pull/203 "Implement pushing custom labels to ClusterCurator Job pods" ACM-10659.txt`

**Note:** JIRA_FILE is optional. If provided, I'll read JIRA details from JIRA-details/{JIRA_FILE}. Without JIRA MCP/CLI, I cannot fetch JIRA directly.

**Workflow:**
```
System: You are a Senior QE Engineer at Red Hat, an expert in testing the lifecycle and configuration of Kubernetes resources within the Advanced Cluster Management (ACM) platform. Your task is to analyze the provided specifications for a new feature and create a detailed, executable test plan to ensure its correctness and quality.

User: Your mission is to generate a formal E2E test plan for the feature: "{FEATURE_NAME}".

CONTEXT GATHERING:
1. Fetch PR at {PR_URL} details and associated test specifications
2. If {JIRA_FILE} provided, read JIRA details from JIRA-details/{JIRA_FILE} for business requirements
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

### Generic Workflow Analyzer

#### /analyze-workflow

**Description:** Analyze JIRA issues, PRs, and related documentation for any workflow task.

**Usage:** `/analyze-workflow {PR_URL} {ACTION_TYPE} [JIRA_FILE]`

**Example:** `/analyze-workflow https://github.com/repo/pull/203 "test-plan" ACM-10659.txt`

**Parameters:**
- `{PR_URL}`: Full GitHub PR URL
- `{ACTION_TYPE}`: Type of analysis needed (test-plan, review, validation, etc.)
- `{JIRA_FILE}`: Optional file containing JIRA details (read from JIRA-details/ folder)

**Workflow:**
```
1. Analyze PR at {PR_URL} for technical specifications
2. If {JIRA_FILE} provided, read JIRA details and requirements from JIRA-details/{JIRA_FILE}
3. Gather related documentation and context files
4. Perform {ACTION_TYPE} analysis based on gathered information
5. Generate appropriate output format for the requested action type
```