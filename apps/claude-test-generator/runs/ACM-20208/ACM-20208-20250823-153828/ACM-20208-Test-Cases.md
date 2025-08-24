# Test Cases for ACM-20208: Support Hub Name Access for RBAC Users

## Description
Comprehensive E2E test plan for validating RBAC user access to hub cluster name functionality in ACM Console. This feature enables users without ManagedCluster permissions to access console functionality that depends on hub cluster name, preventing console crashes and ensuring consistent user experience across all permission levels.

## Setup
**Prerequisites:**
- ACM 2.14.0+ cluster with console access
- Multiple test users with different RBAC permission levels
- Hub cluster accessible via console at https://console-openshift-console.apps.CLUSTER-HOST
- Test users: kubeadmin (full access), cluster-admin user, namespace-admin user, application-manager user

**Environment Variables:**
- CLUSTER_HOST: Target cluster hostname
- HUB_CLUSTER_NAME: Expected hub cluster name (typically "local-cluster")
- TEST_USERS: Available test user credentials

## Test Cases

### Test Case 1: Verify RBAC User Console Access Without ManagedCluster Permissions

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console - Access ACM Console with restricted user credentials | Navigate to https://console-openshift-console.apps.CLUSTER-HOST, complete OpenShift authentication with cluster-admin test user | Verify console accessibility: `curl -k -I https://console-openshift-console.apps.CLUSTER-HOST/health` | Console loads successfully, authentication completes, ACM interface visible with hub cluster context |
| 2 | Navigate to Applications Section - Access application management features with restricted user | Click "Applications" in main navigation menu, observe console behavior and hub name display | Verify API access: `oc get applications.argoproj.io -A --as=system:admin` | Applications page loads without errors, hub cluster name displays correctly in UI headers and breadcrumbs |
| 3 | Access Application Topology View - Validate ACM-20085 fix for console crashes with restricted users | Select any application, click "Topology" tab, verify console stability and hub name display | Validate backend hub name API: `curl -X GET https://console-openshift-console.apps.CLUSTER-HOST/multicloud/hub -H "Authorization: Bearer $(oc whoami -t)"` | Topology view loads successfully, no console crashes, hub cluster name visible in topology context, API returns localHubName field |
| 4 | Verify Hub Name API Integration - Confirm backend service account bypass works correctly | Inspect browser network tab for /multicloud/hub API calls, verify response contains localHubName | Test API endpoint: `curl -X GET https://console-openshift-console.apps.CLUSTER-HOST/multicloud/hub -H "Authorization: Bearer $(oc whoami -t)" -H "Accept: application/json" \| jq '.localHubName'` | API returns JSON with localHubName field containing correct hub cluster name, authentication required but ManagedCluster permissions not needed |
| 5 | Test Console Feature Consistency - Ensure hub name access works across all console sections | Navigate through Clusters, Governance, Search sections, verify hub name context maintained | Verify ManagedCluster access status: `oc auth can-i get managedclusters --as=cluster-admin-user` | All console sections accessible, hub name displayed consistently, user may lack direct ManagedCluster access but console functions work |
| 6 | Validate Error Handling - Test graceful failure scenarios for service account issues | Monitor console behavior during network interruptions or backend service issues | Test API error handling: `curl -X GET https://console-openshift-console.apps.CLUSTER-HOST/multicloud/hub -H "Authorization: Bearer invalid-token"` | Console handles errors gracefully, appropriate error messages displayed, no crashes or broken functionality |

### Test Case 2: Validate Hub Cluster Name Display for Namespace-Admin Users

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console - Access console with namespace-admin permissions | Navigate to https://console-openshift-console.apps.CLUSTER-HOST, authenticate with namespace-admin test user | Verify user permissions: `oc auth can-i get namespaces --as=namespace-admin-user` | Console authentication successful, limited permission user can access ACM interface |
| 2 | Check Hub Cluster Name Display - Verify hub name appears correctly for users with limited permissions | Observe hub cluster name in console header, navigation breadcrumbs, and cluster context indicators | Query hub name via API: `curl -s https://console-openshift-console.apps.CLUSTER-HOST/multicloud/hub -H "Authorization: Bearer $(oc whoami -t)" \| jq -r '.localHubName'` | Hub cluster name displays correctly throughout console interface, API returns consistent hub name value |
| 3 | Test Application Access - Validate application features work with namespace-scoped permissions | Navigate to Applications, verify applications visible within user's namespace scope | Check namespace access: `oc get applications -n user-namespace --as=namespace-admin-user` | Applications page loads, shows applications within user's permission scope, hub context maintained |
| 4 | Verify Permission Boundaries - Confirm console respects user permissions while maintaining hub name access | Attempt to access cluster-wide resources, verify appropriate permission messages | Test permission limits: `oc get managedclusters --as=namespace-admin-user` | Console shows appropriate "access denied" messages for restricted resources, but hub name functionality continues working |
| 5 | Validate Cross-Section Navigation - Test hub name consistency across different console areas | Navigate between Applications, Search, and available Governance sections | Verify consistent API responses: `for i in {1..3}; do curl -s https://console-openshift-console.apps.CLUSTER-HOST/multicloud/hub -H "Authorization: Bearer $(oc whoami -t)" \| jq -r '.localHubName'; done` | Hub name displayed consistently across all accessible console sections, API responses stable and consistent |

### Test Case 3: Test Multi-User Hub Name Access Scenarios

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console - Access console with different user permission levels | Test with kubeadmin (full admin), cluster-admin user, and application-manager user in separate browser sessions | Verify each user's authentication: `for user in kubeadmin cluster-admin app-manager; do oc whoami --as=$user; done` | All user types can access console successfully, authentication works for each permission level |
| 2 | Compare Hub Name Access Across Users - Verify consistent hub name access regardless of permission level | Compare hub name display across different user sessions in separate browser windows | Test API access for each user: `for user in kubeadmin cluster-admin app-manager; do oc login --username=$user; curl -s https://console-openshift-console.apps.CLUSTER-HOST/multicloud/hub -H "Authorization: Bearer $(oc whoami -t)" \| jq '.localHubName'; done` | All users receive identical hub name data, no permission-related failures for hub name access |
| 3 | Validate Application Topology Consistency - Test the primary ACM-20085 fix across user types | Access application topology with each user type, verify no console crashes occur | Verify application access for each user: `oc get applications.argoproj.io -A --as=$user` | Topology views load successfully for all users within their permission scope, no console failures |
| 4 | Test Permission Edge Cases - Validate graceful handling of permission transitions | Simulate user permission changes during active console sessions | Test ManagedCluster access variations: `oc auth can-i get managedclusters --as=kubeadmin; oc auth can-i get managedclusters --as=app-manager` | Console adapts gracefully to permission changes, hub name access remains consistent regardless of ManagedCluster permissions |
| 5 | Verify Service Account Security Model - Confirm user authentication still required for hub name access | Test console access without authentication, verify proper authentication requirements | Test API security: `curl -X GET https://console-openshift-console.apps.CLUSTER-HOST/multicloud/hub` (without auth header) | Unauthenticated requests properly rejected, authenticated users receive hub name data regardless of ManagedCluster permissions |