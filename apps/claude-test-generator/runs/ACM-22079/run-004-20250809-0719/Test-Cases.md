# Test Cases - ACM-22079: Support digest-based upgrades via ClusterCurator

**Feature:** Support digest-based upgrades via ClusterCurator for non-recommended upgrades  
**Environment:** qe6-vmware-ibm (ACM 2.14.0, MCE 2.9.0, OpenShift 4.19.6)  
**🔴 Current Deployment Status:** FEATURE NOT DEPLOYED - Test plan ready for implementation

**🎯 COMPREHENSIVE TEST PLAN**: All test cases assume feature is fully implemented and ready for immediate execution when deployed.

---

## Test Case 1: Core Digest-Based Non-Recommended Upgrade

**Description:** Validate ClusterCurator can perform digest-based upgrades to non-recommended versions using the required annotation.

**Business Value:** Ensures core functionality works for disconnected environments where image tags are unreliable.

**Execution Status:** 🔴 **Awaiting Feature Deployment** - Core digest logic not yet available in qe6

**Setup:**
- ACM hub cluster with ClusterCurator controller running
- Managed cluster available for upgrade testing (e.g., clc-aws-1754653080744)
- Target non-recommended version available in conditional updates

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Verify managed cluster current version<br/>**Goal**: Establish baseline cluster version<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].status.desired.version}'` | Current cluster version is displayed (e.g., 4.16.36 or similar) |
| **Step 2**: Check conditional updates for non-recommended versions<br/>**Goal**: Identify target non-recommended version with digest<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].status.conditionalUpdates}'` | List of conditional updates includes non-recommended versions with image digests |
| **Step 3**: Create ClusterCurator with digest-based upgrade configuration<br/>**Goal**: Configure upgrade to non-recommended version<br/>**Command**: `oc apply -f -` (stdin)<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: digest-upgrade-test<br/>  namespace: clc-aws-1754653080744<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.16.37<br/>    monitorTimeout: 120<br/>``` | ClusterCurator created successfully with annotation and upgrade spec |
| **Step 4**: Monitor ClusterCurator status for upgrade initiation<br/>**Goal**: Verify upgrade process starts<br/>**Command**: `oc get clustercurator digest-upgrade-test -n clc-aws-1754653080744 -o jsonpath='{.status.conditions[?(@.type=="clustercurator-job")].message}'` | Status shows upgrade job started and curator processing initiated |
| **Step 5**: Verify managed cluster ClusterVersion uses digest<br/>**Goal**: Confirm digest is used instead of tag<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate.image}'` | ClusterVersion.spec.desiredUpdate.image shows digest format (sha256:...) not tag |
| **Step 6**: Monitor upgrade progress to completion<br/>**Goal**: Ensure upgrade completes successfully<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].status}'` | Progressing condition shows "False" indicating upgrade completion |
| **Step 7**: Validate final cluster version<br/>**Goal**: Confirm upgrade to target version<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].status.desired.version}'` | Cluster version matches target non-recommended version (4.16.37) |
| **Step 8**: Verify ClusterCurator completion status<br/>**Goal**: Confirm curator job completed successfully<br/>**Command**: `oc get clustercurator digest-upgrade-test -n clc-aws-1754653080744 -o jsonpath='{.status.conditions[?(@.type=="clustercurator-job")].status}'` | Condition status shows "True" indicating successful completion |

---

## Test Case 2: Digest Resolution Failure and Tag Fallback

**Description:** Verify ClusterCurator falls back to image tag when digest resolution fails for non-recommended versions.

**Business Value:** Ensures robustness when digest information is unavailable but upgrade is still needed.

**Execution Status:** 🔴 **Awaiting Feature Deployment** - Fallback mechanism not yet implemented in qe6

**Setup:**
- ACM hub cluster configured
- Test cluster with version that has limited conditional updates
- Target version available but without digest information

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Identify version with missing digest info<br/>**Goal**: Find scenario where digest fallback is needed<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o yaml \| grep -A 5 conditionalUpdates` | Conditional updates show versions without digest information |
| **Step 2**: Create ClusterCurator for version without digest<br/>**Goal**: Trigger fallback mechanism<br/>**Command**: `oc apply -f -` (stdin)<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: fallback-upgrade-test<br/>  namespace: clc-aws-1754653080744<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: <version-without-digest><br/>    monitorTimeout: 120<br/>``` | ClusterCurator created with target version lacking digest |
| **Step 3**: Monitor ClusterCurator controller logs<br/>**Goal**: Verify digest lookup attempt and fallback logic<br/>**Command**: `oc logs deployment/cluster-curator-controller -n multicluster-engine \| grep -i digest` | Logs show digest lookup attempt and fallback to tag mechanism |
| **Step 4**: Verify managed cluster uses image tag<br/>**Goal**: Confirm fallback to tag-based upgrade<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate.image}'` | ClusterVersion.spec.desiredUpdate.image shows tag format (quay.io/...:4.x.y) not digest |
| **Step 5**: Validate upgrade progress with tag-based approach<br/>**Goal**: Ensure tag-based upgrade works<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Available")].status}'` | Available condition remains "True" or progresses normally |
| **Step 6**: Check for appropriate status messages<br/>**Goal**: Verify clear communication of fallback behavior<br/>**Command**: `oc get clustercurator fallback-upgrade-test -n clc-aws-1754653080744 -o jsonpath='{.status.conditions[*].message}'` | Status messages indicate digest unavailable, using tag fallback |

