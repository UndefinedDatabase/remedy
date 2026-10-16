# Plan — amend1016s D2 (operator order remedy-lab-prep, nothing under .data is tracked)

## Goal
Remove the 902 force-added files under `.data/evidence_exports/` from git, keep the history
documents truthful with a dated line, and stop it from happening again (pre-commit hook, guard
test, closure protocol). Branch feature/untrack-runtime-data. Finding R-1334, DECISION
amend1016s D2.

## Current Step
Done: `git rm -r .data`, `.githooks/pre-commit`, the guard test in
tests/test_data_root_isolation.py, the closure protocol paragraph, T2_F280's dated line, R-1334
and the decision.

## Next Steps
- None in this branch. Rule A5's next proposal is still F078, which only the operator starts.
