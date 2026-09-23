# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 9 is the closure's first repair round. It books round 8's PASS,
records the self-use run as a recurrence of R-1007, registers R-1040 and
R-1041, repairs the two guard tests the closure suite found red, and runs the
feature's one full suite again on the repaired tree, whose transcript
replaces round 8's at the same path.

## Next Steps

1. The evidence job and the review package, with the accepted HEAD.
2. The closing round: the ledger rotation, the STATUS line with the README
   counters in the same commit, and the pull request.

## Risks

`constraints.txt` (round 1) is F279's one declared oversize commit; no
second may follow. Hosted CI first runs the new install steps at the
closure's pull request. Under the shrinking rule this round must leave no
bad node and add none; at most two more repair rounds remain.
