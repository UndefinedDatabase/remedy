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
| R-0747, and the inverse of the ledger export | open | this round |
| the loop SUPPLIES a stored ledger, and the two-round end-to-end | open | next |
| R-0745, the door's transitive import closure | open | next door work |
| the operator docs for `patch approve-hunks` | open | closure sequence |
| the integration gate round, then closure | open | after the above |

## Next Steps
1. This round repairs R-0747 and ships `import_hunk_ledger`, the inverse of
   `export_hunk_ledger`. A decision IS stored — on `job.metadata` under
   `hunk_decisions`, persisted by `save_job` at the write door — but its rows
   are mappings keyed `id`, so nothing could rebuild a ledger from them.
2. Then the supply: read that key in the run loop and pass the rebuilt ledger to
   `compose_builder_prompt`, which has taken the parameter since round 21. That
   step also carries the two-round end-to-end the Acceptance asks for.
3. Then R-0745, whose fix clause recommends a transitive-closure test over the
   write door's imports.
4. Then the closure sequence: `docs/` still owes an operator-facing description
   of `remedy patch approve-hunks`, and no round has had a `docs/` path yet. The
   integration gate runs before closure, per docs/agents/integration_gate.md.

## Risks
- Steps 2, 3 and 4 are more rounds than the 25-round soft limit leaves. The
  scope report operator amendment amend0827 rule 6 requires is now likely.
