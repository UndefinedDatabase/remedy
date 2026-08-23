# Plan — F022 Live cost ticker

Branch: feature/f022-live-cost-ticker, cut from `main` at `c34ef32b`, the merge
commit of pull request #211. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
Money is visible while it burns, honestly: the MetricsBar's COST metric renders
from budget tick events {spent, limit, basis} — bar fill against the limit, a
'~' prefix plus tooltip whenever the basis is estimated, warn colour at ≥85% —
and the final figure reconciles with the ledger at terminal. DONE when the
ticker tracks a fixture stream exactly, basis changes flip the prefix and
tooltip live, the warn threshold triggers per tokens, limitless jobs render the
spent-only variant with no fake denominator, and the terminal reconciliation
displays the ledger figure with any delta labelled.

## Current Step
R2 records the R1 verdict on disk and nothing else. R1 PASSED, and a verdict
that exists only in a session dies with it (finding R-0571), so this round
appends the gate entry and carries the reviewer's dated correction to one
sentence R1 landed inside R-0669. It mints no id and builds nothing.

## Next Steps
1. R3 the cost inventory: where the budget guard evaluates spent-vs-limits, what
   the Part E event vocabulary already defines, and what MetricsBar renders
   today — each MEASURED in the source rather than read off the feature file.
2. R4 record R3 and rule the tick envelope as a DECISION: the payload's field
   set, the basis vocabulary and the no-client-arithmetic contract.
3. R5 onward the built work, in the T001/T002/T003 order the feature file's Task
   slicing names.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
