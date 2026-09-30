# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 6, round 22: the closure's decision round. Round 21 is booked PASS and R-1124 resolved:
the closure suite on the tree that ships read exit 0, no process left behind, and 940.64 CPU
seconds, 24.5 percent below T001's 1,246.09. The 40 percent target is missed, so F293 closes at
this scope and the rest of T002 is registered as F294, "Test load diet, part two", directly after
F293 (DECISION F293 D15), with an operator question recording the reversible ruling. R-1125 (the
README's Tier 5 row) is registered for the rolling paydown. The open-findings count is 2
(`R-1117`, `R-1125`, both owned by F290).

## Next Steps
1. The evidence bundle and the review zip (closure algorithm steps 1 and 2), with the staging-copy
   reclaim.
2. The ledger rotation, `SU-040`'s `consumed_by`, the STATUS flip with the README sync, and the pull
   request.

## Risks
- The evidence bundle's verification records never carry a full-suite node list; they carry the
  scoped selections of the closing rounds (STATUS_closure_protocol.md pitfall (d)).
- `base_commit` is the fork point `8a067a3b9`; the branch merged nothing from main, so the
  ancestry-path and plain counts must agree (pitfall (e)).
