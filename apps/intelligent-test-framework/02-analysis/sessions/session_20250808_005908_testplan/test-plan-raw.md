# Test Plan for ACM-22079: Support digest-based upgrades via ClusterCurator

## Setup and Prerequisites
- ACM hub cluster with ClusterCurator operator installed and running
- At least one managed OpenShift cluster (4.12+) imported into ACM hub
- Test user with cluster-admin permissions on both hub and managed clusters
- Target managed cluster must have available updates in its update graph
- Network connectivity for digest resolution from release registry

### Test Case 1: Digest-Based Upgrade Success Scenarios
**Description**: Validates that ClusterCurator can successfully discover and use digest-based images for upgrades when the force annotation is present, and falls back to availableUpdates when conditionalUpdates are not available.

**Setup**: 
- Managed cluster must be in Available state with known update channels
- Target upgrade version should exist in either conditionalUpdates or availableUpdates
- Verify managed cluster has update recommendations available

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster and verify connectivity<br/>CLI: `oc login https://api.hub-cluster.example.com:6443 -u testuser`<br/>UI: Navigate to ACM Console → Login with credentials | CLI verification: `Login successful. You have access to X projects...` showing correct cluster context<br/>UI verification: ACM Console dashboard loads successfully |
| 2. Create test namespace for organized testing<br/>CLI: `oc create namespace digest-upgrade-test`<br/>UI: N/A | CLI verification: `namespace/digest-upgrade-test created` - ensures clean test environment<br/>UI verification: N/A |
| 3. Apply ClusterCurator with force annotation for digest support<br/>CLI: Create file with YAML below and apply with `oc apply -f clustercurator.yaml`<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: digest-upgrade-test<br/>  namespace: ocp<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>    channel: "stable-4.15"<br/>```<br/>UI: Cluster lifecycle → Curators → Create ClusterCurator | CLI verification: `clustercurator.cluster.open-cluster-management.io/digest-upgrade-test created` - confirms resource creation<br/>UI verification: New curator appears in Curators list with pending status |
| 4. Verify force annotation is properly set for digest discovery<br/>CLI: `oc get clustercurator digest-upgrade-test -n ocp -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'`<br/>UI: Cluster lifecycle → Curators → digest-upgrade-test → Details → Annotations | CLI verification: Output shows `"true"` - enables digest-based upgrade capability<br/>UI verification: Annotation visible in resource details panel |
| 5. Monitor ManagedClusterView creation for ClusterVersion retrieval<br/>CLI: `oc get managedclusterview -n ocp --watch` (watch for new resources)<br/>UI: Search → Kind: ManagedClusterView → Filter by namespace | CLI verification: New ManagedClusterView appears with name pattern `digest-upgrade-test-cv-*` - shows controller created view<br/>UI verification: ManagedClusterView resource visible in search results |
| 6. Verify digest extraction from conditionalUpdates<br/>CLI: `oc get managedclusterview -n ocp -o jsonpath='{.items[?(@.metadata.name=="digest-upgrade-test-cv*")].status.result.status.conditionalUpdates[0].image}'`<br/>UI: Search results → Select ManagedClusterView → View YAML → Status section | CLI verification: Returns digest format `quay.io/openshift-release-dev/ocp-release@sha256:abc123...` - validates digest discovery<br/>UI verification: Image field shows digest format in status.result |
| 7. Confirm ManagedClusterAction uses digest without force flag<br/>CLI: `oc get managedclusteraction -n ocp -o yaml \| grep -A10 "desiredUpdate"`<br/>UI: Search → Kind: ManagedClusterAction → View latest action | CLI verification: Shows image with digest format and NO `force: true` flag - proves digest-based upgrade<br/>UI verification: Action spec shows digest image without force parameter |

### Test Case 2: Tag-Based Fallback and Error Handling  
**Description**: Tests the fallback mechanism when digest discovery fails and validates proper error handling for invalid upgrade targets.

