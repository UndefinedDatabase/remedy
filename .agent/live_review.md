# Live Review — Steps 3736-3775: Read-Only Readiness + Runtime Repro Final Closure v0.7

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-23

## Verdict (reviewer-owned)
**FAIL** @ fd4daa5

2 Blocker open (R-0251, R-0252). 2 High open (R-0253, R-0254). 1 Medium open (R-0258).
Builder created `export_readonly_integrity_status()` (integrity_gate.py:344-356) but neither
`_integrity_status()` nor `_build_integrity_summary()` calls it. Both still call
`run_integrity_checks(collect_only=False)` which runs git subprocess and reads `.agent` files.

## Commit reviewed
fd4daa5 Steps 3696-3714: Review bundle side-effect + public truth closure v0.6

## PR reviewed
No open PR. Builder on `feature/steps-3276-3355-job-fulfillment-spine-v0`.

## Uncommitted changes
- `.agent/live_review.md` — reviewer-owned, expected
- No other uncommitted changes

## Protocol compliance
- Builder did NOT write reviewer verdict: PASS
- Builder did NOT self-merge: PASS
- Builder did NOT mark findings as resolved: PASS
- No German in project-facing content: PASS

## Finding status

### R-0251 Blocker — `_integrity_status()` still calls active integrity checks → **OPEN**
`overnight_readiness.py:483` calls `run_integrity_checks(collect_only=False)`.
This function (integrity_gate.py:264-277) calls:
- `_check_handler_import()` — active import check
- `_check_live_review_verdict()` — reads `.agent/live_review.md` (line 116)
- `_check_plan_consistency()` — reads `.agent/plan.md` (line 163)
- `_check_relevant_untracked()` — runs `subprocess.run(["git", "ls-files", ...])` (line 187)
- `_check_high_blockers_open()` — reads `.agent/live_review.md` (line 222)

Builder created `export_readonly_integrity_status()` (line 344-356) that returns safe `unknown`
but `_integrity_status()` does not use it.

**Fix**: Replace `run_integrity_checks(collect_only=False)` with `export_readonly_integrity_status()`
in `_integrity_status()`.

### R-0252 Blocker — Review bundle integrity summary still calls active integrity checks → **OPEN**
`review_bundle.py:1808` calls `run_integrity_checks(collect_only=False)`.
Same active checks as R-0251.

Docstring (line 1802) claims "no subprocess, no pytest, no .agent reads" — contradicted by implementation.

**Fix**: Replace `run_integrity_checks(collect_only=False)` with `export_readonly_integrity_status()`
in `_build_integrity_summary()`.

### R-0253 High — Readiness/review-bundle path can invoke subprocess → **OPEN**
`_check_relevant_untracked()` (integrity_gate.py:187) runs `subprocess.run(["git", "ls-files", ...])`.
Called from both `_integrity_status()` and `_build_integrity_summary()` via `run_integrity_checks()`.

### R-0254 High — `.agent/live_review.md` product dependency remains → **OPEN**
`_check_live_review_verdict()` reads `.agent/live_review.md` (line 116).
`_check_high_blockers_open()` reads `.agent/live_review.md` (line 222).
`_check_plan_consistency()` reads `.agent/plan.md` (line 163).
All called from readiness/bundle path via `run_integrity_checks()`.

### R-0255 Blocker — Runtime lane not reproducible → **Resolved @ fd4daa5**
`scripts/remedy_test_runtime.sh` completes: 4/4 suites passed. No stale processes.

### R-0256 Blocker — Whole fulfillment file not reproducible → **Resolved @ fd4daa5**
`scripts/remedy_pytest.sh tests/orchestration/test_job_fulfillment.py -q` → 106 passed, 8.17s.
No hang. No orphan processes.

### R-0257 Medium — Public changed-files truth regresses → **Resolved @ fd4daa5**
`export_job_fulfillment_json()` now maps `changed_files` → `record.changed_target_files` (line 216).
`changed_files_safe.json` has `scope: "artifact_intent"` with explanatory `scope_note`.
Tests: `TestChangedFilesPublicTruth` (2 tests), `TestChangedFilesSafeScope` (1 test) verify.

### R-0258 Medium — Missing line-range handoff → **OPEN**
Builder plan.md and commit message lack per-file line ranges. Reviewer constructed independent
line map but builder must provide handoff per protocol.

## Test evidence (reviewer-run, commit fd4daa5)

### Targeted tests
- Fulfillment file: `scripts/remedy_pytest.sh tests/orchestration/test_job_fulfillment.py -q` → **106 passed, 8.17s**
- Compile check: `python3 -m compileall -q packages apps tests` → clean

