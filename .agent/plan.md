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

ROUND 2: book round 1's PASS, record DECISION F024 D2, and land T002:
`scrubSnapshots.ts`, the memo that serves the reducer state at any seq
from snapshots every 200 seq under a cap of 64, with the property test
that its state at fuzzed positions equals a fresh reduction of the
prefix, and the guard `tests/ui_contracts/test_scrub_snapshots.py`.

## Next Steps

1. T003: the bar reading the phase mapping and the memo, the scrubber
   with its keyboard, the LIVE toggle with the SCRUBBED banner and the
   capped catch-up, and the end-to-end on a live fake job and the demo
   recording.
2. The closure sequence: the one full suite, the evidence package and
   the STATUS flip.

## Risks

No completion event exists, so Finalized is derived from the reducer's
task states (DECISION F024 D1). Open findings: 1, owned by F285.
