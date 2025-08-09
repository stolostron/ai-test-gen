# Test Plan for ACM-22079: Support digest-based upgrades via ClusterCurator

## Test Case 1: Digest-Based Upgrade Success Scenarios

**Setup**: 
- ACM hub cluster with managed cluster imported (verify with `oc get managedcluster`)
- Target managed cluster must be OpenShift 4.12+ with available updates
- Test user requires cluster-admin permissions on hub cluster
- Ensure managed cluster namespace exists

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster:<br/>CLI: `oc login https://api.hub-cluster.example.com:6443 -u testuser`<br/>UI: Access ACM console → User menu → Copy login command | CLI verification: `Login successful. You have access to X projects...`<br/>UI verification: Console session active, user authenticated |
| 2. Verify managed cluster availability:<br/>CLI: `oc get managedcluster managed-cluster-1 -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'`<br/>UI: Clusters → All Clusters → Check status | CLI verification: Returns `True` confirming cluster ready<br/>UI verification: Cluster shows "Ready" status with green indicator |
| 3. Create ClusterCurator with force annotation for digest upgrade:<br/>CLI: Create file with:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: digest-upgrade-test<br/>  namespace: ocp<br/>  annotations:<br/>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.15.10"<br/>    channel: "stable-4.15"<br/>```<br/>Apply: `oc apply -f clustercurator.yaml`<br/>UI: Cluster lifecycle → Create curator → Fill form with same values | CLI verification: `clustercurator.cluster.open-cluster-management.io/digest-upgrade-test created`<br/>UI verification: New curator appears in list with "Created" status |
| 4. Verify force annotation enables digest lookup:<br/>CLI: `oc get clustercurator digest-upgrade-test -n ocp -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'`<br/>UI: Cluster lifecycle → Curators → digest-upgrade-test → Details tab | CLI verification: Returns `"true"` confirming annotation set<br/>UI verification: Annotation visible in metadata section |
| 5. Monitor ManagedClusterView creation for digest retrieval:<br/>CLI: `oc get managedclusterview -n ocp -l curator=digest-upgrade-test --watch`<br/>UI: N/A | CLI verification: New ManagedClusterView appears with name pattern `digest-upgrade-test-cv-*`<br/>UI verification: N/A |
| 6. Verify digest-based image retrieval from conditionalUpdates:<br/>CLI: `oc get managedclusterview -n ocp -l curator=digest-upgrade-test -o jsonpath='{.items[0].status.result.status.conditionalUpdates[?(@.version=="4.15.10")].image}'`<br/>UI: N/A | CLI verification: Returns digest format `quay.io/openshift-release-dev/ocp-release@sha256:abc123...`<br/>UI verification: N/A |
| 7. Verify ManagedClusterAction uses digest (not tag or force):<br/>CLI: `oc get managedclusteraction -n ocp -o yaml | grep -A10 "desiredUpdate"`<br/>UI: N/A | CLI verification: Shows image with digest format AND no `force: true` flag present<br/>UI verification: N/A |
| 8. Monitor upgrade progress and completion:<br/>CLI: `oc get clustercurator digest-upgrade-test -n ocp -o jsonpath='{.status.conditions[*].type}'`<br/>UI: Cluster lifecycle → Curators → digest-upgrade-test → Status | CLI verification: Shows progression: "Progressing" → "Complete"<br/>UI verification: Status changes from "In Progress" to "Complete" with success indicator |

## Test Case 2: Fallback Mechanisms and Error Handling

**Setup**:
- Same environment as Test Case 1
- Prepare test scenarios for digest unavailability
- Ensure access to ClusterCurator controller logs

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create ClusterCurator targeting version only in availableUpdates:<br/>CLI: Create YAML with `desiredUpdate: "4.15.9"` (modify from previous example)<br/>Apply: `oc apply -f clustercurator-fallback.yaml`<br/>UI: Create new curator with version 4.15.9 | CLI verification: ClusterCurator created successfully<br/>UI verification: New curator appears with specified version |
| 2. Verify fallback to availableUpdates when conditionalUpdates lacks digest:<br/>CLI: `oc get managedclusterview -n ocp -o jsonpath='{.items[0].status.result.status.availableUpdates[?(@.version=="4.15.9")].image}'`<br/>UI: N/A | CLI verification: Returns digest extracted from availableUpdates array<br/>UI verification: N/A |
| 3. Test without force annotation (remove annotation from YAML):<br/>CLI: Delete previous curator: `oc delete clustercurator -n ocp --all`<br/>Create new without annotation<br/>UI: Delete previous curator → Create new without force annotation | CLI verification: ClusterCurator created without digest capability<br/>UI verification: New curator created, no special annotations visible |
| 4. Verify standard behavior without force annotation:<br/>CLI: `oc get managedclusteraction -n ocp -o yaml | grep -E "(force|image)"`<br/>UI: N/A | CLI verification: Shows `force: true` and tag format image (standard behavior)<br/>UI verification: N/A |
| 5. Test error handling with invalid version format:<br/>CLI: Create ClusterCurator with `desiredUpdate: "invalid.version.format"`<br/>UI: Create curator with invalid version in form | CLI verification: ClusterCurator created but validation should fail<br/>UI verification: Form may show validation warning or curator shows error state |
| 6. Check error reporting and status conditions:<br/>CLI: `oc get clustercurator -n ocp -o jsonpath='{.items[0].status.conditions[?(@.type=="Failed")].message}'`<br/>UI: Check curator status in console | CLI verification: Clear error message about invalid version format<br/>UI verification: Error message visible in status section |
| 7. Verify controller logs capture error handling:<br/>CLI: `oc logs -n open-cluster-management deployment/clustercurator-controller | grep -i "digest\|error"`<br/>UI: N/A | CLI verification: Logs show digest lookup attempts and graceful failure handling<br/>UI verification: N/A |

