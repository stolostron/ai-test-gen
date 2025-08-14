# ACM-20640 RBAC UI Implementation - Enhanced Test Plan with Real Deployment Validation

**Generated:** 2025-01-14 17:36:24  
**Environment:** QE6 VMware (qe6-vmware-ibm.install.dev09.red-chesterfield.com)  
**Test Framework:** CLC UI Cypress E2E Testing + Manual ClusterPermission API Testing  
**Coverage:** All deployed RBAC functionality in ACM 2.14.0 with fine-grained RBAC preview

---

## Test Case 1: ClusterPermission CRD Backend Functionality Validation

**Description:** Validate the complete ClusterPermission CRD functionality including creation, deployment via ManifestWork, and cross-cluster RBAC policy enforcement using real test data.

**Setup:** 
- ACM hub cluster qe6 with fine-grained RBAC preview enabled
- Test users: `clc-e2e-view-cluster`, `clc-e2e-admin-cluster`, `john`
- Test groups: `cluster-admins`, `devops`

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 --username=kubeadmin --password=eMgeR-3RUsX-mE4t4-qWiS4 --insecure-skip-tls-verify=true` | Successful authentication to ACM hub cluster. Terminal output shows: `Login successful.` and `Using project "default"` with access to 109 projects |
| **Step 2: Verify ClusterPermission CRD availability** - Check that the ClusterPermission CRD is installed and operational: `oc get crd clusterpermissions.rbac.open-cluster-management.io` | ClusterPermission CRD is installed and shows creation timestamp. Output displays: `NAME: clusterpermissions.rbac.open-cluster-management.io CREATED AT: 2025-08-12T11:29:05Z` |
| **Step 3: List existing ClusterPermission resources** - View all currently deployed ClusterPermission resources: `oc get clusterpermissions -A` | Three existing ClusterPermission resources are visible with their namespaces and ages: ```text NAMESPACE            NAME                           AGE local-cluster        devops-team-read-only-vms      37h local-cluster        vm-admins-local-cluster        37h staging-cluster-01   john-admin-default-namespace   35h ``` |
| **Step 4: Examine a group-based ClusterPermission** - Inspect the vm-admins ClusterPermission for group assignments: `oc get clusterpermission -n local-cluster vm-admins-local-cluster -o yaml` | ClusterPermission shows group-based cluster role binding with cluster-admins group assigned kubevirt.io:admin role. Status shows AppliedRBACManifestWork: True with ManifestWork reference |
| **Step 5: Examine a user-based ClusterPermission** - Inspect the john-admin ClusterPermission for user assignments: `oc get clusterpermission -n staging-cluster-01 john-admin-default-namespace -o yaml` | ClusterPermission shows user-based role binding with john user assigned kubevirt.io:admin role in default namespace. RoleBinding configuration shows namespace-scoped permissions |
| **Step 6: Verify ManifestWork deployment** - Check that ClusterPermission creates corresponding ManifestWork: `oc get manifestwork -n local-cluster | grep vm-admins` | ManifestWork for vm-admins ClusterPermission exists and shows proper age: `vm-admins-local-cluster-6648e 37h` indicating successful deployment pipeline |
| **Step 7: Validate actual RBAC deployment** - Confirm ClusterRoleBinding was created on managed cluster: `oc get clusterrolebinding vm-admins-local-cluster` | Actual ClusterRoleBinding exists on managed cluster showing: ```text NAME                      ROLE                            AGE vm-admins-local-cluster   ClusterRole/kubevirt.io:admin   37h ``` |
| **Step 8: Test cluster-permission operator health** - Check operator status and recent activity: `oc logs -n ocm deployment/cluster-permission --tail=5` | Operator logs show active reconciliation with INFO messages about validating ClusterPermission, preparing ManifestWork payload, and successful reconciliation completion |

---

## Test Case 2: Cross-Cluster RBAC Policy Management and Enforcement

**Description:** Test the complete lifecycle of RBAC policy creation, cross-cluster deployment, and enforcement validation across multiple managed clusters.

**Setup:**
- ACM hub with multiple managed cluster namespaces
- Existing cluster-permission operator running
- Test users and groups configured

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 --username=kubeadmin --password=eMgeR-3RUsX-mE4t4-qWiS4 --insecure-skip-tls-verify=true` | Authentication successful with admin privileges for RBAC policy management. Access to ocm and multicluster-engine namespaces confirmed |
| **Step 2: Create new ClusterPermission for testing** - Create a new RBAC policy for clc-e2e-view-cluster user: Create YAML file with ClusterPermission for cluster-scoped view permissions to pods and apply with `oc apply -f clusterpermission-test.yaml` | ClusterPermission resource created successfully. Resource shows in namespace with pending or progressing status as operator begins reconciliation |
| **Step 3: Monitor operator reconciliation** - Watch cluster-permission operator process the new ClusterPermission: `oc logs -n ocm deployment/cluster-permission --follow` | Operator logs show reconciliation process: validating ClusterPermission, preparing ManifestWork payload, updating ManifestWork, and completion with "done reconciling ClusterPermission" message |
| **Step 4: Verify ManifestWork creation** - Check that operator created corresponding ManifestWork: `oc get manifestwork -n [target-cluster] | grep [clusterpermission-name]` | New ManifestWork appears in target cluster namespace with Applied status. ManifestWork contains ClusterRoleBinding or RoleBinding resources for deployment |
| **Step 5: Validate ClusterRoleBinding deployment** - Confirm RBAC policy deployed to managed cluster: `oc get clusterrolebinding [clusterpermission-name]` or `oc get rolebinding [clusterpermission-name] -n [target-namespace]` | Actual RBAC binding exists on managed cluster with correct subject (user/group), role reference, and creation timestamp matching ManifestWork deployment |
| **Step 6: Test permission enforcement** - Verify user has assigned permissions by testing access: `oc auth can-i get pods --as=[test-user]` or `oc auth can-i create virtualmachines --as=[test-user]` | Permission check returns "yes" for allowed actions and "no" for restricted actions, confirming RBAC policy is actively enforced on managed cluster |
| **Step 7: Update ClusterPermission policy** - Modify existing ClusterPermission to add/remove permissions: Edit ClusterPermission YAML to change role or add namespace-scoped roleBindings and apply changes | ClusterPermission update triggers operator reconciliation. ManifestWork updated with new policy configuration and deployed to managed cluster within operator reconciliation cycle |
| **Step 8: Clean up test ClusterPermission** - Remove test RBAC policy and verify cleanup: `oc delete clusterpermission [test-name] -n [namespace]` | ClusterPermission deletion triggers ManifestWork cleanup. Associated ClusterRoleBinding/RoleBinding removed from managed cluster automatically via owner reference |

