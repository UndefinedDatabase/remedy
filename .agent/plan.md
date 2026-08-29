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
| one evidence-directory resolver, the CLI door, the write door | done | 13-15 |
| T003 the fold's partial truth, the popover label | done | round 16 |
| T003 the tasks-card partial tile and status text | done | round 17, D5 |
| T003 the fold gets a shared home and counts | open | this round |
| T003 the report line | open | next |
| T003 rejection reasons quoted into the repair prompt | open | after that |
| R-0738, resolvable once the report line lands | open | R-0738 |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. The apply fold moves out of `packages/orchestration/ui_server.py` into
   `packages/orchestration/proof_chain.py`, where `ProofChange` and its
   `apply_state` are defined, and gains the APPLIED and TOTAL counts R-0738's
   fix asks for. `_task_truth_maps` keeps its name and signature and delegates,
   so the cockpit's own tests stay untouched. The seam guard in
   `tests/ui_contracts/test_apply_state_partial.py` follows the literals to
   their new file: it walks them by AST, so leaving it behind would EMPTY its
   expected set rather than redden it.
2. Then the report line. `packages/orchestration/run_report.py` holds no apply
   state at all, so `TaskOutcome` gains one and `_task_lines` renders the mixed
   case with its counts. Only then is R-0738 resolvable on all three surfaces.
3. Then rejection reasons quoted VERBATIM into the next repair prompt, with the
   trace proof `docs/roadmap/features/T5_F033.md` calls acceptance material.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has had a `docs/` path yet.

## Risks
- The fold's labels are read by an AST walk in a test that names the file they
  live in; the move and that test's re-pointing must land in one round.
