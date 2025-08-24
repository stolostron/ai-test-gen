# Test Cases: ACM-13644 - Advanced Search Input for Cluster List Page

## Test Case 1: Validate Advanced Search Dropdown Interface and Column Selection

### Description
Verify the advanced search dropdown interface functionality and column selection capabilities for the cluster list page, ensuring the SearchInput component with Key-Operator-Value interface operates correctly for exact string matching against name and namespace columns.

### Setup
- Access to ACM Console with valid credentials
- At least 2-3 managed clusters visible in cluster list
- Clusters with varying names and namespaces for search testing
- Browser with JavaScript enabled for dropdown interaction

### Test Steps

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> and log in with valid credentials | Not applicable for UI feature | ACM Console dashboard displays successfully with cluster management navigation available |
| 2 | Navigate to cluster list page | Click on "Infrastructure" → "Clusters" from the main navigation menu | `oc get managedclusters` to verify cluster availability | Cluster list page loads showing AcmTable with multiple clusters, search interface visible at top of table |
| 3 | Activate advanced search dropdown | Click on the search input field or search icon to activate the advanced search dropdown interface | Not applicable for UI dropdown interaction | SearchInput dropdown appears with Key-Operator-Value interface, showing column selection options (name, namespace) and operator selection |
| 4 | Select search column and operator | From dropdown: Select "name" as column, select "=" as operator, and enter search field | Not applicable for UI dropdown selection | Column "name" selected, operator "=" displayed, text input field ready for search term entry |
| 5 | Enter search term and execute | Enter exact cluster name (e.g., "local-cluster") in the value field and execute search | `oc get managedclusters | grep "local-cluster"` to verify cluster exists | Search executes with exact string matching, table filters to show only clusters matching the exact name criteria |
| 6 | Verify search results accuracy | Review filtered table results and confirm only exact matches are displayed | `oc get managedclusters -o name | grep "local-cluster"` | Table displays only clusters with exact name match, no partial or fuzzy matches visible, search term highlighted in results |

## Test Case 2: Verify Exact String Matching Search Functionality with Real Cluster Data

### Description
Test the exact string matching capability of the advanced search feature against cluster namespace column, validating search accuracy and result filtering with real cluster data from the environment.

### Setup
- ACM Console access with cluster data available
- Clusters deployed in different namespaces
- Knowledge of specific namespace names for testing
- Advanced search dropdown functionality verified

### Test Steps

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> and authenticate | Not applicable | ACM Console loads with access to cluster management interface |
| 2 | Access cluster list with advanced search | Navigate to Infrastructure → Clusters, ensure advanced search dropdown is available | `oc get managedclusters --all-namespaces` | Cluster list page displays with multiple clusters across different namespaces, advanced search interface active |
| 3 | Configure namespace search parameters | Open advanced search dropdown, select "namespace" as column, "=" as operator | Not applicable for UI interaction | Dropdown shows namespace column selected, exact match operator configured, input field ready for namespace value |
| 4 | Execute namespace-specific search | Enter specific namespace (e.g., "openshift-cluster-manager") in value field and execute search | `oc get managedclusters -n openshift-cluster-manager` | Search filters table to show only clusters in the specified namespace, exact namespace matching applied |
| 5 | Validate search result accuracy | Verify all displayed clusters belong to searched namespace, check for false positives or missed results | `oc get managedclusters --all-namespaces | grep "openshift-cluster-manager"` | All visible clusters belong to exact namespace searched, no clusters from other namespaces displayed, search accurately filters data |
| 6 | Test search state management | Clear search and verify table returns to full cluster list display | `oc get managedclusters --all-namespaces` to verify all clusters exist | Search clears completely, table displays all clusters again, search state resets properly without residual filtering |

## Test Case 3: Test Complete Advanced Search Workflow and User Experience

### Description
Validate the end-to-end advanced search user experience including dropdown interaction, search execution, result handling, error scenarios, and overall workflow usability for cluster management operations.

### Setup
- ACM Console access with diverse cluster data
- Clusters with various names, namespaces, and states
- Test data including edge cases (special characters, long names)
- Understanding of expected search behavior and limitations

### Test Steps

| Step | Action | UI Method | CLI Method | Expected Result |
|------|--------|-----------|------------|-----------------|
| 1 | Log into ACM Console | Navigate to https://console-openshift-console.apps.<cluster-host> with valid credentials | Not applicable | Console loads successfully, cluster management interface accessible with search functionality |
| 2 | Test search workflow with valid criteria | Use advanced search: column="name", operator="=", value="existing-cluster-name" | `oc get managedclusters | grep "existing-cluster-name"` | Complete search workflow executes smoothly, results display accurately with proper filtering and UI feedback |
| 3 | Test search with non-existent criteria | Execute search with: column="name", operator="=", value="non-existent-cluster" | `oc get managedclusters | grep "non-existent-cluster"` (should return empty) | Search executes properly, table shows "No results found" or empty state, no error conditions or system failures |
| 4 | Test search interface responsiveness | Perform multiple rapid search operations with different criteria and observe UI responsiveness | Multiple rapid `oc get managedclusters` commands to verify system responsiveness | Search interface remains responsive, no UI freezing or performance degradation, smooth user interaction maintained |
| 5 | Validate search accessibility and usability | Test keyboard navigation, screen reader compatibility, and overall user experience | Not applicable for CLI testing | Search interface accessible via keyboard, clear visual feedback, intuitive user experience with proper error messaging |
| 6 | Verify integration with cluster management | Perform cluster operations (view details, status) while search is active | `oc get managedclusters <cluster-name> -o yaml` while search active | Cluster operations work normally with active search, search state maintains during navigation, no interference with cluster management tasks |