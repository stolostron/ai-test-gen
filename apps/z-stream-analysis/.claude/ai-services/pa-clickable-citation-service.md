# PA Clickable Citation Enhancement Service V4.0

## Service Overview
Transforms all citations in analysis reports into clickable links for enhanced user navigation and enterprise audit trail accessibility.

## Citation Link Formats

### Jenkins Citation Links
**Format:** `[Jenkins:job_name:build_number:result:timestamp](jenkins_url)`

**Examples:**
- `[Jenkins:alc_e2e_tests:2412:UNSTABLE:2025-08-15T18:39:15Z](https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc/job/alc_e2e_tests/2412/)`
- `[Jenkins:clc-e2e-pipeline:3313:FAILURE:2024-01-15T10:30:00Z](https://jenkins-url/job/clc-e2e-pipeline/3313/)`

### Repository Citation Links  
**Format:** `[Repo:branch:file_path:lines:commit_sha](github_url)`

**Examples:**
- `[Repo:release-2.11:tests/cypress/tests/integration/Argo_Appset_Row_Action_Test_Suite.js:75-117:1c7a333c](https://github.com/stolostron/application-ui-test/blob/release-2.11/tests/cypress/tests/integration/Argo_Appset_Row_Action_Test_Suite.js#L75-L117)`
- `[Repo:main:src/components/ClusterList.tsx:23:b2c3d4e5](https://github.com/org/repo/blob/main/src/components/ClusterList.tsx#L23)`

### Environment Citation Links
**Format:** `[Env:cluster_url:connectivity:timestamp](cluster_console_url)`

**Examples:**
- `[Env:https://api.cqu-acm2118-pp.dev09.red-chesterfield.com:6443:200:2025-08-16T16:10:00Z](https://console-openshift-console.apps.cqu-acm2118-pp.dev09.red-chesterfield.com)`
- `[Env:https://api.cluster.example.com:200:2024-01-15T10:30:00Z](https://console.cluster.example.com)`

### Fix Citation Links
**Format:** `[Fix:file_path:operation:lines_affected:verification](github_file_url)`

**Examples:**  
- `[Fix:tests/e2e/cluster_test.js:modify:45-52:syntax_valid](https://github.com/org/repo/blob/main/tests/e2e/cluster_test.js#L45-L52)`
- `[Fix:package.json:update:dependencies:verified](https://github.com/org/repo/blob/main/package.json)`

### JIRA Citation Links
**Format:** `[JIRA:ticket_id:status:last_updated](jira_url)`

**Examples:**
- `[JIRA:ACM-22079:Open:2024-01-15](https://issues.redhat.com/browse/ACM-22079)`
- `[JIRA:RHACM4K-6772:Resolved:2024-01-20](https://issues.redhat.com/browse/RHACM4K-6772)`

## URL Construction Rules

### Jenkins URLs
```
Base: {jenkins_base_url}/job/{job_path}/{build_number}/
Console: {jenkins_base_url}/job/{job_path}/{build_number}/console
API: {jenkins_base_url}/job/{job_path}/{build_number}/api/json
```

### GitHub URLs  
```
File: https://github.com/{org}/{repo}/blob/{branch}/{file_path}
Lines: https://github.com/{org}/{repo}/blob/{branch}/{file_path}#L{start}-L{end}
Commit: https://github.com/{org}/{repo}/commit/{commit_sha}
```

### OpenShift Console URLs
```
Main: https://console-openshift-console.apps.{cluster_domain}
API: https://api.{cluster_domain}:6443
Specific Resource: {console_url}/k8s/ns/{namespace}/{resource_type}/{resource_name}
```

### JIRA URLs
```
Ticket: https://issues.redhat.com/browse/{ticket_id}
Search: https://issues.redhat.com/issues/?jql={search_query}
```

## Implementation Guidelines

### 1. Citation Detection
- Scan report for all citation patterns: `[Source:details]`
- Extract citation components: source type, identifiers, metadata
- Validate required URL construction parameters

### 2. URL Construction
- Use extracted Jenkins base URLs from analysis
- Construct GitHub URLs from repository metadata  
- Build console URLs from cluster domain extraction
- Generate JIRA URLs using standard Red Hat instance

### 3. Link Generation
- Transform `[Citation]` to `[Citation](URL)`
- Preserve all citation metadata for audit compliance
- Ensure links open in new tabs where appropriate
- Validate URL accessibility (optional)

### 4. Error Handling
- If URL construction fails, preserve original citation format
- Log URL construction errors for debugging
- Fallback to non-clickable citations if needed

## Service Integration

This service is automatically invoked during report generation in:
- Detailed analysis reports  
- Executive summaries
- Fix recommendation documents
- Audit trail documentation

## Quality Assurance

- **Link Validation**: Verify constructed URLs are accessible
- **Format Consistency**: Ensure all citations follow standard patterns  
- **Audit Compliance**: Maintain full citation metadata integrity
- **User Experience**: Optimize for navigation and accessibility

## Version History
- V4.0: Initial clickable citation implementation
- Future: Enhanced validation and accessibility features

---
*PA Clickable Citation Enhancement Service - Enterprise AI Services V4.0*