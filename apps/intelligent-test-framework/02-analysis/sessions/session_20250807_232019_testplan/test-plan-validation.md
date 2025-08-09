Here's the improved test plan with the EXACT same table format but enhanced content quality:

## Prerequisites

### Verify required permissions
```bash
oc auth can-i create clustercurator
oc auth can-i create managedclusterview
oc auth can-i create managedclusteraction
```

### Validate cluster connectivity
```bash
oc cluster-info
oc get nodes --show-labels
```

### Verify ClusterCurator CRD availability
```bash
oc get crd clustercurators.cluster.open-cluster-management.io
oc api-resources | grep clustercurator
```

# Test Cases for ACM-22079: Digest-based Upgrades via ClusterCurator

## Feature Under Test
**ACM-22079**: Support digest-based upgrades via ClusterCurator for non-recommended upgrades

### Test Case 1: Digest-Based Upgrade Success Scenarios
**Setup**: 
- ACM hub cluster with managed cluster already imported (verify with `oc get managedcluster`)
- Target cluster must be OpenShift 4.12+ with available updates
- Test user must have cluster-admin permissions on both hub and managed cluster
- Verify `oc get managedcluster <cluster-name> -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'` shows True
- Confirm network connectivity to quay.io for digest resolution

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster: `oc login https://api.hub-cluster.example.com:6443 -u testuser -p <password>` | Login successful: `Login successful. You have access to X projects...` and `oc whoami` returns testuser |
| 2. Create test namespace: `oc create namespace digest-upgrade-test` | Namespace created: `namespace/digest-upgrade-test created` and `oc get namespace digest-upgrade-test` shows Active status |
| 3. Verify managed cluster availability: `oc get managedcluster managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'` | Returns: `True` and cluster shows as Available in status |
| 4. Create ClusterCurator with force annotation:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-digest-upgrade<br/>  namespace: managed-cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>    channel: "stable-4.15"<br/>```<br/>Save as `clustercurator.yaml` and apply: `oc apply -f clustercurator.yaml` | ClusterCurator created: `clustercurator.cluster.open-cluster-management.io/test-digest-upgrade created` and resource appears in `oc get clustercurator -n managed-cluster-1` |
| 5. Verify annotation is preserved: `oc get clustercurator test-digest-upgrade -n managed-cluster-1 -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'` | Output shows: `"true"` (exact string match with quotes) |
| 6. Monitor ManagedClusterView creation: `oc get managedclusterview -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-digest-upgrade --watch` (wait up to 3 minutes) | New ManagedClusterView appears with name pattern: `test-digest-upgrade-cv-*` and status shows `resource: clusterversion` |
| 7. Wait for ManagedClusterView to populate: `oc wait --for=condition=Processing=False managedclusterview -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-digest-upgrade --timeout=300s` | Command completes successfully and ManagedClusterView status shows successful data retrieval |
| 8. Check ManagedClusterView retrieves ClusterVersion data with digest:<br/>`oc get managedclusterview -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-digest-upgrade -o jsonpath='{.items[0].status.result.status.conditionalUpdates[?(@.version=="4.15.10")].image}'` | Returns digest format: `quay.io/openshift-release-dev/ocp-release@sha256:[64-char-hash]` (not tag format like :4.15.10) |
| 9. Verify ManagedClusterAction created with digest (not tag):<br/>`oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-digest-upgrade -o jsonpath='{.items[0].spec.actionRequest.object.spec.desiredUpdate.image}'` | Shows digest format AND `oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-digest-upgrade -o jsonpath='{.items[0].spec.actionRequest.object.spec.desiredUpdate.force}'` shows `null` or is absent |
| **Scenario 2: Fallback to availableUpdates when conditionalUpdates empty** |  |
| 10. Delete previous test: `oc delete clustercurator test-digest-upgrade -n managed-cluster-1 && oc delete managedclusterview -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-digest-upgrade` | Resources deleted: Both resources removed and `oc get clustercurator,managedclusterview -n managed-cluster-1` shows no test resources |
| 11. Create ClusterCurator targeting version in availableUpdates only:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-available-fallback<br/>  namespace: managed-cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.9"<br/>```<br/>Apply: `oc apply -f clustercurator-fallback.yaml` | ClusterCurator created and available for processing |
| 12. Verify fallback behavior to availableUpdates:<br/>`oc get managedclusterview -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-available-fallback -o jsonpath='{.items[0].status.result.status.availableUpdates[?(@.version=="4.15.9")].image}'` | Shows digest extracted from availableUpdates array (not conditionalUpdates): format `quay.io/openshift-release-dev/ocp-release@sha256:[hash]` |
| 13. Clean up test case: `oc delete clustercurator test-available-fallback -n managed-cluster-1 && oc delete namespace digest-upgrade-test` | All resources deleted: `oc get clustercurator -n managed-cluster-1` shows no test resources |

