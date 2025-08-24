# Test Cases: HyperShift Operator 4.12 Validation

## Test Case 1: Create HyperShift Hosted Cluster with OpenShift 4.12

**Description**: Validate HyperShift operator ability to create hosted clusters with OpenShift 4.12 support, testing core operator functionality and platform integration.

**Setup**: Access to ACM hub cluster with HyperShift operator installed. Ensure AWS credentials are configured for hosted cluster creation.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} and authenticate with cluster admin credentials | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {admin-password}` | Successfully authenticated to cluster console |
| 2 | Navigate to Infrastructure | Click Infrastructure → Clusters in left navigation menu | `oc get managedclusters` | Clusters page displayed with existing managed clusters list |
| 3 | Initiate Cluster Creation | Click "Create cluster" button → Select "Red Hat OpenShift Hosted control plane" | `oc create namespace hosted-cluster-demo` | HyperShift cluster creation wizard opens |
| 4 | Configure Hosted Cluster | Fill cluster name: "hypershift-412-test", select OpenShift 4.12.x version, choose AWS provider | Create HostedCluster manifest: `oc apply -f -` with ```yaml\napiVersion: hypershift.openshift.io/v1beta1\nkind: HostedCluster\nmetadata:\n  name: hypershift-412-test\n  namespace: clusters\nspec:\n  release:\n    image: quay.io/openshift-release-dev/ocp-release:4.12.x-x86_64\n  platform:\n    type: AWS\n    aws:\n      region: us-east-1\n      cloudProvider:\n        zone: us-east-1a\n  networking:\n    networkType: OVNKubernetes\n``` | Cluster configuration accepted, creation process initiated |
| 5 | Configure NodePool | Set worker node count: 2, instance type: m5.large, availability zone: us-east-1a | Create NodePool manifest: `oc apply -f -` with ```yaml\napiVersion: hypershift.openshift.io/v1beta1\nkind: NodePool\nmetadata:\n  name: hypershift-412-test-workers\n  namespace: clusters\nspec:\n  clusterName: hypershift-412-test\n  replicas: 2\n  platform:\n    type: AWS\n    aws:\n      instanceType: m5.large\n      instanceProfile: hypershift-412-test-worker\n      subnet:\n        id: subnet-xxxxxxxxx\n``` | NodePool configuration created successfully |
| 6 | Validate Cluster Creation | Monitor cluster status in console, verify "Installing" then "Ready" status | `oc get hostedcluster hypershift-412-test -n clusters -w` | Cluster transitions through Installing → Ready status |
| 7 | Verify OpenShift 4.12 | Access hosted cluster console → Help → About to confirm version | `oc --kubeconfig=hypershift-412-test-kubeconfig get clusterversion` | OpenShift version displays 4.12.x, cluster operational |

## Test Case 2: Validate HyperShift NodePool Scaling Operations

**Description**: Test NodePool scaling functionality to ensure HyperShift operator correctly manages worker node lifecycle operations with 4.12 compatibility.

**Setup**: Existing HyperShift hosted cluster created with initial NodePool configuration.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Access Cluster Details | Navigate to Infrastructure → Clusters → Select "hypershift-412-test" cluster | `oc get nodepool hypershift-412-test-workers -n clusters` | Cluster details page shows current NodePool configuration |
| 2 | Navigate to Node Pools | Click "Node pools" tab in cluster details view | `oc describe nodepool hypershift-412-test-workers -n clusters` | NodePool management interface displayed with current nodes |
| 3 | Scale Up NodePool | Click "Scale node pool" → Increase replica count from 2 to 4 | `oc patch nodepool hypershift-412-test-workers -n clusters --type='merge' -p='{"spec":{"replicas":4}}'` | NodePool scaling operation initiated successfully |
| 4 | Monitor Scaling Progress | Watch node pool status in console, observe "Scaling" status | `oc get nodepool hypershift-412-test-workers -n clusters -w` | NodePool status shows "Scaling" then "Ready" with 4 replicas |
| 5 | Verify New Nodes | Check hosted cluster nodes list, confirm 4 worker nodes present | Connect to hosted cluster: `oc --kubeconfig=hypershift-412-test-kubeconfig get nodes` | 4 worker nodes displayed in Ready status |
| 6 | Scale Down NodePool | Return to console → Scale node pool → Reduce to 3 replicas | `oc patch nodepool hypershift-412-test-workers -n clusters --type='merge' -p='{"spec":{"replicas":3}}'` | Scaling down operation accepted |
| 7 | Validate Final State | Confirm node pool shows 3 replicas, excess node terminated gracefully | `oc --kubeconfig=hypershift-412-test-kubeconfig get nodes` | 3 worker nodes remain, 1 node properly terminated |

## Test Case 3: Test HyperShift Control Plane Health Monitoring

**Description**: Validate HyperShift operator's control plane monitoring capabilities and health validation features with OpenShift 4.12 components.

**Setup**: Active HyperShift hosted cluster with running control plane components.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Access Control Plane View | Navigate to cluster details → "Control plane" tab | `oc get pods -n clusters-hypershift-412-test` | Control plane component overview displayed |
| 2 | Monitor Component Health | Review etcd, API server, controller manager status indicators | `oc describe hostedcontrolplane hypershift-412-test -n clusters-hypershift-412-test` | All components show healthy status with green indicators |
| 3 | Check API Server Metrics | Click on "API server" component → View metrics and logs | `oc logs deployment/kube-apiserver -n clusters-hypershift-412-test` | API server metrics show normal operation, no errors |
| 4 | Validate etcd Health | Select etcd component → Check cluster health status | `oc exec -n clusters-hypershift-412-test deployment/etcd -- etcdctl cluster-health` | etcd cluster reports healthy status with all members |
| 5 | Test Control Plane Connectivity | From hosted cluster: Test API connectivity and authentication | `oc --kubeconfig=hypershift-412-test-kubeconfig cluster-info` | Cluster API endpoint responds with service information |
| 6 | Verify 4.12 Component Versions | Check component versions match OpenShift 4.12 release | `oc get deployment kube-apiserver -n clusters-hypershift-412-test -o yaml \| grep image:` | All components show 4.12.x image versions |
| 7 | Validate Monitoring Integration | Check if control plane metrics appear in ACM observability | `oc get servicemonitor -n clusters-hypershift-412-test` | ServiceMonitor resources present for metrics collection |

## Test Case 4: Validate HyperShift Integration with ACM/MCE

**Description**: Test HyperShift operator integration with Advanced Cluster Management and MultiCluster Engine components to ensure seamless platform functionality.

**Setup**: ACM hub cluster with MCE installed and HyperShift operator configured for integration.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Verify MCE Integration | Navigate to Infrastructure → MultiCluster Engine overview | `oc get multiclusterengine multiclusterengine-sample` | MCE status shows HyperShift provider enabled |
| 2 | Check Hosted Cluster Registration | Go to Infrastructure → Clusters, verify hosted cluster appears | `oc get managedcluster hypershift-412-test` | Hosted cluster registered as managed cluster in ACM |
| 3 | Validate Add-on Deployment | Click cluster → Add-ons tab, check HyperShift add-on status | `oc get managedclusteraddons -n hypershift-412-test` | HyperShift add-ons deployed and available status |
| 4 | Test Policy Deployment | Navigate to Governance → Create policy targeting hosted cluster | Create ConfigurationPolicy: `oc apply -f -` with ```yaml\napiVersion: policy.open-cluster-management.io/v1\nkind: Policy\nmetadata:\n  name: hypershift-test-policy\n  namespace: default\nspec:\n  remediationAction: inform\n  disabled: false\n  policy-templates:\n  - objectDefinition:\n      apiVersion: policy.open-cluster-management.io/v1\n      kind: ConfigurationPolicy\n      metadata:\n        name: test-config\n      spec:\n        object-templates:\n        - complianceType: musthave\n          objectDefinition:\n            apiVersion: v1\n            kind: Namespace\n            metadata:\n              name: test-hypershift\n``` | Policy successfully deployed to hosted cluster |
| 5 | Verify Application Deployment | Applications → Create application targeting hosted cluster | `oc apply -n argocd -f -` with ```yaml\napiVersion: argoproj.io/v1alpha1\nkind: Application\nmetadata:\n  name: hypershift-test-app\nspec:\n  project: default\n  source:\n    repoURL: https://github.com/stolostron/application-samples\n    path: book-import\n    targetRevision: main\n  destination:\n    server: https://api.hypershift-412-test.example.com:6443\n    namespace: book-import\n``` | Application successfully deployed to hosted cluster through ACM |
| 6 | Monitor Cluster Insights | Check cluster insights and recommendations in ACM console | `oc get clusterrecommendations -n hypershift-412-test` | Cluster insights and recommendations displayed for hosted cluster |

