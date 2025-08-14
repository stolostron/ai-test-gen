# ACM-22079 E2E Test Plan: Support digest-based upgrades via ClusterCurator

## Test Case 1: Basic Non-Recommended Upgrade with Digest-Based Image

### Description
Verify that ClusterCurator successfully performs an upgrade to a non-recommended OpenShift version using image digest when the non-recommended annotation is present.

### Setup
- Managed cluster running OpenShift 4.16.36 (or compatible version with non-recommended updates available)
- ACM hub cluster with ClusterCurator functionality enabled
- Access to a non-recommended target version (e.g., 4.16.37)

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully logged into the hub cluster with cluster admin privileges. Terminal shows login confirmation with cluster API URL and user context. |
| **Step 2: Verify managed cluster current version** - Check the current OpenShift version on the target managed cluster: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | Current cluster version is displayed showing starting version (e.g., 4.16.36). Output shows spec.desiredUpdate and status.history with current version details. ```yaml spec: channel: stable-4.16 clusterID: <cluster-id> desiredUpdate: {} status: availableUpdates: - image: quay.io/openshift-release-dev/ocp-release@sha256:... version: 4.16.37 ``` |
| **Step 3: Create ClusterCurator with non-recommended annotation** - Apply the ClusterCurator resource with the required annotation to enable non-recommended upgrades: `oc apply -f -` with ClusterCurator YAML containing `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'` annotation | ClusterCurator resource created successfully. The resource is accepted by the API server and shows "clustercurator.cluster.open-cluster-management.io/cluster1 created" message. ```yaml apiVersion: cluster.open-cluster-management.io/v1beta1 kind: ClusterCurator metadata: annotations: cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true' name: cluster1 namespace: cluster1 spec: desiredCuration: upgrade upgrade: desiredUpdate: 4.16.37 monitorTimeout: 120 ``` |
| **Step 4: Monitor ClusterCurator job creation** - Watch for the curator job to be created and start processing: `oc get jobs -n cluster1 -w` | ClusterCurator job is created and starts running. Job status shows "curator-job-<hash>" with COMPLETIONS 0/1 and AGE showing recent creation time. |
| **Step 5: Verify image digest usage in managed cluster** - Check that the managed cluster ClusterVersion resource uses image digest instead of image tag: `oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' --context=<managed-cluster-context>` | The desiredUpdate.image field contains an image digest (sha256 hash) rather than a version tag. Output shows digest format like `quay.io/openshift-release-dev/ocp-release@sha256:abc123...` instead of `4.16.37` tag. This confirms the digest-based upgrade mechanism is working. |
| **Step 6: Monitor upgrade progress** - Track the upgrade progress on the managed cluster: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | Upgrade progresses through expected phases (Progressing, Partial, Complete). Status shows progression with conditions indicating upgrade status and history entries being updated with new version information. |
| **Step 7: Validate upgrade completion** - Confirm the cluster has successfully upgraded to the target version: `oc get nodes --context=<managed-cluster-context>` and `oc get clusterversion version --context=<managed-cluster-context>` | All nodes show the new version and the ClusterVersion status indicates successful completion. Nodes display target version (4.16.37) and ClusterVersion status.history[0] shows the completed upgrade with the new version. |
| **Step 8: Verify ClusterCurator job completion** - Check that the ClusterCurator job completed successfully: `oc get clustercurator cluster1 -n cluster1 -o yaml` | ClusterCurator shows successful completion status with conditions indicating successful upgrade operation. Status field shows phase "upgrade-complete" or similar success indicator. |

## Test Case 2: Fallback Mechanism Validation

### Description
Verify the three-tier search mechanism (conditionalUpdates → availableUpdates → image tag) when digest is not available in primary source.