### Lanes
- Fast lane: `scripts/remedy_test_fast.sh` → **571 passed, 0.87s**
- Runtime lane: `scripts/remedy_test_runtime.sh` → **4/4 suites passed**
- Lint: `scripts/remedy_lint.sh` → **ruff clean, mypy clean (194 files)**

### Full suite
- `scripts/remedy_pytest.sh -q -k "not test_full_chain_order"` → **7172 passed, 0 failed, 8 skipped** (196.39s)
- Pre-existing failure: `test_project_brain::test_full_chain_order` (same on main, deselected)

### Post-test cleanup
- No stale pytest processes
- Lock file: no holder
- Clean

## Architecture guard scan (fd4daa5)
- `shell=True`: none in production
- Provider SDK imports: none
- Network calls: none
- Subprocess in readiness path: **YES** — `_check_relevant_untracked()` runs git (R-0253)
- Subprocess in review bundle path: **YES** — same via `_build_integrity_summary()` (R-0253)
- Hidden pytest/collect-only: **NO** — `collect_only=False` skips pytest subprocess
- `.agent` reads from readiness/bundle: **YES** — live_review.md, plan.md (R-0254)
- Git push/commit/merge: none
- Direct target writes before promotion: none
- Metadata mutation to staging: none
- Raw absolute staging path leaks: none
- Secret/raw file content leaks: none

## `_integrity_status()` read-only assessment — **FAIL**
Still calls `run_integrity_checks()` which is NOT read-only (git subprocess, .agent reads).
`export_readonly_integrity_status()` exists but is unused.

## Review bundle read-only integrity assessment — **FAIL**
`_build_integrity_summary()` calls `run_integrity_checks()`. Same problem as above.
Docstring claims read-only but implementation contradicts.

## No-hidden-subprocess assessment — **FAIL**
`_check_relevant_untracked()` runs `subprocess.run(["git", "ls-files", ...])`.
Called from both readiness and review bundle paths.

## No `.agent` product dependency assessment — **FAIL**
`.agent/live_review.md` read by `_check_live_review_verdict()` and `_check_high_blockers_open()`.
`.agent/plan.md` read by `_check_plan_consistency()`.
All reachable from readiness/bundle paths.

## Runtime lane result — **PASS**
4/4 suites, no hang, no stale processes.

## Whole fulfillment file result — **PASS**
106 passed, 8.17s, no hang.

## Public changed-files truth assessment — **PASS**
`changed_files` = `changed_target_files` in export. Scope annotations present.

## Staged fulfillment safety regression assessment — **PASS**
No regression in staging, promotion, or append-only safety.

## Docs command-shape assessment — **PASS**
Quickstart docs fixed: no `job create --json`. Demo docs already fixed in v0.5.

## Edited-file line-range map (reviewer-constructed)

| File | Lines | What changed | Tests |
|------|-------|-------------|-------|
| `packages/orchestration/overnight_readiness.py` | 479-490 | `_integrity_status()` docstring expanded, `collect_only=False` | TestOvernightReadinessNoHiddenCollect |
| `packages/orchestration/review_bundle.py` | 558-559 | `scope` + `scope_note` on changed_files_safe | TestChangedFilesSafeScope |
| `packages/orchestration/job_fulfillment.py` | 216 | `changed_files` → `changed_target_files` in export | TestChangedFilesPublicTruth |
| `docs/simple-operator-quickstart-v0.md` | 121-127 | Fix `job create --json` → `JOB_ID=$(...)` | TestDocsCommandShapesV06 |
| `tests/orchestration/test_job_fulfillment.py` | 1714-1826 | 7 new v0.6 test classes (overnight, bundle, changed-files, docs) | Self-covering |

## Top risks
1. **R-0251/R-0252 Blocker** — `export_readonly_integrity_status()` exists but unused. Simple fix: wire it up.
2. **R-0253/R-0254 High** — git subprocess + `.agent` reads from readiness/bundle paths. Same root cause as R-0251/R-0252.
3. Builder tests only check `collect_only` param — don't verify no subprocess or no `.agent` reads.

## Required fixes for PASS
1. `_integrity_status()` must use `export_readonly_integrity_status()` not `run_integrity_checks()`
2. `_build_integrity_summary()` must use `export_readonly_integrity_status()` not `run_integrity_checks()`
3. Tests must monkeypatch `subprocess.run` and assert no calls from readiness/bundle paths
4. Tests must verify no `.agent` file reads from readiness/bundle paths
5. Builder handoff must include line-range map

## Merge readiness
**NOT READY** — 2 Blocker + 2 High open. Fix is straightforward: use existing `export_readonly_integrity_status()`.

NO PR unless user asks.
