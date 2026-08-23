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
R11 rules the terminal reconciliation's source and builds nothing. The feature
file named "the stats endpoint", which does not exist, and the dashboard's
`token_usage` — the obvious substitute — is an estimate summed over a different
event population, so a delta against it would be fabricated. DECISION F022 D7
rules the run log's last budget tick as the authority and this round amends the
feature file to match. It also records the R10 verdict and the R-0625
recurrence.

## Next Steps
1. R12 T003b — the server's final-figure section and the client's terminal
   reconciliation with the delta label, built against DECISION F022 D7.
2. R13 the integration gate.
3. R14 closure.

## Risks
- T003b is now a TWO-SIDED slice: D7 puts a final-figure section on the server
  as well as the reconciliation on the client, so R12 is larger than T003a was
  and may need splitting at its own block.
- Open F022 findings, each with the round that owns it: R-0670 waits for the
  next round touching `packages/orchestration/ui_server.py` on its own account,
  which R12 will be; R-0672 and R-0625 want their next-DECISION and next-numeral
  clauses honoured, which DECISION F022 D7 and this round's ledger entry do.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
