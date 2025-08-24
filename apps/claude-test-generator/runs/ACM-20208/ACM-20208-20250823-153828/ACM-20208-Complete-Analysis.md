# Complete Analysis for ACM-20208: Support Hub Name Access for RBAC Users

## Summary
**Feature**: [ACM-20208: Support hub name access for RBAC users](https://issues.redhat.com/browse/ACM-20208)  
**Customer Impact**: Enables console functionality for organizations using granular RBAC policies by preventing crashes when users lack ManagedCluster permissions  
**Implementation Status**: [GitHub PR #4450: ACM-20208 Support hub name access for RBAC users](https://github.com/stolostron/console/pull/4450) - MERGED  
**Test Environment**: [mist10-0.qe.red-chesterfield.com Console](https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com) - ACM 2.14.0-62, MCE 2.9.0-212  
**Feature Validation**: ✅ FULLY AVAILABLE - Feature implemented and deployed in test environment  
**Testing Approach**: RBAC user console access validation with multi-user permission scenarios and API endpoint testing

## 1. JIRA Analysis Summary
**Ticket Details**: [ACM-20208: Support hub name access for RBAC users](https://issues.redhat.com/browse/ACM-20208) - Closed (Resolution: Done)

**Core Problem**: Console functionality dependent on hub cluster name fails for users without ManagedCluster permissions, causing application topology crashes and broken user experience.

**Root Cause**: Console previously required user-level ManagedCluster permissions to access hub cluster name, creating dependency between user RBAC permissions and basic console functionality.

**Business Value**: Organizations with granular RBAC policies can now provide ACM console access to users without compromising security or functionality. Prevents complete console failure scenarios for permission-restricted users.

**Requirements**: Console must access hub cluster name regardless of user ManagedCluster permissions while maintaining authentication security requirements.

**Fix Version**: ACM 2.14.0, MCE 2.9.0 - Compatible with test environment (ACM 2.14.0-62, MCE 2.9.0-212)

## 2. Environment Assessment
**Test Environment Health**: 10/10 - EXCELLENT  
**Cluster Details**: [mist10-0.qe.red-chesterfield.com](https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com) - 33 ACM pods running, MultiClusterHub status: Running

**Environment Readiness**:
- ✅ ACM 2.14.0-62 deployed (includes target feature)
- ✅ Console accessible via OpenShift integration
- ✅ Hub cluster: local-cluster (ideal for testing hub name functionality)
- ✅ 14 RBAC test users with varying permission levels
- ✅ Multiple user types: cluster-admin, namespace-admin, application-manager

**RBAC Testing Environment**:
- **Full Admin**: kubeadmin (baseline testing)
- **Cluster Admin**: clc-e2e-admin-cluster (cluster-level permissions)
- **Namespace Admin**: clc-e2e-admin-ns (limited namespace permissions)
- **Application Manager**: app-test-cluster-manager-admin (application focus)

**Infrastructure Health**: Console components healthy, authentication working, ACM MultiClusterHub operational

## 3. Implementation Analysis
**Primary Implementation**: [GitHub PR #4450: ACM-20208 Support hub name access for RBAC users](https://github.com/stolostron/console/pull/4450) - MERGED (2025-05-05)

**Technical Architecture**:
- **New Backend Endpoint**: GET /multicloud/hub (renamed from /globalhub)
- **Security Model**: User authentication required + service account authorization bypass
- **Hub Name Caching**: Hub cluster name cached from ManagedCluster resources with local-cluster=true label
- **API Response**: Enhanced to include localHubName field alongside existing isGlobalHub and isHubSelfManaged

**Code Changes**:
- **Backend Route**: backend/src/routes/hub.ts implements new endpoint with service account token usage
- **Hub Detection**: backend/src/routes/events.ts caches hub name from ManagedCluster labels
- **API Integration**: Frontend updated to consume localHubName from enhanced API response
- **Authentication Flow**: Maintains user authentication requirement while bypassing ManagedCluster permissions

**Security Implementation**:
- **User Authentication**: getAuthenticatedToken() validates user is logged in
- **Service Account Access**: getServiceAccountToken() provides elevated ManagedCluster access
- **Permission Separation**: User tokens for authentication, service account tokens for resource access
- **Cache Security**: Hub name cached securely from trusted ManagedCluster resource data

**Previous Related Work**:
- PR #4220: Frontend hub name state management (foundation)
- PR #4078: Remove hard-coded local-cluster references (preparation)
- PR #4205: Backend hub name detection implementation (building blocks)

## 4. Test Scenarios Analysis
**Testing Strategy**: Multi-user RBAC validation with comprehensive console functionality testing

### Test Case 1: Verify RBAC User Console Access Without ManagedCluster Permissions
**Scenario**: Primary RBAC user access validation  
**Purpose**: Validates core feature functionality for users without ManagedCluster permissions  
**Critical Validation**: Console navigation, hub name display, API integration, error handling  
**Customer Value**: Ensures basic console functionality works for permission-restricted users

### Test Case 2: Validate Hub Cluster Name Display for Namespace-Admin Users  
**Scenario**: Limited permission user experience validation  
**Purpose**: Confirms hub name displays correctly for users with namespace-scoped permissions  
**Critical Validation**: Hub name consistency, permission boundary respect, cross-section navigation  
**Customer Value**: Validates user experience for common RBAC permission patterns

### Test Case 3: Test Multi-User Hub Name Access Scenarios
**Scenario**: Comprehensive multi-user permission validation  
**Purpose**: Ensures consistent hub name access across all user permission levels  
**Critical Validation**: Permission independence, application topology stability, security model verification  
**Customer Value**: Confirms feature works universally across organizational RBAC structures

**Comprehensive Coverage Rationale**: These scenarios provide complete validation of the RBAC independence feature across all user permission levels, console sections, and critical integration points. Testing covers both positive scenarios (feature works) and regression prevention (ACM-20085 fix validation), ensuring comprehensive user experience validation while maintaining security model integrity.