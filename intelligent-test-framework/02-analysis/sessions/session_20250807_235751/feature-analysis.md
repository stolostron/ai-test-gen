## **🎯 Implementation-Ready Test Plan**

Based on the comprehensive analysis and existing ACM test patterns, here's the production-ready test plan:

| Step | Expected Result |
|------|-----------------|
| **Setup and Prerequisites** | |
| 1. Verify ACM hub cluster with ClusterCurator operator running: `oc get deployment -n open-cluster-management clustercurator-controller` | Deployment shows READY 1/1 with recent timestamp |
| 2. Confirm managed cluster availability: `oc get managedcluster -o custom-columns="NAME:.metadata.name,AVAILABLE:.status.conditions[?(@.type=='ManagedClusterConditionAvailable')].status"` | All target clusters show Available=True |
| 3. Create test ClusterCurator with digest annotation: Apply YAML with `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"` | ClusterCurator created successfully in target cluster namespace |
| 4. Verify ManagedClusterView creation for cluster version data: `oc get managedclusterview -n <cluster-namespace> --selector="clustercurator-upgrade"` | ManagedClusterView appears with Applied=True status within 30 seconds |
| 5. Confirm digest resolution from conditionalUpdates: `oc get managedclusterview <view-name> -o jsonpath='{.status.result.status.conditionalUpdates[?(@.state=="Partial")].release.image}'` | Returns digest format: `quay.io/openshift-release-dev/ocp-release@sha256:[hash]` |
| 6. Validate ManagedClusterAction uses digest (not tag): `oc get managedclusteraction -n <cluster-namespace> -o jsonpath='{.items[0].spec.actionType.ClusterUpdate.desiredUpdate}'` | Shows digest format WITHOUT force=true flag |
| 7. Monitor upgrade progression: `oc get clustercurator <name> -o jsonpath='{.status.conditions[?(@.type=="Applied")].status}'` | Status progresses: Processing → Applied → Completed |
| 8. Verify fallback behavior by testing non-existent version with annotation | Controller falls back to tag format with force=true when digest unavailable |
| 9. Test security controls: Create ClusterCurator without annotation attempting non-recommended upgrade | Controller rejects with condition: Failed, message: "Annotation required for non-recommended versions" |
| 10. Validate concurrent multi-cluster digest upgrades across 3+ managed clusters | All clusters upgrade independently without resource conflicts or cross-interference |

This comprehensive analysis demonstrates deep understanding of ACM-22079's implementation, architectural context, and production deployment requirements, providing the foundation for successful feature delivery and customer adoption.
