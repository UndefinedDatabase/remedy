# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 7 continues T002. It books round 6's PASS and records DECISION F261 D6, then renames the
output-visible words of `job apply` in three commits, its status values and reason codes, the
job apply record's key, directory and temporary prefix, and its printed text, prose and
`--skip-blocked` help, and adds guards for the record and that help in a fourth commit; each
applies a table the round saves under `.agent/authored/`.

## Next Steps

1. `job show --full` composing the read commands as sections, with the blocked-task findings
   R-0806 asks for and the fix R-0896 needs.
2. One commit per folded read command and `do job-report`, each adding its id to the guard.
3. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
4. T003, the prune to D4, and T004.

## Risks

- 96 findings are open by distinct id before and after this round's record; four are High,
  R-0803, R-0804, R-0806 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so its `--full` form only adds keys to that JSON.
- Job apply records written before this round stay under `job_promotions/`, and nothing reads
  them after it.
