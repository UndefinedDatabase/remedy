# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 8 continues T002. It books round 7's PASS, registers R-0898, R-0899 and R-0900 and
records DECISION F261 D7. Then, in three commits, `job show` takes the `--json` its hints name
and a guard checks every advertised flag (R-0896), prints the last-round findings of blocked
tasks with a `--full` overflow (R-0806), and gains the `--full` sections with `job permissions`
folded in as the first; a last record commit marks R-0896 and R-0806 landed.

## Next Steps

1. The folds of `job assumptions`, `job fences` and `job dod` into sections of `job show --full`,
   one command per commit, each adding its id to the deleted-command guard.
2. The folds of `job summary`, `job digest`, `job status` and `job report`, then `do job-report`,
   the same way.
3. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
4. T003, the prune to D4, with R-0900; then T004.

## Risks

- 96 findings are open by distinct id before this round's record and 99 after it; four are
  High, R-0803, R-0804, R-0806 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- `job fences` refuses a job whose repository was never attached with `job attach-repo`; its
  section reports that as an error envelope rather than an exit.
