# ClusterCurator Digest-Based Upgrade Test Cases

## Summary

**Feature**: Support digest-based upgrades via ClusterCurator for non-recommended upgrades
**Testing Approach**: Direct feature validation with UI E2E scenarios and comprehensive CLI alternatives
**Test Environment**: Environment-agnostic design using `<cluster-host>` placeholders

---

## Test Case 1: ClusterCurator Digest-Based Upgrade Configuration

**Description**: Validate ClusterCurator configuration with image digest for non-recommended OpenShift upgrades in disconnected environments.

**Setup**: 
- Access to ACM Console and CLI tools
- Target managed cluster for upgrade testing
- Valid OpenShift image digest for non-recommended version
- ClusterCurator RBAC permissions configured

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.`<cluster-host>` | `oc login https://api.<cluster-host>:6443 -u <username>` | ACM Console dashboard displays with cluster management options |
| 2 | Navigate to Cluster Curator | All Clusters → Infrastructure → Automation → ClusterCurator | `oc get clustercurators --all-namespaces` | ClusterCurator management interface displays current curator instances |
| 3 | Create ClusterCurator with digest | Click "Create ClusterCurator" → Select target cluster → Configure upgrade section | Create YAML file: `touch clustercurator-digest.yaml` and add:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: digest-upgrade-test
  namespace: target-cluster
spec:
  desiredCuration: upgrade
  cluster: target-cluster
  upgrade:
    desiredUpdate: "quay.io/openshift-release-dev/ocp-release@sha256:abc123def456"
    options:
      allowNonRecommended: "true"
``` | ClusterCurator resource created with digest-based upgrade specification |
| 4 | Configure non-recommended annotation | Add annotation: `cluster.open-cluster-management.io/upgrade-allow-non-recommended: \"true\"` | `oc annotate clustercurator digest-upgrade-test -n target-cluster cluster.open-cluster-management.io/upgrade-allow-non-recommended="true"` | Non-recommended upgrade annotation applied successfully |
| 5 | Apply ClusterCurator configuration | Click "Create" to apply configuration | `oc apply -f clustercurator-digest.yaml` | ClusterCurator resource created and accepted by cluster |
| 6 | Monitor upgrade initiation | Navigate to cluster details → View upgrade status | `oc get clustercurator digest-upgrade-test -n target-cluster -o yaml` | ClusterCurator status shows upgrade initiated with digest validation |
| 7 | Verify digest resolution | Check upgrade logs for digest lookup process | `oc logs -n target-cluster -l job-name=curator-job-digest-upgrade-test` | Logs show successful digest resolution from conditionalUpdates list |
| 8 | Validate upgrade progress | Monitor cluster upgrade status in ACM Console | `oc get clusterversion --kubeconfig=target-cluster-kubeconfig` | Cluster upgrade progresses using specified image digest |

---

## Test Case 2: Digest Fallback Logic Validation

**Description**: Verify ClusterCurator fallback behavior when image digest is unavailable in conditionalUpdates list.

**Setup**:
- Access to ACM Console and CLI tools
- Target managed cluster for testing
- ClusterCurator with digest not in conditionalUpdates list
- Valid image tag for fallback scenario

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.`<cluster-host>` | `oc login https://api.<cluster-host>:6443 -u <username>` | ACM Console access with cluster management capabilities |
| 2 | Create ClusterCurator with unavailable digest | Navigate to ClusterCurator creation → Configure with non-existent digest | Create YAML: `touch clustercurator-fallback.yaml` and add:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: fallback-test
  namespace: target-cluster
spec:
  desiredCuration: upgrade
  cluster: target-cluster
  upgrade:
    desiredUpdate: "quay.io/openshift-release-dev/ocp-release@sha256:nonexistent123"
    options:
      allowNonRecommended: "true"
``` | ClusterCurator configured with unavailable digest specification |
| 3 | Apply configuration and monitor | Click "Create" → Navigate to upgrade monitoring | `oc apply -f clustercurator-fallback.yaml` | ClusterCurator resource created successfully |
| 4 | Verify digest lookup failure | Check upgrade logs for digest resolution attempts | `oc logs -n target-cluster -l job-name=curator-job-fallback-test \| grep "digest"` | Logs show digest not found in conditionalUpdates list |
| 5 | Confirm availableUpdates check | Monitor logs for availableUpdates list verification | `oc logs -n target-cluster -l job-name=curator-job-fallback-test \| grep "availableUpdates"` | System checks availableUpdates list for digest availability |
| 6 | Validate fallback to image tag | Verify curator falls back to image tag approach | `oc get clustercurator fallback-test -n target-cluster -o jsonpath='{.status.conditions[*].message}'` | Status indicates fallback to image tag for backward compatibility |
| 7 | Verify upgrade continues | Check that upgrade proceeds with fallback logic | `oc get clusterversion --kubeconfig=target-cluster-kubeconfig -o jsonpath='{.status.desired.image}'` | Upgrade proceeds using image tag fallback method |

---

## Test Case 3: Disconnected Environment Digest Upgrade

**Description**: Validate ClusterCurator digest-based upgrade functionality in disconnected environment scenarios.

**Setup**:
- Disconnected environment simulation or actual disconnected cluster
- Local image registry with mirrored OpenShift release images
- ClusterCurator RBAC and network access configured
- Image digest for mirrored release content

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Access ACM Console in disconnected environment: https://console-openshift-console.apps.`<cluster-host>` | `oc login https://api.<cluster-host>:6443 -u <username>` | ACM Console access in disconnected environment |
| 2 | Verify image registry configuration | Navigate to cluster details → Check image registry settings | `oc get imagecontentsourcepolicy` and `oc get images.config.openshift.io cluster -o yaml` | Image registry configured for disconnected operations |
| 3 | Create ClusterCurator with local digest | Configure ClusterCurator with local registry digest | Create YAML: `touch clustercurator-disconnected.yaml` and add:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: disconnected-upgrade
  namespace: target-cluster
spec:
  desiredCuration: upgrade
  cluster: target-cluster
  upgrade:
    desiredUpdate: "local-registry.example.com/openshift/release@sha256:localdigest123"
    options:
      allowNonRecommended: "true"
``` | ClusterCurator configured with local registry image digest |
| 4 | Configure disconnected upgrade settings | Add necessary annotations and configurations for disconnected upgrade | `oc annotate clustercurator disconnected-upgrade -n target-cluster cluster.open-cluster-management.io/upgrade-allow-non-recommended="true"` | Disconnected upgrade configuration applied |
| 5 | Apply ClusterCurator in disconnected mode | Click "Create" → Monitor for disconnected-specific behavior | `oc apply -f clustercurator-disconnected.yaml` | ClusterCurator resource applied successfully in disconnected environment |
| 6 | Monitor local registry access | Verify ClusterCurator accesses local image registry | `oc logs -n target-cluster -l job-name=curator-job-disconnected-upgrade \| grep "local-registry"` | Logs show successful access to local image registry |
| 7 | Validate digest resolution from local registry | Check that digest is resolved from local registry content | `oc get clustercurator disconnected-upgrade -n target-cluster -o jsonpath='{.status.conditions[*].message}'` | Status confirms digest resolution from local registry |
| 8 | Verify upgrade execution | Monitor cluster upgrade using local registry digest | `oc get clusterversion --kubeconfig=target-cluster-kubeconfig -o jsonpath='{.status.desired.image}'` | Cluster upgrade proceeds using local registry digest successfully |