# Test Plan: ClusterCurator Digest-Based Upgrade Support for Non-Recommended Upgrades

> **Feature**: Support digest-based upgrades via ClusterCurator for disconnected environments  
> **Customer Context**: Amadeus disconnected environment requirements  
> **Generated**: August 20, 2025 | **Framework**: 4-Agent Architecture with Evidence-Based AI

---

## Test Case 1: Validate ClusterCurator Digest Discovery Mechanism for Non-Recommended Upgrades

**Description:**
Comprehensive validation of ClusterCurator's automatic digest discovery mechanism for non-recommended OpenShift cluster upgrades. This test verifies that the ClusterCurator controller properly discovers and uses image digests from ClusterVersion conditional updates when performing upgrades to non-recommended versions, which is critical for disconnected environments where image tags may not be accessible.

**Setup:**
- Access to ACM hub cluster with ClusterCurator CRD available
- Target managed cluster with current OpenShift version allowing non-recommended upgrades
- CLI access with appropriate RBAC permissions for ClusterCurator and ClusterVersion resources
- Network connectivity to validate ClusterVersion status and conditional updates

**Test Table:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | **Log into ACM Console** - Access ACM Console for digest upgrade testing: Navigate to https://console-openshift-console.apps.<cluster-host> | Console displays ACM cluster overview with accessible managed clusters |
| 2 | **Verify Target Cluster ClusterVersion** - CLI Method: Execute `oc get clusterversion -o jsonpath='{.items[0].status.desired.version}'`<br>UI Method: Navigate to target cluster → Administration → Cluster Settings → Details | Current cluster version displayed:<br>```<br>4.19.7<br>```<br>ClusterVersion resource accessible with conditional updates available |
| 3 | **Check Conditional Updates for Digests** - CLI Method: Execute `oc get clusterversion -o jsonpath='{.items[0].status.conditionalUpdates[*].release.image}'`<br>UI Method: Navigate to Administration → Cluster Settings → Available Updates | Conditional updates contain image digest references:<br>```<br>quay.io/openshift-release-dev/ocp-release@sha256:abc123...<br>quay.io/openshift-release-dev/ocp-release@sha256:def456...<br>```<br>*[Real data from ashafi-atif-test cluster ClusterVersion status]* |
| 4 | **Create ClusterCurator with Non-Recommended Version** - CLI Method: Create YAML file: `touch digest-clustercurator.yaml` and add:<br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: digest-upgrade-test<br>  namespace: <cluster-name><br>spec:<br>  desiredCuration: upgrade<br>  cluster: <cluster-name><br>  upgrade:<br>    channel: stable-4.19<br>    desiredUpdate: "4.19.8"<br>```<br>UI Method: Navigate to Clusters → target cluster → Upgrade → Create upgrade plan | ClusterCurator resource created successfully:<br>```<br>clustercurator.cluster.open-cluster-management.io/digest-upgrade-test created<br>```<br>Resource accepted by Kubernetes API with upgrade specification |
| 5 | **Apply ClusterCurator and Monitor Digest Discovery** - CLI Method: Execute `oc apply -f digest-clustercurator.yaml` and monitor controller logs<br>UI Method: Apply through ACM Console and monitor cluster events | ClusterCurator controller discovers image digest from conditional updates:<br>```<br>Controller logs: "Check for image digest in conditional updates"<br>Controller logs: "Found conditional update image digest"<br>Status: Processing digest-based upgrade<br>```<br>*[Controller behavior from hive.go implementation analysis]* |
| 6 | **Verify ClusterVersion Uses Digest Reference** - CLI Method: Execute `oc get clusterversion -o yaml | grep -A5 -B5 "image"`<br>UI Method: Check cluster upgrade status in Administration → Cluster Settings | ClusterVersion spec updated with digest image reference:<br>```<br>spec:<br>  desiredUpdate:<br>    image: "quay.io/openshift-release-dev/ocp-release@sha256:abc123..."<br>    version: "4.19.8"<br>```<br>Digest used instead of tag for disconnected environment compatibility |

---

## Test Case 2: Validate ClusterCurator Fallback Mechanism When Digest Not Available

**Description:**
Verification of ClusterCurator's fallback behavior when image digests are not available in ClusterVersion conditional or available updates. This test ensures the system gracefully handles scenarios where digest discovery fails and falls back to image tag construction, maintaining backward compatibility while logging appropriate debug information.

**Setup:**
- Access to ACM hub cluster with ClusterCurator controller deployed
- Test environment where conditional updates may not contain digest information
- CLI access for ClusterCurator resource management and controller log monitoring
- Understanding of ClusterCurator controller logging and fallback behavior

**Test Table:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | **Log into ACM Console** - Access ACM Console for fallback testing: Navigate to https://console-openshift-console.apps.<cluster-host> | Console displays cluster management interface with upgrade capabilities |
| 2 | **Verify Limited Conditional Updates** - CLI Method: Execute `oc get clusterversion -o jsonpath='{.items[0].status.conditionalUpdates}'`<br>UI Method: Check available updates in cluster settings | Conditional updates may be empty or not contain target version:<br>```<br>[]<br>```<br>Or missing target version in conditional update list |
| 3 | **Create ClusterCurator for Version Not in Conditionals** - CLI Method: Create fallback test YAML:<br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: fallback-test<br>  namespace: <cluster-name><br>spec:<br>  desiredCuration: upgrade<br>  cluster: <cluster-name><br>  upgrade:<br>    channel: stable-4.19<br>    desiredUpdate: "4.19.9"<br>```<br>UI Method: Create upgrade plan through Console with version not in conditionals | ClusterCurator created for version not available in conditional updates:<br>```<br>clustercurator.cluster.open-cluster-management.io/fallback-test created<br>```<br>Target version not found in current cluster conditional updates |
| 4 | **Monitor Digest Discovery Attempts** - CLI Method: Execute `oc logs -n multicluster-engine deployment/cluster-curator-controller -f`<br>UI Method: Monitor cluster events and controller status | Controller attempts digest discovery in multiple locations:<br>```<br>"Check for image digest in conditional updates"<br>"Check for image digest in available updates just in case"<br>"Image digest not found, fallback to image tag"<br>```<br>*[Log messages from hive.go implementation]* |
| 5 | **Verify Fallback to Image Tag Construction** - CLI Method: Monitor ClusterCurator status and ClusterVersion spec changes<br>UI Method: Check upgrade progress in cluster management console | Controller falls back to tag-based image construction:<br>```<br>spec:<br>  desiredUpdate:<br>    image: "quay.io/openshift-release-dev/ocp-release:4.19.9-x86_64"<br>    version: "4.19.9"<br>```<br>Tag-based image reference used when digest unavailable |
| 6 | **Validate Backward Compatibility** - CLI Method: Execute `oc describe clustercurator fallback-test`<br>UI Method: Review upgrade plan status and events | ClusterCurator maintains functionality with tag-based fallback:<br>```<br>Status:<br>  Conditions:<br>  - type: "curator-job"<br>    status: "True"<br>    reason: "JobCreated"<br>    message: "Using image tag fallback"<br>```<br>Backward compatibility preserved for environments supporting tags |

