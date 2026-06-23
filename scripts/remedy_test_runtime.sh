#!/usr/bin/env bash
# Runtime test lane — CLI integration tests that use subprocess.run.
#
# Subprocess-heavy suites (test_review_bundle_runtime.py) run per-node
# to isolate hangs at the individual test level. Other suites run as
# whole-file invocations.
#
# Per-node diagnostics: START/END markers with wall-clock timing.
# Stale process check at end to catch orphaned children.
#
# Expected runtime: under about 60 seconds on a normal dev machine.
#
# Does NOT run heavy smoke scripts, provider execution, or overnight tests.
# For pure in-process tests: scripts/remedy_test_fast.sh
# For full coverage: scripts/remedy_test_full.sh
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-120}"
export REMEDY_PYTEST_LOCK_WAIT="${REMEDY_PYTEST_LOCK_WAIT:-10}"

echo "=== Runtime Test Lane (CLI Integration — bounded subprocess) ==="

# Subprocess-heavy suites: run each test node individually.
NODE_ISOLATED_FILES=(
    tests/cli/test_review_bundle_runtime.py
)

# Light suites: run as whole file.
WHOLE_FILE_SUITES=(
    tests/cli/test_command_catalog.py
    tests/cli/test_contract_runtime.py
    tests/cli/test_config_cmd.py
)

total_passed=0
total_failed=0
failed_nodes=()

# Outer timeout per node/suite (seconds). Prevents indefinite hangs.
NODE_TIMEOUT="${REMEDY_NODE_TIMEOUT_SEC:-90}"

# Clear stale lock before starting
_clear_stale_lock() {
    local lockfile="/tmp/remedy-pytest.lock"
    if [ -f "$lockfile" ]; then
        local holder
        holder=$(cat "$lockfile" 2>/dev/null || true)
        if [ -n "$holder" ]; then
            kill -0 "$holder" 2>/dev/null || rm -f "$lockfile"
        fi
    fi
}

# --- Per-node isolation for subprocess-heavy suites ---
for f in "${NODE_ISOLATED_FILES[@]}"; do
    echo "--- node-isolated suite: $f ---"
    _clear_stale_lock
    nodes=$(timeout 30 scripts/remedy_pytest.sh "$f" --collect-only -q 2>/dev/null | grep "::" || true)
    if [ -z "$nodes" ]; then
        echo "  (no test nodes collected, skipping)"
        continue
    fi
    suite_pass=0
    suite_fail=0
    while IFS= read -r node; do
        _clear_stale_lock
        node_start=$SECONDS
        echo "  START node: $node"
        if timeout "$NODE_TIMEOUT" scripts/remedy_pytest.sh "$node" -q; then
            node_elapsed=$((SECONDS - node_start))
            echo "  END node: $node status=PASS (${node_elapsed}s)"
            suite_pass=$((suite_pass + 1))
        else
            node_elapsed=$((SECONDS - node_start))
            echo "  END node: $node status=FAIL (${node_elapsed}s)"
            suite_fail=$((suite_fail + 1))
            failed_nodes+=("$node")
        fi
    done <<< "$nodes"
    echo "  suite result: $suite_pass passed, $suite_fail failed"
    if [ "$suite_fail" -eq 0 ]; then
        total_passed=$((total_passed + 1))
    else
        total_failed=$((total_failed + 1))
    fi
done

# --- Whole-file suites ---
for f in "${WHOLE_FILE_SUITES[@]}"; do
    echo "--- runtime suite: $f ---"
    _clear_stale_lock
    if timeout "$NODE_TIMEOUT" scripts/remedy_pytest.sh "$f" -q; then
        total_passed=$((total_passed + 1))
    else
        total_failed=$((total_failed + 1))
        echo "FAIL: $f"
    fi
done

echo "=== Runtime Lane: $total_passed/$((total_passed + total_failed)) suites passed ==="

if [ ${#failed_nodes[@]} -gt 0 ]; then
    echo "Failed nodes:"
    for n in "${failed_nodes[@]}"; do
        echo "  - $n"
    done
fi

# --- Stale process diagnostic ---
stale=$(ps -ef | grep -E 'pytest|apps\.cli\.grouped|remedy_pytest_runner' | grep -v grep | grep -v "$$" || true)
if [ -n "$stale" ]; then
    echo "WARNING: stale test processes detected after runtime lane:"
    echo "$stale"
fi

if [ "$total_failed" -gt 0 ]; then
    exit 1
fi
