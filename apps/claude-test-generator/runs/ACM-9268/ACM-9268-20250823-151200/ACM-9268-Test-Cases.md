# KubeVirt Hosted Cluster Creation UI Test Cases

## Test Case 1: KubeVirt Hosted Cluster Creation via ACM Console UI Wizard

### Description
Verify the complete end-to-end workflow for creating a KubeVirt hosted cluster through the ACM Console UI wizard, validating the UI implementation that replaces the CLI-only approach for HyperShift cluster creation on OpenShift Virtualization Platform.

### Setup
- ACM environment with MCE 2.5.0+ installed and HyperShift enabled
- OpenShift Virtualization configured with KubeVirt operator
- Storage classes available for virtual machine workloads
- Valid pull secret and SSH key configured
- Sufficient cluster resources for hosted cluster deployment

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> and log in with cluster administrator credentials | `oc login https://api.<cluster-host>:6443 -u <admin-user> -p <admin-password>` | Successfully logged into ACM Console with cluster management interface visible |
| 2 | Navigate to cluster creation | Click **Infrastructure** → **Clusters** → **Create cluster** button | `oc get clusters -A` to verify current cluster state | Cluster creation page displays with infrastructure provider options including KubeVirt |
| 3 | Select KubeVirt platform | Click on **KubeVirt** infrastructure provider card | `oc get csv -A \| grep kubevirt` to verify KubeVirt availability | KubeVirt infrastructure provider selected, showing hosted cluster options |
| 4 | Select hosted cluster option | Click **Hosted** option card with description about decoupled control plane | `oc get hostedclusters -A` to check existing hosted clusters | Hosted cluster creation wizard opens with cluster configuration form |
| 5 | Configure basic cluster details | Fill cluster name: **kubevirt-test-cluster**, namespace: **clusters**, base domain: **<cluster-host>**, release image: **quay.io/openshift-release-dev/ocp-release:4.14.15-x86_64** | Create namespace and basic configuration: `oc create namespace clusters --dry-run=client -o yaml > namespace.yaml && oc apply -f namespace.yaml` | Cluster name and configuration validated, form accepts input without errors |
| 6 | Configure node pool settings | Set worker pool: name **worker-pool**, replicas **2**, compute cores **8**, memory **16Gi**, root volume size **32Gi**, storage class **ocs-storagecluster-ceph-rbd-virtualization** | Create NodePool configuration: `oc create -f nodepool.yaml` where nodepool.yaml contains: `apiVersion: hypershift.openshift.io/v1beta1 kind: NodePool metadata: name: worker-pool namespace: clusters spec: clusterName: kubevirt-test-cluster replicas: 2 management: autoRepair: false platform: type: KubeVirt kubevirt: compute: cores: 8 memory: 16Gi rootVolume: type: Persistent persistent: size: 32Gi storageClass: ocs-storagecluster-ceph-rbd-virtualization` | Node pool configuration accepted with storage class validation passed |
| 7 | Configure networking | Set cluster network CIDR **10.132.0.0/14**, service network CIDR **172.31.0.0/16**, network type **OVNKubernetes** | Apply networking configuration: `oc patch hostedcluster kubevirt-test-cluster -n clusters --type='merge' -p='{"spec":{"networking":{"clusterNetwork":[{"cidr":"10.132.0.0/14"}],"serviceNetwork":[{"cidr":"172.31.0.0/16"}],"networkType":"OVNKubernetes"}}}'` | Network configuration validated and applied to cluster specification |
| 8 | Review and create cluster | Review all configurations in summary section and click **Create** button | Apply HostedCluster resource: `oc create -f hostedcluster.yaml` where hostedcluster.yaml contains: `apiVersion: hypershift.openshift.io/v1beta1 kind: HostedCluster metadata: name: kubevirt-test-cluster namespace: clusters spec: release: image: quay.io/openshift-release-dev/ocp-release:4.14.15-x86_64 networking: clusterNetwork: - cidr: 10.132.0.0/14 serviceNetwork: - cidr: 172.31.0.0/16 networkType: OVNKubernetes platform: type: KubeVirt kubevirt: baseDomainPassthrough: true etcd: managed: storage: type: PersistentVolume persistentVolume: size: 8Gi` | Cluster creation initiated, wizard shows progress with status "Creating cluster..." |
| 9 | Verify cluster deployment status | Monitor cluster status in ACM Console clusters list, verify status progresses through **Installing** → **Available** | Check cluster status: `oc get hostedcluster kubevirt-test-cluster -n clusters -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'` and `oc get nodepool worker-pool -n clusters -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'` | Cluster appears in clusters list with deployment progress visible, eventually reaching **Available** status |

## Test Case 2: KubeVirt Hosted Cluster Configuration Validation and Error Handling

### Description
Validate the form validation logic, namespace conflict detection, and error handling capabilities in the KubeVirt hosted cluster creation UI wizard to ensure robust user experience and prevent configuration conflicts.

