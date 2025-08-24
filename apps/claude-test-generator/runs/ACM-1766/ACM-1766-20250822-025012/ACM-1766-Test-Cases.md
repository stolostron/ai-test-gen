# Test Cases for ACM-1766: Upgrade hypershift operator to 4.12

## Description
Validate HyperShift operator upgrade to OpenShift 4.12 compatibility with MCE 2.2 integration ensuring proper operator functionality and hosted cluster management capabilities.

## Setup
- Access to ACM Hub cluster with HyperShift operator deployed and MCE 2.2 integration
- OpenShift 4.12 compatibility requirements and upgrade procedures available
- ACM Console with HyperShift operator management interface accessible
- Test hosted clusters for operator functionality validation

## Test Cases

### Test Case 1: HyperShift Operator Version Validation and Upgrade Preparation

**Description**: Verify current HyperShift operator version and validate upgrade readiness to OpenShift 4.12 compatibility with MCE 2.2 integration.

**Step 1: Log into ACM Console** - Access ACM Console for HyperShift operator upgrade testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in via Console authentication and navigate to "Operators" → "Installed Operators"
- **CLI Method**: Authenticate and verify HyperShift operator: `oc login https://api.<cluster-host>:6443 -u <username> -p <password>`
- **Expected Results**: Console loads with operators page showing HyperShift operator installation status

**Step 2: Check Current HyperShift Operator Version** - Validate current operator version and deployment status
- **UI Method**: Navigate to HyperShift operator details to check current version and status
- **CLI Method**: Check operator version: `oc get csv -n hypershift | grep hypershift`
- **Expected Results**: Current HyperShift operator version displayed with deployment status information

**Step 3: Validate MCE 2.2 Integration Status** - Verify MCE 2.2 compatibility and integration readiness
- **UI Method**: Check MCE integration status in operator configuration interface
- **CLI Method**: Verify MCE components: `oc get multiclusterengine -A -o custom-columns=NAME:.metadata.name,VERSION:.status.currentVersion`
- **Expected Results**: MCE 2.2 integration verified with compatibility status confirmed

**Step 4: Review Upgrade Requirements** - Validate upgrade prerequisites and compatibility requirements
- **UI Method**: Review operator upgrade documentation and requirements in console
- **CLI Method**: Check upgrade compatibility: `oc get nodes --show-labels | grep "node.openshift.io/os_id"`
- **Expected Results**: Upgrade requirements validated with OpenShift 4.12 compatibility confirmed

**Step 5: Prepare Upgrade Environment** - Configure environment for HyperShift operator upgrade process
- **UI Method**: Access operator upgrade configuration through console interface
- **CLI Method**: Prepare upgrade configuration: Create `hypershift-upgrade-config.yaml`:
```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: hypershift-operator
  namespace: hypershift
spec:
  channel: "4.12"
  name: hypershift-operator
  source: community-operators
  sourceNamespace: openshift-marketplace
  installPlanApproval: Manual
```
- **Expected Results**: Upgrade environment prepared with proper configuration for OpenShift 4.12 compatibility

**Step 6: Validate Pre-Upgrade Hosted Clusters** - Verify existing hosted cluster status before operator upgrade
- **UI Method**: Check hosted cluster status in ACM console before upgrade
- **CLI Method**: List hosted clusters: `oc get hostedclusters -A -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[0].status,VERSION:.spec.release.image`
- **Expected Results**: All hosted clusters validated as healthy before operator upgrade process

### Test Case 2: HyperShift Operator Upgrade Execution and MCE Integration

**Description**: Execute HyperShift operator upgrade to OpenShift 4.12 compatibility and validate MCE 2.2 integration functionality.

**Step 1: Log into ACM Console** - Access ACM Console for operator upgrade execution: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to HyperShift operator management for upgrade execution
- **CLI Method**: Verify upgrade readiness: `oc get installplan -n hypershift`
- **Expected Results**: HyperShift operator accessible for upgrade execution with proper permissions

**Step 2: Execute Operator Upgrade** - Initiate HyperShift operator upgrade to OpenShift 4.12 compatibility
- **UI Method**: Trigger operator upgrade through console interface with manual approval
- **CLI Method**: Apply upgrade configuration: `oc apply -f hypershift-upgrade-config.yaml`
- **Expected Results**: Operator upgrade initiated with proper upgrade process tracking

