# E2E Test Plan: ACM-20640 RBAC UI Implementation

**Generated:** 2025-08-10 03:03  
**Environment:** qe6-vmware-ibm  
**Feature Status:** 🟡 Partially Deployed  

## Test Case 1: Navigation Structure Validation

**Description:** Verify the new User Management navigation structure replaces Access Control Management and provides correct routing.

**Setup:**
- Login to ACM console
- Ensure user has cluster-admin privileges
- Clear browser cache to avoid cached navigation

| Step | Expected Result |
|------|----------------|
| Open ACM console at `https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com` | Console loads successfully |
| Login with cluster credentials | Successfully authenticated |
| Navigate to main ACM navigation menu | Main navigation panel displays |
| Look for "User Management" section in navigation | "User Management" section is visible in navigation menu |
| Verify "Access Control Management" is no longer present | Old "Access Control Management" section is not displayed |
| Click on "User Management" → "Overview" | Navigates to `/multicloud/user-management/overview` |
| Verify URL structure | URL contains `/multicloud/user-management/overview` path |
| Check page content loads | Overview page displays without errors |

## Test Case 2: Users Identity Page Functionality

**Description:** Test the Users identity page including list functionality, filtering, and basic user information display.

**Setup:**
- Navigate to User Management section
- Ensure connection to clusters with user identities
- Have test users available in the cluster

| Step | Expected Result |
|------|----------------|
| Navigate to User Management → Identities → Users | Users identity page loads |
| Verify page URL | URL shows `/multicloud/user-management/identities/users` |
| Check users list displays | List of users from connected clusters appears |
| Verify user information columns | Displays: Name, Display Name, Status, Actions |
| Test name filter functionality | Type in filter box: `kubeadmin` |
| Verify filter results | Only users matching "kubeadmin" are displayed |
| Clear filter | All users display again |
| Click on a user entry | User details page opens |
| Verify user details structure | Shows user information, YAML view, Role assignments section |
| Check YAML tab functionality | Click YAML tab → User resource YAML displays as read-only |

## Test Case 3: Role Assignment List Operations

**Description:** Validate the role assignment list functionality and basic operations within the new UI structure.

**Setup:**
- Navigate to User Management section
- Ensure existing role assignments are present
- Have appropriate permissions for role assignment viewing

| Step | Expected Result |
|------|----------------|
| Navigate to User Management → Role Assignments | Role assignment list page loads |
| Verify URL structure | URL contains `/multicloud/user-management/role-assignments` |
| Check list displays existing role assignments | Table shows: Subject, Kind, Role, Scope, Status |
| Verify role assignment status display | Status indicators show properly (Active/Pending/Error) |
| Test list sorting functionality | Click column headers → List sorts by that column |
| Filter by subject type | Select "User" filter → Only user role assignments display |
| Filter by role type | Select "view" role → Only view role assignments display |
| Clear all filters | All role assignments display again |
| Click on role assignment entry | Role assignment details page opens |

## Test Case 4: RoleAssignment CRD Interface Validation

**Description:** Test the new RoleAssignment Custom Resource Definition interface and data structure handling.

**Setup:**
- Have cluster-admin access
- Access to oc CLI for verification
- Understanding of RoleAssignment CRD structure

| Step | Expected Result |
|------|----------------|
| Access role assignment creation interface | Creation form/wizard opens |
| Verify form structure matches CRD spec | Form fields: role, subjects, kind, scope |
| Check role selection dropdown | Available roles populate (view, edit, admin) |
| Verify subject kind options | Options include: User, Group, ServiceAccount |
| Test scope selector interface | Shows cluster and namespace selection options |
| Validate cluster scope selection | Can select multiple clusters from available list |
| Verify namespace scope per cluster | For each cluster, can select specific namespaces |
| Check CRD generation preview | YAML preview shows correct RoleAssignment structure |
| Verify API version in preview | Shows `rbac.open-cluster-management.io/v1alpha1` |

## Test Case 5: User Management Overview Integration

**Description:** Validate the overview page functionality and integration with other User Management components.

**Setup:**
- Navigate to User Management Overview
- Ensure multiple clusters are connected
- Have various identity types available

| Step | Expected Result |
|------|----------------|
| Navigate to User Management → Overview | Overview page loads successfully |
| Check overview dashboard elements | Displays summary cards for Users, Groups, ServiceAccounts |
| Verify user count accuracy | User count matches actual users in connected clusters |
| Check role assignment summary | Shows total active role assignments |
| Verify cluster scope overview | Displays clusters with RBAC configurations |
| Test "Create Role Assignment" button | Button navigates to role assignment creation |
| Check recent activity section | Shows recent role assignment changes (if available) |
| Verify link to documentation | Documentation link opens relevant RBAC help |
| Test navigation to sub-sections | Links to Users, Groups, ServiceAccounts work |

## Environment Setup Commands

```bash
# Login to cluster
oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 -u username -p password --insecure-skip-tls-verify

# Verify ACM installation
oc get namespace ocm multicluster-engine

# Check ACM console route
oc get routes -n ocm

# Verify current user permissions
oc auth can-i '*' '*' --all-namespaces
```

## Post-Test Validation

After completing the test cases, verify:

1. **Navigation Consistency**: All User Management navigation works correctly
2. **Data Integrity**: User and role assignment data displays accurately
3. **Performance**: Pages load within acceptable timeframes
4. **Error Handling**: Graceful handling of missing data or permissions
5. **Browser Compatibility**: Functionality works across supported browsers

## Notes for Future Testing

**When Groups and ServiceAccounts pages are implemented:**
- Add comprehensive test cases for Groups identity management
- Include ServiceAccounts page validation
- Test cross-identity role assignment workflows

**When role assignment wizard is complete:**
- Add end-to-end role assignment creation tests
- Include complex multi-cluster scenario testing
- Validate role assignment modification and deletion