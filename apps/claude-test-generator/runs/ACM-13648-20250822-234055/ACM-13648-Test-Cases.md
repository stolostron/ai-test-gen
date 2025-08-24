# Test Cases for ACM-13648: Advanced Search Version Distribution Filtering

## Test Case 1: Basic Version Distribution Filtering with Single Operators

**Description**: Validate basic version distribution filtering functionality with single comparison operators in ACM Console advanced search to verify the new iteration 2 enhancement works correctly for filtering clusters by distribution version.

**Setup**: 
- Access to ACM Console: https://console-openshift-console.apps.CLUSTER_HOST
- Valid cluster credentials with appropriate permissions
- Managed clusters with applications containing version distribution data
- Feature confirmed available in ACM 2.12.0+ environment
- Existing applications with diverse OpenShift version distributions for comprehensive testing

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.CLUSTER_HOST and login with kubeadmin credentials | oc login https://api.CLUSTER_HOST:6443 -u kubeadmin -p PASSWORD --insecure-skip-tls-verify | Successfully logged into ACM Console with cluster overview visible and CLI authentication confirmed |
| 2 | Navigate to Applications page | Click on "Applications" in the left navigation menu under "Application lifecycle" | oc get applications -A | Applications page displays with list of deployed applications showing version distribution column |
| 3 | Access Advanced Search | Click on the "Advanced search" button or search icon in the applications table header | oc get applications -A --show-labels | Advanced search modal opens with column selection dropdown and operator options |
| 4 | Select Distribution version column | From the column dropdown, select "Distribution version" as the search field | N/A - UI only | Distribution version is selected and operator dropdown becomes active with available comparison operators |
| 5 | Test greater than operator | Select ">" operator and enter "4.14" as the value, then click Search | oc get applications -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.distributionVersion}{"\n"}{end}' | Search results show only applications with distribution version greater than 4.14, results filtered correctly |
| 6 | Clear and test less than operator | Clear the search, select "<" operator with value "4.16", click Search | oc get applications -A --field-selector 'spec.distributionVersion<4.16' | Search results show only applications with distribution version less than 4.16, filtering logic verified |
| 7 | Verify results accuracy | Compare filtered results with actual application version data | oc get applications -A -o yaml \| grep -A 2 -B 2 distributionVersion | All displayed applications match the specified version criteria, no false positives or negatives |

## Test Case 2: Advanced Filtering with Multiple AND Constraints 

**Description**: Validate advanced version distribution filtering using multiple AND constraints to test complex search scenarios and verify proper logical operation combination functionality.

**Setup**:
- ACM Console access with authenticated session
- Multiple managed clusters with varied version distributions
- Test environment with ACM 2.12.0+ containing the iteration 2 enhancement
- Diverse application portfolio with different distribution versions for comprehensive constraint testing

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.CLUSTER_HOST and login with valid credentials | oc login https://api.CLUSTER_HOST:6443 -u kubeadmin -p PASSWORD --insecure-skip-tls-verify | ACM Console loaded successfully with user authenticated and cluster management interface accessible |
| 2 | Navigate to Applications | Access Applications page through main navigation menu | oc get applications -A -o wide | Applications list displays with comprehensive view including distribution version column data |
| 3 | Open Advanced Search | Click Advanced search button to open search configuration interface | N/A - UI only | Advanced search modal opens with multiple constraint addition capability |
| 4 | Add first constraint | Select "Distribution version" with ">=" operator and value "4.14" | oc get applications -A --field-selector 'spec.distributionVersion>=4.14' | First constraint configured correctly in search interface |
| 5 | Add second constraint | Click "Add constraint", select "Distribution version" with "<=" operator and value "4.16" | oc get applications -A --field-selector 'spec.distributionVersion>=4.14,spec.distributionVersion<=4.16' | Multiple constraints visible in search interface with AND logic indicated |
| 6 | Execute combined search | Click Search to apply both constraints simultaneously | oc get applications -A -o jsonpath='{range .items[?(@.spec.distributionVersion>="4.14" && @.spec.distributionVersion<="4.16")]}{.metadata.name}{"\t"}{.spec.distributionVersion}{"\n"}{end}' | Search results show only applications with distribution version between 4.14 and 4.16 inclusive |
| 7 | Validate logical AND operation | Verify all results meet both constraints and no excluded versions appear | oc describe applications -A \| grep -E "(Name:|Distribution Version:)" | All displayed applications satisfy both version constraints, logical AND operation working correctly |

## Test Case 3: Edge Cases and Error Handling Validation

**Description**: Validate edge cases and error handling for version distribution filtering including invalid inputs, boundary conditions, and malformed version strings to ensure robust functionality.

**Setup**:
- ACM Console access with administrative privileges  
- Test environment containing applications with various version formats
- ACM 2.12.0+ with iteration 2 advanced search functionality
- Applications with edge case version distributions including pre-release and development versions

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.CLUSTER_HOST and authenticate | oc login https://api.CLUSTER_HOST:6443 -u kubeadmin -p PASSWORD --insecure-skip-tls-verify | Console access established with full administrative capabilities |
| 2 | Access Applications Advanced Search | Navigate to Applications and open Advanced search interface | oc get applications -A --show-labels | Advanced search modal ready for edge case testing |
| 3 | Test invalid version format | Select "Distribution version" with "=" operator and enter "invalid.version.format" | oc get applications -A --field-selector 'spec.distributionVersion=invalid.version.format' | Appropriate error message displayed indicating invalid version format, search not executed |
| 4 | Test empty value handling | Select ">" operator with empty value field and attempt search | oc get applications -A --field-selector 'spec.distributionVersion>' | User interface prevents search execution or displays validation error for empty value |
| 5 | Test boundary version values | Test with version "0.0.0" using ">" operator | oc get applications -A --field-selector 'spec.distributionVersion>0.0.0' | Search executes correctly showing all applications with any valid version greater than 0.0.0 |
| 6 | Test special characters handling | Enter version with special characters like "4.14-beta.1" with "=" operator | oc get applications -A --field-selector 'spec.distributionVersion=4.14-beta.1' | Search handles pre-release versions correctly, matching applications with exact version string |
| 7 | Verify error recovery | Clear invalid searches and confirm normal operation returns | oc get applications -A | Interface resets to normal state, previous error conditions cleared, standard search functionality restored |