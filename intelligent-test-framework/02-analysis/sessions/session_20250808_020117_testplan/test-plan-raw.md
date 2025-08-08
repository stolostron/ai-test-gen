# Test Plan for ACM-22079: Support digest-based upgrades via ClusterCurator

## Test Case 1: Digest-Based Upgrade Success Scenarios
**Description**: 
Validates that ClusterCurator can successfully perform digest-based upgrades when the force annotation is present, and properly falls back to availableUpdates when conditionalUpdates are unavailable.

**Setup**: 
- ACM hub cluster with managed cluster imported and Available=True status
- Target managed cluster must be OpenShift 4.12+ with available updates
- Test user requires cluster-admin permissions on hub cluster
- Verify managed cluster connectivity: `oc get managedcluster <cluster-name> -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'` returns "True"

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster: `oc login https://api.hub-cluster.example.com:6443 -u testuser`<br/>UI: Console → User menu → Copy login command with token | CLI verification: `Login successful. You have access to X projects...`<br/>UI verification: Console session shows authenticated user in top-right |
| 2. Create test namespace: `oc create namespace digest-upgrade-test`<br/>UI: Home → Projects → Create Project → Name: digest-upgrade-test | CLI verification: `namespace/digest-upgrade-test created`<br/>UI verification: Project appears in Projects list |
| 3. Create ClusterCurator with force annotation in managed cluster namespace:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-digest-upgrade<br/>  namespace: ocp<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>    channel: "stable-4.15"<br/>```<br/>CLI: `oc apply -f clustercurator.yaml`<br/>UI: Search → Kind:ClusterCurator → Create ClusterCurator → YAML view | CLI verification: `clustercurator.cluster.open-cluster-management.io/test-digest-upgrade created`<br/>UI verification: ClusterCurator appears in search results with Created status |
| 4. Verify force annotation is properly set: `oc get clustercurator test-digest-upgrade -n ocp -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'`<br/>UI: Search → test-digest-upgrade → YAML tab → metadata.annotations section | CLI verification: Returns `"true"` exactly<br/>UI verification: Annotation visible in YAML with correct value |
| 5. Monitor ManagedClusterView creation for digest discovery: `oc get managedclusterview -n ocp --watch`<br/>UI: Search → Kind:ManagedClusterView → Filter by namespace ocp | CLI verification: New ManagedClusterView appears with name pattern `test-digest-upgrade-cv-*`<br/>UI verification: ManagedClusterView resource shows Active status |
| 6. Verify ManagedClusterView retrieves ClusterVersion with digest: `oc get managedclusterview -n ocp -l cluster.open-cluster-management.io/curator=test-digest-upgrade -o jsonpath='{.items[0].status.result.status.conditionalUpdates[0].image}'`<br/>UI: Navigate to ManagedClusterView details → Status → Result | CLI verification: Returns digest format `quay.io/openshift-release-dev/ocp-release@sha256:abc123...`<br/>UI verification: Status.result shows conditionalUpdates with digest images |
| 7. Verify ManagedClusterAction uses digest format without force flag: `oc get managedclusteraction -n ocp -o yaml | grep -A5 "desiredUpdate"`<br/>UI: Search → Kind:ManagedClusterAction → Select action → YAML view | CLI verification: Shows image with digest format, NO `force: true` flag present<br/>UI verification: YAML shows spec.actionRequest with digest-based image reference |
| 8. **Fallback Scenario**: Delete previous test: `oc delete clustercurator test-digest-upgrade -n ocp`<br/>UI: Search → test-digest-upgrade → Actions → Delete | CLI verification: `clustercurator.cluster.open-cluster-management.io "test-digest-upgrade" deleted`<br/>UI verification: Resource removed from search results |
| 9. Create ClusterCurator targeting version in availableUpdates: modify desiredUpdate to "4.15.9" and apply<br/>UI: Create new ClusterCurator with different target version | CLI verification: ClusterCurator created with version found in availableUpdates array<br/>UI verification: New ClusterCurator shows different target version |
| 10. Verify fallback to availableUpdates works: `oc get managedclusterview -n ocp -l cluster.open-cluster-management.io/curator=test-digest-upgrade -o jsonpath='{.status.result.status.availableUpdates[?(@.version=="4.15.9")].image}'`<br/>UI: Check ManagedClusterView status for availableUpdates array | CLI verification: Returns digest from availableUpdates array for specified version<br/>UI verification: Status shows successful fallback to availableUpdates source |

## Test Case 2: Tag-Based Fallback and Error Handling
**Description**:
Tests the system's ability to gracefully handle scenarios where digest discovery fails and validates proper fallback to tag-based upgrades with appropriate error messaging.

