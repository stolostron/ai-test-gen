# ACM-13648: Advanced Search Version Distribution Test Cases

## Feature Overview
Support advanced search input - Iteration 2 - advanced search will support filtering for the 'Version distribution' with range operators (>, <, >=, <=, !=, =).

---

## Test Case 1: Validate Basic Version Distribution Search with Equality Operator

### Description
Verify that the advanced search functionality correctly filters clusters by version distribution using the equality operator (=) to find clusters matching a specific version.

### Setup
- Access to ACM Console at https://console-openshift-console.apps.<cluster-host>
- Multiple managed clusters with different OpenShift versions (4.12.x, 4.13.x, 4.14.x)
- User with cluster viewing permissions

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> and authenticate with provided credentials | N/A - UI login required | Successfully logged into ACM Console with cluster overview visible |
| 2 | Navigate to Clusters view | Click on "Infrastructure" → "Clusters" in left navigation menu | `oc get managedclusters` | Clusters page displays with list of managed clusters and their details including version information |
| 3 | Access Advanced Search | Click on "Advanced search" button or link in the clusters interface | N/A - UI feature specific | Advanced search interface opens with available search criteria options |
| 4 | Configure version distribution search | Select "Version distribution" from dropdown, choose "=" operator, enter specific version like "4.13.8" | N/A - UI configuration required | Search interface shows Version distribution field with equality operator selected and version value entered |
| 5 | Execute search query | Click "Search" or "Apply filter" button to execute the version distribution search | N/A - UI action required | Search executes and displays loading indicator |
| 6 | Verify filtered results | Review the filtered cluster results to ensure only clusters with version 4.13.8 are displayed | `oc get managedclusters -o json \| jq '.items[].status.version.kubernetes'` | Results show only clusters matching the exact version "4.13.8", other versions are filtered out |
| 7 | Validate result accuracy | Cross-reference displayed clusters with their actual version information in cluster details | `oc describe managedcluster <cluster-name> \| grep -i version` | Each displayed cluster confirms version 4.13.8 in detailed view, validating search accuracy |

---

## Test Case 2: Validate Version Distribution Range Filtering with Greater Than Operator

### Description
Test the advanced search functionality's ability to filter clusters using the greater than operator (>) to identify clusters with versions above a specified threshold.

### Setup
- Access to ACM Console at https://console-openshift-console.apps.<cluster-host>
- Multiple managed clusters spanning different version ranges (4.11.x, 4.12.x, 4.13.x, 4.14.x)
- Administrative access to view all cluster details

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> and authenticate using kubeadmin credentials | N/A - UI login required | ACM Console dashboard loads with cluster management interface accessible |
| 2 | Access Clusters management | Click "Infrastructure" → "Clusters" to view managed cluster inventory | `oc get managedclusters --no-headers \| wc -l` | Clusters page displays complete inventory of managed clusters with version distribution column visible |
| 3 | Open Advanced Search interface | Click "Advanced search" button to access filtering capabilities | N/A - UI specific functionality | Advanced search dialog opens showing available search criteria including Version distribution option |
| 4 | Configure greater than filter | Select "Version distribution" field, choose ">" operator, enter baseline version "4.12.0" | N/A - UI configuration step | Search interface configured with Version distribution > 4.12.0 filter ready for execution |
| 5 | Apply range filter | Click "Search" to execute greater than filter for version distribution | N/A - UI action required | Filter applies and system processes version comparison logic |
| 6 | Validate filtered cluster set | Review results to confirm only clusters with versions greater than 4.12.0 are shown (4.12.1+, 4.13.x, 4.14.x) | `oc get managedclusters -o json \| jq '.items[] \| select(.status.version.kubernetes > "4.12.0") \| .metadata.name'` | Results display clusters with versions 4.12.1, 4.13.x, 4.14.x while excluding 4.11.x and 4.12.0 exactly |
| 7 | Verify version comparison logic | Check specific cluster details to ensure version comparison algorithm correctly interprets semantic versioning | `oc get managedclusters -o json \| jq '.items[] \| {name: .metadata.name, version: .status.version.kubernetes}'` | Version comparison follows semantic versioning rules (4.13.1 > 4.12.9, 4.14.0 > 4.13.15) |

---

