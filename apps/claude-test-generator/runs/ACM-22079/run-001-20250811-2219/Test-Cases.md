# Test Cases: ACM-22079 - Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Test Case 1: Digest-based upgrade with non-recommended annotation

**Description:** Verify that ClusterCurator uses image digests when upgrading to non-recommended OpenShift versions through the conditional updates list.

**Setup:** 
- ACM hub cluster with ClusterCurator operator deployed
- Managed cluster running an OpenShift version that has non-recommended updates available (e.g., 4.16.36 → 4.16.37)
- Ansible Tower configured with authentication secrets

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into ACM hub cluster** - `source setup_clc qe6 && oc whoami` | Login successful with connection to hub cluster confirmed |
| **Step 2: Create a namespace for the test cluster** - `oc create namespace cluster-digest-test` | ```namespace/cluster-digest-test created``` |
| **Step 3: Create a ClusterCurator resource with non-recommended annotation** | ClusterCurator resource is created with the correct annotation |
| ```yaml
oc apply -f - <<EOF
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'
  name: digest-upgrade-test
  namespace: cluster-digest-test
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.37"
    monitorTimeout: 120
    towerAuthSecret: ansible-secret
    prehook:
      - name: pre-upgrade-validation
    posthook:
      - name: post-upgrade-validation
EOF
``` | ```clustercurator.cluster.open-cluster-management.io/digest-upgrade-test created``` |
| **Step 4: Verify the ClusterCurator resource is created correctly** - `oc get clustercurator digest-upgrade-test -n cluster-digest-test -o yaml` | Resource displays: annotation `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`, `spec.upgrade.desiredUpdate: "4.16.37"`, `spec.desiredCuration: upgrade` |
| **Step 5: Check managed cluster's ClusterVersion conditionalUpdates for target version** - `oc --kubeconfig=/path/to/managed/cluster get clusterversion version -o jsonpath='{.status.conditionalUpdates[?(@.release.version=="4.16.37")].release.image}'` | Returns an image digest: ```quay.io/openshift-release-dev/ocp-release@sha256:abcd1234...``` |
| **Step 6: Monitor ClusterCurator job execution** - `oc logs -n cluster-digest-test job/digest-upgrade-test-upgrade -f` | Log output shows: "Found target version 4.16.37 in conditionalUpdates", "Using image digest: quay.io/openshift-release-dev/ocp-release@sha256:...", Job progresses to upgrade execution |
| **Step 7: Verify managed cluster uses image digest** - `oc --kubeconfig=/path/to/managed/cluster get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}'` | Returns the digest format: ```quay.io/openshift-release-dev/ocp-release@sha256:abcd1234...``` |
| **Step 8: Check ClusterCurator status for completion** - `oc get clustercurator digest-upgrade-test -n cluster-digest-test -o jsonpath='{.status.conditions[?(@.type=="UpgradeSucceeded")].status}'` | ```True``` |

## Test Case 2: Fallback to availableUpdates when not in conditionalUpdates

**Description:** Verify that ClusterCurator falls back to checking availableUpdates list when the target version is not found in conditionalUpdates.

