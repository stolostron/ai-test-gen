# ACM-20640 RBAC UI Implementation [2.15] - Comprehensive Test Plan

**Generated:** 2025-01-14 16:36:24  
**Environment:** Flexible (QE6 or alternative environment)  
**Test Framework:** CLC UI Cypress E2E Testing  
**Coverage:** All RBAC UI Updates for CLC Team in 2.15

---

## Test Case 1: User Management Navigation and Route Validation

**Description:** Validate the new User Management navigation structure and verify all RBAC UI routes are properly configured and accessible.

**Setup:** 
- ACM hub cluster with 2.15+ deployment
- Admin user with cluster-admin privileges
- Test user accounts for RBAC validation

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to ACM hub cluster. Terminal output shows: `Login successful.` and `Using project "default"` |
| **Step 2: Navigate to User Management section** - Open ACM console and access the main navigation menu to locate User Management | User Management section is visible in the navigation menu, replacing the previous Access Control location. Menu structure shows organized RBAC options |
| **Step 3: Verify Identities navigation** - Click on User Management and verify Identities subsection with Users, Groups, and ServiceAccounts | Identities section displays with three tabs: Users (default), Groups, and ServiceAccounts. URL shows `/multicloud/user-management/identities/users/` |
| **Step 4: Test Users route accessibility** - Navigate to Users tab and verify page loads correctly | Users listing page loads successfully showing user table with columns: Name, Display Name, Groups, Status. Empty state or populated list appears based on cluster configuration |
| **Step 5: Verify user detail routes** - Click on a user entry to access individual user details | User detail page loads with tabs: Details, YAML, Role Assignments, Groups. URL pattern shows `/multicloud/user-management/identities/users/{userid}` |
| **Step 6: Test Groups tab navigation** - Navigate to Groups tab in Identities section | Groups listing page loads successfully. URL shows `/multicloud/user-management/identities/groups/`. Page structure matches Users page layout |
| **Step 7: Test ServiceAccounts tab navigation** - Navigate to ServiceAccounts tab in Identities section | ServiceAccounts listing page loads successfully. URL shows `/multicloud/user-management/identities/service-accounts/`. Consistent UI pattern with other identity types |
| **Step 8: Verify Roles section accessibility** - Navigate to Roles section under User Management | Roles listing page loads showing available cluster roles and custom roles. URL shows `/multicloud/user-management/roles/` with proper role listing interface |

---

## Test Case 2: User Identity Management Functionality

**Description:** Test the complete User Identity Management interface including user listing, details view, YAML editing, and group associations.

**Setup:**
- ACM hub cluster with RBAC UI deployed
- Multiple test users created in the system
- Various group associations configured

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication with admin privileges. Console access verified for User Management operations |
| **Step 2: Access Users listing page** - Navigate to User Management > Identities > Users | Users table displays with proper columns: Name, Display Name, Groups, Status. Data shows current system users with accurate information |
| **Step 3: Test user search and filtering** - Use search functionality to filter users by name or display name | Search functionality works correctly, filtering results in real-time. Results update dynamically as search terms are entered |
| **Step 4: Verify user detail view** - Click on a specific user to open detail page | User detail page loads showing: user information, associated groups, current status. Navigation tabs (Details, YAML, Role Assignments, Groups) are functional |
| **Step 5: Test YAML view functionality** - Navigate to YAML tab for selected user | YAML editor displays the user resource definition in read-only format. YAML content shows: ```yaml apiVersion: user.openshift.io/v1 kind: User metadata: name: {username} ``` |
| **Step 6: Verify Groups tab on user detail** - Navigate to Groups tab on user detail page | Groups tab shows all groups associated with the user. Each group entry displays group name and association details |
| **Step 7: Test Role Assignments tab** - Navigate to Role Assignments tab on user detail page | Role Assignments tab displays current role assignments for the user. Shows assigned roles, namespaces, and cluster-wide permissions with clear categorization |
| **Step 8: Verify user status display** - Check UserStatus component functionality across user listings | User status component displays correct status indicators: Active, Inactive, or other relevant states with appropriate visual styling |

---

## Test Case 3: Role Assignment Creation Workflow

**Description:** Test the role assignment creation process using the new modal interface and validate the complete workflow from user selection to role assignment.

