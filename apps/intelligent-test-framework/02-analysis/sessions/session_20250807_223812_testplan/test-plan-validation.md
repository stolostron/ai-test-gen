## Cleanup and Final Verification

| Test Steps | Expected Results |
|------------|------------------|
| 1. Remove all test namespaces: `oc delete namespace digest-upgrade-test --timeout=60s` | Namespace deleted successfully with confirmation message "namespace 'digest-upgrade-test' deleted" |
| 2. Verify no orphaned ManagedClusterViews remain: `oc get managedclusterview -A --field-selector metadata.namespace=digest-upgrade-test` | No resources found or command returns empty result |
| 3. Check for any remaining test-related ClusterRoles: `oc get clusterrole | grep digest-upgrade` | No test-related ClusterRoles exist |
| 4. Verify no test-related ClusterRoleBindings: `oc get clusterrolebinding | grep digest-upgrade` | No test-related ClusterRoleBindings exist |
| 5. Confirm all managed clusters are healthy: `oc get managedcluster -o custom-columns=NAME:.metadata.name,AVAILABLE:.status.conditions[?@.type=='ManagedClusterConditionAvailable'].status,JOINED:.status.conditions[?@.type=='ManagedClusterJoined'].status` | All managed clusters show Available=True and Joined=True |
| 6. Validate multicluster-observability-operator is running: `oc get pods -n open-cluster-management-observability -l name=multicluster-observability-operator` | Pod is Running with Ready status 1/1 |
| 7. Check observability addon status on all managed clusters: `oc get managedclusteraddon -A -l addon.open-cluster-management.io/namespace=open-cluster-management-observability` | All observability addons show Available=True |
| 8. Verify no test data remains in observability storage: `oc exec -n open-cluster-management-observability deployment/observability-thanos-query -- /bin/sh -c "curl -s 'http://localhost:9090/api/v1/label/__name__/values' | grep -i test"` | No test-related metrics or labels found |
