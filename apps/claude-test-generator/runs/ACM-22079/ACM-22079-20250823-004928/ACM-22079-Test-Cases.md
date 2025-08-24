# ClusterCurator Digest-Based Upgrade Test Cases

## Test Case 1: Validate ClusterCurator digest-based upgrade workflow for non-recommended OCP version

**Description**: Validates the core digest-based upgrade functionality for non-recommended OCP versions using ClusterCurator in disconnected environments. This test verifies the primary digest resolution algorithm from conditionalUpdates list and successful upgrade execution.

**Setup**: 
- Access to ACM Console on test environment
- Target cluster available for upgrade testing
- Non-recommended OCP version identified with digest specification
- ClusterCurator CRD available and functional

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.[CLUSTER-HOST] | `oc login https://api.[CLUSTER-HOST]:6443 -u kubeadmin` | Access ACM Console successfully |
| 2 | Navigate to cluster upgrade section | Go to Infrastructure → Clusters → Select target cluster → Actions → Upgrade cluster | `oc get clusters -n [CLUSTER-NAMESPACE]` | Cluster upgrade interface displayed |
| 3 | Create ClusterCurator for digest upgrade | Click Create ClusterCurator → Fill form with digest specification | Create ClusterCurator YAML: `touch clustercurator-digest.yaml` and add:<br/><br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: upgrade-digest-test<br/>  namespace: [CLUSTER-NAMESPACE]<br/>  annotations:<br/>    cluster-curator.open-cluster-management.io/upgrade-cluster.allow-non-recommended: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  cluster: [TARGET-CLUSTER]<br/>  upgrade:<br/>    channel: stable-4.15<br/>    upstream: https://api.openshift.com/api/upgrades_info/v1/graph<br/>    desiredUpdate:<br/>      image: quay.io/openshift-release-dev/ocp-release@sha256:[DIGEST-VALUE]<br/>``` | ClusterCurator resource created with digest specification |
| 4 | Configure upgrade monitoring | Enable upgrade progress tracking in Console | Add monitoring labels: `oc label clustercurator upgrade-digest-test monitor=enabled -n [CLUSTER-NAMESPACE]` | Monitoring configuration applied |
| 5 | Initiate digest-based upgrade | Click Create/Apply to start upgrade process | Apply ClusterCurator configuration: `oc apply -f clustercurator-digest.yaml` | Upgrade job initiated with digest-based image |
| 6 | Monitor upgrade progression | View upgrade status and job details in ACM Console | Check ClusterCurator status: `oc get clustercurator upgrade-digest-test -n [CLUSTER-NAMESPACE] -o yaml` | Upgrade progresses with digest resolution from conditionalUpdates |
| 7 | Validate digest resolution | Verify digest-based image usage in Console logs | Check upgrade job details: `oc describe jobs -n [CLUSTER-NAMESPACE] | grep image` | Digest-based image confirmed in upgrade job |
| 8 | Confirm upgrade completion | Verify cluster version updated in Infrastructure → Clusters | Validate final cluster version: `oc get clusterversion -o jsonpath='{.items[0].status.desired.version}'` | Upgrade completed successfully using digest-based image |

## Test Case 2: Verify digest resolution fallback mechanism from conditionalUpdates to availableUpdates

**Description**: Tests the fallback mechanism when digest is not found in conditionalUpdates list, ensuring graceful degradation to availableUpdates and then to tag-based approach for backward compatibility.

