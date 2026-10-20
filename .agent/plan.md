# Plan — F310 Budgets that fit the provider, and one stop, one question

## Goal
A job's default limits come from the profile of its provider class, its wall clock measures work
and not waiting, and a budget stop asks the operator exactly one question
(`docs/roadmap/features/T12_F310.md`). Owns findings R-1370 and R-1371.

## Current Step
Round 1 (session 1): claim F310, DECISIONs F310 D1 to D3, structure step (6) of
`packages/orchestration/config.py` (the budget keys to `config_keys_budget.py`), and T001 —
`packages/orchestration/budget_profiles.py` (provider class, profiles, `effective_job_budgets`),
`run_job` reading its limits through it, the planner's suggested budgets no longer limits, and
the execution offer naming the profiles and each provider's class.

## Next Steps
1. Round 2, T002 under DECISION F310 D4: the wall clock counts work from the first model call,
   waits are recorded and summed into `budget_actuals.waited_s`; the Pi call's time bound reads
   `effective_job_budgets` (deferred from round 1 by DECISION F310 D2).
2. Round 3, T003 under DECISION F310 D5: the budget decision carries the blockers, `extend`
   without an answer doubles the exhausted limits, the resume follows by itself, the remainder
   decision is raised only for a final job; the two old raise sites are deleted.
3. Round 4, T004: the lab stop of 2026-10-20 rebuilt as a fixture,
   `docs/system/job-budget-enforcement-v0.md` completed.
4. Closure sequence per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- `run_job` and `plan_order_job` are structure-ledger rows: their edits shrink them or stay
  line-neutral, and every shrink lowers its row in the same commit.
- An order's own caps still bind its jobs (DECISION F310 D3, operator question Q19).
