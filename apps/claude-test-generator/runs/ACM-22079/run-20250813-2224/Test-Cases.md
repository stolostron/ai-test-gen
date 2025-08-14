# Test Cases: ACM-22079 - Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Test Case 1: Basic Non-Recommended Upgrade with Digest-Based Discovery

**Description:** Verify ClusterCurator can perform a non-recommended upgrade using image digest discovery from conditionalUpdates list.

**Setup:** 
- OpenShift cluster with ACM/MCE deployed
- ClusterCurator CRD available
- Target managed cluster accessible for upgrade testing

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful login to ACM hub cluster. Terminal shows: `Login successful. You have access to X projects.` |
| **Step 2: Create test namespace for ClusterCurator** - Create a dedicated namespace: `oc create namespace test-digest-upgrade` | Namespace created successfully. Command output shows: `namespace/test-digest-upgrade created` |
| **Step 3: Check current OpenShift version on managed cluster** - Verify current version using ManagedClusterView: `oc apply -f managed-cluster-version-view.yaml` | ManagedClusterView created showing current cluster version. Output displays current OpenShift version like `4.16.36` in the ClusterVersion resource. |
| **Step 4: Identify non-recommended upgrade target** - Check available updates: `oc get clusterversion cluster -o yaml` | Available and conditional updates list displayed. Shows non-recommended versions in conditionalUpdates section with image digests and version information. |
| **Step 5: Create ClusterCurator with non-recommended annotation** - Apply the ClusterCurator resource with digest upgrade configuration | ClusterCurator resource created successfully. Server validates the annotation and upgrade configuration. Resource shows `clustercurator.cluster.open-cluster-management.io/test-upgrade created`. |
| **Step 6: Monitor ClusterCurator job creation** - Check for curator job: `oc get jobs -n test-digest-upgrade` | Curator job created and initiated. Job shows status `ACTIVE` with 1 running pod. Job name follows pattern `curator-job-<cluster-name>-<timestamp>`. |
| **Step 7: Verify image digest usage in upgrade process** - Check ClusterVersion spec on managed cluster: `oc get clusterversion cluster -o yaml` | ClusterVersion resource shows `spec.desiredUpdate.image` contains image digest (sha256:...) instead of version tag. This confirms digest-based upgrade initiation. |
| **Step 8: Monitor upgrade progress** - Track upgrade status: `oc get clusterversion cluster -o yaml \| grep -A 5 status` | Upgrade progress displayed with image digest reference. Status shows progression through upgrade phases with digest-based update mechanism active. |

## Test Case 2: Fallback to Available Updates When Conditional Updates Missing

**Description:** Verify ClusterCurator falls back to availableUpdates list when conditionalUpdates doesn't contain the target version.

**Setup:**
- OpenShift cluster with standard available updates
- Target version present in availableUpdates but not conditionalUpdates
- ClusterCurator configured with non-recommended annotation

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to ACM hub. Terminal displays: `Login successful. You have access to X projects.` |
| **Step 2: Create test namespace** - Set up isolated testing environment: `oc create namespace fallback-upgrade-test` | Test namespace created. Output confirms: `namespace/fallback-upgrade-test created` |
| **Step 3: Verify availableUpdates contains target version** - Check available updates: `oc get clusterversion cluster -o jsonpath='{.status.availableUpdates}'` | Available updates list shows target version with image information. JSON output contains version entries with image references for fallback testing. |
| **Step 4: Confirm conditionalUpdates is empty or missing target** - Check conditional updates: `oc get clusterversion cluster -o jsonpath='{.status.conditionalUpdates}'` | Conditional updates empty or target version absent. This ensures fallback mechanism will be triggered during upgrade process. |
| **Step 5: Apply ClusterCurator with available version** - Create ClusterCurator targeting version in availableUpdates | ClusterCurator validates and accepts configuration. Resource creation shows successful validation of fallback scenario setup. |
| **Step 6: Monitor curator job execution** - Track job creation: `oc get jobs -n fallback-upgrade-test -w` | Job initiates and processes fallback logic. Job logs show progression through conditional updates check then fallback to available updates discovery. |
| **Step 7: Verify fallback mechanism activation** - Check curator logs: `oc logs -n multicluster-engine -l app=cluster-curator-controller` | Logs show fallback from conditionalUpdates to availableUpdates. Log entries indicate digest discovery from available updates list for target version. |
| **Step 8: Confirm image digest extraction from availableUpdates** - Verify managed cluster ClusterVersion: `oc get clusterversion cluster -o yaml` | ClusterVersion shows image digest from availableUpdates in spec.desiredUpdate.image field. Confirms fallback mechanism successfully extracted digest reference. |

