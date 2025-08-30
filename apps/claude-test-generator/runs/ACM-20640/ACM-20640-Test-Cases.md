# ACM-20640 Test Cases - Component-Focused E2E Testing Strategy

---

## Test Case 1A: ClusterPermission Foundation - Core CR Lifecycle & Deployment

### Description
Validate the foundational ClusterPermission Custom Resource system focusing on core CR lifecycle, ManifestWork integration, and cross-cluster RBAC deployment. This test covers the essential infrastructure components that enable multi-cluster permission management.

**Primary Component Coverage:**
- **ClusterPermission CR lifecycle** (creation, validation, initial status monitoring)
- **ManifestWork integration** (cross-cluster deployment mechanism)
- **Multi-cluster RBAC deployment** (hub-to-spoke permission propagation)
- **End-user permission enforcement** (functional validation on managed clusters)

**Secondary Component Integration:**
- **Foundation for MulticlusterRoleAssignment** (auto-generated ClusterPermissions)
- **VM-specific ClusterPermissions** (kubevirt.io role patterns)
- **Backend infrastructure** for UI-driven role assignments

**Related JIRA Tickets:**
- **[ACM-21316](https://issues.redhat.com/browse/ACM-21316)**: ClusterPermission status with ManifestWork validation (CLOSED) - Core deployment mechanism
- **[ACM-22739](https://issues.redhat.com/browse/ACM-22739)**: ClusterPermission CR framework and UI integration (CLOSED) - CR infrastructure
- **[ACM-22615](https://issues.redhat.com/browse/ACM-22615)**: Aggregated API design (CLOSED) - Backend API framework
- **[ACM-22617](https://issues.redhat.com/browse/ACM-22617)**: Console/backend resources implementation (CLOSED) - Backend integration
- **[ACM-22755](https://issues.redhat.com/browse/ACM-22755)**: RoleAssignment client API (CLOSED) - API client framework

### Setup
**Prerequisites:**
```bash
# 1. Login to ACM Hub Cluster (Required First Step)
oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>
# Expected: Login successful

# 2. Verify ACM hub operational with ClusterPermission controller
oc get multiclusterhub -n open-cluster-management
# Expected: STATUS=Running

# 3. Check ClusterPermission CRD availability and controller status
oc get crd clusterpermissions.rbac.open-cluster-management.io
# Expected: CRD exists and available

oc get pods -n open-cluster-management | grep cluster-permission
# Expected: cluster-permission-xxx-xxx READY 1/1 STATUS Running

# 4. Verify managed clusters available for testing
oc get managedclusters
# Expected: 2+ clusters in Available status

# 5. Confirm ManifestWork system operational
oc get crd manifestworks.work.open-cluster-management.io
# Expected: ManifestWork CRD available for cross-cluster deployment
```

**Local RBAC User Setup (Manual Testing):**
```bash
# For manual testing, run the same scripts that Jenkins uses:
# 1. Clone the clc-ui repository (if not already available)
git clone https://github.com/stolostron/clc-ui.git
cd clc-ui

# 2. Set required environment variables
export CYPRESS_CLC_RBAC_PASS="test-RBAC-4-e2e"
export CYPRESS_HUB_API_URL="<CLUSTER_CONSOLE_URL>"

# 3. Run the RBAC user generation script (same as Jenkins)
# Script location: https://github.com/stolostron/clc-ui/blob/main/build/gen-rbac.sh
bash build/gen-rbac.sh

# 4. Verify RBAC users are created:
oc get identity | grep clc-e2e
# Expected: Multiple clc-e2e-* identities present

# 5. Verify HTPasswd identity provider is configured:
oc get oauth cluster -o jsonpath='{.spec.identityProviders[*].name}' | grep clc-e2e-htpasswd
# Expected: clc-e2e-htpasswd identity provider present

# Available users after running gen-rbac.sh:
# - clc-e2e-cluster-admin-cluster  (full cluster admin access)
# - clc-e2e-admin-cluster          (cluster admin access)  
# - clc-e2e-view-cluster           (cluster view access)
# - clc-e2e-clusterset-admin-cluster (cluster set admin access)
# - clc-e2e-admin-ns               (namespace admin access)
# - clc-e2e-edit-ns                (namespace edit access)
# - clc-e2e-view-ns                (namespace view access)
```

**Environment Configuration:**
- ACM Hub: 2.14+ with ClusterPermission controller running
- Managed Clusters: 3+ clusters for multi-cluster deployment testing  
- RBAC Test Users: Created via https://github.com/stolostron/clc-ui/blob/main/build/gen-rbac.sh script for permission validation
- Target Namespaces: `default`, `rbac-test` for scoped permissions
- HTPasswd Identity Provider: `clc-e2e-htpasswd` configured by gen-rbac.sh script

**⚠️ Important: Manual Testing vs Jenkins Execution**
- **Manual Testing**: Run https://github.com/stolostron/clc-ui/blob/main/build/gen-rbac.sh locally to create the same RBAC users that Jenkins uses
- **Jenkins Execution**: RBAC users are automatically provisioned as part of the pipeline
- **Environment Cleanup**: Previous test runs may leave ClusterPermissions that conflict with new tests

**QE Resource Patterns** (from existing https://github.com/stolostron/clc-ui/blob/main/cypress/tests/rbac/managedCluster_rbac.spec.js tests):
- ClusterRoleBindings: `rbac-test-binding-XXX`
- RoleBindings: `rbac-test-rolebinding-XXX` 
- ManagedClusters: `<TEST_CLUSTER_PREFIX>-XXX`

Therefore, **Step 2 (Environment Cleanup)** is **MANDATORY** to avoid `AlreadyExists` errors and resource conflicts.

**Sample ClusterPermission Blueprint:**
```yaml
apiVersion: rbac.open-cluster-management.io/v1alpha1
kind: ClusterPermission
metadata:
  name: test-clusterpermission-vm-access
  namespace: default
spec:
  clusterSelector:
    matchLabels:
      environment: "test"
  roleBindings:
  - namespace: default
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: view
    subject:
      apiGroup: rbac.authorization.k8s.io
      kind: User
      name: <TEST_RBAC_USER>@<TEST_DOMAIN>
```

### Test Steps

| Step | Action | Expected Result | Sample Commands/UI Navigation |
|------|--------|----------------|------------------------------|
| 1 | Login to ACM Hub Cluster | Successfully authenticated to hub with admin privileges and successfully logged into ACM hub cluster with admin privileges | **CLI**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>`  **UI**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with kubeadmin credentials  **Expected Output**: `Login successful. You have access to XX projects.`  **Verify Login**: `oc whoami` returns `kubeadmin` |
| 2 | Check for Existing ClusterPermissions and Clean Up | Environment prepared for new ClusterPermission testing and test environment cleaned of existing ClusterPermission conflicts | **CLI**: `oc get clusterpermissions \| grep -E "(test-\|rbac-test)"`  **If Exists**: Delete existing test ClusterPermissions  **Cleanup**: `oc delete clusterpermission --all --timeout=60s --ignore-not-found=true`  **Wait**: `sleep 30` for cleanup completion  **Verify Clean**: `oc get clusterpermissions` should show only system CPs |
| 3 | Create ClusterPermission CR Blueprint | ClusterPermission accepted and stored on hub, ClusterPermission CR created with proper spec and initial status | **What We're Doing:** Creating the core ClusterPermission custom resource that acts as a centralized RBAC blueprint. This CR defines the permission pattern once on the hub and will be automatically deployed to multiple managed clusters.  **CLI**: `oc apply -f clusterpermission-test.yaml`  **Expected Output**: `clusterpermission.rbac.open-cluster-management.io/test-clusterpermission-vm-access created`  **Verify**: `oc get clusterpermission test-clusterpermission-vm-access -o yaml` |
| 4 | Monitor ClusterPermission Controller Processing | Controller detects CR and initiates processing, controller processes ClusterPermission and begins ManifestWork generation | **What We're Doing:** Observing the ClusterPermission controller as it detects our newly created CR and begins processing it. The controller parses the RBAC blueprint and prepares to generate deployment packages for target clusters.  **CLI**: `oc describe clusterpermission test-clusterpermission-vm-access`  **Expected Status**: Processing condition appears  **Controller Logs**: `oc logs -n open-cluster-management deployment/cluster-permission | grep test-clusterpermission` |
| 5 | Validate ManifestWork Generation | Controller creates ManifestWork resources for target clusters, ManifestWork contains proper RBAC resources (Role, RoleBinding) for deployment | **What We're Doing:** Verifying that the ClusterPermission controller has successfully generated ManifestWork resources containing the actual Kubernetes RBAC objects. ManifestWork is ACM's deployment engine that transports RBAC definitions to managed clusters.  **CLI**: `oc get manifestwork -A | grep test-clusterpermission`  **Expected**: ManifestWork created in target cluster namespaces  **Detailed Check**: `oc get manifestwork test-clusterpermission-vm-access-mw -n <TEST_CLUSTER_1> -o yaml` |
| 6 | Verify Cross-Cluster RBAC Deployment | ManifestWork deploys actual RBAC resources on managed clusters, standard Kubernetes RBAC resources deployed and active on managed cluster | **CLI Target Cluster**: `oc get rolebinding -n default --context <TEST_CLUSTER_1> | grep rbac-test-user`  **Expected**: Role binding created for test user  **Permission Check**: `oc get role,rolebinding -n default --context <TEST_CLUSTER_1>` |
| 7 | Test Multi-Cluster Status Aggregation | ClusterPermission aggregates deployment status from all clusters, status accurately reflects deployment state across all target clusters | **CLI**: `oc get clusterpermission test-clusterpermission-vm-access -o yaml | grep -A10 status`  **Expected Status**:  ```yaml  status:    conditions:    - type: Applied      status: "True"    clusterResults:    - cluster: <TEST_CLUSTER_1>      status: Applied  ``` |
| 8 | Validate End-User Permission Enforcement | Deployed permissions functional for end users on managed clusters, permissions correctly enforced for actual user login sessions via CLI and ACM Console | **What We're Doing:** Testing the complete RBAC workflow by actually logging in as restricted users and verifying they can only access what they're supposed to. This proves the permissions work in real-world scenarios with both CLI and ACM Console access.  **CLI Setup**: First run https://github.com/stolostron/clc-ui/blob/main/build/gen-rbac.sh if not already done  **CLI User Login**: `oc login --insecure-skip-tls-verify -u clc-e2e-view-cluster -p test-RBAC-4-e2e <CLUSTER_CONSOLE_URL>`  **Expected**: Login successful  **Permission Test**: `oc auth can-i get pods -n default --context <TEST_CLUSTER_1>`  **Expected**: `yes`  **Negative Test**: `oc auth can-i delete pods -n default --context <TEST_CLUSTER_1>`  **Expected**: `no`  **UI Login Test**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with clc-e2e-view-cluster / test-RBAC-4-e2e  **Expected**: Limited ACM Console access based on RBAC permissions  **Logout**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>` (return to admin) |
---

## Test Case 1B: ClusterPermission Advanced Operations - Updates, Consistency & Error Handling

### Description
Validate advanced ClusterPermission operations including modifications, multi-cluster consistency, deletion workflows, and error handling. This test covers operational scenarios and edge cases that ensure production-ready RBAC management.

**Primary Component Coverage:**
- **ClusterPermission updates** (modification propagation and deployment updates)
- **Multi-cluster consistency** (identical permissions across fleet)
- **Lifecycle management** (deletion and cleanup workflows)
- **Error handling** (invalid configurations and graceful degradation)

**Secondary Component Integration:**
- **ManifestWork update propagation** (leveraging cross-cluster deployment updates)
- **Controller resilience** (error recovery and status reporting)
- **Fleet-wide validation** (consistency verification across clusters)

**Related JIRA Tickets:**
- **[ACM-21316](https://issues.redhat.com/browse/ACM-21316)**: ClusterPermission status with ManifestWork validation (CLOSED) - Update and cleanup operations
- **[ACM-22739](https://issues.redhat.com/browse/ACM-22739)**: ClusterPermission CR framework and UI integration (CLOSED) - Advanced CR operations

### Setup
**Prerequisites:**
```bash
# 1. Login to ACM Hub Cluster (Required First Step)
oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>
# Expected: Login successful

# 2. Verify ClusterPermission infrastructure from Test Case 1A
oc get crd clusterpermissions.rbac.open-cluster-management.io
# Expected: ClusterPermission system operational

# 3. Create base ClusterPermission for modification testing
oc apply -f clusterpermission-advanced-test.yaml
# Expected: test-clusterpermission-advanced created

# 4. Verify RBAC users available for testing
oc get identity | grep clc-e2e-view
# Expected: Jenkins-generated test users present
```

**Environment Configuration:**
- ACM Hub: 2.14+ with ClusterPermission controller running
- Managed Clusters: 3+ clusters for multi-cluster consistency testing
- Base ClusterPermission: Pre-created for modification and deletion testing
- RBAC Test Users: Available from https://github.com/stolostron/clc-ui/blob/main/build/gen-rbac.sh script execution

### Test Steps

| Step | Action | Expected Result | Sample Commands/UI Navigation |
|------|--------|----------------|------------------------------|
| 1 | Login to ACM Hub Cluster | Successfully authenticated to hub with admin privileges and successfully logged into ACM hub cluster with admin privileges | **CLI**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>`  **UI**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with kubeadmin credentials  **Expected Output**: `Login successful. You have access to XX projects.`  **Verify Login**: `oc whoami` returns `kubeadmin` |
| 2 | Verify Base ClusterPermission Deployed | Baseline ClusterPermission operational across clusters and base permissions deployed and functional across cluster fleet | **What We're Doing:** Confirming that our test ClusterPermission is properly deployed and functional across all target clusters before testing advanced operations. This ensures we have a solid foundation for modification and consistency testing.  **CLI**: `oc get clusterpermission test-clusterpermission-advanced -o yaml`  **Expected Status**: Applied condition = True  **Cluster Check**: `oc get rolebinding -n default --context <TEST_CLUSTER_1> | grep rbac-test-user` |
| 3 | Test ClusterPermission Modification | Updates to ClusterPermission propagate to managed clusters and ClusterPermission updates trigger ManifestWork updates and deployment propagation | **What We're Doing:** Testing the ClusterPermission update workflow by modifying the CR and verifying that changes are automatically propagated to all managed clusters through the ManifestWork system.  **CLI**: Modify ClusterPermission to add namespace `rbac-test`  **Update**: `oc patch clusterpermission test-clusterpermission-advanced --type='merge' -p='{"spec":{"roleBindings":[{"namespace":"rbac-test"}]}}'`  **Monitor**: `oc get manifestwork -A | grep test-clusterpermission-advanced` |
| 4 | Verify Update Propagation Timing | Changes deployed within expected timeframe and update propagation completes within operational SLA requirements | **What We're Doing:** Monitoring the time required for ClusterPermission modifications to propagate through the ManifestWork system to all managed clusters, ensuring updates occur within acceptable operational timeframes.  **CLI**: Monitor update status over time  **Timing Check**: `oc get clusterpermission test-clusterpermission-advanced -o yaml | grep -A5 lastUpdateTime`  **Expected**: Update propagation within 60 seconds |
| 5 | Validate Updated Permissions on Clusters | Modified permissions functional on all target clusters and updated permissions functional across all managed clusters | **What We're Doing:** Testing that the updated ClusterPermission modifications result in functional permission changes on managed clusters, verifying end-to-end update workflow effectiveness.  **CLI User Login**: `oc login --insecure-skip-tls-verify -u clc-e2e-view-cluster -p test-RBAC-4-e2e <CLUSTER_CONSOLE_URL>`  **New Permission Test**: `oc auth can-i get pods -n rbac-test --context <TEST_CLUSTER_1>`  **Expected**: `yes` (new namespace access)  **Cross-Cluster Test**: `oc auth can-i get pods -n rbac-test --context <TEST_CLUSTER_2>`  **Expected**: `yes`  **Logout**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>` (return to admin) |
| 6 | Verify Multi-Cluster Consistency | Same permissions deployed identically across all target clusters and consistent RBAC enforcement across entire cluster fleet | **What We're Doing:** Validating that ClusterPermission creates identical RBAC resources across all target clusters, ensuring consistent security posture and permission enforcement throughout the cluster fleet.  **CLI Multi-Cluster Check**:   ```  for cluster in <TEST_CLUSTER_1> <TEST_CLUSTER_2>; do    echo "=== $cluster ==="    oc get rolebinding -n default --context $cluster | grep rbac-test-user  done  ```  **Expected**: Identical role bindings across all clusters |
| 7 | Test Permission Inheritance Verification | Complex permission scenarios work consistently and complex permission inheritance works correctly across clusters | **What We're Doing:** Testing complex permission scenarios involving multiple namespaces and role bindings to ensure ClusterPermission correctly handles advanced RBAC patterns across all clusters.  **CLI**: Test multiple namespace access  **Multi-NS Test**: `oc auth can-i get pods --as=clc-e2e-view-cluster -n default --context <TEST_CLUSTER_1>`  **Cross-NS Test**: `oc auth can-i get pods --as=clc-e2e-view-cluster -n rbac-test --context <TEST_CLUSTER_1>`  **Expected**: Both return `yes` |
| 8 | Test ClusterPermission Deletion | CR deletion triggers cleanup across all managed clusters and complete cleanup of RBAC resources across all clusters | **What We're Doing:** Validating the ClusterPermission deletion workflow, ensuring that when a ClusterPermission is deleted, all associated RBAC resources are properly cleaned up across all managed clusters.  **CLI**: `oc delete clusterpermission test-clusterpermission-advanced`  **Verify Cleanup**: `oc get manifestwork -A | grep test-clusterpermission-advanced`  **Expected**: ManifestWork resources removed  **Cluster Check**: `oc get rolebinding -n default --context <TEST_CLUSTER_1> | grep rbac-test-user` |
| 9 | Verify Cleanup Completeness | All traces of deleted ClusterPermission removed and complete system cleanup with no orphaned resources | **What We're Doing:** Ensuring comprehensive cleanup by verifying that no remnants of the deleted ClusterPermission remain in the system, including status records, ManifestWork resources, and managed cluster RBAC objects.  **CLI**: Final cleanup verification  **Hub Check**: `oc get clusterpermission | grep test-clusterpermission-advanced`  **Expected**: Resource not found  **Full Cluster Sweep**: Check all namespaces for orphaned role bindings |
| 10 | Validate Error Handling | Invalid ClusterPermission configurations handled gracefully and error handling provides actionable feedback without breaking controller | **What We're Doing:** Testing the ClusterPermission controller's error handling capabilities by applying invalid configurations and verifying that errors are properly detected, reported, and handled without breaking the controller.  **CLI**: Apply invalid ClusterPermission with non-existent role  **Invalid Config**: Create CP with roleRef to non-existent ClusterRole  **Expected Error**: Status shows validation failure  **Status Check**: `oc describe clusterpermission invalid-test`  **Expected**: Clear error message about invalid role reference |

---

## Test Case 2: MulticlusterRoleAssignment Middleware - Simplified RBAC Interface

### Description
Validate the MulticlusterRoleAssignment CR that acts as a user-friendly middleware layer over the complex ClusterPermission system. This test focuses on the abstraction layer that enables simple 4-field role assignments while automatically generating complex infrastructure.

**Primary Component Coverage:**
- **MulticlusterRoleAssignment CR** (simplified interface with 4 fields: User, Role, Clusters, Namespaces)
- **Business logic encapsulation** (automatic ClusterPermission generation)
- **Middleware validation** (input validation and conflict resolution)
- **Automated lifecycle management** (garbage collection and health monitoring)

**Secondary Component Integration:**
- **Automatic ClusterPermission generation** (tests ClusterPermission infrastructure)
- **ManifestWork deployment** (leverages cross-cluster deployment system)
- **UI backend integration** (foundation for console-driven assignments)

**Related JIRA Tickets:**
- **[ACM-23009](https://issues.redhat.com/browse/ACM-23009)**: MulticlusterRoleAssignment CR Implementation (BLOCKER) - Core middleware component
- **[ACM-22925](https://issues.redhat.com/browse/ACM-22925)**: CRD modifications (IN PROGRESS) - MulticlusterRoleAssignment CRD design
- **[ACM-23466](https://issues.redhat.com/browse/ACM-23466)**: MulticlusterRoleAssignment filtering (IN PROGRESS) - Assignment filtering and management
- **[ACM-22760](https://issues.redhat.com/browse/ACM-22760)**: RoleAssignment list (CLOSED) - Backend listing and management

### Setup
**Prerequisites:**
```bash
# 1. Login to ACM Hub Cluster (Required First Step)
oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>
# Expected: Login successful

# 2. Verify MulticlusterRoleAssignment CRD and controller availability
oc get crd multiclusterroleassignments.rbac.open-cluster-management.io
# Expected: CRD available (depends on ACM-23009 completion)

# 3. Check controller status for MulticlusterRoleAssignment processing
oc get pods -n open-cluster-management | grep multicluster-role
# Expected: multicluster-role-assignment controller running

# 4. Verify prerequisite ClusterPermission infrastructure from Test Case 1
oc get crd clusterpermissions.rbac.open-cluster-management.io
# Expected: ClusterPermission infrastructure operational

# 5. Prepare test clusters with proper labeling for selection
oc label managedcluster <TEST_CLUSTER_1> environment=test
oc label managedcluster <TEST_CLUSTER_2> environment=test
# Expected: Clusters labeled for MulticlusterRoleAssignment targeting

# 6. Create required test namespace
oc create namespace rbac-test
# Expected: rbac-test namespace created for scoped permissions

# 7. Verify Jenkins RBAC users are available
oc get identity | grep clc-e2e-admin
# Expected: clc-e2e-admin-cluster and clc-e2e-admin-ns identities present
```

**Environment Configuration:**
- ACM Hub: 2.15+ with MulticlusterRoleAssignment controller (when available)
- Test Clusters: Multiple clusters labeled for assignment targeting (`environment: "test"`)
- RBAC Test Users: Created via https://github.com/stolostron/clc-ui/blob/main/build/gen-rbac.sh script for validation scenarios
- Test User: `clc-e2e-view-cluster` (Jenkins RBAC user with view permissions)
- Test Role: `view` ClusterRole (standard Kubernetes role for testing)
- Test Namespaces: `default`, `rbac-test` (created during setup)

**Sample MulticlusterRoleAssignment (Simplified Interface):**
```yaml
apiVersion: rbac.open-cluster-management.io/v1alpha1
kind: MulticlusterRoleAssignment
metadata:
  name: middleware-test-assignment
  namespace: default
spec:
  user: clc-e2e-view-cluster
  role: view
  clusterSelector:
    matchLabels:
      environment: "test"
  namespaces:
  - default
  - rbac-test
```

### Test Steps

| Step | Action | Expected Result | Sample Commands/UI Navigation |
|------|--------|----------------|------------------------------|
| 1 | Login to ACM Hub Cluster | Successfully authenticated to hub with admin privileges and successfully logged into ACM hub cluster with admin privileges | **CLI**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>`  **UI**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with kubeadmin credentials  **Expected Output**: `Login successful. You have access to XX projects.`  **Verify Login**: `oc whoami` returns `kubeadmin` |
| 2 | Create Simple MulticlusterRoleAssignment | Simplified CR accepted with 4-field interface and MulticlusterRoleAssignment created with simple, user-friendly spec | **What We're Doing:** Using the simplified 4-field interface to assign permissions instead of writing complex YAML. This demonstrates how the middleware layer makes RBAC assignment much easier for administrators by hiding technical complexity.  **Create YAML File**: Create `multicluster-role-assignment.yaml` with:  ```yaml  apiVersion: rbac.open-cluster-management.io/v1alpha1  kind: MulticlusterRoleAssignment  metadata:    name: middleware-test-assignment    namespace: default  spec:    user: clc-e2e-view-cluster    role: view    clusterSelector:      matchLabels:        environment: "test"    namespaces:    - default    - rbac-test  ```  **CLI**: `oc apply -f multicluster-role-assignment.yaml`  **Expected Output**: `multiclusterroleassignment.rbac.open-cluster-management.io/middleware-test-assignment created`  **Verify**: `oc get multiclusterroleassignment middleware-test-assignment` |
| 3 | Monitor Business Logic Processing | Middleware controller processes simple assignment and validates input and middleware validates assignment and prepares for ClusterPermission generation | **What We're Doing:** Watching the smart middleware system automatically process our simple assignment request. The system validates our inputs and prepares to create the complex infrastructure behind the scenes, so we don't have to.  **CLI**: `oc describe multiclusterroleassignment middleware-test-assignment`  **Expected Status**: Processing condition with validation results  **Controller Logs**: `oc logs -n open-cluster-management deployment/multicluster-role-assignment | grep middleware-test` |
| 4 | Validate Automatic ClusterPermission Generation | Simple assignment automatically generates complex ClusterPermission and complex ClusterPermission automatically created from simple 4-field assignment | **What We're Doing:** Discovering the "magic" behind the scenes - our simple 4-field assignment has automatically created a complex ClusterPermission with all the technical details filled in. This shows how the middleware hides complexity from users.  **CLI**: `oc get clusterpermission | grep middleware-test`  **Expected**: Auto-generated ClusterPermission with complex RBAC structure  **Generated CP**: `oc get clusterpermission middleware-test-assignment-generated -o yaml` |
| 5 | Verify ClusterPermission Complexity Abstraction | Auto-generated ClusterPermission contains proper RBAC complexity and generated ClusterPermission encapsulates full RBAC complexity from simple input | **What We're Doing:** Examining the auto-generated complex configuration to see that the system correctly translated our simple request into all the technical details needed for multi-cluster RBAC deployment.  **CLI**: `oc describe clusterpermission middleware-test-assignment-generated`  **Expected Structure**:  - Proper clusterSelector from assignment  - roleBindings for specified user/role  - namespace scoping as specified |
| 6 | Test Inheritance of ClusterPermission Infrastructure | Auto-generated ClusterPermission leverages existing deployment infrastructure and middleware leverages ClusterPermission infrastructure for actual deployment | **What We're Doing:** Verifying that our simple assignment now uses the same powerful deployment system as complex configurations. The middleware creates the infrastructure and then hands it off to the proven deployment mechanisms.  **CLI**: `oc get manifestwork -A | grep middleware-test-assignment`  **Expected**: ManifestWork created for ClusterPermission deployment  **Deployment Check**: `oc get rolebinding -n default --context <TEST_CLUSTER_1> | grep clc-e2e-view-cluster` |
| 7 | Validate Multi-Cluster Assignment Status | MulticlusterRoleAssignment aggregates status from generated ClusterPermission and assignment status aggregates deployment results from infrastructure layer | **What We're Doing:** Checking that our simple assignment shows us the overall deployment status across all clusters in an easy-to-understand summary, without needing to check each cluster individually.  **CLI**: `oc get multiclusterroleassignment middleware-test-assignment -o yaml | grep -A10 status`  **Expected Status**:  ```yaml  status:    conditions:    - type: Applied      status: "True"    assignmentStatus: Applied    clustersTargeted: 2    clustersSuccessful: 2  ``` |
| 8 | Test End-User Permission Validation | Simplified assignment results in functional permissions on managed clusters and simple assignment translates to functional permissions across target clusters | **What We're Doing:** Proving that our easy assignment approach actually works for real users by logging in as a restricted RBAC user. This demonstrates the complete success of the simplified middleware workflow from assignment to actual user access.  **CLI RBAC User Login**: `oc login --insecure-skip-tls-verify -u clc-e2e-view-cluster -p test-RBAC-4-e2e <CLUSTER_CONSOLE_URL>`  **Expected**: Login successful  **Permission Test**: `oc auth can-i get pods -n default --context <TEST_CLUSTER_1>`  **Expected**: `yes`  **Multi-Cluster Test**: `oc auth can-i get pods -n default --context <TEST_CLUSTER_2>`  **Expected**: `yes`  **UI Login Test**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with clc-e2e-view-cluster / test-RBAC-4-e2e  **Expected**: Limited ACM Console access via middleware-generated permissions  **Logout**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>` (return to admin) |
| 9 | Validate Assignment Modification | Updates to MulticlusterRoleAssignment propagate through infrastructure and assignment changes trigger ClusterPermission updates and re-deployment | **What We're Doing:** Testing that we can easily modify our assignment and the changes automatically flow through the entire system. This shows the middleware maintains the simple experience even when making updates.  **CLI**: Add namespace to assignment  **Update**: `oc patch multiclusterroleassignment middleware-test-assignment --type='merge' -p='{"spec":{"namespaces":["default","rbac-test","new-namespace"]}}'`  **Monitor**: Generated ClusterPermission updates |
| 10 | Test Garbage Collection | Deleting MulticlusterRoleAssignment cleans up generated infrastructure and middleware provides automated lifecycle management and cleanup | **What We're Doing:** Verifying that the middleware handles cleanup automatically when we delete our assignment. The system should remove all the complex infrastructure it created, so we don't have to manually clean up multiple resources.  **CLI**: `oc delete multiclusterroleassignment middleware-test-assignment`  **Expected**: Generated ClusterPermission removed automatically  **Infrastructure Check**: `oc get clusterpermission | grep middleware-test`  **Expected**: No orphaned ClusterPermissions |

---

## Test Case 3: Virtual Machine RBAC Specialization - CNV Integration & Granular Permissions

### Description
Validate specialized RBAC features for Container Native Virtualization (CNV) including cluster filtering, VM-specific roles, and fine-grained VM lifecycle permissions. This test focuses on virtualization-specific enhancements to the RBAC system.

**Primary Component Coverage:**
- **CNV cluster filtering** (only clusters with CNV operator visible for VM assignments)
- **VM-specific role templates** (kubevirt.io permissions and VM lifecycle roles)
- **Fine-grained VM permissions** (start, stop, migrate, console access granularity)
- **MTV integration** (Migration Toolkit for Virtualization workflow permissions)

**Secondary Component Integration:**
- **Leverages MulticlusterRoleAssignment** for VM-specific role distribution
- **Uses ClusterPermission infrastructure** for CNV-aware permission deployment
- **UI integration points** for CNV cluster filtering in role assignment creation

**Related JIRA Tickets:**
- **[ACM-21299](https://issues.redhat.com/browse/ACM-21299)**: CNV cluster filtering (CLOSED) - Only show CNV-enabled clusters in dropdowns
- **[ACM-20575](https://issues.redhat.com/browse/ACM-20575)**: VM action granularity (NEW) - Fine-grained VM lifecycle permissions
- **[ACM-22877](https://issues.redhat.com/browse/ACM-22877)**: Virtual Machines - Role Assignments (CLOSED) - VM role assignment tab integration
- **[ACM-23351](https://issues.redhat.com/browse/ACM-23351)**: Virtual Machines - Role Assignments new view (NEW) - Complete VM view reimplementation
- **[ACM-22348](https://issues.redhat.com/browse/ACM-22348)**: CNV addon and MTV-integrations onboarding (IN PROGRESS) - MTV workflow integration

### Setup
**Prerequisites:**
```bash
# Install CNV operator on target clusters for testing
oc apply -f - <<EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: hco-operatorhub
  namespace: openshift-cnv
spec:
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  name: kubevirt-hyperconverged
  channel: stable
EOF

# Verify CNV operator installation and VM readiness
oc get csv -n openshift-cnv | grep kubevirt-hyperconverged
# Expected: kubevirt-hyperconverged.v4.x.x Succeeded

# Check CNV cluster labeling for filtering
oc label managedcluster <CNV_TEST_CLUSTER_1> feature.open-cluster-management.io/addon-hypershift=available
oc label managedcluster <CNV_TEST_CLUSTER_2> feature.open-cluster-management.io/addon-hypershift=available
# Expected: CNV clusters properly labeled for filtering

# Deploy test VMs for RBAC testing
oc apply -f - <<EOF
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: <TEST_VM_NAME>
  namespace: default
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/vm: <TEST_VM_NAME>
    spec:
      domain:
        devices:
          disks:
          - disk:
              bus: virtio
            name: containerdisk
        resources:
          requests:
            memory: 1Gi
      volumes:
      - containerDisk:
          image: registry.redhat.io/ubi8/ubi:latest
        name: containerdisk
EOF
```

**Environment Configuration:**
- CNV Clusters: 2+ clusters with CNV operator installed and VMs deployed
- Standard Clusters: 1+ cluster without CNV for filtering validation
- Test VM User: `<VM_OPERATOR_USER>@<TEST_DOMAIN>` for VM-specific permission testing
- VM Lifecycle Roles: Custom roles for granular VM operation permissions

**Sample VM-Specific MulticlusterRoleAssignment:**
```yaml
apiVersion: rbac.open-cluster-management.io/v1alpha1
kind: MulticlusterRoleAssignment
metadata:
  name: vm-operator-assignment
  namespace: default
spec:
  user: <VM_OPERATOR_USER>@<TEST_DOMAIN>
  role: kubevirt-vm-operator
  clusterSelector:
    matchLabels:
      feature.open-cluster-management.io/addon-hypershift: available
  namespaces:
  - default
  vmResourceNames:
  - <TEST_VM_NAME>
```

### Test Steps

| Step | Action | Expected Result | Sample Commands/UI Navigation |
|------|--------|----------------|------------------------------|
| 1 | Verify CNV Cluster Detection | System identifies clusters with CNV operator installed and CNV cluster filtering operational based on operator presence detection | **CLI**: `oc get managedclusters -l feature.open-cluster-management.io/addon-hypershift=available`  **Expected**: CNV-enabled clusters listed  **Filtering Test**: Only CNV clusters appear in role assignment cluster selection |
| 2 | Create VM-Specific Role Assignment | VM role assignment targeting only CNV clusters and VM assignment correctly scoped to CNV-enabled clusters with VM-specific roles | **CLI**: `oc apply -f vm-role-assignment.yaml`  **Expected**: Assignment created targeting CNV clusters only  **Validation**: `oc describe multiclusterroleassignment vm-operator-assignment` |
| 3 | Validate VM Role Template Application | VM-specific roles (kubevirt.io permissions) deployed to CNV clusters and VM lifecycle permissions (start, stop, migrate) properly configured on CNV clusters | **CLI Target Cluster**: `oc get rolebinding -n default --context <CNV_TEST_CLUSTER_1> | grep vm-operator`  **Expected**: VM role binding created  **Permission Check**: `oc describe rolebinding vm-operator-binding -n default --context <CNV_TEST_CLUSTER_1>` |
| 4 | Test Fine-Grained VM Permissions | User can perform assigned VM operations with granular control and VM lifecycle permissions enforced at subresource level (start/stop/migrate) | **CLI as VM User**: `oc auth can-i patch virtualmachines/<TEST_VM_NAME> --subresource=start --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `yes`  **Granular Test**: `oc auth can-i delete virtualmachines/<TEST_VM_NAME> --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `no` (if role is VM operator, not admin) |
| 5 | Verify CNV Cluster Filtering Logic | Non-CNV clusters excluded from VM role assignments and cluster filtering prevents VM assignments on clusters without CNV capability | **What We're Doing:** Validating that the system correctly filters clusters for VM role assignments, ensuring that only clusters with Container Native Virtualization (CNV) installed receive VM-specific permissions. Standard clusters without CNV should be automatically excluded.  **CLI**: Check assignment doesn't deploy to standard cluster  **Standard Cluster Check**: `oc get rolebinding -n default --context <STANDARD_TEST_CLUSTER> | grep vm-operator`  **Expected**: No output (no VM role bindings on non-CNV cluster)  **Assignment Status Check**: `oc describe multiclusterroleassignment vm-operator-assignment | grep -A5 clustersTargeted`  **Expected**: Only CNV clusters listed in deployment status  **CNV Label Verification**: `oc get managedcluster <STANDARD_TEST_CLUSTER> --show-labels | grep hypershift`  **Expected**: No CNV feature label (confirming why cluster was excluded) |
| 6 | Test VM-Specific Resource Isolation | VM permissions scoped to specific VM resources when specified and VM-level permission isolation when specific VM resources are targeted | **What We're Doing:** Testing resource-level permission isolation to ensure VM operators can only access specific VMs they're assigned to. This validates that the RBAC system supports granular VM-level assignments rather than broad namespace access.  **CLI**: Test access to assigned VM  **Assigned VM**: `oc auth can-i get virtualmachines/<TEST_VM_NAME> --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `yes` (VM operator has access to assigned VM)  **Other VM Test**: `oc auth can-i get virtualmachines/<OTHER_VM_NAME> --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `no` (if vmResourceNames were specified in assignment to limit scope)  **Role Binding Verification**: `oc describe rolebinding vm-operator-binding -n default --context <CNV_TEST_CLUSTER_1> | grep resourceNames`  **Expected**: Shows specific VM resource names if isolation is configured |
| 7 | Validate MTV Integration | Migration-related permissions functional for cross-cluster VM migration and MTV workflow permissions integrated with VM RBAC assignments | **What We're Doing:** Testing Migration Toolkit for Virtualization (MTV) integration with VM RBAC to ensure cross-cluster migration permissions work correctly with our assigned VM operator role.  **CLI**: Test MTV resource access  **Migration CRD Access**: `oc auth can-i get migrations --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `yes` (VM operators need to view migration status)  **Migration Creation**: `oc auth can-i create migrations --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `yes` (VM operators should be able to initiate migrations)  **MTV Plan Access**: `oc auth can-i get migrationplans --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `yes` (needed for migration workflow planning)  **Cross-Cluster Migration**: `oc auth can-i create migrations --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_2>`  **Expected**: `yes` (consistent permissions across CNV clusters) |
| 8 | Test VM Console Access Permissions | VNC/console access controlled by VM RBAC assignments and VM console access properly controlled through RBAC subresource permissions | **What We're Doing:** Testing VM console access permissions to ensure `kubevirt-vm-operator` role provides appropriate console access. The VM operator role should allow console access to assigned VMs but not VMs outside their scope.  **CLI**: Test console subresource access  **Console Test**: `oc auth can-i get virtualmachines/<TEST_VM_NAME> --subresource=console --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `yes` (VM operators need console access for troubleshooting and management)  **VNC Access**: `oc auth can-i get virtualmachines/<OTHER_VM_NAME> --subresource=console --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `no` (if VM-specific resource names were specified in assignment)  **UI Console Test**: Navigate to CNV cluster → VMs → Select <TEST_VM_NAME> → Open console  **Expected**: Console access available for VM operator user |
| 9 | Verify Multi-Cluster VM Management | VM permissions consistent across all CNV clusters and VM RBAC assignments provide consistent permissions across all CNV-enabled clusters | **What We're Doing:** Validating that VM RBAC assignments create identical permissions across all CNV-enabled clusters, ensuring consistent operational experience regardless of which cluster the VM operator accesses.  **CLI Multi-Cluster Validation**:   ```  for cluster in <CNV_TEST_CLUSTER_1> <CNV_TEST_CLUSTER_2>; do    echo "=== Testing VM permissions on $cluster ==="    oc auth can-i patch virtualmachines/<TEST_VM_NAME> --subresource=start --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context $cluster  done  ```  **Expected**: All clusters return `yes` - consistent VM start permissions  **Cross-Cluster Console Test**: `oc auth can-i get virtualmachines/<TEST_VM_NAME> --subresource=console --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_2>`  **Expected**: `yes` (console access consistent across CNV clusters)  **Permission Validation**: Each CNV cluster should have identical Role and RoleBinding resources created by the assignment |
| 10 | Test VM Assignment Lifecycle | VM role assignment updates propagate correctly to CNV infrastructure and VM assignment modifications correctly update CNV permissions across clusters | **What We're Doing:** Testing the complete assignment lifecycle by modifying an existing VM role assignment and verifying that changes automatically propagate to all CNV clusters, updating the deployed RBAC resources appropriately.  **CLI**: Update VM assignment to add VM lifecycle permissions  **Update Assignment**: Modify the `vm-operator-assignment` to add migrate subresource permissions  **Verification**: `oc auth can-i patch virtualmachines/<TEST_VM_NAME> --subresource=migrate --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: `yes` (new migrate permissions available after update)  **Cross-Cluster Verification**: `oc auth can-i patch virtualmachines/<TEST_VM_NAME> --subresource=migrate --as=<VM_OPERATOR_USER>@<TEST_DOMAIN> -n default --context <CNV_TEST_CLUSTER_2>`  **Expected**: `yes` (updates propagated to all CNV clusters)  **Infrastructure Check**: `oc describe rolebinding vm-operator-binding -n default --context <CNV_TEST_CLUSTER_1>`  **Expected**: Role binding reflects updated permissions |

---

## Test Case 4: Universal Role Assignment Tabs - Complete UI Architecture

### Description
Validate the comprehensive UI implementation that adds "Role Assignments" tabs to every entity in the ACM system, providing universal access to role management across all contexts. This test focuses on the complete UI architecture and user experience workflows.

**Primary Component Coverage:**
- **Universal Role Assignment tabs** (every entity gets role assignment management)
- **Identity management interface** (Users, Groups, ServiceAccounts with full workflows)
- **Modal-based assignment creation** (context-aware role assignment workflows)
- **Entity-centric role management** (role assignments from any entity context)

**Secondary Component Integration:**
- **Uses MulticlusterRoleAssignment** for actual assignment creation through UI
- **Leverages CNV cluster filtering** for VM-related assignments through UI
- **Integrates with ClusterPermission** backend through UI-driven workflows

**Related JIRA Tickets:**
- **[ACM-22613](https://issues.redhat.com/browse/ACM-22613)**: Users implementation (TESTING) - User management interface and role assignment tabs
- **[ACM-22614](https://issues.redhat.com/browse/ACM-22614)**: Create role assignments modal (IN PROGRESS) - Modal-based assignment creation workflows
- **[ACM-22874](https://issues.redhat.com/browse/ACM-22874)**: Groups implementation (TESTING) - Group management with role assignment integration
- **[ACM-22875](https://issues.redhat.com/browse/ACM-22875)**: ServiceAccounts implementation (CLOSED) - ServiceAccount role assignment workflows
- **[ACM-22876](https://issues.redhat.com/browse/ACM-22876)**: Roles implementation (IN PROGRESS) - Role management interface with assignment tracking
- **[ACM-22730](https://issues.redhat.com/browse/ACM-22730)**: Menu entry, URL structure (NEW - Blocker) - Navigation infrastructure for Access Control
- **[ACM-23349](https://issues.redhat.com/browse/ACM-23349)**: Clusters - Role Assignment tab (NEW) - Cluster-context role assignments
- **[ACM-23350](https://issues.redhat.com/browse/ACM-23350)**: Cluster Sets - Role Assignment tab (NEW) - Cluster set-context role assignments

### Setup
**Prerequisites:**
```bash
# Verify RBAC UI features enabled through feature flags
oc get multiclusterhub multiclusterhub -n open-cluster-management -o yaml | grep -A5 overrides
# Expected: fine-grained-rbac-preview: enabled: true

# Check ACM console accessibility and RBAC UI availability
curl -k https://console-openshift-console.apps.<CLUSTER_BASE_DOMAIN>
# Expected: Console accessible

# Verify identity provider configuration for user/group testing
oc get oauth cluster -o yaml
# Expected: Identity provider configured for realistic user/group scenarios

# Prepare test entities for universal tab testing
oc create user <TEST_USER_1>
oc create user <TEST_USER_2>
oc create group <TEST_GROUP>
oc adm groups add-users <TEST_GROUP> <TEST_USER_1>
# Expected: Test users and groups available for UI testing
```

**Environment Configuration:**
- ACM Console: RBAC UI features enabled and accessible
- Identity Provider: Configured with test users and groups for realistic testing
- Test Entities: Users, Groups, Roles, Clusters, VMs available for tab testing
- Multi-cluster Environment: Multiple clusters for assignment targeting through UI

**UI Entity Context Map:**
```
Universal Role Assignment Tab Pattern:
├── Identities
│   ├── Users → [User Details] → Role Assignments Tab
│   ├── Groups → [Group Details] → Role Assignments Tab
│   └── ServiceAccounts → [SA Details] → Role Assignments Tab
├── Infrastructure
│   ├── Clusters → [Cluster Details] → Role Assignments Tab
│   └── Cluster Sets → [Cluster Set Details] → Role Assignments Tab
├── Workloads
│   └── Virtual Machines → [VM Context] → Role Assignments Tab
└── Access Control
    └── Roles → [Role Details] → Role Assignments Tab
```

### Test Steps

| Step | Action | Expected Result | Sample Commands/UI Navigation |
|------|--------|----------------|------------------------------|
| 1 | Login to ACM Hub Cluster | Successfully authenticated to hub with admin privileges and successfully logged into ACM hub cluster with admin privileges | **CLI**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>`  **UI**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with kubeadmin credentials  **Expected Output**: `Login successful. You have access to XX projects.`  **Verify Login**: `oc whoami` returns `kubeadmin` |
| 2 | Access RBAC Navigation Infrastructure | Access Control menu available with proper navigation and RBAC navigation infrastructure functional with proper menu integration | **What We're Doing:** Verifying that the RBAC UI features are properly enabled and accessible through the ACM Console navigation, ensuring the Access Control menu is available and functional.  **UI**: Navigate to main menu in ACM Console  **Expected**: "Access Control" menu item visible and clickable  **URL Test**: Navigate directly to `/multicloud/access-control`  **Expected**: RBAC UI loads without 404 errors |
| 3 | Validate Universal Identity Management | Users, Groups, ServiceAccounts interfaces with role assignment tabs and universal role assignment tabs present across all identity management interfaces | **What We're Doing:** Testing the universal role assignment tab pattern across all identity entities to ensure consistent user experience and functionality.  **UI**: Access Control → Identities → Users  **Expected**: User list displays with search/filter functionality  **User Detail**: Click individual user → Verify "Role Assignments" tab present  **Tab Navigation**: Test all identity entity types for universal tab pattern |
| 4 | Test Context-Aware Assignment Creation | Role assignment modal pre-fills context from entity entry point and context-aware assignment creation with smart field pre-filling | **What We're Doing:** Verifying that the role assignment creation workflow intelligently adapts to the entry point, pre-filling known context and simplifying the user experience.  **UI**: Navigate to Users → Select <TEST_USER_1> → Role Assignments tab → "Create Role Assignment"  **Expected**: Modal opens with user pre-selected and field disabled  **Modal Title**: Shows context "Create Role Assignment for <TEST_USER_1>"  **Available Fields**: Only role and cluster selection visible |
| 5 | Validate Cluster Context Role Assignments | Clusters and Cluster Sets provide role assignment management and cluster and cluster set contexts provide role assignment management capabilities with validated RBAC user access | **What We're Doing:** Testing that cluster and cluster set views provide complete role assignment management capabilities, including assignment creation with context-aware pre-filling and verification that RBAC assignments work for actual user login sessions.  **UI**: Navigate to Clusters → Select test cluster → Role Assignments tab  **Expected**: Tab shows assignments for selected cluster  **Create Assignment**: Test assignment creation with cluster pre-selected  **Cluster Set Test**: Repeat for Cluster Sets with set-level assignments  **CLI User Login**: `oc login --insecure-skip-tls-verify -u clc-e2e-admin-cluster -p test-RBAC-4-e2e <CLUSTER_CONSOLE_URL>`  **Expected**: Login successful with cluster admin access  **UI Login Test**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with clc-e2e-admin-cluster / test-RBAC-4-e2e  **Expected**: Full ACM Console access based on cluster admin RBAC permissions  **Logout**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>` (return to admin) |
| 6 | Test Virtual Machine Role Assignment Integration | VM contexts integrate with role assignment workflows and VM integration provides specialized role assignment workflows with CNV filtering | **What We're Doing:** Validating that Virtual Machine contexts provide specialized role assignment workflows with CNV cluster filtering to ensure VM-specific permissions are properly scoped.  **UI**: Navigate to Workloads → Virtual Machines → Select VM → Role Assignments tab  **Expected**: VM-context role assignments displayed  **CNV Filtering**: Create assignment shows only CNV clusters in dropdown  **VM-Specific Roles**: VM lifecycle roles available in role selection |
| 7 | Verify Role-Centric Assignment Management | Roles interface shows where roles are assigned across system and role-centric view provides comprehensive assignment visibility and management | **What We're Doing:** Testing the role-centric view that allows administrators to see all assignments using a specific role across the system, providing comprehensive visibility into role usage.  **UI**: Access Control → Roles → Select view ClusterRole → Role Assignments tab  **Expected**: Shows all assignments using this role across system  **Assignment Context**: Displays user/group and cluster information for each assignment  **Cross-Reference**: Validate assignment data matches entity-specific views |
| 8 | Test Modal Workflow Variations | Assignment creation adapts to different entity entry points and modal workflows intelligently adapt to entry point context | **What We're Doing:** Verifying that the assignment creation modal intelligently adapts its behavior based on the entry point, providing context-appropriate workflows for different starting points.  **UI Test Matrix**:   - From Group: Group pre-selected, choose user/role/cluster  - From Role: Role pre-selected, choose user/group/cluster  - From Cluster: Cluster pre-selected, choose user/group/role  **Expected**: Modal behavior adapts to entry context with appropriate field pre-filling |
| 9 | Validate Assignment List Management | Role assignment lists support filtering, search, and bulk operations and assignment list management provides enterprise-grade operational capabilities | **What We're Doing:** Testing the comprehensive assignment list management capabilities that provide enterprise-grade operations for managing role assignments at scale.  **UI**: Navigate to Access Control → Role Assignments  **Expected**: Comprehensive assignment list with filtering capabilities  **Bulk Operations**: Select multiple assignments for bulk delete  **Search/Filter**: Test filtering by user, role, cluster, status |
| 10 | Verify Cross-Entity Navigation | Assignment management provides seamless navigation between related entities and cross-entity navigation provides seamless role assignment management experience | **What We're Doing:** Testing the seamless navigation capabilities that allow users to move between related entities (users, roles, clusters) while maintaining context and providing an intuitive management experience.  **UI**: From assignment list → Click user name → Navigate to user details  **Expected**: Direct navigation to user's role assignment tab  **Reverse Navigation**: From user → assignment → cluster details  **Entity Linking**: Test navigation paths between all entity types |

---

## Test Case 5: Integrated End-to-End Validation - Complete RBAC Workflow

### Description
Validate the complete integrated RBAC system through comprehensive end-to-end workflows that exercise all components together. This test demonstrates the full system integration from UI-driven assignment creation through infrastructure deployment to end-user permission enforcement.

**Primary Component Coverage:**
- **Complete workflow integration** (UI → MulticlusterRoleAssignment → ClusterPermission → ManifestWork → Cluster RBAC)
- **Feature flag coordination** (conditional rendering and graceful degradation across all components)
- **Error handling and recovery** (comprehensive error scenarios across component boundaries)

**Secondary Component Integration:**
- **All previous test components** working together in realistic scenarios
- **Cross-component error propagation** and recovery mechanisms
- **End-to-end audit trail** and compliance validation

**Related JIRA Tickets:**
- **[ACM-23414](https://issues.redhat.com/browse/ACM-23414)**: Whole RBAC behind feature flag (CLOSED) - Complete feature flag integration
- **[ACM-23529](https://issues.redhat.com/browse/ACM-23529)**: Role assignment tabs behind feature flag (CLOSED) - Component-level feature flags
- **[ACM-22611](https://issues.redhat.com/browse/ACM-22611)**: Routes and menu entries (RESOLVED) - Complete navigation infrastructure
- **[ACM-23587](https://issues.redhat.com/browse/ACM-23587)**: YAML empty state (IN PROGRESS) - Error state handling
- **[ACM-23633](https://issues.redhat.com/browse/ACM-23633)**: Remove mock data, use real client (NEW) - Production data integration

### Setup
**Prerequisites:**
```bash
# Verify complete RBAC system operational
oc get multiclusterhub multiclusterhub -n open-cluster-management -o yaml | grep -A10 overrides
# Expected: All RBAC feature flags enabled

# Check all RBAC controllers operational
oc get pods -n open-cluster-management | grep -E "(cluster-permission|multicluster-role|console)"
# Expected: All RBAC-related controllers running

# Verify multi-cluster environment ready for complete testing
oc get managedclusters
# Expected: 3+ clusters (mix of CNV and standard) in Available status

# Prepare comprehensive test scenario data
oc create namespace e2e-rbac-test
oc create user <E2E_TEST_USER>@<TEST_DOMAIN>
oc create group e2e-test-group
oc adm groups add-users e2e-test-group <E2E_TEST_USER>@<TEST_DOMAIN>
# Expected: Complete test environment with users, groups, namespaces
```

**Environment Configuration:**
- Complete RBAC Stack: All components enabled and operational
- Multi-Cluster Fleet: CNV and standard clusters available
- Comprehensive Test Data: Users, groups, roles, VMs across multiple contexts
- Identity Integration: Full identity provider integration for realistic testing

**Complete E2E Scenario Setup:**
```yaml
# End-to-End Test Scenario: Enterprise VM Administrator Assignment
scenario:
  user: "<TEST_VM_ADMIN_USER>@<COMPANY_DOMAIN>"
  role: "kubevirt-vm-administrator"  
  clusters: ["<PROD_CNV_CLUSTER_1>", "<PROD_CNV_CLUSTER_2>", "<STAGING_CNV_CLUSTER>"]
  namespaces: ["production", "staging"]
  vms: ["<CRITICAL_VM_NAME>", "<WEB_VM_NAME>"]
  workflow: "UI → Assignment → Infrastructure → Enforcement"
```

### Test Steps

| Step | Action | Expected Result | Sample Commands/UI Navigation |
|------|--------|----------------|------------------------------|
| 1 | Login to ACM Hub Cluster | Successfully authenticated to hub with admin privileges and successfully logged into ACM hub cluster with admin privileges | **CLI**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>`  **UI**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with kubeadmin credentials  **Expected Output**: `Login successful. You have access to XX projects.`  **Verify Login**: `oc whoami` returns `kubeadmin` |
| 2 | Execute Complete UI-to-Infrastructure Workflow | Full role assignment workflow from UI through all infrastructure layers and complete workflow creates assignment, generates infrastructure, deploys to clusters | **What We're Doing:** Testing the complete end-to-end workflow from UI-driven assignment creation through all infrastructure components to final deployment, demonstrating the full system integration.  **UI**: Access Control → Users → Select <TEST_VM_ADMIN_USER> → Role Assignments → Create  **Form**: Select kubevirt-vm-administrator role, CNV clusters, <PRODUCTION_NAMESPACE>/<STAGING_NAMESPACE> namespaces  **Submit**: Monitor assignment creation through completion  **Backend**: `oc get multiclusterroleassignment,clusterpermission,manifestwork -A | grep <TEST_VM_ADMIN_USER>` |
| 3 | Validate Cross-Component Integration | Assignment creation triggers proper component interaction chain and component integration chain functional with proper status propagation | **What We're Doing:** Verifying that the assignment creation triggers the proper chain reaction through all system components, with each component processing and forwarding the request correctly.  **Monitor MulticlusterRoleAssignment**: `oc describe multiclusterroleassignment <TEST_VM_ADMIN_USER>`  **Expected**: Status shows processing and ClusterPermission generation  **Monitor ClusterPermission**: `oc describe clusterpermission <TEST_VM_ADMIN_USER>-generated`  **Expected**: Status shows ManifestWork creation and deployment |
| 4 | Test CNV Integration in Complete Workflow | VM assignment leverages CNV filtering and deploys VM-specific permissions and CNV integration properly filters clusters and deploys VM-specific permissions | **What We're Doing:** Validating that CNV integration works correctly in the complete workflow, ensuring VM assignments only target CNV-enabled clusters and deploy appropriate VM lifecycle permissions.  **CNV Cluster Check**: `oc get managedclusters -l feature.open-cluster-management.io/addon-hypershift=available`  **Expected**: Only CNV clusters targeted for VM assignment  **VM Permission Deployment**: `oc get rolebinding -n <PRODUCTION_NAMESPACE> --context <PROD_CNV_CLUSTER_1> | grep <TEST_VM_ADMIN_USER>`  **Expected**: VM lifecycle permissions deployed only to CNV clusters |
| 5 | Verify End-User Permission Enforcement | Complete assignment workflow results in functional end-user permissions and end-to-end workflow delivers functional permissions to target users via both CLI and ACM Console | **What We're Doing:** Testing the most critical aspect of the RBAC system - that the complete workflow from UI assignment creation through infrastructure deployment actually results in working permissions for real users logging in with both CLI and ACM Console access.  **CLI User Login**: `oc login --insecure-skip-tls-verify -u clc-e2e-admin-cluster -p test-RBAC-4-e2e <CLUSTER_CONSOLE_URL>`  **Expected**: Login successful  **VM Permission Test**: `oc auth can-i patch virtualmachines/<CRITICAL_VM_NAME> --subresource=start -n <PRODUCTION_NAMESPACE> --context <PROD_CNV_CLUSTER_1>`  **Expected**: `yes`  **Cross-Cluster Test**: Same permission check on <PROD_CNV_CLUSTER_2>  **Expected**: Consistent permissions across CNV cluster fleet  **UI Login Test**: Navigate to `<CLUSTER_CONSOLE_URL>` → Login with clc-e2e-admin-cluster / test-RBAC-4-e2e  **Expected**: ACM Console access with VM administrative capabilities based on assigned RBAC permissions  **VM Console Access**: Test VM operations through ACM Console → Workloads → Virtual Machines  **Expected**: VM lifecycle operations (start, stop, migrate) accessible based on RBAC assignments  **Logout**: `oc login --insecure-skip-tls-verify -u kubeadmin -p <CLUSTER_CONSOLE_PASSWORD> <CLUSTER_CONSOLE_URL>` (return to admin) |
| 6 | Test Feature Flag Coordination | Feature flags control complete system behavior consistently and feature flag coordination works across UI and backend components | **What We're Doing:** Verifying that feature flags work correctly across the complete system, ensuring UI and backend components respond appropriately to feature flag changes for controlled rollouts.  **Disable UI Flags**: `oc patch multiclusterhub multiclusterhub -n open-cluster-management --type='merge' -p='{"spec":{"overrides":{"components":[{"name":"rbac-role-assignment-tabs","enabled":false}]}}}'`  **UI Test**: Role assignment tabs should disappear from entity views  **Backend Test**: MulticlusterRoleAssignment creation still functional via CLI |
| 7 | Validate Complete Error Handling | Error scenarios properly handled across component boundaries and error handling provides comprehensive feedback across all system layers | **What We're Doing:** Testing comprehensive error handling across all system layers to ensure failures are properly detected, reported, and handled without breaking the overall system.  **Error Test 1**: Create assignment with invalid role  **Expected**: UI shows validation error, no infrastructure created  **Error Test 2**: Simulate cluster connectivity failure during deployment  **Expected**: Assignment shows partial deployment status with recovery guidance |
| 8 | Test Multi-Cluster Status Aggregation | Assignment status accurately reflects state across all target clusters and multi-cluster status aggregation provides accurate fleet-wide visibility | **What We're Doing:** Verifying that the system accurately aggregates and reports status across all target clusters, providing administrators with comprehensive visibility into fleet-wide RBAC deployment status.  **Status Check**: `oc get multiclusterroleassignment <TEST_VM_ADMIN_USER> -o yaml | grep -A15 status`  **Expected**: Status aggregates deployment results from all target clusters  **Cluster Breakdown**: Individual cluster status within overall assignment status  **Real-time Updates**: Status updates as cluster states change |
| 9 | Verify Audit Trail and Compliance | Complete audit trail maintained across all system components and complete audit trail supports compliance and security requirements | **What We're Doing:** Validating that comprehensive audit trails are maintained across all system components, supporting compliance requirements and security monitoring for enterprise environments.  **Assignment Audit**: `oc logs -n open-cluster-management deployment/console | grep "<TEST_VM_ADMIN_USER>"`  **Expected**: Assignment creation logged with user attribution  **Infrastructure Audit**: ClusterPermission and ManifestWork creation logged  **Enforcement Audit**: Permission enforcement logged on managed clusters |
| 10 | Test Assignment Lifecycle Management | Complete assignment lifecycle including updates and deletion and assignment lifecycle management works across complete system stack | **What We're Doing:** Testing the complete assignment lifecycle including updates and deletion to ensure the system properly manages assignments throughout their entire lifecycle with proper cleanup.  **Update Assignment**: Add additional namespace to existing assignment through UI  **Expected**: Update propagates through all infrastructure layers  **Delete Assignment**: Remove assignment and verify complete cleanup  **Expected**: All infrastructure components cleaned up across clusters |

---

*Each test case provides comprehensive validation of its primary component while intelligently leveraging secondary components through natural workflow integration, ensuring complete system coverage with minimal test case overlap.*