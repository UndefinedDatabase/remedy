# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1351 and R-1353 by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D7).

## Current Step
Round 6 (session 1): book round 5 and R-1290 and R-1292; T010 — the lock moves to
`mission_state.py` (a refactor commit), every mission writer holds it (R-1300), and `_seal`
re-seals a changed batch and gives legacy links their batch (R-1285, R-1299), DECISION F307 D7.

## Next Steps
1. Round 7: book round 6; R-1311, the mission leftovers, which closes T010.
2. T011, T012; then the listed-file slices in their written order, each with its structural step
   first (DECISION F307 D5), R-1291 with `doctor_core_report`'s boundary.
3. T021, the closing structural step; then the closure sequence.

## Risks
- Several slices edit functions or files the structure ledger lists; each draws that row's
  boundary first, in a commit of its own.
- The operator's live service writes the data root the test guard watches (R-1411, T019).
