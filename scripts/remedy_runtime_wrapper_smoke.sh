#!/usr/bin/env bash
# Runtime wrapper smoke — verifies pytest integration of runtime wrappers.
# Separate from backend basis smoke to avoid pytest-process contamination.
#
# Each wrapper runs in its own pytest process via remedy_pytest.sh.
# If a wrapper hangs, timeout will kill it cleanly (--kill-after).
#
# Usage:
#   scripts/remedy_runtime_wrapper_smoke.sh
#   REMEDY_PYTEST_TIMEOUT_SEC=30 scripts/remedy_runtime_wrapper_smoke.sh
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-60}"

echo "=== Runtime Wrapper Smoke (timeout=${REMEDY_PYTEST_TIMEOUT_SEC}s) ==="

echo "--- Propose wrapper ---"
scripts/remedy_pytest.sh tests/cli/test_propose_cli_runtime.py -q --cache-clear

echo "--- Worker wrapper ---"
scripts/remedy_pytest.sh tests/cli/test_worker_cli_runtime.py -q --cache-clear

echo "=== Runtime Wrapper Smoke PASSED ==="
