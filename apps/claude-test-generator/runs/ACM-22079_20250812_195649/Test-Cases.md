# ACM-22079: ClusterCurator Digest-Based Upgrades Test Cases

## Test Case 1: ClusterCurator Non-Recommended Version Upgrade with Digest Resolution

**Description:** Verify that ClusterCurator can upgrade a managed cluster to a non-recommended OpenShift version using image digest when the non-recommended annotation is enabled.

**Setup:**
- Managed cluster with OpenShift version that has non-recommended updates available
- ClusterCurator controller deployed and functional
- Ansible Tower credentials configured
- Required permissions to create ClusterCurator resources

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| Log into the ACM hub cluster: `oc login <cluster-url>` | Successfully connected to the ACM hub cluster with appropriate permissions |
| List available managed clusters: `oc get managedclusters` | Display managed clusters including the target cluster for upgrade<br/><br/>```<br/>NAME                    HUB ACCEPTED   MANAGED CLUSTER URLS                        JOINED   AVAILABLE   AGE<br/>staging-cluster-01      true           https://api.cluster-xyz.sandbox.com:6443   True     True        24h<br/>local-cluster           true           https://api.hub-cluster.com:6443          True     True        48h<br/>``` |
| Check current cluster version of managed cluster using ManagedClusterView: Create view resource with `oc apply -f -` and paste:<br/><br/>```yaml<br/>apiVersion: view.open-cluster-management.io/v1beta1<br/>kind: ManagedClusterView<br/>metadata:<br/>  name: clusterversion-view<br/>  namespace: staging-cluster-01<br/>spec:<br/>  scope:<br/>    resource: clusterversions<br/>    name: version<br/>``` | ManagedClusterView created successfully and shows current cluster version information with available and conditional updates<br/><br/>```<br/>Current Version: 4.19.7<br/>Available Updates: null (no standard updates)<br/>Conditional Updates: [list of non-recommended versions]<br/>``` |
| Check the managed cluster's current version: `oc get managedclusterview -n staging-cluster-01 clusterversion-view -o jsonpath='{.status.result.status.desired.version}'` | Current version displayed (e.g., "4.19.7") |
| Create ClusterCurator with non-recommended annotation: `oc apply -f -` and paste:<br/><br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: test-digest-upgrade<br/>  namespace: staging-cluster-01<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.16.37<br/>    monitorTimeout: 120<br/>    towerAuthSecret: ansible-credential-secret<br/>    prehook:<br/>    - name: pre-upgrade-validation<br/>    posthook:<br/>    - name: post-upgrade-validation<br/>``` | ClusterCurator resource created successfully with non-recommended annotation applied |
| Monitor ClusterCurator status: `oc get clustercurator -n staging-cluster-01 test-digest-upgrade -o yaml` | ClusterCurator shows conditions progressing through: Created → Prehook → Activating → Monitoring → Posthook → Complete<br/><br/>```<br/>conditions:<br/>- type: clustercurator-job<br/>  status: "True"<br/>  message: "Job completed successfully"<br/>``` |
| Check that the curator job was created: `oc get jobs -n staging-cluster-01 -l app=clustercurator` | ClusterCurator job pod shows successful completion<br/><br/>```<br/>NAME                           COMPLETIONS   DURATION   AGE<br/>test-digest-upgrade-job        1/1           15m        20m<br/>``` |
| Verify the managed cluster ClusterVersion shows digest-based update in progress: `oc get managedclusterview -n staging-cluster-01 clusterversion-view -o jsonpath='{.status.result.spec.desiredUpdate}'` | ClusterVersion spec shows image digest instead of tag<br/><br/>```<br/>{<br/>  "image": "quay.io/openshift-release-dev/ocp-release@sha256:abcd1234...",<br/>  "version": "4.16.37"<br/>}<br/>``` |
| Monitor upgrade progress on managed cluster: `oc get managedclusterview -n staging-cluster-01 clusterversion-view -o jsonpath='{.status.result.status.conditions[?(@.type=="Progressing")].message}'` | Shows upgrade progress with digest-based image reference<br/><br/>```<br/>"Working towards 4.16.37: downloading update sha256:abcd1234..."<br/>``` |
| Verify successful upgrade completion: `oc get managedclusterview -n staging-cluster-01 clusterversion-view -o jsonpath='{.status.result.status.desired.version}'` | Target version achieved: "4.16.37"<br/><br/>Cluster shows "Available: True" and "Progressing: False" conditions |

## Test Case 2: ClusterCurator Fallback to Image Tag When Digest Not Available

**Description:** Verify that ClusterCurator falls back to using image tag when digest is not available in conditional updates, maintaining backward compatibility.

**Setup:**
- Managed cluster with OpenShift version
- ClusterCurator controller deployed and functional
- Target version that exists as image tag but not in conditional updates list

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| Log into the ACM hub cluster: `oc login <cluster-url>` | Successfully connected to the ACM hub cluster |
| Check managed cluster's conditional updates list: `oc get managedclusterview -n staging-cluster-01 clusterversion-view -o jsonpath='{.status.result.status.conditionalUpdates}'` | List of conditional updates displayed, confirming target version is NOT in this list<br/><br/>```<br/>[<br/>  {"version": "4.19.8", "image": "sha256:xyz123..."},<br/>  {"version": "4.19.9", "image": "sha256:abc456..."}<br/>]<br/>``` |
| Create ClusterCurator for version not in conditional updates: `oc apply -f -` and paste:<br/><br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: fallback-tag-upgrade<br/>  namespace: staging-cluster-01<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.18.0<br/>    monitorTimeout: 120<br/>    towerAuthSecret: ansible-credential-secret<br/>    prehook:<br/>    - name: pre-upgrade-check<br/>    posthook:<br/>    - name: post-upgrade-check<br/>``` | ClusterCurator created successfully |
| Monitor ClusterCurator processing: `oc get clustercurator -n staging-cluster-01 fallback-tag-upgrade -w` | Shows conditions progressing normally despite digest not being available |
| Verify managed cluster ClusterVersion uses image tag: `oc get managedclusterview -n staging-cluster-01 clusterversion-view -o jsonpath='{.status.result.spec.desiredUpdate}'` | ClusterVersion shows image tag instead of digest due to fallback behavior<br/><br/>```<br/>{<br/>  "version": "4.18.0",<br/>  "image": "quay.io/openshift-release-dev/ocp-release:4.18.0-x86_64"<br/>}<br/>``` |
| Check ClusterCurator logs for fallback message: `oc logs -n multicluster-engine deployment/cluster-curator-controller \| grep -i digest` | Log messages indicating digest lookup failed and fallback to tag occurred<br/><br/>```<br/>"digest not found in conditionalUpdates, falling back to image tag"<br/>``` |

