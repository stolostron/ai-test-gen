# ACM-20640 RBAC UI Implementation - E2E Test Cases

**Test Plan Version**: V4.0  
**Feature**: RBAC UI Implementation [ACM 2.15]  
**Test Environment**: Environment-agnostic (designed for ACM 2.15.0+)  
**Generated**: 2025-08-18 16:20:45  

---

## Test Case 1: Verify User Identity Management Interface

**Description**: Validate complete user identity management workflow through ACM Console including user creation, viewing, editing, and deletion with proper RBAC enforcement.

**Setup**: 
- Access to ACM Console with user management permissions
- Multiple test user accounts available for testing
- ClusterAdmin privileges for user management operations

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | **Log into ACM Console** - Access ACM Console for user identity management testing | Navigate to https://multicloud-console.apps.<cluster-host> | `oc login https://api.<cluster-host>:6443 -u <username> -p <password>` | ACM Console dashboard loads successfully with user management menu visible |
| 2 | **Navigate to User Management** - Access the user identity management interface | Click "User Management" → "Identities" → "Users" from main navigation | `oc get users --all-namespaces` | User management page loads showing existing users in table format with create/edit options |
| 3 | **Create New User Identity** - Create a new user for RBAC testing | Click "Create User" → Fill user details form (name, email, groups) → Click "Create" | Create user YAML file: `touch test-user.yaml` and add:<br>```yaml<br>apiVersion: user.openshift.io/v1<br>kind: User<br>metadata:<br>  name: rbac-test-user<br>  labels:<br>    rbac.acm.io/test-user: "true"<br>identities:<br>- htpasswd:rbac-test-user<br>```<br>`oc apply -f test-user.yaml` | New user appears in users list with "Active" status and proper metadata |
| 4 | **View User Details** - Access detailed user information and current role assignments | Click on created user name → Review user details page | `oc describe user rbac-test-user` | User details page displays with personal info, current role assignments, and group memberships |
| 5 | **Edit User Profile** - Modify user information and group assignments | Click "Edit User" → Update user groups and labels → Save changes | Edit existing user YAML:<br>```yaml<br>apiVersion: user.openshift.io/v1<br>kind: User<br>metadata:<br>  name: rbac-test-user<br>  labels:<br>    rbac.acm.io/test-user: "true"<br>    rbac.acm.io/department: "qa"<br>identities:<br>- htpasswd:rbac-test-user<br>groups:<br>- qa-team<br>```<br>`oc apply -f test-user.yaml` | User profile updates successfully with new group assignments reflected immediately |
| 6 | **Verify User Permissions** - Validate that user has appropriate access levels | Navigate to user's "Permissions" tab → Review assigned roles and cluster access | `oc auth can-i --list --as=rbac-test-user` | Permissions tab shows accurate role assignments with proper cluster and namespace scope |
| 7 | **Test User Search and Filter** - Verify user discovery and filtering capabilities | Use search bar to find specific users → Apply group filters → Sort by various columns | `oc get users --selector="rbac.acm.io/department=qa"` | Search returns accurate results with proper filtering and sorting functionality |
| 8 | **Delete User Identity** - Remove test user and verify cleanup | Click user actions menu → "Delete User" → Confirm deletion | `oc delete user rbac-test-user` | User removed from system with confirmation message and proper audit trail |

---

## Test Case 2: Validate Role Assignment Wizard and Workflows

**Description**: Test comprehensive role assignment creation and management workflows including role selection, cluster targeting, and permission validation with cross-cluster scenarios.

