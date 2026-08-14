# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0420. Open findings: forty-nine — the thirty-two carried from F077, plus
R-0403 to R-0419 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R12 records the R11 gate, registers the reviewer-block defect R-0419, corrects
the false role-binding claim this file itself carried, and rules at DECISION
F082 D7 that T003b may add one additive `models` key to the gauntlet's evidence
body. It writes no code.

## Next Steps
1. R13 — T003b: the `models` key on `gauntlet_runner.py::_evidence_body` under
   D7's three conditions, model context carried into the bench record, and a
   fake-provider bench run end to end. R11's Q6 names four blockers for that
   run — no entry point, local-Ollama reach, a `time.monotonic()` call in
   `::run_order`, and history resolving to the real data root — and the round
   must clear or route around each before claiming an end-to-end run.
2. R14 the integration gate, R15 closure.

## Risks
- "The bench never runs implicitly" is an ACCEPTANCE criterion that NO test
  pins (R11 Q7). It holds today only by absence: `append_bench_run` and
  `dry_run_from_order_set` have no caller under `apps/`, `packages/` or
  `scripts/`. An unpinned criterion found at closure is a closure blocker, so
  R13 or R14 pins it.
- T003b needs the D7 exception to the ADDITIVE constraint. If the gauntlet's
  seven test files cannot stay green unmodified, the change is not additive
  and the round stops rather than widening.
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- Reviewer-block defects, not worker defects, are the dominant finding class on
  this branch. No count is stated here because none has been taken; R-0417's
  staleness gate, R-0418's Fortschritt rule and R-0419's grep-every-writer
  rule are the counter-measures, and all three bind every block from here.
