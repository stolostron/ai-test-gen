# Test Cases for ACM-3247: Implement custom CA support for OpenStack credentials

## Description
Validate OpenStack custom CA certificate support functionality enabling secure cluster provisioning with custom certificate authorities through enhanced credential validation and clouds.yaml integration.

## Setup
- Access to ACM Hub cluster with Console enabled for credential management
- OpenStack environment details for credential testing (auth_url, credentials, cloud configuration)
- Test CA certificate files in PEM format for custom certificate authority validation
- ACM Console credential creation interface with OpenStack provider support and CA certificate field

## Test Cases

### Test Case 1: OpenStack Credential Creation with Valid Custom CA Certificate

**Description**: Verify that OpenStack credential creation successfully accepts and processes valid custom CA certificates with proper PEM format validation and clouds.yaml integration.

**Step 1: Log into ACM Console** - Access ACM Console for OpenStack custom CA certificate testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in via Console authentication and navigate to "Credentials" section
- **CLI Method**: Authenticate and verify credential access: `oc login https://api.<cluster-host>:6443 -u <username> -p <password>`
- **Expected Results**: Console loads successfully with Credentials page accessible for OpenStack credential creation

**Step 2: Access OpenStack Credential Creation** - Navigate to credential creation workflow for OpenStack provider with CA certificate support
- **UI Method**: Click "Add credential" button, select "Red Hat OpenStack Platform" as the credential type
- **CLI Method**: Verify OpenStack credential CRD availability: `oc api-resources | grep credential`
- **Expected Results**: OpenStack credential creation form loads with CA certificate field (os_ca_bundle) visible as optional textarea

**Step 3: Configure Basic OpenStack Credentials** - Input standard OpenStack authentication details before adding CA certificate
- **UI Method**: Fill required fields: username, password, domain, project name, and clouds.yaml configuration
- **CLI Method**: Create base OpenStack credential YAML `openstack-base-credential.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-openstack-credential
  namespace: default
type: Opaque
data:
  username: dGVzdHVzZXI=                    # testuser
  password: dGVzdHBhc3N3b3Jk              # testpassword
  clouds.yaml: Y2xvdWRzOgogIHRlc3Q6CiAgICBhdXRoOgogICAgICBhdXRoX3VybDogaHR0cHM6Ly9rZXlzdG9uZS5leGFtcGxlLmNvbTo1MDAwL3YzCiAgICAgIHVzZXJuYW1lOiB0ZXN0dXNlcgogICAgICBwYXNzd29yZDogdGVzdHBhc3N3b3JkCiAgICAgIHByb2plY3RfbmFtZTogdGVzdHByb2plY3QKICAgICAgdXNlcl9kb21haW5fbmFtZTogZGVmYXVsdAogICAgICBwcm9qZWN0X2RvbWFpbl9uYW1lOiBkZWZhdWx0
  cloud: dGVzdA==                          # test
```
- **Expected Results**: Basic OpenStack credential fields configured with valid authentication details

**Step 4: Add Valid Custom CA Certificate** - Input properly formatted PEM certificate in CA certificate field
- **UI Method**: In "Internal CA certificate" field (os_ca_bundle), enter valid PEM formatted certificate:
```
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKL0UG+0zGmCMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMjMwMjA2MTkyMjQ3WhcNMjQwMjA2MTkyMjQ3WjBF
MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEA0123456789ABCDEFabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN
OPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP
QRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPtest
certificate0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuv
wxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
-----END CERTIFICATE-----
```
- **CLI Method**: Create CA-enabled credential YAML `openstack-ca-credential.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-openstack-ca-credential
  namespace: default
type: Opaque
data:
  os_ca_bundle: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURYVENDQWtXZ0F3SUJBZ0lKQUtMMFVHKzB6R21DTUF3R0NTcUdTSWIzRFFFQkN3VUFNRVUKLy4uLnRlc3QgY2VydGlmaWNhdGUgZGF0YS4uLgotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0t
  username: dGVzdHVzZXI=
  password: dGVzdHBhc3N3b3Jk
  clouds.yaml: Y2xvdWRzOgogIHRlc3Q6CiAgICBhdXRoOgogICAgICBhdXRoX3VybDogaHR0cHM6Ly9rZXlzdG9uZS5leGFtcGxlLmNvbTo1MDAwL3YzCiAgICAgIHVzZXJuYW1lOiB0ZXN0dXNlcgogICAgICBwYXNzd29yZDogdGVzdHBhc3N3b3JkCiAgICAgIHByb2plY3RfbmFtZTogdGVzdHByb2plY3QKICAgICAgdXNlcl9kb21haW5fbmFtZTogZGVmYXVsdAogICAgICBwcm9qZWN0X2RvbWFpbl9uYW1lOiBkZWZhdWx0CiAgICAgIGNhY2VydDogL2V0Yy9vcGVuc3RhY2stY2EvY2EuY3J0
  cloud: dGVzdA==
```
- **Expected Results**: CA certificate field accepts properly formatted PEM certificate without validation errors

