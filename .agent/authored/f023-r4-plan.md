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

ROUND 4, T002's SECOND HALF: book round 3's PASS, record DECISION F023
D4, and land the L2 run detail: `runDetailModel.ts`, the words for each
run's verdict, round, tokens, duration and retries; `RunDetailPopover.tsx`
reading the rounds door, with Open diff, Why and a disabled Rerun; the
stage and shell wiring; and the guard
`tests/ui_contracts/test_run_detail_wiring.py`.

## Next Steps

1. T003: the L3 evidence panel with lazy tabs, Open diff and Why moved
   onto its tabs, and the deep links.
2. T003: cluster expansion at the focused task, the 500-node
   performance fixture with its numbers recorded, and the live
   end-to-end.
3. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

The run report keeps no reviewer tokens and only the latest run per
task. Open findings: 1, owned by F285.
