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
R5 records the R4 verdict, splits T001 across two rounds in the round map, rules
the tick's writer as DECISION F022 D2, and builds the first half: one budget
tick per safe-point evaluation in `should_stop`, the matching humanize-catalog
key in the SAME commit, and a backend test file pinning the payload's honesty,
the cadence and the ping-pong job-id shape.

## Next Steps
1. R6 the second half of T001 — the SSE envelope, which drops `metadata` today
   and therefore carries none of the tick's figures to any client.
2. R7 T002 the COST metric on fixture streams; R8 T003 the terminal
   reconciliation and the delta labelling.
3. R9 the integration gate, then closure.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R6 widens `_safe_event_summary`, whose key set is pinned exactly and whose
  frames are a golden byte stream, both in `tests/ui_server/test_sse_stream.py`.
  The widening is conditional on the event kind or both readings go red.
- R7 widens a CLOSED union and a value type with nowhere to put a limit or a
  basis, both measured in the R3 inventory. That is a type-level change.
