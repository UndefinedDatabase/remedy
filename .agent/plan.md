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
| R-0749 first instance, the loop docstring | landed | round 25 |
| the operator guide and its index rows | open | this round |
| R-0749 fourth instance, the renderer docstring | open | this round |
| the integration gate round | open | next |
| the closure sequence and its pull request | open | after the gate |
| R-0745, the door's transitive import closure | open | carried as a risk |

## Next Steps
1. This round books the round 25 PASS, ships the operator guide for
   `remedy patch approve-hunks` with its two `docs/README.md` index rows in the
   same commit, and retires the claim's fourth instance.
2. R-0749 stays OPEN until both of its instances are landed and the reviewer
   resolves it; the round after this one books that resolution alongside its own
   first commits, never in a round of its own.
3. Then the integration gate per docs/agents/integration_gate.md, then the
   closure sequence and its pull request.
4. R-0745 is Low and is not reachable from this feature's Acceptance. The
   closure protocol's precondition 1 admits a documented Medium/Low risk, so it
   is carried as one rather than blocking a feature that has met its Acceptance.

## Risks
- R-0745 stays OPEN at closure and the STATUS line therefore reads
  PASS_WITH_RISKS. Its fix recommends a transitive-closure guard test, which is
  a hardening task deserving its own round rather than a corner of a closure.
- The claim R-0747 opened has now been found in four files across five rounds.
  Its resolution predicate is worded over the CLAIM, so the reviewer resolves it
  only after reading the feature's modules rather than counting a string.
