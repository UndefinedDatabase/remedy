# Live Review — F017 Scope Fences

## Status
**T001 BUILT** — FenceSpec + pure path checker + exhaustive tests.
**T002 BUILT** — Applicator enforcement, atomicity, change-set preflight,
                  violation Evidence, postmortem classification.

Module: `packages/orchestration/scope_fences.py`
Tests:  `tests/orchestration/test_fences.py` — 78 passed
        `tests/orchestration/test_applicator_fences.py` — 43 passed
Total:  121 tests

## Next
- T003: job field, config keys, CLI display (not started)
