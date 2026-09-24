# Plan — F265 Teacher learning UI v1 (post-task lessons)

Branch: feature/f265-teacher-learning-ui, cut from `main` at `0236e3c3`,
the merge commit of pull request 271 (F264 Steering channel).

## Goal

After every completed task, a lesson the teacher writes from the task's
real diff, stored per Run under the teacher's own model and budget pot,
and read in a learning overlay over the cockpit with an index, next and
previous navigation and a Commands mode
(`docs/roadmap/features/T5_F265.md`). Open findings at the claim: 3, all
owned by F284; this claim registers R-1046, owned by F284 as well.

## Current Step

ROUND 1: claim F265, re-head the live review record, record DECISION F265
D1 and operator question Q1, and land T001's substance:
`packages/orchestration/lessons.py`, the sealed lesson per Run built from
that Run's own diff inside the teacher's pot, and the hook in `run_job`
that writes one after every applied task while `teacher.lessons` is on,
with its tests and red proofs.

## Next Steps

1. T001's reach: the lesson announced on the job's event stream, a
   read-only route listing a job's lessons, and `remedy do`'s mission path
   proved end to end.
2. T002: the overlay, an index on the left and the lesson with next and
   previous, rendering stored lessons only.
3. T003: the Commands mode over the catalog entries the diff touched.
4. The closure sequence.

## Risks

A lesson spends one model call per task; the off switch and the pot are
the controls, and a test pins each.
