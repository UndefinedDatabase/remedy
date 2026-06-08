#!/usr/bin/env bash
# Runtime wrapper smoke — thin wrapper for Python supervisor.
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-60}"

exec python3 "$(dirname "$0")/remedy_runtime_wrapper_smoke.py"
