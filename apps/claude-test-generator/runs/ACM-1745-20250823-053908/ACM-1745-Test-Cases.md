# Test Cases for ACM-1745: Implement upgrade modal for AWS HyperShift clusters

## Test Case 1: Validate HyperShift Upgrade Modal Access and Availability

**Description**: Verify that the HyperShift upgrade modal is accessible from the ACM console and displays correctly for HyperShift clusters.

**Setup**: 
- Access to ACM console with HyperShift clusters available
- User has cluster management permissions
- At least one AWS HyperShift cluster present in the environment

### Test Steps

| Step | Description | UI Method | CLI Method | Expected Results |
|------|-------------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> and authenticate with provided credentials | oc login https://api.<cluster-host>:6443 -u <username> -p <password> --insecure-skip-tls-verify=true | Successful authentication and access to ACM dashboard |
| 2 | Navigate to Clusters page | Click on "Infrastructure" → "Clusters" in the left navigation menu | oc get managedclusters | Clusters page displays with list of managed clusters including HyperShift clusters |
| 3 | Locate HyperShift cluster | Find a cluster with "HyperShift" label or type indicator in the clusters table | oc get managedclusters -l cluster.open-cluster-management.io/clusterset=hypershift | HyperShift cluster visible with appropriate indicators |
| 4 | Access cluster actions | Click on the three-dot menu (⋮) next to the HyperShift cluster name | oc get hostedclusters -A | Cluster actions dropdown menu appears with upgrade option available |
| 5 | Open upgrade modal | Click "Upgrade cluster" from the actions menu | N/A (UI-specific functionality) | HyperShift upgrade modal opens showing control plane and node pool upgrade options |

## Test Case 2: Test HyperShift Control Plane Upgrade Workflow

**Description**: Verify the control plane upgrade functionality within the HyperShift upgrade modal.

**Setup**: 
- HyperShift upgrade modal is accessible and functional
- Control plane has available upgrade versions
- User has upgrade permissions for the cluster

### Test Steps

| Step | Description | UI Method | CLI Method | Expected Results |
|------|-------------|-----------|------------|------------------|
| 1 | Open HyperShift upgrade modal | Follow Test Case 1 steps 1-5 to access the upgrade modal | oc get hostedcluster <cluster-name> -n <namespace> -o yaml | Modal displays with control plane and node pool sections |
| 2 | Review control plane current version | Examine the "Control Plane" section showing current version and available upgrades | oc get hostedcluster <cluster-name> -n <namespace> -o jsonpath='{.status.version.history[0].version}' | Current control plane version displayed accurately |
| 3 | Select control plane upgrade version | Choose an available upgrade version from the control plane dropdown | oc patch hostedcluster <cluster-name> -n <namespace> --type='merge' -p='{"spec":{"release":{"image":"<new-version-image>"}}}' | Version selection updates in the modal interface |
| 4 | Initiate control plane upgrade | Click "Upgrade" button for control plane section | oc get hostedcluster <cluster-name> -n <namespace> -w | Upgrade process begins with progress indicators shown |
| 5 | Verify upgrade status | Monitor the upgrade progress and completion status | oc get hostedcluster <cluster-name> -n <namespace> -o jsonpath='{.status.conditions[?(@.type=="Available")].status}' | Upgrade status shows "In Progress" then "Complete" with new version |

## Test Case 3: Verify HyperShift Node Pool Upgrade Process

**Description**: Test the node pool upgrade functionality separate from control plane upgrades.

**Setup**: 
- HyperShift cluster with node pools available for upgrade
- Node pool upgrade permissions
- Different versions available for node pool upgrades

### Test Steps

| Step | Description | UI Method | CLI Method | Expected Results |
|------|-------------|-----------|------------|------------------|
| 1 | Access node pool upgrade section | Open HyperShift upgrade modal and navigate to "Node Pools" section | oc get nodepools -n <namespace> | Node pools section displays with current versions and available upgrades |
| 2 | Review node pool configuration | Examine current node pool versions and available upgrade options | oc get nodepool <nodepool-name> -n <namespace> -o yaml | Node pool details show current version, instance types, and upgrade availability |
| 3 | Select node pool for upgrade | Choose a specific node pool and select target upgrade version | oc patch nodepool <nodepool-name> -n <namespace> --type='merge' -p='{"spec":{"release":{"image":"<upgrade-version>"}}}' | Node pool selected with upgrade version specified |
| 4 | Configure upgrade settings | Set upgrade parameters such as rolling update strategy and timing | oc patch nodepool <nodepool-name> -n <namespace> --type='merge' -p='{"spec":{"management":{"upgradeType":"Replace"}}}' | Upgrade configuration applied with specified parameters |
| 5 | Execute node pool upgrade | Click "Upgrade" for the selected node pool | oc get nodepool <nodepool-name> -n <namespace> -w | Node pool upgrade initiates with progress tracking |
| 6 | Monitor upgrade completion | Track upgrade progress until completion | oc get nodes --selector=nodepool=<nodepool-name> | All node pool nodes successfully upgraded to target version |

## Test Case 4: Validate Managed HCP Cluster Upgrade Restrictions

**Description**: Verify that upgrade restrictions are properly enforced for managed HCP clusters (ROSA HCP imported to ACM).

**Setup**: 
- Managed HCP cluster imported to ACM (ROSA HCP or similar)
- User attempts to access upgrade functionality
- Recent restriction implementation (ACM-19723) active

### Test Steps

| Step | Description | UI Method | CLI Method | Expected Results |
|------|-------------|-----------|------------|------------------|
| 1 | Identify managed HCP cluster | Locate a ROSA HCP or other managed HCP cluster in the clusters list | oc get managedclusters -l cluster.open-cluster-management.io/created-via=hypershift | Managed HCP cluster identified with appropriate labels |
| 2 | Attempt to access cluster actions | Click on the actions menu for the managed HCP cluster | oc get hostedcluster <cluster-name> -n <namespace> 2>/dev/null \|\| echo "HostedCluster resource not present" | Actions menu appears but upgrade option may be disabled or missing |
| 3 | Verify upgrade restriction | Check if "Upgrade cluster" option is available or disabled | N/A (UI-specific behavior) | Upgrade option either disabled or shows appropriate restriction message |
| 4 | Validate restriction message | If upgrade is attempted, verify appropriate error or warning message | N/A (UI-specific validation) | Clear message indicates upgrade not available for managed HCP clusters |
| 5 | Confirm cluster management scope | Verify other cluster management functions remain available | oc get managedcluster <cluster-name> -o jsonpath='{.metadata.labels}' | Other management functions accessible while upgrade is restricted |