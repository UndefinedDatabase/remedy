# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 2, round 7.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 self-replenishing queue | done | rounds 2-4 |
| T002 consumed means executed | done | round 5 |
| T003 findings flow back | done | round 6 |
| the dedicated integration-gate round | done | this round |
| closure sequence | open | next round |

## Next Steps
1. This round books round 6's own verdict (`Gate: F258 R6`) into
   `.agent/live_review.md` first, per amend0827 rule 1.
2. The dedicated integration-gate round (planner_reviewer_prompt.md §3 tier
   3) runs the full suite twice — branch and base, per
   docs/agents/integration_gate.md — and records raw evidence under
   `.agent/gate_f258_r7/`. The reviewer's own verdict on this round's
   readings decides whether closure preconditions are met.
3. Closure (docs/roadmap/STATUS_closure_protocol.md): preconditions 1-6,
   evidence job, fresh review zip, the STATUS line, the PR — the reviewer's
   own next design, not more T-slice work.

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- No closure candidate is open; `.agent/candidates.md` stays empty.
