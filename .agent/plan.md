# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1351 and R-1353 by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D3).

## Current Step
Round 2 (session 1): T003 — book round 1, R-1375's 33 resolution paragraphs and the registration
of R-1412; repair R-1376 and R-1412 in the agent-state check of the commit hook (DECISION F307 D3).

## Next Steps
1. Round 3: book round 2 and R-1375; T004, the failover chain in `model_failover.py`.
2. T005 to T020 in the slice list's order, one module at a time.
3. T021, the closing structural step; then the closure sequence, whose rotation the hook now
   allows.

## Risks
- Several slices edit functions or files the structure ledger lists; each draws that row's
  boundary first, in a commit of its own.
- The operator's live service writes the data root the test guard watches (R-1411, T019).
