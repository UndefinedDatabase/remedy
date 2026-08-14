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
R10 records the R9 gate, splits T003 in two as DECISION F082 D5, retires this
branch's largest stale sentence, and builds T003a: the `remedy stats bench`
read view over the append-only history, with its catalog entry, its
registration and its own test file. T001 and T002 are built and gated.

## Next Steps
1. R11 — T003b: model-context recording per run and a fake-provider bench run
   end to end. The field no `run.json` carries yet is the risk; begin with an
   inspect-the-shape pass over the gauntlet's run writer before authoring a
   change set.
2. R12 the integration gate, R13 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- `repair_rounds` is `None` at every row by construction (R2 Q7). The trend has
  no repair-round series to regress on, and T003a says so in one sentence
  rather than rendering a column of placeholders.
- Six of the last seven findings are reviewer-block defects, not worker
  defects. R-0417's standing staleness gate is the counter-measure; R9 ran it
  for the first time and it caught six stale sentences, so it works.