---

## Test Case 3: User and Group Identity Management with RBAC Integration

**Description:** Validate user and group identity management capabilities with RBAC assignments, testing both individual user permissions and group-based access control.

**Setup:**
- Test users: clc-e2e-view-cluster, clc-e2e-admin-cluster, john
- Test groups: cluster-admins, devops  
- Various ClusterPermission resources for testing

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 --username=kubeadmin --password=eMgeR-3RUsX-mE4t4-qWiS4 --insecure-skip-tls-verify=true` | Successful authentication with access to user and group management capabilities. Can view users and groups across the cluster |
| **Step 2: List available users for RBAC testing** - Enumerate all users available for RBAC assignment: `oc get users` | Comprehensive list of test users displayed including: ```text clc-e2e-admin-cluster, clc-e2e-view-cluster, john ``` Plus 14+ additional CLC test users for various permission scenarios |
| **Step 3: List available groups for RBAC testing** - Enumerate all groups available for group-based permissions: `oc get groups` | Available groups displayed with member information: ```text NAME             USERS cluster-admins   user1, user2 devops           carolyn, luiz ``` |
| **Step 4: Test individual user RBAC assignment** - Verify john user has admin permissions in default namespace via ClusterPermission: `oc auth can-i create virtualmachines --as=john -n default` | Permission check confirms john has VM creation permissions in default namespace due to john-admin-default-namespace ClusterPermission with kubevirt.io:admin role |
| **Step 5: Test group-based RBAC assignment** - Verify cluster-admins group has cluster-wide VM admin permissions: `oc auth can-i "*" virtualmachines --as=system:serviceaccount:default:cluster-admin-member` | Group members have cluster-wide VM administration permissions through vm-admins-local-cluster ClusterPermission assigning kubevirt.io:admin to cluster-admins group |
| **Step 6: Validate user identity details** - Check user identity information and associated identities: `oc get user john -o yaml` | User resource shows identity provider information: ```yaml metadata:   name: john spec:   identities:   - htpasswd-test:john ``` |
| **Step 7: Test cross-namespace permission boundaries** - Verify namespace-scoped permissions don't grant cluster-wide access: `oc auth can-i create virtualmachines --as=john -n kube-system` | Permission check returns "no" for namespaces outside john's assigned scope, confirming namespace-scoped ClusterPermission correctly limits access to default namespace only |
| **Step 8: Validate group membership and inheritance** - Test that group membership properly inherits RBAC assignments: `oc auth can-i admin virtualmachines --as=[cluster-admins-member]` | Group member inherits VM admin permissions from cluster-admins group assignment, demonstrating proper group-based RBAC inheritance through ClusterPermission |

---

## Test Case 4: KubeVirt VM RBAC Integration and Permission Validation

**Description:** Test fine-grained RBAC integration with KubeVirt virtual machine resources, validating VM-specific permissions and role assignments.

**Setup:**
- KubeVirt plugin enabled in console
- kubevirt.io cluster roles available
- VM RBAC test ClusterPermissions deployed

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 --username=kubeadmin --password=eMgeR-3RUsX-mE4t4-qWiS4 --insecure-skip-tls-verify=true` | Authentication successful with access to KubeVirt resources and VM RBAC management. Console plugins include kubevirt-plugin for VM operations |
| **Step 2: Verify KubeVirt ClusterRoles availability** - Check that VM-specific cluster roles are available: `oc get clusterroles | grep kubevirt` | KubeVirt cluster roles are available including: ```text kubevirt.io:admin kubevirt.io:edit kubevirt.io:view ``` |
| **Step 3: Examine VM admin ClusterPermission** - Review the vm-admins ClusterPermission configuration: `oc get clusterpermission -n local-cluster vm-admins-local-cluster -o yaml` | ClusterPermission shows cluster-admins group assigned kubevirt.io:admin ClusterRole via clusterRoleBinding, providing full VM administration capabilities |
| **Step 4: Test VM creation permissions** - Verify cluster-admins group can create VMs: `oc auth can-i create virtualmachines --as=system:serviceaccount:test:cluster-admin-sa` | Permission check returns "yes" for VM creation, confirming kubevirt.io:admin role provides complete VM lifecycle management permissions |
| **Step 5: Test VM read-only permissions** - Verify devops group has read-only VM access: `oc auth can-i get virtualmachines --as=system:serviceaccount:test:devops-member` and `oc auth can-i delete virtualmachines --as=system:serviceaccount:test:devops-member` | Read permission returns "yes" while delete permission returns "no", confirming devops-team-read-only-vms ClusterPermission provides appropriate view-only access |
| **Step 6: Validate VM namespace isolation** - Test that namespace-scoped VM permissions are properly isolated: `oc auth can-i create virtualmachines --as=john -n default` and `oc auth can-i create virtualmachines --as=john -n kube-system` | john can create VMs in default namespace but not in kube-system, confirming namespace-scoped roleBinding in john-admin-default-namespace ClusterPermission |
| **Step 7: Test VM resource hierarchy** - Verify permissions extend to related VM resources: `oc auth can-i create virtualmachineinstances --as=system:serviceaccount:test:cluster-admin-sa` | Cluster admin can manage VirtualMachineInstance resources, confirming kubevirt.io:admin role covers complete VM resource hierarchy |
| **Step 8: Validate ManifestWork VM RBAC deployment** - Confirm VM RBAC policies deployed via ManifestWork: `oc get manifestwork -n local-cluster vm-admins-local-cluster-* -o yaml` | ManifestWork contains ClusterRoleBinding for kubevirt.io:admin role with cluster-admins subjects, showing proper cross-cluster VM RBAC policy deployment |

