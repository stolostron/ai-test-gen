# ACM-22079: Support Digest-based Upgrades via ClusterCurator Test Plan

## Feature Analysis Summary

**JIRA Ticket**: ACM-22079 - Support digest-based upgrades via ClusterCurator for non-recommended upgrades  
**Implementation**: PR #468 in stolostron/cluster-curator-controller repository  
**Merge Date**: July 16, 2025 (commit: be3fbc09bd07df17c33ff3535c34a71eb73de28a)  
**Business Value**: Enables Amadeus and other customers to use digest-based upgrades in disconnected environments

### Key Functionality
- Uses image digests from ClusterVersion conditionalUpdates when non-recommended annotation is present
- Fallback logic: conditionalUpdates → availableUpdates → image tag
- Annotation required: `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`

## Feature Availability Analysis

**Implementation Status**: ✅ Merged to main (commit: be3fbc09, July 16, 2025)  
**Current qe6 Environment**: ❌ Missing feature (cluster-curator-controller image: sha256:902c5b3b4a4e8cb0a14fa5aba8451ec02830d5167ff1b91323ded62255983cd9)  
**Test Execution**: 🔄 Test plans ready, requires environment update  
**Expected Availability**: Next qe6 deployment cycle (estimate: 1-2 weeks)

### Environment Validation Results
- ✅ ClusterCurator CRD installed: `clustercurators.cluster.open-cluster-management.io`
- ✅ Managed clusters available: `local-cluster`, `clc-aws-1754653080744`
- ✅ Current OCP version: 4.19.6
- ❌ Feature implementation missing in current cluster-curator-controller deployment

---

## Test Plan

### Test Case 1: Basic Non-Recommended Upgrade with Digest Support
**Description**: 
- Verify ClusterCurator can upgrade a managed cluster to a non-recommended version using image digest
- Test the core functionality where digest is preferred over image tag for non-recommended upgrades

**Setup**: 
- Hub cluster with ACM/MCE installed
- At least one managed cluster available for upgrade testing
- ClusterCurator operator deployed and functional

| Test Steps | Expected Results |
|------------|------------------|
| 1. `oc get managedclusters` | List available managed clusters |
| 2. `oc get clusterversion -o yaml` on managed cluster | Note current version and conditionalUpdates list |
| 3. Create ClusterCurator with non-recommended annotation: `kubectl apply -f clustercurator-digest-upgrade.yaml` | ClusterCurator resource created successfully |
| 4. `oc get clustercurator <cluster-name> -o yaml` | Verify annotation `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'` is present |
| 5. `oc get jobs -n <cluster-namespace>` | ClusterCurator job created and running |
| 6. Monitor job logs: `oc logs job/<curator-job-name> -n <cluster-namespace>` | Logs show checking conditionalUpdates for image digest |
| 7. `oc get clusterversion -o yaml` on managed cluster | spec.desiredUpdate.image contains digest (sha256:...) not tag |
| 8. Wait for upgrade completion: `oc get clusterversion` | status.desired.version matches target non-recommended version |

### Test Case 2: Fallback Mechanism Validation
**Description**:
- Verify the fallback logic when digest is not found in conditionalUpdates
- Test behavior when availableUpdates or image tag must be used

**Setup**:
- Hub cluster with managed cluster
- Target version not present in conditionalUpdates list

| Test Steps | Expected Results |
|------------|------------------|
| 1. Identify version not in conditionalUpdates: `oc get clusterversion -o jsonpath='{.status.conditionalUpdates}'` | List current conditionalUpdates |
| 2. Create ClusterCurator for version not in conditionalUpdates | ClusterCurator created with non-recommended annotation |
| 3. Monitor curator job execution: `oc logs job/<curator-job> -f` | Logs show "not found in conditionalUpdates, checking availableUpdates" |
| 4. `oc get clusterversion -o yaml` on managed cluster | If availableUpdates has digest, uses digest; otherwise uses image tag |
| 5. Verify upgrade progresses | Upgrade initiated with appropriate image reference |

### Test Case 3: Annotation Requirement Validation
**Description**:
- Verify that digest-based logic only applies when non-recommended annotation is present
- Test behavior without the required annotation

**Setup**:
- Managed cluster ready for upgrade
- ClusterCurator without non-recommended annotation

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create ClusterCurator without annotation: `kubectl apply -f clustercurator-no-annotation.yaml` | ClusterCurator created without non-recommended annotation |
| 2. `oc get clustercurator <cluster-name> -o yaml` | Confirm annotation is absent |
| 3. Monitor job behavior: `oc logs job/<curator-job>` | Standard upgrade logic used, no digest preference |
| 4. `oc get clusterversion -o yaml` on managed cluster | Standard image tag used in spec.desiredUpdate.image |
| 5. Add annotation to existing ClusterCurator: `kubectl annotate clustercurator <name> cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions=true` | Annotation added successfully |
| 6. Monitor subsequent job execution | Digest-based logic now activated |

