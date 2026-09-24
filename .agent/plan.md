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

ROUND 2, T002's first half: book round 1's PASS, record DECISION F020 D2,
and land the palette bridge `renderers/palette.ts` and the node painter
`renderers/paintNode.ts`, with `ForceBrainGraph.tsx` painting every
non-core kind through them, the state table's glyph ink, and the token
guard pinning that wiring.

## Next Steps

1. T002's second half: the legend popover from the graph's chrome,
   enumerated from the glyph and state modules, the cluster's count, and
   the kind-by-state matrix fixture.
2. T003: transition and pulse motion with visibility pausing, the
   conformance assertions and the live fixture pass.
3. The closure sequence.

## Risks

The veto is drawn by no reducer yet, so its treatment is proved by the
matrix fixture alone. Open findings after this round: 1, owned by F285.
