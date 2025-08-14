# ACM-22079 E2E Test Plan: Support digest-based upgrades via ClusterCurator (V3.0)

## Test Case 1: Core Digest-Based Upgrade with Non-Recommended Annotation

### Description
Validate that ClusterCurator successfully performs an upgrade to a non-recommended OpenShift version using image digest when the non-recommended annotation is present and the three-tier search mechanism functions correctly.

### Setup
- Managed cluster running OpenShift 4.16.36 with available non-recommended updates
- ACM hub cluster with ClusterCurator functionality enabled
- Access to non-recommended target version (e.g., 4.16.37) in conditionalUpdates list

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully authenticated to the hub cluster with cluster administrator privileges. Terminal displays successful login confirmation with cluster API URL and user context verification. |
| **Step 2: Verify managed cluster current version and conditional updates** - Check the current OpenShift version and available conditional updates: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | Current cluster version displays as 4.16.36 with conditionalUpdates list containing non-recommended versions. Output shows available conditional updates with image digests for target versions. ```yaml status: history: - state: "Completed" version: "4.16.36" conditionalUpdates: - image: "quay.io/openshift-release-dev/ocp-release@sha256:abc123..." version: "4.16.37" ``` |
| **Step 3: Create ClusterCurator with non-recommended annotation** - Apply ClusterCurator resource with digest-based upgrade configuration: `oc apply -f -` with YAML containing non-recommended annotation and target version | ClusterCurator resource successfully created and accepted by API server. Resource validates successfully and shows "clustercurator.cluster.open-cluster-management.io/cluster1 created" confirmation message. ```yaml apiVersion: cluster.open-cluster-management.io/v1beta1 kind: ClusterCurator metadata: annotations: cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true' name: cluster1 namespace: cluster1 spec: desiredCuration: upgrade upgrade: desiredUpdate: 4.16.37 monitorTimeout: 120 ``` |
| **Step 4: Monitor ClusterCurator job creation and execution** - Track curator job startup and processing: `oc get jobs -n cluster1 -w` | ClusterCurator job created and starts running with active status. Job displays as "curator-job-<hash>" with COMPLETIONS 0/1 and AGE showing recent creation timestamp indicating processing has begun. |
| **Step 5: Verify digest retrieval from conditionalUpdates** - Confirm ClusterCurator found image digest in primary source: `oc logs job/curator-job-<hash> -n cluster1` | Curator job logs show successful digest discovery in conditionalUpdates list. Logs display "Found image digest in conditionalUpdates for version 4.16.37" with specific digest hash confirmation from primary search tier. |
| **Step 6: Validate managed cluster upgrade initiation** - Check that managed cluster received digest-based upgrade instruction: `oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' --context=<managed-cluster-context>` | Managed cluster ClusterVersion shows image digest format instead of version tag. Output displays `quay.io/openshift-release-dev/ocp-release@sha256:abc123...` confirming digest-based upgrade mechanism activated successfully. |
| **Step 7: Monitor upgrade progress through phases** - Track upgrade progression on managed cluster: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | Upgrade progresses through expected phases with status showing Progressing → Partial → Complete transitions. ClusterVersion conditions indicate normal upgrade progression with digest-based image reference maintained throughout process. |
| **Step 8: Verify successful upgrade completion** - Confirm cluster upgraded to target version: `oc get nodes --context=<managed-cluster-context>` and `oc get clusterversion version --context=<managed-cluster-context>` | All nodes display target version 4.16.37 and ClusterVersion status shows successful completion. History entry added for completed upgrade with digest-based upgrade confirmed successful and cluster operational. |

## Test Case 2: Fallback Mechanism Validation - availableUpdates Search

### Description
Verify the three-tier search mechanism functions correctly when target version is not available in conditionalUpdates but exists in availableUpdates, testing the intelligent fallback logic.

