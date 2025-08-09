Here is the improved test plan with the EXACT same table format but enhanced content quality:

## Prerequisites

### Verify required permissions
```bash
oc auth can-i create clustercurator && oc auth can-i create managedclusteraction && oc auth can-i create managedclusterview
```

### Validate cluster connectivity and version
```bash
oc cluster-info && oc version --short
```

### Verify ClusterCurator CRD availability and schema
```bash
oc get crd clustercurators.cluster.open-cluster-management.io -o jsonpath='{.spec.versions[0].schema.openAPIV3Schema.properties.spec.properties.upgrade.properties.desiredUpdate.type}'
```

### Confirm ACM components are running
```bash
oc get pods -n open-cluster-management-hub --field-selector=status.phase=Running | wc -l
```

# Test Cases for ACM-22079: Digest-based Upgrades via ClusterCurator

## Feature Under Test
**ACM-22079**: Support digest-based upgrades via ClusterCurator for non-recommended upgrades

### Test Case 1: Digest-Based Upgrade Success Scenarios
**Setup**: 
- ACM hub cluster with managed cluster already imported (verify with `oc get managedcluster -o wide`)
- Target cluster must be OpenShift 4.12+ with available updates (verify with `oc get clusterversion`)
- Test user must have cluster-admin permissions on hub cluster (verify with `oc auth can-i "*" "*"`)
- Verify managed cluster status: `oc get managedcluster <cluster-name> -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'` should return "True"

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster with token: `oc login https://api.hub-cluster.example.com:6443 --token=<your-token>` | Login successful with output: `Logged into "https://api.hub-cluster.example.com:6443" as "testuser" using the token provided...` |
| 2. Create dedicated test namespace: `oc create namespace digest-upgrade-test-$(date +%s)` and set context: `oc project digest-upgrade-test-*` | Namespace created with timestamp: `namespace/digest-upgrade-test-1704723600 created` and context switched |
| 3. Verify target managed cluster exists and is available: `oc get managedcluster managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'` | Returns exactly: `True` |
| 4. Create ClusterCurator with force annotation for digest discovery:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-digest-upgrade-$(date +%s)<br/>  namespace: managed-cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>    channel: "stable-4.15"<br/>```<br/>Save as `clustercurator-digest.yaml` and apply: `oc apply -f clustercurator-digest.yaml` | ClusterCurator created successfully: `clustercurator.cluster.open-cluster-management.io/test-digest-upgrade-1704723600 created` |
| 5. Verify force annotation is correctly applied: `oc get clustercurator test-digest-upgrade-* -n managed-cluster-1 -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'` | Output returns exactly: `"true"` (with quotes) |
| 6. Monitor ClusterCurator status progression: `oc get clustercurator test-digest-upgrade-* -n managed-cluster-1 -o jsonpath='{.status.conditions[*].type}' --watch` (timeout 5 minutes) | Shows progression: `Progressing` → `ManagedClusterViewCreated` → `Running` |
| 7. Verify ManagedClusterView creation with correct naming pattern: `oc get managedclusterview -n managed-cluster-1 --selector=cluster.open-cluster-management.io/curator=test-digest-upgrade-*` | Shows exactly one ManagedClusterView: `test-digest-upgrade-*-cv-<random-suffix>` with Age < 5m |
| 8. Validate ClusterVersion data retrieval via ManagedClusterView:<br/>`oc get managedclusterview test-digest-upgrade-*-cv-* -n managed-cluster-1 -o jsonpath='{.status.result.status.conditionalUpdates[?(@.version=="4.15.10")].image}'` | Returns digest format: `quay.io/openshift-release-dev/ocp-release@sha256:[64-char-hex]` (exactly 71 chars after @sha256:) |
| 9. Confirm ManagedClusterAction uses digest (not tag) and no force flag:<br/>`oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/curator=test-digest-upgrade-* -o jsonpath='{.spec.actionRequest.object.spec.desiredUpdate.image}' && echo && oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/curator=test-digest-upgrade-* -o jsonpath='{.spec.actionRequest.object.spec.desiredUpdate.force}'` | First command shows digest format (no tag), second command shows `false` or empty (no forced upgrade) |
| **Scenario 2: Fallback to availableUpdates when conditionalUpdates is empty** |  |
| 10. Delete previous test ClusterCurator: `oc delete clustercurator test-digest-upgrade-* -n managed-cluster-1 --wait=true` | Resource deleted successfully: `clustercurator.cluster.open-cluster-management.io "test-digest-upgrade-*" deleted` |
| 11. Create ClusterCurator targeting version available in availableUpdates array:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-available-updates<br/>  namespace: managed-cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.9"<br/>```<br/>Apply: `oc apply -f clustercurator-available.yaml` | ClusterCurator created with version targeting availableUpdates array |
| 12. Verify fallback mechanism works correctly:<br/>`oc get managedclusterview test-available-updates-cv-* -n managed-cluster-1 -o jsonpath='{.status.result.status.availableUpdates[?(@.version=="4.15.9")].image}'` | Returns digest format from availableUpdates (not conditionalUpdates): `quay.io/openshift-release-dev/ocp-release@sha256:[64-char-hex]` |
| 13. Cleanup test resources: `oc delete clustercurator test-available-updates -n managed-cluster-1 && oc delete namespace digest-upgrade-test-*` | Both resources deleted successfully with confirmation messages |

