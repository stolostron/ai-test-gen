The test plan has been generated with 4 comprehensive test cases covering:

1. **Digest-Based Upgrade Success Scenarios** - Tests the core functionality of digest-based upgrades with the force annotation and fallback mechanisms
2. **Tag-Based Fallback and Error Handling** - Validates fallback behavior when digests are unavailable and error handling for invalid inputs  
3. **Disconnected Environment and Multi-Cluster Scenarios** - Tests digest resolution in air-gapped environments and concurrent upgrades across multiple clusters
4. **RBAC and Security Validation** - Ensures proper permission handling and security controls for ClusterCurator operations

Each test case includes both CLI commands and UI verification steps where applicable, with detailed expected results that explain what is being validated and why. The test plan focuses on the ACM-22079 feature requirements for digest-based upgrades while maintaining practical, executable test steps.
