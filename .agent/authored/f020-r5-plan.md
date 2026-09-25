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

ROUND 5, T003's second half: book round 4's PASS, record DECISION F020
D5, and land the conformance probes over the matrix fixture's pixels, the
headless harness that reads them, and its transcript as evidence.

## Next Steps

1. The closure sequence: the Built State, the checklist consolidation,
   the self-use track and the one full suite.
2. The evidence bundle and the review package.
3. The closing round: the ledger rotation, the STATUS flip and the pull
   request.

## Risks

The harness needs Chrome and the UI toolchain, so it runs as a tool, not
in the suite; F044 owns its CI stage. Open findings after this round: 1,
owned by F285.
