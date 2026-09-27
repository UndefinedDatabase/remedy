# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 2: book round 1's PASS and register R-1076, record DECISION F028
D2, repair R-1076, and land the first half of T002 — the confirmation,
the runner's fold at four points, the `plan_add_task` edit kind, the
provenance on the task entry and the edit log.

## Next Steps

1. The second half of T002: the shortfall seed's three answers, its
   labels as a mapping, and the run-log event with its readers.
2. T003: `remedy job inject`, the browser's command, the Add Task sheet,
   the provenance chip, and the end-to-end proof.
3. The closure sequence.

## Risks

A running job's record is written only by its runner. Open findings: 1
(R-1076, Low, repaired this round).
