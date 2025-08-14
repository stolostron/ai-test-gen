# ACM-22079: Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## 🚨 DEPLOYMENT STATUS

**Status**: ❌ NOT DEPLOYED  
**Evidence**: This is a new feature targeting ACM 2.15+ (current development phase). The feature requires annotation `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'` and enhanced ClusterCurator controller logic that checks conditional updates for image digests before falling back to image tags.

**Version Correlation**: 
- Feature filed: July 2025 (ACM-22079)
- Target release: ACM 2.15+
- Documentation ticket: ACM-22457 (Backlog - waiting for 2.15 branch)
- Current status: Development/Review phase

**Deployment Assessment**:
- **Controller Enhancement**: stolostron/cluster-curator-controller needs updates for digest-based logic
- **Annotation Support**: New annotation processing for non-recommended version allowance
- **Conditional Updates Integration**: Enhanced logic to check Cincinnati conditional updates API
- **Fallback Mechanism**: Digest-first approach with image tag fallback

## Implementation Status

**Feature Summary**: Urgent customer request (Amadeus) to enable digest-based upgrades for non-recommended OpenShift versions in disconnected environments where image tags don't work properly.

**Key Changes Required**:
1. **Annotation Processing**: Support for `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`
2. **Digest Resolution**: Check conditional updates list for image digest of target version
3. **Fallback Logic**: Use image tag if digest not found in conditional updates
4. **Non-recommended Support**: Allow upgrades to versions marked as having issues/not recommended

**Related Work**:
- **QE Task**: ACM-22080 (In Progress) - Test case creation and validation
- **QE Automation**: ACM-22081 (New) - Automation test implementation  
- **Documentation**: ACM-22457 (Backlog) - User documentation for the feature

## Environment & Validation Status

**Test Environment**: Standard cluster with ACM/MCE installed required for validation
**Validation Approach**: AI-powered analysis of JIRA hierarchy, GitHub investigation, and technical documentation
**Limitations**: Feature not yet deployed - test cases designed for post-implementation validation

**Key Validation Points**:
- ClusterCurator resource creation with non-recommended version annotation
- Verification that image digest is used instead of image tag on managed cluster
- Validation of upgrade behavior in disconnected environments
- Error handling when digest lookup fails

## Investigation Summary

**JIRA Analysis**: Complete 3-level hierarchy analysis covering main story (ACM-22079), QE tasks (ACM-22080, ACM-22081), and documentation work (ACM-22457)

**GitHub Investigation**: Enhanced analysis of stolostron/cluster-curator-controller repository and related cluster lifecycle repositories

**Technical Research**: Comprehensive research on OpenShift conditional updates, ClusterCurator architecture, and digest-based upgrade mechanisms

**Business Context**: Critical customer (Amadeus) requirement for disconnected environment upgrade support where standard image tag approach fails