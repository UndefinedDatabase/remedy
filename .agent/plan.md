# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1351 and R-1353 by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D15).

## Current Step
Round 15 (session 4): book round 14 with R-1416, R-1278 and R-1276; `run_pingpong`'s structural
step (6), the two role providers built in one block; R-1289 and R-1287, which close T005
(DECISION F307 D15).

## Next Steps
1. Book round 15 with R-1287 and R-1289; then T006, R-1279 (the job and run ids bound once around
   `run_job` and `run_pingpong`), with its structural step first.
2. T008, T009, T013, T015 to T020, each with its structural step first (DECISION F307 D5);
   R-1291 with `doctor_core_report`'s boundary, `plan_source` with T013.
3. T021, the closing structural step; then the closure sequence, which carries R-1281's rest.

## Risks
- Several slices edit functions or files the structure ledger lists; each draws that row's
  boundary first, in a commit of its own, and every edit of a listed file is line-neutral or
  shrinks it.
- A move's consumers include module aliases and patch strings; a round's selection is every test
  file that names a module the round touches (R-1416).
- `packages/orchestration/mission_contract.py` stands at 991 lines, nine below the file limit.
- The operator's live service writes the data root the test guard watches (R-1411, T019).