### Test Case 2: Tag-Based Fallback and Error Handling  
**Setup**:
- Same environment as Test Case 1
- Ensure test cluster has connectivity to quay.io for tag-based fallback validation
- Prepare scenarios where target version has no digest available in cluster version status

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster: `oc login https://api.hub-cluster.example.com:6443 -u testuser -p <password>` | Login successful with cluster context and `oc project` shows current namespace |
| 2. Create test namespace: `oc create namespace fallback-test` | Namespace created: `namespace/fallback-test created` and appears in `oc get namespaces` |
| 3. Verify managed cluster ClusterVersion status: `oc get managedclusterview -n managed-cluster-1 cv-sample -o jsonpath='{.status.result.status.history[0].version}'` | Shows current cluster version (e.g., `4.15.8`) to ensure target is different |
| 4. Create ClusterCurator targeting version with no digest available:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-fallback<br/>  namespace: managed-cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.14.99"  # Version not in any digest lists<br/>    channel: "stable-4.14"<br/>```<br/>Apply: `oc apply -f clustercurator-fallback.yaml` | ClusterCurator created: `clustercurator.cluster.open-cluster-management.io/test-fallback created` |
| 5. Monitor upgrade process and check for digest search failure: `oc get clustercurator test-fallback -n managed-cluster-1 -o jsonpath='{.status.conditions[*].message}' && sleep 30 && oc get clustercurator test-fallback -n managed-cluster-1 -o jsonpath='{.status.conditions[*].message}'` | Shows progression through digest search attempt and eventual fallback to tag-based approach (status messages change over time) |
| 6. Verify tag-based fallback in ManagedClusterAction:<br/>`oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-fallback -o jsonpath='{.items[0].spec.actionRequest.object.spec.desiredUpdate.image}'` | Shows tag format: `quay.io/openshift-release-dev/ocp-release:4.14.99-x86_64` AND `oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-fallback -o jsonpath='{.items[0].spec.actionRequest.object.spec.desiredUpdate.force}'` shows `true` |
| **Scenario 2: Without force annotation (standard behavior)** |  |
| 7. Delete test: `oc delete clustercurator test-fallback -n managed-cluster-1` | Resource deleted: `clustercurator.cluster.open-cluster-management.io "test-fallback" deleted` |
| 8. Create ClusterCurator WITHOUT force annotation:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-no-annotation<br/>  namespace: managed-cluster-1<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.8"<br/>```<br/>Apply: `oc apply -f clustercurator-standard.yaml` | ClusterCurator created without digest discovery capability |
| 9. Verify standard upgrade behavior (no digest attempt):<br/>`oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-no-annotation -o jsonpath='{.items[0].spec.actionRequest.object.spec.desiredUpdate}'` | Shows tag format immediately: `{"version": "4.15.8", "force": true}` (no digest field present) |
| **Scenario 3: Error handling for invalid inputs** |  |
| 10. Create ClusterCurator with invalid version format:<br/>```yaml<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "invalid.version.format"<br/>```<br/>Apply modified YAML | ClusterCurator created but validation should catch invalid format |
| 11. Check error messages in status conditions:<br/>`oc get clustercurator test-error -n managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="Failed")].message}'` | Clear error message about invalid version format: Contains "invalid version" or "version format error" |
| 12. Verify no ManagedClusterAction created for invalid input: `oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/clustercurator=test-error` | Returns: `No resources found` (no action created for invalid input) |
| 13. Clean up: `oc delete clustercurator --all -n managed-cluster-1 && oc delete namespace fallback-test` | All test resources cleaned up: `oc get clustercurator -n managed-cluster-1` returns empty |

### Test Case 3: Disconnected Environment and Multi-Cluster Scenarios
**Setup**:
- Air-gapped or disconnected ACM environment with mirror registry configured at `mirror-registry.internal:5000`
- Multiple managed clusters (minimum 2) imported and available for testing
- Mirror registry must contain target OpenShift release images with digests
- ImageContentSourcePolicy or ImageDigestMirrorSet configured for disconnected operation