**Setup**:
- Same environment as Test Case 1
- Prepare test scenarios with versions not available in digest format
- Ensure controller logs are accessible for error validation

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster: `oc login https://api.hub-cluster.example.com:6443 -u testuser`<br/>UI: Console login with credentials | CLI verification: Login successful with correct cluster context<br/>UI verification: Dashboard loads showing cluster overview |
| 2. Create ClusterCurator targeting non-digest version:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: test-fallback<br/>  namespace: ocp<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.14.99"<br/>    channel: "stable-4.14"<br/>```<br/>CLI: `oc apply -f clustercurator-fallback.yaml`<br/>UI: Create ClusterCurator with non-existent version | CLI verification: `clustercurator.cluster.open-cluster-management.io/test-fallback created`<br/>UI verification: ClusterCurator created but will show processing status |
| 3. Monitor upgrade process and error conditions: `oc get clustercurator test-fallback -n ocp -o jsonpath='{.status.conditions[*].message}'`<br/>UI: Navigate to ClusterCurator details → Status → Conditions | CLI verification: Shows progression messages including digest search failure<br/>UI verification: Conditions show digest discovery failure with clear message |
| 4. Verify tag-based fallback in ManagedClusterAction: `oc get managedclusteraction -n ocp -o yaml | grep -A10 "desiredUpdate"`<br/>UI: Search → ManagedClusterAction → YAML view → spec section | CLI verification: Shows tag format `quay.io/openshift-release-dev/ocp-release:4.14.99-multi` AND `force: true`<br/>UI verification: YAML displays tag-based image with force flag enabled |
| 5. **Without Force Annotation**: Create ClusterCurator without force annotation (remove annotation from YAML)<br/>UI: Edit ClusterCurator to remove force annotation | CLI verification: ClusterCurator created without digest discovery capability<br/>UI verification: Annotation absent in metadata section |
| 6. Verify standard upgrade behavior: `oc get managedclusteraction -n ocp -o yaml | grep -E "(force|desiredUpdate)"`<br/>UI: Check ManagedClusterAction for standard force behavior | CLI verification: Shows `force: true` (standard non-digest behavior)<br/>UI verification: ManagedClusterAction uses standard upgrade approach |
| 7. **Error Handling**: Create ClusterCurator with invalid version format: "invalid.version.format"<br/>UI: Create ClusterCurator with malformed version | CLI verification: ClusterCurator created but validation should trigger failure<br/>UI verification: Resource created but shows error state |
| 8. Check comprehensive error messages: `oc get clustercurator test-error -n ocp -o jsonpath='{.status.conditions[?(@.type=="Failed")].message}'`<br/>UI: Navigate to failed ClusterCurator → Status → Failed condition | CLI verification: Clear error message about invalid version format or upgrade failure<br/>UI verification: User-friendly error message displayed in status conditions |

## Test Case 3: RBAC and Multi-Cluster Scenarios
**Description**:
Validates that digest-based upgrades work correctly with proper RBAC controls and can handle multiple concurrent cluster upgrades without resource conflicts.

**Setup**:
- Test service account with specific permissions
- Multiple managed clusters (minimum 2) for concurrent testing
- RBAC policies configured for ClusterCurator operations

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create test service account: `oc create serviceaccount clustercurator-test -n ocm`<br/>UI: Administration → Service Accounts → Create Service Account | CLI verification: `serviceaccount/clustercurator-test created`<br/>UI verification: Service account appears in ocm namespace list |
| 2. Create appropriate RBAC role for ClusterCurator operations:<br/>```yaml<br/>apiVersion: rbac.authorization.k8s.io/v1<br/>kind: ClusterRole<br/>metadata:<br/>  name: clustercurator-operator<br/>rules:<br/>- apiGroups: ["cluster.open-cluster-management.io"]<br/>  resources: ["clustercurators", "managedclusteractions", "managedclusterviews"]<br/>  verbs: ["get", "list", "create", "update", "patch"]<br/>```<br/>CLI: `oc apply -f clustercurator-role.yaml`<br/>UI: Administration → Roles → Create Role | CLI verification: `clusterrole.rbac.authorization.k8s.io/clustercurator-operator created`<br/>UI verification: ClusterRole visible in roles list with correct permissions |
| 3. Bind role to service account: `oc create clusterrolebinding clustercurator-test --clusterrole=clustercurator-operator --serviceaccount=ocm:clustercurator-test`<br/>UI: Administration → Role Bindings → Create Binding | CLI verification: `clusterrolebinding.rbac.authorization.k8s.io/clustercurator-test created`<br/>UI verification: RoleBinding shows correct service account and role association |
| 4. Test permissions validation: `oc auth can-i create clustercurators --as=system:serviceaccount:ocm:clustercurator-test`<br/>UI: N/A | CLI verification: Returns `yes` - service account can create ClusterCurators<br/>UI verification: N/A |
| 5. **Multi-Cluster Scenario**: Create ClusterCurator for first cluster:<br/>```yaml<br/>metadata:<br/>  name: upgrade-cluster-1<br/>  namespace: ocp<br/>spec:<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>```<br/>CLI: `oc apply -f clustercurator-cluster1.yaml --as=system:serviceaccount:ocm:clustercurator-test`<br/>UI: Create ClusterCurator targeting cluster-1 | CLI verification: ClusterCurator created successfully with service account permissions<br/>UI verification: ClusterCurator appears for cluster-1 with correct target version |
| 6. Create concurrent ClusterCurator for second cluster: modify namespace to target different managed cluster<br/>CLI: `oc apply -f clustercurator-cluster2.yaml --as=system:serviceaccount:ocm:clustercurator-test`<br/>UI: Create second ClusterCurator for different cluster | CLI verification: Second ClusterCurator created independently<br/>UI verification: Both ClusterCurators show in different namespaces without conflicts |
| 7. Monitor both upgrades for independence: `oc get clustercurator -A --watch | grep -E "(upgrade-cluster-[12])"`<br/>UI: Search → Kind:ClusterCurator → Watch mode | CLI verification: Both show independent progress states (Processing/Completed)<br/>UI verification: Each ClusterCurator progresses independently without state interference |
| 8. Verify separate resource isolation: `oc get managedclusterview -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,CURATOR:.metadata.labels.cluster\\.open-cluster-management\\.io/curator`<br/>UI: Search → ManagedClusterView → Custom columns view | CLI verification: Each cluster has separate ManagedClusterView with correct curator labels<br/>UI verification: Resources properly isolated by namespace and curator labels |
| 9. Cleanup and verify no resource leaks: `oc delete clustercurator -A --all`<br/>UI: Bulk delete all ClusterCurators | CLI verification: All ClusterCurators deleted, associated ManagedClusterViews cleaned up<br/>UI verification: Search results show no remaining ClusterCurator resources |
