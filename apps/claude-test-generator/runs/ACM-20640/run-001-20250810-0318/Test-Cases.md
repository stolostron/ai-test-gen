# RBAC UI Implementation - E2E Test Cases

**Feature:** ACM-20640 RBAC UI Implementation  
**Environment:** OpenShift 4.19.6 with ACM  
**Test Focus:** ClusterPermissions API and UI components  

---

## Test Case 1: ClusterPermissions CRD Basic Operations

**Description:** Validate core ClusterPermissions CRD functionality for creating and managing RBAC resources across managed clusters.

**Setup:**
- Access to ACM hub cluster with admin privileges
- At least one managed cluster attached to ACM
- kubectl/oc CLI configured

| Step | Expected Result |
|------|----------------|
| `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Login successful |
| `oc get crd clusterpermissions.rbac.open-cluster-management.io` | CRD exists with API version rbac.open-cluster-management.io/v1alpha1 |
| Create ClusterPermission YAML:<br/>`cat <<EOF \| oc apply -f -`<br/>`apiVersion: rbac.open-cluster-management.io/v1alpha1`<br/>`kind: ClusterPermission`<br/>`metadata:`<br/>`  name: test-vm-viewer`<br/>`  namespace: default`<br/>`spec:`<br/>`  clusterRole:`<br/>`    rules:`<br/>`    - apiGroups: ["kubevirt.io"]`<br/>`      resources: ["virtualmachines"]`<br/>`      verbs: ["get", "list", "watch"]`<br/>`  clusterRoleBinding:`<br/>`    roleRef:`<br/>`      apiGroup: rbac.authorization.k8s.io`<br/>`      kind: ClusterRole`<br/>`      name: test-vm-viewer`<br/>`    subjects:`<br/>`    - kind: User`<br/>`      name: testuser`<br/>`      apiGroup: rbac.authorization.k8s.io`<br/>`EOF` | ClusterPermission created successfully |
| `oc get clusterpermissions test-vm-viewer -o yaml` | YAML shows created ClusterPermission with complete spec |
| `oc describe clusterpermissions test-vm-viewer` | Status shows conditions and managed cluster propagation |
| `oc delete clusterpermissions test-vm-viewer` | ClusterPermission deleted successfully |

---

## Test Case 2: Multi-Cluster Permission Propagation

**Description:** Test ClusterPermissions creation and propagation to managed clusters with role enforcement validation.

**Setup:**
- ACM hub cluster with multiple managed clusters
- Test user account available for permission testing

| Step | Expected Result |
|------|----------------|
| `oc get managedclusters` | List shows 2+ managed clusters in Ready status |
| Create namespace-scoped permission:<br/>`cat <<EOF \| oc apply -f -`<br/>`apiVersion: rbac.open-cluster-management.io/v1alpha1`<br/>`kind: ClusterPermission`<br/>`metadata:`<br/>`  name: namespace-vm-editor`<br/>`  namespace: default`<br/>`spec:`<br/>`  roles:`<br/>`  - namespace: kube-system`<br/>`    rules:`<br/>`    - apiGroups: ["kubevirt.io"]`<br/>`      resources: ["virtualmachines"]`<br/>`      verbs: ["get", "list", "create", "update", "patch"]`<br/>`  roleBindings:`<br/>`  - namespace: kube-system`<br/>`    roleRef:`<br/>`      kind: Role`<br/>`      name: namespace-vm-editor`<br/>`    subjects:`<br/>`    - kind: User`<br/>`      name: vmuser`<br/>`      apiGroup: rbac.authorization.k8s.io`<br/>`EOF` | ClusterPermission created with namespace-scoped roles |
| `oc get clusterpermissions namespace-vm-editor -o jsonpath='{.status.conditions}'` | Status conditions show Applied=True, Available=True |
| Switch to managed cluster context:<br/>`oc config use-context managed-cluster-1` | Context switched to managed cluster |
| `oc get role namespace-vm-editor -n kube-system` | Role exists with correct kubevirt.io permissions |
| `oc get rolebinding namespace-vm-editor -n kube-system -o yaml` | RoleBinding shows vmuser subject correctly bound |
| Switch back to hub cluster and cleanup:<br/>`oc config use-context hub-cluster`<br/>`oc delete clusterpermissions namespace-vm-editor` | ClusterPermission deleted, resources cleaned up |

---

## Test Case 3: Permission Validation and Error Handling

**Description:** Validate ClusterPermissions schema validation and error handling for invalid configurations.

**Setup:**
- ACM hub cluster access
- Invalid YAML configurations for testing

| Step | Expected Result |
|------|----------------|
| Attempt invalid ClusterPermission (missing roleRef):<br/>`cat <<EOF \| oc apply -f -`<br/>`apiVersion: rbac.open-cluster-management.io/v1alpha1`<br/>`kind: ClusterPermission`<br/>`metadata:`<br/>`  name: invalid-permission`<br/>`  namespace: default`<br/>`spec:`<br/>`  clusterRoleBinding:`<br/>`    subjects:`<br/>`    - kind: User`<br/>`      name: testuser`<br/>`EOF` | Error: validation failed, roleRef required |
| Attempt invalid subject configuration:<br/>`cat <<EOF \| oc apply -f -`<br/>`apiVersion: rbac.open-cluster-management.io/v1alpha1`<br/>`kind: ClusterPermission`<br/>`metadata:`<br/>`  name: invalid-subject`<br/>`  namespace: default`<br/>`spec:`<br/>`  clusterRole:`<br/>`    rules:`<br/>`    - verbs: ["get"]`<br/>`      resources: ["pods"]`<br/>`  clusterRoleBinding:`<br/>`    roleRef:`<br/>`      apiGroup: rbac.authorization.k8s.io`<br/>`      kind: ClusterRole`<br/>`      name: invalid-subject`<br/>`EOF` | Error: Either subject or subjects required in clusterRoleBinding |
| Test maximum field lengths with very long names | Error: field length validation enforced |
| `oc get clusterpermissions` | No invalid ClusterPermissions created |

---

## Test Case 4: RBAC UI Navigation and Access

**Description:** Validate RBAC UI components are accessible and functional within the ACM console.

**Setup:**
- ACM Console access via web browser
- User with appropriate UI access permissions

| Step | Expected Result |
|------|----------------|
| Navigate to ACM Console: `https://console-openshift-console.apps.cluster-url.com` | ACM Console loads successfully |
| Login with admin credentials | Authentication successful, ACM dashboard visible |
| Navigate to Infrastructure → Virtual Machines | Virtual Machines page loads |
| Look for "Role Assignments" tab or RBAC section | Role Assignments tab visible (if implemented) |
| Navigate to User Management → Identities (if available) | Identities page loads with user listing |
| Check for RBAC-related menu items in navigation | RBAC menu entries visible in left navigation |
| Verify URL structure for RBAC routes: `/multicloud/infrastructure/virtualmachines/role-assignments` | RBAC routes accessible and functional |

