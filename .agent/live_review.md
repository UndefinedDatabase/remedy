# Live Review — Steps 1110-1134

Reviewer: parallel reviewer
Scope: Test Evidence Durability + Snapshot / Rollback Proof v1
Timestamp: 2026-06-12
Last check: 2026-06-12 — Reviewed commit 4572764 (Steps 1118-1133)

## Verdict
PASS WITH RISKS — All 19 block-if conditions resolved or not-found. 5106 tests pass. 1 pre-existing failure (test_full_chain_order, on main). R-0051 (LOW) carry-forward. R-0052 (MEDIUM) new finding on legacy compat path.

## Prior Block Status
- Steps 940-974: PASS
- Steps 975-994: PASS
- Steps 995-1009: PASS
- Steps 1010-1029: PASS WITH RISKS
- Steps 1030-1044: PASS WITH RISKS
- Steps 1045-1064: PASS
- Steps 1065-1084: PASS WITH RISKS (R-0027 carry-forward, resolved in 1086)
- Steps 1085-1109: PASS WITH RISKS (R-0038/R-0041/R-0042/R-0043 carry-forward, resolved in 1111-1117)
- Steps 1110-1134: PASS WITH RISKS (R-0051 carry-forward, R-0052 new)

## Block-If Condition Tracker

| # | Block-If Condition | Status | Finding | Fix Step |
|---|---|---|---|---|
| 1 | test.status command absent from catalog | RESOLVED (38ae52f) | R-0041 | 1111 |
| 2 | same repo concurrent tests across jobs | RESOLVED (38ae52f) | R-0042 | 1112 |
| 3 | evidence failure silently reported as complete | RESOLVED (38ae52f) | R-0043 | 1114-1116 |
| 4 | persistence helpers use broad silent except | RESOLVED (38ae52f) | R-0038 | 1115-1116 |
| 5 | no test_run_started event for actual process | RESOLVED (38ae52f) | R-0050 | 1113 |
| 6 | failure artifact persistence failure hidden | RESOLVED (38ae52f) | R-0038 | 1115-1116 |
| 7 | apply proceeds when snapshot fails | RESOLVED (4572764) | R-0044 | 1121-1123 |
| 8 | structured source snapshots memory-only | RESOLVED (4572764) | R-0045 | 1118-1122 |
| 9 | markdown apply keeps snapshot best-effort | RESOLVED (4572764) | R-0044 | 1123 |
| 10 | snapshot path set incomplete | RESOLVED (4572764) | R-0046 | 1120 |
| 11 | recovery blobs exposed publicly | RESOLVED (4572764) | R-0049 | 1118-1119 |
| 12 | revert uses git reset/checkout/clean | NOT FOUND | — | — |
| 13 | revert overwrites files changed after apply | RESOLVED (4572764) | R-0047 | 1126 |
| 14 | restore hashes/existence not verified | RESOLVED (4572764) | R-0048 | 1127 |
| 15 | generic snapshot_created alone satisfies readiness | NOT FOUND | — | Steps 1130-1132 not started (out of scope) |
| 16 | permission/approval/contract gates weakened | NOT FOUND | — | — |
| 17 | raw source/diff/snapshot/output/secrets leak | NOT FOUND | — | — |
| 18 | final handoff lacks changed files table | RESOLVED (4572764 + this file) | — | 1134 |
| 19 | latest review verdict PENDING while merge-ready claimed | RESOLVED | — | 1134 |

## Finding Ledger

### Carry-forward from Steps 1085-1109

All resolved. See prior block sections.

### R-0051: _emit() still uses except Exception: pass for non-finalization events (LOW)

- **Status**: Open (low priority, carry-forward)
- **Severity**: Low
- **Area**: error-handling
- **Details**: `_emit()` helper at line 494 of `test_execution_service.py` wraps `append_run_event` with `except Exception: pass`. Called for `test_run_blocked`, `test_run_started`, and lifecycle events outside `finalize_test_outcome`. Event loss is non-critical.

### New Findings — Steps 1118-1134

### R-0052: Legacy patch_revert.py compatibility exception is broad (MEDIUM)

- **Status**: Open
- **Severity**: Medium
- **Area**: error-handling
- **Details**: `patch_apply.py:8c` calls `store_pre_apply_snapshot()` with `except (ImportError, OSError, ValueError, KeyError, AttributeError, TypeError): pass`. This is broad but necessary for backward compat. The legacy path is intentionally best-effort. The NEW mandatory snapshot (8b) gates the apply correctly.
- **Impact**: If a future bug in `store_pre_apply_snapshot()` raises a RuntimeError or similar not in the tuple, it will propagate and block the apply. However, blocking is the safe behavior.
- **Mitigation**: The new mandatory snapshot (8b) means `patch_revert.py` tests can be migrated to the new revert service at any time, removing this compat path.

