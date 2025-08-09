## Key Implementation References

- **Core Logic**: `pkg/jobs/hive/hive.go:75-114` - Digest discovery algorithm
- **Test Coverage**: `pkg/jobs/hive/hive_test.go:163-175` - Comprehensive test cases
- **Architecture**: ClusterCurator controller monitors for new resources and creates curator jobs
- **Integration**: Uses ManagedClusterView/Action for hub-spoke communication

This analysis demonstrates comprehensive understanding of both the specific ACM-22079 feature and its critical role in enabling enterprise customers like Amadeus to perform reliable cluster upgrades in air-gapped environments. The implementation represents a significant capability enhancement for ACM's cluster lifecycle management in disconnected deployments.
