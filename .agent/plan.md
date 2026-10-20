# Plan — F310 Budgets that fit the provider, and one stop, one question

## Goal
A job's default limits come from the profile of its provider class, its wall clock measures work
and not waiting, and a budget stop asks the operator exactly one question
(`docs/roadmap/features/T12_F310.md`). Owns findings R-1370, R-1371 and R-1373.

## Current Step
Round 4 (session 1): book round 3's verdict, R-1373 and the resolution of R-1372, DECISION F310
D6 with the continuations of F269 D9 and F295 D11 and D12, repair R-1373 with a test, and land
T003 part two and T004: the walk's raise of the remainder decision at a budget stop is deleted,
an `abandon` raises it once, and the lab stop of 2026-10-20 is rebuilt as a test.

## Next Steps
1. Resolution lines for R-1370, R-1371 and R-1373 at the gate that proves them.
2. The closure sequence per `docs/roadmap/STATUS_closure_protocol.md`: the one full suite in the
   integration-gate round, the evidence job and the review package, the STATUS line and the PR.

## Risks
- Every listed function a round touches shrinks or stays as long as its row.
- An order's own caps still bind its jobs (DECISION F310 D3, operator question Q19).
