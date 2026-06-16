#!/usr/bin/env bash
# remedy_coverage.sh — Run pytest with coverage measurement.
#
# Produces terminal report + JSON artifact.
# Does NOT run by default on every test — only when explicitly invoked.
#
# Usage:
#   scripts/remedy_coverage.sh                    # full coverage run
#   scripts/remedy_coverage.sh tests/orchestration  # scoped
#
# Environment:
#   REMEDY_PYTEST_TIMEOUT_SEC  — max seconds (default: 600)
#   REMEDY_PYTHON              — python binary (default: python3)

set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-600}"
PYTHON="${REMEDY_PYTHON:-python3}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUNNER="${SCRIPT_DIR}/remedy_pytest_runner.py"
LOCK_FILE="${REMEDY_PYTEST_LOCK:-/tmp/remedy-pytest.lock}"

COV_DIR="${SCRIPT_DIR}/../.coverage_reports"
mkdir -p "${COV_DIR}"

exec 200>"${LOCK_FILE}"

if ! flock -n 200; then
    echo "ERROR: Another pytest run is already active." >&2
    exit 1
fi

PYTEST_ARGS=(
    "--cov=packages"
    "--cov=apps"
    "--cov-report=term-missing"
    "--cov-report=json:${COV_DIR}/coverage.json"
    "--cov-config=pyproject.toml"
    "-q"
    "-k" "not test_full_chain_order"
)

# Append any extra args (e.g. test path)
if [ $# -gt 0 ]; then
    PYTEST_ARGS+=("$@")
fi

echo "remedy_coverage: timeout=${REMEDY_PYTEST_TIMEOUT_SEC}s"
echo "remedy_coverage: ${PYTHON} -m pytest ${PYTEST_ARGS[*]}"

set +e
"${PYTHON}" "${RUNNER}" -- "${PYTEST_ARGS[@]}"
EXIT_CODE=$?
set -e

if [ "${EXIT_CODE}" -eq 0 ]; then
    echo ""
    echo "Coverage report: ${COV_DIR}/coverage.json"
fi

exit "${EXIT_CODE}"
