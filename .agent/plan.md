# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 1 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| restart F033 from current main | done | round 1, DECISION F033 D1 |
| claim F033, book the F257 verdict, register R-0738 | done | round 1 |
| survey the hunk-identity surface | done | round 1, in the handback |
| the shared identity function and its tests | done | this round |
| wire it into the parser, bump DIFF_VIEW_VERSION | open | round 3 |
| rule the client's fallback id synthesis | open | round 3 |
| retire the diff-repair local hunk helper | open | round 4 |
| T002 approve_hunks, subset atomicity, ledger | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Round 3 wires `hunk_identity` into `packages/orchestration/diff_parser.py`,
   bumps `DIFF_VIEW_VERSION` to 2 and moves the tests that pin version 1.
2. Round 3 also rules the client fallback at `apps/ui/src/api/diffViewModel.ts`,
   which synthesises a positional id when the server sends an empty one.
3. Round 4 retires the local hunk helper in
   `packages/orchestration/diff_repair.py` onto the shared identity.

## Risks
- `packages/orchestration/diff_parser.py` is PURE and TOTAL by its own docstring
  and never raises on malformed input. The identity function must not change that.
- The client fallback means an empty server id becomes a POSITIONAL id on screen
  rather than an error, so a content-hash contract can be violated silently. It
  is ruled in round 3, not worked around here.
- The parked branch `feature/f033-hunk-approval` at `ed040812` holds a 574-line
  inventory taken at `32cde54e`. It is INPUT to be re-derived, never fact.
