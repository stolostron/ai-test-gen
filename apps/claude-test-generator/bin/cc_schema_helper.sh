#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<EOF
Usage:
  $(basename "$0") generate --name <name> --namespace <ns> --version <ocpVersion>

Description:
  Generates a minimal, schema-aware ClusterCurator YAML that includes fields commonly
  required by the ClusterCurator CRD in qe environments (e.g., towerAuthSecret, prehook, posthook,
  and install section). This avoids server-side validation failures when applying resources.

Examples:
  $(basename "$0") generate --name digest-upgrade-test --namespace cluster-namespace --version 4.16.37
EOF
}

cmd=${1:-}
shift || true

if [[ "$cmd" != "generate" ]]; then
  usage
  exit 1
fi

NAME=""
NAMESPACE=""
VERSION=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      NAME="$2"; shift 2;;
    --namespace)
      NAMESPACE="$2"; shift 2;;
    --version)
      VERSION="$2"; shift 2;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown arg: $1" >&2; usage; exit 1;;
  esac
done

if [[ -z "$NAME" || -z "$NAMESPACE" || -z "$VERSION" ]]; then
  echo "Missing required args." >&2
  usage
  exit 1
fi

cat <<YAML
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: ${NAME}
  namespace: ${NAMESPACE}
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"
spec:
  desiredCuration: upgrade
  upgrade:
    desiredUpdate: "${VERSION}"
    monitorTimeout: 120
    towerAuthSecret: ""
    prehook: []
    posthook: []
  install:
    towerAuthSecret: ""
    prehook: []
    posthook: []
YAML


