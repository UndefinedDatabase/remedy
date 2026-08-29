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
| landing the subset all-or-nothing | done | round 8, on `source_apply.py` |
| the seam tells the truth about a failed rollback | open | this round, R-0740 |
| the hunk-decision ledger in evidence | open | |
| the write-door command and its exposure | open | needs the door's effect ruled |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Repair R-0740: the apply seam's failure sentence is DERIVED from the
   applier's errors, so a rollback that did not finish is never reported as an
   unchanged repository, and the comments asserting the old absolute go with it.
2. Then the hunk-decision ledger — approved, rejected and pending hunks with the
   rejection reasons kept VERBATIM. It moves ahead of the write door because it
   is what the door's effect writes.
3. Then the write door, opened by a DECISION that first rules what its effect IS.
   `packages.orchestration.hunk_apply` imports `source_apply`, the first entry of
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py`, so a door
   importing the seam runs the applicator inside the HTTP handler and defeats the
   P3 contract by naming a module the list has not caught up to.
4. Then T003: rejection reasons quoted verbatim into the next repair prompt, and
   partial state rendered truthfully in viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard, so a new import reddens the
  branch tip unless it is ruled in the same commit.
- The subset builder refuses rather than shrinking a diff silently, and every
  later caller must keep that refusal rather than defaulting past it.
- R-0738 stays open and is T003's to repair.
