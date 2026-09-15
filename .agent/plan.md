# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 12 finishes T002. It books round 11's PASS and the resolutions of R-0901 and R-0902 and
records DECISION F261 D11, then gives the job-result sense of `promote` apply words in the
staging pipeline, at the run level and in the builder's repair prompt, and adds
`tests/docs/test_retired_promote_word.py`, which holds the senses DECISION amend0905-vocab D5
keeps by file and token, one table per commit.

## Next Steps

1. T003, the prune to D4, with R-0900, its split planned by group before its first round.
2. T004, the descriptions, role labels, help wrapping and the remaining Acceptance tests.

## Risks

- 99 findings are open by distinct id before this round's record and 97 after it; three are
  High, R-0803, R-0804 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- T003 deletes groups and flags across the catalog and is the slice most likely to exceed the
  commit-size cap.
