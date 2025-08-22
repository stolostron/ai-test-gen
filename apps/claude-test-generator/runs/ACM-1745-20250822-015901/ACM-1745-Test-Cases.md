# Test Cases for ACM-1745: Implement upgrade modal for AWS Hypershift clusters

## Description
Validate HyperShift AWS hosted cluster upgrade modal functionality enabling control plane and node pool version management through integrated upgrade workflows with version compatibility validation.

## Setup
- Access to ACM Hub cluster with HyperShift operator enabled and AWS hosted clusters
- HyperShift AWS hosted clusters with available upgrade versions for testing
- ACM Console with HyperShift cluster management interface accessible
- supported-versions ConfigMap in hypershift namespace with available upgrade paths

## Test Cases

### Test Case 1: AWS HyperShift Control Plane Upgrade via Modal

**Description**: Verify HyperShift upgrade modal successfully manages AWS hosted cluster control plane upgrades with proper version selection and compatibility validation.

**Step 1: Log into ACM Console** - Access ACM Console for HyperShift cluster upgrade testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in via Console authentication and navigate to "Infrastructure" → "Clusters"
- **CLI Method**: Authenticate and verify HyperShift access: `oc login https://api.<cluster-host>:6443 -u <username> -p <password>`
- **Expected Results**: Console loads with clusters page showing HyperShift hosted clusters with upgrade availability indicators

**Step 2: Access HyperShift Cluster Details** - Navigate to AWS HyperShift hosted cluster for upgrade testing
- **UI Method**: Click on AWS HyperShift hosted cluster name to access cluster details page
- **CLI Method**: List HyperShift clusters: `oc get hostedclusters -n clusters --show-labels`
- **Expected Results**: Cluster details page displays with HyperShift-specific information and upgrade button visible

**Step 3: Open Upgrade Modal** - Launch HyperShift upgrade modal for version selection and upgrade configuration
- **UI Method**: Click "Upgrade cluster" button to open HyperShift upgrade modal dialog
- **CLI Method**: Check available versions: `oc get configmap supported-versions -n hypershift -o yaml | grep -A 10 "versions:"`
- **Expected Results**: Upgrade modal opens showing control plane section with current version and available upgrade options

**Step 4: Configure Control Plane Upgrade** - Select target version for control plane upgrade with compatibility validation
- **UI Method**: Check "Upgrade control plane" checkbox, select target version from dropdown menu
- **CLI Method**: Verify cluster upgrade eligibility: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.spec.release.image}'`
- **Expected Results**: Control plane upgrade option enabled with version dropdown populated and compatibility validation successful

**Step 5: Execute Control Plane Upgrade** - Submit upgrade request and monitor progress through modal interface
- **UI Method**: Click "Upgrade" button to initiate control plane upgrade, observe progress indicators
- **CLI Method**: Monitor upgrade progress: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.status.version}'`
- **Expected Results**: Upgrade initiated successfully with progress tracking displayed in modal

**Step 6: Validate Upgrade Completion** - Confirm control plane upgrade completion and version update
- **UI Method**: Verify upgrade completion in modal progress display and cluster details update
- **CLI Method**: Validate new version: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.status.version.desired}' && oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.status.version.history[0].version}'`
- **Expected Results**: Control plane upgrade completes successfully with version updated in cluster status

### Test Case 2: Node Pool Upgrade Management via HyperShift Modal

**Description**: Validate HyperShift upgrade modal manages AWS node pool upgrades with proper version compatibility and individual node pool selection capabilities.

**Step 1: Log into ACM Console** - Access ACM Console for node pool upgrade testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to HyperShift cluster with multiple node pools for comprehensive testing
- **CLI Method**: List node pools: `oc get nodepools -n clusters --show-labels | grep <cluster-name>`
- **Expected Results**: HyperShift cluster accessible with multiple node pools available for upgrade testing

**Step 2: Access Upgrade Modal for Node Pools** - Open upgrade modal focusing on node pool upgrade capabilities
- **UI Method**: Open cluster upgrade modal and expand node pools section for individual management
- **CLI Method**: Check node pool versions: `oc get nodepools -n clusters -o custom-columns=NAME:.metadata.name,VERSION:.spec.release.image`
- **Expected Results**: Upgrade modal displays node pools section with expandable interface showing individual node pools

**Step 3: Select Node Pools for Upgrade** - Configure individual node pool upgrade selections with version compatibility
- **UI Method**: Check specific node pool checkboxes, select target versions for each node pool
- **CLI Method**: Verify node pool upgrade compatibility: Create test YAML `nodepool-upgrade-test.yaml`:
```yaml
apiVersion: hypershift.openshift.io/v1beta1
kind: NodePool
metadata:
  name: test-nodepool
  namespace: clusters