### Setup  
- Managed cluster with limited conditional updates
- Target version available in availableUpdates but not conditionalUpdates

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully logged into the hub cluster with cluster admin privileges confirming access to managed clusters and ClusterCurator resources. |
| **Step 2: Examine ClusterVersion conditionalUpdates and availableUpdates** - Review the update sources on the managed cluster: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | ClusterVersion shows both conditionalUpdates and availableUpdates lists. Identify a version that exists in availableUpdates but not in conditionalUpdates to test fallback mechanism. ```yaml status: conditionalUpdates: [] availableUpdates: - image: quay.io/openshift-release-dev/ocp-release@sha256:def456... version: 4.16.38 ``` |
| **Step 3: Create ClusterCurator targeting availableUpdates version** - Apply ClusterCurator with non-recommended annotation targeting a version from availableUpdates: `oc apply -f -` | ClusterCurator resource created successfully targeting a version that will trigger the fallback search mechanism to availableUpdates list. |
| **Step 4: Monitor curator job execution** - Watch the curator job logs to observe fallback mechanism: `oc logs -f job/curator-job-<hash> -n cluster1` | Job logs show the search progression through conditionalUpdates (not found) then availableUpdates (found). Logs indicate "Searching conditionalUpdates for version X" followed by "Not found, checking availableUpdates" and "Found in availableUpdates". |
| **Step 5: Verify correct image digest retrieval** - Confirm the managed cluster received the digest from availableUpdates: `oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' --context=<managed-cluster-context>` | The image field contains the digest from the availableUpdates list, confirming successful fallback mechanism operation. Output matches the expected sha256 digest from availableUpdates rather than conditionalUpdates. |
| **Step 6: Validate upgrade proceeds normally** - Monitor that the upgrade continues successfully despite using fallback source: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | Upgrade progresses normally using the digest retrieved from availableUpdates. Status conditions show normal upgrade progression confirming the fallback mechanism doesn't impact upgrade reliability. |

## Test Case 3: Error Handling and Final Fallback to Image Tag

### Description
Test the system behavior when neither conditionalUpdates nor availableUpdates contain the requested version, forcing fallback to image tag.

### Setup
- Managed cluster with limited update options
- Target version not available in either update list

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully logged into the hub cluster with proper administrative access to create and monitor ClusterCurator resources. |
| **Step 2: Identify version not in update lists** - Examine ClusterVersion to find a version not in conditionalUpdates or availableUpdates: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | ClusterVersion output shows current conditionalUpdates and availableUpdates lists. Identify a valid but unlisted version for testing final fallback mechanism. |
| **Step 3: Create ClusterCurator with unlisted version** - Apply ClusterCurator targeting a version not in either update list: `oc apply -f -` | ClusterCurator resource created successfully with target version that will force the system to use image tag fallback mechanism. |
| **Step 4: Monitor curator job for fallback behavior** - Watch job logs to observe complete search sequence: `oc logs -f job/curator-job-<hash> -n cluster1` | Job logs show complete search sequence: "Searching conditionalUpdates... not found", "Searching availableUpdates... not found", "Using image tag fallback for version X". This demonstrates the three-tier search mechanism working as designed. |
| **Step 5: Verify image tag usage** - Check that the managed cluster uses image tag format instead of digest: `oc get clusterversion version -o jsonpath='{.spec.desiredUpdate}' --context=<managed-cluster-context>` | The desiredUpdate field shows version tag format rather than digest. Output shows `{"version": "4.16.X"}` instead of image digest, confirming final fallback mechanism activated successfully. |
| **Step 6: Validate upgrade attempt or appropriate error** - Monitor the upgrade status for expected behavior: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | System either attempts upgrade with image tag or provides appropriate error message if version is truly unavailable. Status conditions show either upgrade progression or clear error messaging about version availability. |

## Test Case 4: Rollback and Recovery Procedures

### Description
Verify rollback capabilities and error recovery when digest-based upgrades encounter issues.

