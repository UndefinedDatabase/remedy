# Context — F023 Semantic zoom L0–L3

## Active Branch
feature/f023-semantic-zoom-l0-l3, cut from `main` at `441f4e8e`
(the merge commit of pull request 277, F020 Node lifecycle & glyph
language).

## Scope
F023 (Tier 5): semantic zoom over the brain graph — the pure state
machine and its wheel adapter with goldens (T001), the render effects,
breadcrumbs and the L2 run popover (T002), and the L3 evidence panel,
deep links, cluster expansion and the performance fixture (T003), as
`docs/roadmap/features/T5_F023.md` specifies, with
`docs/ui/design_reference/graph_spec.md` §10 authoritative on conflict.

## Do not touch
The stage decision, the reducer and ontology, the glyph language, and
the chat backend.

## Active assumptions
- The machine is pure in `semanticZoom.ts` and the hysteresis lives in
  `zoomWheel.ts`; focus is validated against the reducer's model plus
  its cluster view (DECISION F023 D1).

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
