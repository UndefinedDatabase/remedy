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

ROUND 6, T003's SECOND PART: book round 5's PASS, record DECISION F023
D6, and land the deep link (`zoomDeepLink.ts`, `useZoomDeepLink.ts`),
cluster expansion at the focused task (`clusterExpansion.ts` through
`buildBrainLayout`), the camera that waits for the canvas, and the
guard `tests/ui_contracts/test_zoom_deep_link_wiring.py`.

## Next Steps

1. T003's last part: the 500-node performance fixture driven through
   every zoom level with its numbers recorded, and the live end-to-end.
2. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

The performance fixture runs in headless Chrome, which paces frames at
60 Hz, so it shows no dropped frame rather than headroom. Open
findings: 1, owned by F285.
