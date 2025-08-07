# ACM-22079 JIRA Ticket Analysis

## Ticket Information
- **JIRA ID**: ACM-22079
- **Title**: Support digest-based upgrades via ClusterCurator for non-recommended upgrades
- **URL**: https://issues.redhat.com/browse/ACM-22079
- **Component**: Advanced Cluster Management (ACM) - ClusterCurator
- **Priority**: High (Customer requirement)
- **Customer**: Amadeus (Enterprise customer)

## Problem Statement

### Business Context
- **Customer Need**: Amadeus requires reliable cluster upgrades in disconnected/air-gapped environments
- **Current Issue**: Traditional tag-based image references fail in disconnected environments
- **Specific Requirement**: Support for non-recommended upgrade paths using image digests

### Technical Challenge
- **Environment**: Disconnected/air-gapped deployments
- **Problem**: Image tags like `4.5.10` resolve to `quay.io/openshift-release-dev/ocp-release:4.5.10-multi` which don't work reliably in disconnected environments
- **Solution**: Use cryptographic image digests (`@sha256:...`) instead of tags for precise image identification

## Feature Overview

### What It Does
1. **Digest Discovery**: When force upgrade annotation is present, ClusterCurator searches for image digests in the cluster's conditionalUpdates and availableUpdates
2. **Priority Order**: Searches conditionalUpdates first (non-recommended), then availableUpdates (recommended)
3. **Fallback Strategy**: If no digest found, gracefully falls back to traditional tag-based approach
4. **Force Flag Management**: Only uses `force: true` for tag-based upgrades, not needed for digest-based

### Key Benefits
- **Reliability**: Digests are immutable and work consistently in disconnected environments
- **Precision**: Exact image identification regardless of registry differences
- **Non-Recommended Support**: Enables upgrade paths not normally allowed
- **Backwards Compatibility**: Maintains existing functionality for recommended upgrades

## Implementation Summary

### Pull Request Details
- **PR Number**: #468
- **Title**: "ACM-22079 Initial non-recommended image digest feature"
- **Repository**: stolostron/cluster-curator-controller
- **Changes**: +400 -31 lines
- **Files Modified**: 4 files

### Code Changes Overview
1. **cmd/curator/curator.go**: Updated to use new LoadConfig() helper
2. **pkg/jobs/hive/hive.go**: Main implementation of digest-based upgrade logic
3. **pkg/jobs/hive/hive_test.go**: Comprehensive test cases for new functionality
4. **pkg/jobs/utils/helpers.go**: New LoadConfig() function for development support

## Customer Impact

### Direct Benefits for Amadeus
- **Reliable Upgrades**: Consistent upgrade behavior in air-gapped environments
- **Non-Recommended Paths**: Ability to skip intermediate versions as needed
- **Operational Flexibility**: Reduced dependency on external registry connectivity

### Broader ACM Customer Benefits
- **Disconnected Support**: Improves ACM deployment options for security-conscious customers
- **Enterprise Readiness**: Better support for complex enterprise upgrade scenarios
- **Risk Mitigation**: More reliable upgrade processes in constrained environments

## Technical Requirements for Testing

### Force Upgrade Annotation
```yaml
metadata:
  annotations:
    "cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions": "true"
```

### Example Digest Format
```
quay.io/openshift-release-dev/ocp-release@sha256:71e158c6173ad6aa6e356c119a87459196bbe70e89c0db1e35c1f63a87d90676
```

### ClusterVersion Structure
- **conditionalUpdates**: Non-recommended upgrades (searched first)
- **availableUpdates**: Recommended upgrades (fallback)
- **desiredUpdate**: Target upgrade specification

## Testing Focus Areas

### Core Functionality
1. **Digest Discovery**: Verify digest extraction from conditionalUpdates and availableUpdates
2. **Priority Logic**: Confirm conditionalUpdates searched before availableUpdates
3. **Fallback Behavior**: Test graceful degradation to tag-based approach
4. **Force Flag Logic**: Verify force flag only used for tag-based upgrades

### Environment Scenarios
1. **Disconnected Environment**: Simulate air-gapped deployment scenarios
2. **Non-Recommended Upgrades**: Test version skipping and candidate releases
3. **Backwards Compatibility**: Ensure existing recommended upgrade flows unaffected
4. **Error Conditions**: Test various failure scenarios and error handling

### ACM Integration
1. **ManagedClusterView**: Test cluster state retrieval and caching
2. **ManagedClusterAction**: Verify upgrade action creation and execution
3. **Hub-Spoke Communication**: Test communication in disconnected scenarios
4. **Monitoring and Logging**: Verify appropriate logging and status reporting

## Related Tickets and Dependencies
- **Base Functionality**: ClusterCurator upgrade mechanisms
- **Customer Escalations**: Related disconnected environment issues
- **Security Reviews**: Image digest validation and security implications

## Success Criteria for Testing
1. **Functional**: All digest-based upgrade scenarios work correctly
2. **Reliability**: Consistent behavior across different environments
3. **Performance**: No significant impact on upgrade timing
4. **Compatibility**: No regression in existing upgrade functionality
5. **Documentation**: Clear test documentation for future maintenance

---
*This analysis provides the foundation for comprehensive test case generation and implementation planning.*