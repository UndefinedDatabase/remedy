# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 13 books round 12's independently-reviewed PASS (Gate: F280 R12, one prose slip, no new
R-id), authors DECISION F280 D8, and lands the first of DECISION F280 D7's two deferred items:
the prompt-trace `kind` values `"flight-plan"`/`"flight-plan-retry"` become
`"task-plan"`/`"task-plan-retry"` at their two exact-quoted sites (`job_plan.py:181`,
`test_prompt_trace.py:294`) — measured to have no wider pattern match and no collision with the
new spellings, per a dry run in a disposable worktree before authoring.

## Next Steps

1. DECISION F280 D7's remaining deferred item: the DAG-scheduling `inputs["flight"]` key —
   needs its own naming DECISION (no existing convention; `task_plan` already retired for the
   whole-job field, so it cannot simply reuse that name).
2. D5's third owed item: the surviving English-prose noun "flight plan"/"flight-plan" (catalog
   descriptions, CLI print statements, comments describing the concept, including the stale
   `flight_plan.py` filename citations rounds 12 and earlier deliberately left untouched).
3. The `"fp:"` decision-id prefix (5 sites) — explicitly out of scope for D6 (CHOSEN, SECOND);
   needs its own DECISION and measurement before any round touches it.
4. `propose`, once operator question Q4 is answered.
5. `job attach-repo` and `job permit`, once a DECISION gives a writer (DECISION F280 D4).
6. T002: README quickstart (R-0895), flag scanner blind spot (R-0934).

## Risks

- 129 findings open by distinct id (unchanged this round); High: R-0803, R-0804, R-0807, none
  this feature's.
- R-0899 (owned F273): `scripts/remedy_smoke.sh` section 3 reads a `state` key `job show` never
  prints. R-0937 (owned F273): stale flag names in a test's comments. R-0938 (owned F280): a
  stale round-6 handback count; nothing to fix.
- `job attach-repo`/`job permit` are the only writers of a job's repo and test/revert grants;
  their Acceptance line can't hold until a DECISION supplies a writer.
- R-0935: the run contract never inherits a job's F018 budgets. Q4 (propose's deletion) is open.
