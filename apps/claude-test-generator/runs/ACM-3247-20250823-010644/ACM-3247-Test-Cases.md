# Test Cases for ACM-3247: OpenStack Custom CA Support

## Test Case 1: Create OpenStack Credential with Custom CA Certificate

### Description
Test the end-to-end creation of OpenStack credentials using custom Certificate Authority (CA) certificates through ACM Console and CLI methods. This test validates the new CA field functionality that enables users to configure custom certificate authorities for OpenStack cluster provisioning without manual configuration steps.

### Setup
- Access to ACM Console at https://console-openshift-console.apps.{cluster-host}
- Valid OpenStack environment details (auth URL, username, password, project details)
- Custom CA certificate content available for testing
- CLI access with oc command configured

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|---------|-----------|------------|------------------|
| 1 | Log into ACM Console | Access ACM Console for OpenStack credential creation: Navigate to https://console-openshift-console.apps.{cluster-host} | `oc login https://api.{cluster-host}:6443` then access Console | Successfully logged into ACM Console with dashboard visible |
| 2 | Navigate to Credentials | Go to Credentials → Create credential → Cloud provider: OpenStack | `oc login https://api.{cluster-host}:6443` then access Console | OpenStack credential creation form displayed with all required fields including new CA field |
| 3 | Configure basic credential details | Fill in credential name, namespace, auth URL, username, password, project name, and domain name in the form | Create credential YAML file: `touch openstack-credential.yaml` and add:  ```yaml  apiVersion: v1  kind: Secret  metadata:    name: openstack-credential    namespace: default    labels:      cluster.open-cluster-management.io/type: "openstack"  type: Opaque  stringData:    clouds.yaml: |      clouds:        openstack:          auth:            auth_url: "https://openstack.example.com:5000/v3"            username: "admin"            password: "password123"            project_name: "test-project"            user_domain_name: "Default"            project_domain_name: "Default"  ``` | Basic OpenStack credential fields populated correctly, CA field visible and empty |
| 4 | Add Custom CA Certificate | Locate the "CA Certificate" field and paste the custom CA certificate content (PEM format) | Update credential YAML to include CA certificate:  ```yaml  stringData:    clouds.yaml: |      clouds:        openstack:          auth:            auth_url: "https://openstack.example.com:5000/v3"            username: "admin"            password: "password123"            project_name: "test-project"            user_domain_name: "Default"            project_domain_name: "Default"          cacert: |            -----BEGIN CERTIFICATE-----            MIIDXTCCAkWgAwIBAgIJAKL0UG+8G0KJMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV            BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX            -----END CERTIFICATE-----  ``` | CA certificate content accepted and displayed in form, no validation errors |
| 5 | Validate and create credential | Click "Create" button to save the credential | Apply credential: `oc apply -f openstack-credential.yaml` | Credential created successfully, appears in credentials list with OpenStack type and CA certificate configured |
| 6 | Verify credential details | Click on created credential to view details and confirm CA certificate is stored | View credential details: `oc get secret openstack-credential -o yaml` | Credential details show complete configuration including CA certificate in clouds.yaml format, ready for cluster deployment |

## Test Case 2: Validate OpenStack Credential CA Integration with Cluster Creation

### Description  
Test the integration of custom CA certificates during OpenStack cluster creation process. This test validates that CA certificates from credentials are properly integrated into cluster deployment specifications and that the system creates appropriate Secrets referencing the CA during cluster provisioning.

