# Test Cases for ACM-9268: KubeVirt Hosted Cluster Creation UI Implementation

## Description
Validate KubeVirt hosted cluster creation UI wizard functionality enabling cluster deployment through integrated form-based interface with namespace selection and resource configuration.

## Setup
Access to ACM Console with KubeVirt cluster creation wizard available. Ensure HyperShift operator configured and OpenShift Virtualization platform enabled for hosted cluster creation.

## Test Case 1: Validate KubeVirt Cluster Creation UI Wizard Flow and Platform Selection

**Description**: Verify KubeVirt cluster creation wizard accessibility, navigation flow, and platform selection functionality for hosted cluster deployment.

**Setup**: ACM Console access with cluster creation privileges and KubeVirt platform option available.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} and authenticate with admin credentials | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {password}` | Successfully authenticated to ACM Console with clusters page accessible |
| 2 | Navigate to Cluster Creation | Click Infrastructure → Clusters → Create cluster button | `oc get managedclusters` | Cluster creation wizard opens with platform selection options displayed |
| 3 | Select KubeVirt Platform | Click cluster catalog card for KubeVirt/OpenShift Virtualization platform | `oc get kubevirt -n openshift-cnv` | KubeVirt platform selected, wizard proceeds to configuration steps |
| 4 | Configure Basic Cluster Information | Enter cluster name "kubevirt-ui-test", select namespace "clusters" | `oc create namespace clusters` | Basic cluster configuration form completed successfully with name and namespace set |
| 5 | Access Platform Configuration | Click "Next" to proceed to KubeVirt-specific configuration options | `oc get storageclass` | KubeVirt platform configuration page displayed with VM resource options |
| 6 | Configure VM Resource Settings | Set CPU: 4 cores, Memory: 8Gi, Storage: 120Gi, StorageClass: standard | Create HostedCluster manifest preparation: `touch kubevirt-cluster.yaml` | VM resource specifications configured with appropriate values for cluster nodes |

## Test Case 2: Test Enhanced Namespace Selection and Form Validation in KubeVirt Wizard

**Description**: Validate enhanced namespace selection combobox functionality and form validation features in KubeVirt cluster creation wizard.

**Setup**: ACM Console access with multiple namespaces available and hypershift.openshift.io/hosted-cluster-namespace=true annotations configured.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} for namespace testing | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {password}` | Successfully authenticated to ACM Console with access to namespace management |
| 2 | Prepare Test Namespaces | Navigate to Administration → Namespaces to view available options | `oc create namespace hypershift-test && oc annotate namespace hypershift-test hypershift.openshift.io/hosted-cluster-namespace=true` | Test namespace created with proper HyperShift annotation for selection |
| 3 | Access KubeVirt Creation Wizard | Click Infrastructure → Clusters → Create cluster → Select KubeVirt platform | `oc get namespaces -l hypershift.openshift.io/hosted-cluster-namespace=true` | KubeVirt wizard opened with namespace selection combobox visible |
| 4 | Test Namespace Selection Combobox | Click namespace dropdown to view available annotated namespaces | `oc describe namespace hypershift-test` | Dropdown displays namespaces with hypershift.openshift.io/hosted-cluster-namespace=true annotation |
| 5 | Validate Form Input Requirements | Leave cluster name empty and attempt to proceed | `oc apply --dry-run=client -f -` with empty cluster name | Form validation prevents progression with required field error messages |
| 6 | Complete Valid Form Submission | Enter cluster name "namespace-test-cluster", select "hypershift-test" namespace | Create complete manifest: `oc apply -f -` with ```yaml
apiVersion: hypershift.openshift.io/v1beta1
kind: HostedCluster
metadata:
  name: namespace-test-cluster
  namespace: hypershift-test
spec:
  release:
    image: quay.io/openshift-release-dev/ocp-release:4.14.0-x86_64
  platform:
    type: KubeVirt
    kubevirt:
      storageClass: standard
``` | Form accepts valid input with namespace properly selected from annotated options |

