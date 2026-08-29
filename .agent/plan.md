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
| T003 partial truth on all three surfaces, R-0738 | done | rounds 16-19 |
| R-0746, the module's public API list | done | round 19 |
| T003 rejection reasons rendered verbatim as repair findings | open | this round |
| T003 that renderer wired into the next builder round | open | next |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |
| the integration gate round, then closure | open | after the above |

## Next Steps
1. The rejection half of T003's loop, as a PURE renderer with no caller yet:
   `packages/orchestration/hunk_ledger.py` already holds each rejected hunk's
   reason VERBATIM and says in its own docstring that T003 quotes it into the
   next repair prompt. This round ships the function that does the quoting and
   the trace proof the feature file calls acceptance material — a reason with
   awkward bytes in it survives into the rendered text unchanged.
2. Then wiring: the renderer's output reaches the next builder round's prompt,
   and the two-round end-to-end the feature's Acceptance asks for.
3. Then R-0745, whose fix clause recommends a transitive-closure test over the
   write door's imports.
4. Then the closure sequence: `docs/` still owes an operator-facing description
   of `remedy patch approve-hunks`, and no round has had a `docs/` path yet. The
   integration gate runs before closure, per docs/agents/integration_gate.md.

## Risks
- A new module under `packages/orchestration/` is swept by repo-wide guards that
  name no path, so this round gates the two sweeps as well as its own tests.
