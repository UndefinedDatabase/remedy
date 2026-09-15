# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 6 continues T002. It books round 5's PASS and records DECISION F261 D5, then renames
`packages/orchestration/job_promote.py` to `job_apply.py` with its two test files in one commit
and its Python identifiers to apply words in a second, each applying a table the round saves
under `.agent/authored/`. No string value, JSON key or name on disk changes in this round.

## Next Steps

1. The output-visible promote words of `job_apply.py`: its status values, reason codes, the
   record key `promotion_id`, the directory `job_promotions` and its human text, with the
   kept-by-sense list DECISION amend0905-vocab D5 names written into the record.
2. `job show --full` composing the read commands as sections, with the blocked-task findings
   R-0806 asks for and the fix R-0896 needs.
3. One commit per folded read command and `do job-report`, each adding its id to the guard.
4. The remaining run-level promote words, and a test for the Acceptance grep of the retired
   word; then T003, the prune to D4, and T004.

## Risks

- 96 findings are open by distinct id before and after this round's record; four are High,
  R-0803, R-0804, R-0806 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so its `--full` form only adds keys to that JSON.
- Renaming the status `promoted` to `applied` meets the task and manifest status `applied`
  that already exists; the words round rules on it before it renames.
