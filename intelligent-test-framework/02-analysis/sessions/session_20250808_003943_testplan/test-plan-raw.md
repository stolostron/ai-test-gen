# Test Plan for ACM-22079: Support digest-based upgrades via ClusterCurator

## Test Case 1: Digest-Based Upgrade Success Scenarios
**Setup**: 
- ACM hub cluster with managed cluster already imported
- Target cluster must be OpenShift 4.12+ with available updates
- Test user must have cluster-admin permissions on both hub and managed cluster
- Verify `oc get managedcluster <cluster-name>` shows Available=True

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster: `oc login https://api.hub-cluster.example.com:6443 -u testuser`<br/>UI: ACM Console → Login with credentials | CLI verification: `Login successful. You have access to X projects...`<br/>UI verification: ACM Console dashboard loads successfully |
| 2. Create test namespace: `oc create namespace ocp`<br/>UI: Administration → Namespaces → Create Namespace | CLI verification: `namespace/ocp created`<br/>UI verification: Namespace 'ocp' appears in namespace list |
| 3. Create ClusterCurator with force annotation:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: digest-upgrade-test<br/>  namespace: ocp<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>    channel: "stable-4.15"<br/>```<br/>Apply with: `oc apply -f clustercurator.yaml`<br/>UI: Cluster lifecycle → Upgrade clusters → Create ClusterCurator | CLI verification: `clustercurator.cluster.open-cluster-management.io/digest-upgrade-test created`<br/>UI verification: ClusterCurator appears in cluster lifecycle view |
| 4. Verify annotation is set: `oc get clustercurator digest-upgrade-test -n ocp -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'`<br/>UI: Cluster lifecycle → ClusterCurator details → Annotations tab | CLI verification: Output shows `"true"`<br/>UI verification: Annotation visible in ClusterCurator details |
| 5. Monitor ManagedClusterView creation: `oc get managedclusterview -n ocp --watch`<br/>UI: Search → Kind:ManagedClusterView → namespace:ocp | CLI verification: New ManagedClusterView appears with name pattern `digest-upgrade-test-cv-xxxxx`<br/>UI verification: ManagedClusterView resource shows in search results |
| 6. Check ManagedClusterView retrieves ClusterVersion: `oc get managedclusterview -n ocp -o jsonpath='{.items[0].status.result.status.conditionalUpdates[0].image}'`<br/>UI: N/A | CLI verification: Returns digest format `quay.io/openshift-release-dev/ocp-release@sha256:abc123...`<br/>UI verification: N/A |
| 7. Verify ManagedClusterAction uses digest (not tag): `oc get managedclusteraction -n ocp -o yaml | grep -A5 "desiredUpdate"`<br/>UI: Search → Kind:ManagedClusterAction → View YAML | CLI verification: Shows image with digest format, NO force: true flag<br/>UI verification: YAML view shows desiredUpdate with digest format |

## Test Case 2: Tag-Based Fallback and Error Handling
**Setup**:
- Same environment as Test Case 1
- Configure scenario where target version has no digest available
- Ensure test cluster has connectivity to verify fallback behavior

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster: `oc login https://api.hub-cluster.example.com:6443 -u testuser`<br/>UI: ACM Console → Login | CLI verification: Login successful with cluster context<br/>UI verification: Console session active |
| 2. Create ClusterCurator targeting version with no digest:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: fallback-test<br/>  namespace: ocp<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.14.99"<br/>    channel: "stable-4.14"<br/>```<br/>Apply with: `oc apply -f fallback-clustercurator.yaml`<br/>UI: Cluster lifecycle → Create ClusterCurator | CLI verification: `clustercurator.cluster.open-cluster-management.io/fallback-test created`<br/>UI verification: ClusterCurator created in console |
| 3. Monitor upgrade process: `oc get clustercurator fallback-test -n ocp -o jsonpath='{.status.conditions[*].message}'`<br/>UI: Cluster lifecycle → ClusterCurator details → Status | CLI verification: Shows progression through digest search failure<br/>UI verification: Status conditions show digest lookup attempt |
| 4. Verify tag-based fallback in ManagedClusterAction: `oc get managedclusteraction -n ocp -o yaml | grep -A10 "desiredUpdate"`<br/>UI: Search → ManagedClusterAction → View YAML | CLI verification: Shows tag format `quay.io/openshift-release-dev/ocp-release:4.14.99-multi` AND `force: true`<br/>UI verification: YAML shows tag format with force flag |
| 5. Create ClusterCurator WITHOUT force annotation:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: standard-test<br/>  namespace: ocp<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.8"<br/>    channel: "stable-4.15"<br/>```<br/>UI: Cluster lifecycle → Create ClusterCurator | CLI verification: ClusterCurator created without digest capability<br/>UI verification: ClusterCurator appears without special annotations |
| 6. Verify standard upgrade behavior: `oc get managedclusteraction -n ocp -o yaml | grep force`<br/>UI: Search → ManagedClusterAction → View YAML | CLI verification: Shows `force: true` (standard behavior)<br/>UI verification: YAML shows standard force flag behavior |
| 7. Create ClusterCurator with invalid version: modify desiredUpdate to "invalid.version.format"<br/>UI: Cluster lifecycle → Create ClusterCurator with invalid version | CLI verification: ClusterCurator created but upgrade should fail gracefully<br/>UI verification: Error status visible in console |
| 8. Check error messages: `oc get clustercurator -n ocp -o jsonpath='{.items[*].status.conditions[?(@.type=="Failed")].message}'`<br/>UI: ClusterCurator details → Conditions tab | CLI verification: Clear error message about invalid version format<br/>UI verification: Error condition displayed with descriptive message |

