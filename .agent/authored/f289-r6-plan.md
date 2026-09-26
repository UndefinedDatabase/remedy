# Plan — F289 Self-use sources completion

Branch: feature/f289-self-use-sources, cut from `main` at `d0239fa3`,
the merge commit of pull request 283 (F027 Task veto).

## Goal

A closure's self-use run has real work when the finding ledger is empty:
the generator's Tier 2 checks documents against shipped truth, and its
Tier 3 turns an actionable `remedy doctor core` warning into a one-task
job (`docs/roadmap/features/T5_F289.md`).

## Current Step

ROUND 6, the closure sequence's evidence round: book round 5, build the
evidence bundle at the accepted head, and build the review package.

## Next Steps

1. The closing round: book round 6, rotate the ledger, set SU-033's
   `consumed_by`, accept F289 in STATUS with its README pins, and open
   the pull request.

## Risks

None open. Open findings: 0.
