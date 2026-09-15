# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 10 continues T002. It books round 9's PASS, registers R-0901 and records DECISION F261
D9, then folds `job digest`, `job summary` and `job status` into sections of `job show --full`,
one command per commit, each applying a table the round saves under `.agent/authored/` and
adding the command's id to the deleted-command guard.

## Next Steps

1. The fold of `job report` with its `--final` and `--interim` forms and the deletion of
   `do job-report`, with their hints, their `related=` tuples and R-0901.
2. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
3. T003, the prune to D4, with R-0900; then T004.

## Risks

- 97 findings are open by distinct id before this round's record and 98 after it; three are
  High, R-0803, R-0804 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- `job report` carries the most read tests and printed hints left to fold, so its hints may
  need a commit of their own ahead of the fold to keep each commit under 500 insertions.
