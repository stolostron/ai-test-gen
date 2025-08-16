# Test Case Format Requirements

## 🚨 CRITICAL FORMAT REQUIREMENTS - ENFORCED BY VALIDATION

**Quality Target: 85+ points** (Current average: 60/100)

### ❌ ZERO TOLERANCE FAILURES
1. **NO HTML TAGS**: Never use `<br/>`, `<b>`, `<i>` - causes 10-point deduction
2. **EXACT LOGIN FORMAT**: Must use exact Step 1 format - causes 15-point deduction if wrong
3. **DEPLOYMENT STATUS HEADER**: Must use `## 🚨 DEPLOYMENT STATUS` exactly - causes 15-point deduction if wrong
4. **SAMPLE OUTPUTS**: Must include realistic outputs in code blocks - causes 10-point deduction if missing
5. **NO INTERNAL SCRIPTS**: Never mention `setup_clc` or `login_oc` - causes 10-point deduction

## 🎯 Test Case Structure Standards

### Required Test Case Structure (Mandatory)
Each test case MUST include:
1. **Description:** Clear explanation of what the test case does/tests exactly
2. **Setup:** Required setup/prerequisites needed for the test case
3. **Test Steps Table:** Step-by-step execution with verbal instructions
4. **EXACT LOGIN FORMAT:** Must start with: `**Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: oc login...`

### ❌ MANDATORY TEST STEP FORMAT REQUIREMENTS
All test steps MUST include:
1. **Verbal instruction** describing what to do (NEVER start with only a command)
2. **CLI command** (when applicable) 
3. **UI guidance** (when applicable)

**✅ CORRECT (verbal instruction first):**
```markdown
| **Step 2: Create test namespace** - Run: `oc create namespace test-ns` | Namespace created successfully |
```

**❌ WRONG (command only):**
```markdown
| `oc create namespace test-ns` | Namespace created |
```

**CRITICAL:** Never start a step with only a CLI command - always include verbal explanation first.

### ❌ MANDATORY EXPECTED RESULT REQUIREMENTS (10-point deduction)
Expected Results MUST contain:
1. **Verbal explanation** of what should happen
2. **Sample YAML/data outputs** in triple backticks when fetching/updating data (MANDATORY)
3. **Expected command outputs** when commands/grep are used (so testers can easily see and match probable outputs)
4. **Specific values** or realistic sample data (NOT placeholders)

**✅ CORRECT (includes sample output):**
```markdown
| **Step 2: Check status** - Run: `oc get pods` | Pods are running:
```
NAME                    READY   STATUS
controller-abc123       1/1     Running
``` |
```

**❌ WRONG (missing sample output):**
```markdown
| **Step 2: Check status** - Run: `oc get pods` | Pods should be running |
```

**✅ PERFECT EXAMPLE (85+ points):**
```markdown
## Test Case 1: Environment Setup and Resource Creation

**Description:** Validates environment access and creates ClusterCurator with required annotation for digest-based upgrades.

**Setup:** 
- Access to ACM hub cluster
- ClusterCurator CRD available
- Cluster admin permissions

| Step | Expected Result |
|------|------------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify` | Login successful with access confirmed:
```
Login successful.
You have access to 67 projects, the list has been suppressed.
Using project "default".
``` |
| **Step 2: Verify annotation is stored correctly** - Check the annotation value: `oc get clustercurator digest-upgrade-test -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'` | Annotation value shows 'true' confirming feature is enabled:
```
true
``` |
| **Step 3: Check resource YAML configuration** - Retrieve full resource details: `oc get clustercurator digest-upgrade-test -o yaml` | YAML output shows annotation in metadata confirming feature activation:
```yaml
metadata:
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'
  name: digest-upgrade-test
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.37"
``` |
```

**KEY SUCCESS FACTORS:**
- ✅ No HTML tags anywhere
- ✅ Exact Step 1 format with "Log into the ACM hub cluster"
- ✅ Realistic sample outputs in code blocks
- ✅ Verbal instructions before commands
- ✅ No internal script references

## ❌ CRITICAL FORMAT VIOLATIONS (CAUSES VALIDATION FAILURE):

### ❌ HTML Tags (10-point deduction):
```markdown
| **Verify annotation is stored correctly**<br/>`oc get clustercurator` | Shows result |
```

### ✅ CORRECT Format (Use ` - ` instead):
```markdown
| **Verify annotation is stored correctly** - Run: `oc get clustercurator` | Shows result:
```
upgrade-allow-not-recommended-versions: true
``` |
```

### ❌ Wrong Login Format (15-point deduction):
```markdown
| **Step 1: Access cluster** - Login: `oc login` | Success |
```

### ✅ REQUIRED Login Format:
```markdown
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify` | Login successful... |
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
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login...` | Login successful with access confirmed:
```
Login successful.
``` |
| **Step 2: Create test namespace** - Run: `oc create namespace test-ns` | Namespace created successfully:
```
namespace/test-ns created
``` |
| **Step 3: Apply test resource** - Apply configuration: `oc apply -f test-resource.yaml` | Resource created successfully:
```
clustercurator.cluster.open-cluster-management.io/test-curator created
``` |
| **Step 4: Validate feature** - Check status: `oc get clustercurator test-curator` | Shows expected behavior:
```
NAME           STATUS   AGE
test-curator   Ready    30s
``` |
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
| **Create ClusterCurator through ACM Console or CLI** - *UI:* ACM Console → Infrastructure → Clusters → Create ClusterCurator - *CLI:* `oc apply -f clustercurator.yaml` | ClusterCurator resource created successfully:
```
clustercurator.cluster.open-cluster-management.io/my-curator created
``` |
```

## 📋 Complete Analysis Report Structure

### ❌ MANDATORY DEPLOYMENT STATUS HEADER (15-point deduction)
**EXACT HEADER REQUIRED in Complete-Analysis.md:**

✅ **REQUIRED FORMAT:**
```markdown
## 🚨 DEPLOYMENT STATUS

