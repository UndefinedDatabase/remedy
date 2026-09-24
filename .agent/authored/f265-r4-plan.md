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

ROUND 4: book round 3's PASS, record DECISION F265 D4, and land T003: the
overlay's Commands mode, the commands whose handler module or catalog
line the task's diff changed, each with the catalog's shipped
description, computed from the stored diff whenever the lessons route is
read, with tests, contract pins and red proofs. T001 to T003 are then
built.

## Next Steps

1. The closure sequence: Built State and the user guide, the checklist
   consolidation, self-use, the one full suite, the evidence package, the
   bookings, the ledger rotation, the STATUS flip and the pull request.

## Risks

A lesson spends one model call per task; the off switch and the pot are
the controls, and a test pins each. The overlay has no focus trap, which
the assumption log records.
