# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 2, round 5.

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
| T002 consumed means executed | done | this round |
| T003 findings flow back | open | |

## Next Steps
1. This round books round 4's own verdict (`Gate: F258 R4`) into
   `.agent/live_review.md` first, per amend0827 rule 1.
2. `packages/orchestration/self_use_runner.py` composes
   `plan_next_self_use_item` with `run_job` under a small `JobBudgets`
   (`max_provider_calls`, `max_cost_usd`), stopping at `JOB_COMPLETED` or
   `JOB_BLOCKED` — never calling `job_promote.promote_job`. T002 is now
   feature-complete against the feature file's own text, tested end to end
   including a real generate → plan → run cycle.
3. T003 is next: findings surfaced by a self-use run flow back into
   `.agent/live_review.md` under the normal ledger rules.

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- T003 still needs a concrete wiring point — likely the closure round itself,
  since that is where a self-use run's outcome is already recorded.
