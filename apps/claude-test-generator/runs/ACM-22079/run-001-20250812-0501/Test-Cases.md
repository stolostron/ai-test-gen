# E2E Test Cases for ACM-22079: Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Overview
These test cases validate the digest-based upgrade functionality for non-recommended OpenShift versions using ClusterCurator. The feature enables using image digests from ClusterVersion conditionalUpdates for upgrades that may not be available through standard availableUpdates.

---

## Test Case 1: Basic Non-Recommended Upgrade with Image Digest

**Description:** Verify ClusterCurator can upgrade a managed cluster to a non-recommended OpenShift version using image digest lookup from conditionalUpdates.

**Setup:** 
- Managed cluster running a version with available non-recommended upgrades in conditionalUpdates
- Hub cluster with ClusterCurator capability
- Non-recommended version available in ClusterVersion conditionalUpdates

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully logged into hub cluster |
| 2 | Verify managed cluster current version: `oc get managedcluster <cluster-name> -o jsonpath='{.status.version.kubernetes}'` | Current cluster version displayed (e.g., "v1.29.10+6abe8a2") |
| 3 | Check conditionalUpdates on managed cluster: `oc get managedclusterview <cluster-name>-clusterversion -n <cluster-name> -o yaml` | Verify ClusterVersion resource shows conditionalUpdates with non-recommended versions |
| 4 | Create ClusterCurator with non-recommended annotation:<br>`oc apply -f - <<EOF`<br>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br>`kind: ClusterCurator`<br>`metadata:`<br>&nbsp;&nbsp;`annotations:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`<br>&nbsp;&nbsp;`name: digest-upgrade-test`<br>&nbsp;&nbsp;`namespace: <cluster-name>`<br>`spec:`<br>&nbsp;&nbsp;`desiredCuration: upgrade`<br>&nbsp;&nbsp;`upgrade:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`desiredUpdate: "4.16.37"`<br>&nbsp;&nbsp;`monitorTimeout: 120`<br>&nbsp;&nbsp;`towerAuthSecret: tower-auth`<br>&nbsp;&nbsp;`prehook: {}`<br>&nbsp;&nbsp;`posthook: {}`<br>&nbsp;&nbsp;`install: {}`<br>`EOF` | ClusterCurator created successfully |
| 5 | Monitor ClusterCurator status: `oc get clustercurator digest-upgrade-test -n <cluster-name> -w` | ClusterCurator progresses through upgrade phases |
| 6 | Check upgrade job logs: `oc logs -n <cluster-name> -l job-name=digest-upgrade-test-upgrade-job -f` | Logs show image digest lookup from conditionalUpdates: "Found image digest from conditionalUpdates" |
| 7 | Verify ClusterVersion on managed cluster shows image digest: `oc get managedclusterview <cluster-name>-clusterversion -n <cluster-name> -o jsonpath='{.status.spec.desiredUpdate.image}'` | Shows image digest format: `quay.io/openshift-release-dev/ocp-release@sha256:...` (not tag format) |
| 8 | Wait for upgrade completion: `oc get clustercurator digest-upgrade-test -n <cluster-name> -o jsonpath='{.status.conditions[?(@.type=="upgrade-job")].status}'` | Status shows "True" indicating successful upgrade |
| 9 | Verify final cluster version: `oc get managedcluster <cluster-name> -o jsonpath='{.status.version.kubernetes}'` | Version updated to target version (e.g., "v1.29.12+abcd123") |

**Expected Results:**
- ClusterCurator successfully upgrades managed cluster to non-recommended version
- Image digest (not tag) is used in ClusterVersion.spec.desiredUpdate.image  
- Upgrade logs show digest lookup from conditionalUpdates
- Final cluster version matches the desired non-recommended version

---

## Test Case 2: Fallback to availableUpdates When conditionalUpdates Missing

**Description:** Verify ClusterCurator falls back to availableUpdates when the desired version is not found in conditionalUpdates.

**Setup:**
- Managed cluster with desired version available in availableUpdates but not conditionalUpdates
- Hub cluster with ClusterCurator capability

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully logged into hub cluster |
| 2 | Check available updates: `oc get managedclusterview <cluster-name>-clusterversion -n <cluster-name> -o jsonpath='{.status.availableUpdates[*].version}'` | List available update versions |
| 3 | Create ClusterCurator for version in availableUpdates:<br>`oc apply -f - <<EOF`<br>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br>`kind: ClusterCurator`<br>`metadata:`<br>&nbsp;&nbsp;`annotations:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`<br>&nbsp;&nbsp;`name: fallback-upgrade-test`<br>&nbsp;&nbsp;`namespace: <cluster-name>`<br>`spec:`<br>&nbsp;&nbsp;`desiredCuration: upgrade`<br>&nbsp;&nbsp;`upgrade:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`desiredUpdate: "<available-version>"`<br>&nbsp;&nbsp;`monitorTimeout: 120`<br>&nbsp;&nbsp;`towerAuthSecret: tower-auth`<br>&nbsp;&nbsp;`prehook: {}`<br>&nbsp;&nbsp;`posthook: {}`<br>&nbsp;&nbsp;`install: {}`<br>`EOF` | ClusterCurator created successfully |
| 4 | Monitor upgrade job logs: `oc logs -n <cluster-name> -l job-name=fallback-upgrade-test-upgrade-job -f` | Logs show fallback: "Image digest not found in conditionalUpdates, checking availableUpdates" |
| 5 | Verify image source in logs: `oc logs -n <cluster-name> -l job-name=fallback-upgrade-test-upgrade-job` \| `grep -E "(conditionalUpdates\|availableUpdates\|fallback)"` | Logs indicate source as "availableUpdates" |
| 6 | Check ClusterVersion uses digest: `oc get managedclusterview <cluster-name>-clusterversion -n <cluster-name> -o jsonpath='{.status.spec.desiredUpdate.image}'` | Shows image digest from availableUpdates |

