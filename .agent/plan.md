# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 9, the closure sequence's first half. It books round 8's PASS and
resolves R-1037 and R-1038, writes the feature file's Built State, folds this
feature's two prose lessons into the reviewer checklist without lengthening
it, runs the closure's self-use item to its approval gate, and runs the
feature's one full suite, committing the transcript.

## Next Steps

1. The closure sequence's second half: register whatever the self-use run's
   own defect reader reports, the evidence job and a fresh review zip.
2. The closing round: the ledger rotation, the STATUS line with the README
   counters in the same commit, and the pull request, which is never merged
   in the session that opens it.

## Risks

Twenty-six findings are open after this round's resolutions and none is this
feature's own. Nine rounds are spent of the soft limit of 25.
