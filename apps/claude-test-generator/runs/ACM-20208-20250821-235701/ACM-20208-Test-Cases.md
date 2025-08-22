# Test Cases for ACM-20208: Support hub name access for RBAC users

## Description
Validate that ACM Console can access and display the hub cluster name correctly for users with restricted RBAC permissions, ensuring proper functionality without requiring full ManagedCluster resource access.

## Setup
- Access to ACM Hub cluster with Console enabled
- Test users with varying RBAC permission levels configured
- ManagedCluster resources present representing the hub cluster
- Backend API endpoint `/multicloud/hub` accessible for hub name retrieval

## Test Cases

### Test Case 1: Hub Name Access for View-Only Users

**Description**: Verify that users with view-only permissions can access hub cluster name information through the Console without full ManagedCluster resource access.

**Step 1: Log into ACM Console** - Access ACM Console for RBAC hub name testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in with view-only user credentials via the Console login page
- **CLI Method**: Authenticate using oc login: `oc login https://api.<cluster-host>:6443 -u view-user -p <password>`
- **Expected Results**: Successful authentication with view-only user permissions established

**Step 2: Navigate to Clusters Overview** - Access the main Clusters page to verify hub name display functionality
- **UI Method**: Click "Infrastructure" → "Clusters" in the left navigation menu
- **CLI Method**: Verify cluster access permissions: `oc auth can-i get managedclusters`
- **Expected Results**: Clusters page loads successfully, hub cluster name displays correctly in the cluster list table

**Step 3: Verify Hub Name API Access** - Validate backend API endpoint returns hub name information for RBAC users
- **UI Method**: Use browser Developer Tools to inspect Network tab for `/multicloud/hub` API calls
- **CLI Method**: Test API endpoint directly: `curl -H "Authorization: Bearer $(oc whoami -t)" https://console-openshift-console.apps.<cluster-host>/multicloud/hub`
- **Expected Results**: API returns JSON response with `localHubName` field populated with correct hub cluster name, status code 200

**Step 4: Validate Hub Name in Search Results** - Confirm hub name appears correctly in Advanced Search functionality
- **UI Method**: Navigate to "Search" page, enter search query `kind:Pod namespace:open-cluster-management-hub`
- **CLI Method**: Search for hub-related resources: `oc get pods -n open-cluster-management-hub --show-labels | grep hub`
- **Expected Results**: Search results display hub cluster name consistently with clusters page, hub-related resources visible

**Step 5: Verify Console Navigation Context** - Ensure hub name context is maintained across different Console sections
- **UI Method**: Navigate between Overview, Applications, and Governance pages, verify hub cluster identification
- **CLI Method**: Check managedcluster resource for hub: `oc get managedcluster local-cluster -o yaml | grep name:`
- **Expected Results**: Hub cluster name remains consistent across all Console sections, no permission errors displayed

### Test Case 2: Hub Name Consistency Across User Roles

**Description**: Validate that different RBAC user roles (admin, edit, view) all receive consistent hub cluster name information through the Console interface.

**Step 1: Log into ACM Console** - Access ACM Console for multi-role hub name testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in sequentially with admin, edit, and view user credentials
- **CLI Method**: Test authentication for each role: `oc login https://api.<cluster-host>:6443 -u <role-user> -p <password>`
- **Expected Results**: All user roles authenticate successfully with appropriate permission levels

**Step 2: Collect Hub Name Data** - Gather hub name information from each user role perspective
- **UI Method**: For each user, navigate to Clusters page and record displayed hub name
- **CLI Method**: Query hub API for each role: `curl -H "Authorization: Bearer $(oc whoami -t)" https://console-openshift-console.apps.<cluster-host>/multicloud/hub | jq .localHubName`
- **Expected Results**: All roles return identical hub cluster name value, no permission-based variations

**Step 3: Verify API Response Consistency** - Ensure backend API provides same hub name data regardless of user permissions
- **UI Method**: Use browser tools to compare API responses between different user sessions
- **CLI Method**: Compare API responses: Create YAML file `hub-test.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hub-name-test
  namespace: default
data:
  admin-hub-name: "extracted-from-api"
  edit-hub-name: "extracted-from-api"
  view-hub-name: "extracted-from-api"
```
- **Expected Results**: All user roles receive identical JSON structure and hub name value from `/multicloud/hub` endpoint

**Step 4: Test Hub Name in Error Scenarios** - Validate hub name access during permission denied situations
- **UI Method**: With view-only user, attempt actions requiring higher permissions, observe hub name display
- **CLI Method**: Test restricted operations: `oc create managedcluster test-cluster --dry-run=client -o yaml`
- **Expected Results**: Even during permission errors, hub cluster name remains accessible and consistent

### Test Case 3: Hub Name Service Account Validation

**Description**: Verify that the backend service account mechanism correctly retrieves hub cluster name information independent of user token permissions.

**Step 1: Log into ACM Console** - Access ACM Console for service account hub name testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in with minimal permission user account (no ManagedCluster access)
- **CLI Method**: Authenticate with restricted user: `oc login https://api.<cluster-host>:6443 -u restricted-user -p <password>`
- **Expected Results**: User authentication successful but with minimal cluster permissions

**Step 2: Verify ManagedCluster Access Restriction** - Confirm user cannot directly access ManagedCluster resources
- **UI Method**: Attempt to navigate to individual cluster details page, observe permission restrictions
- **CLI Method**: Test direct ManagedCluster access: `oc get managedclusters`
- **Expected Results**: Direct ManagedCluster access denied with permission error, user lacks required RBAC

**Step 3: Validate Backend Service Account Access** - Ensure backend service retrieves hub name using elevated permissions
- **UI Method**: Verify Clusters page still displays hub cluster name despite user restrictions
- **CLI Method**: Check Console backend service account: `oc get serviceaccount -n open-cluster-management-hub | grep console`
- **Expected Results**: Console displays hub cluster name correctly, backend service account has necessary permissions

**Step 4: Test Hub Name API Functionality** - Confirm API endpoint works through service account token mechanism
- **UI Method**: Use Network tools to verify `/multicloud/hub` API call succeeds despite user restrictions
- **CLI Method**: Verify service account permissions: Create test YAML `service-account-test.yaml`:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: test-hub-access
subjects:
- kind: User
  name: restricted-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```
- **Expected Results**: API returns hub name successfully using backend service account, not user token