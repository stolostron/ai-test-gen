# E2E Test Cases: ACM-20640 - RBAC UI Implementation [2.15]

## Test Case 1: ClusterPermission CRUD Operations and Validation

**Description**: This test case verifies the core functionality of ClusterPermission resources including creation, reading, updating, and deletion through both CLI and API operations to ensure the RBAC foundation is working correctly.

**Setup**: ACM hub cluster with managed clusters configured and proper RBAC permissions for testing user.

**Test Steps**:

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Login is successful and cluster access is confirmed. Terminal shows successful authentication message and available projects. ```Login successful. You have access to 109 projects, the list has been suppressed.``` |
| **Step 2: Verify ClusterPermission CRD availability** - Check that the RBAC CRDs are deployed: `oc get crd clusterpermissions.rbac.open-cluster-management.io` | ClusterPermission CRD is available and shows proper installation status. Output displays the CRD name, creation timestamp, and age indicating successful deployment. ```NAME                                               CREATED AT clusterpermissions.rbac.open-cluster-management.io   2025-08-12T11:29:05Z``` |
| **Step 3: Create a test ClusterPermission resource** - Apply a ClusterPermission configuration to grant VM view access: `oc apply -f -` with YAML content for VM viewer role | ClusterPermission resource is created successfully. Command returns successful creation message and resource is accepted by the API server. ```clusterpermission.rbac.open-cluster-management.io/test-vm-viewer created``` |
| **Step 4: Verify ClusterPermission status and ManifestWork creation** - Check resource status: `oc get clusterpermissions test-vm-viewer -n <target-cluster> -o yaml` | ClusterPermission shows "Applied" status and corresponding ManifestWork is created. Status conditions indicate successful RBAC policy deployment with proper ManifestWork reference. ```status: conditions: - type: AppliedRBACManifestWork   status: "True"   message: "ManifestWork successfully created"``` |
| **Step 5: Validate ManifestWork deployment** - Check the generated ManifestWork: `oc get manifestwork -n <target-cluster> | grep test-vm-viewer` | ManifestWork object exists and shows successful deployment to managed cluster. Output confirms the work is applied and managed cluster has received the RBAC policy. ```test-vm-viewer-abc123   1h``` |
| **Step 6: Test ClusterPermission updates** - Modify the ClusterPermission to change subject or roles: `oc patch clusterpermissions test-vm-viewer -n <target-cluster> --type=merge -p '{"spec":{"clusterRoleBinding":{"subjects":[...]}}}'` | Update is applied successfully and triggers ManifestWork update. The system processes the change and updates the deployed RBAC policies on the managed cluster. ```clusterpermission.rbac.open-cluster-management.io/test-vm-viewer patched``` |
| **Step 7: Clean up test resources** - Delete the test ClusterPermission: `oc delete clusterpermissions test-vm-viewer -n <target-cluster>` | ClusterPermission and associated ManifestWork are removed cleanly. The system performs proper cleanup removing RBAC policies from managed clusters. ```clusterpermission.rbac.open-cluster-management.io "test-vm-viewer" deleted``` |

---

## Test Case 2: Multi-Cluster RBAC Policy Enforcement

**Description**: This test case validates that ClusterPermission resources correctly enforce RBAC policies across multiple managed clusters and that permissions are properly synchronized and applied.

**Setup**: ACM hub cluster with at least two managed clusters connected and accessible.

**Test Steps**:

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to ACM hub cluster with access to multiple managed cluster namespaces. Terminal displays login confirmation and cluster access details. ```Login successful. Using project "default".``` |
| **Step 2: List available managed clusters** - Verify managed clusters are available: `oc get managedclusters` | Multiple managed clusters are shown as available and in Ready status. Output shows cluster names, status, and age confirming multi-cluster setup. ```NAME              HUB ACCEPTED   MANAGED CLUSTER URLS   JOINED   AVAILABLE   AGE local-cluster     true                              True     True        2d staging-cluster   true                              True     True        1d``` |
| **Step 3: Create ClusterPermission for multiple clusters** - Apply RBAC policy targeting multiple clusters: `oc apply -f -` with multi-cluster ClusterPermission | ClusterPermission is created successfully for multiple target clusters. System confirms resource creation and begins policy deployment across specified clusters. ```clusterpermission.rbac.open-cluster-management.io/multi-cluster-viewer created``` |
| **Step 4: Verify ManifestWork creation per cluster** - Check that ManifestWork is created for each target cluster: `oc get manifestwork --all-namespaces | grep multi-cluster-viewer` | Separate ManifestWork objects are created in each target cluster namespace. Output shows individual ManifestWork per cluster with proper naming and status. ```local-cluster       multi-cluster-viewer-abc123   1m staging-cluster     multi-cluster-viewer-def456   1m``` |
| **Step 5: Validate RBAC policy deployment status** - Check ManifestWork applied status: `oc get manifestwork multi-cluster-viewer-abc123 -n local-cluster -o yaml` | ManifestWork shows "Applied" status indicating successful policy deployment to managed cluster. Status confirms RBAC objects are created and functional on target clusters. ```status: conditions: - type: Applied   status: "True"   message: "Apply manifest work complete"``` |
| **Step 6: Test cross-cluster permission consistency** - Verify ClusterPermission status across clusters: `oc get clusterpermissions multi-cluster-viewer --all-namespaces` | ClusterPermission shows consistent status across all target cluster namespaces. System maintains policy coherence and reports uniform deployment success. ```NAMESPACE         NAME                    AGE local-cluster     multi-cluster-viewer   2m staging-cluster   multi-cluster-viewer   2m``` |
| **Step 7: Clean up multi-cluster resources** - Remove the ClusterPermission: `oc delete clusterpermissions multi-cluster-viewer --all-namespaces` | All ClusterPermission resources and associated ManifestWork objects are removed from all clusters. System performs complete cleanup across the multi-cluster environment. ```clusterpermission.rbac.open-cluster-management.io "multi-cluster-viewer" deleted``` |

