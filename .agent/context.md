# Context — F286 Findings paydown v5

## Active Branch
feature/f286-findings-paydown-v5, cut from `main` at `6ba1f4be`
(the merge commit of pull request 293, F039 Story/replay mode).

## Scope
F286 (Tier 2): the fifth rolling findings paydown — every open finding it
owns repaired by its own text, as `docs/roadmap/features/T2_F286.md` and
DECISION F286 D1 specify.

## Do not touch
The resolutions earlier paydowns landed; the record is append-only.

## Active assumptions
- R-1104 is the one id F286 owns, and its repair lands in the claiming
  round (DECISION F286 D1).

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
