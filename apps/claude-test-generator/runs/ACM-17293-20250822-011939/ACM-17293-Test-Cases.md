# Test Cases for ACM-17293: Implement validation for vCenter username

## Description
Validate VMware vCenter username format validation functionality requiring @ character for domain separation in ACM Console credential creation workflow.

## Setup
- Access to ACM Hub cluster with Console enabled for credential management
- VMware vSphere environment details for credential testing (vCenter server, domain information)
- Test user accounts in domain format (user@domain) and various invalid formats for validation testing
- ACM Console credential creation interface with VMware provider support

## Test Cases

### Test Case 1: Valid vCenter Username Format Validation

**Description**: Verify that VMware credential creation accepts valid vCenter username formats with proper @ character domain separation.

**Step 1: Log into ACM Console** - Access ACM Console for VMware credential validation testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in via Console authentication and navigate to "Credentials" section
- **CLI Method**: Authenticate and verify credential access: `oc login https://api.<cluster-host>:6443 -u <username> -p <password>`
- **Expected Results**: Console loads successfully with Credentials page accessible for VMware credential creation

**Step 2: Access VMware Credential Creation** - Navigate to credential creation workflow for VMware vSphere provider
- **UI Method**: Click "Add credential" button, select "VMware vSphere" as the credential type
- **CLI Method**: Verify credential CRD availability: `oc api-resources | grep credential` 
- **Expected Results**: VMware credential creation form loads with vCenter username field visible and required

**Step 3: Enter Valid Domain Username Format** - Input properly formatted vCenter username with @ character domain separation
- **UI Method**: Enter valid username "testuser@example.com" in the vCenter username field
- **CLI Method**: Create test credential YAML `valid-vmware-credential.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-vmware-credential
  namespace: default
type: Opaque
data:
  username: dGVzdHVzZXJAZXhhbXBsZS5jb20=  # testuser@example.com
  password: dGVzdHBhc3N3b3Jk              # testpassword
  vcenter: dmNlbnRlci5leGFtcGxlLmNvbQ==    # vcenter.example.com
```
- **Expected Results**: Username field accepts the @ character input without validation errors

**Step 4: Validate Form Accepts Username** - Confirm that form validation passes for properly formatted domain username
- **UI Method**: Tab out of username field or click elsewhere to trigger validation, observe no error messages
- **CLI Method**: Validate base64 encoding: `echo "testuser@example.com" | base64`
- **Expected Results**: No validation errors displayed, form remains in valid state for submission

**Step 5: Complete Credential Creation** - Finalize credential creation with valid username format
- **UI Method**: Fill remaining required fields (password, vCenter server) and submit the credential creation form
- **CLI Method**: Apply credential: `oc apply -f valid-vmware-credential.yaml`
- **Expected Results**: Credential created successfully with @ character preserved in username field

### Test Case 2: Invalid Username Format Validation and Error Handling

**Description**: Verify that VMware credential creation properly validates and rejects username formats missing the required @ character with appropriate error messaging.

**Step 1: Log into ACM Console** - Access ACM Console for invalid username validation testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to Credentials page and initiate VMware credential creation
- **CLI Method**: Prepare test environment: `oc get secrets -n default | grep vmware || echo "No existing VMware credentials"`
- **Expected Results**: VMware credential creation form accessible for validation testing

**Step 2: Enter Invalid Username Without Domain** - Input username format missing @ character to trigger validation error
- **UI Method**: Enter "testuser" (without @domain) in the vCenter username field
- **CLI Method**: Create invalid credential test YAML `invalid-vmware-credential.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-invalid-vmware
  namespace: default
type: Opaque
data:
  username: dGVzdHVzZXI=                    # testuser (no @domain)
  password: dGVzdHBhc3N3b3Jk              # testpassword
  vcenter: dmNlbnRlci5leGFtcGxlLmNvbQ==    # vcenter.example.com
```
- **Expected Results**: Username entered without @ character, ready for validation testing

**Step 3: Trigger Validation Error** - Activate field validation to display error message for invalid format
- **UI Method**: Tab out of username field or attempt to submit form to trigger validation
- **CLI Method**: Test validation logic conceptually: `echo "testuser" | grep '@' || echo "Missing @ character"`
- **Expected Results**: Validation error message displayed: "Value must be in <user>@<domain> format."

**Step 4: Verify Error Message Content** - Confirm error message provides clear guidance on required username format
- **UI Method**: Observe error message text and styling, ensure it clearly indicates required @domain format
- **CLI Method**: Verify expected error pattern matches implementation: `grep -r "user>@<domain" /path/to/translations || echo "Translation pattern check"`
- **Expected Results**: Error message clearly states "Value must be in <user>@<domain> format." with appropriate styling

**Step 5: Test Form Submission Prevention** - Verify that form cannot be submitted with invalid username format
- **UI Method**: Attempt to submit form with invalid username, confirm submission is blocked
- **CLI Method**: Test kubectl validation: `oc apply -f invalid-vmware-credential.yaml --dry-run=client`
- **Expected Results**: Form submission prevented due to validation error, user cannot proceed without fixing username format

### Test Case 3: Username Format Edge Cases and Boundary Testing

**Description**: Validate username format validation handles edge cases including multiple @ characters, empty domains, and special character combinations.

**Step 1: Log into ACM Console** - Access ACM Console for edge case username validation testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Access VMware credential creation form for comprehensive validation testing
- **CLI Method**: Set up edge case testing environment: `oc create namespace edge-case-testing || echo "Namespace exists"`
- **Expected Results**: Credential creation form ready for edge case validation scenarios

**Step 2: Test Multiple @ Character Handling** - Verify validation behavior with username containing multiple @ symbols
- **UI Method**: Enter "test@user@domain.com" in username field to test multiple @ character handling
- **CLI Method**: Create multiple @ test YAML `multi-at-credential.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: multi-at-test
  namespace: edge-case-testing
type: Opaque
data:
  username: dGVzdEB1c2VyQGRvbWFpbi5jb20=  # test@user@domain.com
  password: dGVzdHBhc3N3b3Jk
  vcenter: dmNlbnRlci5leGFtcGxlLmNvbQ==
```
- **Expected Results**: Validation accepts multiple @ characters (implementation allows any @ presence)

**Step 3: Test Empty Domain Validation** - Verify handling of username with @ but no domain portion
- **UI Method**: Enter "testuser@" (with @ but empty domain) to test boundary validation
- **CLI Method**: Test empty domain pattern: `echo "testuser@" | grep '@' && echo "Has @ character"`
- **Expected Results**: Validation passes (current implementation only checks @ presence, not format completeness)

**Step 4: Test Special Characters with @** - Validate username with @ character plus other special characters
- **UI Method**: Enter "test.user-name@corp-domain.com" to test special character combinations
- **CLI Method**: Create special character test YAML `special-char-credential.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: special-char-test
  namespace: edge-case-testing  
type: Opaque
data:
  username: dGVzdC51c2VyLW5hbWVAY29ycC1kb21haW4uY29t  # test.user-name@corp-domain.com
  password: dGVzdHBhc3N3b3Jk
  vcenter: dmNlbnRlci5leGFtcGxlLmNvbQ==
```
- **Expected Results**: Special characters with @ character accepted, validation focuses on @ presence requirement

**Step 5: Test Maximum Length Boundaries** - Verify username field handles reasonable length limits appropriately
- **UI Method**: Enter very long username with @ character to test length handling and form behavior
- **CLI Method**: Generate long username test: `echo "very-long-username-$(date +%s)@very-long-domain-name-example.com"`
- **Expected Results**: Form accepts reasonable length usernames with @ character, handles long inputs gracefully