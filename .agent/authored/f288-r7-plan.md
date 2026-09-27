# Plan — F288 Event stream completeness & prompt nodes in the live graph

Branch: feature/f288-event-stream-completeness, cut from `main` at
`db691093`, the merge commit of pull request 285 (F289 Self-use sources).

## Goal

Every builder, review, check, test and repair event the browser receives
carries the attempt id, the task id and the result; a plan-approved event
exists; and the live graph draws test-run, repair and prompt nodes
(`docs/roadmap/features/T5_F288.md`).

## Current Step

ROUND 7, the closure sequence's first round: book round 6's PASS, add the
closure's consolidation paragraph to the checklist, write the Built State,
and generate and run the closure's self-use item to its approval gate.

## Next Steps

1. Land the self-use item's reviewed diff and run the one full suite.
2. Build the evidence bundle and the review package.
3. Rotate the ledger, accept F288 in STATUS with its README pins, consume
   the self-use item, and open the pull request.

## Risks

The self-use run makes real provider calls within its default budget.
Open findings: 0.
