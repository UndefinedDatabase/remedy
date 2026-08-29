# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 7 of this feature, running past the
amend0827 rule 6 soft limit under the scope report that limit required.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001, T002 and T003 | done | rounds 1-24 |
| THE FEATURE'S FUNCTIONAL SCOPE | complete | at round 24 |
| R-0749, both instances landed | done | rounds 25 and 26 |
| the operator guide and its index rows | done | round 26 |
| the integration gate | open | this round |
| the closure sequence and its pull request | open | after the gate |
| R-0745, the door's transitive import closure | open | carried as a risk |

## Next Steps
1. This round books the round 26 PASS and the `Done: R-0749` resolution, then
   runs the integration gate of docs/agents/integration_gate.md: the full suite
   on this branch and at the merge base `bd8d9529`, compared and attributed.
2. Only this round's gate entry may carry a "full suite" claim. A reproducible
   branch-only failure coupled to feature code is a BLOCKER and buys its own
   reviewer-gated repair round rather than being fixed inside this one.
3. Then the closure sequence per docs/roadmap/STATUS_closure_protocol.md: the
   feature file's Built State, the evidence job, the review zip, the STATUS line
   and the pull request, which is NOT merged in this session.
4. R-0745 is Low and is not reachable from this feature's Acceptance. The
   closure protocol's precondition 1 admits a documented Medium/Low risk, so it
   is carried as one and the STATUS line reads PASS_WITH_RISKS.

## Risks
- The base worktree lacks build artifacts the suite needs. Parity is restored by
  COPY with symlinks preserved, and every base-only failure is attributed by
  direct evidence whether or not the parity claim holds.
