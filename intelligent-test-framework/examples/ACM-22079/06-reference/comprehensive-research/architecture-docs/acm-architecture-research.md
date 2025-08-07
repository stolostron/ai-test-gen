# ACM Architecture Research for ClusterCurator

## Key Architecture Documents to Research

### ClusterCurator Architecture
- Component interaction diagrams
- Upgrade workflow sequences
- Hub-spoke communication patterns
- ManagedClusterView/Action lifecycle

### ACM Core Architecture
- Multi-cluster management overview
- Cluster lifecycle management flows
- Application lifecycle integration
- Governance and policy enforcement

### OpenShift Integration
- ClusterVersion operator integration
- Cluster upgrade mechanisms
- Image registry and mirroring
- Disconnected environment patterns

## Design Patterns to Analyze

### Upgrade Patterns
1. **Traditional Tag-Based**: `quay.io/openshift-release-dev/ocp-release:4.5.10-multi`
2. **Digest-Based**: `quay.io/openshift-release-dev/ocp-release@sha256:...`
3. **Mirror Registry**: Custom registry with digest preservation
4. **Air-Gapped**: Completely disconnected with local registries

### Error Handling Patterns
- Upgrade failure recovery
- Network connectivity issues
- Image pull failures
- Version validation errors

### Testing Patterns
- Hub cluster test setup
- Managed cluster simulation
- Disconnected environment mocking
- Upgrade scenario orchestration

## Related Enhancement Proposals
Research stolostron/enhancements for:
- ClusterCurator enhancements
- Disconnected environment improvements
- Multi-cluster upgrade strategies
- Image digest support proposals