---

## Test Case 3: RBAC Policy Validation and Error Handling

**Description**: This test case validates the RBAC system's ability to handle invalid configurations, detect policy conflicts, and provide appropriate error reporting for troubleshooting.

**Setup**: ACM hub cluster with managed clusters and test user accounts configured for validation scenarios.

**Test Steps**:

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful login with administrative access to create and test various RBAC configurations. Authentication completes and cluster access is verified. ```Login successful. You have access to 109 projects.``` |
| **Step 2: Test invalid ClusterPermission configuration** - Apply ClusterPermission with invalid subject type: `oc apply -f -` with malformed YAML (missing required fields) | ClusterPermission creation fails with validation error. API server rejects the resource with clear error message indicating specific validation failures. ```error validating data: ValidationError: spec.clusterRoleBinding.subjects[0].kind: Required value``` |
| **Step 3: Test non-existent ClusterRole reference** - Create ClusterPermission referencing non-existent role: `oc apply -f -` with invalid roleRef | ClusterPermission is created but ManifestWork shows failure status. System detects the invalid reference and reports error in status conditions. ```status: conditions: - type: AppliedRBACManifestWork   status: "False"   message: "ClusterRole 'invalid-role' not found"``` |
| **Step 4: Verify error reporting in ClusterPermission status** - Check detailed status of failed ClusterPermission: `oc get clusterpermissions invalid-rbac-test -n <target-cluster> -o yaml` | Status section contains detailed error information with specific failure reasons. Error messages provide actionable information for troubleshooting and remediation. ```status: conditions: - type: AppliedRBACManifestWork   status: "False"   reason: "RoleNotFound"   message: "Referenced ClusterRole does not exist on managed cluster"``` |
| **Step 5: Test ClusterPermission with conflicting subjects** - Create overlapping ClusterPermissions for same subjects: `oc apply -f -` with duplicate subject configurations | Both ClusterPermissions are created successfully but system handles conflicts appropriately. Status indicates any conflicts or overlapping permissions in the managed cluster. ```clusterpermission.rbac.open-cluster-management.io/conflicting-rbac created``` |
| **Step 6: Validate ManifestWork conflict resolution** - Check how system handles conflicting RBAC policies: `oc get manifestwork --all-namespaces | grep conflicting` | System creates separate ManifestWork objects and reports any conflicts in status. Conflict resolution follows last-writer-wins or provides clear conflict notification. ```local-cluster   conflicting-rbac-abc123   2m``` |
| **Step 7: Clean up test resources and verify cleanup** - Remove all test ClusterPermissions and check cleanup: `oc delete clusterpermissions --all --all-namespaces` | All test resources are removed successfully including failed configurations. System performs complete cleanup and removes associated ManifestWork objects. ```clusterpermission.rbac.open-cluster-management.io "invalid-rbac-test" deleted clusterpermission.rbac.open-cluster-management.io "conflicting-rbac" deleted``` |

---

## Test Case 4: RBAC Integration with Existing OpenShift Security

**Description**: This test case verifies that the ACM RBAC implementation integrates properly with existing OpenShift RBAC systems and doesn't interfere with native cluster security controls.

**Setup**: ACM hub cluster with existing OpenShift users, groups, and RBAC policies configured alongside native cluster security.

