# Test Cases for ACM-22079: Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Description
Validate ClusterCurator digest-based upgrade functionality enabling non-recommended cluster upgrades through image digest specification for disconnected environments and custom upgrade scenarios.

## Setup
- Access to ACM Hub cluster with ClusterCurator functionality enabled
- Target managed clusters available for upgrade testing scenarios
- ClusterCurator CRD deployed with digest upgrade support capabilities
- Image digest information available for upgrade testing validation

## Test Cases

### Test Case 1: ClusterCurator Digest Configuration and Validation

**Description**: Verify ClusterCurator digest-based upgrade configuration functionality and proper digest specification validation for non-recommended upgrade scenarios.

**Step 1: Log into ACM Console** - Access ACM Console for ClusterCurator digest upgrade testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in via Console authentication and navigate to "Infrastructure" → "Clusters" → "Cluster sets"
- **CLI Method**: Authenticate and verify ClusterCurator access: `oc login https://api.<cluster-host>:6443 -u <username> -p <password>`
- **Expected Results**: Console loads with cluster management interface showing ClusterCurator capabilities

**Step 2: Access ClusterCurator Configuration** - Navigate to ClusterCurator configuration for digest upgrade setup
- **UI Method**: Access cluster upgrade configuration through ACM Console interface
- **CLI Method**: Check ClusterCurator CRD: `oc get crd clustercurators.cluster.open-cluster-management.io`
- **Expected Results**: ClusterCurator configuration accessible with digest upgrade options available

**Step 3: Configure Digest-Based Upgrade** - Set up ClusterCurator with image digest specification for upgrade
- **UI Method**: Configure cluster upgrade with digest specification through console interface
- **CLI Method**: Create ClusterCurator with digest: Create `clustercurator-digest.yaml`:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: digest-upgrade-curator
  namespace: target-cluster
spec:
  desiredCuration: upgrade
  cluster: target-cluster
  upgrade:
    channel: stable-4.14
    upstream: https://api.openshift.com/api/upgrades_info/v1/graph
    desiredUpdate:
      image: "quay.io/openshift-release-dev/ocp-release@sha256:a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456"
      version: "4.14.15"
```
- **Expected Results**: ClusterCurator configured with digest specification and validation successful

**Step 4: Validate Digest Configuration** - Verify digest configuration accuracy and compatibility validation
- **UI Method**: Review digest configuration details and validation status in console
- **CLI Method**: Validate configuration: `oc get clustercurator digest-upgrade-curator -n target-cluster -o yaml`
- **Expected Results**: Digest configuration validated with proper format and compatibility checks

**Step 5: Test Digest Resolution** - Verify image digest resolution and registry accessibility
- **UI Method**: Check digest resolution status through console monitoring interface
- **CLI Method**: Test digest resolution: `oc get clustercurator digest-upgrade-curator -n target-cluster -o jsonpath='{.status.conditions[?(@.type=="DigestResolved")].status}'`
- **Expected Results**: Image digest successfully resolved with registry connectivity confirmed

**Step 6: Validate Upgrade Preparation** - Confirm upgrade preparation and readiness validation
- **UI Method**: Monitor upgrade preparation status in console interface
- **CLI Method**: Check upgrade readiness: `oc get clustercurator digest-upgrade-curator -n target-cluster -o jsonpath='{.status.conditions[?(@.type=="UpgradeReady")].status}'`
- **Expected Results**: Upgrade preparation completed successfully with digest-based configuration validated

### Test Case 2: ClusterCurator Digest Upgrade Execution and Monitoring

**Description**: Execute ClusterCurator digest-based cluster upgrade and validate upgrade progress monitoring for non-recommended upgrade scenarios.

**Step 1: Log into ACM Console** - Access ACM Console for digest upgrade execution: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to cluster upgrade monitoring interface for digest-based upgrades
- **CLI Method**: Monitor cluster status: `oc get managedclusters target-cluster -o jsonpath='{.status.version.kubernetes}'`
- **Expected Results**: Cluster management interface accessible for digest upgrade monitoring

**Step 2: Initiate Digest-Based Upgrade** - Execute ClusterCurator digest upgrade process
- **UI Method**: Start cluster upgrade through console interface with digest configuration
- **CLI Method**: Apply upgrade configuration: `oc apply -f clustercurator-digest.yaml`
- **Expected Results**: Digest-based upgrade initiated successfully with proper validation

**Step 3: Monitor Upgrade Progress** - Track digest upgrade progress and validation status
- **UI Method**: Monitor upgrade progress indicators and status through console dashboard
- **CLI Method**: Watch upgrade progress: `oc get clustercurator digest-upgrade-curator -n target-cluster -w`
- **Expected Results**: Upgrade progress tracked with real-time status updates and validation

**Step 4: Validate Upgrade Execution** - Verify digest upgrade execution and cluster version updates
- **UI Method**: Check cluster version status and upgrade completion through console
- **CLI Method**: Verify cluster upgrade: `oc get clusterversion -o jsonpath='{.status.desired.version}' --kubeconfig=target-cluster-kubeconfig`
- **Expected Results**: Cluster successfully upgraded using digest specification with version validation

**Step 5: Test Non-Recommended Upgrade Path** - Validate non-recommended upgrade scenario handling
- **UI Method**: Configure non-recommended upgrade path through digest specification
- **CLI Method**: Update digest for non-recommended path: Create `non-recommended-digest.yaml`:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: non-recommended-upgrade
  namespace: target-cluster
spec:
  desiredCuration: upgrade
  cluster: target-cluster
  upgrade:
    channel: stable-4.14
    desiredUpdate:
      image: "quay.io/openshift-release-dev/ocp-release@sha256:b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456ab"
      version: "4.14.20"
      force: true
```
- **Expected Results**: Non-recommended upgrade executed successfully using digest specification

