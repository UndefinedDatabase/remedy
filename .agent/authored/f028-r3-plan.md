# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 3: book round 2's PASS, resolve R-1076 and register R-1077, record
DECISION F028 D3, repair R-1077, and land the second half of T002 — the
shortfall seed's three answers, its labels as a mapping of sentences,
and the budget extension from the answer through the fold to the run.

## Next Steps

1. The run-log event of a folded injection with every reader of its
   name, and `remedy job inject` with its `--after` and `--yes`.
2. T003: the browser's command, the Add Task sheet, the provenance chip,
   and the end-to-end proof.
3. The closure sequence.

## Risks

A running job's record is written only by its runner. Open findings: 1
(R-1077, Low, repaired this round).
