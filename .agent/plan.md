# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, PR #233 open into `main`
since F110 R19 (session 7). F110 is CLOSED as a build feature; this round
is a REPAIR round against the still-open PR, triggered by CI going red.

## Goal

Fix the two doc-consistency failures CI reported on PR #233: R19's C3
(`86bc9444`) authored the new STATUS `[x] F110` line and README capability
paragraph but never re-derived the two counts those additions moved, so
`tests/docs/test_docs_consistency.py` failed
`test_the_readme_accepted_count_equals_the_status_count` (68 vs 69) and
`test_the_readme_tier_table_done_column_matches_the_ledger` (Tier 3
Done=3 vs ledger 4).

## Current Step

Round 20 (repair). Rewrite README.md's accepted-count line and Tier 3
Done cell to match the real STATUS.md ledger, register and resolve
finding R-0790 for the omission, push, and confirm CI goes green.

## Next Steps

Once CI is green on PR #233, the Open PR Gate merges it (AGENTS.md):
`gh pr merge 233 --merge --delete-branch`, then `git checkout main` and
`git pull --ff-only`. No further F110 rounds are planned after the
merge — the next session claims the next STATUS `[ ]` feature.

## Risks

- `R-0767` and `R-0784` stay OPEN; both predate F110, documented in the
  Built State section, not F110 defects.
