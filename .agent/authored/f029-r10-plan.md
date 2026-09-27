# Plan — F029 Subtree rerun

Branch: feature/f029-subtree-rerun, cut from `main` at `b2863af4`, the
merge commit of pull request 287 (F028 Task injection).

## Goal

"Do that part again" is safe and cheap: a rerun from a task in the middle
of a job resets that task and everything depending on it, restores the
files they changed to their state before the task (proved by tree
hashes), keeps earlier attempts as evidence in an attempt fan, and may run
with a model override that the evidence records
(`docs/roadmap/features/T5_F029.md`).

## Current Step

ROUND 10, the closure's evidence round: book round 9's PASS, then build
the evidence bundle and the review package at the accepted head.

## Next Steps

1. The review of round 10.
2. The closing round: the ledger rotation, the STATUS line with the
   README counters, and the pull request.

## Risks

Open findings: none.
