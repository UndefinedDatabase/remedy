# Plan — F282 Findings paydown v2

Branch: feature/f282-findings-paydown-v2, cut from `main` at
`b8fa02ba`, the merge commit of pull request 269 (amend0923-selfuse-write).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F282.md`). The open set at the claim is 30 by
distinct id, and the feature file lists every one under a slice.

## Current Step

ROUND 11, the closure suite's first repair round: book round 10 and the
resolutions of R-0662, R-0819 and R-0820; give each packer run of the
one red node its own archive stamp, DECISION F282 D11; and run the full
suite again, replacing the closure transcript.

## Next Steps

1. The evidence job and the review package over the repaired tree.
2. The closing round: the ledger rotation, the ownership step for
   R-0499, R-0950 and R-1008, the next paydown's registration, the
   STATUS line with the README counters, and the pull request.

## Risks

A second full suite may list a node the first did not; the repair rule
allows two more repair rounds before the xfail route.