## Test Case 3: Image Tag Fallback for Backward Compatibility

**Description:** Test the final fallback to image tag when neither conditionalUpdates nor availableUpdates contain the target version.

**Setup:**
- ClusterCurator configured with version not in any updates list
- Backward compatibility scenario testing
- Non-recommended annotation enabled

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Authenticated access to ACM hub cluster. Login confirmation: `Login successful. You have access to X projects, the list has been suppressed.` |
| **Step 2: Create namespace for compatibility test** - Establish test environment: `oc create namespace tag-fallback-test` | Test namespace ready for compatibility testing. Command output: `namespace/tag-fallback-test created` |
| **Step 3: Verify target version absent from all update lists** - Check both update sources: `oc get clusterversion cluster -o yaml \| grep -A 20 "availableUpdates\|conditionalUpdates"` | Both availableUpdates and conditionalUpdates empty or missing target version. This confirms image tag fallback scenario is properly configured. |
| **Step 4: Create ClusterCurator with custom version** - Apply ClusterCurator with version requiring tag fallback | ClusterCurator accepts configuration for tag-based upgrade. Resource validates despite version absence from update lists, enabling backward compatibility testing. |
| **Step 5: Monitor job initialization** - Track curator job startup: `oc get jobs -n tag-fallback-test` | Curator job starts processing tag fallback logic. Job status shows `ACTIVE` with pod executing compatibility upgrade workflow. |
| **Step 6: Verify image tag usage in upgrade** - Check managed cluster upgrade configuration: `oc get clusterversion cluster -o yaml` | ClusterVersion spec.desiredUpdate contains image tag instead of digest. Field shows traditional tag-based upgrade format for backward compatibility maintenance. |
| **Step 7: Confirm fallback logic execution** - Review curator controller logs: `oc logs -n multicluster-engine -l app=cluster-curator-controller --tail=50` | Logs demonstrate three-tier fallback execution. Log entries show progression: conditionalUpdates check → availableUpdates check → image tag fallback activation. |
| **Step 8: Validate upgrade process continuation** - Monitor upgrade status: `oc get clusterversion cluster -o jsonpath='{.status.conditions}' \| jq '.[].message'` | Upgrade proceeds using traditional tag-based mechanism. Status messages confirm upgrade process continues with legacy compatibility mode for environments lacking digest support. |

## Test Case 4: Annotation Validation and Error Handling

**Description:** Verify proper handling of the non-recommended upgrade annotation and appropriate error responses for invalid configurations.

**Setup:**
- Various ClusterCurator configurations for validation testing
- Different annotation values and formats
- Error scenario validation

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful login to ACM hub with administrative access. Terminal shows: `Login successful. You have access to X projects.` |
| **Step 2: Create validation test namespace** - Set up testing environment: `oc create namespace annotation-validation-test` | Test namespace created for annotation validation. Output confirms: `namespace/annotation-validation-test created` |
| **Step 3: Test valid annotation acceptance** - Apply ClusterCurator with correct annotation: `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'` | Annotation accepted by API server. Server-side validation passes and resource creates successfully with proper annotation recognition. |
| **Step 4: Test invalid annotation value** - Apply ClusterCurator with incorrect annotation value: `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'invalid'` | API server accepts resource but curator logic ignores invalid value. Behavior reverts to standard upgrade path without non-recommended version support. |
| **Step 5: Test missing annotation scenario** - Create ClusterCurator without the annotation | ClusterCurator follows standard upgrade workflow. No digest discovery attempted, uses traditional upgrade path through available updates only. |
| **Step 6: Verify annotation case sensitivity** - Test annotation with different case: `UPGRADE-ALLOW-NOT-RECOMMENDED-VERSIONS: 'true'` | Annotation not recognized due to case sensitivity. Controller behavior shows standard upgrade processing without non-recommended version handling activated. |
| **Step 7: Test dry-run validation** - Validate configuration before application: `oc apply --dry-run=server -f clustercurator-config.yaml` | Server-side validation confirms resource structure and annotation format. Dry-run output shows successful validation of ClusterCurator configuration with proper annotation syntax. |
| **Step 8: Monitor curator behavior with valid annotation** - Check job execution with proper annotation: `oc get jobs -n annotation-validation-test` | Curator job processes non-recommended upgrade logic. Job execution shows activation of digest discovery workflow when valid annotation present. |