spec:
  clusterName: test-cluster
  release:
    image: "quay.io/openshift-release-dev/ocp-release:4.14.0-x86_64"
  replicas: 3
  platform:
    aws:
      instanceType: m5.large
```
- **Expected Results**: Node pool selection interface allows individual node pool selection with version compatibility validation

**Step 4: Validate Version Compatibility** - Verify version compatibility between control plane and selected node pool versions
- **UI Method**: Observe compatibility warnings for node pools more than 2 versions behind control plane
- **CLI Method**: Test version compatibility logic: `echo "Control plane: 4.14.0, Node pool: 4.12.0" | awk -F': ' '{cp=$2; np=$4; print (cp > np && (cp - np) <= 0.2) ? "Compatible" : "Incompatible"}'`
- **Expected Results**: Version compatibility validation displays appropriate warnings for unsupported version combinations

**Step 5: Execute Node Pool Upgrades** - Submit node pool upgrade requests with progress monitoring
- **UI Method**: Click "Upgrade" to initiate selected node pool upgrades, monitor individual progress
- **CLI Method**: Monitor node pool upgrade: `oc patch nodepool <nodepool-name> -n clusters --type merge -p '{"spec":{"release":{"image":"<new-image>"}}}'`
- **Expected Results**: Node pool upgrades initiated with individual progress tracking for each selected node pool

**Step 6: Verify Node Pool Upgrade Status** - Confirm node pool upgrade completion and status updates
- **UI Method**: Validate upgrade completion status for all selected node pools in modal interface
- **CLI Method**: Check upgrade status: `oc get nodepools -n clusters -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[0].type,VERSION:.spec.release.image`
- **Expected Results**: All selected node pools upgrade successfully with status reflected in modal and cluster details

### Test Case 3: HyperShift Upgrade Modal Error Handling and Validation

**Description**: Validate HyperShift upgrade modal error handling, validation logic, and recovery scenarios for various upgrade failure conditions.

**Step 1: Log into ACM Console** - Access ACM Console for upgrade error handling testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Access HyperShift cluster for comprehensive error scenario testing
- **CLI Method**: Prepare error testing environment: `oc get hostedcluster -n clusters | grep -E "(Failed|Progressing)"`
- **Expected Results**: HyperShift cluster accessible for error handling and validation testing scenarios

**Step 2: Test Version Compatibility Validation** - Trigger version compatibility errors to validate modal error handling
- **UI Method**: Attempt to select incompatible version combinations (node pool > control plane + 2 versions)
- **CLI Method**: Test invalid version scenario conceptually: `echo "Testing: Node pool 4.15.0 with Control plane 4.12.0 should trigger validation error"`
- **Expected Results**: Modal displays version compatibility error messages preventing invalid upgrade configurations

**Step 3: Test Missing Supported Versions** - Validate modal behavior when supported-versions ConfigMap is unavailable
- **UI Method**: Observe modal behavior when version information is unavailable or incomplete
- **CLI Method**: Simulate missing versions: `oc get configmap supported-versions -n hypershift || echo "ConfigMap not found - testing error scenario"`
- **Expected Results**: Modal handles missing version information gracefully with appropriate error messaging

**Step 4: Test Network Connectivity Issues** - Validate modal error handling during network failures or API timeouts
- **UI Method**: Simulate network issues during upgrade submission and observe error handling
- **CLI Method**: Test API connectivity: `oc get hostedcluster <cluster-name> -n clusters --request-timeout=1s || echo "Testing timeout scenario"`
- **Expected Results**: Modal provides appropriate error messages for network connectivity issues with retry options

**Step 5: Test Upgrade Progress Monitoring** - Validate progress tracking and error reporting during upgrade execution
- **UI Method**: Monitor upgrade progress indicators and error states in modal interface
- **CLI Method**: Check upgrade status and conditions: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.status.conditions[?(@.type=="Progressing")]}'`
- **Expected Results**: Modal provides real-time progress updates and handles upgrade failures with clear error reporting

**Step 6: Test Error Recovery and Retry** - Validate error recovery mechanisms and retry functionality
- **UI Method**: Test retry functionality for failed upgrades and error recovery workflows
- **CLI Method**: Verify cluster recovery state: `oc get hostedcluster <cluster-name> -n clusters -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'`
- **Expected Results**: Modal provides retry mechanisms for recoverable errors and clear guidance for resolution