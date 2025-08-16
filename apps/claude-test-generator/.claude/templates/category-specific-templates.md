# Category-Specific Test Scenario Templates

## 🎯 Quick Templates for Common Ticket Types

### For Upgrade Tickets (ACM/OpenShift Upgrades)

**Required Test Scenarios:**
1. **Pre-upgrade Environment Validation** - Verify cluster health and backup status
2. **Upgrade Prerequisites Check** - Validate version compatibility and resource requirements  
3. **Upgrade Execution and Monitoring** - Execute upgrade and monitor progress
4. **Post-upgrade Feature Validation** - Verify all features work after upgrade
5. **Rollback Testing (if applicable)** - Test rollback procedures if upgrade fails

**Sample Test Case Structure:**
```markdown
## Test Case 1: Complete Pre-upgrade to Post-upgrade Validation

**Description:** End-to-end validation of ACM upgrade from version X.Y to X.Z including rollback verification.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify` | Login successful with cluster access confirmed |
| **Step 2: Verify current ACM version** - Check installed version: `oc get multiclusterhub -A -o jsonpath='{.items[0].status.currentVersion}'` | Current version displays as expected:
```
2.9.0
``` |
```

### For UI Changes/Frontend Features

**Required Test Scenarios:**
1. **Component Rendering Validation** - Verify new UI components display correctly
2. **User Interaction Flow Testing** - Test click paths and form submissions
3. **Visual Regression Detection** - Compare before/after screenshots
4. **Accessibility Compliance** - Verify keyboard navigation and screen readers
5. **Cross-browser Compatibility** - Test on Chrome, Firefox, Safari

**Sample Test Case Structure:**
```markdown
## Test Case 1: New UI Component Interaction Validation

**Description:** Validates new dashboard component renders and responds to user interactions.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify` | Login successful and ready for console access |
| **Step 2: Access ACM Console** - Open browser and navigate to ACM console: `https://multicloud-console.apps.cluster-url.com` | ACM console loads with new component visible |
```

### For Import/Export Features

**Required Test Scenarios:**
1. **Happy Path Import** - Successful import with valid configuration
2. **Import with Validation Errors** - Handle malformed or invalid data  
3. **Retry Mechanisms** - Test automatic and manual retry functionality
4. **Timeout and Interruption Handling** - Test behavior during network issues
5. **Cleanup and Resource Management** - Verify proper resource cleanup

**Sample Test Case Structure:**
```markdown
## Test Case 1: Complete Import-Export Lifecycle Validation

**Description:** End-to-end testing of cluster import with error handling and cleanup validation.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify` | Login successful and ready for import operations |
| **Step 2: Prepare import configuration** - Create import YAML: `oc apply -f import-config.yaml` | Import configuration created successfully:
```
managedcluster.cluster.open-cluster-management.io/test-cluster created
``` |
```

### For API/Backend Changes

**Required Test Scenarios:**
1. **API Endpoint Functionality** - Test new/modified API endpoints
2. **Request/Response Validation** - Verify correct data formats and responses
3. **Authentication and Authorization** - Test security controls
4. **Performance and Load Testing** - Verify performance under load
5. **Error Handling and Edge Cases** - Test boundary conditions

**Sample Test Case Structure:**
```markdown
## Test Case 1: New API Endpoint Validation

**Description:** Comprehensive testing of new REST API endpoint including authentication and error handling.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify` | Login successful with API access token obtained |
| **Step 2: Test API endpoint** - Make API call: `curl -k -H "Authorization: Bearer $(oc whoami -t)" https://api.cluster-url.com/apis/new-endpoint` | API responds with expected data:
```json
{
  "status": "success",
  "data": {...}
}
``` |
```

### For Security/RBAC Features

**Required Test Scenarios:**
1. **Permission Grant Testing** - Verify new permissions work correctly
2. **Permission Denial Testing** - Confirm unauthorized access is blocked
3. **Role Inheritance** - Test role hierarchy and inheritance
4. **Audit Trail Validation** - Verify security events are logged
5. **Cross-tenant Isolation** - Ensure proper tenant separation

### For Performance/Scalability Features  

**Required Test Scenarios:**
1. **Baseline Performance Measurement** - Establish performance baseline
2. **Load Testing** - Test behavior under expected load
3. **Stress Testing** - Test behavior beyond normal limits
4. **Resource Utilization** - Monitor CPU, memory, storage usage
5. **Scaling Validation** - Test auto-scaling and manual scaling

### For Integration Features

**Required Test Scenarios:**
1. **Integration Point Testing** - Test all external system connections
2. **Data Flow Validation** - Verify data moves correctly between systems
3. **Error Propagation** - Test how errors are handled across systems
4. **Dependency Management** - Test behavior when dependencies are unavailable
5. **Version Compatibility** - Test with different versions of integrated systems

## 🔧 Usage Guidelines

1. **Select appropriate template** based on ticket type/component
2. **Customize scenarios** to match specific feature requirements
3. **Always maintain exact format** requirements (login step, deployment status header)
4. **Include realistic sample outputs** for all validation steps
5. **Focus on NEW functionality** - avoid testing unchanged components

## 📋 Quality Checklist

Before using any template:
- [ ] No HTML tags anywhere
- [ ] Exact login step format
- [ ] Deployment status header correct
- [ ] Sample outputs included
- [ ] No internal script references
- [ ] Verbal instructions before commands