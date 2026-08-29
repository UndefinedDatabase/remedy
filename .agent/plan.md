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
| T002 decision core, subset apply, ledger, the door | done | rounds 6-15 |
| T003 partial truth on all three surfaces, R-0738 | done | rounds 16-19 |
| rejections rendered verbatim as repair findings | done | round 20 |
| that renderer reaches the builder prompt as a segment | done | round 21 |
| R-0747, and the inverse of the ledger export | done | round 22 |
| the stored decision selected, and forwarded by the loop | done | round 23 |
| R-0748, and the job-level caller supplies the ledger | open | this round |
| R-0745, the door's transitive import closure | open | not scheduled |
| the operator docs for `patch approve-hunks` | open | not scheduled |
| the integration gate round, then closure | open | not scheduled |

## Next Steps
1. This round retires R-0747's false sentence from the second file it reached,
   and wires `packages/orchestration/pingpong_job.py` — the one place holding
   the job — to read the task's decision and hand it to the loop. That
   completes the feature's FUNCTIONAL scope.
2. THE SOFT LIMIT IS ROUND 25 AND THE REMAINING WORK DOES NOT FIT IN IT.
   Outstanding: R-0745, the `docs/` operator description no round has yet been
   allowed a path for, the integration-gate round, and the two-round closure
   sequence. That is four to five rounds against one.
3. The session-6 handoff therefore carries the operator scope report operator
   amendment amend0827 rule 6 requires, with a proposal. It is a DOCUMENTED
   PROPOSAL and is never executed on the reviewer's own authority.
4. No pull request exists and none should be created before the closure
   sequence, which is where docs/agents/split_workflow.md rules it.

## Risks
- R-0745 is open against the write door's import closure and is unscheduled. It
  is not a blocker for the functional scope but it is a block condition at
  closure, so the scope report must name it explicitly.
