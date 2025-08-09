## ACM-22079: Digest-based Upgrades via ClusterCurator – Test Plan and Rationale

### Feature overview

Digest-based upgrades ensure the managed OpenShift cluster is upgraded using an immutable digest reference (quay image with sha256) rather than a mutable tag. This improves determinism, auditability, and security. The ClusterCurator controller on the hub coordinates the flow:

- If annotation `cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"` is present, the controller performs digest discovery.
- ManagedClusterView (MCV) queries the managed cluster’s ClusterVersion for upgrade options.
  - Prefer `status.conditionalUpdates[*].release.image` (digest).
  - If not present, fall back to `status.availableUpdates[*].image` (digest).
- If a digest is available, it creates a ManagedClusterAction (MCA) with the digest image (no `force`).
- If no digest is available, it falls back to tag-based upgrade and sets `force: true`.

Key scenarios to test:

- Digest success path (annotation present, digest discovered from conditionalUpdates).
- Fallback from conditionalUpdates to availableUpdates.
- Tag-based fallback when digest is unavailable; verify `force: true` is set.
- Error handling (invalid version, malformed input) with clear status messages.
- RBAC correctness (service account roles, ownership, and privileged resource creation via controller only).
- Multi-cluster concurrency and resource isolation between namespaces.

The sections below include the generated test tables (latest run) and explain how each table covers the necessary scenarios.

---

### Test Case 1: Digest-Based Upgrade Success Scenarios

Description: Validates digest discovery and usage, plus fallback to availableUpdates when conditionalUpdates is missing, using hub namespace `ocp` for ClusterCurator examples.

Explanation of coverage:

- Steps 1–2 authenticate and set up a dedicated project, ensuring preconditions are explicit and reproducible.
- Step 3 applies a valid ClusterCurator YAML (namespace `ocp`) with the force/allow-not-recommended annotation, which triggers digest-based logic in the controller.
- Step 4 verifies the annotation is correctly set (CLI+UI), anchoring the test to the feature gate.
- Step 5 confirms an MCV is created, proving the discovery mechanism is engaged.
- Step 6 explicitly checks for a digest image in ClusterVersion via the MCV. This is the core success criterion (digest present and returned).
- Step 7 verifies MCA references a digest and does not set `force`, proving tag-less digest upgrade.
- Steps 8–10 implement and validate the availableUpdates fallback path by changing the target version and ensuring digest is discovered in availableUpdates. This completes the digest success + fallback story.

Test table:

| Test Steps | Expected Results |
|------------|------------------|
| 1. Log into ACM hub cluster: `oc login https://api.hub-cluster.example.com:6443 -u testuser`<br/>UI: Console → User menu → Copy login command with token | CLI verification: `Login successful. You have access to X projects...`<br/>UI verification: Console session shows authenticated user in top-right |
| 2. Create test namespace: `oc create namespace digest-upgrade-test`<br/>UI: Home → Projects → Create Project → Name: digest-upgrade-test | CLI verification: `namespace/digest-upgrade-test created`<br/>UI verification: Project appears in Projects list |
| 3. Create ClusterCurator with force annotation in managed cluster namespace:<br/>```yaml\napiVersion: cluster.open-cluster-management.io/v1beta1\nkind: ClusterCurator\nmetadata:\n  name: test-digest-upgrade\n  namespace: ocp\n  annotations:\n    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"\nspec:\n  desiredCuration: upgrade\n  upgrade:\n    desiredUpdate: "4.15.10"\n    channel: "stable-4.15"\n```<br/>CLI: `oc apply -f clustercurator.yaml`<br/>UI: Search → Kind:ClusterCurator → Create ClusterCurator → YAML view | CLI verification: `clustercurator.cluster.open-cluster-management.io/test-digest-upgrade created`<br/>UI verification: ClusterCurator appears in search results with Created status |
| 4. Verify force annotation is properly set: `oc get clustercurator test-digest-upgrade -n ocp -o jsonpath='{.metadata.annotations.cluster\.open-cluster-management\.io/upgrade-allow-not-recommended-versions}'`<br/>UI: YAML tab → metadata.annotations | CLI verification: Returns `"true"`<br/>UI verification: Annotation visible with correct value |
| 5. Monitor ManagedClusterView creation for digest discovery: `oc get managedclusterview -n ocp --watch`<br/>UI: Search → Kind:ManagedClusterView | CLI verification: New ManagedClusterView appears `test-digest-upgrade-cv-*`<br/>UI verification: ManagedClusterView is Active |
| 6. Verify digest in ClusterVersion via MCV: `oc get managedclusterview -n ocp -l cluster.open-cluster-management.io/curator=test-digest-upgrade -o jsonpath='{.items[0].status.result.status.conditionalUpdates[0].image}'` | CLI verification: `quay.io/openshift-release-dev/ocp-release@sha256:...` digest is returned |
| 7. Verify MCA uses digest and not force: `oc get managedclusteraction -n ocp -o yaml | grep -A5 "desiredUpdate"` | CLI verification: digest reference present, no `force: true` |
| 8. Delete prior curator: `oc delete clustercurator test-digest-upgrade -n ocp` | Resource deleted successfully |
| 9. Create curator targeting version only in availableUpdates | Curator created targeting the alternate version |
| 10. Verify availableUpdates fallback: jsonpath on MCV `...availableUpdates[?(@.version=="4.15.9")].image` | Digest for specified version returned from availableUpdates |

