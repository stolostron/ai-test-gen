# ACM-22079 Pull Request #468 - Complete Details

## PR Information
- **URL**: https://github.com/stolostron/cluster-curator-controller/pull/468/files
- **Title**: ACM-22079 Initial non-recommended image digest feature
- **Status**: Merged (Jul 16, 2025)
- **Author**: fxiang1
- **Branch**: fxiang1:feng-digest → stolostron:main
- **Changes**: +400 -31 lines across 4 files

## Commits Overview
1. **6a9fe54**: Initial non-recommended image digest feature (Jul 14, 2025)
2. **41bcc83**: Fix typo (Jul 14, 2025)
3. **0346143**: Change param return order (Jul 14, 2025)
4. **5912245**: Fix code from code review suggestions (Jul 15, 2025)
5. **29641ba**: Improve LoadConfig (Jul 16, 2025)

## Files Changed

### 1. cmd/curator/curator.go (2 changes: 1 addition & 1 deletion)
```go
// BEFORE:
config, err := rest.InClusterConfig()

// AFTER:
config, err := utils.LoadConfig()
```

**Purpose**: Switch to new LoadConfig() helper function that supports both in-cluster and local development configurations.

### 2. pkg/jobs/hive/hive.go (148 changes: 121 additions & 27 deletions)

#### Key Changes:

**A. Error Constant Update:**
```go
// BEFORE:
var getErr = errors.New("Failed to get remote clusterversion")

// AFTER:
var GetErrConst = errors.New("failed to get remote clusterversion")
```

**B. Enhanced UpgradeCluster Function:**
```go
// BEFORE:
desiredUpdate := curator.Spec.Upgrade.DesiredUpdate
var err error

if err := validateUpgradeVersion(client, clusterName, curator); err != nil {
    return err
}

// AFTER:
desiredUpdate := curator.Spec.Upgrade.DesiredUpdate
imageWithDigest := ""
var err error

if imageWithDigest, err = validateUpgradeVersion(client, clusterName, curator); err != nil {
    return err
}
```

**C. Modified Function Signature:**
```go
// BEFORE:
mcaStatus, err := retreiveAndUpdateClusterVersion(client, clusterName, curator, desiredUpdate)

// AFTER:
mcaStatus, err := retreiveAndUpdateClusterVersion(client, clusterName, curator, desiredUpdate, imageWithDigest)
```

**D. Enhanced validateUpgradeVersion Function:**
The function now returns both error and imageWithDigest string, and includes comprehensive digest discovery logic:

```go
func validateUpgradeVersion(client clientv1.Client, clusterName string, curator *clustercuratorv1.ClusterCurator) (string, error) {
    // ... existing validation logic ...
    
    imageWithDigest := ""
    
    // New digest discovery logic when force annotation is present
    if curatorAnnotations != nil && curatorAnnotations[ForceUpgradeAnnotation] == "true" {
        // Create/get ManagedClusterView for remote cluster state
        // Search conditionalUpdates first, then availableUpdates
        // Extract image digest if found
        
        if clusterConditionalUpdates, ok := clusterVersion["status"].(map[string]interface{})["conditionalUpdates"]; ok {
            for _, conditionalUpdate := range clusterConditionalUpdates.([]interface{}) {
                updateVersion := conditionalUpdate.(map[string]interface{})["release"].(map[string]interface{})["version"].(string)
                if updateVersion == desiredUpdate {
                    imageWithDigest = conditionalUpdate.(map[string]interface{})["release"].(map[string]interface{})["image"].(string)
                    break
                }
            }
        }
        
        // Fallback to availableUpdates if not found in conditionalUpdates
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
    }
    
    return imageWithDigest, nil
}
```

**E. Enhanced retreiveAndUpdateClusterVersion Function:**
Now accepts imageWithDigest parameter and uses it conditionally:

