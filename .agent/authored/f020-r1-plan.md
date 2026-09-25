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

ROUND 1: claim F020, re-head the live review record with F284's round 4
verdict, record DECISION F020 D1, and land T001 — `glyphPaths.ts` and
`nodeStates.ts` under `apps/ui/src/components/graph/renderers/`, their
vitest tests, the two tokens they need, and the token guard.

## Next Steps

1. T002: the canvas painter reads both modules in place of F019's glyph
   slots through the palette bridge `renderers/palette.ts`, the legend is
   generated from the same source, and the matrix fixture.
2. T003: transition and pulse motion with visibility pausing, the
   conformance assertions and the live fixture pass.
3. The closure sequence.

## Risks

The veto is drawn by no reducer yet, so its treatment is proved by the
matrix fixture alone. Open findings after this round: 1, owned by F285.
