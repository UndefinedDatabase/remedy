# Context — F020 Node lifecycle & glyph language

## Active Branch
feature/f020-node-lifecycle-glyph-language, cut from `main` at `955a6240`
(the merge commit of pull request 276, F284 Findings paydown v3).

## Scope
F020 (Tier 5): the brain graph's glyph and state language — pure glyph
and state modules (T001), the canvas and the generated legend reading them
with the matrix fixture (T002), and the transition and pulse motion with
the conformance assertions (T003), as `docs/roadmap/features/T5_F020.md`
specifies, with `docs/ui/design_reference/graph_spec.md` §5 and
`assets_spec.md` §4 authoritative on conflict.

## Do not touch
The ontology and the reducer, zoom, and layout physics.

## Active assumptions
- Glyph geometry is stored once as SVG path strings and the canvas builds
  its Path2D from them; the state module names tokens only (DECISION F020
  D1).
- The veto's grey is the token `--remedy-state-vetoed` (DECISION F020 D1).

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
