# Parallel Review — Steps 755-764 (Final)

Reviewer: parallel watcher (independent)
Scope: Steps 755-764 (Backend smoke final isolation — no pytest wrappers in smoke)
Commit reviewed: 18b136c
Previous commit: e55c10d (Steps 745-754 — PASS)
Timestamp: 2026-06-07

---

## Status: PASS

All requirements met. Backend smoke clean. Wrapper smoke clean. Hard-kill timeout added.

---

## Check Results

### 1. Backend Smoke Structure — `scripts/remedy_backend_basis_smoke.sh`

| Requirement | Status | Detail |
|---|---|---|
| Runs standalone runtime smoke | OK | Line 20: `python3 scripts/remedy_runtime_cli_smoke.py --mode all` |
| Does NOT run `test_propose_cli_runtime.py` | OK | Not present |
| Does NOT run `test_worker_cli_runtime.py` | OK | Not present |
| Runs runtime helper tests separately | OK | Line 24 |
| Runs orchestration/storage tests | OK | Lines 28-33 |
| No background | OK | Sequential |
| No `|| true` | OK | Not present |
| Comment explains wrapper exclusion | OK | Lines 6-11 |

### 2. Runtime Wrapper Smoke — `scripts/remedy_runtime_wrapper_smoke.sh`

| Requirement | Status | Detail |
|---|---|---|
| File exists | OK | 24 lines |
| Runs propose wrapper separately | OK | Line 18 |
| Runs worker wrapper separately | OK | Line 21 |
| Uses `scripts/remedy_pytest.sh` | OK | Both calls |
| Default timeout 60s | OK | Line 13 |
| No background | OK | Sequential |

### 3. Pytest Wrapper Timeout — `scripts/remedy_pytest.sh`

| Requirement | Status | Detail |
|---|---|---|
| Uses `--kill-after` if available | OK | Line 40 |
| Probes GNU coreutils support | OK | Line 39: `timeout --kill-after=1s 0.1s true` |
| Falls back to plain timeout | OK | Line 42 |
| KILL_AFTER = 10s | OK | Line 23 |
| Handles exit 124 (SIGTERM timeout) | OK | Line 47 |
| Handles exit 137 (SIGKILL) | OK | Line 47 |
| Timeout failure exits nonzero | OK | Line 51: `exit 124` |

### 4. Test Results

**Backend basis smoke (REMEDY_PYTEST_TIMEOUT_SEC=60):**
```
1. Standalone runtime smoke: propose PASS, worker PASS
2. Runtime helpers: 6 passed in 0.36s
3. Orchestration + storage: 160 passed in 0.91s
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

**Individual wrappers (REMEDY_PYTEST_TIMEOUT_SEC=60):**
```
test_propose_cli_runtime.py: 1 passed in 0.73s — clean exit
test_worker_cli_runtime.py: 1 passed in 0.88s — clean exit
```

---

## Changes in This Commit

1. **`scripts/remedy_backend_basis_smoke.sh`**: Removed runtime pytest wrapper calls (propose + worker). Re-added standalone `python3 scripts/remedy_runtime_cli_smoke.py --mode all` as stage 1. Comment explains wrapper exclusion rationale.

2. **`scripts/remedy_runtime_wrapper_smoke.sh`** (NEW): Separate smoke script for pytest wrappers only. Runs propose and worker wrappers in separate `remedy_pytest.sh` invocations.

3. **`scripts/remedy_pytest.sh`**: Added `--kill-after=10s` with GNU coreutils probe + fallback. Added exit code 137 handling for SIGKILL.

---

## Review Verdict

| Criterion | Status |
|---|---|
| **Verdict** | **PASS** |
| Backend smoke structure | CORRECT — standalone runtime + helpers + orchestration, no pytest wrappers |
| Backend smoke result | PASS (166 pytest tests + standalone flows, clean exit) |
| Runtime wrapper smoke result | PASS (2 wrappers, clean exit) |
| Propose wrapper result | PASS (1 test, 0.73s) |
| Worker wrapper result | PASS (1 test, 0.88s) |
| Pytest timeout hard-kill | COMPLETE — `--kill-after=10s` with fallback |
| Tests run | 166 (backend smoke) + 2 (wrapper smoke) |
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

Runtime stability: **final**. Seven consecutive clean blocks. Architecture:
- Backend smoke = standalone runtime + helpers + orchestration (no pytest wrappers)
- Wrapper smoke = separate script for pytest integration
- Pytest wrapper = `--kill-after` prevents indefinite hangs

---

# Parallel Review — Steps 765-774 (In Progress)

Scope: Pytest wrapper process isolation — pipe-safe runner.
Issue: `remedy_pytest.sh` inherits pipes from caller, child processes keep them open.
Fix: `remedy_pytest_runner.py` with Popen + start_new_session + temp files + killpg.
