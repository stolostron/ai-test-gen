# Test Cases for ACM-1745: Implement upgrade modal for AWS Hypershift clusters

## Description
Validate the HyperShift upgrade modal functionality that enables independent control plane and node pool upgrades for AWS hosted clusters through a comprehensive modal interface with version compatibility validation and progress tracking.

## Setup
- Access to ACM Hub cluster with HyperShift operator enabled and AWS hosted clusters available
- AWS HyperShift hosted clusters with available upgrade versions for comprehensive testing
- ACM Console with integrated HyperShift cluster management interface accessible
- Valid AWS credentials configured for HyperShift cluster operations and upgrades

## Test Cases

### Test Case 1: AWS HyperShift Control Plane Upgrade Workflow via Modal Interface

**Description**: Verify the HyperShift upgrade modal successfully initiates and manages control plane upgrades for AWS hosted clusters with proper version selection, compatibility validation, and progress monitoring throughout the upgrade process.

**Step 1: Log into ACM Console** - Access ACM Console for HyperShift cluster upgrade functionality testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in through Console authentication interface and navigate to "Infrastructure" → "Clusters" to access cluster management
- **CLI Method**: Authenticate and establish HyperShift access: `oc login https://api.<cluster-host>:6443 -u <username> -p <password>`
- **Expected Results**: Console loads successfully displaying clusters page with HyperShift hosted clusters visible and upgrade availability indicators shown

**Step 2: Access AWS HyperShift Cluster Management** - Navigate to specific AWS HyperShift hosted cluster for upgrade testing and modal access
- **UI Method**: Click on target AWS HyperShift hosted cluster name to access detailed cluster management page with upgrade options
- **CLI Method**: List available HyperShift clusters and verify status: `oc get hostedclusters -n clusters --show-labels | grep aws`
- **Expected Results**: Cluster details page displays with HyperShift-specific information, cluster status, and prominent upgrade button accessible

**Step 3: Launch HyperShift Upgrade Modal** - Open the upgrade modal interface for version selection and upgrade configuration management
- **UI Method**: Click "Upgrade cluster" button to launch the HyperShift upgrade modal dialog with component selection options
- **CLI Method**: Check current cluster version and available upgrades: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.spec.release.image}'`
- **Expected Results**: Modal opens displaying control plane section with current version information and dropdown showing available upgrade versions

**Step 4: Configure Control Plane Upgrade Settings** - Select target version for control plane upgrade with compatibility validation and upgrade confirmation
- **UI Method**: Enable "Upgrade control plane" checkbox and select desired target version from available options dropdown
- **CLI Method**: Verify upgrade path availability using version config: `oc get configmap supported-versions -n hypershift -o yaml | grep -A 5 "4.14"`
- **Expected Results**: Control plane upgrade section enabled with version dropdown populated, compatibility validation successful, and upgrade options clearly displayed

**Step 5: Initiate Control Plane Upgrade Process** - Submit upgrade request and monitor real-time progress through modal progress tracking interface
- **UI Method**: Click "Upgrade" button to submit control plane upgrade request and observe live progress indicators and status updates
- **CLI Method**: Monitor upgrade initiation and progress: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.status.conditions[?(@.type=="Progressing")]}'`
- **Expected Results**: Control plane upgrade initiates successfully with progress tracking visible in modal and upgrade status updating in real-time

**Step 6: Validate Control Plane Upgrade Completion** - Confirm successful control plane upgrade completion and verify version update in cluster status
- **UI Method**: Monitor upgrade completion through modal interface and verify updated version information in cluster details
- **CLI Method**: Validate successful version update: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.status.version.history[0].version}'`
- **Expected Results**: Control plane upgrade completes successfully with new version reflected in cluster status and modal confirming completion

### Test Case 2: Node Pool Upgrade Management through HyperShift Modal Selection

**Description**: Validate the HyperShift upgrade modal manages individual node pool upgrades with proper version compatibility checking, selective node pool targeting, and independent upgrade execution monitoring.

**Step 1: Log into ACM Console** - Access ACM Console for comprehensive node pool upgrade functionality testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to HyperShift cluster with multiple node pools configured for thorough testing coverage
- **CLI Method**: List cluster node pools and verify configuration: `oc get nodepools -n clusters --show-labels | grep <cluster-name>`
- **Expected Results**: HyperShift cluster accessible with multiple node pools displayed and individual upgrade management capabilities available

**Step 2: Access Node Pool Upgrade Interface** - Open upgrade modal with focus on node pool management and individual selection capabilities
- **UI Method**: Launch cluster upgrade modal and expand node pools section to display individual node pool upgrade options
- **CLI Method**: Check current node pool versions and upgrade availability: `oc get nodepools -n clusters -o custom-columns=NAME:.metadata.name,VERSION:.spec.release.image`
- **Expected Results**: Modal displays expandable node pools section with table interface showing individual node pools and their current versions