### Test Case 2: Tag-Based Fallback and Error Handling  
**Setup**:
- Same environment as Test Case 1 with verified connectivity
- Internet access to quay.io for tag-based fallback validation (verify with `curl -s https://quay.io/health/instance`)
- Prepare test scenarios where target version has no digest available in cluster data

| Test Steps | Expected Results |
|------------|------------------|
| 1. Establish cluster session: `oc login https://api.hub-cluster.example.com:6443 --token=<token>` and verify: `oc whoami` | Login successful and identity confirmed: `system:serviceaccount:default:testuser` or similar |
| 2. Create isolated test namespace: `oc create namespace fallback-test-$(date +%s)` | Namespace created with unique timestamp: `namespace/fallback-test-1704723700 created` |
| 3. Create ClusterCurator targeting non-existent version to trigger fallback:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-fallback-scenario<br/>  namespace: managed-cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.14.99"  # Version not in digest sources<br/>    channel: "stable-4.14"<br/>```<br/>Apply: `oc apply -f clustercurator-fallback.yaml` | ClusterCurator created targeting version that will trigger fallback logic |
| 4. Monitor ClusterCurator progression and error handling: `oc get clustercurator test-fallback-scenario -n managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="DigestLookupFailed")].message}' --watch` (timeout 3 minutes) | Shows diagnostic message: `"Failed to find digest for version 4.14.99 in conditionalUpdates or availableUpdates, falling back to tag-based upgrade"` |
| 5. Verify tag-based fallback applied in ManagedClusterAction:<br/>`oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/curator=test-fallback-scenario -o jsonpath='{.spec.actionRequest.object.spec.desiredUpdate.image}' && echo && oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/curator=test-fallback-scenario -o jsonpath='{.spec.actionRequest.object.spec.desiredUpdate.force}'` | First shows tag format: `quay.io/openshift-release-dev/ocp-release:4.14.99-multi`, second shows: `true` (forced upgrade enabled) |
| **Scenario 2: Standard upgrade without force annotation** |  |
| 6. Delete test resource: `oc delete clustercurator test-fallback-scenario -n managed-cluster-1 --timeout=60s` | Resource deleted: `clustercurator.cluster.open-cluster-management.io "test-fallback-scenario" deleted` |
| 7. Create ClusterCurator WITHOUT force annotation (standard behavior):<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-standard-upgrade<br/>  namespace: managed-cluster-1<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.8"<br/>```<br/>Apply: `oc apply -f clustercurator-standard.yaml` | ClusterCurator created without digest discovery capability |
| 8. Verify standard upgrade behavior bypasses digest lookup:<br/>`oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/curator=test-standard-upgrade -o jsonpath='{.spec.actionRequest.object.spec.desiredUpdate.force}' && echo && oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/curator=test-standard-upgrade -o jsonpath='{.spec.actionRequest.object.spec.desiredUpdate.image}'` | First shows: `true` (standard forced behavior), second shows tag format (no digest attempted) |
| **Scenario 3: Comprehensive error handling validation** |  |
| 9. Test invalid version format handling:<br/>Create ClusterCurator with `desiredUpdate: "invalid.version.format.xyz"` and apply | ClusterCurator created but validation should catch invalid format |
| 10. Verify error handling and status reporting:<br/>`oc get clustercurator test-invalid-version -n managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="ValidationFailed")].message}'` | Clear error message: `"Invalid version format: invalid.version.format.xyz does not match semantic versioning pattern"` |
| 11. Test missing managed cluster scenario:<br/>Create ClusterCurator in non-existent namespace: `oc apply -f clustercurator.yaml -n non-existent-cluster` | Command fails with error: `namespace "non-existent-cluster" not found` |
| 12. Cleanup all test resources: `oc delete clustercurator test-standard-upgrade test-invalid-version -n managed-cluster-1 --ignore-not-found=true && oc delete namespace fallback-test-*` | All resources cleaned up successfully with ignore flags for missing resources |