**Setup**:
- Use managed cluster where target version may not be in conditionalUpdates
- Prepare scenarios with invalid version formats for error testing
- Ensure network access to verify tag-based fallback behavior

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create ClusterCurator targeting version likely in availableUpdates only<br/>CLI: Apply YAML with `desiredUpdate: "4.14.25"` (older version)<br/>UI: Create new ClusterCurator with different target version | CLI verification: ClusterCurator created successfully - tests fallback scenario setup<br/>UI verification: Resource appears in Curators list |
| 2. Verify fallback to availableUpdates when conditionalUpdates empty<br/>CLI: `oc get managedclusterview -n ocp -o jsonpath='{.status.result.status.availableUpdates[?(@.version=="4.14.25")].image}'`<br/>UI: Check ManagedClusterView status for availableUpdates array | CLI verification: Shows digest extracted from availableUpdates array - confirms fallback logic works<br/>UI verification: Status shows availableUpdates contains target version |
| 3. Test upgrade with version having no digest available<br/>CLI: Create ClusterCurator with `desiredUpdate: "4.14.99"` (non-existent version)<br/>UI: N/A | CLI verification: ClusterCurator created but will demonstrate tag fallback - tests edge case handling<br/>UI verification: N/A |
| 4. Monitor tag-based fallback in ManagedClusterAction<br/>CLI: `oc get managedclusteraction -n ocp -o yaml \| grep -A5 "force\|desiredUpdate"`<br/>UI: View ManagedClusterAction details | CLI verification: Shows tag format `quay.io/openshift-release-dev/ocp-release:4.14.99-multi` AND `force: true` - validates fallback<br/>UI verification: Action shows tag-based image with force parameter |
| 5. Create ClusterCurator WITHOUT force annotation to test standard behavior<br/>CLI: Apply YAML without the annotation line<br/>UI: Create ClusterCurator with standard configuration | CLI verification: ClusterCurator created successfully - establishes baseline comparison<br/>UI verification: Resource created without special annotations |
| 6. Verify standard upgrade behavior without digest capability<br/>CLI: `oc get managedclusteraction -n ocp -o yaml \| grep force`<br/>UI: Check action parameters | CLI verification: Shows `force: true` (standard behavior) - confirms annotation controls digest logic<br/>UI verification: Action uses standard upgrade parameters |
| 7. Test error handling with invalid version format<br/>CLI: Create ClusterCurator with `desiredUpdate: "invalid.version.format"`<br/>UI: N/A | CLI verification: ClusterCurator created but upgrade fails gracefully - validates input validation<br/>UI verification: N/A |
| 8. Check comprehensive error messages<br/>CLI: `oc get clustercurator -n ocp -o jsonpath='{.items[*].status.conditions[?(@.type=="Failed")].message}'`<br/>UI: View ClusterCurator status conditions | CLI verification: Clear error message about invalid version format - ensures proper user feedback<br/>UI verification: Error condition visible in resource status |

### Test Case 3: Multi-Cluster and RBAC Validation
**Description**: Validates digest-based upgrades work correctly across multiple managed clusters simultaneously and verifies proper RBAC behavior for different user permission levels.

**Setup**:
- Multiple managed clusters (minimum 2) imported into ACM hub
- Test service account with limited ClusterCurator permissions
- RBAC policies configured to test permission boundaries

| Test Steps | Expected Results |
|------------|------------------|
| 1. Verify multiple managed clusters available<br/>CLI: `oc get managedcluster \| grep Available`<br/>UI: Cluster management → Clusters → Filter by Available | CLI verification: Shows 2+ clusters in Available state - ensures multi-cluster test environment<br/>UI verification: Multiple clusters visible with Available status |
| 2. Create concurrent ClusterCurator resources for different clusters<br/>CLI: Apply two YAML files with different namespace values (ocp, ocp-staging)<br/>UI: Create multiple ClusterCurators targeting different clusters | CLI verification: Both ClusterCurators created successfully - tests concurrent resource handling<br/>UI verification: Multiple curators appear in list with different target clusters |
| 3. Monitor independent digest discovery across clusters<br/>CLI: `oc get managedclusterview -A \| grep -E "(ocp\|ocp-staging)"`<br/>UI: Search across all namespaces for ManagedClusterViews | CLI verification: Each cluster has separate ManagedClusterView resources - validates isolation<br/>UI verification: Views show different clusters without resource conflicts |
| 4. Verify no cross-cluster resource interference<br/>CLI: `oc get managedclusteraction -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,TARGET:.spec.actionRequest.object.metadata.name`<br/>UI: View all ManagedClusterActions across namespaces | CLI verification: Each action targets correct cluster without interference - confirms proper isolation<br/>UI verification: Actions correctly scoped to intended clusters |
| 5. Create test service account with limited permissions<br/>CLI: `oc create serviceaccount clustercurator-test -n default && oc create clusterrole clustercurator-limited --verb=get,list,create --resource=clustercurators`<br/>UI: N/A | CLI verification: Service account and limited role created - establishes RBAC test scenario<br/>UI verification: N/A |
| 6. Test ClusterCurator creation with limited permissions<br/>CLI: `oc create -f clustercurator.yaml --as=system:serviceaccount:default:clustercurator-test`<br/>UI: N/A | CLI verification: ClusterCurator created successfully (controller handles ManagedClusterAction) - validates permission model<br/>UI verification: N/A |
| 7. Verify controller creates ManagedClusterAction with proper service account<br/>CLI: `oc get managedclusteraction -n ocp -o jsonpath='{.items[0].metadata.ownerReferences[0].name}'`<br/>UI: Check ManagedClusterAction owner references | CLI verification: Shows ClusterCurator as owner, not test user - confirms controller-driven security model<br/>UI verification: Owner reference points to ClusterCurator resource |
| 8. Clean up test resources and verify proper deletion<br/>CLI: `oc delete clustercurator --all -n ocp && oc delete namespace digest-upgrade-test`<br/>UI: Delete ClusterCurators from Curators list | CLI verification: All resources deleted cleanly without errors - ensures proper cleanup<br/>UI verification: Resources removed from UI listings |
