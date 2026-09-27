# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 10, the closure sequence's first round: book round 9's PASS, add
the closure's consolidation paragraph to the checklist, write the Built
State, and generate and run the closure's self-use item to its approval
gate.

## Next Steps

1. Land the self-use item's reviewed diff and run the one full suite.
2. Build the evidence bundle and the review package.
3. Rotate the ledger, accept F028 in STATUS with its README pins, consume
   the self-use item, and open the pull request.

## Risks

The self-use run makes real provider calls within its default budget.
Open findings: 0.
