# Live Migration ACM Console UI Integration - E2E Test Plan

## Test Case 1: ACM Console Feature Flag Configuration and UI Visibility

**Description**: Verify ACM console administrators can control live migration feature visibility through feature flag configuration and confirm UI elements respond appropriately.

**Setup**: 
- ACM hub cluster with console access
- Administrative privileges for feature flag configuration
- Live migration feature flag system deployed (PR #4677)

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Login successful with access to ACM console. Terminal shows authentication success and available projects. Console accessible at the configured URL. |
| **Step 2: Access ACM console feature flag configuration** - Navigate to ACM console administration settings and locate live migration feature flag controls | Feature flag configuration interface is accessible through admin settings. Live migration feature toggle is visible with current state (enabled/disabled). Configuration options are clearly labeled and functional. |
| **Step 3: Enable live migration features through feature flag** - Toggle live migration feature flag to enabled state and apply configuration changes | Feature flag successfully updated to enabled state. Configuration change confirmation displayed. UI indicates live migration features will be available after page refresh or session reload. |
| **Step 4: Navigate to Infrastructure Virtual Machines page** - Access Infrastructure → Virtual Machines section in ACM console to verify feature visibility | Virtual Machines page loads successfully with live migration features visible. Migration-related UI elements, action buttons, and menu options are displayed. Page layout includes migration workflow components. |
| **Step 5: Disable live migration features and verify UI changes** - Return to feature flag configuration, disable live migration, and confirm UI elements are hidden | Feature flag successfully disabled with confirmation. Virtual Machines page no longer shows migration-specific UI elements. Migration actions and buttons are properly hidden while other VM management features remain available. |

## Test Case 2: VM Table Integration and Migration Action Discovery

**Description**: Test the integration of migration actions into the VM management table and verify users can discover and access migration functionality for eligible VMs.

**Setup**:
- ACM console with live migration features enabled
- Multiple managed clusters with VMs deployed
- VM table adaptations deployed (PR #4643)

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Login successful with ACM console access. User can navigate to Infrastructure → Virtual Machines section. Authentication confirmed and project access available. |
| **Step 2: Navigate to Virtual Machines table** - Access Infrastructure → Virtual Machines to view VMs across managed clusters | VM table loads displaying VMs from multiple managed clusters. Table shows VM name, cluster location, status, and action options. Multi-cluster VM discovery is working properly with cluster attribution visible. |
| **Step 3: Locate VMs eligible for migration** - Identify VMs that support migration based on storage configuration and cluster compatibility | Table clearly identifies migration-eligible VMs through visual indicators or status columns. VMs with shared storage or compatible configurations show migration availability. Ineligible VMs display appropriate status or restrictions. |
| **Step 4: Access migration actions through table interface** - Click on Actions dropdown for an eligible VM to reveal migration options | Actions dropdown opens with migration options visible alongside standard VM operations (start, stop, restart). Migration actions are clearly labeled and distinguishable from other operations. Action availability matches VM eligibility status. |
| **Step 5: Verify migration action states and prerequisites** - Review migration action availability and any prerequisite warnings or requirements | Migration actions show appropriate states (available, disabled with reason, warning messages). Prerequisites clearly displayed such as storage requirements, network connectivity, or resource availability. Users receive clear guidance on migration readiness. |

## Test Case 3: Live Migration Wizard User Interface and Target Selection

**Description**: Validate the live migration wizard interface for target cluster selection, configuration options, and user workflow completion.

**Setup**:
- ACM console with migration wizard components (PR #4797 when merged)
- Multiple target clusters available for migration
- VM selected for migration from table interface

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Login successful with access to migration wizard functionality. ACM console loads with VM management features available including migration workflow components. |
| **Step 2: Initiate migration wizard from VM table** - Select a migration-eligible VM and choose "Live Migrate" from the actions dropdown | Migration wizard opens in modal or dedicated page interface. Wizard displays selected VM details including current cluster, resource requirements, and migration readiness status. Initial wizard screen provides clear migration overview. |
| **Step 3: Configure target cluster selection** - Use wizard interface to browse and select destination cluster from available managed clusters | Target cluster selection interface displays compatible managed clusters with resource availability indicators. Cluster options show CPU, memory, storage capacity and compatibility status. Selection process is intuitive with clear visual feedback. |
| **Step 4: Review migration configuration options** - Configure migration parameters such as storage mapping, network settings, and timing preferences | Configuration interface provides relevant migration options based on VM requirements and target cluster capabilities. Options include storage class mapping, network configuration, and migration scheduling. Settings validation provides immediate feedback. |
| **Step 5: Submit migration request through wizard** - Complete wizard workflow by reviewing settings and submitting migration request to MTV | Wizard displays comprehensive migration summary with all selected options. Submission confirmation shows migration request successfully dispatched to MTV orchestration system. User receives migration tracking reference and status monitoring guidance. |

## Test Case 4: Cross-Cluster Action Routing and MTV Integration

**Description**: Verify ACM console properly routes migration requests to MTV and manages the integration between console UI and migration orchestration backend.

**Setup**:
- MTV addon deployed and operational
- ACM console with MTV integration active
- Migration request initiated through ACM interface

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Login successful with access to ACM console and MTV integration features. Console displays VM management capabilities with migration actions available. |
| **Step 2: Initiate migration request from ACM console** - Submit a migration request through the ACM interface using established wizard workflow | Migration request successfully submitted from ACM console interface. System confirms request acceptance and provides migration tracking identifier. Console indicates request has been dispatched to MTV orchestration system. |
| **Step 3: Verify ACM to MTV request routing** - Confirm migration request properly routes from ACM console to MTV backend systems | MTV system receives migration request from ACM console with correct parameters and authentication. Request routing occurs seamlessly without user intervention. Backend logs or status indicators confirm successful request transfer. |
| **Step 4: Monitor ACM console for MTV response integration** - Check ACM console for MTV status updates and integration feedback | ACM console receives and displays MTV status updates including migration progress, phase information, and completion status. Integration between ACM UI and MTV backend provides real-time bidirectional communication. Status synchronization works correctly. |
| **Step 5: Validate error handling for failed routing** - Test scenarios where MTV is unavailable or request routing fails | ACM console properly handles MTV unavailability with appropriate error messages and user guidance. Failed routing scenarios display clear error information and suggested resolution steps. Console maintains functionality for other operations when MTV integration is impaired. |

## Test Case 5: Real-Time Migration Status Monitoring Through ACM Interface

**Description**: Test ACM console's ability to display real-time migration progress and status information from MTV orchestration system.

**Setup**:
- Active migration in progress
- ACM console with status monitoring capabilities
- MTV providing progress updates

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Login successful with access to migration monitoring dashboard. ACM console shows ongoing migrations and status tracking capabilities. Real-time monitoring interface is accessible. |
| **Step 2: Access migration monitoring dashboard** - Navigate to migration status section and locate active migration progress | Migration monitoring dashboard displays active migrations with progress indicators. Interface shows migration phases, completion percentages, and estimated time remaining. Status information updates in real-time without page refresh. |
| **Step 3: Verify detailed migration phase tracking** - Monitor migration progression through various phases including preparation, memory transfer, storage migration, and completion | Detailed phase information displays current migration stage with descriptive labels and progress indicators. Each phase shows relevant metrics such as data transfer rates, memory synchronization progress, and storage migration status. User understands current migration activity. |
| **Step 4: Test status update frequency and accuracy** - Observe status refresh rates and verify information accuracy against actual migration progress | Status updates occur frequently enough to provide meaningful progress feedback (every 30 seconds or better). Information displayed in console matches actual migration progress in backend systems. No significant delays or stale information present. |
| **Step 5: Monitor migration completion and final status** - Observe migration completion workflow and final status reporting in ACM console | Migration completion clearly indicated with success status and final VM location information. Post-migration VM status shows running state on target cluster. Console provides migration summary including duration, data transferred, and final validation status. |

## Test Case 6: Console Integration Error Handling and User Guidance

**Description**: Validate ACM console error handling for migration failures, networking issues, and provides appropriate user guidance for troubleshooting.

**Setup**:
- Migration scenarios with potential failure points
- ACM console with error handling mechanisms
- Test environments with controlled failure conditions

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Login successful with access to error handling and troubleshooting features. ACM console displays migration capabilities with error reporting mechanisms available. |
| **Step 2: Trigger migration prerequisite failure** - Attempt migration with insufficient target cluster resources or incompatible storage configuration | Console detects prerequisite failures and displays clear error messages with specific issues identified. Error reporting includes resource requirements, current availability, and steps needed to resolve issues. Migration blocked until prerequisites met. |
| **Step 3: Test MTV communication failure handling** - Simulate MTV unavailability or communication failure during migration request submission | Console handles MTV communication failures gracefully with appropriate error messages and retry options. User informed of integration issues and provided with troubleshooting guidance. Console maintains stability and functionality for other operations. |
| **Step 4: Verify migration progress error reporting** - Monitor console behavior when migration encounters errors during execution | Console displays migration errors with detailed information about failure points and potential causes. Error messages include actionable guidance for resolution such as checking network connectivity or resource availability. Users can determine next steps based on error information. |
| **Step 5: Test error recovery and retry mechanisms** - Use console to attempt error recovery or migration retry after resolving underlying issues | Console provides clear options for retrying failed migrations after issue resolution. Retry mechanisms work correctly without requiring complete workflow restart. Error state clears appropriately when issues are resolved and operations can proceed normally. |