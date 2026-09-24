# Context — F019 Live node materialization

## Active Branch
feature/f019-live-node-materialization, cut from `main` at `92b7f5f1`
(the merge commit of pull request 274, F015 Interactive plan editing).

## Scope
F019 (Tier 5): the brain graph materializes live — a pure reducer from the
stream's frames to the graph ontology (T001), rendering on
react-force-graph-2d at the design reference's bar (T002), and the live
wiring with gap and snapshot recovery and the performance fixture (T003),
as `docs/roadmap/features/T5_F019.md` specifies, with
`docs/ui/design_reference/graph_spec.md` and `graph_tech_recommendation.md`
authoritative on conflict.

## Do not touch
The glyph and state visual language (the next feature), zoom mechanics,
and the event schema. No renderer dependency is added (stage decision).

## Active assumptions
- The reducer reads the envelope the server really writes, a run node is
  keyed by the frame that birthed it, and the task ring is born from the
  dashboard's task list (DECISION F019 D1).
- `buildForceBrainModel.ts` stays the single builder of force-graph data.

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
