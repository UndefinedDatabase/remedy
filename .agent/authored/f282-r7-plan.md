# Plan — F282 Findings paydown v2

Branch: feature/f282-findings-paydown-v2, cut from `main` at
`b8fa02ba`, the merge commit of pull request 269 (amend0923-selfuse-write).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F282.md`). The open set at the claim is 30 by
distinct id, and the feature file lists every one under a slice.

## Current Step

ROUND 7 books round 6's PASS and the resolutions of R-1004 and R-1045, and
lands T015 and T016: the UI lint parses TypeScript, finds one real hook
defect, repairs it and becomes a gate (R-0622), and session bootstrap
reads `.agent/decisions.md` by part (R-1029), DECISION F282 D7.

## Next Steps

1. T014 and T017: R-0892, the evidence package, and R-0866, the parked rail.
2. T018, the parallel-run flakes: R-0950, R-1028 and R-0499.
3. T019 in the closure's consolidation pass, then the closure sequence,
   whose self-use run is R-1008's only proof.

## Risks

T014 and T018 may not fit one round each; what does not fit is carried by
name to the next paydown feature at this closure.
