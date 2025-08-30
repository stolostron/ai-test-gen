# Complete Analysis Report Template

## EXACT SECTION ORDER (NO DEVIATIONS)

```markdown
## 🎯 Summary
**JIRA Ticket**: [JIRA-ID] - [Full title]
**Priority**: [Priority level]
**Status**: [Current status with completion percentage]
**Component**: [Component/Product area]
**Target Release**: [ACM version the feature is targeted for]

**Test Environment Status**: [Feature deployment status in test environment - deployed/not deployed]
**Feature Validation**: [Agent validation results - working/not working/partially working with details]
**Test Environment Details**:
- **Console URL**: [Full console URL used for testing]
- **ACM Version**: [Current ACM version in test environment]
- **OCP Version**: [Current OCP version in test environment]

**Business Impact**: [Critical business value and customer impact description]

## 🔧 Implementation Analysis
### Feature Overview
[Brief conceptual explanation of the feature - what it does, how it works, and its purpose]

### Code Changes & Implementation Details
[Detailed explanation of code changes with actual code snippets fetched from git, including:
- Key files modified/added
- Implementation approach and patterns used
- Integration points and architectural decisions
- Code examples showing the implementation]

## 🧪 Test Scenarios
### Test Case Coverage Overview
[Point-by-point summary of each test scenario and what it covers:
- Test Case 1: [Brief description of what this test validates]
- Test Case 2: [Brief description of what this test validates]
- Test Case 3: [Brief description of what this test validates]
- Additional test cases as generated...]

### Testing Approach Summary
[Overview of the testing strategy and methodology used for validation]

## 📈 Business Impact & Strategic Value
### Customer Benefits
[Direct customer value proposition]

### Technical Advantages
[Technical benefits and capabilities]

### Competitive Positioning
[Strategic market advantages]

## 🎯 Risk Assessment & Mitigation
### High-Risk Implementation Areas
[Technical and operational risks]

### Mitigation Strategies
[Risk reduction approaches]

## 📋 Success Criteria & Metrics
### Functional Success Criteria
[Measurable functional requirements]

### Performance Success Criteria
[Performance benchmarks and SLAs]

### Quality Success Criteria
[Quality gates and compliance measures]

## 🚀 Next Steps & Action Items
### Immediate Actions
[Short-term action items]

### Short-term Actions
[Medium-term deliverables]

### Long-term Actions
[Strategic objectives]
```

## MANDATORY REQUIREMENTS

- ✅ **REQUIRED**: Summary with test environment status and feature validation results
- ✅ **REQUIRED**: Implementation Analysis with feature overview and code changes
- ✅ **REQUIRED**: Test Scenarios with point-by-point test case summaries
- ✅ **REQUIRED**: Business Impact & Strategic Value
- ✅ **REQUIRED**: Risk Assessment & Mitigation
- ✅ **REQUIRED**: Success Criteria & Metrics
- ✅ **REQUIRED**: Next Steps & Action Items
- ❌ **BLOCKED**: Generic analysis without agent-specific insights
- ❌ **BLOCKED**: Missing test environment deployment status
- ❌ **BLOCKED**: Missing feature validation results from agent testing
- ❌ **BLOCKED**: Missing actual code changes with git-fetched examples