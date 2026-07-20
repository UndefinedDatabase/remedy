# Live Review — F017 Scope Fences

## Status
**T001 BUILT** — FenceSpec + pure path checker + exhaustive tests.
**T002 BUILT + REPAIRED** — Applicator enforcement, atomicity, change-set
                  preflight, violation Evidence, postmortem classification.
                  Repairs: config enforcement, fail-closed builtins, role dedup.
**T003 BUILT** — Job model fences field, config keys, CLI display.

Module: `packages/orchestration/scope_fences.py`
Model:  `packages/core/models.py` — JobFences
Config: `packages/orchestration/config.py` — scope.allow, scope.deny
CLI:    `apps/cli/commands/job.py` — remedy job fences
Tests:  `tests/orchestration/test_fences.py` — 78 passed
        `tests/orchestration/test_applicator_fences.py` — 43 passed
        `tests/orchestration/test_fence_e2e.py` — 43 passed
Total:  164 tests (+ 112 postmortem + 57 config)

## Package discrepancy (a0aa69f)
ZIP `remedy-review-20260720-233422-READY_FOR_REVIEW.zip` was built at
HEAD `0846a18` (10 commits). Commit `a0aa69f` was created AFTER packaging
as an agent state update (live_review + plan + STATUS). It is the 11th
commit on the branch but is not covered by the review subject, commit
chain, or content proof in the ZIP. The ZIP content is correct for the
10-commit authority set.

## External review findings (under repair)
1. Duplicate TOML authority — `_read_scope_table` bypasses central config
2. Malformed config fails open — parse error → default allow-all
3. JobFences not closed — accepts unknown fields
4. Five applicators diverge — different subsets of resolve/check/write/raise
5. `enforce_change_set()` has no production callers
6. Artifact writer uses `write_text` — no symlink protection, no atomic write
7. Exception message leaks absolute paths
8. repo_applicator doesn't pass job_fences
9. patch_apply writes no Evidence artifact
10. do_continue uses APPLY_FAILED instead of FENCE_VIOLATION

## Next
Scope 2-5 implementation: centralized resolver, shared enforcement,
secure Evidence, complete E2E tests, fresh package.
