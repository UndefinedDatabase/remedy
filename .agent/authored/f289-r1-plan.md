# Plan — F289 Self-use sources completion

Branch: feature/f289-self-use-sources, cut from `main` at `d0239fa3`,
the merge commit of pull request 283 (F027 Task veto).

## Goal

A closure's self-use run has real work when the finding ledger is empty:
the generator's Tier 2 checks documents against shipped truth, and its
Tier 3 turns an actionable `remedy doctor core` warning into a one-task
job (`docs/roadmap/features/T5_F289.md`).

## Current Step

ROUND 1: claim F289, re-head the live review record, book F027's round
14, register and repair R-1073, record DECISION F289 D1, and land T002 —
`doctor_core_report()` returning structured warnings, the command
printing from it unchanged, and the generator's Tier 3.

## Next Steps

1. T001: the documentation-staleness catalog of at least ten checks,
   each proven red on a stale fixture, and the generator's Tier 2.
2. T003: three consecutive generator calls on an empty ledger produce
   three distinct items, and one runs to completion under the test
   provider inside the default cost cap.
3. The closure sequence.

## Risks

The command's output must stay byte-identical while its body moves into
a function. Open findings: 1 (R-1073, repaired this round).
