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
R8 records the R7 verdict, resolves R-0653, registers R-0671 and R-0672, rules
DECISION F022 D5, and closes T002 with the RENDER half: the coin glyph, the
formatted value, the estimate marker, the fill track and the threshold
treatment, pinned by fixture-stream goldens and a source contract.

## Next Steps
1. R9 T003 the terminal reconciliation, the delta labelling, the live wiring
   through `remedyApi.ts` and `RemedyShell.tsx`, and the fake-job end-to-end.
2. R10 the integration gate.
3. R11 closure.

## Risks
- T002 was split across R7 and R8 because its logic half is testable under the
  node-environment vitest and its render half is not: the config collects
  `src/**/*.test.ts` only, so the component is gated by a `tests/ui_contracts/`
  source contract instead. The live WIRING moved to R9 with T003, where the
  feature file already puts the end-to-end.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md` and says so, which is a
  route rather than a fix.
