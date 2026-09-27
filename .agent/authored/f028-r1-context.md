# Context — F028 Task injection

## Active Branch
feature/f028-task-injection, cut from `main` at `ceb90b8a`
(the merge commit of pull request 286, F288 Event stream completeness).

## Scope
F028 (Tier 5): the Add Task button as real additive control — a planner
draft of the operator's task text with placement, rationale, budget check
and fence flags, applied to the running job only on confirmation, with
provenance end to end, as `docs/roadmap/features/T5_F028.md` and DECISION
F028 D1 specify.

## Do not touch
The approval machinery (reused, not duplicated), the fence rules, and the
DoD compile internals.

## Active assumptions
- A running job's `job.json` is written only by its runner; an injection
  reaches it as a create-only control file (DECISION F028 D1).
- Placement is computed by code and always appends at the end of the plan.

## Constraints
- Every pytest run in a round is targeted and serial; the resource and
  pytest budgets of `tests/regression/test_resource_safety.py` apply.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
