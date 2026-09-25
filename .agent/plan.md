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

ROUND 7, T003's LAST PART: book round 6's PASS, record DECISION F023
D7, and land the live end-to-end
`tests/ui_server/test_semantic_zoom_live.py`, the zoom's performance
tool kept as evidence under `.agent/authored/f023-r7-perf-*`, the
worker's own run of it at 500 nodes over every zoom level, and the
run detail's missing golden for a restarted task.

## Next Steps

1. The closure sequence's first half: the Built State, the checklist
   consolidation, the self-use track and the one full suite.
2. The closure sequence's evidence half: the evidence bundle and the
   review package.
3. The closing round: the ledger rotation, the STATUS flip with its
   README pins, and the pull request.

## Risks

Headless Chrome paces frames at 60 Hz, so the budget reading shows no
dropped frame rather than headroom. Open findings: 1, owned by F285.
