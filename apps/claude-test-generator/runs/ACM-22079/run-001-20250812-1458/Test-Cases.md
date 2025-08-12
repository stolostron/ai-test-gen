# E2E Test Cases: ACM-22079 - Digest-based Upgrades via ClusterCurator

## Test Case 1: Basic Digest-based Upgrade with conditionalUpdates

### Description
Test ClusterCurator digest-based upgrade functionality using the primary digest resolution path from ClusterVersion conditionalUpdates list. This validates the core feature of ACM-22079 for non-recommended OpenShift upgrades in disconnected environments.

### Setup
- Target managed cluster with OpenShift 4.16.x or 4.17.x 
- ClusterVersion status contains conditionalUpdates with digest information
- ACM hub cluster with ClusterCurator functionality available
- Ansible Tower integration configured (optional for minimal testing)

### Test Steps

| Step | Action | Command/UI | Expected Result |
|------|--------|------------|----------------|
| 1 | Login to ACM hub cluster | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully authenticated to hub cluster |
| 2 | Verify target managed cluster availability | `oc get managedclusters` | Target cluster shows HUB ACCEPTED=true, AVAILABLE=true |
| 3 | Check ClusterVersion conditionalUpdates on target cluster | `oc get managedclusterview -n <target-cluster> view-clusterversion -o yaml \| grep -A20 conditionalUpdates` | ClusterVersion contains conditionalUpdates array with target version and image digest |
| 4 | Create ClusterCurator with digest upgrade annotation | `oc apply -f clustercurator-digest-upgrade.yaml` | ClusterCurator resource created successfully |
| 5 | Monitor ClusterCurator job creation | `oc get jobs -n <target-cluster> \| grep curator` | Curator job created and running within 30 seconds |
| 6 | Monitor upgrade progress | `oc get clustercurator <name> -n <target-cluster> -o yaml \| grep -A10 conditions` | Conditions show "UpgradeJobCompleted: True" within timeout period |
| 7 | Verify digest was used in upgrade | `oc logs -n <target-cluster> job/<curator-job-name> \| grep -i digest` | Log shows image digest from conditionalUpdates was used |
| 8 | Validate post-upgrade cluster version | `oc get managedclusterview -n <target-cluster> view-clusterversion -o yaml \| grep -A5 "version:"` | Cluster version matches desired version from ClusterCurator spec |

### Expected ClusterCurator YAML
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: digest-upgrade-test-1
  namespace: target-cluster
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-force: "true"
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.37"
    monitorTimeout: 120
    towerAuthSecret: ""
    prehook: []
    posthook: []
```

### Expected Results
- **Successful Digest Resolution**: ClusterCurator extracts image digest from conditionalUpdates
- **Upgrade Execution**: ManagedClusterAction created with digest-based image reference  
- **Version Validation**: Post-upgrade ClusterVersion.status.desired.version matches target
- **Status Conditions**: ClusterCurator conditions reflect successful upgrade completion

---

## Test Case 2: Fallback to availableUpdates Digest Resolution  

### Description
Test ClusterCurator digest resolution fallback mechanism when target version exists in availableUpdates but not in conditionalUpdates. This validates the second tier of the digest resolution hierarchy.

### Setup
- Target managed cluster where desired version exists in availableUpdates only
- ClusterVersion conditionalUpdates does not contain target version
- Same ACM hub setup as Test Case 1

### Test Steps

| Step | Action | Command/UI | Expected Result |
|------|--------|------------|----------------|
| 1 | Login to ACM hub cluster | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully authenticated to hub cluster |
| 2 | Verify target cluster ClusterVersion structure | `oc get managedclusterview -n <target-cluster> view-clusterversion -o yaml` | Target version exists in availableUpdates, not in conditionalUpdates |
| 3 | Create ClusterCurator for availableUpdates version | `oc apply -f clustercurator-fallback-test.yaml` | ClusterCurator created targeting version in availableUpdates |
| 4 | Monitor curator job logs for fallback behavior | `oc logs -n <target-cluster> job/<curator-job> -f` | Logs show "digest not found in conditionalUpdates, checking availableUpdates" |
| 5 | Verify digest extraction from availableUpdates | `oc logs -n <target-cluster> job/<curator-job> \| grep -A2 -B2 availableUpdates` | Successfully extracted digest from availableUpdates list |
| 6 | Monitor upgrade execution | `oc get clustercurator <name> -n <target-cluster> -o yaml \| grep -A5 conditions` | Upgrade progresses using digest from availableUpdates |
| 7 | Validate successful upgrade completion | `oc get managedclusterview -n <target-cluster> view-clusterversion -o yaml \| grep version` | Cluster upgraded to target version using availableUpdates digest |

### Expected ClusterCurator YAML
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: fallback-digest-test
  namespace: target-cluster
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-force: "true"
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.35"  # Version in availableUpdates only
    monitorTimeout: 120
```

