# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 11 finishes the read views of T002. It books round 10's PASS, registers R-0902 and
records DECISION F261 D10, then points the `job report` and `do job-report` hints at
`job show --full` with R-0901, folds `job report` into the `report` section, deletes
`do job-report`, and makes `job show` name an unreadable job record, one table per commit,
and appends the Landed lines of R-0901 and R-0902.

## Next Steps

1. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
2. T003, the prune to D4, with R-0900; then T004.

## Risks

- 98 findings are open by distinct id before this round's record and 99 after it; three are
  High, R-0803, R-0804 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- `job show --full` builds every section, the run report's sources among them, so it is the
  slowest read of a job.