---

## Test Case 5: RBAC Policy Lifecycle Management and Operator Validation

**Description:** Test the complete lifecycle of RBAC policy management including creation, updates, deletion, and operator health monitoring.

**Setup:**
- cluster-permission operator running in ocm namespace
- Multiple test ClusterPermissions for lifecycle testing
- ManifestWork monitoring capabilities

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 --username=kubeadmin --password=eMgeR-3RUsX-mE4t4-qWiS4 --insecure-skip-tls-verify=true` | Authentication successful with administrative access to RBAC operator management and policy lifecycle operations |
| **Step 2: Verify cluster-permission operator health** - Check operator pod status and recent activity: `oc get pods -n ocm | grep permission` and `oc logs -n ocm deployment/cluster-permission --tail=10` | Operator pod shows Running status: `cluster-permission-85b74455bd-9hsss 1/1 Running` with recent reconciliation logs showing successful ClusterPermission processing |
| **Step 3: Monitor operator reconciliation cycle** - Observe operator processing existing ClusterPermissions: `oc logs -n ocm deployment/cluster-permission --follow` | Operator logs show regular reconciliation cycles with INFO messages: validating ClusterPermission, preparing ManifestWork payload, updating ManifestWork, and completion messages |
| **Step 4: Create new test ClusterPermission** - Deploy a new RBAC policy and monitor operator response: Create ClusterPermission YAML and apply while monitoring operator logs | Operator immediately detects new ClusterPermission and begins reconciliation. Logs show validation, ManifestWork creation, and successful deployment within minutes |
| **Step 5: Validate policy deployment pipeline** - Track complete deployment from ClusterPermission to active RBAC: Check ClusterPermission status, ManifestWork creation, and final RBAC binding deployment | End-to-end pipeline completes successfully: ClusterPermission shows Applied status, ManifestWork created with Applied condition, and ClusterRoleBinding/RoleBinding active on managed cluster |
| **Step 6: Test policy modification** - Update existing ClusterPermission and verify operator handles changes: Edit ClusterPermission to modify role or add permissions and apply | Operator detects ClusterPermission changes and updates corresponding ManifestWork. New RBAC configuration deployed to managed cluster maintaining policy consistency |
| **Step 7: Simulate operator recovery** - Test operator resilience by restarting and verifying state recovery: `oc rollout restart deployment/cluster-permission -n ocm` | Operator restarts successfully and resumes ClusterPermission reconciliation. All existing policies remain intact and operator continues normal reconciliation cycles |
| **Step 8: Test policy cleanup** - Delete ClusterPermission and verify complete cleanup: `oc delete clusterpermission [test-name] -n [namespace]` | ClusterPermission deletion triggers ManifestWork cleanup. Associated RBAC bindings removed from managed cluster and operator logs confirm successful policy removal |

---

## Test Case 6: Integration with Existing CLC Workflows and RBAC Compatibility

**Description:** Validate that new ClusterPermission RBAC functionality integrates seamlessly with existing CLC cluster management, automation, and credential workflows.

**Setup:**
- Existing CLC test users with various permission levels
- Active cluster management and automation configurations
- Legacy RBAC configurations alongside new ClusterPermissions

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 --username=kubeadmin --password=eMgeR-3RUsX-mE4t4-qWiS4 --insecure-skip-tls-verify=true` | Authentication successful with access to both legacy CLC features and new ClusterPermission RBAC functionality |
| **Step 2: Test CLC user with ClusterPermission assignments** - Verify CLC test user can access cluster management with new RBAC: Login as `clc-e2e-admin-cluster` and test cluster listing capabilities | CLC test user maintains existing cluster management permissions while gaining additional ClusterPermission-based RBAC assignments for VM management |
| **Step 3: Validate automation RBAC integration** - Test that automation templates work with ClusterPermission users: Verify user can access ansible automation features based on ClusterPermission assignments | ClusterPermission RBAC correctly integrates with automation features. Users with appropriate ClusterPermission assignments can view/execute automation templates |
| **Step 4: Test credentials management compatibility** - Verify credential access follows both legacy and ClusterPermission RBAC: Check user access to cloud provider credentials and namespace-scoped credentials | Credential access respects both traditional OpenShift RBAC and new ClusterPermission assignments, with no conflicts or permission escalation |
| **Step 5: Validate cluster lifecycle operations** - Test cluster creation/management with ClusterPermission users: Attempt cluster operations with users having different ClusterPermission assignments | Cluster lifecycle operations work correctly with ClusterPermission-based RBAC. Users can manage clusters based on their assigned roles without conflicts |
| **Step 6: Test namespace isolation** - Verify ClusterPermission namespace scoping works with CLC features: Test user access to different namespaces in cluster management context | Namespace-scoped ClusterPermissions properly limit user access to specific namespaces while maintaining CLC feature functionality |
| **Step 7: Validate permission inheritance** - Test that group-based ClusterPermissions work with CLC group assignments: Verify devops group members inherit both CLC and ClusterPermission-based access | Group-based permission inheritance works correctly across both legacy CLC RBAC and new ClusterPermission assignments |
| **Step 8: Test backward compatibility** - Ensure existing ClusterRoleBindings continue working alongside ClusterPermissions: Verify legacy RBAC policies function normally with ClusterPermission operator running | Legacy ClusterRoleBindings and RoleBindings continue working normally. ClusterPermission operator doesn't interfere with existing RBAC configurations |

