# Test Cases for ACM-1766: Upgrade hypershift operator to 4.12

## Description
Comprehensive validation of HyperShift operator 4.12 functionality through hosted control plane lifecycle management, platform integration testing, and operational verification. Tests focus on validating the completed operator upgrade to ensure OpenShift 4.12 compatibility across core HyperShift capabilities including cluster creation, NodePool management, monitoring, ACM/MCE integration, and CLI operations.

## Setup
**Prerequisites:**
- Access to ACM hub cluster with HyperShift operator 4.12 installed
- Valid AWS credentials for hosted cluster provisioning
- ACM console access with cluster admin permissions
- CLI tools: oc, hcp (HyperShift CLI)
- Test namespace: hypershift-test

**Environment Access:**
```bash
# Access ACM Console
URL: https://console-openshift-console.apps.{cluster-host}
Credentials: kubeadmin / {admin-password}
```

---

## Test Case 1: Create HyperShift Hosted Cluster with OpenShift 4.12 Support

**Description**: Validate core HyperShift operator functionality for creating hosted clusters with OpenShift 4.12 support, ensuring proper platform integration and cluster lifecycle management.

**Setup**: ACM Console access with HyperShift operator 4.12 installed and AWS credentials configured for hosted cluster provisioning.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} and authenticate with cluster admin credentials | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {admin-password}` | Successfully authenticated to ACM Console with clusters page accessible |
| 2 | Navigate to Cluster Creation | Click Infrastructure → Clusters → Create cluster → Hosted control plane | `oc get pods -n hypershift \| grep hypershift-operator` | Cluster creation wizard opens with HyperShift option available, operator pod shows Running status |
| 3 | Select HyperShift Platform Configuration | Select "Hosted control plane" → Choose AWS platform → Enter cluster name: test-hypershift-412 | Create HostedCluster configuration: `touch hostedcluster.yaml` and add complete YAML with 4.12 image | Platform configuration accepts 4.12 image specification, AWS settings validate successfully |
| 4 | Configure NodePool Settings | Configure node pool → Set instance type to m5.large → Set replica count to 2 → Configure 4.12 release image | Create NodePool YAML: `touch nodepool.yaml` with 4.12 release image and AWS instance configuration | NodePool configuration validates with 4.12 image compatibility, instance settings confirm |
| 5 | Create Hosted Cluster | Review configuration → Click "Create" → Monitor cluster creation progress | Apply resources: `oc apply -f hostedcluster.yaml && oc apply -f nodepool.yaml` | Cluster creation initiates successfully, HyperShift operator begins provisioning control plane components |
| 6 | Verify Cluster Provisioning | Navigate to cluster details → Monitor status indicators → Verify "Available" status | Check HostedCluster status: `oc get hostedcluster test-hypershift-412 -n hypershift-test -o jsonpath='{.status.conditions[?(@.type=="Available")].status}'` | HostedCluster reports "Available" status, control plane components deploy with OpenShift 4.12 images |
| 7 | Validate Worker Nodes | View cluster nodes → Verify 2 worker nodes in Ready state | Check NodePool status: `oc get nodepool test-hypershift-412 -n hypershift-test -o jsonpath='{.status.readyReplicas}'` | NodePool shows 2 ready replicas, worker nodes register as Ready with 4.12 kubelet version |
| 8 | Access Hosted Cluster | Click "Open Console" → Verify OpenShift 4.12 console loads | Extract kubeconfig: `oc extract secret/admin-kubeconfig -n hypershift-test-test-hypershift-412 --to=- > test-kubeconfig` | Hosted cluster console displays OpenShift 4.12 interface, kubectl access works with extracted kubeconfig |

## Test Case 2: Validate HyperShift NodePool Scaling and Management Operations

**Description**: Test HyperShift NodePool scaling capabilities to validate operator's worker node management functionality for cost optimization and workload flexibility.

**Setup**: Existing HyperShift hosted cluster test-hypershift-412 with 2 worker nodes available for scaling operations testing.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} and authenticate | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {admin-password}` | Successfully authenticated with access to cluster management interface |
| 2 | Navigate to NodePool Management | Navigate to Clusters → test-hypershift-412 → NodePools tab | List current NodePools: `oc get nodepool -n hypershift-test` | NodePool displays current configuration with 2 replicas, management interface accessible |
| 3 | Scale NodePool Up | Click NodePool → Edit → Change replica count from 2 to 3 → Save | Scale NodePool: `oc patch nodepool test-hypershift-412 -n hypershift-test -p '{"spec":{"nodeCount":3}}' --type merge` | NodePool configuration updates to 3 replicas, scaling operation initiates |
| 4 | Monitor Scale-Up Progress | Monitor NodePool status → Watch for "Ready" state with 3/3 nodes | Watch NodePool scaling: `oc get nodepool test-hypershift-412 -n hypershift-test -w` | NodePool shows scaling progress, third worker node provisions successfully |
| 5 | Validate Node Availability | View cluster nodes → Verify 3 worker nodes in Ready state | Check node status: `KUBECONFIG=test-kubeconfig oc get nodes` | Three worker nodes show Ready status, all running OpenShift 4.12 kubelet |
| 6 | Scale NodePool Down | Edit NodePool → Change replica count from 3 to 2 → Save | Scale down: `oc patch nodepool test-hypershift-412 -n hypershift-test -p '{"spec":{"nodeCount":2}}' --type merge` | NodePool initiates scale-down operation, excess worker node termination begins |
| 7 | Verify Scale-Down Completion | Monitor NodePool until showing 2/2 Ready nodes | Verify status: `oc get nodepool test-hypershift-412 -n hypershift-test -o jsonpath='{.status.readyReplicas}'` | NodePool shows 2 ready replicas, one worker node removed cleanly, cluster remains stable |

