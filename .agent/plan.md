# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 5 opens T002. It books round 4's PASS, registers R-0896 and R-0897, records DECISION
F261 D4, the deletion paragraph of `do promote` and of the run-level apply library only it
used, and deletes both in two commits, each applying a table the round saves under
`.agent/authored/` and the first adding `do.promote` to the deleted-command guard.

## Next Steps

1. The rename of `job_promote.py` to `job_apply.py` with its tests, then its identifiers and
   its output-visible words, keeping the evidence keys D4 names as history.
2. `job show --full` composing the read commands as sections, with the blocked-task findings
   R-0806 asks for and the fix R-0896 needs.
3. One commit per folded read command and `do job-report`, each adding its id to the guard.
4. The remaining run-level promote words; then T003, the prune to D4, and T004.

## Risks

- 94 findings are open by distinct id before this round's record and 96 after it; four are
  High, R-0803, R-0804, R-0806 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so its `--full` form only adds keys to that JSON.
- A run started without a job has no apply command after this round; R-0897 records it for
  F268.