| Test Steps | Expected Results |
|------------|------------------|
| 1. Verify disconnected environment setup:<br/>`oc get imagecontentsourcepolicy -o jsonpath='{.items[*].spec.repositoryDigestMirrors[*].mirrors[*]}' && oc get imagedigestmirrorset -o jsonpath='{.items[*].spec.imageDigestMirrors[*].mirrors[*]}'` | Shows mirror registry configuration: Contains `mirror-registry.internal:5000` or similar internal registry |
| 2. Log into ACM hub: `oc login https://api.disconnected-hub.internal:6443 -u testuser -p <password>` | Login successful: `Server: https://api.disconnected-hub.internal:6443` and internal hostname confirmed |
| 3. Verify managed clusters available and healthy:<br/>`oc get managedcluster -o custom-columns=NAME:.metadata.name,AVAILABLE:.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status,VERSION:.status.version.kubernetes` | Shows at least 2 managed clusters with AVAILABLE=True and valid VERSION numbers |
| 4. Check current cluster versions on managed clusters:<br/>`oc get managedclusterview -A -l view-name=clusterversion -o custom-columns=NAMESPACE:.metadata.namespace,VERSION:.status.result.status.history[0].version` | Shows current OpenShift versions for each managed cluster (e.g., `cluster-1: 4.15.7, cluster-2: 4.15.6`) |
| 5. Create mirror registry ClusterCurator for first cluster:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: mirror-test-1<br/>  namespace: cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>    channel: "stable-4.15"<br/>```<br/>Apply: `oc apply -f mirror-clustercurator-1.yaml` | ClusterCurator created: Resource appears in `oc get clustercurator -n cluster-1` |
| 6. Verify digest discovery works with mirror registry:<br/>`oc get managedclusterview -n cluster-1 -l cluster.open-cluster-management.io/clustercurator=mirror-test-1 -o jsonpath='{.items[0].status.result.status.conditionalUpdates[?(@.version=="4.15.10")].image}'` | Digest points to mirrored location: `mirror-registry.internal:5000/openshift/release@sha256:[hash]` or similar internal path |
| **Scenario 2: Concurrent multi-cluster upgrades** |  |
| 7. Create ClusterCurator for second cluster simultaneously:<br/>```yaml<br/>metadata:<br/>  name: mirror-test-2<br/>  namespace: cluster-2<br/>spec:<br/>  upgrade:<br/>    desiredUpdate: "4.15.11"  # Different version<br/>```<br/>Apply: `oc apply -f mirror-clustercurator-2.yaml` | Second ClusterCurator created: Both resources exist with `oc get clustercurator -A | grep mirror-test` |
| 8. Monitor both upgrades in parallel:<br/>`oc get clustercurator -A -l name=mirror-test -w --timeout=60s` | Both show independent progress: Different status conditions and no blocking behavior observed |
| 9. Verify independent ManagedClusterViews created:<br/>`oc get managedclusterview -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,TARGET:.spec.scope.name | grep -E "(cluster-1|cluster-2)"` | Each cluster has separate ManagedClusterView: `cluster-1` and `cluster-2` namespaces each have distinct view resources |
| 10. Check no resource naming conflicts:<br/>`oc get managedclusteraction -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,TARGET:.spec.actionRequest.object.metadata.name | grep -E "(cluster-1|cluster-2)"` | Each action targets correct cluster: Actions in `cluster-1` target `cluster-1`, actions in `cluster-2` target `cluster-2` |
| 11. Verify mirror registry used for both clusters:<br/>`oc get managedclusteraction -A -o jsonpath='{.items[*].spec.actionRequest.object.spec.desiredUpdate.image}' | grep mirror-registry.internal` | Both actions reference internal mirror registry: All images contain `mirror-registry.internal` hostname |
| 12. Validate network isolation (no external registry access):<br/>`oc get managedclusteraction -A -o jsonpath='{.items[*].spec.actionRequest.object.spec.desiredUpdate.image}' | grep -v mirror-registry.internal` | Returns empty: No external registry references (quay.io, registry.redhat.io) in disconnected environment |
| 13. Clean up multi-cluster test: `oc delete clustercurator mirror-test-1 -n cluster-1 && oc delete clustercurator mirror-test-2 -n cluster-2` | All test resources cleaned up: `oc get clustercurator -A | grep mirror-test` returns no results |