### Setup
- ACM environment with existing managed cluster **local-cluster**
- At least one existing hosted cluster namespace to test conflicts
- Invalid configuration scenarios prepared for testing
- Network connectivity to test external image registry validation

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> and authenticate | `oc login https://api.<cluster-host>:6443 -u <admin-user> -p <admin-password>` | ACM Console accessible with administrative privileges |
| 2 | Access cluster creation wizard | Navigate **Infrastructure** → **Clusters** → **Create cluster** → **KubeVirt** → **Hosted** | `oc get managedclusters` to list existing clusters for reference | KubeVirt hosted cluster creation wizard loaded |
| 3 | Test cluster name validation | Enter cluster name **local-cluster** (same as existing managed cluster) | Verify conflict: `oc get managedcluster local-cluster -o jsonpath='{.metadata.name}'` | Error message displayed: "The cluster name you selected is already used by an existing managed cluster" |
| 4 | Test namespace validation | Set cluster name **test-cluster**, then set namespace **test-cluster** (same as cluster name) | Check namespace rules: `oc get namespaces test-cluster --ignore-not-found` | Error message: "The namespace cannot be the same as the cluster name" |
| 5 | Test namespace conflict detection | Set namespace **local-cluster** (existing managed cluster namespace) | Verify namespace conflict: `oc get managedcluster local-cluster -o jsonpath='{.metadata.namespace}'` | Error message: "The namespace you selected is already used by an existing managed cluster" |
| 6 | Test invalid release image | Enter invalid release image URL **invalid-registry.example.com/nonexistent:latest** | Validate image accessibility: `oc image info invalid-registry.example.com/nonexistent:latest` | Image validation error with message about inaccessible or invalid image reference |
| 7 | Test resource constraint validation | Set node pool with cores **1000** (exceeding cluster capacity) | Check resource availability: `oc describe nodes \| grep -A5 "Capacity:" \| grep cpu` | Warning or error about insufficient cluster resources for requested configuration |
| 8 | Test form field clearing | Clear required field **cluster name** and attempt to proceed | Verify required field validation in UI | Form validation prevents proceeding with error highlighting missing required fields |
| 9 | Verify successful validation bypass | Correct all validation errors: cluster name **valid-test-cluster**, namespace **clusters**, valid release image, reasonable resources | Validate configuration: `oc get namespace clusters` and verify no conflicting cluster names | All validations pass, **Create** button becomes enabled and functional |

## Test Case 3: KubeVirt Hosted Cluster Resource Verification and Management Integration

### Description
Verify that the KubeVirt hosted cluster creation through ACM Console UI correctly creates the required HyperShift resources (HostedCluster, NodePool) and integrates with cluster management capabilities for ongoing operations.

### Setup
- Successfully created KubeVirt hosted cluster from previous test cases
- ACM Console access with cluster management permissions
- CLI access for resource verification
- Network connectivity for cluster API access verification

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Access cluster management | Navigate to **Infrastructure** → **Clusters** in ACM Console | `oc login https://api.<cluster-host>:6443 -u <admin-user> -p <admin-password>` | Clusters overview page showing all managed clusters including hosted clusters |
| 2 | Verify hosted cluster visibility | Locate the created **kubevirt-test-cluster** in clusters list | `oc get hostedcluster kubevirt-test-cluster -n clusters -o wide` | Hosted cluster visible with status **Available**, platform type **KubeVirt**, and API endpoint |
| 3 | Verify HostedCluster resource | Click on **kubevirt-test-cluster** to view details | `oc get hostedcluster kubevirt-test-cluster -n clusters -o yaml` | HostedCluster resource shows: kind: HostedCluster, platform.type: KubeVirt, networking configuration (clusterNetwork: 10.132.0.0/14, serviceNetwork: 172.31.0.0/16), etcd.managed.storage configuration |
| 4 | Verify NodePool resource | View node pool information in cluster details | `oc get nodepool worker-pool -n clusters -o yaml` | NodePool resource exists with: clusterName: kubevirt-test-cluster, replicas: 2, platform.type: KubeVirt, compute cores: 8, memory: 16Gi, storage configuration |
| 5 | Verify cluster API accessibility | Test cluster API connection from ACM Console cluster details | `oc get nodes --kubeconfig=<hosted-cluster-kubeconfig>` | Hosted cluster API responds, showing worker nodes in Ready state matching NodePool replica count |
| 6 | Verify storage class assignment | Check storage configuration in cluster details | `oc get pv -A \| grep kubevirt-test-cluster` and `oc get storageclass ocs-storagecluster-ceph-rbd-virtualization` | Storage volumes created using specified storage class **ocs-storagecluster-ceph-rbd-virtualization** |
| 7 | Test cluster lifecycle operations | Access cluster actions menu (hibernate, resume, destroy options) | `oc get hostedcluster kubevirt-test-cluster -n clusters -o jsonpath='{.status.conditions}'` | Cluster lifecycle operations available, status conditions show healthy operational state |
| 8 | Verify ManagedCluster creation | Check if ManagedCluster resource created for cluster import | `oc get managedcluster kubevirt-test-cluster -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'` | ManagedCluster resource exists with Available: True status, enabling cluster management through ACM |
| 9 | Verify end-to-end management | Navigate through cluster details tabs (Overview, Nodes, Add-ons) to verify full management integration | `oc get klusterletaddonconfig kubevirt-test-cluster -n kubevirt-test-cluster --ignore-not-found` | Full cluster management integration active with monitoring, logging, and add-on management capabilities accessible through ACM Console |
