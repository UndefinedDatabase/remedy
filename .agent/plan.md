# Plan — F055 Rehearsal (dry check)

## Goal
`remedy do --rehearse` plans an order and stops at the approval of its plan, building no worker,
applying nothing and writing nothing into the repository; it records what a run would cost, risk
and write, and a real run reuses the rehearsed plan without planning again
(docs/roadmap/features/T3_F055.md; DECISIONs F055 D1 and D2).

## Current Step
Session 1, round 2 on `feature/f055-rehearsal`: book round 1 and R-1316, then land T002 — the
rehearsal's record and summary under DECISION F055 D2 — and repair R-1316 with a positive control
of the applicator counter.

## Next Steps
1. T003: the real run from a rehearsed plan without a second planning call, the warning when the
   repository moved, the rehearsed label, and the end-to-end proof.
2. The closure sequence: the one full suite, the self-use run, the evidence and the pull request.