## Test Case 3: Multi-Cluster and Concurrent Operations

**Setup**:
- Multiple managed clusters (minimum 2) imported to ACM hub
- Each cluster should have different namespaces in hub
- Verify cluster isolation and resource naming

| Test Steps | Expected Results |
|------------|------------------|
| 1. Verify multiple managed clusters available:<br/>CLI: `oc get managedcluster -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[0].status`<br/>UI: Clusters → All Clusters → View cluster list | CLI verification: Shows at least 2 clusters with "True" status<br/>UI verification: Multiple clusters visible with "Ready" status |
| 2. Create concurrent ClusterCurators for different clusters:<br/>CLI: Apply curator for cluster-1 namespace: `oc apply -f clustercurator-cluster1.yaml`<br/>Apply curator for cluster-2 namespace: `oc apply -f clustercurator-cluster2.yaml`<br/>UI: Create curators for different clusters simultaneously | CLI verification: Both ClusterCurators created successfully<br/>UI verification: Multiple curators appear in different namespaces |
| 3. Monitor independent ManagedClusterView creation:<br/>CLI: `oc get managedclusterview -A | grep -E "(cluster-1|cluster-2)"`<br/>UI: N/A | CLI verification: Each cluster has separate ManagedClusterView resources without naming conflicts<br/>UI verification: N/A |
| 4. Verify no resource conflicts between concurrent operations:<br/>CLI: `oc get managedclusteraction -A -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,TARGET:.spec.actionRequest.object.metadata.name`<br/>UI: N/A | CLI verification: Each action targets correct cluster without interference<br/>UI verification: N/A |
| 5. Check independent progress tracking:<br/>CLI: `oc get clustercurator -A --watch`<br/>UI: Monitor all curators in console | CLI verification: Both show independent progress without blocking each other<br/>UI verification: Progress bars/statuses update independently |
| 6. Verify cleanup isolation after completion:<br/>CLI: `oc delete clustercurator -n cluster-1-namespace --all`<br/>Check cluster-2 resources unaffected: `oc get clustercurator -n cluster-2-namespace`<br/>UI: Delete curator from one cluster, verify others unaffected | CLI verification: Only cluster-1 resources deleted, cluster-2 resources remain intact<br/>UI verification: Deletion affects only selected curator, others remain visible |

## Test Case 4: RBAC and Security Validation

**Setup**:
- Create test service account with limited permissions
- Prepare RBAC policies for testing permission boundaries
- Access to controller and audit logs

| Test Steps | Expected Results |
|------------|------------------|
| 1. Create limited test service account:<br/>CLI: `oc create serviceaccount clustercurator-test -n default`<br/>UI: N/A | CLI verification: `serviceaccount/clustercurator-test created`<br/>UI verification: N/A |
| 2. Create restricted ClusterRole for testing:<br/>CLI: Apply YAML:<br/>```yaml<br/>apiVersion: rbac.authorization.k8s.io/v1<br/>kind: ClusterRole<br/>metadata:<br/>  name: clustercurator-limited<br/>rules:<br/>- apiGroups: ["cluster.open-cluster-management.io"]<br/>  resources: ["clustercurators"]<br/>  verbs: ["get", "list", "create"]<br/>```<br/>UI: N/A | CLI verification: ClusterRole created with limited permissions only<br/>UI verification: N/A |
| 3. Bind limited role to test service account:<br/>CLI: `oc create clusterrolebinding clustercurator-test --clusterrole=clustercurator-limited --serviceaccount=default:clustercurator-test`<br/>UI: N/A | CLI verification: RoleBinding created successfully<br/>UI verification: N/A |
| 4. Test permission boundaries for ManagedClusterAction:<br/>CLI: `oc auth can-i create managedclusteraction --as=system:serviceaccount:default:clustercurator-test`<br/>UI: N/A | CLI verification: Returns `no` - service account cannot create ManagedClusterAction directly<br/>UI verification: N/A |
| 5. Verify ClusterCurator creation works with limited permissions:<br/>CLI: `oc create -f clustercurator.yaml --as=system:serviceaccount:default:clustercurator-test`<br/>UI: N/A | CLI verification: ClusterCurator created successfully (controller handles privileged operations)<br/>UI verification: N/A |
| 6. Confirm controller creates ManagedClusterAction with proper service account:<br/>CLI: `oc get managedclusteraction -n ocp -o jsonpath='{.items[0].metadata.ownerReferences[0].name}'`<br/>UI: N/A | CLI verification: Shows ClusterCurator as owner, confirming controller created the action<br/>UI verification: N/A |
| 7. Verify audit trail captures permission validation:<br/>CLI: `oc logs -n open-cluster-management deployment/clustercurator-controller | grep -i "rbac\|permission"`<br/>UI: N/A | CLI verification: Shows proper permission checks and service account usage in logs<br/>UI verification: N/A |
| 8. Cleanup test resources:<br/>CLI: `oc delete clusterrolebinding clustercurator-test`<br/>`oc delete clusterrole clustercurator-limited`<br/>`oc delete serviceaccount clustercurator-test -n default`<br/>UI: N/A | CLI verification: All test RBAC resources cleaned up successfully<br/>UI verification: N/A |
