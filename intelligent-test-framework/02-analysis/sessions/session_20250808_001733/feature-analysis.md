# Comprehensive Analysis of ACM-22079: ClusterCurator Digest Upgrades

## 1. Complete Feature Context

### Business Drivers and Customer Use Cases
Based on the comprehensive research, ACM-22079 addresses critical customer needs in enterprise environments:

**Disconnected/Air-Gapped Environments:**
- Customers with strict security requirements who cannot connect to external registries
- Mirror registries that require digest-based image references for reliable content verification
- Compliance environments where image integrity validation is mandatory

**Non-Recommended Upgrade Paths:**
- Early access to candidate releases for testing and validation
- Emergency patches that may not follow standard upgrade paths  
- Version skipping scenarios for specific customer requirements
- Developer/QE environments needing access to nightly builds

**Enterprise Reliability:**
- Digest-based upgrades provide cryptographic verification of image content
- Eliminates risks of tag mutations in registry environments
- Ensures consistent upgrades across multiple clusters

### ACM Architecture Integration
The feature integrates deeply with ACM's multi-cluster management architecture:

**Hub-Spoke Communication:**
- `ManagedClusterView` resources query spoke cluster state
- `ManagedClusterAction` resources execute upgrade commands
- ClusterCurator controller orchestrates the entire workflow

**Component Dependencies:**
- OpenShift ClusterVersion operator on spoke clusters
- Hive ClusterDeployment for cluster provisioning
- ACM ManagedCluster lifecycle integration
- Container image registry connectivity

## 2. Implementation Analysis

### Core Algorithm (hive.go:697-833)
The digest discovery implementation follows a sophisticated priority hierarchy:

```go
// Priority 1: conditionalUpdates (preferred for non-recommended versions)
if clusterConditionalUpdates, ok := clusterVersion["status"].(map[string]interface{})["conditionalUpdates"]; ok {
    for _, conditionalUpdate := range clusterConditionalUpdates.([]interface{}) {
        updateVersion := conditionalUpdate.(map[string]interface{})["release"].(map[string]interface{})["version"].(string)
        if updateVersion == desiredUpdate {
            imageWithDigest = conditionalUpdate.(map[string]interface{})["release"].(map[string]interface{})["image"].(string)
            break
        }
    }
}

// Priority 2: availableUpdates (fallback for standard versions)
if imageWithDigest == "" {
    if clusterAvailableUpdates, ok := clusterVersion["status"].(map[string]interface{})["availableUpdates"]; ok {
        for _, availableUpdate := range clusterAvailableUpdates.([]interface{}) {
            updateVersion := availableUpdate.(map[string]interface{})["version"].(string)
            if updateVersion == desiredUpdate {
                imageWithDigest = availableUpdate.(map[string]interface{})["image"].(string)
                break
            }
        }
    }
}
```

### Smart Image Reference Selection (hive.go:1006-1030)
The implementation intelligently chooses between digest and tag-based approaches:

**With Digest Found:**
```go
if imageWithDigest != "" {
    cvDesiredUpdate.(map[string]interface{})["image"] = imageWithDigest
    // Note: No "force": true needed when using digest
}
```

**Fallback to Tag-Based:**
```go
else {
    cvDesiredUpdate.(map[string]interface{})["force"] = true
    cvDesiredUpdate.(map[string]interface{})["image"] = 
        "quay.io/openshift-release-dev/ocp-release:" + desiredUpdate + "-multi"
}
```

### Security and Validation Features
**Activation Mechanism:**
- Only activated when `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"`
- Prevents accidental use of non-recommended upgrade paths
- Maintains backward compatibility for standard upgrades

**Error Handling:**
- Graceful fallback to tag-based approach if digest not found
- Comprehensive validation of cluster vendor and version compatibility
- Retry mechanism with configurable backoff limits

## 3. Exhaustive Test Strategy

