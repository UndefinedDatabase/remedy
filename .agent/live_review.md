# Live Review — Steps 3519-3655: Workspace-Staged Fulfillment v0.2-v0.4

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Timestamp: 2026-06-22

## Verdict (reviewer-owned)
**FAIL** @ 02989df

Closure commit 8190c73 (Steps 3606-3655) submitted. Awaiting re-review.

## Prior verdicts
- **FAIL** @ 2d52bca — 2 Blocker, 4 High, 5 Medium, 2 Low (Steps 3519-3555)
- **FAIL** @ 02989df — 3 Blocker, 3 High, 4 Medium (Steps 3556-3605)
- **PASS** @ 79890f3 — Steps 3276-3435 (merged as PR #100)

## Finding status from prior FAIL (02989df → 8190c73 closure)

### R-0214 Blocker — Tests run against target repo instead of staging → **Resolved @ 8190c73**
`test_execution_service.py` now has `repo_root_override` field on `TestExecutionRequest`.
`execute_test_run()` accepts `data_dir` param and uses `repo_root_override` when set.
Fulfillment wires `repo_root_override=str(staging_ws.staging_dir)` and `scope="staged"`.
Tests: `TestStagedTestExecution` (2 tests) verify no .pytest_cache or __pycache__ in target.

### R-0215 Blocker — Target repo test artifact mutation → **Resolved @ 8190c73**
Tests now run in staging dir via `repo_root_override`. Test artifacts created in staging,
not target. Staging is discarded after fulfillment. `TestStagedTestExecution` verifies.

### R-0218 Blocker — Completion without promotion contract → **Resolved @ 8190c73**
Contract now has `requires_target_promotion: bool = True`. `check()` adds blockers
`target_not_promoted` and `no_promotion_files` when promotion didn't succeed.
Promotion-first ordering: promote → record result → contract check → completion decision.
Tests: `TestPromotionContract` (2 tests) verify blocked/allowed.

### R-0202 Blocker (prior) — Completion without promotion truth → **Resolved @ 8190c73**
Same fix as R-0218. Contract gates on `staging_promoted` and `promotion_files`.
Promotion happens BEFORE contract check. Contract has full truth when checking.

### R-0216 High — code_applied truth still counts staged apply → **Resolved @ 8190c73**
`_extract_job_truth()` in job.py now uses `staging_promoted` as authoritative for
`code_applied` when `staging_used=True`. Staged-scope apply records don't count.
Tests: `TestCodeAppliedTruthV04` (2 tests) verify.

### R-0219 High — Promotion blockers ignored → **Resolved @ 8190c73**
Promotion-first ordering means blockers are known before contract check. Contract
`requires_target_promotion` gates on `staging_promoted`. If promotion has blockers
and files aren't promoted, contract fails. Tests verify via `TestPromotionContract`.

### R-0203 High (prior) — Blocked jobs report code_applied=true → **Resolved @ 8190c73**
Same fix as R-0216. `staging_promoted` is authoritative. Blocked jobs show
`code_applied=false`. Fulfillment blockers and next_safe_action surfaced in status.
Tests: `TestBlockedFulfillmentStatus` (2 tests) verify.

### R-0222 Medium — Review bundle missing staging truth → **Resolved @ 8190c73**
`review_bundle.py` now has `_build_fulfillment_summary()` function and
`fulfillment_summary.json` in `REQUIRED_SECTIONS` and `_REVIEW_BUNDLE_SECTION_SPECS`.
Tests: `TestReviewBundleFulfillment` verifies section in bundle.

### R-0223 Medium — Demo docs invalid command → **Resolved @ 8190c73**
`docs/first-fulfilled-job-demo-v0.md` changed from `remedy job create "..." --json`
to `JOB_ID=$(remedy job create "...")`. Tests: `TestDemoDocsCommands` (3 tests).

### R-0225 Medium — 5 introduced test failures → **Resolved @ 8190c73**
- 3 contract tests: updated to include `staging_promoted=True, promotion_files=[...]`
- `test_apply_blocked_stops_completion`: renamed to `test_existing_md_uses_modify_intent`
  (existing MD now uses modify intent, so apply succeeds — this is correct behavior)
- `TestApplyRecord` tests: `scope` field properly added to `PatchApplyResult`

### R-0221 Medium — data_dir inconsistency → **Resolved @ 8190c73**
`_persist_test_record`, `_create_failure_artifact`, `finalize_test_outcome` all now
accept and use `data_dir` parameter. `load_job(job_id, data_dir)` and
`save_job(job, root=data_dir)` used consistently.

### R-0208 Medium (prior) — Review bundle missing staging truth → **Resolved @ 8190c73**
Same as R-0222. Fulfillment summary section added.

### R-0209 Medium (prior) — Missing target unchanged proof → **Resolved @ 8190c73**
Tests now run in staging via `repo_root_override`. No .pytest_cache or __pycache__
created in target repo. Test `TestStagedTestExecution` verifies clean target.

### R-0226 Low — Mid-function import → Deferred
`import shutil as _shutil` at line 760. Low priority, not a correctness issue.

### R-0212 Low — Branch reuse → Same. Low.

### R-0213 Low — Lint → Deferred. I001 import sort.

## Test evidence (builder-run, commit 8190c73)
- Fulfillment tests: 90 passed, 7.47s
- Full suite: 2127 passed, 1 failed (pre-existing test_project_brain::test_full_chain_order), 2 skipped
- Pre-existing failure verified: same test fails on stashed/clean HEAD

## Architecture guard scan (8190c73)
- No `shell=True`
- No provider SDK imports
- No network calls
- No subprocess in staging/fulfillment engine
- No git operations
- No metadata mutation
- `repo_root_override` on both apply and test execution
- `data_dir` threaded through all persist helpers

## Merge readiness
Awaiting reviewer re-review @ 8190c73. All 3 Blockers, 3 High, 4 Medium resolved.
2 Low deferred (import sort, branch reuse).

NO PR merge unless reviewer passes and user asks.

## Reviewer audit log
- PR #101 @ 2d52bca (Steps 3519-3555): FAIL with 2B/4H/5M/2L.
- Closure @ 02989df (Steps 3556-3605): addressed R-0201, R-0204, R-0205, R-0206, R-0211.
- Verdict FAIL @ 02989df — 3B/3H/4M remaining.
- Closure @ 8190c73 (Steps 3606-3655): addressed R-0214, R-0215, R-0218, R-0216, R-0219,
  R-0203, R-0222, R-0223, R-0225, R-0221, R-0208, R-0209. All Blocker/High/Medium resolved.
- Awaiting reviewer re-review.
