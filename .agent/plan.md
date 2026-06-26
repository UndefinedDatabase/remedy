# Plan — Steps 5021-5036: Pingpong Staging Symlink + Review Zip Hygiene Closure v5

## Goal
Harden pingpong staging copy, change scanning, and safe diff against symlinks.
Add review ZIP hygiene check for debug detritus.
Add job workflow readiness checklist.

## Current Step
All implementation and tests complete. Ready for commit.

## Completed
- Step 5021: `StagingResult` dataclass + `_create_staging()` rewrite — `followlinks=False`, filter symlink dirs, skip symlink files, `read_bytes`/`write_bytes` instead of `shutil.copy2`, record skipped paths with reasons
- Step 5022: Regression test — external symlink not copied (1 test)
- Step 5023: Regression test — internal symlink not copied (1 test), parent symlink not followed (1 test), normal files copy (1 test)
- Step 5024: `_is_safe_staged_path()` helper — symlink, parent symlink walk, escape, regular file checks
- Step 5025: Regression test — regular file safe (1 test), symlink unsafe (1 test), parent symlink unsafe (1 test)
- Step 5026: `_find_staging_changes()` rewrite — `followlinks=False`, filter symlink dirs, both staged and original paths checked via `_is_safe_staged_path()`
- Step 5027: Regression test — builder staging symlink not in diff (1 test), internal symlink skipped (1 test), parent symlink not in diff (1 test)
- Step 5028: Workspace apply hardening tests verified — 187 task runner tests pass
- Step 5029: Job-promote hardening tests verified — 74 promote tests pass
- Step 5030: `_compute_safe_diff()` updated — checks both staged and original paths via `_is_safe_staged_path()`, produces `[unsafe staged artifact skipped: reason]` placeholder
- Step 5031: `make_review_zip.sh` detritus check + regression test using real `git init`
- Step 5032: `.agent/job_workflow_readiness.md` — readiness checklist for single-command workflow
- Step 5033: All runner/evidence/promote safety tests pass — 449 orchestration tests, 8067 full suite
- Step 5034: Targeted smokes — fulfillment 109 (×2), fast lane 571, runtime 4/4 suites
- Step 5035: Architecture guard clean — no `shutil.copy2` in pingpong, no `followlinks=True`, no `os.symlink`, no git subprocess in product code
- Step 5036: Handoff — awaiting 5-minute quiet window

## Test Counts
- pingpong_cli: 135 (was 123, +12 new)
- job_task_runner: 187 (unchanged)
- job_promote: 74 (unchanged)
- job_evidence: 53 (unchanged)
- job_fulfillment: 109 (unchanged)
- Full suite: 8067 passed, 8 skipped, 0 failed