### Setup
- OpenStack credential with custom CA certificate already created (from Test Case 1)
- Access to ACM Console cluster creation workflow
- CLI access for cluster deployment YAML creation
- Valid OpenStack cluster configuration parameters

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|---------|-----------|------------|------------------|
| 1 | Log into ACM Console | Access ACM Console for cluster creation: Navigate to https://console-openshift-console.apps.{cluster-host} | `oc login https://api.{cluster-host}:6443` then access Console | Successfully logged into ACM Console with clusters view available |
| 2 | Start cluster creation | Go to Clusters → Create cluster → OpenStack | `oc login https://api.{cluster-host}:6443` then access Console | OpenStack cluster creation wizard initiated with provider selection confirmed |
| 3 | Select OpenStack credential | Choose the credential created in Test Case 1 from the dropdown list | Create ClusterDeployment YAML: `touch openstack-cluster.yaml` and add:  ```yaml  apiVersion: hive.openshift.io/v1  kind: ClusterDeployment  metadata:    name: openstack-test-cluster    namespace: default  spec:    clusterName: openstack-test-cluster    platform:      openstack:        cloud: openstack        credentialsSecretRef:          name: openstack-credential  ``` | Credential selected successfully, CA certificate detected and ready for integration |
| 4 | Configure cluster details | Fill in cluster name, base domain, OpenStack cloud details, and node configuration | Update cluster YAML with complete configuration:  ```yaml  spec:    clusterName: openstack-test-cluster    baseDomain: example.com    platform:      openstack:        cloud: openstack        credentialsSecretRef:          name: openstack-credential        region: regionOne        computeFlavor: m1.large        controlPlaneFlavor: m1.xlarge  ``` | Cluster configuration completed with all required OpenStack parameters, credential reference validated |
| 5 | Review and create cluster | Review cluster configuration and click "Create" to initiate deployment | Apply cluster deployment: `oc apply -f openstack-cluster.yaml` | Cluster creation initiated, ClusterDeployment resource created with proper credential reference |
| 6 | Verify CA Secret creation | Monitor cluster deployment and verify that CA Secret is automatically created | Check for CA Secret creation: `oc get secrets | grep openstack-test-cluster` and view Secret details: `oc get secret openstack-test-cluster-ca -o yaml` | CA Secret automatically created and referenced in ClusterDeployment spec, containing custom CA certificate for OpenStack authentication |

## Test Case 3: Validate CA Certificate Error Handling and clouds.yaml Formats

### Description
Test the validation and error handling mechanisms for custom CA certificates in OpenStack credentials. This test validates that the system properly validates CA certificate formats, handles invalid certificates, and supports both supported clouds.yaml CA reference formats as documented in the feature requirements.

### Setup  
- Access to ACM Console credential creation
- Sample valid and invalid CA certificate content for testing
- CLI access for YAML validation testing
- Understanding of clouds.yaml CA reference formats

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|---------|-----------|------------|------------------|
| 1 | Log into ACM Console | Access ACM Console for credential validation testing: Navigate to https://console-openshift-console.apps.{cluster-host} | `oc login https://api.{cluster-host}:6443` then access Console | Successfully logged into ACM Console, ready for credential validation testing |
| 2 | Test invalid CA certificate | Create new OpenStack credential and enter invalid CA certificate content (malformed PEM) | Create test credential with invalid CA:  ```yaml  apiVersion: v1  kind: Secret  metadata:    name: invalid-ca-credential    namespace: default  stringData:    clouds.yaml: |      clouds:        openstack:          auth:            auth_url: "https://openstack.example.com:5000/v3"          cacert: "INVALID-CERTIFICATE-CONTENT"  ``` | Validation error displayed for invalid CA certificate format, credential creation blocked |
| 3 | Test valid CA certificate format 1 | Create credential using inline CA certificate in clouds.yaml (cacert field) | Create credential with inline CA format:  ```yaml  stringData:    clouds.yaml: |      clouds:        openstack:          auth:            auth_url: "https://openstack.example.com:5000/v3"          cacert: |            -----BEGIN CERTIFICATE-----            MIIDXTCCAkWgAwIBAgIJAKL0UG+8G0KJMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV            -----END CERTIFICATE-----  ``` | Credential created successfully with inline CA format, validation passes |
| 4 | Test valid CA certificate format 2 | Create credential using CA file reference path in clouds.yaml | Create credential with CA file reference:  ```yaml  stringData:    clouds.yaml: |      clouds:        openstack:          auth:            auth_url: "https://openstack.example.com:5000/v3"          ca_file: "/etc/ssl/certs/openstack-ca.pem"  ``` | Credential created successfully with CA file reference format, both supported formats validated |
| 5 | Verify clouds.yaml validation | Test that credential validates proper clouds.yaml structure with CA references | Validate YAML structure: `oc apply --dry-run=client -f credential-with-ca.yaml` | YAML validation passes, clouds.yaml structure confirmed correct for both CA reference formats |
| 6 | Test credential usage readiness | Verify that created credentials with CA are available for cluster creation | List available credentials: `oc get secrets -l cluster.open-cluster-management.io/type=openstack` | All valid CA credentials available for selection in cluster creation, invalid credentials properly rejected |