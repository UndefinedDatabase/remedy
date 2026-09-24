# Plan — F282 Findings paydown v2

Branch: feature/f282-findings-paydown-v2, cut from `main` at
`b8fa02ba`, the merge commit of pull request 269 (amend0923-selfuse-write).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F282.md`). The open set at the claim is 30 by
distinct id, and the feature file lists every one under a slice.

## Current Step

ROUND 12, the closure's evidence half: book round 11, whose repaired
suite is green, then build the evidence bundle against the fork point
and the fresh review package, recording its name, its SHA-256 and the
directory it ends up in.

## Next Steps

1. The closing round: the ledger rotation, the ownership step for
   R-0499, R-0950 and R-1008, the next paydown's registration, the
   STATUS line with the README counters, and the pull request.

## Risks

A package that does not read READY_FOR_REVIEW blocks the closure until
its cause is repaired.