## Test Case 3: Test HyperShift Control Plane Health Monitoring and Observability

**Description**: Validate HyperShift control plane component health monitoring capabilities to ensure proper observability and operational awareness of hosted cluster infrastructure.

**Setup**: Active HyperShift hosted cluster test-hypershift-412 with control plane components running for health monitoring validation.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} for control plane monitoring | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {admin-password}` | Successfully authenticated with access to cluster monitoring interface |
| 2 | Access Control Plane Monitoring | Navigate to Clusters → test-hypershift-412 → Control Plane tab | Check HostedCluster conditions: `oc get hostedcluster test-hypershift-412 -n hypershift-test -o yaml \| grep -A 10 conditions` | Control plane tab displays component health status, conditions show healthy state |
| 3 | Verify etcd Health | View control plane components → Check etcd status indicators | Check etcd pod status: `oc get pods -n hypershift-test-test-hypershift-412 \| grep etcd` | etcd components show healthy status, all etcd pods Running |
| 4 | Monitor API Server Availability | View API server metrics → Verify response times and availability | Test API connectivity: `KUBECONFIG=test-kubeconfig oc get --raw /healthz` | API server responds with "ok" status, latency metrics within acceptable range |
| 5 | Check Controller Manager Health | Monitor control plane components → Review controller manager status | Check logs: `oc logs -n hypershift-test-test-hypershift-412 deployment/kube-controller-manager --tail=10` | Controller manager shows active status, logs indicate normal operation |
| 6 | Validate Scheduler Functionality | View scheduler component status → Check scheduling metrics | Create test pod: `KUBECONFIG=test-kubeconfig oc run test-pod --image=nginx --restart=Never` | Scheduler shows healthy status, test pod schedules successfully to worker node |
| 7 | Monitor Resource Utilization | View resource metrics → Monitor CPU/memory usage of control plane | Check resources: `oc top pods -n hypershift-test-test-hypershift-412` | Control plane components show reasonable resource utilization, no resource starvation |

## Test Case 4: Verify HyperShift Integration with ACM Hub and MCE Platform

**Description**: Validate seamless integration between HyperShift hosted clusters and Advanced Cluster Management hub with MultiCluster Engine platform capabilities.

**Setup**: HyperShift hosted cluster test-hypershift-412 deployed and available for ACM/MCE integration testing.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} for platform integration testing | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {admin-password}` | Successfully authenticated with access to ACM cluster management features |
| 2 | Verify Cluster Registration | Navigate to Clusters → All clusters → Verify test-hypershift-412 listed | Check ManagedCluster resource: `oc get managedcluster test-hypershift-412` | Hosted cluster appears in ACM cluster list with "Available" status |
| 3 | Test Add-on Deployment | Navigate to test-hypershift-412 → Add-ons → Install application-manager | Create ManagedClusterAddOn YAML with application-manager configuration and apply | Add-on deploys successfully to hosted cluster, shows Available status |
| 4 | Configure Policy Management | Navigate to Governance → Create policy → Target test-hypershift-412 | Create and apply Policy YAML with ConfigurationPolicy for namespace creation | Policy creates successfully, applies to hosted cluster through ACM |
| 5 | Test Application Deployment | Navigate to Applications → Create application → Target test-hypershift-412 | Create Application resource YAML with ArgoCD guestbook example and apply | Application deploys successfully to hosted cluster, GitOps synchronization works |
| 6 | Verify MCE Integration | Navigate to Infrastructure → Clusters → Verify test-hypershift-412 in MCE view | Check MCE registration: `oc get clusterset -o yaml \| grep test-hypershift-412` | Hosted cluster registered with MCE, cluster lifecycle management available |

