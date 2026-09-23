# Plan — F282 Findings paydown v2

Branch: feature/f282-findings-paydown-v2, cut from `main` at
`b8fa02ba`, the merge commit of pull request 269 (amend0923-selfuse-write).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F282.md`). The open set at the claim is 30 by
distinct id, and the feature file lists every one under a slice.

## Current Step

ROUND 8 books round 7's PASS and the resolutions of R-0622 and R-1029,
resolves R-0892 by the evidence F268 and amend0920-selfuse-real landed
(T014), and lands T017: a self-improvement attempt stops `blocked` at
the removed candidate route instead of waiting for nothing (R-0866),
DECISION F282 D8.

## Next Steps

1. T018, the parallel-run flakes: R-0950, R-1028 and R-0499, each
   failing node captured first.
2. T019 in the closure's consolidation pass, then the closure sequence,
   whose self-use run is R-1008's only proof.

## Risks

T018 may not fit one round; what does not fit is carried by name to the
next paydown feature at this closure.
