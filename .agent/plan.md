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
| T001 wire the highlighting | done | `678bc698`, `8bcff3db`, DECISIONS D1 D2 |
| T003 rule on the sidebar's treatment | done | `1b70fb02`, DECISION F256 D3 |
| T002 measure, server half | done | `4aea7ba2`, DECISION F256 D4 |
| T002 measure, client half | done | `95ecaf14`, DECISIONS F256 D5 D6 |
| T002 record the numbers | done | this round |
| the integration gate | open | next round |
| the closure sequence | open | needs two rounds |

## Next Steps
1. Run the integration gate over the whole branch.
2. Build the closure evidence and the review zip.
3. Commit the STATUS closure in a round of its own, per the closure protocol.

## Risks
- The closure sequence needs TWO rounds — evidence and zip, then the STATUS
  commit — and a STATUS `[x]` flip needs its README and ledger pins in the same
  commit or `tests/docs/` goes red.
- `.agent/candidates.md` is empty and must stay empty through closure.
