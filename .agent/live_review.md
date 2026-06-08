# Parallel Review — Steps 785-794 (Final)

Reviewer: parallel watcher (independent)
Scope: Steps 785-794 (Final smoke decoupling — three separate smoke surfaces)
Commit reviewed: eac78e3
Previous commit: d4f9c26 (Steps 775-784 — PASS)
Timestamp: 2026-06-08

---

## Status: PASS

Three clean smoke surfaces. Backend smoke no longer mixes helper tests with runtime. All exit cleanly.

---

## Check Results

### 1. Backend Smoke Composition — `scripts/remedy_backend_basis_smoke.py`

| Requirement | Status | Detail |
|---|---|---|
| Runs standalone runtime smoke | OK | Phase 1: `remedy_runtime_cli_smoke.py --mode all` |
| Runs orchestration/storage tests | OK | Phase 2: 4 test files |
| Does NOT run `test_runtime_helpers.py` | OK | Removed (was Phase 2 in prior) |
| Does NOT run runtime wrappers | OK | Confirmed absent |
| Comment explains exclusion | OK | Lines 7-8 |
| Uses `smoke_runner.run_phase` | OK | Lines 37, 46 |

### 2. Process Isolation Smoke — `scripts/remedy_process_isolation_smoke.py` (NEW)

| Requirement | Status | Detail |
|---|---|---|
| Exists | OK | 68 lines |
| Phase 1: runtime helper tests | OK | Line 35 |
| Phase 2: smoke script contracts | OK | Line 45 |
| Phase 3: pytest runner contracts | OK | Line 55 |
| Uses `smoke_runner.run_phase` | OK | All three phases |
| Shell wrapper exists | OK | `remedy_process_isolation_smoke.sh` |
| Shell wrapper uses `exec` | OK | Line 8 |

### 3. Contract Tests — `tests/cli/test_smoke_scripts.py`

| Test | Status |
|---|---|
| `test_backend_smoke_sh_delegates_to_python` | PASS |
| `test_backend_smoke_py_uses_smoke_runner` | PASS |
| `test_runtime_wrapper_smoke_sh_delegates_to_python` | PASS |
| `test_runtime_wrapper_smoke_py_uses_smoke_runner` | PASS |
| `test_smoke_runner_no_shell_true` | PASS |
| `test_smoke_runner_uses_start_new_session` | PASS |
| `test_smoke_runner_uses_temp_files` | PASS |
| `test_process_isolation_smoke_sh_delegates_to_python` | PASS (NEW) |
| `test_process_isolation_smoke_py_uses_smoke_runner` | PASS (NEW) |
| `test_backend_smoke_no_helper_tests` | PASS (NEW) |
| `test_no_or_true_in_smoke_scripts` | PASS (updated) |
All 11 passed in 0.01s.

### 4. Smoke Results

**Backend basis smoke (REMEDY_PYTEST_TIMEOUT_SEC=60):**
```
1. Standalone runtime smoke: propose PASS, worker PASS
2. Orchestration + storage: 160 passed in 0.93s
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

**Process isolation smoke (REMEDY_PYTEST_TIMEOUT_SEC=60):**
```
1. Runtime helpers: 6 passed in 0.36s
2. Smoke contracts: 11 passed in 0.01s
3. Pytest runner contracts: 8 passed in 2.38s
=== Process Isolation Smoke PASSED ===
Exit: clean
```

### 5. Direct Sanity Proofs

```
python3 scripts/remedy_runtime_cli_smoke.py --mode all  → propose PASS, worker PASS
test_runtime_helpers.py: 6 passed in 0.36s
orchestration + storage: 160 passed in 0.91s
```

---

## Changes in This Commit

1. **`scripts/remedy_backend_basis_smoke.py`**: Removed `test_runtime_helpers.py` phase. Now two phases: standalone runtime + orchestration/storage.

2. **`scripts/remedy_process_isolation_smoke.py`** (NEW): Python supervisor for helper/contract tests. Three phases: runtime helpers, smoke contracts, pytest runner contracts.

3. **`scripts/remedy_process_isolation_smoke.sh`** (NEW): Thin shell wrapper with `exec`.

4. **`tests/cli/test_smoke_scripts.py`**: Three new contract tests for process isolation smoke.

---

## Review Verdict

| Criterion | Status |
|---|---|
| **Verdict** | **PASS** |
| Backend smoke composition | CORRECT — standalone runtime + orchestration only, no helper/wrapper tests |
| Backend smoke result | PASS (160 pytest + standalone, clean exit) |
| Runtime wrapper smoke result | PASS (2 wrappers, clean exit) |
| Process isolation smoke result | PASS (25 tests across 3 phases, clean exit) |
| Direct sanity proof | PASS (all commands clean) |
| Tests run | 160 (backend) + 2 (wrapper) + 25 (isolation) + 6 + 160 (direct) = 187 unique |
| Full pytest run | No (three targeted smoke surfaces — sufficient for scope) |
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
| Steps 775-784 | d4f9c26 | PASS | Python smoke supervisors — no Bash shell chaining |
| Steps 785-794 | eac78e3 | PASS | Final smoke decoupling — three separate surfaces |

Runtime stability: **final**. Ten consecutive clean blocks. Full architecture:
- Backend smoke = standalone runtime + orchestration/storage (2 phases)
- Wrapper smoke = propose + worker wrappers (2 phases)
- Process isolation smoke = helpers + smoke contracts + runner contracts (3 phases)
- All phases via `smoke_runner.run_phase` (Popen/session/temp/killpg)
- Shell wrappers = thin `exec` delegation only
- No Bash chaining, no pipe inheritance, no helper-runtime mixing