---

## Test Case 7: Multi-Cluster RBAC Deployment and ManifestWork Validation

**Description:** Test RBAC policy deployment across multiple managed clusters using ManifestWork, validating cross-cluster permission propagation and cluster-specific configurations.

**Setup:**
- Multiple managed cluster namespaces (local-cluster, staging-cluster-01)
- ManifestWork deployment pipeline active
- Various cluster-specific RBAC requirements

| Step | Expected Result |
|------|----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 --username=kubeadmin --password=eMgeR-3RUsX-mE4t4-qWiS4 --insecure-skip-tls-verify=true` | Hub cluster authentication successful with access to multiple managed cluster namespaces and ManifestWork management capabilities |
| **Step 2: Examine cross-cluster ClusterPermission deployment** - Review how ClusterPermissions deploy to different managed clusters: `oc get clusterpermissions -A` | Multiple ClusterPermissions deployed across different cluster namespaces: local-cluster (2 policies) and staging-cluster-01 (1 policy) with different RBAC configurations |
| **Step 3: Validate ManifestWork creation per cluster** - Check that each ClusterPermission creates cluster-specific ManifestWork: `oc get manifestwork -n local-cluster` and `oc get manifestwork -n staging-cluster-01` | Each managed cluster namespace contains ManifestWork resources corresponding to ClusterPermissions, with cluster-specific naming and configuration |
| **Step 4: Test cluster-scoped vs namespace-scoped policies** - Compare cluster-wide and namespace-specific RBAC deployments: Examine vm-admins-local-cluster (cluster-scoped) vs john-admin-default-namespace (namespace-scoped) | Cluster-scoped ClusterPermission creates ClusterRoleBinding while namespace-scoped creates RoleBinding, correctly targeting different permission scopes |
| **Step 5: Verify ManifestWork status across clusters** - Check deployment status for all cluster-specific ManifestWorks: `oc get manifestwork -A -l [clusterpermission-label] -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,APPLIED:.status.conditions[?(@.type=='Applied')].status` | All ManifestWorks show Applied: True status across all managed cluster namespaces, confirming successful cross-cluster RBAC policy deployment |
| **Step 6: Test policy propagation timing** - Monitor how quickly RBAC changes propagate across clusters: Modify ClusterPermission and track ManifestWork updates across cluster namespaces | ClusterPermission changes trigger ManifestWork updates within operator reconciliation cycle (typically within minutes) across all target cluster namespaces |
| **Step 7: Validate cluster-specific customization** - Test that different clusters can have different RBAC configurations: Compare local-cluster ClusterPermissions (group-based) with staging-cluster-01 (user-based) | Different managed clusters can have cluster-specific RBAC policies via separate ClusterPermissions, allowing customized permission models per cluster |
| **Step 8: Test ManifestWork cleanup across clusters** - Delete ClusterPermission and verify cleanup propagates to all target clusters: Delete ClusterPermission and monitor ManifestWork removal and RBAC binding cleanup | ClusterPermission deletion triggers ManifestWork cleanup across all target clusters, with RBAC bindings removed from managed clusters automatically |