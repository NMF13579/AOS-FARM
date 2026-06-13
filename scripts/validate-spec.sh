#!/usr/bin/env bash
set -euo pipefail
SPEC_DIR="$1"

# Check files exist
[ -f "$SPEC_DIR/spec.md" ] || { echo "MISSING $SPEC_DIR/spec.md" >&2; exit 2; }
[ -f "$SPEC_DIR/tasks.md" ] || { echo "MISSING $SPEC_DIR/tasks.md" >&2; exit 2; }
[ -f "$SPEC_DIR/acceptance.md" ] || { echo "MISSING $SPEC_DIR/acceptance.md" >&2; exit 2; }

# Validate frontmatter keys in spec.md
REQ_KEYS=(id author owner status requires_human_approval)
for k in "${REQ_KEYS[@]}"; do
  if ! grep -q "^$k:\"\?" "$SPEC_DIR/spec.md"; then
    # also allow YAML key without quotes
    if ! grep -q "^$k:" "$SPEC_DIR/spec.md"; then
      echo "MISSING frontmatter key: $k" >&2
      exit 3
    fi
  fi
done

# Validate tasks has preconditions/postconditions
if ! grep -q "preconditions" "$SPEC_DIR/tasks.md"; then
  echo "tasks.md missing preconditions" >&2; exit 4
fi
if ! grep -q "postconditions" "$SPEC_DIR/tasks.md"; then
  echo "tasks.md missing postconditions" >&2; exit 5
fi

echo "SPEC VALIDATION PASSED"
exit 0
