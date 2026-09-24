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

ROUND 2: book round 1's PASS, record DECISION F265 D2, and land T001's
reach: a stored lesson announced on the job's run log as
`task_lesson_written`, the stream's `lesson` field naming its Run and
status, `GET /api/jobs/<job_id>/lessons` listing every task's lesson or
the reason it has none, and the hook naming the job's mission, with tests
and red proofs.

## Next Steps

1. T002: the overlay, an index on the left and the lesson with next and
   previous, reading the lessons route when the stream announces one.
2. T003: the Commands mode over the catalog entries the diff touched.
3. The closure sequence.

## Risks

A lesson spends one model call per task; the off switch and the pot are
the controls, and a test pins each. The overlay binds
`docs/ui/design_reference`, which T002 reads before it builds.
