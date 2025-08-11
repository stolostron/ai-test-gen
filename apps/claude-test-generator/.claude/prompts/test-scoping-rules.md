# Smart Test Scoping Rules

## Core Philosophy
Focus ONLY on testing what actually changed in the implementation, avoiding redundant testing of existing stable functionality.

**CRITICAL**: Always validate implementation reality before generating test cases to prevent assumption-based errors.

## Analysis Framework

### 1. Code Change Classification
```
NEW: Functions/logic that didn't exist before
MODIFIED: Existing functions with changed behavior  
UNCHANGED: Existing functions with no changes
```

### 2. Implementation Reality Assessment (RECOMMENDED)

#### **Attempt to validate when possible:**
- **Resource Schemas**: Check OpenShift/ACM resource structures when environment accessible
- **Component Patterns**: Identify standard operator/controller deployment patterns
- **Feature Status**: Assess basic functionality availability when environment allows
- **Operational Patterns**: Understand logging and monitoring approaches for accurate commands

#### **Adaptive Generation Rules:**
- **Continue regardless of validation results** - always generate comprehensive test plan
- **Document validation limitations** - clearly report what couldn't be verified
- **Provide multiple approaches** - offer alternative validation methods when specific ones fail
- **Use OpenShift/ACM best practices** - leverage standard patterns even when verification incomplete

### 3. Test Scope Rules

#### ✅ INCLUDE IN TESTING:
- NEW functionality and code paths
- MODIFIED business logic flows
- Integration points between new and existing code
- NEW error handling specific to the feature
- NEW configuration/annotation processing

#### ❌ EXCLUDE FROM TESTING:
- Existing unchanged functionality
- General error handling (unless specifically modified)
- Monitoring and logging (unless enhanced for new feature)
- UI components (unless changed for new feature)
- Network/infrastructure (unless modified)

### 4. Table Optimization
- **Target**: 1-3 tables for most features
- **Maximum**: 8-10 steps per table
- **Focus**: E2E scenarios exercising new code paths
- **Avoid**: Comprehensive testing of every edge case in unchanged code

### 5. Enhanced Test Case Structure

#### Test Case Format:
```markdown
## Test Case N: [Clear Test Case Name]

### Description
[Brief explanation of what this test case validates, including business value and technical scope in 2-3 sentences]

### Setup
**Prerequisites**:
- Hub cluster access (choose one):
  - **Option A**: Automatic setup: `source setup_clc qe6`
  - **Option B**: Custom kubeconfig: `export KUBECONFIG=/path/to/your/kubeconfig && oc login <cluster-url>`
- Environment verification: `oc whoami && oc get managedclusters`
- [Any specific setup requirements]

**Required Files**: 
[List any YAML files or configurations needed]
```

#### Table Structure:
- **Column Names**: Strictly use "Steps" and "Expected Result"
- **Steps Column**: Clear action with copy-pasteable commands
- **Expected Result Column**: Show actual expected output, NOT commands to run

#### Steps Column Format:
```markdown
**Step N: [Action Description]**

Instructions: 
1. Go to your terminal
2. Run the following command: `[exact copy-pasteable command]`
3. [Additional context if needed]
```

#### Expected Result Column Format:
```markdown
**Success Criteria**: [Specific, measurable outcome]

**Expected Output**:
```
[actual expected terminal output with explanations]
```

**YAML Result** (when applicable):
```yaml
[relevant YAML showing expected state]
```
```

#### E2E Focus Requirements:
- **E2E Coverage**: Test complete workflows end-to-end covering all NEW functionality
- **Multiple Tables**: OK to create multiple focused tables for clarity
- **Simple Execution**: Keep steps simple to follow and execute
- **Clear Output**: Show actual expected results, not commands to validate

## Example Application: ACM-22079

### What Changed (TEST THESE):
- NEW: validateUpgradeVersion() returns digest string
- NEW: Digest discovery algorithm (conditionalUpdates → availableUpdates → fallback)
- NEW: Smart force flag logic (no force needed with digests)
- NEW: Annotation processing for non-recommended upgrades

### What Didn't Change (SKIP THESE):
- General upgrade monitoring
- Timeout handling
- Network error recovery
- UI upgrade workflows
- Basic ClusterCurator CRUD operations

### Recommended Test Tables:
1. Core Digest Discovery Workflow
2. Fallback Mechanism Validation  
3. Integration with Existing Upgrade Flow

### 6. E2E Test Focus

**E2E COVERAGE APPROACH**: 
- Focus on complete end-to-end workflows covering all NEW functionality
- Test the full user journey from start to finish
- Multiple focused tables are acceptable for clarity
- Keep execution simple and straightforward

**AVOID**: 
- Excessive preamble sections about what's not being tested
- Complex security validation sections unless core to the feature
- Commands in expected results (show actual output instead)
