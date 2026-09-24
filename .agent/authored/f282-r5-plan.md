# Plan — F282 Findings paydown v2

Branch: feature/f282-findings-paydown-v2, cut from `main` at
`b8fa02ba`, the merge commit of pull request 269 (amend0923-selfuse-write).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F282.md`). The open set at the claim is 30 by
distinct id, and the feature file lists every one under a slice.

## Current Step

ROUND 5 books round 4's PASS and the resolutions of R-1007, R-1016, R-1027
and R-1035, and lands T008 to T011: an empty diff is the evidence a failing
review needs (R-0999), the self-use generator skips a retired word
(R-1015), `ui stop` is a local state change (R-1034), and closure
precondition 7 names `RESERVED_NAMESPACES` (R-1000), DECISION F282 D5.

## Next Steps

1. T012 and T013: R-1004 in `tests/conftest.py`, R-1045's `uv` pin.
2. T014 to T018: R-0892, R-0622, R-1029, R-0866, then the flakes.
3. T019 in the closure's consolidation pass, then the closure sequence,
   whose self-use run is R-1008's only proof.

## Risks

T014, T015 and T018 may not fit one round each; what does not fit is
carried by name to the next paydown feature at this closure.
