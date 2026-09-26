# Plan — F289 Self-use sources completion

Branch: feature/f289-self-use-sources, cut from `main` at `d0239fa3`,
the merge commit of pull request 283 (F027 Task veto).

## Goal

A closure's self-use run has real work when the finding ledger is empty:
the generator's Tier 2 checks documents against shipped truth, and its
Tier 3 turns an actionable `remedy doctor core` warning into a one-task
job (`docs/roadmap/features/T5_F289.md`).

## Current Step

ROUND 3: book round 2, register and repair R-1074, record DECISION F289
D3, and land T003 — three consecutive generator calls on an empty ledger
produce three distinct items, and the first runs to completion under the
fake providers inside the self-use run's default budget.

## Next Steps

1. The closure sequence: the integration gate's one full suite, then the
   evidence bundle and the review package with the Built State, then the
   closing round.

## Risks

None open. Open findings: 1 (R-1074, repaired this round).
