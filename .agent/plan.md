# Plan — F288 Event stream completeness & prompt nodes in the live graph

Branch: feature/f288-event-stream-completeness, cut from `main` at
`db691093`, the merge commit of pull request 285 (F289 Self-use sources).

## Goal

Every builder, review, check, test and repair event the browser receives
carries the attempt id, the task id and the result; a plan-approved event
exists; and the live graph draws test-run, repair and prompt nodes
(`docs/roadmap/features/T5_F288.md`).

## Current Step

ROUND 3 landed (C1-C6, C5b): booked round 2's PASS, recorded DECISION F288
D3, gave the long-run cycle's repair events their attempt id and result,
landed T002, and repaired R-1075 by re-capturing the demo recording. G4's
full-suite gate is RED: the re-capture shifted the recording's job/task ids
and frame count, and four vitest files outside this round's tracked path
set — `renderers/stateMotion.test.ts`, `timeline/timelineView.test.ts`,
`timeline/timelineIndex.test.ts`, `graph/brainLedger.test.ts` — hard-code the
OLD recording's ids/seq positions and now fail (8 tests). Awaiting the
reviewer's ruling before round 4.

## Next Steps

1. The reviewer's disposition of the four newly-red vitest files.
2. T003: the prompt node kind, its look, and its mouse and keyboard reach.
3. The closure sequence.

## Risks

Every golden in `brainReducer.fixtures.ts` must stay byte-identical: a
run's meta gains `attemptId` only when its row carries one. Open findings: 1
(R-1075, repaired this round) plus the newly-discovered vitest breakage
above, not yet minted as a finding by this worker.
