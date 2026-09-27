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

ROUND 9, the closure sequence's first round: book round 8's PASS, write
the Built State, consolidate the checklist, ask the self-use generator
for the closure's item, build the browser bundle, and take the feature's
one full suite on the tree that ships.

## Next Steps

1. The review of round 9.
2. The closure's evidence round: the evidence job and the review zip,
   with any repair the full suite requires.
3. The closing round: the ledger rotation, the STATUS line, the README
   counters and the pull request.

## Risks

Open findings: none.
