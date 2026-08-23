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
R4 records the R3 verdict, carries a recurrence of the open finding R-0553 that
R3's own context slice landed, and rules the budget tick envelope as DECISION
F022 D1 — the emission site, the payload's field set, the basis vocabulary and
the no-client-arithmetic contract — on the ground the R3 inventory measured. It
mints no id and builds nothing.

## Next Steps
1. R5 T001 the tick emission in `should_stop`, with its backend tests, the
   humanize-catalog key and the catalog pin gated in the same commit.
2. R6 T002 the COST metric on fixture streams; R7 T003 the terminal
   reconciliation and the delta labelling.
3. R8 the integration gate, then closure.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- T002 widens a CLOSED union and a value type that has nowhere to put a limit or
  a basis, both measured in the R3 inventory. That is a type-level change, not an
  additive one, and R6 is sized for it.
