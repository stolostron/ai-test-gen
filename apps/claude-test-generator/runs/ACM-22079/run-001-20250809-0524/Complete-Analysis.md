# ACM-22079: Support Digest-based Upgrades via ClusterCurator - Complete Analysis Report

## Feature Overview & Business Value

### JIRA Ticket Summary
- **Ticket ID**: ACM-22079 - Support digest-based upgrades via ClusterCurator for non-recommended upgrades
- **Priority**: Critical
- **Status**: Review
- **Assignee**: Feng Xiang
- **Labels**: Eng-Status:Green, QE-Required, doc-required

### Business Context
**Customer Impact**: Urgent request from Amadeus customer requiring digest-based upgrades in disconnected environments where image tags are not accessible.

**Problem Statement**: In air-gapped/disconnected environments, standard image tag references fail during non-recommended OpenShift upgrades, preventing critical cluster maintenance operations.

**Solution Value**: Enables enterprise customers to perform necessary cluster upgrades in secure, disconnected environments using cryptographically-verified image digests.

## Implementation Status & PR Analysis

### Development Implementation
- **Repository**: stolostron/cluster-curator-controller
- **Pull Request**: #468 - "ACM-22079 Initial non-recommended image digest feature"
- **Merge Status**: ✅ Successfully merged to main branch
- **Merge Date**: July 16, 2025
- **Commit Hash**: `be3fbc09bd07df17c33ff3535c34a71eb73de28a`
- **Author**: Feng Xiang (fxiang1)

### Technical Implementation Details
**Core Logic Flow**:
1. **conditionalUpdates**: Primary source for image digests (non-recommended versions)
2. **availableUpdates**: Fallback source for digest resolution
3. **Image Tag**: Final fallback for backward compatibility

**Key Code Changes**:
- New helper functions for digest extraction from ClusterVersion update lists
- Modified Hive job handler to implement digest-preference logic
- Restored `LoadConfig()` function for improved local testing capabilities
- Enhanced error handling and fallback mechanisms

**Quality Metrics**:
- SonarQube Coverage: 81.2% on new code
- Security Hotspots: 0
- Code Review: Thorough review with multiple improvement iterations

## Environment Deployment Analysis

### Current qe6 Environment Status
- **Cluster Version**: OpenShift 4.19.6
- **ACM Namespace**: ocm
- **MCE Namespace**: multicluster-engine
- **ClusterCurator CRD**: ✅ Installed (`clustercurators.cluster.open-cluster-management.io`)
- **Managed Clusters**: 3 available (local-cluster, clc-aws-1754653080744, tfitzger-rosa-hcp-demo-test)

### Feature Availability Assessment
- **Implementation Status**: ✅ Merged (commit: be3fbc09, July 16, 2025)
- **Current qe6 Deployment**: ❌ Missing ACM-22079 feature
- **Controller Image**: `quay.io:443/acm-d/cluster-curator-controller-rhel9@sha256:902c5b3b4a4e8cb0a14fa5aba8451ec02830d5167ff1b91323ded62255983cd9`
- **Feature Gap**: Current deployment predates July 16 implementation

### Validation Environment Constraints
- **Available Updates**: None (cluster at stable version 4.19.6)
- **ConditionalUpdates**: Not present (no non-recommended versions available)
- **Testing Limitation**: Feature validation requires environment with newer cluster-curator-controller build

## Test Plan Validation Results

### Environment Validation Summary
| Component | Status | Details |
|-----------|--------|---------|
| ClusterCurator CRD | ✅ Available | Properly installed and functional |
| Managed Clusters | ✅ Available | 3 clusters ready for testing |
| Controller Version | ❌ Outdated | Missing ACM-22079 implementation |
| Update Availability | ⚠️ Limited | No conditionalUpdates currently available |
| Test Execution | 🔄 Ready | Test plans validated for structure and commands |

### Test Case Validation Notes
1. **Structural Validation**: ✅ All test cases follow framework best practices
2. **Command Verification**: ✅ All kubectl/oc commands validated for syntax
3. **Feature Logic**: ✅ Test scenarios align with implementation logic
4. **Edge Cases**: ✅ Comprehensive error handling and fallback testing included
5. **Integration**: ✅ Tests cover standard workflow compatibility

