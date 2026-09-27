# Plan — F288 Event stream completeness & prompt nodes in the live graph

Branch: feature/f288-event-stream-completeness, cut from `main` at
`db691093`, the merge commit of pull request 285 (F289 Self-use sources).

## Goal

Every builder, review, check, test and repair event the browser receives
carries the attempt id, the task id and the result; a plan-approved event
exists; and the live graph draws test-run, repair and prompt nodes
(`docs/roadmap/features/T5_F288.md`).

## Current Step

ROUND 8: book round 7's PASS, land the self-use item SU-034's reviewed
diff, add the self-use run to the Built State, and run the one full suite
of the closure.

## Next Steps

1. Build the evidence bundle and the review package.
2. Rotate the ledger, accept F288 in STATUS with its README pins, consume
   the self-use item, and open the pull request.

## Risks

A red suite is repaired under the shrinking rule before the evidence.
Open findings: 0.
