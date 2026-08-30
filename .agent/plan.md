# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 2, round 6.

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
| the F040 closure candidate | done | round 1 |
| the F258 claim and the seam inventory | done | round 1 |
| T001 part 1 — schema v2, the provenance field | done | round 2 |
| T001 part 2 — the generator module, tier 1 | done | round 3 |
| T001 part 3 — wiring the closure protocol doc | done | round 4 |
| T002 consumed means executed | done | round 5 |
| T003 findings flow back | done | this round |

## Next Steps
1. This round books round 5's own verdict (`Gate: F258 R5`) into
   `.agent/live_review.md` first, per amend0827 rule 1.
2. `packages/orchestration/self_use_findings.py` reads a run's own `JobPlan`
   and answers every defect verbatim (job- and task-level `error` fields),
   never inventing wording, never registering anything itself. Wired into
   `STATUS_closure_protocol.md` precondition 6 and `self-use-track-v1.md`.
3. All three of F258's T-slices are now built against the feature file's own
   text. Next: the closure sequence — evidence job, fresh review zip, the
   STATUS line, the PR.

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- No closure candidate is open; `.agent/candidates.md` stays empty.
