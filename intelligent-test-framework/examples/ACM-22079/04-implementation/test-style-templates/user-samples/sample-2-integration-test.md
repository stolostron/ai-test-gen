# Test Case: ACM-CLC-INT-002 - ClusterCurator Digest-Based Upgrade Integration

## 📝 Test Metadata
| Field | Value |
|-------|-------|
| **Test ID** | ACM-CLC-INT-002 |
| **Title** | End-to-End Digest-Based Cluster Upgrade via ClusterCurator |
| **Priority** | **HIGH** |
| **Component** | ClusterCurator - Integration |
| **Type** | Integration Test |
| **Duration** | 45-60 minutes |
| **JIRA** | ACM-22079 |
| **Dependencies** | Hub cluster, Managed cluster, Registry access |

---

## 🎯 **Test Objective**

Validate the complete integration flow of digest-based cluster upgrades through ClusterCurator, ensuring proper hub-spoke communication, ManagedClusterView/Action coordination, and successful upgrade completion using image digests instead of tags.

---

## 🛠️ **Prerequisites**

### Environment Setup
- [x] **Hub Cluster**: ACM 2.9+ deployed and operational
- [x] **Managed Cluster**: OpenShift 4.5.8 cluster imported and managed
- [x] **Network**: Hub-spoke connectivity established  
- [x] **Permissions**: ClusterCurator RBAC configured
- [x] **Registry**: Access to OpenShift release registry

### Test Data Configuration  
```yaml
source_version: "4.5.8"
target_version: "4.5.10"  
expected_digest: "sha256:71e158c6173ad6aa6e356c119a87459196bbe70e89c0db1e35c1f63a87d90676"
cluster_name: "integration-test-cluster"
namespace: "integration-test-cluster"
```

### Required Annotations
```yaml
metadata:
  annotations:
    "cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions": "true"
```

---

## 🧪 **Test Execution Steps**

### Phase 1: Setup and Validation
1. **Verify Environment**
   - Confirm hub cluster operational status
   - Validate managed cluster connectivity (`oc get managedclusters`)
   - Check ClusterCurator operator status

2. **Create Test ClusterCurator**
   ```bash
   # Apply ClusterCurator CR with digest-based upgrade configuration
   kubectl apply -f test-clustercurator-digest-upgrade.yaml
   ```

3. **Verify Initial State**
   - Managed cluster shows version 4.5.8
   - No pending upgrades in progress
   - ClusterCurator in "Ready" state

### Phase 2: Digest Discovery Validation  
4. **Trigger Upgrade Process**
   ```bash
   # Patch ClusterCurator to initiate upgrade
   kubectl patch clustercurator integration-test-cluster -p '{"spec":{"desiredCuration":"upgrade"}}'
   ```

5. **Monitor ManagedClusterView Creation**
   - Verify MCV created for target cluster
   - Confirm MCV retrieves ClusterVersion data
   - Validate conditionalUpdates populated

6. **Verify Digest Discovery**
   ```bash
   # Check ClusterCurator logs for digest discovery
   kubectl logs -l app=cluster-curator-controller | grep "Found conditional update image digest"
   ```

### Phase 3: Upgrade Execution
7. **Monitor ManagedClusterAction Creation**
   - Verify MCA created with digest-based image reference
   - Confirm no `force: true` flag when using digest
   - Validate proper ClusterVersion spec update

8. **Track Upgrade Progress**
   ```bash
   # Monitor cluster upgrade status
   watch 'oc --kubeconfig=managed-cluster.kubeconfig get clusterversion version -o yaml | grep -A5 -B5 "image\|version\|progressing"'
   ```

9. **Validate Hub-Spoke Communication**
   - MCA status updates reflected on hub
   - ClusterCurator status shows progress
   - No communication errors in logs

### Phase 4: Completion Verification
10. **Confirm Upgrade Success**
    - Managed cluster reports version 4.5.10
    - Cluster operators all available
    - No degraded conditions present

