# Complete Analysis: ACM-22079 - Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Implementation Status

**Feature Implementation:** ✅ **COMPLETED**  
**Primary PR:** [#468 - ACM-22079 Initial non-recommended image digest feature](https://github.com/stolostron/cluster-curator-controller/pull/468)  
**Deployment Status:** Feature merged and available in cluster-curator-controller  
**Key Behavior:** Hierarchical image lookup (conditionalUpdates → availableUpdates → tag fallback)

**Technical Implementation Details:**
- **New Function:** `GetImageDigestFromClusterVersion()` in `pkg/jobs/utils/helpers.go`
- **Priority Logic:** Searches conditionalUpdates first for non-recommended versions, then availableUpdates
- **Fallback Mechanism:** Uses image tag format for backward compatibility when digest lookup fails
- **Hive Integration:** Modified `pkg/jobs/hive/hive.go` to call digest lookup during upgrade processing
- **Logging Enhancement:** Added source tracking for debugging (conditionalUpdates vs availableUpdates vs fallback)

## Environment & Validation Status

**Environment:** qe6-vmware-ibm cluster (OpenShift 4.19.6)  
**Validation Results:**
- ✅ ClusterCurator CRD available and accessible
- ✅ ClusterVersion conditionalUpdates structure confirmed  
- ✅ Hub cluster connectivity and permissions validated
- ✅ Schema inspection completed for desiredUpdate field
- ⚠️ No existing ClusterCurator instances for live testing validation

**Limitations Encountered:**
- Limited conditionalUpdates data in current cluster state for comprehensive validation
- Test cases use realistic scenarios based on implementation analysis and schema inspection

## Investigation Summary

**JIRA Hierarchy Analysis:**
- **Main Story:** ACM-22079 - Critical priority feature for Amadeus customer requirement
- **QE Task:** ACM-22080 - Manual test case developed: "Set ClusterCurator desiredUpdate to non-recommended version, verify image digest usage"
- **QE Automation:** ACM-22081 - Automation task for test coverage
- **Documentation:** ACM-22457 - Documentation update for non-recommended upgrade procedures

**GitHub Analysis:**
- **Commit:** be3fbc0 - "ACM-22079 Initial non-recommended image digest feature (#468)"
- **Repository:** stolostron/cluster-curator-controller
- **Code Review:** 81.2% test coverage achieved, proper error handling implemented
- **Quality Gates:** All checks passed, approved and merged

**Customer Context:**
- **Urgency:** Critical request from Amadeus for disconnected environment support
- **Problem:** Image tags don't work in disconnected environments for non-recommended upgrades
- **Solution:** Use image digests from ClusterVersion conditionalUpdates for reliable upgrade paths

## Feature Summary

This feature enables ClusterCurator to handle non-recommended OpenShift upgrades in disconnected environments by using image digests instead of tags. The implementation adds intelligent lookup logic that prioritizes conditionalUpdates for non-recommended versions while maintaining backward compatibility.

**Key Capabilities:**
1. **Digest Lookup Priority:** Searches conditionalUpdates first when the `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'` annotation is present
2. **Graceful Fallback:** Falls back to availableUpdates if version not found in conditionalUpdates
3. **Backward Compatibility:** Uses image tag format when digest lookup fails entirely
4. **Enhanced Logging:** Provides clear source tracking for debugging upgrade paths
5. **Error Handling:** Robust error handling for invalid versions and lookup failures

**Annotation Requirement:**
The feature is activated by adding the annotation `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'` to the ClusterCurator resource, ensuring controlled usage for non-recommended upgrades.

## Deployment Assessment

**Current Availability:** ✅ **READY FOR TESTING**  
**Implementation Evidence:** 
- PR #468 merged into cluster-curator-controller repository
- Feature code available in latest builds
- Schema validation confirms ClusterCurator supports required fields

**Testing Readiness:**
- ✅ All test cases can be executed with proper cluster setup
- ✅ Feature functionality is fully implemented and available
- ✅ Environment supports ClusterCurator operations
- ⚠️ Requires managed clusters with appropriate OpenShift versions for complete validation

**Recommendations:**
1. Execute test cases in environment with managed clusters that have conditionalUpdates
2. Validate both success and failure scenarios with various version combinations
3. Confirm logging output provides sufficient debugging information
4. Test annotation requirement enforcement