# Test Cases: ACM-13644 - Advanced Search Input for Cluster List Page

## Test Case 1: Validate Advanced Search Dropdown Interface and Column Selection Capabilities

**Description**: Verify that the advanced search dropdown interface opens correctly and provides proper column selection options for exact string matching against cluster list table columns.

**Setup**: 
- Access ACM Console with authenticated user credentials
- Navigate to cluster list page with available managed clusters
- Ensure advanced search feature is visible in the cluster list interface

### Test Steps

| Step | Action | UI Method | CLI Method | Expected Result |
|------|---------|-----------|------------|-----------------|
| 1 | Log into ACM Console - Access ACM Console for advanced search testing | Navigate to https://console-openshift-console.apps.CLUSTER-HOST | oc login https://api.CLUSTER-HOST:6443 --username=USERNAME --password=PASSWORD | Successfully logged into OpenShift console with ACM access |
| 2 | Navigate to cluster list page for search functionality testing | Click "Cluster management" → "Clusters" from left navigation menu | oc get managedclusters | Cluster list page displays with available managed clusters and search interface |
| 3 | Open advanced search dropdown interface | Click "Open advanced search" button (magnifying glass icon with dropdown arrow) | N/A - UI-specific functionality | Advanced search dropdown opens with form containing search options |
| 4 | Verify column selection dropdown functionality | Click "Column" dropdown to view available search columns | N/A - UI-specific functionality | Column dropdown displays options: Name, Namespace, Distribution version |
| 5 | Validate column selection behavior | Select "Name" from column dropdown options | N/A - UI-specific functionality | Column dropdown shows "Name" as selected, operator dropdown becomes available |
| 6 | Verify operator selection for name column | Click "Operator" dropdown after selecting Name column | N/A - UI-specific functionality | Operator dropdown displays "=" (equals) option for exact string matching |

## Test Case 2: Verify Exact String Matching Search Functionality with Real Cluster Data

**Description**: Test the exact string matching capability of the advanced search feature using real cluster names and namespaces to ensure accurate search results.

**Setup**:
- ACM Console access with authenticated user
- Cluster list page with at least one managed cluster (local-cluster expected)
- Advanced search interface available and functional

### Test Steps

| Step | Action | UI Method | CLI Method | Expected Result |
|------|---------|-----------|------------|-----------------|
| 1 | Log into ACM Console - Access ACM Console for exact string search testing | Navigate to https://console-openshift-console.apps.CLUSTER-HOST | oc login https://api.CLUSTER-HOST:6443 --username=USERNAME --password=PASSWORD | Successfully authenticated with ACM Console access |
| 2 | Navigate to cluster management page | Click "Cluster management" → "Clusters" from navigation menu | oc get managedclusters --no-headers | Cluster list displays managed clusters including local-cluster |
| 3 | Configure advanced search for name column exact matching | Click "Open advanced search" → Select "Name" from Column dropdown → Select "=" from Operator dropdown | oc get managedclusters local-cluster -o name | Advanced search configured for exact name matching with inputs ready |
| 4 | Execute exact string search for cluster name | Enter "local-cluster" in Value field → Click "Close" to apply search | oc get managedclusters local-cluster | Search results display only local-cluster matching exact string criteria |
| 5 | Verify search result accuracy with exact match | Confirm cluster list shows only "local-cluster" entry | oc get managedclusters local-cluster -o custom-columns=NAME:.metadata.name | Table displays exactly one row with local-cluster matching search criteria |
| 6 | Reset search and test namespace column functionality | Click "Open advanced search" → Click "Reset" → Select "Namespace" column → Select "=" operator → Enter "local-cluster" in Value field | oc get managedclusters local-cluster -o jsonpath='{.metadata.namespace}' | Search resets, namespace search configured, results show clusters in local-cluster namespace |

## Test Case 3: Test Complete Advanced Search Workflow Integration with Cluster List Table

**Description**: Validate the end-to-end advanced search workflow including multiple search constraints, constraint management, and integration with the cluster list table display.

**Setup**:
- Authenticated access to ACM Console
- Cluster list page with managed cluster data available  
- Advanced search functionality enabled and accessible

### Test Steps

| Step | Action | UI Method | CLI Method | Expected Result |
|------|---------|-----------|------------|-----------------|
| 1 | Log into ACM Console - Access ACM Console for complete workflow testing | Navigate to https://console-openshift-console.apps.CLUSTER-HOST | oc login https://api.CLUSTER-HOST:6443 --username=USERNAME --password=PASSWORD | ACM Console loaded with full cluster management access |
| 2 | Access cluster list with advanced search capabilities | Navigate to "Cluster management" → "Clusters" page | oc get managedclusters | Cluster list page displays with advanced search button visible |
| 3 | Create multiple search constraints for comprehensive testing | Open advanced search → Configure Name="local-cluster" → Click "Add a search constraint" → Configure second constraint Namespace="local-cluster" | oc get managedclusters local-cluster -o jsonpath='{.metadata.name}{" "}{.metadata.namespace}' | Multiple search constraints configured with both name and namespace criteria |
| 4 | Apply combined search criteria and validate results | Click "Close" to execute search with multiple constraints | oc get managedclusters -o custom-columns=NAME:.metadata.name,NAMESPACE:.metadata.namespace | Table displays clusters matching both name=local-cluster AND namespace=local-cluster |
| 5 | Test constraint removal functionality | Open advanced search → Click "Remove constraint" button for second constraint → Click "Close" | oc get managedclusters local-cluster | One constraint removed, search results update to show name-only filtering |
| 6 | Validate search reset and clear functionality | Open advanced search → Click "Reset" button → Click "Close" | oc get managedclusters | All search constraints cleared, full cluster list restored to original state |