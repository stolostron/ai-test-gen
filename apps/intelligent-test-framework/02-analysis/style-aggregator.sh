#!/usr/bin/env bash
set -e

OUTPUT_DIR="02-analysis"
STYLE_PROFILE="$OUTPUT_DIR/style-profile.yaml"
STYLE_GUIDE="$OUTPUT_DIR/style-guide.md"

# Scan previous examples and compute style metrics
steps_total=0; files_count=0; yaml_total=0; cli_total=0; cats_total=0

> "$STYLE_PROFILE"
> "$STYLE_GUIDE"

find examples -type f -path "*/02-test-planning/test-plan.md" 2>/dev/null | sort | while read -r f; do
  files_count=$((files_count + 1))
  steps=$(grep -c '^|' "$f" 2>/dev/null || echo 0)
  yaml=$(grep -c '```yaml' "$f" 2>/dev/null || echo 0)
  cli=$(grep -c '\`oc ' "$f" 2>/dev/null || echo 0)
  cats=$(grep -c '\*\*.*\*\*' "$f" 2>/dev/null || echo 0)
  steps_total=$((steps_total + steps))
  yaml_total=$((yaml_total + yaml))
  cli_total=$((cli_total + cli))
  cats_total=$((cats_total + cats))
done

if [ "$files_count" -gt 0 ]; then
  avg_steps=$((steps_total / files_count))
  avg_yaml=$((yaml_total / files_count))
  avg_cli=$((cli_total / files_count))
  avg_cats=$((cats_total / files_count))
else
  avg_steps=0; avg_yaml=0; avg_cli=0; avg_cats=0
fi

rec_steps=$(( avg_steps>55 ? avg_steps : 55 ))
rec_yaml=$(( avg_yaml>6 ? avg_yaml : 6 ))
rec_cli=$(( avg_cli>6 ? avg_cli : 6 ))
rec_cats=$(( avg_cats>12 ? avg_cats : 12 ))

cat > "$STYLE_PROFILE" <<YAML
filesAnalyzed: $files_count
averages:
  steps: $avg_steps
  yamlBlocks: $avg_yaml
  cliBlocks: $avg_cli
  categories: $avg_cats
recommendedTargets:
  steps: $rec_steps
  yamlBlocks: $rec_yaml
  cliBlocks: $rec_cli
  categories: $rec_cats
YAML

cat > "$STYLE_GUIDE" <<'MD'
# Cross-Team Test Plan Style Guide (Synthesized)

- Use table format with two columns: Step | Expected Result
- Group steps with bold section headers (e.g., **Setup and Prerequisites**)
- Include complete YAML examples for resources in-line under relevant steps
- Include concrete CLI validation commands (prefer `oc`) with expected outputs
- Cover multiple cluster types where relevant (AWS multi-node, SNO, Hosted)
- Include error handling (invalid inputs, network issues, rollback) with expected messages
- Include performance and security validation where applicable
- Always include cleanup and final state verification
- Prefer concise, executable steps with clear, testable outcomes
- Keep tone consistent, professional, and implementation-ready
MD

echo "[STYLE] Created $STYLE_PROFILE and $STYLE_GUIDE (analyzed $files_count plans)"