## Test Case 3: Validate Multiple Operator Support and Complex Version Filtering

### Description
Verify comprehensive operator support (>=, <=, !=) and validate complex filtering scenarios to ensure the advanced search handles all operator types correctly for version distribution.

### Setup
- Access to ACM Console at https://console-openshift-console.apps.<cluster-host>
- Diverse cluster environment with versions spanning 4.11.x through 4.15.x
- Clusters with various patch versions (4.13.1, 4.13.5, 4.13.12, etc.)

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Access https://console-openshift-console.apps.<cluster-host> with administrative credentials | N/A - Console access required | ACM Console accessible with full cluster management permissions |
| 2 | Navigate to cluster inventory | Go to "Infrastructure" → "Clusters" for complete cluster overview | `oc get managedclusters -o wide` | Full cluster listing with version distribution column showing diverse OpenShift versions |
| 3 | Test Greater Than or Equal (>=) | Open Advanced search, select Version distribution >= "4.13.0" | N/A - UI filter configuration | Search shows clusters with versions 4.13.0, 4.13.x, 4.14.x, 4.15.x (inclusive of 4.13.0) |
| 4 | Test Less Than or Equal (<=) | Modify search to Version distribution <= "4.13.5" | N/A - UI filter modification | Results include clusters with versions up to and including 4.13.5 (4.11.x, 4.12.x, 4.13.0-4.13.5) |
| 5 | Test Not Equal (!=) operator | Change filter to Version distribution != "4.13.0" | N/A - UI filter update | All clusters except those with exactly version 4.13.0 are displayed |
| 6 | Validate operator precedence | Test Less Than (<) operator with Version distribution < "4.14.0" | `oc get managedclusters -o json \| jq '.items[] \| select(.status.version.kubernetes < "4.14.0") \| .metadata.name'` | Shows clusters with versions below 4.14.0 (excludes 4.14.0 and higher, includes 4.13.x and below) |
| 7 | Cross-validate operator logic | Verify each operator produces expected results by comparing UI results with CLI version queries | `oc get managedclusters -o json \| jq '.items[] \| {name: .metadata.name, version: .status.version.kubernetes, operator_test: (.status.version.kubernetes >= "4.13.0")}'` | All operators (=, >, <, >=, <=, !=) function correctly with proper semantic version comparison logic |

---

## Test Case 4: Validate Advanced Search Integration and User Experience

### Description
Test the integration of version distribution filtering with the broader advanced search functionality and validate the overall user experience including search persistence and result management.

### Setup
- Access to ACM Console at https://console-openshift-console.apps.<cluster-host>
- Environment with sufficient clusters to test pagination and large result sets
- Mixed cluster environment for comprehensive filtering validation

### Test Table

| Step | Action | UI Method | CLI Method | Expected Results |
|------|--------|-----------|------------|------------------|
| 1 | Log into ACM Console | Access https://console-openshift-console.apps.<cluster-host> and authenticate | N/A - UI access required | ACM Console dashboard accessible with cluster management navigation |
| 2 | Access comprehensive cluster view | Navigate to "Infrastructure" → "Clusters" to view complete cluster inventory | `oc get managedclusters --show-labels` | Clusters page shows complete inventory with version distribution and other searchable attributes |
| 3 | Test search combination | Use Advanced search to combine Version distribution filter with other criteria (e.g., Status = "Ready" AND Version distribution >= "4.13.0") | N/A - UI multiple filter configuration | Advanced search allows multiple criteria combination with AND logic |
| 4 | Validate search persistence | Apply version distribution filter, navigate to cluster details, return to clusters view | N/A - UI navigation test | Search filter remains applied after navigation, maintaining user context |
| 5 | Test search reset functionality | Clear version distribution filter and verify all clusters return to view | N/A - UI reset action | Search reset removes filter and displays complete cluster inventory |
| 6 | Validate result export capability | If available, test export functionality with filtered version distribution results | `oc get managedclusters -o yaml > filtered-clusters.yaml` | Filtered results can be exported or saved for external analysis |
| 7 | Test search performance | Apply version distribution filter to large cluster set and measure response time | `time oc get managedclusters -o json \| jq '.items[] \| select(.status.version.kubernetes >= "4.13.0")'` | Search executes within acceptable time limits (< 5 seconds) with visual loading indicators |