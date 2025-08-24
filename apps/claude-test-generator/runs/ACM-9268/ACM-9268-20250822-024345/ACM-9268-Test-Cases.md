# Test Cases for ACM-9268: KubeVirt hosted cluster creation UI implementation

## Description
Validate KubeVirt hosted cluster creation UI functionality enabling OpenShift Virtualization-based cluster deployment through integrated wizard interface with VM resource configuration and virtual machine orchestration.

## Setup
- Access to ACM Hub cluster with KubeVirt operator and OpenShift Virtualization enabled
- Available VM resources and storage for hosted cluster infrastructure deployment
- ACM Console with KubeVirt cluster creation interface accessible
- HyperShift operator configured for KubeVirt platform integration

## Test Cases

### Test Case 1: KubeVirt Hosted Cluster Creation Wizard Access and Platform Selection

**Description**: Verify KubeVirt hosted cluster creation wizard accessibility and platform selection functionality for virtual machine-based cluster deployment.

**Step 1: Log into ACM Console** - Access ACM Console for KubeVirt cluster creation testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in via Console authentication and navigate to "Infrastructure" → "Clusters"
- **CLI Method**: Authenticate and verify KubeVirt access: `oc login https://api.<cluster-host>:6443 -u <username> -p <password>`
- **Expected Results**: Console loads with clusters page showing create cluster options including KubeVirt platform selection

**Step 2: Access Create Cluster Wizard** - Launch cluster creation wizard with KubeVirt platform options
- **UI Method**: Click "Create cluster" button to open cluster creation wizard
- **CLI Method**: Check available KubeVirt resources: `oc get virtualmachines -n openshift-cnv`
- **Expected Results**: Cluster creation wizard opens with platform selection showing KubeVirt/OpenShift Virtualization option

**Step 3: Select KubeVirt Platform** - Choose KubeVirt platform for hosted cluster deployment
- **UI Method**: Select "KubeVirt" or "OpenShift Virtualization" platform option from wizard
- **CLI Method**: Verify KubeVirt operator status: `oc get csv -n openshift-cnv | grep kubevirt`
- **Expected Results**: KubeVirt platform selected with wizard proceeding to configuration steps

**Step 4: Configure Cluster Basic Information** - Set cluster name and namespace for KubeVirt deployment
- **UI Method**: Enter cluster name, namespace, and basic configuration in wizard form
- **CLI Method**: Prepare cluster configuration template: Create `kubevirt-cluster-config.yaml`:
```yaml
apiVersion: hypershift.openshift.io/v1beta1
kind: HostedCluster
metadata:
  name: kubevirt-hosted-cluster
  namespace: clusters
spec:
  release:
    image: "quay.io/openshift-release-dev/ocp-release:4.14.0-x86_64"
  pullSecret:
    name: pullsecret-cluster
  platform:
    type: KubeVirt
    kubevirt:
      storageClass: standard
```
- **Expected Results**: Cluster basic information configured with KubeVirt-specific settings available

**Step 5: Configure Virtual Machine Resources** - Set VM specifications for hosted cluster nodes
- **UI Method**: Configure VM resource specifications (CPU, memory, storage) in wizard interface
- **CLI Method**: Define NodePool configuration: Create `kubevirt-nodepool.yaml`:
```yaml
apiVersion: hypershift.openshift.io/v1beta1
kind: NodePool
metadata:
  name: kubevirt-nodepool
  namespace: clusters
spec:
  clusterName: kubevirt-hosted-cluster
  release:
    image: "quay.io/openshift-release-dev/ocp-release:4.14.0-x86_64"
  replicas: 3
  platform:
    type: KubeVirt
    kubevirt:
      compute:
        memory: "8Gi"
        cores: 4
      rootVolume:
        size: "120Gi"
        storageClass: standard
```
- **Expected Results**: VM resource configuration completed with appropriate specifications for cluster requirements

**Step 6: Review and Create KubeVirt Cluster** - Submit cluster creation request with validation
- **UI Method**: Review configuration summary and click "Create" to submit cluster creation
- **CLI Method**: Apply cluster configuration: `oc apply -f kubevirt-cluster-config.yaml && oc apply -f kubevirt-nodepool.yaml`
- **Expected Results**: Cluster creation initiated with KubeVirt platform showing deployment progress

### Test Case 2: KubeVirt Hosted Cluster VM Infrastructure Validation

**Description**: Validate KubeVirt hosted cluster virtual machine infrastructure deployment and resource allocation through cluster management interface.

**Step 1: Log into ACM Console** - Access ACM Console for KubeVirt infrastructure validation: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to hosted cluster details for KubeVirt infrastructure monitoring
- **CLI Method**: Monitor cluster creation progress: `oc get hostedcluster kubevirt-hosted-cluster -n clusters -o yaml`
- **Expected Results**: KubeVirt hosted cluster visible in infrastructure with VM deployment status

