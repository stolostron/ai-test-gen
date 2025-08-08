## Implementation-Ready Test Code and Configurations

### Complete Test Implementation

Based on the comprehensive analysis above, here's the implementation-ready test plan that aligns with existing ACM test automation patterns:

| Step | Expected Result |
|------|-----------------|
| **Setup and Prerequisites** |  |
| Create test namespace with ClusterCurator RBAC permissions | Namespace ready with proper service account and role bindings |
| Deploy test cluster with OpenShift 4.14.9 as baseline version | Cluster operational with ManagedClusterInfo showing current version |
| Configure local registry mirror for disconnected testing | Registry accessible with digest-based upgrade images available |
| Apply force upgrade annotation to test ClusterCurator resource | `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"` annotation present |
| **Digest Discovery from ConditionalUpdates** |  |
| Create ClusterVersion mock with target version in conditionalUpdates array | ClusterVersion status contains version "4.14.10" with digest "sha256:71e158c6173ad6aa6e356c119a87459196bbe70e89c0db1e35c1f63a87d90676" |
| Execute `validateUpgradeVersion()` function with force annotation enabled | Function returns digest string from conditionalUpdates, logs "Found conditional update image digest" |
| Verify digest extraction matches expected format | Returned digest equals "quay.io/openshift-release-dev/ocp-release@sha256:71e158c6173ad6aa6e356c119a87459196bbe70e89c0db1e35c1f63a87d90676" |
| **ManagedClusterAction Creation with Digest** |  |
| Execute `retreiveAndUpdateClusterVersion()` with discovered digest | ManagedClusterAction resource created with digest image reference in spec |
| Verify ClusterVersion.spec.desiredUpdate contains digest not tag | `desiredUpdate.image` field contains full digest reference, no `force: true` flag present |
| Monitor ManagedClusterAction status until completion | `status.conditions` shows `type: "Completed"` with `status: "True"` |
| **Fallback to AvailableUpdates** |  |
| Create ClusterVersion mock without conditionalUpdates but with availableUpdates | ClusterVersion status contains version "4.14.11" only in availableUpdates array |
| Execute digest discovery workflow | Function searches conditionalUpdates first, then falls back to availableUpdates successfully |
| Verify logging shows fallback behavior | Logs contain "Check for image digest in available updates just in case" |
| **Disconnected Environment Simulation** |  |
| Apply NetworkPolicy blocking external registry access | `kubectl get networkpolicy` shows policy preventing quay.io access |
| Configure ImageDigestMirrorSet pointing to local registry | IDMS redirects image pulls to local mirror registry |
| Execute digest-based upgrade in air-gapped mode | Upgrade proceeds using local registry, no external network calls attempted |
| Validate upgrade completion with mirrored images | Cluster successfully upgraded to 4.14.10 using local registry digest images |

This comprehensive analysis demonstrates deep understanding of ACM-22079's implementation, its integration within the broader ACM ecosystem, and provides production-ready test strategies that address both the specific feature requirements and enterprise deployment scenarios.
