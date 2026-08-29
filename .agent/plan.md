# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 5 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| decision core · subset diff · all-or-nothing apply | done | rounds 6, 7, 8 |
| failed-rollback truth · ledger · the door's effect | done | rounds 9-11, D4 |
| the recorder takes the viewer's envelope | done | round 12 |
| one evidence-directory resolver for viewer and doors | done | round 13 |
| the CLI command and its handler | done | rounds 14, 15 |
| the write door's exposure and dispatch | done | round 15 |
| T003 the apply fold's partial truth, and the popover label | done | round 16 |
| T003 the task row's partial tile and status text | open | this round, R-0738 |
| T003 the report line | open | next |
| T003 rejection reasons quoted into the repair prompt | open | after that |
| R-0745, the door's transitive import closure | open | with the next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. R-0738's second surface: `apps/ui/src/components/panels/TaskChecklistCard.tsx`
   reads `applyStatus` beside the lifecycle state, so a partially applied task
   shows the blue filled check tile and a distinct status text instead of
   reading "Done". DECISION F033 D5 rules this the task node's partial
   treatment and `RemedyState` is NOT widened. R-0738 STAYS OPEN: one of the
   three surfaces its resolution names is still untouched.
2. Then the report line. `packages/orchestration/run_report.py` holds no apply
   state at all, so its `TaskOutcome` gains one and the fold moves to a home
   both readers may import. Only after that is R-0738 resolvable.
3. Then rejection reasons quoted VERBATIM into the next repair prompt, with the
   trace proof `docs/roadmap/features/T5_F033.md` calls acceptance material.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has been allowed a `docs/` path yet.

## Risks
- The apply fold has one consumer but three downstream surfaces; a value added on
  one side only renders as "Unknown", which is why the contract test pins both ends.
