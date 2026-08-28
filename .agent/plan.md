# Plan — F256 Diff viewer completion

Branch: feature/f256-diff-viewer-completion, cut from `main` at `0e8ab5b4`.
F256 was claimed by Rule A5 as the first unchecked line of Package 1 in
`docs/roadmap/STATUS.md`.

## Goal
Finish the rendered diff viewer F037 shipped: highlighting actually rendered
rather than only modelled, the 10k-line budget measured and recorded, and the
file sidebar's visual treatment ruled by a named authority.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the per-line highlight model | done | `apps/ui/src/api/diffHighlight.ts` |
| the DiffView wiring and the derived palette | done | `678bc698` |
| make the lazy load real, repairing `R-0732` | done | `8bcff3db` |
| rule on the sidebar's treatment | done | `1b70fb02`, DECISION F256 D3 |
| measure the 10k fixture, server half | done | this round |
| measure the 10k fixture, client half | open | round 7, in vitest |
| record the numbers in the feature file | open | round 8 |

## Next Steps
1. Measure `buildDiffRowModels` and `diffRowWindowForViewport` over a 10k-row
   envelope in vitest, which is the client half of the same fixture.
2. Write all measured numbers into the Built State of
   `docs/roadmap/features/T5_F256.md`, which is what Acceptance asks for.
3. Run the integration gate, then the closure sequence.

## Risks
- A perf assertion that pins an absolute second count on a hosted runner is a
  report on machine speed; DECISION F256 D4 rules the ratio guard instead.
- The 10k measurement must be a real run against a real fixture; a budget is
  re-derived from a re-measured maximum and never raised by hand.
