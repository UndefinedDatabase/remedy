# Context — F288 Event stream completeness & prompt nodes in the live graph

## Active Branch
feature/f288-event-stream-completeness, cut from `main` at `db691093`
(the merge commit of pull request 285, F289 Self-use sources).

## Scope
F288 (Tier 5): attempt id, task id and result on every builder, review,
check, test and repair event the UI server sends, a plan-approved event,
test-run and repair nodes and tasks born at plan approval in the live
graph's reducer, and prompts as a node kind of the live graph, as
`docs/roadmap/features/T5_F288.md` and DECISION F288 D1 specify.

## Do not touch
The simple view, which stays one click away; the graph's rule that it
never draws a node its data model does not hold.

## Active assumptions
- An attempt is one execution of a task, and its id is that execution's
  ping-pong run id (DECISION F288 D1).
- Every stream frame outside the attempt kinds stays byte-identical.

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
