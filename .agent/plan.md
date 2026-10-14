# Plan — F055 Rehearsal (dry check)

## Goal
`remedy do --rehearse` plans an order and stops at the approval of its plan, building no worker,
applying nothing and writing nothing into the repository; it records what a run would cost, risk
and write, and a real run reuses the rehearsed plan without planning again
(docs/roadmap/features/T3_F055.md; DECISION F055 D1).

## Current Step
Session 1, round 1 on `feature/f055-rehearsal`: claim F055, book F308's round 6, move the
catalog's `do` group to a module of its own, write the boundaries of `_cmd_do_order` and `_cmd_do`,
and land T001 — the flag, the stop, the refusals and the counters with their tests.

## Next Steps
1. T002: the rehearsal's record and summary — the planner's cost with its basis, the estimate
   bands, the risks, the DoD's check matrix and the fence simulation.
2. T003: the real run from a rehearsed plan without a second planning call, the warning when the
   repository moved, the rehearsed label, and the end-to-end proof.
3. The closure sequence: the one full suite, the self-use run, the evidence and the pull request.
