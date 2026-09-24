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

ROUND 4, T003's first half: book round 3's PASS, record DECISION F020 D4,
and land the state crossfade and completion ripple, the pulse, the frame
rule that stops drawing on a hidden page, the canvas wired to them, and
the replay of the demo recording's state changes.

## Next Steps

1. T003's second half: the conformance assertions over the matrix
   fixture's pixels, with the headless harness that reads them.
2. The closure sequence.

## Risks

The veto is drawn by no reducer yet, so its treatment is proved by the
matrix fixture alone. Open findings after this round: 1, owned by F285.