**Setup**:
- Access to ACM Console with role assignment permissions  
- Multiple managed clusters connected to hub
- Various user accounts and groups available for assignment
- ClusterAdmin privileges for role management operations

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | **Log into ACM Console** - Access ACM Console for role assignment testing | Navigate to https://multicloud-console.apps.<cluster-host> | `oc login https://api.<cluster-host>:6443 -u <username> -p <password>` | ACM Console loads with role assignment features accessible |
| 2 | **Access Role Assignment Interface** - Navigate to role assignment management | User Management → Identities → Users → Select user → "Role Assignments" tab | `oc get roleassignments -A` | Role assignment interface loads showing current assignments in organized table |
| 3 | **Launch Assignment Wizard** - Start new role assignment creation process | Click "Create RoleAssignment" → Role Assignment Wizard opens | Create RoleAssignment YAML: `touch roleassignment-vm-admin.yaml` and add:<br>```yaml<br>apiVersion: rbac.open-cluster-management.io/v1alpha1<br>kind: RoleAssignment<br>metadata:<br>  name: vm-admin-assignment<br>  namespace: target-cluster<br>spec:<br>  role: kubevirt.io:admin<br>  subjects:<br>  - kind: User<br>    name: rbac-test-user<br>    clusters:<br>    - name: target-cluster<br>      clusterWide: false<br>      namespaces: ["default", "vm-workloads"]<br>```<br>`oc apply -f roleassignment-vm-admin.yaml` | Role Assignment Wizard displays with clear step-by-step process and validation |
| 4 | **Select Target Role** - Choose appropriate role for assignment | Select role type → Choose "kubevirt.io:admin" from dropdown → Review role permissions | `oc get clusterroles | grep kubevirt` | Role selection shows available VM roles with clear permission descriptions |
| 5 | **Configure Subject Assignment** - Assign role to users or groups | Select "User" as subject type → Enter username → Add additional users/groups if needed | Verify user exists: `oc get user rbac-test-user` | Subject configuration allows multiple users/groups with validation |
| 6 | **Define Cluster Scope** - Specify which clusters and namespaces receive the assignment | Select target clusters → Choose "Namespace-scoped" → Select specific namespaces: default, vm-workloads | `oc get managedclusters` | Cluster scope selection shows available clusters with namespace options |
| 7 | **Review and Create** - Validate assignment configuration before creation | Review assignment summary → Verify all settings → Click "Create Assignment" | `oc apply -f roleassignment-vm-admin.yaml` | Assignment created successfully with confirmation and immediate effect |
| 8 | **Verify Assignment Effectiveness** - Test that role assignment works as intended | Navigate to Virtual Machines → Verify user can access VM management features | `oc auth can-i create virtualmachines --as=rbac-test-user -n vm-workloads` | User successfully accesses VM features with assigned permissions |
| 9 | **Edit Existing Assignment** - Modify role assignment scope and permissions | Click assignment actions → "Edit" → Modify namespace scope → Save changes | Edit RoleAssignment YAML to add namespace:<br>```yaml<br>      namespaces: ["default", "vm-workloads", "production"]<br>```<br>`oc apply -f roleassignment-vm-admin.yaml` | Assignment updates successfully with expanded namespace access |
| 10 | **Remove Role Assignment** - Clean up test assignment | Click assignment actions → "Delete" → Confirm removal | `oc delete roleassignment vm-admin-assignment -n target-cluster` | Assignment removed with immediate permission revocation |

---

## Test Case 3: Test Virtual Machine Access Control Integration

**Description**: Validate VM-specific RBAC functionality through ACM Console including role assignments for VM lifecycle operations, console access, and cross-cluster VM management.

**Setup**:
- ACM Console access with VM management permissions
- OpenShift Virtualization (CNV) installed and configured  
- Multiple managed clusters with VM capabilities
- Test virtual machines deployed across clusters
- Various user roles configured for VM operations

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | **Log into ACM Console** - Access ACM Console for VM RBAC testing | Navigate to https://multicloud-console.apps.<cluster-host> | `oc login https://api.<cluster-host>:6443 -u <username> -p <password>` | ACM Console loads with Infrastructure and VM sections accessible |
| 2 | **Navigate to Virtual Machines** - Access VM management interface with RBAC integration | Infrastructure → Virtual Machines → Select cluster | `oc get virtualmachines -A` | VM management page loads showing VMs with role-based visibility |
| 3 | **Access VM Role Assignments** - View RBAC-specific tab for virtual machines | Click "Role Assignments" tab in VM interface | `oc get roleassignments -l component=vm-access` | Role assignments tab displays VM-specific RBAC configurations |
| 4 | **Create VM-Scoped Role Assignment** - Assign VM management roles to users | Click "Create VM Role Assignment" → Select VM admin role → Target specific VMs | Create VM RoleAssignment: `touch vm-rbac-assignment.yaml` and add:<br>```yaml<br>apiVersion: rbac.open-cluster-management.io/v1alpha1<br>kind: RoleAssignment<br>metadata:<br>  name: vm-lifecycle-admin<br>  namespace: vm-workloads<br>spec:<br>  role: kubevirt.io:admin<br>  subjects:<br>  - kind: User<br>    name: vm-admin-user<br>    clusters:<br>    - name: production-cluster<br>      clusterWide: false<br>      namespaces: ["vm-workloads"]<br>      resources:<br>      - virtualmachines<br>      - virtualmachineinstances<br>```<br>`oc apply -f vm-rbac-assignment.yaml` | VM role assignment created with granular VM operation permissions |
| 5 | **Test VM Lifecycle Permissions** - Verify user can perform VM operations based on assigned role | Login as assigned user → Create new VM → Start/Stop/Restart operations | `oc auth can-i create virtualmachines --as=vm-admin-user -n vm-workloads` | User successfully performs VM lifecycle operations within assigned scope |
| 6 | **Validate VM Console Access** - Test VM console access based on RBAC assignments | Select VM → Click "Console" → Verify access granted/denied based on role | `oc auth can-i get virtualmachineinstances/console --as=vm-admin-user -n vm-workloads` | VM console access properly enforced based on role assignments |
| 7 | **Test Cross-Cluster VM Visibility** - Verify user sees only VMs they have permission to access | Switch between managed clusters → Verify VM list filtering | `oc get virtualmachines --as=vm-admin-user --all-namespaces` | VM visibility correctly filtered by user's cluster and namespace permissions |
| 8 | **Verify VM Resource Quotas** - Test RBAC enforcement for VM resource limitations | Attempt to create VM exceeding assigned resource limits → Verify denial | `oc auth can-i create resourcequotas --as=vm-admin-user -n vm-workloads` | Resource quota enforcement works properly with meaningful error messages |
| 9 | **Test VM Migration Permissions** - Validate VM migration access control | Select VM → Attempt migration → Verify permission enforcement | `oc auth can-i patch virtualmachineinstances --as=vm-admin-user -n vm-workloads` | VM migration permissions properly enforced based on role assignments |
| 10 | **Cleanup VM RBAC Configuration** - Remove test role assignments and verify access revocation | Delete VM role assignments → Verify user loses VM access | `oc delete roleassignment vm-lifecycle-admin -n vm-workloads` | VM access properly revoked with immediate effect |

