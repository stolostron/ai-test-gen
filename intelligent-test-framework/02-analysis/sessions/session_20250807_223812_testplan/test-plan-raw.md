## Cleanup and Final Verification

| Test Steps | Expected Results |
|------------|------------------|
| 1. Remove all test namespaces: `oc delete namespace digest-upgrade-test` | Namespace deleted successfully |
| 2. Verify no orphaned ManagedClusterViews: `oc get managedclusterview -A \| grep test` | No test-related resources remain |
| 3. Confirm managed clusters still healthy: `oc get managedcluster -o custom-columns=NAME:.metadata.name,AVAILABLE:.status.conditions[?@.type=='ManagedClusterConditionAvailable'].status` | All managed clusters show Available=True |
