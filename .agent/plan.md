# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 2 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| restart, claim, register R-0738 | done | round 1, DECISION F033 D1 |
| the shared identity function and its tests | done | round 2, 10 tests |
| wire the parser, bump DIFF_VIEW_VERSION to 2 | done | round 3, 50 tests |
| rule the client's invented id | done | round 4, DECISION F033 D2 |
| repair the two stale production comments | done | this round, R-0739 |
| retire the diff-repair local hunk helper | dropped | this round, DECISION F033 D3 — no such helper exists |
| T001 stable ids, viewer v2, consolidation | done | closed by this round |
| T002 approve_hunks, subset atomicity, ledger | open | next |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Open T002 on the seam this round's handback inventories: the validation core
   for `approve_hunks` — ids exist in that attempt's diff, approved and rejected
   are disjoint, a rejection carries a reason — as a pure function with tests,
   before any write door or applicator work.
2. Then the subset apply itself, all-or-nothing over the approved set, built on
   `packages/orchestration/source_apply.py`.
3. Then the write-door command and the hunk-decision ledger in evidence.

## Risks
- `packages/orchestration/repo_applicator.py` applies nothing by design, so the
  subset seam is new work rather than a parameter on something existing.
- The write door's import guard is an EQUALITY guard, so T002 widens it in the
  same commit that adds an import, or the branch tip ships red.
- R-0738 stays open and is T003's to repair.
