#!/bin/bash

# feature-detection.sh — Heuristic feature detector for JIRA Stories
# Outputs key=value pairs suitable for `source` or eval

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JIRA_TICKET="${1:-}"
JIRA_CONTENT_FILE="${2:-${SCRIPT_DIR}/jira-details.md}"

detect_team() {
  # Default to CLC for now; later derive from repo ownership or labels
  echo "CLC"
}

detect_feature_key() {
  local content
  if [ -f "$JIRA_CONTENT_FILE" ]; then
    content=$(tr '[:upper:]' '[:lower:]' < "$JIRA_CONTENT_FILE")
  else
    content=$(echo "$JIRA_TICKET" | tr '[:upper:]' '[:lower:]')
  fi

  if echo "$content" | grep -Eq 'curator|clustercurator|digest|upgrade'; then
    echo "cluster_lifecycle_upgrade_digest"
    return
  fi

  if echo "$content" | grep -Eq 'policy|governance|grc'; then
    echo "governance_policy"
    return
  fi

  if echo "$content" | grep -Eq 'application|appset|argo'; then
    echo "application_lifecycle"
    return
  fi

  echo "generic_story"
}

TEAM=$(detect_team)
FEATURE_KEY=$(detect_feature_key)

echo "DETECTED_TEAM=$TEAM"
echo "DETECTED_FEATURE_KEY=$FEATURE_KEY"
