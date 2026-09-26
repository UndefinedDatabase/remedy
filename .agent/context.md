# Context — F289 Self-use sources completion

## Active Branch
feature/f289-self-use-sources, cut from `main` at `d0239fa3`
(the merge commit of pull request 283, F027 Task veto).

## Scope
F289 (Tier 5): the self-use generator's Tier 2, a documentation-staleness
catalog of at least ten checks over the README, the guides and the command
catalog, and its Tier 3, `remedy doctor core`'s actionable warnings as
one-task jobs, with the proof that three consecutive generator calls on an
empty ledger produce three distinct items, as
`docs/roadmap/features/T5_F289.md` and DECISION F289 D1 specify.

## Do not touch
Tier 1 (the finding ledger) and the standing order's precedence; the deny
fence over `.agent/` a self-use run carries (DECISION
amend0926-decisions-selfuse D4).

## Active assumptions
- `doctor core`'s text and JSON output stay byte-identical while its body
  moves into `doctor_core_report()` (DECISION F289 D1).
- A warning is actionable only when a tracked file of this repository is
  its repair.

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
