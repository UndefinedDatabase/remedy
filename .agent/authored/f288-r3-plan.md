# Plan — F288 Event stream completeness & prompt nodes in the live graph

Branch: feature/f288-event-stream-completeness, cut from `main` at
`db691093`, the merge commit of pull request 285 (F289 Self-use sources).

## Goal

Every builder, review, check, test and repair event the browser receives
carries the attempt id, the task id and the result; a plan-approved event
exists; and the live graph draws test-run, repair and prompt nodes
(`docs/roadmap/features/T5_F288.md`).

## Current Step

ROUND 3: book round 2's PASS, register R-1075, record DECISION F288 D3,
give the long-run cycle's repair events their attempt id and result, land
T002 — the stream's rows carry the attempt id and the approved task ids,
and the live graph's reducer births tasks at plan approval, test runs and
repair runs — and repair R-1075 by re-capturing the demo recording.

## Next Steps

1. T003: the prompt node kind, its look, and its mouse and keyboard reach.
2. The closure sequence.

## Risks

Every golden in `brainReducer.fixtures.ts` must stay byte-identical: a
run's meta gains `attemptId` only when its row carries one. Open findings: 1 (R-1075,
repaired this round).
