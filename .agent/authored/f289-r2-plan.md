# Plan — F289 Self-use sources completion

Branch: feature/f289-self-use-sources, cut from `main` at `d0239fa3`,
the merge commit of pull request 283 (F027 Task veto).

## Goal

A closure's self-use run has real work when the finding ledger is empty:
the generator's Tier 2 checks documents against shipped truth, and its
Tier 3 turns an actionable `remedy doctor core` warning into a one-task
job (`docs/roadmap/features/T5_F289.md`).

## Current Step

ROUND 2: book round 1 and R-1073's resolution, record DECISION F289 D2,
and land T001 — `packages/orchestration/doc_staleness.py` with its
twelve checks, each proven red on a stale fixture, and the generator's
Tier 2.

## Next Steps

1. T003: three consecutive generator calls on an empty ledger produce
   three distinct items, and one runs to completion under the test
   provider inside the default cost cap.
2. The closure sequence.

## Risks

A check that misreads a document reports a claim that is not stale, and
a self-use run would then edit a correct document. Open findings: 0.
