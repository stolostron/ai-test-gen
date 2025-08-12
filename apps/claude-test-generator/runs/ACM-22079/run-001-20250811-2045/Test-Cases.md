# Test Cases - ACM-22079: Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Test Case 1: Verify ClusterCurator uses digest for non-recommended upgrades with annotation

**Description:** Test that ClusterCurator selects image digest from conditionalUpdates when the non-recommended annotation is present and upgrades to a non-recommended version.

**Setup:** 
- Managed cluster with OpenShift version that has available non-recommended updates
- ClusterCurator resource with upgrade-allow-not-recommended-versions annotation set to 'true'
- Target version that exists in the conditionalUpdates list of the managed cluster's ClusterVersion

**Test Steps:**

| Step | Expected Result |
|------|-----------------|
| `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successful login to hub cluster |
| Create namespace for test cluster: `oc create namespace test-cluster-digest` | Namespace test-cluster-digest created |
| Create ClusterCurator with non-recommended annotation:<br/>`cat <<EOF \| oc apply -f -`<br/>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br/>`kind: ClusterCurator`<br/>`metadata:`<br/>`  annotations:`<br/>`    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`<br/>`  name: test-cluster-digest`<br/>`  namespace: test-cluster-digest`<br/>`spec:`<br/>`  desiredCuration: upgrade`<br/>`  upgrade:`<br/>`    desiredUpdate: "4.16.37"`<br/>`    monitorTimeout: 120`<br/>`EOF` | ClusterCurator created successfully with annotation. Output should show: `clustercurator.cluster.open-cluster-management.io/test-cluster-digest created` |
| Verify ClusterCurator contains the annotation: `oc get clustercurator test-cluster-digest -n test-cluster-digest -o yaml \| grep -A1 annotations` | Annotation present in output:<br/>```<br/>annotations:<br/>  cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"<br/>``` |
| Check managed cluster's ClusterVersion conditionalUpdates for the target version: `oc get clusterversion version -o yaml \| grep -A10 conditionalUpdates` | ConditionalUpdates list contains entries with version 4.16.37 and associated image digests like: `image: quay.io/openshift-release-dev/ocp-release@sha256:abc123...` |
| Monitor ClusterCurator job creation: `oc get jobs -n test-cluster-digest` | ClusterCurator job created with name like: `curator-job-test-cluster-digest-xxxxx` |
| Verify the managed cluster's ClusterVersion spec.desiredUpdate uses digest format: `oc get clusterversion version -o yaml \| grep -A3 "desiredUpdate"` | DesiredUpdate shows digest format:<br/>```<br/>desiredUpdate:<br/>  image: quay.io/openshift-release-dev/ocp-release@sha256:abc123...<br/>  version: "4.16.37"<br/>``` |
| Check ClusterCurator status for upgrade progress: `oc get clustercurator test-cluster-digest -n test-cluster-digest -o yaml \| grep -A5 status` | Status shows upgrade in progress or completed with appropriate phase information |

## Test Case 2: Verify fallback behavior when conditionalUpdates doesn't contain target version

**Description:** Test that ClusterCurator falls back to availableUpdates then to image tag when the target version is not found in conditionalUpdates.

**Setup:**
- Managed cluster with limited conditionalUpdates list
- ClusterCurator targeting a version not in conditionalUpdates but potentially in availableUpdates
- Non-recommended annotation enabled

**Test Steps:**

