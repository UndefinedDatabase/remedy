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

ROUND 4: book round 3's PASS, record DECISION F024 D4, and land T003's
components: the one ledger and one scrubber in the shell, the bar as a
slider in `PhaseTimeline.tsx`, the stage drawing the scrubbed prefix
under a SCRUBBED banner, the REPLAY pill, LIVE's fast-forward in
`useTimelineScrub.ts`, and the guard
`tests/ui_contracts/test_timeline_scrub_wiring.py`.

## Next Steps

1. T003's end-to-end: a live fake job scrubbed to every position against
   a fresh fold, the demo recording as a scrubbable story, and the scrub
   budget on the 500-node fixture with its snapshot arithmetic.
2. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

No completion event exists, so Finalized is derived from the reducer's
task states (DECISION F024 D1). Open findings: 1, owned by F285.