## Test Case 5: Test HyperShift Upgrade and Maintenance Operations

**Description**: Validate HyperShift operator's ability to perform upgrade operations and maintenance tasks on hosted clusters with 4.12 components.

**Setup**: Operational HyperShift hosted cluster ready for upgrade testing.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Check Current Version | Navigate to cluster details → Overview tab, note current version | `oc get hostedcluster hypershift-412-test -n clusters -o jsonpath='{.spec.release.image}'` | Current cluster version 4.12.x displayed |
| 2 | Access Upgrade Options | Click cluster Actions → "Upgrade cluster" option | `oc get clusterversion -o yaml --kubeconfig=hypershift-412-test-kubeconfig` | Available upgrade versions listed |
| 3 | Pause Reconciliation | Select "Pause reconciliation" from cluster actions | `oc annotate hostedcluster hypershift-412-test -n clusters hypershift.openshift.io/paused="true"` | Cluster reconciliation paused successfully |
| 4 | Verify Pause Status | Check cluster status shows "Paused" indicator | `oc get hostedcluster hypershift-412-test -n clusters -o jsonpath='{.metadata.annotations}'` | Cluster displays paused status with annotation |
| 5 | Resume Operations | Click "Resume reconciliation" to restore normal operations | `oc annotate hostedcluster hypershift-412-test -n clusters hypershift.openshift.io/paused-` | Reconciliation resumed, normal operations restored |
| 6 | Restart Control Plane | Use "Restart control plane" option for maintenance testing | `oc delete pods -n clusters-hypershift-412-test -l app=kube-apiserver` | Control plane components restart successfully |
| 7 | Validate Post-Restart | Verify cluster returns to Ready status after restart | `oc get hostedcluster hypershift-412-test -n clusters` | Cluster status returns to Ready, all components operational |

