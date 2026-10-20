# Plan — F310 Budgets that fit the provider, and one stop, one question

## Goal
A job's default limits come from the profile of its provider class, its wall clock measures work
and not waiting, and a budget stop asks the operator exactly one question
(`docs/roadmap/features/T12_F310.md`). Owns findings R-1370 and R-1371.

## Current Step
Round 2 (session 1): book round 1's verdict, DECISION F310 D4, the boundary and step (1) of
`decode_persisted_budget_actuals` (the start instant to `budget_clock.py`), and T002 — version 3
of the persisted record with `waited_s` and `active_until`, `run_job` adding every gap between
runs to the seconds waited, the guard and the Pi call's time bound measuring work alone.

## Next Steps
1. Round 3, T003 under DECISION F310 D5: the budget decision carries the blockers, `extend`
   without an answer doubles the exhausted limits (against the limits the run read), the resume
   follows by itself, the remainder decision is raised only for a final job; the two old raise
   sites are deleted.
2. Round 4, T004: the lab stop of 2026-10-20 rebuilt as a fixture,
   `docs/system/job-budget-enforcement-v0.md` completed, resolution of R-1370 and R-1371.
3. Closure sequence per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- `run_job`, `plan_order_job` and `decode_persisted_budget_actuals` are structure-ledger rows,
  and `budget_guard.py` stands near 1,000 lines: every edit shrinks them or stays line-neutral.
- An order's own caps still bind its jobs (DECISION F310 D3, operator question Q19).
- A budget decision's `extend` still compares against `job.budgets` alone; round 3 repairs that.