### Unit Test Coverage Analysis
The existing test suite (hive_test.go:1673-1914) provides excellent coverage:

**Test Case 1: Digest from conditionalUpdates**
```go
func TestUpgradeClusterForceUpgradeWithImageDigest(t *testing.T) {
    // Tests primary path: digest discovery from conditionalUpdates array
    ConditionalUpdates: []clusterversionv1.ConditionalUpdate{
        {
            Release: clusterversionv1.Release{
                Image:   "quay.io/openshift-release-dev/ocp-release@sha256:71e158c6173ad6aa6e356c119a87459196bbe70e89c0db1e35c1f63a87d90676",
                Version: "4.5.10",
            },
        },
    },
}
```

**Test Case 2: Digest from availableUpdates (fallback)**
```go
func TestUpgradeClusterForceUpgradeWithImageDigestInAvailableList(t *testing.T) {
    // Tests secondary path: digest discovery from availableUpdates array
    AvailableUpdates: []clusterversionv1.Release{
        {
            Version: "4.5.10",
            Image:   "quay.io/openshift-release-dev/ocp-release@sha256:71e158c6173ad6aa6e356c119a87459196bbe70e89c0db1e35c1f63a87d90676",
        },
    },
}
```

### Comprehensive Integration Test Plan

Based on existing ACM test patterns and the Application Model, here's a complete test strategy:

| Step | Expected Result |
|------|-----------------|
| **Setup and Prerequisites** | |
| Verify ACM hub cluster has MultiClusterEngine installed | MCE pods running in multicluster-engine namespace |
| Create test managed cluster with ClusterDeployment | Cluster in "Ready" state with ManagedCluster imported |
| Configure test cluster credentials and pull secrets | Credentials available for cluster operations |
| Verify baseline OpenShift version on managed cluster | ClusterVersion shows current stable version |
| **Digest Discovery Happy Path** | |
| Create ClusterCurator with force upgrade annotation: `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"` | ClusterCurator created with annotation |
| Set desiredUpdate to version available in conditionalUpdates | Version found in cluster's conditionalUpdates list |
| Apply ClusterCurator upgrade specification | ClusterCurator job initiated |
| Monitor ManagedClusterView creation for ClusterVersion | MCV created and populated with remote cluster data |
| Verify digest extracted from conditionalUpdates array | Logs show "Found conditional update image digest" |
| Confirm ManagedClusterAction uses digest reference | MCA ObjectTemplate contains image digest, no force flag |
| Monitor upgrade progress through ClusterVersion conditions | Upgrade progresses without force-related warnings |
| **Fallback to availableUpdates** | |
| Create ClusterCurator for version not in conditionalUpdates | Version only in availableUpdates list |
| Verify digest discovery falls back to availableUpdates | Logs show "Found available update image digest" |
| Confirm upgrade proceeds with discovered digest | MCA uses digest from availableUpdates |
| **Tag-Based Fallback** | |
| Create ClusterCurator for version not in either list | Version not available in cluster update lists |
| Verify fallback to tag-based image reference | Logs show "Image digest not found, fallback to image tag" |
| Confirm force flag is set for tag-based upgrade | MCA ObjectTemplate contains "force": true |
| **Error Handling and Edge Cases** | |
| Attempt upgrade without force annotation | Error: "Provided version is not valid" |
| Test with non-OpenShift cluster type | Error: "Can not upgrade non openshift cluster" |
| Simulate ManagedClusterView timeout | Proper error handling and retry behavior |
| Test with invalid digest format | Graceful fallback to tag-based approach |
| **Multi-Cloud Provider Testing** | |
| Test digest upgrades on AWS managed cluster | Successful digest-based upgrade on AWS |
| Test digest upgrades on Azure managed cluster | Successful digest-based upgrade on Azure |
| Test digest upgrades on GCP managed cluster | Successful digest-based upgrade on GCP |
| **Disconnected Environment Simulation** | |
| Configure mirror registry with digest-only images | Registry accessible with digest references |
| Test digest upgrade in air-gapped environment | Upgrade succeeds using mirrored digest images |
| Verify tag-based upgrade fails in disconnected mode | Tag-based approach fails due to registry access |
| **Performance and Scale Testing** | |
| Test concurrent digest upgrades on multiple clusters | All upgrades proceed without resource conflicts |
| Measure digest discovery performance vs tag-based | Digest approach has minimal performance overhead |
| Test with large number of available updates | Efficient search through conditionalUpdates list |

