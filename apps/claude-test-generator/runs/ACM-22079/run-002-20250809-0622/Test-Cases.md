# Test Cases - ACM-22079: Digest-Based Upgrades via ClusterCurator

## Test Case 1: Basic Digest-Based Non-Recommended Upgrade

**Business Value**: Validates core functionality for disconnected enterprise environments  
**Technical Scope**: ClusterCurator with digest-based upgrade to non-recommended OCP version  
**Risk Level**: High - Core feature functionality  

**Prerequisites**: 
- ACM Hub cluster with cluster-curator-controller deployed
- At least one managed cluster available for upgrade testing
- Access to non-recommended OCP version with known image digest

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Identify current OCP version on managed cluster<br/>**Goal**: Establish baseline for upgrade testing<br/>**Command**: `oc get clusterversion -o jsonpath='{.items[0].status.desired.version}'` | Current version displayed (e.g., "4.16.36"). Record this as the starting version for upgrade validation. |
| **Step 2**: Identify available non-recommended upgrade target<br/>**Goal**: Find a valid non-recommended version with known digest<br/>**Command**: `oc get clusterversion -o jsonpath='{.items[0].status.conditionalUpdates[*].release.version}'` | List of available non-recommended versions displayed. Select one for testing (e.g., "4.16.37"). |
| **Step 3**: Create ClusterCurator resource with non-recommended version<br/>**Goal**: Configure digest-based upgrade via ClusterCurator<br/>Apply YAML:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: digest-upgrade-test<br/>  namespace: managed-cluster-ns<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    channel: "stable-4.16"<br/>    desiredUpdate: "4.16.37"<br/>  clusterName: target-managed-cluster<br/>``` | ClusterCurator resource created successfully. Status shows "Pending" or "InProgress" for upgrade curation. |
| **Step 4**: Verify ClusterCurator processes the upgrade request<br/>**Goal**: Confirm upgrade workflow initiated<br/>**Command**: `oc get clustercurator digest-upgrade-test -o jsonpath='{.status.conditions[?(@.type=="UpgradeStarted")].status}'` | UpgradeStarted condition shows "True". ClusterCurator begins processing the non-recommended upgrade. |
| **Step 5**: Monitor managed cluster ClusterVersion for digest usage<br/>**Goal**: Validate digest-based upgrade implementation<br/>**Command**: `oc get clusterversion --context=managed-cluster -o jsonpath='{.items[0].spec.desiredUpdate.image}'` | ClusterVersion spec shows image digest format (e.g., "quay.io/openshift-release-dev/ocp-release@sha256:abc123...") instead of tag format. |
| **Step 6**: Verify upgrade completion and cluster health<br/>**Goal**: Confirm successful digest-based upgrade<br/>**Commands**:<br/>• `oc get clusterversion --context=managed-cluster -o jsonpath='{.items[0].status.history[0].version}'`<br/>• `oc get nodes --context=managed-cluster` | Cluster successfully upgraded to target version "4.16.37". All nodes show "Ready" status. ClusterVersion history reflects successful upgrade. |
| **Step 7**: Validate ClusterCurator completion status<br/>**Goal**: Confirm ClusterCurator workflow completed successfully<br/>**Command**: `oc get clustercurator digest-upgrade-test -o jsonpath='{.status.conditions[?(@.type=="UpgradeComplete")].status}'` | UpgradeComplete condition shows "True". ClusterCurator status indicates successful completion of digest-based upgrade. |

---

## Test Case 2: Digest Resolution and Fallback Validation

**Business Value**: Ensures robust upgrade behavior with proper fallback mechanisms  
**Technical Scope**: Digest lookup logic and backward compatibility testing  
**Risk Level**: Medium - Fallback and error handling validation  

**Prerequisites**: 
- ACM Hub cluster with multiple managed clusters available
- Access to both recommended and non-recommended OCP versions
- Understanding of current cluster upgrade paths

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Create ClusterCurator with non-recommended version (digest lookup)<br/>**Goal**: Test primary digest resolution path<br/>Apply YAML:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: digest-primary-test<br/>  namespace: managed-cluster-ns<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.16.37"<br/>  clusterName: target-cluster-1<br/>``` | ClusterCurator successfully resolves digest from conditionalUpdates list. Upgrade proceeds with digest-based image reference. |
| **Step 2**: Create ClusterCurator with recommended version (fallback test)<br/>**Goal**: Validate fallback to availableUpdates when conditionalUpdates empty<br/>Apply YAML:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: digest-fallback-test<br/>  namespace: managed-cluster-ns<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.16.38"<br/>  clusterName: target-cluster-2<br/>``` | ClusterCurator falls back to availableUpdates list. Upgrade proceeds with appropriate image reference from available updates. |
| **Step 3**: Monitor cluster-curator-controller logs for digest resolution<br/>**Goal**: Verify correct digest lookup logic execution<br/>**Command**: `oc logs deployment/cluster-curator-controller -n ocm -f \| grep -i digest` | Logs show digest resolution attempts: "Looking up digest for version X in conditionalUpdates" followed by successful resolution or fallback messages. |
| **Step 4**: Compare image references between digest and tag-based upgrades<br/>**Goal**: Validate different image reference formats<br/>**Commands**:<br/>• `oc get clusterversion --context=cluster-1 -o jsonpath='{.spec.desiredUpdate.image}'`<br/>• `oc get clusterversion --context=cluster-2 -o jsonpath='{.spec.desiredUpdate.image}'` | Cluster-1 shows digest format: "registry/path@sha256:hash". Cluster-2 may show tag format or digest based on availableUpdates content. Clear difference in image reference strategy. |
| **Step 5**: Verify both upgrades complete successfully<br/>**Goal**: Confirm fallback mechanism doesn't impact upgrade success<br/>**Commands**:<br/>• `oc get clustercurator digest-primary-test -o jsonpath='{.status.conditions}'`<br/>• `oc get clustercurator digest-fallback-test -o jsonpath='{.status.conditions}'` | Both ClusterCurator resources show successful completion. Upgrade conditions indicate "UpgradeComplete: True" for both digest and fallback scenarios. |

