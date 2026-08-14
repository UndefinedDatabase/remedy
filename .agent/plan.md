# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0419. Open findings: forty-eight — the thirty-two carried from F077, plus
R-0403 to R-0418 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R11 records the R10 gate, registers the reviewer-block defect R-0418, retires
the scope sentence R10's own change made half-stale, and answers the seven
T003b inventory questions in the feature file's Built State. It writes no code.

## Next Steps
1. R12 — T003b: model-context recording and a fake-provider bench run end to
   end, ordered against R11's answers rather than against a guess.
2. R13 the integration gate, R14 closure.

## Risks
- T003b's shape is UNKNOWN until R11's Q1-Q4 are answered. No `model_context`
  symbol exists in any bench module today, and only one role is bound to a
  model. If Q4 answers (c), T003b cannot be built additively and the feature
  file's Design bullet needs an operator-visible amendment.
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- Two acceptance criteria may be unpinned by any test (R11 Q7). An unpinned
  criterion discovered at closure is a closure blocker, which is why Q7 is
  asked three rounds early.
- Seven of the last nine findings are reviewer-block defects, not worker
  defects. R-0417's standing staleness gate and R-0418's Fortschritt rule are
  the counter-measures; both now bind every block.