## Test Case 6: Validate HyperShift CLI Tools and API Compatibility

**Description**: Test HyperShift command-line tools (hcp CLI) and API operations to ensure 4.12 compatibility and full functionality.

**Setup**: HyperShift CLI tools installed and configured for cluster operations.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Verify HCP CLI Installation | Console Settings → Command line tools → Download hcp CLI | `hcp version` | HCP CLI version information displayed |
| 2 | List Hosted Clusters | Use console cluster list as reference | `hcp list clusters --namespace clusters` | All hosted clusters listed with status information |
| 3 | Create Cluster via CLI | N/A (CLI-focused test) | `hcp create cluster aws --name cli-test-412 --release-image quay.io/openshift-release-dev/ocp-release:4.12.x-x86_64 --node-pool-replicas 2` | Cluster creation initiated through CLI |
| 4 | Monitor CLI Creation | Track progress in console for comparison | `hcp list clusters --namespace clusters \| grep cli-test-412` | CLI-created cluster appears with Installing status |
| 5 | Inspect Cluster Details | Compare console details with CLI output | `hcp describe cluster cli-test-412 --namespace clusters` | Detailed cluster information matches console view |
| 6 | Delete Test Cluster | Use console confirmation for safety | `hcp delete cluster cli-test-412 --namespace clusters` | CLI cluster deletion initiated successfully |
| 7 | Verify API Operations | Test direct API calls for advanced operations | `oc get hostedcluster -n clusters -o json \| jq '.items[].status.conditions'` | API returns detailed status conditions for all clusters |