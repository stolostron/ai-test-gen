The comprehensive test plan for ACM-22079 (digest-based upgrades via ClusterCurator) has been generated with four focused test cases covering:

1. **Digest-Based Upgrade Success Scenarios** - Core functionality with force annotation
2. **Tag-Based Fallback and Error Handling** - Fallback mechanisms and error conditions  
3. **Disconnected Environment and Multi-Cluster** - Air-gapped setups and concurrent operations
4. **RBAC and Security Validation** - Permission controls and audit compliance

Each test case includes dual CLI/UI validation steps where applicable, complete command examples with expected outputs, and practical YAML configurations using the `ocm` namespace as specified. The test plan incorporates the adaptive feedback insights and uses the validated ClusterCurator schema provided.