---

## Test Case 3: Error Handling and Invalid Digest Scenarios

**Business Value**: Validates system resilience and error recovery for production environments  
**Technical Scope**: Error handling for invalid versions and digest resolution failures  
**Risk Level**: Medium - System reliability under error conditions  

**Prerequisites**: 
- ACM Hub cluster with cluster-curator-controller
- Test managed cluster that can handle failed upgrade attempts
- Knowledge of invalid or unavailable OCP versions

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Create ClusterCurator with invalid version<br/>**Goal**: Test error handling for non-existent versions<br/>Apply YAML:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: invalid-version-test<br/>  namespace: managed-cluster-ns<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.99.99"<br/>  clusterName: test-managed-cluster<br/>``` | ClusterCurator created but upgrade fails gracefully. Status conditions show appropriate error message about version not found. |
| **Step 2**: Monitor ClusterCurator status for error conditions<br/>**Goal**: Verify proper error reporting and status tracking<br/>**Command**: `oc get clustercurator invalid-version-test -o jsonpath='{.status.conditions[?(@.type=="Failed")]}' \| jq .` | Failed condition present with descriptive message: "Version 4.99.99 not found in available or conditional updates". Reason indicates digest resolution failure. |
| **Step 3**: Verify managed cluster remains stable during failed upgrade<br/>**Goal**: Ensure failed digest lookup doesn't impact cluster stability<br/>**Commands**:<br/>• `oc get clusterversion --context=test-cluster -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'`<br/>• `oc get nodes --context=test-cluster --no-headers \| wc -l` | ClusterVersion Available condition remains "True". All cluster nodes maintain "Ready" status. No impact on cluster stability from failed upgrade attempt. |
| **Step 4**: Test recovery with valid version after failure<br/>**Goal**: Validate system recovery from previous error state<br/>**Command**: `oc patch clustercurator invalid-version-test --type='merge' -p '{"spec":{"upgrade":{"desiredUpdate":"4.16.37"}}}'` | ClusterCurator updates successfully. System recovers from error state and processes valid version upgrade request. |
| **Step 5**: Verify successful recovery and upgrade completion<br/>**Goal**: Confirm system resilience and proper error recovery<br/>**Commands**:<br/>• `oc get clustercurator invalid-version-test -o jsonpath='{.status.conditions[?(@.type=="UpgradeComplete")].status}'`<br/>• `oc get clusterversion --context=test-cluster -o jsonpath='{.status.desired.version}'` | UpgradeComplete condition shows "True". Managed cluster successfully upgraded to valid version "4.16.37". Error state cleared and normal operation restored. |

---

## Test Case 4: Disconnected Environment Simulation

**Business Value**: Validates functionality in customer-like disconnected environments  
**Technical Scope**: Digest resolution with limited registry connectivity  
**Risk Level**: High - Customer environment simulation  

**Prerequisites**: 
- ACM Hub cluster with network policy capability
- Ability to simulate registry connectivity restrictions
- Managed cluster suitable for connectivity testing

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Baseline connectivity test with full registry access<br/>**Goal**: Establish working baseline before simulating restrictions<br/>Create and apply ClusterCurator:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: baseline-connectivity-test<br/>  namespace: managed-cluster-ns<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.16.37"<br/>  clusterName: connectivity-test-cluster<br/>``` | ClusterCurator processes successfully with full registry connectivity. Digest resolution works normally, upgrade proceeds as expected. |
| **Step 2**: Simulate limited registry connectivity<br/>**Goal**: Test digest resolution under connectivity constraints<br/>**Network Policy**: Apply network restrictions to simulate disconnected environment:<br/>```yaml<br/>apiVersion: networking.k8s.io/v1<br/>kind: NetworkPolicy<br/>metadata:<br/>  name: restrict-registry-access<br/>  namespace: ocm<br/>spec:<br/>  podSelector:<br/>    matchLabels:<br/>      app: cluster-curator-controller<br/>  policyTypes:<br/>  - Egress<br/>  egress:<br/>  - to: []<br/>    ports:<br/>    - protocol: TCP<br/>      port: 443<br/>``` | Network policy applied successfully. Registry access limited for cluster-curator-controller pods. Simulates disconnected environment conditions. |
| **Step 3**: Create ClusterCurator under restricted connectivity<br/>**Goal**: Validate digest-based upgrade functionality with limited connectivity<br/>Apply similar ClusterCurator with different name and target. | ClusterCurator creation succeeds. System adapts to connectivity restrictions while maintaining digest-based upgrade capability. |
| **Step 4**: Monitor upgrade progress under connectivity constraints<br/>**Goal**: Verify robust operation in disconnected-like conditions<br/>**Commands**:<br/>• `oc logs deployment/cluster-curator-controller -n ocm \| grep -E "(digest\|connectivity\|registry)"`<br/>• `oc get clustercurator -o wide` | Logs show adaptation to connectivity constraints. ClusterCurator continues processing with available digest information. Graceful handling of limited connectivity. |
| **Step 5**: Remove connectivity restrictions and verify completion<br/>**Goal**: Confirm upgrade completion when connectivity restored<br/>**Command**: `oc delete networkpolicy restrict-registry-access -n ocm` | Network policy removed successfully. ClusterCurator completes upgrade process. Demonstrates resilience to temporary connectivity issues. |
| **Step 6**: Validate final upgrade state and cluster health<br/>**Goal**: Ensure successful completion despite connectivity challenges<br/>**Commands**:<br/>• `oc get clustercurator -o jsonpath='{.items[*].status.conditions[?(@.type=="UpgradeComplete")].status}'`<br/>• `oc get clusterversion --context=connectivity-test-cluster -o jsonpath='{.status.desired.version}'` | All ClusterCurator resources show "UpgradeComplete: True". Managed cluster reflects successful upgrade to target version. System resilient to connectivity variations. |

