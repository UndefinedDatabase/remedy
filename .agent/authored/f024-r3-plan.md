# Plan — F024 Phase timeline with scrubber

Branch: feature/f024-phase-timeline-scrubber, cut from `main` at
`1bb3a35d`, the merge commit of pull request 278 (F023 Semantic zoom
L0–L3).

## Goal

Time becomes navigable: a phase bar derived from the ledger's own
events, sub-glyphs at their seq, and a scrubber that renders exactly the
reducer state of any prefix from memoized snapshots, with a LIVE toggle
that returns to the present (`docs/roadmap/features/T5_F024.md`).

## Current Step

ROUND 3: book round 2's PASS, record DECISION F024 D3, and land T003's
pure half: `timelineIndex.ts`, every prefix's phases from one fold;
`scrubState.ts`, the scrubber machine with its keyboard and LIVE's
capped catch-up; `timelineView.ts`, the bar's view model; and the guard
`tests/ui_contracts/test_timeline_scrub_contract.py`.

## Next Steps

1. T003's components: the bar and scrubber in `PhaseTimeline.tsx`, the
   ledger and scrub state lifted into the shell, the graph rendering the
   scrubbed prefix, the SCRUBBED banner and the REPLAY pill.
2. T003's end-to-end on a live fake job and the demo recording, with
   the scrub budget on the 500-node fixture.
3. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

No completion event exists, so Finalized is derived from the reducer's
task states (DECISION F024 D1). Open findings: 1, owned by F285.
