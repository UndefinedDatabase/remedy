# Plan — F133 Provider trust score

## Goal
Make "which model earns which work" a rolling, queryable fact: per model and role, the pass quota,
the repair need, the format-error rate and the cost per pass, each with its window and sample size,
in one trust home; `remedy stats trust` shows it, and routing reads it only as a recommendation.

## Current Step
Round 3: register R-1429 to R-1431 and repair them; DECISION F133 D3; the clear leader and the
recommendation line of `remedy stats trust`.

## Next Steps
1. Round 4: the informational note "trust suggests otherwise" in `remedy job plan-show`, the
   one-home guard, the page completed, the end-to-end.
2. The closure sequence.

## Risks
- The model of most calls comes from the provider attempt, not a verified identity; the view says
  which figures rest on how many calls, and unattributed calls are counted, never guessed.
