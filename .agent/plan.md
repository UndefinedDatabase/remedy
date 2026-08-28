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
| T001 wire the highlighting | done | DECISIONS F256 D1 and D2 |
| T003 rule on the sidebar's treatment | done | DECISION F256 D3 |
| T002 measure and record, both halves | done | `f6d5d064`, D4 D5 D6 |
| the integration gate | done | this round, full suite |
| the evidence bundle and the package | done | this round |
| the STATUS closure commit | open | next round, with the README sync |

## Next Steps
1. Author the STATUS line from the package name, SHA-256 and archived path this
   round recorded, and apply it with the README capability sync in ONE commit.
2. Open the closure PR per the AGENTS.md workflow; it is NOT merged this
   session — the gap is the operator's manual-review window.
3. Leave `.agent/candidates.md` empty unless the closure gate raises one.

## Risks
- The STATUS `[x]` flip and the README sync must land in the SAME commit or the
  ledger cross-check pin goes red.
- The closure commit is the last on the branch (Rule A4), with the single
  permitted successor DECISION amend0827 D2 names.