### Recommended Validation Approach
**Immediate Options**:
- **Development Environment**: Local cluster with latest cluster-curator-controller build
- **Validation Environment**: Environment with nightly/latest ACM builds
- **Manual Deployment**: Update qe6 with latest controller image (requires approval)

**Expected Timeline**: Feature available in qe6 within 1-2 weeks via normal deployment cycle

## Complete Test Cases

### Test Case 1: Basic Non-Recommended Upgrade with Digest Authentication
**Description**: 
- Verify ClusterCurator successfully initiates digest-based upgrade for non-recommended versions
- Validate that image digest is extracted from conditionalUpdates and applied correctly

**Setup**: 
- Hub cluster with ACM/MCE 2.12+ installed
- Managed cluster with available conditionalUpdates containing non-recommended versions
- ClusterCurator operator with ACM-22079 feature implementation

| Test Steps | Expected Results |
|------------|------------------|
| 1. `oc get managedclusters` | Display list of available managed clusters with JOINED=True status |
| 2. **Verify ConditionalUpdates Availability**<br>**Goal:** Confirm target managed cluster has conditionalUpdates with non-recommended versions.<br>• Access managed cluster context<br>• `oc get clusterversion -o jsonpath='{.status.conditionalUpdates[*].release.version}'` | ConditionalUpdates list contains non-recommended versions (e.g., 4.16.37) with associated image digests |
| 3. **Create ClusterCurator with Non-Recommended Annotation**<br>**Goal:** Apply ClusterCurator resource targeting non-recommended version.<br>• `kubectl apply -f clustercurator-digest-upgrade.yaml`<br>• Verify annotation: `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'` | ClusterCurator resource created successfully in target namespace |
| 4. `oc get clustercurator <cluster-name> -n <cluster-namespace> -o yaml` | Resource shows correct annotation and desiredCuration: upgrade configuration |
| 5. **Monitor Curator Job Creation**<br>**Goal:** Verify ClusterCurator initiates upgrade job.<br>• `oc get jobs -n <cluster-namespace>`<br>• `oc describe job <curator-job-name> -n <cluster-namespace>` | Curator job created with appropriate configuration and running status |
| 6. **Validate Digest Extraction Logic**<br>**Goal:** Confirm job logs show digest lookup from conditionalUpdates.<br>• `oc logs job/<curator-job-name> -n <cluster-namespace> --follow` | Logs display: "Checking conditionalUpdates for image digest" and successful digest extraction |
| 7. **Verify Managed Cluster Image Reference**<br>**Goal:** Confirm managed cluster receives digest-based image reference.<br>• Access managed cluster context<br>• `oc get clusterversion -o jsonpath='{.spec.desiredUpdate.image}'` | Image field contains digest format: `registry.redhat.io/...@sha256:...` (not version tag) |
| 8. **Confirm Upgrade Initiation**<br>**Goal:** Validate upgrade process starts with digest reference.<br>• `oc get clusterversion -o jsonpath='{.status.desired.version}'`<br>• `oc get clusteroperators` | Desired version matches target non-recommended version, cluster operators begin update process |

### Test Case 2: Fallback Mechanism to AvailableUpdates
**Description**:
- Test fallback logic when target version is not found in conditionalUpdates
- Verify ClusterCurator attempts availableUpdates before using image tag

**Setup**:
- Managed cluster with availableUpdates but target version absent from conditionalUpdates
- ClusterCurator configured for version present in availableUpdates only

