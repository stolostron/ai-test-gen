# Enhanced Analysis Report Template

## 🚨 MANDATORY CITATION REQUIREMENTS
**CRITICAL**: All factual claims in complete reports MUST include verified citations
**SCOPE**: Complete reports only - test tables maintain clean format
**FORMAT**: Use standardized citation formats for audit compliance

## 🚨 DEPLOYMENT STATUS

**Feature Deployment:** ✅ DEPLOYED / 🟡 PARTIALLY DEPLOYED / ❌ NOT DEPLOYED / ❓ UNKNOWN  
**Environment Used:** [qe6/qe7/custom]  
**Implementation Status:** ✅ COMPLETED / 🚧 IN PROGRESS / ⏳ PENDING  
**Primary PR:** [Link and description] [GitHub:org/repo#PR:state:commit_sha]  
**Version Target:** [Fix Version from JIRA] [JIRA:ACM-XXXXX:status:last_updated]  
**Key Behavior:** [Core functionality description] [Docs:URL#section:last_verified]

## Environment & Validation Status

**Environment:** [cluster name and details]  
**Environment ACM Version:** [actual version detected]  
**Validation Commands Executed:**
```bash
# List actual commands run during validation
oc get multiclusterhub -A -o jsonpath='{.items[*].status.currentVersion}'
# Additional component-specific validation commands
```

**Validation Results:**
- ✅ [Successful validations with evidence] [Env:cluster_url:connectivity:timestamp]
- ⚠️ [Partial validations with explanations] [Code:file_path:lines:commit_sha]  
- ❌ [Failed validations with error details] [JIRA:ticket_id:status:last_updated]

## Root Cause Assessment

**Version Analysis:**
- **Feature Target Version:** [from JIRA Fix Version] [JIRA:ACM-XXXXX:status:last_updated]
- **Environment Version:** [detected from cluster] [Env:cluster_url:connectivity:timestamp]
- **Version Compatibility:** COMPATIBLE / INCOMPATIBLE [Docs:URL#version-matrix:last_verified]

**Feature Availability Diagnosis:**

### Scenario A: Feature Not Yet Deployed (Expected)
- **Evidence:** Version mismatch detected (feature targets X.Y, environment runs X.Z where Z < Y) [Env:cluster_url:connectivity:timestamp]
- **PR Status:** Merged but not included in current environment build [GitHub:org/repo#PR:state:commit_sha]
- **Assessment:** Expected behavior - no bug suspected [JIRA:ACM-XXXXX:status:last_updated]
- **Recommendation:** Feature will be available when environment upgrades to target version [Docs:URL#release-schedule:last_verified]

### Scenario B: Feature Should Be Available But Failing (Potential Bug)  
- **Evidence:** Version compatibility suggests feature should work [Docs:URL#version-matrix:last_verified]
- **PR Status:** Merged and environment version should include feature [GitHub:org/repo#PR:state:commit_sha]
- **Validation Failure:** [Specific validation failures with error messages] [Code:file_path:lines:commit_sha]
- **Assessment:** Potential deployment issue, configuration problem, or feature regression [JIRA:ticket_id:status:last_updated]
- **Recommendation:** Investigate deployment process or file bug report [Docs:URL#troubleshooting:last_verified]

### Scenario C: Feature Available and Working
- **Evidence:** [Successful validation results]
- **Assessment:** Feature ready for comprehensive testing
- **Recommendation:** Execute full test suite

## Testing Readiness Assessment

**Current Capability:**
- ✅ [What can be tested immediately]
- ⚠️ [What can be partially tested with limitations]
- ❌ [What cannot be tested until feature availability]

**Future Testing Roadmap:**
- [What will be possible when feature becomes available]
- [Environment requirements for complete testing]
- [Timeline expectations based on version analysis]

## Investigation Summary
[Brief summary of JIRA analysis, GitHub research, and internet investigation findings]

## Feature Summary
[Concise technical description focusing on user value and implementation approach]