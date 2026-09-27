# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 9: book round 8's PASS and resolve R-1079, and land the end-to-end
proof — a task injected into a paused job through the live door and
through `remedy job inject --yes`, run in the same job, its origin shown
on the dashboard, in the stream and in the final report.

## Next Steps

1. The closure sequence: the checklist consolidation, the Built State,
   the one full suite, the self-use item, the evidence bundle and the
   review package, the ledger rotation, and the STATUS acceptance.

## Risks

None open beyond the closure's own. Open findings: 0.
