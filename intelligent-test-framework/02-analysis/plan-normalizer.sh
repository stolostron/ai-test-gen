#!/usr/bin/env bash
set -euo pipefail

# plan-normalizer.sh <plan-file> [max_steps_per_table]

PLAN_FILE="${1:-}"
MAX_STEPS="${2:-10}"

if [ -z "${PLAN_FILE}" ] || [ ! -f "${PLAN_FILE}" ]; then
  echo "[NORMALIZER] Plan not found or not provided: ${PLAN_FILE:-<none>}" >&2
  exit 0
fi

tmpfile="${PLAN_FILE}.normalized.tmp"
rm -f "$tmpfile"

# Read all lines
mapfile -t lines < "$PLAN_FILE"

# Identify header and step lines
HEADER_1='| Test Steps | Expected Results |'
HEADER_2='|------------|------------------|'

echo "$HEADER_1" >> "$tmpfile"
echo "$HEADER_2" >> "$tmpfile"

steps=()
for ln in "${lines[@]}"; do
  # Skip initial header duplicates when normalizing
  if [[ "$ln" == "$HEADER_1" ]] || [[ "$ln" == "$HEADER_2" ]]; then
    continue
  fi
  if [[ "$ln" =~ ^\|.*\|$ ]]; then
    steps+=("$ln")
  fi
done

# Ensure setup section exists at the beginning
has_setup=0
for s in "${steps[@]}"; do
  if echo "$s" | grep -qE '^\| (\*\*)?Setup'; then
    has_setup=1; break
  fi
done
if [ "$has_setup" -eq 0 ]; then
  steps=("| Setup | Prerequisites and environment validation present |" "${steps[@]}")
fi

# Emit steps in chunks with table headers
count=0
emitted=0
for ln in "${steps[@]}"; do
  if [ "$count" -ge "$MAX_STEPS" ]; then
    echo >> "$tmpfile"
    echo "$HEADER_1" >> "$tmpfile"
    echo "$HEADER_2" >> "$tmpfile"
    count=0
  fi
  echo "$ln" >> "$tmpfile"
  count=$((count+1))
  emitted=$((emitted+1))
done

mv "$tmpfile" "$PLAN_FILE"
echo "[NORMALIZER] Normalized ${PLAN_FILE} into tables of up to ${MAX_STEPS} steps (total steps: ${emitted})" >&2

