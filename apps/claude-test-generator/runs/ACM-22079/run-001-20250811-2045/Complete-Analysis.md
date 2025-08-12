# Complete Analysis - ACM-22079: Support digest-based upgrades via ClusterCurator for non-recommended upgrades

## Environment & Validation Status

**Environment Used:**
- **Cluster:** qe6-vmware-ibm 
- **API Server:** https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443
- **Console:** https://console-openshift-console.apps.qe6-vmware-ibm.install.dev09.red-chesterfield.com
- **OpenShift Version:** 4.19.6
- **ACM Namespace:** ocm
- **MCE Namespace:** multicluster-engine

**Validation Status:** ✅ SUCCESSFUL
- Environment access confirmed
- ClusterCurator CRD present: `clustercurators.cluster.open-cluster-management.io`
- ClusterVersion resource accessible for testing
- Test environment ready for digest-based upgrade testing

**Potential Failure Causes:**
- Feature requires specific ACM/MCE version with the new digest selection logic
- Non-recommended version must be available in OpenShift Cincinnati backend
- Managed clusters required for testing upgrade functionality
- Feature may be behind feature flags in certain environments

## Feature Summary

**Feature:** Support digest-based upgrades via ClusterCurator for non-recommended upgrades

**Business Value:** Addresses urgent Amadeus customer requirement to use image digests for non-recommended upgrades in disconnected environments where image tags don't work.

**Implementation Status:** ✅ DEPLOYED via PR #468
- New `GetImageDigestFromClusterVersion` function implements three-tier fallback logic
- Checks conditionalUpdates first, then availableUpdates, finally falls back to image tags
- Feature enabled by annotation: `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: 'true'`

**Key Investigation Results:**
- **JIRA Analysis:** Main story ACM-22079 with QE task ACM-22080 and automation task ACM-22081
- **GitHub PR Analysis:** PR #468 in cluster-curator-controller repository implements the core digest selection logic
- **Technical Implementation:** Three-tier fallback approach prioritizes digest over tag usage
- **Documentation:** ACM-22457 provides customer documentation for the new annotation usage

## Test Case Generation Approach

Based on the investigation, the test plan focuses on:
1. Testing the new digest selection logic with non-recommended annotations
2. Validating the three-tier fallback mechanism (conditionalUpdates → availableUpdates → tag fallback)
3. Verifying ClusterVersion resource receives correct digest format
4. Testing annotation-driven feature enablement

The test cases target the core change: ClusterCurator now uses image digests from the ClusterVersion conditionalUpdates list when the non-recommended annotation is present, providing better support for disconnected environments.