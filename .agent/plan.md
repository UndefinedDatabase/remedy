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
R10 is T003a, the live wiring. It records the R9 verdict and the R-0644
recurrence, repairs the round map, rules DECISION F022 D6, and then carries the
latest budget tick from the stream's one ingest point through the runner view
and the shell into the metrics bar — the step that gives `costMetricOf`, correct
since R7 and drawn since R8, its first production caller. It also pins R-0671's
missing assertion.

## Next Steps
1. R11 T003b — the terminal reconciliation, the delta labelling and the
   fake-job end-to-end, opening with the DECISION that rules where the ledger's
   final figure is read from.
2. R12 the integration gate.
3. R13 closure.

## Risks
- The feature file names "the stats endpoint" as the source of the ledger figure
  for the terminal reconciliation, and no such endpoint exists among the job
  endpoints `ui_server.py` dispatches. R11 opens by ruling that source as a
  DECISION rather than by building against a name.
- Open F022 findings, each with the round that owns it: R-0670 waits for the
  next round touching `packages/orchestration/ui_server.py` on its own account;
  R-0672 and its recurrence want a path-by-path reversal, which DECISION F022 D6
  carries; R-0673 wants a whole-file absence run at the base first, which G12
  does; R-0644's recurrence is the correction this round appends.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
