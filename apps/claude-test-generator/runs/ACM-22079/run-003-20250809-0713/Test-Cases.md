# Test Cases - ACM-22079 [CORRECTED]: Limited Testing Scope

**Feature:** Support digest-based upgrades via ClusterCurator for non-recommended upgrades  
**Environment:** qe6-vmware-ibm (ACM 2.14.0, MCE 2.9.0, OpenShift 4.19.6)  
**🔴 Deployment Status:** **FEATURE NOT DEPLOYED** - Limited testing possible

**⚠️ IMPORTANT**: Core digest-based upgrade functionality is NOT deployed in qe6. These test cases focus on available functionality only.

---

## ✅ PHASE 1: Available Testing (Execute Now)

### Test Case 1: Annotation Recognition and Processing

**Description:** Validate that ClusterCurator recognizes and processes the non-recommended upgrade annotation, even though core digest logic is not implemented.

**Business Value:** Confirms infrastructure readiness for when feature is deployed.

**Limitation:** Core digest logic validation not possible in current environment.

**Setup:**
- ACM hub cluster with ClusterCurator controller running
- Access to create ClusterCurator resources in test namespace

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Create ClusterCurator with non-recommended annotation<br/>**Goal**: Verify annotation is recognized by controller<br/>**Command**: `oc apply -f -` (stdin)<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br/>  name: annotation-test<br/>  namespace: ocm<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.99.99<br/>    monitorTimeout: 5<br/>``` | ClusterCurator created successfully with annotation |
| **Step 2**: Monitor controller processing<br/>**Goal**: Verify controller recognizes resource<br/>**Command**: `oc get clustercurator annotation-test -n ocm -o yaml` | Resource shows controller processing, annotation preserved in metadata |
| **Step 3**: Check controller logs for annotation processing<br/>**Goal**: Confirm controller sees the annotation<br/>**Command**: `oc logs deployment/cluster-curator-controller -n multicluster-engine --tail=50 \| grep annotation-test` | Controller logs show resource processing |
| **Step 4**: Verify resource status conditions<br/>**Goal**: Check for any annotation-related status messages<br/>**Command**: `oc get clustercurator annotation-test -n ocm -o jsonpath='{.status.conditions[*].message}'` | Status conditions show processing results (likely failure due to invalid version) |
| **Step 5**: Test annotation value validation<br/>**Goal**: Verify annotation value handling<br/>**Command**: `oc annotate clustercurator annotation-test -n ocm cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions='false' --overwrite` | Annotation updated successfully |
| **Step 6**: Clean up test resources<br/>**Goal**: Remove test ClusterCurator<br/>**Command**: `oc delete clustercurator annotation-test -n ocm` | Resource deleted successfully |

---

### Test Case 2: Basic ClusterCurator Upgrade Infrastructure

**Description:** Validate basic ClusterCurator upgrade workflow works with standard (recommended) versions to confirm infrastructure readiness.

**Business Value:** Ensures ClusterCurator upgrade mechanism is functional before adding digest logic.

**Setup:**
- Managed cluster available for testing
- Current cluster version that has recommended upgrade path

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Identify available managed cluster<br/>**Goal**: Select cluster for basic upgrade testing<br/>**Command**: `oc get managedclusters -o jsonpath='{.items[*].metadata.name}'` | List of available managed clusters displayed |
| **Step 2**: Check managed cluster current version<br/>**Goal**: Establish baseline version<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].status.desired.version}'` | Current cluster version displayed |
| **Step 3**: Create basic ClusterCurator without annotation<br/>**Goal**: Test standard upgrade workflow<br/>**Command**: `oc apply -f -` (stdin)<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: basic-upgrade-test<br/>  namespace: <managed-cluster-namespace><br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: <recommended-version><br/>    monitorTimeout: 10<br/>``` | ClusterCurator created for standard upgrade |
| **Step 4**: Monitor curator job creation<br/>**Goal**: Verify upgrade job is created<br/>**Command**: `oc get jobs -n <managed-cluster-namespace> \| grep curator` | Curator job created by controller |
| **Step 5**: Check upgrade initiation on managed cluster<br/>**Goal**: Verify upgrade request reaches managed cluster<br/>**Command**: `oc --kubeconfig=<managed-cluster> get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate}'` | Managed cluster shows upgrade request |
| **Step 6**: Stop test upgrade and clean up<br/>**Goal**: Prevent actual upgrade completion<br/>**Command**: `oc delete clustercurator basic-upgrade-test -n <managed-cluster-namespace>` | Test resources cleaned up |

---

### Test Case 3: Error Handling and Invalid Configuration

