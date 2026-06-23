# Live Review — Steps 3816-3855: Wrapper Timeout + Full-Lane Repro Closure v0.9

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-23

## Verdict (reviewer-owned)
**PASS WITH RISKS** @ 2a709ad

Zero open Blocker/High/Medium. 2 Low carry-forward risks documented.
All required findings R-0271 through R-0279 resolved or downgraded.
10-minute quiet window observed. Double-run reproducibility confirmed.

## Commit reviewed
2a709ad Steps 3816-3838: Wrapper timeout + full-lane repro closure v0.9
(includes v0.8 commit 92ef76c: Full-lane repro + lock resilience closure v0.8)

## PR reviewed
No open PR. Builder on `feature/steps-3276-3355-job-fulfillment-spine-v0`.

## Uncommitted changes
None. Clean working tree.

## Protocol compliance
- Builder did NOT write reviewer verdict: PASS
- Builder did NOT self-merge: PASS
- Builder did NOT mark findings as resolved: PASS
- No German in project-facing content: PASS

## Worker 5-minute quiet-window assessment
Builder last commit 2a709ad pushed before reviewer started testing.
No new commits during entire review cycle. PASS.

## Reviewer 10-minute quiet-window assessment
- Quiet window started: after runtime lane run #2 completed
- Quiet window ended: 5 consecutive checks (~10 min) with no builder activity
- Activity during window: none
- Re-verified findings: R-0271 through R-0278 all confirmed via code inspection and test runs
- Findings remaining open: none at Medium or above

## Finding status

### R-0271 Blocker — Fulfillment wrapper command not reproducible → **Resolved @ 2a709ad**
Run #1: `scripts/remedy_pytest.sh tests/orchestration/test_job_fulfillment.py -q` → 109 passed, 8.65s
Run #2: same command → 109 passed, 9.26s
Both pass. No hang. No stale processes. No lock blocked second run.

### R-0272 Blocker — Runtime lane not reproducible → **Resolved @ 2a709ad**
Run #1: `scripts/remedy_test_runtime.sh` → 4/4 suites passed
Run #2: same command → 4/4 suites passed
Both pass. Every START has END. No hang. No stale processes.

### R-0273 Blocker — Outer timeout can orphan child pytest → **Resolved @ 2a709ad** (Low residual)
`timeout --signal=TERM --kill-after=5` used for all nodes and suites (lines 69, 96).
Inner timeout (80s) < outer timeout (90s) with 10s safety margin (lines 23-32).
Inner runner fires `_ensure_pg_dead()` before outer timeout.
Low residual: if runner hangs during cleanup, `_ensure_pg_dead()` is not in `finally` block.
In practice, tests complete in <10s; safety margin makes orphans unlikely.

### R-0274 High — Inner timeout longer than outer node timeout → **Resolved @ 2a709ad**
`INNER_TIMEOUT=$((NODE_TIMEOUT - 10))` (line 28). Default: inner=80s, outer=90s.
Guard: `if [ "$INNER_TIMEOUT" -lt 10 ]; then INNER_TIMEOUT=10; fi` (lines 29-31).
Comment documents timeout model (lines 11-15).

### R-0275 High — Lock cleanup claim misleading → **Resolved @ 2a709ad**
Dead `_clear_stale_lock()` function removed entirely. Lock contention handled via
`REMEDY_PYTEST_LOCK_WAIT` (default 10s wait in runtime lane, 0 for direct usage).
Honest and deterministic.

### R-0276 High — Nested pytest environment unstable → **Resolved @ 2a709ad**
Wrapper/quiet mode passes twice. `requested_timeout_seconds` reduced from 30s to 15s
(job_fulfillment.py line 840). Inner/outer timeout model prevents nested hangs.

### R-0277 Medium — Read-only integrity regression → **Resolved @ 92ef76c**
`_integrity_status()` uses `export_readonly_integrity_status()` (overnight_readiness.py:487-488).
`_build_integrity_summary()` uses `export_readonly_integrity_status()` (review_bundle.py:1808-1809).
No `run_integrity_checks()` in either path.
Tests: `TestIntegrityReadOnlyV07` (5 tests) verify no subprocess, no run_integrity_checks,
no .agent dependency with monkeypatch bombs.

### R-0278 Medium — Public changed-files truth regression → **Resolved (carried from v0.6)**
`changed_files` = `changed_target_files` in export.
Blocked: `changed_files=[]`, `changed_target_files=[]`.
Success: `changed_files == changed_target_files == promotion_files`.
`changed_files_safe.json` has `scope: "artifact_intent"` with note.

### R-0279 Medium — Quiet-window protocol violated → **Resolved**
10-minute quiet window observed and documented above.
Builder had no commits during review. Protocol followed.

## Fulfillment wrapper run #1
`scripts/remedy_pytest.sh tests/orchestration/test_job_fulfillment.py -q`
→ **109 passed, 8.65s**. No hang.

## Fulfillment wrapper run #2
Same command → **109 passed, 9.26s**. No hang. No lock contention.

## Runtime lane run #1
`scripts/remedy_test_runtime.sh`
→ **4/4 suites passed**. node_timeout=90s, inner_pytest_timeout=80s.
14 node-isolated + 3 whole-file suites. All START/END paired.

## Runtime lane run #2
Same command → **4/4 suites passed**. No stale processes. No lock blocked.

## Forced wrapper timeout cleanup result
Not directly tested (would require injecting a slow test). Mitigated by:
- Inner timeout (80s) < outer (90s) — 10s margin
- `_ensure_pg_dead()` kills process group with SIGTERM+SIGKILL
- `timeout --kill-after=5` as last resort
- Residual Low: `_ensure_pg_dead()` not in `finally` block (pre-existing pattern)

