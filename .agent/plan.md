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
| measure the 10k fixture, server half | done | `4aea7ba2`, DECISION F256 D4 |
| measure the 10k fixture, client half | done | this round |
| record the numbers in the feature file | open | next round |

## Next Steps
1. Write both halves' measured numbers into the Built State of
   `docs/roadmap/features/T5_F256.md`, which is what Acceptance asks for: a
   recorded measurement rather than a claim.
2. Run the integration gate.
3. Run the closure sequence, which needs two rounds — evidence and zip, then the
   STATUS commit.

## Risks
- A collapsed hunk emits no line rows, so a client benchmark built with the
  DEFAULT collapsed set measures two rows however large the fixture is.
- The client model costs about a millisecond with a threefold run-to-run spread,
  so a timing assertion there would measure the JIT; DECISION F256 D5 rules the
  exact bounded-window property instead.