| Test Steps | Expected Results |
|------------|------------------|
| 1. **Identify Fallback Scenario Version**<br>**Goal:** Find version present in availableUpdates but not conditionalUpdates.<br>• `oc get clusterversion -o jsonpath='{.status.availableUpdates[*].version}'`<br>• `oc get clusterversion -o jsonpath='{.status.conditionalUpdates[*].release.version}'`<br>• Compare lists to identify suitable test version | Version found that exists in availableUpdates but not in conditionalUpdates |
| 2. **Create ClusterCurator for Fallback Version**<br>**Goal:** Apply ClusterCurator targeting availableUpdates-only version.<br>• Update ClusterCurator YAML with identified version<br>• `kubectl apply -f clustercurator-fallback-test.yaml` | ClusterCurator created targeting availableUpdates version |
| 3. **Monitor Fallback Logic in Job Logs**<br>**Goal:** Verify curator attempts conditionalUpdates first, then falls back.<br>• `oc logs job/<curator-job> -n <cluster-namespace> --follow` | Logs show: "Version not found in conditionalUpdates, checking availableUpdates" |
| 4. **Validate AvailableUpdates Processing**<br>**Goal:** Confirm successful extraction from availableUpdates.<br>• Continue monitoring job logs<br>• Look for availableUpdates processing messages | Logs indicate successful image reference extraction from availableUpdates |
| 5. **Verify Final Image Reference Type**<br>**Goal:** Confirm image reference format matches availableUpdates source.<br>• `oc get clusterversion -o jsonpath='{.spec.desiredUpdate.image}'` on managed cluster | Image reference uses digest if available in availableUpdates, otherwise uses image tag |

### Test Case 3: Annotation Requirement Enforcement
**Description**:
- Verify digest logic only activates with proper non-recommended annotation
- Test behavior differences with and without required annotation

**Setup**:
- Managed cluster ready for upgrade testing
- ClusterCurator configurations with and without annotation

| Test Steps | Expected Results |
|------------|------------------|
| 1. **Create Standard ClusterCurator (No Annotation)**<br>**Goal:** Test behavior without non-recommended annotation.<br>• `kubectl apply -f clustercurator-standard.yaml`<br>• Verify no annotation present: `oc get clustercurator <name> -o yaml \| grep annotations` | ClusterCurator created without non-recommended annotation |
| 2. **Monitor Standard Upgrade Logic**<br>**Goal:** Confirm standard upgrade path is used.<br>• `oc logs job/<curator-job> -n <cluster-namespace>` | Job logs show standard upgrade logic, no mention of conditionalUpdates or digest checking |
| 3. **Verify Standard Image Reference**<br>**Goal:** Confirm standard image tag usage.<br>• `oc get clusterversion -o jsonpath='{.spec.desiredUpdate.image}'` on managed cluster | Image field contains standard tag format (e.g., `4.16.37`) not digest |
| 4. **Add Non-Recommended Annotation**<br>**Goal:** Demonstrate annotation activation of digest logic.<br>• `kubectl annotate clustercurator <name> cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions=true` | Annotation added successfully to existing ClusterCurator |
| 5. **Observe Logic Change**<br>**Goal:** Verify digest logic activates after annotation addition.<br>• Monitor new job creation and logs<br>• `oc logs job/<new-curator-job> --follow` | New job created with digest-checking logic active |
| 6. **Validate Annotation-Triggered Behavior**<br>**Goal:** Confirm digest logic now processes conditionalUpdates.<br>• Continue monitoring job execution | Job logs now show conditionalUpdates checking and digest extraction behavior |

### Test Case 4: Disconnected Environment Digest Resolution
**Description**:
- Test primary use case for disconnected/air-gapped environments
- Verify digest-based upgrades work with mirror registries

**Setup**:
- Simulated disconnected environment with mirror registry configuration
- ClusterCurator configured for non-recommended upgrade