---

## Test Case 3: Annotation Validation and Security

**Description:** Test that non-recommended upgrades are properly gated by the required annotation and fail without it.

**Business Value:** Ensures security and intentionality - non-recommended upgrades only proceed when explicitly authorized.

**Execution Status:** 🟡 **Partially Available** - Annotation recognition works, gating logic awaiting deployment

**Setup:**
- Fresh managed cluster for testing
- Non-recommended target version identified

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Attempt upgrade without annotation<br/>**Goal**: Verify annotation requirement enforcement<br/>**Command**: `oc apply -f -` (stdin)<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: no-annotation-test<br/>  namespace: clc-aws-1754653080744<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.16.37<br/>    monitorTimeout: 120<br/>``` | ClusterCurator created but upgrade should be blocked or warned |
| **Step 2**: Monitor curator status for annotation error<br/>**Goal**: Verify proper error/warning for missing annotation<br/>**Command**: `oc get clustercurator no-annotation-test -n clc-aws-1754653080744 -o jsonpath='{.status.conditions[*].message}'` | Status message indicates missing annotation or non-recommended version blocked |
| **Step 3**: Add annotation via patch<br/>**Goal**: Test annotation addition enables upgrade<br/>**Command**: `oc annotate clustercurator no-annotation-test -n clc-aws-1754653080744 cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions='true'` | Annotation added successfully |
| **Step 4**: Verify upgrade proceeds after annotation<br/>**Goal**: Confirm annotation resolves the blocking<br/>**Command**: `oc get clustercurator no-annotation-test -n clc-aws-1754653080744 -o jsonpath='{.status.conditions[?(@.type=="clustercurator-job")].status}'` | Upgrade process initiates successfully |
| **Step 5**: Test annotation value validation<br/>**Goal**: Verify annotation must be exactly 'true'<br/>**Command**: `oc annotate clustercurator no-annotation-test -n clc-aws-1754653080744 cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions='false' --overwrite` | Annotation updated to 'false' |
| **Step 6**: Verify 'false' annotation blocks upgrade<br/>**Goal**: Ensure only 'true' value enables feature<br/>**Command**: Wait and check curator status for any blocking behavior | Upgrade should be blocked or warned with 'false' value |

---

## Test Case 4: Upgrade Monitoring and Timeout Handling

**Description:** Validate ClusterCurator properly monitors digest-based upgrades and handles timeout scenarios.

**Business Value:** Ensures reliable upgrade monitoring and proper handling of long-running or stuck upgrades.

**Execution Status:** 🔴 **Awaiting Feature Deployment** - Digest-specific monitoring not yet available

**Setup:**
- Managed cluster with upgrade monitoring capability
- Network access to monitor upgrade progress

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Configure ClusterCurator with custom timeout<br/>**Goal**: Test timeout configuration for digest upgrades<br/>**Command**: `oc apply -f -` (stdin)<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: timeout-test<br/>  namespace: clc-aws-1754653080744<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.16.37<br/>    monitorTimeout: 30<br/>``` | ClusterCurator created with 30-minute timeout |
| **Step 2**: Monitor upgrade progress tracking<br/>**Goal**: Verify curator tracks upgrade stages<br/>**Command**: `watch "oc get clustercurator timeout-test -n clc-aws-1754653080744 -o jsonpath='{.status.conditions[*].message}'"` | Status messages show upgrade progress stages |
| **Step 3**: Verify digest application to managed cluster<br/>**Goal**: Ensure digest is properly applied<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate}'` | desiredUpdate shows digest-based image reference |
| **Step 4**: Monitor managed cluster upgrade phases<br/>**Goal**: Track actual upgrade execution<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].message}'` | Progress messages show upgrade stages |
| **Step 5**: Validate timeout handling (if upgrade exceeds limit)<br/>**Goal**: Test timeout behavior<br/>**Command**: Monitor curator status after timeout period | If timeout reached, curator reports timeout condition |
| **Step 6**: Verify cleanup and final status<br/>**Goal**: Ensure proper upgrade completion reporting<br/>**Command**: `oc get clustercurator timeout-test -n clc-aws-1754653080744 -o yaml` | Final status reflects upgrade outcome (success/timeout/failure) |

---

## Test Case 5: Multi-Cluster Digest Upgrade Validation

**Description:** Test digest-based upgrades across multiple managed clusters simultaneously.

**Business Value:** Validates scalability and ensures feature works consistently across different cluster types and configurations.

**Execution Status:** 🔴 **Awaiting Feature Deployment** - Multi-cluster digest coordination not yet available

