# Live Review — Steps 1110-1134

Reviewer: parallel reviewer
Scope: Test Evidence Durability + Snapshot / Rollback Proof v1
Timestamp: 2026-06-12
Last check: 2026-06-12 — Reviewed commit 38ae52f (Steps 1111-1117)

## Verdict
IN PROGRESS — Steps 1111-1117 committed. 6 block-if conditions resolved. 7 snapshot/revert blockers remain (Steps 1118-1134). 83 tests pass.

## Prior Block Status
- Steps 940-974: PASS
- Steps 975-994: PASS
- Steps 995-1009: PASS
- Steps 1010-1029: PASS WITH RISKS
- Steps 1030-1044: PASS WITH RISKS
- Steps 1045-1064: PASS
- Steps 1065-1084: PASS WITH RISKS (R-0027 carry-forward, resolved in 1086)
- Steps 1085-1109: PASS WITH RISKS (R-0038/R-0041/R-0042/R-0043 carry-forward)

## Block-If Condition Tracker

| # | Block-If Condition | Status | Finding | Fix Step |
|---|---|---|---|---|
| 1 | test.status command absent from catalog | RESOLVED (38ae52f) | R-0041 | 1111 |
| 2 | same repo concurrent tests across jobs | RESOLVED (38ae52f) | R-0042 | 1112 |
| 3 | evidence failure silently reported as complete | RESOLVED (38ae52f) | R-0043 | 1114-1116 |
| 4 | persistence helpers use broad silent except | RESOLVED (38ae52f) | R-0038 | 1115-1116 |
| 5 | no test_run_started event for actual process | RESOLVED (38ae52f) | R-0050 | 1113 |
| 6 | failure artifact persistence failure hidden | RESOLVED (38ae52f) | R-0038 | 1115-1116 |
| 7 | apply proceeds when snapshot fails | OPEN | R-0044 | 1121 |
| 8 | structured source snapshots memory-only | OPEN | R-0045 | 1118-1122 |
| 9 | markdown apply keeps snapshot best-effort | OPEN | R-0044 | 1123 |
| 10 | snapshot path set incomplete | OPEN | R-0046 | 1120 |
| 11 | recovery blobs exposed publicly | OPEN | R-0049 | 1118-1119 |
| 12 | revert uses git reset/checkout/clean | NOT FOUND | — | — |
| 13 | revert overwrites files changed after apply | OPEN | R-0047 | 1126 |
| 14 | restore hashes/existence not verified | OPEN | R-0048 | 1127 |
| 15 | generic snapshot_created alone satisfies readiness | NOT YET TESTABLE | — | 1132 |
| 16 | permission/approval/contract gates weakened | NOT FOUND | — | — |
| 17 | raw source/diff/snapshot/output/secrets leak | NOT FOUND | — | — |
| 18 | final handoff lacks changed files table | NOT YET TESTABLE | — | 1134 |
| 19 | latest review verdict PENDING while merge-ready claimed | NOT YET TESTABLE | — | 1134 |

## Finding Ledger

### Carry-forward from Steps 1085-1109

### R-0038: Silent exception swallowing in persistence helpers

- **Status**: Resolved (38ae52f)
- **Severity**: High (raised — 6 instances, not 2)
- **Area**: error-handling
- **Details**: test_execution_service.py had 6 `except Exception` blocks with 4 bare `pass`.
- **Resolution**: Commit 38ae52f (Steps 1115-1117):
  - `_persist_test_record()`: Now returns `bool`. `except (OSError, ValueError, KeyError): return False` + broad fallback `return False`.
  - `_create_failure_artifact()`: Same pattern. Idempotent by test_run_id.
  - `finalize_test_outcome()`: Consolidates gates 10-13. Each failure appends to `evidence_warnings`. `evidence_status` field = complete/partial/failed.
  - 8 `except Exception` remain but none silent in persistence path — all return False or append warnings.
  - `_emit()` (line 494) still has `except Exception: pass` but is event emitter, not persistence helper. Lifecycle events outside `finalize_test_outcome` (test_run_blocked, test_run_started) still silently swallow. LOW risk — noted as R-0051.
- **Block-if**: RESOLVED — persistence helpers no longer silent

### R-0041: Fake test.status next_safe_action

