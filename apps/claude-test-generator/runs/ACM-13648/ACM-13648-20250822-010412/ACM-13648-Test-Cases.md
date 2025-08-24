# Test Cases for ACM-13648: Support advanced search input - Iteration 2 - advanced search will support filtering for the "Version distribution"

## Description
Validate ACM Console advanced search functionality for distribution version filtering using semantic version comparison operators (>, <, >=, <=, !=, =) with multiple AND constraints support.

## Setup
- Access to ACM Hub cluster with Console enabled and multiple managed clusters with varying distribution versions
- Test clusters with different OpenShift/Kubernetes versions for semantic version comparison validation
- AcmSearchInput component with distribution version filtering capabilities implemented
- Advanced search interface with full operator support for version comparison

## Test Cases

### Test Case 1: Basic Distribution Version Filtering with Comparison Operators

**Description**: Verify semantic version comparison functionality for distribution version filtering using greater than and less than operators.

**Step 1: Log into ACM Console** - Access ACM Console for distribution version filtering testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Log in via Console authentication and navigate to "Infrastructure" → "Clusters"
- **CLI Method**: Authenticate and check cluster versions: `oc login https://api.<cluster-host>:6443 -u <username> -p <password>`
- **Expected Results**: Clusters page loads with multiple clusters showing different distribution versions in the cluster list

**Step 2: Access Advanced Search for Version Filtering** - Open advanced search interface to configure distribution version comparison
- **UI Method**: Click "Open advanced search" button to display the advanced search modal with version filtering options
- **CLI Method**: Query cluster distribution versions: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}'`
- **Expected Results**: Advanced search modal opens showing Column dropdown with "Distribution version" option available

**Step 3: Configure Greater Than Version Search** - Set up semantic version comparison using greater than operator
- **UI Method**: Select "Distribution version" from Column dropdown, choose ">" operator, enter version "4.12.0" in Value field
- **CLI Method**: Create version filter test YAML `version-gt-test.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: version-comparison-test
data:
  search-column: "distribution"
  search-operator: ">"
  search-value: "4.12.0"
  expected-behavior: "semantic-version-comparison"
```
- **Expected Results**: Advanced search form configured with Distribution version column, greater than operator, and semantic version value

**Step 4: Execute Version Comparison Search** - Run semantic version filtering and validate comparison logic
- **UI Method**: Click "Run search" to apply version filtering, observe cluster list filtered by version comparison
- **CLI Method**: Validate version comparison logic: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}' | awk -F': ' '$2 > "4.12.0"'`
- **Expected Results**: Cluster list shows only clusters with distribution versions semantically greater than 4.12.0 (e.g., 4.13.x, 4.14.x)

**Step 5: Test Less Than Operator** - Validate less than semantic version comparison functionality
- **UI Method**: Change operator to "<" and enter "4.14.0" to filter clusters with older versions
- **CLI Method**: Test less than comparison: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}' | awk -F': ' '$2 < "4.14.0"'`
- **Expected Results**: Cluster list updates to show only clusters with versions semantically less than 4.14.0

### Test Case 2: Advanced Version Operators and Range-Based Filtering

**Description**: Validate comprehensive operator support including greater than or equal, less than or equal, and not equal operators for version comparison.

**Step 1: Log into ACM Console** - Access ACM Console for comprehensive version operator testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to clusters page and access advanced search for operator testing
- **CLI Method**: Gather version data for testing: `oc get managedclusters -o custom-columns=NAME:.metadata.name,VERSION:.status.version.kubernetes`
- **Expected Results**: Clusters page accessible with version information visible for comprehensive operator testing

**Step 2: Test Greater Than or Equal Operator** - Validate inclusive minimum version filtering functionality
- **UI Method**: Configure advanced search with "Distribution version" column, ">=" operator, value "4.13.0"
- **CLI Method**: Simulate greater than or equal logic: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}' | awk -F': ' '$2 >= "4.13.0"'`
- **Expected Results**: Cluster list includes clusters with versions 4.13.0 and higher, demonstrating inclusive comparison

