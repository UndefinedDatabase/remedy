# Plan — F288 Event stream completeness & prompt nodes in the live graph

Branch: feature/f288-event-stream-completeness, cut from `main` at
`db691093`, the merge commit of pull request 285 (F289 Self-use sources).

## Goal

Every builder, review, check, test and repair event the browser receives
carries the attempt id, the task id and the result; a plan-approved event
exists; and the live graph draws test-run, repair and prompt nodes
(`docs/roadmap/features/T5_F288.md`).

## Current Step

ROUND 1: claim F288, re-head the live review record, book F289's round 7,
record DECISION F288 D1, and land the first half of T001 — the attempt id
as the ping-pong run id, a test and a repair event per ping-pong round,
the attempt id in the stream's envelope, and the readers of the two new
event names.

## Next Steps

1. The second half of T001: the run-next path, the test service, the
   long-run repair events and the plan-approved event.
2. T002: the live graph's reducer draws test-run and repair nodes and the
   tasks born at plan approval.
3. T003: the prompt node kind, its look, and its mouse and keyboard reach.
4. The closure sequence.

## Risks

Every frame outside the attempt kinds must stay byte-identical in the
stream. Open findings: 0.