### Setup
- Managed cluster with successful initial upgrade
- Ability to simulate upgrade failure scenarios

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully logged into the hub cluster with administrative privileges to manage ClusterCurator resources and monitor upgrade operations. |
| **Step 2: Record pre-upgrade cluster state** - Document current cluster version and configuration: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` and `oc get nodes --context=<managed-cluster-context>` | Complete record of cluster state before upgrade attempt. Output shows current version, node status, and system health indicators for rollback reference. ```yaml status: history: - state: "Completed" version: "4.16.36" startedTime: "2025-08-14T10:00:00Z" ``` |
| **Step 3: Initiate problematic upgrade** - Create ClusterCurator with potentially problematic configuration to test error handling: `oc apply -f -` | ClusterCurator created and starts processing. Initial validation passes but upgrade may encounter issues to test recovery mechanisms. |
| **Step 4: Monitor for upgrade failure indicators** - Watch for upgrade issues and failure conditions: `oc get clusterversion version -w --context=<managed-cluster-context>` | Upgrade failure detected through ClusterVersion conditions. Status shows degraded state, error conditions, or stalled progression requiring intervention. ```yaml conditions: - type: "Failing" status: "True" message: "Upgrade failed due to..." ``` |
| **Step 5: Execute rollback procedure** - Create new ClusterCurator to rollback to previous version: `oc apply -f -` with ClusterCurator specifying previous known-good version | Rollback ClusterCurator created successfully and begins downgrade process. Job shows creation and processing of rollback operation to restore cluster to previous stable state. |
| **Step 6: Verify rollback completion** - Confirm cluster returns to stable state: `oc get clusterversion version --context=<managed-cluster-context>` and `oc get nodes --context=<managed-cluster-context>` | Cluster successfully returned to previous version with all nodes healthy. ClusterVersion shows rollback completed and system restored to known-good configuration. All components operational. |
| **Step 7: Validate cluster functionality** - Test basic cluster operations post-rollback: `oc get pods --all-namespaces --context=<managed-cluster-context>` | All critical cluster services are running normally after rollback. System pods show running status and cluster demonstrates full operational capability. |

## Test Case 5: Disconnected Environment Simulation

### Description
Validate digest-based upgrade functionality in simulated disconnected environment conditions.

### Setup
- Managed cluster with restricted network access simulation
- Local registry with mirrored images
- ClusterCurator configured for disconnected operation

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully logged into the hub cluster with access to disconnected environment simulation capabilities and ClusterCurator resources. |
| **Step 2: Configure disconnected registry settings** - Set up image registry configuration for disconnected environment: `oc get imagecontentsourcepolicy --context=<managed-cluster-context>` | Image registry configuration shows proper mirroring setup for disconnected environment. Registry policies direct image pulls to local mirror rather than external registries. ```yaml apiVersion: operator.openshift.io/v1alpha1 kind: ImageContentSourcePolicy metadata: name: mirror-config spec: repositoryDigestMirrors: - mirrors: ["local-registry.example.com/openshift"] source: "quay.io/openshift-release-dev" ``` |
| **Step 3: Verify digest availability in local registry** - Check that target upgrade images are available in local mirror: `oc image info <local-registry>/ocp-release@sha256:<digest> --context=<managed-cluster-context>` | Local registry contains the required image digest for upgrade. Image info shows digest, layers, and manifest confirming availability in disconnected environment. |
| **Step 4: Create ClusterCurator for disconnected upgrade** - Apply ClusterCurator with non-recommended annotation for disconnected upgrade: `oc apply -f -` | ClusterCurator created successfully and configured for disconnected environment operation. Resource validates and begins processing with local registry configuration. |
| **Step 5: Monitor image pull from local registry** - Watch upgrade process to confirm images pulled from local registry: `oc logs -f job/curator-job-<hash> -n cluster1` | Upgrade process shows image pulls from local registry rather than external sources. Logs confirm successful image retrieval from disconnected registry using digest-based references. |
| **Step 6: Validate upgrade completion in disconnected mode** - Confirm upgrade succeeds using only local resources: `oc get clusterversion version --context=<managed-cluster-context>` | Upgrade completes successfully using only local registry resources. ClusterVersion shows target version achieved without external connectivity, validating disconnected environment support. |
| **Step 7: Verify digest persistence** - Confirm upgrade used digest format throughout process: `oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' --context=<managed-cluster-context>` | Final upgrade configuration shows digest-based image reference from local registry. Output confirms digest format was maintained throughout the disconnected upgrade process. |