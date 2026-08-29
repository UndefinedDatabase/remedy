# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 7 of this feature, which is the last under
the amend0827 rule 6 soft limit; the scope report it requires is written.

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
| R-0749, the retired claim's third instance | open | this round |
| the operator guide for `patch approve-hunks` | open | next round |
| the integration gate round | open | after the guide |
| the closure sequence and its pull request | open | after the gate |
| R-0745, the door's transitive import closure | open | carried as a risk |

## Next Steps
1. This round books the round 24 PASS and the `Done: R-0748` resolution, and
   retires the same false claim from the third file it reached.
2. Then the `docs/` round: an operator guide for `remedy patch approve-hunks`
   under `docs/guides/`, registered in the `docs/README.md` index in the same
   commit, gated with `python3 -m pytest tests/docs/ -q` beside the canary.
3. Then the integration gate per docs/agents/integration_gate.md, then the
   closure sequence and its pull request.
4. R-0745 is Low and is not reachable from this feature's Acceptance. The
   closure protocol's precondition 1 admits a documented Medium/Low risk, so it
   is carried as one rather than blocking a feature that has met its Acceptance.

## Risks
- R-0745 stays OPEN at closure and the STATUS line therefore reads
  PASS_WITH_RISKS. Its fix recommends a transitive-closure guard test, which is
  a hardening task deserving its own round rather than a corner of a closure.