---

## Test Case 5: User Identity Management UI

**Description:** Test user identity listing, search, and role assignment preparation features.

**Setup:**
- ACM Console with RBAC UI components deployed
- Multiple user identities available in the system

| Step | Expected Result |
|------|----------------|
| Navigate to User Management → Identities → Users | Users list page displays |
| Verify user listing shows name and display name | User table shows identity information |
| Test search functionality with user name filter | Search filters user list correctly |
| Select a user and view details | User details page shows YAML and metadata |
| Check for "Create Role Assignment" button | Button visible and functional |
| Click "Create Role Assignment" button | Modal or form opens for role assignment creation |
| Verify fallback from FullName to name field | Users without FullName show name field |
| Test pagination for large user lists | Pagination controls work correctly |

---

## Test Case 6: Group and ServiceAccount Management

**Description:** Validate group and service account identity management through the RBAC UI.

**Setup:**
- ACM Console with identity management features
- Test groups and service accounts configured

| Step | Expected Result |
|------|----------------|
| Navigate to User Management → Identities → Groups | Groups list page displays |
| Verify group listing and metadata display | Group information correctly shown |
| Navigate to User Management → Identities → ServiceAccounts | ServiceAccounts list displays |
| Test group search and filtering capabilities | Search functions work across group names |
| Select a group and view role assignment options | Group-specific role assignment interface |
| Verify ServiceAccount namespace visibility | ServiceAccounts show correct namespace context |
| Test bulk selection for multiple groups | Multi-select functionality works |

---

## Test Case 7: Role Assignment Lifecycle

**Description:** Test complete role assignment creation, editing, and deletion workflow.

**Setup:**
- RBAC UI fully deployed with RoleAssignment functionality
- Test users, groups, and clusters available

| Step | Expected Result |
|------|----------------|
| Navigate to Role Assignments list view | RoleAssignment list displays with filtering |
| Click "Create Role Assignment" button | Creation modal/form opens |
| Select role type: "view" from available options | Role dropdown populated with available roles |
| Select subject type: "Group" and specify "Security team" | Subject selection interface functional |
| Configure scope: cluster1 with namespaces ns1, ns2 | Cluster and namespace selection working |
| Submit role assignment creation | RoleAssignment created successfully |
| Verify new assignment appears in list | List updated with new role assignment |
| Edit the created role assignment | Edit modal opens with current values |
| Modify scope to add cluster2 | Scope modification saves correctly |
| Delete the role assignment with confirmation | Deletion modal and confirmation working |
| Verify deletion from list view | Role assignment removed from list |

---

## Test Case 8: Virtual Machine RBAC Integration

**Description:** Test RBAC tab integration within Virtual Machines view for contextual permission management.

**Setup:**
- Virtual Machines available in ACM
- RBAC UI integration completed

| Step | Expected Result |
|------|----------------|
| Navigate to Infrastructure → Virtual Machines | VM list displays correctly |
| Verify tab structure includes "Role Assignments" | Tab navigation shows RBAC option |
| Click on "Role Assignments" tab | Tab switches to show VM-specific RBAC view |
| Verify URL maintains VM context: `/multicloud/infrastructure/virtualmachines/role-assignments` | URL structure correct for VM RBAC |
| Test role assignment creation within VM context | VM-scoped role assignment workflow |
| Switch between VM list and Role Assignments tabs | Tab navigation functions smoothly |
| Verify role assignments filtered by VM context | Only VM-relevant permissions shown |

---

## Environment Setup Commands

```bash
# Login to cluster
oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify

# Verify ACM installation
oc get multiclusterhub -n ocm
oc get managedclusters

# Check RBAC CRD availability
oc get crd clusterpermissions.rbac.open-cluster-management.io
oc api-resources | grep rbac.open-cluster-management.io

# Access ACM Console
echo "Navigate to: https://console-openshift-console.apps.cluster-url.com"
```

## Notes

- **Feature Availability**: UI components may not be fully deployed; focus testing on available functionality
- **Progressive Testing**: Execute backend tests first, then UI tests as components become available
- **Error Validation**: Always verify proper error handling for invalid inputs
- **Multi-cluster Setup**: Ensure managed clusters are properly connected for propagation testing