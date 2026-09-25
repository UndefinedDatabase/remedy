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

ROUND 1: claim F024, re-head the live review record, book F023's round
10, record DECISION F024 D1, and land T001: `phaseMapping.ts`, the phase
mapping table over the measured writers, the boundaries of any prefix
and the sub-glyph extraction, goldened on fixture ledgers and the demo
recording, with the guard `tests/ui_contracts/test_phase_mapping.py`.

## Next Steps

1. T002: snapshot memoization every 200 seq with its memory cap and
   lazy rebuild, and the property test that the state at any fuzzed
   position equals a fresh reduction of that prefix.
2. T003: the bar, scrubber, LIVE toggle, SCRUBBED banner, capped
   catch-up and keyboard, and the end-to-end on a live fake job and the
   demo recording.
3. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

No completion event exists, so Finalized is derived from the reducer's
task states (DECISION F024 D1). Open findings: 1, owned by F285.
