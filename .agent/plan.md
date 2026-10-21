# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1351 and R-1353 by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D4).

## Current Step
Round 3 (session 1): book round 2 and R-1375, R-1376 and R-1412; T004 — R-1310 and R-1294 as one
refactor commit, then R-1286 and R-1288 in the failover walk (DECISION F307 D4).

## Next Steps
1. Round 4: book round 3; T005 — the boundary of `pingpong_loop.py`'s provider call first, then
   R-1276, R-1277, R-1278, R-1287 and R-1289.
2. T006 to T020 in the slice list's order, one module at a time.
3. T021, the closing structural step; then the closure sequence.

## Risks
- Several slices edit functions or files the structure ledger lists; each draws that row's
  boundary first, in a commit of its own.
- The operator's live service writes the data root the test guard watches (R-1411, T019).
