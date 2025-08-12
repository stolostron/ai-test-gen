# E2E Test Cases: ACM-22079 - Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Test Case 1: Basic Non-Recommended Upgrade with Image Digest

**Description:** Verify that ClusterCurator can successfully upgrade a managed cluster to a non-recommended version using image digest from conditionalUpdates when the non-recommended annotation is present.

**Setup:** 
- Hub cluster with ACM/MCE installed and ClusterCurator controller running
- At least one managed cluster imported and available for upgrade
- Managed cluster must have a current version with available non-recommended updates in conditionalUpdates
- Ansible Tower credentials configured if using prehook/posthook

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| 1. Log into the hub cluster: `oc login --server=<HUB_API_URL> --username=<USERNAME> --password=<PASSWORD>` | Successfully logged into hub cluster |
| 2. Verify managed cluster is available: `oc get managedcluster` | Display managed clusters in "Available" state |
| 3. Get managed cluster's current version: `oc get managedclusterinfo <CLUSTER-NAME> -o yaml \| grep -A 5 version` | Shows current OpenShift version of managed cluster |
| 4. Check cluster's ClusterVersion for conditionalUpdates via ManagedClusterView: Create ManagedClusterView to read ClusterVersion from managed cluster and check conditionalUpdates list | Should show available non-recommended updates with image digests in the conditionalUpdates array. Example output: `conditionalUpdates: - image: quay.io/openshift-release-dev/ocp-release@sha256:abc123...` |
| 5. Create ClusterCurator for upgrade with non-recommended version: Apply ClusterCurator YAML with desiredUpdate set to a version found in conditionalUpdates | ClusterCurator resource created successfully |
| 6. Monitor ClusterCurator status: `oc get clustercurator <NAME> -o yaml` and watch for status changes | ClusterCurator shows "upgrade-cluster" job created and running |
| 7. Verify upgrade job uses image digest on managed cluster: Check managed cluster's ClusterVersion spec.desiredUpdate.image via ManagedClusterView | ClusterVersion shows image digest being used instead of tag. Example: `spec.desiredUpdate.image: quay.io/openshift-release-dev/ocp-release@sha256:abc123...` |
| 8. Monitor upgrade progress: `oc get clustercurator <NAME> -o jsonpath='{.status.conditions}'` | Shows upgrade progressing through phases: job-created → job-running → upgrade-complete |
| 9. Verify final upgrade completion: Check managed cluster version via ManagedClusterView | Managed cluster ClusterVersion shows successful upgrade to target version |

## Test Case 2: Fallback to availableUpdates when conditionalUpdates Unavailable

**Description:** Verify that ClusterCurator falls back to availableUpdates list when the desired version is not found in conditionalUpdates.

**Setup:**
- Hub cluster with ACM/MCE installed 
- Managed cluster with available recommended updates
- Target version exists in availableUpdates but not in conditionalUpdates

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| 1. Log into the hub cluster: `oc login --server=<HUB_API_URL> --username=<USERNAME> --password=<PASSWORD>` | Successfully logged into hub cluster |
| 2. Check managed cluster's update status: Create ManagedClusterView to read ClusterVersion and examine both conditionalUpdates and availableUpdates | Shows availableUpdates list with target version present, conditionalUpdates empty or missing target version |
| 3. Create ClusterCurator targeting recommended version from availableUpdates: Apply ClusterCurator with desiredUpdate matching version in availableUpdates | ClusterCurator created successfully |
| 4. Monitor upgrade job execution: `oc get clustercurator <NAME> -o yaml` | Shows upgrade job created and running |
| 5. Verify image source used: Check managed cluster ClusterVersion via ManagedClusterView | Uses appropriate image reference from availableUpdates (could be tag or digest) |
| 6. Confirm upgrade completion: Monitor ClusterCurator status and managed cluster version | Upgrade completes successfully to target version |

## Test Case 3: Backward Compatibility with Traditional Image Tags

**Description:** Verify that ClusterCurator maintains backward compatibility when neither conditionalUpdates nor availableUpdates contain the desired version, falling back to traditional image tag approach.

**Setup:**
- Hub cluster with ACM/MCE installed
- Managed cluster available for upgrade
- Target version not present in cluster's update lists

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| 1. Log into the hub cluster: `oc login --server=<HUB_API_URL> --username=<USERNAME> --password=<PASSWORD>` | Successfully logged into hub cluster |
| 2. Check update availability: Create ManagedClusterView to examine ClusterVersion update lists | Verify target version is not in conditionalUpdates or availableUpdates |
| 3. Create ClusterCurator with custom version: Apply ClusterCurator specifying desiredUpdate to version not in update lists | ClusterCurator created successfully |
| 4. Monitor upgrade behavior: `oc get clustercurator <NAME> -o yaml` | Shows upgrade job attempts with traditional approach |
| 5. Verify fallback mechanism: Check upgrade job logs or managed cluster ClusterVersion | System attempts upgrade using traditional image tag format as fallback |
| 6. Validate error handling or success: Monitor final status | Either succeeds with fallback approach or provides clear error messaging |

