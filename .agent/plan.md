# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 4: book round 3's PASS and resolve R-1077, record DECISION F028
D4, and land the command line — `remedy job inject`, `inject-confirm`
and `inject-answer` — with the `--yes` audit mark, the shared budget
and planner helpers, and the extension's amount computed at answer time.

## Next Steps

1. The browser's command for the three steps, the run-log event of a
   folded injection with every reader of its name, and the send module.
2. T003: the Add Task sheet, the provenance chip, and the end-to-end
   proof.
3. The closure sequence.

## Risks

A running job's record is written only by its runner. Open findings: 0.
