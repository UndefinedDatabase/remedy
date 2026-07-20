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
Total:  164 tests (+ 112 postmortem/config)

## Evidence
Job ID: `492b969f-b802-453f-b9da-77554071d7ab`
Base: `fe9898aec951486ee72e6d42eef5cd905c71c625`
Head: `0846a1878cf3f239b7d1f12c4715e030346b9c86`
Authority: 17 files, 3 tasks (T001-T003)
Verdict: PASS_WITH_RISKS (operator-attested manual)
ZIP: `remedy-review-20260720-233422-READY_FOR_REVIEW.zip` (7.8M, 1438 members)
Package status: READY_FOR_REVIEW
Evidence authoritative: true
Review subject alignment: PASS

## Next
Awaiting external acceptance. F017 stays `[~]`.
