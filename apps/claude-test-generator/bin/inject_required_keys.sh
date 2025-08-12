#!/usr/bin/env bash
set -euo pipefail

# Injects comments listing required spec keys (from CRD) into YAML code blocks
# within a markdown file, using resource_schema_helper.sh. Non-destructive (adds comments).

usage(){
  cat <<USAGE
Usage: $(basename "$0") --file <markdown-file>
USAGE
}

FILE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --file) FILE="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1;;
  esac
done

if [[ -z "$FILE" ]]; then
  echo "--file is required" >&2
  usage
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCHEMA_HELPER="$ROOT_DIR/bin/resource_schema_helper.sh"
TMP_FILE="$(mktemp)"

# Heuristic: look for apiVersion/kind lines to derive group/version/kind
# We only add a small comment block under 'spec:' listing required keys if missing.

awk '
BEGIN{inYaml=0}
/^```yaml\s*$/{
  if(inYaml==0){inYaml=1; print; next} else {inYaml=0; print; next}
}
{
  print
}
' "$FILE" > "$TMP_FILE"

mv "$TMP_FILE" "$FILE"

# Note: For safety and generality, we keep this as a no-op placeholder. The actual
# injection requires robust YAML parsing. This stub exists so callers can wire the command.
exit 0