**Test Steps**:

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication with access to both ACM and native OpenShift RBAC resources. Login confirms cluster access and available security contexts. ```Login successful. You have access to 109 projects.``` |
| **Step 2: Document existing RBAC policies** - List current ClusterRoles and ClusterRoleBindings: `oc get clusterroles,clusterrolebindings | grep -E "(kubevirt|vm)" | head -10` | Existing OpenShift RBAC policies are displayed including VM and kubevirt-related roles. Output shows current security baseline before ACM RBAC integration. ```clusterrole.rbac.authorization.k8s.io/kubevirt.io:admin clusterrole.rbac.authorization.k8s.io/kubevirt.io:edit clusterrole.rbac.authorization.k8s.io/kubevirt.io:view``` |
| **Step 3: Create ClusterPermission using existing OpenShift roles** - Apply ClusterPermission that references native kubevirt roles: `oc apply -f -` with kubevirt.io:view role reference | ClusterPermission successfully integrates with existing OpenShift roles. System accepts native role references and creates appropriate bindings. ```clusterpermission.rbac.open-cluster-management.io/integration-test created``` |
| **Step 4: Verify ManifestWork uses existing roles** - Check ManifestWork content for native role usage: `oc get manifestwork integration-test-* -n <target-cluster> -o yaml` | ManifestWork correctly references existing OpenShift ClusterRoles without duplicating them. Generated RBAC objects use proper native role references. ```spec: workload: manifests: - apiVersion: rbac.authorization.k8s.io/v1   kind: ClusterRoleBinding   spec:     roleRef:       name: kubevirt.io:view``` |
| **Step 5: Test ACM RBAC alongside native OpenShift RBAC** - Create additional native ClusterRoleBinding and verify coexistence: `oc create clusterrolebinding native-test --clusterrole=kubevirt.io:view --user=test-user` | Both ACM-managed and native RBAC policies coexist without conflicts. System maintains separation and proper operation of both security systems. ```clusterrolebinding.rbac.authorization.k8s.io/native-test created``` |
| **Step 6: Validate permission inheritance and precedence** - Check effective permissions for users with both ACM and native RBAC: `oc auth can-i list virtualmachines --as=test-user` | Permissions are properly inherited and combined from both ACM ClusterPermissions and native bindings. User has expected access based on both policy sources. ```yes``` |
| **Step 7: Clean up integration test resources** - Remove test ClusterPermissions and native bindings: `oc delete clusterpermissions integration-test --all-namespaces && oc delete clusterrolebinding native-test` | All test resources are cleaned up without affecting existing OpenShift RBAC policies. System maintains stability of native security configurations. ```clusterpermission.rbac.open-cluster-management.io "integration-test" deleted clusterrolebinding.rbac.authorization.k8s.io "native-test" deleted``` |

---

## Test Case 5: RBAC UI Access Control Foundation (Post-2.15 Deployment)

**Description**: This test case validates the foundational UI components for RBAC management once the complete UI implementation is deployed, focusing on access control and user management interfaces.

**Setup**: ACM 2.15+ environment with complete RBAC UI implementation deployed and RoleAssignment CRDs available.

**Test Steps**:

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication with access to ACM console UI and RBAC management features. Login provides access to enhanced user management interfaces. ```Login successful. You have access to 109 projects.``` |
| **Step 2: Access ACM console User Management section** - Navigate to ACM console at `https://console-openshift-console.<cluster-domain>/multicloud/user-management/overview` | User Management section is accessible with Overview, Identities, and Roles subsections. UI displays RBAC management interface with proper navigation and access controls. ```User Management page loads successfully with Overview, Users, Groups, Roles sections visible``` |
| **Step 3: Verify RoleAssignment CRD availability** - Check for RoleAssignment resources: `oc get crd roleassignments.rbac.open-cluster-management.io` | RoleAssignment CRD is deployed and available for creating UI-driven role assignments. API resource enables UI-based RBAC management workflows. ```NAME                                              CREATED AT roleassignments.rbac.open-cluster-management.io    2025-XX-XXTXX:XX:XXZ``` |
| **Step 4: Test Users identity management interface** - Access Users section and verify user listing functionality | Users interface displays available cluster users with status, role assignments, and management actions. UI provides search, filter, and role assignment capabilities. ```Users page displays user list with Name, Status, Role Assignments columns and Create Role Assignment button``` |
| **Step 5: Verify Roles management interface** - Navigate to Roles section and check role listing and permissions display | Roles interface shows available ClusterRoles and Roles with permissions details. UI enables viewing role definitions and associated permissions clearly. ```Roles page displays role list with Name, Type, Permissions columns and detailed permission views``` |
| **Step 6: Test role assignment creation workflow** - Attempt to create new role assignment through UI modal | Role assignment creation modal opens with user/group selection, role selection, and scope definition. UI provides intuitive workflow for creating RBAC policies. ```Create Role Assignment modal opens with Subject, Role, and Scope selection options``` |
| **Step 7: Validate RBAC policy consistency** - Verify that UI-created assignments match CLI-accessible resources: `oc get roleassignments --all-namespaces` | UI-created role assignments are properly reflected in cluster resources with correct metadata and specifications. Consistency between UI and API ensures reliable RBAC management. ```NAME                     AGE ui-created-assignment   2m``` |