---

## Test Case 4: Validate Cross-Cluster RBAC Operations

**Description**: Test RBAC functionality across multiple managed clusters including hub-to-spoke role propagation, cluster-specific permissions, and cross-cluster user management workflows.

**Setup**:
- Hub cluster with multiple managed clusters connected
- Cross-cluster user authentication configured
- Hub admin privileges for cross-cluster role management  
- Test user accounts configured across clusters
- Various cluster-specific resources available for testing

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | **Log into ACM Console** - Access hub cluster console for cross-cluster RBAC testing | Navigate to https://multicloud-console.apps.<cluster-host> | `oc login https://api.<cluster-host>:6443 -u <username> -p <password>` | Hub console loads with managed cluster overview accessible |
| 2 | **View Managed Clusters** - Review available clusters for RBAC configuration | Infrastructure → Clusters → Review managed cluster list | `oc get managedclusters` | Managed clusters displayed with connection status and RBAC readiness indicators |
| 3 | **Create Cross-Cluster Role Assignment** - Assign roles that span multiple clusters | User Management → Create RoleAssignment → Select multiple target clusters | Create cross-cluster RoleAssignment: `touch cross-cluster-rbac.yaml` and add:<br>```yaml<br>apiVersion: rbac.open-cluster-management.io/v1alpha1<br>kind: RoleAssignment<br>metadata:<br>  name: multi-cluster-operator<br>  namespace: open-cluster-management<br>spec:<br>  role: cluster-manager-admin<br>  subjects:<br>  - kind: User<br>    name: cross-cluster-admin<br>    clusters:<br>    - name: production-east<br>      clusterWide: true<br>    - name: production-west<br>      clusterWide: true<br>    - name: staging-cluster<br>      clusterWide: false<br>      namespaces: ["default", "testing"]<br>```<br>`oc apply -f cross-cluster-rbac.yaml` | Cross-cluster role assignment created with proper cluster targeting |
| 4 | **Verify Role Propagation** - Confirm roles are properly distributed to target clusters | Check each managed cluster → Verify role assignments exist | `oc get rolebindings,clusterrolebindings --as=cross-cluster-admin -A` | Role assignments successfully propagated to all specified clusters |
| 5 | **Test Hub-to-Spoke Access** - Validate user can access resources on managed clusters from hub | Login as assigned user → Access managed cluster resources through hub console | `oc auth can-i get nodes --as=cross-cluster-admin --context=production-east` | User successfully accesses managed cluster resources through hub interface |
| 6 | **Validate Cluster-Specific Restrictions** - Test that permissions are properly scoped per cluster | Attempt to access resources outside assigned cluster scope → Verify denial | `oc auth can-i delete pods --as=cross-cluster-admin -n kube-system` | Access properly restricted to assigned clusters and namespaces |
| 7 | **Test User Search Across Clusters** - Verify cross-cluster user discovery functionality | User Management → Search for users → Filter by cluster | `oc get users --context=production-east` | User search returns results from appropriate clusters with proper filtering |
| 8 | **Verify Cross-Cluster Resource Visibility** - Test resource access across multiple clusters | Navigate to Applications → Verify app visibility across assigned clusters | `oc get applications.argoproj.io --as=cross-cluster-admin --context=production-west` | Resource visibility properly filtered by user's cross-cluster permissions |
| 9 | **Test Cluster Set Permissions** - Validate ManagedClusterSet-based access control | Cluster Sets → Verify user can only access assigned cluster sets | `oc get managedclustersets --as=cross-cluster-admin` | Cluster set access properly enforced based on role assignments |
| 10 | **Cleanup Cross-Cluster Configuration** - Remove cross-cluster role assignments | Delete cross-cluster role assignments → Verify access revocation across all clusters | `oc delete roleassignment multi-cluster-operator -n open-cluster-management` | Cross-cluster access properly revoked from all target clusters |