**Setup:**
- ACM hub cluster with ClusterCurator operator deployed  
- Managed cluster with a version that has updates in availableUpdates but not conditionalUpdates
- Ansible Tower configured with authentication secrets

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into ACM hub cluster** - `source setup_clc qe6 && oc whoami` | Login successful with connection to hub cluster confirmed |
| **Step 2: Create namespace for the fallback test** - `oc create namespace cluster-fallback-test` | ```namespace/cluster-fallback-test created``` |
| **Step 3: Create ClusterCurator targeting a version in availableUpdates** | ClusterCurator resource is created |
| ```yaml
oc apply -f - <<EOF
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: fallback-upgrade-test
  namespace: cluster-fallback-test
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.38"
    monitorTimeout: 120
    towerAuthSecret: ansible-secret
    prehook:
      - name: pre-upgrade-validation
    posthook:
      - name: post-upgrade-validation
EOF
``` | ```clustercurator.cluster.open-cluster-management.io/fallback-upgrade-test created``` |
| **Step 4: Verify target version exists in availableUpdates** - `oc --kubeconfig=/path/to/managed/cluster get clusterversion version -o jsonpath='{.status.availableUpdates[?(@.version=="4.16.38")].image}'` | Returns image digest: ```quay.io/openshift-release-dev/ocp-release@sha256:efgh5678...``` |
| **Step 5: Confirm version not in conditionalUpdates** - `oc --kubeconfig=/path/to/managed/cluster get clusterversion version -o jsonpath='{.status.conditionalUpdates[?(@.release.version=="4.16.38")].release.image}'` | Returns empty (version not in conditionalUpdates) |
| **Step 6: Monitor ClusterCurator job logs for fallback behavior** - `oc logs -n cluster-fallback-test job/fallback-upgrade-test-upgrade -f` | Log output shows: "Target version 4.16.38 not found in conditionalUpdates", "Checking availableUpdates list...", "Found target version in availableUpdates", "Using image digest: quay.io/openshift-release-dev/ocp-release@sha256:..." |
| **Step 7: Verify managed cluster uses digest from availableUpdates** - `oc --kubeconfig=/path/to/managed/cluster get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}'` | ```quay.io/openshift-release-dev/ocp-release@sha256:efgh5678...``` |

## Test Case 3: Backward compatibility fallback to image tag

**Description:** Verify that ClusterCurator falls back to using image tags when the target version is not found in either conditionalUpdates or availableUpdates.

**Setup:**
- ACM hub cluster with ClusterCurator operator deployed
- Managed cluster where the target version is not available in update lists
- Ansible Tower configured with authentication secrets

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into ACM hub cluster** - `source setup_clc qe6 && oc whoami` | Login successful with connection to hub cluster confirmed |
| **Step 2: Create namespace for backward compatibility test** - `oc create namespace cluster-compat-test` | ```namespace/cluster-compat-test created``` |
| **Step 3: Create ClusterCurator targeting a version not in either update list** | ClusterCurator resource is created |
| ```yaml
oc apply -f - <<EOF
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: compat-upgrade-test
  namespace: cluster-compat-test
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.17.0"
    monitorTimeout: 120
    towerAuthSecret: ansible-secret
    prehook:
      - name: pre-upgrade-validation
    posthook:
      - name: post-upgrade-validation
EOF
``` | ```clustercurator.cluster.open-cluster-management.io/compat-upgrade-test created``` |
| **Step 4: Verify target version not in conditionalUpdates** - `oc --kubeconfig=/path/to/managed/cluster get clusterversion version -o jsonpath='{.status.conditionalUpdates[?(@.release.version=="4.17.0")].release.image}'` | Returns empty |
| **Step 5: Verify target version not in availableUpdates** - `oc --kubeconfig=/path/to/managed/cluster get clusterversion version -o jsonpath='{.status.availableUpdates[?(@.version=="4.17.0")].image}'` | Returns empty |
| **Step 6: Monitor ClusterCurator job logs for backward compatibility** - `oc logs -n cluster-compat-test job/compat-upgrade-test-upgrade -f` | Log output shows: "Target version 4.17.0 not found in conditionalUpdates", "Target version 4.17.0 not found in availableUpdates", "Falling back to image tag for backward compatibility", "Using image tag: quay.io/openshift-release-dev/ocp-release:4.17.0" |
| **Step 7: Verify managed cluster uses image tag format** - `oc --kubeconfig=/path/to/managed/cluster get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}'` | ```quay.io/openshift-release-dev/ocp-release:4.17.0``` |

## Test Case 4: Non-recommended annotation requirement validation

**Description:** Verify that the non-recommended annotation is properly enforced when attempting upgrades to non-recommended versions.

