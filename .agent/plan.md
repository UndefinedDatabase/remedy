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
R16 records the R15 verdict, registers the R-0445 recurrence, repairs the round
map and ends the session cleanly. It builds nothing: T001, T002 and T003 are
complete, the integration gate has passed, and a verdict that lives only in a
session is a verdict that did not happen.

## Next Steps
1. R17 closure, per docs/roadmap/STATUS_closure_protocol.md — the evidence job
   and a FRESH review zip are mandatory, the reviewer authors the STATUS line,
   and the worker commits it last and creates the PR.

## Risks
- The closure PR is created but NOT merged by the round that makes it: it merges
  at the NEXT feature's Open PR Gate, which is what preserves the operator's
  manual-review window.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured, and R-0672 gained a third instance at R14;
  R-0431, R-0413, R-0533 and R-0445 are already recorded and already paid for.
- R-0445 is a standing defect of `docs/agents/integration_gate.md` itself, not
  of this branch: its repair is routed to a follow-up branch by the finding, and
  performing it from here would be scope drift into a process doc.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
