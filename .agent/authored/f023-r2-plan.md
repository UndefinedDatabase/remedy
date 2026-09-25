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

ROUND 2: book round 1's PASS, record DECISION F023 D2, and land T002's
first half: `zoomView.ts`, the render effects as data, the
`useSemanticZoom.ts` hook with Escape and reconcile, the
`ZoomBreadcrumbs.tsx` chip, the live canvas painting the effects and
moving its camera per level, and the guard
`tests/ui_contracts/test_semantic_zoom_wiring.py`.

## Next Steps

1. T002's second half: the L2 run popover anchored to its node, its
   buttons wired to real endpoints or honestly marked not yet, after an
   inventory of the evidence endpoints.
2. T003: the L3 evidence panel with lazy tabs, deep links, cluster
   expansion, the 500-node performance fixture and the live end-to-end.
3. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

Per-run tokens and duration have no read route yet; the popover round
orders any thin route as a named prerequisite. Open findings: 1, owned
by F285.