## Test Case 5: Validate HyperShift CLI Operations and API Compatibility Testing

**Description**: Test HyperShift CLI tool functionality and direct API operations to validate programmatic interface compatibility with 4.12 operator upgrade.

**Setup**: HyperShift operator 4.12 environment with hcp CLI tool available for direct cluster management operations testing.

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.{cluster-host} for CLI operations monitoring | `oc login https://api.{cluster-host}:6443 -u kubeadmin -p {admin-password}` | Successfully authenticated with access to cluster monitoring interface |
| 2 | Install HyperShift CLI | Navigate to HyperShift documentation → Download hcp CLI for platform | Install hcp CLI: `curl -LO https://github.com/openshift/hypershift/releases/latest/download/hypershift && chmod +x hypershift && mv hypershift /usr/local/bin/hcp` | hcp CLI installs successfully, version command works: `hcp version` |
| 3 | Create Cluster via CLI | Monitor cluster creation through ACM Console | Create cluster: `hcp create cluster aws --name cli-test-412 --namespace hypershift-test --base-domain test.example.com --pull-secret pullsecret.json --aws-creds aws-creds.json --region us-east-1 --generate-ssh` | hcp CLI creates HostedCluster and NodePool resources, cluster provisioning begins |
| 4 | Manage Cluster Lifecycle | Verify CLI operations reflect in ACM Console | List hosted clusters: `hcp list clusters --namespace hypershift-test` | Both UI-created and CLI-created clusters appear in list, status information accurate |
| 5 | Access Cluster Credentials | Compare credentials with Console-provided access | Generate kubeconfig: `hcp create kubeconfig --name cli-test-412 --namespace hypershift-test > cli-kubeconfig` | Generated kubeconfig provides access to hosted cluster, matches Console credentials |
| 6 | Test API Operations | Monitor API changes in ACM Console | Scale NodePool: `oc patch nodepool cli-test-412 -n hypershift-test -p '{"spec":{"nodeCount":3}}' --type merge` | API operations execute successfully, changes visible in both CLI and Console |
| 7 | Cleanup via CLI | Verify cleanup progress in ACM Console | Delete cluster: `hcp destroy cluster aws --name cli-test-412 --namespace hypershift-test` | CLI deletion removes all cluster resources cleanly, no orphaned resources remain |