## Test Case 3: ClusterCurator Validation Without Non-Recommended Annotation

**Description:** Verify that ClusterCurator upgrade behavior works correctly when the non-recommended annotation is not present, following standard upgrade paths.

**Setup:**
- Managed cluster with available standard updates
- ClusterCurator controller deployed and functional

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| Log into the ACM hub cluster: `oc login <cluster-url>` | Successfully connected to the ACM hub cluster |
| Check managed cluster's available standard updates: `oc get managedclusterview -n staging-cluster-01 clusterversion-view -o jsonpath='{.status.result.status.availableUpdates}'` | List of standard available updates displayed<br/><br/>```<br/>[<br/>  {"version": "4.19.8", "image": "sha256:def789..."},<br/>  {"version": "4.19.9", "image": "sha256:ghi012..."}<br/>]<br/>``` |
| Create ClusterCurator WITHOUT non-recommended annotation for standard upgrade: `oc apply -f -` and paste:<br/><br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: standard-upgrade<br/>  namespace: staging-cluster-01<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.19.8<br/>    monitorTimeout: 120<br/>    towerAuthSecret: ansible-credential-secret<br/>    prehook:<br/>    - name: standard-pre-upgrade<br/>    posthook:<br/>    - name: standard-post-upgrade<br/>``` | ClusterCurator created without non-recommended annotation |
| Monitor standard upgrade progress: `oc get clustercurator -n staging-cluster-01 standard-upgrade -o yaml` | Upgrade proceeds using standard available updates path with appropriate image digest from availableUpdates list |
| Verify cluster uses appropriate image reference: `oc get managedclusterview -n staging-cluster-01 clusterversion-view -o jsonpath='{.status.result.spec.desiredUpdate.image}'` | Image reference matches the digest from availableUpdates list<br/><br/>```<br/>"quay.io/openshift-release-dev/ocp-release@sha256:def789..."<br/>``` |

## Test Case 4: ClusterCurator Error Handling for Invalid Non-Recommended Version

**Description:** Verify that ClusterCurator handles error cases gracefully when attempting to upgrade to a version that doesn't exist in any update path.

**Setup:**
- Managed cluster with current OpenShift version
- ClusterCurator controller deployed and functional

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| Log into the ACM hub cluster: `oc login <cluster-url>` | Successfully connected to the ACM hub cluster |
| Create ClusterCurator with invalid/non-existent version: `oc apply -f -` and paste:<br/><br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: invalid-version-upgrade<br/>  namespace: staging-cluster-01<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.99.99<br/>    monitorTimeout: 120<br/>    towerAuthSecret: ansible-credential-secret<br/>    prehook:<br/>    - name: invalid-pre-upgrade<br/>    posthook:<br/>    - name: invalid-post-upgrade<br/>``` | ClusterCurator created successfully (validation occurs during processing) |
| Monitor ClusterCurator status for error conditions: `oc get clustercurator -n staging-cluster-01 invalid-version-upgrade -o yaml` | ClusterCurator shows error condition with appropriate failure message<br/><br/>```<br/>conditions:<br/>- type: clustercurator-job<br/>  status: "False"<br/>  reason: "UpgradeVersionNotFound"<br/>  message: "Version 4.99.99 not found in available or conditional updates"<br/>``` |
| Check ClusterCurator job logs for error details: `oc logs -n staging-cluster-01 job/invalid-version-upgrade-job` | Job logs show clear error message about version not being available in any update path<br/><br/>```<br/>"ERROR: Target version 4.99.99 not found in availableUpdates or conditionalUpdates"<br/>``` |
| Verify managed cluster remains unchanged: `oc get managedclusterview -n staging-cluster-01 clusterversion-view -o jsonpath='{.status.result.status.desired.version}'` | Managed cluster version remains unchanged from original version (e.g., "4.19.7") |

