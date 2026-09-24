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

ROUND 3, T002's second half: book round 2's PASS, record DECISION F020
D3, and land the legend popover from the graph's chrome, generated from
the glyph and state modules, the cluster's count, and the kind-by-state
matrix fixture painted by the live painter.

## Next Steps

1. T003: transition and pulse motion with visibility pausing, the
   conformance assertions over the matrix fixture's pixels, and the live
   fixture pass on a streamed fake job.
2. The closure sequence.

## Risks

The veto is drawn by no reducer yet, so its treatment is proved by the
matrix fixture alone. Open findings after this round: 1, owned by F285.
