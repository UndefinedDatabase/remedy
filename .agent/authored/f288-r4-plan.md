# Plan — F288 Event stream completeness & prompt nodes in the live graph

Branch: feature/f288-event-stream-completeness, cut from `main` at
`db691093`, the merge commit of pull request 285 (F289 Self-use sources).

## Goal

Every builder, review, check, test and repair event the browser receives
carries the attempt id, the task id and the result; a plan-approved event
exists; and the live graph draws test-run, repair and prompt nodes
(`docs/roadmap/features/T5_F288.md`).

## Current Step

ROUND 4, the repair of round 3: book round 3's FAIL, record DECISION F288
D4, and bring the four vitest files that read the demo recording or the
widened row to the new recording and row, by expectations derived again
by hand, so the vitest suite is green again (R-1075's remaining readers).

## Next Steps

1. T003: the prompt node kind, its look, and its mouse and keyboard
   reach, with R-1075's resolution booked.
2. The closure sequence.

## Risks

No production file changes this round, and no green expectation moves.
Open findings: 1 (R-1075, its remaining readers repaired this round).
