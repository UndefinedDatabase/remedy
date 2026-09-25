# Plan — F023 Semantic zoom L0–L3

Branch: feature/f023-semantic-zoom-l0-l3, cut from `main` at `441f4e8e`,
the merge commit of pull request 277 (F020 Node lifecycle & glyph
language).

## Goal

One mental model from organism to evidence: a zoom state machine
{level, focusId} drives L0 to L3 through wheel thresholds with
hysteresis, clicks, breadcrumbs and Escape, with cluster expansion and
the stage-1 performance budget (`docs/roadmap/features/T5_F023.md`).

## Current Step

ROUND 1: claim F023, re-head the live review record, book F020's round
8, record DECISION F023 D1, and land T001: `semanticZoom.ts`, the pure
machine with its whole transition matrix goldened, `zoomWheel.ts`, the
wheel adapter holding the hysteresis, and the guard
`tests/ui_contracts/test_semantic_zoom_contract.py`.

## Next Steps

1. T002: the `useSemanticZoom.ts` hook driving the canvas, the render
   effects (sibling dimming, branch glow, run fan-out), the breadcrumbs
   and Escape, then the L2 run popover and its buttons.
2. T003: the L3 evidence panel with lazy tabs, deep links, cluster
   expansion, the 500-node performance fixture and the live end-to-end.
3. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

Per-run tokens and duration have no read route yet; T002 inventories the
endpoints and orders any thin route as a named prerequisite. Open
findings: 1, owned by F285.
