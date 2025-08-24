# Test Cases for ACM-13644: Support advanced search input - Iteration 1 - Exact string match search against any valid column

## Description
Validate ACM Console advanced search functionality including fuzzy search and exact string match search capabilities for cluster list filtering with Key-Operator-Value styled search components.

## Setup
- Access to ACM Hub cluster with Console enabled and multiple managed clusters
- Test clusters with varying names, namespaces, and distribution versions for search validation
- AcmTable component with advanced search functionality implemented
- PatternFly SearchInput component integration in Console interface

## Test Cases

### Test Case 1: Basic Fuzzy Search Functionality

**Description**: Verify fuzzy search capability works correctly for cluster name and namespace filtering in the cluster list page.

**Step 1: Log into ACM Console** - Access ACM Console for fuzzy search testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in via Console authentication and navigate to "Infrastructure" → "Clusters"
- **CLI Method**: Authenticate and verify cluster access: `oc login https://api.<cluster-host>:6443 -u <username> -p <password>`
- **Expected Results**: Clusters page loads with searchable cluster list and advanced search button visible

**Step 2: Access Fuzzy Search Interface** - Open the search functionality for basic text-based cluster filtering
- **UI Method**: Click the search input field in the clusters table toolbar
- **CLI Method**: List available clusters for reference: `oc get managedclusters -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[0].type`
- **Expected Results**: Search input field is active and accepts text input for fuzzy matching

**Step 3: Execute Fuzzy Search Query** - Perform partial text search to validate fuzzy matching functionality
- **UI Method**: Type partial cluster name (e.g., "prod" for "production-cluster") in search input
- **CLI Method**: Search clusters with grep pattern: `oc get managedclusters | grep -i prod`
- **Expected Results**: Cluster list filters to show matching results with search terms highlighted in cluster names

**Step 4: Test Search Highlighting** - Verify search result highlighting displays matched terms clearly
- **UI Method**: Observe highlighted text in search results showing matched portions of cluster names
- **CLI Method**: Verify search pattern matching: `oc get managedclusters -o name | grep -i prod | wc -l`
- **Expected Results**: Matched search terms are visually highlighted in cluster list with appropriate styling

**Step 5: Clear Search Results** - Validate search clearing functionality returns to full cluster list
- **UI Method**: Click the clear button (X) in search input field or press Escape key
- **CLI Method**: Display all clusters again: `oc get managedclusters`
- **Expected Results**: Search input clears and cluster list returns to showing all available clusters

### Test Case 2: Advanced Search with Key-Operator-Value Interface

**Description**: Validate advanced search functionality using structured Key-Operator-Value search components for exact string matching against specific columns.

**Step 1: Log into ACM Console** - Access ACM Console for advanced search testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to "Infrastructure" → "Clusters" and locate advanced search functionality
- **CLI Method**: Prepare test environment: `oc get managedclusters -o custom-columns=NAME:.metadata.name,NAMESPACE:.metadata.namespace`
- **Expected Results**: Clusters page displays with advanced search button accessible in toolbar

**Step 2: Open Advanced Search Modal** - Access the Key-Operator-Value search interface for structured filtering
- **UI Method**: Click "Open advanced search" button to display the advanced search popper/modal
- **CLI Method**: Identify searchable cluster attributes: `oc get managedclusters -o yaml | grep -E "name:|namespace:" | head -6`
- **Expected Results**: Advanced search modal opens showing fuzzy search input and structured search fields (Column, Operator, Value)

**Step 3: Configure Name-Based Search** - Set up exact string match search for cluster name column
- **UI Method**: Select "Name" from Column dropdown, select "=" operator, enter exact cluster name in Value field
- **CLI Method**: Create test filter yaml `name-search-test.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: search-test-config
data:
  search-column: "name"
  search-operator: "="
  search-value: "local-cluster"
```
- **Expected Results**: Advanced search form configured with Name column, equals operator, and specific cluster name value

**Step 4: Execute Advanced Search** - Run the structured search and validate exact matching results
- **UI Method**: Click "Run search" or "Apply" button to execute the configured advanced search
- **CLI Method**: Validate exact name match: `oc get managedclusters -o name | grep "local-cluster"`
- **Expected Results**: Cluster list filters to show only clusters with exact name match, other clusters hidden

**Step 5: Test Multiple Search Constraints** - Add additional search constraints to validate multi-criteria filtering
- **UI Method**: Add second constraint for namespace column with exact namespace match
- **CLI Method**: Test multi-criteria search: `oc get managedclusters -o custom-columns=NAME:.metadata.name,NS:.metadata.namespace | grep "local-cluster\|open-cluster"`
- **Expected Results**: Multiple search constraints combine with AND logic, showing clusters meeting all criteria

**Step 6: Reset Advanced Search** - Clear all search constraints and return to unfiltered cluster list
- **UI Method**: Click "Reset" or "Clear all" button to remove all search constraints
- **CLI Method**: Display all clusters: `oc get managedclusters --no-headers | wc -l`
- **Expected Results**: All search constraints removed, cluster list returns to displaying all available clusters

### Test Case 3: Distribution Version Search with Operator Comparison

**Description**: Validate advanced search functionality for distribution version filtering using comparison operators (>, <, >=, <=, !=) for semantic version matching.

**Step 1: Log into ACM Console** - Access ACM Console for version-based search testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to clusters page and access advanced search for version filtering
- **CLI Method**: Check cluster distribution versions: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}'`
- **Expected Results**: Clusters page accessible with version information visible for comparison testing

**Step 2: Configure Version Comparison Search** - Set up distribution version search with greater-than operator
- **UI Method**: Open advanced search, select "Distribution version" column, choose ">" operator, enter version "4.12"
- **CLI Method**: Create version comparison test: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}' | grep -E "4\.(1[3-9]|[2-9][0-9])"`
- **Expected Results**: Advanced search configured with Distribution version column, greater-than operator, and version comparison value

**Step 3: Execute Version-Based Filtering** - Run semantic version comparison search and validate results
- **UI Method**: Apply the version search to filter clusters with distribution versions greater than specified value
- **CLI Method**: Validate version filtering logic with test YAML `version-filter-test.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: version-filter-config
data:
  filter-column: "distribution"
  filter-operator: ">"
  filter-value: "4.12"
  expected-matches: "clusters with Kubernetes 4.13+ versions"
```
- **Expected Results**: Cluster list shows only clusters with distribution versions higher than 4.12, using semantic version comparison

**Step 4: Test Additional Version Operators** - Validate different comparison operators for version filtering
- **UI Method**: Test "<=", ">=", "!=" operators with various version values to verify operator logic
- **CLI Method**: Compare version operators: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}' | awk -F': ' '$2 <= "4.11"'`
- **Expected Results**: Each operator correctly filters clusters based on semantic version comparison logic

**Step 5: Validate Inferred Range Logic** - Test partial version matching with automatic range inference
- **UI Method**: Enter partial version "4.13" and verify it matches 4.13.x versions correctly
- **CLI Method**: Test partial version matching: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}' | grep "4\.13"`
- **Expected Results**: Partial version input correctly infers version ranges and matches appropriate cluster versions