**Expected Results:**
- ClusterCurator successfully falls back to availableUpdates lookup
- Upgrade logs clearly indicate the fallback behavior
- Image digest is still used (from availableUpdates source)
- Upgrade completes successfully

---

## Test Case 3: Backward Compatibility with Image Tag Fallback

**Description:** Verify ClusterCurator maintains backward compatibility by using image tag when digest lookup fails entirely.

**Setup:**
- Scenario where digest lookup fails for both conditionalUpdates and availableUpdates
- Hub cluster with ClusterCurator capability

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully logged into hub cluster |
| 2 | Create ClusterCurator with version not in any updates list:<br>`oc apply -f - <<EOF`<br>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br>`kind: ClusterCurator`<br>`metadata:`<br>&nbsp;&nbsp;`annotations:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`<br>&nbsp;&nbsp;`name: tag-fallback-test`<br>&nbsp;&nbsp;`namespace: <cluster-name>`<br>`spec:`<br>&nbsp;&nbsp;`desiredCuration: upgrade`<br>&nbsp;&nbsp;`upgrade:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`desiredUpdate: "4.16.40"`<br>&nbsp;&nbsp;`monitorTimeout: 120`<br>&nbsp;&nbsp;`towerAuthSecret: tower-auth`<br>&nbsp;&nbsp;`prehook: {}`<br>&nbsp;&nbsp;`posthook: {}`<br>&nbsp;&nbsp;`install: {}`<br>`EOF` | ClusterCurator created successfully |
| 3 | Check upgrade job logs for fallback behavior: `oc logs -n <cluster-name> -l job-name=tag-fallback-test-upgrade-job -f` | Logs show: "Image digest not found, using tag format for backward compatibility" |
| 4 | Verify ClusterVersion uses image tag format: `oc get managedclusterview <cluster-name>-clusterversion -n <cluster-name> -o jsonpath='{.status.spec.desiredUpdate.image}'` | Shows tag format: `quay.io/openshift-release-dev/ocp-release:4.16.40-x86_64` (not digest) |
| 5 | Monitor upgrade status: `oc get clustercurator tag-fallback-test -n <cluster-name> -o jsonpath='{.status.conditions[?(@.type=="upgrade-job")].message}'` | Status message indicates processing with tag format |

**Expected Results:**
- ClusterCurator gracefully falls back to image tag when digest lookup fails
- Upgrade logs clearly document the fallback to tag format
- Backward compatibility is maintained for scenarios where digest is unavailable
- Upgrade proceeds with tag-based image reference

---

## Test Case 4: Annotation Requirement Validation

**Description:** Verify the non-recommended upgrade annotation is required for digest-based upgrades to work properly.

**Setup:**
- Managed cluster requiring non-recommended upgrade
- Hub cluster with ClusterCurator capability

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully logged into hub cluster |
| 2 | Create ClusterCurator WITHOUT the non-recommended annotation:<br>`oc apply -f - <<EOF`<br>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br>`kind: ClusterCurator`<br>`metadata:`<br>&nbsp;&nbsp;`name: no-annotation-test`<br>&nbsp;&nbsp;`namespace: <cluster-name>`<br>`spec:`<br>&nbsp;&nbsp;`desiredCuration: upgrade`<br>&nbsp;&nbsp;`upgrade:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`desiredUpdate: "4.16.37"`<br>&nbsp;&nbsp;`monitorTimeout: 120`<br>&nbsp;&nbsp;`towerAuthSecret: tower-auth`<br>&nbsp;&nbsp;`prehook: {}`<br>&nbsp;&nbsp;`posthook: {}`<br>&nbsp;&nbsp;`install: {}`<br>`EOF` | ClusterCurator created successfully |
| 3 | Monitor upgrade behavior: `oc get clustercurator no-annotation-test -n <cluster-name> -w` | ClusterCurator proceeds with standard upgrade logic |
| 4 | Check upgrade job logs: `oc logs -n <cluster-name> -l job-name=no-annotation-test-upgrade-job -f` | Logs show standard upgrade process without digest lookup from conditionalUpdates |
| 5 | Verify annotation controls digest lookup: `oc logs -n <cluster-name> -l job-name=no-annotation-test-upgrade-job` \| `grep -i "conditionalUpdates"` | No conditionalUpdates lookup performed without annotation |
| 6 | Compare with annotated ClusterCurator (from Test Case 1) logs: `oc logs -n <cluster-name> -l job-name=digest-upgrade-test-upgrade-job` \| `grep -i "conditionalUpdates"` | Shows conditionalUpdates lookup when annotation present |