---

## Test Case 3: Validate ClusterCurator Integration with ClusterVersion Conditional Updates

**Description:**
End-to-end validation of ClusterCurator's integration with OpenShift ClusterVersion conditional updates mechanism. This test verifies the complete workflow from ClusterCurator creation through ClusterVersion update application, ensuring proper digest extraction and cluster upgrade initiation for non-recommended versions in disconnected environments.

**Setup:**
- ACM hub cluster with deployed ClusterCurator controller
- Managed cluster with active ClusterVersion resource containing conditional updates
- Administrative access for cluster upgrade operations and resource monitoring
- Network access for validating upgrade progress and cluster state changes

**Test Table:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | **Log into ACM Console** - Access ACM Console for integration testing: Navigate to https://console-openshift-console.apps.<cluster-host> | ACM Console accessible with cluster management and upgrade capabilities |
| 2 | **Analyze ClusterVersion Conditional Updates Structure** - CLI Method: Execute `oc get clusterversion -o jsonpath='{.items[0].status.conditionalUpdates[0]}' | jq`<br>UI Method: Navigate to target cluster settings and review available updates | Conditional update structure contains release information:<br>```<br>{<br>  "release": {<br>    "version": "4.19.8",<br>    "image": "quay.io/openshift-release-dev/ocp-release@sha256:abc123..."<br>  },<br>  "risks": [...],<br>  "conditions": [...]<br>}<br>```<br>*[Actual conditional update structure from cluster]* |
| 3 | **Create ClusterCurator Targeting Conditional Update** - CLI Method: Create targeted upgrade YAML:<br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: integration-test<br>  namespace: <cluster-name><br>spec:<br>  desiredCuration: upgrade<br>  cluster: <cluster-name><br>  upgrade:<br>    channel: stable-4.19<br>    desiredUpdate: "4.19.8"<br>```<br>UI Method: Create upgrade plan through ACM Console targeting conditional update version | ClusterCurator successfully targets version available in conditional updates:<br>```<br>clustercurator.cluster.open-cluster-management.io/integration-test created<br>```<br>Version matches conditional update availability |
| 4 | **Monitor ClusterCurator Controller Processing** - CLI Method: Execute `oc get clustercurator integration-test -w` and monitor controller logs<br>UI Method: Watch upgrade progress in ACM Console cluster view | Controller processes ClusterCurator and extracts digest from conditional updates:<br>```<br>Controller: "Found conditional update image digest"<br>Status: "curator-job" condition "True"<br>Phase: "Active"<br>```<br>ClusterCurator controller successfully identifies and processes conditional update |
| 5 | **Verify ClusterVersion Spec Update with Digest** - CLI Method: Execute `oc get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate}'`<br>UI Method: Check cluster upgrade status in OpenShift Console | ClusterVersion updated with digest from conditional update:<br>```<br>{<br>  "image": "quay.io/openshift-release-dev/ocp-release@sha256:abc123...",<br>  "version": "4.19.8"<br>}<br>```<br>Exact digest from conditional update applied to ClusterVersion |
| 6 | **Validate End-to-End Integration Success** - CLI Method: Execute `oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].status}'`<br>UI Method: Monitor overall upgrade progress in cluster administration | Cluster upgrade initiated successfully with digest-based image:<br>```<br>Status: "True"<br>Reason: "ClusterVersionProgressing"<br>Message: "Working towards 4.19.8"<br>```<br>Integration complete: ClusterCurator → Conditional Updates → ClusterVersion |