**Feature Deployment:** ✅ DEPLOYED / 🟡 PARTIALLY DEPLOYED / ❌ NOT DEPLOYED
```

❌ **WRONG (causes validation failure):**
```markdown
## 🚀 Implementation Status & Feature Validation Assessment
## Implementation Status
## Deployment Assessment
```

### Required Structure:
1. **Title and metadata** (Run ID, Analysis Date)
2. **🚨 DEPLOYMENT STATUS** (EXACT header text - mandatory)
3. **Understanding Feature Summary** (concise feature explanation + brief data collection summary)
4. **Implementation Status** (what is implemented, PRs, key behavior)
5. **Environment & Validation Status** (environment used, validation results, limitations)
6. **Investigation Quality Assessment** (if needed)

### UNDERSTANDING FEATURE SUMMARY Requirements:
- **Brief feature explanation:** 2-3 sentences on what the story/feature adds
- **Data collection summary:** Brief mention of data sources used (JIRA, GitHub, environment validation)
- **Key discoveries:** Technical implementation details and business context
- **NO detailed step-by-step framework process explanations**

### ✅ CORRECT Analysis Structure (85+ points):
```markdown
# TICKET-ID: Feature Name - COMPLETE INVESTIGATION ANALYSIS

**Run ID:** run-XXX-YYYYMMDD-HHMM  
**Analysis Date:** Date

---

## 🚨 DEPLOYMENT STATUS

**Feature Deployment:** ✅ DEPLOYED / 🟡 PARTIALLY DEPLOYED / ❌ NOT DEPLOYED

[Evidence-based assessment with concrete validation data]

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

**CRITICAL:** The `## 🚨 DEPLOYMENT STATUS` header MUST be the exact text - validation will fail otherwise.

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
  - Prefer generating skeletons via AI Schema Service and standard commands:
    - Example: `oc explain <resource>.spec` and `oc create <resource> <name> --dry-run=client -o yaml`

### ❌ MANDATORY HTML TAGS PROHIBITION (10-point deduction)
**NEVER USE HTML TAGS** - causes immediate validation failure:
- ❌ `<br/>` or `<br>` - Use ` - ` instead
- ❌ `<b>` or `<i>` - Use **bold** or *italic* markdown instead
- ❌ `<div>`, `<span>`, etc. - Use proper markdown formatting

**✅ CORRECT Formatting:**
- Use ` - ` for inline separation: `**Step 1: Action** - Command: \`oc login\``
- Use `\n` for line breaks in expected results
- Use backticks for inline commands: `oc create namespace test-ns`
- Use fenced code blocks for sample outputs
- Prefer `grep -E` for alternations and avoid escaping `|` in shell pipelines

### ❌ MANDATORY LOGIN STEP FORMAT (15-point deduction)
**ALL test cases MUST start with this EXACT format:**

✅ **REQUIRED FORMAT (EXACT TEXT):**
```markdown
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify` | Login successful with access confirmed:
```
Login successful.
You have access to 67 projects, the list has been suppressed.
Using project "default".
``` |
```

**Validation looks for this exact text pattern:** `Log into the ACM hub cluster: \`oc login`

❌ **WRONG (causes validation failure):**
- `Step 1: Access cluster`
- `Step 1: Login to hub`
- `Step 1: Connect to cluster`

✅ **MUST USE EXACT TEXT:** `Step 1: Log into the ACM hub cluster`

❌ **NEVER expose internal scripts (10-point deduction):**
- Never mention `setup_clc` or `login_oc` in test cases
- Always use generic `oc login <cluster-url>` format

## ✅ VALIDATION CHECKLIST (85+ POINTS TARGET)

**BEFORE GENERATING ANY OUTPUT, VERIFY:**
- [ ] ❌ NO HTML tags (`<br/>`, `<b>`, `<i>`) anywhere (10 points)
- [ ] ✅ First step EXACTLY: "**Step 1: Log into the ACM hub cluster**" (15 points)
- [ ] ✅ Header EXACTLY: "## 🚨 DEPLOYMENT STATUS" (15 points)
- [ ] ✅ Sample outputs in triple backticks (10 points)
- [ ] ❌ No `setup_clc` or `login_oc` mentioned (10 points)
- [ ] ✅ Files exist (Complete-Analysis.md, Test-Cases.md, metadata.json) (30 points)
- [ ] ✅ Other formatting requirements (10 points)

**QUALITY SCORING WEIGHTS:**
- Files exist: 30 points
- No HTML tags: 10 points  
- Correct login step: 15 points
- Deployment status header: 15 points
- Sample outputs: 10 points
- No internal scripts: 10 points
- Other formatting: 10 points

**TOTAL POSSIBLE: 100 points | TARGET: 85+ points**

### ✅ Additional Quality Checks:
- [ ] All steps have verbal instructions
- [ ] CLI commands are complete and realistic
- [ ] UI guidance provided where applicable  
- [ ] Test cases are standalone (no setup dependencies)
- [ ] Related scenarios merged appropriately
- [ ] Expected results are specific with realistic sample outputs
- [ ] Complete Analysis follows required structure