---

## Test Case 5: Backward Compatibility and Tag-Based Upgrades

**Business Value**: Ensures existing customer workflows remain unimpacted  
**Technical Scope**: Compatibility testing with traditional tag-based upgrade patterns  
**Risk Level**: Medium - Backward compatibility validation  

**Prerequisites**: 
- ACM Hub cluster with both old and new ClusterCurator functionality
- Managed clusters suitable for testing different upgrade approaches
- Understanding of legacy upgrade workflows

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Create traditional ClusterCurator without digest annotations<br/>**Goal**: Test backward compatibility with existing upgrade patterns<br/>Apply YAML:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: traditional-upgrade-test<br/>  namespace: managed-cluster-ns<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    channel: "stable-4.16"<br/>    desiredUpdate: "4.16.37"<br/>  clusterName: traditional-test-cluster<br/>``` | ClusterCurator created successfully. System maintains backward compatibility with traditional upgrade specifications. |
| **Step 2**: Monitor upgrade execution for traditional approach<br/>**Goal**: Verify legacy upgrade logic still functions correctly<br/>**Commands**:<br/>• `oc get clustercurator traditional-upgrade-test -o jsonpath='{.status.conditions}'`<br/>• `oc logs deployment/cluster-curator-controller -n ocm -f \| grep "traditional-upgrade-test"` | Upgrade processes using traditional logic path. Logs indicate normal upgrade workflow without digest-specific processing. |
| **Step 3**: Compare with digest-enabled ClusterCurator<br/>**Goal**: Validate both approaches work simultaneously<br/>Create parallel digest-enabled resource:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: digest-enabled-test<br/>  namespace: managed-cluster-ns<br/>  annotations:<br/>    cluster.open-cluster-management.io/digest-source: "conditionalUpdates"<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.16.37"<br/>  clusterName: digest-test-cluster<br/>``` | Both ClusterCurator resources process simultaneously. Traditional and digest-based approaches operate without interference. |
| **Step 4**: Verify different image reference handling<br/>**Goal**: Confirm appropriate image reference format for each approach<br/>**Commands**:<br/>• `oc get clusterversion --context=traditional-cluster -o jsonpath='{.spec.desiredUpdate.image}'`<br/>• `oc get clusterversion --context=digest-cluster -o jsonpath='{.spec.desiredUpdate.image}'` | Traditional cluster uses standard image references. Digest-enabled cluster uses sha256 digest format. Clear differentiation between approaches. |
| **Step 5**: Validate both upgrades complete successfully<br/>**Goal**: Ensure backward compatibility doesn't compromise functionality<br/>**Commands**:<br/>• `oc get clustercurator traditional-upgrade-test -o jsonpath='{.status.conditions[?(@.type=="UpgradeComplete")].status}'`<br/>• `oc get clustercurator digest-enabled-test -o jsonpath='{.status.conditions[?(@.type=="UpgradeComplete")].status}'` | Both ClusterCurator resources complete successfully. Traditional and digest-based upgrades achieve same end result with different implementation approaches. |