**Setup:**
- ACM hub cluster with ClusterCurator operator deployed
- Managed cluster with conditional updates containing non-recommended versions
- Ansible Tower configured with authentication secrets

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into ACM hub cluster** - `source setup_clc qe6 && oc whoami` | Login successful with connection to hub cluster confirmed |
| **Step 2: Create namespace for annotation validation test** - `oc create namespace cluster-annotation-test` | ```namespace/cluster-annotation-test created``` |
| **Step 3: Create ClusterCurator without non-recommended annotation** | ClusterCurator processes but may show warnings or restrictions |
| ```yaml
oc apply -f - <<EOF
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: annotation-test
  namespace: cluster-annotation-test
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.37"
    monitorTimeout: 120
    towerAuthSecret: ansible-secret
    prehook:
      - name: pre-upgrade-validation
    posthook:
      - name: post-upgrade-validation
EOF
``` | ```clustercurator.cluster.open-cluster-management.io/annotation-test created``` |
| **Step 4: Monitor ClusterCurator job behavior without annotation** - `oc logs -n cluster-annotation-test job/annotation-test-upgrade -f` | Log output shows standard processing: Version lookup in conditionalUpdates, Digest resolution if found, Normal upgrade flow |
| **Step 5: Add the non-recommended annotation** - `oc annotate clustercurator annotation-test -n cluster-annotation-test cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions='true'` | ```clustercurator.cluster.open-cluster-management.io/annotation-test annotated``` |
| **Step 6: Verify the annotation is properly set** - `oc get clustercurator annotation-test -n cluster-annotation-test -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'` | ```true``` |
| **Step 7: Trigger a new upgrade operation with annotation** - `oc patch clustercurator annotation-test -n cluster-annotation-test --type='merge' -p='{"spec":{"upgrade":{"desiredUpdate":"4.16.37","monitorTimeout":121}}}'` | ```clustercurator.cluster.open-cluster-management.io/annotation-test patched``` |

## Test Case 5: ManagedClusterView validation of managed cluster upgrade status

**Description:** Verify upgrade status by reading managed cluster ClusterVersion through ManagedClusterView from the hub.

**Setup:**
- ACM hub cluster with ClusterCurator operator deployed
- Active managed cluster undergoing or completed digest-based upgrade
- ManagedClusterView resources available

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into ACM hub cluster** - `source setup_clc qe6 && oc whoami` | Login successful with connection to hub cluster confirmed |
| **Step 2: Create ManagedClusterView to read ClusterVersion from managed cluster** | ManagedClusterView resource is created |
| ```yaml
oc apply -f - <<EOF
apiVersion: view.open-cluster-management.io/v1beta1
kind: ManagedClusterView
metadata:
  name: clusterversion-view
  namespace: clc-aws-1754912177798
spec:
  scope:
    apiGroup: config.openshift.io
    kind: ClusterVersion
    name: version
    resource: clusterversions
EOF
``` | ```managedclusterview.view.open-cluster-management.io/clusterversion-view created``` |
| **Step 3: Wait for ManagedClusterView to sync** - `oc get managedclusterview clusterversion-view -n clc-aws-1754912177798 -o jsonpath='{.status.conditions[?(@.type=="Processing")].status}'` | ```True``` |
| **Step 4: Verify managed cluster's current version** - `oc get managedclusterview clusterversion-view -n clc-aws-1754912177798 -o jsonpath='{.status.result.status.desired.version}'` | Current version (e.g.): ```4.16.36``` |
| **Step 5: Check desired update shows digest format** - `oc get managedclusterview clusterversion-view -n clc-aws-1754912177798 -o jsonpath='{.status.result.spec.desiredUpdate.image}'` | Image digest format if upgrade active: ```quay.io/openshift-release-dev/ocp-release@sha256:abcd1234...``` |
| **Step 6: Verify conditionalUpdates via ManagedClusterView** - `oc get managedclusterview clusterversion-view -n clc-aws-1754912177798 -o jsonpath='{.status.result.status.conditionalUpdates[0].release.image}'` | Sample conditional update with digest: ```quay.io/openshift-release-dev/ocp-release@sha256:efgh5678...``` |
| **Step 7: Monitor upgrade progress** - `oc get managedclusterview clusterversion-view -n clc-aws-1754912177798 -o jsonpath='{.status.result.status.conditions[?(@.type=="Progressing")].message}'` | Progress message (e.g.): ```Working towards 4.16.37: downloading update``` |
