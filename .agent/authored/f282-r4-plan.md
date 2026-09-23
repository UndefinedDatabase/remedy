# Plan — F282 Findings paydown v2

Branch: feature/f282-findings-paydown-v2, cut from `main` at
`b8fa02ba`, the merge commit of pull request 269 (amend0923-selfuse-write).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F282.md`). The open set at the claim is 30 by
distinct id, and the feature file lists every one under a slice.

## Current Step

ROUND 4 books round 3's PASS and the resolutions of R-1040 and R-1005, and
lands T006 and T007: a stopped self-use task keeps the reviewer's last
verdict and the default call ceiling clears the loop (R-1007), and a
timed-out provider call ends `provider_timeout` (R-1016, R-1027, R-1035,
DECISION F282 D4).

## Next Steps

1. T008 to T011: R-0999, R-1015, R-1034 and R-1000.
2. T012 to T018, then T019 in the closure's consolidation pass.
3. The closure sequence, whose self-use run is R-1008's only proof.

## Risks

T014, T015 and T018 may not fit one round each; what does not fit is
carried by name to the next paydown feature at this closure.