```go
func retreiveAndUpdateClusterVersion(
    client clientv1.Client,
    clusterName string,
    curator *clustercuratorv1.ClusterCurator,
    desiredUpdate, imageWithDigest string) (managedclusteractionv1beta1.ManagedClusterAction, error) {
    
    // ... existing logic ...
    
    // Smart image reference selection
    if imageWithDigest != "" {
        cvDesiredUpdate.(map[string]interface{})["image"] = imageWithDigest
        // Note: No "force": true needed when using digest
    } else {
        // only force when using image tag
        cvDesiredUpdate.(map[string]interface{})["force"] = true
        // fallback to using image tag if digest not found - also for backwards compatibility
        cvDesiredUpdate.(map[string]interface{})["image"] =
            "quay.io/openshift-release-dev/ocp-release:" + desiredUpdate + "-multi"
    }
    
    // For new desiredUpdate creation
    if imageWithDigest != "" {
        clusterVersion["spec"].(map[string]interface{})["desiredUpdate"] = map[string]interface{}{
            "version": desiredUpdate,
            "image":   imageWithDigest,
        }
    } else {
        // fallback to using image tag if digest not found - also for backwards compatibility
        clusterVersion["spec"].(map[string]interface{})["desiredUpdate"] = map[string]interface{}{
            "version": desiredUpdate,
            "force":   true,
            "image":   "quay.io/openshift-release-dev/ocp-release:" + desiredUpdate + "-multi",
        }
    }
}
```

### 3. pkg/jobs/hive/hive_test.go (243 additions)
Two comprehensive test cases added:

#### A. TestUpgradeClusterForceUpgradeWithImageDigest
Tests digest extraction from conditionalUpdates array:
```go
ConditionalUpdates: []clusterversionv1.ConditionalUpdate{
    {
        Release: clusterversionv1.Release{
            Image:   "quay.io/openshift-release-dev/ocp-release@sha256:71e158c6173ad6aa6e356c119a87459196bbe70e89c0db1e35c1f63a87d90676",
            Version: "4.5.10",
        },
    },
},
```

#### B. TestUpgradeClusterForceUpgradeWithImageDigestInAvailableList  
Tests digest extraction from availableUpdates array (fallback scenario).

### 4. pkg/jobs/utils/helpers.go (38 changes: 35 additions & 3 deletions)

#### New LoadConfig Function:
```go
func LoadConfig() (*rest.Config, error) {
    kubeconfig := os.Getenv("DEV_ONLY_KUBECONFIG")
    if kubeconfig != "" {
        return configFromFile(kubeconfig)
    }
    return rest.InClusterConfig()
}

func configFromFile(kubeconfig string) (*rest.Config, error) {
    config, err := clientcmd.LoadFromFile(kubeconfig)
    if err != nil {
        return nil, err
    }
    return clientcmd.NewDefaultClientConfig(
        *config,
        &clientcmd.ConfigOverrides{}).ClientConfig()
}
```

**Purpose**: Enables local development by checking for DEV_ONLY_KUBECONFIG environment variable.

## Technical Implementation Summary

### Core Algorithm:
1. **Force Annotation Check**: Only activate digest discovery when `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"`
2. **Digest Discovery Priority**: Search conditionalUpdates first, then availableUpdates
3. **Image Reference Selection**: Use digest if found, fallback to tag-based approach
4. **Force Flag Logic**: Only set `force: true` for tag-based upgrades, not needed with digests

### Key Benefits:
- **Disconnected Environment Support**: Digests work reliably in air-gapped deployments
- **Non-Recommended Upgrades**: Enables version skipping and candidate releases  
- **Backwards Compatibility**: Maintains existing upgrade behavior for recommended paths
- **Development Support**: New LoadConfig enables local testing

## Code Review Comments
The PR includes resolved code review discussions, particularly around parameter ordering and implementation details.

---
*This PR successfully implements digest-based upgrades for ClusterCurator, enabling reliable non-recommended upgrade paths in disconnected environments.*