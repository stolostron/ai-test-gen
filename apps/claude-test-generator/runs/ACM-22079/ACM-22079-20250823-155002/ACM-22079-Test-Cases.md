# Test Cases for ACM-22079: ClusterCurator Digest-Based Non-Recommended Upgrades

## Test Case 1: Validate ClusterCurator digest-based non-recommended upgrade workflow

### Description
Validate that ClusterCurator can perform cluster upgrades using image digests when the non-recommended annotation is enabled, specifically testing the digest lookup functionality in conditionalUpdates and the complete upgrade workflow.

### Setup
- Access to ACM Console with ClusterCurator capabilities enabled
- Target managed cluster available for upgrade testing
- Appropriate RBAC permissions for ClusterCurator operations
- OpenShift cluster with conditional updates available

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> | oc login https://api.<cluster-host>:6443 --username=<username> --password=<password> | Successful authentication and access to ACM Console |
| 2 | Navigate to cluster upgrade automation | ACM Console → Clusters → Cluster sets → target cluster → Actions → Upgrade cluster | oc get managedclusters | Display available managed clusters and cluster set information |
| 3 | Create ClusterCurator with non-recommended annotation | Create automation template with digest-based upgrade configuration | Create and apply ClusterCurator YAML: `touch clustercurator-digest.yaml` and add:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: digest-upgrade-test<br>  namespace: target-cluster<br>  annotations:<br>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate: "4.16.37"<br>    monitorTimeout: 120<br>```<br><br>`oc apply -f clustercurator-digest.yaml` | ClusterCurator resource created successfully with non-recommended annotation, upgrade configuration shows digest lookup capability |
| 4 | Verify ClusterCurator resource creation | Console → Automation → View ClusterCurator details | `oc get clustercurator digest-upgrade-test -n target-cluster -o yaml` | ClusterCurator shows status "Active" with proper annotation and upgrade specification |
| 5 | Monitor upgrade job initialization | Console → Jobs → View curator job progress | `oc get jobs -n target-cluster | grep curator` | Curator job starts successfully and begins conditional updates lookup for image digest |
| 6 | Validate digest lookup functionality | Console → Events → Filter by ClusterCurator events | `oc get events -n target-cluster --field-selector involvedObject.kind=ClusterCurator` | Events show successful digest lookup from conditionalUpdates list or fallback mechanism activation |
| 7 | Verify upgrade progress monitoring | Console → Clusters → target cluster → Upgrade status | `oc get clusterversion -o yaml | grep -A 10 conditionalUpdates` | Upgrade progresses using image digest, cluster version shows proper digest reference in update process |
| 8 | Confirm upgrade completion | Console → Clusters → target cluster → Version information | `oc get managedcluster target-cluster -o yaml | grep version` | Cluster successfully upgraded to target version using digest-based approach, version reflects updated state |

## Test Case 2: Verify ClusterCurator image lookup fallback strategy and error handling

### Description
Test the ClusterCurator fallback strategy that searches conditionalUpdates first, then availableUpdates, and finally uses image tag fallback for backward compatibility when digest-based lookup fails.

### Setup
- Access to ACM Console with ClusterCurator capabilities enabled
- Target managed cluster with limited conditional updates
- Test environment where digest lookup may encounter fallback scenarios
- Monitoring capabilities for ClusterCurator job logs

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> | oc login https://api.<cluster-host>:6443 --username=<username> --password=<password> | Successful authentication and access to ClusterCurator functionality |
| 2 | Create ClusterCurator for fallback testing | Console → Automation → Create new automation template | Create ClusterCurator with version not in conditionalUpdates: `touch clustercurator-fallback.yaml` and add:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: fallback-test<br>  namespace: target-cluster<br>  annotations:<br>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate: "4.16.38"<br>    monitorTimeout: 120<br>```<br><br>`oc apply -f clustercurator-fallback.yaml` | ClusterCurator created with version that may not be in conditionalUpdates list |
| 3 | Monitor initial digest lookup attempt | Console → Jobs → View curator job logs | `oc logs -n target-cluster -l job-name=curator-job-fallback-test -f` | Job logs show attempt to find image digest in conditionalUpdates list |
| 4 | Verify fallback to availableUpdates | Console → Events → ClusterCurator events | `oc get events -n target-cluster --field-selector involvedObject.name=fallback-test` | Events indicate fallback to availableUpdates list when conditionalUpdates search fails |
| 5 | Test image tag fallback behavior | Console → Automation → Review job execution details | `oc describe clustercurator fallback-test -n target-cluster` | ClusterCurator shows fallback to image tag approach when digest lookup fails in both lists |
| 6 | Validate error handling for invalid versions | Console → Automation → View error messages | `oc get clustercurator fallback-test -n target-cluster -o jsonpath='{.status.conditions}'` | Proper error handling displays when version is not available in any lookup method |
| 7 | Verify backward compatibility | Console → Compare with standard upgrade workflow | Create standard ClusterCurator without annotation: `oc create -f - <<EOF<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: standard-upgrade<br>  namespace: target-cluster<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate: "4.16.35"<br>EOF` | Standard upgrade without annotation works normally using traditional image tag approach |
| 8 | Compare behavior between approaches | Console → Jobs → Compare job execution patterns | `oc get jobs -n target-cluster | grep curator` | Both digest-based and traditional approaches complete successfully with appropriate methods |