### Expected Results
- **Fallback Logic**: Primary conditionalUpdates check fails gracefully
- **Secondary Resolution**: Digest successfully extracted from availableUpdates
- **Upgrade Success**: Cluster upgraded using fallback digest resolution
- **Logging Transparency**: Clear logs showing fallback decision path

---

## Test Case 3: Image Tag Fallback for Backward Compatibility

### Description  
Test ClusterCurator fallback to image tag format when digest resolution fails for both conditionalUpdates and availableUpdates. This validates the tertiary fallback mechanism ensuring backward compatibility.

### Setup
- Target managed cluster where desired version not available in either conditionalUpdates or availableUpdates
- Registry access to quay.io/openshift-release-dev/ocp-release for tag-based images
- ACM hub with ClusterCurator configured for non-recommended upgrades

### Test Steps

| Step | Action | Command/UI | Expected Result |
|------|--------|------------|----------------|
| 1 | Login to ACM hub cluster | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully authenticated to hub cluster |
| 2 | Verify target version not in ClusterVersion updates | `oc get managedclusterview -n <target-cluster> view-clusterversion -o yaml \| grep -A20 -E "(conditionalUpdates\|availableUpdates)"` | Target version "4.15.25" not found in either updates list |
| 3 | Create ClusterCurator for unsupported version | `oc apply -f clustercurator-tag-fallback.yaml` | ClusterCurator created for version not in updates |
| 4 | Monitor curator job for tag fallback | `oc logs -n <target-cluster> job/<curator-job> -f` | Logs show "digest not found, using tag fallback: quay.io/openshift-release-dev/ocp-release:4.15.25-multi" |
| 5 | Verify ManagedClusterAction uses tag format | `oc get managedclusteraction -n <target-cluster> -o yaml \| grep image` | ManagedClusterAction contains tag-based image reference |
| 6 | Monitor upgrade attempt with tag format | `oc get clustercurator <name> -n <target-cluster> -o yaml \| grep -A10 conditions` | Upgrade proceeds using tag format (may succeed or fail based on image availability) |
| 7 | Document tag fallback behavior | `oc get events -n <target-cluster> --sort-by='.lastTimestamp' \| grep curator` | Events show tag-based upgrade attempt and result |

### Expected ClusterCurator YAML
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: tag-fallback-test  
  namespace: target-cluster
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-force: "true"
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.15.25"  # Version not in any updates list
    monitorTimeout: 120
```

### Expected Results
- **Graceful Degradation**: Both digest resolution attempts fail without breaking workflow
- **Tag Generation**: Correct tag format "quay.io/openshift-release-dev/ocp-release:4.15.25-multi"
- **Backward Compatibility**: Legacy tag-based upgrade mechanism functions as fallback
- **Clear Logging**: Detailed logs explaining fallback decision and image format used

---

## Test Case 4: Annotation Dependency Validation

### Description
Test that ClusterCurator digest-based upgrade functionality requires the specific annotation "cluster.open-cluster-management.io/upgrade-allow-force: true" and fails appropriately without it.

### Setup
- Target managed cluster with available conditionalUpdates
- ClusterCurator created without required annotation
- ACM hub with standard ClusterCurator validation

### Test Steps

| Step | Action | Command/UI | Expected Result |
|------|--------|------------|----------------|
| 1 | Login to ACM hub cluster | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully authenticated to hub cluster |
| 2 | Create ClusterCurator without required annotation | `oc apply -f clustercurator-no-annotation.yaml` | ClusterCurator created but should not trigger digest upgrade |
| 3 | Monitor curator job behavior | `oc get jobs -n <target-cluster> \| grep curator` | Curator job created but should follow standard upgrade validation |
| 4 | Check for digest resolution attempt | `oc logs -n <target-cluster> job/<curator-job> \| grep -i digest` | No digest resolution logic triggered in logs |
| 5 | Verify standard validation behavior | `oc logs -n <target-cluster> job/<curator-job> \| grep -i "availableUpdates"` | Standard availableUpdates validation applied instead |
| 6 | Confirm upgrade fails for non-recommended version | `oc get clustercurator <name> -n <target-cluster> -o yaml \| grep -A5 conditions` | Conditions show upgrade failure due to version validation |
| 7 | Add annotation and retry | `oc annotate clustercurator <name> -n <target-cluster> cluster.open-cluster-management.io/upgrade-allow-force=true` | Annotation added successfully |
| 8 | Verify digest resolution now works | `oc logs -n <target-cluster> job/<new-curator-job> \| grep -i digest` | Digest resolution logic now active with annotation present |

### Expected ClusterCurator YAML (Without Annotation)
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: no-annotation-test
  namespace: target-cluster
  # Missing required annotation
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.37"
    monitorTimeout: 120
```

