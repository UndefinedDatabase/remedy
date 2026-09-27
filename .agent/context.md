# Context — F029 Subtree rerun

## Active Branch
feature/f029-subtree-rerun, cut from `main` at `b2863af4`
(the merge commit of pull request 287, F028 Task injection).

## Scope
F029 (Tier 5): a rerun from a task in the middle of a job — the task and
its downstream reset to pending, their files restored to the state before
the task with a hash proof, earlier attempts kept as evidence in an
attempt fan, the command gated by the cost preview, and an optional model
override recorded — as `docs/roadmap/features/T5_F029.md` and DECISION
F029 D1 specify.

## Do not touch
Checkpoint semantics, applicator internals beyond the commit seam, and
the routing policy (an override is disclosure, not policy).

## Active assumptions
- A task applied in worktree mode has one commit on the job branch; the
  first parent of that commit is the state before the task (DECISION
  F029 D1).
- A reset is a new commit; no commit of an earlier attempt is rewritten.

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
