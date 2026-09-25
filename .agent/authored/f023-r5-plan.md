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

ROUND 5, T003's FIRST PART: book round 4's PASS, record DECISION F023
D5, and land the L3 evidence panel: `EvidencePanel.tsx` with the
binding CSS, its tabs from `evidencePanel.ts` loading only the open
one, the run detail's Open diff and Why moved onto its tabs, the zoom
surfaces on layer tokens, and the guard
`tests/ui_contracts/test_evidence_panel_contract.py`.

## Next Steps

1. T003: deep links that restore the zoom state, and cluster expansion
   at the focused task with focus following into it.
2. T003: the 500-node performance fixture with its numbers recorded,
   and the live end-to-end.
3. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

The implementation plan says the app keeps no URL router; the deep
links must restore state without one. Open findings: 1, owned by F285.
