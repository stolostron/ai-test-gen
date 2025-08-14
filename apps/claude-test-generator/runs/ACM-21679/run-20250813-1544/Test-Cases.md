# E2E Test Cases - ACM Live Migration Tech Preview

## Test Case 1: MTV Addon Lifecycle Management and Deployment Validation

**Description**: Validate the complete lifecycle of MTV (Migration Toolkit for Virtualization) addon integration with ACM installer framework, ensuring proper deployment and configuration across managed clusters.

**Setup**: ACM hub cluster with managed clusters labeled for CNV operator installation. Ensure proper RBAC and network connectivity between clusters.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to ACM hub cluster. Terminal shows login confirmation and current context set to hub cluster with admin privileges for addon management. |
| **Step 2: Verify managed clusters with CNV compatibility** - List managed clusters and check CNV operator requirements: `oc get managedclusters -o yaml` | Display of all managed clusters with their status, availability, and labels. Clusters should show "Available=True" status indicating readiness for addon deployment. Sample output: `clc-aws-1754999178646 true True`, `staging-cluster-01 true True` |
| **Step 3: Apply CNV operator label to target managed cluster** - Label cluster for automatic CNV operator installation: `oc label managedcluster <cluster-name> acm/cnv-operator-install=true` | Successful labeling operation confirmed. Label applied to managed cluster enables automatic CNV operator deployment through ACM addon framework. Terminal shows: `managedcluster/<cluster-name> labeled` |
| **Step 4: Deploy MTV integrations addon via ACM installer** - Apply MTV addon template to hub cluster: `oc apply -f mtv-integrations-addon.yaml` | MTV addon deployment initiated successfully. Addon template creates necessary resources including ServiceAccount, ClusterRole, and addon configuration. Template application shows all resources created without errors. |
| **Step 5: Verify addon deployment status on hub** - Check MTV addon deployment on local-cluster: `oc get managedclusteraddons -A | grep mtv` | MTV addon appears in managedclusteraddons list with "Available=True" status. Addon shows successful deployment on local-cluster (hub) with proper CSV status and operator health indicators. |
| **Step 6: Validate CNV operator deployment on managed cluster** - Check CNV operator installation on labeled cluster: `oc get csv -n openshift-cnv --kubeconfig=<managed-cluster-kubeconfig>` | CNV operator successfully installed on managed cluster. CSV shows "Succeeded" phase with kubevirt-hyperconverged-operator running. Operator version matches expected deployment (e.g., v4.19.3). |
| **Step 7: Verify cross-cluster communication** - Test hub-to-spoke connectivity for migration workflows: `oc get managedclusterinfo <cluster-name> -o yaml` | Managed cluster info displays complete connectivity details including API endpoints, network configuration, and addon status. Communication channels established for cross-cluster operations. |
| **Step 8: Test addon removal and cleanup** - Remove CNV label and verify cleanup: `oc label managedcluster <cluster-name> acm/cnv-operator-install-` | Label removal triggers automatic addon uninstallation. CNV operator cleanup initiated on managed cluster with proper resource removal and namespace cleanup verification. |

## Test Case 2: Cross-Cluster VM Migration Workflow via ACM Console

**Description**: Test complete cross-cluster VM migration workflow initiated from ACM console, validating MTV integration, migration request routing, and status monitoring across cluster boundaries.