### Integration with CLC UI Automation

Based on the Application Model components, UI tests should cover:

**ClusterListPage Integration:**
```typescript
// Navigate to cluster upgrade interface
cy.get('[data-testid="clusters-table"]').contains(clusterName).click()
cy.get('[data-testid="cluster-actions"]').click()
cy.get('[data-testid="upgrade-cluster"]').click()

// Configure digest-based upgrade
cy.get('[data-testid="force-upgrade-toggle"]').click()
cy.get('[data-testid="desired-version"]').type('4.14.15')
cy.get('[data-testid="enable-digest-upgrade"]').check()
```

### Advanced Test Scenarios

**EUS to EUS Upgrades with Digests:**
- Test intermediate update discovery for EUS paths
- Verify admin-acks configuration for API removals
- Confirm channel switching during EUS upgrades

**Failure Recovery Testing:**
- Simulate registry unavailability during upgrade
- Test cluster state recovery after failed digest upgrades  
- Verify proper cleanup of ManagedClusterAction resources

## 4. Production Readiness Assessment

### Deployment Considerations

**Environment-Specific Configurations:**
- **Connected Environments:** Standard deployment, all features available
- **Restricted Networks:** Requires mirror registry configuration
- **Air-Gapped:** Mandatory digest-based workflows, disable tag fallbacks

**Security Requirements:**
- Digest verification integration with image trust policies
- RBAC for force upgrade annotation management
- Audit trail for non-recommended upgrade requests

### Monitoring and Observability

**Key Metrics to Track:**
- Digest discovery success rate vs fallback to tags
- Upgrade success rate for digest-based vs tag-based
- Performance impact of conditional/available update parsing
- Error rates for different cluster configurations

**Alert Conditions:**
- Consistent failures in digest discovery
- High rate of tag-based fallbacks
- ManagedClusterView timeout patterns
- Force annotation usage tracking

### Troubleshooting Runbook

**Common Issues and Resolutions:**

1. **Digest Not Found**
   - Check cluster's ClusterVersion status for conditionalUpdates
   - Verify version exists in availableUpdates
   - Confirm cluster update service connectivity

2. **Force Annotation Missing**
   - Validate ClusterCurator annotation syntax
   - Check RBAC permissions for annotation modification
   - Verify version is actually non-recommended

3. **ManagedClusterView Failures**
   - Check hub-spoke network connectivity
   - Verify managed cluster agent health
   - Review ManagedCluster import status

### Documentation and Training

**Developer Documentation:**
- Digest discovery algorithm documentation
- Integration testing best practices
- Custom registry configuration guide

**Operations Documentation:**
- Upgrade workflow troubleshooting guide
- Performance tuning recommendations
- Security configuration guidelines

**Training Materials:**
- ACM upgrade fundamentals
- Disconnected environment management
- Digest-based upgrade workflows

## Conclusion

ACM-22079 represents a sophisticated enhancement to ACM's cluster lifecycle management capabilities. The implementation demonstrates deep understanding of enterprise requirements while maintaining backward compatibility and reliability. The comprehensive test strategy ensures robust validation across multiple deployment scenarios, while the production readiness assessment addresses real-world operational concerns.

The feature successfully bridges the gap between ACM's multi-cluster orchestration capabilities and OpenShift's cluster upgrade mechanisms, enabling reliable upgrades in the most demanding enterprise environments.
