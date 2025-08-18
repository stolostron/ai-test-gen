# JIRA FixVersion Awareness Intelligence Service

## Purpose
MANDATORY awareness service that provides JIRA fixVersion intelligence vs test environment ACM/MCE version to enable context-aware comprehensive analysis and test plan generation.

## Service: tg-jira-fixversion-validation-service

### CRITICAL VALIDATION PROTOCOL

#### Phase 0 - MANDATORY EXECUTION
**Execute BEFORE any other AI services:**

1. **JIRA FixVersion Extraction**
   - Extract `Fix Version/s` field from JIRA ticket
   - Parse ACM version (e.g., "ACM 2.15.0" → 2.15)
   - Validate ticket status and resolution

2. **Test Environment Version Detection**
   - Check `oc get multiclusterengine -o jsonpath='{.items[0].status.currentVersion}'`
   - Extract MCE version and correlate to ACM version:
     - MCE 2.9.x = ACM 2.14.x
     - MCE 2.10.x = ACM 2.15.x
     - MCE 2.11.x = ACM 2.16.x

3. **Version Context Intelligence**
   - **CONTINUE WITH AWARENESS**: Proceed with comprehensive analysis regardless of version mismatch
   - **VERSION CONTEXT**: Provide intelligent context for test plan generation
   - **FUTURE-READY**: Generate test plans suitable for when environment is upgraded

### ENFORCEMENT RULES

#### VERSION AWARENESS SCENARIOS
⚠️ **CONTINUE WITH VERSION AWARENESS** when:
- JIRA fixVersion (e.g., ACM 2.15) > Test Environment (e.g., ACM 2.14) → **FEATURE NOT YET AVAILABLE**
- JIRA status = "Unresolved" with future fixVersion → **FEATURE IN DEVELOPMENT**
- Cannot determine JIRA fixVersion from ticket → **VERSION UNKNOWN**

#### ANALYSIS APPROACH
✅ **ALWAYS PROCEED WITH COMPREHENSIVE ANALYSIS**:
- Generate complete test plans regardless of version status
- Provide version context intelligence in reports
- Create future-ready test plans for when environment is upgraded
- Include specific validation steps to check feature availability

### ERROR HANDLING

#### Version Awareness Response
When JIRA fixVersion > test environment version:

```
**⚠️ FEATURE NOT YET AVAILABLE IN CURRENT TEST ENVIRONMENT**

**JIRA Analysis**: ACM-XXXXX targets ACM X.XX (JIRA fixVersion)
**Test Environment**: ACM Y.YY (MCE Z.ZZ detected)
**Version Context**: Feature will be available when environment upgraded to ACM X.XX+

**Intelligent Response Strategy**: 
✅ **CONTINUE**: Generate comprehensive test plan with version awareness
✅ **FUTURE-READY**: Test plan prepared for environment upgrade
✅ **VERSION CONTEXT**: Include feature availability validation steps
✅ **COMPREHENSIVE**: Full analysis including GitHub implementation details

**PROCEEDING**: Generating version-aware comprehensive test plan
```

### SUCCESS CRITERIA

#### Intelligent Execution
Regardless of version compatibility, proceed with comprehensive analysis:
- **Version Context Provided**: Include version awareness in all analysis
- **Continue to JIRA Analysis Service**: Execute full investigation workflow
- **Generate Comprehensive Test Plans**: Create future-ready test scenarios
- **Include Validation Steps**: Add feature availability checking in test cases

#### Version Correlation Table
```yaml
MCE_to_ACM_Mapping:
  "2.8.x": "ACM 2.13.x"
  "2.9.x": "ACM 2.14.x" 
  "2.10.x": "ACM 2.15.x"
  "2.11.x": "ACM 2.16.x"
  "2.12.x": "ACM 2.17.x"
```

### Integration Points

#### Service Dependencies
- **Before**: No dependencies (runs first)
- **After**: All other AI services (blocks execution if version incompatible)
- **Parallel**: None (sequential execution required)

#### Framework Integration
- Integrated into Phase 0 of workflow
- Mandatory execution in FINAL ENFORCEMENT DECLARATION
- Prevents framework validation errors for unavailable features

### Quality Assurance

#### Validation Metrics
- **Version Detection Accuracy**: 100% for MCE to ACM mapping
- **JIRA Parsing Accuracy**: 100% for fixVersion extraction  
- **Context Awareness**: 100% version context intelligence provided
- **Analysis Continuation**: 100% comprehensive analysis regardless of version status

#### Test Scenarios
1. **Compatible Versions**: JIRA ACM 2.14 + Test Env ACM 2.14 → PROCEED WITH FEATURE AVAILABLE CONTEXT
2. **Future Feature**: JIRA ACM 2.15 + Test Env ACM 2.14 → PROCEED WITH FEATURE NOT YET AVAILABLE CONTEXT
3. **Backported Feature**: JIRA ACM 2.15 + Test Env ACM 2.16 → PROCEED WITH FEATURE AVAILABLE CONTEXT
4. **Unresolved Feature**: JIRA Unresolved ACM 2.15 + Test Env ACM 2.14 → PROCEED WITH FEATURE IN DEVELOPMENT CONTEXT

### Implementation Notes

#### Command Examples
```bash
# Check test environment version
oc get multiclusterengine -o jsonpath='{.items[0].status.currentVersion}'

# JIRA validation via WebFetch
WebFetch("https://issues.redhat.com/browse/ACM-XXXXX", "Extract Fix Version/s field")

# Version comparison logic with intelligence
if jira_version <= environment_version:
    proceed_with_analysis(feature_available=True)
else:
    proceed_with_analysis(feature_available=False, version_context=True)
```

#### Intelligence Enhancement
- Provides version context intelligence for ACM-22079 type scenarios (ACM 2.15 feature on ACM 2.14 environment)
- Enables comprehensive analysis with feature availability awareness
- Generates future-ready test plans for environment upgrades
- Continues full investigation while providing version context

---

**Framework Enhancement**: This service provides intelligent version awareness that enables comprehensive analysis and test plan generation regardless of current feature availability, creating future-ready test plans while maintaining full investigation capabilities and version context intelligence.