- **Status**: Resolved (38ae52f)
- **Severity**: Medium
- **Area**: command-catalog
- **Details**: `execute_test_run()` emitted `"remedy test status {job.id}"` when lease held. `test.status` not in command catalog.
- **Resolution**: Commit 38ae52f adds `test.status` to CATALOG (read_only, supports_json). `_cmd_test_status()` implemented — read-only lease probe, usage display, latest run (safe fields only). Handler registered. 3 catalog validation tests verify invariant.
- **Block-if**: RESOLVED

### R-0042: Test lease is job-scoped only

- **Status**: Resolved (38ae52f)
- **Severity**: Medium
- **Area**: concurrency
- **Details**: `TestExecutionLease` key = job_id only. Two different jobs targeting same repo could run tests simultaneously.
- **Resolution**: Commit 38ae52f adds `DualTestExecutionLease` with job + repo leases. `_repo_lease_name()` uses SHA-256(canonical_path)[:32] for non-reversible filename. Acquire order: job→repo (deterministic). Release order: repo→job (reverse). Stored at `.data/workspaces/_repo_leases/<hash>.lock`. 7 dual lease tests verify same-job blocked, same-repo blocked, different-repos allowed, stale recovery, name stability.
- **Block-if**: RESOLVED

### R-0043: Partial evidence persistence

- **Status**: Resolved (38ae52f)
- **Severity**: High
- **Area**: evidence-durability
- **Details**: Usage, test record, events, failure artifact were in separate saves. Crash after usage increment but before record persist = budget consumed + invisible run.
- **Resolution**: Commit 38ae52f adds `finalize_test_outcome()` consolidating gates 10-13. Single job reload for usage+record. `evidence_status` field (complete/partial/failed). `evidence_warnings` list. `recovery_action` when failed. Idempotent by test_run_id — retries don't double-count. `TestExecutionResult` has 7 new evidence fields.
- **Block-if**: RESOLVED — evidence failures now surfaced, not silent

### New Findings — Steps 1110-1134 Baseline

### R-0044: Apply proceeds when snapshot creation fails (BLOCKER)

- **Status**: Open → Fix in Steps 1121, 1123
- **Severity**: Blocker
- **Area**: snapshot-integrity
- **Details**: `patch_apply.py:186-189` wraps `store_pre_apply_snapshot()` in `except (ImportError, OSError, ValueError): pass`. Apply continues regardless of snapshot outcome. No verification that snapshot was actually stored. Source apply (`source_apply.py`) has no external snapshot at all — only in-memory FileSnapshot.
- **Evidence**: `patch_apply.py:188-189`: `except (ImportError, OSError, ValueError): pass  # Snapshot is best-effort; apply must not be blocked by snapshot failure.`
- **Block-if**: "apply can proceed when snapshot creation or verification fails"

### R-0045: Structured source snapshots are memory-only (BLOCKER)

- **Status**: Open → Fix in Steps 1118-1122
- **Severity**: Blocker
- **Area**: snapshot-durability
- **Details**: `source_apply.py:FileSnapshot` stores raw `content: str` in memory only. No `snapshot_id`. No persistence to disk. `revert_apply()` at line 398 takes `list[FileSnapshot]`, not `apply_id` — no durable lookup possible. If process crashes after apply, all snapshot data lost.
- **Evidence**: `source_apply.py:70-77` — `FileSnapshot(path, existed, content_hash, content)` with `content: str` field.
- **Block-if**: "structured source snapshots remain memory-only"

### R-0046: Snapshot path set incomplete — no structured source coverage (BLOCKER)

- **Status**: Open → Fix in Step 1120
- **Severity**: Blocker
- **Area**: snapshot-coverage
- **Details**: `patch_revert.py` has durable snapshots at `.data/workspaces/<job_id>/patch_snapshots/<intent_id>/` but only for markdown patches. Source patches (`source_apply.py`) have zero durable snapshot coverage. No unified snapshot path derivation from structured patch contents.
- **Evidence**: `patch_revert.py:10` stores at `patch_snapshots/<intent_id>/`. `source_apply.py` has no equivalent storage path.
- **Block-if**: "snapshot path set is incomplete"

### R-0047: Revert overwrites post-apply changes without drift detection (BLOCKER)