## Changed Files Table (Steps 1118-1134, commit 4572764)

| File | Change | Type |
|------|--------|------|
| `packages/orchestration/repository_snapshot.py` | NEW — unified snapshot service | New |
| `packages/orchestration/source_apply.py` | Mandatory durable snapshot; FileSnapshot.content removed; revert_apply() new API | Modified |
| `packages/orchestration/patch_apply.py` | Mandatory snapshot + DurableApplyRecord; legacy compat call | Modified |
| `apps/cli/command_catalog.py` | snapshot group + inspect + list-applies entries | Modified |
| `apps/cli/commands/__init__.py` | Register snapshot_cmds handlers | Modified |
| `apps/cli/commands/snapshot_cmds.py` | NEW — snapshot.inspect + snapshot.list-applies handlers | New |
| `tests/orchestration/test_repository_snapshot.py` | NEW — 48 tests for snapshot service | New |
| `tests/orchestration/test_source_apply.py` | Updated revert tests for new API | Modified |
| `tests/orchestration/test_source_apply_transaction.py` | Updated for removed FileSnapshot/_rollback | Modified |
| `tests/test_patch_apply.py` | allowed_keys includes snapshot_id/snapshot_verified | Modified |
| `docs/snapshot-rollback-v1.md` | NEW — design docs | New |

## Test Results (commit 4572764)

- 5106 passed, 8 skipped, 1 deselected (pre-existing test_full_chain_order failure on main)
- 48 new snapshot tests in test_repository_snapshot.py — all pass
- All execution service tests (60), CLI runtime tests (23), patch apply tests, source apply tests pass

## Steps 1130-1132 Status

Not started in this block (explicitly out of scope per spec). These require:
- Step 1130: Proof Chain + File Provenance integration
- Step 1131: Progress Ledger + Feature Planner + Review Bundle
- Step 1132: Readiness integration (require verified snapshot + linked apply record)

Block-if #15 ("generic snapshot_created alone satisfies readiness") is deferred to the next block when Steps 1130-1132 are implemented.

## Resolved Findings (Steps 1085-1109)

<details>
<summary>Click to expand resolved findings from prior block</summary>

### R-0027: high_risk_command_execution not in canonical action vocabulary
- **Status**: Resolved — Step 1086
- **Severity**: Low

### R-0029: test_runner.py uses capture_output=True (pipe-based)
- **Status**: Resolved — test_execution_service.py:_run_isolated_process()
- **Severity**: Blocker → Resolved

### R-0030: No process-group cleanup on timeout
- **Status**: Resolved — _kill_process_group() with SIGTERM→SIGKILL
- **Severity**: Blocker → Resolved

### R-0031: No contract enforcement in test_runner.py
- **Status**: Resolved — 13-gate execute_test_run()
- **Severity**: Blocker → Resolved

### R-0032: No secret/environment stripping before subprocess
- **Status**: Resolved — _build_safe_env() strips 14 patterns
- **Severity**: High → Resolved

### R-0033: No concurrency guard for same job/repo
- **Status**: Resolved — TestExecutionLease with fcntl.flock
- **Severity**: High → Resolved

### R-0034: No TestFailureArtifact created on failed/timeout runs
- **Status**: Resolved — Gate 13 _create_failure_artifact()
- **Severity**: High → Resolved

### R-0035: test_runs_used not incremented by test_runner
- **Status**: Resolved — Gate 10 save_usage()
- **Severity**: High → Resolved

### R-0036: max_test_runs=0 makes tests permanently impossible
- **Status**: Resolved — run_test in _DEFAULT_ALLOWED_ACTIONS
- **Severity**: Medium → Resolved

### R-0037: Step 1084 handoff not committed
- **Status**: Resolved — Commit 016d715
- **Severity**: Medium → Resolved

### R-0039: Old test_runner.py:run_tests_local() still has capture_output=True
- **Status**: Resolved — CLI routes through execute_test_run()
- **Severity**: Medium → Resolved

### R-0040: 2 old CLI tests fail — gate order + message format mismatch
- **Status**: Resolved — Gates reordered, tests updated
- **Severity**: Medium → Resolved

</details>
