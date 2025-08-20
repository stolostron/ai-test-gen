# Mandatory Complete Analysis Report Template

## 🚨 **FIXED TEMPLATE STRUCTURE - NO DEVIATIONS ALLOWED**

This template is **MANDATORY** and must be followed **EXACTLY** with no variations or reordering.

### **SECTION 1: Feature Deployment Status (MANDATORY FIRST)**

```markdown
## Feature Deployment Status

### **Feature Availability: [DEPLOYED/NOT_DEPLOYED/PARTIALLY_DEPLOYED]**

**Supporting Data:**
- **JIRA FixVersion**: [Exact JIRA version from ticket]
- **Test Environment Version**: [Actual environment version detected]
- **Implementation PR**: [GitHub PR reference with merge status]
- **Controller Status**: [Actual controller deployment status]

**Deployment Evidence:**
[Complete evidence supporting the deployment status determination]
```

### **SECTION 2A: Feature Validation Results (IF DEPLOYED)**

```markdown
## Feature Validation Results

### **Validation Status: [PASSED/FAILED/PARTIAL]**

**Validation Tests Performed:**
1. [Specific validation test 1 with results]
2. [Specific validation test 2 with results]
3. [Specific validation test 3 with results]

**Supporting Data:**
[Clear explanation of what validation was performed and results]

**Environment Capability Assessment:**
[Assessment of whether environment can fully validate the feature]
```

### **SECTION 2B: Validation Limitation (IF NOT DEPLOYED)**

```markdown
## Feature Validation Limitation

### **Validation Status: NOT POSSIBLE**

**Reason:**
Feature validation could not be performed because the feature is not deployed in the current test environment.

**Evidence:**
[Supporting evidence showing feature unavailability]

**Alternative Assessment:**
[Description of what analysis was performed instead of direct validation]
```

### **SECTION 3: Test Environment Status (MANDATORY)**

```markdown
## Test Environment Status

### **Environment Summary:**
- **Cluster Name**: [Actual cluster name]
- **OpenShift Version**: [Detected OCP version]
- **ACM Version**: [Detected ACM version]  
- **MCE Version**: [Detected MCE version]
- **Overall Health**: [Environment health assessment]

**Key Capabilities:**
- [List of validated capabilities relevant to testing]
- [Infrastructure readiness for test execution]

**Test Readiness Assessment:**
[Clear statement of environment readiness for test execution]
```

### **SECTION 4: Feature Implementation Analysis (MANDATORY)**

```markdown
## Feature Implementation Analysis

### **Implementation Overview:**
[Verbal conceptual explanation of what the feature does and how it works]

**Core Implementation Details:**
[Detailed explanation with exact code portions from actual PR]

**Code Evidence** [Code:file_path:lines:commit_sha]:
```[language]
[Exact code portions from the PR implementation]
```

**Technical Architecture:**
[Explanation of how the feature integrates with existing system]

**Implementation Complexity:**
[Assessment of implementation sophistication and technical approach]
```

### **SECTION 5: Main Test Scenarios (MANDATORY)**

```markdown
## Main Test Scenarios

### **Test Case 1: [Title]**
**Purpose**: [Clear explanation of what this test case validates]
**Logic**: [Detailed reasoning behind the test approach and why these steps]
**Coverage**: [What aspects of the feature this test case covers]

### **Test Case 2: [Title]**  
**Purpose**: [Clear explanation of what this test case validates]
**Logic**: [Detailed reasoning behind the test approach and why these steps]
**Coverage**: [What aspects of the feature this test case covers]

### **Test Case 3: [Title]**
**Purpose**: [Clear explanation of what this test case validates]  
**Logic**: [Detailed reasoning behind the test approach and why these steps]
**Coverage**: [What aspects of the feature this test case covers]

**Overall Test Strategy Rationale:**
[Explanation of why these scenarios together provide comprehensive coverage]
```

### **SECTION 6: Business Impact (MANDATORY)**

```markdown
## Business Impact

### **Customer Value:**
- **Primary Customer**: [Customer name and type]
- **Business Problem**: [Clear problem statement]
- **Solution Provided**: [How feature solves the problem]
- **Urgency Level**: [Priority and timeline implications]

### **Enterprise Impact:**
- **Market Significance**: [Broader market implications]
- **Competitive Advantage**: [How this strengthens competitive position]
- **Revenue Impact**: [Financial implications if applicable]
- **Risk Mitigation**: [Risks addressed by this feature]

### **Technical Benefits:**
- [List of technical advantages provided by the feature]
- [Integration benefits with existing systems]
- [Operational improvements enabled]
```

### **SECTION 7: Quality Metrics (MANDATORY)**

```markdown
## Quality Metrics

### **Implementation Quality:**
- **Code Quality Score**: [Assessment of implementation quality]
- **Test Coverage**: [Level of test coverage achieved or planned]
- **Implementation Complexity**: [Complexity assessment and implications]
- **Integration Risk**: [Risk assessment for integration and deployment]

### **Test Plan Quality:**
- **Pattern Traceability**: [Percentage of test elements traceable to proven patterns]
- **Environment Coverage**: [Coverage of different environment scenarios]
- **Error Scenario Coverage**: [Coverage of failure and edge cases]
- **Automation Readiness**: [Readiness for automated test execution]

### **Framework Validation:**
- **Evidence-Based Analysis**: [Validation that all analysis backed by evidence]
- **Implementation Reality Alignment**: [Alignment with actual codebase]
- **Cross-Agent Consistency**: [Consistency across all framework services]
- **Quality Gate Compliance**: [Compliance with framework quality standards]
```

### **SECTION 8: Conclusion (MANDATORY LAST)**

```markdown
## Conclusion

**Summary Assessment:**
[Concise summary of feature readiness and test strategy]

**Test Execution Readiness:**
[Clear statement of readiness to execute tests]

**Key Success Factors:**
1. [Primary success factor]
2. [Secondary success factor]  
3. [Additional success factors]

**Strategic Recommendations:**
[Clear recommendations for test execution and strategy optimization]

**Framework Confidence:**
[Statement of framework confidence in analysis and recommendations]
```

## 🚨 **ENFORCEMENT RULES**

### **MANDATORY STRUCTURE:**
- ✅ **EXACT ORDER**: Sections must appear in exact order specified
- ✅ **ALL SECTIONS**: No sections can be omitted
- ✅ **EXACT HEADINGS**: Section headings must match exactly
- ✅ **SUBSECTION COMPLIANCE**: All subsections must be included

### **BLOCKING CONDITIONS:**
- ❌ **BLOCK**: Report with missing sections
- ❌ **BLOCK**: Report with sections in wrong order
- ❌ **BLOCK**: Report with modified section headings
- ❌ **BLOCK**: Report missing mandatory subsections

### **CONTENT REQUIREMENTS:**
- **Feature Status**: Must be explicitly stated as DEPLOYED/NOT_DEPLOYED/PARTIALLY_DEPLOYED
- **Validation Results**: Must clearly state validation outcome
- **Code Evidence**: Must include actual code portions from PRs
- **Verbal Explanations**: Must include conceptual explanations alongside technical details
