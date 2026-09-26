# Plan — F289 Self-use sources completion

Branch: feature/f289-self-use-sources, cut from `main` at `d0239fa3`,
the merge commit of pull request 283 (F027 Task veto).

## Goal

A closure's self-use run has real work when the finding ledger is empty:
the generator's Tier 2 checks documents against shipped truth, and its
Tier 3 turns an actionable `remedy doctor core` warning into a one-task
job (`docs/roadmap/features/T5_F289.md`).

## Current Step

ROUND 4, the closure sequence's first round: book round 3 and R-1074's
resolution, consolidate the checklist, and generate and run the
closure's self-use item on the `self_use` role, recording its readings.

## Next Steps

1. Land the self-use run's diff if the reviewer passes it, write the
   Built State, and take the feature's one full suite.
2. The evidence bundle and the review package.
3. The closing round: rotation, STATUS, README pins, pull request.

## Risks

A self-use run that blocks is an outcome to record, not a stop. Open
findings: 0.