**Description:** Test ClusterCurator error handling with invalid versions and configurations.

**Business Value:** Validates error handling mechanisms work correctly before digest functionality is added.

**Setup:**
- Access to create ClusterCurator resources
- Test namespace for validation

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Create ClusterCurator with invalid version<br/>**Goal**: Test error handling for non-existent versions<br/>**Command**: `oc apply -f -` (stdin)<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: invalid-version-test<br/>  namespace: ocm<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 99.99.99<br/>    monitorTimeout: 5<br/>``` | ClusterCurator created with invalid version |
| **Step 2**: Monitor error reporting<br/>**Goal**: Verify appropriate error messages<br/>**Command**: `oc get clustercurator invalid-version-test -n ocm -o jsonpath='{.status.conditions[*].message}'` | Error messages indicate invalid version |
| **Step 3**: Test missing managed cluster scenario<br/>**Goal**: Verify handling of non-existent clusters<br/>**Command**: `oc apply -f -` (stdin)<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: missing-cluster-test<br/>  namespace: non-existent-cluster<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: 4.19.7<br/>    monitorTimeout: 5<br/>``` | Error about missing managed cluster |
| **Step 4**: Validate timeout configuration<br/>**Goal**: Test timeout parameter handling<br/>**Command**: Create ClusterCurator with monitorTimeout: 0 | Appropriate timeout validation or default value used |
| **Step 5**: Check controller error logging<br/>**Goal**: Verify detailed error logging<br/>**Command**: `oc logs deployment/cluster-curator-controller -n multicluster-engine --tail=50 \| grep -i error` | Controller logs show detailed error information |
| **Step 6**: Clean up all test resources<br/>**Goal**: Remove test ClusterCurators<br/>**Command**: `oc delete clustercurator invalid-version-test missing-cluster-test -n ocm` | All test resources cleaned up |

---

## ❌ PHASE 2: Blocked Testing (Awaiting Feature Deployment)

The following test cases **CANNOT be executed** in the current qe6 environment due to missing feature implementation:

### Blocked Test Case 4: Core Digest-Based Non-Recommended Upgrade
**Status**: ❌ **BLOCKED** - Digest resolution logic not implemented  
**Blocker**: Controller lacks digest lookup and conditional update processing

### Blocked Test Case 5: Digest Resolution Failure and Tag Fallback  
**Status**: ❌ **BLOCKED** - Fallback mechanism not implemented  
**Blocker**: No tag fallback logic detected in controller

### Blocked Test Case 6: Multi-Cluster Digest Upgrade Validation
**Status**: ❌ **BLOCKED** - Core digest functionality missing  
**Blocker**: Cannot test digest upgrades without digest resolution

### Blocked Test Case 7: Upgrade Monitoring with Digest Details
**Status**: ❌ **BLOCKED** - No digest-specific monitoring  
**Blocker**: Controller does not track digest-based upgrade progress

### Blocked Test Case 8: Disconnected Environment Digest Support
**Status**: ❌ **BLOCKED** - Primary feature functionality missing  
**Blocker**: Digest resolution required for disconnected environment support

### Blocked Test Case 9: Advanced Digest Error Scenarios
**Status**: ❌ **BLOCKED** - Digest error handling not implemented  
**Blocker**: No digest-specific error handling logic present

---

## Prerequisites for Limited Testing

**Environment Setup:**
- ACM hub cluster with kubectl/oc access (✅ Available)
- ClusterCurator controller running in multicluster-engine namespace (✅ Available)
- Access to create ClusterCurator resources (✅ Available)
- Test namespace for validation (✅ Available)

**Access Requirements:**
- Cluster administrator access to hub cluster (✅ Available)
- Ability to create/modify ClusterCurator resources (✅ Available)
- Access to ClusterCurator controller logs (✅ Available)

**Validation Notes:**
- Tests focus on annotation processing and basic infrastructure
- Core digest functionality testing requires feature deployment
- Error handling tests use invalid configurations to avoid actual upgrades

---

## Post-Deployment Testing Plan

Once the ACM-22079 feature is deployed to qe6, execute the full test plan with these additional test cases:

1. **Core Digest-Based Upgrade** - Basic digest resolution functionality
2. **Fallback Mechanism Testing** - Tag-based fallback when digest unavailable  
3. **Multi-Cluster Validation** - Digest upgrades across multiple clusters
4. **Monitoring and Timeout** - Digest-specific upgrade tracking
5. **Integration Testing** - End-to-end digest-based upgrade workflows
6. **Advanced Error Scenarios** - Digest resolution failure handling

**Estimated Full Testing Duration**: 4-5 hours after feature deployment