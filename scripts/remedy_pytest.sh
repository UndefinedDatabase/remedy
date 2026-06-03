#!/usr/bin/env bash
# remedy_pytest.sh — Lock-protected, timeout-bound pytest wrapper.
#
# Prevents parallel pytest runs on the same machine.
# Uses flock -n to fail fast if another run is active.
# Uses timeout to prevent runaway test processes.
#
# Usage:
#   scripts/remedy_pytest.sh tests/ -q --cache-clear
#   scripts/remedy_pytest.sh tests/cli -q
#   scripts/remedy_pytest.sh tests/orchestration/test_event_replay.py -v
#
# Environment:
#   REMEDY_PYTEST_TIMEOUT_SEC  — max seconds (default: 600)
#   REMEDY_PYTEST_LOCK         — lock file path (default: /tmp/remedy-pytest.lock)

set -euo pipefail

TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-600}"
LOCK_FILE="${REMEDY_PYTEST_LOCK:-/tmp/remedy-pytest.lock}"

exec 200>"${LOCK_FILE}"

if ! flock -n 200; then
    echo "ERROR: Another pytest run is already active. Refusing to start a parallel run." >&2
    echo "Lock file: ${LOCK_FILE}" >&2
    echo "To find the active process: pgrep -af 'pytest|python.*pytest'" >&2
    exit 1
fi

echo "remedy_pytest: timeout=${TIMEOUT_SEC}s, lock=${LOCK_FILE}"
PYTHON="${REMEDY_PYTHON:-python3}"

echo "remedy_pytest: ${PYTHON} -m pytest $*"

if ! timeout "${TIMEOUT_SEC}" "${PYTHON}" -m pytest "$@"; then
    EXIT_CODE=$?
    if [ "${EXIT_CODE}" -eq 124 ]; then
        echo "" >&2
        echo "ERROR: pytest timed out after ${TIMEOUT_SEC} seconds." >&2
        echo "To increase: REMEDY_PYTEST_TIMEOUT_SEC=900 scripts/remedy_pytest.sh ..." >&2
        exit 124
    fi
    exit "${EXIT_CODE}"
fi
