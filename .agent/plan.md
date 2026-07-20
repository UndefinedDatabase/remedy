# Plan — F017 Scope Fences — Final Repair & Authority Block

## Goal
Close all external-review findings: duplicate TOML authority, malformed-config
fail-open, open JobFences model, divergent applicator enforcement, unsafe
artifact writer, missing E2E coverage. Reconcile stale package. Produce one
corrected READY_FOR_REVIEW ZIP.

## Discrepancy resolution
ZIP `remedy-review-20260720-233422-READY_FOR_REVIEW.zip` was built at
HEAD `0846a18` (10 commits). Commit `a0aa69f` was created AFTER packaging
(agent state update only — 3 files: live_review, plan, STATUS). The ZIP
content is valid for the 10-commit review subject; `a0aa69f` is a post-
packaging commit not covered by the package. This block starts from the
actual branch HEAD `a0aa69f` (11 commits) and will produce a new package
covering all commits.

## Scope 1 — reconcile branch, STATUS, operator truth
- Record a0aa69f discrepancy in live_review.md
- Update STATUS.md truthfully: T001-T003 built, external-review findings
  under repair, pending external acceptance
- Update context.md, plan.md, live_review.md

## Scope 2 — closed centralized FenceSpec resolution
- Remove `_read_scope_table` private TOML parser from scope_fences.py
- Use central config system (scope.allow, scope.deny) for project/env config
- Add `FenceConfigError` — malformed config blocks, never defaults
- Close `JobFences` with `extra="forbid"`, validate list members
- Create `EffectiveFenceResult` typed provenance carrier
- Document precedence: per-job > central config (env > project > user > default)
  > defaults; builtins always apply

## Scope 3 — shared production enforcement + per-job propagation
- All 5 applicators use `enforce_change_set` — no divergent load/check/write
- Propagate job_fences to repo_applicator (fix check_and_apply_to_repo)
- patch_apply: Evidence artifact + typed classification (not just blocked_reason)
- do_continue: FENCE_VIOLATION stop reason (not APPLY_FAILED), Evidence artifact
- Consistent postmortem classification everywhere

## Scope 4 — secure durable Evidence + redaction
- Replace write_text with secure_fs.write_file_atomically (O_NOFOLLOW, O_EXCL)
- anchor_destination for containment
- No-clobber unique event IDs (uuid-based)
- Closed artifact schema with event_id, provenance, warnings
- Redact absolute paths in exception messages and postmortem reasons
- ContinueStopReason.FENCE_VIOLATION added

## Scope 5 — real E2E tests + Evidence + package
- E2E tests for all 5 applicators with per-job/project/env fences
- CLI execution tests (real CLI against persisted jobs)
- Security tests (closed model, symlink, abs path, malformed config)
- Regression matrix (all existing suites)
- Fresh canonical F017 Evidence + READY_FOR_REVIEW ZIP

## Commits
1. fix(f017): reconcile branch/STATUS/operator state with review findings
2. fix(f017): centralized FenceSpec resolution + closed JobFences + FenceConfigError
3. fix(f017): shared production enforcement boundary + per-job propagation
4. fix(f017): secure durable Evidence + consistent redaction
5. test(f017): complete E2E coverage for all write paths and CLI
6. docs(f017): final implementation state + Evidence + READY_FOR_REVIEW ZIP

## Current Step
Scope 3 complete. Committing shared enforcement, then Scope 4.

## Constraints
- No Fable/subagents/providers/network/Docker. Manual only.
- Do not amend/squash existing F017 commits.
- Do not push, create PR, merge, modify main, or start F018.
- Do not weaken, delete, skip, or xfail tests.
- F017 stays `[~]`, F018 stays `[ ]`.

## Pre-existing baseline failures
test_job_fulfillment.py::TestFulfilledDemoGuide — 7 tests fail because
docs/first-fulfilled-job-demo-v0.md was moved to docs/system/ in commit
e4023a4 (docs restructure) BEFORE F017 branched. Not an F017 regression.
