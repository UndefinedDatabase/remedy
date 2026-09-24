# Context — F284 Findings paydown v3

## Active Branch
feature/f284-findings-paydown-v3, cut from `main` at `a36a8759`
(the merge commit of pull request 275, F019 Live node materialization).

## Scope
F284 (Tier 2): the rolling findings paydown, v3. The four open findings it
owns — R-0499, R-0950, R-1008 and R-1046 — are repaired by the slices
`docs/roadmap/features/T2_F284.md` lists, each finding's text being its
spec (DECISION F284 D1).

## Do not touch
The resolutions earlier paydowns landed; the record is append-only.

## Active assumptions
- One helper, `teacher_role_overrides`, reads `teacher.model` for every
  teacher call (DECISION F284 D1).
- R-0499's node is the one a controlled reproduction named (DECISION F284
  D1).

## Constraints
- UI checks run through the pytest nodes that wrap the toolchain in the
  primary checkout: eslint in `tests/ui_contracts/test_ui_lint.py`, tsc in
  `tests/ui_server/test_dashboard_contract.py`, and vitest in
  `tests/orchestration/test_test_runner.py`.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
