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
R18 records the R17 verdict, registers finding R-0676 and the R-0371
recurrence, then builds the two artifacts closure cannot be authored without:
a fresh feature-scoped evidence bundle and a FRESH review zip. It builds no
product code; T001, T002 and T003 are complete and the Built State is current.

## Next Steps
1. R19 closure: the reviewer authors the STATUS line from the evidence job id,
   the package filename and the package SHA-256 that R18 produced, the worker
   commits it LAST with the README capability sync in the SAME commit and
   empties `.agent/candidates.md`, then creates the PR.

## Risks
- A failing zip build is a closure BLOCKER, never a thing to work around: the
  feature does not close without the package.
- The closure PR is created but NOT merged by the round that makes it: it merges
  at the NEXT feature's Open PR Gate, which preserves the operator's window.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured; R-0431, R-0413 and R-0533 are recorded and
  already paid for; R-0674, R-0675 and R-0676 are registered and repaired by
  none, their subjects being landed append-only text; and R-0445 is a standing
  defect of `docs/agents/integration_gate.md`, routed by the finding itself to
  a follow-up branch rather than to this one.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0403 is open and this package will show it: `.remedy-wt/` scratch is a large
  share of every review zip built on this machine. It routes to a paydown
  branch and is not an F022 defect.
