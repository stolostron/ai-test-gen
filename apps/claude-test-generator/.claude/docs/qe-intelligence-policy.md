# QE AUTOMATION REPOSITORY INTELLIGENCE POLICY

## 🎯 Core Coverage Philosophy

**PRIMARY PRINCIPLE**: Complete feature coverage is prioritized over duplication avoidance.

### Coverage Priority Policy

**✅ ACCEPTABLE**: Minor duplication if it ensures comprehensive feature testing  
**❌ UNACCEPTABLE**: Missing critical test scenarios to avoid duplication  

## 📊 Intelligence Framework

### QE Repository Analysis Process

1. **Repository Identification**: Use predefined mapping from JIRA components
2. **Coverage Gap Analysis**: Identify what exists vs. what's needed for complete feature coverage
3. **Coverage Decision Matrix**:
   - **Full Gap**: Create comprehensive test coverage (no existing overlap)
   - **Partial Gap**: Create additional tests to fill missing scenarios (accept minor overlap)
   - **Significant Overlap**: Still create tests if they add unique value or perspective

### Decision Framework

```yaml
Coverage_Decision_Logic:
  scenario_missing: "CREATE - Always ensure complete coverage"
  scenario_partial: "CREATE - Fill gaps even with minor overlap"
  scenario_covered_differently: "CREATE - Different approach adds value"
  scenario_identical: "EVALUATE - Only skip if truly redundant"
```

## 🧠 Intelligent Coverage Analysis

### What Constitutes "Minor Duplication"?

**ACCEPTABLE OVERLAPS**:
- Same feature tested from different perspectives (e.g., CLI vs UI vs API)
- Different test environments or configurations
- Different error scenarios or edge cases
- Enhanced test coverage with better validation

**AVOID ONLY**:
- Identical test steps with identical validation
- Same exact command sequences and expected results
- Redundant basic functionality tests

### Coverage Completeness Checklist

**For Each Feature, Ensure Coverage Of**:
- ✅ Happy path scenarios
- ✅ Error handling and edge cases  
- ✅ Security and permissions validation
- ✅ Integration with related components
- ✅ Performance and scalability considerations
- ✅ Upgrade and migration scenarios
- ✅ Rollback and recovery procedures

## 📋 Implementation Guidelines

### QE Repository Restrictions and Team Focus

**MANDATORY REPOSITORY RESTRICTIONS**:
- **Primary Repository**: stolostron/clc-ui-e2e (team-managed, UI-based cluster lifecycle testing)
- **EXCLUDED REPOSITORY**: stolostron/cluster-lifecycle-e2e (NOT team-managed, NEVER analyze or reference)
- **API Repository**: stolostron/acmqe-clc-test (non-UI/API repository, use ONLY when specifically mentioned by user)

**Framework Must NEVER**:
- ❌ Analyze stolostron/cluster-lifecycle-e2e (not team-managed)
- ❌ Reference stolostron/cluster-lifecycle-e2e in analysis or recommendations
- ❌ Use stolostron/acmqe-clc-test unless user specifically mentions it
- ❌ Include excluded repositories in fallback search strategies

### QE Intelligence Analysis Output

**Framework Must Provide**:
1. **Existing Coverage Summary**: What scenarios are already tested in TEAM repositories only
2. **Gap Analysis**: What scenarios are missing or inadequately covered in team-managed repos
3. **Overlap Assessment**: Where new tests might duplicate existing coverage in team repos
4. **Coverage Justification**: Why each new test case is necessary despite any overlap

### Test Case Design Principles

**WHEN OVERLAP EXISTS**:
- **Document the overlap**: Clearly state what existing tests cover
- **Justify the addition**: Explain why additional coverage is valuable
- **Differentiate approach**: Show how new tests add unique perspective or validation
- **Maintain quality**: Ensure new tests meet 85+ quality score standards

## 🎯 Success Metrics

**Framework Success Indicators**:
- ✅ **100% Feature Coverage**: All critical scenarios tested
- ✅ **Justified Overlaps**: Any duplication clearly adds value
- ✅ **Quality Maintenance**: 85+ quality scores achieved
- ✅ **Clear Documentation**: Gap analysis and coverage rationale provided

**Example Success Pattern**:
```
Existing QE Test: Basic ClusterCurator creation
Framework Test: ClusterCurator with digest annotation + error handling + edge cases
Justification: Existing test covers basic creation; new test covers digest-specific functionality missing from QE automation
Overlap: Minimal (both create ClusterCurator but for different purposes)
Value Added: Critical digest functionality not covered elsewhere
```

## 🔒 Framework Enforcement

**QE Intelligence Must**:
- ✅ Analyze existing QE test coverage thoroughly
- ✅ Identify genuine gaps in feature testing
- ✅ Justify any overlapping test scenarios
- ✅ Prioritize complete feature coverage over duplication concerns
- ✅ Document coverage analysis and decision rationale

**REMEMBER**: It's better to have comprehensive test coverage with minor duplication than to miss critical test scenarios for a feature.