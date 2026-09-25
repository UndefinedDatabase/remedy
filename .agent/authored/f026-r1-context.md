# Context — F026 Task edit at runtime

## Active Branch
feature/f026-task-edit-runtime, cut from `main` at `90555849`
(the merge commit of pull request 280, F025 Pause/resume).

## Scope
F026 (Tier 5): editing a task at runtime — the state gate, the versioned
apply, the spec archive and the revalidation (T001), the write-channel
command with its audit, the failed-to-pending semantics and the
prompt-trace proof on a fake run (T002), and the version chip, the
popover's version list, the edit affordance and the end-to-end (T003), as
`docs/roadmap/features/T5_F026.md` specifies, with
`docs/ui/design_reference/` authoritative on the visuals.

## Do not touch
Clarification immutability, attempt semantics beyond the reset, and
subtree rerun mechanics.

## Active assumptions
- A runtime edit is the plan editor's `plan_edit_task` on one task of an
  approved plan while no run holds the record; the task entry is updated
  in place with a spec version, the prior spec is archived, the approval
  seal follows the edit, and a failed task returns to pending with the
  tasks its block skipped (DECISION F026 D1).

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
