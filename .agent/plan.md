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
R7 records the R6 verdict, registers R-0670, rules DECISION F022 D4, and lands
T002's LOGIC half: `apps/ui/src/api/costMetric.ts` turns one budget tick into
every render decision the COST metric needs — unit, denominator, fill,
threshold, estimate marker and tooltip — with vitest tests for each.

## Next Steps
1. R8 T002's RENDER half: the COST metric in `TopMetricsBar.tsx`, its CSS
   tokens, the `remedyApi.ts` wiring and the shell seam that feeds it the live
   tick, plus the ui_contracts source guard.
2. R9 T003 the terminal reconciliation and the delta labelling.
3. R10 the integration gate, then closure.

## Risks
- T002 is split across R7 and R8 because its logic half is testable under the
  node-environment vitest and its render half is not testable at all: the
  config collects `src/**/*.test.ts` only, so the component is gated by
  `tests/ui_contracts/` source contracts instead. Splitting keeps each round's
  evidence answerable by its own gates.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R8 is the round that touches the shipped stylesheet, where the design_reference
  sheet defines tokens the shipped one never adopted; grep the shipped CSS, never
  the reference, when a token is claimed to exist (R-0661). There is no warn
  token in the shipped sheet today.
