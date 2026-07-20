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

## Next
- Fresh canonical F017 Evidence + READY_FOR_REVIEW ZIP
