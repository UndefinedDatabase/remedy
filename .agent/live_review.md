# Live Review — Steps 3519-3605: Workspace-Staged Fulfillment v0.2-v0.3

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Timestamp: 2026-06-22

## Verdict (reviewer-owned)
**FAIL** @ 02989df

6 files changed, +581/-261 (closure delta from 3058440).
PR #101 open (builder did NOT self-merge). Builder did NOT write reviewer verdict.
Working tree clean.

## Prior verdicts
- **FAIL** @ 2d52bca — 2 Blocker, 4 High, 5 Medium, 2 Low (Steps 3519-3555)
- **PASS** @ 79890f3 — Steps 3276-3435 (merged as PR #100)

## Finding status from prior FAIL (2d52bca)

### R-0201 Blocker — Target repo metadata mutation → **Resolved**
No more metadata mutation. Line 778-779: "NO metadata mutation — target_repo stays as real repo."
Apply uses `target_repo_override=staging_ws.staging_dir` (line 797). `try/finally` cleanup (line 949).
Tests `test_target_repo_unchanged_on_success` and `test_target_repo_unchanged_on_test_failure` verify.

### R-0202 Blocker — Completion without promotion truth → **NOT Resolved**
Contract `requires_staging` (line 127) checks `staging_used` but NOT `staging_promoted`.
Contract check runs BEFORE promotion (line 898-900). Promotion at line 903.
Line 923 sets `COMPLETED_VERIFIED` even if promotion has blockers (e.g. all files blocked as
non-markdown). Promotion blockers are appended (line 912) but never re-checked.
See also R-0218, R-0219.

### R-0203 High — Blocked jobs report code_applied=true → **NOT Resolved**
`_extract_job_truth()` (job.py lines 738-787) still determines `code_applied` from artifact
metadata `patch_intent_apply_records` state "applied". Staged apply writes these records.
Blocked jobs would show `code_applied=true` from staged apply records even though target
was never touched. No test verifies `code_applied=false` for blocked jobs.

### R-0204 High — Unsafe filtered copy → **Resolved**
`_is_env_file()`: pattern `name.startswith(".env.")` or `.env-` covers all variants.
`_is_symlink_escape()`: checks `is_symlink()`, resolves path, verifies `is_relative_to()`.
Tests: `test_env_variants_excluded`, `test_symlink_escape_excluded`.

### R-0205 High — Unsafe promotion path → **Resolved**
`_check_path_containment()` verifies both staged and target paths.
Non-markdown blocked with `blockers.append(f"non_markdown:...")`.
Tests: `test_non_markdown_blocked`, `test_path_traversal_blocked`.

### R-0206 High — Existing Markdown append-only → **Resolved**
Prefix-based: `staged_content.startswith(target_content)`. Only suffix appended.
Tests: `test_md_append_only_prefix`, `test_md_replacement_blocked`.

### R-0208 Medium — Review bundle missing staging truth → **NOT Resolved**
`review_bundle.py` not touched. No staging/promotion fields in review bundle.

### R-0209 Medium — Missing target unchanged proof → **PARTIALLY Resolved**
`test_failing_test_leaves_target_unchanged` uses hash comparison BUT explicitly
filters out `.pytest_cache` and `__pycache__` artifacts (line 1316-1318), hiding R-0215.
Hash check is good for content files but the test masks test artifact leakage.

### R-0210/R-0221 Medium — data_dir inconsistency → **PARTIALLY Resolved**
Apply has `target_repo_override` (line 573). Test execution does NOT (see R-0214).

### R-0211 Medium — Test isolation failure → **Resolved**
`atexit.register` replaced with `try/finally` (lines 787, 949-952).
Staging lives under `_fulfillment_dir()` not `/tmp`.
Whole file: 75 passed in 4.86s. No hangs. No full-suite isolation failures from atexit.

### R-0212 Low — Branch reuse → Same. Low.
### R-0213 Low — Lint → NOT Resolved. I001 import sort in job_fulfillment.py:760.

## New findings (Steps 3556-3605 prompt)

### R-0214 Blocker — Tests run against target repo instead of staging
`test_execution_service.py` was NOT modified. `execute_test_run()` reads `target_repo`
from `job.metadata["target_repo"]` (line 591), which points to REAL repo (since R-0201 fix
removed metadata mutation). Tests run at `cwd=str(repo_root)` (line 780) — the real target.

This means:
1. Tests do NOT test staged changes
2. Test pass/fail is based on pre-existing code, not staged work
3. Test artifacts (`.pytest_cache`, `__pycache__`) created in real target repo
4. The entire staging concept is undermined — tests don't validate what was staged

### R-0215 Blocker — Target repo test artifact mutation
Since tests run in real target repo (R-0214), `.pytest_cache` and `__pycache__` are created
in the target BEFORE promotion. The `test_failing_test_leaves_target_unchanged` test
explicitly filters these out (line 1316-1318), masking the issue rather than fixing it.

### R-0216 High — code_applied truth still counts staged apply
Same as R-0203. `_extract_job_truth()` unchanged. Artifact metadata `patch_intent_apply_records`
with state "applied" sets `code_applied=True` regardless of staging vs target scope.

### R-0218 Blocker — Completion without promotion contract
Same as R-0202. Contract does not gate on `staging_promoted`. Completion can happen
without successful promotion. Promotion blockers are recorded but don't prevent
`COMPLETED_VERIFIED` at line 923.

### R-0219 High — Promotion blockers ignored
Line 911-912: `if promotion.blockers: record.contract_blockers.extend(promotion.blockers)`
But line 923 STILL sets `COMPLETED_VERIFIED`. Next suggestions generated at line 930.
Blockers are recorded but have no effect on completion.

### R-0222 Medium — Review bundle missing staging truth
Same as R-0208. review_bundle.py not touched.

### R-0223 Medium — Demo docs invalid command
Demo doc line 22: `remedy job create "..." --json` — but `job.create` in command_catalog
does not have `_JSON_OPT` or `supports_json`. The `--json` flag would be rejected.

### R-0225 Medium — 5 introduced test failures (NEW)
Full suite: 5 failures introduced by closure commit:
- `TestFulfillmentModel::test_contract_check_all_pass` — `requires_staging` requires `staging_used=True`
- `TestCompletionContract::test_accepted_proof_with_reason_passes` — same
- `TestCompletionContract::test_all_gates_pass` — same
- `TestApplyRecord::test_no_diff_preview_in_record` — unexpected `scope` key in record
- `TestApplyRecord::test_apply_state_visible_after_reload` — `JobNotFoundError`

All 5 pass on main. All introduced by this commit.

### R-0226 Low — Mid-function import
Line 760: `import shutil as _shutil` mid-function. Should be module-level.

## Required checks assessment
1. Protocol compliance — **PASS**. Builder did not self-merge, did not write verdict.
2. Staged test execution — **FAIL** (R-0214 Blocker). Tests run against real target.
3. Target mutation — **FAIL** (R-0215 Blocker). Test artifacts in real target.
4. Pytest/cache artifact leakage — **FAIL** (R-0215). Test masks the issue.
5. Explicit data_dir — **PARTIAL** (R-0221). Apply has override, test does not.
6. Apply scope — **PARTIAL**. `StagingApplyRecord.scope` exists but leaks into apply records (R-0225).
7. code_applied truth — **FAIL** (R-0216). Staged apply counts as applied.
8. Blocked status truth — **PARTIAL**. Blockers recorded but don't prevent completion.
9. Promotion contract — **FAIL** (R-0218). Not gated on promotion success.
10. Promotion blockers — **FAIL** (R-0219). Blockers ignored for completion.
11. Existing Markdown actual flow — **PASS**. Prefix-based append works.
12. Staged vs target changed files — **PARTIAL**. `scope` field exists but not consistently used.
13. Review bundle truth — **FAIL** (R-0222). Not touched.
14. Demo docs exactness — **FAIL** (R-0223). Invalid `--json` on `job create`.
15. Whole fulfillment file — **PASS** (75 passed, 4.86s). No hangs.

## Test evidence (reviewer-run, commit 02989df)
- Compileall: clean
- Fulfillment tests (targeted): 75 passed, 4.86s
- Product spine: 72 passed, 0.13s
- Command catalog: 23 passed, 0.41s
- Fast lane: 571 passed, 0.96s
- Runtime lane: 4/4 suites passed
- Lint: NOT clean (I001 import sort)
- Full suite: 7133 passed, **5 failed (introduced)**, 8 skipped, 1 deselected, 212s
  - 3 contract tests fail (requires_staging without staging_used in test data)
  - 2 patch_apply tests fail (scope key leak, JobNotFoundError)

## Architecture guard scan
- No `shell=True`
- No provider SDK imports
- No network calls
- No subprocess in staging/fulfillment engine
- No git operations
- No `.agent/live_review.md` runtime dependency
- No metadata mutation to staging (R-0201 fixed)
- `target_repo_override` added to patch_apply (good)
- test_execution_service NOT modified (R-0214 Blocker)

## Changed Line Map spot-check (3058440..02989df)
- packages/orchestration/staging_workspace.py (+189/-88→369 lines): env file pattern, symlink escape, path containment, prefix-based append, non-md blocker, promotion blockers list.
- packages/orchestration/job_fulfillment.py (+341/-261→956 lines): no metadata mutation, target_repo_override for apply, try/finally cleanup, staging under fulfillment_dir, promotion blocker tracking.
- packages/orchestration/patch_apply.py (+16): target_repo_override parameter.
- apps/cli/commands/job.py (unchanged in this delta but carries prior staging fields).
- tests/orchestration/test_job_fulfillment.py (+247→1322 lines): metadata tests, filtered copy safety, promotion safety, code_applied hash test (but masks pytest artifacts).
- docs/first-fulfilled-job-demo-v0.md (+27): staging invariants. Invalid `--json` on create.

## Top risks
3 Blocker findings (R-0214, R-0215, R-0218).
3 High findings (R-0216, R-0219, R-0203).
4 Medium findings (R-0222, R-0223, R-0225, R-0221).
2 Low (R-0226, R-0212).

The R-0214 Blocker is the most critical: the entire staging concept is undermined because
tests run against the real target repo, not the staging workspace. The R-0201 fix (removing
metadata mutation) created a new problem — test execution lost its only mechanism to find
the staging dir. `test_execution_service.py` needs `target_repo_override` or equivalent.

## Merge readiness
NOT ready to merge. 3 Blockers + 3 High + 4 Medium + 5 introduced test failures.

NO PR unless user asks.

## Reviewer audit log
- PR #101 @ 2d52bca (Steps 3519-3555): FAIL with 2B/4H/5M/2L.
- Closure commit @ 02989df (Steps 3556-3605): addressed R-0201, R-0204, R-0205, R-0206, R-0211.
- R-0214 Blocker discovered: test execution not modified for staging override.
- R-0215 Blocker: test artifacts leak to target, masked by test filter.
- R-0218 Blocker: promotion success not gated in contract.
- 5 introduced test failures.
- Verdict: **FAIL** @ 02989df — 3 Blockers, 3 High, 4 Medium remaining.
