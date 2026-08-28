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
| T002 measure and record both halves | done | D4, D5, D6, Built State |
| T003 rule on the sidebar's treatment | done | DECISION F256 D3 |
| the integration gate and the package | done | READY_FOR_REVIEW at `c6775b3c` |
| resolve `R-0732` | done | this round |
| the STATUS closure and the PR | done | this round |

## Next Steps
1. The closure PR is NOT merged this session; it merges at the next feature's
   start through the Open PR Gate, which is the operator's review window.
2. The next feature by Rule A5 is F257 — Self-use track, the first unchecked
   STATUS line after F256.
3. `.agent/candidates.md` stays empty unless the closure gate raised one.

## Risks
- None open against F256. `R-0732` is resolved this round; the wider ledger's
  251 open findings belong to earlier features.