- **Status**: Open → Fix in Step 1126
- **Severity**: Blocker
- **Area**: revert-safety
- **Details**: `patch_revert.py:209-225` restores snapshot bytes without checking if file was modified after original apply. If human edits file between apply and revert, those edits silently destroyed. `source_apply.py:_rollback()` at line 232-245 has same issue — writes `snap.content` without verifying current hash matches post-apply hash.
- **Evidence**: `patch_revert.py:215-217` — `restored_bytes = content_path.read_bytes(); resolved_target.write_bytes(restored_bytes)` — no current-state check.
- **Block-if**: "revert overwrites files changed after the original apply"

### R-0048: Restore does not verify restored hash matches expected (BLOCKER)

- **Status**: Open → Fix in Step 1127
- **Severity**: Blocker
- **Area**: revert-verification
- **Details**: `patch_revert.py:227-229` computes `after_sha256` after revert but does not compare it to `before_sha256` from metadata. No assertion that restore actually produced correct content. `source_apply.py:_rollback()` has no hash verification at all.
- **Evidence**: `patch_revert.py:228-229` — reads `after_data` and computes hash but never asserts `after_sha256 == before_sha256`.
- **Block-if**: "restore hashes/existence are not verified"

### R-0049: Recovery blobs exposed publicly in FileSnapshot (BLOCKER)

- **Status**: Open → Fix in Steps 1118-1119
- **Severity**: Blocker
- **Area**: data-privacy
- **Details**: `source_apply.py:FileSnapshot.content` holds raw file content as public attribute. `ApplyResult.snapshots` list is returned to callers. Any code with `ApplyResult` reference can read raw recovery data. `patch_revert.py` stores recovery in private workspace dir (correct pattern) but `source_apply` does not.
- **Evidence**: `source_apply.py:76` — `content: str` is a public field on `FileSnapshot` dataclass.
- **Block-if**: "recovery blobs are exposed publicly"

### R-0050: No test_run_started event after Popen success (BLOCKER)

- **Status**: Resolved (38ae52f)
- **Severity**: Blocker
- **Area**: event-completeness
- **Details**: `test_execution_service.py` emitted `test_run_completed` and `test_run_timed_out` events but no `test_run_started` event when Popen succeeds.
- **Resolution**: Commit 38ae52f adds `process_started` boolean return from `_run_isolated_process()`. `test_run_started` event emitted only when `process_started is True`. Event includes test_run_id, contract_id, command_source_type, linked IDs, started_at. No PID, no argv, no environment.
- **Block-if**: RESOLVED

### R-0051: _emit() still uses except Exception: pass for non-finalization events (LOW)

- **Status**: Open (low priority)
- **Severity**: Low
- **Area**: error-handling
- **Details**: `_emit()` helper at line 494 wraps `append_run_event` with `except Exception: pass`. Called for `test_run_blocked` (gate 7), `test_run_started` (post-Popen), and lifecycle events outside `finalize_test_outcome`. Event loss is non-critical (events are secondary to durable records) but silent.
- **Impact**: Low — events outside finalization are informational. Durable persistence (usage, test_record, failure_artifact) uses structured returns.

## Baseline Check Matrix (Steps 1110-1134)

| Category | Status | Gap Count | Fix Steps |
|---|---|---|---|
| Test Execution closure | 4 OPEN | R-0038,R-0041,R-0042,R-0043,R-0050 | 1111-1117 |
| Snapshot model | BLOCKER | R-0045 (memory-only) | 1118 |
| Snapshot storage | BLOCKER | R-0046 (no source coverage), R-0049 (public blobs) | 1119-1120 |
| Pre-apply proof | BLOCKER | R-0044 (best-effort snapshot) | 1121 |
| Apply record | OPEN | No durable apply record with snapshot ref | 1124 |
| Revert | BLOCKER | R-0047 (no drift detect), R-0048 (no verify) | 1125-1127 |
| CLI runtime | PENDING | Snapshot/revert CLI not yet needed | 1129 |
| Readiness | PENDING | Cannot test until snapshot model exists | 1132 |
| Integrations | PENDING | Proof Chain, Progress, Review Bundle | 1130-1131 |
| Tests | PENDING | Full test suite for new modules | 1133 |

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

## Test Results
Targeted run (38ae52f): 60 passed test_execution_service + 23 passed CLI runtime = 83 targeted pass
Pre-existing failure: test_project_brain.py::test_full_chain_order (on main)
Next full run: After worker commits snapshot/revert steps (1118+)
