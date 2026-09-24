# Plan — F020 Node lifecycle & glyph language

Branch: feature/f020-node-lifecycle-glyph-language, cut from `main` at
`955a6240`, the merge commit of pull request 276 (F284 Findings paydown
v3).

## Goal

Every node tells its truth at a glance: one glyph per kind and one state
language, drawn on the canvas and in the legend from a single source, with
state transitions animated per the motion tokens and a conformance fixture
over the whole kind-by-state matrix (`docs/roadmap/features/T5_F020.md`).

## Current Step

ROUND 8, THE CLOSING ROUND: book round 7's PASS, rotate the ledger,
accept F020 in STATUS with its README pins, and open the pull request.
T001, T002 and T003 are built; the package is READY_FOR_REVIEW.

## Next Steps

1. The next session's Open PR Gate merges this feature's pull request.
2. Rule A5 then claims the first unchecked feature in
   `docs/roadmap/STATUS.md`.

## Risks

The conformance harness needs Chrome and the UI toolchain, so it runs as
a tool; F044 owns its CI stage. Open findings: 1, owned by F285.