**Setup**: Hub cluster with MTV addon deployed, source cluster with running VM, target RHOV spoke cluster prepared for migration. Ensure network connectivity and storage compatibility.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to ACM hub cluster with access to multi-cluster VM management interface. Console shows connected clusters and virtualization capabilities. |
| **Step 2: Navigate to Virtual Machines overview in ACM console** - Access VM management through ACM web console at `https://console-openshift-console.apps.<hub-domain>` | ACM console displays Virtual Machines section with cross-cluster VM inventory. Interface shows VMs from all managed clusters with their current status, resource usage, and available actions. |
| **Step 3: Create source VM on managed cluster** - Deploy test VM for migration: `oc apply -f test-vm.yaml --kubeconfig=<source-cluster-kubeconfig>` | Test VM successfully created on source cluster. VM shows "Running" status with proper resource allocation. VM details include CPU, memory, storage configuration for migration planning. |
| **Step 4: Initiate cross-cluster migration from ACM console** - Select VM and choose "Migrate to Cluster" option from actions menu | Migration wizard opens with cluster selection dropdown populated with compatible target clusters. Interface provides migration configuration options and validation checks for storage and network compatibility. |
| **Step 5: Select target RHOV spoke cluster and configure migration** - Choose target cluster and configure migration parameters including storage mapping | Target cluster selection validated for compatibility. Migration configuration shows storage class mapping, network configuration, and resource requirements. Validation passes with green status indicators. |
| **Step 6: Submit migration request and monitor status** - Execute migration and track progress through ACM console status monitoring | Migration request successfully submitted to MTV orchestration layer. Status monitoring displays real-time progress including preparation, data transfer, and cutover phases with estimated completion time. |
| **Step 7: Verify VM status during migration** - Monitor VM state transitions during migration process | VM status updates show progression through migration phases: "Preparing", "Migrating", "Completing". Source VM remains accessible until final cutover, maintaining service availability during migration window. |
| **Step 8: Validate successful migration completion** - Confirm VM operational on target cluster: `oc get vm <vm-name> -n <namespace> --kubeconfig=<target-cluster-kubeconfig>` | VM successfully migrated to target cluster with "Running" status. All VM configurations preserved including CPU, memory, storage, and network settings. Source cluster cleanup completed automatically. |

## Test Case 3: RBAC Integration for Cross-Cluster VM Management

**Description**: Validate fine-grained RBAC controls for virtualization operations across managed clusters, ensuring proper permission enforcement and role assignment workflows.

**Setup**: Multiple managed clusters with CNV installed, external identity provider configured, user accounts and groups for RBAC testing.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to ACM hub cluster with cluster-admin privileges for RBAC configuration. Access to identity management and role assignment interfaces confirmed. |
| **Step 2: Configure external identity provider integration** - Set up IDP for user/group synchronization: `oc apply -f identity-provider-config.yaml` | External identity provider successfully configured with user and group synchronization. IDP integration shows active status with proper authentication flow established for cross-cluster operations. |
| **Step 3: Create virtualization-specific roles** - Define VM management roles with specific permissions: `oc apply -f vm-management-roles.yaml` | Custom roles created with granular VM permissions including vm-viewer, vm-operator, and vm-admin with appropriate ClusterRole and Role definitions for different operational scopes. |
| **Step 4: Access ACM RBAC management interface** - Navigate to RBAC section in ACM console for role assignment creation | RBAC management interface displays users, groups, and service accounts from connected identity providers. Interface shows cluster filtering options and role assignment creation workflows. |
| **Step 5: Create cross-cluster role assignment for VM management** - Assign vm-operator role to user across multiple managed clusters | Role assignment wizard allows cluster selection with CNV filter showing only clusters with virtualization capabilities. Assignment created successfully with propagation to target clusters confirmed. |
| **Step 6: Validate permission enforcement on managed clusters** - Test user access to VM operations on assigned clusters: `oc auth can-i create vm --as=<test-user> --kubeconfig=<managed-cluster-kubeconfig>` | Permission validation confirms proper role enforcement. User can perform allowed operations (start/stop VMs) but blocked from unauthorized actions (delete VMs) with appropriate error messages. |
| **Step 7: Test permission matrix across cluster boundaries** - Verify role-to-permission mapping for cross-cluster scenarios | Permission matrix displays correctly in ACM console showing user capabilities across different clusters. Role assignments properly propagated with cluster-specific permission validation working as expected. |
| **Step 8: Monitor role assignment status and propagation** - Check ClusterPermissions API for cross-cluster role distribution | ClusterPermissions resources show successful propagation across all target clusters. Role assignment status monitoring displays real-time synchronization status with any propagation errors clearly indicated. |

## Test Case 4: VNC Console Integration During Live Migration

**Description**: Test VNC console accessibility and user transition during cross-cluster VM migration, ensuring seamless console access without requiring separate cluster authentication.

