| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into hub: `oc whoami` | Shows logged-in user |
| 2. Verify API access: `oc get ns` | Namespaces listed successfully |
| 3. Check CRDs: `oc api-resources | grep -i clustercurator` | ClusterCurator API present |