**Step 3: Test Less Than or Equal Operator** - Verify inclusive maximum version filtering capabilities
- **UI Method**: Change operator to "<=" and test with version "4.13.5" to include boundary version
- **CLI Method**: Test inclusive maximum: Create test YAML `version-lte-test.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: version-lte-comparison
data:
  operator: "<="
  test-value: "4.13.5"
  expected-results: "4.13.5 and earlier versions included"
  boundary-test: "4.13.5 should be included in results"
```
- **Expected Results**: Cluster list shows versions 4.13.5 and earlier, confirming inclusive boundary behavior

**Step 4: Test Not Equal Operator** - Validate version exclusion filtering functionality
- **UI Method**: Configure search with "!=" operator and specific version to exclude from results
- **CLI Method**: Test exclusion logic: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}' | awk -F': ' '$2 != "4.13.0"'`
- **Expected Results**: Cluster list excludes the specified version while showing all other versions

**Step 5: Test Partial Version Matching** - Verify inferred range logic for incomplete version inputs
- **UI Method**: Enter partial version "4.13" and observe automatic range inference behavior
- **CLI Method**: Test partial version matching: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}' | grep "4\.13"`
- **Expected Results**: Partial version "4.13" matches all 4.13.x versions using semantic version range logic

### Test Case 3: Multiple AND Constraints for Distribution Version Filtering

**Description**: Validate advanced search functionality supporting multiple simultaneous distribution version constraints with logical AND combination.

**Step 1: Log into ACM Console** - Access ACM Console for multi-constraint version filtering testing: Navigate to https://console-openshift-console.apps.<cluster-host>
- **UI Method**: Navigate to clusters page and prepare for complex multi-constraint search configuration
- **CLI Method**: Prepare comprehensive version data: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": OpenShift "}{.status.version.kubernetes}{"\n"}{end}'`
- **Expected Results**: Clusters page displays with advanced search capability for multiple constraint configuration

**Step 2: Configure Primary Version Constraint** - Set up first distribution version filter as baseline for multi-constraint testing
- **UI Method**: Open advanced search, configure "Distribution version" with ">=" operator and "4.12.0" value
- **CLI Method**: Establish baseline filter: Create multi-constraint test YAML `multi-version-test.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: multi-constraint-version-test
data:
  constraint-1-column: "distribution"
  constraint-1-operator: ">="
  constraint-1-value: "4.12.0"
  constraint-2-column: "distribution"
  constraint-2-operator: "<"
  constraint-2-value: "4.15.0"
  logic-operator: "AND"
```
- **Expected Results**: First constraint configured showing clusters with versions 4.12.0 and higher

**Step 3: Add Second Version Constraint** - Configure additional version filter to create range-based filtering
- **UI Method**: Click "Add constraint" button, add second "Distribution version" constraint with "<" operator and "4.15.0" value
- **CLI Method**: Test range logic: `oc get managedclusters -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.status.version.kubernetes}{"\n"}{end}' | awk -F': ' '$2 >= "4.12.0" && $2 < "4.15.0"'`
- **Expected Results**: Multiple constraints visible in advanced search interface, both constraints active simultaneously

**Step 4: Execute Multi-Constraint Search** - Apply multiple version constraints and validate AND logic combination
- **UI Method**: Apply the multi-constraint search to filter clusters within the specified version range
- **CLI Method**: Validate AND logic behavior: `oc get managedclusters -o custom-columns=NAME:.metadata.name,VERSION:.status.version.kubernetes | awk 'NR>1 && $2 >= "4.12.0" && $2 < "4.15.0"'`
- **Expected Results**: Cluster list shows only clusters with versions between 4.12.0 (inclusive) and 4.15.0 (exclusive)

**Step 5: Test Constraint Management** - Validate adding, editing, and removing individual version constraints
- **UI Method**: Add third constraint, then remove middle constraint to test constraint management functionality
- **CLI Method**: Test constraint removal simulation by modifying filter criteria and re-running version queries
- **Expected Results**: Constraint management works correctly, allowing dynamic addition and removal of version filters with real-time result updates