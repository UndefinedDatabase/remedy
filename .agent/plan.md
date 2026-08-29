# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 6 closed at round 24; next is SESSION 7.

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
| T003 rejection to repair, rendered, wired, end to end | done | rounds 20-24 |
| THE FEATURE'S FUNCTIONAL SCOPE | complete | at round 24 |
| the operator docs for `patch approve-hunks` | open | session 7 |
| the integration gate round | open | session 7 |
| the closure sequence | open | session 7 |
| R-0745, the door's transitive import closure | open | PROPOSED to split |

## Next Steps
1. Session 7 books the round 24 PASS from `.agent/handoff.md` into
   `.agent/live_review.md` in the first commits of its first round.
2. THE SOFT LIMIT IS REACHED AT SESSION 7. The scope report operator amendment
   amend0827 rule 6 requires is written in `.agent/handoff.md`, with a proposal
   the operator decides on. Session 7 reads it BEFORE planning work.
3. The remaining closure obligations, in order: the `docs/` operator-facing
   description of `remedy patch approve-hunks`, which no round has yet been
   allowed a path for; then the integration gate per
   docs/agents/integration_gate.md; then the closure sequence and its PR.
4. R-0745 is open and unscheduled. The handoff proposes splitting it onto its
   own STATUS line so a feature that has met its Acceptance can close. That is a
   PROPOSAL and is never executed on the reviewer's own authority.

## Risks
- If R-0745 must be fixed inside F033, session 7 cannot also close the feature
  and the operator should expect an eighth session.
