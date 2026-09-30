# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 6, round 23: the closure's evidence round (STATUS_closure_protocol.md algorithm steps 1
and 2). Round 22 is booked PASS: F293 closes at a 24.5 percent cut and the rest of T002 is F294
(DECISION F293 D15). This round's first commit is the accepted head; the worker then previews the
staging-copy reclaim, builds the evidence job `f293r23e1001` from the fork point `8a067a3b9`, and
builds the review package from the clean, pushed tree. The open-findings count is 2 (`R-1117`,
`R-1125`, both owned by F290).

## Next Steps
1. The closing round: book round 23, rotate the ledger, set `SU-040`'s `consumed_by` to F293, flip
   F293's STATUS line to `[x]` with the package readings and sync the README in the same commit,
   and open the pull request.

## Risks
- The evidence run is serial (`pytest -v` without `-n`) over 1,195 node ids; it takes a few
  minutes.
- A package that does not read `READY_FOR_REVIEW` is a closure blocker; the worker reports the raw
  error and hands back.
