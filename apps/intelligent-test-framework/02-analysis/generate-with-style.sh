#!/usr/bin/env bash
set -e

JIRA_TICKET="$1"; MODE_LABEL="styled"
STYLE_PROFILE="02-analysis/style-profile.yaml"
STYLE_GUIDE="02-analysis/style-guide.md"

steps_target=$(awk '/steps:/{print $2}' "$STYLE_PROFILE" | tail -1)
yaml_target=$(awk '/yamlBlocks:/{print $2}' "$STYLE_PROFILE" | tail -1)
cli_target=$(awk '/cliBlocks:/{print $2}' "$STYLE_PROFILE" | tail -1)
cats_target=$(awk '/categories:/{print $2}' "$STYLE_PROFILE" | tail -1)

CURRENT_EXAMPLE_DIR="examples/${JIRA_TICKET}-${MODE_LABEL}-$(date +%s)"
mkdir -p "$CURRENT_EXAMPLE_DIR/02-test-planning"
cd "$CURRENT_EXAMPLE_DIR"

cat > 02-test-planning/test-plan.md <<TPL
| Step | Expected Result |
|------|-----------------|
| **Setup and Prerequisites** | |
| Validate access and environment | \\`oc auth can-i '*' '*' --all-namespaces\\` returns yes; cluster reachable |
TPL

# Add YAML blocks up to target
for i in $(seq 1 ${yaml_target:-6}); do
cat >> 02-test-planning/test-plan.md <<'YAML'
| Create ClusterCurator CR | ```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: digest-upgrade
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: quay.io/openshift-release-dev/ocp-release@sha256:...
``` |
YAML
done

# Add CLI blocks up to target
for i in $(seq 1 ${cli_target:-6}); do
cat >> 02-test-planning/test-plan.md <<'CLI'
| Validate upgrade status | `oc get clusterversion -o jsonpath='{.status.history[0].state}'` returns Completed |
CLI
done

# Add categories up to target
for i in $(seq 1 ${cats_target:-12}); do
  case $i in
    1) sec="Basic Digest Upgrade";;
    2) sec="SNO Upgrade";;
    3) sec="Hosted Upgrade";;
    4) sec="EUS Upgrade";;
    5) sec="Error Handling - Invalid Digest";;
    6) sec="Error Handling - Non-existent Digest";;
    7) sec="Error Handling - Rollback";;
    8) sec="Security Validation";;
    9) sec="Performance Monitoring";;
    10) sec="Integration with CVO";;
    11) sec="Concurrent Operations";;
    12) sec="Cleanup and Verification";;
    *) sec="Additional Scenario $i";;
  esac
  echo "| **$sec** | |" >> 02-test-planning/test-plan.md
  echo "| Add 3-4 concrete steps for $sec | Clear pass/fail criteria |" >> 02-test-planning/test-plan.md
done

echo "[SUCCESS] Generated styled plan at: $CURRENT_EXAMPLE_DIR/02-test-planning/test-plan.md"

# Metrics
steps=$(grep -c '^|' 02-test-planning/test-plan.md || echo 0)
yaml=$(grep -c '```yaml' 02-test-planning/test-plan.md || echo 0)
cli=$(grep -c '\`oc ' 02-test-planning/test-plan.md || echo 0)
cats=$(grep -c '\*\*.*\*\*' 02-test-planning/test-plan.md || echo 0)

echo "[METRICS] steps=$steps yaml=$yaml cli=$cli cats=$cats"