**Setup:**
- ACM cluster with RBAC UI components deployed
- Test users and roles available for assignment
- Multiple clusters and namespaces configured

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Authentication successful with RBAC management permissions enabled. Access to User Management section confirmed |
| **Step 2: Navigate to Role Assignments** - Access User Management > Role Assignments list | Role Assignments listing page displays existing assignments with columns: Subject, Subject Type, Role, Scope, Clusters/Namespaces. Create assignment button is visible and accessible |
| **Step 3: Initiate role assignment creation** - Click "Create role assignment" button to open creation modal | CreateRoleAssignmentModal opens successfully showing form fields: Subject Type selection (Users/Groups/ServiceAccounts), Subject selection, Role selection, Scope configuration |
| **Step 4: Select subject type and subject** - Choose subject type and select specific user/group/service account | Subject selection dropdown populates correctly based on type selection. Chosen subject displays with proper identification and details |
| **Step 5: Configure role selection** - Select appropriate role from available cluster roles | Role dropdown shows available cluster roles including: cluster-admin, admin, edit, view, and custom roles. Selected role displays with description and permissions summary |
| **Step 6: Set assignment scope** - Configure cluster and namespace scope for the assignment | Scope configuration allows selection of: All clusters, Specific clusters, or Namespace-specific assignments. Cluster/namespace selection interface provides proper filtering and search capabilities |
| **Step 7: Validate assignment configuration** - Review all assignment details before creation | Assignment summary displays: Subject details, Role information, Scope configuration, Affected clusters/namespaces. Validation shows no conflicts or errors |
| **Step 8: Create and verify assignment** - Submit role assignment and verify successful creation | Assignment created successfully. New role assignment appears in list with correct details. User/subject gains specified permissions on target clusters/namespaces |

---

## Test Case 4: Role and Permissions Management

**Description:** Validate the Roles management interface including role listing, permissions view, and role assignment tracking functionality.

**Setup:**
- ACM hub cluster with role management UI deployed
- Various cluster roles and custom roles configured
- Existing role assignments for testing

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful cluster access with permissions to view and manage roles. RBAC UI components accessible |
| **Step 2: Access Roles listing page** - Navigate to User Management > Roles | Roles listing displays with columns: Role Name, Type (ClusterRole/Role), Permissions Count, Assignments. Both system and custom roles are visible |
| **Step 3: Test role filtering and search** - Use search functionality to filter roles by name or type | Role search works correctly filtering by role name. Results update dynamically and show relevant matches with highlighting |
| **Step 4: Verify role detail view** - Click on a specific role to open detail page | Role detail page displays with tabs: Overview, Permissions, Role Assignments. Role information shows creation date, description, and usage statistics |
| **Step 5: Test Permissions tab functionality** - Navigate to Permissions tab for selected role | Permissions list displays with columns: Resource, API Group, Verbs (actions). Each permission entry shows: ```yaml resources: ["pods"] apiGroups: [""] verbs: ["get", "list", "create"] ``` |
| **Step 6: Filter permissions by resource type** - Use permissions filter to search for specific resource types | Permission filtering works correctly showing only matching resources. Filter supports resource names, API groups, and action verbs |
| **Step 7: Verify Role Assignments tab** - Navigate to Role Assignments tab on role detail page | Role Assignments tab shows all current assignments using this role. Displays: Subject name, Subject type, Scope (cluster/namespace), Target clusters |
| **Step 8: Test role assignment navigation** - Click on role assignment entries to navigate to subject details | Links from role assignments navigate correctly to user/group/service account detail pages. Bidirectional navigation works between roles and subjects |

---

## Test Case 5: Groups and ServiceAccounts Management

**Description:** Test the Groups and ServiceAccounts identity management interfaces including listing, details, and role assignment capabilities.

**Setup:**
- ACM cluster with all identity types configured
- Test groups with user memberships
- ServiceAccounts in various namespaces

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Authentication successful with access to all identity management features. Groups and ServiceAccounts sections accessible |
| **Step 2: Access Groups management** - Navigate to User Management > Identities > Groups | Groups listing page displays with columns: Group Name, Members Count, Description, Role Assignments. Search and filtering capabilities available |
| **Step 3: Test group detail functionality** - Click on a group to open detail view | Group detail page shows tabs: Details, Members, Role Assignments, YAML. Group information displays member count and group description |
| **Step 4: Verify group members tab** - Navigate to Members tab on group detail page | Members tab displays all users belonging to the group. Each member shows: User name, Display name, Join date, Status with links to user detail pages |
| **Step 5: Test ServiceAccounts listing** - Navigate to User Management > Identities > ServiceAccounts | ServiceAccounts listing displays with columns: Name, Namespace, Created, Role Assignments. Namespace filtering and search functionality available |
| **Step 6: Verify ServiceAccount detail view** - Click on a ServiceAccount to open detail page | ServiceAccount detail page shows: Namespace information, Creation details, Associated secrets, Role assignments with proper YAML representation |
| **Step 7: Test ServiceAccount YAML functionality** - Navigate to YAML tab for ServiceAccount | YAML editor displays ServiceAccount resource: ```yaml apiVersion: v1 kind: ServiceAccount metadata: name: {sa-name} namespace: {namespace} ``` |
| **Step 8: Verify cross-identity role assignments** - Test role assignment creation for groups and service accounts | Role assignment modal supports all identity types. Groups and ServiceAccounts can be assigned roles with proper scope configuration and validation |