**Step 5: Validate Certificate Integration** - Confirm that credential creation processes CA certificate correctly with clouds.yaml enhancement
- **UI Method**: Submit the credential creation form and verify successful creation with CA certificate integration
- **CLI Method**: Apply credential and verify CA certificate secret creation: `oc apply -f openstack-ca-credential.yaml && oc get secret test-openstack-ca-credential -o yaml`
- **Expected Results**: Credential created successfully with CA certificate stored and clouds.yaml automatically enhanced with cacert reference

### Test Case 2: CA Certificate Format Validation and Error Handling

**Description**: Verify that OpenStack credential creation properly validates CA certificate format and provides appropriate error messaging for invalid certificate formats.

**Step 1: Log into ACM Console** - Access ACM Console for CA certificate validation testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to Credentials page and initiate OpenStack credential creation
- **CLI Method**: Prepare validation test environment: `oc get secrets -n default | grep openstack || echo "No existing OpenStack credentials"`
- **Expected Results**: OpenStack credential creation form accessible for certificate validation testing

**Step 2: Enter Invalid Certificate Format** - Input malformed certificate data to trigger validation error
- **UI Method**: In CA certificate field, enter invalid certificate format (missing headers, malformed content):
```
INVALID CERTIFICATE DATA
This is not a valid PEM certificate
Missing proper headers and formatting
Random text content without structure
```
- **CLI Method**: Create invalid certificate test YAML `invalid-ca-credential.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-invalid-ca
  namespace: default
type: Opaque
data:
  os_ca_bundle: SW5WYWxpZCBjZXJ0aWZpY2F0ZSBkYXRh  # Invalid certificate data
  username: dGVzdHVzZXI=
  password: dGVzdHBhc3N3b3Jk
  clouds.yaml: Y2xvdWRzOgogIHRlc3Q6CiAgICBhdXRoOgogICAgICBhdXRoX3VybDogaHR0cHM6Ly9rZXlzdG9uZS5leGFtcGxlLmNvbTo1MDAwL3YzCiAgICAgIHVzZXJuYW1lOiB0ZXN0dXNlcgogICAgICBwYXNzd29yZDogdGVzdHBhc3N3b3JkCiAgICAgIHByb2plY3RfbmFtZTogdGVzdHByb2plY3QKICAgICAgdXNlcl9kb21haW5fbmFtZTogZGVmYXVsdAogICAgICBwcm9qZWN0X2RvbWFpbl9uYW1lOiBkZWZhdWx0
  cloud: dGVzdA==
```
- **Expected Results**: Invalid certificate format entered, ready for validation testing

**Step 3: Trigger Certificate Validation** - Activate field validation to display error message for invalid certificate format
- **UI Method**: Tab out of CA certificate field or attempt to submit form to trigger certificate validation
- **CLI Method**: Test certificate validation conceptually: `echo "Invalid certificate" | grep "BEGIN CERTIFICATE" || echo "Missing PEM headers"`
- **Expected Results**: Validation error message displayed indicating invalid certificate format

**Step 4: Test Empty Certificate Handling** - Verify that empty CA certificate field is handled appropriately (optional field)
- **UI Method**: Clear CA certificate field completely and verify form remains valid (optional field)
- **CLI Method**: Create credential without CA certificate: `oc apply -f openstack-base-credential.yaml --dry-run=client`
- **Expected Results**: Empty CA certificate field accepted (optional), form validation passes without CA certificate

**Step 5: Verify Error Message Guidance** - Confirm error messages provide clear guidance on required certificate format
- **UI Method**: Observe error message content for invalid certificate, ensure it specifies PEM format requirements
- **CLI Method**: Validate expected certificate pattern: `grep -E "BEGIN CERTIFICATE|END CERTIFICATE" <<< "Valid PEM format"`
- **Expected Results**: Error messages clearly indicate PEM format requirement with proper certificate headers

