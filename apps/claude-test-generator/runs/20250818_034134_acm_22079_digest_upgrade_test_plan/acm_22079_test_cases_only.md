# ACM-22079 Digest-Based ClusterCurator Upgrade Test Cases

**JIRA**: [ACM-22079](https://issues.redhat.com/browse/ACM-22079)  
**Feature**: Support digest-based upgrades via ClusterCurator for non-recommended upgrades  
**Version Requirement**: ACM 2.15.0+  
**Component**: Cluster Lifecycle

---

## Test Case 1: Basic Digest-Based ClusterCurator Upgrade

**Description**: Validate ClusterCurator can perform successful digest-based cluster upgrade using image digest specification for enhanced disconnected environment support.

**Setup**: 
- Access to ACM environment with ClusterCurator functionality enabled
- Target managed cluster available for upgrade testing
- Required RBAC permissions for ClusterCurator operations
- Valid OpenShift release digest for target upgrade version

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | **Log into ACM Console** - Access ACM Console for ClusterCurator digest upgrade testing | Navigate to https://multicloud-console.apps.<cluster-host> | Login via CLI: `oc login https://api.<cluster-host>:6443 -u <username>` | Successful authentication and Console access to cluster management features |
| 2 | **Navigate to Cluster Management** - Access ClusterCurator automation section | Console → Infrastructure → Clusters → [target-cluster] → Actions | Access cluster resource: `oc get managedcluster <target-cluster> -o yaml` | Cluster management interface displayed with automation options available |
| 3 | **Create Digest-Based ClusterCurator** - Configure ClusterCurator with digest upgrade specification | Infrastructure → Automation → ClusterCurator → Create ClusterCurator | Create YAML file: `touch clustercurator-digest.yaml` and add:<br><pre>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: digest-upgrade-test<br>  namespace: target-cluster<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate:<br>      image: "quay.io/openshift-release-dev/ocp-release@sha256:5b54d0cd0ab6fc89da7d2becc4b2d086271691d3b6fd8d787527cd53403f8c35"<br>    channel: stable-4.19</pre> | ClusterCurator resource created with digest specification visible in Console automation section |
| 4 | **Apply ClusterCurator Configuration** - Submit digest-based upgrade configuration for processing | Click "Create" to submit ClusterCurator configuration | Apply configuration: `oc apply -f clustercurator-digest.yaml` | ClusterCurator resource successfully created and visible in cluster automation list |
| 5 | **Monitor Digest Processing** - Verify ClusterCurator processes digest specification correctly | Infrastructure → Clusters → [target-cluster] → Overview → Curator Jobs | Monitor job creation: `oc get jobs -n target-cluster \| grep curator` | ClusterCurator job created with digest-based upgrade configuration processing initiated |
| 6 | **Validate Upgrade Initiation** - Confirm cluster upgrade begins using digest specification | Monitor cluster status in Console Overview → Cluster Status | Check upgrade status: `oc get clusterversion -o jsonpath='{.status.conditions[?(@.type=="Progressing")].status}'` | Cluster upgrade initiated using digest specification with progress indicators active |
| 7 | **Verify Digest Resolution** - Ensure ClusterCurator resolved digest correctly for upgrade process | View cluster details → Settings → Version Information | Validate upgrade details: `oc get clustercurator digest-upgrade-test -n target-cluster -o yaml` | Digest resolved correctly with proper image reference and upgrade process proceeding |

---

## Test Case 2: Non-Recommended Digest Upgrade with Force Annotation

**Description**: Validate ClusterCurator handles digest-based upgrades to non-recommended versions using force annotation for critical enterprise scenarios.

**Setup**:
- ACM environment with ClusterCurator digest functionality
- Target managed cluster for non-recommended upgrade testing
- Valid digest for non-recommended OpenShift version
- Administrative privileges for force upgrade operations

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | **Log into ACM Console** - Access ACM Console for non-recommended digest upgrade testing | Navigate to https://multicloud-console.apps.<cluster-host> | Login via CLI: `oc login https://api.<cluster-host>:6443 -u <username>` | Successful authentication and Console access to advanced cluster management features |
| 2 | **Access Advanced Cluster Operations** - Navigate to ClusterCurator configuration with advanced options | Console → Infrastructure → Clusters → [target-cluster] → Actions → Advanced Options | Access cluster configuration: `oc get managedcluster <target-cluster> -o yaml` | Advanced cluster management options available including force upgrade capabilities |
| 3 | **Create Force Annotation ClusterCurator** - Configure ClusterCurator with non-recommended digest upgrade and force annotation | Infrastructure → Automation → ClusterCurator → Create ClusterCurator → Advanced Configuration | Create YAML file: `touch clustercurator-force-digest.yaml` and add:<br><pre>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: force-digest-upgrade<br>  namespace: target-cluster<br>  annotations:<br>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate:<br>      image: "quay.io/openshift-release-dev/ocp-release@sha256:example-digest-for-non-recommended"<br>    channel: stable-4.19<br>    force: true</pre> | ClusterCurator configured with force annotation and non-recommended digest specification |
| 4 | **Submit Force Upgrade Configuration** - Apply non-recommended digest upgrade with force annotation | Click "Create" with force upgrade acknowledgment | Apply configuration: `oc apply -f clustercurator-force-digest.yaml` | Force upgrade ClusterCurator created with non-recommended digest configuration accepted |
| 5 | **Monitor Force Upgrade Processing** - Verify ClusterCurator processes force annotation and digest correctly | Infrastructure → Clusters → [target-cluster] → Overview → Curator Jobs (Force Upgrade) | Monitor force upgrade job: `oc get jobs -n target-cluster \| grep curator` and `oc describe clustercurator force-digest-upgrade -n target-cluster` | Force upgrade job initiated with digest processing and annotation validation complete |
| 6 | **Validate Non-Recommended Override** - Confirm upgrade proceeds despite non-recommended version status | Monitor upgrade progress with force indicator in Console | Check upgrade override status: `oc get clustercurator force-digest-upgrade -n target-cluster -o jsonpath='{.status.conditions[?(@.type=="UpgradeStarted")].reason}'` | Non-recommended upgrade proceeding with force annotation override and digest resolution successful |
| 7 | **Verify Force Upgrade Completion** - Ensure digest-based non-recommended upgrade completes successfully | View cluster status → Version Information → Upgrade History | Validate final status: `oc get clusterversion -o jsonpath='{.status.history[0].image}'` | Non-recommended digest upgrade completed successfully with proper image digest recorded |

---

## Test Case 3: Digest Fallback to Image Tag Behavior

**Description**: Validate ClusterCurator gracefully falls back to image tag method when digest resolution fails, ensuring backward compatibility.

**Setup**:
- ACM environment with ClusterCurator digest functionality
- Target managed cluster for fallback testing
- Network conditions simulating digest resolution failures
- Valid image tag specifications for fallback testing

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | **Log into ACM Console** - Access ACM Console for digest fallback testing | Navigate to https://multicloud-console.apps.<cluster-host> | Login via CLI: `oc login https://api.<cluster-host>:6443 -u <username>` | Successful authentication and Console access to ClusterCurator fallback testing |
| 2 | **Configure Digest Unavailable Scenario** - Set up ClusterCurator with digest that triggers fallback mechanism | Console → Infrastructure → Automation → ClusterCurator → Create | Prepare cluster state: `oc get clusterversion -o yaml \| grep -A 5 availableUpdates` | Cluster state prepared for digest fallback testing with controlled conditions |
| 3 | **Create Mixed Upgrade Configuration** - Configure ClusterCurator with both digest and version specifications | Infrastructure → Automation → ClusterCurator → Create ClusterCurator | Create YAML file: `touch clustercurator-fallback.yaml` and add:<br><pre>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: fallback-test-upgrade<br>  namespace: target-cluster<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate:<br>      version: "4.19.8"<br>      image: "invalid-digest-specification"<br>    channel: stable-4.19</pre> | ClusterCurator configured with invalid digest and valid version for fallback testing |
| 4 | **Apply Fallback Configuration** - Submit mixed configuration to trigger fallback behavior | Click "Create" to submit fallback test configuration | Apply configuration: `oc apply -f clustercurator-fallback.yaml` | ClusterCurator created with mixed specification ready for fallback processing |
| 5 | **Monitor Fallback Processing** - Observe ClusterCurator digest resolution failure and image tag fallback | Infrastructure → Clusters → [target-cluster] → Overview → Curator Jobs | Monitor fallback behavior: `oc logs deployment/cluster-curator-controller -n multicluster-engine --tail=20 \| grep fallback` | Digest resolution attempted, failed gracefully, and fallback to image tag initiated |
| 6 | **Verify Image Tag Usage** - Confirm upgrade proceeds using image tag method after digest failure | Monitor cluster upgrade progress in Console → Cluster Status | Validate fallback success: `oc get clustercurator fallback-test-upgrade -n target-cluster -o yaml \| grep -A 5 status` | Upgrade proceeding successfully using image tag method with fallback behavior documented |
| 7 | **Validate Backward Compatibility** - Ensure fallback maintains existing ClusterCurator functionality | View cluster details → Settings → Upgrade History | Check upgrade method: `oc get clusterversion -o jsonpath='{.status.desired.version}'` | Backward compatibility maintained with successful upgrade completion using image tag fallback |

---

## Test Case 4: Digest Upgrade Error Handling and Validation

**Description**: Validate ClusterCurator provides comprehensive error handling for invalid digest specifications and network connectivity issues.

**Setup**:
- ACM environment with ClusterCurator digest functionality
- Target managed cluster for error scenario testing
- Network simulation capabilities for connectivity testing
- Invalid digest specifications for validation testing

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | **Log into ACM Console** - Access ACM Console for digest error handling testing | Navigate to https://multicloud-console.apps.<cluster-host> | Login via CLI: `oc login https://api.<cluster-host>:6443 -u <username>` | Successful authentication and Console access to ClusterCurator error testing capabilities |
| 2 | **Prepare Error Scenario Testing** - Set up invalid digest specifications for validation testing | Console → Infrastructure → Automation → ClusterCurator | Prepare test scenarios: `oc get clusterversion -o yaml \| grep -A 10 conditionalUpdates` | Test environment prepared for comprehensive digest error validation scenarios |
| 3 | **Create Invalid Digest Configuration** - Configure ClusterCurator with intentionally invalid digest specification | Infrastructure → Automation → ClusterCurator → Create ClusterCurator | Create YAML file: `touch clustercurator-error-test.yaml` and add:<br><pre>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: error-handling-test<br>  namespace: target-cluster<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate:<br>      image: "quay.io/invalid/digest@sha256:invalid-digest-hash"<br>    channel: stable-4.19</pre> | ClusterCurator configured with invalid digest for comprehensive error handling validation |
| 4 | **Submit Invalid Configuration** - Apply invalid digest configuration to test error handling | Click "Create" and observe error validation | Apply configuration: `oc apply -f clustercurator-error-test.yaml` | ClusterCurator created with invalid configuration ready for error handling testing |
| 5 | **Monitor Error Detection** - Observe ClusterCurator error detection and validation processes | Infrastructure → Clusters → [target-cluster] → Overview → Curator Jobs | Monitor error handling: `oc describe clustercurator error-handling-test -n target-cluster` and `oc get events -n target-cluster --sort-by=.lastTimestamp` | Error detection active with comprehensive validation messages and proper error classification |
| 6 | **Verify Error Messaging** - Confirm clear error messages provided for digest validation failures | View error details in Console → Cluster Details → Events | Check error details: `oc get clustercurator error-handling-test -n target-cluster -o jsonpath='{.status.conditions[?(@.type=="UpgradeFailed")].message}'` | Clear error messages provided indicating digest validation failure with specific error details |
| 7 | **Validate Error Recovery** - Ensure ClusterCurator maintains stable state after error scenarios | Monitor cluster status stability in Console | Verify system stability: `oc get clustercurator -n target-cluster` and `oc get managedcluster target-cluster -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'` | System remains stable after error scenarios with proper cleanup and maintained cluster health |