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
R13 records the R12 verdict, registers the R-0533 recurrence, repairs the round
map and ends the session cleanly. It builds nothing: T003a is complete, the
server half of T003b is complete, the session's round budget is spent, and a
verdict that lives only in a session is a verdict that did not happen.

## Next Steps
1. R14 T003b-b — read `budget_final` into the dashboard type and render the
   terminal reconciliation with its delta label, per DECISION F022 D7.
2. R15 the integration gate.
3. R16 closure.

## Risks
- The delta R14 renders is a TRANSPORT statement, not arithmetic: both sides are
  the same quantity from the same producer, so a difference means frames were
  missed. A round that reads it as drift would reintroduce the fabricated
  honesty moment DECISION F022 D7 exists to prevent.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured; R-0431, R-0413 and R-0533 are reviewer-block
  defects already recorded and already paid for.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch. Its measured value is in the
  `R-0625` recurrence, not in this sentence.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