### Test Case 3: clouds.yaml Integration and CA Reference Validation

**Description**: Validate automatic clouds.yaml enhancement with CA certificate references and verification of cacert path consistency for secure OpenStack cluster provisioning.

**Step 1: Log into ACM Console** - Access ACM Console for clouds.yaml CA integration testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Access OpenStack credential creation form for clouds.yaml integration testing
- **CLI Method**: Set up clouds.yaml integration testing: `oc create namespace ca-integration-test || echo "Namespace exists"`
- **Expected Results**: Credential creation form ready for clouds.yaml and CA certificate integration validation

**Step 2: Configure clouds.yaml Without CA Reference** - Input clouds.yaml configuration without existing cacert field
- **UI Method**: Enter clouds.yaml configuration in appropriate field without cacert reference:
```yaml
clouds:
  production:
    auth:
      auth_url: https://keystone.production.com:5000/v3
      username: produser
      password: prodpass
      project_name: production-project
      user_domain_name: default
      project_domain_name: default
    verify: true
```
- **CLI Method**: Create clouds.yaml integration test YAML `clouds-yaml-integration.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: clouds-yaml-integration-test
  namespace: ca-integration-test
type: Opaque
data:
  clouds.yaml: Y2xvdWRzOgogIHByb2R1Y3Rpb246CiAgICBhdXRoOgogICAgICBhdXRoX3VybDogaHR0cHM6Ly9rZXlzdG9uZS5wcm9kdWN0aW9uLmNvbTo1MDAwL3YzCiAgICAgIHVzZXJuYW1lOiBwcm9kdXNlcgogICAgICBwYXNzd29yZDogcHJvZHBhc3MKICAgICAgcHJvamVjdF9uYW1lOiBwcm9kdWN0aW9uLXByb2plY3QKICAgICAgdXNlcl9kb21haW5fbmFtZTogZGVmYXVsdAogICAgICBwcm9qZWN0X2RvbWFpbl9uYW1lOiBkZWZhdWx0CiAgICB2ZXJpZnk6IHRydWU=
  username: cHJvZHVzZXI=
  password: cHJvZHBhc3M=
  cloud: cHJvZHVjdGlvbg==
```
- **Expected Results**: clouds.yaml configured without cacert reference, ready for CA certificate integration

**Step 3: Add CA Certificate for Automatic Integration** - Input CA certificate to trigger automatic clouds.yaml enhancement
- **UI Method**: Add valid CA certificate in CA certificate field while maintaining existing clouds.yaml configuration
- **CLI Method**: Update credential with CA certificate addition:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: clouds-yaml-ca-integration
  namespace: ca-integration-test
type: Opaque
data:
  os_ca_bundle: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURYVENDQWtXZ0F3SUJBZ0lKQUtMMFVHKzB6R21DTUF3R0NTcUdTSWIzRFFFQkN3VUFNRVUKLy4uLnRlc3QgY2VydGlmaWNhdGUgZGF0YS4uLgotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0t
  clouds.yaml: <enhanced-with-cacert-reference>
  username: cHJvZHVzZXI=
  password: cHJvZHBhc3M=
  cloud: cHJvZHVjdGlvbg==
```
- **Expected Results**: CA certificate field populated, ready for clouds.yaml automatic enhancement validation

**Step 4: Validate Automatic clouds.yaml Enhancement** - Verify that clouds.yaml is automatically updated with cacert reference
- **UI Method**: Submit credential and verify that clouds.yaml includes cacert: '/etc/openstack-ca/ca.crt' reference
- **CLI Method**: Apply credential and check enhanced clouds.yaml: `oc apply -f clouds-yaml-ca-integration.yaml && oc get secret -o jsonpath='{.data.clouds\.yaml}' clouds-yaml-ca-integration | base64 -d`
- **Expected Results**: clouds.yaml automatically enhanced with cacert: '/etc/openstack-ca/ca.crt' reference when CA certificate provided

**Step 5: Verify CA Certificate Secret Creation** - Confirm that separate CA certificate secret is created for cluster deployment integration
- **UI Method**: After credential creation, verify that CA certificate is properly stored and referenced for cluster deployment
- **CLI Method**: Check for CA certificate secret creation: `oc get secrets -n ca-integration-test | grep "trust" || echo "Checking CA certificate secret creation"`
- **Expected Results**: CA certificate stored appropriately for cluster deployment integration, secret references configured correctly