---

### Test Case 2: Tag-Based Fallback and Error Handling

Description: Covers the path where digest discovery fails, requiring a tag-based upgrade with `force: true`. Also validates graceful handling of invalid inputs and clear error messages.

Explanation of coverage:

- Steps 1–2 create a curator for a version not represented by digest; this provokes the fallback flow.
- Step 3 inspects curator status messages to confirm discovery behavior and outcome (digest search failure).
- Step 4 confirms MCA contains a tag image and `force: true`, the expected behavior when digest is unavailable.
- Steps 5–6 remove the annotation and show the standard (non-digest) path explicitly sets `force`.
- Steps 7–8 create an invalid version and confirm a clear failure message is presented in status, demonstrating robust error handling.

Test table (excerpt):

| Test Steps | Expected Results |
|------------|------------------|
| 2. Create ClusterCurator targeting non-digest version (namespace `ocp`) and apply | Curator created; processing begins |
| 3. Monitor curator conditions for digest failure | Status/conditions include clear digest discovery failure message |
| 4. Verify MCA shows tag image AND `force: true` | YAML shows `quay.io/openshift-release-dev/ocp-release:<tag>` and `force: true` |
| 7–8. Invalid version format scenario | Resource enters Failed with an explanatory message |

---

### Test Case 3: RBAC and Multi-Cluster Scenarios

Description: Ensures only authorized identities can create ClusterCurator; the controller creates privileged resources (MCV/MCA). Also validates concurrent upgrades to multiple clusters proceed independently without cross-namespace conflicts.

Explanation of coverage:

- Steps 1–3 establish a service account and appropriate roles/bindings, proving the policy boundaries.
- Step 4 confirms permissions with `oc auth can-i`, ensuring only intended verbs are allowed.
- Steps 5–6 create curators in different namespaces (clusters), launched under the service account, proving least-privilege execution.
- Step 7 monitors both curators to verify independence (no state coupling).
- Step 8 inspects MCVs to verify resources are isolated per namespace and correctly labeled.
- Step 9 cleans up and verifies no resource leaks remain.

Test table (excerpt):

| Test Steps | Expected Results |
|------------|------------------|
| 1–3. Create SA/Role/Binding in hub ns `ocm` | SA, Role, and Binding created and visible in UI |
| 4. `oc auth can-i` checks | Returns `yes` only for permitted verbs |
| 5–6. Create curators concurrently in different namespaces | Both created successfully in isolation |
| 7–8. Monitor curators and verify isolated MCV/MCA | Independent progression; labels/namespaces reflect correct scoping |
| 9. Cleanup | All curators and associated resources removed |

---

### Why this plan is complete

- Validates digest discovery (success) and both fallback branches (availableUpdates and tag+force).
- Exercises realistic failure modes with clear, testable status messages.
- Verifies controller ownership and RBAC boundaries for privileged resources.
- Proves multi-cluster concurrency and namespace isolation.
- Presents dual CLI/UI instructions and explicit expected outputs, improving readability and auditability.

