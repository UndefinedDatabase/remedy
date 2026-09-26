# Plan — F288 Event stream completeness & prompt nodes in the live graph

Branch: feature/f288-event-stream-completeness, cut from `main` at
`db691093`, the merge commit of pull request 285 (F289 Self-use sources).

## Goal

Every builder, review, check, test and repair event the browser receives
carries the attempt id, the task id and the result; a plan-approved event
exists; and the live graph draws test-run, repair and prompt nodes
(`docs/roadmap/features/T5_F288.md`).

## Current Step

ROUND 2: book round 1's PASS, record DECISION F288 D2, and land the
second half of T001's writers — the run-next path's attempt id, the test
service's attempt id, task id and result, and the `plan_approved` event
with its `plan` block in the stream's envelope.

## Next Steps

1. The long-run executor's repair events under their own ruling, and
   T002: the live graph's reducer draws test-run and repair nodes and the
   tasks born at plan approval.
2. T003: the prompt node kind, its look, and its mouse and keyboard reach.
3. The closure sequence.

## Risks

A failed `plan_approved` write must never undo a saved approval. Open
findings: 0.
