# Plan — F024 Phase timeline with scrubber

Branch: feature/f024-phase-timeline-scrubber, cut from `main` at
`1bb3a35d`, the merge commit of pull request 278 (F023 Semantic zoom
L0–L3). Pull request 279 into `main` is open.

## Goal

Time becomes navigable: a phase bar derived from the ledger's own
events, sub-glyphs at their seq, and a scrubber that renders exactly the
reducer state of any prefix from memoized snapshots, with a LIVE toggle
that returns to the present (`docs/roadmap/features/T5_F024.md`). F024
is accepted in STATUS.

## Current Step

ROUND 9, a repair of pull request 279's hosted CI under the Open PR
Gate: the live scrub test removes vitest's colour escapes before it
reads the summary, so it passes where `CI` is set (R-1048). Test code
only; no production file.

## Next Steps

1. The reviewer gates this round, waits for the pull request's hosted CI
   on the pushed commit, and merges pull request 279 at the Open PR Gate
   when it is green.
2. The next feature's first commit books this round's verdict and
   resolves R-1048, then Rule A5 claims the next feature.

## Risks

Open findings: 2 — R-1008, owned by F285, and R-1048, owned by F024 and
repaired by this round.