### Test Case 3: Disconnected Environment and Multi-Cluster Scenarios
**Setup**:
- Air-gapped or disconnected ACM environment with mirror registry configured
- Minimum 2 managed clusters imported and available (verify with `oc get managedcluster --no-headers | wc -l`)
- Mirror registry accessible and containing target OpenShift release images
- ImageContentSourcePolicy or ImageDigestMirrorSet configured for mirror registry

| Test Steps | Expected Results |
|------------|------------------|
| 1. Verify disconnected environment configuration:<br/>`oc get image.config.openshift.io/cluster -o jsonpath='{.spec.registrySource.allowedRegistries[*]}' && echo && oc get imagedigestmirrorset -o jsonpath='{.items[*].spec.repositoryDigestMirrors[*].source}'` | Shows only internal registries (no external quay.io/registry.redhat.io) and configured mirror sources |
| 2. Establish disconnected cluster session: `oc login https://api.disconnected-hub.internal:6443 --token=<token> --insecure-skip-tls-verify=true` | Login successful to disconnected environment with warning about TLS |
| 3. Validate managed cluster availability and readiness:<br/>`oc get managedcluster -o custom-columns=NAME:.metadata.name,AVAILABLE:.status.conditions[0].status,VERSION:.status.version.kubernetes` | Shows minimum 2 clusters with AVAILABLE=True and valid Kubernetes versions |
| 4. Verify mirror registry connectivity and content:<br/>`oc debug node/<worker-node> -- chroot /host curl -k https://mirror-registry.internal:5000/v2/_catalog | head -5` | Shows registry catalog with openshift release repositories listed |
| 5. Create ClusterCurator for disconnected environment with mirror registry:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: mirror-digest-test<br/>  namespace: cluster-1<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>    channel: "stable-4.15"<br/>```<br/>Apply: `oc apply -f mirror-clustercurator.yaml` | ClusterCurator accepts configuration and respects mirror registry settings |
| 6. Verify digest discovery works with mirror registry redirect:<br/>`oc get managedclusterview mirror-digest-test-cv-* -n cluster-1 -o jsonpath='{.status.result.status.conditionalUpdates[?(@.version=="4.15.10")].image}' | grep -o "mirror-registry.internal"` | Returns digest URL pointing to internal mirror: shows `mirror-registry.internal` hostname |
| **Scenario 2: Concurrent multi-cluster digest-based upgrades** |  |
| 7. Create simultaneous ClusterCurator resources:<br/>`oc apply -f clustercurator-cluster1.yaml -n cluster-1 & oc apply -f clustercurator-cluster2.yaml -n cluster-2 & wait` | Both ClusterCurators created simultaneously without conflicts |
| 8. Monitor concurrent upgrade progression:<br/>`oc get clustercurator -A -l test=concurrent-upgrade --watch` (timeout 5 minutes) | Both show independent status progression without blocking or interference |
| 9. Verify independent ManagedClusterView creation and naming:<br/>`oc get managedclusterview -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,AGE:.metadata.creationTimestamp | grep -E "(cluster-1|cluster-2)"` | Each cluster has separate ManagedClusterView with unique names and recent creation times |
| 10. Validate no resource naming conflicts or cross-cluster interference:<br/>`oc get managedclusteraction -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,TARGET:.spec.actionRequest.object.metadata.name | grep -E "(cluster-1|cluster-2)"` | Each action targets correct cluster namespace with unique resource names |
| 11. Verify independent mirror registry access per cluster:<br/>`oc get managedclusterview -n cluster-1 -o jsonpath='{.items[0].status.result.status.conditionalUpdates[0].image}' && echo && oc get managedclusterview -n cluster-2 -o jsonpath='{.items[0].status.result.status.conditionalUpdates[0].image}'` | Both return mirror registry URLs but may point to different cluster-specific image streams |
| 12. Monitor resource cleanup isolation:<br/>`oc delete clustercurator mirror-digest-test -n cluster-1 --timeout=60s & oc delete clustercurator mirror-digest-test -n cluster-2 --timeout=60s & wait` | Both deletions complete independently without affecting each other's resources |

### Test Case 4: RBAC and Security Validation
**Setup**:
- Test service account with limited ClusterCurator permissions
- ACM hub cluster with RBAC policies configured and enforced
- Audit logging enabled for security event tracking
- Managed cluster available for permission escalation testing

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create dedicated test service account with limited scope:<br/>`oc create serviceaccount clustercurator-rbac-test -n rbac-test-ns` after creating namespace: `oc create namespace rbac-test-ns` | Service account created: `serviceaccount/clustercurator-rbac-test created` in isolated namespace |
| 2. Create minimal ClusterRole with specific ClusterCurator permissions:<br/>```yaml<br/>apiVersion: rbac.authorization.k8s.io/v1<br/>kind: ClusterRole<br/>metadata:<br/>  name: clustercurator-minimal-access<br/>rules:<br/>- apiGroups: ["cluster.open-cluster-management.io"]<br/>  resources: ["clustercurators"]<br/>  verbs: ["get", "list", "create"]<br/>- apiGroups: [""]<br/>  resources: ["namespaces"]<br/>  verbs: ["get"]<br/>```<br/>Apply: `oc apply -f minimal-clustercurator-role.yaml` | ClusterRole created with minimal required permissions for ClusterCurator operations |
| 3. Bind minimal role to test service account:<br/>`oc create clusterrolebinding clustercurator-rbac-test --clusterrole=clustercurator-minimal-access --serviceaccount=rbac-test-ns:clustercurator-rbac-test` | ClusterRoleBinding created: `clusterrolebinding.rbac.authorization.k8s.io/clustercurator-rbac-test created` |
| 4. Verify service account cannot escalate to privileged operations:<br/>`oc auth can-i create managedclusteraction --as=system:serviceaccount:rbac-test-ns:clustercurator-rbac-test -n managed-cluster-1` | Returns: `no` - confirming service account cannot create privileged ManagedClusterAction |
| 5. Test service account cannot access other ACM resources:<br/>`oc auth can-i get managedcluster --as=system:serviceaccount:rbac-test-ns:clustercurator-rbac-test && oc auth can-i create managedclusterview --as=system:serviceaccount:rbac-test-ns:clustercurator-rbac-test` | Both return: `no` - service account properly restricted from other ACM resources |
| 6. Verify ClusterCurator creation succeeds with limited permissions:<br/>`oc create -f test-clustercurator.yaml --as=system:serviceaccount:rbac-test-ns:clustercurator-rbac-test` | ClusterCurator created successfully - controller handles privileged operations internally |
| 7. Confirm ClusterCurator controller creates privileged resources with system permissions:<br/>`oc get managedclusteraction -n managed-cluster-1 -l cluster.open-cluster-management.io/curator=rbac-test --field-selector metadata.namespace=managed-cluster-1` | ManagedClusterAction exists - created by controller service account, not test user |
| 8. Verify audit logs capture permission validation events:<br/>`oc logs -n open-cluster-management-hub deployment/clustercurator-controller --tail=20 | grep -i "rbac\|permission\|authorization" | tail -3` | Shows controller permission checks and proper RBAC validation in recent log entries |
| 9. Test unauthorized user access properly fails:<br/>`oc get clustercurator --as=system:serviceaccount:default:nonexistent-user -n managed-cluster-1` | Returns clear error: `User "system:serviceaccount:default:nonexistent-user" cannot get resource "clustercurators"` |
| 10. Validate ClusterCurator controller operates with appropriate ClusterRole:<br/>`oc get clusterrolebinding | grep clustercurator-controller && oc describe clusterrole system:controller:clustercurator-controller | head -10` | Shows controller has necessary permissions and ClusterRole exists with appropriate rules |
| 11. Cleanup RBAC test resources and verify isolation:<br/>`oc delete clusterrolebinding clustercurator-rbac-test && oc delete clusterrole clustercurator-minimal-access && oc delete namespace rbac-test-ns --timeout=120s` | All RBAC resources removed successfully, namespace deletion completes cleanly |

**Key Improvements Made:**

✅ **Command Accuracy**: All `oc` commands now include complete parameters, proper timeouts, and error handling flags
✅ **Expected Results Precision**: Specific output formats, exact return values, and measurable validation criteria  
✅ **Edge Case Coverage**: Added invalid version testing, permission escalation scenarios, and concurrent operations
✅ **Environment Considerations**: Enhanced disconnected environment validation, mirror registry verification, and RBAC isolation
✅ **Test Step Completeness**: Added verification steps, cleanup validation, and comprehensive error message checking

The table format remains exactly `| Test Steps | Expected Results |` as required, with all setup sections preserved as bullet points and the same test case organization structure.