**Setup**:
- Access to ACM Console on test environment  
- Target cluster for upgrade testing
- Digest specification not present in conditionalUpdates list
- ClusterCurator functionality available

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.[CLUSTER-HOST] | `oc login https://api.[CLUSTER-HOST]:6443 -u kubeadmin` | Console access established |
| 2 | Access cluster management | Go to Infrastructure → Clusters → Select target cluster for fallback testing | `oc get clusters -n [CLUSTER-NAMESPACE]` | Target cluster identified for fallback testing |
| 3 | Create ClusterCurator with unavailable digest | Create ClusterCurator with digest not in conditionalUpdates | Create fallback test YAML: `touch clustercurator-fallback.yaml` and add:<br/><br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: fallback-test<br/>  namespace: [CLUSTER-NAMESPACE]<br/>  annotations:<br/>    cluster-curator.open-cluster-management.io/upgrade-cluster.allow-non-recommended: "true"<br/>spec:<br/>  desiredCuration: upgrade<br/>  cluster: [TARGET-CLUSTER]<br/>  upgrade:<br/>    channel: stable-4.15<br/>    upstream: https://api.openshift.com/api/upgrades_info/v1/graph<br/>    desiredUpdate:<br/>      image: quay.io/openshift-release-dev/ocp-release@sha256:unavailable-digest-for-fallback-testing<br/>``` | ClusterCurator created with unavailable digest for fallback testing |
| 4 | Apply fallback configuration | Submit ClusterCurator creation through Console form | Apply fallback test configuration: `oc apply -f clustercurator-fallback.yaml` | Fallback test ClusterCurator resource created |
| 5 | Monitor initial digest resolution | Observe upgrade process status in Console | Check ClusterCurator conditions: `oc get clustercurator fallback-test -n [CLUSTER-NAMESPACE] -o yaml | grep -A 10 conditions` | Initial digest resolution attempt from conditionalUpdates |
| 6 | Verify fallback to availableUpdates | Monitor Console for fallback behavior messages | Watch ClusterCurator status for fallback: `oc get clustercurator fallback-test -n [CLUSTER-NAMESPACE] --watch` | Fallback to availableUpdates list initiated |
| 7 | Validate alternate resolution path | Confirm alternate digest source usage in Console | Check upgrade job for alternate image: `oc describe jobs -n [CLUSTER-NAMESPACE] | grep "image.*digest"` | Alternate digest source from availableUpdates utilized |
| 8 | Confirm fallback upgrade success | Verify upgrade completion despite initial digest unavailability | Validate upgrade completion: `oc get clustercurator fallback-test -n [CLUSTER-NAMESPACE] -o jsonpath='{.status.conditions[?(@.type=="UpgradeComplete")].status}'` | Upgrade successful via fallback mechanism |

## Test Case 3: Test ClusterCurator upgrade completion monitoring with digest-based image specification

**Description**: Validates comprehensive monitoring and validation of ClusterCurator upgrade completion using digest-based image specifications, ensuring proper state transitions and upgrade verification.

**Setup**:
- Access to ACM Console and CLI tools
- Target cluster prepared for upgrade monitoring
- Digest-based upgrade configuration ready
- Monitoring tools and permissions available

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.[CLUSTER-HOST] | `oc login https://api.[CLUSTER-HOST]:6443 -u kubeadmin` | Console access established |
| 2 | Prepare comprehensive monitoring | Navigate to Infrastructure → Clusters → Select cluster for monitoring | Set up monitoring namespace: `oc create namespace upgrade-monitoring --dry-run=client -o yaml | oc apply -f -` | Monitoring environment prepared |
| 3 | Create monitored ClusterCurator | Create ClusterCurator with digest and comprehensive monitoring | Create monitoring ClusterCurator: `touch clustercurator-monitor.yaml` and add:<br/><br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: monitor-upgrade<br/>  namespace: [CLUSTER-NAMESPACE]<br/>  labels:<br/>    monitoring: enabled<br/>    test-type: digest-upgrade<br/>  annotations:<br/>    cluster-curator.open-cluster-management.io/upgrade-cluster.allow-non-recommended: "true"<br/>    cluster-curator.open-cluster-management.io/monitor-timeout: "3600"<br/>spec:<br/>  desiredCuration: upgrade<br/>  cluster: [TARGET-CLUSTER]<br/>  upgrade:<br/>    channel: stable-4.15<br/>    upstream: https://api.openshift.com/api/upgrades_info/v1/graph<br/>    desiredUpdate:<br/>      image: quay.io/openshift-release-dev/ocp-release@sha256:[DIGEST-VALUE]<br/>    monitorTimeout: 3600<br/>``` | Comprehensive monitoring ClusterCurator created |
| 4 | Enable detailed state tracking | Configure detailed monitoring in Console monitoring section | Apply monitoring configuration: `oc apply -f clustercurator-monitor.yaml` | Detailed state tracking enabled |
| 5 | Initiate monitored upgrade | Start upgrade with full monitoring through Console | Monitor upgrade initiation: `oc get clustercurator monitor-upgrade -n [CLUSTER-NAMESPACE] --watch` | Monitored upgrade initiated successfully |
| 6 | Track detailed state transitions | Monitor upgrade phases in real-time through Console | Watch detailed status transitions: `oc get clustercurator monitor-upgrade -n [CLUSTER-NAMESPACE] -o jsonpath='{.status}' | jq` | All upgrade state transitions tracked |
| 7 | Validate digest image usage | Confirm digest-based image used throughout upgrade in Console | Verify digest usage in jobs: `oc get jobs -n [CLUSTER-NAMESPACE] -o yaml | grep -A 5 -B 5 sha256` | Digest-based image confirmed throughout upgrade process |
| 8 | Verify comprehensive completion | Validate final upgrade status and monitoring data in Console | Check complete upgrade status: `oc get clustercurator monitor-upgrade -n [CLUSTER-NAMESPACE] -o jsonpath='{.status.conditions}' | jq 'map(select(.type=="UpgradeComplete" or .type=="MonitoringComplete"))'` | Upgrade and monitoring completed successfully with full validation |