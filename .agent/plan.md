# Plan — F288 Event stream completeness & prompt nodes in the live graph

Branch: feature/f288-event-stream-completeness, cut from `main` at
`db691093`, the merge commit of pull request 285 (F289 Self-use sources).

## Goal

Every builder, review, check, test and repair event the browser receives
carries the attempt id, the task id and the result; a plan-approved event
exists; and the live graph draws test-run, repair and prompt nodes
(`docs/roadmap/features/T5_F288.md`).

## Current Step

ROUND 9: book round 8's PASS, then build the evidence bundle and the
review package at the accepted head.

## Next Steps

1. Rotate the ledger, accept F288 in STATUS with its README pins, consume
   the self-use item, and open the pull request.

## Risks

A package that does not read READY_FOR_REVIEW blocks the closure.
Open findings: 0.
