# Test Case Format Requirements

## 🎯 Test Case Structure Standards

### Required Test Case Structure (Mandatory)
Each test case MUST include:
1. **Description:** Clear explanation of what the test case does/tests exactly
2. **Setup:** Required setup/prerequisites needed for the test case
3. **Test Steps Table:** Step-by-step execution with verbal instructions

### Test Step Format Requirements (Mandatory)
All test steps MUST include:
1. **Verbal instruction** describing what to do
2. **CLI command** (when applicable) 
3. **UI guidance** (when applicable)

### Expected Result Format Requirements (Mandatory)
Expected Results MUST contain:
1. **Verbal explanation** of what should happen
2. **Sample YAML/data outputs** when relevant and helpful
3. **Expected command outputs** when commands/grep are used (so testers can easily see and match probable outputs)
4. **Specific values** or output descriptions

**Example:**
```markdown
## Test Case 1: Environment Setup and Resource Creation

**Description:** Validates environment access and creates ClusterCurator with required annotation for digest-based upgrades.

**Setup:** 
- Access to ACM hub cluster
- ClusterCurator CRD available
- Cluster admin permissions

| Step | Expected Result |
|------|-----------------|
| **Log into ACM hub cluster**<br>`oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Login successful with access confirmed. |
| **Verify annotation is stored correctly**<br>`oc get clustercurator digest-upgrade-test -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'` | Annotation value shows 'true' confirming feature is enabled. |
| **Check resource YAML configuration**<br>`oc get clustercurator digest-upgrade-test -o yaml` | YAML output shows annotation in metadata confirming feature activation:<br><br>```yaml<br>metadata:<br>  annotations:<br>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br>  name: digest-upgrade-test<br>spec:<br>  desiredCuration: upgrade<br>  upgrade:<br>    desiredUpdate: "4.16.37"<br>``` |
```

**NOT:**
```markdown
| **Verify annotation is stored correctly**<br>`oc get clustercurator digest-upgrade-test -o jsonpath='{.metadata.annotations}'` | Shows upgrade-allow-not-recommended-versions: true |
```

### Standalone Test Case Requirements
- **No setup dependencies:** Each test case must be completely standalone
- **Self-contained:** All required setup steps included in the test case
- **Merge related scenarios:** If dependencies exist, merge into single test case (max 10 steps)
- **Multiple tables allowed:** If >10 steps needed, use multiple tables with clear references

**Example of proper standalone structure:**
```markdown
## Test Case 1: Complete Environment Setup and Feature Validation

**Description:** End-to-end validation including environment setup and feature testing.

| Step | Expected Result |
|------|----------------|
| **Log into cluster**<br>`oc login...` | Login successful. |
| **Create test namespace**<br>`oc create namespace...` | namespace created |
| **Apply test resource**<br>`oc apply -f...` | resource created |
| **Validate feature**<br>`oc get...` | Shows expected behavior |
```

**AVOID:**
```markdown
## Test Case 1: Environment Setup
**Setup:** Fresh cluster

## Test Case 2: Feature Testing  
**Setup:** Continue from Test Case 1
```

### UI and CLI Guidance Standards

#### When to include UI guidance:
- Resource creation through OpenShift Console
- ACM Console navigation
- Configuration through web interfaces

#### When to include CLI guidance:
- Resource validation
- Status checking
- Troubleshooting commands
- Bulk operations

#### Combined approach example:
```markdown
| **Create ClusterCurator through ACM Console or CLI**<br>*UI:* ACM Console → Infrastructure → Clusters → Create ClusterCurator<br>*CLI:* `oc apply -f clustercurator.yaml` | ClusterCurator resource created successfully |
```

## 📋 Complete Analysis Report Structure

### Required Structure:
1. **Title and metadata** (Run ID, Analysis Date)
2. **Understanding Feature Summary** (concise feature explanation + brief data collection summary)
3. **Implementation Status & Feature Validation Assessment** (include specific environment used)
4. **Investigation Quality Assessment** (if needed)

### UNDERSTANDING FEATURE SUMMARY Requirements:
- **Brief feature explanation:** 2-3 sentences on what the story/feature adds
- **Data collection summary:** Brief mention of data sources used (JIRA, GitHub, environment validation)
- **Key discoveries:** Technical implementation details and business context
- **NO detailed step-by-step framework process explanations**

### Example structure:
```markdown
# TICKET-ID: Feature Name - COMPLETE INVESTIGATION ANALYSIS

**Run ID:** run-XXX-YYYYMMDD-HHMM  
**Analysis Date:** Date

---

## 🎯 UNDERSTANDING FEATURE SUMMARY

This feature adds [brief explanation of what the story implements].

Investigation gathered data from JIRA ticket hierarchy, GitHub repository analysis, and live environment validation to understand the complete implementation.

**Technical Implementation (VALIDATED):**
[Key technical details]

**Business Impact (CONFIRMED):**
[Customer and business context]

---

## 🚀 Implementation Status & Feature Validation Assessment

**Environment Used:** [Specify which environment was used for validation]
**Feature Deployment:** [Status with environment context]

[Validation results and confidence assessment]

---

## 📋 INVESTIGATION QUALITY ASSESSMENT

[Quality metrics and confidence levels]
```

## 🔧 Implementation Guidelines

### Test Case Naming:
- Use descriptive names that indicate scope
- Include "Complete" for end-to-end scenarios
- Specify validation focus

### Step Descriptions:
- Start with action verb
- Be specific about the goal
- Include context when needed

### Expected Results:
- Show actual output when possible
- Use specific values, not placeholders
- Include error messages for negative tests

### Commands:
- Use realistic cluster URLs and namespaces
- Include complete command syntax
- Add necessary flags and parameters
- For managed-cluster resource reads, prefer ManagedClusterView from the hub context
  - Include creation, read, and cleanup of `ManagedClusterView` in steps when validating `ClusterVersion`
  - Example read: `oc get managedclusterview clusterversion -n <managed-cluster-namespace> -o jsonpath='{.status.result.status.conditionalUpdates[?(@.release.version=="<ver>")].release.image}'`
  
### Schema-aware YAML requirement (Generic):
- All CRD-backed resource YAML samples MUST be schema-aware for the target environment
  - Include required fields per CRD schema (use empty/default values if not used)
  - Prefer generating skeletons via `bin/resource_schema_helper.sh`:
    - Example: `bin/resource_schema_helper.sh --group <group> --version <v> --kind <Kind> --name <name> [--namespace <ns>]`

## ✅ Quality Checklist

Before finalizing test cases, verify:
- [ ] All steps have verbal instructions
- [ ] CLI commands are complete and realistic
- [ ] UI guidance provided where applicable
- [ ] Test cases are standalone (no setup dependencies)
- [ ] Related scenarios merged appropriately
- [ ] Expected results are specific and realistic
- [ ] Complete Analysis follows required structure
- [ ] Removed deprecated sections