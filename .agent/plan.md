# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 10 books round 9's independently-reviewed PASS (Gate: F280 R9, no new finding) and lands
the first half of DECISION F280 D5's own CONSEQUENCE paragraph: module `flight_plan.py` becomes
`job_plan.py`, `FlightPlanResult` becomes `TaskPlanResult`, and D5's eight named lowercase
function names take the `task_plan` spelling, across every importer. `docs/system/vocabulary.md`
moves with them (operator-facing corpus, zero missing paths). `FLIGHT_PLAN_SCHEMA_V` and
`_MAX_FLIGHT_PLAN_TASKS` stay untouched — they live in `schemas/models.py`, and the schema-tag
constant's VALUE is a persisted literal owed to the next round with its sibling literals. No
persisted literal and no English-prose noun changes this round.

## Next Steps

1. The rename's second half: persisted literals (`flight_plan` job-record key, schema tag
   `"flight_plan_v1"`/`FLIGHT_PLAN_SCHEMA_V`, decision type `"flight_plan_approval"` and its
   `decision_queue.py` siblings, `_MAX_FLIGHT_PLAN_TASKS`) and the surviving English-prose noun,
   behind a DECISION naming the new spellings (ruling 9's "no reader of the old job key").
2. `propose`, once operator question Q4 is answered.
3. `job attach-repo` and `job permit`, once a DECISION gives a writer (DECISION F280 D4).
4. T002: README quickstart (R-0895), flag scanner blind spot (R-0934).

## Risks

- 129 findings open by distinct id (unchanged this round); High: R-0803, R-0804, R-0807, none
  this feature's.
- R-0899 (owned F273): `scripts/remedy_smoke.sh` section 3 reads a `state` key `job show` never
  prints. R-0937 (owned F273): stale flag names in a test's comments. R-0938 (owned F280): a
  stale round-6 handback count; nothing to fix.
- `job attach-repo`/`job permit` are the only writers of a job's repo and test/revert grants;
  their Acceptance line can't hold until a DECISION supplies a writer.
- R-0935: the run contract never inherits a job's F018 budgets. Q4 (propose's deletion) is open.