**Step 2: Validate Virtual Machine Creation** - Verify virtual machines created for hosted cluster infrastructure
- **UI Method**: Check cluster infrastructure tab showing VM resources and status
- **CLI Method**: List created VMs: `oc get virtualmachines -n clusters-kubevirt-hosted-cluster`
- **Expected Results**: Virtual machines deployed with appropriate resource specifications and running status

**Step 3: Monitor Cluster Deployment Progress** - Track hosted cluster deployment through VM orchestration
- **UI Method**: Monitor deployment progress indicators in cluster details interface
- **CLI Method**: Check cluster conditions: `oc get hostedcluster kubevirt-hosted-cluster -n clusters -o jsonpath='{.status.conditions}'`
- **Expected Results**: Deployment progress tracked with VM provisioning and cluster initialization status

**Step 4: Validate Storage Integration** - Verify persistent volume and storage class configuration
- **UI Method**: Check storage configuration in cluster infrastructure details
- **CLI Method**: Verify storage resources: `oc get pvc -n clusters-kubevirt-hosted-cluster`
- **Expected Results**: Storage properly allocated with persistent volumes attached to VMs

**Step 5: Test VM Network Connectivity** - Validate virtual machine network configuration and connectivity
- **UI Method**: Check network status in infrastructure monitoring interface
- **CLI Method**: Verify network configuration: `oc get virtualmachineinstances -n clusters-kubevirt-hosted-cluster -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IPS:.status.interfaces[0].ipAddress`
- **Expected Results**: VMs properly networked with IP addresses assigned and connectivity established

**Step 6: Verify Hosted Cluster Accessibility** - Confirm hosted cluster API and console accessibility
- **UI Method**: Access hosted cluster console link from ACM interface
- **CLI Method**: Test hosted cluster API: `oc get nodes --kubeconfig=kubeconfig-kubevirt-hosted-cluster`
- **Expected Results**: Hosted cluster fully accessible with working API and console interface

### Test Case 3: KubeVirt Hosted Cluster Management and Operations

**Description**: Validate KubeVirt hosted cluster management operations including scaling, monitoring, and lifecycle management through virtual machine orchestration.

**Step 1: Log into ACM Console** - Access ACM Console for KubeVirt cluster management: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Access KubeVirt hosted cluster management interface
- **CLI Method**: List managed clusters: `oc get managedclusters | grep kubevirt`
- **Expected Results**: KubeVirt hosted cluster available for management operations

**Step 2: Scale Node Pool Virtual Machines** - Test scaling operations for hosted cluster node pools
- **UI Method**: Use cluster management interface to scale node pool replicas
- **CLI Method**: Scale node pool: `oc patch nodepool kubevirt-nodepool -n clusters --type merge -p '{"spec":{"replicas":5}}'`
- **Expected Results**: Node pool scaling initiated with additional VMs provisioned

**Step 3: Monitor VM Resource Utilization** - Validate resource monitoring and metrics collection
- **UI Method**: Check resource utilization metrics in cluster monitoring dashboard
- **CLI Method**: Get resource usage: `oc get virtualmachineinstances -n clusters-kubevirt-hosted-cluster -o custom-columns=NAME:.metadata.name,CPU:.status.guestOSInfo.kernelRelease,MEMORY:.spec.domain.resources.requests.memory`
- **Expected Results**: Resource utilization properly monitored with accurate VM metrics

**Step 4: Test VM Maintenance Operations** - Validate virtual machine maintenance and update procedures
- **UI Method**: Access VM maintenance options through cluster management interface
- **CLI Method**: Check VM update status: `oc get virtualmachines -n clusters-kubevirt-hosted-cluster -o jsonpath='{.items[*].status.ready}'`
- **Expected Results**: VM maintenance operations available with proper status reporting

**Step 5: Validate Cluster Upgrade Capability** - Test hosted cluster upgrade through VM orchestration
- **UI Method**: Access cluster upgrade options in management interface
- **CLI Method**: Check upgrade availability: `oc get hostedcluster kubevirt-hosted-cluster -n clusters -o jsonpath='{.status.version}'`
- **Expected Results**: Cluster upgrade options available with VM-based upgrade orchestration

**Step 6: Test Cluster Deletion and Cleanup** - Verify proper cluster deletion with VM resource cleanup
- **UI Method**: Use cluster management interface to delete hosted cluster
- **CLI Method**: Delete cluster resources: `oc delete hostedcluster kubevirt-hosted-cluster -n clusters && oc delete nodepool kubevirt-nodepool -n clusters`
- **Expected Results**: Cluster deletion completes with all VMs and resources properly cleaned up