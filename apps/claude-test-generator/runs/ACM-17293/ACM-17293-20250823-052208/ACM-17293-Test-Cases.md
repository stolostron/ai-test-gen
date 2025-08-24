# ACM-17293: vCenter Username Validation Test Cases

## Description
Comprehensive E2E test plan for validating vCenter username format requirements in ACM credential creation workflows. Tests focus on the new @ character validation feature implemented in MCE 2.8.0 to prevent credential creation failures and improve user experience.

## Setup
- **Test Environment**: ACM Console access required
- **Prerequisites**: Valid OpenShift cluster with ACM deployed (MCE 2.8.0+)  
- **Access Requirements**: Cluster administrator credentials for console access
- **Feature Status**: vCenter username validation deployed and active

## Test Cases

### Test Case 1: Validate vCenter Username Format Requirements in Credential Creation

**Description**: Verify that vCenter credential creation accepts usernames in valid user@domain format and properly validates the @ character requirement.

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Access ACM Console for vCenter credential validation testing: Navigate to https://console-openshift-console.apps.<cluster-host> | N/A - UI only step | ACM Console dashboard loads successfully |
| 2 | Access Credential Creation | Click "Credentials" → "Create credential" → Select "VMware vSphere" | N/A - UI navigation step | VMware vSphere credential form displays |
| 3 | Enter Valid Credential Information | Fill form with Name: "test-vcenter-valid", Base domain: "example.com", Username: "testuser@vsphere.local", Password: "testpass123", vCenter server: "vcenter.example.com" | Create credential YAML file: `touch vcenter-credential.yaml` and add: ```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-vcenter-valid
  namespace: credentials
type: Opaque
stringData:
  username: "testuser@vsphere.local"
  password: "testpass123"
  vcenter: "vcenter.example.com"
  baseDomain: "example.com"
``` | Form accepts valid username format, validation passes |
| 4 | Submit Credential Creation | Click "Create" button | Apply credential: `oc apply -f vcenter-credential.yaml` | Credential created successfully with valid username format |

### Test Case 2: Verify Error Handling for Invalid vCenter Username Formats

**Description**: Confirm that invalid vCenter usernames without @ character are rejected with clear error messaging to guide users toward correct format.

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Access ACM Console for vCenter credential validation testing: Navigate to https://console-openshift-console.apps.<cluster-host> | N/A - UI only step | ACM Console dashboard loads successfully |
| 2 | Access Credential Creation | Click "Credentials" → "Create credential" → "VMware vSphere" | N/A - UI navigation step | VMware vSphere credential form displays |
| 3 | Enter Invalid Username Format | Fill form with Name: "test-vcenter-invalid", Username: "testuser" (missing @domain), other fields valid | Create invalid credential YAML: `touch invalid-credential.yaml` and add: ```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-vcenter-invalid
  namespace: credentials
type: Opaque
stringData:
  username: "testuser"
  password: "testpass123"
  vcenter: "vcenter.example.com"
``` | Validation error displays: "Username must include @ character separating user and domain" |
| 4 | Verify Error Prevention | Attempt to click "Create" button | Apply invalid credential: `oc apply -f invalid-credential.yaml` | UI: Create button disabled, CLI: Validation webhook rejects with error message |

### Test Case 3: Test Boundary Conditions for vCenter Username Character Validation

**Description**: Validate edge cases and boundary conditions for vCenter username validation including multiple @ characters and special character handling.

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Access ACM Console for vCenter credential validation testing: Navigate to https://console-openshift-console.apps.<cluster-host> | N/A - UI only step | ACM Console dashboard loads successfully |
| 2 | Test Multiple @ Characters | Enter username "user@@domain.com" in credential form | Create boundary test YAML: `touch boundary-test.yaml` and add: ```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-boundary
  namespace: credentials
type: Opaque
stringData:
  username: "user@@domain.com"
  password: "testpass123"
``` | Validation handles multiple @ characters appropriately |
| 3 | Test Edge Case Formats | Try usernames: "@domain.com", "user@", "user@.com" | Test edge cases with: `oc create secret generic test-edge1 --from-literal=username="@domain.com" -n credentials` | Clear validation feedback for each edge case format |
| 4 | Confirm Valid Complex Username | Enter "complex.user+test@subdomain.domain.com" | Create complex username YAML: `touch complex-credential.yaml` and add: ```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-complex
  namespace: credentials
type: Opaque
stringData:
  username: "complex.user+test@subdomain.domain.com"
  password: "testpass123"
``` | Complex but valid username format accepted |

### Test Case 4: Confirm End-to-End vCenter Credential Creation with Username Validation

**Description**: Complete end-to-end workflow validation from credential creation through usage in cluster provisioning to ensure validation integration works seamlessly.

**Test Steps**:

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Access ACM Console for vCenter credential validation testing: Navigate to https://console-openshift-console.apps.<cluster-host> | N/A - UI only step | ACM Console dashboard loads successfully |
| 2 | Create Valid vCenter Credential | Complete credential creation with username "admin@vsphere.local" | Create production credential YAML: `touch production-credential.yaml` and add: ```yaml
apiVersion: v1
kind: Secret
metadata:
  name: vcenter-credential
  namespace: cluster-ns
type: Opaque
stringData:
  username: "admin@vsphere.local"
  password: "secure-password"
  vcenter: "vcenter.company.com"
``` | Credential created and stored successfully |
| 3 | Verify Credential Availability | Navigate to "Clusters" → "Create cluster" → Select vSphere | List available credentials: `oc get secrets -n cluster-ns --field-selector type=Opaque` | vCenter credential appears in cluster creation dropdown with output: "NAME TYPE AGE vcenter-credential Opaque 1m" |
| 4 | Validate Integration Usage | Select created credential in cluster creation workflow | Reference credential in cluster template: `touch cluster-template.yaml` and add: ```yaml
apiVersion: hive.openshift.io/v1
kind: ClusterDeployment
metadata:
  name: test-cluster
  namespace: cluster-ns
spec:
  provisioning:
    installConfigSecretRef:
      name: vcenter-credential
``` | Credential validation passes, cluster creation proceeds successfully |