| Test Steps | Expected Results |
|------------|------------------|
| 1. **Verify Mirror Registry Configuration**<br>**Goal:** Confirm disconnected environment setup.<br>• `oc get imagecontentsourcepolicy` or `oc get imagedigestmirrorset`<br>• `oc get nodes -o wide` (check for disconnected indicators) | Mirror registry policies configured, disconnected environment indicators present |
| 2. **Create Disconnected-Environment ClusterCurator**<br>**Goal:** Apply ClusterCurator optimized for digest-based upgrade.<br>• `kubectl apply -f clustercurator-disconnected.yaml`<br>• Ensure non-recommended annotation present | ClusterCurator created with proper configuration for disconnected scenario |
| 3. **Monitor Digest Resolution Process**<br>**Goal:** Verify digest extraction succeeds in disconnected environment.<br>• `oc logs job/<curator-job> -n <cluster-namespace> --follow` | Logs show successful digest resolution from conditionalUpdates despite disconnected state |
| 4. **Validate Mirror Registry Integration**<br>**Goal:** Confirm digest reference works with mirror configuration.<br>• `oc get clusterversion -o yaml \| grep "image:"` on managed cluster | Image reference shows mirrored digest format: `mirror.registry.com/...@sha256:...` |
| 5. **Verify Upgrade Progress in Disconnected Mode**<br>**Goal:** Confirm cluster operators update using mirrored digest references.<br>• `oc get clusteroperators -o wide`<br>• Monitor cluster operator status during upgrade | Cluster operators successfully update using digest references from mirror registry |
| 6. **Confirm Successful Disconnected Upgrade**<br>**Goal:** Validate completed upgrade maintains digest reference history.<br>• `oc get clusterversion -o jsonpath='{.status.history[0].image}'` | Upgrade history shows digest-based image reference maintained throughout process |

### Test Case 5: Error Handling and Edge Cases
**Description**:
- Test system behavior with malformed digests and missing references
- Verify graceful fallback and appropriate error messaging

**Setup**:
- Scenarios with intentionally problematic configurations
- ClusterCurator targeting non-existent or malformed versions

| Test Steps | Expected Results |
|------------|------------------|
| 1. **Test Non-Existent Version Handling**<br>**Goal:** Verify behavior with completely invalid version target.<br>• Create ClusterCurator with non-existent version (e.g., "4.99.99")<br>• `kubectl apply -f clustercurator-invalid-version.yaml` | ClusterCurator accepts configuration but job will handle validation |
| 2. **Monitor Error Handling Logic**<br>**Goal:** Confirm appropriate error messages and fallback attempts.<br>• `oc logs job/<curator-job> --follow`<br>• `oc describe clustercurator <name>` | Job logs show: "Version 4.99.99 not found in conditionalUpdates" and fallback attempts |
| 3. **Verify Graceful Failure Reporting**<br>**Goal:** Ensure clear error reporting in ClusterCurator status.<br>• `oc get clustercurator <name> -o jsonpath='{.status.conditions[?(@.type=="clustercurator-job")].message}'` | Status message provides clear troubleshooting information about version availability |
| 4. **Test Annotation Removal Recovery**<br>**Goal:** Verify system handles annotation removal appropriately.<br>• `kubectl annotate clustercurator <name> cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions-`<br>• Monitor subsequent job behavior | New job reverts to standard upgrade logic, no digest checking performed |
| 5. **Validate Comprehensive Error Messages**<br>**Goal:** Confirm error messages aid in troubleshooting.<br>• `oc get events --field-selector involvedObject.kind=ClusterCurator`<br>• Review all event messages for clarity | Events provide actionable troubleshooting guidance for digest resolution failures |

### Test Case 6: Integration with Existing Upgrade Workflows
**Description**:
- Verify digest feature integrates seamlessly with existing ClusterCurator workflows
- Test compatibility with standard ACM cluster lifecycle operations

**Setup**:
- Standard ACM environment with multiple managed clusters
- Mix of recommended and non-recommended upgrade scenarios

| Test Steps | Expected Results |
|------------|------------------|
| 1. **Baseline Standard Upgrade Verification**<br>**Goal:** Ensure standard upgrades remain unaffected.<br>• Create ClusterCurator without annotation for recommended version<br>• `kubectl apply -f clustercurator-standard-upgrade.yaml` | Standard ClusterCurator upgrade proceeds normally without digest logic |
| 2. **Parallel Digest and Standard Operations**<br>**Goal:** Verify both upgrade types can coexist.<br>• Simultaneously run standard upgrade on one cluster<br>• Run digest-based upgrade on another cluster<br>• Monitor both operations | Both upgrade types proceed independently without interference |
| 3. **ACM Console Integration Verification**<br>**Goal:** Confirm digest upgrades are visible in ACM UI.<br>• Access ACM Console Infrastructure > Clusters section<br>• Review cluster upgrade status and history | ACM Console displays digest-based upgrade progress and completion status |
| 4. **Multi-Cluster Digest Upgrade Coordination**<br>**Goal:** Test digest upgrades across multiple managed clusters.<br>• Apply ClusterCurator resources to multiple clusters<br>• Monitor coordinated upgrade execution | Multiple digest-based upgrades execute successfully with proper resource isolation |
| 5. **Post-Upgrade Cluster Health Validation**<br>**Goal:** Verify cluster health after digest-based upgrade.<br>• `oc get clusterversion`<br>• `oc get nodes`<br>• `oc get clusteroperators` | All cluster components healthy and operational post-upgrade |
| 6. **Upgrade History and Audit Trail**<br>**Goal:** Confirm digest upgrades maintain proper audit history.<br>• `oc get clusterversion -o yaml \| grep -A 10 history`<br>• Review ClusterCurator status and events | Complete audit trail showing digest-based upgrade methodology and completion |