## Test Case 3: Test ClusterCurator backward compatibility with standard upgrade workflows

### Description
Ensure that existing ClusterCurator upgrade workflows continue to function normally when the digest-based feature is available but not activated through annotations, maintaining full backward compatibility.

### Setup
- Access to ACM Console with ClusterCurator capabilities
- Target managed cluster configured for standard upgrade testing
- Existing automation templates and upgrade configurations
- Ability to compare upgrade methods side-by-side

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> | oc login https://api.<cluster-host>:6443 --username=<username> --password=<password> | Successful authentication and access to cluster management features |
| 2 | Create standard ClusterCurator without digest annotation | Console → Automation → Create automation template | Create traditional ClusterCurator: `touch clustercurator-standard.yaml` and add:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: standard-upgrade-test<br>  namespace: target-cluster<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate: "4.16.36"<br>    monitorTimeout: 120<br>```<br><br>`oc apply -f clustercurator-standard.yaml` | ClusterCurator created without non-recommended annotation, follows traditional upgrade path |
| 3 | Verify standard upgrade behavior | Console → Jobs → Monitor curator job execution | `oc get clustercurator standard-upgrade-test -n target-cluster -o yaml` | Standard upgrade proceeds using image tag method without digest lookup |
| 4 | Monitor upgrade execution | Console → Clusters → View upgrade progress | `oc logs -n target-cluster -l job-name=curator-job-standard-upgrade-test` | Upgrade logs show traditional image tag resolution without digest lookup attempts |
| 5 | Create ClusterCurator with digest annotation for comparison | Console → Automation → Create second automation template | Create digest-enabled ClusterCurator: `touch clustercurator-digest-compare.yaml` and add:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: digest-compare-test<br>  namespace: target-cluster<br>  annotations:<br>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br>spec:<br>  desiredCuration: upgrade<br>  cluster: target-cluster<br>  upgrade:<br>    desiredUpdate: "4.16.36"<br>    monitorTimeout: 120<br>```<br><br>`oc apply -f clustercurator-digest-compare.yaml` | ClusterCurator with digest annotation created for behavior comparison |
| 6 | Compare execution methods | Console → Jobs → Compare both curator jobs | `oc get jobs -n target-cluster | grep curator | head -2` | Two different execution approaches visible: standard tag-based and digest-based lookup |
| 7 | Validate both approaches reach same result | Console → Clusters → Compare final cluster versions | `oc get clusterversion -o yaml | grep 'version\|image'` | Both upgrade methods successfully reach target version with appropriate image references |
| 8 | Verify no regression in standard functionality | Console → Automation → Review standard workflow integrity | `oc describe clustercurator standard-upgrade-test -n target-cluster` | Standard ClusterCurator functionality remains unaffected by presence of digest feature code |