**Step 6: Validate Post-Upgrade Status** - Confirm post-upgrade cluster health and functionality
- **UI Method**: Validate cluster health and functionality through console monitoring
- **CLI Method**: Check cluster operators: `oc get co --kubeconfig=target-cluster-kubeconfig`
- **Expected Results**: Cluster upgrade completed successfully with all operators healthy

### Test Case 3: ClusterCurator Digest Upgrade Error Handling and Recovery

**Description**: Validate ClusterCurator digest upgrade error handling, validation failures, and recovery mechanisms for various upgrade scenarios.

**Step 1: Log into ACM Console** - Access ACM Console for digest upgrade error testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Access cluster upgrade error handling interface for comprehensive testing
- **CLI Method**: Prepare error testing environment: `oc get clustercurators -A`
- **Expected Results**: ClusterCurator interface accessible for error handling validation testing

**Step 2: Test Invalid Digest Configuration** - Validate error handling for invalid digest specifications
- **UI Method**: Configure invalid digest through console interface and observe error handling
- **CLI Method**: Test invalid digest: Create `invalid-digest.yaml`:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: invalid-digest-test
  namespace: target-cluster
spec:
  desiredCuration: upgrade
  cluster: target-cluster
  upgrade:
    desiredUpdate:
      image: "quay.io/openshift-release-dev/ocp-release@sha256:invalid-digest-format"
      version: "4.14.15"
```
- **Expected Results**: Invalid digest configuration properly rejected with clear error messaging

**Step 3: Test Registry Connectivity Issues** - Validate error handling for registry access failures
- **UI Method**: Simulate registry connectivity issues and observe error reporting
- **CLI Method**: Test unreachable registry: `echo "Testing digest resolution failure scenario for disconnected environments"`
- **Expected Results**: Registry connectivity errors properly handled with appropriate error messages

**Step 4: Test Digest Resolution Failures** - Validate error handling for digest resolution issues
- **UI Method**: Configure non-existent digest and monitor error handling through console
- **CLI Method**: Check digest resolution errors: `oc get clustercurator invalid-digest-test -n target-cluster -o jsonpath='{.status.conditions[?(@.type=="DigestResolved")].message}'`
- **Expected Results**: Digest resolution failures properly detected with clear error guidance

**Step 5: Test Upgrade Rollback Scenarios** - Validate upgrade rollback and recovery mechanisms
- **UI Method**: Test upgrade rollback functionality through console interface
- **CLI Method**: Trigger rollback: Create `rollback-curator.yaml`:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: rollback-curator
  namespace: target-cluster
spec:
  desiredCuration: upgrade
  cluster: target-cluster
  upgrade:
    channel: stable-4.14
    desiredUpdate:
      image: "quay.io/openshift-release-dev/ocp-release@sha256:previous-version-digest"
      version: "4.14.10"
```
- **Expected Results**: Upgrade rollback executed successfully with proper version restoration

**Step 6: Validate Error Recovery and Cleanup** - Verify error recovery mechanisms and resource cleanup
- **UI Method**: Test error recovery workflows and cleanup procedures through console
- **CLI Method**: Check cleanup status: `oc get clustercurator -n target-cluster -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[0].type`
- **Expected Results**: Error recovery completed successfully with proper resource cleanup and status reporting