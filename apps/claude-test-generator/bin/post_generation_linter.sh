#!/usr/bin/env bash
set -euo pipefail

# Post-generation linter for Test-Cases.md / Complete-Analysis.md
# - Flags escaped pipes in bash code blocks
# - Detects managed-cluster reads that should use ManagedClusterView
# - Optionally validates YAML blocks with `oc apply --dry-run=server -f -`
# - Optionally auto-injects required spec keys (comments) using resource_schema_helper

usage() {
  cat <<USAGE
Usage: $(basename "$0") --path <dir-or-file> [--validate-yaml] [--auto-inject-required-keys]

Examples:
  $(basename "$0") --path runs/ACM-22079/latest --validate-yaml
  $(basename "$0") --path runs/ACM-22079/latest/Test-Cases.md --auto-inject-required-keys
USAGE
}

TARGET=""
VALIDATE_YAML=0
AUTO_INJECT=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --path) TARGET="$2"; shift 2;;
    --validate-yaml) VALIDATE_YAML=1; shift 1;;
    --auto-inject-required-keys) AUTO_INJECT=1; shift 1;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1;;
  esac
done

if [[ -z "$TARGET" ]]; then
  echo "--path is required" >&2
  usage
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCHEMA_HELPER="$ROOT_DIR/bin/resource_schema_helper.sh"

red(){ printf "\e[31m%s\e[0m\n" "$*"; }
yellow(){ printf "\e[33m%s\e[0m\n" "$*"; }
green(){ printf "\e[32m%s\e[0m\n" "$*"; }

FILES=()
if [[ -d "$TARGET" ]]; then
  while IFS= read -r -d '' f; do FILES+=("$f"); done < <(find "$TARGET" -maxdepth 1 -type f -name '*.md' -print0)
else
  FILES+=("$TARGET")
fi

ESCAPED_PIPE_ISSUES=0
MCV_MISSING_ISSUES=0
YAML_ERRORS=0

# Helper: extract code blocks of a given language from a file
extract_blocks(){
  local file="$1" lang="$2"
  awk -v lang="$lang" '
    $0==("```" lang){inb=1; next}
    inb && /^```/{inb=0; print SEP; next}
    inb{print $0}
  ' SEP=$'\036' "$file" | sed '/^$/d'
}

# Determine if oc is usable for validate-yaml
OC_AVAILABLE=0
if [[ $VALIDATE_YAML -eq 1 ]]; then
  if command -v oc >/dev/null 2>&1 && oc whoami >/dev/null 2>&1; then
    OC_AVAILABLE=1
  else
    yellow "Skipping --validate-yaml: oc not available or not logged in"
    VALIDATE_YAML=0
  fi
fi

for file in "${FILES[@]}"; do
  echo "Linting: $file"

  # 1) Escaped pipes in bash blocks
  IFS=$'\036' read -r -d '' -a bash_blocks < <(extract_blocks "$file" bash && printf '\0') || true
  for block in "${bash_blocks[@]:-}"; do
    if grep -q '\\\\|' <<< "$block"; then
      red "  [PIPE] Escaped pipe detected in bash code block"
      ESCAPED_PIPE_ISSUES=$((ESCAPED_PIPE_ISSUES+1))
    fi
  done

  # 2) Managed-cluster reads should use ManagedClusterView
  # Heuristic: if file references clusterversion commands and does not mention managedclusterview, flag
  if grep -Ei 'oc .*get .*clusterversion' "$file" >/dev/null 2>&1; then
    if ! grep -Ei 'managedclusterview|ManagedClusterView' "$file" >/dev/null 2>&1; then
      yellow "  [MCV] clusterversion referenced without ManagedClusterView guidance"
      MCV_MISSING_ISSUES=$((MCV_MISSING_ISSUES+1))
    fi
  fi

  # 3) YAML validate (optional)
  if [[ $VALIDATE_YAML -eq 1 && $OC_AVAILABLE -eq 1 ]]; then
    IFS=$'\036' read -r -d '' -a yaml_blocks < <(extract_blocks "$file" yaml && printf '\0') || true
    idx=0
    for block in "${yaml_blocks[@]:-}"; do
      idx=$((idx+1))
      if ! printf '%s\n' "$block" | oc apply --dry-run=server -f - >/dev/null 2>&1; then
        red "  [YAML] Server validation failed for YAML block #$idx"
        YAML_ERRORS=$((YAML_ERRORS+1))
      fi
    done
  fi

  # 4) Auto-inject required keys as comments (optional)
  if [[ $AUTO_INJECT -eq 1 ]]; then
    "$ROOT_DIR/bin/inject_required_keys.sh" --file "$file" || true
  fi

done

SUMMARY=""
[[ $ESCAPED_PIPE_ISSUES -gt 0 ]] && SUMMARY+=$"Escaped pipe issues: $ESCAPED_PIPE_ISSUES\n"
[[ $MCV_MISSING_ISSUES -gt 0 ]] && SUMMARY+=$"ManagedClusterView guidance missing: $MCV_MISSING_ISSUES\n"
[[ $YAML_ERRORS -gt 0 ]] && SUMMARY+=$"YAML validation failures: $YAML_ERRORS\n"

if [[ -n "$SUMMARY" ]]; then
  echo ""
  red "Post-generation linter found issues:\n$SUMMARY"
  exit 2
else
  green "No issues found by post-generation linter."
fi