| Step | Expected Result |
|------|-----------------|
| `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successful login to hub cluster |
| Create namespace: `oc create namespace test-fallback-digest` | Namespace test-fallback-digest created |
| Check managed cluster's available updates: `oc get clusterversion version -o yaml \| grep -A20 availableUpdates` | Shows list of available updates with version and image information |
| Create ClusterCurator targeting version in availableUpdates but not conditionalUpdates:<br/>`cat <<EOF \| oc apply -f -`<br/>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br/>`kind: ClusterCurator`<br/>`metadata:`<br/>`  annotations:`<br/>`    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`<br/>`  name: test-fallback-digest`<br/>`  namespace: test-fallback-digest`<br/>`spec:`<br/>`  desiredCuration: upgrade`<br/>`  upgrade:`<br/>`    desiredUpdate: "4.16.38"`<br/>`    monitorTimeout: 120`<br/>`EOF` | ClusterCurator created successfully. Output: `clustercurator.cluster.open-cluster-management.io/test-fallback-digest created` |
| Monitor curator job logs to see digest selection process: `oc logs -f job/$(oc get jobs -n test-fallback-digest -o name \| head -1) -n test-fallback-digest` | Logs show digest selection logic:<br/>- "Checking conditionalUpdates for version 4.16.38"<br/>- "Version not found in conditionalUpdates, checking availableUpdates"<br/>- "Found digest in availableUpdates" or "Falling back to image tag" |
| Verify the managed cluster's ClusterVersion spec shows appropriate format: `oc get clusterversion version -o yaml \| grep -A3 "desiredUpdate"` | DesiredUpdate uses either digest from availableUpdates or falls back to tag format based on what was found |
| Check ClusterCurator status: `oc get clustercurator test-fallback-digest -n test-fallback-digest -o yaml \| grep -A10 status` | Status reflects successful processing of the fallback logic and upgrade attempt |

## Test Case 3: Verify behavior without non-recommended annotation

**Description:** Test that ClusterCurator behaves normally (uses standard logic) when the non-recommended annotation is not present.

**Setup:**
- Managed cluster ready for upgrade testing
- ClusterCurator without the non-recommended annotation
- Target version for standard upgrade path

**Test Steps:**

| Step | Expected Result |
|------|-----------------|
| `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successful login to hub cluster |
| Create namespace: `oc create namespace test-standard-upgrade` | Namespace test-standard-upgrade created |
| Create ClusterCurator WITHOUT the non-recommended annotation:<br/>`cat <<EOF \| oc apply -f -`<br/>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br/>`kind: ClusterCurator`<br/>`metadata:`<br/>`  name: test-standard-upgrade`<br/>`  namespace: test-standard-upgrade`<br/>`spec:`<br/>`  desiredCuration: upgrade`<br/>`  upgrade:`<br/>`    desiredUpdate: "4.16.36"`<br/>`    monitorTimeout: 120`<br/>`EOF` | ClusterCurator created without annotation. Output: `clustercurator.cluster.open-cluster-management.io/test-standard-upgrade created` |
| Verify no annotation is present: `oc get clustercurator test-standard-upgrade -n test-standard-upgrade -o yaml \| grep -A5 annotations` | No upgrade-allow-not-recommended-versions annotation present, or annotations section is empty |
| Monitor curator job for standard upgrade behavior: `oc get jobs -n test-standard-upgrade` | Standard curator job created without special digest selection logic |
| Check curator job logs for standard processing: `oc logs -f job/$(oc get jobs -n test-standard-upgrade -o name \| head -1) -n test-standard-upgrade` | Logs show standard upgrade processing without mention of conditional/available updates digest checking |
| Verify managed cluster receives standard upgrade format: `oc get clusterversion version -o yaml \| grep -A3 "desiredUpdate"` | Standard upgrade format applied based on normal OpenShift update mechanisms |

## Test Case 4: Verify annotation validation and error handling

**Description:** Test ClusterCurator behavior with invalid annotation values and verify proper error handling for non-existent target versions.

**Setup:**
- Managed cluster environment
- ClusterCurator with various annotation configurations
- Non-existent target version for error testing

**Test Steps:**

| Step | Expected Result |
|------|-----------------|
| `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successful login to hub cluster |
| Create namespace: `oc create namespace test-validation` | Namespace test-validation created |
| Create ClusterCurator with invalid annotation value:<br/>`cat <<EOF \| oc apply -f -`<br/>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br/>`kind: ClusterCurator`<br/>`metadata:`<br/>`  annotations:`<br/>`    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'invalid'`<br/>`  name: test-validation`<br/>`  namespace: test-validation`<br/>`spec:`<br/>`  desiredCuration: upgrade`<br/>`  upgrade:`<br/>`    desiredUpdate: "4.99.99"`<br/>`    monitorTimeout: 120`<br/>`EOF` | ClusterCurator created with invalid annotation. Resource creation succeeds but processing should handle invalid values |
| Monitor curator job for error handling: `oc get jobs -n test-validation` | Curator job created for processing the invalid configuration |
| Check curator job logs for error handling: `oc logs job/$(oc get jobs -n test-validation -o name \| head -1) -n test-validation` | Logs show appropriate error handling:<br/>- "Invalid annotation value 'invalid' for upgrade-allow-not-recommended-versions"<br/>- "Target version 4.99.99 not found in updates lists"<br/>- Error messages with helpful guidance |
| Check ClusterCurator status for error reporting: `oc get clustercurator test-validation -n test-validation -o yaml \| grep -A15 status` | Status contains error information:<br/>```<br/>status:<br/>  conditions:<br/>  - type: "Failed"<br/>    status: "True"<br/>    message: "Target version not found in available updates"<br/>``` |
| Update ClusterCurator with correct annotation: `oc patch clustercurator test-validation -n test-validation --type='merge' -p '{"metadata":{"annotations":{"cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions":"true"}}}'` | Annotation updated successfully. Output: `clustercurator.cluster.open-cluster-management.io/test-validation patched` |
| Verify the correction is applied: `oc get clustercurator test-validation -n test-validation -o yaml \| grep -A2 annotations` | Annotation now shows correct value: `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"` |