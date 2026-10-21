# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1351 and R-1353 by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D12).

## Current Step
Round 12 (session 3): book round 11 with R-1297, R-1414 and R-1415; R-1281's writer part —
`create_mission` loses `project_ids`, tests write legacy umbrella records directly; the gauntlet's
route and the umbrella readers are carried (DECISION F307 D12).

## Next Steps
1. Book round 12 with R-1281 landed in part; then the listed-file slices in their written order,
   each with its structural step first (DECISION F307 D5): T005, T006, T008, T009, T013, T015 to
   T020; R-1291 with `doctor_core_report`'s boundary, `plan_source` with T013.
2. T021, the closing structural step; then the closure sequence, which carries R-1281's rest.

## Risks
- Several slices edit functions or files the structure ledger lists; each draws that row's
  boundary first, in a commit of its own.
- `packages/orchestration/mission_contract.py` stands at 991 lines, nine below the file limit.
- The operator's live service writes the data root the test guard watches (R-1411, T019).
