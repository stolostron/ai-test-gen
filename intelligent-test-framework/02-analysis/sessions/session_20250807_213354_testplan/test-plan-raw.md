This test plan covers all critical aspects of the ACM-22079 digest-based upgrade feature:

1. **Test Case 1** validates successful digest discovery and usage from both conditionalUpdates and availableUpdates
2. **Test Case 2** ensures proper fallback to tag-based upgrades and error handling
3. **Test Case 3** verifies functionality in disconnected environments and concurrent multi-cluster scenarios
4. **Test Case 4** validates RBAC security and permission handling

Each test case provides complete `oc` commands with expected outputs, making them executable by engineers new to ACM/OpenShift while ensuring comprehensive coverage of the digest-based upgrade functionality.
