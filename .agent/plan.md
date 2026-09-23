# Plan — amendment amend0923-selfuse-write

Branch: feature/amend0923-selfuse-write, cut from `origin/main` at
`64cffc44`, the merge commit of pull request 268 (F263's closure).

## Goal

Make the self-use track able to DELIVER — its builder gets a write tool,
its per-call timeout fits a real call, and an order file may declare the
budget it needs — and clean the repository root, so reviewer scratch can
neither sit there nor be packaged.

## Current Step

Parts 1 through 4 are done. R-1043, R-1044 and R-1045 are registered and
three older findings carry a new measured sentence; the self-use runner
asks for a write tool and ten minutes per call, an order file may declare
its own budget, the product default for the builder's write mode moved,
the four root leftovers are moved out, and the packer and the integrity
gate both refuse them now. What remains is Part 5: the gate selection,
`ruff`, `remedy integrity check`, one real package with its member check,
the `Done: R-0829` paragraph, the pull request and the merge.

## Next Steps

1. Part 5 — gates, a real package, the pull request and the merge.
2. Restore the original branch, which pull request 268's merge deleted,
   so the restore target is `main`.

## Risks

Part 2E changes a product default and Part 4.4 turns two lenient packer
tests into refusals; every test either touches is listed in the handback.
