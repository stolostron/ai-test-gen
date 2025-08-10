# YAML Sample Templates for Expected Results

## Complete Test Scenarios with Expected Outputs

### Digest-Based Upgrade Test (NEW Functionality)

**Complete ClusterCurator YAML** (`clustercurator-digest-upgrade.yaml`):
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"  # NEW: Required for digest logic
  name: digest-upgrade-test
  namespace: cluster-namespace
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.37"  # Non-recommended version
    monitorTimeout: 120
```

**Expected Controller Logs** when running `oc logs -n multicluster-engine deployment/cluster-curator-controller | grep -i "digest\|conditional"`:
```
2024-08-09T19:30:15Z INFO Checking conditionalUpdates for digest information version=4.16.37
2024-08-09T19:30:16Z INFO Found digest in conditionalUpdates digest=sha256:abc123def456...
2024-08-09T19:30:17Z INFO Using digest-based upgrade image=registry.redhat.io/...@sha256:abc123def456...
```

**Expected ClusterCurator Status**:
```yaml
status:
  conditions:
  - type: "clustercurator-job"
    status: "True"
    lastTransitionTime: "2024-08-09T19:30:20Z"
    message: "Using digest from conditionalUpdates for upgrade to 4.16.37"  # NEW behavior
    reason: "DigestResolved"
```

### Fallback Test Scenario (NEW Functionality)

**Complete ClusterCurator YAML** (`clustercurator-fallback-test.yaml`):
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"  # NEW: Enables digest logic
  name: fallback-test
  namespace: cluster-namespace
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.15.25"  # Version present in availableUpdates but NOT in conditionalUpdates
    monitorTimeout: 120
```

**Expected Controller Logs** when running `oc logs -n multicluster-engine deployment/cluster-curator-controller | grep -i "fallback\|available"`:
```
2024-08-09T19:35:10Z INFO Checking conditionalUpdates for digest information version=4.15.25
2024-08-09T19:35:11Z WARN Version not found in conditionalUpdates, checking availableUpdates version=4.15.25
2024-08-09T19:35:12Z INFO Found digest in availableUpdates digest=sha256:xyz789abc123...
2024-08-09T19:35:13Z INFO Using fallback digest from availableUpdates image=registry.redhat.io/...@sha256:xyz789abc123...
```

### Standard Upgrade (No Annotation - Traditional Behavior)

**Complete ClusterCurator YAML** (`clustercurator-standard.yaml`):
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: standard-upgrade-test
  namespace: cluster-namespace
  # NOTE: No digest annotation - uses traditional upgrade logic
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "4.16.37"
    monitorTimeout: 120
```

**Expected Controller Logs** when running `oc logs -n multicluster-engine deployment/cluster-curator-controller | grep -i "standard\|traditional"`:
```
2024-08-09T19:40:05Z INFO Starting standard upgrade process version=4.16.37
2024-08-09T19:40:06Z INFO Using traditional image tag approach image=4.16.37
2024-08-09T19:40:07Z INFO ClusterVersion update applied with force flag
```

## ClusterVersion Examples

### With Digest Reference (NEW Behavior)
```yaml
apiVersion: config.openshift.io/v1
kind: ClusterVersion
metadata:
  name: version
spec:
  desiredUpdate:
    version: "4.16.37"
    image: "registry.redhat.io/ubi8/ubi@sha256:abc123def456..."
status:
  desired:
    version: "4.16.37"
  conditions:
  - type: "Progressing"
    status: "False"
    message: "Cluster version is 4.16.37"
  - type: "Available"
    status: "True"
```

### With Tag Reference (Traditional Behavior)
```yaml
apiVersion: config.openshift.io/v1
kind: ClusterVersion
metadata:
  name: version
spec:
  desiredUpdate:
    version: "4.16.37"
    image: "4.16.37"
status:
  desired:
    version: "4.16.37"
  conditions:
  - type: "Progressing"
    status: "False"
    message: "Cluster version is 4.16.37"
