#!/usr/bin/env bash
# Real provider tests — requires running Ollama server.
#
# Usage:
#   REMEDY_RUN_REAL_OLLAMA=1 scripts/remedy_test_real_providers.sh
#
# Without REMEDY_RUN_REAL_OLLAMA=1, prints skip message and exits 0.
set -euo pipefail

if [ "${REMEDY_RUN_REAL_OLLAMA:-}" != "1" ]; then
    echo "Skipping real provider tests. Set REMEDY_RUN_REAL_OLLAMA=1 to run."
    echo "Requires: running Ollama server with a model."
    exit 0
fi

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-300}"
export REMEDY_REAL_OLLAMA_SMOKE=1
export REMEDY_REAL_OLLAMA_EVAL=1

echo "=== Real Provider Tests (Ollama) ==="
exec scripts/remedy_pytest.sh tests/ -q --cache-clear -m real_ollama
