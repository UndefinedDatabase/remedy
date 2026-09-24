# Plan — F265 Teacher learning UI v1 (post-task lessons)

Branch: feature/f265-teacher-learning-ui, cut from `main` at `0236e3c3`,
the merge commit of pull request 271 (F264 Steering channel).

## Goal

After every completed task, a lesson the teacher writes from the task's
real diff, stored per Run under the teacher's own model and budget pot,
and read in a learning overlay over the cockpit with an index, next and
previous navigation and a Commands mode
(`docs/roadmap/features/T5_F265.md`). Open findings: 4, all owned by F284.

## Current Step

ROUND 3: book round 2's PASS, record DECISION F265 D3, and land T002: the
learning overlay, a right-anchored dialog sheet the right panel's
"Lessons" button opens, with the index on the left and the lesson with
previous and next, reading the lessons route through `api/lessons.ts` and
reading it again when the stream announces a lesson, with vitest, a
contract test, two assumption-log rows and red proofs.

## Next Steps

1. T003: the Commands mode, the catalog entries of the commands the
   task's diff touched, as a second mode of the overlay.
2. The closure sequence.

## Risks

A lesson spends one model call per task; the off switch and the pot are
the controls, and a test pins each. The overlay has no focus trap, which
the assumption log records.
