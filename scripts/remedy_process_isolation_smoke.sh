#!/usr/bin/env bash
# Process isolation smoke — thin wrapper for Python supervisor.
# Verifies helper/contract tests separately from runtime and backend smoke.
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-60}"

exec python3 "$(dirname "$0")/remedy_process_isolation_smoke.py"
