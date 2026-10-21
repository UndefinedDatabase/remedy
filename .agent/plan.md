# Plan — F307 Findings paydown v9

## Goal
Pay down the open findings F307 takes at its claim, each by the repair its own text names, with
the evidence that discharged it, and carry R-1246, R-1351 and R-1353 by name to the next paydown
(docs/roadmap/features/T2_F307.md; DECISIONs F307 D1 to D11).

## Current Step
Round 11 (session 3): book round 10 (FAIL) with R-1414 and R-1415; repair them — the machine
client interface names the batch's `repo_path` at version 1.26, and the remainder test and a
newest-batch test fail without D11's rules. R-1297 is resolved with them.

## Next Steps
1. Book round 11 with R-1297, R-1414 and R-1415; the rest of T012: R-1281 (the umbrella
   writer), with the structural step of a listed function it touches first.
2. The listed-file slices in their written order, each with its structural step first
   (DECISION F307 D5), R-1291 with `doctor_core_report`'s boundary, `plan_source` with T013.
3. T021, the closing structural step; then the closure sequence.

## Risks
- Several slices edit functions or files the structure ledger lists; each draws that row's
  boundary first, in a commit of its own.
- `packages/orchestration/mission_contract.py` stands at 991 lines, nine below the file limit.
- The operator's live service writes the data root the test guard watches (R-1411, T019).
