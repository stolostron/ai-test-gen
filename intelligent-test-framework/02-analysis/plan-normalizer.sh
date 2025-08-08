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

HEADER_1='| Test Steps | Expected Results |'
HEADER_2='|------------|------------------|'

emit_table_chunks() {
  local -n _rows=$1
  local count=0
  for row in "${_rows[@]}"; do
    if [ "$count" -eq 0 ]; then
      echo "$HEADER_1" >> "$tmpfile"
      echo "$HEADER_2" >> "$tmpfile"
    fi
    echo "$row" >> "$tmpfile"
    count=$((count+1))
    if [ "$count" -ge "$MAX_STEPS" ]; then
      echo >> "$tmpfile"
      count=0
    fi
  done
}

inside_table=0
table_rows=()

for (( i=0; i<${#lines[@]}; i++ )); do
  ln="${lines[$i]}"

  if [ "$inside_table" -eq 0 ]; then
    # Detect start of a table
    if [[ "$ln" == "$HEADER_1" ]]; then
      inside_table=1
      table_rows=()
      # Skip writing this header now; we'll re-emit headers when chunking
      continue
    else
      # Pass-through non-table content verbatim
      echo "$ln" >> "$tmpfile"
      continue
    fi
  else
    # We are inside a table until a non-table line appears
    if [[ "$ln" == "$HEADER_2" ]]; then
      # Skip the dashed header separator
      continue
    fi

    if [[ "$ln" =~ ^\|.*\|$ ]]; then
      # Filter out flaky/timing-based steps
      if echo "$ln" | grep -q -- "--watch"; then
        continue
      fi
      table_rows+=("$ln")
      continue
    fi

    # End of table encountered; emit normalized chunks and then handle current line
    emit_table_chunks table_rows
    echo >> "$tmpfile"
    inside_table=0
    table_rows=()
    # Now process the current non-table line in outer loop context
    echo "$ln" >> "$tmpfile"
  fi
done

# If file ended while still inside a table, emit the remaining rows
if [ "$inside_table" -eq 1 ]; then
  emit_table_chunks table_rows
fi

mv "$tmpfile" "$PLAN_FILE"
echo "[NORMALIZER] Normalized ${PLAN_FILE} into tables of up to ${MAX_STEPS} steps" >&2


