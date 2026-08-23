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
R17 records the R16 verdict, registers findings R-0674 and R-0675, repairs the
round map for a three-round closure, and writes the feature file's `## Built
State` section. It builds no product code: T001, T002 and T003 are complete and
the integration gate has passed.

## Next Steps
1. R18 the evidence job and a FRESH review zip, per
   docs/roadmap/STATUS_closure_protocol.md steps 1 and 2. A failing zip build is
   a closure BLOCKER, never a thing to work around.
2. R19 closure: the reviewer authors the STATUS line from the values only that
   zip produces, the worker commits it last with the README capability sync in
   the SAME commit, and creates the PR.

## Risks
- The closure PR is created but NOT merged by the round that makes it: it merges
  at the NEXT feature's Open PR Gate, which preserves the operator's window.
- Closure precondition 4 was never satisfiable at closure itself: the closure
  commit's allowed path set holds no feature file, so the Built State must land
  before the package. R17 is that round.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured; R-0431, R-0413 and R-0533 are recorded and
  already paid for; R-0674 and R-0675 are registered by this round and repaired
  by none, their subjects being landed append-only text; and R-0445 is a
  standing defect of `docs/agents/integration_gate.md`, routed by the finding
  itself to a follow-up branch rather than to this one.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
