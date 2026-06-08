#!/usr/bin/env bash
# Backend basis smoke — thin wrapper for Python supervisor.
#
# The Python supervisor (remedy_backend_basis_smoke.py) runs each phase
# in full process isolation (Popen + start_new_session + temp files + killpg).
# This shell script only sets the timeout and delegates.
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-120}"

exec python3 "$(dirname "$0")/remedy_backend_basis_smoke.py"
