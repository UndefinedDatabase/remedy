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
| T003 the fold's shared home and its counts | done | round 18 |
| T003 the report line, R-0738's third surface | open | this round |
| R-0746, the module's stale public API list | open | this round |
| T003 rejection reasons quoted into the repair prompt | open | next |
| R-0738, resolvable once the report line is gated | open | after that |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. The report line. `packages/orchestration/run_report.py` holds no apply state
   at all, so `TaskOutcome` gains one with its counts, `build_report_sources`
   attaches it from `fold_task_apply_states`, and `_task_lines` renders the
   mixed case. A task with NO recorded apply state renders exactly as it does
   today — the golden reports in `tests/orchestration/test_run_report.py` are
   full-text fixtures and are the guard for that. R-0746 is fixed in the same
   round, because this is the round that gives the fold its second importer.
2. Then rejection reasons quoted VERBATIM into the next repair prompt, with the
   trace proof `docs/roadmap/features/T5_F033.md` calls acceptance material.
3. Then R-0738 is resolvable: viewer badge, tasks-card row and report line all
   tell a mixed apply state apart from a complete one.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has had a `docs/` path yet.

## Risks
- The report's task ids are truncated to eight characters while the fold keys on
  the full id, so the attach must not match on the truncated value.
