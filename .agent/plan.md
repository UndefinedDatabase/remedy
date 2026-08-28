# Plan — amend0828-daily-driver

Branch: feature/amend0828-daily-driver, cut from `main` at the merge of PR #218
(which closed F037). Operator collective order amend0828-daily-driver, five
points, carrying the operator's authorization for every decision it names.

## Goal
Make Remedy fit as a daily driver. Two operator dogfooding findings become built
behaviour (deliberate partial promotion on `do job-promote`; cost truth on the
`do job-run` path), one blind test is repaired, and the two remaining pieces of
planned-but-unregistered scope get honest STATUS lines.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| 3 — repair the R-0714 tautology test | done | red-proved in both directions |
| 1 — `--skip-blocked` partial promotion | done | red-proved; flag-shape pinned |
| 2 — cost truth on the job-run path | done | stats cost shows 1 row |
| 4 — register the split-off F037 rest | next | new line before F033 |
| 5 — register the self-use track | pending | registration only, not built |

## Next Steps
1. Point 1: `--skip-blocked` on `do job-promote`, plus the honest `Next:` line on
   every blocked output. The guardrail itself is NOT weakened.
2. Point 2: arm the F103 ledger mirror on the `do job-run` path.
3. Points 4 and 5: two new Package 1 feature lines with full ledger atomicity —
   the TOTAL_FEATURES pin and the README counters in the same commit as STATUS.
4. Full battery (docs suite, canary, touched tests, ruff), PR, hosted run green,
   then merge. End state: 0 open PRs.

## Risks
- The two registrations shift every downstream feature counter; STATUS and the
  four README pins must land in ONE commit or `tests/docs/` goes red.
- Point 2 makes `do job-run` write an evidence bundle it did not write before.
