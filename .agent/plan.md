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
R3 records the R2 verdict, repairs the round map that R2 shifted without
repairing, and takes the cost inventory. The inventory MEASURES three things in
the source rather than reading them off the feature file: every call site that
evaluates spent-vs-limits, the event kinds the ledger stream carries today on
both the Python and the TypeScript side, and what the metrics bar renders now.
It mints no id and builds nothing.

## Next Steps
1. R4 record R3 and rule the tick envelope as a DECISION: the payload's field
   set, the basis vocabulary and the no-client-arithmetic contract.
2. R5 T001 the tick emission, at the evaluation sites the inventory names.
3. R6 T002 the COST metric, R7 T003 the terminal reconciliation, then the
   integration gate and closure.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- The feature file states its preconditions as settled fact, which is the R-0612
  class. The inventory measures them instead, and reports any disagreement.
