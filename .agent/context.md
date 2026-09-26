# Context — F027 Task veto

## Active Branch
feature/f027-task-veto, cut from `main` at `557cbbcc`
(the merge commit of pull request 282, F285 Findings paydown v4).

## Scope
F027 (Tier 5, the operator cockpit): the task veto with a mandatory
reason, the unreachable downstream, the run continuing on independent
branches, the replan proposal with its two-option menu, the strike on
the page and the diamond end-to-end, as
`docs/roadmap/features/T5_F027.md` and DECISION F027 D1 specify.

## Do not touch
Mid-run replanning mechanics, DAG internals (`dag_schedule.py`) and
glyph geometry, per T5_F027.md; the kill switch's `safe_points.py` and
the pause's `pause_control.py`.

## Active assumptions
- A veto is a create-only control file per task; the command never
  writes the job record, and a runner folds the veto at its safe points
  (DECISION F027 D1).
- Nothing replans without the decision answer.

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