---

## Test Case 6: Multi-Cluster Digest Upgrade Orchestration

**Business Value**: Validates enterprise-scale upgrade coordination using digest-based approach  
**Technical Scope**: Coordinated digest-based upgrades across multiple managed clusters  
**Risk Level**: High - Multi-cluster upgrade coordination  

**Prerequisites**: 
- ACM Hub cluster managing multiple managed clusters
- Access to coordinated upgrade planning and execution
- Clusters at compatible baseline versions for upgrade testing

| Test Steps | Expected Results |
|------------|------------------|
| **Step 1**: Identify multiple managed clusters for coordinated testing<br/>**Goal**: Establish multi-cluster test environment<br/>**Command**: `oc get managedclusters -o jsonpath='{.items[*].metadata.name}' \| tr ' ' '\n' \| head -3` | At least 3 managed clusters available for coordinated upgrade testing. Each cluster accessible and in healthy state. |
| **Step 2**: Create coordinated ClusterCurator resources for digest-based upgrades<br/>**Goal**: Set up simultaneous multi-cluster digest upgrades<br/>Apply multiple YAML resources:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: coordinated-upgrade-cluster-1<br/>  namespace: cluster-1-ns<br/>spec:<br/>  desiredCuration: upgrade<br/>  upgrade:<br/>    desiredUpdate: "4.16.37"<br/>  clusterName: managed-cluster-1<br/>``` | Multiple ClusterCurator resources created successfully. Each configured for digest-based upgrade to same target version across different clusters. |
| **Step 3**: Monitor coordinated upgrade initiation<br/>**Goal**: Verify simultaneous upgrade start across multiple clusters<br/>**Command**: `oc get clustercurator -A --no-headers \| grep "coordinated-upgrade" \| awk '{print $2, $4}'` | All coordinated ClusterCurator resources show "InProgress" status. Multi-cluster upgrade coordination begins simultaneously. |
| **Step 4**: Track digest resolution across clusters<br/>**Goal**: Validate consistent digest usage across all managed clusters<br/>**Command**: `for cluster in cluster-1 cluster-2 cluster-3; do echo "=== $cluster ==="; oc get clusterversion --context=$cluster -o jsonpath='{.spec.desiredUpdate.image}'; echo; done` | All managed clusters show identical digest-based image references. Consistent digest resolution ensures uniform upgrade targets across clusters. |
| **Step 5**: Monitor upgrade progress and coordination<br/>**Goal**: Track multi-cluster upgrade execution and timing<br/>**Commands**:<br/>• `oc get clustercurator -A -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[?(@.type=="UpgradeComplete")].status`<br/>• `watch "oc get managedclusters -o jsonpath='{.items[*].status.conditions[?(@.type==\"ManagedClusterConditionAvailable\")].status}'"` | Coordinated upgrade progress across clusters. All managed clusters maintain "Available" status during upgrade process. Upgrade completion occurs within reasonable time window. |
| **Step 6**: Verify successful coordinated completion<br/>**Goal**: Confirm all clusters reach target state with digest-based upgrades<br/>**Commands**:<br/>• `oc get clustercurator -A --no-headers \| grep "coordinated-upgrade" \| awk '{print $2, $4}'`<br/>• `for cluster in cluster-1 cluster-2 cluster-3; do oc get clusterversion --context=$cluster -o jsonpath='{.status.desired.version}'; echo; done` | All ClusterCurator resources show "Succeeded" status. All managed clusters successfully upgraded to target version "4.16.37". Coordinated digest-based upgrade execution completed successfully. |