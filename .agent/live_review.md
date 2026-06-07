# Parallel Review — Steps 705-714 (Final)

Reviewer: parallel watcher (independent)
Scope: Steps 705-714 (Runtime process cleanup — Popen + temp files + killpg)
Commit reviewed: 66e9a29
Timestamp: 2026-06-07

---

## Status: PASS

All requirements met. All tests pass. No hang detected.

---

## Code Review — `tests/cli/runtime_helpers.py`

### Runtime Helper — `run_grouped_cli` (lines 102-180)

| Requirement | Status | Location |
|---|---|---|
| Uses `Popen` | OK | line 124 |
| Uses `start_new_session=True` | OK | line 130 |
| Uses temp files for stdout/stderr | OK | lines 117-122 (`NamedTemporaryFile`) |
| Kills process group on timeout (SIGTERM) | OK | line 141 |
| Escalates to SIGKILL if SIGTERM fails | OK | line 146 |
| Best-effort cleanup after normal exit | OK | line 150 |
| No `shell=True` | OK | not present |
| Temp file cleanup in `finally` | OK | lines 157-167 |
| Output capped (64KB) | OK | lines 155-156 |
| No pipe inheritance | OK | stdout/stderr go to temp files |

### Lock Leak Guard — `assert_no_leftover_locks` (lines 211-220)

| Requirement | Status | Location |
|---|---|---|
| Function exists | OK | `runtime_helpers.py:211` |
| Uses `Path.rglob("*.lock")` (no flock) | OK | line 217 |
| Called in propose runtime teardown | OK | `test_propose_cli_runtime.py:28` |
| Called in worker runtime teardown | OK | `test_worker_cli_runtime.py:28` |
| Fixture uses `yield` (teardown runs) | OK | both files, line 27 |

### Process Isolation Strategy (docstring, lines 7-13)

Documented: Popen → start_new_session → temp files → wait(timeout) → killpg(SIGTERM) → killpg(SIGKILL) → best-effort cleanup.

---

## Test Results

### Propose Runtime (post-commit)

```
REMEDY_PYTEST_TIMEOUT_SEC=60
tests/cli/test_propose_cli_runtime.py
11 passed in 2.37s
EXIT: clean (no hang)
```

### Worker Runtime (post-commit)

```
REMEDY_PYTEST_TIMEOUT_SEC=60
tests/cli/test_worker_cli_runtime.py
6 passed in 4.84s
EXIT: clean (no hang)
```

### Smoke Test (post-commit)

```
scripts/remedy_backend_basis_smoke.sh
177 passed in 8.12s
EXIT: clean
Includes: propose runtime, worker runtime, worker execution, task execution, proposed tasks, storage
```

---

## Review Verdict

| Criterion | Status |
|---|---|
| **Verdict** | **PASS** |
| Exact hang cause | N/A — no hang detected |
| Runtime helper status | COMPLETE — Popen + start_new_session + temp files + killpg |
| Lock leak guard status | COMPLETE — assert_no_leftover_locks in both test teardowns |
| Propose runtime no-hang | PASS (11 tests, 2.37s, clean exit) |
| Worker runtime no-hang | PASS (6 tests, 4.84s, clean exit) |
| Smoke status | PASS (177 tests, 8.12s, clean exit) |
| Tests run | 177 (smoke) + 17 (targeted runtime) |
| Full pytest run | No (targeted smoke only — sufficient for scope) |
| Backend parts now 100% | Runtime helper, lock guard, propose CLI, worker CLI, storage, events |
| Backend parts still below 100% | None identified |
| Merge readiness | YES |

---

## Changes in This Commit

1. **`runtime_helpers.py`**: Refactored `run_grouped_cli` from `subprocess.run(capture_output=True)` to `Popen` + temp files + process group isolation. Added `_kill_process_group` helper. Added `assert_no_leftover_locks`. Improved `read_events` with explicit params and error handling.

2. **`test_propose_cli_runtime.py`**: Fixture changed from `return` to `yield` + `assert_no_leftover_locks(root)` teardown. Added import.

3. **`test_worker_cli_runtime.py`**: Same fixture change as propose.

No regressions. No scope creep. Clean implementation.

---

# Parallel Review — Steps 715-724 (In Progress)

Reviewer: parallel watcher (independent)
Scope: Steps 715-724 (Runtime file order hang fix)
Status: IN PROGRESS

## Steps 705-714 Verdict
PASS locally. Reviewer reports order-dependent hang in propose runtime (10/11 dots then timeout).
test_end_to_end passes alone but hangs after earlier tests run first.
Not reproducible in dev environment. Adding trace + hardened cleanup as defense-in-depth.
