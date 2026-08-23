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
R6 records the R5 verdict, rules the envelope widening as DECISION F022 D3, and
closes T001: `_safe_event_summary` carries the budget tick's whitelisted figures
for that ONE event kind, so every other kind's frame stays byte-identical and
the tick's numbers reach a client for the first time.

## Next Steps
1. R7 T002 the COST metric on fixture streams — the client type widening, the
   fill, the '~' prefix and tooltip, the thresholds and the no-limit variant.
2. R8 T003 the terminal reconciliation and the delta labelling.
3. R9 the integration gate, then closure.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R7 widens a CLOSED union, `RemedyMetricKey`, and a value type with nowhere to
  put a limit or a basis, both measured in the R3 inventory. That is a
  type-level change rather than an additive one, and R7 is sized for it.
- R7 is the first F022 round to touch `apps/ui/src`, where the shipped stylesheet
  and the design_reference sheet define different token sets; grep the shipped
  CSS, never the reference, when a token is claimed to exist.