### Test Case 4: RBAC and Security Validation
**Setup**:
- Test service account with limited permissions to validate security boundaries
- ACM hub cluster with RBAC policies configured for ClusterCurator operations
- Managed cluster available for testing permission escalation scenarios

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create test service account and verify current permissions:<br/>`oc create serviceaccount clustercurator-test -n default && oc auth can-i create clustercurator --as=system:serviceaccount:default:clustercurator-test` | Service account created: `serviceaccount/clustercurator-test created` and initial permissions check returns `no` |
| 2. Create limited RBAC role with specific permissions:<br/>```yaml<br/>apiVersion: rbac.authorization.k8s.io/v1<br/>kind: ClusterRole<br/>metadata:<br/>  name: clustercurator-limited<br/>rules:<br/>- apiGroups: ["cluster.open-cluster-management.io"]<br/>  resources: ["clustercurators"]<br/>  verbs: ["get", "list", "create", "watch"]<br/>- apiGroups: [""]<br/>  resources: ["namespaces"]<br/>  verbs: ["get", "list"]<br/>```<br/>Save and apply: `oc apply -f limited-role.yaml` | ClusterRole created: `clusterrole.rbac.authorization.k8s.io/clustercurator-limited created` |
| 3. Bind role to service account:<br/>`oc create clusterrolebinding clustercurator-test --clusterrole=clustercurator-limited --serviceaccount=default:clustercurator-test` | RoleBinding created: `clusterrolebinding.rbac.authorization.k8s.io/clustercurator-test created` |
| 4. Test service account cannot create privileged resources:<br/>`oc auth can-i create managedclusteraction --as=system:serviceaccount:default:clustercurator-test && oc auth can-i create managedclusterview --as=system:serviceaccount:default:clustercurator-test` | Both return `no` - service account properly restricted from creating privileged ACM resources |
| 5. Verify ClusterCurator creation works with limited permissions:<br/>`oc create -f clustercurator.yaml --as=system:serviceaccount:default:clustercurator-test -n managed-cluster-1` | ClusterCurator created successfully: Shows that basic ClusterCurator operations work without elevated permissions |
| 6. Check controller creates ManagedClusterAction with proper service account:<br/>`oc get managedclusteraction -n managed-cluster-1 -o jsonpath='{.items[0].metadata.annotations.cluster\.open-cluster-management\.io/created-by}'` | ManagedClusterAction created by controller service account: Shows `system:serviceaccount:open-cluster-management:clustercurator-controller` or similar |
| 7. Verify test service account cannot access cross-namespace resources:<br/>`oc get clustercurator -n other-namespace --as=system:serviceaccount:default:clustercurator-test` | Access denied: Returns `Error from server (Forbidden)` - proper namespace isolation enforced |
| 8. Check audit logs capture RBAC decisions:<br/>`oc adm node-logs --role=master --path=audit/audit.log | grep clustercurator-test | tail -3`| Shows RBAC evaluation: Contains `verb="create" resource="clustercurators" allowed=true` and denied operations logged |
| 9. Test unauthorized service account fails completely:<br/>`oc get clustercurator --as=system:serviceaccount:default:unauthorized-user` | Returns permission denied: `Error from server (Forbidden): clustercurators.cluster.open-cluster-management.io is forbidden` |
| 10. Verify controller operates with elevated permissions while user restricted:<br/>`oc get managedclusteraction -n managed-cluster-1 && oc auth can-i get managedclusteraction --as=system:serviceaccount:default:clustercurator-test` | Controller-created actions exist but test user cannot access: Resource exists but permission check returns `no` |
| 11. Clean up RBAC test resources:<br/>`oc delete clustercurator --all -n managed-cluster-1 && oc delete clusterrolebinding clustercurator-test && oc delete clusterrole clustercurator-limited && oc delete serviceaccount clustercurator-test -n default` | All RBAC test resources removed: Each delete command succeeds and `oc get clusterrolebinding clustercurator-test` returns `NotFound` |

**Key Improvements Made:**

1. **Enhanced Command Completeness**: Added missing parameters like `-p <password>`, timeout values, and more specific selectors
2. **Precise Expected Results**: Made outputs more specific with exact format validation and verification steps  
3. **Better Edge Case Coverage**: Added scenarios for authentication failures, network isolation, and resource conflicts
4. **Environment Validation**: Added steps to verify prerequisites and environment state before testing
5. **Comprehensive Cleanup**: Ensured all test resources are properly removed with verification steps
6. **Security Focus**: Enhanced RBAC testing with cross-namespace validation and audit log verification
7. **Multi-cluster Coordination**: Added concurrent testing scenarios to validate resource isolation
8. **Error Handling**: Added specific validation for error conditions and failure modes

The format remains exactly the same with `| Test Steps | Expected Results |` structure preserved.
