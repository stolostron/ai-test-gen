# Deployment Validation Checklist

## 🚨 CRITICAL FORMAT ENFORCEMENT

**VALIDATION CHECKLIST FOR 85+ QUALITY SCORE**

### ❌ ZERO TOLERANCE VALIDATION FAILURES
1. **DEPLOYMENT STATUS HEADER**: Must use exact `## 🚨 DEPLOYMENT STATUS` format (15-point deduction)
2. **NO HTML TAGS**: Forbidden in all outputs (10-point deduction)
3. **LOGIN STEP FORMAT**: Must be exact `**Step 1: Log into the ACM hub cluster**` (15-point deduction)
4. **SAMPLE OUTPUTS**: Must include realistic outputs in code blocks (10-point deduction)
5. **NO INTERNAL SCRIPTS**: Never mention setup_clc or login_oc (10-point deduction)

## ⚠️ MANDATORY Feature Deployment Validation

**CRITICAL:** This checklist MUST be completed before making any claims about feature availability in test environments.

### 📋 Evidence Collection Checklist

**✅ Container Image Analysis:**
- [ ] Extract running controller/operator pod images from test environment
- [ ] Record image digests and registry information  
- [ ] Cross-reference image build dates with PR merge dates
- [ ] Determine if image was built after feature implementation

**✅ Feature Behavior Verification:**
- [ ] Attempt to exercise new functionality in test environment
- [ ] Test new fields/APIs/behaviors work as expected
- [ ] Document what works vs. what fails/missing
- [ ] Capture error messages or unexpected behaviors

**✅ Version Correlation Analysis:**
- [ ] Map PR merge date to product release cycles
- [ ] Identify minimum product version containing feature
- [ ] Compare test environment version to minimum required
- [ ] Account for downstream build and release lag times

**✅ Supporting Evidence Documentation:**
- [ ] Record specific validation commands executed
- [ ] Capture command outputs and results
- [ ] Document any blockers or limitations encountered
- [ ] Provide concrete evidence supporting conclusions

### 🎯 Deployment Status Classification

**Select ONE status based on evidence:**

- **🟢 DEPLOYED**: Feature confirmed working in test environment
  - *Required Evidence*: Successful feature behavior test + image version correlation

- **🟡 PARTIALLY DEPLOYED**: Some components available, others missing
  - *Required Evidence*: Specify exactly what works and what doesn't

- **🔴 NOT DEPLOYED**: Feature code merged but not available in test environment  
  - *Required Evidence*: Image analysis showing pre-feature build dates

- **❓ UNKNOWN**: Unable to verify deployment status
  - *Required Evidence*: Document validation attempts and blockers

### 📝 Evidence-Based Reporting Template

```markdown
## 🚨 DEPLOYMENT STATUS

**Feature Deployment:** ✅ DEPLOYED / 🟡 PARTIALLY DEPLOYED / ❌ NOT DEPLOYED

**Evidence Summary:**
- Container Image: [digest and correlation analysis]
- Behavior Testing: [what was tested and results]
- Version Analysis: [PR date vs. environment version]
- Validation Commands: [specific commands executed]

**Supporting Data:**
[Include specific command outputs, error messages, or verification results]

**Impact on Testing:**
- Can test immediately: [specific scenarios]
- Cannot test yet: [specific scenarios and why]
- Requires future validation: [when feature becomes available]
```

### 🔧 Standard Validation Commands

**Image Analysis:**
```bash
# Extract controller images
oc get pods -n <NAMESPACE> | grep <CONTROLLER>
oc get pod <POD> -n <NAMESPACE> -o jsonpath='{.spec.containers[0].image}'

# Get deployment info
oc get deployment <CONTROLLER> -n <NAMESPACE> -o yaml | grep -A 5 -B 5 image:
```

**Feature Testing:**
```bash
# Test new CRD fields/behaviors
oc apply -f test-resource.yaml --dry-run=server
oc get <RESOURCE> -o yaml | grep <NEW_FIELD>

# Check controller logs for new functionality
oc logs -n <NAMESPACE> <CONTROLLER_POD> | grep <FEATURE_KEYWORD>
```

**Version Verification:**
```bash
# Get cluster/product versions
oc get clusterversion
oc get csv -A | grep <OPERATOR>
```

### ⚠️ Common Validation Mistakes to Avoid

- **❌ CRD Schema != Feature Deployed**: CRD may exist but controller doesn't implement new behavior
- **❌ Assuming Latest Code**: Test environments may run older builds
- **❌ Ignoring Downstream Lag**: Features merged upstream may take time to reach test environments
- **❌ Incomplete Testing**: Must test actual behavior, not just resource creation
- **❌ Missing Evidence**: Claims must be backed by concrete validation results

### 🎯 Framework Integration Points

**Before Test Generation:**
- Run deployment validation checklist
- Document evidence in metadata.json
- Include status in Complete-Analysis.md header

**During Test Generation:**
- Adjust test scenarios based on deployment status
- Include deployment-aware setup instructions  
- Provide alternative approaches for missing features

**After Test Generation:**
- Clearly communicate testing limitations
- Provide roadmap for future testing when features deploy
- Update framework learning based on validation accuracy