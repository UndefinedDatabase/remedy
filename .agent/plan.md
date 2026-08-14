# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0418. Open findings: forty-seven — the thirty-two carried from F077, plus
R-0403 to R-0417 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R9 records the R8 gate, registers R-0417, retires the stale golden-count
sentence in the bench-history test docstring, and re-syncs the plan. T001 and
T002 are built and gated; T003 is the only slice left.

## Next Steps
1. R10 — T003: the `stats bench` CLI, model-context recording, and a
   fake-provider bench run end to end. Begin with an inspect-the-shape pass over
   `apps/cli/commands/stats_ledger_cmd.py` and the CLI registration path before
   authoring the change set — the ground is unknown and the planning contract
   sanctions a shrunken step for exactly that.
2. R11 the integration gate, R12 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- `repair_rounds` is `None` at every row by construction (R2 Q7). The trend has
  no repair-round series to regress on, and T003's report says so rather than
  printing a zero.
- Six of the last seven findings are reviewer-block defects, not worker
  defects. R-0417's standing staleness gate is the counter-measure; if R10 also
  registers one of this class, the block format itself needs re-planning.