## Test Case 3: Multi-Cluster and Concurrent Scenarios
**Setup**:
- Multiple managed clusters (minimum 2) imported to ACM hub
- Both clusters must be available and healthy
- Different target versions for concurrent testing
- Verify clusters are in different namespaces

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub: `oc login https://api.hub.example.com:6443 -u testuser`<br/>UI: ACM Console → Login | CLI verification: Login successful to hub cluster<br/>UI verification: Console session established |
| 2. Create ClusterCurator for first cluster:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: cluster1-upgrade<br/>  namespace: ocp<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>    channel: "stable-4.15"<br/>```<br/>Apply with: `oc apply -f cluster1-curator.yaml`<br/>UI: Cluster lifecycle → Create ClusterCurator for cluster1 | CLI verification: `clustercurator.cluster.open-cluster-management.io/cluster1-upgrade created`<br/>UI verification: First ClusterCurator visible in lifecycle view |
| 3. Create ClusterCurator for second cluster (different namespace):<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: cluster2-upgrade<br/>  namespace: ocp<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.11"<br/>    channel: "stable-4.15"<br/>```<br/>UI: Create second ClusterCurator | CLI verification: Second ClusterCurator created simultaneously<br/>UI verification: Both ClusterCurators visible in console |
| 4. Monitor both upgrades concurrently: `oc get clustercurator -n ocp --watch`<br/>UI: Cluster lifecycle → Overview → Monitor both upgrades | CLI verification: Both show independent progress without conflicts<br/>UI verification: Console shows separate progress for each cluster |
| 5. Verify independent ManagedClusterViews: `oc get managedclusterview -n ocp | grep -E "(cluster1\|cluster2)"`<br/>UI: Search → Kind:ManagedClusterView → Filter by cluster names | CLI verification: Each cluster has separate ManagedClusterView resources<br/>UI verification: Separate ManagedClusterView entries for each cluster |
| 6. Check no resource conflicts: `oc get managedclusteraction -n ocp -o custom-columns=NAME:.metadata.name,TARGET:.spec.actionType`<br/>UI: Search → Kind:ManagedClusterAction → Custom columns view | CLI verification: Each action targets correct cluster without interference<br/>UI verification: Actions clearly separated by target cluster |
| 7. Verify digest extraction works independently: `oc get managedclusterview -n ocp -o jsonpath='{.items[*].status.result.status.conditionalUpdates[0].image}'`<br/>UI: N/A | CLI verification: Both clusters show appropriate digest formats for their target versions<br/>UI verification: N/A |

## Test Case 4: RBAC and Security Validation
**Setup**:
- Test service account with limited permissions
- ACM hub cluster with RBAC policies configured
- Managed cluster with different permission levels for testing

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create test service account: `oc create serviceaccount clustercurator-test -n ocp`<br/>UI: Administration → Service Accounts → Create | CLI verification: `serviceaccount/clustercurator-test created`<br/>UI verification: Service account appears in ocp namespace |
| 2. Create limited RBAC role:<br/>```yaml<br/>apiVersion: rbac.authorization.k8s.io/v1<br/>kind: ClusterRole<br/>metadata:<br/>  name: clustercurator-limited<br/>rules:<br/>- apiGroups: ["cluster.open-cluster-management.io"]<br/>  resources: ["clustercurators"]<br/>  verbs: ["get", "list", "create"]<br/>```<br/>Apply with: `oc apply -f limited-role.yaml`<br/>UI: Administration → Roles → Create ClusterRole | CLI verification: `clusterrole.rbac.authorization.k8s.io/clustercurator-limited created`<br/>UI verification: ClusterRole created with limited permissions |
| 3. Bind role to service account: `oc create clusterrolebinding clustercurator-test --clusterrole=clustercurator-limited --serviceaccount=ocp:clustercurator-test`<br/>UI: Administration → Role Bindings → Create ClusterRoleBinding | CLI verification: `clusterrolebinding.rbac.authorization.k8s.io/clustercurator-test created`<br/>UI verification: RoleBinding shows correct subject and role |
| 4. Test with limited permissions: `oc auth can-i create managedclusteraction --as=system:serviceaccount:ocp:clustercurator-test`<br/>UI: N/A | CLI verification: Returns `no` - service account cannot create ManagedClusterAction<br/>UI verification: N/A |
| 5. Verify ClusterCurator creation works: `oc create -f clustercurator.yaml --as=system:serviceaccount:ocp:clustercurator-test`<br/>UI: N/A | CLI verification: ClusterCurator created (controller will handle ManagedClusterAction)<br/>UI verification: N/A |
| 6. Check controller creates ManagedClusterAction: `oc get managedclusteraction -n ocp`<br/>UI: Search → Kind:ManagedClusterAction | CLI verification: ManagedClusterAction created by controller, not test user<br/>UI verification: ManagedClusterAction visible in console |
| 7. Verify audit logs capture permission checks: `oc logs -n open-cluster-management deployment/clustercurator-controller | grep "RBAC"`<br/>UI: Workloads → Deployments → clustercurator-controller → Logs | CLI verification: Shows proper permission validation in controller logs<br/>UI verification: Logs show RBAC validation entries |
| 8. Cleanup test resources: `oc delete clusterrolebinding clustercurator-test && oc delete clusterrole clustercurator-limited && oc delete serviceaccount clustercurator-test -n ocp`<br/>UI: Delete resources via console | CLI verification: All test RBAC resources removed cleanly<br/>UI verification: Resources no longer visible in console |