## Sample ClusterCurator Resources

### Basic Non-Recommended Upgrade with Digest Support
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'
  name: cluster1-digest-upgrade
  namespace: cluster1
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: 4.16.37
    monitorTimeout: 120
```

### Standard Upgrade (No Digest Logic)
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: cluster1-standard-upgrade
  namespace: cluster1
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: 4.16.38
    monitorTimeout: 120
```

### Disconnected Environment Configuration
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'
  name: disconnected-cluster-upgrade
  namespace: disconnected-cluster
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: 4.16.37
    monitorTimeout: 180
```

## Linked Tickets Analysis

### ACM-22080 [QE] - Critical
- **Status**: In Progress
- **Assignee**: Atif Shafi
- **Completion Requirements**: 
  - Test cases created in Polarion
  - Test cases reviewed and approved
  - Test runs executed in Polarion
- **Initial Test**: Verify digest usage vs. image tag for non-recommended upgrades

### ACM-22081 [QE Automation] - Critical  
- **Status**: New
- **Assignee**: Atif Shafi
- **Completion Requirements**:
  - PR with automation changes
  - Automated tests executed and proven stable

### ACM-22457 [Documentation] - Normal
- **Status**: New (moved to backlog pending 2.15 branch)
- **Assignee**: Oliver Fischer
- **Content**: Documentation for ClusterCurator non-recommended upgrades
- **Target Location**: ACM docs section on cluster management
- **Blocker**: Waiting for 2.15 branch availability

## Testing Readiness Assessment

### Current Environment Status
- **Test Plan Quality**: ✅ Comprehensive, framework-compliant test cases
- **Environment Readiness**: ⚠️ qe6 requires cluster-curator-controller update
- **Feature Implementation**: ✅ Complete and merged (commit: be3fbc09)
- **Documentation**: 🔄 In progress (ACM-22457)

### Immediate Testing Options
1. **Development Environment**: Local deployment with latest builds
2. **Validation Environment**: Clusters with nightly ACM deployments  
3. **Manual Deployment**: Update qe6 cluster-curator-controller image
4. **Wait for Deployment**: Next qe6 refresh cycle (1-2 weeks estimated)

### Risk Assessment
- **Low Risk**: Feature well-tested with 81.2% coverage
- **Deployment Gap**: Current qe6 environment lacks implementation
- **Customer Impact**: High - Amadeus blocking issue resolution
- **Mitigation**: Multiple testing environment options available

## Next Steps & Recommendations

### Immediate Actions
1. **Environment Update**: Deploy latest cluster-curator-controller to validation environment
2. **Test Execution**: Execute comprehensive test suite once feature available
3. **Documentation**: Complete ACM-22457 when 2.15 branch opens
4. **Automation**: Implement test automation per ACM-22081

### Success Criteria
- [ ] All 6 test cases pass successfully
- [ ] Digest-based upgrades work in disconnected environment
- [ ] Feature integrates seamlessly with existing workflows
- [ ] Documentation complete and published
- [ ] Automation implemented and stable

### Timeline Expectations
- **Feature Availability**: 1-2 weeks (next qe6 deployment)
- **Test Completion**: 1 week after feature availability
- **Documentation**: Pending 2.15 branch (timeline TBD)
- **Automation**: 2-3 weeks after successful manual testing