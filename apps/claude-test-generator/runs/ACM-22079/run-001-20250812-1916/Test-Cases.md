# Test Cases - ACM-22079: Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Test Case 1: Digest-based upgrade for non-recommended version with annotation

**Description**: Verify that ClusterCurator uses image digest instead of image tag when upgrading to a non-recommended OpenShift version with the required annotation enabled.

**Setup**: 
- Managed cluster with current OpenShift version (e.g., 4.16.36)
- Access to ACM hub cluster with ClusterCurator capabilities
- Non-recommended target version available (e.g., 4.16.37)

**Test Steps**:

| Step | Expected Result |
|------|----------------|
| Log into the ACM hub cluster: `oc login <cluster-url>` | Successfully authenticated to ACM hub cluster |
| Verify managed cluster current version: `oc get managedclusterinfo <cluster-name> -o jsonpath='{.status.version.kubernetes}'` | ```<br>4.16.36<br>``` |
| Create ClusterCurator with non-recommended annotation and version: `oc apply -f -` and paste the YAML:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  annotations:<br>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br>  name: test-cluster<br>  namespace: test-cluster<br>spec:<br>  desiredCuration: upgrade<br>  upgrade:<br>    desiredUpdate: 4.16.37<br>    towerAuthSecret: ansible-secret<br>    prehook: []<br>    posthook: []<br>  monitorTimeout: 120<br>``` | ```<br>clustercurator.cluster.open-cluster-management.io/test-cluster created<br>``` |
| Wait for ClusterCurator job to start and check status: `oc get clustercurator test-cluster -o jsonpath='{.status.conditions[?(@.type=="ClusterUpgradeCompleted")].status}'` | ```<br>False<br>``` (upgrade in progress) |
| Monitor the ClusterCurator job execution: `oc get jobs -n test-cluster \| grep curator` | ```<br>curator-job-test-cluster-xxxxx   1/1     45s     2m<br>``` |
| Check managed cluster ClusterVersion for image digest usage: `oc get clusterversion -o yaml \| grep "image:"` (on managed cluster or via ManagedClusterView) | ```<br>image: quay.io/openshift-release-dev/ocp-release@sha256:abc123def456...<br>``` (digest format, not tag) |
| Verify upgrade completion: `oc get clustercurator test-cluster -o jsonpath='{.status.conditions[?(@.type=="ClusterUpgradeCompleted")].status}'` | ```<br>True<br>``` |
| Confirm final cluster version: `oc get managedclusterinfo test-cluster -o jsonpath='{.status.version.kubernetes}'` | ```<br>4.16.37<br>``` |

## Test Case 2: Verify annotation requirement for non-recommended upgrades

**Description**: Confirm that ClusterCurator fails gracefully when attempting to upgrade to a non-recommended version without the required annotation.

**Setup**:
- Managed cluster with current OpenShift version
- Access to ACM hub cluster
- Non-recommended target version identified

**Test Steps**:

| Step | Expected Result |
|------|----------------|
| Log into the ACM hub cluster: `oc login <cluster-url>` | Successfully authenticated to ACM hub cluster |
| Create ClusterCurator WITHOUT annotation for non-recommended version: `oc apply -f -` and paste the YAML:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  name: test-cluster-no-annotation<br>  namespace: test-cluster<br>spec:<br>  desiredCuration: upgrade<br>  upgrade:<br>    desiredUpdate: 4.16.37<br>    towerAuthSecret: ansible-secret<br>    prehook: []<br>    posthook: []<br>  monitorTimeout: 120<br>``` | ```<br>clustercurator.cluster.open-cluster-management.io/test-cluster-no-annotation created<br>``` |
| Monitor ClusterCurator status for error conditions: `oc get clustercurator test-cluster-no-annotation -o yaml \| grep -A5 conditions` | ```<br>conditions:<br>- type: ClusterUpgradeCompleted<br>  status: False<br>  reason: UpgradeNotAllowed<br>  message: "Non-recommended version upgrade requires annotation"<br>``` |
| Verify no upgrade occurs on managed cluster: `oc get managedclusterinfo test-cluster -o jsonpath='{.status.version.kubernetes}'` | ```<br>4.16.36<br>``` (unchanged) |
| Check that no curator job was created: `oc get jobs -n test-cluster \| grep curator \| grep no-annotation` | ```<br>No resources found<br>``` |

## Test Case 3: Image tag fallback when digest not available

**Description**: Verify that ClusterCurator falls back to image tag when image digest is not found in conditional updates list, even with annotation present.