```

## ConditionalUpdates Examples

### With Available Digests
```yaml
status:
  conditionalUpdates:
  - release:
      version: "4.16.37"
      image: "registry.redhat.io/ubi8/ubi@sha256:abc123def456..."
    conditions:
    - type: "Recommended"
      status: "False"
      reason: "NonRecommendedUpdate"
```

### Without Digest Information
```yaml
status:
  conditionalUpdates:
  - release:
      version: "4.16.37"
      # Note: Missing image field - digest not available
    conditions:
    - type: "Recommended"
      status: "False"
      reason: "NonRecommendedUpdate"
```

## Command Output Examples

### Digest Discovery Commands
```bash
# Check for digest in ClusterVersion
oc get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate.image}'
# Expected with digest: "registry.redhat.io/...@sha256:abc123..."
# Expected with tag: "4.16.37"

# Extract digest from conditionalUpdates
oc get clusterversion -o jsonpath='{.items[0].status.conditionalUpdates[?(@.release.version=="4.16.37")].release.image}'
# Expected: "registry.redhat.io/...@sha256:abc123..."
```

## Standard Setup Steps for All Test Cases

### Prerequisites (Include in every test case)
```markdown
**Step 1: Hub Cluster Access**
**Goal**: Establish connection to ACM hub cluster
**Instructions**: 
1. Go to your terminal
2. Run the following command: `source setup_clc qe6` (or your target environment)
3. Verify connectivity: `oc whoami --show-server`

**Expected Output**: 
```
https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443
```

**Step 2: Verify ACM Components**
**Goal**: Confirm ACM/MCE installation and identify managed clusters
**Instructions**:
1. In your terminal, run: `oc get managedclusters`
2. Run: `oc get mce -A` to verify MCE installation

**Expected Output**:
```
NAME              HUB ACCEPTED   JOINED   AVAILABLE   AGE
local-cluster     true           True     True        25d
spoke-cluster-1   true           True     True        10d
```
```

## Enhanced Test Table Format

### Test Steps Column
```markdown
**Step N: [Action Description]**
**Goal**: [Why this step matters for the NEW functionality]
**Instructions**: 
1. Go to your terminal
2. Run the following command: `[command]`
3. [Additional context or setup if needed]

**Command**: `[exact command to copy-paste]`
```

### Expected Results Column
```markdown
**Success Criteria**: [Specific, measurable outcome]
**Validation Instructions**:
1. In your terminal, run: `[validation command]`
2. Look for: [specific text or pattern]

**Expected Command Output**:
```
[exact expected output with explanations]
```

**Sample YAML Result** (when applicable):
```yaml
[relevant YAML sections with comments]
```
```

## Skipped Functionality Statements

When areas are intentionally not tested due to no changes:

```markdown
### ❌ FUNCTIONALITY INTENTIONALLY SKIPPED

**Unchanged Upgrade Infrastructure**: The following areas remain unchanged in this implementation and are intentionally excluded from testing:
- **Upgrade Monitoring**: No changes to cluster operator monitoring logic
- **Timeout Handling**: Existing timeout mechanisms unchanged
- **UI Components**: ACM Console upgrade flows use existing code paths
- **General Error Recovery**: Standard error handling patterns unchanged
- **Network Connectivity**: Connection retry logic unchanged

**Focus**: Testing concentrates ONLY on the NEW digest discovery algorithm and annotation-gated functionality introduced in ACM-22079.
```

## Command Output Examples with Grep Instructions

### Digest Discovery Validation
```markdown
**Instructions**: 
1. Go to your terminal
2. Run the following command: `oc logs -n multicluster-engine deployment/cluster-curator-controller | grep -i "digest\|conditional"`
3. Look for digest resolution messages

**Expected Output**:
```
2024-08-09T19:30:15Z INFO Checking conditionalUpdates for digest information version=4.16.37
2024-08-09T19:30:16Z INFO Found digest in conditionalUpdates digest=sha256:abc123def456...
```
```
