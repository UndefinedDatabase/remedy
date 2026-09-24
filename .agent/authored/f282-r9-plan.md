# Plan — F282 Findings paydown v2

Branch: feature/f282-findings-paydown-v2, cut from `main` at
`b8fa02ba`, the merge commit of pull request 269 (amend0923-selfuse-write).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F282.md`). The open set at the claim is 30 by
distinct id, and the feature file lists every one under a slice.

## Current Step

ROUND 9 books round 8's PASS and the resolution of R-0866, and lands
T018: the runtime cleanup scans match a temporary path as a path, so a
parallel worker no longer counts a sibling's live runtimes as its own
(R-1028), and the real-run identity test freezes Remedy's own checkout
(R-0950's first group), DECISION F282 D9. R-0499 and R-0950's zombie
node are carried.

## Next Steps

1. The closure sequence: book round 9, T019's checklist consolidation
   pass for R-0662, R-0819 and R-0820, the one full suite, the self-use
   run that is R-1008's only proof, and the carry of what stays open.

## Risks

The closure suite may list bad nodes this feature must repair first.
