# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 6 of this feature.

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
| rejections rendered verbatim as repair findings | done | round 20 |
| that renderer reaches the builder prompt as a segment | done | round 21 |
| R-0747, and the inverse of the ledger export | done | round 22 |
| the stored decision is selected and reaches the real loop | open | this round |
| the JOB-level caller in `pingpong_job.py` supplies it | open | next |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |
| the integration gate round, then closure | open | after the above |

## Next Steps
1. This round adds the reader that selects a task's latest recorded decision
   from `job.metadata`, gives `run_pingpong` the parameter it forwards, and
   proves through the REAL loop that a rejection reason reaches the composed
   prompt's segment manifest.
2. Then the last wiring step: `packages/orchestration/pingpong_job.py` holds the
   job at its `run_pingpong` call, so it reads the decision and passes it. That
   is the only remaining hop, and it is deliberately its own round because it
   touches the job runner.
3. Then R-0745, whose fix clause recommends a transitive-closure test over the
   write door's imports.
4. Then the closure sequence: `docs/` still owes an operator-facing description
   of `remedy patch approve-hunks`, and no round has had a `docs/` path yet. The
   integration gate runs before closure, per docs/agents/integration_gate.md.

## Risks
- Steps 2, 3 and 4 plus the two closure rounds exceed what the 25-round soft
  limit leaves. The scope report amend0827 rule 6 requires is now expected, and
  the session-6 handoff carries the proposal.