### Expected Results
- **Annotation Enforcement**: Digest upgrade only triggered with correct annotation
- **Standard Validation**: Normal ClusterCurator validation without annotation
- **Dynamic Behavior**: Adding annotation enables digest upgrade functionality
- **Security Model**: Prevents accidental non-recommended upgrades

---

## Test Case 5: Error Handling and Recovery Scenarios

### Description
Test ClusterCurator error handling when digest resolution encounters network issues, malformed ClusterVersion data, or invalid image references.

### Setup
- Target managed cluster with potentially unstable network or malformed data
- ACM hub configured for comprehensive logging
- Test scenarios for various failure modes

### Test Steps

| Step | Action | Command/UI | Expected Result |
|------|--------|------------|----------------|
| 1 | Login to ACM hub cluster | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully authenticated to hub cluster |
| 2 | Test ManagedClusterView failure scenario | `oc get managedclusterview -n <target-cluster> \| grep clusterversion` | Simulate ClusterVersion access failure |
| 3 | Create ClusterCurator during network issues | `oc apply -f clustercurator-error-test.yaml` | ClusterCurator created despite network challenges |
| 4 | Monitor error handling in curator job | `oc logs -n <target-cluster> job/<curator-job> -f` | Logs show "failed to get remote clusterversion" with retry attempts |
| 5 | Verify retry mechanism (5 attempts) | `oc logs -n <target-cluster> job/<curator-job> \| grep -c "retry"` | Shows 5 retry attempts before failure |
| 6 | Check ClusterCurator status conditions | `oc get clustercurator <name> -n <target-cluster> -o yaml \| grep -A10 conditions` | Conditions reflect error state with descriptive message |
| 7 | Test malformed ClusterVersion data handling | Create test with invalid JSON | Curator handles parsing errors gracefully |
| 8 | Verify recovery after issue resolution | Resolve network/data issues and monitor | New curator job succeeds after manual retry |

### Expected ClusterCurator YAML
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: error-handling-test
  namespace: target-cluster
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-force: "true"
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.37"
    monitorTimeout: 120
```

### Expected Results
- **Retry Logic**: 5 attempts for ManagedClusterView operations as per implementation
- **Error Propagation**: Clear error messages in ClusterCurator status conditions
- **Graceful Failure**: No cluster corruption during error scenarios
- **Recovery Capability**: System recovers when issues are resolved

---

## Test Execution Environment Details

**Test Environment**: qe6-vmware-ibm cluster  
**Hub Cluster**: https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443  
**ACM Version**: 2.14.0-62 (Feature targets 2.15.0)  
**MCE Version**: 2.9.0-212  
**OpenShift Version**: 4.20.0-ec.4  

**Feature Availability Note**: ACM-22079 targets ACM 2.15.0. Current environment (2.14.0-62) may not have full digest upgrade functionality implemented. Test cases are designed to validate schema compatibility and identify feature gaps for future validation when ACM 2.15.0 becomes available.

**Authentication**: Use generic login format for team usability  
**Managed Clusters**: Tests require at least one managed cluster with lower OpenShift version for upgrade scenarios