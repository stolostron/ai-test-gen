# ACM-22079 Complete Analysis Report

## Summary
**Feature**: [JIRA:ACM-22079:Review:2025-08-21](https://issues.redhat.com/browse/ACM-22079)
**Customer Impact**: Critical capability for disconnected environments where image tags fail, enabling Amadeus and similar customers to perform non-recommended upgrades
**Implementation Status**: [GitHub:stolostron/cluster-curator-controller#468:merged:2025-07-16](https://github.com/stolostron/cluster-curator-controller/pull/468) - Initial non-recommended image digest feature
**Test Environment**: [Env:ashafi-atif-test:healthy:2025-08-21](https://console-openshift-console.apps.ashafi-atif-test.dev09.red-chesterfield.com) - OCP 4.19.7, AWS us-east-2
**Feature Validation**: ⚠️ **VERSION AWARE** - Feature targets ACM 2.15.0, test environment has OCP 4.19.7 (test cases prepared for future ACM deployment)
**Testing Approach**: Comprehensive E2E validation with digest configuration, fallback logic verification, and disconnected environment testing

## 1. JIRA Analysis Summary
**Ticket Details**: [JIRA:ACM-22079:Review:2025-08-21](https://issues.redhat.com/browse/ACM-22079)

**Business Requirements**: Urgent customer request from Amadeus for digest-based upgrade capability in disconnected environments. Traditional image tag approach fails in disconnected environments, requiring digest-based approach for non-recommended OpenShift upgrades.

**Technical Scope**: Enable ClusterCurator to use image digests from conditionalUpdates list for non-recommended upgrades, with intelligent fallback to availableUpdates list and backward-compatible image tag fallback.

**Customer Context**: Critical for disconnected environment operations where customers cannot rely on image tags for cluster upgrades outside recommended upgrade paths.

**Priority**: Critical - requires immediate attention following blocker issues
**Story Points**: 3 - moderate complexity implementation
**Component**: Cluster Lifecycle management within ACM

## 2. Environment Assessment
**Test Environment Health**: ✅ **HEALTHY** - Full connectivity and infrastructure verified
**Cluster Details**: [Env:ashafi-atif-test:healthy:2025-08-21](https://console-openshift-console.apps.ashafi-atif-test.dev09.red-chesterfield.com)

**Infrastructure Summary**:
- **Platform**: AWS us-east-2 region
- **OpenShift Version**: 4.19.7 (stable-4.19 channel)
- **Cluster ID**: fca2802e-f9c6-43b2-9f5e-bb83c134f275
- **Infrastructure ID**: ashafi-atif-test-fw9tt
- **Identity Provider**: kube:admin authentication
- **Connectivity**: API and Console access confirmed (200 OK)

**Real Environment Data**:
- API URL: `https://api.ashafi-atif-test.dev09.red-chesterfield.com:6443`
- Console URL: `https://console-openshift-console.apps.ashafi-atif-test.dev09.red-chesterfield.com`
- Username: kubeadmin
- Platform: AWS cloud infrastructure
- Region: us-east-2 availability

## 3. Implementation Analysis
**Primary Implementation**: [GitHub:stolostron/cluster-curator-controller#468:merged:2025-07-16](https://github.com/stolostron/cluster-curator-controller/pull/468)

**Code Changes Summary**:
- **Three-Tier Fallback Strategy**: Implemented conditionalUpdates → availableUpdates → image tag fallback logic
- **Digest Resolution Logic**: Added helper function in `pkg/jobs/utils/helpers.go` for digest lookup
- **Hive Integration**: Modified `pkg/jobs/hive/hive.go` for non-recommended annotation detection
- **Testing Capability**: Restored LoadConfig() function for local testing and development

**Technical Implementation Details**:
- **Lines Changed**: +400 additions, -31 deletions
- **Core Enhancement**: Modified upgrade workflow to query ClusterVersion conditionalUpdates
- **Annotation-Based Activation**: Uses `cluster.open-cluster-management.io/upgrade-allow-non-recommended: "true"`
- **Error Handling**: Robust fallback mechanism ensures backward compatibility

**Integration Points**:
- ClusterVersion conditionalUpdates API integration
- Hub cluster configuration management
- Remote cluster upgrade orchestration
- Ansible automation workflow compatibility

## 4. Test Scenarios Analysis
**Testing Strategy**: Comprehensive E2E validation covering digest configuration, fallback behavior, and disconnected environment scenarios

### Test Case 1: ClusterCurator Digest-Based Upgrade Configuration and Execution
**Scenario**: Primary digest upgrade workflow validation
**Purpose**: Validates core functionality of ClusterCurator digest-based upgrade configuration and successful execution
**Critical Validation**: Digest resolution from conditionalUpdates list and upgrade progress monitoring
**Customer Value**: Enables disconnected environment upgrades using reliable digest approach instead of failing image tags

### Test Case 2: Digest Fallback Logic Validation with Conditional Updates  
**Scenario**: Fallback behavior when digest unavailable in conditionalUpdates
**Purpose**: Verifies three-tier fallback logic (conditionalUpdates → availableUpdates → image tag)
**Critical Validation**: Automated fallback mechanism and backward compatibility preservation
**Customer Value**: Ensures robust upgrade capability even when optimal digest path is unavailable

### Test Case 3: Disconnected Environment Digest Upgrade Workflow
**Scenario**: Local registry digest upgrade in disconnected environment
**Purpose**: Validates complete disconnected environment workflow with local image registry integration
**Critical Validation**: Local registry access and digest resolution in isolated network environment
**Customer Value**: Addresses primary customer use case (Amadeus) for disconnected infrastructure operations

**Comprehensive Coverage Rationale**: These test scenarios provide complete validation of the digest upgrade feature across all deployment scenarios (connected, degraded, disconnected) while verifying both primary functionality and fallback behavior. The test cases address the core customer need (disconnected upgrades) while ensuring backward compatibility and robust error handling for enterprise environments.