**Setup**: Running VM with VNC console access, cross-cluster migration capability configured, ACM console with integrated virtualization features.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to ACM hub cluster with access to integrated virtualization console features. Multi-cluster VM management interface available with console integration capabilities. |
| **Step 2: Launch VNC console for VM on source cluster** - Access VM console through ACM interface without cluster-specific login | VNC console opens successfully within ACM interface. Console displays VM desktop/terminal without requiring separate authentication to source managed cluster. Console URL shows ACM integration pattern. |
| **Step 3: Verify console connectivity and functionality** - Test console interaction and responsiveness before migration | Console responds to keyboard and mouse input with real-time interaction. Display updates smoothly with no connectivity issues. Console session maintains stable connection through ACM proxy. |
| **Step 4: Initiate live migration while console is active** - Start cross-cluster migration process while maintaining console session | Migration process begins with console session remaining active. User receives informational alert about migration in progress but console access continues without interruption during preparation phase. |
| **Step 5: Monitor console during migration phases** - Track console accessibility through migration preparation, transfer, and cutover | Console maintains connectivity during preparation and data transfer phases. During cutover phase, brief reconnection occurs automatically with minimal disruption to user session. |
| **Step 6: Validate console transition to target cluster** - Confirm console access redirects to target cluster post-migration | Console automatically transitions to target cluster endpoint without requiring new authentication. URL updates to reflect target cluster location while maintaining session continuity. |
| **Step 7: Test console functionality on target cluster** - Verify full console capabilities after migration completion | Console operates normally on target cluster with all functionality restored. Keyboard, mouse, and display functions work correctly with same performance characteristics as source cluster. |
| **Step 8: Verify error handling for console connectivity issues** - Test console behavior during network interruptions or cluster unavailability | Console displays appropriate error messages for connectivity issues with retry mechanisms. Graceful degradation when clusters unavailable with user-friendly error messaging and recovery guidance. |

## Test Case 5: MTV Integration Status Monitoring and Error Handling

**Description**: Validate comprehensive status monitoring for MTV integration workflows, error handling scenarios, and recovery procedures for failed migration operations.

**Setup**: ACM hub with MTV addon configured, managed clusters with various readiness states, test VMs for migration scenarios including failure conditions.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to ACM hub cluster with access to MTV integration monitoring and management interfaces. Full visibility into cross-cluster migration status and health monitoring. |
| **Step 2: Check MTV addon health across managed clusters** - Verify MTV integration status: `oc get managedclusteraddons -A -o wide` | MTV addon status displays across all managed clusters showing health, version, and connectivity information. Addons show "Available=True" for healthy clusters and specific error details for any problematic clusters. |
| **Step 3: Create test migration with storage incompatibility** - Initiate migration between clusters with incompatible storage classes | Migration validation detects storage class incompatibility and prevents submission. Error message provides specific details about storage requirements and suggests compatible target clusters or storage configuration changes. |
| **Step 4: Monitor failed migration recovery workflow** - Test migration failure handling and retry mechanisms | Failed migration displays in ACM console with detailed error analysis including root cause, affected resources, and recommended recovery actions. Retry option available with corrected configuration parameters. |
| **Step 5: Validate network connectivity error scenarios** - Test migration behavior during network interruptions between clusters | Network interruption during migration triggers automatic retry with exponential backoff. Status monitoring shows connection attempts and recovery progress with estimated time to resolution. |
| **Step 6: Test MTV operator downtime handling** - Simulate MTV operator unavailability and monitor system response | MTV operator downtime detected by ACM monitoring with clear alerts and degraded service indicators. Migration requests queued for processing once operator connectivity restored. |
| **Step 7: Verify cross-cluster resource cleanup after failures** - Check resource cleanup for failed migrations: `oc get migrationjobs -A` | Failed migration resources properly cleaned up across both source and target clusters. No orphaned resources or incomplete configurations left behind with clear audit trail of cleanup actions. |
| **Step 8: Test bulk migration error handling** - Submit multiple migration requests with mixed success/failure scenarios | Bulk migration interface handles mixed results appropriately with individual job status tracking. Successful migrations complete while failed ones provide specific error details and recovery options without affecting other operations. |