### Setup
- Managed cluster with limited conditionalUpdates but broader availableUpdates list
- Target version available in availableUpdates but not conditionalUpdates

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully authenticated to hub cluster with administrative access to manage ClusterCurator resources and monitor managed cluster operations. |
| **Step 2: Examine update sources and identify fallback scenario** - Review conditionalUpdates and availableUpdates lists: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | ClusterVersion displays empty conditionalUpdates but populated availableUpdates containing target version. Ideal test scenario for fallback mechanism validation with clear source differentiation. ```yaml status: conditionalUpdates: [] availableUpdates: - image: "quay.io/openshift-release-dev/ocp-release@sha256:def456..." version: "4.16.38" ``` |
| **Step 3: Create ClusterCurator targeting availableUpdates version** - Apply ClusterCurator for version only in availableUpdates: `oc apply -f -` | ClusterCurator resource created successfully targeting version that will trigger fallback search mechanism to secondary tier (availableUpdates) validation. |
| **Step 4: Monitor curator job logs for fallback behavior** - Watch job execution for search progression: `oc logs -f job/curator-job-<hash> -n cluster1` | Job logs demonstrate three-tier search sequence: "Searching conditionalUpdates for 4.16.38... not found", "Searching availableUpdates... found digest", confirming intelligent fallback mechanism operation. |
| **Step 5: Verify digest retrieval from secondary source** - Confirm correct digest obtained from availableUpdates: `oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' --context=<managed-cluster-context>` | Managed cluster receives correct image digest from availableUpdates list. Output matches expected sha256 digest from secondary search tier confirming fallback mechanism successful operation. |
| **Step 6: Validate normal upgrade progression** - Monitor upgrade continues successfully despite fallback source: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | Upgrade proceeds normally using digest from availableUpdates with standard progression phases. Status conditions show normal upgrade progression confirming fallback mechanism maintains upgrade reliability and integrity. |

## Test Case 3: Final Fallback to Image Tag Mechanism

### Description
Test system behavior when neither conditionalUpdates nor availableUpdates contain the requested version, forcing final fallback to image tag for backward compatibility validation.

