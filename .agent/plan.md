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
R9 records the R8 verdict, registers R-0673, records the R-0672 recurrence and
ends the session cleanly. It builds nothing: T001 and T002 are complete, the
session's round budget is spent, and a verdict that lives only in a session is
a verdict that did not happen.

## Next Steps
1. R10 T003 — the terminal reconciliation, the delta labelling, the live wiring
   through `remedyApi.ts` and `RemedyShell.tsx`, and the fake-job end-to-end.
2. R11 the integration gate.
3. R12 closure.

## Risks
- Three F022 findings are open and all are Low: R-0671 wants one assertion in
  `costMetric.test.ts` pinning a negative spend as the limitless view; R-0672
  and its recurrence want the next DECISION on this ground to state a complete
  reversal; R-0673 is a reviewer-gate defect that has already been paid for.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md` and says so, which is a
  route rather than a fix.
