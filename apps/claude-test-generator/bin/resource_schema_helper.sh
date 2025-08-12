#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<EOF
Generate a minimal, schema-aware YAML skeleton for any Kubernetes resource (CRD-backed or built-in).

Usage:
  $(basename "$0") --group <apiGroup> --version <version> --kind <Kind> --name <name> [--namespace <ns>]

Notes:
  - Requires: oc, jq
  - For CRDs, attempts to read the OpenAPI v3 schema to list required fields under .spec
  - Emits a safe skeleton with metadata and spec placeholder; includes comments for required keys

Examples:
  $(basename "$0") --group cluster.open-cluster-management.io --version v1beta1 --kind ClusterCurator \
    --name digest-upgrade-test --namespace cluster-namespace
EOF
}

GROUP=""
VERSION=""
KIND=""
NAME=""
NAMESPACE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --group) GROUP="$2"; shift 2;;
    --version) VERSION="$2"; shift 2;;
    --kind) KIND="$2"; shift 2;;
    --name) NAME="$2"; shift 2;;
    --namespace) NAMESPACE="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1;;
  esac
done

if [[ -z "$GROUP" || -z "$VERSION" || -z "$KIND" || -z "$NAME" ]]; then
  echo "Missing required args." >&2
  usage
  exit 1
fi

NS_BLOCK=""
if [[ -n "$NAMESPACE" ]]; then
  NS_BLOCK="  namespace: ${NAMESPACE}\n"
fi

# Try to find the CRD for this Group/Kind
REQUIRED_KEYS=$(oc get crd -o json 2>/dev/null \
  | jq -r --arg g "$GROUP" --arg v "$VERSION" --arg k "$KIND" '
    .items[]
    | select(.spec.group == $g and .spec.names.kind == $k)
    | .spec.versions[]
    | select(.name == $v)
    | .schema.openAPIV3Schema.properties.spec.required // empty
    | .[]' || true)

cat <<YAML
apiVersion: ${GROUP}/${VERSION}
kind: ${KIND}
metadata:
  name: ${NAME}
${NS_BLOCK}spec:
  # TODO: populate required fields for your use case
YAML

if [[ -n "$REQUIRED_KEYS" ]]; then
  echo "  # Required keys from CRD schema:" 
  while IFS= read -r key; do
    [[ -z "$key" ]] && continue
    echo "  ${key}:" | sed 's/^/  # /'
  done <<< "$REQUIRED_KEYS"
fi