## Test Case 3: Verify Resource Creation Consistency Between UI Wizard and CLI Methods

**Description**: Validate that UI wizard-generated resources match expected HostedCluster and NodePool resource specifications for consistency with CLI methods.

**Setup**: KubeVirt cluster creation wizard completed and resources generated for comparison with CLI-created resources.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} for resource validation | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {password}` | Console access established for resource comparison and validation |
| 2 | Create Cluster via UI Wizard | Complete KubeVirt cluster creation with name "ui-consistency-test" | Prepare CLI comparison cluster configuration: `touch cli-cluster-config.yaml` | UI wizard cluster creation initiated with resource generation in progress |
| 3 | Inspect Generated HostedCluster | Navigate to cluster details → View YAML configuration | `oc get hostedcluster ui-consistency-test -n clusters -o yaml` | HostedCluster resource displayed with complete specification and metadata |
| 4 | Validate NodePool Configuration | Check cluster details → Node pools tab for configuration | `oc get nodepool -n clusters -l cluster.open-cluster-management.io/cluster-name=ui-consistency-test -o yaml` | NodePool resource shows proper configuration matching UI input specifications |
| 5 | Compare Resource Specifications | Review UI-generated resource specs for accuracy | Create equivalent CLI resources: `oc apply -f -` with ```yaml
apiVersion: hypershift.openshift.io/v1beta1
kind: HostedCluster
metadata:
  name: cli-consistency-test
  namespace: clusters
spec:
  release:
    image: quay.io/openshift-release-dev/ocp-release:4.14.0-x86_64
  platform:
    type: KubeVirt
    kubevirt:
      storageClass: standard
---
apiVersion: hypershift.openshift.io/v1beta1
kind: NodePool
metadata:
  name: cli-consistency-test-workers
  namespace: clusters
spec:
  clusterName: cli-consistency-test
  replicas: 3
  platform:
    type: KubeVirt
    kubevirt:
      compute:
        memory: 8Gi
        cores: 4
      rootVolume:
        size: 120Gi
        storageClass: standard
``` | UI and CLI generated resources show identical specifications and structure |
| 6 | Verify Deployment Status | Monitor both clusters in console for deployment progress | `oc get hostedcluster -n clusters -w` | Both UI and CLI created clusters show consistent deployment behavior and status |

## Test Case 4: Validate End-to-End KubeVirt Cluster Provisioning Through ACM Console Workflow

**Description**: Validate complete cluster lifecycle from UI wizard creation through cluster ready status and management operations in ACM Console.

**Setup**: Clean environment ready for complete cluster provisioning testing with KubeVirt platform and sufficient resources.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} for end-to-end testing | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {password}` | Console authenticated and ready for complete workflow validation |
| 2 | Execute Complete Wizard Flow | Infrastructure → Clusters → Create cluster → KubeVirt platform → Complete all forms | `oc get hostedcluster -n clusters` | Complete wizard navigation successful with all forms properly submitted |
| 3 | Monitor Cluster Provisioning | Watch cluster status progress through Installing → Ready states | `oc get hostedcluster e2e-kubevirt-test -n clusters -w` | Cluster provisioning progresses through expected status phases |
| 4 | Validate Virtual Machine Creation | Check cluster infrastructure → View VM resources and status | `oc get virtualmachines -n clusters-e2e-kubevirt-test` | Virtual machines created with proper resource specifications and running status |
| 5 | Test Cluster Management Functions | Access cluster details → Test scale operations and monitoring | `oc get nodepool -n clusters -l cluster.open-cluster-management.io/cluster-name=e2e-kubevirt-test` | Cluster management functions accessible with scaling and monitoring capabilities |
| 6 | Verify Hosted Cluster Access | Click cluster console link to access hosted cluster | `oc get nodes --kubeconfig=kubeconfig-e2e-kubevirt-test` | Hosted cluster fully accessible with working console and API endpoints |