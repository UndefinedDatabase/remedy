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

ROUND 5: book round 4's PASS, record DECISION F024 D5, and land T003's
end-to-end: the live fake job scrubbed at every position by the real
modules (`scrubLive.test.ts` driven by
`tests/ui_server/test_timeline_scrub_live.py`), the fixture's ledger
export, and the scrub budget on the 500-node fixture, measured and
committed as evidence with its red control.

## Next Steps

1. The closure sequence's first half: the Built State, the one full
   suite, the self-use track and the checklist consolidation.
2. The closure's evidence half and its closing round: the evidence
   package, the ledger rotation, the STATUS flip and the pull request.

## Risks

No completion event exists, so Finalized is derived from the reducer's
task states (DECISION F024 D1). Open findings: 1, owned by F285.
