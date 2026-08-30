# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 3, round 8.

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
| the dedicated integration-gate round | done | round 7 |
| precondition 6 — plan + run the queue's next item for real | open | this round |
| closure sequence (preconditions 1,3,4,5; evidence job; zip; STATUS+README; PR) | open | next round |

## Next Steps
1. This round books round 7's own verdict (`Gate: F258 R7`) into
   `.agent/live_review.md` first, per amend0827 rule 1.
2. Run `packages.orchestration.self_use_runner.run_next_self_use_item` for
   real against the shipped queue's next pending item, in an isolated
   `REMEDY_DATA_DIR`, recording the raw `JobPlan` and
   `packages.orchestration.self_use_findings.describe_self_use_run_defects`
   output under `.agent/gate_f258_closure/`. No finding is registered this
   round — the reviewer authors any `- R-XXXX` text next round from the
   real recorded output (STATUS_closure_protocol.md precondition 6;
   T5_F258.md T003).
3. `scripts/self_use_queue.json` stays byte-unchanged this round —
   `consumed_by` is set only in the final closure commit (Algorithm step 5).

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- No closure candidate is open; `.agent/candidates.md` stays empty.
