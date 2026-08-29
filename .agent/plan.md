# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 3 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | closed round 5, DECISION F033 D3 |
| the approval decision core | done | round 6, 30 cases |
| the approved subset diff | done | round 7, 17 cases |
| landing the subset all-or-nothing | done | round 8 |
| the seam tells the truth about a failed rollback | done | round 9, R-0740 |
| the hunk-decision ledger | open | this round, plus R-0741 |
| the write-door command and its exposure | open | needs the door's effect ruled |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The hunk-decision ledger: the ordered record of every hunk in an attempt on
   TWO axes — the operator's decision and whether those bytes landed — kept
   apart because an approved hunk whose apply failed is neither landed nor
   rejected. Pure, and deliberately unable to import the applier. R-0741 repairs
   the last comment still asserting the absolute round 9 retired.
2. Then the write door, opened by a DECISION that first rules what its effect IS.
   `packages.orchestration.hunk_apply` imports `source_apply`, the first entry of
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py`, so a door
   importing the seam runs the applicator inside the HTTP handler and defeats the
   P3 contract by naming a module the list has not caught up to. The ledger is
   built to be what the door writes instead.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report's "partially approved (5/8 hunks)" line derived from the ledger, and
   partial state rendered truthfully in viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard, so a new import reddens the
  branch tip unless it is ruled in the same commit.
- `UI_EXPOSED_COMMANDS` is pinned at exactly two ids by `TestUiExposedCommands`,
  and exposure without dispatch answers 501.
- R-0738 stays open and is T003's to repair.
