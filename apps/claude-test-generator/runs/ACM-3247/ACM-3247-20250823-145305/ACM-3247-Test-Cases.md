# ACM-3247 Test Cases: OpenStack Custom CA Support

## Test Case 1: Validate OpenStack Credential Creation with Custom CA Certificate

**Description**: Verify that OpenStack credentials can be successfully created with custom CA certificate support through the ACM Console, including proper certificate validation and storage.

**Setup**: 
- Access ACM Console with admin privileges
- Prepare sample OpenStack clouds.yaml configuration
- Prepare custom CA certificate in PEM format
- Ensure OpenStack environment credentials are available

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.CLUSTER_HOST and authenticate with admin credentials | oc login --token=TOKEN --server=https://api.CLUSTER_HOST:6443 | Successful access to ACM Console dashboard with cluster management options visible |
| 2 | Navigate to Credentials page | Click Infrastructure → Credentials in left navigation menu | oc get secrets -A --field-selector type=Opaque | Credentials page displays with existing credentials list and "Add credential" button available |
| 3 | Initiate OpenStack credential creation | Click "Add credential" button, select "OpenStack" from cloud provider options | oc create secret generic openstack-creds --namespace=NAMESPACE --dry-run=client -o yaml | OpenStack credential creation form opens with required fields: Name, Namespace, clouds.yaml, Cloud name, CA certificate |
| 4 | Configure basic credential information | Enter credential name: "openstack-ca-test", select namespace: "open-cluster-management", enter base domain: "example.com" | Set CREDENTIAL_NAME="openstack-ca-test" and NAMESPACE="open-cluster-management" | Basic information accepted with validation success indicators |
| 5 | Configure OpenStack clouds.yaml | Paste clouds.yaml content with OpenStack authentication details in textarea field | Create clouds.yaml file with content: clouds:\n  openstack:\n    auth:\n      auth_url: https://keystone.example.com:5000/v3\n      username: testuser\n      password: testpass\n      project_name: testproject\n      user_domain_name: Default\n      project_domain_name: Default | clouds.yaml content accepted and parsed successfully with no validation errors |
| 6 | Configure cloud name | Enter cloud name: "openstack" matching the cloud entry in clouds.yaml | Set CLOUD_NAME="openstack" | Cloud name validated against clouds.yaml entries |
| 7 | Add custom CA certificate | Paste custom CA certificate PEM content in "CA Certificate" field | Create ca-cert.pem file with certificate content: -----BEGIN CERTIFICATE-----\nMIIC...certificate_content...\n-----END CERTIFICATE----- | CA certificate content accepted with PEM format validation success |
| 8 | Complete credential creation | Click "Add" button to create the credential | oc apply -f credential-manifest.yaml | Credential created successfully with confirmation message and redirect to credentials list |
| 9 | Verify credential in console | Locate "openstack-ca-test" credential in list and click to view details | oc get secret openstack-ca-test -n open-cluster-management -o yaml | Credential appears in list with "OpenStack" type and shows CA certificate field populated |
| 10 | Validate CA certificate storage | Verify CA certificate is stored in the credential secret | oc get secret openstack-ca-test -n open-cluster-management -o jsonpath='{.data.os_ca_bundle}' | base64 encode | Secret contains os_ca_bundle field with base64-encoded CA certificate matching the uploaded content |

## Test Case 2: Verify Custom CA Certificate Integration in OpenStack ClusterDeployment

**Description**: Validate that OpenStack credentials with custom CA certificates are properly integrated into ClusterDeployment resources for cluster provisioning workflows.

