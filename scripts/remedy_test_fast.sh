#!/usr/bin/env bash
# Fast test lane — the owner tests of what changed, plus the core product spine.
#
# The selection is change-aware (scripts/select_changed_tests.py): every test file that imports a
# changed module under packages/ or apps/, the CLI dispatch tests when a CLI module changed, the
# documentation checks when docs/ changed, every changed test file, and every test file that
# names a changed path. Selected owner tests may spawn subprocesses: the lane proves the changed
# subsystem, not only the in-process part of it.
#
# The spine below always runs:
#   worker facade:      alias registry, doctor/add/disable, catalog, contract
#   artifact boundary:  dev artifact vs product truth guard tests
#   product spine:      operator command consistency, stale doc scanner, lane self-test
#
# A change to the test machinery (tests/conftest.py, tests/load_governor.py, pyproject.toml,
# constraints.txt, the pytest runner) has no owner selection: the lane says so and exits 3.
# Does NOT replace the full suite: before a merge and at release run scripts/remedy_test_full.sh
# (or the gate the active protocol names).
#
# Usage: scripts/remedy_test_fast.sh            # changes since the merge base with origin/main
#        scripts/remedy_test_fast.sh main       # the base as a revision of your choice
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-600}"
BASE="${1:-origin/main}"

echo "=== Fast Test Lane (owner tests of the change since ${BASE}, plus the spine) ==="

set +e
selected="$(python3 scripts/select_changed_tests.py --base "${BASE}")"
status=$?
set -e
if [ "${status}" -eq 3 ]; then
    echo "The change touches the test machinery; run scripts/remedy_test_full.sh instead." >&2
    exit 3
elif [ "${status}" -ne 0 ]; then
    echo "ERROR: the change-aware selection failed (exit ${status})." >&2
    exit "${status}"
fi

spine=(
    tests/cli/test_worker_facade_cmd.py
    tests/orchestration/test_development_artifact_boundary.py
    tests/cli/test_product_spine.py
)
mapfile -t owners <<< "${selected}"
files=("${spine[@]}")
for f in "${owners[@]}"; do
    if [ -z "${f}" ]; then
        continue
    fi
    case " ${files[*]} " in *" ${f} "*) ;; *) files+=("${f}") ;; esac
done
echo "selected: $(( ${#files[@]} - ${#spine[@]} )) owner test file(s) + ${#spine[@]} spine file(s)"

# Workers pay off only when there is enough to share; tests/conftest.py caps their number.
workers=()
if [ "${#files[@]}" -gt 8 ]; then
    workers=(-n auto)
fi
exec scripts/remedy_pytest.sh "${files[@]}" -q "${workers[@]}"
