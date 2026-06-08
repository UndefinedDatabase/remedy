# Parallel Review — Steps 765-774 (Final)

Reviewer: parallel watcher (independent)
Scope: Steps 765-774 (Pipe-safe pytest runner — no inherited stdout/stderr pipes)
Commit reviewed: 9ecba41
Previous commit: 18b136c (Steps 755-764 — PASS)
Timestamp: 2026-06-08

---

## Status: PASS

Pytest runner fully process-isolated. All smoke tests exit cleanly. No hangs.

---

## Check Results

### 1. Pytest Runner — `scripts/remedy_pytest_runner.py`

| Requirement | Status | Detail |
|---|---|---|
| File exists | OK | 149 lines |
| Uses `Popen` | OK | Line 72 |
| `start_new_session=True` | OK | Line 78 |
| Temp files for stdout/stderr | OK | Lines 64-69: `NamedTemporaryFile` |
| `stdin=subprocess.DEVNULL` | OK | Line 76 |
| `close_fds=True` | OK | Line 77 |
| `killpg` on timeout | OK | Lines 87, 91 |
| `_ensure_pg_dead` on success path | OK | Line 98 |
| No `shell=True` | OK | Confirmed absent |
| Bounded output (512KB) | OK | Line 26: `MAX_OUTPUT_BYTES = 512 * 1024` |
| Returns pytest exit code | OK | Line 136 |
| Timeout returns 124 | OK | Line 134 |
| Temp file cleanup in finally | OK | Lines 105-115 |

### 2. remedy_pytest.sh

| Requirement | Status | Detail |
|---|---|---|
| Keeps flock lock | OK | Lines 28-35 |
| Calls pytest runner | OK | Line 42: `"${PYTHON}" "${RUNNER}" -- "$@"` |
| No direct `timeout ... python3 -m pytest` | OK | Removed — uses runner |
| Exports timeout env | OK | Line 22 |

### 3. Contract Tests — `tests/cli/test_pytest_runner.py`

| Test | Status |
|---|---|
| `test_runner_exists` | PASS |
| `test_runner_no_shell_true` | PASS |
| `test_runner_uses_start_new_session` | PASS |
| `test_runner_uses_temp_files` | PASS |
| `test_runner_uses_devnull` | PASS |
| `test_runner_passing_pytest` | PASS |
| `test_runner_failing_pytest` | PASS |
| `test_runner_timeout_returns_124` | PASS |
All 8 passed in 2.36s.

### 4. Test Results

**Backend basis smoke (REMEDY_PYTEST_TIMEOUT_SEC=60):**
```
1. Standalone runtime smoke: propose PASS, worker PASS
2. Runtime helpers: 6 passed in 0.36s
3. Orchestration + storage: 160 passed in 0.92s
=== Backend Basis Smoke PASSED ===
Exit: clean
```

**Runtime wrapper smoke (REMEDY_PYTEST_TIMEOUT_SEC=60):**
```
1. Propose wrapper: 1 passed in 0.73s
2. Worker wrapper: 1 passed in 0.88s
=== Runtime Wrapper Smoke PASSED ===
Exit: clean
```

**Direct wrapper proofs (REMEDY_PYTEST_TIMEOUT_SEC=60):**
```
test_runtime_helpers.py: 6 passed in 0.36s — clean exit
orchestration + storage: 160 passed in 0.96s — clean exit
test_pytest_runner.py: 8 passed in 2.36s — clean exit
```

---

## Changes in This Commit

1. **`scripts/remedy_pytest_runner.py`** (NEW): Pipe-safe pytest runner. Popen + start_new_session + temp files + killpg. Bounded output (512KB). Returns pytest exit code. Timeout returns 124.

2. **`scripts/remedy_pytest.sh`**: Now delegates to `remedy_pytest_runner.py`. Keeps flock lock. Removed direct `timeout ... python3 -m pytest` invocation.

3. **`tests/cli/test_pytest_runner.py`** (NEW): 8 contract tests verifying runner isolation patterns and behavior.

---

## Review Verdict

| Criterion | Status |
|---|---|
| **Verdict** | **PASS** |
| Pytest runner status | COMPLETE — Popen + start_new_session + temp files + killpg + bounded output |
| remedy_pytest.sh status | CORRECT — delegates to runner, keeps flock |
| Backend smoke status | PASS (166 tests + standalone, clean exit) |
| Runtime wrapper smoke status | PASS (2 wrappers, clean exit) |
| Direct wrapper proof status | PASS (174 tests, clean exit) |
| Tests run | 166 (backend) + 2 (wrapper) + 6 (helpers) + 160 (orch/storage) + 8 (runner) = 176 unique |
| Full pytest run | No (targeted smoke — sufficient for scope) |
| Backend parts now 100% | All backend basis components |
| Backend parts below 100% | None identified |
| Merge readiness | YES |

---

## Cumulative Confidence

| Block | Commit | Verdict | Key Change |
|---|---|---|---|
| Steps 695-704 | f705aaf | PASS w/risks | Eliminated flock imports |
| Steps 705-714 | 66e9a29 | PASS | Popen + temp files + killpg |
| Steps 715-724 | a60acff | PASS | Trace + proven cleanup + anti-regression |
| Steps 725-734 | b79746d | PASS | Standalone smoke + thin wrappers |
| Steps 735-744 | 1858f02 | PASS | No pipes in wrappers + split smoke invocations |
| Steps 745-754 | e55c10d | PASS | Remove smoke duplication |
| Steps 755-764 | 18b136c | PASS | No pytest wrappers in backend smoke + hard-kill timeout |
| Steps 765-774 | 9ecba41 | PASS | Pipe-safe pytest runner — full process isolation |

Runtime stability: **final**. Eight consecutive clean blocks. Full architecture:
- Backend smoke = standalone runtime + helpers + orchestration (no pytest wrappers)
- Wrapper smoke = separate script for pytest integration
- Pytest runner = Popen + start_new_session + temp files + killpg (no pipe inheritance)
- remedy_pytest.sh = flock + delegates to runner

---

# Parallel Review — Steps 775-784 (In Progress)

Scope: Backend smoke Python supervisor — replace Bash chaining.
Issue: Bash smoke chains phases in one shell process, inherited fds leak between phases.
Fix: Python supervisor with isolated Popen per phase.