**Step 3: Monitor Upgrade Progress** - Track operator upgrade progress and validation status
- **UI Method**: Monitor upgrade progress indicators in operator management interface
- **CLI Method**: Monitor upgrade status: `oc get csv -n hypershift -w`
- **Expected Results**: Upgrade progress tracked with status updates and completion indicators

**Step 4: Validate Post-Upgrade Operator Status** - Verify operator upgrade completion and functionality
- **UI Method**: Check upgraded operator status and version in console interface
- **CLI Method**: Verify new version: `oc get csv -n hypershift -o custom-columns=NAME:.metadata.name,VERSION:.spec.version,PHASE:.status.phase`
- **Expected Results**: HyperShift operator successfully upgraded to OpenShift 4.12 compatibility

**Step 5: Test MCE 2.2 Integration** - Validate MCE 2.2 integration functionality after operator upgrade
- **UI Method**: Test MCE integration through ACM console interface
- **CLI Method**: Verify MCE integration: `oc get multiclusterengine -A -o jsonpath='{.items[0].status.conditions[?(@.type=="Available")].status}'`
- **Expected Results**: MCE 2.2 integration fully functional with upgraded HyperShift operator

**Step 6: Validate Operator Configuration** - Confirm operator configuration and settings after upgrade
- **UI Method**: Review operator configuration settings in console interface
- **CLI Method**: Check operator configuration: `oc get deployment hypershift-operator -n hypershift -o yaml | grep -A 5 "image:"`
- **Expected Results**: Operator configuration validated with proper OpenShift 4.12 compatibility settings

### Test Case 3: Post-Upgrade Hosted Cluster Functionality Validation

**Description**: Validate hosted cluster management functionality and operations after HyperShift operator upgrade to ensure compatibility and performance.

**Step 1: Log into ACM Console** - Access ACM Console for post-upgrade validation: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Access hosted cluster management interface for functionality testing
- **CLI Method**: List hosted clusters: `oc get hostedclusters -A`
- **Expected Results**: Hosted cluster management interface accessible with upgraded operator

**Step 2: Test Existing Hosted Cluster Management** - Validate existing hosted cluster operations after upgrade
- **UI Method**: Access existing hosted cluster details and management options
- **CLI Method**: Check cluster status: `oc get hostedcluster <cluster-name> -n <namespace> -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'`
- **Expected Results**: Existing hosted clusters fully manageable with upgraded operator functionality

**Step 3: Test New Hosted Cluster Creation** - Validate new hosted cluster creation capability with upgraded operator
- **UI Method**: Test hosted cluster creation wizard with upgraded operator
- **CLI Method**: Create test hosted cluster: Create `test-hosted-cluster.yaml`:
```yaml
apiVersion: hypershift.openshift.io/v1beta1
kind: HostedCluster
metadata:
  name: test-upgrade-cluster
  namespace: clusters
spec:
  release:
    image: "quay.io/openshift-release-dev/ocp-release:4.12.0-x86_64"
  pullSecret:
    name: pullsecret-cluster
  platform:
    type: AWS
    aws:
      region: us-east-1
      cloudProvider:
        zone: us-east-1a
```
- **Expected Results**: New hosted cluster creation successful with OpenShift 4.12 compatibility

**Step 4: Validate Hosted Cluster Operations** - Test hosted cluster scaling and management operations
- **UI Method**: Test hosted cluster scaling and configuration changes through console
- **CLI Method**: Scale cluster nodes: `oc patch nodepool <nodepool-name> -n <namespace> --type merge -p '{"spec":{"replicas":3}}'`
- **Expected Results**: Hosted cluster operations fully functional with proper scaling and management

**Step 5: Test MCE Integration with Hosted Clusters** - Validate MCE 2.2 integration with hosted cluster management
- **UI Method**: Test MCE features through hosted cluster management interface
- **CLI Method**: Check MCE cluster registration: `oc get managedclusters | grep <hosted-cluster-name>`
- **Expected Results**: MCE integration working properly with hosted cluster management functionality

**Step 6: Validate Performance and Stability** - Verify upgraded operator performance and stability metrics
- **UI Method**: Monitor operator performance metrics through console dashboards
- **CLI Method**: Check operator resource usage: `oc top pods -n hypershift --sort-by=memory`
- **Expected Results**: Upgraded operator performing optimally with stable resource utilization and proper functionality