## Test Case 4: EUS to EUS Upgrade with Digest Support

**Description:** Verify that digest-based upgrades work correctly for Extended Update Support (EUS) to EUS scenarios with intermediate updates.

**Setup:**
- Hub cluster with ACM/MCE installed
- Managed cluster on EUS version (e.g., 4.16.x) 
- Target EUS version available (e.g., 4.18.x) with intermediate version required
- Both intermediate and final versions have digest references in conditionalUpdates

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| 1. Log into the hub cluster: `oc login --server=<HUB_API_URL> --username=<USERNAME> --password=<PASSWORD>` | Successfully logged into hub cluster |
| 2. Verify EUS cluster status: Check managed cluster version via ManagedClusterView | Shows cluster on EUS version (e.g., 4.16.latest) |
| 3. Check available EUS paths: Examine conditionalUpdates for both intermediate and target versions | Shows digest references for both intermediate and final EUS versions |
| 4. Create EUS-to-EUS ClusterCurator: Apply ClusterCurator with both intermediateUpdate and desiredUpdate specified | ClusterCurator created with EUS upgrade configuration |
| 5. Monitor first phase upgrade: `oc get clustercurator <NAME> -o yaml` | Shows upgrade to intermediate version using digest from conditionalUpdates |
| 6. Verify intermediate upgrade completion: Check managed cluster ClusterVersion via ManagedClusterView | Cluster successfully upgraded to intermediate version with digest |
| 7. Monitor second phase upgrade: Continue monitoring ClusterCurator status | Shows automatic progression to final EUS version upgrade |
| 8. Verify final EUS upgrade: Check final managed cluster version via ManagedClusterView | Cluster successfully upgraded to target EUS version using digest |

## Test Case 5: Disconnected Environment Digest Validation

**Description:** Verify that digest-based upgrades work in disconnected environments where image tags may not be available but digests are accessible.

**Setup:**
- Hub cluster in disconnected/restricted network environment
- Managed cluster with limited registry access
- Mirror registry with digest-based images available
- ClusterCurator configured for disconnected environment

**Test Steps:**

| Step | Expected Result |
|------|----------------|
| 1. Log into the hub cluster: `oc login --server=<HUB_API_URL> --username=<USERNAME> --password=<PASSWORD>` | Successfully logged into hub cluster in disconnected environment |
| 2. Verify disconnected cluster status: `oc get managedcluster` and check network policies | Shows managed cluster accessible with restricted network configuration |
| 3. Check mirror registry availability: Verify mirror registry contains target images with digests | Shows digest-based images available in local mirror registry |
| 4. Examine conditionalUpdates in disconnected cluster: Create ManagedClusterView to read ClusterVersion | Shows conditionalUpdates pointing to mirror registry with digest references |
| 5. Create ClusterCurator for disconnected upgrade: Apply ClusterCurator targeting non-recommended version with digest | ClusterCurator created successfully |
| 6. Monitor upgrade in disconnected environment: `oc get clustercurator <NAME> -o yaml` | Shows upgrade job accessing mirror registry using digest |
| 7. Verify digest utilization: Check managed cluster ClusterVersion via ManagedClusterView | Upgrade uses digest from conditionalUpdates, bypassing tag dependency |
| 8. Confirm disconnected upgrade success: Monitor final upgrade status | Upgrade completes successfully in disconnected environment using digest |

**Sample ClusterCurator YAML for Testing:**

```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: digest-upgrade-test
  namespace: <MANAGED-CLUSTER-NAMESPACE>
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.17.1"  # Version available in conditionalUpdates
    monitorTimeout: 120
    towerAuthSecret: ansible-credential-secret
    prehook:
    - name: pre-upgrade-checks
    posthook:
    - name: post-upgrade-validation
```

**Sample ManagedClusterView YAML for ClusterVersion Inspection:**

```yaml
apiVersion: view.open-cluster-management.io/v1beta1
kind: ManagedClusterView
metadata:
  name: clusterversion-view
  namespace: <MANAGED-CLUSTER-NAMESPACE>
spec:
  scope:
    resource: clusterversion
    name: version
```