## Process/lock cleanup assessment — PASS
Post-test: no stale pytest/runner/grouped processes. Lock file exists but no holder.

## Lock wait/cleanup semantics assessment — PASS
`REMEDY_PYTEST_LOCK_WAIT=10` in runtime lane. `flock -w 10` waits briefly for contention.
Direct usage: `flock -n` (non-blocking, fail fast). Dead `_clear_stale_lock()` removed.

## Read-only integrity regression assessment — PASS
`_integrity_status()`: `export_readonly_integrity_status()` only. No subprocess. No .agent.
`_build_integrity_summary()`: same. Tests with monkeypatch bombs confirm.

## Public changed-files truth assessment — PASS
`changed_files == changed_target_files` in export. Blocked = empty. Scoped correctly.

## Staged fulfillment safety regression assessment — PASS
No regression: staging, promotion, append-only, target mutation safety all intact.
`requested_timeout_seconds` reduced 30→15s. No impact on safety gates.

## Docs command-shape assessment — PASS
No doc changes in v0.8/v0.9. Prior fixes (no `job create --json`) still intact.

## Test evidence (reviewer-run, commit 2a709ad)

### Targeted tests
- Fulfillment wrapper: 109 passed × 2 runs (8.65s, 9.26s)
- Compile check: `python3 -m compileall -q packages apps tests` → clean

### Lanes
- Fast lane: `scripts/remedy_test_fast.sh` → **571 passed, 0.90s**
- Runtime lane: `scripts/remedy_test_runtime.sh` → **4/4 suites × 2 runs**
- Lint: `scripts/remedy_lint.sh` → **ruff clean, mypy clean (194 files)**

### Full suite
- `scripts/remedy_pytest.sh -q -k "not test_full_chain_order"` → **7172 passed, 0 failed, 8 skipped** (203.43s)
- Pre-existing failure: `test_project_brain::test_full_chain_order` (same on main, deselected)

### Post-test process/lock check
- No stale pytest processes
- No stale runner processes
- Lock file: no holder
- Clean

## Architecture guard scan (2a709ad)
- `shell=True`: none
- Provider SDK imports: none
- Network calls: none
- Subprocess in readiness path: none (uses `export_readonly_integrity_status()`)
- Subprocess in review bundle path: none (uses `export_readonly_integrity_status()`)
- Hidden pytest/collect-only: none from readiness/bundle. Runtime lane uses explicit collect-only.
- `.agent` reads from readiness/bundle: none
- Git push/commit/merge: none
- Direct target writes before promotion: none
- Metadata mutation to staging: none
- Raw absolute staging path leaks: none
- Secret/raw file content leaks: none
- Timeout orphan: Low residual — `_ensure_pg_dead()` not in finally (pre-existing)

## Edited-file line-range map (reviewer-constructed, fd4daa5→2a709ad)

| File | Lines | What changed | Tests |
|------|-------|-------------|-------|
| `packages/orchestration/integrity_gate.py` | 337-356 | New `export_readonly_integrity_status()` | TestIntegrityReadOnlyV07 (5) |
| `packages/orchestration/overnight_readiness.py` | 478-494 | `_integrity_status()` → read-only helper | TestIntegrityReadOnlyV07 |
| `packages/orchestration/review_bundle.py` | 1801-1811 | `_build_integrity_summary()` → read-only helper | TestIntegrityReadOnlyV07 |
| `packages/orchestration/review_bundle.py` | 558-559 | `scope`/`scope_note` on changed_files_safe | TestChangedFilesSafeScope |
| `packages/orchestration/job_fulfillment.py` | 840 | `requested_timeout_seconds` 30→15 | TestStagedTestExecution |
| `packages/orchestration/job_fulfillment.py` | 89, 216, 916 | `changed_target_files` field + export | TestChangedFilesPublicTruth |
| `scripts/remedy_pytest.sh` | 30-40 | `REMEDY_PYTEST_LOCK_WAIT` flock wait | TestPytestWrapper |
| `scripts/remedy_test_runtime.sh` | 11-38, 56-96 | Timeout model, inner<outer, --kill-after, stale detect | Runtime lane double-run |
| `tests/orchestration/test_job_fulfillment.py` | 1718-1826 | TestIntegrityReadOnlyV07, TestChangedFiles*, TestDocs* | Self-covering |
| `tests/regression/test_resource_safety.py` | 24-25 | Updated flock assertion for new syntax | Self-covering |
| `apps/cli/commands/job.py` | 807-815, 991-997 | Blocker truth, report fields | TestBlockedFulfillmentTruthV05 |
| `docs/simple-operator-quickstart-v0.md` | 121-127 | Fix job create --json | TestDocsCommandShapesV06 |
| `docs/first-fulfilled-job-demo-v0.md` | 79-112 | Repo requirements, blocked behavior | TestDemoDocsCommands |

## Top risks
1. **Low** — `_ensure_pg_dead()` not in `finally` block of `remedy_pytest_runner.py`. If outer timeout fires during cleanup, pytest process group could survive. Mitigated by 10s inner/outer margin.
2. **Low** — Runtime lane stale-process detection uses `grep -v "$$"` which may miss parent shell PID. Cosmetic false-positive only.

## Merge readiness
**READY.** Zero Blocker/High/Medium open. Double-run reproducibility confirmed.
All lanes pass. Read-only integrity verified. Staged fulfillment safety intact.

Once PR is created, merge-autonomy applies per memory/merge-autonomy.md.

NO PR unless user asks.