### Test Case 4: Digest Extraction and Validation
**Description**:
- Verify ClusterCurator correctly identifies and uses digest from conditionalUpdates
- Validate the specific digest format and extraction logic

**Setup**:
- Hub cluster with OCP version that has conditionalUpdates containing non-recommended versions
- Access to cluster with available version upgrades

| Test Steps | Expected Results |
|------------|------------------|
| 1. `oc get clusterversion -o jsonpath='{.status.conditionalUpdates[*].release.image}'` | List digest-based images in conditionalUpdates |
| 2. `oc get clusterversion -o jsonpath='{.status.conditionalUpdates[?(@.release.version=="4.16.37")].release.image}'` | Extract specific digest for target version |
| 3. Create ClusterCurator targeting version from conditionalUpdates | ClusterCurator created with annotation |
| 4. `oc describe clustercurator <name> -n <namespace>` | Events show digest extraction process |
| 5. Monitor upgrade initiation: `oc get clusterversion -o jsonpath='{.spec.desiredUpdate.image}'` | Image field contains sha256 digest, not version tag |
| 6. `oc get events --field-selector involvedObject.kind=ClusterCurator` | Events log digest vs tag decision process |

### Test Case 5: Disconnected Environment Simulation
**Description**:
- Test the feature's primary use case for disconnected/air-gapped environments like Amadeus
- Verify digest-based upgrades work when image tags are not accessible

**Setup**:
- Managed cluster configured for disconnected operation
- Mirror registry with digest-based image references

| Test Steps | Expected Results |
|------------|------------------|
| 1. `oc get imagecontentsourcepolicy` or `oc get imagedigestmirrorset` | Verify mirror configuration exists |
| 2. Create ClusterCurator with non-recommended version and annotation | ClusterCurator uses digest from conditionalUpdates |
| 3. `oc logs job/<curator-job> -n <cluster-namespace>` | Logs show successful digest resolution |
| 4. `oc get clusterversion -o yaml \| grep "image:"` | Confirms digest format: `image: registry.mirror.com/...@sha256:...` |
| 5. Monitor upgrade progress: `oc get co` | Cluster operators update successfully using mirrored digest |
| 6. `oc get clusterversion -o jsonpath='{.status.history[0].image}'` | Completed upgrade shows digest reference |

### Test Case 6: Error Handling and Fallback Scenarios
**Description**:
- Test error conditions and validate proper fallback behavior
- Ensure graceful degradation when digest lookup fails

**Setup**:
- Scenarios with missing or invalid digest references
- Test edge cases in the fallback logic

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create ClusterCurator with non-existent version in conditionalUpdates | Job attempts conditionalUpdates lookup first |
| 2. Monitor curator logs: `oc logs job/<curator-job> --follow` | "Version not found in conditionalUpdates, checking availableUpdates" |
| 3. Create scenario with malformed digest in conditionalUpdates | Curator falls back to availableUpdates or image tag |
| 4. `oc describe clustercurator <name>` | Status conditions show fallback reason |
| 5. Test without annotation: Remove `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions` | Standard upgrade logic used, no digest preference |
| 6. `oc get clustercurator <name> -o jsonpath='{.status.conditions[?(@.type=="clustercurator-job")].message}'` | Clear error messages for troubleshooting |

---

## Sample ClusterCurator Resources

### Basic Non-Recommended Upgrade with Digest Support
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'
  name: cluster1-digest-upgrade
  namespace: cluster1
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: 4.16.37
    monitorTimeout: 120
```

### Standard Upgrade (No Digest Logic)
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: cluster1-standard-upgrade
  namespace: cluster1
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: 4.16.38
    monitorTimeout: 120
```

---

## Linked JIRA Tickets Analysis

- **ACM-22080** [QE]: Test case created for non-recommended version upgrades with digest validation
- **ACM-22081** [QE Automation]: Automation required for digest-based upgrade testing
- **ACM-22457** [Documentation]: Documentation task for ClusterCurator upgrade procedures

---

## Testing Readiness

**Current Status**: Test plans are complete and validated for structure. Ready for execution once cluster-curator-controller is updated with ACM-22079 implementation.

**Next Steps**:
1. Monitor qe6 cluster for deployment updates including commit be3fbc09 or later
2. Execute test cases once feature is available
3. Document actual test results and any environment-specific adaptations needed

**Alternative Testing Environments**:
- Local development environment with latest cluster-curator-controller build
- Validation environment with nightly builds
- Manual deployment of updated cluster-curator-controller image to existing environment