11. **Verify Digest Usage**
    ```bash
    # Confirm digest was used instead of tag
    oc --kubeconfig=managed-cluster.kubeconfig get clusterversion version -o jsonpath='{.spec.desiredUpdate.image}'
    ```

12. **Validate ClusterCurator Status**
    - ClusterCurator shows "upgrade-complete"
    - Success conditions properly set
    - Appropriate status messages

---

## ✅ **Expected Results**

### 🎯 **Success Criteria**
| Verification Point | Expected Outcome | Validation Method |
|--------------------|------------------|-------------------|
| **Digest Discovery** | Digest extracted from conditionalUpdates | Log analysis + MCA inspection |
| **Image Reference** | Uses `@sha256:...` format, not tag | ClusterVersion spec verification |
| **Force Flag** | No `force: true` when using digest | MCA payload inspection |
| **Upgrade Success** | Cluster upgraded to 4.5.10 | Version verification |
| **Communication** | Hub-spoke coordination works | Status propagation check |
| **Performance** | Upgrade completes within 60 minutes | Duration measurement |

### 🔍 **Detailed Validations**

#### ManagedClusterView Validation
```bash
# Expected MCV structure and data population
kubectl get managedclusterview integration-test-cluster -o yaml
# Should show populated conditionalUpdates with target version
```

#### ManagedClusterAction Validation  
```bash
# Expected MCA with digest-based image
kubectl get managedclusteraction integration-test-cluster -o yaml
# Should show image: "quay.io/openshift-release-dev/ocp-release@sha256:..."
```

#### ClusterVersion Validation
```bash
# Expected cluster state post-upgrade
oc --kubeconfig=managed-cluster.kubeconfig get clusterversion version -o yaml
# Should show completed upgrade with digest-based image
```

---

## 🚨 **Error Scenarios & Handling**

### Scenario 1: Digest Not Found
- **Condition**: Version not in conditionalUpdates or availableUpdates  
- **Expected**: Graceful fallback to tag-based approach with `force: true`
- **Validation**: Check MCA for tag-based image and force flag

### Scenario 2: Network Connectivity Issues
- **Condition**: Hub-spoke communication interrupted
- **Expected**: Appropriate timeout and retry behavior
- **Validation**: Monitor logs for connectivity errors and recovery

### Scenario 3: Permission Denied  
- **Condition**: Insufficient RBAC for ClusterCurator operations
- **Expected**: Clear error messages in ClusterCurator status
- **Validation**: Review status conditions and error descriptions

---

## 🧹 **Cleanup Procedures**

1. **Reset Cluster State** (if needed for retesting)
   ```bash
   # Remove test ClusterCurator
   kubectl delete clustercurator integration-test-cluster
   ```

2. **Verify Resource Cleanup**
   - ManagedClusterView removed
   - ManagedClusterAction completed/removed  
   - No orphaned resources remain

3. **Document Results**
   - Capture final status screenshots
   - Export relevant logs for analysis
   - Update test execution tracking

---

## 📊 **Integration Points Validated**

- ✅ **ClusterCurator ↔ ManagedClusterView**: Cluster state retrieval
- ✅ **ClusterCurator ↔ ManagedClusterAction**: Upgrade execution
- ✅ **Hub ↔ Spoke**: Command propagation and status reporting  
- ✅ **ACM ↔ OpenShift**: Native upgrade mechanism integration
- ✅ **Registry ↔ Cluster**: Image pull using digest reference

---

## 📈 **Success Metrics**

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Discovery Time** | < 5 minutes | MCV creation to digest extraction |
| **Execution Time** | < 60 minutes | MCA creation to upgrade completion |
| **Success Rate** | 100% | Successful completion without errors |
| **Resource Usage** | Minimal impact | Hub cluster resource monitoring |

---

## 🔗 **Related Test Cases**

- **ACM-CLC-001**: Unit test for validateUpgradeVersion function
- **ACM-CLC-003**: Disconnected environment upgrade testing  
- **ACM-CLC-004**: Error handling and recovery scenarios
- **ACM-CLC-005**: Performance and scalability validation

---

*Test Case Version: 1.0 | Created: January 2025 | Next Review: March 2025*