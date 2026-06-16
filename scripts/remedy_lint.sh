#!/usr/bin/env bash
# remedy_lint.sh — Run Ruff + Mypy baseline checks.
#
# Usage:
#   scripts/remedy_lint.sh          # run both
#   scripts/remedy_lint.sh ruff     # ruff only
#   scripts/remedy_lint.sh mypy     # mypy only

set -euo pipefail

PYTHON="${REMEDY_PYTHON:-python3}"
RUN_RUFF=true
RUN_MYPY=true

if [ "${1:-}" = "ruff" ]; then
    RUN_MYPY=false
elif [ "${1:-}" = "mypy" ]; then
    RUN_RUFF=false
fi

EXIT=0

if $RUN_RUFF; then
    echo "=== Ruff check ==="
    if ! "${PYTHON}" -m ruff check .; then
        EXIT=1
    fi
    echo ""
fi

if $RUN_MYPY; then
    echo "=== Mypy check ==="
    if ! "${PYTHON}" -m mypy packages apps; then
        EXIT=1
    fi
    echo ""
fi

if [ "${EXIT}" -eq 0 ]; then
    echo "All lint checks passed."
else
    echo "Lint checks failed." >&2
fi

exit "${EXIT}"