**Setup**:
- Managed cluster with current version
- Access to ACM hub cluster
- Target version with limited conditional update support

**Test Steps**:

| Step | Expected Result |
|------|----------------|
| Log into the ACM hub cluster: `oc login <cluster-url>` | Successfully authenticated to ACM hub cluster |
| Check available conditional updates for current cluster: `oc get clusterversion -o jsonpath='{.status.conditionalUpdates[*].release.version}'` (on managed cluster via ManagedClusterView) | ```<br>4.16.37 4.16.38 4.17.0<br>``` |
| Create ClusterCurator with annotation for version not in conditional updates: `oc apply -f -` and paste the YAML:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  annotations:<br>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br>  name: test-cluster-fallback<br>  namespace: test-cluster<br>spec:<br>  desiredCuration: upgrade<br>  upgrade:<br>    desiredUpdate: 4.16.39<br>    towerAuthSecret: ansible-secret<br>    prehook: []<br>    posthook: []<br>  monitorTimeout: 120<br>``` | ```<br>clustercurator.cluster.open-cluster-management.io/test-cluster-fallback created<br>``` |
| Monitor ClusterCurator execution: `oc get clustercurator test-cluster-fallback -o jsonpath='{.status.conditions[?(@.type=="ClusterUpgradeCompleted")].status}'` | ```<br>False<br>``` (upgrade in progress) |
| Verify managed cluster uses image tag format: `oc get clusterversion -o yaml \| grep "image:"` (on managed cluster) | ```<br>image: quay.io/openshift-release-dev/ocp-release:4.16.39-x86_64<br>``` (tag format, not digest) |
| Check upgrade completion: `oc get clustercurator test-cluster-fallback -o jsonpath='{.status.conditions[?(@.type=="ClusterUpgradeCompleted")].status}'` | ```<br>True<br>``` |

## Test Case 4: End-to-end workflow validation with pre/post hooks

**Description**: Validate complete ClusterCurator workflow with digest-based upgrade including pre and post-upgrade hooks.

**Setup**:
- Managed cluster ready for upgrade
- Ansible Tower/AAP credentials configured
- Pre and post-upgrade automation tasks defined

**Test Steps**:

| Step | Expected Result |
|------|----------------|
| Log into the ACM hub cluster: `oc login <cluster-url>` | Successfully authenticated to ACM hub cluster |
| Create Ansible secret for ClusterCurator: `oc create secret generic ansible-secret --from-literal=host=<tower-host> --from-literal=token=<tower-token> -n test-cluster` | ```<br>secret/ansible-secret created<br>``` |
| Create comprehensive ClusterCurator with hooks: `oc apply -f -` and paste the YAML:<br><br>```yaml<br>apiVersion: cluster.open-cluster-management.io/v1beta1<br>kind: ClusterCurator<br>metadata:<br>  annotations:<br>    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'<br>  name: test-cluster-complete<br>  namespace: test-cluster<br>spec:<br>  desiredCuration: upgrade<br>  upgrade:<br>    desiredUpdate: 4.16.37<br>    towerAuthSecret: ansible-secret<br>    prehook:<br>    - name: pre-upgrade-backup<br>      extra_vars:<br>        cluster_name: test-cluster<br>    posthook:<br>    - name: post-upgrade-validation<br>      extra_vars:<br>        expected_version: 4.16.37<br>  monitorTimeout: 180<br>``` | ```<br>clustercurator.cluster.open-cluster-management.io/test-cluster-complete created<br>``` |
| Monitor pre-hook execution: `oc get jobs -n test-cluster \| grep prehook` | ```<br>prehook-test-cluster-complete-xxxxx   1/1     30s     1m<br>``` |
| Verify upgrade phase with digest usage: `oc get clusterversion -o yaml \| grep "image:"` (on managed cluster) | ```<br>image: quay.io/openshift-release-dev/ocp-release@sha256:def789abc123...<br>``` |
| Monitor post-hook execution: `oc get jobs -n test-cluster \| grep posthook` | ```<br>posthook-test-cluster-complete-xxxxx   1/1     45s     2m<br>``` |
| Verify complete workflow success: `oc get clustercurator test-cluster-complete -o jsonpath='{.status.conditions[?(@.type=="ClusterUpgradeCompleted")].message}'` | ```<br>"Cluster upgrade completed successfully with digest-based image"<br>``` |
| Confirm final cluster state: `oc get managedclusterinfo test-cluster -o jsonpath='{.status.version.kubernetes}'` | ```<br>4.16.37<br>``` |