## Test Case 5: ClusterCurator Digest Lookup in Conditional Updates List

**Description:** Verify that ClusterCurator correctly searches and uses image digests from the conditionalUpdates list when the non-recommended annotation is present.

**Setup:**
- Managed cluster with conditional updates available
- ClusterCurator controller deployed and functional
- Target version available in conditional updates with digest

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| Log into the ACM hub cluster: `oc login <cluster-url>` | Successfully connected to the ACM hub cluster |
| Create ManagedClusterView to inspect conditional updates: `oc apply -f -` and paste:<br/><br/>```yaml<br/>apiVersion: view.open-cluster-management.io/v1beta1<br/>kind: ManagedClusterView<br/>metadata:<br/>  name: conditional-updates-view<br/>  namespace: staging-cluster-01<br/>spec:<br/>  scope:<br/>    resource: clusterversions<br/>    name: version<br/>``` | ManagedClusterView created to monitor conditional updates |
| Check for conditional updates containing target version: `oc get managedclusterview -n staging-cluster-01 conditional-updates-view -o jsonpath='{.status.result.status.conditionalUpdates[?(@.version=="4.16.37")].image}'` | Conditional update with target version and digest found<br/><br/>```<br/>"quay.io/openshift-release-dev/ocp-release@sha256:1234abcd..."<br/>``` |
| Create ClusterCurator targeting version in conditional updates: `oc apply -f -` and paste:<br/><br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: conditional-digest-upgrade<br/>  namespace: staging-cluster-01<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.16.37<br/>    monitorTimeout: 120<br/>    towerAuthSecret: ansible-credential-secret<br/>    prehook:<br/>    - name: conditional-pre-upgrade<br/>    posthook:<br/>    - name: conditional-post-upgrade<br/>``` | ClusterCurator created targeting version available in conditional updates |
| Monitor ClusterCurator progress: `oc get clustercurator -n staging-cluster-01 conditional-digest-upgrade -w` | ClusterCurator progresses through upgrade phases successfully |
| Verify managed cluster uses digest from conditional updates: `oc get managedclusterview -n staging-cluster-01 conditional-updates-view -o jsonpath='{.status.result.spec.desiredUpdate.image}'` | Managed cluster ClusterVersion shows exact digest from conditional updates list<br/><br/>```<br/>"quay.io/openshift-release-dev/ocp-release@sha256:1234abcd..."<br/>``` |
| Confirm upgrade completion: `oc get managedclusterview -n staging-cluster-01 conditional-updates-view -o jsonpath='{.status.result.status.conditions[?(@.type=="Available")].status}'` | Cluster shows "Available: True" indicating successful upgrade completion |
| Clean up test resources: `oc delete clustercurator -n staging-cluster-01 conditional-digest-upgrade && oc delete managedclusterview -n staging-cluster-01 conditional-updates-view` | Test resources cleaned up successfully |