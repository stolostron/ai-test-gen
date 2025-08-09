#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$ROOT_DIR/02-analysis/utils/logging.sh"

print_status "🔎 Capability detection: probing cluster APIs and CRDs"

if ! command -v oc >/dev/null 2>&1; then
  print_error "oc CLI not found on PATH"
  exit 1
fi

OUTPUT_DIR="$ROOT_DIR/06-reference"
mkdir -p "$OUTPUT_DIR"
CAPS_FILE="$OUTPUT_DIR/capabilities.json"

# Basic cluster info
oc_version_json=$(oc version -o json 2>/dev/null || echo '{}')

# API resources and CRDs
api_resources=$(oc api-resources --verbs=list --namespaced -o name 2>/dev/null || true)
crds=$(oc get crd -o name 2>/dev/null || true)

# Key ACM CRDs
has_clustercurator=false; has_mcv=false; has_mca=false
echo "$crds" | grep -q '^clustercurators\.cluster\.open-cluster-management\.io' && has_clustercurator=true || true
echo "$crds" | grep -q '^managedclusterviews\.view\.open-cluster-management\.io' && has_mcv=true || true
echo "$crds" | grep -q '^managedclusteractions\.action\.open-cluster-management\.io' && has_mca=true || true

# ClusterVersion digest capability (managed cluster check will vary; hub check shown)
cv_image=""
if oc get clusterversion version >/dev/null 2>&1; then
  cv_image=$(oc get clusterversion version -o jsonpath='{.status.desired.image}' 2>/dev/null || echo "")
fi

# Namespaces
namespaces=$(oc get ns -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' 2>/dev/null || true)
has_ns_ocm=false
echo "$namespaces" | grep -qx 'ocm' && has_ns_ocm=true || true

# Compose JSON (prefer jq if available)
if command -v jq >/dev/null 2>&1; then
  jq -n \
    --argjson ocVersion "${oc_version_json}" \
    --arg cvImage "$cv_image" \
    --arg apiCount "$(printf "%s" "$api_resources" | grep -c "." || echo 0)" \
    --arg crdCount "$(printf "%s" "$crds" | grep -c "." || echo 0)" \
    --arg hasCurator "$has_clustercurator" \
    --arg hasMCV "$has_mcv" \
    --arg hasMCA "$has_mca" \
    --arg hasOcmNS "$has_ns_ocm" \
    '{
      timestamp: now | todate, 
      oc: $ocVersion,
      apiResourcesCount: ($apiCount|tonumber),
      crdCount: ($crdCount|tonumber),
      capabilities: {
        clustercuratorCRD: ($hasCurator == "true"),
        managedclusterviewCRD: ($hasMCV == "true"),
        managedclusteractionCRD: ($hasMCA == "true"),
        ocmNamespace: ($hasOcmNS == "true"),
        hubClusterVersionImage: ($cvImage // "")
      }
    }' > "$CAPS_FILE"
else
  cat > "$CAPS_FILE" <<EOF
{
  "timestamp": "$(date -Iseconds)",
  "oc": {},
  "apiResourcesCount": 0,
  "crdCount": 0,
  "capabilities": {
    "clustercuratorCRD": $([ "$has_clustercurator" = true ] && echo true || echo false),
    "managedclusterviewCRD": $([ "$has_mcv" = true ] && echo true || echo false),
    "managedclusteractionCRD": $([ "$has_mca" = true ] && echo true || echo false),
    "ocmNamespace": $([ "$has_ns_ocm" = true ] && echo true || echo false),
    "hubClusterVersionImage": "${cv_image}"
  }
}
EOF
fi

print_success "Capabilities written to: $CAPS_FILE"
echo "$CAPS_FILE"