**Setup**:
- OpenStack credential with custom CA certificate already created
- ClusterDeployment template prepared for OpenStack
- Access to cluster provisioning workflows

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.CLUSTER_HOST and authenticate | oc login --token=TOKEN --server=https://api.CLUSTER_HOST:6443 | Access to ACM Console with cluster management capabilities |
| 2 | Navigate to cluster creation | Click Infrastructure → Clusters, then "Create cluster" button | oc get clusterdeployments -A | Cluster creation wizard opens with cloud provider selection |
| 3 | Select OpenStack provider | Choose "OpenStack" from cloud provider options | Set CLOUD_PROVIDER="OpenStack" | OpenStack cluster creation form loads with credential selection |
| 4 | Select credential with CA certificate | Choose "openstack-ca-test" credential from dropdown | Set CREDENTIAL_NAME="openstack-ca-test" | Credential selected with CA certificate information displayed |
| 5 | Configure cluster details | Enter cluster name: "test-cluster-ca", select OpenStack flavor and network settings | Configure cluster manifest with name: test-cluster-ca | Cluster configuration accepted with OpenStack-specific options populated |
| 6 | Verify CA certificate reference | Review cluster configuration to ensure CA certificate is referenced | oc get clusterdeployment test-cluster-ca -o yaml | grep -A5 "caBundle\|certificateAuthorities" | ClusterDeployment spec includes CA certificate reference in platform.openstack.certificateAuthorities or similar field |
| 7 | Validate Secret creation | Check that CA Secret is created for cluster provisioning | oc get secret test-cluster-ca-ca-bundle -n CLUSTER_NAMESPACE | CA certificate Secret created with proper CA bundle content for cluster installation |
| 8 | Check ClusterDeployment status | Monitor ClusterDeployment status for proper CA certificate handling | oc get clusterdeployment test-cluster-ca -o jsonpath='{.status.conditions}' | ClusterDeployment shows no certificate validation errors in status conditions |
| 9 | Verify install configuration | Review install-config Secret for CA certificate inclusion | oc get secret test-cluster-ca-install-config -o yaml | grep -A10 "additionalTrustBundle\|certificateAuthorities" | Install configuration includes CA certificate in additionalTrustBundle or certificateAuthorities section |
| 10 | Validate cluster provisioning readiness | Confirm cluster is ready for provisioning with CA certificate support | oc get clusterdeployment test-cluster-ca -o jsonpath='{.status.installerImage}' | ClusterDeployment configured correctly with installer image and CA certificate integration ready |

## Test Case 3: Test OpenStack Credential CA Certificate Validation and Error Handling

**Description**: Verify proper validation and error handling for custom CA certificates in OpenStack credentials, including invalid certificate formats and missing certificate scenarios.

**Setup**:
- Access to ACM Console credential creation
- Sample invalid CA certificate content
- Valid clouds.yaml configuration

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.CLUSTER_HOST and authenticate | oc login --token=TOKEN --server=https://api.CLUSTER_HOST:6443 | Successful authentication with credential management access |
| 2 | Navigate to credential creation | Click Infrastructure → Credentials → "Add credential" → "OpenStack" | oc create secret generic test-validation --dry-run=client -o yaml | OpenStack credential form opens with all required fields |
| 3 | Test invalid CA certificate format | Enter basic info, add clouds.yaml, then paste invalid certificate content (missing BEGIN/END tags) | Create invalid-ca.pem with content: "INVALID CERTIFICATE CONTENT" | Validation error displayed: "Invalid PEM format. Certificate must begin with -----BEGIN CERTIFICATE----- and end with -----END CERTIFICATE-----" |
| 4 | Test malformed PEM certificate | Replace with malformed PEM certificate (corrupted base64 content) | Set INVALID_CERT with malformed base64 content | Validation error shown: "Invalid certificate format. Unable to parse PEM certificate content" |
| 5 | Test valid certificate format | Replace with properly formatted CA certificate in PEM format | Use valid CA certificate: -----BEGIN CERTIFICATE-----\nValid_base64_content...\n-----END CERTIFICATE----- | Certificate validation passes with success indicator |
| 6 | Verify clouds.yaml CA reference validation | Use clouds.yaml that references CA file not matching provided certificate | Configure clouds.yaml with cacert: /path/to/different-ca.pem | Warning message: "CA certificate provided doesn't match cacert reference in clouds.yaml. Ensure certificate content matches the specified path" |
| 7 | Test clouds.yaml without CA reference | Use clouds.yaml without cacert specification but provide CA certificate | Create clouds.yaml without cacert field but include CA certificate | Information message: "CA certificate provided will be available for cluster provisioning even though not referenced in clouds.yaml" |
| 8 | Validate empty CA certificate field | Leave CA certificate field empty with standard clouds.yaml | Do not include ca-cert.pem in manifest | Credential created successfully without CA certificate, standard OpenStack validation applies |
| 9 | Test credential creation completion | Complete credential creation with valid CA certificate | oc apply -f openstack-credential-ca.yaml | Credential "openstack-validation-test" created successfully with CA certificate properly stored |
| 10 | Verify error persistence | Attempt to edit credential with invalid CA certificate | oc patch secret openstack-validation-test --patch='{"data":{"os_ca_bundle":"invalid_content"}}' | Edit operation blocked with validation error, existing valid certificate preserved |