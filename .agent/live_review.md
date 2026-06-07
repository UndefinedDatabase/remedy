# Parallel Review — Steps 705-714 (Baseline Assessment)

Reviewer: parallel watcher (independent)
Scope: Steps 705-714 (Runtime process exit fix)
Last commit reviewed: f705aaf (Step 704 — no 705-714 commits exist yet)
Timestamp: 2026-06-07

---

## Status: WAITING FOR CHANGES

No commits for Steps 705-714 exist yet. This is a baseline assessment of the current state.

---

## Current State Assessment

### 1. Runtime Helper — `tests/cli/runtime_helpers.py:85-109`

| Requirement | Status | Detail |
|---|---|---|
| Uses `Popen` | MISSING | Uses `subprocess.run` |
| Uses `start_new_session=True` | MISSING | Not present |
| Uses temp files for stdout/stderr | MISSING | Uses `capture_output=True` (pipes) |
| Kills process group on timeout | MISSING | Only `TimeoutExpired` catch, no pgid kill |
| Best-effort cleanup after success | MISSING | No cleanup |
| No `shell=True` | OK | Not used |

**Verdict: `subprocess.run(capture_output=True)` without process-group cleanup = BLOCK condition per spec.**

However: tests currently pass and exit cleanly (see test results below). The `close_fds=True` + `stdin=subprocess.DEVNULL` mitigations from Step 704 appear effective for now.

### 2. Lock Leak Guard — `assert_no_leftover_locks`

| Requirement | Status |
|---|---|
| Function exists | NOT FOUND in any source file |
| Called in propose runtime teardown | NO |
| Called in worker runtime teardown | NO |

**Verdict: MISSING. No lock leak guard in test files.**

### 3. Propose Runtime — No-Hang Test

```
REMEDY_PYTEST_TIMEOUT_SEC=60
tests/cli/test_propose_cli_runtime.py
11 passed in 1.84s
EXIT: clean (no hang)
```

### 4. Worker Runtime — No-Hang Test

```
REMEDY_PYTEST_TIMEOUT_SEC=60
tests/cli/test_worker_cli_runtime.py
6 passed in 3.73s
EXIT: clean (no hang)
```

### 5. Smoke Test

```
scripts/remedy_backend_basis_smoke.sh
177 passed in 6.43s
EXIT: clean
Includes: propose runtime, worker runtime, worker execution, task execution, proposed tasks, storage
```

---

## Findings Summary

### Structural Gaps (for Steps 705-714 to address)

1. **Runtime helper does not use `Popen`** — uses `subprocess.run(capture_output=True)`. Per spec, this is a BLOCK condition. The builder must refactor to `Popen` + `start_new_session=True` + temp files + process-group kill.

2. **No `assert_no_leftover_locks` guard** — Neither runtime test file has teardown that checks for leftover lock files. Builder must add this.

3. **No process-group cleanup** — On timeout, only `TimeoutExpired` is caught. No `os.killpg()` call. Orphan processes possible under edge conditions.

### What Works Now (carry forward from Step 704)

- `close_fds=True` prevents fd inheritance
- `stdin=subprocess.DEVNULL` prevents stdin blocking
- No flock imports in runtime test files (docstring enforced)
- Tests pass and exit cleanly
- Smoke passes in 6.43s

---

## Review Verdict (Pre-705 Baseline)

| Criterion | Status |
|---|---|
| Runtime helper status | INCOMPLETE — needs Popen refactor |
| Lock leak guard status | MISSING |
| Propose runtime no-hang | PASS (1.84s, clean exit) |
| Worker runtime no-hang | PASS (3.73s, clean exit) |
| Smoke status | PASS (177 tests, 6.43s) |
| Tests run | 177 |
| Full pytest run | No (targeted smoke only) |
| Backend parts now 100% | Tests pass, exit clean |
| Backend parts still below 100% | Runtime helper architecture, lock guard |
| Merge readiness | NOT YET — awaiting Steps 705-714 commits |

**Overall: PASS WITH RISKS**

Tests pass and exit cleanly, but the runtime helper architecture does not meet the spec requirements (Popen, start_new_session, temp files, process-group kill). The current `subprocess.run` approach works due to Step 704 mitigations (`close_fds=True`, `stdin=subprocess.DEVNULL`, no flock imports), but is fragile under edge cases (e.g., subprocess spawning children that inherit pipes).

Steps 705-714 must:
1. Refactor `run_grouped_cli` to use `Popen` + `start_new_session=True`
2. Use temp files (not pipes) for stdout/stderr capture
3. Add `os.killpg()` on timeout
4. Add best-effort process-group cleanup after success
5. Add `assert_no_leftover_locks` teardown to both runtime test files