### Setup
- Managed cluster with limited update options
- Target version not available in either conditional or available updates lists

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully authenticated to hub cluster with proper administrative privileges to create ClusterCurator resources and monitor upgrade operations across managed clusters. |
| **Step 2: Identify version requiring image tag fallback** - Find version not in either update list: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | ClusterVersion output shows current conditionalUpdates and availableUpdates lists without target version. Scenario confirmed for testing final tier fallback mechanism to image tag format. |
| **Step 3: Create ClusterCurator with unlisted version** - Apply ClusterCurator targeting version requiring final fallback: `oc apply -f -` | ClusterCurator resource created successfully with target version that will force three-tier search to complete cycle and use image tag fallback mechanism. |
| **Step 4: Monitor complete search sequence execution** - Watch job logs for full three-tier search: `oc logs -f job/curator-job-<hash> -n cluster1` | Job logs show complete search progression: "Checking conditionalUpdates... not found", "Checking availableUpdates... not found", "Using image tag fallback for version 4.16.39", demonstrating complete three-tier mechanism. |
| **Step 5: Verify image tag format usage** - Check managed cluster uses tag instead of digest: `oc get clusterversion version -o jsonpath='{.spec.desiredUpdate}' --context=<managed-cluster-context>` | ClusterVersion desiredUpdate shows version tag format rather than digest. Output displays `{"version": "4.16.39"}` confirming final fallback tier activated successfully with backward compatibility maintained. |
| **Step 6: Validate upgrade attempt or appropriate error handling** - Monitor system response to tag-based upgrade: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` | System either attempts upgrade with image tag or provides clear error messaging about version availability. Status conditions show appropriate response with clear error reporting if version truly unavailable or upgrade attempt if accessible. |

## Test Case 4: Rollback and Error Recovery Procedures

### Description
Verify comprehensive rollback capabilities and intelligent error recovery when digest-based upgrades encounter issues, testing system resilience and recovery mechanisms.

### Setup
- Managed cluster with successful initial state
- Ability to simulate upgrade failure scenarios for recovery testing

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully authenticated to hub cluster with comprehensive administrative privileges to manage ClusterCurator resources and execute upgrade rollback operations. |
| **Step 2: Document pre-upgrade cluster baseline** - Record complete cluster state before upgrade attempt: `oc get clusterversion version -o yaml --context=<managed-cluster-context>` and `oc get nodes --context=<managed-cluster-context>` | Complete baseline documentation captured showing current version, node status, and system health indicators. Pre-upgrade state recorded for rollback reference and recovery validation procedures. ```yaml status: history: - state: "Completed" version: "4.16.36" startedTime: "2025-08-14T14:00:00Z" ``` |
| **Step 3: Initiate controlled upgrade failure scenario** - Create ClusterCurator with problematic configuration for recovery testing: `oc apply -f -` | ClusterCurator created with configuration designed to test error handling and recovery mechanisms. Initial validation passes but upgrade encounters controlled issues for recovery testing. |
| **Step 4: Monitor and identify upgrade failure conditions** - Track upgrade issues and failure detection: `oc get clusterversion version -w --context=<managed-cluster-context>` | Upgrade failure detected through ClusterVersion conditions showing degraded state. Status displays error conditions requiring rollback intervention with clear failure indicators and diagnostic information. ```yaml conditions: - type: "Failing" status: "True" message: "Upgrade failed: unable to complete digest-based upgrade" ``` |
| **Step 5: Execute rollback operation using ClusterCurator** - Create rollback ClusterCurator to restore previous version: `oc apply -f -` with ClusterCurator specifying previous stable version | Rollback ClusterCurator created successfully and initiates downgrade process. Job starts processing rollback operation with clear confirmation of restoration to previous known-good configuration state. |
| **Step 6: Verify complete rollback success** - Confirm cluster restoration to stable state: `oc get clusterversion version --context=<managed-cluster-context>` and `oc get nodes --context=<managed-cluster-context>` | Cluster successfully returned to baseline version 4.16.36 with all nodes healthy. ClusterVersion history shows rollback completion and system fully restored to pre-upgrade stable operational state. |
| **Step 7: Validate post-rollback system functionality** - Test critical cluster operations after recovery: `oc get pods --all-namespaces --context=<managed-cluster-context>` | All critical cluster services running normally after rollback operation. System pods display healthy running status and cluster demonstrates full operational capability with complete functionality restoration. |

## Test Case 5: Disconnected Environment Simulation and Validation

### Description
Validate digest-based upgrade functionality in simulated disconnected environment conditions, testing the core use case for which this feature was specifically developed.

### Setup
- Managed cluster configured for disconnected operation with restricted network access
- Local registry with mirrored images containing target upgrade content
- ClusterCurator configured for disconnected environment operations

### Test Steps

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successfully authenticated to hub cluster with access to disconnected environment management capabilities and ClusterCurator resources for disconnected operations. |
| **Step 2: Configure disconnected registry and validate image availability** - Set up and verify local registry configuration: `oc get imagecontentsourcepolicy --context=<managed-cluster-context>` | Disconnected environment properly configured with local registry mirroring setup. Image content source policies direct pulls to local mirror registry rather than external repositories. ```yaml apiVersion: operator.openshift.io/v1alpha1 kind: ImageContentSourcePolicy metadata: name: mirror-config spec: repositoryDigestMirrors: - mirrors: ["local-registry.example.com/openshift"] source: "quay.io/openshift-release-dev" ``` |
| **Step 3: Verify target upgrade images in local registry** - Confirm required upgrade images available locally: `oc image info <local-registry>/ocp-release@sha256:<digest> --context=<managed-cluster-context>` | Local registry contains required image digest for upgrade operation. Image information displays digest, layers, and manifest data confirming complete availability in disconnected environment. |
| **Step 4: Create ClusterCurator for disconnected digest upgrade** - Apply ClusterCurator configured for disconnected operation: `oc apply -f -` | ClusterCurator created successfully and configured for disconnected environment upgrade operation. Resource validates and begins processing with local registry configuration and disconnected settings. |
| **Step 5: Monitor image retrieval from local registry during upgrade** - Watch upgrade process for local image usage: `oc logs -f job/curator-job-<hash> -n cluster1` | Upgrade process shows image pulls exclusively from local registry without external connectivity attempts. Logs confirm successful digest-based image retrieval from disconnected mirror registry. |
| **Step 6: Validate successful disconnected upgrade completion** - Confirm upgrade success using only local resources: `oc get clusterversion version --context=<managed-cluster-context>` | Upgrade completes successfully using exclusively local registry resources without external dependencies. ClusterVersion shows target version achieved validating complete disconnected environment functionality. |
| **Step 7: Verify digest persistence throughout disconnected process** - Confirm digest format maintained in disconnected operation: `oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' --context=<managed-cluster-context>` | Final configuration shows digest-based image reference from local registry throughout process. Output confirms digest format maintained validating disconnected upgrade using image digest mechanism successfully. |