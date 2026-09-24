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

ROUND 7, the closure sequence's evidence half: book round 6's PASS, whose
one full suite is green, then build the evidence bundle against the fork
point and the fresh review package.

## Next Steps

1. The closing round: the ledger rotation, the STATUS flip with the
   README counters, and the pull request.

## Risks

The conformance harness needs Chrome and the UI toolchain, so it runs as
a tool; F044 owns its CI stage. Open findings: 1, owned by F285.
