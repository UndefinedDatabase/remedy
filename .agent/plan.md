# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 9 continues T002. It books round 8's PASS and the resolutions of R-0896 and R-0806,
records DECISION F261 D8, then folds `job assumptions`, `job fences` and `job dod` into
sections of `job show --full`, one command per commit, each applying a table the round saves
under `.agent/authored/` and adding the command's id to the deleted-command guard.

## Next Steps

1. The folds of `job summary`, `job digest`, `job status` and `job report`, one per commit.
2. The fold of `do job-report`, with its hints and `related=` tuples.
3. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
4. T003, the prune to D4, with R-0900; then T004.

## Risks

- 99 findings are open by distinct id before this round's record and 97 after it; three are
  High, R-0803, R-0804 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- `job status` and `job report` carry most of the read tests and printed hints left to fold.
