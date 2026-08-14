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
R13 records the R12 gate, rules at DECISION F082 D8 that `intake.py` is inside
D7's exception and that T003b splits in two, and builds the WRITE half: a
gauntlet run records which model served which role in its own `run.json`, and a
role the runner cannot observe is recorded as absent rather than guessed.

## Next Steps
1. R14 — T003b the read half and the run: carry the models from
   `gauntlet_evidence.py::RunEvidence` into the bench record, which needs its
   own additive ruling; then the fake-provider bench run, clearing R11's Q6
   four blockers — no entry point, local-Ollama reach, a `time.monotonic()`
   call in `::run_order`, and history resolving to the real data root; and the
   Q7 pin for "the bench never runs implicitly".
2. R15 the integration gate, R16 closure.

## Risks
- "The bench never runs implicitly" is an ACCEPTANCE criterion that NO test
  pins (R11 Q7). It holds today only by absence: `append_bench_run` and
  `dry_run_from_order_set` have no caller under `apps/`, `packages/` or
  `scripts/`. An unpinned criterion found at closure is a closure blocker, so
  R14 pins it.
- The builder's model stays unobservable after R13, because making it visible
  means reaching into `orchestrator_loop.py::execute_dispatched_job`. Closure
  states that absence rather than implying three roles were recorded.
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- Reviewer-block defects, not worker defects, are the dominant finding class on
  this branch. No count is stated here because none has been taken; R-0417's
  staleness gate, R-0418's Fortschritt rule and R-0419's grep-every-writer
  rule are the counter-measures, and all three bind every block from here.
