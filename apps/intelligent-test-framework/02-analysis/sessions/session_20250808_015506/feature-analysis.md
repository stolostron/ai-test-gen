## Implementation-Ready Test Code

Based on the ACM test automation patterns analyzed, here are implementation-ready test configurations:

### Cypress Test Implementation

```javascript
describe('ACM-22079: ClusterCurator Digest Upgrades', {
  tags: ['@CLC', '@digest-upgrade', '@clustercurator']
}, function() {
  
  const testCluster = `digest-test-${Date.now()}`
  const targetVersion = '4.13.7'
  const imageDigest = 'quay.io/openshift-release-dev/ocp-release@sha256:abc123...'
  
  before(function() {
    cy.clearOCMCookies()
    cy.loginViaAPI()
    // Setup test cluster with baseline version
    managedClustersMethods.createSNOCluster('aws', '4.13.0-multi', null, 'amd64', false)
      .then((clusterName) => {
        managedClustersMethods.validateSNOClusterCreation(clusterName)
      })
  })
  
  it('RHACM4K-22079-1: Digest-based cluster upgrade with force annotation', function() {
    // Create ClusterCurator with digest upgrade
    automationMethods.createClusterCurator(testCluster, {
      desiredCuration: 'upgrade',
      upgrade: {
        desiredUpdate: targetVersion,
        annotations: {
          'cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions': 'true'
        }
      }
    })
    
    // Monitor digest resolution
    cy.waitUntil(() => {
      return cluster.getClusterVersion(testCluster).then((resp) => {
        return resp.spec.desiredUpdate.image.includes('@sha256:')
      })
    }, {
      errorMsg: 'Digest not resolved in cluster version',
      interval: 5000,
      timeout: 60000
    })
    
    // Verify upgrade completion
    managedClustersMethods.validateUpgradeCompletion(testCluster, targetVersion)
  })
})
```

### Go Unit Tests Extension

```go
func TestUpgradeClusterWithConditionalDigest(t *testing.T) {
    clustercurator := &clustercuratorv1.ClusterCurator{
        ObjectMeta: v1.ObjectMeta{
            Name: ClusterName,
            Namespace: ClusterName,
            Annotations: map[string]string{
                ForceUpgradeAnnotation: "true",
            },
        },
        Spec: clustercuratorv1.ClusterCuratorSpec{
            DesiredCuration: "upgrade",
            Upgrade: clustercuratorv1.UpgradeHooks{
                DesiredUpdate: "4.13.7",
            },
        },
    }
    
    // Mock cluster version with conditional updates containing digest
    clusterVersion := createMockClusterVersionWithDigest("4.13.7", 
        "quay.io/openshift-release-dev/ocp-release@sha256:abc123...")
    
    client := setupFakeClient(clustercurator, getManagedClusterInfo(), clusterVersion)
    
    err := UpgradeCluster(client, ClusterName, clustercurator)
    assert.Nil(t, err, "Digest-based upgrade should succeed")
    
    // Verify digest was used instead of tag
    verifyDigestUsage(t, client, ClusterName)
}
```

This comprehensive analysis provides the foundation for implementing and testing ACM-22079's digest upgrade capabilities, ensuring robust support for precise cluster lifecycle management in enterprise environments.