**Expected Results:**
- ClusterCurator without annotation skips conditionalUpdates lookup
- Standard upgrade logic is used without the annotation
- Annotation requirement is properly enforced
- Digest-based lookup only occurs when annotation is present

---

## Test Case 5: Error Handling for Invalid Version

**Description:** Verify ClusterCurator handles invalid or non-existent version gracefully with appropriate error messages.

**Setup:**
- Hub cluster with ClusterCurator capability
- Invalid version specified for upgrade

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify` | Successfully logged into hub cluster |
| 2 | Create ClusterCurator with invalid version:<br>`oc apply -f - <<EOF`<br>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br>`kind: ClusterCurator`<br>`metadata:`<br>&nbsp;&nbsp;`annotations:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`<br>&nbsp;&nbsp;`name: invalid-version-test`<br>&nbsp;&nbsp;`namespace: <cluster-name>`<br>`spec:`<br>&nbsp;&nbsp;`desiredCuration: upgrade`<br>&nbsp;&nbsp;`upgrade:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`desiredUpdate: "4.99.99"`<br>&nbsp;&nbsp;`monitorTimeout: 120`<br>&nbsp;&nbsp;`towerAuthSecret: tower-auth`<br>&nbsp;&nbsp;`prehook: {}`<br>&nbsp;&nbsp;`posthook: {}`<br>&nbsp;&nbsp;`install: {}`<br>`EOF` | ClusterCurator created successfully |
| 3 | Monitor upgrade job status: `oc get clustercurator invalid-version-test -n <cluster-name> -o jsonpath='{.status.conditions[?(@.type=="upgrade-job")].status}'` | Status shows "False" indicating failure |
| 4 | Check error message: `oc get clustercurator invalid-version-test -n <cluster-name> -o jsonpath='{.status.conditions[?(@.type=="upgrade-job")].message}'` | Clear error message about invalid version |
| 5 | Verify upgrade job logs: `oc logs -n <cluster-name> -l job-name=invalid-version-test-upgrade-job` | Logs show proper error handling: "Version 4.99.99 not found in conditionalUpdates or availableUpdates" |
| 6 | Check ClusterVersion remains unchanged: `oc get managedcluster <cluster-name> -o jsonpath='{.status.version.kubernetes}'` | Original version unchanged |

**Expected Results:**
- ClusterCurator properly handles invalid version requests
- Clear error messages are provided in status conditions
- Upgrade job fails gracefully with informative logs
- Cluster version remains unchanged after failed upgrade attempt