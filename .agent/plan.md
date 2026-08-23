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
R12 is the server half of T003b. It adds one read-only section to the dashboard
payload carrying the ledger's last budget tick, which DECISION F022 D7 rules as
the authority for the terminal reconciliation, and it needs no new endpoint
because the dashboard builder already loads every tick the job emitted. It also
repairs R-0670, whose fix waited for a round that touches `ui_server.py` on its
own account, and records the R11 verdict with two recurrences.

## Next Steps
1. R13 T003b-b — the client half: read `budget_final` into the dashboard type
   and render the terminal reconciliation with its delta label.
2. R14 the integration gate.
3. R15 closure.

## Risks
- The delta R13 renders is a TRANSPORT statement, not arithmetic: both sides are
  the same quantity from the same producer, so a difference means frames were
  missed. A round that reads it as drift would reintroduce the fabricated
  honesty moment DECISION F022 D7 exists to prevent.
- Open F022 findings after this round: R-0672 and R-0625 want their
  next-DECISION and next-numeral clauses honoured; R-0431 and R-0413, recorded
  this round, are reviewer-block defects already paid for.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
