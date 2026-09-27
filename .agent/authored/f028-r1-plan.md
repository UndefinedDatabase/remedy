# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 1: claim F028, re-head the live review record, book F288's round
10, record DECISION F028 D1, and land T001 — the draft pass of an
injection in `packages/orchestration/task_injection.py` and its tests.

## Next Steps

1. T002: the confirmation — the runner folds a confirmed injection into
   a running job, the plan's edit log gains the add, the task carries its
   provenance, one event with its readers, and the shortfall seed's three
   answers.
2. T003: `remedy job inject`, the browser's command, the Add Task sheet,
   the provenance chip, and the end-to-end proof.
3. The closure sequence.

## Risks

A running job's record is written only by its runner. Open findings: 0.