**Step 3: Configure Node Pool Upgrade Selection** - Select specific node pools for upgrade with version compatibility validation and target version specification
- **UI Method**: Use expandable checkbox interface to select individual node pools and specify target versions for each selected node pool
- **CLI Method**: Prepare node pool upgrade configuration by creating upgrade specification: Create `nodepool-upgrade-config.yaml`:
```yaml
apiVersion: hypershift.openshift.io/v1beta1
kind: NodePool
metadata:
  name: aws-nodepool-workers
  namespace: clusters
spec:
  clusterName: test-hypershift-cluster
  release:
    image: "quay.io/openshift-release-dev/ocp-release:4.14.0-x86_64"
  replicas: 3
  platform:
    aws:
      instanceType: m5.large
      subnet:
        id: subnet-1234567890abcdef0
  management:
    upgradeType: Replace
    autoRepair: true
```
- **Expected Results**: Node pool selection interface allows individual targeting with version dropdown populated and compatibility validation active

**Step 4: Validate Version Compatibility Rules** - Verify version compatibility validation between control plane and selected node pool upgrade versions
- **UI Method**: Test compatibility validation by attempting to select node pool versions that exceed control plane version by more than one minor version
- **CLI Method**: Test version compatibility logic with validation check: `echo "Validating: Control plane 4.14.0 vs Node pool 4.12.0 - should be compatible within version skew policy"`
- **Expected Results**: Modal displays appropriate compatibility warnings for unsupported version combinations and prevents invalid upgrade configurations

**Step 5: Execute Individual Node Pool Upgrades** - Submit node pool upgrade requests with comprehensive progress monitoring for each selected node pool
- **UI Method**: Click "Upgrade" to initiate selected node pool upgrades and monitor individual progress tracking for each node pool
- **CLI Method**: Apply node pool upgrade and monitor status: `oc apply -f nodepool-upgrade-config.yaml && oc get nodepools -n clusters -w`
- **Expected Results**: Selected node pool upgrades initiate with individual progress indicators and status tracking for each node pool upgrade operation

**Step 6: Verify Node Pool Upgrade Completion** - Confirm successful node pool upgrade completion and validate updated versions across all selected node pools
- **UI Method**: Monitor completion status through modal interface and verify all selected node pools reach desired version successfully
- **CLI Method**: Validate node pool upgrade success: `oc get nodepools -n clusters -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[0].type,VERSION:.status.version`
- **Expected Results**: All selected node pools complete upgrades successfully with final versions matching target specifications and status indicators confirming completion

### Test Case 3: HyperShift Modal Error Handling and Version Compatibility Validation

**Description**: Validate comprehensive error handling, validation logic, and recovery scenarios within the HyperShift upgrade modal for various failure conditions and edge cases.

**Step 1: Log into ACM Console** - Access ACM Console for comprehensive error handling and validation testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Access HyperShift cluster environment prepared for error scenario testing and validation workflow verification
- **CLI Method**: Prepare error testing environment and verify cluster state: `oc get hostedcluster -n clusters | grep -E "(Failed|Progressing|Available)"`
- **Expected Results**: HyperShift cluster accessible with stable baseline state for comprehensive error scenario testing and validation

**Step 2: Test Version Compatibility Validation Logic** - Trigger version compatibility errors to validate modal error handling and user guidance
- **UI Method**: Attempt to configure incompatible version combinations such as node pool versions exceeding control plane by more than supported skew
- **CLI Method**: Test version validation conceptually by checking supported version policies: `echo "Testing scenario: Node pool 4.15.0 with Control plane 4.13.0 should trigger validation error"`
- **Expected Results**: Modal displays clear version compatibility error messages with specific guidance and prevents submission of invalid upgrade configurations

**Step 3: Validate Missing Version Information Handling** - Test modal behavior when supported version data is unavailable or incomplete
- **UI Method**: Observe modal response when version information is missing or when supported-versions ConfigMap is unavailable
- **CLI Method**: Check version configuration availability: `oc get configmap supported-versions -n hypershift -o jsonpath='{.data}' || echo "ConfigMap unavailable - testing error scenario"`
- **Expected Results**: Modal handles missing version information gracefully with informative error messaging and guidance for resolution

**Step 4: Test Network Connectivity and API Failure Scenarios** - Validate modal error handling during network failures, API timeouts, and connectivity issues
- **UI Method**: Simulate network connectivity issues during upgrade submission and observe error handling with recovery options
- **CLI Method**: Test API connectivity and timeout scenarios: `oc get hostedcluster <cluster-name> -n clusters --request-timeout=2s || echo "Testing API timeout scenario"`
- **Expected Results**: Modal provides clear error messages for connectivity issues with appropriate retry mechanisms and user guidance

**Step 5: Validate Upgrade Progress Error Handling** - Test progress monitoring, error reporting, and failure recovery during upgrade execution
- **UI Method**: Monitor upgrade progress indicators and observe error state handling when upgrades encounter failures or timeout conditions
- **CLI Method**: Monitor upgrade status and error conditions: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.status.conditions[?(@.type=="Degraded")]}'`
- **Expected Results**: Modal provides real-time progress updates with clear error reporting for upgrade failures and appropriate recovery guidance

**Step 6: Test Error Recovery and Retry Mechanisms** - Validate error recovery workflows, retry functionality, and resolution guidance for failed operations
- **UI Method**: Test retry functionality for recoverable errors and validate error recovery workflows through modal interface
- **CLI Method**: Verify cluster recovery state and health: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'`
- **Expected Results**: Modal provides comprehensive retry mechanisms for recoverable errors with clear resolution guidance and successful error recovery workflows