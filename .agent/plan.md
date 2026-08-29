# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 4 of this feature.

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
| T003 partial apply truth, and its first surface | open | this round, R-0738 |
| T003 the node glyph and the report line | open | next |
| T003 rejection reasons quoted into the repair prompt | open | after that |
| R-0745, the door's transitive import closure | open | with the next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. R-0738's truth half: the apply fold in `ui_server._task_truth_maps` becomes an
   AGREEMENT test with a distinct `partial` state, taking the shape of the proof
   fold three lines above it, and the detail popover gains the matching label in
   the SAME commit — the fold alone would render the new state as "Unknown".
   R-0738 STAYS OPEN: its resolution names three surfaces and this reaches one.
2. Then the remaining two surfaces R-0738 names — the task-node glyph and the
   report line — and only then is R-0738 resolvable.
3. Then rejection reasons quoted VERBATIM into the next repair prompt, with the
   trace proof the feature file calls acceptance material.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has been allowed a `docs/` path yet.

## Risks
- The apply fold has one consumer but three downstream surfaces; a value added on
  one side only renders as "Unknown", which is why the contract test pins both ends.
