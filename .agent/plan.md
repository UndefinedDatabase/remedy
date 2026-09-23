# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 8 opens the closure sequence. It books round 7's PASS, writes the
feature file's Built State, generates and runs the closure's self-use item
to its approval gate, and runs this feature's one full suite, committing
its transcript. Every slice, T001 to T004, has a PASS round.

## Next Steps

1. Register whatever the self-use run's defect list asks for, and repair
   every bad node the closure suite lists, under the shrinking rule.
2. The evidence job and the review package, with the accepted HEAD.
3. The closing round: the ledger rotation, the STATUS line with the README
   counters in the same commit, and the pull request.

## Risks

`constraints.txt` (round 1) is F279's one declared oversize commit; no
second may follow. Hosted CI first runs the new install steps at the
closure's pull request. The self-use item is the toolchain refresh order,
the first order the track has queued.
