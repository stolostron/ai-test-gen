# ACM-22079: Support Digest-Based Upgrades via ClusterCurator - Test Cases

**Test Environment:** qe6-vmware-ibm  
**OpenShift Version:** 4.19.6  
**Test Focus:** Digest-based upgrades for non-recommended versions  

---

## Test Case 1: Basic Digest-Based Upgrade Validation

**Description:** Verify that ClusterCurator uses image digest instead of image tag when performing non-recommended upgrades.

**Setup:**
1. Login to OpenShift cluster
2. Identify non-recommended upgrade version
3. Create test namespace for ClusterCurator

| Step | Expected Result |
|------|----------------|
| `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 -u kubeadmin -p password --insecure-skip-tls-verify` | Login successful. |
| `oc get clusterversion version -o jsonpath='{.status.desired.version}'` | 4.19.6 |
| `oc create namespace test-digest-upgrade` | namespace/test-digest-upgrade created |
| `oc project test-digest-upgrade` | Now using project "test-digest-upgrade" on server "https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443". |

---

## Test Case 2: ClusterCurator Digest Upgrade Configuration

**Description:** Create and apply ClusterCurator with non-recommended version to verify digest-based upgrade mechanism.

**Setup:** Continue from Test Case 1

| Step | Expected Result |
|------|----------------|
| Create ClusterCurator YAML with non-recommended version:<br>`cat > clustercurator-digest-test.yaml << EOF`<br>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br>`kind: ClusterCurator`<br>`metadata:`<br>`  name: digest-upgrade-test`<br>`  namespace: test-digest-upgrade`<br>`spec:`<br>`  upgrade:`<br>`    desiredUpdate: "4.19.5"`<br>`    channel: "stable-4.19"`<br>`EOF` | File created successfully |
| `oc apply -f clustercurator-digest-test.yaml` | clustercurator.cluster.open-cluster-management.io/digest-upgrade-test created |
| `oc get clustercurator digest-upgrade-test -o yaml` | ClusterCurator resource shows spec.upgrade.desiredUpdate: "4.19.5" |
| `oc describe clustercurator digest-upgrade-test` | Shows Status conditions and events related to upgrade processing |

---

## Test Case 3: ClusterVersion Digest Validation

**Description:** Verify that the managed cluster's ClusterVersion resource uses image digest format instead of image tag for the upgrade.

**Setup:** Continue from Test Case 2, wait for ClusterCurator processing

| Step | Expected Result |
|------|----------------|
| Monitor ClusterCurator status:<br>`oc get clustercurator digest-upgrade-test -o jsonpath='{.status.conditions[?(@.type=="upgrade-cluster")].status}'` | "True" (when upgrade begins) |
| Check ClusterVersion resource for digest usage:<br>`oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}'` | Contains image digest format (sha256:...) not tag format |
| Verify image digest format:<br>`oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' \| grep -c "sha256:"` | 1 |
| Validate ClusterVersion status:<br>`oc get clusterversion version -o jsonpath='{.status.conditions[?(@.type=="Progressing")].message}'` | Contains digest-based upgrade information |

---

## Test Case 4: Integration and Cleanup Verification

**Description:** Verify end-to-end integration and perform cleanup validation.

**Setup:** Continue from Test Case 3

| Step | Expected Result |
|------|----------------|
| Monitor upgrade progress:<br>`oc get clusterversion version -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'` | "True" (indicates stable state) |
| Verify ClusterCurator completion:<br>`oc get clustercurator digest-upgrade-test -o jsonpath='{.status.conditions[?(@.type=="clustercurator-job")].status}'` | "True" |
| Check for upgrade-related events:<br>`oc get events --field-selector involvedObject.name=digest-upgrade-test --sort-by='.lastTimestamp'` | Shows ClusterCurator upgrade processing events |
| Cleanup test resources:<br>`oc delete clustercurator digest-upgrade-test`<br>`oc delete namespace test-digest-upgrade` | clustercurator.cluster.open-cluster-management.io "digest-upgrade-test" deleted<br>namespace "test-digest-upgrade" deleted |

---

## Test Case 5: Negative Testing - Tag vs Digest Verification

**Description:** Verify that digest format is specifically used instead of tag format for non-recommended upgrades.

**Setup:** Fresh environment setup

| Step | Expected Result |
|------|----------------|
| `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 -u kubeadmin -p password --insecure-skip-tls-verify` | Login successful. |
| Check current ClusterVersion image format:<br>`oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' \| head -c 20` | Shows beginning of image reference |
| Verify NOT using tag format (should not end with version tag):<br>`oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' \| grep -v ":4.19"`| Image reference without version tag |
| Confirm digest format presence:<br>`oc get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}' \| grep "sha256"` | Contains sha256 digest identifier |

---

## 🎯 Test Execution Notes

1. **Version Selection:** Use appropriate non-recommended version based on current cluster version
2. **Monitoring:** Allow sufficient time for ClusterCurator processing
3. **Validation Focus:** Primary verification is digest vs tag format in ClusterVersion resource
4. **Safety:** Tests can be run safely as they focus on validation rather than actual upgrade completion

## ✅ Success Criteria

- ClusterCurator processes non-recommended upgrade request
- ClusterVersion.spec.desiredUpdate.image contains digest format (sha256:...)
- No image tag format (version number) in ClusterVersion resource
- All ClusterCurator status conditions show successful processing