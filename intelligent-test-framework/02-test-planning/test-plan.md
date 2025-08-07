# Test Cases for ACM-22079: Support digest-based upgrades via ClusterCurator

## Test Case 1: Digest-Based Upgrade Success Scenarios
**Setup**: 
- ACM hub cluster with ClusterCurator operator running and CRD available
- Managed cluster imported with Available=True status
- Target cluster must be OpenShift 4.12+ with available updates
- Test user requires cluster-admin permissions on hub cluster
- Verify ACM installation: `oc get deployment -n open-cluster-management clustercurator-controller`

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster: `oc login https://api.hub-cluster.example.com:6443 -u testuser -p <password>` | Login successful with output: `Login successful. You have access to X projects, using project "default"` |
| 2. Verify ClusterCurator CRD exists: `oc get crd clustercurators.cluster.open-cluster-management.io` | CRD found with output: `NAME: clustercurators.cluster.open-cluster-management.io AGE: <timestamp>` |
| 3. Verify managed cluster status: `oc get managedcluster managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'` | Returns: `True` indicating cluster is ready for operations |
| 4. Check available updates on target cluster: `oc get managedclusterview -n managed-cluster-1 --selector="cluster.open-cluster-management.io/view-name=clusterversion" -o jsonpath='{.items[0].status.result.status.availableUpdates[*].version}'` | Returns list of available versions like: `4.15.8 4.15.9 4.15.10` |
| 5. Create ClusterCurator with digest annotation:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-digest-upgrade<br/>  namespace: managed-cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>```<br/>Apply with: `oc apply -f clustercurator.yaml` | ClusterCurator created with output: `clustercurator.cluster.open-cluster-management.io/test-digest-upgrade created` |
| 6. Verify digest annotation is properly set: `oc get clustercurator test-digest-upgrade -n managed-cluster-1 -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'` | Returns exactly: `"true"` |
| 7. Monitor ManagedClusterView creation for ClusterVersion data: `oc get managedclusterview -n managed-cluster-1 --watch --field-selector metadata.name=test-digest-upgrade-clusterversion` | ManagedClusterView appears with status: `Applied: True` within 30 seconds |
| 8. Verify digest extraction from conditionalUpdates: `oc get managedclusterview test-digest-upgrade-clusterversion -n managed-cluster-1 -o jsonpath='{.status.result.status.conditionalUpdates[?(@.state=="Partial")].release.image}'` | Returns digest format: `quay.io/openshift-release-dev/ocp-release@sha256:[64-character-hash]` |
| 9. Confirm ManagedClusterAction uses digest (NOT tag): `oc get managedclusteraction -n managed-cluster-1 -l clustercurator=test-digest-upgrade -o jsonpath='{.items[0].spec.actionType.ClusterUpdate.desiredUpdate}'` | Shows digest format and contains NO `force: true` field in the spec |
| 10. Test fallback to availableUpdates: Create ClusterCurator with desiredUpdate "4.15.9" (assuming it's in availableUpdates but not conditionalUpdates) | ManagedClusterAction created using digest from availableUpdates array |
| 11. Verify ClusterCurator status progression: `oc get clustercurator test-digest-upgrade -n managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="Applied")].status}'` | Status shows: `True` with reason: `Applied` |

## Test Case 2: Tag-Based Fallback and Error Handling
**Setup**:
- Same environment as Test Case 1
- Ensure ClusterCurator controller is responsive
- Test cluster connectivity for fallback scenarios

| Test Steps | Expected Results |
|------------|------------------|
| 1. Establish cluster connection: `oc login https://api.hub-cluster.example.com:6443 -u testuser -p <password>` | Login successful with proper cluster context displayed |
| 2. Create ClusterCurator targeting version NOT in conditionalUpdates or availableUpdates:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-tag-fallback<br/>  namespace: managed-cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.99"<br/>```<br/>Apply with: `oc apply -f clustercurator-fallback.yaml` | ClusterCurator created: `clustercurator.cluster.open-cluster-management.io/test-tag-fallback created` |
| 3. Monitor digest resolution attempt and fallback: `oc get clustercurator test-tag-fallback -n managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="Processing")].message}' --watch-only=true` | Messages show: `Attempting digest lookup` followed by `Digest not found, falling back to tag format` |
| 4. Verify tag-based ManagedClusterAction creation: `oc get managedclusteraction -n managed-cluster-1 -l clustercurator=test-tag-fallback -o jsonpath='{.items[0].spec.actionType.ClusterUpdate}'` | Shows tag format: `desiredUpdate: "quay.io/openshift-release-dev/ocp-release:4.15.99-x86_64"` AND `force: true` |
| 5. Test ClusterCurator WITHOUT digest annotation:<br/>```yaml<br/>metadata:<br/>  name: test-no-annotation<br/>  namespace: managed-cluster-1<br/>  # NO annotations section<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>```<br/>Apply as new resource | ClusterCurator created, controller skips digest lookup entirely |
| 6. Verify standard upgrade behavior without annotation: `oc get managedclusteraction -n managed-cluster-1 -l clustercurator=test-no-annotation -o jsonpath='{.items[0].spec.actionType.ClusterUpdate}'` | Shows: tag format with `force: true` regardless of digest availability |
| 7. Test invalid version format handling: Create ClusterCurator with desiredUpdate: "invalid.version.99.format" | ClusterCurator accepts creation (validation is not strict on creation) |
| 8. Monitor error handling for invalid version: `oc get clustercurator test-invalid -n managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="Failed")].message}'` | Error message: `Unable to parse version: invalid.version.99.format` |
| 9. Test network failure simulation: Block ManagedClusterView creation and monitor behavior | ClusterCurator status shows: `Waiting for ClusterVersion data` with appropriate timeout handling |
| 10. Verify cleanup on ClusterCurator deletion: `oc delete clustercurator test-tag-fallback -n managed-cluster-1` | Associated ManagedClusterView and ManagedClusterAction are removed within 30 seconds |

## Test Case 3: Multi-Cluster and Concurrent Upgrade Scenarios
**Setup**:
- ACM hub with minimum 3 managed clusters imported
- All managed clusters in Available=True state with different OpenShift versions
- Network connectivity verified between hub and all managed clusters
- Test different cluster architectures (amd64, arm64 if available)

| Test Steps | Expected Results |
|------------|------------------|
| 1. Verify multi-cluster environment: `oc get managedcluster -o custom-columns="NAME:.metadata.name,AVAILABLE:.status.conditions[?(@.type=='ManagedClusterConditionAvailable')].status,VERSION:.metadata.labels.openshiftVersion"` | Shows minimum 3 clusters all with Available=True and different versions displayed |
| 2. Establish hub cluster session: `oc login https://api.hub-cluster.example.com:6443 -u testuser -p <password>` | Login successful with cluster-admin context confirmed |
| 3. Create ClusterCurator for first cluster with specific target:<br/>```yaml<br/>metadata:<br/>  name: concurrent-upgrade-1<br/>  namespace: managed-cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>```<br/>Apply: `oc apply -f clustercurator-1.yaml` | First ClusterCurator created: `clustercurator.cluster.open-cluster-management.io/concurrent-upgrade-1 created` |
| 4. Simultaneously create ClusterCurator for second cluster:<br/>Same YAML structure but: name: `concurrent-upgrade-2`, namespace: `managed-cluster-2`, desiredUpdate: `"4.15.8"` | Second ClusterCurator created within 5 seconds: `clustercurator.cluster.open-cluster-management.io/concurrent-upgrade-2 created` |
| 5. Create third ClusterCurator for stress testing:<br/>Same structure: name: `concurrent-upgrade-3`, namespace: `managed-cluster-3`, desiredUpdate: `"4.15.9"` | Third ClusterCurator created successfully without resource conflicts |
| 6. Monitor all upgrades progress simultaneously: `oc get clustercurator -A -l app=clustercurator -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.conditions[?(@.type=='Applied')].status" --watch-only=true` | All three show independent progression: `Processing` → `Applied` without interference |
| 7. Verify isolated ManagedClusterView creation: `oc get managedclusterview -A --selector="clustercurator-upgrade" -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,CLUSTER-REF:.spec.clusterName"` | Each cluster has separate ManagedClusterView with correct clusterName reference |
| 8. Check resource naming uniqueness: `oc get managedclusteraction -A -o jsonpath='{range .items[*]}{.metadata.namespace}{" "}{.metadata.name}{" "}{.spec.clusterName}{"\n"}{end}' | grep concurrent` | Each action has unique name format: `<namespace> <curator-name>-<hash> <target-cluster>` |
| 9. Verify digest resolution works per cluster architecture: `oc get managedclusterview -A -o jsonpath='{range .items[?(@.metadata.name~"concurrent-upgrade")]}{.metadata.namespace}{" "}{.status.result.status.conditionalUpdates[0].release.image}{"\n"}{end}'` | Each returns appropriate digest for cluster architecture (different sha256 hashes for amd64/arm64) |
| 10. Test concurrent completion handling: Monitor all three until completion | All three complete successfully with final status: `Completed` and no cross-cluster resource conflicts |
| 11. Verify cleanup isolation: `oc delete clustercurator concurrent-upgrade-1 -n managed-cluster-1` | Only resources for managed-cluster-1 are cleaned up, other clusters unaffected |

## Test Case 4: RBAC and Security Validation
**Setup**:
- Test service account with restricted permissions
- ACM hub cluster with strict RBAC policies
- ClusterCurator controller running with proper service account permissions
- Security scanning tools available for validation

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create restricted test service account: `oc create serviceaccount clustercurator-restricted -n open-cluster-management` | Service account created: `serviceaccount/clustercurator-restricted created` |
| 2. Create minimal RBAC role for testing:<br/>```yaml<br/>apiVersion: rbac.authorization.k8s.io/v1<br/>kind: ClusterRole<br/>metadata:<br/>  name: clustercurator-minimal<br/>rules:<br/>- apiGroups: ["cluster.open-cluster-management.io"]<br/>  resources: ["clustercurators"]<br/>  verbs: ["get", "list", "create", "watch"]<br/>- apiGroups: [""]<br/>  resources: ["namespaces"]<br/>  verbs: ["get"]<br/>```<br/>Apply: `oc apply -f minimal-role.yaml` | ClusterRole created: `clusterrole.rbac.authorization.k8s.io/clustercurator-minimal created` |
| 3. Bind restricted role to test service account: `oc create clusterrolebinding clustercurator-test-binding --clusterrole=clustercurator-minimal --serviceaccount=open-cluster-management:clustercurator-restricted` | ClusterRoleBinding created: `clusterrolebinding.rbac.authorization.k8s.io/clustercurator-test-binding created` |
| 4. Test ManagedClusterAction creation permissions: `oc auth can-i create managedclusteractions --as=system:serviceaccount:open-cluster-management:clustercurator-restricted -n managed-cluster-1` | Returns: `no` (restricted account cannot directly create ManagedClusterActions) |
| 5. Test ManagedClusterView creation permissions: `oc auth can-i create managedclusterviews --as=system:serviceaccount:open-cluster-management:clustercurator-restricted -n managed-cluster-1` | Returns: `no` (only controller service account has these permissions) |
| 6. Verify ClusterCurator creation with restricted account: `oc create -f clustercurator.yaml --as=system:serviceaccount:open-cluster-management:clustercurator-restricted` | ClusterCurator created successfully: `clustercurator.cluster.open-cluster-management.io/test-rbac created` |
| 7. Confirm controller escalates privileges appropriately: `oc get managedclusteraction -n managed-cluster-1 --show-labels | grep test-rbac` | ManagedClusterAction appears, created by controller service account with proper ownership labels |
| 8. Audit controller service account permissions: `oc auth can-i '*' '*' --as=system:serviceaccount:open-cluster-management:clustercurator-controller` | Returns: `yes` for required resources, `no` for unnecessary system resources |
| 9. Verify annotation-based security controls: `oc get clustercurator -A -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}{"\n"}{end}'` | Only ClusterCurators with explicit annotation show `"true"`, others show `<no value>` |
| 10. Test privilege escalation prevention: Create ClusterCurator attempting to upgrade to non-existent version without annotation | Controller rejects with status condition: `Failed` and message: `Annotation required for non-recommended versions` |
| 11. Validate controller logs for security events: `oc logs -n open-cluster-management deployment/clustercurator-controller --tail=100 | grep -E "(RBAC|permission|security|unauthorized|denied)"` | Logs show proper RBAC enforcement, no privilege escalation attempts, access denied events handled gracefully |
| 12. Test cluster isolation security: Create ClusterCurator in managed-cluster-1 namespace targeting managed-cluster-2 | Controller validates namespace-cluster mapping and rejects with error: `ClusterCurator namespace must match target cluster` |
