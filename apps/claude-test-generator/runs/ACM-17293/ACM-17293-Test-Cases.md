# Test Cases: vCenter Username Validation

## Test Case 1: Validate vCenter Username Format Requirements

### Description
Verify that ACM Console enforces proper vCenter username format (user@domain) during VMware vSphere credential creation, ensuring users cannot create credentials with incorrect username formats.

### Setup
- Access to ACM Console on test environment
- Administrative credentials for cluster access
- VMware vSphere server details for credential creation testing

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> | oc login https://api.<cluster-host>:6443 --username=<admin-user> --password=<admin-password> | Successfully logged into ACM Console with cluster overview displayed |
| 2 | Access Credential Creation | Click on Infrastructure → Clusters → Credentials → Add credential | oc get secrets -n <namespace> --field-selector type=Opaque | Credential creation page loads with provider selection options |
| 3 | Select VMware vSphere Provider | Select "VMware vSphere" from the provider dropdown menu | Begin creating secret with VMware vSphere credential type: oc create secret generic <credential-name> --from-literal=type=vmw | VMware vSphere credential form displays with required fields including username field |
| 4 | Enter Valid Username Format | In the username field, enter: testuser@domain.com | Add username to secret: --from-literal=username=testuser@domain.com | Username field accepts the input without validation errors, form allows continuation |
| 5 | Complete Credential Creation | Fill remaining fields (vCenter server, password, certificate) and click Create | Complete secret creation: oc create secret generic test-vmware-cred --from-literal=type=vmw --from-literal=username=testuser@domain.com --from-literal=password=testpass --from-literal=vcenterServer=vcenter.example.com --from-literal=cacertificate="" -n default | Credential successfully created and appears in credentials list |

## Test Case 2: Verify Invalid Username Format Error Handling

### Description
Verify that ACM Console properly validates vCenter username format and prevents credential creation when username lacks the required @ character, displaying appropriate error messages to guide users.

### Setup
- Access to ACM Console on test environment
- Administrative credentials for cluster access
- Understanding of required username format validation behavior

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> | oc login https://api.<cluster-host>:6443 --username=<admin-user> --password=<admin-password> | Successfully logged into ACM Console with cluster overview displayed |
| 2 | Access Credential Creation | Click on Infrastructure → Clusters → Credentials → Add credential | oc get secrets -n <namespace> --field-selector type=Opaque | Credential creation page loads with provider selection options |
| 3 | Select VMware vSphere Provider | Select "VMware vSphere" from the provider dropdown menu | Begin creating secret with VMware vSphere credential type: oc create secret generic <credential-name> --from-literal=type=vmw | VMware vSphere credential form displays with required fields including username field |
| 4 | Enter Invalid Username Format | In the username field, enter: invaliduser (without @ character) | Attempt secret creation with invalid username: --from-literal=username=invaliduser | Username field displays validation error: "Value must be in <user>@<domain> format." |
| 5 | Verify Form Submission Prevention | Attempt to click Create button with invalid username | Attempt to apply invalid secret: oc create secret generic test-invalid-vmware --from-literal=type=vmw --from-literal=username=invaliduser --from-literal=password=testpass --from-literal=vcenterServer=vcenter.example.com -n default | Create button remains disabled or form submission is blocked, error message persists until valid format entered |

## Test Case 3: Test Real-time Username Validation Feedback

### Description
Verify that ACM Console provides immediate validation feedback as users type vCenter usernames, ensuring real-time error detection and user guidance for proper format requirements.

### Setup
- Access to ACM Console on test environment
- Administrative credentials for cluster access
- Browser with JavaScript enabled for real-time validation testing

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> | oc login https://api.<cluster-host>:6443 --username=<admin-user> --password=<admin-password> | Successfully logged into ACM Console with cluster overview displayed |
| 2 | Access Credential Creation | Click on Infrastructure → Clusters → Credentials → Add credential | oc get namespaces | grep credentials or similar validation | Credential creation page loads with provider selection options |
| 3 | Select VMware vSphere Provider | Select "VMware vSphere" from the provider dropdown menu | Check available credential types: oc get crd | grep credential | VMware vSphere credential form displays with username field ready for input |
| 4 | Test Progressive Username Entry | Type progressively: "user" → "user@" → "user@domain" → "user@domain.com" | Monitor validation during progressive secret preparation: echo "username: user" then "username: user@" then complete format | Real-time validation shows error for "user", clears error after "@" is added, accepts complete format |
| 5 | Verify Error Clearance | Observe validation messages as format becomes valid | Complete valid secret with proper format: oc create secret generic test-realtime-vmware --from-literal=type=vmw --from-literal=username=user@domain.com --from-literal=password=testpass --from-literal=vcenterServer=vcenter.example.com -n default | Error message disappears when valid format achieved, form becomes submittable, credential creation succeeds |