# Test Cases: ACM-22079 - Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Test Case 1: ClusterCurator Non-Recommended Upgrade with Digest Resolution

**Description**: Verify that ClusterCurator can successfully perform upgrades to non-recommended OpenShift versions using image digests when the annotation is enabled.

**Setup**: 
- ACM hub cluster with ClusterCurator controller deployed
- Managed cluster running OpenShift 4.16.36 (or earlier version with known non-recommended update path)
- Network access to Cincinnati conditional updates API for digest resolution

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to the ACM hub cluster. Terminal shows successful login message with cluster information and current project. |
| **Step 2: Verify managed cluster current version** - Check the current OpenShift version of the target managed cluster: `oc get managedcluster <managed-cluster-name> -o jsonpath='{.status.version.openshift}'` | Current OpenShift version is displayed (example: 4.16.36). This confirms the starting point for the upgrade test and validates the managed cluster is properly connected to ACM. |
| **Step 3: Identify non-recommended upgrade target** - Research available non-recommended versions from the current version: `oc get clusterversion -o jsonpath='{.status.availableUpdates}' --kubeconfig=<managed-cluster-kubeconfig>` | List of available updates including non-recommended versions is displayed. Example output showing version 4.16.37 with conditional update warnings or restrictions. |
| **Step 4: Create ClusterCurator with non-recommended annotation** - Apply ClusterCurator resource with special annotation: `oc apply -f clustercurator-nonrecommended.yaml` | ClusterCurator resource created successfully in the managed cluster namespace. YAML content includes the annotation `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'` and desiredUpdate field set to non-recommended version. |
| **Step 5: Monitor ClusterCurator job creation** - Watch for curator job to be created: `oc get jobs -n <managed-cluster-namespace> -w` | Curator job appears with name pattern `curator-job-<random>`. Job status shows Running state indicating the upgrade process has started. |
| **Step 6: Verify digest resolution in curator job logs** - Check curator job logs for digest lookup activity: `oc logs job/<curator-job-name> -c activate-and-monitor -n <managed-cluster-namespace>` | Logs show successful digest resolution from conditional updates API. Messages indicate digest found for target version and image digest being used instead of image tag for upgrade. |
| **Step 7: Validate managed cluster ClusterVersion update** - Check ClusterVersion resource on managed cluster shows digest usage: `oc get clusterversion -o yaml --kubeconfig=<managed-cluster-kubeconfig>` | ClusterVersion spec.desiredUpdate.image field contains image digest (sha256:...) rather than version tag. This confirms digest-based upgrade mechanism is working correctly. |
| **Step 8: Monitor upgrade progress** - Track the upgrade progress on managed cluster: `oc get clusterversion -o jsonpath='{.status.conditions[?(@.type=="Progressing")]}' --kubeconfig=<managed-cluster-kubeconfig>` | Upgrade progress condition shows status "True" with progression messages. Upgrade proceeds normally using the resolved image digest instead of failing due to non-recommended version restrictions. |

## Test Case 2: ClusterCurator Fallback to Image Tag When Digest Not Available

**Description**: Verify that ClusterCurator falls back to using image tag when image digest cannot be resolved from conditional updates API.

**Setup**:
- ACM hub cluster with ClusterCurator controller
- Managed cluster with internet connectivity issues or non-standard version that may not have digest in conditional updates
- ClusterCurator configured for non-recommended upgrade

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful authentication to ACM hub cluster with confirmation message and cluster context information displayed. |
| **Step 2: Create ClusterCurator with limited digest access** - Apply ClusterCurator targeting version with limited digest availability: `oc apply -f clustercurator-fallback-test.yaml` | ClusterCurator resource created successfully. Configuration includes non-recommended annotation and targets version that may not have readily available digest in conditional updates. |
| **Step 3: Monitor curator job digest resolution attempts** - Track digest lookup attempts in curator job logs: `oc logs job/<curator-job-name> -c activate-and-monitor -n <managed-cluster-namespace> -f` | Logs show digest lookup attempts to conditional updates API. Warning or info messages indicate digest not found for target version, initiating fallback to image tag approach. |
| **Step 4: Verify fallback to image tag usage** - Check that image tag is used when digest unavailable: `oc get clusterversion -o jsonpath='{.spec.desiredUpdate.version}' --kubeconfig=<managed-cluster-kubeconfig>` | ClusterVersion shows version number (e.g., 4.16.37) in desiredUpdate.version field instead of image digest, confirming successful fallback mechanism when digest resolution fails. |
| **Step 5: Validate upgrade continues with tag** - Monitor upgrade progress with image tag approach: `oc get clusterversion -o jsonpath='{.status.history[0]}' --kubeconfig=<managed-cluster-kubeconfig>` | Upgrade proceeds using version tag. History shows the target version being applied and upgrade progress continuing normally despite digest resolution failure. |

## Test Case 3: ClusterCurator Upgrade Validation in Disconnected Environment

**Description**: Test ClusterCurator digest-based upgrade functionality in disconnected environment scenario (primary use case for Amadeus customer).

**Setup**:
- ACM hub cluster in disconnected environment  
- Managed cluster with restricted internet access
- Local image registry with mirrored OpenShift images including digests
- ClusterCurator configured for non-recommended upgrade

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the disconnected ACM hub cluster: `oc login <cluster-api-url> --username=<username> --password=<password> --insecure-skip-tls-verify=true` | Successful login to disconnected environment hub cluster. Network isolation confirmed and cluster accessibility verified within disconnected network boundaries. |
| **Step 2: Verify image registry configuration** - Check that local registry contains required images: `oc get imagecontentsourcepolicy -o yaml` | ImageContentSourcePolicy resources show proper mirror configuration mapping external OpenShift images to local registry. Registry mirrors configured for release images with digest mappings. |
| **Step 3: Create ClusterCurator for disconnected upgrade** - Apply ClusterCurator with mirror registry configuration: `oc apply -f clustercurator-disconnected.yaml` | ClusterCurator created successfully with annotation for non-recommended versions and mirror registry configuration. Resource includes proper image pull specifications for disconnected environment. |
| **Step 4: Monitor digest resolution in disconnected mode** - Track how digest resolution works without internet access: `oc logs job/<curator-job-name> -c activate-and-monitor -n <managed-cluster-namespace>` | Logs show successful digest resolution using local mirror registry metadata. Messages confirm digest found in local registry and image digest being used for upgrade in disconnected environment. |
| **Step 5: Validate managed cluster uses mirrored digest** - Verify ClusterVersion references local registry digest: `oc get clusterversion -o jsonpath='{.spec.desiredUpdate.image}' --kubeconfig=<managed-cluster-kubeconfig>` | ClusterVersion shows image digest pointing to local mirror registry (e.g., local-registry.com/openshift/release@sha256:...) confirming proper disconnected environment upgrade configuration. |
| **Step 6: Confirm upgrade success in isolation** - Monitor upgrade completion in disconnected environment: `oc get clusterversion -o jsonpath='{.status.version}' --kubeconfig=<managed-cluster-kubeconfig>` | Upgrade completes successfully showing target version (e.g., 4.16.37) in status.version field. Disconnected environment upgrade achieved using digest-based approach without external connectivity requirements. |