---

## Test Case 5: Verify RBAC Error Handling and User Experience

**Description**: Validate proper error handling, user feedback, and edge case scenarios in RBAC UI including invalid configurations, permission conflicts, and graceful degradation.

**Setup**:
- ACM Console access with limited permissions for testing error scenarios
- Various user accounts with different permission levels
- Test scenarios configured for permission conflicts
- Access to view system logs and error responses

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | **Log into ACM Console** - Access ACM Console for RBAC error handling testing | Navigate to https://multicloud-console.apps.<cluster-host> | `oc login https://api.<cluster-host>:6443 -u <username> -p <password>` | Console loads with appropriate error handling framework active |
| 2 | **Test Invalid Role Assignment** - Attempt to create role assignment with invalid configuration | Create RoleAssignment → Enter invalid role name → Attempt submission | Create invalid RoleAssignment: `touch invalid-rbac.yaml` and add:<br>```yaml<br>apiVersion: rbac.open-cluster-management.io/v1alpha1<br>kind: RoleAssignment<br>metadata:<br>  name: invalid-assignment<br>spec:<br>  role: non-existent-role<br>  subjects:<br>  - kind: User<br>    name: test-user<br>```<br>`oc apply -f invalid-rbac.yaml` | Clear error message displayed with specific validation failure details |
| 3 | **Verify Permission Conflict Handling** - Test scenarios where role assignments conflict | Create conflicting role assignments for same user/cluster → Review conflict resolution | Apply conflicting assignment:<br>```yaml<br>spec:<br>  role: kubevirt.io:admin<br>  subjects:<br>  - kind: User<br>    name: test-user<br>    clusters:<br>    - name: production<br>      clusterWide: true<br>---<br>spec:<br>  role: kubevirt.io:view<br>  subjects:<br>  - kind: User<br>    name: test-user<br>    clusters:<br>    - name: production<br>      clusterWide: true<br>```<br>`oc apply -f conflicting-rbac.yaml` | System properly handles conflicts with appropriate precedence and user notification |
| 4 | **Test Insufficient Permission Scenarios** - Verify graceful handling when user lacks required permissions | Login as limited user → Attempt role assignment creation → Review error handling | `oc auth can-i create roleassignments --as=limited-user` | Clear permission denial messages with guidance for required permissions |
| 5 | **Validate YAML Editor Error Handling** - Test error handling in YAML configuration mode | Switch to YAML editor → Enter malformed YAML → Attempt save | Create malformed YAML:<br>```yaml<br>apiVersion: rbac.open-cluster-management.io/v1alpha1<br>kind: RoleAssignment<br>metadata:<br>  name: test<br>spec:<br>  invalid-field: value<br>  missing-required-fields: true<br>```<br>`oc apply -f malformed-rbac.yaml` | YAML validation errors clearly displayed with line numbers and correction suggestions |
| 6 | **Test Network Connectivity Issues** - Verify handling when managed clusters are unreachable | Simulate network issues → Attempt cross-cluster role operations → Review error messages | `oc get managedclusters --show-labels` | Network errors properly communicated with retry options and cluster status indicators |
| 7 | **Verify Form Validation** - Test comprehensive form field validation and user guidance | Fill role assignment form with invalid data → Test each field validation | Attempt CLI with missing required fields:<br>```bash<br>oc create roleassignment --dry-run=client<br>```<br>Review required field validation | Form validation provides immediate feedback with clear correction guidance |
| 8 | **Test Bulk Operation Error Handling** - Verify error handling during multiple role assignments | Perform bulk role assignment operations with mixed valid/invalid entries | Apply multiple assignments including failures:<br>```bash<br>oc apply -f valid-rbac.yaml,invalid-rbac.yaml<br>```<br>Review batch operation results | Bulk operations report individual successes/failures with detailed error breakdown |
| 9 | **Validate User Feedback and Help** - Test help system and user guidance features | Access help documentation → Review tooltips and guidance → Test support links | `oc explain roleassignment.spec` | Comprehensive help system provides actionable guidance for RBAC configuration |
| 10 | **Verify Audit Trail and Logging** - Test that RBAC operations are properly logged and auditable | Perform various RBAC operations → Review audit logs → Verify compliance tracking | `oc get events --field-selector type=Warning,reason=FailedCreate` | All RBAC operations properly logged with audit trail for compliance requirements |

---

**Test Plan Complete**: 5 comprehensive E2E test cases covering all RBAC UI Implementation features with dual UI+CLI approaches and realistic environment integration.