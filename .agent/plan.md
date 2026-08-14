# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0417. Open findings: forty-six — the thirty-two carried from F077, plus
R-0403 to R-0416 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R8 records the R7 gate, registers R-0415 and R-0416, persists DECISION F082 D4,
retires the two regions of `.agent/context.md` the R-0414 sweep left standing,
and pins T002's regression threshold and trailing median with a fourth golden
whose trailing values are not all equal.

## Next Steps
1. R9 — T003: the `stats bench` CLI, model-context recording, and a
   fake-provider bench run end to end.
2. R10 the integration gate, R11 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- `repair_rounds` is `None` at every row by construction (R2 Q7). The trend
  therefore has no repair-round series to regress on, and T003's report says so
  rather than printing a zero.
