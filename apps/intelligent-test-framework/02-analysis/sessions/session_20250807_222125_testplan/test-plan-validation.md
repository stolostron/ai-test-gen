## Cleanup and Final Verification

| Test Steps | Expected Results |
|------------|------------------|
| 1. Clean up all test ClusterCurator resources: `oc delete clustercurator --all -A --timeout=300s` | All test ClusterCurator resources removed within 5 minutes; command returns `No resources found` on subsequent queries |
| 2. Verify no orphaned ManagedClusterViews exist: `oc get managedclusterview -A --field-selector='metadata.name!=klusterlet-addon-workmgr'` | Only system ManagedClusterViews remain; no test-created views with custom labels persist |
| 3. Check ManagedClusterAction cleanup: `oc get managedclusteraction -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.namespace}{"\t"}{.metadata.labels.test-id}{"\n"}{end}'` | No resources with test-id labels remain; only system-generated actions persist |
| 4. Validate managed cluster connectivity: `oc get managedcluster -o custom-columns=NAME:.metadata.name,AVAILABLE:.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status,JOINED:.status.conditions[?(@.type=="ManagedClusterJoined")].status` | All managed clusters show Available=True and Joined=True; no clusters in Unknown or False state |
| 5. Verify hub cluster resource utilization: `oc adm top nodes --selector='node-role.kubernetes.io/control-plane'` | Control plane nodes show normal CPU/memory usage (<80%); no resource exhaustion from test activities |
| 6. Check for any remaining test artifacts: `oc get all -A -l test-scenario=acm-22079 --ignore-not-found` | Command returns `No resources found`; all test-labeled resources successfully removed |
| 7. Validate ACM operator health: `oc get pods -n open-cluster-management -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,READY:.status.containerStatuses[*].ready` | All ACM pods in Running state with Ready=true; no pods in CrashLoopBackOff or Error state |