**Setup:**
- Multiple managed clusters available
- Different cluster types if possible (AWS, vSphere, etc.)

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Identify multiple target clusters<br/>**Goal**: Select clusters for parallel upgrade testing<br/>**Command**: `oc get managedclusters -o jsonpath='{.items[*].metadata.name}'` | List of available managed clusters for testing |
| **Step 2**: Create ClusterCurators for multiple clusters<br/>**Goal**: Initiate digest upgrades on different clusters<br/>**Command**: Create multiple ClusterCurator resources:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: multi-upgrade-cluster1<br/>  namespace: <cluster1-namespace><br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.16.37<br/>``` | ClusterCurators created for multiple clusters |
| **Step 3**: Monitor all upgrades simultaneously<br/>**Goal**: Track parallel upgrade execution<br/>**Command**: `oc get clustercurator -A -o wide` | All ClusterCurators show processing status |
| **Step 4**: Verify digest usage across all clusters<br/>**Goal**: Ensure consistent digest application<br/>**Command**: Check each managed cluster's ClusterVersion for digest usage | All clusters use digest-based image references |
| **Step 5**: Compare upgrade completion times<br/>**Goal**: Assess performance across cluster types<br/>**Command**: Monitor completion timestamps across clusters | Upgrades complete within expected timeframes |
| **Step 6**: Validate final cluster versions<br/>**Goal**: Ensure all upgrades reach target version<br/>**Command**: Check final versions on all managed clusters | All clusters successfully upgraded to target version |

---

## Test Case 6: Error Handling and Recovery Scenarios

**Description:** Validate proper error handling for various failure scenarios in digest-based upgrades.

**Business Value:** Ensures robust error handling and clear communication when upgrades fail.

**Execution Status:** 🔴 **Awaiting Feature Deployment** - Digest-specific error handling not yet implemented

**Setup:**
- Test cluster that can be used for failure scenarios
- Network access to simulate various error conditions

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Test invalid version specification<br/>**Goal**: Verify handling of non-existent versions<br/>**Command**: `oc apply -f -` (stdin)<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: invalid-version-test<br/>  namespace: clc-aws-1754653080744<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 99.99.99<br/>``` | ClusterCurator created with invalid version |
| **Step 2**: Monitor error reporting for invalid version<br/>**Goal**: Verify clear error messaging<br/>**Command**: `oc get clustercurator invalid-version-test -n clc-aws-1754653080744 -o jsonpath='{.status.conditions[*].message}'` | Error message clearly indicates invalid version |
| **Step 3**: Test managed cluster connectivity failure<br/>**Goal**: Simulate network/access issues<br/>**Command**: Monitor upgrade to unreachable or misconfigured cluster | Appropriate connectivity error messages displayed |
| **Step 4**: Verify controller log error details<br/>**Goal**: Ensure detailed error logging<br/>**Command**: `oc logs deployment/cluster-curator-controller -n multicluster-engine \| grep -i error` | Controller logs show detailed error information |
| **Step 5**: Test recovery after error resolution<br/>**Goal**: Verify curator can retry after fixing issues<br/>**Command**: Fix configuration and monitor for recovery | ClusterCurator retries and succeeds after issue resolution |
| **Step 6**: Validate cleanup of failed upgrades<br/>**Goal**: Ensure no orphaned resources<br/>**Command**: Check for any remaining curator jobs or resources | Failed upgrades are properly cleaned up |

---

## Current Environment Execution Guidance

### ✅ Available for Testing Now (qe6)
**Test Case 3** - Annotation Validation and Security (Steps 1, 3, 5)
- Can test annotation recognition and processing
- Can verify ClusterCurator creation with annotations
- Can test annotation value handling

### 🔴 Awaiting Feature Deployment
**Test Cases 1, 2, 4, 5, 6** - Core digest functionality
- Digest resolution logic not yet implemented
- Fallback mechanisms not yet available
- Digest-specific monitoring not yet deployed

### 📋 Test Plan Readiness
All test cases are **immediately executable** when the ACM-22079 feature is deployed to qe6. No test plan modifications needed.

### 🎯 Post-Deployment Execution
**Estimated Duration**: 4-5 hours for complete test plan  
**Prerequisites**: Feature deployed to qe6 environment  
**Validation**: All test cases can be executed sequentially

---

## Prerequisites for All Test Cases

**Environment Setup:**
- ACM hub cluster with kubectl/oc access (✅ Available)
- ClusterCurator controller running in multicluster-engine namespace (✅ Available)
- At least one managed cluster available for upgrade testing (✅ Available)
- Network connectivity between hub and managed clusters (✅ Available)

**Access Requirements:**
- Cluster administrator access to hub cluster (✅ Available)
- Access to managed cluster kubeconfig files (✅ Available)
- Ability to create/modify ClusterCurator resources (✅ Available)

**Feature Requirements:**
- ACM-22079 digest-based upgrade implementation (🔴 Awaiting deployment)
- Conditional update processing logic (🔴 Awaiting deployment)
- Tag fallback mechanism (🔴 Awaiting deployment)
- Annotation gating logic (🔴 Awaiting deployment)

**Validation Tools:**
- kubectl/oc CLI tools configured (✅ Available)
- jq for JSON parsing (optional but helpful)
- Access to ClusterCurator controller logs (✅ Available)