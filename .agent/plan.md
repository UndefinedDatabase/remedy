# Plan — F133 Provider trust score

## Goal
Make "which model earns which work" a rolling, queryable fact: per model and role, the pass quota,
the repair need, the format-error rate and the cost per pass, each with its window and sample size,
in one trust home; `remedy stats trust` shows it, and routing reads it only as a recommendation.

## Current Step
Round 2: T002 and the trust view (DECISION F133 D2): `packages/orchestration/model_trust_score.py`,
its three settings, its goldens on a constructed history, and `remedy stats trust` with the prior
window's change.

## Next Steps
1. Round 3, the rest of T003: the recommendation line per role, the informational routing note, the
   per-tier summary, the one-home guard, the docs completed, the end-to-end.
2. The closure sequence.

## Risks
- The model of most calls comes from the provider attempt, not a verified identity; the view says
  which figures rest on how many calls, and unattributed calls are counted, never guessed.
