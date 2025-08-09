Based on my analysis of the validation failures, here are the **critical content improvements** needed while preserving the exact `| Test Steps | Expected Results |` table format:

## Key Validation Issues Addressed:

### 1. **ClusterCurator Resource Definition Fixed**
- **Problem**: Invalid resource schemas causing creation failures
- **Solution**: Added required fields like `channel`, `install.towerAuthSecret`, and proper API version
- **Improved YAML**:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: test-digest-upgrade
  namespace: managed-cluster-1
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.15.10"
    channel: "stable-4.15"  # ADDED: Required field
  install:
    towerAuthSecret: ""     # ADDED: Required field
```

### 2. **Command Accuracy and API Schema Updates**
- **Problem**: Commands using outdated API resource names
- **Fixed Commands**:
  - `oc auth can-i create clustercurator` → `oc auth can-i create clustercurators.cluster.open-cluster-management.io`
  - Added proper schema validation: `oc get crd clustercurators.cluster.open-cluster-management.io -o yaml | grep -A3 "served: true"`
  - Enhanced connectivity checks: `oc cluster-info && oc get nodes`

### 3. **Expected Results Specificity Enhanced**
- **Problem**: Vague expected results lacking specific validation criteria
- **Improved Examples**:
  - Vague: "ClusterCurator created" 
  - **Specific**: "ClusterCurator created successfully and enters Pending phase: `clustercurator.cluster.open-cluster-management.io/test-digest-upgrade created`. Verify status: `oc get clustercurator test-digest-upgrade -o jsonpath='{.status.conditions[0].type}'` shows `Ready` or `Running`"

### 4. **Status Structure Validation Added**
- **Problem**: Missing validation of actual API response structures
- **Enhanced Validations**:
  - Digest format verification: `quay.io/openshift-release-dev/ocp-release@sha256:[64-char-hex]` (must contain '@sha256:')
  - ManagedClusterAction structure: `spec.actionRequest.object.spec.desiredUpdate` contains digest format AND `spec.actionRequest.object.spec.force` is `false`
  - Condition types: Check for `Ready`, `Running`, `Failed` in `status.conditions`

### 5. **Error Handling and Cleanup Procedures**
- **Added Comprehensive Cleanup**:
  - Verification steps: `oc get clustercurator test-digest-upgrade || echo "Successfully deleted"`
  - Namespace cleanup with verification: `oc delete namespace fallback-test && oc get clustercurator -n managed-cluster-1 | grep test-fallback || echo "All test resources removed"`
  - RBAC cleanup verification: `oc get clusterrole clustercurator-limited || echo "Cleanup successful"`

### 6. **Missing Test Scenarios Added**
- **Multi-cluster concurrency testing** with proper namespace isolation
- **Mirror registry validation** for disconnected environments  
- **RBAC security boundaries** with service account testing
- **Error condition handling** with proper status validation

## **Format Preservation Maintained:**
✅ Exact `| Test Steps | Expected Results |` table structure preserved  
✅ Setup sections kept as bullet points  
✅ Test case organization and numbering maintained  
✅ No changes to table format or structure  

These improvements directly address the validation failures:
- **test_logic**: Fixed invalid resource definitions and commands
- **expected_results**: Enhanced specificity and API structure validation  
- **Root cause**: Updated schemas and added missing required fields

The improved test plan maintains the exact format while providing actionable, executable test steps that will pass validation.
