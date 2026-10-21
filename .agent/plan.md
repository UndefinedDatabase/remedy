# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1351 and R-1353 by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D13).

## Current Step
Round 13 (session 4): book round 12 with R-1281 landed in part; `pingpong_loop.py`'s structural
step (3), the provider call to `pingpong_provider_call.py`; R-1277 in the moved seam (DECISION
F307 D13).

## Next Steps
1. Book round 13 with R-1277; then the rest of T005 in the new module: R-1276 (one attempt row
   per real invocation, with its model), R-1278 (a backup link built once, with stream counters
   that continue the primary's), R-1287 and R-1289 (the stop check and the chains handed down).
2. T006, T008, T009, T013, T015 to T020, each with its structural step first (DECISION F307 D5);
   R-1291 with `doctor_core_report`'s boundary, `plan_source` with T013.
3. T021, the closing structural step; then the closure sequence, which carries R-1281's rest.

## Risks
- Several slices edit functions or files the structure ledger lists; each draws that row's
  boundary first, in a commit of its own.
- `packages/orchestration/mission_contract.py` stands at 991 lines, nine below the file limit.
- The operator's live service writes the data root the test guard watches (R-1411, T019).
