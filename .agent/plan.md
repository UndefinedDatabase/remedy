# Plan — F055 Rehearsal (dry check)

## Goal
`remedy do --rehearse` plans an order and stops at the approval of its plan, building no worker,
applying nothing and writing nothing into the repository; it records what a run would cost, risk
and write, and a real run reuses the rehearsed plan without planning again
(docs/roadmap/features/T3_F055.md; DECISIONs F055 D1 to D3).

## Current Step
Session 1, round 3 on `feature/f055-rehearsal`: book round 2, resolve R-1316 and register
R-1317, write the boundaries of `_cmd_job_run` and `_cmd_status`, then repair R-1317 and land
T003 — the staleness warning, the rehearsed label and the end-to-end proofs.

## Next Steps
1. The closure sequence: the one full suite, the self-use run, the evidence, the STATUS line and
   the pull request.
