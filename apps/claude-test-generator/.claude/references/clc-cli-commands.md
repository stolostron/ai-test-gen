# Essential CLC-Specific CLI Commands with Expected Outputs

## 1. Environment Discovery & Validation

```bash
# ACM/MCE namespace auto-discovery (from setup_clc)
export ACM_NS=$(oc get subscriptions.operators.coreos.com -A -o json | jq -r '.items[] | select(.spec.name=="advanced-cluster-management").metadata.namespace')
export MCE_NS=$(oc get mce -ojsonpath="{.items[0].spec.targetNamespace}")

echo "ACM Namespace: $ACM_NS"    # Expected: "open-cluster-management" or custom
echo "MCE Namespace: $MCE_NS"    # Expected: "multicluster-engine" or custom

# Cluster connectivity validation
oc whoami --show-server
# Expected: https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443

oc get clusterversion
# Expected: 
# NAME      VERSION   AVAILABLE   PROGRESSING   SINCE   STATUS
# version   4.15.10   True        False         5d      Cluster version is 4.15.10

# Environment validation commands
kubectl version --client
kubectl cluster-info

# Check ACM/MCE installation
kubectl get operators -n openshift-operators | grep advanced-cluster-management
kubectl get mce -A

# List managed clusters
kubectl get managedclusters
```

## 2. ACM Component Status Verification

```bash
# ACM Hub Status
oc get multiclusterhub -n $ACM_NS
# Expected:
# NAME                STATUS    AGE
# multiclusterhub     Running   25d

# MCE Engine Status  
oc get multiclusterengine -n $MCE_NS
# Expected:
# NAME                        STATUS      AGE
# multiclusterengine-sample   Available   25d

# Managed Cluster Inventory
oc get managedclusters
# Expected:
# NAME              HUB ACCEPTED   MANAGED CLUSTER URLS                                            JOINED   AVAILABLE   AGE
# local-cluster     true           https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com   True     True        25d
# spoke-cluster-1   true           https://api.spoke1.company.com:6443                             True     True        10d
```

## 3. CLC Operations Monitoring

```bash
# ClusterCurator Status (Upgrade Operations)
oc get clustercurator -A -o wide
# Expected:
# NAMESPACE        NAME                     CURATION   STATUS        AGE
# cluster-ns-1     production-upgrade       upgrade    InProgress    15m
# cluster-ns-2     staging-upgrade          upgrade    Succeeded     2h

# ClusterDeployment Status (Creation Operations)
oc get clusterdeployment -A
# Expected:
# NAMESPACE      NAME                    PLATFORM   REGION      AGE
# spoke-ns-1     new-cluster-deploy      vsphere    us-east-1   45m
# spoke-ns-2     backup-cluster-deploy   aws        us-west-2   2h

# Hive ClusterImageSet Availability
oc get clusterimageset
# Expected:
# NAME                      RELEASE
# img4.15.10-x86-64         quay.io/openshift-release-dev/ocp-release:4.15.10-x86_64
# img4.14.15-x86-64         quay.io/openshift-release-dev/ocp-release:4.14.15-x86_64
```

## 4. Enhanced Digest-Based Upgrade Verification with YAML Samples

```bash
# Check ClusterCurator annotation (NEW functionality)
oc get clustercurator production-upgrade -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'
# Expected: "true" (feature activated) or empty (standard upgrade)

# ManagedClusterView-based verification from the hub (recommended)
# Discover served versions of ManagedClusterView CRD
oc get crd managedclusterviews.view.open-cluster-management.io -o jsonpath='{.spec.versions[*].name}'

# Create a view to read ClusterVersion from a managed cluster namespace
cat <<EOF | oc apply -f -
apiVersion: view.open-cluster-management.io/v1beta1
kind: ManagedClusterView
metadata:
  name: clusterversion
  namespace: <managed-cluster-namespace>
spec:
  scope:
    apiGroup: config.openshift.io
    kind: ClusterVersion
    name: version
EOF

# Verify digest usage in ClusterVersion via the view
oc get managedclusterview clusterversion -n <managed-cluster-namespace> \
  -o jsonpath='{.status.result.spec.desiredUpdate.image}'
# Expected with NEW feature: "registry.redhat.io/...@sha256:abc123..." (digest format)
# Expected without feature: "4.16.37" or "registry.redhat.io/...:4.16.37" (tag format)

# Sample YAML - ClusterVersion with digest (NEW behavior):
oc --kubeconfig=<managed-cluster> get clusterversion -o yaml
# Expected output:
# apiVersion: config.openshift.io/v1
# kind: ClusterVersion
# metadata:
#   name: version
# spec:
#   desiredUpdate:
#     version: "4.16.37"
#     image: "registry.redhat.io/ubi8/ubi@sha256:abc123def456..."  # ← DIGEST FORMAT
# status:
#   desired:
#     version: "4.16.37"
#   conditions:
#   - type: "Progressing"
#     status: "True"  # or "False" when complete

# Verify conditionalUpdates source (what the NEW feature uses) via the view
oc get managedclusterview clusterversion -n <managed-cluster-namespace> \
  -o jsonpath='{.status.result.status.conditionalUpdates[?(@.release.version=="4.16.37")].release.image}'
# Expected: "registry.redhat.io/...@sha256:abc123..." (digest that gets extracted)

# Sample ClusterCurator with NEW annotation (schema-aware minimal fields included):
oc get clustercurator production-upgrade -o yaml
# Expected output:
# apiVersion: cluster.open-cluster-management.io/v1beta1
# kind: ClusterCurator
# metadata:
#   annotations:
#     cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"  # ← NEW
#   name: production-upgrade
# spec:
#   desiredCuration: upgrade
#   upgrade:
#     desiredUpdate: "4.16.37"  # Non-recommended version
#     towerAuthSecret: ""
#     prehook: []
#     posthook: []
#   install:
#     towerAuthSecret: ""
#     prehook: []
#     posthook: []
# status:
#   conditions:
#   - type: "clustercurator-job"
#     status: "True"
#     message: "Using digest from conditionalUpdates for upgrade"  # ← NEW behavior
```

## 5. Troubleshooting & Debug Commands

```bash
# ClusterCurator Controller Logs
oc logs deployment/cluster-curator-controller -n $ACM_NS -f
# Expected: Real-time controller logs showing upgrade operations

# Hive Controller Logs for ClusterDeployment issues
oc logs deployment/hive-controllers -n hive -f
# Expected: Logs from Hive controllers managing cluster lifecycle

# ACM Console Pod Status (for UI testing)
oc get pods -n $ACM_NS | grep console
# Expected:
# console-chart-v2-console-v2-abc123-xyz789   1/1     Running   0          25d

# Check for failed pods across ACM components
oc get pods -A | grep -E "(Error|CrashLoopBackOff|ImagePullBackOff)"
# Expected: Empty output (no failed pods) or specific failure details to investigate
```

## 6. JIRA Analysis Commands

```bash
# View ticket details with description and comments
jira issue view <TICKET-ID> --plain

# Get ticket with comments
jira issue view <TICKET-ID> --comments

# List subtasks and linked issues
jira issue view <TICKET-ID> # Shows linked tickets in output
```

## 7. GitHub PR Analysis Commands

```bash
# Use WebFetch tool with GitHub URLs for PR analysis
# Format: https://github.com/<owner>/<repo>/pull/<number>
```

## 8. Common ACM Repository Patterns

```bash
# Key repositories to monitor:
# - stolostron/console - ACM Console UI
# - stolostron/* - Red Hat ACM components
# - Enterprise repositories as discovered
```
