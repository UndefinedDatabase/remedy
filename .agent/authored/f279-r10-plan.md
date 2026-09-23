# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 10 is the closure's evidence half. It books round 9's PASS and the
two flaky suite nodes as recurrences of R-0950 and R-1028, then builds the
evidence bundle against the fork point `c9bc5c20` and the fresh review
package over the accepted HEAD this round's booking commit becomes.

## Next Steps

1. The closing round: the ledger rotation, the STATUS line and the README
   counters in one commit with the self-use item's `consumed_by`, and the
   pull request.

## Risks

Hosted CI first runs the new install steps at the closure's pull request.
The closure is PASS_WITH_RISKS: two suite nodes are known flakes owned by
F282, and R-1040 and R-1041 are open and owned by F282.