---

## Test Case 6: RBAC Integration with Existing CLC Workflows

**Description:** Test integration between new RBAC UI and existing CLC cluster management, automation, and credential workflows to ensure seamless operation.

**Setup:**
- ACM cluster with both new RBAC UI and existing CLC features
- Test users with varying permission levels
- Existing clusters, credentials, and automation configurations

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication with hybrid RBAC and CLC feature access. Both old and new interfaces accessible |
| **Step 2: Test user with limited RBAC permissions** - Create role assignment with view-only permissions for cluster management | User with view-only role assignment can access cluster listings but cannot create, edit, or delete clusters. Proper permission enforcement across CLC interfaces |
| **Step 3: Verify automation RBAC integration** - Test user permissions for automation templates and job execution | RBAC permissions correctly control access to ansible automation features. Users can view templates based on namespace permissions and execute based on assigned roles |
| **Step 4: Test credentials management RBAC** - Validate credential access based on role assignments | Credential access follows RBAC rules with namespace-scoped permissions. Users can view/edit credentials only in namespaces where they have appropriate role assignments |
| **Step 5: Verify ClusterSet RBAC integration** - Test ClusterSet access management with new role assignments | ClusterSet access controlled by role assignments. Users can manage ClusterSets based on cluster-admin or custom role permissions assigned through new RBAC UI |
| **Step 6: Test cross-feature permission inheritance** - Verify consistent permission enforcement across all CLC features | Permission inheritance works correctly between User Management RBAC settings and existing CLC features. No permission escalation or unexpected access grants |
| **Step 7: Validate backward compatibility** - Ensure existing role bindings continue working with new UI | Existing ClusterRoleBindings and RoleBindings function correctly with new RBAC UI. Legacy permissions visible and manageable through new interface |
| **Step 8: Test permission troubleshooting** - Use new RBAC UI to diagnose and fix permission issues | New RBAC UI provides clear visibility into user permissions across all CLC features. Permission conflicts and missing access easily identified and resolved |

---

## Test Case 7: Multi-cluster RBAC Assignment and Validation

**Description:** Test RBAC assignments across multiple managed clusters and validate permission propagation and enforcement in multi-cluster scenarios.

**Setup:**
- ACM hub cluster with multiple managed clusters
- Test users requiring multi-cluster access
- Various cluster sets and namespace configurations

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Hub cluster authentication successful with multi-cluster management permissions. Access to all connected managed clusters confirmed |
| **Step 2: Create multi-cluster role assignment** - Assign cluster-admin role to user across multiple managed clusters | Role assignment creation supports multi-cluster selection. User gains administrative access to selected clusters with proper scope configuration |
| **Step 3: Verify cluster-specific namespace permissions** - Assign namespace-admin role to user for specific namespaces across clusters | Namespace-scoped role assignment works across multiple clusters. User permissions limited to specified namespaces on target clusters only |
| **Step 4: Test cluster set RBAC integration** - Assign permissions based on cluster set membership | Role assignments can target entire cluster sets. Users gain permissions on all clusters within assigned cluster sets automatically |
| **Step 5: Validate permission propagation** - Verify role assignments propagate correctly to managed clusters | Permission propagation completes successfully. User can access assigned namespaces/clusters with expected permission levels within reasonable time |
| **Step 6: Test permission enforcement on managed clusters** - Login to managed cluster and verify assigned permissions work correctly | User permissions function correctly on managed clusters. Access to resources matches role assignment scope with proper enforcement |
| **Step 7: Verify role assignment visibility** - Check role assignment status across all clusters in assignment scope | Role assignment status displays correctly for each target cluster. Success/failure states clearly indicated with error details where applicable |
| **Step 8: Test multi-cluster permission removal** - Remove role assignments and verify permission revocation | Permission revocation works correctly across all assigned clusters. User loses access within expected timeframe with complete cleanup |