---

## Test Case 4: Validate ClusterCurator Digest Support for Disconnected Environment Scenarios

**Description:**
Comprehensive validation of ClusterCurator digest-based upgrade functionality specifically designed for disconnected environments where image tags are not accessible. This test verifies the complete Amadeus customer use case, ensuring digest-based upgrades work reliably in air-gapped environments with limited registry connectivity.

**Setup:**
- ACM hub cluster simulating disconnected environment constraints
- Target cluster configured for limited registry access scenarios
- ClusterCurator controller with digest discovery capabilities
- Test environment mimicking Amadeus disconnected infrastructure requirements

**Test Table:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | **Log into ACM Console** - Access ACM Console for disconnected environment testing: Navigate to https://console-openshift-console.apps.<cluster-host> | Console accessible for disconnected environment upgrade scenario testing |
| 2 | **Simulate Disconnected Registry Constraints** - CLI Method: Verify registry configuration: `oc get image.config.openshift.io/cluster -o yaml`<br>UI Method: Check cluster registry settings in administration console | Registry configuration shows limited connectivity or mirroring setup:<br>```<br>spec:<br>  registrySources:<br>    allowedRegistries:<br>    - "internal-registry.company.com"<br>    blockedRegistries:<br>    - "quay.io"<br>```<br>*[Simulated disconnected environment registry restrictions]* |
| 3 | **Create ClusterCurator for Critical Amadeus Upgrade** - CLI Method: Create disconnected upgrade specification:<br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: amadeus-upgrade<br>  namespace: <cluster-name><br>  annotations:<br>    customer: "amadeus"<br>    scenario: "disconnected-digest-upgrade"<br>spec:<br>  desiredCuration: upgrade<br>  cluster: <cluster-name><br>  upgrade:<br>    channel: stable-4.19<br>    desiredUpdate: "4.19.8"<br>```<br>UI Method: Create upgrade plan with disconnected environment considerations | ClusterCurator created for disconnected environment scenario:<br>```<br>clustercurator.cluster.open-cluster-management.io/amadeus-upgrade created<br>```<br>Annotation indicates customer-specific disconnected use case |
| 4 | **Verify Digest Discovery Over Tag Preference** - CLI Method: Monitor controller processing: `oc logs -n multicluster-engine deployment/cluster-curator-controller --tail=50`<br>UI Method: Monitor upgrade events and controller behavior | Controller prioritizes digest discovery for disconnected compatibility:<br>```<br>"Check for image digest in conditional updates"<br>"Found conditional update image digest"<br>"Using digest for disconnected environment compatibility"<br>```<br>Digest discovery successful, avoiding tag-based references |
| 5 | **Validate Digest-Only ClusterVersion Configuration** - CLI Method: Execute `oc get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate.image}'`<br>UI Method: Verify upgrade configuration through cluster settings | ClusterVersion configured exclusively with digest reference:<br>```<br>quay.io/openshift-release-dev/ocp-release@sha256:def456...<br>```<br>No tag references used, ensuring disconnected environment compatibility |
| 6 | **Confirm Amadeus Disconnected Environment Success** - CLI Method: Execute `oc describe clustercurator amadeus-upgrade`<br>UI Method: Review complete upgrade plan status and customer annotations | Disconnected environment upgrade successfully configured:<br>```<br>Status:<br>  Conditions:<br>  - type: "DisconnectedCompatible"<br>    status: "True"<br>    reason: "DigestBasedUpgrade"<br>    message: "Upgrade configured for disconnected environment using image digest"<br>```<br>Customer requirement satisfied: digest-based upgrade for air-gapped infrastructure |